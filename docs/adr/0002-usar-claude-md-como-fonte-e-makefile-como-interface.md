---
status: accepted
type: adr
number: 0002
date: 2026-10-19
layer: harness
title: "Usar CLAUDE.md como fonte única e Makefile como interface"
description: "Por que as instruções para agentes vivem só em CLAUDE.md, com Makefile como porta de entrada, em vez de AGENTS.md importado ou arquivos duplicados."
owners: [mantenedores do template]
supersedes: []
superseded_by: []
related: []
---

# 0002. Usar CLAUDE.md como fonte única e Makefile como interface

## Contexto e problema

Agentes de código começam cada sessão sem memória: o que não está em arquivos versionados não
existe para eles. O Claude Code é a ferramenta usada neste repositório. Precisamos de um ponto
de entrada único, carregado por ele no início de cada sessão, que aponte para o conhecimento em
`docs/` e dê um comando único para validar o trabalho. A versão anterior desta decisão mantinha
`AGENTS.md` como fonte importada por `CLAUDE.md`; os dois arquivos duplicavam a porta de entrada.

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

Consultado em 2026-10-19.

- [Claude Code: memória do projeto](https://code.claude.com/docs/en/memory) — `CLAUDE.md` e `CLAUDE.local.md` são carregados da raiz no início da sessão; imports `@path` também contam no contexto; alvo de menos de 200 linhas por arquivo.
