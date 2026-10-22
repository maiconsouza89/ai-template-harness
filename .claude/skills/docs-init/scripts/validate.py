#!/usr/bin/env python3
"""Valida a documentação em docs/.

Uso: python3 validate.py [--root docs]

Checa frontmatter, links relativos, numeração de ADRs e FDDs, índice de cada pasta e marcas de
lacuna. Para PRDs aplica as checagens de conteúdo de prd_checks.py (seções, RF-NNN, contratos,
tabela de dependências) e, para o roadmap, confere que a seção "Ordem de execução" bate com o que a
tabela de cada PRD produz e que todo RF-NNN citado existe em algum PRD.
Sai com código 1 se houver erros; avisos não falham. Sem dependências externas.
"""

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prd_checks  # noqa: E402

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "assets" / "templates"
# Tipos cujos títulos H2 precisam ser os do template. PRD é checado por prd_checks (com ordem).
TEMPLATE_SECTION_TYPES = ("roadmap",)

TYPED_FOLDERS = ["product", "architecture", "adr", "features", "runbooks", "guides"]
IGNORED_FOLDERS = {"templates", "_intake"}
IGNORED_FILES = {"readme.md", "glossary.md"}

STATUS_BY_TYPE = {
    "adr": {"proposed", "accepted", "deprecated", "superseded"},
    "prd": {"draft", "review", "approved", "archived"},
    "hld": {"draft", "review", "approved", "archived"},
    "fdd": {"draft", "review", "approved", "implemented"},
    "roadmap": {"active", "archived"},
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ADR_NAME_RE = re.compile(r"^(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
FDD_NAME_RE = re.compile(r"^fdd-(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
GAP_RE = re.compile(r"\[A CONFIRMAR")
HYPOTHESIS = "(hipótese)"


def parse_frontmatter(text):
    """Parser simples: chave: valor, listas em colchetes, comentários após '#'. Retorna dict ou None."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        value = strip_comment(raw.strip())
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [unquote(v.strip()) for v in inner.split(",") if v.strip()] if inner else []
        else:
            data[key] = unquote(value)
    return None


def strip_comment(value):
    in_quote = None
    for i, ch in enumerate(value):
        if ch in ("'", '"'):
            in_quote = None if in_quote == ch else (in_quote or ch)
        elif ch == "#" and in_quote is None and (i == 0 or value[i - 1] in " \t"):
            return value[:i].rstrip()
    return value


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def as_list(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [v for v in value if v]
    return [value]


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.gaps = 0
        self.hypotheses = 0

    def error(self, path, message):
        self.errors.append(f"{path}: {message}")

    def warning(self, path, message):
        self.warnings.append(f"{path}: {message}")


def iter_documents(root):
    for folder in TYPED_FOLDERS:
        base = root / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            if any(part in IGNORED_FOLDERS for part in path.relative_to(root).parts):
                continue
            if path.name.lower() in IGNORED_FILES:
                continue
            yield path


def check_frontmatter(path, rel, text, report):
    fm = parse_frontmatter(text)
    if fm is None:
        report.error(rel, "sem frontmatter YAML (bloco entre '---' no início do arquivo)")
        return None
    doc_type = fm.get("type", "")
    for key in ("title", "type", "status"):
        if not fm.get(key):
            report.error(rel, f"frontmatter sem a chave obrigatória '{key}'")
    date_key = "updated" if doc_type == "roadmap" and "date" not in fm else "date"
    date = fm.get(date_key)
    if not date:
        report.error(rel, f"frontmatter sem a chave obrigatória '{date_key}'")
    elif not DATE_RE.match(str(date)):
        report.error(rel, f"'{date_key}' deve ser ISO AAAA-MM-DD, encontrado '{date}'")
    if doc_type:
        allowed = STATUS_BY_TYPE.get(doc_type)
        if allowed is None:
            report.error(rel, f"type '{doc_type}' desconhecido; use {', '.join(sorted(STATUS_BY_TYPE))}")
        elif fm.get("status") and fm["status"] not in allowed:
            report.error(
                rel,
                f"status '{fm['status']}' não é válido para type '{doc_type}'; use {', '.join(sorted(allowed))}",
            )
    return fm


def check_adrs(root, docs, report):
    numbers = {}
    for path, fm in docs:
        if path.parent != root / "adr":
            continue
        rel = path.relative_to(root).as_posix()
        match = ADR_NAME_RE.match(path.name)
        if not match:
            report.error(rel, "nome de ADR deve seguir NNNN-titulo-em-kebab.md")
            continue
        number = match.group(1)
        numbers.setdefault(number, []).append(rel)
        if fm is None:
            continue
        if str(fm.get("number", "")).zfill(4) != number:
            report.error(rel, f"'number' no frontmatter ({fm.get('number')}) não bate com o nome do arquivo ({number})")
        if fm.get("status") == "superseded" and not as_list(fm.get("superseded_by")):
            report.error(rel, "ADR superseded precisa de 'superseded_by' preenchido")
    for number, paths in sorted(numbers.items()):
        if len(paths) > 1:
            report.error("adr/", f"número {number} duplicado: {', '.join(paths)}")
    if numbers:
        expected = range(1, max(int(n) for n in numbers) + 1)
        missing = [f"{n:04d}" for n in expected if f"{n:04d}" not in numbers]
        if missing:
            report.error("adr/", f"lacuna na numeração dos ADRs: faltam {', '.join(missing)}")


def check_fdds(root, docs, report):
    for path, fm in docs:
        if path.parent != root / "features":
            continue
        rel = path.relative_to(root).as_posix()
        match = FDD_NAME_RE.match(path.name)
        if not match:
            report.error(rel, "nome de FDD deve seguir fdd-NNN-titulo-em-kebab.md")
            continue
        if fm is not None and str(fm.get("number", "")).zfill(3) != match.group(1):
            report.error(rel, f"'number' no frontmatter ({fm.get('number')}) não bate com o nome do arquivo ({match.group(1)})")


def check_links(root, path, text, report):
    rel = path.relative_to(root).as_posix()
    for line_no, line in enumerate(text.splitlines(), 1):
        for match in LINK_RE.finditer(line):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if "://" in target:
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                report.error(rel, f"linha {line_no}: link para arquivo inexistente '{target}'")


def check_gaps(root, path, text, report):
    rel = path.relative_to(root).as_posix()
    for line_no, line in enumerate(text.splitlines(), 1):
        for _ in GAP_RE.finditer(line):
            report.gaps += 1
            report.warning(rel, f"linha {line_no}: {line.strip()}")


def check_index(root, path, report):
    """Avisa se o README.md da pasta do documento não tem link para ele."""
    index = path.parent / "README.md"
    rel = path.relative_to(root).as_posix()
    if not index.exists():
        report.warning(rel, f"pasta sem índice README.md")
        return
    if f"({path.name})" not in index.read_text(encoding="utf-8"):
        report.warning(rel, f"não está no índice {index.relative_to(root).as_posix()}")


def template_sections(doc_type):
    tpl = TEMPLATES_DIR / f"{doc_type}.md"
    if not tpl.is_file():
        return []
    return re.findall(r"^## (.+)$", prd_checks.strip_frontmatter(tpl.read_text(encoding="utf-8")), re.MULTILINE)


def check_template_sections(path, text, doc_type, report):
    """Erro quando um título H2 do template do tipo falta ou foi renomeado."""
    rel = path
    titles = set(re.findall(r"^## (.+)$", text, re.MULTILINE))
    for expected in template_sections(doc_type):
        if expected.strip() not in titles:
            report.error(rel, f"seção do template '{doc_type}' ausente ou renomeada: '## {expected}'")


def check_prd(rel, text, report):
    rep, _ = prd_checks.analyze(text)
    for item in rep.errors:
        report.error(rel, item)
    for item in rep.warnings:
        report.warning(rel, item)
    report.hypotheses += rep.hypotheses


def check_roadmap_order(root, path, text, report):
    """Confere a seção Ordem de execução com os PRDs ligados; devolve os RF citados no roadmap."""
    rel = path.relative_to(root).as_posix()

    def load_prd(prd_path):
        return prd_path.read_text(encoding="utf-8") if prd_path.is_file() else None

    errors, warnings, cited = prd_checks.check_roadmap_order(text, path, load_prd)
    for item in errors:
        report.error(rel, item)
    for item in warnings:
        report.warning(rel, item)
    return cited


def check_roadmap(root, path, text, report):
    rel = path.relative_to(root).as_posix()
    section = None
    header = None
    for line_no, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip()
            header = None
            continue
        if section not in ("Agora", "Próximo") or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if "Docs" not in header:
            continue
        idx = header.index("Docs")
        docs = cells[idx] if idx < len(cells) else ""
        if not docs:
            name = cells[0] if cells else "?"
            report.warning(rel, f"linha {line_no}: item '{name}' em {section} sem documento na coluna Docs")


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida a documentação em docs/.")
    parser.add_argument("--root", default="docs", help="pasta raiz da documentação (padrão: docs)")
    args = parser.parse_args()
    root = Path(args.root)
    report = Report()

    if not root.is_dir():
        print(f"erro: pasta '{root}' não encontrada", file=sys.stderr)
        return 1

    docs = []
    known_rfs = set()
    cited_rfs = {}
    for path in iter_documents(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        fm = check_frontmatter(path, rel, text, report)
        docs.append((path, fm))
        check_links(root, path, text, report)
        check_gaps(root, path, text, report)
        check_index(root, path, report)
        doc_type = fm.get("type") if fm is not None else None
        if doc_type in TEMPLATE_SECTION_TYPES:
            check_template_sections(rel, text, doc_type, report)
        if doc_type == "prd":
            check_prd(rel, text, report)
            known_rfs.update(prd_checks.RF_ID.findall(text))
        elif doc_type == "roadmap":
            check_roadmap(root, path, text, report)
            cited_rfs[rel] = check_roadmap_order(root, path, text, report)
        elif doc_type == "fdd":
            cited_rfs[rel] = set(prd_checks.RF_ID.findall(text))
    for rel, cited in cited_rfs.items():
        for rid in sorted(cited - known_rfs):
            if rid != "RF-000":
                report.error(rel, f"cita {rid}, que não existe em nenhum PRD de product/")

    check_adrs(root, docs, report)
    check_fdds(root, docs, report)

    print("Erros:")
    for item in report.errors:
        print(f"  - {item}")
    if not report.errors:
        print("  nenhum")
    print("Avisos:")
    for item in report.warnings:
        print(f"  - {item}")
    if not report.warnings:
        print("  nenhum")
    print(
        f"Resumo: {len(docs)} documento(s), {len(report.errors)} erro(s), "
        f"{len(report.warnings)} aviso(s), {report.gaps} ocorrência(s) de [A CONFIRMAR], "
        f"{report.hypotheses} de {HYPOTHESIS}"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
