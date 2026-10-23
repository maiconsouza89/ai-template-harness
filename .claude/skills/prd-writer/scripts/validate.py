#!/usr/bin/env python3
"""Valida a estrutura de um PRD gerado pela skill prd-writer.

Uso: python3 validate.py docs/product/prd.md

Checa o que é mecânico: seções obrigatórias na ordem do template, requisitos funcionais
completos (com critérios de aceitação próprios), placeholders esquecidos, mapa de
dependências coerente (arestas para nós existentes, sem ciclo, ondas respeitando
predecessores e ordenadas por prioridade), 'Usa de' casando com as arestas 'dado' e cada
uma com critério de integração. Sai com código 1 quando há erro. Avisos não derrubam.
Só biblioteca padrão. roadmap.py importa os parsers daqui.
"""
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Resumo",
    "Contexto e problema",
    "Objetivos e métricas",
    "Escopo",
    "Requisitos funcionais",
    "Requisitos não funcionais",
    "Decisões de produto e trade-offs",
    "Dependências",
    "Riscos e mitigação",
    "Critérios de aceitação",
    "Validação",
    "Mapa de dependências e paralelismo",
]
NFR_REQUIRED = ["Performance", "Disponibilidade"]
PRIORITIES = {"alta", "media", "média", "baixa"}
RANK = {"alta": 3, "media": 2, "baixa": 1}
EDGE_LABELS = {"dado", "fluxo", "regra"}
STACK_WORDS = re.compile(
    r"\b(postgres\w*|mysql|mongodb|redis|kafka|rabbitmq|react|vue|angular|django|rails|"
    r"spring|node\.?js|typescript|python|java|golang|kotlin|docker|kubernetes|aws|azure|gcp|"
    r"grpc|graphql|rest api|microsservi\w+|monólito|monolito)\b",
    re.IGNORECASE,
)

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def norm_id(raw):
    """RF001, RF-001, rf001 -> RF-001; DEP1 -> DEP-1."""
    m = re.fullmatch(r"([A-Za-z]+)-?(\d+)", raw.strip())
    if not m:
        return raw.strip()
    prefix, num = m.group(1).upper(), m.group(2)
    if prefix == "RF":
        return f"RF-{int(num):03d}"
    return f"{prefix}-{int(num)}"


def split_sections(text):
    """Retorna lista (titulo_h2, corpo) na ordem do arquivo."""
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    sections = []
    for i in range(1, len(parts), 2):
        sections.append((parts[i].strip(), parts[i + 1]))
    return sections


def check_header(text):
    if not re.search(r"^# PRD: \S", text, re.MULTILINE):
        err("título deve ser '# PRD: <nome do sistema>'")
    for field in ("Versão:", "Data:", "Responsável:"):
        if not re.search(rf"^{field} \S", text, re.MULTILINE):
            err(f"cabeçalho sem '{field} ...'")
    m = re.search(r"^Data: (\S+)", text, re.MULTILINE)
    if m and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", m.group(1)):
        err(f"Data '{m.group(1)}' não está em AAAA-MM-DD")


def check_sections(sections):
    titles = [t for t, _ in sections]
    missing = [s for s in REQUIRED_SECTIONS if s not in titles]
    for s in missing:
        err(f"seção obrigatória ausente: '## {s}'")
    present = [s for s in REQUIRED_SECTIONS if s in titles]
    order = [t for t in titles if t in REQUIRED_SECTIONS]
    if order != present:
        err("seções obrigatórias fora da ordem do template")
    extra = [t for t in titles if t not in REQUIRED_SECTIONS]
    for t in extra:
        warn(f"seção fora do template: '## {t}'")


def check_placeholders(text):
    # [texto em minúsculas sem link] é placeholder do template esquecido.
    for m in re.finditer(r"\[([a-záéíóúâêôãõç][^\]\n]{2,})\](?!\()", text):
        inner = m.group(1)
        if inner.startswith("RF-") or inner.startswith("DEP-") or inner.startswith("x") or inner == " ":
            continue
        err(f"placeholder não preenchido: [{inner[:40]}]")
    if "AAAA-MM-DD" in text:
        err("data do cabeçalho ainda é AAAA-MM-DD")


def check_goals(body):
    rows = [l for l in body.splitlines() if l.startswith("|")]
    data = [r for r in rows[2:] if r.strip("| ").strip()]
    if not data:
        err("tabela de objetivos sem linhas")
    for r in data:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(cells) < 3 or any(not c for c in cells[:3]):
            err(f"objetivo incompleto (objetivo, métrica, meta): {r.strip()[:60]}")
        elif not re.search(r"\d", cells[2]):
            warn(f"meta sem número: '{cells[2][:50]}'")


def rf_blocks(body):
    """Retorna lista (id, nome, bloco) dos '### RF-NNN Nome' da seção de requisitos."""
    out = []
    for b in re.split(r"^### ", body, flags=re.MULTILINE)[1:]:
        m = re.match(r"(RF-\d{3})\s+(.+)", b.splitlines()[0].strip())
        out.append((m.group(1), m.group(2).strip(), b) if m else (None, b.splitlines()[0].strip(), b))
    return out


def bullets_after(block, title):
    """Itens '- ...' logo abaixo de '**title**'; None se o bloco não existe."""
    m = re.search(rf"^\*\*{re.escape(title)}\*\*\n((?:- .*\n?)*)", block, re.MULTILINE)
    if not m:
        return None
    return [l[2:].strip() for l in m.group(1).strip().splitlines() if l.startswith("- ")]


def parse_priority(block):
    pm = re.search(r"\*\*Prioridade:\*\*\s*(\S+)", block)
    if not pm:
        return None
    p = pm.group(1).lower().strip("*")
    return "media" if p == "média" else p


def check_rfs(body):
    blocks = re.split(r"^### ", body, flags=re.MULTILINE)[1:]
    ids, prios, uses = [], {}, {}
    if not blocks:
        err("nenhum requisito funcional (### RF-NNN Nome)")
    for b in blocks:
        head = b.splitlines()[0].strip()
        m = re.match(r"(RF-\d{3})\s+(.+)", head)
        if not m:
            err(f"cabeçalho de RF fora do padrão '### RF-NNN Nome': '{head[:50]}'")
            continue
        rid = m.group(1)
        if rid in ids:
            err(f"{rid} duplicado")
        ids.append(rid)
        desc = [l for l in b.splitlines()[1:] if l.strip() and not l.startswith("**")]
        if not desc or desc[0].startswith("-"):
            err(f"{rid} sem descrição em uma frase antes do fluxo")
        if not re.search(r"^\*\*Para quem:\*\* \S", b, re.MULTILINE):
            err(f"{rid} sem '**Para quem:** <público e ganho>'")
        used = bullets_after(b, "Usa de")
        uses[rid] = set()
        if used is not None:
            if not used:
                err(f"{rid} tem '**Usa de**' vazio; remova o bloco ou liste 'RF-NNN: dado'")
            for item in used:
                um = re.match(r"((?:RF|DEP)-?\d+)\s*:\s*\S", item)
                if not um:
                    err(f"{rid} 'Usa de' fora do padrão '- RF-NNN: dado': '{item[:50]}'")
                else:
                    uses[rid].add(norm_id(um.group(1)))
        crit = bullets_after(b, "Critérios de aceitação")
        if crit is None:
            err(f"{rid} sem '**Critérios de aceitação**' com itens")
        elif len(crit) < 2:
            err(f"{rid} com {len(crit)} critério(s) de aceitação; mínimo 2 (sucesso e falha)")
        elif len(crit) > 5:
            warn(f"{rid} com {len(crit)} critérios de aceitação (orçamento: 2 a 5)")
        fm = re.search(r"\*\*Fluxo principal\*\*\n((?:- .*\n?)+)", b)
        if not fm:
            err(f"{rid} sem '**Fluxo principal**' com passos")
        else:
            n = len(fm.group(1).strip().splitlines())
            if n < 3 or n > 8:
                warn(f"{rid} fluxo principal com {n} passos (orçamento: 3 a 8)")
        if "**Fluxos alternativos e exceções**" not in b:
            err(f"{rid} sem '**Fluxos alternativos e exceções**'")
        # Erros previstos é condicional (só RF que mexe em dado, dinheiro, permissão ou é
        # irreversível); o critério é de julgamento, então o validador não cobra.
        p = parse_priority(b)
        if p is None:
            err(f"{rid} sem '**Prioridade:** alta|media|baixa'")
        elif p not in PRIORITIES:
            err(f"{rid} prioridade inválida '{p}'")
        else:
            prios[rid] = p
    if len(ids) > 15:
        warn(f"{len(ids)} RFs; acima de 15 costuma ser mais de uma entrega")
    seq = [int(i[3:]) for i in ids]
    if seq != sorted(seq):
        warn("RFs fora de ordem numérica")
    return ids, prios, uses


def check_nfr(body):
    for cat in NFR_REQUIRED:
        if not re.search(rf"^{cat}\n- \S", body, re.MULTILINE):
            err(f"requisitos não funcionais sem '{cat}' com pelo menos uma meta")


def check_risks(body):
    blocks = re.split(r"^### ", body, flags=re.MULTILINE)[1:]
    if not blocks:
        warn("nenhum risco listado")
    for b in blocks:
        name = b.splitlines()[0].strip()[:50]
        for field in ("Probabilidade", "Impacto", "Mitigação", "Plano de contingência"):
            if f"**{field}:**" not in b:
                err(f"risco '{name}' sem '**{field}:**'")
        pm = re.search(r"\*\*Probabilidade:\*\*\s*(\S+)", b)
        if pm and pm.group(1).lower() not in PRIORITIES:
            err(f"risco '{name}' com probabilidade inválida '{pm.group(1)}'")
        if "**Mitigação:**" in b and not re.search(r"\*\*Mitigação:\*\*\n(?:\s+- \S)", b):
            err(f"risco '{name}': mitigação deve ser lista de subitens")


def check_decisions(body):
    blocks = re.split(r"^### ", body, flags=re.MULTILINE)[1:]
    for b in blocks:
        name = b.splitlines()[0].strip()[:50]
        for field in ("Justificativa", "Trade-off"):
            if f"**{field}:**" not in b:
                err(f"decisão '{name}' sem '**{field}:**'")


def parse_mermaid(body):
    """Retorna (mermaid_bruto, nós {id: rótulo}, arestas [(a, rótulo, b)]) ou None."""
    m = re.search(r"```mermaid\n(.*?)```", body, re.DOTALL)
    if not m:
        return None
    mer = m.group(1)
    nodes, edges = {}, []
    for line in mer.splitlines():
        line = line.strip()
        if not line or line.startswith(("graph", "flowchart", "%%", "classDef", "class ")):
            continue
        em = re.match(r"([A-Za-z]+-?\d+)\s*--+>\s*(?:\|([^|]*)\|\s*)?([A-Za-z]+-?\d+)", line)
        if em:
            a, lbl, b = norm_id(em.group(1)), (em.group(2) or "").strip().lower(), norm_id(em.group(3))
            edges.append((a, lbl, b))
            nodes.setdefault(a, a)
            nodes.setdefault(b, b)
            continue
        # Rótulo entre aspas pode ter parênteses e colchetes; sem aspas, vai até o fechamento.
        nm = re.match(r"([A-Za-z]+-?\d+)\s*[\[\{\(]+(?:\"([^\"]*)\"|([^\]\}\)]*))", line)
        if nm:
            nodes[norm_id(nm.group(1))] = (nm.group(2) if nm.group(2) is not None else nm.group(3)).strip()
    return mer, nodes, edges


def parse_waves(body):
    """Linhas da tabela de ondas: lista (onda, [RF-NNN na ordem escrita])."""
    rows = []
    for r in body.splitlines():
        if not r.startswith("|"):
            continue
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(cells) >= 2 and re.fullmatch(r"\d+", cells[0]):
            rows.append((int(cells[0]), re.findall(r"RF-\d{3}", cells[1])))
    return rows


def check_map(body, rf_ids, prios, uses):
    parsed = parse_mermaid(body)
    if not parsed:
        err("mapa sem bloco ```mermaid")
        return
    mer, node_labels, labeled = parsed
    if not re.search(r"^\s*(graph|flowchart)\s+(LR|TD|TB|RL|BT)", mer, re.MULTILINE):
        err("bloco mermaid deve começar com 'graph LR' (ou flowchart)")
    nodes = set(node_labels)
    edges = [(a, b) for a, _, b in labeled]
    for a, lbl, b in labeled:
        if lbl not in EDGE_LABELS:
            err(f"aresta {a} → {b} sem rótulo dado|fluxo|regra (tem '{lbl}')")
    # 'Usa de' e aresta 'dado' são a mesma informação vista dos dois lados.
    data_edges = {(a, b) for a, lbl, b in labeled if lbl == "dado"}
    for a, b in sorted(data_edges):
        if b in uses and a not in uses[b]:
            err(f"aresta {a} -->|dado| {b} sem '- {a}: ...' em '**Usa de**' de {b}")
    for b, srcs in uses.items():
        for a in sorted(srcs):
            if (a, b) not in data_edges:
                err(f"{b} 'Usa de' {a}, mas o mapa não tem aresta {a} -->|dado| {b}")
    rf_set = set(rf_ids)
    for n in nodes:
        if n.startswith("RF-") and n not in rf_set:
            err(f"mapa cita {n}, que não existe nos requisitos funcionais")
    for rid in rf_ids:
        if rid not in nodes:
            err(f"{rid} não aparece no mapa de dependências")
    if len(edges) != len(set(edges)):
        err("aresta duplicada no mapa")
    # ciclos e arestas transitivas
    succ = {}
    for a, b in edges:
        succ.setdefault(a, set()).add(b)

    def reach(start):
        seen, stack = set(), [start]
        while stack:
            x = stack.pop()
            for y in succ.get(x, ()):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen

    for n in nodes:
        if n in reach(n):
            err(f"ciclo no mapa envolvendo {n}")
            break
    for a, b in edges:
        others = succ[a] - {b}
        if any(b in reach(o) for o in others):
            warn(f"aresta transitiva {a} → {b} (já alcançável por outro caminho)")
    # prioridade herda para trás
    for a, b in edges:
        pa, pb = prios.get(a), prios.get(b)
        if pa and pb and RANK[pa] < RANK[pb]:
            err(f"{b} ({pb}) depende de {a} ({pa}): a prioridade de {a} precisa subir")
    # nós atípicos: questionar, não proibir
    for rid in rf_ids:
        ins = [a for a, b in edges if b == rid]
        outs = [b for a, b in edges if a == rid]
        if rid in nodes and not ins and not outs and len(rf_ids) > 1:
            warn(f"{rid} isolado no mapa; confirme que não lê nem alimenta nenhum outro RF")
        if len(ins) >= 4:
            warn(f"{rid} com {len(ins)} predecessores; confira se todos são dado, fluxo ou regra de verdade")
    # ondas
    waves = {}
    for w, ids in parse_waves(body):
        for rid in ids:
            if rid in waves:
                err(f"{rid} aparece em mais de uma onda")
            waves[rid] = w
        key = [(-RANK.get(prios.get(r), 0), r) for r in ids]
        if key != sorted(key):
            err(f"onda {w}: RFs devem vir por prioridade (alta, media, baixa) e depois por número")
    if not waves:
        err("tabela de ondas ausente ou sem linhas numeradas")
        return
    for rid in rf_ids:
        if rid not in waves:
            err(f"{rid} não está em nenhuma onda")
    for a, b in edges:
        if a in waves and b in waves and waves[a] >= waves[b]:
            err(f"{b} está na onda {waves[b]} mas depende de {a} na onda {waves[a]}")
    pred = {}
    for a, b in edges:
        pred.setdefault(b, set()).add(a)
    for rid, w in waves.items():
        rf_pred = {p for p in pred.get(rid, ()) if p.startswith("RF-")}
        if not rf_pred and w != 1 and not any(p.startswith("DEP-") for p in pred.get(rid, ())):
            warn(f"{rid} não tem predecessor mas está na onda {w}")
    if "Caminho crítico:" not in body:
        err("mapa sem linha 'Caminho crítico: ...'")


def check_integration(body, uses):
    """Cada item de 'Usa de' precisa de um critério transversal citando os dois lados."""
    lines = [l for l in body.splitlines() if l.startswith("- ")]
    for b, srcs in uses.items():
        for a in sorted(srcs):
            if not any(a in l and b in l for l in lines):
                err(f"critérios de aceitação sem item de integração citando {a} e {b}")


def check_style(text):
    if "—" in text:
        warn(f"{text.count('—')} travessão(ões) '—' no texto; a regra do PRD é não usar")
    hyp = len(re.findall(r"\(hipótese\)", text))
    if hyp > 30:
        warn(f"{hyp} hipóteses; acima de 30 o documento está decidindo demais pelo usuário")
    lines = text.count("\n")
    if lines > 1000:
        warn(f"{lines} linhas; orçamento do PRD é 250 a 1000")
    body_no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for m in STACK_WORDS.finditer(body_no_code):
        warn(f"termo de stack no PRD: '{m.group(0)}' (vai para ADR, salvo integração obrigatória)")
    return hyp


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"arquivo não encontrado: {path}")
        return 2
    text = path.read_text(encoding="utf-8")
    check_header(text)
    sections = split_sections(text)
    check_sections(sections)
    check_placeholders(text)
    by_title = dict(sections)
    rf_ids, prios, uses = [], {}, {}
    if "Objetivos e métricas" in by_title:
        check_goals(by_title["Objetivos e métricas"])
    if "Requisitos funcionais" in by_title:
        rf_ids, prios, uses = check_rfs(by_title["Requisitos funcionais"])
    if "Requisitos não funcionais" in by_title:
        check_nfr(by_title["Requisitos não funcionais"])
    if "Decisões de produto e trade-offs" in by_title:
        check_decisions(by_title["Decisões de produto e trade-offs"])
    if "Riscos e mitigação" in by_title:
        check_risks(by_title["Riscos e mitigação"])
    if "Mapa de dependências e paralelismo" in by_title:
        check_map(by_title["Mapa de dependências e paralelismo"], rf_ids, prios, uses)
    if "Critérios de aceitação" in by_title:
        check_integration(by_title["Critérios de aceitação"], uses)
    hyp = check_style(text)

    for w in warnings:
        print(f"aviso: {w}")
    for e in errors:
        print(f"erro: {e}")
    print(f"{path}: {len(rf_ids)} RFs, {hyp} hipóteses, {len(errors)} erro(s), {len(warnings)} aviso(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
