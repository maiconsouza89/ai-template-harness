---
title: Manter na raiz como trabalhar e em docs o produto e as decisões
type: adr
number: 0008
status: accepted
date: 2026-10-21
layer: harness
owners: [mantenedores do template]
supersedes: []
superseded_by: []
related: [0002, 0007]
---

# ADR-0008: Manter na raiz como trabalhar e em docs o produto e as decisões

## Contexto
Desde o ADR 0002, `docs/` guardava quatro documentos sobre o próprio template: `ARCHITECTURE.md`
(mapa do repositório), `SETUP.md` (ambiente), `STANDARDS.md` (tabela de padrões, configuração do
GitHub e lista de fontes) e `TESTING.md` (o que cada check valida). Com o ADR 0007, `docs/` passou
a ser a casa da documentação do produto, e os dois usos colidiram: no projeto gerado,
`docs/ARCHITECTURE.md` descreveria o template ao lado de `docs/architecture/hld-*.md`, que
descreve o produto. Além disso, boa parte desses quatro arquivos repetia o que já estava em
`CLAUDE.md`, `CONTRIBUTING.md`, nos cabeçalhos dos scripts, em `make help` e nas seções
Referências dos ADRs.

## Decisão
A raiz diz como trabalhar no repositório e `docs/` fala do produto e das decisões. Os quatro
arquivos saem: ambiente, verificações, checks obrigatórios e como adicionar um check vão para
`CONTRIBUTING.md`; a configuração do GitHub e as referências de harness engineering vão para
`README.md`; a tabela "onde colocar o quê" vai para `CLAUDE.md`. A tabela de padrões e a lista
de fontes não são movidas: os ADRs e o índice em `docs/adr/README.md` já as respondem.
`docs/` fica com `README.md` (convenções), `adr/` e o que a skill `docs-init` criar.

## Alternativas consideradas
- **Manter os quatro arquivos e renomeá-los** (por exemplo `docs/harness/`): evita a colisão de nomes, mas mantém a duplicação com `CONTRIBUTING.md` e os cabeçalhos dos scripts.
- **Mover tudo para um único `docs/HARNESS.md`**: um arquivo a menos, mas ainda um documento sobre o template dentro da pasta do produto, e sem o reconhecimento que o GitHub dá a `CONTRIBUTING.md`.
- **Raiz para o repositório, `docs/` para o produto (escolhida)**: cada conteúdo tem um dono só e o projeto gerado não herda documentos sobre o template.

## Consequências
### Positivas
- Um `ls` na raiz mostra como trabalhar; `docs/` mostra o produto. Nada sobre o template vaza para o projeto gerado além de `CLAUDE.md`, `CONTRIBUTING.md` e os ADRs.
- `CONTRIBUTING.md` concentra ambiente, checks, fluxo, commits e release em um arquivo que o GitHub exibe ao abrir issues e PRs.
- Menos cópias da mesma regra para manter em sincronia.

### Negativas e trade-offs
- `CONTRIBUTING.md` cresce para cerca de 110 linhas.
- Os ADRs 0001 e 0002 citam `docs/STANDARDS.md` e `docs/ARCHITECTURE.md` em texto; são aceitos e imutáveis, então a citação fica como histórico.
- A tabela que dizia onde cada padrão vive deixa de existir; quem precisar, consulta o ADR ou faz `grep`.

## Referências
- [ADR 0002](0002-usar-claude-md-como-fonte-e-makefile-como-interface.md): criou os documentos em `docs/`.
- [ADR 0007](0007-adotar-o-sistema-de-documentacao-docs-init-em-docs.md): fez de `docs/` a casa do produto.
