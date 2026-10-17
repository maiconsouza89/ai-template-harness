# AGENTS.md

Instruções para agentes de código (Claude Code, Codex, Cursor, Copilot, Gemini CLI e outros).
Este arquivo é um mapa: aponta para os documentos em `docs/`, não os repete. Leia o que a tarefa
pedir antes de alterar código.

## O que é este repositório

Template para desenvolvimento assistido por IA. Convenções viram arquivos versionados e, sempre
que possível, verificação automática. O que não está no repositório não existe para o agente.

## Onde está cada coisa

| Precisa de | Leia |
| --- | --- |
| Estrutura do repositório e onde colocar o quê | `docs/ARCHITECTURE.md` |
| Preparar o ambiente | `docs/SETUP.md` |
| O que `make check` valida e como adicionar verificações | `docs/TESTING.md` |
| Fluxo de trabalho, commits, PRs e versões | `CONTRIBUTING.md` |
| Por que cada padrão existe, com fontes | `docs/01-fundacao-git-e-padroes.md` |
| Decisões já tomadas e alternativas descartadas | `docs/decisions/` |

## Comandos

Use o `Makefile` como única porta de entrada. Não chame scripts diretamente, salvo para depurar.

```sh
make setup   # uma vez após o clone: ativa os hooks versionados
make check   # roda todas as verificações; deve passar antes de abrir um PR
make help    # lista os alvos
```

## Regras de trabalho

- Trabalhe em um branch a partir de `main`. `main` só recebe mudanças por pull request com
  squash. Nunca faça push direto em `main`.
- Commits no formato Conventional Commits: tipos em inglês (`feat`, `fix`, `docs`...), descrição
  em português, minúsculas, até 72 caracteres, sem ponto final. O hook `commit-msg` rejeita o
  que não segue. O título do PR segue a mesma regra.
- Rode `make check` antes de cada commit e de abrir o PR. Se uma verificação falhar, corrija a
  causa; não desative a verificação.
- Mudança que cria ou altera um padrão do repositório exige um ADR novo em `docs/decisions/`
  (formato em `docs/01-fundacao-git-e-padroes.md` §4.7) e uma linha em `CHANGELOG.md` sob
  `[Unreleased]`, quando afetar quem usa o template.
- Documentação em português. Código, nomes de arquivo, tipos e escopos de commit em inglês.
- Texto em UTF-8 com fim de linha LF (`.editorconfig` e `.gitattributes`). Shell em POSIX `sh`,
  sem bashismos.
- Não adicione dependências de linguagem ou ferramentas de stack: a stack ainda não foi definida
  (ver `docs/decisions/0001`). Proponha em um ADR primeiro.
- Não crie `CLAUDE.local.md` nem arquivos pessoais versionados. Segredos nunca entram no
  repositório (`.gitignore` cobre `.env*` e `*.pem`).

## Ao terminar uma tarefa

1. `make check` passa.
2. Documentos afetados atualizados (`docs/`, `CONTRIBUTING.md`, `CHANGELOG.md`).
3. PR aberto com título convencional e descrição do quê e do porquê.
