# Preparar o ambiente

## Requisitos

| Ferramenta | Versão | Uso |
| --- | --- | --- |
| Git | ≥ 2.9 | `core.hooksPath` |
| POSIX `sh` | qualquer | hooks e scripts |
| GNU Make | ≥ 3.81 | `make setup`, `make check` |
| shellcheck | opcional | lint dos scripts em `make check-shell`; sem ele, só a sintaxe é validada |

No Windows, use WSL ou Git Bash (ambos trazem `sh`; `make` vem via WSL, Chocolatey ou Scoop).

## Passos

```sh
git clone git@github.com:maiconsouza89/ai-template-harness.git
cd ai-template-harness
make setup    # aponta core.hooksPath para .githooks/
make check    # confirma que tudo passa
```

`make setup` é o único passo manual após o clone. O Git não ativa hooks sozinho por segurança.

## Git na máquina (uma vez por pessoa)

```sh
git config --global user.name  "Seu Nome"
git config --global user.email "voce@exemplo.com"
git config --global init.defaultBranch main
```

## Editor

`.editorconfig` cuida de UTF-8, LF e indentação. No VS Code, aceite a extensão recomendada em
`.vscode/extensions.json` (EditorConfig).
