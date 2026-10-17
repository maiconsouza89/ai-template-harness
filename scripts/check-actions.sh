#!/bin/sh
# Valida os workflows do GitHub Actions com actionlint.
# Sem actionlint: pula com aviso localmente; falha na CI (CI=true).
set -eu
cd "$(git rev-parse --show-toplevel)"
if ! command -v actionlint >/dev/null 2>&1; then
  if [ "${CI:-}" = "true" ]; then
    echo "check-actions: actionlint não encontrado na CI" >&2
    exit 1
  fi
  echo "aviso: actionlint não instalado, verificação pulada (https://github.com/rhysd/actionlint)"
  exit 0
fi
actionlint
echo "ok: workflows válidos (actionlint)"
