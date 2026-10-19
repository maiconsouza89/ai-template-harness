---
status: accepted
date: 2026-10-16
layer: harness
title: "Usar CLAUDE.md como fonte única e Makefile como interface"
description: "Por que as instruções para agentes vivem só em CLAUDE.md, com Makefile como porta de entrada, em vez de AGENTS.md importado ou arquivos duplicados."
supersedes:
superseded-by:
---

# 0002. Usar CLAUDE.md como fonte única e Makefile como interface

## Contexto e problema

Agentes de código começam cada sessão sem memória: o que não está em arquivos versionados não
existe para eles. Precisamos de um ponto de entrada único, lido por qualquer ferramenta, que
aponte para o conhecimento em `docs/` e dê um comando único para validar o trabalho.

## Opções consideradas

- **Só `CLAUDE.md`** — um arquivo, lido pelo Claude Code; os outros agentes não leem.
- **`AGENTS.md` como fonte, `CLAUDE.md` importa com `@AGENTS.md`** — formato aberto lido por Codex, Cursor, Copilot, Gemini CLI; dois arquivos na raiz para manter.
- **Um arquivo por ferramenta** — mesmo conteúdo copiado; diverge com o tempo.
- **Superfície de comandos**: `Makefile` chamando `scripts/*.sh` (escolhida) contra só `scripts/` ou Taskfile/just.

## Decisão

Escolhida a opção **só `CLAUDE.md`**, mais `Makefile` chamando `scripts/*.sh` e
`docs/ARCHITECTURE.md`, `SETUP.md` e `TESTING.md` como conhecimento, porque o Claude Code é a
ferramenta usada, um arquivo só na raiz elimina a dupla `AGENTS.md` + import, e `make check` é
reconhecido por agentes e CI mantendo a lógica em `sh` testável. Regra derivada: `CLAUDE.md`
aponta, `docs/` explica, `Makefile` executa.

## Consequências

- Bom: agente ou pessoa descobre o repositório a partir de `CLAUDE.md` e `README.md` na raiz.
- Bom: a CI roda `make check`, o mesmo comando usado localmente.
- Ruim: `make` precisa estar instalado (WSL ou Git Bash no Windows).
- Ruim: Codex, Cursor, Copilot e Gemini CLI não leem `CLAUDE.md`; quem usar outro agente precisa apontá-lo para o arquivo.
- Ruim: o conteúdo conta no contexto do Claude Code; `CLAUDE.md` deve continuar curto.

## Referências

Consultado em 2026-10-16.

- [Claude Code: memória do projeto](https://code.claude.com/docs/en/memory) — o que o Claude Code carrega da raiz do projeto e como `CLAUDE.local.md` se soma.
