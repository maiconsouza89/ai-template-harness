# Release automática com release-please e auto-merge

## Contexto e problema

A release era manual: mover `[Unreleased]` no changelog, commitar e criar a tag. O usuário quer
release automática a cada merge em `main`, com changelog em português, início em `0.1.0` e sem
abrir exceções no ruleset que protege `main`.

## Opções consideradas

* release-please com auto-merge do PR de release
* semantic-release (sem `CHANGELOG.md` no repositório, notas só na GitHub Release)
* cocogitto (`cog bump --auto` no push em `main`, com bypass do ruleset para o bot)
* git-cliff com script e workflow próprios (também exige bypass)

Gatilho: PR de release com merge manual; automática a cada merge; manual por `workflow_dispatch`.

## Decisão

Opção escolhida: "release-please com auto-merge", porque é a única que fica automática sem dar
bypass a um bot: o PR de release passa pelos mesmos checks obrigatórios e o GitHub mescla quando
ficam verdes. Suporta `0.x` (`bump-minor-pre-major`), mantém `CHANGELOG.md` no repositório e
aceita seções em português (`changelog-sections`). Não exige nada instalado localmente.

O semantic-release foi descartado por dois conflitos documentados na FAQ oficial: não suporta
versões `0.x` e desaconselha fortemente commitar o changelog de volta em branch protegido.
cocogitto e git-cliff exigiriam um token com bypass no ruleset.

Detalhes:

* Tipo `simple`: atualiza `CHANGELOG.md` e `.release-please-manifest.json` (só atualizaria
  `version.txt` se o arquivo existisse; optamos por não tê-lo). A tag `vX.Y.Z` e a GitHub
  Release são criadas no merge do PR de release; a tag é a fonte da verdade.
* Seções: `feat` → Adicionado, `fix` → Corrigido, `perf` → Alterado, `revert` → Revertido.
  `ci`, `build`, `docs`, `chore`, `refactor`, `style`, `test` ficam ocultos. No release-please,
  todo tipo visível no changelog conta como lançável e sobe PATCH; `ci` e `build` ficaram
  visíveis na primeira configuração e um commit `ci` abriu a v0.1.1 indevidamente (PR #8,
  fechado). Ocultá-los mantém a regra de `docs/01` §5.1: só `feat`, `fix`, `perf` e `revert`
  geram versão.
* Formato do changelog: o do release-please, com as seções do Keep a Changelog. Não há mais
  seção `[Unreleased]`: o que não foi lançado está no PR de release aberto.
* Primeira versão: `release-as: 0.1.0` agrupou todo o histórico em `v0.1.0` (2026-10-17); a
  chave foi removida em seguida, como a documentação manda.
* Token: PRs criados com `GITHUB_TOKEN` não disparam a CI, então o auto-merge não completaria.
  O workflow usa o secret `RELEASE_PLEASE_TOKEN` (token pessoal fine-grained com Contents e
  Pull requests em leitura e escrita) e cai para `GITHUB_TOKEN` se o secret não existir; nesse
  caso o PR de release fica para merge manual.
* O branch do bot (`release-please--branches--main`) é isento de `check-branch`.

### Consequências

* Bom, porque toda mudança com `feat` ou `fix` vira versão sem trabalho manual e sem bypass.
* Bom, porque o changelog deixa de ser editado à mão: a descrição do commit é a entrada.
* Ruim, porque a qualidade do changelog depende da qualidade das descrições dos commits.
* Ruim, porque o template precisa de um secret configurado à mão em cada repositório gerado.
* Ruim, porque a tag criada pela GitHub Release é leve, não anotada; a Release carrega as notas.
