# Harness para agentes: AGENTS.md, CLAUDE.md e Makefile

## Contexto e problema

Agentes de código começam cada sessão sem memória. O que não está em arquivos versionados não
existe para eles. Precisamos de um ponto de entrada único, lido por qualquer ferramenta, que
aponte para o conhecimento em `docs/` e dê um comando único para validar o trabalho. Referências:
agents.md, documentação de memória do Claude Code, artigos de harness engineering (OpenAI,
Anthropic, Adobe).

## Opções consideradas

| Tema | Escolhida | Alternativas consideradas |
| --- | --- | --- |
| Instruções para agentes | `AGENTS.md` como fonte; `CLAUDE.md` importa com `@AGENTS.md` | Só `CLAUDE.md`; um arquivo por ferramenta com conteúdo duplicado |
| Superfície de comandos | `Makefile` chamando `scripts/*.sh` | Só `scripts/`; Taskfile ou just |
| Conhecimento | `docs/ARCHITECTURE.md`, `SETUP.md`, `TESTING.md` | Só `ARCHITECTURE.md`; tudo dentro de `AGENTS.md` |
| `make check` inicial | hook, fim de linha, sintaxe sh | Só o teste do hook |

## Decisão

Opção escolhida: a coluna "Escolhida" da tabela, porque `AGENTS.md` é o formato aberto lido por
Codex, Cursor, Copilot, Gemini CLI e outros, e o Claude Code o importa sem duplicar conteúdo;
`CLAUDE.md` explícito é necessário porque, havendo `CLAUDE.local.md`, o Claude Code deixa de ler
`AGENTS.md` sozinho. `Makefile` é reconhecido por agentes e CI e mantém a lógica em `sh`
testável. Os três documentos de `docs/` mantêm `AGENTS.md` como mapa, abaixo de 100 linhas,
mesmo quando a stack entrar.

Regra derivada: `AGENTS.md` aponta, `docs/` explica, `Makefile` executa.

### Consequências

* Bom, porque qualquer agente ou pessoa descobre o repositório a partir de dois arquivos na raiz.
* Bom, porque a CI do passo 3 roda `make check`, o mesmo comando usado localmente.
* Ruim, porque `make` precisa estar instalado (WSL ou Git Bash no Windows).
* Ruim, porque o conteúdo importado conta no contexto do Claude Code; `AGENTS.md` deve continuar curto.
