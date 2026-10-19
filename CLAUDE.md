# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Template de repositório, agnóstico de stack, para desenvolvimento assistido por IA. Regra do
harness: `CLAUDE.md` aponta, `docs/` explica, `Makefile` executa. Este arquivo é um mapa, não um
manual; leia o documento que a tarefa pedir antes de alterar código.

## Comandos

O `Makefile` é a única porta de entrada. Não chame `scripts/` diretamente, salvo para depurar.

```sh
make setup           # uma vez após o clone: ativa os hooks de .githooks/ via core.hooksPath
make check           # todas as verificações; a CI roda exatamente este alvo
make check-<nome>    # uma verificação isolada (check-hooks, check-adr, ...; lista em make help)
CI=true make check   # reproduz a CI: falha se shellcheck, actionlint, gitleaks ou python3 faltarem
make lint|format|test|build   # contrato da stack: roda scripts/<alvo>.sh se existir, senão avisa e passa
```

## Como o harness funciona

- **Verificações.** Cada alvo `check-*` chama um `scripts/checks/check-*.sh` em POSIX `sh` com
  `set -eu`; `make check` agrega todos e `.github/workflows/ci.yml` roda o mesmo alvo. Para
  adicionar uma: script, alvo com comentário `##` no `Makefile`, dependência de `check` e linha
  na tabela de `docs/TESTING.md`.
- **Hook `commit-msg`.** Vive em `.githooks/` e é testado por `scripts/tests/test-commit-msg.sh`
  (`make check-hooks`). Antes de mudar o hook, acrescente um caso aceito e um rejeitado.
- **Stack por contrato** (`docs/ADR/0003`). `scripts/contract.sh` despacha `lint`, `format`,
  `test` e `build` para `scripts/<alvo>.sh`. O projeto gerado cria esses scripts e registra a
  stack em um ADR; `Makefile` e `CLAUDE.md` não mudam.
- **Release automática** (`docs/ADR/0004`). O release-please gera `CHANGELOG.md` e
  `.release-please-manifest.json` a partir dos commits; não edite nenhum dos dois. Só `feat`,
  `fix`, `perf` e `revert` geram versão, e a descrição do commit vira a entrada do changelog.
- **ADRs** em `docs/ADR/` (regras em `docs/ADR/README.md`): front-matter com status, data e
  camada válida em `layers.md`; `index.md` é gerado. `make check-adr` roda o `audit.py` da skill
  `.claude/skills/adr-writer/` e falha se o índice estava desatualizado, então inclua o índice
  regenerado no commit. Use `/adr-writer` para criar, auditar ou substituir um ADR.

## Regras

- Branch `<tipo>/<descricao>` a partir de `main`, com os tipos do commit (`make check-branch`).
  Commits e título do PR em Conventional Commits: tipo e escopo em inglês, descrição em
  português, cabeçalho até 72 caracteres. `main` só recebe PR com squash; o título do PR vira o
  commit.
- `make check` passa antes de cada commit e de abrir o PR. Verificação que falha se corrige, não
  se desativa.
- Mudança que cria ou altera um padrão do repositório exige ADR novo. ADR `accepted` é imutável:
  um registro novo o substitui com `supersedes` e `superseded-by` preenchidos nos dois lados.
- Documentação em português; código, tipos e escopos de commit em inglês. Shell em POSIX `sh`,
  sem bashismos. Texto em UTF-8 com LF.
- Actions em `.github/workflows/` fixadas por SHA completo com comentário da versão
  (`make check-actions` valida); ao atualizar, troque SHA e comentário juntos.
- Preferências pessoais vão em `CLAUDE.local.md`, já ignorado pelo Git.

## Só no repositório do template

Nenhuma ferramenta ou dependência de stack entra aqui. Toda convenção nova precisa valer em
qualquer linguagem e vir com um `check-*` em `make check`.

## Onde ler mais

| Precisa de | Leia |
| --- | --- |
| Mapa do repositório e onde colocar o quê | `docs/ARCHITECTURE.md` |
| Requisitos e preparo do ambiente | `docs/SETUP.md` |
| O que cada `check-*` valida e os checks obrigatórios do ruleset | `docs/TESTING.md` |
| Fluxo de trabalho, commits e versões | `CONTRIBUTING.md` |
| Cada padrão, sua fonte oficial e a configuração do GitHub | `docs/STANDARDS.md` |
