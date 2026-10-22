---
title: Usar Google Places API para pré-preencher o local
type: adr
number: 0012
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: []
---

# ADR-0012: Usar Google Places API para pré-preencher o local

## Contexto
O exibidor cadastra locais e telas. O usuário pediu integrar com a Google Places API para facilitar o cadastro, trazendo os dados pré-preenchidos.

## Decisão
O cadastro de local usa a Google Places API para pré-preencher nome, endereço, coordenadas, categoria, horário e foto. O exibidor edita o que quiser. Se o local não for encontrado, o cadastro é manual.

## Alternativas consideradas
- [A CONFIRMAR: quais alternativas foram consideradas?]

## Consequências
### Positivas
- Cadastro mais rápido, com dados pré-preenchidos.

### Negativas e trade-offs
- Cria dependência externa que trava o RF-002.
- [A CONFIRMAR: quais são os custos e limites de uso da Google Places API?]
- [A CONFIRMAR: quais são os demais trade-offs?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-002 (Cadastrar local e telas).
