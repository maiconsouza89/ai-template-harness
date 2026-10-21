#!/bin/sh
# Valida docs/ com o validate.py da skill docs-init e testa os scripts da documentação.
# Falha se houver erro de front-matter, link quebrado, numeração de ADR ou FDD, ou se os
# scripts (scaffold, new_adr, validate) quebrarem o fluxo da documentação.
# Sem python3: pula com aviso localmente; falha na CI (CI=true).
set -eu
cd "$(git rev-parse --show-toplevel)"
validate=.claude/skills/docs-init/scripts/validate.py
if ! command -v python3 >/dev/null 2>&1; then
  if [ "${CI:-}" = "true" ]; then
    echo "check-docs: python3 não encontrado na CI" >&2
    exit 1
  fi
  echo "aviso: python3 não instalado, validação de docs/ pulada"
  exit 0
fi
python3 "$validate" --root docs | tail -n 1
sh scripts/tests/test-docs-scripts.sh
echo "ok: docs/ válida e scripts da documentação testados"
