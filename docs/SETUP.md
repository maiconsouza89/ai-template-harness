# Preparar o ambiente

## Requisitos

| Ferramenta | Versão | Uso |
| --- | --- | --- |
| Git | ≥ 2.22 | `core.hooksPath`, `git branch --show-current` |
| POSIX `sh` | qualquer | hooks e scripts |
| GNU Make | ≥ 3.81 | `make setup`, `make check` |
| shellcheck | opcional | lint dos scripts em `make check-shell`; sem ele, só a sintaxe é validada |
| actionlint | opcional | valida os workflows em `make check-actions`; sem ele, pula com aviso |
| gitleaks | opcional | procura segredos em `make check-secrets`; sem ele, pula com aviso |
| python3 | opcional | validação de `docs/` em `make check-docs`; sem ele, pula com aviso |

As ferramentas opcionais são obrigatórias na CI (`CI=true` faz o check falhar se faltarem).

No Windows, use WSL ou Git Bash (ambos trazem `sh`; `make` vem via WSL, Chocolatey ou Scoop).

## Passos

```sh
git clone git@github.com:<owner>/<repo>.git
cd <repo>
make setup    # aponta core.hooksPath para .githooks/
make check    # confirma que tudo passa
```

`make setup` é o único passo manual após o clone. O Git não ativa hooks sozinho por segurança.

## Editor

`.editorconfig` cuida de UTF-8, LF e indentação. No VS Code, aceite a extensão recomendada em
`.vscode/extensions.json` (EditorConfig).
