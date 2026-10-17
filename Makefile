# Superfície única de comandos para pessoas e agentes. A lógica fica em scripts/.
# Alvos documentados com "## " aparecem em `make help`.

SHELL := /bin/sh
.DEFAULT_GOAL := help

.PHONY: help setup check check-hooks check-eol check-shell check-actions check-secrets check-contract \
	lint format test build

help: ## Lista os alvos disponíveis
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

setup: ## Ativa os hooks versionados (uma vez após o clone)
	@sh scripts/setup.sh

check: check-hooks check-eol check-shell check-actions check-secrets check-contract lint test ## Roda todas as verificações
	@echo "ok: todas as verificações passaram"

check-hooks: ## Testa o hook commit-msg com cabeçalhos válidos e inválidos
	@sh scripts/test-commit-msg.sh

check-eol: ## Garante que nenhum arquivo versionado tem CRLF
	@sh scripts/check-eol.sh

check-shell: ## Valida a sintaxe dos scripts sh (e shellcheck, se instalado)
	@sh scripts/check-shell.sh

check-actions: ## Valida os workflows do GitHub Actions (actionlint)
	@sh scripts/check-actions.sh

check-secrets: ## Procura segredos nos arquivos versionados (gitleaks)
	@sh scripts/check-secrets.sh

check-contract: ## Lista os alvos do contrato ainda não implementados (informativo)
	@sh scripts/check-contract.sh

# Contrato de alvos: cada projeto gerado implementa scripts/<alvo>.sh. Sem ele, avisa e passa.
lint: ## Lint da stack (contrato; implementa em scripts/lint.sh)
	@sh scripts/contract.sh lint

format: ## Formata o código da stack (contrato; implementa em scripts/format.sh)
	@sh scripts/contract.sh format

test: ## Testes da stack (contrato; implementa em scripts/test.sh)
	@sh scripts/contract.sh test

build: ## Build da stack (contrato; implementa em scripts/build.sh)
	@sh scripts/contract.sh build
