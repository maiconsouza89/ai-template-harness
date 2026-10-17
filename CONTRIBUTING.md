# Contribuindo

Obrigado por contribuir. Este guia resume o fluxo de trabalho. A fundamentação de cada regra
está em [`docs/01-fundacao-git-e-padroes.md`](docs/01-fundacao-git-e-padroes.md).

## Configuração inicial

Após clonar, ative os hooks versionados uma única vez:

```sh
sh scripts/setup.sh
```

Isso aponta `core.hooksPath` para `.githooks/`, onde o hook `commit-msg` valida o cabeçalho de
cada commit.

## Fluxo de trabalho (GitHub Flow)

1. Crie um branch a partir de `main`, com nome curto e descritivo: `add-commit-msg-hook`,
   `fix-crlf-powershell`.
2. Faça commits convencionais no branch (ver abaixo).
3. Abra o pull request com título no formato Conventional Commits. Com squash merge, o título
   do PR vira o cabeçalho do commit em `main`.
4. Responda à revisão.
5. Faça merge por squash. O branch é apagado automaticamente.

`main` só recebe mudanças por pull request. Não há branches permanentes de `develop` ou
`release`.

## Mensagens de commit

Formato ([Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/)):

```text
<tipo>[(escopo)][!]: <descrição>

[corpo]

[rodapé(s)]
```

| Tipo | Uso | Efeito na versão |
| --- | --- | --- |
| `feat` | Nova funcionalidade | MINOR |
| `fix` | Correção | PATCH |
| `perf` | Desempenho | PATCH |
| `refactor`, `docs`, `style`, `test`, `build`, `ci`, `chore`, `revert` | Sem efeito, salvo breaking change | nenhum |

Regras:

- Tipos e escopos em inglês; descrição em português, minúsculas, no imperativo, sem ponto
  final, até 72 caracteres.
- Breaking change: `!` antes dos dois-pontos ou rodapé `BREAKING CHANGE: ...`. Efeito MAJOR.
- Corpo: o quê e por quê, separado do cabeçalho por uma linha em branco.
- Rodapés no formato `Token: valor` (`Refs: #12`, `Co-authored-by: ...`).

Exemplos:

```text
feat(hooks): valida cabeçalho de commit com hook commit-msg
fix(gitattributes): mantém crlf em scripts powershell
chore!: exige commits assinados
```

## Versões e releases

- [SemVer 2.0.0](https://semver.org/lang/pt-BR/). Primeira versão `0.1.0`. Enquanto `0.y.z`,
  `feat` e breaking change sobem MINOR e `fix` sobe PATCH.
- A tag anotada `vX.Y.Z` é a fonte da verdade da versão.
- Release manual:

  ```sh
  git log "$(git describe --tags --abbrev=0)"..HEAD --oneline
  # mover [Unreleased] do CHANGELOG para [X.Y.Z] - AAAA-MM-DD; commit: chore(release): vX.Y.Z
  git tag -a vX.Y.Z -m "vX.Y.Z"
  git push --follow-tags
  ```

- Mapeamento para o `CHANGELOG.md` ([Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)):
  `feat` → Added, `fix` → Fixed, `perf` → Changed, breaking que remove → Removed.

## Decisões

Decisões de arquitetura e de processo são registradas em `docs/decisions/` no formato
[MADR 4.0](https://adr.github.io/madr/), um arquivo por decisão: `NNNN-titulo-com-hifens.md`.
