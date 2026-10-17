# Verificações

`make check` é a única porta de entrada. Deve passar antes de cada commit e de abrir um PR. A CI
roda o mesmo alvo (`.github/workflows/ci.yml`), então o que passa local passa lá.

## O que roda hoje

| Alvo | Script | Verifica |
| --- | --- | --- |
| `check-branch` | `scripts/check-branch.sh` | Nome do branch no formato `<tipo>/<descricao>` com os tipos do commit; `main` isento |
| `check-hooks` | `scripts/test-commit-msg.sh` | Hook `commit-msg` com cabeçalhos válidos e inválidos (acentos, limite de 72 caracteres, tipos, escopo, ponto final, segunda linha) |
| `check-eol` | `scripts/check-eol.sh` | Nenhum arquivo versionado com CRLF ou fim de linha misto (`git ls-files --eol`) |
| `check-shell` | `scripts/check-shell.sh` | `sh -n` em todos os scripts e hooks; `shellcheck -s sh` se instalado |
| `check-actions` | `scripts/check-actions.sh` | Workflows do GitHub Actions com actionlint (pula localmente se ausente; falha na CI) |
| `check-secrets` | `scripts/check-secrets.sh` | Segredos no histórico do Git com gitleaks (pula localmente se ausente; falha na CI) |
| `lint`, `test` | `scripts/contract.sh` | Alvos do contrato; rodam `scripts/lint.sh` e `test.sh` se existirem, senão avisam e passam |

Cada alvo também roda sozinho: `make check-hooks`.

## Status checks obrigatórios

O ruleset de `main` exige dois checks verdes antes do merge. É a única lista; os outros
documentos apontam para cá.

| Check | Workflow | O que faz |
| --- | --- | --- |
| `check` | `ci.yml` | `make check` em Ubuntu com shellcheck, actionlint e gitleaks instalados (histórico completo) |
| `pr-title` | `pr-title.yml` | Título do PR no padrão do hook `commit-msg` |

## Release

`release.yml` não é um check: roda no push em `main` e abre ou atualiza o PR de release. Esse PR
passa pelos mesmos checks e é mesclado sozinho quando ficam verdes. Para testar a
configuração sem criar nada:

```sh
npx release-please release-pr --repo-url=<owner>/<repo> --token="$(gh auth token)" --dry-run
```

## Contrato de alvos

`make lint`, `make format`, `make test` e `make build` existem em qualquer projeto gerado. Para
implementar, crie `scripts/<alvo>.sh` (POSIX sh, pode chamar a ferramenta da stack) e registre um
ADR. Enquanto o script não existe, o alvo avisa e passa.

## Como adicionar uma verificação

1. Crie `scripts/check-<nome>.sh` em POSIX `sh`, com `set -eu`, saída `ok: ...` no sucesso e
   mensagem clara no erro (`exit 1`).
2. Adicione o alvo `check-<nome>` no `Makefile` com comentário `##` e inclua-o nas dependências
   de `check`.
3. Documente a linha na tabela acima.
4. Se a verificação aplicar uma regra nova, registre a regra em `AGENTS.md` e, se for decisão de
   padrão, um ADR.

## Ao mudar o hook `commit-msg`

Acrescente o caso em `scripts/test-commit-msg.sh` antes de mudar o hook: um aceito e um rejeitado
para cada regra nova.
