---
name: adr-writer
description: Escreve e mantém Architecture Decision Records (ADRs) em formato MADR-minimal na pasta `docs/architecture/adr/` da raiz — cria a pasta do zero, redige registros novos, move um registro pelo ciclo proposed/accepted/rejected/superseded/deprecated, e audita o acervo em busca de numeração quebrada, cadeia de supersede sem saída ou front-matter fora do formato. Cobre só decisões de arquitetura e tecnologia; regra de negócio vai para o PRD. Use esta skill sempre que o usuário pedir para registrar, escrever ou atualizar uma decisão de arquitetura ("cria um ADR pra escolha do Zod", "registra essa decisão", "documenta por que a gente escolheu X"), pedir para revisar ou consertar registros existentes ("os ADRs estão consistentes?", "audita a pasta docs/architecture/adr"), pedir para aceitar/rejeitar/supersedir/depreciar um deles, ou montar a pasta de ADRs pela primeira vez. Consulte também quando uma decisão de arquitetura cara de reverter estiver sendo tomada na conversa sem registro nenhum — a skill cobre como oferecer o ADR em uma linha sem atrapalhar o trabalho em andamento.
---

# ADR Writer

Um ADR responde uma pergunta para quem chegar daqui a seis meses: **por que está assim, e o que mais foi tentado?**

Tudo abaixo serve a isso. Registro que só diz o que foi escolhido é meio inútil — o leitor repropõe as opções descartadas, porque nada contou a ele que elas já foram pesadas e recusadas.

## Modos

| Situação | Modo |
|---|---|
| Registrar uma decisão; escrever um ADR | **Novo ADR** |
| `docs/architecture/adr/` não existe ou está vazia | **Bootstrap**, depois Novo ADR |
| Aceitar / rejeitar / supersedir / depreciar um registro existente | **Mudança de status** |
| "Os ADRs estão consistentes?"; ou você vai somar a um acervo que ainda não inspecionou | **Auditoria** |
| Uma decisão está sendo tomada de passagem, sem registro | **Oferta** |

Os modos se compõem. Bootstrap → Novo ADR é a primeira execução normal. Rodar a auditoria antes de somar a um acervo que você não viu é barato e pega um número duplicado antes de você criar um.

## Passo 0 — resolver o diretório (todos os modos)

O acervo deste repositório é **`docs/architecture/adr/` na raiz**. Um registro arquivado em outro lugar é pior que registro nenhum: parte o acervo em dois e metade dele deixa de ser encontrada.

1. Caminho dado explicitamente pelo usuário → use esse, e diga que está fora do padrão.
2. Senão → `docs/architecture/adr/` a partir da raiz do repositório (`git rev-parse --show-toplevel`).
3. A pasta não existe, ou existe sem nenhum ADR → **Bootstrap** antes de qualquer outra coisa.

Não há sub-pasta por status ou por ano: o diretório plano **é** o acervo, e o `index.md` gerado lista tudo em ordem numérica. Pasta por status obrigaria a mover o arquivo a cada transição, quebrando link e histórico à toa.

---

## As regras

### Nome e numeração

`NNNN-titulo-com-hifens.md` — quatro dígitos, sequencial, **nunca reutilizado**, mesmo que um ADR seja apagado. Buraco na numeração não faz mal; número repetido destrói toda referência cruzada. Próximo número = maior existente + 1.

O título é a decisão em voz ativa, não o tema. Quem roda `ls` tem que ler decisões, não títulos de capítulo:

- `0007-usar-zod-para-validar-env.md` ✓
- `0007-validacao-de-env.md` ✗ (isso é um assunto, e não diz o que foi decidido)

### Front-matter

```yaml
---
status: proposed
date: 2026-09-05
title: "Título da decisão"
description: "Por que X em vez de Y, em uma frase."
supersedes:
superseded-by:
---
```

- `status` — um dos cinco abaixo, minúsculo.
- `date` — ISO, data em que o registro chegou ao status **atual**. Atualiza a cada mudança de status.
- `title` — só a decisão, sem prefixo numérico (o número já está no nome do arquivo e no `# NNNN.` do corpo).
- `description` — uma frase, "por que X em vez de Y". É o que uma pessoa — ou um agente — lê ao escanear o acervo sem abrir cada arquivo; sem ela, escanear vira abrir tudo.
- `supersedes` / `superseded-by` — número do outro ADR como string de 4 dígitos (`"0003"`), vazio quando não se aplica. As duas chaves ficam sempre no arquivo, mesmo vazias, para a cadeia continuar greppável.

As chaves e os valores de `status` ficam em inglês; o conteúdo, em português. É a mesma divisão do `CLAUDE.md`: formato é código, texto é comunicação.

### Ciclo de status

| Status | Significado | Vai para |
|---|---|---|
| `proposed` | Escrito, em discussão. Único estado livremente editável. | `accepted`, `rejected` |
| `accepted` | Vale hoje. Texto congelado. | `superseded`, `deprecated` |
| `rejected` | Discutido e recusado. Fica no repo — o valor é o motivo registrado. | — |
| `superseded` | Trocado por uma decisão mais nova. Exige `superseded-by`. | — |
| `deprecated` | Não vale mais e nada substituiu (o problema deixou de existir). | — |

Qualquer outra transição é erro. Sinalize e pergunte em vez de executar — um ADR `rejected` que volta à mesa é uma decisão **nova**, que o supersede, não uma edição.

### Imutabilidade do `accepted`

Depois de aceito, só o front-matter muda. Conteúdo errado ou desatualizado → escreva um ADR novo que o supersede.

O motivo é o que torna o acervo confiável: o ADR registra o que foi decidido **e o que se sabia naquele momento**. Editar retroativamente deixa o histórico do git como única testemunha do raciocínio original, e ninguém lê `git log` para entender uma decisão. Corrigir typo ou link quebrado, tudo bem; mudar o raciocínio ou o resultado, não.

### Supersede é bidirecional

Sempre os dois lados:

- ADR novo: `supersedes: "0003"`, e o **Contexto** abre dizendo o que mudou desde o 0003.
- ADR antigo: `status: superseded`, `superseded-by: "0011"`, `date` atualizada.

Cadeia de um lado só é beco sem saída: alguém cai no 0003, acredita, e nunca encontra o 0011.

### Quando uma decisão merece um ADR

Escreva quando a decisão for **cara de reverter** ou quando **alguém vai questioná-la em seis meses**: a escolha de uma ferramenta ou de uma parte da stack, o formato de um contrato entre componentes, estratégia de auth/persistência/erro, ou a escolha deliberada da opção não óbvia.

O acervo é só de **arquitetura e tecnologia do repositório**: stack, ferramentas, infraestrutura, integração, formato de contratos técnicos. Regra de negócio (o que o sistema faz, para quem, sob que condição) não vira ADR; ela vai para o PRD (`docs/product/prd.md`, skill `/prd-writer`); se o pedido de ADR é na verdade uma regra de produto, diga isso em uma linha e ofereça o PRD. Misturar as duas faz o acervo responder perguntas que não são dele e esconde as decisões técnicas no meio das de produto.

Não escreva para decisão trivialmente reversível, para "como fazer X" (isso é `CLAUDE.md` ou README), nem para escolha que não teve alternativa real — sem deliberação, não há o que registrar. Na dúvida, pergunte. Acervo inflado deixa de ser lido, o que custa mais caro que uma entrada faltando.

---

## Modo: Novo ADR

1. **Grep o acervo pelo tema primeiro.** Se já está coberto, isto é um **supersede**, não um registro novo e independente — trabalho diferente, contabilidade diferente.
2. **Pegue as alternativas reais.** Se o usuário nomeou só o vencedor, pergunte o que mais estava na mesa. Nunca invente opções plausíveis: deliberação fabricada é pior que um registro honesto de opção única, porque engana exatamente o leitor futuro para quem o ADR existe. Se de fato não havia alternativa, diga isso em uma linha e reconsidere se isto é um ADR.
3. **Colete as fontes.** Toda afirmação sobre o mundo externo — versão de framework, issue aberta, "sem manutenção há dois anos", benchmark — precisa de link em `## Referências`, com a data de consulta. Pesquise nesta ordem: `docs/` do projeto, context7, doc oficial, web; as fontes do ADR são as dessa pesquisa, citadas enquanto você escreve e não de memória depois. Nada externo em jogo → apague a seção.
4. **Escreva a partir do template da skill.** Leia `assets/template.md` e crie o registro direto em `docs/architecture/adr/NNNN-titulo.md`, preenchido. Não copie o template para `docs/architecture/adr/`: a cópia viraria uma segunda fonte de verdade que descola da skill, e é do `assets/template.md` que a auditoria deriva seções e chaves obrigatórias.
5. **Status inicial:** `proposed` quando o time ainda tem que concordar; `accepted` quando a decisão já foi tomada e está valendo. Escrever o ADR depois do fato é normal — não encene uma fase `proposed` falsa para uma decisão que já entrou.
6. **Regenere o índice:** `python3 <skill-dir>/scripts/audit.py docs/architecture/adr --index`.
7. Reporte caminho e número de volta.

## Estilo de escrita — o ponto de verdade

Um ADR é lido uma vez, rápido, por alguém sob pressão. Tamanho não é rigor; é o principal motivo de acervo de ADR ser abandonado.

| Seção | Orçamento |
|---|---|
| Contexto e problema | até 5 frases |
| Opções consideradas | 2 a 4 opções, uma linha cada |
| Decisão | 1 a 3 frases |
| Consequências | 2 a 5 bullets, uma linha cada |
| Referências (opcional) | só o que foi de fato usado |

Estourar o orçamento quase sempre significa duas decisões embaralhadas no mesmo registro. Separe.

Dois hábitos fazem quase todo o trabalho:

**Corte o pigarro.** Nada de "é importante notar", "vale ressaltar", nada de repetir o título da seção como primeira frase, nada de parágrafo explicando o que é um ADR. Comece no primeiro fato que importa.

**Consequência tem que ser falsificável.** Consequência que alguém pode descobrir depois que é *falsa* é informação. Desejo não é.

> ✗ Bom: código mais manutenível e escalável.
> ✗ Ruim: adiciona uma dependência.
>
> ✓ Bom: env inválida derruba o boot, então erro de configuração aparece no deploy e não em produção às 3h.
> ✓ Ruim: cada variável nova tem que ser declarada em dois lugares (schema + `.env.example`); esquecer um passa no build.

Mesma régua para as opções: uma linha dizendo o que a opção **é** e por que perdeu — não um parágrafo, não uma lista de features.

**Cite toda fonte externa, com data.** `## Referências` é opcional como seção, mas obrigatória no instante em que o raciocínio se apoia em algo fora do repositório:

> ✗ "A biblioteca X está sem manutenção."
> ✓ "A biblioteca X está sem release há mais de dois anos" + link, sob `Consultado em 2026-09-05.`

A data é o ponto. "Issue continua aberta" e "sem manutenção" eram verdade **naquele dia** — sem a data, o leitor daqui a um ano não tem como saber se a premissa ainda vale, e premissa vencida é o jeito mais comum de um ADR aceito virar mentira em silêncio. Cada bullet também diz o que aquela fonte sustenta **nesta** decisão; link solto obriga o leitor a abrir a página para descobrir por que ele está ali.

Nunca cite fonte que você não leu, e nunca vista uma lembrança de citação — link errado é pior que link nenhum, porque parece conferido.

## Modo: Mudança de status

1. Leia o ADR e confirme que a transição é permitida pela tabela acima.
2. Troque `status`, atualize `date`.
3. Supersedir também significa: criar o ADR novo (modo Novo ADR), pôr `supersedes` nele, pôr `superseded-by` no antigo. Os dois, na mesma mudança.
4. Se o pedido é "consertar" um ADR `accepted`, diga qual é a regra e ofereça o caminho do supersede — curto, uma vez, e depois faça o que o usuário decidir.
5. Regenere o índice (`--index`): status e data aparecem lá.

## Modo: Auditoria

Rode o script; ele checa tudo que é mecânico, de forma determinística:

```bash
python3 <skill-dir>/scripts/audit.py docs/architecture/adr
```

Ele reporta nome de arquivo fora do padrão, front-matter ausente/inválido, status desconhecido, número duplicado, divergência entre o número do arquivo e o do `# NNNN.`, seção obrigatória faltando, cadeia de supersede de um lado só, `index.md` desatualizado e — quando `## Referências` existe — bullet sem URL (erro) ou sem `Consultado em AAAA-MM-DD` (aviso). Sai com código 1 quando há erro.

As seções e chaves obrigatórias saem de `assets/template.md` desta skill, não de uma cópia no acervo: mudar o formato é mudar um arquivo só. Sem o template, o script cai no conjunto padrão.

Seções em `OPTIONAL_SECTIONS` (hoje `## Referências`) só são checadas quando presentes, então acrescentar uma seção ao template não quebra retroativamente todo registro existente.

Depois leia o que o script não alcança: registros que descolaram da realidade (um ADR `accepted` descrevendo algo que o código não faz mais) e registros acima do orçamento de tamanho. Reporte agrupado em **erros** (quebram as regras) e **suspeitas** (precisam de decisão humana). Corrija os erros sob pedido; nunca reescreva o corpo de um `accepted` para "consertar" o descolamento — isso é supersede.

## Modo: Bootstrap

Quando `docs/architecture/adr/` não existe, crie exatamente estes arquivos e nada além:

- `README.md` — cópia de `assets/README.md`, as regras em forma legível.
- `0001-usar-adrs-para-decisoes-de-arquitetura.md` — cópia de `assets/0001-usar-adrs-para-decisoes-de-arquitetura.md`, já `accepted`, servindo também de exemplo preenchido. Troque `AAAA-MM-DD` pela data de hoje.
- `index.md` — **gerado**, nunca escrito à mão: `python3 <skill-dir>/scripts/audit.py docs/architecture/adr --index`.

Nada de scaffolding extra (sem pasta por status, sem `CHANGELOG`, sem `index` manual). Cada arquivo a mais é mais uma coisa para manter em sincronia, e o acervo já tem a fonte de verdade de que precisa: o front-matter dos registros. O template **não** é copiado: ele fica em `assets/template.md` e é lido de lá a cada ADR novo.

Ajuste os caminhos do README se o acervo, por algum motivo, não ficar em `docs/architecture/adr/`.

## Modo: Oferta

Quando uma decisão cara de reverter está sendo tomada na conversa e não existe registro, ofereça uma vez, em uma linha, numa pausa natural — depois que o trabalho entrega, não no meio dele:

> "Isso bate nos critérios de ADR (caro de reverter). Quer que eu registre em `docs/architecture/adr`?"

Se a resposta for não, deixe pra lá e não levante de novo para aquela decisão. Interromper a entrega para fazer campanha por documentação é como documentação vira motivo de rejeição.

## Idioma

ADRs são escritos em **português**, seguindo o `CLAUDE.md` deste repositório. Os títulos de seção seguem `assets/template.md`. As chaves de front-matter e os valores de `status` ficam em **inglês**, para o formato continuar compatível com ferramenta e para casar com a regra do `CLAUDE.md` de que código é em inglês.
