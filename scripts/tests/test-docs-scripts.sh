#!/bin/sh
# Smoke test dos scripts da documentação em um diretório temporário:
# scaffold idempotente, dois ADRs (o segundo substituindo o primeiro) e validação sem erros.
set -eu
cd "$(git rev-parse --show-toplevel)"
scaffold=.claude/skills/docs-init/scripts/scaffold.py
validate=.claude/skills/docs-init/scripts/validate.py
new_adr=.claude/skills/adr/scripts/new_adr.py
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT INT TERM
root="$tmp/docs"
fail() { echo "test-docs-scripts: $1" >&2; exit 1; }

python3 "$scaffold" --root "$root" >/dev/null
[ -f "$root/README.md" ] || fail "scaffold não criou README.md"
[ -f "$root/templates/adr.md" ] || fail "scaffold não copiou os templates"
second=$(python3 "$scaffold" --root "$root")
echo "$second" | grep -q '^criado:' && fail "scaffold não é idempotente: criou algo na segunda execução"

first=$(python3 "$new_adr" "Usar Postgres como banco principal" --root "$root")
[ -f "$first" ] || fail "new_adr não criou o primeiro ADR"
case "$first" in */0001-usar-postgres-como-banco-principal.md) ;; *) fail "nome inesperado: $first" ;; esac
second_adr=$(python3 "$new_adr" "Trocar Postgres por CockroachDB" --supersedes 0001 --root "$root")
grep -q '^supersedes: \[0001\]$' "$second_adr" || fail "segundo ADR sem supersedes"
grep -q '^superseded_by: \[0002\]$' "$first" || fail "primeiro ADR sem superseded_by"
grep -q '^status: superseded$' "$first" || fail "primeiro ADR não ficou superseded"
grep -c '^| 000[12] |' "$root/adr/README.md" | grep -qx 2 || fail "índice de ADRs sem as duas linhas"
python3 "$validate" --root "$root" >/dev/null || fail "validate acusou erro no diretório de teste"

printf -- '---\ntitle: Quebrado\ntype: adr\nnumber: 0099\nstatus: proposed\ndate: hoje\nowners: []\n---\n' > "$root/adr/0099-quebrado.md"
if python3 "$validate" --root "$root" >/dev/null 2>&1; then
  fail "validate aceitou ADR com data inválida e lacuna na numeração"
fi
echo "ok: scripts da documentação (scaffold, new_adr, validate)"
