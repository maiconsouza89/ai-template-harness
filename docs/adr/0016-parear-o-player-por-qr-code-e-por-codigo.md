---
title: Parear o player por QR Code e por código
type: adr
number: 0016
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: []
---

# ADR-0016: Parear o player por QR Code e por código

## Contexto
O player na TV precisa ser vinculado a uma tela cadastrada. Motivo do usuário: "na maioria dos casos o exibidor estará conectado pelo celular".

## Decisão
O player mostra um QR Code e um código de 6 caracteres ao mesmo tempo. O exibidor lê o QR no celular logado ou digita o código na tela cadastrada. QR e código expiram em 10 min (hipótese aceita).

## Alternativas consideradas
- [A CONFIRMAR: quais alternativas foram consideradas?]

## Consequências
### Positivas
- Pareamento simples pelo celular, que o exibidor já usa.
- O código serve quando não dá para ler o QR.

### Negativas e trade-offs
- Depende de a plataforma do player poder exibir QR Code. [A CONFIRMAR: o player roda em Android TV, Smart TV ou navegador?]
- [A CONFIRMAR: quais são os demais trade-offs?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-003 (Parear tela com o player).
