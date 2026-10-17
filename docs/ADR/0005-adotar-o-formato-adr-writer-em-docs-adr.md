---
status: accepted
date: 2026-10-17
layer: stack
title: "Adotar o formato da skill adr-writer em docs/ADR"
description: "Por que os ADRs passam a ter front-matter, camada, ciclo de status e índice gerado em docs/ADR, em vez do MADR mínimo sem metadados em docs/decisions."
supersedes: "0000"
superseded-by:
---

# 0005. Adotar o formato da skill adr-writer em docs/ADR

## Contexto e problema

Desde o ADR 0000 o acervo cresceu para cinco registros em `docs/decisions/`, sem metadados: não
há status, data nem cadeia de substituição, e o 0001 recebeu uma nota manual de "parcialmente
substituído". A skill `adr-writer`, versionada em `.claude/skills/`, define um formato com
front-matter, camada, ciclo de status, supersede bidirecional e um script de auditoria que gera o
índice. Manter dois padrões no mesmo repositório faria metade do acervo deixar de ser encontrada.

## Opções consideradas

- **Migrar tudo para `docs/ADR/` no formato da skill** — front-matter, `# NNNN.`, `layers.md`, `index.md` gerado, auditoria em `make check`.
- **Manter o MADR mínimo em `docs/decisions/`** — sem metadados; a skill ficaria sem uso.
- **Só adicionar front-matter aos arquivos atuais** — ganha metadados, mas o acervo fica fora do caminho que a skill e o script esperam.

## Decisão

Escolhida a **migração para `docs/ADR/` no formato da skill**, porque o script de auditoria passa
a verificar numeração, chaves, camadas e cadeias em `make check-adr`, e o índice deixa de ser
mantido à mão. Os ADRs 0000 a 0004 mudaram de forma, não de substância; os números foram
mantidos e os nomes de arquivo passaram a dizer a decisão.

## Consequências

- Bom: `make check` acusa ADR sem chave, camada fora do registro, cadeia de supersede de um lado só e índice desatualizado.
- Bom: ADR aceito é imutável; correção vira um registro novo com `supersedes`, e o histórico do raciocínio sobrevive.
- Ruim: a auditoria exige `python3`; sem ele, a verificação é pulada localmente e falha na CI.
- Ruim: a skill vive em `.claude/skills/`, específico do Claude Code; outros agentes seguem só o `docs/ADR/README.md`.
