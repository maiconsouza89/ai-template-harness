---
status: accepted
date: AAAA-MM-DD
layer: stack
title: "Usar ADRs para decisões de arquitetura"
description: "Por que decisões caras de reverter viram arquivo em docs/ADR em vez de ficarem no histórico de conversa."
supersedes:
superseded-by:
---

# 0001. Usar ADRs para decisões de arquitetura

## Contexto e problema

O DevFlow-AI é montado como stack: cada camada é escolhida, e a escolha exclui alternativas.
Conversa de sessão não persiste e histórico do git não é lido para entender motivo, então
seis meses depois ninguém sabe por que a camada X ficou com a ferramenta Y — e a alternativa
já descartada volta à mesa. Faltava um lugar onde a decisão e o que foi recusado ficassem
juntos, versionados com o código.

## Opções consideradas

- **ADRs em `docs/ADR/`** — um arquivo Markdown numerado por decisão, versionado com o código, formato MADR-minimal.
- **Uma página só de decisões** — arquivo único que cresce; sem numeração, sem status, sem como supersedir uma entrada.
- **Nada formal** — decisões ficam em issues, PRs e conversa; recuperar o motivo depende de quem estava lá.

## Decisão

Escolhidos os **ADRs em `docs/ADR/`**, porque numeração estável dá referência cruzada, o
status dá o ciclo de vida (incluindo supersede bidirecional) e um arquivo por decisão
mantém cada registro dentro de um orçamento de leitura. Cada ADR declara também a camada
da stack a que pertence, no campo `layer`.

## Consequências

- Bom: para saber por que uma camada é o que é, basta `grep` em `docs/ADR/` — o motivo e as opções recusadas estão no mesmo arquivo.
- Bom: `scripts/audit.py` valida numeração, front-matter, camada e cadeias de supersede, então inconsistência aparece em comando e não em revisão manual.
- Ruim: toda decisão cara de reverter passa a custar um arquivo a mais; decisão trivial registrada infla o acervo e o acervo inflado deixa de ser lido.
- Ruim: ADR `accepted` tem texto congelado — corrigir conteúdo exige escrever um ADR novo que o supersede, não editar o antigo.

## Referências

Consultado em AAAA-MM-DD.

- [MADR — Markdown Any Decision Records](https://adr.github.io/madr/) — formato e conjunto mínimo de seções adotados aqui.
