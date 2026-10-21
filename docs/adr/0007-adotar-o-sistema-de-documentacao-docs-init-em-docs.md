---
title: Adotar o sistema de documentação docs-init em docs
type: adr
number: 0007
status: accepted
date: 2026-10-21
layer: harness
owners: [mantenedores do template]
supersedes: [0005]
superseded_by: []
related: []
---

# ADR-0007: Adotar o sistema de documentação docs-init em docs

## Contexto
O repositório tinha três skills independentes em `.claude/skills/`: `adr-writer` (ADRs em `docs/ADR/`
com camada, `index.md` gerado e `audit.py` em `make check-adr`), `prd-writer` (`docs/PRD.md` com
`prd_progress.json`) e `hld-writer` (`docs/HLD.md`). Cada uma tinha o próprio template, a própria
entrevista e o próprio validador, somando mais de quatro mil linhas, e nenhuma cobria FDD, roadmap,
runbooks ou guias. Um projeto gerado a partir do template precisa de uma única forma de documentar
produto, arquitetura, decisões e features, com uma única validação em `make check`.

## Decisão
Substituir as três skills por um sistema de documentação em `docs/`, organizado por tipo
(`product/`, `architecture/`, `adr/`, `features/`, `runbooks/`, `guides/`, `templates/`, `_intake/`),
com a skill `docs-init` (entrevista e geração via subagents `prd-writer`, `architecture-writer`,
`adr-extractor` e `docs-reviewer`), as skills `adr`, `fdd` e `docs-review`, e um só validador
(`validate.py`) rodado por `make check-docs`. Os ADRs existentes migram para `docs/adr/` mudando
apenas o front-matter; o corpo dos registros aceitos fica intacto.

## Alternativas consideradas
- **Manter as três skills e só adicionar FDD e roadmap**: menos mudança agora, mas quatro validadores, quatro entrevistas e três lugares para a mesma regra de front-matter.
- **Manter `docs/ADR/` no formato antigo e adotar o sistema novo só para o resto**: dois formatos de ADR no mesmo repositório, dois índices e duas auditorias.
- **Sistema único em `docs/` com skills e subagents (escolhida)**: um template por tipo, um validador, lacunas explícitas marcadas como A CONFIRMAR, e subagents que escrevem a partir de uma entrevista registrada em `docs/_intake/`.

## Consequências
### Positivas
- Um só validador cobre front-matter, links, numeração de ADRs e FDDs e itens do roadmap sem documento.
- A documentação deixa explícito o que falta: tudo que não foi respondido fica marcado como A CONFIRMAR, e a validação conta as marcas.
- FDD, roadmap, runbooks e guias passam a ter lugar e modelo.
- Os scripts são idempotentes e testados em `make check-docs`, então o projeto gerado pode rodar o scaffold mais de uma vez.

### Negativas e trade-offs
- Python 3 continua necessário para a validação; sem ele, o check é pulado localmente e falha na CI.
- Skills e subagents são específicos do Claude Code; outros agentes seguem só `docs/README.md` e as convenções.
- Os ADRs 0001 a 0006 mantêm o H1 `# NNNN.` do formato anterior, enquanto os novos usam `# ADR-NNNN:`.
- O índice de ADRs volta a ser mantido pelo script `new_adr.py` em vez de regenerado em cada check.

## Referências
- [Convenções da documentação](../README.md) e `.claude/skills/docs-init/references/convencoes.md`.
- [ADR 0005](0005-adotar-o-formato-adr-writer-em-docs-adr.md), substituído por este registro.
