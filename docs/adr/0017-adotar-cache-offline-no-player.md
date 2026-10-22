---
title: Adotar cache offline no player
type: adr
number: 0017
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: [0018]
---

# ADR-0017: Adotar cache offline no player

## Contexto
O wi-fi de bar e academia oscila. Sem cache, o exibidor perde receita. O motivo foi proposto pelo entrevistador e aceito pelo usuário.

## Decisão
O player guarda em cache local a programação e os criativos das próximas 24 h (hipótese aceita) e segue exibindo quando a internet cai.

## Alternativas consideradas
- **Só online (streaming)**: descartada. Prós e contras: [A CONFIRMAR: quais?]

## Consequências
### Positivas
- A exibição continua com a internet fora, o que protege o repasse do exibidor.

### Negativas e trade-offs
- O player ganha complexidade de sincronização e de armazenamento local.
- Cache vencido sem internet exibe conteúdo padrão. [A CONFIRMAR: o conteúdo padrão é anúncio da plataforma, do exibidor ou tela preta?]
- [A CONFIRMAR: quais são os demais trade-offs?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-007 (Exibir campanha na tela).
