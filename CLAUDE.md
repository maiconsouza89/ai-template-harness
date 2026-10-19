# CLAUDE.md

Instruções para o Claude Code neste repositório. Este arquivo é um mapa: aponta para os
documentos em `docs/`, não os repete. O que o template é e como usá-lo está em `README.md`.
Leia o que a tarefa pedir antes de alterar código.

## Onde está cada coisa

| Precisa de | Leia |
| --- | --- |
| Estrutura do repositório e onde colocar o quê | `docs/ARCHITECTURE.md` |
| Preparar o ambiente | `docs/SETUP.md` |
| O que `make check` valida e como adicionar verificações | `docs/TESTING.md` |
| Fluxo de trabalho, commits, PRs e versões | `CONTRIBUTING.md` |
| Cada padrão, onde vive e a fonte oficial | `docs/STANDARDS.md` |
| Decisões já tomadas e alternativas descartadas | `docs/ADR/` |

## Comandos

Use o `Makefile` como única porta de entrada. Não chame scripts diretamente, salvo para depurar.

```sh
make setup   # uma vez após o clone: ativa os hooks versionados
make check   # roda todas as verificações; deve passar antes de abrir um PR
make help    # lista os alvos
```

- Cada verificação roda sozinha (`make check-hooks`, `make check-adr`, ...; lista em `make help`).
  Para reproduzir a CI, que falha quando shellcheck, actionlint, gitleaks ou python3 faltam em vez
  de pular, rode `CI=true make check`.
- `make lint`, `make format`, `make test` e `make build` seguem o contrato de alvos descrito em
  `docs/TESTING.md`; a CI executa o mesmo `make check`.

## Regras de trabalho

- Branch `<tipo>/<descricao>` a partir de `main`, commits e título do PR em Conventional Commits
  com descrição em português; `main` só recebe PR com squash. O hook `commit-msg`, `make check`
  e a CI validam; as regras completas estão em `CONTRIBUTING.md`.
- Rode `make check` antes de cada commit e de abrir o PR. Se uma verificação falhar, corrija a
  causa; não desative a verificação.
- Mudança que cria ou altera um padrão do repositório exige um ADR novo em `docs/ADR/`
  (formato e regras em `docs/ADR/README.md`). ADR aceito não se edita: um registro novo o
  substitui com `supersedes` e `superseded-by` nos dois lados. `make check-adr` audita e gera o
  `index.md`; inclua o índice regenerado no commit.
- Não edite `CHANGELOG.md` nem `.release-please-manifest.json`: são gerados pelo
  release-please a partir dos commits (`docs/ADR/0004`). A descrição do commit é a
  entrada do changelog, então escreva-a para quem usa o template.
- Documentação em português. Código, nomes de arquivo, tipos e escopos de commit em inglês.
- Texto em UTF-8 com fim de linha LF (`.editorconfig` e `.gitattributes`). Shell em POSIX `sh`,
  sem bashismos.
- Stack por contrato (`docs/ADR/0003`): a stack do projeto vive em `scripts/lint.sh`,
  `format.sh`, `test.sh` e `build.sh`, registrada em um ADR. Ao criar esses scripts, use as
  ferramentas da stack; o `Makefile` e `CLAUDE.md` não mudam.
- Workflows em `.github/workflows/` usam actions fixadas por SHA completo com comentário da
  versão. Ao atualizar, troque o SHA e o comentário juntos.
- Não versione arquivos pessoais; `CLAUDE.local.md` já está no `.gitignore`. Segredos nunca entram no
  repositório (`.gitignore` cobre `.env*` e `*.pem`).

## Específico do Claude Code

- Preferências pessoais não versionadas vão em `CLAUDE.local.md` (já ignorado pelo Git).
- Regras por caminho, quando a stack existir, vão em `.claude/rules/`.
- Para registrar, auditar ou substituir um ADR, use a skill `/adr-writer` (`.claude/skills/adr-writer/`);
  ela segue as regras de `docs/ADR/README.md` e roda o mesmo `audit.py` de `make check-adr`.

## Só no repositório do template

Vale apenas em `ai-template-harness`, não nos projetos gerados a partir dele:

- Nenhuma ferramenta ou dependência de stack entra aqui; o template continua agnóstico.
- Toda convenção nova precisa funcionar em qualquer linguagem e vir com verificação em `make check`.

## Ao terminar uma tarefa

`make check` passa, documentos afetados atualizados e PR aberto com título convencional,
seguindo o checklist de `.github/pull_request_template.md`.
