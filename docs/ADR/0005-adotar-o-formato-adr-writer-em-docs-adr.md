---
status: accepted
date: 2026-10-17
layer: stack
title: "Adotar o formato da skill adr-writer em docs/ADR"
description: "Por que as decisões viram arquivos em docs/ADR com front-matter, camada, ciclo de status e índice gerado, em vez de MADR sem metadados ou documentos narrativos."
supersedes:
superseded-by:
---

# 0005. Adotar o formato da skill adr-writer em docs/ADR

## Contexto e problema

Queremos registrar as decisões de arquitetura e de processo deste repositório para que pessoas e
agentes entendam o porquê de cada escolha e encontrem o registro sem ler o acervo inteiro. A
skill `adr-writer`, versionada em `.claude/skills/`, define um formato com front-matter, camada,
ciclo de status, supersede bidirecional e um script de auditoria que gera o índice. Qual formato
usar?

## Opções consideradas

- **Formato da skill `adr-writer` em `docs/ADR/`** — MADR mínimo com front-matter, `# NNNN.`, `layers.md`, `index.md` gerado e auditoria em `make check`.
- **MADR 4.0 mínimo sem metadados** — padrão conhecido, mas sem status, data nem cadeia de substituição; índice mantido à mão.
- **Documentos narrativos em `docs/`** — sem numeração, sem status, sem supersede.

## Decisão

Escolhido o **formato da skill `adr-writer` em `docs/ADR/`**, porque mantém a estrutura do MADR
mínimo, obriga a listar as opções consideradas e o script de auditoria verifica numeração,
chaves, camadas e cadeias em `make check-adr`, com o índice gerado em vez de mantido à mão.
Títulos de seção e frases fixas em português; chaves e valores do front-matter em inglês.

## Consequências

- Bom: cada decisão fica em um arquivo pequeno e versionado, com o histórico das alternativas rejeitadas.
- Bom: `make check` acusa ADR sem chave, camada fora do registro, cadeia de supersede de um lado só e índice desatualizado.
- Bom: ADR aceito é imutável; correção vira um registro novo com `supersedes`, e o raciocínio original sobrevive.
- Ruim: a auditoria exige `python3`; sem ele, a verificação é pulada localmente e falha na CI.
- Ruim: a skill vive em `.claude/skills/`, específico do Claude Code; outros agentes seguem só o `docs/ADR/README.md`.

## Referências

Consultado em 2026-10-16.

- [MADR](https://adr.github.io/madr/) — formato e conjunto mínimo de seções que a skill estende.
