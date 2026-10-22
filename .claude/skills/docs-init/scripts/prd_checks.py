#!/usr/bin/env python3
"""Checagens de conteúdo do PRD e da seção "Ordem de execução" do roadmap.

Uso direto:
  python3 prd_checks.py docs/product/prd-x.md            # lista erros e avisos do PRD
  python3 prd_checks.py docs/product/prd-x.md --ondas    # imprime o bloco de Ordem de execução para o roadmap

O validate.py importa este módulo e aplica as mesmas checagens em `make check-docs`.

O que é checado no PRD (seções fixas do template prd.md): as 9 seções na ordem, placeholders do
template não preenchidos, requisitos funcionais completos (frase, Capacidades, Experiência),
contratos Consome/Fornece fechados dos dois lados, tabela de dependências em ordem topológica sem
ciclo nem referência órfã, Consome dentro de Depende de, prioridade que herda para trás, requisitos
de fundação na ordem da tabela, histórias e critérios para todo RF, critério de integração para
todo Consome, e marcas `(hipótese)` só em Capacidades e Tratamento de erros.

Ondas, caminho crítico e Mermaid não ficam no PRD: são derivados da tabela e vivem no roadmap.
`check_roadmap_order` recalcula tudo a partir do PRD e acusa divergência. Só biblioteca padrão.
"""
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
    "8. Dependências entre requisitos",
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
HYPOTHESIS_BLOCKS = {"Capacidades", "Tratamento de erros"}
HYPOTHESIS_LIMIT = 30
RF_ID = re.compile(r"RF-\d{3}")
GAP = "[A CONFIRMAR"
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "templates" / "prd.md"


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []
        self.hypotheses = 0

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


# ---------- utilidades de leitura ----------

def strip_frontmatter(text):
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return "".join(lines[i + 1:])
    return text


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


def bold_groups(body):
    """Grupos '**Título**' seguidos de bullets -> [(título, [itens])]."""
    groups = []
    for m in re.finditer(r"^\*\*([^*\n]+)\*\*\s*\n((?:- .*\n?)+)", body, re.MULTILINE):
        groups.append((m.group(1).strip().rstrip("."), bullets(m.group(2))))
    return groups


def rf_blocks(body):
    """'### RF-NNN Nome' -> [(id, nome, corpo)]. IDs fora do padrão viram None."""
    out = []
    for head, b in split_h3(body):
        m = re.match(r"(RF-\d{3})\s+(.+)", head)
        out.append((m.group(1) if m else None, m.group(2).strip() if m else head, b))
    return out


def parse_labeled(body):
    """Blocos '**Rótulo:**' com bullets dentro de um RF -> (dict rótulo -> itens, ordem)."""
    found, order = {}, []
    for m in re.finditer(r"^\*\*([^*\n]+?):\*\*[ \t]*\n((?:[ \t]*- .*\n?)+)", body, re.MULTILINE):
        label = m.group(1).strip()
        found[label] = bullets(m.group(2))
        order.append(label)
    return found, order


def has_number_or_gap(text):
    return bool(re.search(r"\d", text)) or GAP in text


# ---------- leitura das seções ----------

def read_requirements(body, rep):
    reqs, seen = [], set()
    for rid, name, b in rf_blocks(body):
        if not rid:
            rep.err(f"seção 6: cabeçalho fora do padrão '### RF-NNN Nome': '{name[:50]}'")
            continue
        if rid in seen:
            rep.err(f"{rid} duplicado na seção 6")
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
        for label, items in blocks.items():
            if label not in HYPOTHESIS_BLOCKS and any("(hipótese)" in i for i in items):
                rep.warn(f"{rid}: '(hipótese)' em '{label}'; a marca só vale em Capacidades e Tratamento de erros")
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
            provides.append({"data": item[: m.start()].strip(), "used_by": [norm_id(x) for x in RF_ID.findall(m.group(1))]})
        for item in blocks.get("Tratamento de erros", []):
            if ":" not in item:
                rep.warn(f"{rid} Tratamento de erros: '{item[:40]}' sem 'cenário: o que o usuário vê'")
        reqs.append({"id": rid, "name": name, "description": desc, "consumes": consumes, "provides": provides,
                     "blocks": blocks})
    if not reqs:
        rep.err("nenhum requisito funcional (### RF-NNN Nome) na seção 6")
    nums = [int(r["id"][3:]) for r in reqs]
    if nums != sorted(nums):
        rep.warn("RFs fora de ordem numérica na seção 6")
    if nums and nums != list(range(nums[0], nums[0] + len(nums))):
        rep.warn("numeração de RF com lacuna: aceitável só em atualização, com o RF removido listado em Fora de escopo")
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
            for t in [t.strip() for t in deps_raw.split(",") if t.strip()]:
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
                out.append({"title": title, "blocks": blocks})
    return out


def read_mermaid(body, rep, where):
    m = re.search(r"```mermaid\n(.*?)```", body, re.DOTALL)
    if not m:
        rep.err(f"{where}: sem bloco ```mermaid")
        return set(), []
    mer = m.group(1)
    if not re.search(r"^\s*(graph|flowchart)\s+TD\b", mer, re.MULTILINE):
        rep.err(f"{where}: bloco mermaid deve começar com 'graph TD'")
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
    return nodes, edges


def read_waves(body):
    waves = {}
    for m in re.finditer(r"^- \*\*Onda (\d+)\*\*\s*:\s*(.+)$", body, re.MULTILINE):
        waves[int(m.group(1))] = [norm_id(x) for x in re.findall(r"RF-?\d{3}", m.group(2))]
    return waves


# ---------- grafo ----------

def topo_canonical(ids, deps):
    """Ordem topológica com desempate pelo menor ID. None se houver ciclo."""
    pending, done, order = set(ids), set(), []
    while pending:
        ready = sorted((i for i in pending if set(deps.get(i, [])) <= done), key=lambda x: int(x[3:]))
        if not ready:
            return None
        order.append(ready[0])
        done.add(ready[0])
        pending.remove(ready[0])
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
        best[rid] = (best[max(preds, key=lambda d: len(best[d]))] + [rid]) if preds else [rid]
    return max(best.values(), key=len) if best else []


def waves_listing(wave_of, prio):
    """{onda: [RF ordenados por prioridade e ID]}."""
    out = {}
    for rid, w in wave_of.items():
        out.setdefault(w, []).append(rid)
    for w in out:
        out[w].sort(key=lambda i: (prio.get(i) or 9, int(i[3:])))
    return out


# ---------- checagens ----------

def check_sections(sections, rep):
    titles = [t for t, _ in sections]
    for s in SECTIONS:
        if s not in titles:
            rep.err(f"seção obrigatória ausente: '## {s}'")
    if [t for t in titles if t in SECTIONS] != [s for s in SECTIONS if s in titles]:
        rep.err("seções fora da ordem do template")
    for t in titles:
        if t not in SECTIONS:
            rep.err(f"seção fora do template: '## {t}' (o PRD tem exatamente 9 seções)")


def template_placeholders():
    if not TEMPLATE.is_file():
        return set()
    return set(re.findall(r"\[([^\]\n]{3,})\]", strip_frontmatter(TEMPLATE.read_text(encoding="utf-8"))))


def check_placeholders(text, rep):
    """Só o que veio do template conta como placeholder: colchetes em mensagens ('Olá [nome]') passam."""
    body = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    known = template_placeholders()
    for m in re.finditer(r"\[([^\]\n]{3,})\](?!\()", body):
        if m.group(1) in known:
            rep.err(f"placeholder do template não preenchido: [{m.group(1)[:40]}]")


def check_problem(body, rep):
    subs = dict(split_h3(body))
    pains = bold_groups(subs.get("O problema", ""))
    if "O problema" not in subs or not pains:
        rep.err("seção 2 sem '### O problema' com categorias em negrito e bullets")
    elif not (3 <= len(pains) <= 5):
        rep.warn(f"{len(pains)} categorias de dor; o orçamento é 3 a 5")
    for title, items in pains:
        if not any(has_number_or_gap(i) for i in items):
            rep.warn(f"dor '{title[:40]}' sem número de impacto nem [A CONFIRMAR]")
    opp = bullets(subs.get("A oportunidade", ""))
    if "A oportunidade" not in subs or not opp:
        rep.err("seção 2 sem '### A oportunidade' com bullets")
    elif pains and len(opp) < len(pains):
        rep.warn("oportunidade com menos itens que categorias de dor: toda dor precisa de resposta")


def check_audience(body, rep):
    subs = dict(split_h3(body))
    profiles = bold_groups(subs.get("Usuários primários", ""))
    if not profiles:
        rep.err("seção 3 sem '### Usuários primários' com perfis em negrito e bullets")
    for name, items in profiles:
        if len(items) < 2:
            rep.warn(f"perfil '{name[:30]}' com menos de 2 características")
    if len(profiles) == 1 and "Perfil comportamental" in subs:
        rep.warn("'Perfil comportamental' com um perfil só: omita, o perfil já diz tudo")
    if len(profiles) > 1 and not bullets(subs.get("Perfil comportamental", "")):
        rep.warn("mais de um perfil sem 'Perfil comportamental' com o que é comum a todos")


def check_objectives(body, rep):
    subs = dict(split_h3(body))
    goals = 0
    rows = [l for l in subs.get("Objetivos de produto", "").splitlines() if l.startswith("|")]
    for r in rows[2:]:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if not any(cells):
            continue
        if len(cells) < 3 or any(not c for c in cells[:3]):
            rep.err(f"objetivo incompleto (objetivo, métrica, meta): {r.strip()[:60]}")
            continue
        if not has_number_or_gap(cells[2]):
            rep.err(f"meta sem número nem [A CONFIRMAR]: '{cells[2][:50]}'")
        goals += 1
    if not goals:
        rep.err("seção 4 sem tabela de objetivos com linhas")
    elif not (3 <= goals <= 5):
        rep.warn(f"{goals} objetivos; o orçamento é 3 a 5")
    nfr_body = subs.get("Requisitos não funcionais", "")
    cats = {}
    for m in re.finditer(r"^([A-ZÁÉÍÓÚÂÊÔÃÕ][^\n*|#-]{2,60})\n((?:- .*\n?)+)", nfr_body, re.MULTILINE):
        cats[m.group(1).strip()] = bullets(m.group(2))
    for cat in NFR_REQUIRED:
        if cat not in cats:
            rep.err(f"requisitos não funcionais sem '{cat}' com pelo menos uma meta")
        elif not any(has_number_or_gap(i) for i in cats[cat]):
            rep.err(f"requisitos não funcionais: '{cat}' sem meta numérica nem [A CONFIRMAR]")


def check_stories(body, rep, rf_set):
    stories = {}
    for rid, name, b in rf_blocks(body):
        if not rid:
            rep.err(f"seção 5: cabeçalho fora do padrão '### RF-NNN Nome': '{name[:50]}'")
            continue
        items = bullets(b)
        if not items:
            rep.err(f"{rid} sem histórias (bullets) na seção 5")
        for s in items:
            if not s.startswith("Como "):
                rep.warn(f"{rid} história fora do padrão 'Como <papel>, quero ... para ...': '{s[:40]}'")
        stories[rid] = items
    for rid in sorted(rf_set - set(stories)):
        rep.err(f"{rid} está na seção 6 mas não tem histórias na seção 5")
    for rid in sorted(set(stories) - rf_set):
        rep.err(f"{rid} tem histórias na seção 5 mas não existe na seção 6")


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
            rep.warn(f"{r['id']} Consome cita autenticação ou sessão: é dependência de infraestrutura, só na tabela")


def check_graph(sec8, reqs, rep):
    """Valida a tabela da seção 8 e devolve o grafo derivado (ordem, ondas, caminho crítico, fundação)."""
    rf_set = {r["id"] for r in reqs}
    rows = read_table(sec8, rep)
    table_ids = [r["id"] for r in rows]
    for rid in set(table_ids):
        if table_ids.count(rid) > 1:
            rep.err(f"{rid} aparece mais de uma vez na tabela de dependências")
    for rid in sorted(rf_set - set(table_ids)):
        rep.err(f"{rid} está na seção 6 mas não na tabela de dependências")
    for rid in sorted(set(table_ids) - rf_set):
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
    deps_valid = {i: [d for d in deps[i] if d in set(table_ids) and d != i] for i in valid_ids}
    graph = {"ids": valid_ids, "deps": deps_valid, "priority": prio, "names": names,
             "order": None, "wave_of": {}, "waves": {}, "critical": [], "foundation": None}
    order = topo_canonical(valid_ids, deps_valid)
    if order is None:
        rep.err("ciclo na tabela de dependências: dois requisitos são um só ou um deles precisa ser dividido")
        return graph
    pos = {rid: i for i, rid in enumerate(table_ids)}
    for rid, ds in deps_valid.items():
        for d in ds:
            if pos.get(d, -1) > pos[rid]:
                rep.err(f"{rid} depende de {d}, que aparece abaixo na tabela (ordem topológica quebrada)")
    if valid_ids != order:
        rep.err(f"ordem da tabela deve ser topológica com desempate pelo menor ID: {', '.join(order)}")
    for r in reqs:
        for c in r["consumes"]:
            if c["from"] not in deps.get(r["id"], []):
                rep.err(f"{r['id']} consome de {c['from']} mas a tabela não lista {c['from']} em 'Depende de'")
    for rid, ds in deps_valid.items():
        for d in ds:
            if prio.get(d) and prio.get(rid) and prio[d] > prio[rid]:
                rep.err(f"{rid} (prioridade {prio[rid]}) depende de {d} (prioridade {prio[d]}): a prioridade de {d} precisa subir")

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
    foundation = read_foundation(sec8)
    if foundation is not None:
        for f in foundation:
            if not f["id"]:
                rep.err(f"fundação: item fora do padrão '- **RF-NNN Nome**: contribuição' ('{f['name']}')")
            elif f["id"] not in rf_set:
                rep.err(f"fundação cita {f['id']}, que não existe")
            elif not f["contribution"]:
                rep.warn(f"fundação: {f['id']} sem dizer o que contribui para a base")
        known = [f["id"] for f in foundation if f["id"] in pos]
        if known != sorted(known, key=lambda i: pos[i]):
            rep.err("requisitos de fundação fora da ordem da tabela")
    if not re.search(r"^### Níveis de prioridade", sec8, re.MULTILINE) or not all(
        re.search(rf"^- \*\*{n}\*\*", sec8, re.MULTILINE) for n in "123"
    ):
        rep.err("seção 8 sem '### Níveis de prioridade' com os níveis **1**, **2** e **3**")
    for moved in ("### Ondas de execução", "```mermaid", "Caminho crítico:"):
        if moved in sec8:
            rep.err(f"seção 8 contém '{moved}': ondas, caminho crítico e diagrama vivem no roadmap, em Ordem de execução")
    read_external(sec8, rep, rf_set)
    graph["order"] = order
    graph["wave_of"] = compute_waves(order, deps_valid)
    graph["waves"] = waves_listing(graph["wave_of"], prio)
    graph["critical"] = critical_path(order, deps_valid)
    graph["foundation"] = [f["id"] for f in foundation if f["id"]] if foundation else []
    return graph


def check_out_of_scope(body, rep):
    if not bold_groups(body) and not bullets(body):
        rep.warn("seção 7 vazia: fora de escopo explícito é o que evita 'mas eu achei que...'")


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
    for rid in sorted(rf_set - set(per_rf)):
        rep.err(f"{rid} está na seção 6 mas não tem critérios na seção 9")
    for rid in sorted(set(per_rf) - rf_set):
        rep.err(f"{rid} tem critérios na seção 9 mas não existe na seção 6")
    if not re.search(r"^### Integração entre requisitos", body, re.MULTILINE):
        rep.err("seção 9 sem '### Integração entre requisitos'")
    pairs = {(c["from"], r["id"]) for r in reqs for c in r["consumes"]}
    for a, b in sorted(pairs):
        if not any(a in i and b in i for i in integration):
            rep.err(f"{b} consome de {a}, mas nenhum critério de integração cita {a} e {b} juntos")
    if not pairs and integration and not any("não se aplica" in i.lower() for i in integration):
        rep.warn("critérios de integração sem nenhum Consome declarado: ou falta Consome ou sobra critério")


def check_style(text, rep):
    if "—" in text:
        rep.warn(f"{text.count('—')} travessão(ões) no texto; a convenção é não usar")
    rep.hypotheses = text.count("(hipótese)")
    if rep.hypotheses > HYPOTHESIS_LIMIT:
        rep.warn(f"{rep.hypotheses} hipóteses; acima de {HYPOTHESIS_LIMIT} o documento está decidindo demais pelo usuário")
    if text.count("\n") > 700:
        rep.warn(f"{text.count(chr(10))} linhas; orçamento do PRD é 300 a 700")


# ---------- análise completa ----------

def analyze(text):
    """Roda todas as checagens do PRD. Retorna (Report, grafo derivado da seção 8)."""
    rep = Report()
    body_text = strip_frontmatter(text)
    if not re.search(r"^# PRD: \S", body_text, re.MULTILINE):
        rep.err("título deve ser '# PRD: <nome do produto>'")
    sections = split_h2(body_text)
    check_sections(sections, rep)
    check_placeholders(body_text, rep)
    by = dict(sections)
    reqs = read_requirements(by.get("6. Requisitos funcionais", ""), rep) if "6. Requisitos funcionais" in by else []
    rf_set = {r["id"] for r in reqs}
    if "2. Problema e oportunidade" in by:
        check_problem(by["2. Problema e oportunidade"], rep)
    if "3. Público-alvo" in by:
        check_audience(by["3. Público-alvo"], rep)
    if "4. Objetivos e métricas" in by:
        check_objectives(by["4. Objetivos e métricas"], rep)
    if "5. Histórias de usuário" in by:
        check_stories(by["5. Histórias de usuário"], rep, rf_set)
    check_contracts(reqs, rep)
    graph = check_graph(by.get("8. Dependências entre requisitos", ""), reqs, rep)
    if "7. Fora de escopo" in by:
        check_out_of_scope(by["7. Fora de escopo"], rep)
    if "9. Critérios de aceitação" in by:
        check_acceptance(by["9. Critérios de aceitação"], rep, reqs)
    check_style(body_text, rep)
    return rep, graph


# ---------- ordem de execução (roadmap) ----------

def render_order(graph):
    """Bloco Markdown da subseção de Ordem de execução do roadmap, derivado do grafo."""
    if graph["order"] is None:
        return ""
    lines = []
    for w in sorted(graph["waves"]):
        lines.append(f"- **Onda {w}**: {', '.join(graph['waves'][w])}")
    cp = graph["critical"]
    lines += ["", f"Caminho crítico: {' > '.join(cp)} ({len(cp)} onda{'s' if len(cp) != 1 else ''})."]
    if graph["foundation"]:
        lines += ["", "**Nota:** requisitos de fundação (" + ", ".join(graph["foundation"]) +
                  ") não rodam em paralelo em um projeto novo, mesmo quando aparecem juntos em uma onda: eles tocam os mesmos arquivos de base e são implementados em sequência até a base existir."]
    lines += ["", "```mermaid", "graph TD"]
    labeled = set()

    def node(rid):
        if rid in labeled:
            return rid.replace("-", "")
        labeled.add(rid)
        label = f"{rid} {graph['names'].get(rid, '')}".rstrip()
        return f'{rid.replace("-", "")}["{label}"]'

    edges = [(d, rid) for rid in graph["order"] for d in graph["deps"].get(rid, [])]
    for a, b in edges:
        lines.append(f"  {node(a)} --> {node(b)}")
    for rid in graph["order"]:
        if rid not in labeled:
            lines.append(f"  {node(rid)}")
    lines.append("```")
    return "\n".join(lines) + "\n"


def check_roadmap_order(roadmap_text, roadmap_path, load_prd):
    """Compara a seção 'Ordem de execução' do roadmap com o que a tabela de cada PRD produz.

    `load_prd(path)` devolve o texto do PRD ou None. Retorna (erros, avisos, {RF citados no roadmap}).
    """
    errors, warnings = [], []
    body = strip_frontmatter(roadmap_text)
    cited = {norm_id(x) for x in RF_ID.findall(body)}
    sections = dict(split_h2(body))
    order_body = sections.get("Ordem de execução")
    if order_body is None:
        return errors, warnings, cited
    subs = split_h3(order_body)
    if not subs and cited:
        warnings.append("'Ordem de execução' vazia enquanto o roadmap cita RF-NNN; gere o bloco com prd_checks.py --ondas")
    for head, sub in subs:
        link = re.search(r"\]\(([^)\s]+)\)", head)
        if not link:
            errors.append(f"Ordem de execução: subseção '{head[:40]}' sem link para o PRD no título")
            continue
        prd_path = (Path(roadmap_path).parent / link.group(1).split("#", 1)[0]).resolve()
        prd_text = load_prd(prd_path)
        if prd_text is None:
            errors.append(f"Ordem de execução: PRD '{link.group(1)}' não encontrado")
            continue
        rep, graph = analyze(prd_text)
        if graph["order"] is None:
            errors.append(f"Ordem de execução: PRD '{link.group(1)}' tem erro na tabela de dependências; corrija o PRD antes")
            continue
        where = f"Ordem de execução de '{link.group(1)}'"
        got = read_waves(sub)
        if not got:
            errors.append(f"{where}: sem linhas '- **Onda N**: RF-...'")
        for w in sorted(set(graph["waves"]) | set(got)):
            exp, has = graph["waves"].get(w, []), got.get(w, [])
            if set(exp) != set(has):
                errors.append(f"{where}: Onda {w} deveria ter {', '.join(exp) or 'nada'}; tem {', '.join(has) or 'nada'}")
            elif exp != has:
                errors.append(f"{where}: Onda {w} na ordem prioridade crescente e depois ID: {', '.join(exp)}")
        cp = graph["critical"]
        cm = re.search(r"^Caminho crítico:\s*(.+)$", sub, re.MULTILINE)
        if not cm:
            errors.append(f"{where}: sem linha 'Caminho crítico: RF-... > RF-... (N ondas)'")
        else:
            found = [norm_id(x) for x in RF_ID.findall(cm.group(1))]
            n = re.search(r"\((\d+) ondas?\)", cm.group(1))
            if found != cp or not n or int(n.group(1)) != len(cp):
                errors.append(f"{where}: caminho crítico deveria ser {' > '.join(cp)} ({len(cp)} ondas)")
        has_note = bool(re.search(r"^\*\*Nota:\*\*", sub, re.MULTILINE))
        if graph["foundation"] and not has_note:
            errors.append(f"{where}: PRD tem requisitos de fundação, falta a '**Nota:**' sobre fundação em sequência")
        if not graph["foundation"] and has_note:
            errors.append(f"{where}: há '**Nota:**' de fundação, mas o PRD não tem requisitos de fundação")
        local = Report()
        nodes, edges = read_mermaid(sub, local, where)
        errors.extend(local.errors)
        if nodes or edges:
            table_edges = {(d, rid) for rid, ds in graph["deps"].items() for d in ds}
            for a, b in sorted(set(edges) - table_edges):
                errors.append(f"{where}: mermaid tem {a} --> {b}, mas a tabela do PRD não diz que {b} depende de {a}")
            for a, b in sorted(table_edges - set(edges)):
                errors.append(f"{where}: tabela do PRD diz que {b} depende de {a}, mas o mermaid não tem {a} --> {b}")
            for rid in sorted(set(graph["ids"]) - nodes):
                errors.append(f"{where}: {rid} não aparece no mermaid")
            for n in sorted(nodes - set(graph["ids"])):
                errors.append(f"{where}: mermaid cita {n}, que não existe no PRD")
    return errors, warnings, cited


def main(argv):
    if len(argv) < 2 or argv[1].startswith("-"):
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        print("Uso: python3 prd_checks.py <prd.md> [--ondas]", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"erro: arquivo não encontrado: {path}", file=sys.stderr)
        return 2
    rep, graph = analyze(path.read_text(encoding="utf-8"))
    if "--ondas" in argv[2:]:
        if rep.errors:
            print("erro: o PRD tem erros; corrija antes de gerar a ordem de execução:", file=sys.stderr)
            for e in rep.errors:
                print(f"  - {e}", file=sys.stderr)
            return 1
        sys.stdout.write(render_order(graph))
        return 0
    print("Erros:")
    for e in rep.errors:
        print(f"  - {e}")
    if not rep.errors:
        print("  nenhum")
    print("Avisos:")
    for w in rep.warnings:
        print(f"  - {w}")
    if not rep.warnings:
        print("  nenhum")
    print(f"Resumo: {len(rep.errors)} erro(s), {len(rep.warnings)} aviso(s), {rep.hypotheses} hipótese(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
