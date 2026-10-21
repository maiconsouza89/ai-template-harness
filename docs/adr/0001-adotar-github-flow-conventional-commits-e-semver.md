---
status: accepted
type: adr
number: 0001
date: 2026-10-16
layer: workflow
title: "Adotar GitHub Flow, Conventional Commits e SemVer"
description: "Por que o repositório usa GitHub Flow com squash, commits convencionais em português e SemVer em vez de Git Flow, formato livre ou CalVer."
owners: [mantenedores do template]
supersedes: []
superseded_by: []
related: []
---

# 0001. Adotar GitHub Flow, Conventional Commits e SemVer

> Parcialmente substituído: a linha "Changelog" pelo ADR 0004 (gerado pelo release-please) e a
> evolução da validação local pelo ADR 0003 (CI agnóstica). O restante continua em vigor.

## Contexto e problema

O template precisa de convenções de Git, commits, versionamento e changelog antes de qualquer
escolha de linguagem ou pipeline. As decisões devem ser agnósticas de stack, mínimas para começar
e verificáveis por máquina sempre que possível. Fundamentação e fontes em `docs/STANDARDS.md`.

## Opções consideradas

| Tema | Escolhida | Alternativas consideradas |
| --- | --- | --- |
| Modelo de branches | GitHub Flow, branches `<tipo>/<descricao>` com os tipos do commit | Git Flow, trunk-based com flags; nomes livres |
| Merge de PR | Squash | Rebase, merge commit |
| Commits | Conventional Commits 1.0.0, tipos em inglês, descrição em português | Descrição em inglês; formato livre |
| Versionamento | SemVer 2.0.0, tag `vX.Y.Z` | CalVer |
| Changelog | Keep a Changelog 1.1.0 (substituído: ADR 0004) | Gerado só a partir dos commits |
| Validação local | Hook `commit-msg` em POSIX sh em `.githooks/` | pre-commit + conventional-pre-commit; lefthook; commitlint + husky; cocogitto; só na CI |
| Licença | MIT | Apache-2.0; sem licença |
| Assinatura de commits | Não configurar | Opcional via SSH; obrigatória no ruleset |
| Idioma da documentação | pt-BR | Inglês; pt-BR agora e inglês depois |

## Decisão

Escolhida a coluna **Escolhida** da tabela, porque atende ao mínimo para começar sem impor stack:
o hook em `sh` não depende de Node nem de Python; squash mantém `main` linear com um commit por
PR, cujo título segue Conventional Commits; MIT é a licença mais simples para um template; a
descrição do commit em português facilita o time, enquanto os tipos em inglês mantêm
compatibilidade com ferramentas.

## Consequências

- Bom: todas as convenções estão em arquivos versionados e o hook verifica o cabeçalho.
- Bom: nenhuma ferramenta de stack é imposta ao template.
- Ruim: o hook em `sh` cobre só o cabeçalho; regras mais ricas exigem outra ferramenta.
- Ruim: commits em português e bots em inglês (Dependabot) misturam idiomas no histórico.

## Referências

Consultado em 2026-10-16.

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/) — formato do cabeçalho e efeito na versão.
- [SemVer 2.0.0](https://semver.org/lang/pt-BR/) — regras de MAJOR, MINOR e PATCH.
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) — os seis passos do fluxo.
- [githooks](https://git-scm.com/docs/githooks) — `core.hooksPath` para hooks versionados.
