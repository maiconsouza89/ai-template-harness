---
title: Aceitar só Pix como pagamento
type: adr
number: 0021
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: [0015]
---

# ADR-0021: Aceitar só Pix como pagamento

## Contexto
O pagamento da campanha aceita um único meio. A entrevista registra como restrição. [A CONFIRMAR: por que só Pix?]

## Decisão
O pagamento é só via Pix. Ficam fora de escopo cartão, boleto e parcelamento.

## Alternativas consideradas
- Cartão, boleto e parcelamento ficam fora de escopo. Prós e contras: [A CONFIRMAR: quais?]

## Consequências
### Positivas
- [A CONFIRMAR: quais são os ganhos de aceitar só Pix?]

### Negativas e trade-offs
- Pix comum não tem pré-autorização, o que levou ao crédito do não exibido (ADR-0015).
- A plataforma retém e repassa dinheiro de terceiros. [A CONFIRMAR: reter e repassar exige split do PSP ou licença de subcredenciador?]
- [A CONFIRMAR: qual PSP ou banco processa o Pix?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-006 (Pagar campanha via Pix).
