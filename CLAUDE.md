# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Template de repositório, agnóstico de stack, para desenvolvimento assistido por IA. Regra do
harness: `CLAUDE.md` aponta, `CONTRIBUTING.md` explica, `Makefile` executa. Este arquivo é um
mapa, não um manual; leia o documento que a tarefa pedir antes de alterar código. A raiz diz como
trabalhar no repositório; `docs/` fala do produto e das decisões técnicas.

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

- **Verificações.** Cada alvo `check-*` chama um `scripts/checks/check-*.sh` em POSIX `sh`;
  `make check` agrega todos e a CI roda o mesmo alvo. O cabeçalho de cada script diz o que ele
  valida; para adicionar uma, veja `CONTRIBUTING.md`.
- **Hook `commit-msg`.** Vive em `.githooks/` e é testado por `scripts/tests/test-commit-msg.sh`
  (`make check-hooks`). Antes de mudar o hook, acrescente um caso aceito e um rejeitado.
- **Stack por contrato.** `scripts/contract.sh` despacha `lint`, `format`, `test` e `build` para
  `scripts/<alvo>.sh`. O projeto gerado cria esses scripts e registra a stack em um ADR;
  `Makefile` e `CLAUDE.md` não mudam.
- **Release automática.** `CHANGELOG.md` e `.release-please-manifest.json` são gerados pelo
  release-please a partir dos commits; não edite nenhum dos dois.
- **Documentação do projeto** em `docs/product/` (o quê e quando) e `docs/architecture/` (como e
  por quê), criada pelas skills: `/prd-writer` (`docs/product/prd.md`, regras de produto e
  requisitos `RF-NNN`, sem stack, e `docs/product/roadmap.md`, andamento por RF gerado do PRD),
  `/hld-writer` (`docs/architecture/hld.md`, o como técnico entre o PRD e os ADRs) e `/adr-writer`
  (ADRs em `docs/architecture/adr/`, só arquitetura e tecnologia; monta a pasta na primeira vez e
  `make check-adr` audita). Cada skill valida a própria estrutura.

## Onde colocar o quê

| Conteúdo | Lugar | Motivo |
| --- | --- | --- |
| Instrução para agente | `CLAUDE.md` | Fonte única; aponta, não repete |
| Preferência pessoal | `CLAUDE.local.md` (ignorado) | Não polui o repositório |
| Como trabalhar no repositório (ambiente, checks, fluxo, commits, release) | `CONTRIBUTING.md` | Um arquivo, reconhecido pelo GitHub |
| Uso do template e configuração do GitHub | `README.md` | Primeiro arquivo que a pessoa lê |
| Comando que pessoa ou agente executa | Alvo no `Makefile` chamando `scripts/*.sh` | Uma porta de entrada, lógica testável em sh |
| Verificação automática | `scripts/checks/check-*.sh` e alvo `check-*` | `make check` agrega tudo; a CI roda o mesmo |
| Implementação de lint, format, test, build da stack | `scripts/<alvo>.sh` no projeto gerado | O contrato do `Makefile` não muda |
| Decisão de arquitetura ou tecnologia | `docs/architecture/adr/NNNN-*.md` | Histórico com alternativas descartadas |
| Regras de produto e requisitos | `docs/product/prd.md` | Regra de negócio não é ADR |
| Andamento da implementação por requisito | `docs/product/roadmap.md` (via `/prd-writer`) | O PRD só muda quando o produto muda |
| Desenho técnico do sistema | `docs/architecture/hld.md` | Liga requisitos do PRD aos ADRs |
| Arquivo de comunidade (`CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`) | Raiz | Reconhecido pelo GitHub; `LICENSE` só é detectado na raiz |

## Regras

- Branch `<tipo>/<descricao>` a partir de `main`; commits e título do PR em Conventional Commits,
  tipo e escopo em inglês e descrição em português (formato completo em `CONTRIBUTING.md`).
  `main` só recebe PR com squash.
- `make check` passa antes de cada commit e de abrir o PR. Verificação que falha se corrige, não
  se desativa.
- Decisão de arquitetura ou tecnologia cara de reverter vira ADR; regra de negócio vai para o
  PRD. ADR `accepted` é imutável: um registro novo o substitui com `supersedes` e
  `superseded-by` preenchidos nos dois lados.
- Documentação em português; código, tipos e escopos de commit em inglês. Shell em POSIX `sh`,
  sem bashismos. Texto em UTF-8 com LF.
- Actions em `.github/workflows/` fixadas por SHA completo com comentário da versão
  (`make check-actions` valida); ao atualizar, troque SHA e comentário juntos.

## Só no repositório do template

Nenhuma ferramenta ou dependência de stack entra aqui. Toda convenção nova precisa valer em
qualquer linguagem e vir com um `check-*` em `make check`.

## Onde ler mais

| Precisa de | Leia |
| --- | --- |
| Ambiente, verificações, fluxo de trabalho, commits e versões | `CONTRIBUTING.md` |
| Uso do template e configuração do GitHub | `README.md` |
| Regras de ADR, PRD e HLD | `SKILL.md` de cada skill em `.claude/skills/` |
