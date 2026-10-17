# Padrões de trabalho do repositório

> Parcialmente substituído: a linha "Changelog" pelo ADR 0004 (gerado pelo release-please) e a
> evolução da validação local pelo ADR 0003 (CI agnóstica). O restante continua em vigor.

## Contexto e problema

O template precisa de convenções de Git, commits, versionamento e changelog antes de qualquer
escolha de linguagem ou pipeline. As decisões devem ser agnósticas de stack, mínimas para começar
e verificáveis por máquina sempre que possível. Fundamentação e fontes em
`docs/STANDARDS.md`.

## Opções consideradas

| Tema | Escolhida | Alternativas consideradas |
| --- | --- | --- |
| Modelo de branches | GitHub Flow, branches `<tipo>/<descricao>` com os tipos do commit | Git Flow, trunk-based com flags; nomes livres |
| Merge de PR | Squash | Rebase, merge commit |
| Commits | Conventional Commits 1.0.0, tipos em inglês, descrição em português | Descrição em inglês; formato livre |
| Versionamento | SemVer 2.0.0, tag `vX.Y.Z` | CalVer |
| Changelog | Keep a Changelog 1.1.0 (substituído: ADR 0004) | Gerado só a partir dos commits |
| Validação local | Hook `commit-msg` em POSIX sh em `.githooks/` | pre-commit + conventional-pre-commit; lefthook; commitlint + husky; cocogitto; só na CI |
| Decisões | MADR 4.0 | Nygard; sem ADR |
| Licença | MIT | Apache-2.0; sem licença |
| Assinatura de commits | Não configurar | Opcional via SSH; obrigatória no ruleset |
| Idioma da documentação | pt-BR | Inglês; pt-BR agora e inglês depois |

## Decisão

Opção escolhida: a coluna "Escolhida" da tabela, porque atende ao mínimo para começar sem impor
stack: o hook em `sh` não depende de Node nem de Python; squash mantém `main` linear com um
commit por PR, cujo título segue Conventional Commits; MIT é a licença mais simples para um
template; a assinatura de commits fica de fora até haver mais colaboradores; a descrição do commit
em português facilita o time, enquanto os tipos em inglês mantêm compatibilidade com ferramentas.

### Consequências

* Bom, porque todas as convenções estão em arquivos versionados e o hook verifica o cabeçalho.
* Bom, porque nenhuma ferramenta de stack é imposta ao template.
* Ruim, porque o hook em `sh` cobre só o cabeçalho; regras mais ricas ficam para a migração.
* Ruim, porque commits em português e bots em inglês (Dependabot) vão misturar idiomas no histórico.
