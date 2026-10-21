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
make check-<nome>    # uma verificação isolada (check-hooks, check-docs, ...; lista em make help)
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
- **Stack por contrato** (`docs/adr/0003`). `scripts/contract.sh` despacha `lint`, `format`,
  `test` e `build` para `scripts/<alvo>.sh`. O projeto gerado cria esses scripts e registra a
  stack em um ADR; `Makefile` e `CLAUDE.md` não mudam.
- **Release automática** (`docs/adr/0004`). O release-please gera `CHANGELOG.md` e
  `.release-please-manifest.json` a partir dos commits; não edite nenhum dos dois. Só `feat`,
  `fix`, `perf` e `revert` geram versão, e a descrição do commit vira a entrada do changelog.
- **Documentação** (`docs/ADR` virou `docs/adr`; ADR 0007). `docs/` é organizada por tipo:
  `product/` (PRD, roadmap), `architecture/` (HLD, componentes), `adr/`, `features/` (FDD),
  `runbooks/`, `guides/`, `templates/` (modelos) e `_intake/` (entrevistas brutas). Índice e
  convenções em `docs/README.md`; regras completas em
  `.claude/skills/docs-init/references/convencoes.md`. Todo documento tem front-matter (`title`,
  `type`, `status`, `date`, `owners`); o que não se sabe fica como `[A CONFIRMAR: pergunta]`.
  `make check-docs` roda o `validate.py` da skill e o smoke test dos scripts.
- **Skills e subagents.** `/docs-init` entrevista e gera PRD, HLD, ADRs e roadmap delegando aos
  subagents de `.claude/agents/` (`prd-writer`, `architecture-writer`, `adr-extractor`,
  `docs-reviewer`); `/adr` cria um ADR com `scripts/new_adr.py`, que numera e atualiza
  `docs/adr/README.md`; `/fdd` cria o design de uma feature; `/docs-review` audita tudo.
  Entrevistas fazem uma pergunta por vez, com alternativas e uma recomendada.

## Regras

- Branch `<tipo>/<descricao>` a partir de `main`, com os tipos do commit (`make check-branch`).
  Commits e título do PR em Conventional Commits: tipo e escopo em inglês, descrição em
  português, cabeçalho até 72 caracteres. `main` só recebe PR com squash; o título do PR vira o
  commit.
- `make check` passa antes de cada commit e de abrir o PR. Verificação que falha se corrige, não
  se desativa.
- Mudança que cria ou altera um padrão do repositório exige ADR novo. ADR `accepted` é imutável:
  um registro novo o substitui com `supersedes` e `superseded_by` preenchidos nos dois lados.
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
| Estrutura e convenções da documentação do produto | `docs/README.md` |
| Requisitos e preparo do ambiente | `docs/SETUP.md` |
| O que cada `check-*` valida e os checks obrigatórios do ruleset | `docs/TESTING.md` |
| Fluxo de trabalho, commits e versões | `CONTRIBUTING.md` |
| Cada padrão, sua fonte oficial e a configuração do GitHub | `docs/STANDARDS.md` |
