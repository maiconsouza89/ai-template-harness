---
title: Adotar monólito modular com player separado
type: adr
number: 0020
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: []
---

# ADR-0020: Adotar monólito modular com player separado

## Contexto
O MVP precisa sair com um time pequeno. O motivo foi proposto pelo entrevistador e aceito: entrega mais rápida. O player fica separado porque roda na TV. Stack ainda não decidida.

## Decisão
Adotar monólito modular para web e API, com módulos de contas, locais e telas, campanhas, moderação, pagamentos, exibições e repasses e crédito. O player é um componente separado. Jobs agendados leem o mesmo banco relacional.

## Alternativas consideradas
- **Microsserviços**: descartada. Prós e contras: [A CONFIRMAR: quais?]
- **Backend como serviço (Firebase ou Supabase)**: descartada. Prós e contras: [A CONFIRMAR: quais?]

## Consequências
### Positivas
- Entrega mais rápida no MVP para um time pequeno.
- Banco relacional único para dinheiro e estados.

### Negativas e trade-offs
- Os módulos precisam de fronteiras claras para permitir separação futura.
- Pendente: [A CONFIRMAR: linguagem, framework, banco, cloud e PSP Pix]
- Pendente: [A CONFIRMAR: plataforma do player]
- [A CONFIRMAR: quais são os demais trade-offs?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- Seção Arquitetura da entrevista.
