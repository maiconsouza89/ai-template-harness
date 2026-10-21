# CLAUDE.md

Template de repositório, agnóstico de stack, para desenvolvimento assistido por IA. Regra do
harness: `CLAUDE.md` aponta, `docs/` explica, `Makefile` executa. Este arquivo é um mapa, não um
manual; leia o documento que a tarefa pedir antes de alterar código. A raiz diz como trabalhar
no repositório; `docs/` fala do produto e das decisões.

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

- **Verificações.** Cada alvo `check-*` chama um `scripts/checks/check-*.sh` em POSIX `sh`;
  `make check` agrega todos e a CI roda o mesmo alvo. O cabeçalho de cada script diz o que ele
  valida; para adicionar uma, veja `CONTRIBUTING.md`.
- **Hook `commit-msg`.** Vive em `.githooks/` e é testado por `scripts/tests/test-commit-msg.sh`
  (`make check-hooks`). Antes de mudar o hook, acrescente um caso aceito e um rejeitado.
- **Stack por contrato** (`docs/adr/0003`). `scripts/contract.sh` despacha `lint`, `format`,
  `test` e `build` para `scripts/<alvo>.sh`. O projeto gerado cria esses scripts e registra a
  stack em um ADR; `Makefile` e `CLAUDE.md` não mudam.
- **Release automática** (`docs/adr/0004`). `CHANGELOG.md` e `.release-please-manifest.json` são
  gerados pelo release-please a partir dos commits; não edite nenhum dos dois.
- **Documentação** (`docs/adr/0007`). `docs/` é organizada por tipo e `docs/README.md` é a fonte
  única das convenções: front-matter obrigatório, nomes, ADR imutável, lacunas como
  `[A CONFIRMAR: pergunta]`. `make check-docs` valida tudo com o `validate.py` da skill `docs-init`.
- **Skills e subagents.** `/docs-init` entrevista e gera PRD, HLD, ADRs e roadmap delegando aos
  subagents de `.claude/agents/`; `/adr` cria um ADR numerado e indexado; `/fdd` desenha uma
  feature; `/docs-review` audita. Entrevistas fazem uma pergunta por vez, com alternativas e uma
  recomendada.

## Onde colocar o quê

| Conteúdo | Lugar | Motivo |
| --- | --- | --- |
| Instrução para agente | `CLAUDE.md` | Fonte única; aponta, não repete |
| Preferência pessoal | `CLAUDE.local.md` (ignorado) | Não polui o repositório |
| Como trabalhar no repositório (ambiente, checks, fluxo, commits, release) | `CONTRIBUTING.md` | Um arquivo, reconhecido pelo GitHub |
| Comando que pessoa ou agente executa | Alvo no `Makefile` chamando `scripts/*.sh` | Uma porta de entrada, lógica testável em sh |
| Verificação automática | `scripts/checks/check-*.sh` e alvo `check-*` | `make check` agrega tudo; a CI roda o mesmo |
| Implementação de lint, format, test, build da stack | `scripts/<alvo>.sh` no projeto gerado | O contrato do `Makefile` não muda (`docs/adr/0003`) |
| Decisão de padrão ou arquitetura | `docs/adr/NNNN-*.md` | Histórico com alternativas descartadas; skill `adr` numera e indexa |
| Requisitos, arquitetura, design de feature, operação | `docs/<tipo>/` | Um template por tipo; convenções em `docs/README.md` |
| Arquivo de comunidade (`CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`) | Raiz | Reconhecido pelo GitHub; `LICENSE` só é detectado na raiz |

## Regras

- Branch `<tipo>/<descricao>` a partir de `main`; commits e título do PR em Conventional Commits,
  tipo e escopo em inglês e descrição em português (formato completo em `CONTRIBUTING.md`).
  `main` só recebe PR com squash.
- `make check` passa antes de cada commit e de abrir o PR. Verificação que falha se corrige, não
  se desativa.
- Mudança que cria ou altera um padrão do repositório exige ADR novo (regras em `docs/README.md`).
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
| Ambiente, verificações, fluxo de trabalho, commits, versões e configuração do GitHub | `CONTRIBUTING.md`, `README.md` |
| Convenções e estrutura da documentação do produto | `docs/README.md` |
| Por que cada padrão existe e o que foi descartado | `docs/adr/README.md` |
