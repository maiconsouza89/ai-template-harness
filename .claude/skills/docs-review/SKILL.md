---
name: docs-review
description: Audita a documentação em docs/: frontmatter, links quebrados, numeração de ADRs e FDDs, itens do roadmap sem documento, contradições entre documentos, lacunas marcadas como A CONFIRMAR e documentos desatualizados. Use sempre que o usuário pedir para revisar, auditar, validar ou conferir a documentação, ou perguntar "o que está faltando nos docs", "a documentação está atualizada?", ou antes de uma release.
---

# docs-review

## Fluxo
1. Rode `python3 .claude/skills/docs-init/scripts/validate.py` e guarde a saída.
2. Rode o subagent `docs-reviewer` sobre `docs/`, passando a saída do validate como contexto para ele não repetir o que já foi apontado.
3. Verifique datas: liste documentos cujo `date` (ou `updated`, no roadmap) tenha mais de 90 dias e status diferente de `archived`, `deprecated` ou `superseded`.
4. Verifique consistência de status: PRD `approved` com FDDs todos `draft`, FDD `implemented` com PRD `draft`, ADR `accepted` sem referência em nenhum HLD ou FDD.

## Relatório
Entregue em quatro blocos, nesta ordem:
1. Erros (bloqueiam): saída do validate.
2. Contradições: apontadas pelo docs-reviewer, com os dois arquivos envolvidos.
3. Lacunas: todos os `[A CONFIRMAR]`, agrupados por documento.
4. Sugestões: documentos desatualizados, status incoerentes, ADRs órfãos.

Ao final, pergunte se o usuário quer corrigir os erros agora. Não altere nenhum documento sem confirmação. Português do Brasil, frases curtas, sem travessões.
