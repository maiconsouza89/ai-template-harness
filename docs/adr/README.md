# Architecture Decision Records

ADRs são imutáveis depois de aceitos: uma decisão muda por meio de um ADR novo, que preenche
`supersedes`, enquanto o antigo recebe `superseded_by` e o status `superseded`. Os ADRs do
template carregam a chave opcional `layer` (ver 0006); ela não é exigida em registros novos.
Regras completas em `.claude/skills/docs-init/references/convencoes.md`; modelo em
`../templates/adr.md`; crie registros com a skill `adr`.

| Número | Título | Status | Data |
|---|---|---|---|
| 0001 | [Adotar GitHub Flow, Conventional Commits e SemVer](0001-adotar-github-flow-conventional-commits-e-semver.md) | accepted | 2026-10-16 |
| 0002 | [Usar CLAUDE.md como fonte única e Makefile como interface](0002-usar-claude-md-como-fonte-e-makefile-como-interface.md) | accepted | 2026-10-19 |
| 0003 | [Manter o template agnóstico por contrato de alvos e CI sem stack](0003-manter-o-template-agnostico-por-contrato-de-alvos.md) | accepted | 2026-10-17 |
| 0004 | [Automatizar a release com release-please e auto-merge](0004-automatizar-release-com-release-please.md) | accepted | 2026-10-17 |
| 0005 | [Adotar o formato da skill adr-writer em docs/ADR](0005-adotar-o-formato-adr-writer-em-docs-adr.md) | superseded | 2026-10-17 |
| 0006 | [Organizar as decisões nas camadas workflow, harness, ci e release](0006-organizar-as-decisoes-por-camada.md) | accepted | 2026-10-17 |
| 0007 | [Adotar o sistema de documentação docs-init em docs](0007-adotar-o-sistema-de-documentacao-docs-init-em-docs.md) | accepted | 2026-10-21 |
