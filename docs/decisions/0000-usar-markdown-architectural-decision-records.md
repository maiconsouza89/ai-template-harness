# Usar Markdown Architectural Decision Records

## Context and Problem Statement

Queremos registrar as decisões de arquitetura e de processo deste repositório para que pessoas e
agentes entendam o porquê de cada escolha. Qual formato usar?

## Considered Options

* [MADR](https://adr.github.io/madr/) 4.0, template mínimo
* ADR de Michael Nygard (Title, Status, Context, Decision, Consequences)
* Registrar decisões apenas em documentos narrativos em `docs/`

## Decision Outcome

Chosen option: "MADR 4.0, template mínimo", because é um padrão conhecido por ferramentas e
agentes, obriga a listar as opções consideradas e tem um template mínimo que cabe em uma tela.
Títulos de seção ficam em inglês (padrão MADR); o texto, em português.

### Consequences

* Good, because cada decisão fica em um arquivo pequeno e versionado em `docs/decisions/`.
* Good, because o histórico de alternativas rejeitadas evita rediscutir o mesmo tema.
* Bad, because exige disciplina para criar um ADR a cada decisão relevante.
