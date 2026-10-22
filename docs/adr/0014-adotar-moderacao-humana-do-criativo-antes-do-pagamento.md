---
title: Adotar moderação humana do criativo antes do pagamento
type: adr
number: 0014
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: [0021]
---

# ADR-0014: Adotar moderação humana do criativo antes do pagamento

## Contexto
O criativo aparece em local público de terceiros. Pagar só depois de aprovar evita estorno por reprovação. O motivo foi proposto pelo entrevistador e aceito pelo usuário.

## Decisão
O admin da plataforma modera cada criativo antes do pagamento. A campanha só vai a pagamento depois de aprovada.

## Alternativas consideradas
- **Aprovação também pelo exibidor**: descartada. Prós e contras: [A CONFIRMAR: quais?]
- **Moderação automática**: descartada. Prós e contras: [A CONFIRMAR: quais?]

## Consequências
### Positivas
- Controle do conteúdo exibido em local público.
- Sem estorno por reprovação, porque o pagamento vem depois da aprovação.

### Negativas e trade-offs
- A moderação humana limita a escala e exige decisão em até 24 h úteis (hipótese aceita).
- Evolução prevista: moderação por IA, sem prazo definido.
- [A CONFIRMAR: quais são as regras de conteúdo vetado?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-005 (Moderar criativo).
- RF-006 (Pagar campanha via Pix).
