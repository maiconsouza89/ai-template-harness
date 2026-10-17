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
| Cada padrão, onde vive e a fonte oficial | `docs/STANDARDS.md` |
| Decisões já tomadas e alternativas descartadas | `docs/decisions/` |

## Comandos

Use o `Makefile` como única porta de entrada. Não chame scripts diretamente, salvo para depurar.

```sh
make setup   # uma vez após o clone: ativa os hooks versionados
make check   # roda todas as verificações; deve passar antes de abrir um PR
make help    # lista os alvos
```

Contrato de alvos, igual em qualquer stack: `make lint`, `make format`, `make test`,
`make build`. Cada um roda `scripts/<alvo>.sh` se existir; sem o script, avisa e passa.
`make check` inclui `lint` e `test`; `format` e `build` são manuais. A CI executa o mesmo
`make check` (ver `docs/TESTING.md`).

## Regras de trabalho

- Branch `<tipo>/<descricao>` a partir de `main`, commits e título do PR em Conventional Commits
  com descrição em português; `main` só recebe PR com squash. O hook `commit-msg`, `make check`
  e a CI validam; as regras completas estão em `CONTRIBUTING.md`.
- Rode `make check` antes de cada commit e de abrir o PR. Se uma verificação falhar, corrija a
  causa; não desative a verificação.
- Mudança que cria ou altera um padrão do repositório exige um ADR novo em `docs/decisions/`
  (formato em `docs/decisions/README.md`).
- Não edite `CHANGELOG.md` nem `.release-please-manifest.json`: são gerados pelo
  release-please a partir dos commits (`docs/decisions/0004`). A descrição do commit é a
  entrada do changelog, então escreva-a para quem usa o template.
- Documentação em português. Código, nomes de arquivo, tipos e escopos de commit em inglês.
- Texto em UTF-8 com fim de linha LF (`.editorconfig` e `.gitattributes`). Shell em POSIX `sh`,
  sem bashismos.
- Stack por contrato (`docs/decisions/0003`): a stack do projeto vive em `scripts/lint.sh`,
  `format.sh`, `test.sh` e `build.sh`, registrada em um ADR. Ao criar esses scripts, use as
  ferramentas da stack; o `Makefile` e `AGENTS.md` não mudam.
- Workflows em `.github/workflows/` usam actions fixadas por SHA completo com comentário da
  versão. Ao atualizar, troque o SHA e o comentário juntos.
- Não versione arquivos pessoais; `CLAUDE.local.md` já está no `.gitignore`. Segredos nunca entram no
  repositório (`.gitignore` cobre `.env*` e `*.pem`).

## Só no repositório do template

Vale apenas em `ai-template-harness`, não nos projetos gerados a partir dele:

- Nenhuma ferramenta ou dependência de stack entra aqui; o template continua agnóstico.
- Toda convenção nova precisa funcionar em qualquer linguagem e vir com verificação em `make check`.

## Ao terminar uma tarefa

1. `make check` passa.
2. Documentos afetados atualizados (`docs/`, `CONTRIBUTING.md`, `README.md`, `AGENTS.md`).
3. PR aberto com título convencional e descrição do quê e do porquê.
