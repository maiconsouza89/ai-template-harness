# Arquitetura do repositório

Estrutura atual e regra de onde colocar cada coisa. O template não tem stack (ver
`decisions/0003`); diretórios de código entram no projeto gerado a partir dele.

## Mapa

```text
.
├── AGENTS.md              Instruções para agentes (fonte única). Mapa, não manual.
├── CLAUDE.md              Importa AGENTS.md; só o específico do Claude Code.
├── Makefile               Superfície única de comandos: make setup, make check.
├── README.md              Para pessoas: o que é e como usar o template.
├── CONTRIBUTING.md        Fluxo de trabalho, commits, PRs, versões.
├── CHANGELOG.md           Gerado pelo release-please; não editar (decisions/0004).
├── release-please-config.json, .release-please-manifest.json   Configuração da release.
├── LICENSE                MIT.
├── .editorconfig          UTF-8, LF, indentação.
├── .gitattributes         Fim de linha por tipo de arquivo; vence o core.autocrlf.
├── .gitignore             Só o comum a qualquer stack.
├── .githooks/             Hooks versionados (commit-msg). Ativados por make setup.
├── .github/               ISSUE_TEMPLATE/ (formulários de bug e funcionalidade),
│                          pull_request_template.md (checklist do PR) e workflows/:
│                          ci.yml (make check), pr-title.yml (título do PR),
│                          release.yml (release-please + auto-merge).
├── .vscode/               extensions.json: extensões recomendadas (EditorConfig).
├── scripts/               Lógica dos alvos do Makefile, em POSIX sh. check-*.sh verificam;
│                          contract.sh despacha lint/format/test/build para <alvo>.sh se existir.
│                          O projeto gerado adiciona lint.sh, format.sh, test.sh, build.sh.
│                          bootstrap-github.sh e reset-template.sh: pós-"Use this template".
└── docs/
    ├── ARCHITECTURE.md    Este arquivo.
    ├── SETUP.md           Preparar o ambiente.
    ├── STANDARDS.md       Cada padrão, onde vive, fonte oficial e configuração do GitHub.
    ├── TESTING.md         O que make check valida.
    └── decisions/         ADRs (MADR), um por decisão; README.md tem o template.
```

## Onde colocar o quê

| Conteúdo | Lugar | Motivo |
| --- | --- | --- |
| Instrução para agente que vale para todo o repositório | `AGENTS.md` | Lido por todas as ferramentas; `CLAUDE.md` importa |
| Instrução só do Claude Code | `CLAUDE.md` | Sem duplicar o conteúdo de `AGENTS.md` |
| Preferência pessoal | `CLAUDE.local.md` (ignorado) | Não polui o repositório |
| Comando que pessoa ou agente executa | Alvo no `Makefile` chamando `scripts/*.sh` | Uma porta de entrada, lógica testável em sh |
| Verificação automática | `scripts/check-*.sh` e alvo `check-*` | `make check` agrega tudo; a CI roda o mesmo |
| Implementação de lint, format, test, build da stack | `scripts/<alvo>.sh` no projeto gerado | O contrato do `Makefile` não muda; ver `decisions/0003` |
| Decisão de padrão ou arquitetura | `docs/decisions/NNNN-*.md` | Histórico com alternativas descartadas |
| Explicação longa, com fontes | `docs/*.md` | `AGENTS.md` aponta, não repete |
| Arquivo de comunidade (`CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`) | Raiz | Reconhecido pelo GitHub; `LICENSE` só é detectado na raiz |

## Princípios

- **Raiz é contrato, `docs/` é conhecimento.** Um `ls` na raiz mostra como trabalhar; `docs/`
  explica por quê.
- **Convenção vira arquivo, arquivo vira verificação.** Toda regra em `AGENTS.md` deve ter, quando
  possível, um `check-*` que a aplica.
- **Agnóstico por contrato.** Nada no template depende de linguagem. O `Makefile` fixa a interface
  (`lint`, `format`, `test`, `build`); o projeto gerado implementa `scripts/<alvo>.sh` e registra
  um ADR (`decisions/0003`).
