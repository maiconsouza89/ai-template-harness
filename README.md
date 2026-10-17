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

| Arquivo | Função |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md` | Instruções para agentes de código; `CLAUDE.md` importa `AGENTS.md` |
| `Makefile`, `scripts/` | `make setup`, `make check`; lógica em POSIX sh |
| `.editorconfig`, `.gitattributes` | UTF-8, LF e indentação iguais em qualquer máquina |
| `.githooks/commit-msg` | Valida o cabeçalho do commit (Conventional Commits 1.0.0) |
| `CONTRIBUTING.md` | Fluxo de trabalho (GitHub Flow), commits e versões |
| `CHANGELOG.md` | Keep a Changelog 1.1.0 |
| `docs/decisions/` | Registros de decisão (ADR) no formato MADR 4.0 |
| `docs/ARCHITECTURE.md`, `SETUP.md`, `TESTING.md` | Estrutura, ambiente e verificações |
| `docs/01-fundacao-git-e-padroes.md` | Fundamentação de cada padrão, com fontes oficiais |

## Padrões

- Commits: Conventional Commits 1.0.0, tipos em inglês, descrição em português.
- Versões: SemVer 2.0.0, tag anotada `vX.Y.Z`.
- Branches: GitHub Flow, merge por squash, `main` protegido.

## Licença

[MIT](LICENSE).
