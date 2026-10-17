#!/bin/sh
# Lista os alvos do contrato (lint, format, test, build) ainda não implementados para a stack.
# Informativo: nunca falha. A implementação entra com a stack, via ADR.
set -eu
cd "$(git rev-parse --show-toplevel)"
missing=""
for target in lint format test build; do
  if [ ! -f "scripts/$target.sh" ]; then
    missing="$missing $target"
  fi
done
if [ -n "$missing" ]; then
  echo "aviso: alvos do contrato sem implementação para esta stack:$missing (crie scripts/<alvo>.sh)"
else
  echo "ok: contrato completo (lint, format, test, build)"
fi
