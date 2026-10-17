# Contribuindo

Obrigado por contribuir. Este guia resume o fluxo de trabalho. A fundamentação de cada regra
está em [`docs/01-fundacao-git-e-padroes.md`](docs/01-fundacao-git-e-padroes.md).

## Configuração inicial

Após clonar, ative os hooks versionados uma única vez:

```sh
make setup
make check
```

`make setup` aponta `core.hooksPath` para `.githooks/`, onde o hook `commit-msg` valida o
cabeçalho de cada commit. `make check` roda todas as verificações e deve passar antes de cada
commit e de abrir um PR (detalhes em [`docs/TESTING.md`](docs/TESTING.md)). Ambiente completo em
[`docs/SETUP.md`](docs/SETUP.md).

## Fluxo de trabalho (GitHub Flow)

1. Crie um branch a partir de `main` no formato `<tipo>/<descricao-com-hifens>`, com os mesmos
   tipos do commit: `feat/hook-commit-msg`, `fix/crlf-powershell`, `docs/traduz-adrs`.
   `make check-branch` valida o nome.
2. Faça commits convencionais no branch (ver abaixo), com `make check` passando.
3. Abra o pull request com título no formato Conventional Commits e preencha o template (o quê,
   por quê, checklist). Com squash merge, o título do PR vira o cabeçalho do commit em `main`.
4. Aguarde os checks obrigatórios (`check`, `secrets`, `pr-title`) e responda à revisão.
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
- A tag `vX.Y.Z` é a fonte da verdade da versão; `.release-please-manifest.json` guarda a última lançada.
- A release é automática ([ADR 0004](docs/decisions/0004-release-automatica-com-release-please.md)):
  a cada merge em `main`, o release-please abre ou atualiza o PR `chore(release): vX.Y.Z` com a
  versão e o `CHANGELOG.md` calculados dos commits. Quando os checks passam, o PR é mesclado
  sozinho, criando a tag e a GitHub Release.
- Não edite o `CHANGELOG.md` à mão: a descrição do commit é a entrada. Seções: `feat` →
  Adicionado, `fix` → Corrigido, `perf` → Alterado, `revert` → Revertido. Os demais tipos não
  aparecem nem geram versão.
- Para segurar uma release, não mescle o PR de release; ele continua sendo atualizado.

## Decisões

Decisões de arquitetura e de processo são registradas em `docs/decisions/` no formato
[MADR 4.0](https://adr.github.io/madr/), um arquivo por decisão: `NNNN-titulo-com-hifens.md`.
