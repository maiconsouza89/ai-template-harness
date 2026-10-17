# ai-template-harness

Template de repositório para desenvolvimento assistido por IA, construído em torno de
*harness engineering*: convenções viram arquivos versionados e, sempre que possível,
verificação automática. O que não está no repositório não existe para o agente.

## Como usar

1. No GitHub, clique em **Use this template** e crie o seu repositório.
2. Clone e ative os hooks versionados (passo único por clone):

   ```sh
   make setup
   make check
   ```

3. Leia o [guia de contribuição](CONTRIBUTING.md) e os padrões em [`docs/`](docs/).
   Agentes de código começam por [`AGENTS.md`](AGENTS.md).

## O que está incluído

Instruções para agentes (`AGENTS.md`), `Makefile` com `make check`, hook de commit, CI agnóstica
de stack e release automática. O mapa completo está em [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md);
cada padrão e sua fonte, em [`docs/STANDARDS.md`](docs/STANDARDS.md).

## Padrões

- Commits: Conventional Commits 1.0.0, tipos em inglês, descrição em português.
- Versões: SemVer 2.0.0, tag `vX.Y.Z` criada pela GitHub Release a cada merge com `feat` ou `fix`.
- Branches: GitHub Flow, merge por squash, `main` protegido.

## Licença

[MIT](LICENSE).
