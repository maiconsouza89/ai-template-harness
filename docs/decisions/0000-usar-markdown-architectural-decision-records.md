# Usar Markdown Architectural Decision Records

## Contexto e problema

Queremos registrar as decisões de arquitetura e de processo deste repositório para que pessoas e
agentes entendam o porquê de cada escolha. Qual formato usar?

## Opções consideradas

* [MADR](https://adr.github.io/madr/) 4.0, template mínimo
* ADR de Michael Nygard (Título, Status, Contexto, Decisão, Consequências)
* Registrar decisões apenas em documentos narrativos em `docs/`

## Decisão

Opção escolhida: "MADR 4.0, template mínimo", porque é um padrão conhecido por ferramentas e
agentes, obriga a listar as opções consideradas e tem um template mínimo que cabe em uma tela.
A estrutura do MADR é mantida; títulos de seção e frases fixas são escritos em português, como o
restante da documentação.

### Consequências

* Bom, porque cada decisão fica em um arquivo pequeno e versionado em `docs/decisions/`.
* Bom, porque o histórico de alternativas rejeitadas evita rediscutir o mesmo tema.
* Ruim, porque exige disciplina para criar um ADR a cada decisão relevante.
