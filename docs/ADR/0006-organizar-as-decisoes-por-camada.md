---
status: accepted
date: 2026-10-17
layer: stack
title: "Organizar as decisões nas camadas workflow, harness, ci e release"
description: "Por que o template é descrito em quatro camadas trocáveis, em vez de uma lista linear de decisões."
supersedes:
superseded-by:
---

# 0006. Organizar as decisões nas camadas workflow, harness, ci e release

## Contexto e problema

O formato adotado no ADR 0005 exige que cada registro declare a camada a que pertence, e o
registro `layers.md` só cresce por ADR `stack`. O template não tem stack de linguagem; suas
camadas são as partes que um projeto gerado pode trocar sem afetar as outras.

## Opções consideradas

- **Quatro camadas: `workflow`, `harness`, `ci`, `release`** — uma por parte trocável do template.
- **Uma camada só (`template`)** — equivale a não ter camada; o índice vira lista linear.
- **Camadas por arquivo (`git`, `hooks`, `makefile`, `workflows`, ...)** — granulares demais; uma decisão quase sempre toca várias.

## Decisão

Escolhidas as **quatro camadas**, porque cada uma pode ser substituída por outra ferramenta sem
tocar nas demais (trocar release-please por cocogitto não muda o hook nem o `AGENTS.md`), e os
ADRs existentes caem em exatamente uma delas: 0001 em `workflow`, 0002 em `harness`, 0003 em
`ci`, 0004 em `release`.

## Consequências

- Bom: `index.md` responde "o que já foi decidido sobre release?" sem ler o acervo inteiro.
- Bom: um projeto gerado que adota uma stack cria a camada dela por um ADR `stack`, sem mexer nestas.
- Ruim: decisão que cruza camadas (ex.: CI validando o título do PR) tem que escolher uma; a escolha fica registrada no ADR.
