# Verificações

`make check` é a única porta de entrada. Deve passar antes de cada commit e de abrir um PR. A CI
(passo 3) vai rodar o mesmo alvo, então o que passa local passa lá.

## O que roda hoje

| Alvo | Script | Verifica |
| --- | --- | --- |
| `check-hooks` | `scripts/test-commit-msg.sh` | Hook `commit-msg` com 22 cabeçalhos válidos e inválidos (acentos, limite de 72 caracteres, tipos, escopo, ponto final, segunda linha) |
| `check-eol` | `scripts/check-eol.sh` | Nenhum arquivo versionado com CRLF ou fim de linha misto (`git ls-files --eol`) |
| `check-shell` | `scripts/check-shell.sh` | `sh -n` em todos os scripts e hooks; `shellcheck -s sh` se instalado |

Cada alvo também roda sozinho: `make check-hooks`.

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
