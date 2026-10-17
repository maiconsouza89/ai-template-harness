#!/bin/sh
# Procura segredos nos arquivos versionados com gitleaks.
# Sem gitleaks: pula com aviso localmente; falha na CI (CI=true).
set -eu
cd "$(git rev-parse --show-toplevel)"
if ! command -v gitleaks >/dev/null 2>&1; then
  if [ "${CI:-}" = "true" ]; then
    echo "check-secrets: gitleaks não encontrado na CI" >&2
    exit 1
  fi
  echo "aviso: gitleaks não instalado, verificação pulada (https://github.com/gitleaks/gitleaks)"
  exit 0
fi
gitleaks dir . --no-banner --redact --exit-code 1
echo "ok: nenhum segredo encontrado (gitleaks)"
