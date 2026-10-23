# Architecture Decision Records

Cada decisão de arquitetura cara de reverter vira um arquivo aqui. O ADR responde uma pergunta para quem chegar daqui a seis meses: **por que está assim, e o que mais foi tentado?**

Formato: [MADR](https://adr.github.io/madr/) minimal. Ponto de partida: o `assets/template.md` da skill `adr-writer`, que não é copiado para cá.

## O que tem nesta pasta

| Arquivo | O que é |
|---|---|
| `NNNN-*.md` | Os registros. Um arquivo por decisão. |
| `index.md` | Índice em ordem numérica. **Gerado**, nunca editado à mão. |
| `README.md` | Este arquivo. |

## Quando escrever

Escreva quando a decisão for **cara de reverter** ou quando **alguém vai questioná-la em seis meses**: a escolha de uma ferramenta ou de uma parte da stack, o formato de um contrato entre componentes, estratégia de auth/persistência/erro, ou a escolha deliberada da opção não óbvia.

O acervo é só de **arquitetura e tecnologia do repositório**: stack, ferramentas, infraestrutura, integração, formato de contratos técnicos. Regra de negócio (o que o sistema faz, para quem, sob que condição) não vira ADR; ela vai para o PRD (`docs/product/prd.md`). Misturar as duas faz o acervo responder perguntas que não são dele e esconde as decisões técnicas no meio das de produto.

Não escreva para decisão trivialmente reversível, para "como fazer X" (isso é `CLAUDE.md`/README), nem para escolha que não teve alternativa real — sem deliberação, não há o que registrar. Acervo inflado deixa de ser lido, o que custa mais caro que uma entrada faltando.

## Nome e numeração

`NNNN-titulo-com-hifens.md` — quatro dígitos, sequencial, **nunca reutilizado**, mesmo que um ADR seja apagado. Buraco na numeração não faz mal; número repetido quebra todas as referências.

O título é a decisão em voz ativa, não o tema. Quem roda `ls` tem que ler decisões:

- `0007-usar-zod-para-validar-env.md` ✓
- `0007-validacao-de-env.md` ✗

## Front-matter

```yaml
---
status: accepted
date: 2026-09-05
title: "Usar Zod para validar env"
description: "Por que a validação de env passou a usar Zod em vez de checagem manual."
supersedes: "0003"
superseded-by:
---
```

- `status` — um dos cinco abaixo, minúsculo.
- `date` — ISO, data em que o ADR chegou ao status **atual**. Atualiza a cada mudança de status.
- `title` — só o título, sem o prefixo numérico (esse já está no nome do arquivo e no `# NNNN.` do corpo).
- `description` — uma frase, "por que X em vez de Y". É o que aparece quando alguém — pessoa ou agente — está escaneando a lista de ADRs sem abrir cada arquivo; sem ela, a única forma de saber do que se trata é abrir o arquivo inteiro.
- `supersedes` / `superseded-by` — número do outro ADR como string de 4 dígitos, vazio quando não se aplica. As duas chaves ficam sempre no arquivo, mesmo vazias.

As chaves e os valores de `status` ficam em inglês; o texto, em português.

## Ciclo de status

| Status | Significado | Vai para |
|---|---|---|
| `proposed` | Escrito, em discussão. Único estado livremente editável. | `accepted`, `rejected` |
| `accepted` | Vale hoje. Texto congelado. | `superseded`, `deprecated` |
| `rejected` | Discutido e recusado. Fica no repo — o valor é o motivo registrado. | — |
| `superseded` | Trocado por uma decisão mais nova. Exige `superseded-by`. | — |
| `deprecated` | Não vale mais e nada substituiu (o problema deixou de existir). | — |

Qualquer outra transição é erro. Um ADR `rejected` que volta à mesa é uma decisão **nova**, que o supersede — não uma edição.

## Imutabilidade

ADR `accepted` tem o texto congelado: dali em diante só o front-matter muda. Conteúdo errado ou desatualizado → abre-se um ADR novo que o supersede.

É isso que torna o acervo confiável: o ADR registra o que foi decidido **e o que se sabia naquele momento**. Editar retroativamente deixa o histórico do git como única testemunha do raciocínio original, e ninguém lê `git log` para entender uma decisão. Corrigir typo ou link quebrado, tudo bem; mudar o raciocínio ou o resultado, não.

## Supersede é bidirecional

Sempre os dois lados:

- ADR novo: `supersedes: "0003"`, e o **Contexto** começa dizendo o que mudou desde o 0003.
- ADR antigo: `status: superseded`, `superseded-by: "0011"`, `date` atualizada.

Cadeia de um lado só é beco sem saída: alguém cai no 0003, acredita, e nunca encontra o 0011.

## Referências

Seção **opcional**, no fim do arquivo. Existe quando a decisão se apoia em fato externo — versão de framework, issue aberta, estado de manutenção de uma biblioteca, benchmark. Nesse caso ela é obrigatória na prática: sem a fonte, o leitor não tem como checar se a premissa ainda vale, e uma premissa vencida é o jeito mais comum de um ADR virar mentira sem ninguém notar.

```markdown
## Referências

Consultado em 2026-09-05.

- [MADR — Markdown Any Decision Records](https://adr.github.io/madr/) — formato e conjunto mínimo de seções adotados aqui.
```

Duas regras:

- **Data de consulta obrigatória** (`Consultado em AAAA-MM-DD`). Fato externo envelhece: "issue aberta" e "sem release há dois anos" eram verdade na data, não para sempre.
- **Cada bullet diz o que a fonte sustenta** naquela decisão — não é bibliografia, é rastreabilidade. Link solto obriga o leitor a abrir a página para descobrir por que ela está ali.

Decisão sem fato externo (uma convenção interna, um trade-off só do próprio código) não tem o que citar: apague a seção em vez de encher de link genérico.

## Tamanho

| Seção | Limite |
|---|---|
| Contexto e problema | até 5 frases |
| Opções consideradas | 2 a 4 opções, uma linha cada |
| Decisão | 1 a 3 frases |
| Consequências | 2 a 5 bullets, uma linha cada |
| Referências | sem limite, mas só o que foi de fato usado |

Estourar o limite quase sempre significa que há duas decisões embaralhadas no mesmo arquivo. Separe.

Consequência tem que ser **verificável** — algo que alguém possa descobrir depois que é falso. "Código mais manutenível" é desejo, não consequência.

## Manutenção

```bash
# audita: nomes, front-matter, numeração, cadeias de supersede, índice
python3 .claude/skills/adr-writer/scripts/audit.py docs/architecture/adr

# regenera o index.md a partir do front-matter (rode a cada ADR novo ou mudança de status)
python3 .claude/skills/adr-writer/scripts/audit.py docs/architecture/adr --index
```
