# Passo 1 — Fundação do repositório: Git, Conventional Commits e SemVer

> Status: aprovado e implementado · Data: 2026-10-16 · Escopo: agnóstico de stack, mínimo para começar
> Decisões registradas em `docs/decisions/0001-padroes-de-trabalho-do-repositorio.md`.

Define como trabalhamos no repositório antes de qualquer decisão de linguagem ou pipeline.
Cada decisão traz a fonte oficial. O que não está aqui fica para os próximos passos (§7).

---

## 1. Decisões

| Tema | Decisão | Fonte |
| --- | --- | --- |
| Branch padrão | `main` | git-init |
| Modelo de branches | GitHub Flow: branch curto a partir de `main`, PR, revisão, merge por squash, branch apagado | GitHub Docs (GitHub flow) |
| Commits | Conventional Commits 1.0.0, tipos do `config-conventional` em inglês, descrição em português, cabeçalho ≤ 72 caracteres | conventionalcommits.org, commitlint, cbea.ms |
| Versionamento | SemVer 2.0.0, início em `0.1.0`, tag anotada `vX.Y.Z` como fonte da verdade | semver.org, Pro Git |
| Changelog | Seções do Keep a Changelog em `CHANGELOG.md`, gerado pelo release-please | keepachangelog.com, release-please |
| Texto | LF e UTF-8 via `.gitattributes` e `.editorconfig` | gitattributes, editorconfig.org |
| Validação local | Hook `commit-msg` em `sh` puro, versionado em `.githooks/` | githooks |
| Decisões | ADRs no formato MADR 4.0 em `docs/decisions/` | adr.github.io/madr |
| Licença | MIT | choosealicense.com |
| Assinatura de commits | Não adotada neste passo | — |

Motivo de registrar tudo em arquivos: para um agente, o que não está no repositório não existe.
Convenções viram arquivos versionados e, sempre que possível, verificação automática.

---

## 2. Git na máquina (uma vez por pessoa)

```sh
git config --global user.name  "Seu Nome"
git config --global user.email "voce@exemplo.com"
git config --global init.defaultBranch main
```

Não adotado neste passo (decisão em §6): assinatura de commits. Se for adotada depois, usar a
chave SSH (Git ≥ 2.34) cadastrada no GitHub como *Signing key*:

```sh
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

---

## 3. Inicializar

```sh
git init -b main ai-template-harness
```

Já feito neste repositório: branch `main`, remoto `maiconsouza89/ai-template-harness`.

---

## 4. Arquivos mínimos

```text
.
├── .editorconfig
├── .gitattributes
├── .githooks/commit-msg
├── .gitignore
├── .vscode/settings.json, extensions.json
├── CHANGELOG.md                (gerado; ver ADR 0004)
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── docs/
│   ├── 01-fundacao-git-e-padroes.md   (este documento)
│   └── decisions/
│       ├── 0000-usar-markdown-architectural-decision-records.md
│       └── 0001-padroes-de-trabalho-do-repositorio.md
└── scripts/setup.sh           (demais scripts e o Makefile: passo 2, docs/ARCHITECTURE.md)
```

### 4.1 `.editorconfig`

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

### 4.2 `.gitattributes`

Atributos têm precedência sobre o `core.autocrlf` de cada máquina, então todos têm o mesmo
resultado.

```gitattributes
*        text=auto eol=lf
*.sh     text eol=lf
*.bat    text eol=crlf
*.ps1    text eol=crlf
*.png    binary
*.jpg    binary
*.pdf    binary
```

### 4.3 `.gitignore`

Só o comum a qualquer stack. Regras de linguagem entram com a stack. Em `.vscode/`, só
`settings.json` e `extensions.json` são versionados (fim de linha e extensão EditorConfig
recomendada); o resto é pessoal.

```gitignore
.env
.env.*
!.env.example
*.pem
CLAUDE.local.md
.DS_Store
Thumbs.db
.idea/
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json
*.log
tmp/
```

### 4.4 `.githooks/commit-msg`

POSIX `sh`, sem dependências. Testado com 22 cabeçalhos válidos e inválidos. Precisa de `chmod +x`.
Adaptado para descrição em português: `LC_ALL=C.UTF-8` para acentos no regex, tamanho medido em
caracteres com `wc -m` (não em bytes), e o primeiro caractere da descrição pode ser acentuado,
mas não maiúsculo ASCII.

Alternativas consideradas e registradas no ADR 0001: pre-commit com `conventional-pre-commit`,
lefthook, commitlint com husky, cocogitto, validação só na CI. A escolha pode mudar quando a
stack for definida; `scripts/setup.sh` continua sendo a porta de entrada.

```sh
#!/bin/sh
# Valida o cabeçalho da mensagem segundo Conventional Commits 1.0.0.
# Ativado por `git config core.hooksPath .githooks` (ver scripts/setup.sh).
# Tipos e escopos em inglês; descrição em português.

export LC_ALL=C.UTF-8

msg_file="$1"
header=$(sed -n '1p' "$msg_file")

case "$header" in
  "Merge "*|"fixup! "*|"squash! "*|"Revert "*) exit 0 ;;
esac

types='build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test'
pattern="^($types)(\([a-z0-9._/-]+\))?!?: [^A-Z[:space:]].*[^.[:space:]]$"

fail() {
  printf '%s\n' "commit-msg: cabeçalho inválido:" "  $header" "" "$1" "" \
    "Formato: <tipo>[(escopo)][!]: <descrição>" \
    "Tipos:   $types" \
    "Regras:  descrição em minúsculas, no imperativo, sem ponto final, até 72 caracteres" \
    "Exemplo: feat(hooks): valida cabeçalho do commit" >&2
  exit 1
}

length=$(printf '%s' "$header" | wc -m | tr -d ' ')
[ "$length" -le 72 ] || fail "O cabeçalho tem $length caracteres (máximo 72)."
printf '%s\n' "$header" | grep -Eq "$pattern" || fail "O cabeçalho não segue o padrão Conventional Commits."

second=$(sed -n '2p' "$msg_file")
[ -z "$second" ] || fail "A segunda linha deve estar em branco (separa cabeçalho e corpo)."

exit 0
```

### 4.5 `scripts/setup.sh`

Hooks ficam em `.git/hooks`, fora do clone. Este script aponta o Git para a pasta versionada. É o
único passo manual após clonar.

```sh
#!/bin/sh
set -eu
cd "$(git rev-parse --show-toplevel)"
git config core.hooksPath .githooks
chmod +x .githooks/*
echo "ok: hooks ativados"
```

### 4.6 `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`

| Arquivo | Conteúdo mínimo |
| --- | --- |
| `README.md` | O que é o template, como usar ("Use this template"), rodar `scripts/setup.sh`, link para `CONTRIBUTING.md` |
| `LICENSE` | Texto integral da licença (premissa: MIT). Na raiz, nome em caixa alta, para o GitHub detectar |
| `CONTRIBUTING.md` | Fluxo GitHub Flow (§5.3), formato de commit (§5.1), como rodar o setup. O GitHub mostra o link ao abrir PRs |
| `CHANGELOG.md` | Esqueleto abaixo |

```markdown
# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versionamento: [SemVer](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
```

### 4.7 `docs/decisions/`

Um arquivo por decisão, `NNNN-titulo-com-hifens.md`, template mínimo do MADR 4.0 com a estrutura
original e o texto em português (títulos e frases fixas incluídos):

```markdown
# {título curto: problema e solução}

## Contexto e problema

{duas a três frases}

## Opções consideradas

* {opção 1}
* {opção 2}

## Decisão

Opção escolhida: "{opção 1}", porque {justificativa}.

### Consequências

* Bom, porque {...}
* Ruim, porque {...}
```

ADRs iniciais: `0000` adota MADR (o próprio MADR distribui esse ADR); `0001` registra a tabela do §1.

---

## 5. Padrões

### 5.1 Commits

```text
<tipo>[(escopo)][!]: <descrição>

[corpo]

[rodapé(s)]
```

| Tipo | Uso | SemVer |
| --- | --- | --- |
| `feat` | Nova funcionalidade | MINOR |
| `fix` | Correção | PATCH |
| `perf` | Desempenho | PATCH |
| `refactor`, `docs`, `style`, `test`, `build`, `ci`, `chore`, `revert` | Sem efeito, salvo breaking change | nenhum |

- Breaking change: `!` antes dos dois-pontos ou rodapé `BREAKING CHANGE: ...`. Efeito MAJOR.
- Cabeçalho: minúsculas, imperativo, sem ponto final, até 72 caracteres (GitHub trunca acima).
- Corpo: o quê e por quê, em 72 colunas, separado por linha em branco.
- Rodapés no formato `Token: valor` (`Refs: #12`, `Co-authored-by: ...`).
- Idioma: tipos e escopos em inglês (tokens das ferramentas); descrição em português.

```text
feat(hooks): valida cabeçalho de commit com hook commit-msg
fix(gitattributes): mantém crlf em scripts powershell
chore!: exige commits assinados
```

Com squash merge, o **título do PR** vira o cabeçalho do commit em `main` e segue a mesma regra.

### 5.2 Versões

- Primeira versão `0.1.0`. Enquanto `0.y.z`: `feat` e breaking change sobem MINOR; `fix` sobe PATCH.
- A partir de `1.0.0`: breaking → MAJOR, `feat` → MINOR, `fix` → PATCH. Vai para `1.0.0` quando
  houver uso real e mudanças incompatíveis custarem para quem usa.
- A tag `vX.Y.Z` é a fonte da verdade; `.release-please-manifest.json` guarda a última versão
  lançada. A versão é `X.Y.Z`; o `v` é só convenção de tag.

Release automática (ADR 0004): a cada push em `main`, o release-please abre ou atualiza o PR
`chore(release): vX.Y.Z` com versão e `CHANGELOG.md` calculados dos commits. O PR entra em
auto-merge; quando os checks passam, o GitHub mescla, cria a tag e a GitHub Release. Ninguém
edita o `CHANGELOG.md` à mão.

Mapeamento para o changelog: `feat` → Adicionado, `fix` → Corrigido, `perf` → Alterado,
`revert` → Revertido. Demais tipos ficam de fora e não geram versão.

### 5.3 GitHub Flow

Os seis passos da documentação do GitHub:

1. Criar um branch a partir de `main` no formato `<tipo>/<descricao-com-hifens>`, com os mesmos
   tipos do commit: `feat/hook-commit-msg`, `fix/crlf-powershell`. O GitHub sugere nomes curtos
   e descritivos; o prefixo de tipo alinha o branch ao commit e ao título do PR.
2. Fazer commits convencionais no branch.
3. Abrir o pull request com título em Conventional Commits.
4. Responder à revisão.
5. Fazer merge por squash.
6. Apagar o branch.

`main` só recebe mudanças por PR. Sem branches permanentes de `develop` ou `release`.

### 5.4 Configuração do GitHub

1. **Pull Requests**: permitir só *squash merging*, mensagem padrão "Pull request title and
   description", *Automatically delete head branches*.
2. **Ruleset `main`** (Active): *Restrict deletions*, *Block force pushes*, *Require a pull request
   before merging*. Status checks entram com a CI; *Require signed commits* se a assinatura for
   adotada.
3. **Template repository**: marcar em General.

---

## 6. Premissas confirmadas (2026-10-16)

| Item | Decisão | Alternativas consideradas |
| --- | --- | --- |
| Idioma dos commits | Português na descrição; tipos em inglês | Inglês |
| Idioma da documentação | pt-BR | Inglês; pt-BR agora e inglês depois |
| Licença | MIT | Apache-2.0; sem licença |
| Assinatura de commits | Não configurar | Opcional via SSH; obrigatória no ruleset |
| Validação local | Hook `sh` em `.githooks/` | pre-commit; lefthook; commitlint + husky; cocogitto; só CI |
| Merge | Squash | Rebase; merge commit |
| `.vscode/` | Versionar `settings.json` e `extensions.json` | Ignorar tudo; não ignorar |
| ADRs | MADR 4.0 mínimo | Nygard; sem ADR |
| Primeira tag | Só após o passo 2 | `v0.1.0` já na fundação |

---

## 7. Próximos passos

1. ~~**Harness base**~~: feito (ADR 0002): `AGENTS.md`, `CLAUDE.md`, `Makefile` com `make check`,
   `docs/ARCHITECTURE.md`, `SETUP.md`, `TESTING.md`.
2. ~~**Stack e CI**~~: redefinido e feito como **CI agnóstica** (ADR 0003): `make check` e
   título do PR como status checks obrigatórios; contrato de alvos no `Makefile` em vez de stack.
3. ~~**Automação de release**~~: feito (ADR 0004): release-please com auto-merge do PR de release.
4. **Arquivos de comunidade adicionais** quando houver colaboradores: `CODE_OF_CONDUCT.md`,
   `SECURITY.md`, `CODEOWNERS`, templates de issue e PR.

---

## 8. Referências

- Conventional Commits 1.0.0: https://www.conventionalcommits.org/en/v1.0.0/ (pt-BR: https://www.conventionalcommits.org/pt-br/v1.0.0/)
- SemVer 2.0.0: https://semver.org/spec/v2.0.0.html (pt-BR: https://semver.org/lang/pt-BR/)
- Keep a Changelog 1.1.0: https://keepachangelog.com/en/1.1.0/
- GitHub Flow: https://docs.github.com/en/get-started/using-github/github-flow
- Tipos de commit (`config-conventional`): https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional
- Chris Beams, How to Write a Git Commit Message: https://cbea.ms/git-commit/
- Pro Git, First-Time Setup: https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup
- Pro Git, Tagging: https://git-scm.com/book/en/v2/Git-Basics-Tagging
- git-init: https://git-scm.com/docs/git-init · gitattributes: https://git-scm.com/docs/gitattributes · gitignore: https://git-scm.com/docs/gitignore · githooks: https://git-scm.com/docs/githooks
- EditorConfig: https://editorconfig.org/
- MADR 4.0: https://adr.github.io/madr/
- GitHub: licença https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository · CONTRIBUTING https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors · squash merge https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests · rulesets https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets · template repository https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository · assinatura https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key
- Harness engineering: OpenAI https://openai.com/index/harness-engineering · Anthropic https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents · Adobe https://opensource.adobe.com/ai-repo-harness-guide/ · AGENTS.md https://agents.md/ · Claude Code memory https://code.claude.com/docs/en/memory
