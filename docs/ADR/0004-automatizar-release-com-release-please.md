---
status: accepted
date: 2026-10-17
layer: release
title: "Automatizar a release com release-please e auto-merge"
description: "Por que a release é um PR do release-please mesclado automaticamente, em vez de semantic-release, cocogitto ou git-cliff com bypass do ruleset."
supersedes:
superseded-by:
---

# 0004. Automatizar a release com release-please e auto-merge

## Contexto e problema

A release era manual: mover `[Unreleased]` no changelog, commitar e criar a tag. O usuário quer
release automática a cada merge em `main`, com changelog em português, início em `0.1.0` e sem
abrir exceções no ruleset que protege `main`.

## Opções consideradas

- **release-please com auto-merge do PR de release** — o PR passa pelos checks e o GitHub mescla; sem bypass.
- **semantic-release sem `CHANGELOG.md`** — começa em 1.0.0 e a FAQ desaconselha commitar changelog em branch protegido.
- **cocogitto com bypass para o bot** — `cog bump --auto` no push; exige token com bypass no ruleset.
- **git-cliff com script próprio** — também exige bypass.

## Decisão

Escolhido o **release-please com auto-merge**, porque é a única opção automática sem dar bypass a
um bot, suporta `0.x` (`bump-minor-pre-major`), mantém `CHANGELOG.md` no repositório e aceita
seções em português. Tipo `simple`; só `feat`, `fix`, `perf` e `revert` geram versão (tipos
visíveis no changelog contam como lançáveis, por isso `ci` e `build` ficam ocultos); PRs criados
com `GITHUB_TOKEN` não disparam a CI, então o workflow usa o secret `RELEASE_PLEASE_TOKEN` com
fallback para merge manual.

## Consequências

- Bom: toda mudança com `feat` ou `fix` vira versão sem trabalho manual e sem bypass.
- Bom: o changelog deixa de ser editado à mão; a descrição do commit é a entrada.
- Ruim: a qualidade do changelog depende da qualidade das descrições dos commits.
- Ruim: cada repositório gerado precisa do secret configurado à mão.
- Ruim: a tag criada pela GitHub Release é leve, não anotada; a Release carrega as notas.

## Referências

Consultado em 2026-10-17.

- [release-please-action](https://github.com/googleapis/release-please-action) — limitação do `GITHUB_TOKEN` e inputs da action.
- [release-please: manifest config](https://github.com/googleapis/release-please/blob/main/docs/manifest-releaser.md) — `release-as`, `bump-minor-pre-major`, `changelog-sections`.
- [semantic-release FAQ](https://semantic-release.gitbook.io/semantic-release/support/faq) — sem suporte a `0.x` e recomendação contra commitar o changelog.
