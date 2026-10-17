---
status: accepted
date: 2026-10-16
layer: harness
title: "Usar AGENTS.md como fonte única e Makefile como interface"
description: "Por que as instruções para agentes vivem em AGENTS.md importado por CLAUDE.md, com Makefile como porta de entrada, em vez de só CLAUDE.md ou arquivos duplicados."
supersedes:
superseded-by:
---

# 0002. Usar AGENTS.md como fonte única e Makefile como interface

## Contexto e problema

Agentes de código começam cada sessão sem memória: o que não está em arquivos versionados não
existe para eles. Precisamos de um ponto de entrada único, lido por qualquer ferramenta, que
aponte para o conhecimento em `docs/` e dê um comando único para validar o trabalho.

## Opções consideradas

- **`AGENTS.md` como fonte, `CLAUDE.md` importa com `@AGENTS.md`** — formato aberto lido por Codex, Cursor, Copilot, Gemini CLI; sem duplicação.
- **Só `CLAUDE.md`** — simples se o Claude Code for a única ferramenta; os outros agentes não leem.
- **Um arquivo por ferramenta** — mesmo conteúdo copiado; diverge com o tempo.
- **Superfície de comandos**: `Makefile` chamando `scripts/*.sh` (escolhida) contra só `scripts/` ou Taskfile/just.

## Decisão

Escolhida a opção **`AGENTS.md` como fonte com `CLAUDE.md` importando**, mais `Makefile` chamando
`scripts/*.sh` e `docs/ARCHITECTURE.md`, `SETUP.md` e `TESTING.md` como conhecimento, porque
qualquer agente lê `AGENTS.md`, o Claude Code o importa sem duplicar, e `make check` é reconhecido
por agentes e CI mantendo a lógica em `sh` testável. `CLAUDE.md` explícito é necessário porque,
havendo `CLAUDE.local.md`, o Claude Code deixa de ler `AGENTS.md` sozinho. Regra derivada:
`AGENTS.md` aponta, `docs/` explica, `Makefile` executa.

## Consequências

- Bom: qualquer agente ou pessoa descobre o repositório a partir de dois arquivos na raiz.
- Bom: a CI roda `make check`, o mesmo comando usado localmente.
- Ruim: `make` precisa estar instalado (WSL ou Git Bash no Windows).
- Ruim: o conteúdo importado conta no contexto do Claude Code; `AGENTS.md` deve continuar curto.

## Referências

Consultado em 2026-10-16.

- [AGENTS.md](https://agents.md/) — formato aberto e lista de ferramentas que o leem.
- [Claude Code: memória do projeto](https://code.claude.com/docs/en/memory) — sintaxe `@path` de import e quando `AGENTS.md` é lido sem `CLAUDE.md`.
