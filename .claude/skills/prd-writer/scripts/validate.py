#!/usr/bin/env python3
"""Valida a estrutura de um PRD gerado pela skill prd-writer e, opcionalmente, exporta JSON.

Uso: python3 validate.py docs/PRD.md [--json docs/PRD.json]

Checa o que é mecânico: as 9 seções na ordem do template, placeholders esquecidos, requisitos
funcionais completos (descrição, Capacidades, Experiência), contratos Consome/Fornece fechados
nos dois lados, tabela de dependências em ordem topológica sem ciclo nem referência órfã,
ondas calculadas a partir da tabela, Mermaid igual à tabela, histórias e critérios de aceitação
para todo RF e critérios de integração para todo Consome. Sai com código 1 quando há erro.
Avisos não derrubam. Só biblioteca padrão.

O módulo também expõe `analyze(text)` para o progress.py reaproveitar a leitura do PRD.
"""
import json
import re
import sys
from pathlib import Path

SECTIONS = [
    "1. Resumo executivo",
    "2. Problema e oportunidade",
    "3. Público-alvo",
    "4. Objetivos e métricas",
    "5. Histórias de usuário",
    "6. Requisitos funcionais",
    "7. Fora de escopo",
    "8. Mapa de dependências e paralelismo",
    "9. Critérios de aceitação",
]
NFR_REQUIRED = ["Performance", "Disponibilidade"]
RF_BLOCKS = [
    "Consome",
    "Fornece",
    "Escopo mínimo",
    "Adições de escopo completo",
    "Capacidades",
    "Experiência",
    "Tratamento de erros",
]
RF_ID = re.compile(r"RF-\d{3}")
STACK_WORDS = re.compile(
    r"\b(postgres\w*|mysql|mongodb|redis|kafka|rabbitmq|react|vue|angular|django|rails|next\.?js|"
    r"spring|node\.?js|typescript|python|java|golang|kotlin|docker|kubernetes|aws|azure|gcp|"
    r"grpc|graphql|rest api|microsservi\w+|monólito|monolito|prisma|whisper)\b",
    re.IGNORECASE,
)


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def norm_id(raw):
    """RF001, RF-001, rf001 -> RF-001."""
    m = re.fullmatch(r"([A-Za-z]+)-?(\d+)", raw.strip())
    if not m:
        return raw.strip()
    prefix, num = m.group(1).upper(), m.group(2)
    return f"{prefix}-{int(num):03d}" if prefix == "RF" else f"{prefix}-{int(num)}"


def split_h2(text):
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def split_h3(body):
    parts = re.split(r"^### (.+)$", body, flags=re.MULTILINE)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def bullets(block):
    out = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("- "):
            out.append(s[2:].strip())
        elif out and s and not s.startswith(("**", "#", "|", "```")) and line.startswith(("  ", "\t")):
            out[-1] += " " + s
    return out


def bullets_under(body, label):
    m = re.search(rf"^{re.escape(label)}\n((?:- .*\n?)+)", body, re.MULTILINE)
    return bullets(m.group(1)) if m else []


def bold_groups(body):
    """Grupos '**Título**' seguidos de bullets -> [(título, [itens])]."""
    groups = []
    for m in re.finditer(r"^\*\*([^*\n]+)\*\*\s*\n((?:- .*\n?)+)", body, re.MULTILINE):
        groups.append((m.group(1).strip().rstrip("."), bullets(m.group(2))))
    return groups


def rf_blocks(body):
    """Divide uma seção em blocos '### RF-NNN Nome' -> [(id, nome, corpo)]. IDs fora do padrão viram None."""
    out = []
    for head, b in split_h3(body):
        m = re.match(r"(RF-\d{3})\s+(.+)", head)
        out.append((m.group(1) if m else None, m.group(2).strip() if m else head, b))
    return out


def parse_labeled(body):
    """Blocos '**Rótulo:**' com bullets dentro de um RF -> dict rótulo -> itens, mais a ordem."""
    found, order = {}, []
    for m in re.finditer(r"^\*\*([^*\n]+?):\*\*[ \t]*\n((?:[ \t]*- .*\n?)+)", body, re.MULTILINE):
        label = m.group(1).strip()
        found[label] = bullets(m.group(2))
        order.append(label)
    return found, order


# ---------- leitura ----------

def read_requirements(body, rep):
    reqs = []
    seen = set()
    for rid, name, b in rf_blocks(body):
        if not rid:
            rep.err(f"cabeçalho fora do padrão '### RF-NNN Nome' em Requisitos funcionais: '{name[:50]}'")
            continue
        if rid in seen:
            rep.err(f"{rid} duplicado em Requisitos funcionais")
        seen.add(rid)
        lines = [l for l in b.splitlines() if l.strip()]
        desc = lines[0].strip() if lines and not lines[0].startswith(("**", "-", "|", "#")) else ""
        if not desc:
            rep.err(f"{rid} sem descrição em uma frase antes dos blocos")
        blocks, order = parse_labeled(b)
        for label in order:
            if label not in RF_BLOCKS:
                rep.warn(f"{rid}: bloco '{label}' não é um dos blocos do template")
        known = [l for l in order if l in RF_BLOCKS]
        if known != sorted(known, key=RF_BLOCKS.index):
            rep.warn(f"{rid}: blocos fora da ordem do template ({' > '.join(RF_BLOCKS)})")
        for label in ("Capacidades", "Experiência"):
            if not blocks.get(label):
                rep.err(f"{rid} sem bloco '**{label}:**' com itens")
        if blocks.get("Adições de escopo completo") and not blocks.get("Escopo mínimo"):
            rep.err(f"{rid} tem 'Adições de escopo completo' sem 'Escopo mínimo'")
        consumes = []
        for item in blocks.get("Consome", []):
            m = re.match(r"(RF-\d{3})\s*:\s*(.+)", item)
            if not m:
                rep.err(f"{rid} Consome: item fora do padrão '- RF-NNN: dado' ('{item[:40]}')")
                continue
            consumes.append({"from": m.group(1), "data": m.group(2).strip()})
        provides = []
        for item in blocks.get("Fornece", []):
            m = re.search(r"\((?:usad[oa]s?|consumid[oa]s?) por ([^)]+)\)\s*$", item)
            if not m:
                rep.err(f"{rid} Fornece: item sem '(usado por RF-NNN, ...)' no fim ('{item[:40]}')")
                continue
            users = [norm_id(x) for x in RF_ID.findall(m.group(1))]
            provides.append({"data": item[: m.start()].strip(), "used_by": users})
        for item in blocks.get("Tratamento de erros", []):
            if ":" not in item:
                rep.warn(f"{rid} Tratamento de erros: '{item[:40]}' sem 'cenário: o que o usuário vê'")
        reqs.append({
            "id": rid,
            "name": name,
            "description": desc,
            "consumes": consumes,
            "provides": provides,
            "core_scope": blocks.get("Escopo mínimo", []),
            "full_scope_additions": blocks.get("Adições de escopo completo", []),
            "capabilities": blocks.get("Capacidades", []),
            "experience": blocks.get("Experiência", []),
            "error_handling": blocks.get("Tratamento de erros", []),
        })
    if not reqs:
        rep.err("nenhum requisito funcional (### RF-NNN Nome) na seção 6")
    nums = [int(r["id"][3:]) for r in reqs]
    if nums != sorted(nums):
        rep.warn("RFs fora de ordem numérica na seção 6")
    if nums and nums != list(range(nums[0], nums[0] + len(nums))):
        rep.warn("numeração de RF com lacuna: aceitável só em revisão, com o RF removido listado em Fora de escopo")
    if len(reqs) > 20:
        rep.warn(f"{len(reqs)} RFs; acima de 20 há capacidades a consolidar ou mais de uma entrega")
    elif 0 < len(reqs) < 3:
        rep.warn(f"{len(reqs)} RFs; abaixo de 3 os requisitos podem estar agrupados demais")
    return reqs


def read_table(body, rep):
    rows = []
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not re.fullmatch(r"RF-\d{3}", cells[0]):
            continue
        rid, name, prio, deps_raw = cells[0], cells[1], cells[2], cells[3]
        prio_n = int(prio) if re.fullmatch(r"[123]", prio) else None
        if prio_n is None:
            rep.err(f"{rid}: prioridade '{prio}' na tabela não é 1, 2 ou 3")
        deps = []
        if deps_raw.strip().lower() not in ("nenhum", "nenhuma", "none", "-", ""):
            tokens = [t.strip() for t in deps_raw.split(",") if t.strip()]
            for t in tokens:
                if re.fullmatch(r"RF-?\d+", t):
                    deps.append(norm_id(t))
                else:
                    rep.err(f"{rid}: 'Depende de' contém '{t}', que não é um RF-NNN")
        rows.append({"id": rid, "name": name, "priority": prio_n, "dependencies": deps})
    if not rows:
        rep.err("seção 8 sem tabela '| # | Requisito | Prioridade | Depende de |' com linhas RF-NNN")
    return rows


def read_foundation(body):
    for head, b in split_h3(body):
        if head.startswith("Requisitos de fundação"):
            items = []
            for item in bullets(b):
                m = re.match(r"\*\*(RF-\d{3})\s*([^*]*)\*\*\s*:?\s*(.*)", item)
                if m:
                    items.append({"id": m.group(1), "name": m.group(2).strip(), "contribution": m.group(3).strip()})
                else:
                    items.append({"id": None, "name": item[:40], "contribution": ""})
            return items
    return None


def read_waves(body):
    waves = {}
    for m in re.finditer(r"^- \*\*Onda (\d+)\*\*\s*:\s*(.+)$", body, re.MULTILINE):
        waves[int(m.group(1))] = [norm_id(x) for x in re.findall(r"RF-?\d{3}", m.group(2))]
    return waves


def read_mermaid(body, rep):
    m = re.search(r"```mermaid\n(.*?)```", body, re.DOTALL)
    if not m:
        rep.err("seção 8 sem bloco ```mermaid")
        return "", set(), []
    mer = m.group(1)
    if not re.search(r"^\s*(graph|flowchart)\s+TD\b", mer, re.MULTILINE):
        rep.err("bloco mermaid deve começar com 'graph TD'")
    node_re = r"([A-Za-z]+-?\d+)(?:\[[^\]]*\]|\([^)]*\)|\{[^}]*\})?"
    nodes, edges = set(), []
    for line in mer.splitlines():
        line = line.strip()
        if not line or line.startswith(("graph", "flowchart", "%%")):
            continue
        em = re.match(rf"{node_re}\s*--+>\s*(?:\|[^|]*\|\s*)?{node_re}", line)
        if em:
            a, b = norm_id(em.group(1)), norm_id(em.group(2))
            edges.append((a, b))
            nodes.update([a, b])
            continue
        nm = re.match(node_re + r"\s*$", line)
        if nm:
            nodes.add(norm_id(nm.group(1)))
    return mer.strip(), nodes, edges


def read_external(body, rep, rf_set):
    out = []
    for head, b in split_h3(body):
        if head.startswith("Dependências externas"):
            for item in bullets(b):
                m = re.match(r"\*\*([^*]+)\*\*\s*:?\s*(.*)", item)
                title, desc = (m.group(1).strip(), m.group(2).strip()) if m else (item[:40], item)
                blocks = [norm_id(x) for x in RF_ID.findall(desc)]
                for rid in blocks:
                    if rid not in rf_set:
                        rep.err(f"dependência externa '{title}' cita {rid}, que não existe")
                if not blocks:
                    rep.warn(f"dependência externa '{title}' não diz que RF ela trava '(trava RF-NNN)'")
                out.append({"title": title, "description": re.sub(r"\s*\((?:trava|bloqueia)[^)]*\)\s*$", "", desc), "blocks": blocks})
    return out


# ---------- grafo ----------

def topo_canonical(ids, deps):
    """Ordem topológica com desempate pelo menor ID. Retorna None se houver ciclo."""
    pending = set(ids)
    done, order = set(), []
    while pending:
        ready = sorted((i for i in pending if set(deps.get(i, [])) <= done), key=lambda x: int(x[3:]))
        if not ready:
            return None
        nxt = ready[0]
        order.append(nxt)
        done.add(nxt)
        pending.remove(nxt)
    return order


def compute_waves(order, deps):
    wave = {}
    for rid in order:
        wave[rid] = 1 + max((wave[d] for d in deps.get(rid, []) if d in wave), default=0)
    return wave


def critical_path(order, deps):
    best = {}
    for rid in order:
        preds = [d for d in deps.get(rid, []) if d in best]
        if preds:
            p = max(preds, key=lambda d: len(best[d]))
            best[rid] = best[p] + [rid]
        else:
            best[rid] = [rid]
    return max(best.values(), key=len) if best else []


# ---------- checagens ----------

def check_header(text, rep):
    if not re.search(r"^# PRD: \S", text, re.MULTILINE):
        rep.err("título deve ser '# PRD: <nome do sistema>'")
    for field in ("Versão:", "Data:", "Responsável:"):
        if not re.search(rf"^{field} \S", text, re.MULTILINE):
            rep.err(f"cabeçalho sem '{field} ...'")
    m = re.search(r"^Data: (\S+)", text, re.MULTILINE)
    if m and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", m.group(1)):
        rep.err(f"Data '{m.group(1)}' não está em AAAA-MM-DD")


def check_sections(sections, rep):
    titles = [t for t, _ in sections]
    for s in SECTIONS:
        if s not in titles:
            rep.err(f"seção obrigatória ausente: '## {s}'")
    present = [s for s in SECTIONS if s in titles]
    if [t for t in titles if t in SECTIONS] != present:
        rep.err("seções fora da ordem do template")
    for t in titles:
        if t not in SECTIONS:
            rep.err(f"seção fora do template: '## {t}' (o PRD tem exatamente 9 seções)")


PLACEHOLDER_PREFIXES = (
    "nome", "descrição", "uma frase", "critério", "item", "impacto", "característica", "limite",
    "dado", "fluxo", "cenário", "meta", "métrica", "objetivo", "categoria", "verbo", "papel", "ação",
    "resultado", "capacidade", "estado", "título", "quem entrega", "o que", "como ", "2 a 3", "ex:",
    "omita", "inclua", "regra", "outro", "público", "perfil", "passo", "mensagem", "efeito",
)


def template_placeholders():
    tpl = Path(__file__).resolve().parent.parent / "assets" / "template.md"
    if not tpl.is_file():
        return set()
    return set(re.findall(r"\[([^\]\n]{3,})\]", tpl.read_text(encoding="utf-8")))


def check_placeholders(text, rep):
    """Só o que veio do template conta como placeholder: colchetes em mensagens ("Olá [nome]") passam."""
    body = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    known = template_placeholders()
    for m in re.finditer(r"\[([^\]\n]{3,})\](?!\()", body):
        inner = m.group(1)
        low = inner.strip().lower()
        if inner in known or low.startswith(PLACEHOLDER_PREFIXES) and (" " in low or inner in known):
            rep.err(f"placeholder não preenchido: [{inner[:40]}]")
    if re.search(r"^Data: AAAA-MM-DD", text, re.MULTILINE):
        rep.err("data do cabeçalho ainda é AAAA-MM-DD")


def check_problem(body, rep):
    subs = dict(split_h3(body))
    pains = bold_groups(subs.get("O problema", ""))
    if "O problema" not in subs or not pains:
        rep.err("seção 2 sem '### O problema' com categorias em negrito e bullets")
    elif not (3 <= len(pains) <= 5):
        rep.warn(f"{len(pains)} categorias de dor; o orçamento é 3 a 5")
    for title, items in pains:
        if not any(re.search(r"\d", i) for i in items):
            rep.warn(f"dor '{title[:40]}' sem nenhum número de impacto")
    opp = bullets(subs.get("A oportunidade", ""))
    if "A oportunidade" not in subs or not opp:
        rep.err("seção 2 sem '### A oportunidade' com bullets")
    elif pains and len(opp) < len(pains):
        rep.warn("oportunidade com menos itens que categorias de dor: toda dor precisa de resposta")
    return pains, opp


def check_audience(body, rep):
    subs = dict(split_h3(body))
    profiles = bold_groups(subs.get("Usuários primários", ""))
    if not profiles:
        rep.err("seção 3 sem '### Usuários primários' com perfis em negrito e bullets")
    for name, items in profiles:
        if len(items) < 2:
            rep.warn(f"perfil '{name[:30]}' com menos de 2 características")
    behav = bullets(subs.get("Perfil comportamental", ""))
    if len(profiles) == 1 and "Perfil comportamental" in subs:
        rep.warn("'Perfil comportamental' com um perfil só: omita, o perfil já diz tudo")
    if len(profiles) > 1 and not behav:
        rep.warn("mais de um perfil sem 'Perfil comportamental' com o que é comum a todos")
    return profiles, behav


def check_objectives(body, rep):
    subs = dict(split_h3(body))
    goals = []
    rows = [l for l in subs.get("Objetivos de produto", "").splitlines() if l.startswith("|")]
    for r in rows[2:]:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if not any(cells):
            continue
        if len(cells) < 3 or any(not c for c in cells[:3]):
            rep.err(f"objetivo incompleto (objetivo, métrica, meta): {r.strip()[:60]}")
            continue
        if not re.search(r"\d", cells[2]):
            rep.err(f"meta sem número: '{cells[2][:50]}'")
        goals.append({"objective": cells[0], "metric": cells[1], "target": cells[2]})
    if not goals:
        rep.err("seção 4 sem tabela de objetivos com linhas")
    elif not (3 <= len(goals) <= 5):
        rep.warn(f"{len(goals)} objetivos; o orçamento é 3 a 5")
    nfr_body = subs.get("Requisitos não funcionais", "")
    nfr = []
    for m in re.finditer(r"^([A-ZÁÉÍÓÚÂÊÔÃÕ][^\n*|#-]{2,60})\n((?:- .*\n?)+)", nfr_body, re.MULTILINE):
        nfr.append({"category": m.group(1).strip(), "items": bullets(m.group(2))})
    cats = {n["category"] for n in nfr}
    for cat in NFR_REQUIRED:
        if cat not in cats:
            rep.err(f"requisitos não funcionais sem '{cat}' com pelo menos uma meta")
        elif not any(re.search(r"\d", i) for n in nfr if n["category"] == cat for i in n["items"]):
            rep.err(f"requisitos não funcionais: '{cat}' sem meta numérica")
    return goals, nfr


def check_stories(body, rep, rf_set):
    stories = {}
    for rid, name, b in rf_blocks(body):
        if not rid:
            rep.err(f"cabeçalho fora do padrão '### RF-NNN Nome' em Histórias: '{name[:50]}'")
            continue
        items = bullets(b)
        if not items:
            rep.err(f"{rid} sem histórias (bullets) na seção 5")
        for s in items:
            if not re.match(r"Como ", s):
                rep.warn(f"{rid} história fora do padrão 'Como <papel>, quero ... para ...': '{s[:40]}'")
        stories[rid] = items
    for rid in rf_set - set(stories):
        rep.err(f"{rid} está na seção 6 mas não tem histórias na seção 5")
    for rid in set(stories) - rf_set:
        rep.err(f"{rid} tem histórias na seção 5 mas não existe na seção 6")
    return stories


def check_contracts(reqs, rep):
    by_id = {r["id"]: r for r in reqs}
    for r in reqs:
        for c in r["consumes"]:
            src = by_id.get(c["from"])
            if not src:
                rep.err(f"{r['id']} consome de {c['from']}, que não existe")
            elif c["from"] == r["id"]:
                rep.err(f"{r['id']} consome de si mesmo")
            elif not any(r["id"] in p["used_by"] for p in src["provides"]):
                rep.err(f"{r['id']} consome de {c['from']}, mas o Fornece de {c['from']} não lista '(usado por {r['id']})'")
        for p in r["provides"]:
            for u in p["used_by"]:
                tgt = by_id.get(u)
                if not tgt:
                    rep.err(f"{r['id']} Fornece cita {u}, que não existe")
                elif not any(c["from"] == r["id"] for c in tgt["consumes"]):
                    rep.err(f"{r['id']} Fornece diz '(usado por {u})', mas {u} não tem '- {r['id']}:' em Consome")
        if re.search(r"\b(autentica|sess[aã]o|login|token)\w*", " ".join(c["data"] for c in r["consumes"]), re.IGNORECASE):
            rep.warn(f"{r['id']} Consome cita autenticação ou sessão: autenticação é dependência de infraestrutura, só na tabela")


def check_graph(sec8, reqs, rep):
    rf_ids = [r["id"] for r in reqs]
    rf_set = set(rf_ids)
    rows = read_table(sec8, rep)
    table_ids = [r["id"] for r in rows]
    for rid in table_ids:
        if table_ids.count(rid) > 1:
            rep.err(f"{rid} aparece mais de uma vez na tabela de dependências")
    for rid in rf_set - set(table_ids):
        rep.err(f"{rid} está na seção 6 mas não na tabela de dependências")
    for rid in set(table_ids) - rf_set:
        rep.err(f"{rid} está na tabela de dependências mas não na seção 6")
    deps = {r["id"]: r["dependencies"] for r in rows}
    prio = {r["id"]: r["priority"] for r in rows}
    names = {r["id"]: r["name"] for r in rows}
    for rid, ds in deps.items():
        for d in ds:
            if d not in set(table_ids):
                rep.err(f"{rid} depende de {d}, que não está na tabela")
            if d == rid:
                rep.err(f"{rid} depende de si mesmo")
        if len(set(ds)) != len(ds):
            rep.err(f"{rid} repete uma dependência")
        if len(ds) >= 4:
            rep.warn(f"{rid} com {len(ds)} dependências: confira se cada uma é real, não 'bom fazer antes'")
    valid_ids = [i for i in table_ids if i in rf_set]
    deps_valid = {i: [d for d in deps[i] if d in set(table_ids)] for i in valid_ids}
    order = topo_canonical(valid_ids, deps_valid)
    result = {"rows": rows, "order": order, "waves": {}, "critical": [], "foundation": None, "mermaid": "", "external": []}
    if order is None:
        rep.err("ciclo na tabela de dependências: dois requisitos são um só ou um deles precisa ser dividido")
        return result
    # ordem da tabela: dependência sempre em linha acima; desempate pelo menor ID
    pos = {rid: i for i, rid in enumerate(table_ids)}
    for rid, ds in deps_valid.items():
        for d in ds:
            if pos.get(d, -1) > pos[rid]:
                rep.err(f"{rid} depende de {d}, que aparece abaixo na tabela (ordem topológica quebrada)")
    if valid_ids != order:
        rep.err(f"ordem da tabela deve ser topológica com desempate pelo menor ID: {', '.join(order)}")
    # Consome é subconjunto de Depende de
    for r in reqs:
        for c in r["consumes"]:
            if c["from"] not in deps.get(r["id"], []):
                rep.err(f"{r['id']} consome de {c['from']} mas a tabela não lista {c['from']} em 'Depende de'")
    # prioridade herda para trás
    for rid, ds in deps_valid.items():
        for d in ds:
            if prio.get(d) and prio.get(rid) and prio[d] > prio[rid]:
                rep.err(f"{rid} (prioridade {prio[rid]}) depende de {d} (prioridade {prio[d]}): a prioridade de {d} precisa subir")
    # só dependências diretas
    def reach(start):
        seen, stack = set(), list(deps_valid.get(start, []))
        while stack:
            x = stack.pop()
            if x not in seen:
                seen.add(x)
                stack.extend(deps_valid.get(x, []))
        return seen
    consumed = {(c["from"], r["id"]) for r in reqs for c in r["consumes"]}
    for rid, ds in deps_valid.items():
        for d in ds:
            if (d, rid) not in consumed and any(d in reach(o) for o in ds if o != d):
                rep.warn(f"{rid} depende de {d}, que já é alcançável por outra dependência e não está em Consome (aresta transitiva)")
    # fundação
    foundation = read_foundation(sec8)
    has_note = bool(re.search(r"^\*\*Nota:\*\*", sec8, re.MULTILINE))
    if foundation is not None:
        f_ids = [f["id"] for f in foundation]
        for f in foundation:
            if not f["id"]:
                rep.err(f"fundação: item fora do padrão '- **RF-NNN Nome**: contribuição' ('{f['name']}')")
            elif f["id"] not in rf_set:
                rep.err(f"fundação cita {f['id']}, que não existe")
            elif not f["contribution"]:
                rep.warn(f"fundação: {f['id']} sem dizer o que contribui para a base")
        known = [i for i in f_ids if i in pos]
        if known != sorted(known, key=lambda i: pos[i]):
            rep.err("requisitos de fundação fora da ordem da tabela")
        if not has_note:
            rep.err("há requisitos de fundação, mas falta a '**Nota:**' nas ondas sobre fundação em sequência")
    elif has_note:
        rep.err("há '**Nota:**' sobre fundação nas ondas, mas não há '### Requisitos de fundação'")
    # ondas
    expected = compute_waves(order, deps_valid)
    waves = read_waves(sec8)
    if not waves:
        rep.err("seção 8 sem '### Ondas de execução' com linhas '- **Onda N**: RF-...'")
    else:
        listed = [rid for w in sorted(waves) for rid in waves[w]]
        for rid in listed:
            if listed.count(rid) > 1:
                rep.err(f"{rid} aparece em mais de uma onda")
        for rid in rf_set - set(listed):
            rep.err(f"{rid} não está em nenhuma onda")
        for rid in set(listed) - rf_set:
            rep.err(f"onda cita {rid}, que não existe")
        for w in sorted(set(expected.values()) | set(waves)):
            exp = sorted((i for i in expected if expected[i] == w), key=lambda i: (prio.get(i) or 9, int(i[3:])))
            got = waves.get(w, [])
            if set(exp) != set(got):
                rep.err(f"Onda {w} deveria ter {', '.join(exp) or 'nada'}; tem {', '.join(got) or 'nada'}")
            elif exp != got:
                rep.err(f"Onda {w}: ordem deve ser prioridade crescente e depois ID: {', '.join(exp)}")
    result["waves"] = {w: sorted((i for i in expected if expected[i] == w), key=lambda i: (prio.get(i) or 9, int(i[3:]))) for w in set(expected.values())}
    # caminho crítico
    cp = critical_path(order, deps_valid)
    result["critical"] = cp
    cm = re.search(r"^Caminho crítico:\s*(.+)$", sec8, re.MULTILINE)
    if not cm:
        rep.err("seção 8 sem linha 'Caminho crítico: RF-... → RF-... (N ondas)'")
    else:
        n = re.search(r"\((\d+) ondas?\)", cm.group(1))
        if n and int(n.group(1)) != len(cp):
            rep.err(f"caminho crítico diz {n.group(1)} ondas, mas a cadeia mais longa tem {len(cp)} ({' → '.join(cp)})")
    # legenda
    legend = re.search(r"^### Níveis de prioridade", sec8, re.MULTILINE)
    if not legend or not all(re.search(rf"^- \*\*{n}\*\*", sec8, re.MULTILINE) for n in "123"):
        rep.err("seção 8 sem '### Níveis de prioridade' com os níveis **1**, **2** e **3**")
    # mermaid
    mer, nodes, edges = read_mermaid(sec8, rep)
    result["mermaid"] = mer
    if mer:
        table_edges = {(d, rid) for rid, ds in deps_valid.items() for d in ds}
        for a, b in set(edges) - table_edges:
            rep.err(f"mermaid tem {a} --> {b}, mas a tabela não diz que {b} depende de {a}")
        for a, b in table_edges - set(edges):
            rep.err(f"tabela diz que {b} depende de {a}, mas o mermaid não tem {a} --> {b}")
        if len(edges) != len(set(edges)):
            rep.err("aresta duplicada no mermaid")
        for rid in rf_set - nodes:
            rep.err(f"{rid} não aparece no mermaid")
        for n in nodes - rf_set:
            rep.err(f"mermaid cita {n}, que não existe nos requisitos")
    result["external"] = read_external(sec8, rep, rf_set)
    result["foundation"] = foundation
    result["names"] = names
    result["priority"] = prio
    result["deps"] = deps_valid
    result["wave_of"] = expected
    return result


def check_out_of_scope(body, rep):
    groups = bold_groups(body)
    loose = bullets(body)
    if not groups and not loose:
        rep.warn("seção 7 vazia: fora de escopo explícito é o que evita 'mas eu achei que...'")
    return groups if groups else [("Geral", loose)]


def check_acceptance(body, rep, reqs):
    rf_set = {r["id"] for r in reqs}
    per_rf, integration = {}, []
    for head, b in split_h3(body):
        items = [re.sub(r"^\[[ x]\]\s*", "", i) for i in bullets(b)]
        m = re.match(r"(RF-\d{3})\s+", head)
        if m:
            if not items:
                rep.err(f"{m.group(1)} sem critérios de aceitação")
            elif len(items) < 2:
                rep.warn(f"{m.group(1)} com um critério só: cubra sucesso e falha")
            per_rf[m.group(1)] = items
        elif head.startswith("Integração entre requisitos"):
            integration = items
        else:
            rep.warn(f"seção 9: subseção '{head[:40]}' fora do padrão RF-NNN ou Integração entre requisitos")
    for rid in rf_set - set(per_rf):
        rep.err(f"{rid} está na seção 6 mas não tem critérios na seção 9")
    for rid in set(per_rf) - rf_set:
        rep.err(f"{rid} tem critérios na seção 9 mas não existe na seção 6")
    if not re.search(r"^### Integração entre requisitos", body, re.MULTILINE):
        rep.err("seção 9 sem '### Integração entre requisitos'")
    pairs = {(c["from"], r["id"]) for r in reqs for c in r["consumes"]}
    for a, b in sorted(pairs):
        if not any(a in i and b in i for i in integration):
            rep.err(f"{b} consome de {a}, mas nenhum critério de integração cita {a} e {b} juntos")
    if not pairs and integration and not any("não se aplica" in i.lower() for i in integration):
        rep.warn("critérios de integração sem nenhum Consome declarado: ou falta Consome ou sobra critério")
    return per_rf, integration


def check_style(text, rep):
    if "—" in text:
        rep.warn(f"{text.count('—')} travessão(ões) '—' no texto; a regra do PRD é não usar")
    hyp = len(re.findall(r"\(hipótese\)", text))
    if hyp > 30:
        rep.warn(f"{hyp} hipóteses; acima de 30 o documento está decidindo demais pelo usuário")
    lines = text.count("\n")
    if lines > 700:
        rep.warn(f"{lines} linhas; orçamento do PRD é 300 a 700")
    body = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for m in STACK_WORDS.finditer(body):
        rep.warn(f"termo de stack no PRD: '{m.group(0)}' (vai para ADR, salvo integração obrigatória)")
    return hyp


# ---------- análise completa ----------

def analyze(text):
    """Roda todas as checagens. Retorna (report, data) com o que o JSON e o progress.py precisam."""
    rep = Report()
    data = {"requirements": [], "graph": {}}
    check_header(text, rep)
    sections = split_h2(text)
    check_sections(sections, rep)
    check_placeholders(text, rep)
    by = dict(sections)
    reqs = read_requirements(by.get("6. Requisitos funcionais", ""), rep) if "6. Requisitos funcionais" in by else []
    rf_set = {r["id"] for r in reqs}
    data["meta"] = {
        "system": (re.search(r"^# PRD: (.+)$", text, re.MULTILINE) or [None, ""])[1].strip(),
        "version": (re.search(r"^Versão: (.+)$", text, re.MULTILINE) or [None, ""])[1].strip(),
        "date": (re.search(r"^Data: (.+)$", text, re.MULTILINE) or [None, ""])[1].strip(),
        "owner": (re.search(r"^Responsável: (.+)$", text, re.MULTILINE) or [None, ""])[1].strip(),
    }
    data["summary"] = by.get("1. Resumo executivo", "").strip()
    data["pains"], data["opportunity"] = check_problem(by.get("2. Problema e oportunidade", ""), rep) if "2. Problema e oportunidade" in by else ([], [])
    data["profiles"], data["behavior"] = check_audience(by.get("3. Público-alvo", ""), rep) if "3. Público-alvo" in by else ([], [])
    data["goals"], data["nfr"] = check_objectives(by.get("4. Objetivos e métricas", ""), rep) if "4. Objetivos e métricas" in by else ([], [])
    data["stories"] = check_stories(by.get("5. Histórias de usuário", ""), rep, rf_set) if "5. Histórias de usuário" in by else {}
    data["requirements"] = reqs
    check_contracts(reqs, rep)
    data["out_of_scope"] = check_out_of_scope(by.get("7. Fora de escopo", ""), rep) if "7. Fora de escopo" in by else []
    data["graph"] = check_graph(by.get("8. Mapa de dependências e paralelismo", ""), reqs, rep) if "8. Mapa de dependências e paralelismo" in by else {}
    data["acceptance"], data["integration"] = check_acceptance(by.get("9. Critérios de aceitação", ""), rep, reqs) if "9. Critérios de aceitação" in by else ({}, [])
    data["hypotheses"] = check_style(text, rep)
    return rep, data


# ---------- json ----------

def prune(obj):
    if isinstance(obj, dict):
        return {k: v for k, v in ((k, prune(v)) for k, v in obj.items()) if v not in ("", None, [], {})}
    if isinstance(obj, list):
        return [v for v in (prune(x) for x in obj) if v not in ("", None, [], {})]
    return obj


def build_json(data):
    g = data.get("graph", {})
    f_ids = {f["id"] for f in (g.get("foundation") or [])}
    reqs = []
    for r in data["requirements"]:
        rid = r["id"]
        reqs.append({
            **r,
            "priority": g.get("priority", {}).get(rid),
            "dependencies": g.get("deps", {}).get(rid, []),
            "wave": g.get("wave_of", {}).get(rid),
            "foundation": rid in f_ids,
            "stories": data.get("stories", {}).get(rid, []),
            "acceptance": data.get("acceptance", {}).get(rid, []),
        })
    doc = {
        "meta": data["meta"],
        "executive_summary": data.get("summary", ""),
        "problem": {
            "pains": [{"title": t, "items": i} for t, i in data.get("pains", [])],
            "opportunity": data.get("opportunity", []),
        },
        "audience": {
            "profiles": [{"name": n, "items": i} for n, i in data.get("profiles", [])],
            "behavioral_profile": data.get("behavior", []),
        },
        "objectives": data.get("goals", []),
        "non_functional": data.get("nfr", []),
        "requirements": reqs,
        "out_of_scope": [{"category": c, "items": i} for c, i in data.get("out_of_scope", [])],
        "dependency_graph": {
            "order": g.get("order") or [],
            "foundation": g.get("foundation") or [],
            "waves": [{"wave": w, "requirements": g["waves"][w]} for w in sorted(g.get("waves", {}))],
            "critical_path": g.get("critical", []),
            "external_dependencies": g.get("external", []),
            "mermaid": g.get("mermaid", ""),
        },
        "integration_criteria": data.get("integration", []),
    }
    return prune(doc)


def main(argv):
    args = list(argv[1:])
    json_out = None
    if "--json" in args:
        i = args.index("--json")
        json_out = Path(args[i + 1]) if i + 1 < len(args) else None
        del args[i : i + 2]
    if len(args) != 1:
        print(__doc__)
        return 2
    path = Path(args[0])
    if not path.is_file():
        print(f"arquivo não encontrado: {path}")
        return 2
    text = path.read_text(encoding="utf-8")
    rep, data = analyze(text)
    for w in rep.warnings:
        print(f"aviso: {w}")
    for e in rep.errors:
        print(f"erro: {e}")
    g = data.get("graph", {})
    n_waves = len(g.get("waves", {}))
    cp = " → ".join(g.get("critical", []))
    print(f"{path}: {len(data['requirements'])} RFs em {n_waves} onda(s), caminho crítico {cp or 'n/a'}, "
          f"{data.get('hypotheses', 0)} hipóteses, {len(rep.errors)} erro(s), {len(rep.warnings)} aviso(s)")
    if json_out and not rep.errors:
        json_out.write_text(json.dumps(build_json(data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"json: {json_out}")
    elif json_out:
        print("json não gerado: corrija os erros primeiro")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
