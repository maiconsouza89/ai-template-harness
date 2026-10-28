# Fechamento: merge, push e PR

Só com avaliação limpa e com o fechamento autorizado no Passo 0. O trabalho já está feito quando isto roda; falha aqui vira aviso no relatório e o status continua sucesso, exceto conflito sem solução (pr bloqueado). Registre cada passo na seção Fechamento do diário.

## 1. Branch

`git branch --show-current` igual à `main` (ou ao branch padrão de `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`): não abra PR. O status continua sucesso, com o aviso "PR não aberto: o trabalho está no branch padrão; mova os commits para um branch `feat/...`". Pelo Passo 0 isso não deveria acontecer.

## 2. Merge da main

```
git fetch origin main
git merge origin/main
```

| Resultado | Próximo |
|---|---|
| Já atualizado | Seção 4 |
| Merge limpo | Seção 3 |
| Conflito (`git diff --name-only --diff-filter=U` não vazio) | `/fix-runner` modo conflito (`references/subagentes.md`). `corrigido`: seção 3. `validação falhou` ou `abortado`: status **pr bloqueado**, sem push e sem PR; diga no relatório os arquivos e o motivo, e que a pessoa resolve, commita e roda de novo |
| Outro erro do git (rede, fetch) | Aviso com o erro e siga para a seção 4 sem o merge |

Merge, não rebase: rebase reescreve commits já avaliados e exigiria push forçado.

## 3. Reavaliar depois do merge

O merge trouxe código da `main`; o veredito anterior não vale mais para o HEAD. Despache a `/evaluator` de novo.

- `limpo`: seção 4.
- Qualquer outro: volte ao Passo 2.2 do laço, com o orçamento que sobrou. Se terminar em sucesso de novo, **não** faça outro merge (um por execução, para não perseguir uma `main` que anda): siga para a seção 4. Se não terminar em sucesso, vá para Finalizar sem push nem PR.

## 4. Commit de registro

`avaliacao.md`, `orquestracao.md` (com a seção Fechamento preenchida até aqui) e `docs/product/roadmap.md`:

```
docs(<escopo>): registra avaliação de <RF-NNN | fundação>

Avaliação limpa em <N> ciclo(s) de correção.

Refs: <RF-NNN | fundacao>
```

## 5. Push

```
git push -u origin <branch>
```

Falhou (autenticação, remoto recusou): aviso com o motivo e o comando para rodar à mão; sem PR.

## 6. PR existente

```
gh pr list --head <branch> --json url,number --limit 1
```

Existe: o push já atualizou; registre a URL e termine.

## 7. PR novo

**Título**, no formato do hook e do `pr-title.yml`: `feat(<escopo>): <o que o RF entrega, em português, minúsculas>`, com até 72 caracteres. Na fundação: `feat(monorepo): monta a base do projeto` ou o que descrever melhor a entrega. Com squash, o título vira o commit na `main` e alimenta o CHANGELOG pelo release-please; escreva para quem lê o changelog.

**Issue**: `gh issue list --search "[RF-NNN] in:title" --state open --json number,title,url --limit 5` (fundação: `[fundação] in:title`), filtrando título que começa com o prefixo. Uma: `Closes #N`. Mais de uma: a primeira, e aviso com as outras. Nenhuma ou erro do `gh`: sem a linha.

**Corpo**, nas seções do `.github/pull_request_template.md`:

````markdown
## O quê e por quê

Implementa o **<RF-NNN Nome>** (<docs/features/<pasta>/>): <descrição do RF em uma frase, do PRD>.

Critérios de aceitação verificados pela avaliação (`avaliacao.md`):

- [x] <texto literal de cada critério, da tabela Critérios do avaliacao.md>

Ciclo: <F> fases pela implement-feature, <N> correções pela fix-runner, avaliação final limpa. Diário em `orquestracao.md`.

Closes #<N>

## Checklist

- [x] `make check` passa localmente.
- [x] Documentos afetados atualizados (`CONTRIBUTING.md`, `README.md`, `CLAUDE.md`, `docs/`).
- [ ] Se toma uma decisão de arquitetura ou tecnologia cara de reverter: ADR novo em `docs/architecture/adr/`.
- [ ] Se este é o repositório do template: a mudança continua agnóstica de stack.
````

Marque cada item da checklist pelo que de fato aconteceu: `make check` passou como gate na última avaliação; documentos, pelos registros das fases; ADR e agnosticismo, só se a execução tocou nisso. Item que você não conferiu fica desmarcado.

```
gh pr create --base main --title "<título>" --body "<corpo>"
```

Falhou: aviso com o motivo e o comando para rodar à mão.
