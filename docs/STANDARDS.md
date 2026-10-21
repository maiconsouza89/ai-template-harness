# Padrões do repositório e suas fontes

Cada padrão adotado, onde ele vive no repositório e a fonte oficial que o fundamenta. O "como"
está em `CONTRIBUTING.md`; o "por quê" de cada escolha, com as alternativas descartadas, está em
`docs/adr/`. Motivo de registrar tudo em arquivos: para um agente, o que não está no
repositório não existe. Convenções viram arquivos versionados e, sempre que possível,
verificação automática (`make check`).

## Decisões

| Tema | Decisão | Vive em | Fonte | ADR |
| --- | --- | --- | --- | --- |
| Branch padrão | `main` | — | git-init | 0001 |
| Modelo de branches | GitHub Flow; branches `<tipo>/<descricao>`; merge por squash; branch apagado | `scripts/checks/check-branch.sh`, ruleset | GitHub Docs (GitHub flow) | 0001 |
| Commits | Conventional Commits 1.0.0 (formato em `CONTRIBUTING.md`) | `.githooks/commit-msg`, `pr-title.yml` | conventionalcommits.org, commitlint, cbea.ms | 0001 |
| Versionamento | SemVer 2.0.0, início em `0.1.0`; tag `vX.Y.Z` criada pela GitHub Release | `release-please-config.json` | semver.org | 0001, 0004 |
| Changelog | Gerado pelo release-please, seções do Keep a Changelog em português | `CHANGELOG.md` | keepachangelog.com, release-please | 0004 |
| Release | Automática a cada merge em `main`, por PR de release com auto-merge | `.github/workflows/release.yml` | release-please | 0004 |
| Texto | UTF-8 e LF | `.editorconfig`, `.gitattributes` | editorconfig.org, gitattributes | 0001 |
| Validação local | Hook `commit-msg` em POSIX `sh`, ativado por `core.hooksPath` | `.githooks/`, `scripts/setup.sh` | githooks | 0001 |
| Harness | `CLAUDE.md` como fonte única; `Makefile` como superfície única | raiz | Claude Code memory | 0002 |
| Stack | Agnóstico por contrato de alvos (`lint`, `format`, `test`, `build`) | `Makefile`, `scripts/contract.sh` | — | 0003 |
| CI | `make check` e título do PR como checks obrigatórios; actions fixadas por SHA | `.github/workflows/` | GitHub Docs, OpenSSF | 0003 |
| Decisões | ADRs em português com front-matter e índice mantido por script (skill `adr`) | `docs/adr/`, `.claude/skills/adr/` | adr.github.io/madr | 0006, 0007 |
| Documentação | `docs/` por tipo; convenções em `docs/README.md`; validação em `make check-docs` (skill `docs-init`) | `docs/README.md`, `.claude/skills/docs-init/` | — | 0007 |
| Licença | MIT | `LICENSE` | choosealicense.com | 0001 |
| Assinatura de commits | Não adotada | — | — | 0001 |

## Configuração do GitHub

Nada disto vem junto com "Use this template". `scripts/templates/bootstrap-github.sh` aplica os itens 1, 2 e 4
via `gh`; o 3 é manual (o script avisa); o 5 só vale para o template.

1. **Pull requests**: só *squash merging*, título e corpo do PR como mensagem, *Allow auto-merge*,
   *Automatically delete head branches*.
2. **Actions**: *Allow GitHub Actions to create and approve pull requests* (fallback sem token).
3. **Secret `RELEASE_PLEASE_TOKEN`**: token pessoal fine-grained com *Contents* e *Pull requests*
   em leitura e escrita, para a CI rodar no PR de release.
4. **Ruleset `main`** (Active): *Restrict deletions*, *Block force pushes*, *Require a pull request
   before merging*, *Require status checks* `check` e `pr-title`.
5. **Template repository**: marcar em General, só no repositório do template.

## Referências

As fontes de cada padrão estão na seção Referências do ADR correspondente. Sobre harness
engineering, que não tem ADR próprio: OpenAI https://openai.com/index/harness-engineering ·
Anthropic https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents ·
Adobe https://opensource.adobe.com/ai-repo-harness-guide/
