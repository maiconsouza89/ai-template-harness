---
status: accepted
type: adr
number: 0003
date: 2026-10-17
layer: ci
title: "Manter o template agnóstico por contrato de alvos e CI sem stack"
description: "Por que o template fixa a interface lint/format/test/build no Makefile e roda CI universal, em vez de escolher uma stack ou ter um template por linguagem."
owners: [mantenedores do template]
supersedes: []
superseded_by: []
related: []
---

# 0003. Manter o template agnóstico por contrato de alvos e CI sem stack

## Contexto e problema

O roteiro previa "stack e CI" como passo 3, mas o objetivo do template é servir a qualquer
linguagem. Como entregar CI útil e uma interface estável para agentes sem escolher uma stack?

## Opções consideradas

- **Base agnóstica com contrato de alvos e CI universal** — `make lint/format/test/build` despacham para `scripts/<alvo>.sh`; CI só com verificações válidas em qualquer repositório.
- **Um template por stack derivado da base** — sem herança no GitHub; cópias mantidas à mão.
- **Perfis de stack com `scripts/init.sh --stack`** — modelo cookiecutter/copier; vira gerador.
- **Nunca ter stack** — cada projeto refaz a CI.

## Decisão

Escolhida a **base agnóstica com contrato de alvos**, porque mantém um único template, dá aos
agentes uma interface fixa que não muda quando a stack entra, e a CI roda o mesmo `make check`
usado localmente. Alvos sem `scripts/<alvo>.sh` avisam e passam; actionlint e gitleaks entram
como verificações universais; `pr-title` valida o título do PR com as regras do hook; actions
fixadas por SHA completo sem Dependabot (atualização manual).

## Consequências

- Bom: o template serve a qualquer linguagem e `CLAUDE.md` não muda com a stack.
- Bom: local e CI rodam o mesmo comando; o que passa aqui passa lá.
- Ruim: `make lint` e `make test` passam sem fazer nada até a stack ser implementada.
- Ruim: os SHAs das actions envelhecem sem Dependabot; revisar a cada release.
- Revisão de 2026-10-17: o job `secrets` foi absorvido por `check-secrets` (histórico completo); checks obrigatórios são `check` e `pr-title`.

## Referências

Consultado em 2026-10-17.

- [action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request) — validação do título do PR, inputs `types` e `subjectPattern`.
- [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#using-third-party-actions) — fixar actions por SHA completo.
