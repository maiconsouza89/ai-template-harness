# Contribuindo

Obrigado por contribuir. Este guia resume o fluxo de trabalho; o "por quê" de cada regra, com
as alternativas descartadas, está em [`docs/adr/`](docs/adr/).

## Ambiente

| Ferramenta | Versão | Uso |
| --- | --- | --- |
| Git | ≥ 2.22 | `core.hooksPath`, `git branch --show-current` |
| POSIX `sh` | qualquer | hooks e scripts |
| GNU Make | ≥ 3.81 | `make setup`, `make check` |
| shellcheck | opcional | lint dos scripts em `make check-shell`; sem ele, só a sintaxe é validada |
| actionlint | opcional | valida os workflows em `make check-actions`; sem ele, pula com aviso |
| gitleaks | opcional | procura segredos em `make check-secrets`; sem ele, pula com aviso |
| python3 | opcional | validação de `docs/` em `make check-docs`; sem ele, pula com aviso |

As ferramentas opcionais são obrigatórias na CI (`CI=true make check` reproduz isso localmente).
No Windows, use WSL ou Git Bash (ambos trazem `sh`; `make` vem via WSL, Chocolatey ou Scoop).
`.editorconfig` cuida de UTF-8, LF e indentação; no VS Code, aceite a extensão recomendada em
`.vscode/extensions.json`.

Após o clone, uma única vez:

```sh
make setup    # aponta core.hooksPath para .githooks/; o Git não ativa hooks sozinho
make check    # confirma que tudo passa
```

## Verificações

`make check` é a única porta de entrada e deve passar antes de cada commit e de abrir um PR. A
CI (`.github/workflows/ci.yml`) roda o mesmo alvo, então o que passa local passa lá. `make help`
lista cada `check-*` com o que ele valida; o cabeçalho de cada `scripts/checks/check-*.sh`
detalha. Cada alvo também roda sozinho: `make check-hooks`.

O ruleset de `main` exige dois checks verdes antes do merge; é a única lista.

| Check | Workflow | O que faz |
| --- | --- | --- |
| `check` | `ci.yml` | `make check` em Ubuntu com shellcheck, actionlint e gitleaks instalados (histórico completo) |
| `pr-title` | `pr-title.yml` | Título do PR no padrão do hook `commit-msg` |

Para adicionar uma verificação:

1. Crie `scripts/checks/check-<nome>.sh` em POSIX `sh`, com `set -eu`, saída `ok: ...` no sucesso
   e mensagem clara no erro (`exit 1`).
2. Adicione o alvo `check-<nome>` no `Makefile` com comentário `##` e inclua-o nas dependências
   de `check`.
3. Se a verificação aplicar uma regra nova, registre a regra em `CLAUDE.md` e, se for decisão de
   padrão, um ADR.

Ao mudar o hook `commit-msg`, acrescente antes o caso em `scripts/tests/test-commit-msg.sh`: um
aceito e um rejeitado para cada regra nova.

`make lint`, `make format`, `make test` e `make build` existem em qualquer projeto gerado. Para
implementar, crie `scripts/<alvo>.sh` (POSIX sh, pode chamar a ferramenta da stack) e registre
um ADR. Enquanto o script não existe, o alvo avisa e passa.

## Fluxo de trabalho (GitHub Flow)

1. Crie um branch a partir de `main` no formato `<tipo>/<descricao-com-hifens>`, com os mesmos
   tipos do commit: `feat/hook-commit-msg`, `fix/crlf-powershell`, `docs/traduz-adrs`.
   `make check-branch` valida o nome.
2. Faça commits convencionais no branch (ver abaixo), com `make check` passando.
3. Abra o pull request com título no formato Conventional Commits e preencha o template (o quê,
   por quê, checklist). Com squash merge, o título do PR vira o cabeçalho do commit em `main`.
4. Aguarde os checks obrigatórios e responda à revisão.
5. Faça merge por squash. O branch é apagado automaticamente.

`main` só recebe mudanças por pull request. Não há branches permanentes de `develop` ou
`release`.

## Mensagens de commit

Formato ([Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/)):

```text
<tipo>[(escopo)][!]: <descrição>

[corpo]

[rodapé(s)]
```

| Tipo | Uso | Efeito na versão |
| --- | --- | --- |
| `feat` | Nova funcionalidade | MINOR |
| `fix` | Correção | PATCH |
| `perf` | Desempenho | PATCH |
| `refactor`, `docs`, `style`, `test`, `build`, `ci`, `chore`, `revert` | Sem efeito, salvo breaking change | nenhum |

Regras:

- Tipos e escopos em inglês; descrição em português, minúsculas, no imperativo, sem ponto
  final, até 72 caracteres.
- Breaking change: `!` antes dos dois-pontos ou rodapé `BREAKING CHANGE: ...`. Efeito MAJOR.
- Corpo: o quê e por quê, separado do cabeçalho por uma linha em branco.
- Rodapés no formato `Token: valor` (`Refs: #12`, `Co-authored-by: ...`).

Exemplos:

```text
feat(hooks): valida cabeçalho de commit com hook commit-msg
fix(gitattributes): mantém crlf em scripts powershell
chore!: exige commits assinados
```

## Versões e releases

- [SemVer 2.0.0](https://semver.org/lang/pt-BR/) a partir de `0.1.0`; a tag `vX.Y.Z` é a fonte
  da verdade da versão.
- A release é automática ([ADR 0004](docs/adr/0004-automatizar-release-com-release-please.md)):
  a cada merge em `main`, o release-please abre ou atualiza o PR `chore(release): vX.Y.Z` com a
  versão e o `CHANGELOG.md` calculados dos commits (`feat` → Adicionado, `fix` → Corrigido,
  `perf` → Alterado, `revert` → Revertido; os demais tipos não aparecem nem geram versão) e o
  mescla sozinho quando os checks passam. Para segurar uma release, não mescle esse PR.
- Não edite `CHANGELOG.md` nem `.release-please-manifest.json` à mão.
- Para testar a configuração sem criar nada:
  `npx release-please release-pr --repo-url=<owner>/<repo> --token="$(gh auth token)" --dry-run`.

## Decisões

Mudança que cria ou altera um padrão do repositório exige um ADR em `docs/adr/`. Regras e como
criar em [`docs/README.md`](docs/README.md).
