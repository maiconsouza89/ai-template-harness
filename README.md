# ai-template-harness

[![CI](https://github.com/maiconsouza89/ai-template-harness/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/maiconsouza89/ai-template-harness/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/maiconsouza89/ai-template-harness)](https://github.com/maiconsouza89/ai-template-harness/releases)
[![License: MIT](https://img.shields.io/github/license/maiconsouza89/ai-template-harness)](LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-fe5196?logo=conventionalcommits&logoColor=white)](https://www.conventionalcommits.org/pt-br/v1.0.0/)
[![Use this template](https://img.shields.io/badge/Use%20this-template-2ea44f?logo=github)](https://github.com/maiconsouza89/ai-template-harness/generate)

Template de repositório para desenvolvimento assistido por IA, construído em torno de
*harness engineering*: convenções viram arquivos versionados e, sempre que possível,
verificação automática. O que não está no repositório não existe para o agente.

## Como usar

1. No GitHub, clique em **Use this template** e crie o seu repositório.
2. Clone, ative os hooks e confira que tudo passa:

   ```sh
   make setup
   make check
   ```

3. Aplique o que "Use this template" não copia e zere o que ele copia demais:

   ```sh
   sh scripts/templates/bootstrap-github.sh   # PRs só por squash, auto-merge, ruleset de main com os checks
   sh scripts/templates/reset-template.sh     # remove o CHANGELOG do template e zera a versão
   ```

   O bootstrap avisa se falta o secret `RELEASE_PLEASE_TOKEN` e diz como criá-lo. Detalhes em
   [`docs/STANDARDS.md`](docs/STANDARDS.md#configuração-do-github).

4. Substitua este README pelo do seu projeto, implemente `scripts/lint.sh`, `format.sh`,
   `test.sh` e `build.sh` para a sua stack e registre a escolha em um ADR
   ([`docs/ADR/README.md`](docs/ADR/README.md)).
5. Leia o [guia de contribuição](CONTRIBUTING.md). Agentes de código começam por
   [`CLAUDE.md`](CLAUDE.md).

## O que está incluído

Instruções para agentes (`CLAUDE.md`), `Makefile` com `make check`, hook de commit, CI agnóstica
de stack e release automática. O mapa completo está em [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md);
cada padrão e sua fonte, em [`docs/STANDARDS.md`](docs/STANDARDS.md).

## Licença

[MIT](LICENSE).
