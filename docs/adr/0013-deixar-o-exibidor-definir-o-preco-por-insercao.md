---
title: Deixar o exibidor definir o preço por inserção
type: adr
number: 0013
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: []
---

# ADR-0013: Deixar o exibidor definir o preço por inserção

## Contexto
Cada tela precisa de um preço por inserção. O usuário decidiu na rodada do RF-004 que o preço é definido pelo exibidor, por tela, com piso da plataforma. [A CONFIRMAR: por que o exibidor define o preço?]

## Decisão
O exibidor define o preço por inserção de cada tela, não abaixo do piso da plataforma. O preço fica gravado na campanha no momento da compra.

## Alternativas consideradas
- **Tabela única definida pela plataforma**: era a opção recomendada. Descartada. Prós e contras: [A CONFIRMAR: quais?]
- **Pacotes fechados**: descartada. Prós e contras: [A CONFIRMAR: quais?]

## Consequências
### Positivas
- [A CONFIRMAR: quais são os ganhos do preço definido pelo exibidor?]
- O preço gravado na campanha serve de base para o repasse.

### Negativas e trade-offs
- Exige definir um piso. [A CONFIRMAR: qual é o valor do piso por inserção?]
- [A CONFIRMAR: quais são os demais trade-offs?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-002 (Cadastrar local e telas).
- RF-004 (Criar campanha com criativo).
