---
title: Repassar 70% ao exibidor pelo exibido
type: adr
number: 0011
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: [0015, 0018, 0019]
---

# ADR-0011: Repassar 70% ao exibidor pelo exibido

## Contexto
O anunciante paga via Pix, a plataforma retém 30% e repassa 70% ao exibidor. O usuário quer que o repasse seja "proporcional ao que foi exibido de verdade, não ao que foi prometido".

## Decisão
O exibidor recebe 70% do valor das inserções comprovadas e a plataforma retém 30%. O repasse não depende do que foi vendido, só do que foi exibido de verdade.

## Alternativas consideradas
- [A CONFIRMAR: quais alternativas foram consideradas?]

## Consequências
### Positivas
- O exibidor é pago pelo que de fato exibiu.
- O repasse é auditável pelos registros de exibição.

### Negativas e trade-offs
- Exige prova de exibição confiável (ADR-0018) e fechamento de contas por período.
- [A CONFIRMAR: quais são os demais trade-offs do modelo?]
- Pendência relacionada: [A CONFIRMAR: reter e repassar exige split do PSP ou licença de subcredenciador?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-009 (Repassar 70% ao exibidor pelo exibido).
- RF-008 (Registrar exibições comprovadas).
