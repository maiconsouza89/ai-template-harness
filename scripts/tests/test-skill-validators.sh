#!/bin/sh
# Testa os validadores das skills (spec-writer e evaluator) com casos aceitos e rejeitados.
# Cada caso monta uma árvore nova: PRD, HLD e ADRs do fixture de evals da spec-writer, mais o
# RF-001 de scripts/tests/fixtures/skill-validators, com uma mutação aplicada.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  if [ "${CI:-}" = "true" ]; then
    echo "erro: python3 ausente; os validadores das skills precisam dele na CI" >&2
    exit 1
  fi
  echo "aviso: python3 ausente; validadores das skills não testados"
  exit 0
fi

spec=.claude/skills/spec-writer/scripts/validate.py
aval=.claude/skills/evaluator/scripts/validate.py
docs=.claude/skills/spec-writer/evals/files/viewstore/docs
rf=RF-001-criar-conta-de-exibidor-ou-anunciante
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
pass=0
fail=0

reset() { # recria a árvore do caso; $f é a pasta do RF
  rm -rf "$tmp/raiz"
  mkdir -p "$tmp/raiz/docs/features"
  cp -R "$docs/." "$tmp/raiz/docs/"
  cp -R "scripts/tests/fixtures/skill-validators/$rf" "$tmp/raiz/docs/features/"
  f="$tmp/raiz/docs/features/$rf"
}

edit() { # edit <arquivo da pasta do RF> <expressão sed>
  sed "$2" "$f/$1" > "$tmp/editado" && mv "$tmp/editado" "$f/$1"
}

check() { # check <0 aceita|1 rejeita> <spec|aval> <descrição>
  expected=$1
  if [ "$2" = spec ]; then
    python3 -I "$spec" "$f" --raiz "$tmp/raiz" > "$tmp/saida" 2>&1
  else
    python3 -I "$aval" "docs/features/$rf" --raiz "$tmp/raiz" > "$tmp/saida" 2>&1
  fi
  if [ $? -eq 0 ]; then got=0; else got=1; fi
  if [ "$got" -eq "$expected" ]; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    printf 'FALHOU (esperado=%s obtido=%s): %s: %s\n' "$expected" "$got" "$2" "$3" >&2
    sed 's/^/  /' "$tmp/saida" >&2
  fi
}

# spec-writer
reset
check 0 spec 'trio base'

reset
edit spec.md 's/^# Spec: RF-001/# Spec: RF-002/'
check 1 spec 'título da spec com outro RF'

reset
edit contract.md '/^Modo de verificação: /d'
check 1 spec 'superfície sem Modo de verificação'

# evaluator
reset
check 0 aval 'avaliação e diário base'

reset
edit orquestracao.md 's/^- Status: esgotado$/- Status: terminado/'
check 1 aval 'status de diário desconhecido'

reset
edit avaliacao.md 's/^- Status: reprovado$/- Status: limpo/'
check 1 aval 'limpo com critério reprovado'

total=$((pass + fail))
if [ "$fail" -gt 0 ]; then
  echo "erro: validadores das skills: $fail de $total casos falharam" >&2
  exit 1
fi
echo "ok: validadores das skills: $total casos"
