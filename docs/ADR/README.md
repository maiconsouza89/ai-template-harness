# Architecture Decision Records

Cada decisão de arquitetura cara de reverter vira um arquivo aqui. O ADR responde uma pergunta para quem chegar daqui a seis meses: **por que está assim, e o que mais foi tentado?**

Formato: [MADR](https://adr.github.io/madr/) minimal. Ponto de partida: `template.md`.

## O que tem nesta pasta

| Arquivo | O que é |
|---|---|
| `NNNN-*.md` | Os registros. Um arquivo por decisão. |
| `template.md` | Ponto de partida para um registro novo. É dele que a auditoria deriva as seções e chaves obrigatórias. |
| `layers.md` | Registro das camadas da stack — o vocabulário válido do campo `layer`. |
| `index.md` | Índice por camada. **Gerado**, nunca editado à mão. |
| `README.md` | Este arquivo. |

## Quando escrever

Escreva quando a decisão for **cara de reverter** ou quando **alguém vai questioná-la em seis meses**: a escolha de uma camada da stack ou da ferramenta que a implementa, o formato de um contrato entre camadas, estratégia de auth/persistência/erro, ou a escolha deliberada da opção não óbvia.

Não escreva para decisão trivialmente reversível, para "como fazer X" (isso é `CLAUDE.md`/README), nem para escolha que não teve alternativa real — sem deliberação, não há o que registrar. Acervo inflado deixa de ser lido, o que custa mais caro que uma entrada faltando.

## Nome e numeração

`NNNN-titulo-com-hifens.md` — quatro dígitos, sequencial, **nunca reutilizado**, mesmo que um ADR seja apagado. Buraco na numeração não faz mal; número repetido quebra todas as referências.

O título é a decisão em voz ativa, não o tema. Quem roda `ls` tem que ler decisões:

- `0007-usar-zod-para-validar-env.md` ✓
- `0007-validacao-de-env.md` ✗

A camada **não** entra no nome do arquivo: fronteira entre camadas se move, e renomear quebraria toda referência por número. Nome é identidade; camada é atributo, e vive no front-matter.

## Front-matter

```yaml
---
status: accepted
date: 2026-09-05
layer: validation
title: "Usar Zod para validar env"
description: "Por que a validação de env passou a usar Zod em vez de checagem manual."
supersedes: "0003"
superseded-by:
---
```

- `status` — um dos cinco abaixo, minúsculo.
- `date` — ISO, data em que o ADR chegou ao status **atual**. Atualiza a cada mudança de status.
- `layer` — a camada da stack a que a decisão pertence (ver abaixo).
- `title` — só o título, sem o prefixo numérico (esse já está no nome do arquivo e no `# NNNN.` do corpo).
- `description` — uma frase, "por que X em vez de Y". É o que aparece quando alguém — pessoa ou agente — está escaneando a lista de ADRs sem abrir cada arquivo; sem ela, a única forma de saber do que se trata é abrir o arquivo inteiro.
- `supersedes` / `superseded-by` — número do outro ADR como string de 4 dígitos, vazio quando não se aplica. As duas chaves ficam sempre no arquivo, mesmo vazias.

As chaves, os valores de `status` e os slugs de `layer` ficam em inglês; o texto, em português.

## Camada

O projeto é pensado como stack: camadas compostas, cada uma com responsabilidade definida, escolhidas e trocáveis de forma explícita. Um ADR quase sempre registra a escolha *de uma camada*, então ele diz de qual está falando — é o que permite perguntar "o que já foi decidido sobre a camada X?" em vez de ler o acervo inteiro.

Os valores válidos são os slugs da tabela de `layers.md`, mais o reservado **`stack`**, que marca a decisão sobre a composição da stack em si: quais camadas existem, onde ficam as fronteiras, como elas se conectam.

Camada nova entra em `layers.md` **pelo ADR que a criou**, no mesmo commit. Se o `layer` que você precisa não está lá, ou o slug está errado, ou falta uma decisão `stack` antes desta — a auditoria acusa os dois casos do mesmo jeito, e é assim que se descobre a decisão que falta.

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

Estourar o limite quase sempre significa que há duas decisões embaralhadas no mesmo arquivo — e, num acervo por camada, decisões embaralhadas costumam ser decisões de camadas diferentes. Separe.

Consequência tem que ser **verificável** — algo que alguém possa descobrir depois que é falso. "Código mais manutenível" é desejo, não consequência.

## Manutenção

```sh
# audita nomes, front-matter, camadas, numeração e cadeias de supersede; regenera o index.md
make check-adr
```

Para depurar, o script pode ser chamado direto:
`python3 .claude/skills/adr-writer/scripts/audit.py docs/ADR [--index]`.
