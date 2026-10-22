#!/bin/sh
# Smoke test dos scripts da documentação em um diretório temporário:
# scaffold idempotente, dois ADRs (o segundo substituindo o primeiro), PRD e roadmap de exemplo
# (scripts/tests/fixtures/docs/) válidos, --ondas reproduzindo a Ordem de execução do roadmap, e
# mutações que precisam falhar: ciclo, contrato Consome sem Fornece e onda divergente no roadmap.
set -eu
cd "$(git rev-parse --show-toplevel)"
scaffold=.claude/skills/docs-init/scripts/scaffold.py
validate=.claude/skills/docs-init/scripts/validate.py
prd_checks=.claude/skills/docs-init/scripts/prd_checks.py
new_adr=.claude/skills/adr/scripts/new_adr.py
fixtures=scripts/tests/fixtures/docs
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

# PRD e roadmap de exemplo passam, e --ondas reproduz a Ordem de execução do roadmap.
cp "$fixtures"/product/*.md "$root/product/"
prd="$root/product/prd-agenda-barbearia.md"
roadmap="$root/product/roadmap.md"
python3 "$validate" --root "$root" >/dev/null || fail "validate acusou erro no PRD ou roadmap de exemplo"
python3 "$prd_checks" "$prd" --ondas > "$tmp/ondas.txt" || fail "prd_checks --ondas falhou no PRD de exemplo"
sed -n '/^### \[PRD/,/^## Agora/p' "$roadmap" | sed '1d;$d' | sed '/./,$!d' > "$tmp/roadmap-ondas.txt"
printf '\n' >> "$tmp/ondas.txt"
cmp -s "$tmp/ondas.txt" "$tmp/roadmap-ondas.txt" || fail "--ondas não reproduz a seção Ordem de execução do roadmap"

# Mutações que o validate precisa recusar. Cada uma parte da fixture íntegra.
# mutate <arquivo> <trecho antigo> <trecho novo>: troca exata, falha se o trecho não existir.
mutate() {
  python3 - "$1" "$2" "$3" <<'PY' || fail "mutação não aplicada em $1: $2"
import sys
from pathlib import Path
path, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
text = Path(path).read_text(encoding="utf-8")
if text.count(old) != 1:
    sys.exit(1)
Path(path).write_text(text.replace(old, new), encoding="utf-8")
PY
}
expect_fail() {
  if python3 "$validate" --root "$root" >/dev/null 2>&1; then
    fail "validate aceitou $1"
  fi
  cp "$fixtures"/product/*.md "$root/product/"
}
mutate "$prd" "| RF-001 | Acesso de dono e barbeiro | 1 | nenhum |" "| RF-001 | Acesso de dono e barbeiro | 1 | RF-003 |"
expect_fail "PRD com ciclo na tabela de dependências"
mutate "$prd" "- RF-003: agendamento com cliente, serviço, barbeiro, data, horário e status, acessado pelo link individual" \
  "- RF-003: agendamento com cliente, serviço, barbeiro, data, horário e status, acessado pelo link individual
- RF-002: catálogo de serviços"
expect_fail "PRD com Consome sem Fornece correspondente"
mutate "$roadmap" "- **Onda 4**: RF-004, RF-005" "- **Onda 4**: RF-004"
expect_fail "roadmap com onda divergente da tabela do PRD"
python3 "$validate" --root "$root" >/dev/null || fail "fixtures restauradas não passam"

printf -- '---\ntitle: Quebrado\ntype: adr\nnumber: 0099\nstatus: proposed\ndate: hoje\nowners: []\n---\n' > "$root/adr/0099-quebrado.md"
if python3 "$validate" --root "$root" >/dev/null 2>&1; then
  fail "validate aceitou ADR com data inválida e lacuna na numeração"
fi
echo "ok: scripts da documentação (scaffold, new_adr, validate, prd_checks)"
