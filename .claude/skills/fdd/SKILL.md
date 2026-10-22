---
name: fdd
description: Cria um Feature Design Document em docs/features/ a partir de uma feature ou de um item do roadmap, ligado ao PRD e ao HLD. Use sempre que o usuário quiser desenhar, especificar ou detalhar tecnicamente uma feature, ou disser coisas como "cria o FDD", "documenta o design dessa feature", "como vamos implementar X", "especifica a feature Y".
---

# fdd

## Fluxo
1. Leia `docs/README.md` (convenções da documentação), o PRD em `docs/product/` e o HLD em `docs/architecture/`. Se o PRD não existir, avise e sugira rodar `docs-init` antes; se o usuário quiser seguir mesmo assim, crie o FDD sem o link e marque `prd: [A CONFIRMAR: qual PRD cobre esta feature?]`.
2. Identifique qual ou quais requisitos `RF-NNN` do PRD a feature implementa e se ela já aparece no roadmap. Se aparecer, use o nome de lá. Preencha `requirements` no frontmatter com os IDs e cite o RF no Resumo com link para a seção dele no PRD (`../product/prd-<nome>.md#rf-001-nome`). O FDD herda do RF as capacidades, a experiência e os critérios de aceitação; não os reescreva, detalhe como serão construídos.
3. Faça uma entrevista curta, no máximo 6 perguntas, só sobre o que o PRD e o HLD não respondem: escopo incluído e excluído, mudanças no modelo de dados, APIs ou eventos novos, impactos (segurança, desempenho, migração), estratégia de rollout. Uma pergunta por vez com `AskUserQuestion`, 2 a 4 opções montadas a partir do PRD, do HLD e do código, a recomendada em primeiro lugar com " (Recomendado)" no rótulo e uma frase dizendo por quê; "Outro" fica para resposta livre, "não sei" e "pular". O usuário reage a uma proposta mais rápido e melhor do que escreve do zero.
4. Calcule o próximo número lendo `docs/features/` (3 dígitos, começando em 001) e crie `docs/features/fdd-NNN-<nome-kebab>.md` a partir de `docs/templates/fdd.md`.
5. Preencha o FDD. Use o vocabulário e os nomes de componentes do HLD. Decisões técnicas relevantes tomadas durante a entrevista viram candidatos a ADR: sugira ao usuário criar com a skill `adr`.
6. Atualize `docs/features/README.md` e, se o item existir no roadmap (procure pelos `RF-NNN` na coluna Requisitos), preencha a coluna Docs com o link do FDD.
7. Rode `python3 .claude/skills/docs-init/scripts/validate.py`.

## Regras
- Não remova seções do template. O que não foi respondido fica como `[A CONFIRMAR: ...]`.
- Critérios de aceite no formato "Dado ... quando ... então ...".
- O FDD nasce como `draft`.
- Português do Brasil, frases curtas, sem travessões.
