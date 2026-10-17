---
status: superseded
date: 2026-10-17
layer: stack
title: "Usar Markdown Architectural Decision Records"
description: "Por que decisões viram arquivos MADR em docs/decisions em vez de ficarem só em documentos narrativos."
supersedes:
superseded-by: "0005"
---

# 0000. Usar Markdown Architectural Decision Records

## Contexto e problema

Queremos registrar as decisões de arquitetura e de processo deste repositório para que pessoas e
agentes entendam o porquê de cada escolha. Qual formato usar?

## Opções consideradas

- **MADR 4.0, template mínimo** — padrão conhecido por ferramentas e agentes, obriga a listar opções.
- **ADR de Michael Nygard** — Título, Status, Contexto, Decisão, Consequências; sem lista de opções.
- **Documentos narrativos em `docs/`** — sem numeração, sem status, sem supersede.

## Decisão

Escolhido o **MADR 4.0, template mínimo**, em `docs/decisions/`, porque é um padrão conhecido,
obriga a listar as opções consideradas e cabe em uma tela. Estrutura do MADR mantida; títulos de
seção e frases fixas em português.

## Consequências

- Bom: cada decisão fica em um arquivo pequeno e versionado.
- Bom: o histórico de alternativas rejeitadas evita rediscutir o mesmo tema.
- Ruim: exige disciplina para criar um ADR a cada decisão relevante.

## Referências

Consultado em 2026-10-16.

- [MADR](https://adr.github.io/madr/) — formato e template mínimo adotados.
