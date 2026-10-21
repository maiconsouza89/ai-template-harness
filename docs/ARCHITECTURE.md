# Arquitetura do repositório

Estrutura atual e regra de onde colocar cada coisa. O template não tem stack (ver
`adr/0003`); diretórios de código entram no projeto gerado a partir dele.

## Mapa

```text
.
├── CLAUDE.md              Instruções para agentes (fonte única). Mapa, não manual.
├── Makefile               Superfície única de comandos: make setup, make check.
├── README.md              Para pessoas: o que é e como usar o template.
├── CONTRIBUTING.md        Fluxo de trabalho, commits, PRs, versões.
├── CHANGELOG.md           Gerado pelo release-please; não editar (adr/0004).
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
├── .claude/               skills/ (docs-init, adr, fdd, docs-review) e agents/ (subagents que
│                          escrevem e revisam a documentação). Específico do Claude Code.
├── scripts/               Lógica dos alvos do Makefile, em POSIX sh.
│   ├── setup.sh           Ativa os hooks versionados (make setup).
│   ├── contract.sh        Despacha lint/format/test/build para scripts/<alvo>.sh se existir.
│   │                      O projeto gerado adiciona lint.sh, format.sh, test.sh, build.sh aqui.
│   ├── checks/            Verificações de make check (check-*.sh).
│   ├── tests/             Testes do próprio template (test-commit-msg.sh testa o hook).
│   └── templates/         Pós-"Use this template": bootstrap-github.sh e reset-template.sh.
└── docs/
    ├── ARCHITECTURE.md    Este arquivo.
    ├── SETUP.md           Preparar o ambiente.
    ├── STANDARDS.md       Cada padrão, onde vive, fonte oficial e configuração do GitHub.
    ├── TESTING.md         O que make check valida.
    ├── README.md          Fonte única das convenções e da estrutura da documentação do produto.
    ├── adr/               ADRs; README.md é o índice, mantido por new_adr.py.
    └── <tipo>/            product/, architecture/, features/, ... criados pela skill docs-init
                           no projeto gerado; tabela em docs/README.md.
```

## Onde colocar o quê

| Conteúdo | Lugar | Motivo |
| --- | --- | --- |
| Instrução para agente | `CLAUDE.md` | Fonte única; aponta para `docs/`, não repete |
| Preferência pessoal | `CLAUDE.local.md` (ignorado) | Não polui o repositório |
| Comando que pessoa ou agente executa | Alvo no `Makefile` chamando `scripts/*.sh` | Uma porta de entrada, lógica testável em sh |
| Verificação automática | `scripts/checks/check-*.sh` e alvo `check-*` | `make check` agrega tudo; a CI roda o mesmo |
| Implementação de lint, format, test, build da stack | `scripts/<alvo>.sh` no projeto gerado | O contrato do `Makefile` não muda; ver `adr/0003` |
| Decisão de padrão ou arquitetura | `docs/adr/NNNN-*.md` | Histórico com alternativas descartadas; skill `adr` numera e indexa |
| Requisitos, arquitetura e design de feature | `docs/<tipo>/` | Um template por tipo; ver `docs/README.md` |
| Explicação longa, com fontes | `docs/*.md` | `CLAUDE.md` aponta, não repete |
| Arquivo de comunidade (`CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`) | Raiz | Reconhecido pelo GitHub; `LICENSE` só é detectado na raiz |

## Princípios

- **Raiz é contrato, `docs/` é conhecimento.** Um `ls` na raiz mostra como trabalhar; `docs/`
  explica por quê.
- **Convenção vira arquivo, arquivo vira verificação.** Toda regra em `CLAUDE.md` deve ter, quando
  possível, um `check-*` que a aplica.
- **Agnóstico por contrato.** Nada no template depende de linguagem. O `Makefile` fixa a interface
  e o projeto gerado a implementa; ver `docs/TESTING.md` e `adr/0003`.
