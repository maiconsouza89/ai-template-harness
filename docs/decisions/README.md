# Registros de decisão (ADR)

Um arquivo por decisão, `NNNN-titulo-com-hifens.md`, numeração sequencial, formato
[MADR 4.0](https://adr.github.io/madr/) mínimo com títulos e frases fixas em português. ADRs não
são editados depois de aceitos: uma decisão nova que substitui outra ganha um arquivo novo, e o
antigo recebe no topo uma nota "Substituído por NNNN" (parcial ou total).

Template:

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
