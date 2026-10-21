# Contribuindo

Obrigado por contribuir. Este guia resume o fluxo de trabalho. A fundamentação de cada regra
está em [`docs/STANDARDS.md`](docs/STANDARDS.md) e em [`docs/adr/`](docs/adr/).

## Configuração inicial

Preparo do ambiente e `make setup` em [`docs/SETUP.md`](docs/SETUP.md). `make check` deve passar
antes de cada commit e de abrir um PR; o que ele valida está em [`docs/TESTING.md`](docs/TESTING.md).

## Fluxo de trabalho (GitHub Flow)

1. Crie um branch a partir de `main` no formato `<tipo>/<descricao-com-hifens>`, com os mesmos
   tipos do commit: `feat/hook-commit-msg`, `fix/crlf-powershell`, `docs/traduz-adrs`.
   `make check-branch` valida o nome.
2. Faça commits convencionais no branch (ver abaixo), com `make check` passando.
3. Abra o pull request com título no formato Conventional Commits e preencha o template (o quê,
   por quê, checklist). Com squash merge, o título do PR vira o cabeçalho do commit em `main`.
4. Aguarde os checks obrigatórios (lista em [`docs/TESTING.md`](docs/TESTING.md)) e responda à revisão.
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

- [SemVer 2.0.0](https://semver.org/lang/pt-BR/) a partir de `0.1.0`; a tag `vX.Y.Z` é a fonte
  da verdade da versão.
- A release é automática ([ADR 0004](docs/adr/0004-automatizar-release-com-release-please.md)):
  a cada merge em `main`, o release-please abre ou atualiza o PR `chore(release): vX.Y.Z` com a
  versão e o `CHANGELOG.md` calculados dos commits (`feat` → Adicionado, `fix` → Corrigido,
  `perf` → Alterado, `revert` → Revertido; os demais tipos não aparecem nem geram versão) e o
  mescla sozinho quando os checks passam. Para segurar uma release, não mescle esse PR.
- Não edite `CHANGELOG.md` nem `.release-please-manifest.json` à mão.

## Decisões

Mudança que cria ou altera um padrão do repositório exige um ADR em `docs/adr/`. Regras e como
criar em [`docs/README.md`](docs/README.md).
