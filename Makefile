# Superfície única de comandos para pessoas e agentes. A lógica fica em scripts/.
# Alvos documentados com "## " aparecem em `make help`.

SHELL := /bin/sh
.DEFAULT_GOAL := help

.PHONY: help setup check check-branch check-hooks check-eol check-shell check-actions check-secrets \
	lint format test build

help: ## Lista os alvos disponíveis
	@grep -E '^[a-zA-Z_ -]+:.*## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  %-14s %s\n", $$1, $$2}'

setup: ## Ativa os hooks versionados (uma vez após o clone)
	@sh scripts/setup.sh

check: check-branch check-hooks check-eol check-shell check-actions check-secrets lint test ## Roda todas as verificações
	@echo "ok: todas as verificações passaram"

check-branch: ## Valida o nome do branch (<tipo>/<descricao>)
	@sh scripts/check-branch.sh

check-hooks: ## Testa o hook commit-msg com cabeçalhos válidos e inválidos
	@sh scripts/test-commit-msg.sh

check-eol: ## Garante que nenhum arquivo versionado tem CRLF
	@sh scripts/check-eol.sh

check-shell: ## Valida a sintaxe dos scripts sh (e shellcheck, se instalado)
	@sh scripts/check-shell.sh

check-actions: ## Valida os workflows do GitHub Actions (actionlint)
	@sh scripts/check-actions.sh

check-secrets: ## Procura segredos no histórico do Git (gitleaks)
	@sh scripts/check-secrets.sh

# Contrato de alvos, igual em qualquer stack. Cada projeto gerado implementa scripts/<alvo>.sh;
# sem o script, contract.sh avisa e passa. check inclui lint e test; format e build são manuais.
lint format test build: ## Alvos do contrato da stack (scripts/<alvo>.sh)
	@sh scripts/contract.sh $@
