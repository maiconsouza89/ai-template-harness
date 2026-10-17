# Padrões do repositório e suas fontes

Cada padrão adotado, onde ele vive no repositório e a fonte oficial que o fundamenta. O "como"
está em `CONTRIBUTING.md`; o "por quê" de cada escolha, com as alternativas descartadas, está em
`docs/decisions/`. Motivo de registrar tudo em arquivos: para um agente, o que não está no
repositório não existe. Convenções viram arquivos versionados e, sempre que possível,
verificação automática (`make check`).

## Decisões

| Tema | Decisão | Vive em | Fonte | ADR |
| --- | --- | --- | --- | --- |
| Branch padrão | `main` | — | git-init | 0001 |
| Modelo de branches | GitHub Flow; branches `<tipo>/<descricao>`; merge por squash; branch apagado | `scripts/check-branch.sh`, ruleset | GitHub Docs (GitHub flow) | 0001 |
| Commits | Conventional Commits 1.0.0; tipos do `config-conventional` em inglês; descrição em português; cabeçalho ≤ 72 caracteres | `.githooks/commit-msg`, `pr-title.yml` | conventionalcommits.org, commitlint, cbea.ms | 0001 |
| Versionamento | SemVer 2.0.0, início em `0.1.0`; tag `vX.Y.Z` criada pela GitHub Release | `release-please-config.json` | semver.org | 0001, 0004 |
| Changelog | Gerado pelo release-please, seções do Keep a Changelog em português | `CHANGELOG.md` | keepachangelog.com, release-please | 0004 |
| Release | Automática a cada merge em `main`, por PR de release com auto-merge | `.github/workflows/release.yml` | release-please | 0004 |
| Texto | UTF-8 e LF | `.editorconfig`, `.gitattributes` | editorconfig.org, gitattributes | 0001 |
| Validação local | Hook `commit-msg` em POSIX `sh`, ativado por `core.hooksPath` | `.githooks/`, `scripts/setup.sh` | githooks | 0001 |
| Harness | `AGENTS.md` como fonte; `CLAUDE.md` importa; `Makefile` como superfície única | raiz | agents.md, Claude Code memory | 0002 |
| Stack | Agnóstico por contrato de alvos (`lint`, `format`, `test`, `build`) | `Makefile`, `scripts/contract.sh` | — | 0003 |
| CI | `make check` e título do PR como checks obrigatórios; actions fixadas por SHA | `.github/workflows/` | GitHub Docs, OpenSSF | 0003 |
| Decisões | ADRs no formato MADR 4.0, em português | `docs/decisions/` | adr.github.io/madr | 0000 |
| Licença | MIT | `LICENSE` | choosealicense.com | 0001 |
| Assinatura de commits | Não adotada | — | — | 0001 |

## Configuração do GitHub

Nada disto vem junto com "Use this template"; precisa ser aplicado em cada repositório gerado.

1. **Pull requests**: só *squash merging*, título e corpo do PR como mensagem, *Allow auto-merge*,
   *Automatically delete head branches*.
2. **Actions**: *Allow GitHub Actions to create and approve pull requests* (fallback sem token).
3. **Secret `RELEASE_PLEASE_TOKEN`**: token pessoal fine-grained com *Contents* e *Pull requests*
   em leitura e escrita, para a CI rodar no PR de release.
4. **Ruleset `main`** (Active): *Restrict deletions*, *Block force pushes*, *Require a pull request
   before merging*, *Require status checks* `check` e `pr-title`.
5. **Template repository**: marcar em General, só no repositório do template.

## Referências

- Conventional Commits 1.0.0: https://www.conventionalcommits.org/pt-br/v1.0.0/
- Tipos de commit (`config-conventional`): https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional
- Chris Beams, How to Write a Git Commit Message: https://cbea.ms/git-commit/
- SemVer 2.0.0: https://semver.org/lang/pt-BR/
- Keep a Changelog 1.1.0: https://keepachangelog.com/en/1.1.0/
- release-please: https://github.com/googleapis/release-please
- GitHub Flow: https://docs.github.com/en/get-started/using-github/github-flow
- GitHub: squash merge https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests · rulesets https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets · template repository https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository · community files https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
- Git: githooks https://git-scm.com/docs/githooks · gitattributes https://git-scm.com/docs/gitattributes · gitignore https://git-scm.com/docs/gitignore
- EditorConfig: https://editorconfig.org/
- MADR 4.0: https://adr.github.io/madr/
- Harness engineering: OpenAI https://openai.com/index/harness-engineering · Anthropic https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents · Adobe https://opensource.adobe.com/ai-repo-harness-guide/ · AGENTS.md https://agents.md/ · Claude Code memory https://code.claude.com/docs/en/memory
- Fixação de actions por SHA: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#using-third-party-actions
