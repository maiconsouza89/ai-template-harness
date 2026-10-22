---
title: Comprovar a exibição por registro assinado do player
type: adr
number: 0018
status: proposed
date: 2026-10-21
owners: [Maicon Souza]
supersedes: []
superseded_by: []
related: [0011, 0017]
---

# ADR-0018: Comprovar a exibição por registro assinado do player

## Contexto
O repasse e o relatório dependem de provar o que foi exibido. O motivo foi proposto pelo entrevistador e aceito: não exige hardware e é auditável.

## Decisão
O player registra cada inserção exibida e assina o registro. A plataforma valida: duração completa, dentro do período da campanha e do horário ligado da tela, sem duplicidade.

## Alternativas consideradas
- **Foto periódica do exibidor**: descartada. Prós e contras: [A CONFIRMAR: quais?]
- **Captura de tela por amostragem**: descartada. Prós e contras: [A CONFIRMAR: quais?]

## Consequências
### Positivas
- Não exige hardware extra.
- Registros auditáveis, úteis para contestações.

### Negativas e trade-offs
- Lacuna aberta: [A CONFIRMAR: como provar que a TV estava ligada, e não só o player?]
- Exige gestão da chave de assinatura de cada player.
- [A CONFIRMAR: quais são os demais trade-offs?]

## Referências
- [Entrevista de 2026-10-21](../_intake/entrevista-2026-10-21.md).
- RF-008 (Registrar exibições comprovadas).
