---
title: Converter o valor não exibido em crédito
type: adr
number: 0015
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: [0011, 0021]
---

# ADR-0015: Converter o valor não exibido em crédito

## Contexto
O anunciante paga antes da exibição e o repasse é pelo exibido. Sobra valor pago que não foi exibido. O motivo foi proposto pelo entrevistador e aceito: fecha a conta com o repasse pelo exibido e mantém o dinheiro na rede.

## Decisão
O valor pago e não exibido vira crédito na conta do anunciante, usado nos próximos pagamentos. O crédito cobre a campanha toda ou em parte.

## Alternativas consideradas
- **Estorno Pix ao fim**: descartada. Prós e contras: [A CONFIRMAR: quais?]
- **Cobrar só o exibido**: descartada. Pix comum não tem pré-autorização.

## Consequências
### Positivas
- O anunciante não perde dinheiro pelo que não foi exibido.
- O dinheiro permanece na rede.

### Negativas e trade-offs
- Exige controle de saldo de crédito por conta.
- [A CONFIRMAR: o crédito expira ou pode ser resgatado em dinheiro?]
- [A CONFIRMAR: quais são os demais trade-offs?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-012 (Gerar e usar crédito do não exibido).
- RF-010 (Acompanhar resultados da campanha).
