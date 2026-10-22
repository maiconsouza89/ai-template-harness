---
title: Estruturar o PRD por requisitos rastreáveis e derivar a ordem de execução no roadmap
type: adr
number: 0009
status: proposed
date: 2026-10-21
layer: harness
owners: [mantenedores do template]
supersedes: []
superseded_by: []
related: [0007]
---

# ADR-0009: Estruturar o PRD por requisitos rastreáveis e derivar a ordem de execução no roadmap

## Contexto
O ADR 0007 substituiu as skills `prd-writer`, `hld-writer` e `adr-writer` pelo sistema `docs-init`.
Na troca, o template de PRD passou a ter dez seções genéricas: um requisito era um bullet, sem ID
usado fora da própria lista, sem contrato com os outros requisitos, sem dependências e sem critérios
de aceitação. A entrevista não tinha rodada de requisitos, o agente `prd-writer` não validava nada e
o `validate.py` só olhava frontmatter, links e numeração. Um PRD assim não serve ao propósito do
harness, que é permitir que pessoas e agentes implementem um requisito de cada vez sabendo o que ele
consome, o que fornece e quando pode começar. A versão anterior da skill `prd-writer` (v0.6.0) já
tinha esse formato, adaptado de uma referência em nove seções com IDs, contratos Consome/Fornece,
tabela de dependências, ondas de execução e arquivo de progresso.

## Decisão
O PRD em `docs/product/` tem nove seções fixas: resumo executivo, problema e oportunidade,
público-alvo, objetivos e métricas (com os requisitos não funcionais), histórias de usuário,
requisitos funcionais, fora de escopo, dependências entre requisitos e critérios de aceitação. Cada
requisito funcional tem um ID `RF-NNN` imutável, usado nas seções 5, 6, 8 e 9, e blocos fixos:
Consome, Fornece, Escopo mínimo, Adições de escopo completo, Capacidades, Experiência e Tratamento
de erros. A seção 8 guarda só o que é propriedade do requisito: tabela topológica com prioridade e
"Depende de", requisitos de fundação e dependências externas. O que é ordem de construção (ondas,
caminho crítico e diagrama Mermaid) vive no roadmap, na seção "Ordem de execução", gerada por
`prd_checks.py --ondas` a partir da tabela do PRD. Número operacional que o usuário não deu pode
ser proposto com a marca `(hipótese)`, só em Capacidades e Tratamento de erros; tudo o mais que falta
continua marcado como A CONFIRMAR. A entrevista da skill `docs-init` ganha rodadas de escopo, um
requisito por vez, contratos, aceitação e roadmap, em que a skill propõe e o usuário confirma. O
`validate.py`, via `prd_checks.py`, valida o conteúdo do PRD e a coerência do roadmap com ele em
`make check-docs`, e o smoke test cobre fixtures válidas e mutações que precisam falhar.

## Alternativas consideradas
- **Seção 8 completa no PRD, como na referência**: um só arquivo para o agente ler, mas o PRD mistura
  o que o produto faz com a ordem de construção, e o roadmap repete parte disso.
- **Tudo no roadmap, PRD só com Consome/Fornece**: menos duplicação, mas a dependência de
  infraestrutura (acesso, cadastro base) não aparece em Consome e ficaria sem casa no PRD, que é o
  documento que sobrevive ao arquivamento do roadmap.
- **Manter o template genérico e detalhar só em FDDs**: menos entrevista, mas o FDD chega sem
  contrato entre requisitos e sem ordem, e cada FDD redescobre as dependências.
- **Inferir detalhes sem marcar, como a referência**: PRD mais completo na primeira versão, mas o
  leitor não distingue fato de suposição, contra a regra de lacunas explícitas do ADR 0007.
- **Restaurar também o `prd_progress.json`**: adiado até existir uma skill de implementação que o
  consuma; a seção 8 já tem tudo que ele precisa e o script anterior está no histórico do Git.

## Consequências
### Positivas
- O PRD passa a ser executável requisito por requisito: cada RF diz o que consome, o que fornece,
  do que depende e como se verifica, e a integração entre RFs tem critério próprio.
- Ondas e caminho crítico são derivados mecanicamente da tabela, nunca calculados de cabeça, e a
  validação acusa roadmap desatualizado em relação ao PRD.
- Hipóteses e lacunas são distinguíveis no texto e contadas pela validação.

### Negativas e trade-offs
- `prd_checks.py` acrescenta cerca de 750 linhas de Python ao harness, todas em biblioteca padrão.
- A entrevista fica mais longa: uma pergunta por requisito, mais as rodadas de contratos e aceitação.
- Projetos já gerados precisam rodar `scaffold.py --force` para atualizar `docs/templates/` e
  migrar o PRD existente para as nove seções; o validador recusa o formato antigo.
- A regra de origem fica com duas marcas (A CONFIRMAR e `(hipótese)`) em vez de uma.

## Referências
- [Convenções da documentação](../README.md), seções "Regras por tipo" e "Lacunas".
- [ADR 0007](0007-adotar-o-sistema-de-documentacao-docs-init-em-docs.md), que criou o sistema
  `docs-init`.
- Skill `prd-writer` v0.6.0 (commit `eea9ba9`), origem do formato de nove seções e dos scripts
  portados para `prd_checks.py`.
