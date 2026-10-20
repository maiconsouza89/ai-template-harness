#!/usr/bin/env python3
"""Cria ou atualiza o arquivo de progresso de implementação a partir do PRD.

Uso: python3 progress.py docs/PRD.md [--progress docs/prd_progress.json] [--dry-run]

Lê o PRD com o validate.py (e para se ele tiver erro), deriva nome, prioridade, onda e
dependências de cada RF a partir da seção 8 e grava o JSON seguindo o contrato de merge de
references/progresso.md: estado de execução (status, cycles, failure_reason, report_path,
started_at, completed_at) é preservado para RF que continua no PRD; RF que sumiu vira
status "removed" e nunca é apagado; RF "removed" que volta recomeça como "pending".
A escrita é atômica (.tmp e rename). Só biblioteca padrão.
"""
import datetime
import json
import os
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import analyze  # noqa: E402

SCHEMA_VERSION = 1
RUNTIME_FIELDS = ("status", "cycles", "failure_reason", "report_path", "started_at", "completed_at")
PRD_FIELDS = ("name", "priority", "wave", "dependencies")
FIELD_ORDER = ("name", "priority", "wave", "dependencies", "status", "cycles", "failure_reason",
               "report_path", "started_at", "updated_at", "completed_at")


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ordered(entry):
    out = {k: entry.get(k) for k in FIELD_ORDER}
    out.update({k: v for k, v in entry.items() if k not in FIELD_ORDER})
    return out


def fresh_entry(feat, now):
    return ordered({
        **feat,
        "status": "pending",
        "cycles": 0,
        "failure_reason": None,
        "report_path": None,
        "started_at": None,
        "updated_at": now,
        "completed_at": None,
    })


def features_from_prd(data):
    g = data["graph"]
    feats = {}
    for rid in g["order"]:
        feats[rid] = {
            "name": g["names"][rid],
            "priority": g["priority"][rid],
            "wave": g["wave_of"][rid],
            "dependencies": list(g["deps"].get(rid, [])),
        }
    return feats


def merge(existing, feats, prd_path, now):
    """Aplica o contrato de merge. Retorna (documento, relatório)."""
    report = {"added": [], "refreshed": [], "unchanged": [], "resurrected": [], "removed": [], "already_removed": []}
    old = existing.get("features", {}) if existing else {}
    doc = {
        "schema_version": SCHEMA_VERSION,
        "prd_path": prd_path,
        "generated_at": existing.get("generated_at", now) if existing else now,
        "features": {},
    }
    ids = sorted(set(old) | set(feats), key=lambda x: (x[:2], int(x[3:]) if x[3:].isdigit() else 0, x))
    for rid in ids:
        if rid in feats and rid in old:
            entry = dict(old[rid])
            if entry.get("status") == "removed":
                entry = fresh_entry(feats[rid], now)
                entry.update({k: v for k, v in old[rid].items() if k not in FIELD_ORDER})
                report["resurrected"].append(rid)
            else:
                changed = any(entry.get(k) != feats[rid][k] for k in PRD_FIELDS)
                entry.update(feats[rid])
                if changed:
                    entry["updated_at"] = now
                    report["refreshed"].append(rid)
                else:
                    report["unchanged"].append(rid)
            doc["features"][rid] = ordered(entry)
        elif rid in feats:
            doc["features"][rid] = fresh_entry(feats[rid], now)
            report["added"].append(rid)
        else:
            entry = dict(old[rid])
            if entry.get("status") != "removed":
                entry["status"] = "removed"
                entry["updated_at"] = now
                report["removed"].append(rid)
            else:
                report["already_removed"].append(rid)
            doc["features"][rid] = ordered(entry)
    return doc, report


def main(argv):
    args = list(argv[1:])
    progress_arg, dry = None, False
    if "--progress" in args:
        i = args.index("--progress")
        progress_arg = Path(args[i + 1]) if i + 1 < len(args) else None
        del args[i : i + 2]
    if "--dry-run" in args:
        dry = True
        args.remove("--dry-run")
    if len(args) != 1:
        print(__doc__)
        return 2
    prd_path = Path(args[0])
    if not prd_path.is_file():
        print(f"arquivo não encontrado: {prd_path}")
        return 2
    rep, data = analyze(prd_path.read_text(encoding="utf-8"))
    if rep.errors:
        for e in rep.errors:
            print(f"erro: {e}")
        print("progresso não gerado: o PRD precisa passar no validate.py sem erro")
        return 1
    feats = features_from_prd(data)
    progress_path = progress_arg or (prd_path.parent / "prd_progress.json")
    now = now_iso()

    existing, notes = None, []
    if progress_path.exists():
        try:
            existing = json.loads(progress_path.read_text(encoding="utf-8"))
            if not isinstance(existing, dict) or not isinstance(existing.get("features"), dict):
                raise ValueError("estrutura inesperada")
        except (ValueError, json.JSONDecodeError) as exc:
            broken = progress_path.with_name(f"{progress_path.name}.broken-{int(time.time())}")
            if not dry:
                os.replace(progress_path, broken)
            notes.append(f"arquivo de progresso anterior não era JSON válido ({exc}); preservado em {broken}")
            existing = None
        if existing and int(existing.get("schema_version", 1)) > SCHEMA_VERSION:
            print(f"erro: {progress_path} tem schema_version {existing['schema_version']}, mais novo que {SCHEMA_VERSION}; nada foi escrito")
            return 1

    doc, report = merge(existing, feats, str(prd_path), now)

    if not dry:
        tmp = progress_path.with_name(progress_path.name + ".tmp")
        tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, progress_path)
        check = json.loads(progress_path.read_text(encoding="utf-8"))
        missing = [rid for rid in feats if rid not in check.get("features", {})]
        if missing:
            print(f"erro: {progress_path} gravado sem {', '.join(missing)}")
            return 1

    for n in notes:
        print(f"aviso: {n}")
    verb = "simulação" if dry else ("criado" if existing is None else "atualizado")
    counts = {}
    for e in doc["features"].values():
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    print(f"{progress_path}: {verb}, {len(doc['features'])} RF(s) [" + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())) + "]")
    for key, label in (("added", "novos"), ("refreshed", "atualizados pelo PRD"), ("resurrected", "reativados"),
                       ("removed", "marcados removed"), ("unchanged", "sem mudança")):
        if report[key]:
            print(f"  {label}: {', '.join(report[key])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
