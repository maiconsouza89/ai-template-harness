---
title: Adotar repasse semanal
type: adr
number: 0019
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: [0011]
---

# ADR-0019: Adotar repasse semanal

## Contexto
O pequeno exibidor precisa ver o dinheiro cedo para confiar na plataforma. O motivo foi proposto pelo entrevistador e aceito pelo usuário.

## Decisão
O repasse tem fechamento semanal, de segunda 00h a domingo 23h59, e pagamento por Pix até D+2 úteis após o fechamento. Esses números são hipóteses aceitas. [A CONFIRMAR: prazo do repasse]

## Alternativas consideradas
- **Mensal**: descartada. Prós e contras: [A CONFIRMAR: quais?]
- **Ao fim da campanha**: descartada. Prós e contras: [A CONFIRMAR: quais?]

## Consequências
### Positivas
- O exibidor recebe com frequência, o que reforça a confiança.

### Negativas e trade-offs
- Mais pagamentos e mais custo operacional. Por isso, saldo abaixo de R$ 20 (hipótese) acumula para a semana seguinte.
- [A CONFIRMAR: quais são os demais trade-offs?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-009 (Repassar 70% ao exibidor pelo exibido).
