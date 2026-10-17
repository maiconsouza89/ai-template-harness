# Superfície única de comandos para pessoas e agentes. A lógica fica em scripts/.
# Alvos documentados com "## " aparecem em `make help`.

SHELL := /bin/sh
.DEFAULT_GOAL := help

.PHONY: help setup check check-hooks check-eol check-shell

help: ## Lista os alvos disponíveis
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

setup: ## Ativa os hooks versionados (uma vez após o clone)
	@sh scripts/setup.sh

check: check-hooks check-eol check-shell ## Roda todas as verificações
	@echo "ok: todas as verificações passaram"

check-hooks: ## Testa o hook commit-msg com cabeçalhos válidos e inválidos
	@sh scripts/test-commit-msg.sh

check-eol: ## Garante que nenhum arquivo versionado tem CRLF
	@sh scripts/check-eol.sh

check-shell: ## Valida a sintaxe dos scripts sh (e shellcheck, se instalado)
	@sh scripts/check-shell.sh
