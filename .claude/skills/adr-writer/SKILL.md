---
name: adr-writer
description: Escreve e mantém Architecture Decision Records (ADRs) em formato MADR-minimal na pasta `docs/ADR/` da raiz — cria a pasta do zero, redige registros novos, move um registro pelo ciclo proposed/accepted/rejected/superseded/deprecated, e audita o acervo em busca de numeração quebrada, cadeia de supersede sem saída, camada inválida ou front-matter fora do formato. Use esta skill sempre que o usuário pedir para registrar, escrever ou atualizar uma decisão de arquitetura ("cria um ADR pra escolha do Zod", "registra essa decisão", "documenta por que a gente escolheu X"), pedir para revisar ou consertar registros existentes ("os ADRs estão consistentes?", "audita a pasta docs/ADR"), pedir para aceitar/rejeitar/supersedir/depreciar um deles, ou montar a pasta de ADRs pela primeira vez. Consulte também quando uma decisão de arquitetura cara de reverter estiver sendo tomada na conversa sem registro nenhum — a skill cobre como oferecer o ADR em uma linha sem atrapalhar o trabalho em andamento.
---

# ADR Writer

Um ADR responde uma pergunta para quem chegar daqui a seis meses: **por que está assim, e o que mais foi tentado?**

Tudo abaixo serve a isso. Registro que só diz o que foi escolhido é meio inútil — o leitor repropõe as opções descartadas, porque nada contou a ele que elas já foram pesadas e recusadas.

## Modos

| Situação | Modo |
|---|---|
| Registrar uma decisão; escrever um ADR | **Novo ADR** |
| `docs/ADR/` não existe ou está vazia | **Bootstrap**, depois Novo ADR |
| Aceitar / rejeitar / supersedir / depreciar um registro existente | **Mudança de status** |
| "Os ADRs estão consistentes?"; ou você vai somar a um acervo que ainda não inspecionou | **Auditoria** |
| Uma decisão está sendo tomada de passagem, sem registro | **Oferta** |

Os modos se compõem. Bootstrap → Novo ADR é a primeira execução normal. Rodar a auditoria antes de somar a um acervo que você não viu é barato e pega um número duplicado antes de você criar um.

## Passo 0 — resolver o diretório (todos os modos)

O acervo deste repositório é **`docs/ADR/` na raiz**. Um registro arquivado em outro lugar é pior que registro nenhum: parte o acervo em dois e metade dele deixa de ser encontrada.

1. Caminho dado explicitamente pelo usuário → use esse, e diga que está fora do padrão.
2. Senão → `docs/ADR/` a partir da raiz do repositório (`git rev-parse --show-toplevel`).
3. A pasta não existe, ou existe sem nenhum ADR → **Bootstrap** antes de qualquer outra coisa.

Não há sub-pasta por camada, por status ou por ano: o diretório plano **é** o acervo, e o recorte por camada sai do `index.md` gerado. Pasta por status obrigaria a mover o arquivo a cada transição, quebrando link e histórico à toa.

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
layer: stack
title: "Título da decisão"
description: "Por que X em vez de Y, em uma frase."
supersedes:
superseded-by:
---
```

- `status` — um dos cinco abaixo, minúsculo.
- `date` — ISO, data em que o registro chegou ao status **atual**. Atualiza a cada mudança de status.
- `layer` — a camada da stack a que a decisão pertence (ver abaixo).
- `title` — só a decisão, sem prefixo numérico (o número já está no nome do arquivo e no `# NNNN.` do corpo).
- `description` — uma frase, "por que X em vez de Y". É o que uma pessoa — ou um agente — lê ao escanear o acervo sem abrir cada arquivo; sem ela, escanear vira abrir tudo.
- `supersedes` / `superseded-by` — número do outro ADR como string de 4 dígitos (`"0003"`), vazio quando não se aplica. As duas chaves ficam sempre no arquivo, mesmo vazias, para a cadeia continuar greppável.

As chaves e os valores de `status` ficam em inglês; o conteúdo, em português. É a mesma divisão do `CLAUDE.md`: formato é código, texto é comunicação.

### Camada (`layer`)

O DevFlow-AI é pensado como stack: camadas compostas, cada uma com responsabilidade definida, escolhidas e trocáveis de forma explícita. Um ADR quase sempre registra a escolha *de uma camada* — então ele diz de qual camada está falando. Sem isso, o acervo vira uma lista linear e o leitor não consegue perguntar "o que já foi decidido sobre a camada X?", que é a pergunta que ele realmente tem.

`layer` recebe um slug do registro `docs/ADR/layers.md`, mais um valor reservado:

- **`stack`** — a decisão é sobre a composição da stack em si: quais camadas existem, onde ficam as fronteiras, como elas se conectam. Não sobre o interior de uma delas.

Quais camadas existem **ainda é decisão em aberto** neste repositório (ver `CLAUDE.md`). Por isso o vocabulário não está nem no código nem nesta skill: mora em `docs/ADR/layers.md`, uma tabela que cresce por ADR. Um `layer` fora do registro é erro de auditoria — ou o slug está errado, ou falta um ADR `stack` criando essa camada. As duas coisas se descobrem juntas, que é justamente o ponto.

A camada **não** entra no nome do arquivo. Fronteira entre camadas se move, e renomear o arquivo quebraria toda referência por número. Nome do arquivo é identidade; camada é atributo. O índice por camada é derivado do front-matter (`audit.py --index`), então acompanha sozinho.

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

Escreva quando a decisão for **cara de reverter** ou quando **alguém vai questioná-la em seis meses**: a escolha de uma camada da stack ou da ferramenta que a implementa, o formato de um contrato entre camadas, estratégia de auth/persistência/erro, ou a escolha deliberada da opção não óbvia.

Não escreva para decisão trivialmente reversível, para "como fazer X" (isso é `CLAUDE.md` ou README), nem para escolha que não teve alternativa real — sem deliberação, não há o que registrar. Na dúvida, pergunte. Acervo inflado deixa de ser lido, o que custa mais caro que uma entrada faltando.

---

## Modo: Novo ADR

1. **Grep o acervo pelo tema primeiro.** Se já está coberto, isto é um **supersede**, não um registro novo e independente — trabalho diferente, contabilidade diferente.
2. **Pegue as alternativas reais.** Se o usuário nomeou só o vencedor, pergunte o que mais estava na mesa. Nunca invente opções plausíveis: deliberação fabricada é pior que um registro honesto de opção única, porque engana exatamente o leitor futuro para quem o ADR existe. Se de fato não havia alternativa, diga isso em uma linha e reconsidere se isto é um ADR.
3. **Determine a camada.** Leia `docs/ADR/layers.md` e escolha o slug. Se a decisão é sobre quais camadas existem ou onde ficam as fronteiras, é `layer: stack` — e esse ADR provavelmente adiciona linhas em `layers.md` no mesmo commit: a tabela é consequência da decisão, não um arquivo separado que alguém lembra de atualizar depois. Se a camada que você precisa não está no registro, pare: ou o slug está errado, ou falta uma decisão `stack` antes desta. Pergunte em vez de inventar slug.
4. **Colete as fontes.** Toda afirmação sobre o mundo externo — versão de framework, issue aberta, "sem manutenção há dois anos", benchmark — precisa de link em `## Referências`, com a data de consulta. O `CLAUDE.md` já define a ordem de pesquisa (docs/ → context7 → doc oficial → web); as fontes do ADR são as dessa pesquisa, citadas enquanto você escreve e não de memória depois. Nada externo em jogo → apague a seção.
5. **Copie o template** para o diretório e preencha: `docs/ADR/template.md` quando existir, `assets/template.md` como fallback. O template do acervo ganha sempre que divergir — é ele que a auditoria usa para derivar seções e chaves obrigatórias.
6. **Status inicial:** `proposed` quando o time ainda tem que concordar; `accepted` quando a decisão já foi tomada e está valendo. Escrever o ADR depois do fato é normal — não encene uma fase `proposed` falsa para uma decisão que já entrou.
7. **Regenere o índice:** `python3 <skill-dir>/scripts/audit.py docs/ADR --index`.
8. Reporte caminho, número e camada de volta.

## Estilo de escrita — o ponto de verdade

Um ADR é lido uma vez, rápido, por alguém sob pressão. Tamanho não é rigor; é o principal motivo de acervo de ADR ser abandonado.

| Seção | Orçamento |
|---|---|
| Contexto e problema | até 5 frases |
| Opções consideradas | 2 a 4 opções, uma linha cada |
| Decisão | 1 a 3 frases |
| Consequências | 2 a 5 bullets, uma linha cada |
| Referências (opcional) | só o que foi de fato usado |

Estourar o orçamento quase sempre significa duas decisões embaralhadas no mesmo registro. Separe — e, num acervo por camada, decisões embaralhadas costumam ser decisões de camadas diferentes.

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
python3 <skill-dir>/scripts/audit.py docs/ADR
```

Ele reporta nome de arquivo fora do padrão, front-matter ausente/inválido, status desconhecido, `layer` fora do registro de camadas, número duplicado, divergência entre o número do arquivo e o do `# NNNN.`, seção obrigatória faltando, cadeia de supersede de um lado só, `index.md` desatualizado e — quando `## Referências` existe — bullet sem URL (erro) ou sem `Consultado em AAAA-MM-DD` (aviso). Sai com código 1 quando há erro.

Duas coisas ele deriva do próprio acervo em vez de fixar no código:

- **Seções e chaves obrigatórias** saem de `docs/ADR/template.md` — assim o acervo pode ganhar uma chave que esta skill não conhece sem quebrar a auditoria. Sem template localizável, cai no conjunto padrão.
- **Camadas válidas** saem da primeira coluna da tabela de `docs/ADR/layers.md`, mais o reservado `stack`. Sem `layers.md`, ele avisa uma vez e não valida `layer` — é aviso, não erro, porque num repo onde as camadas ainda não foram decididas o registro vazio é o estado correto.

Seções em `OPTIONAL_SECTIONS` (hoje `## Referências`) só são checadas quando presentes, então acrescentar uma seção ao template não quebra retroativamente todo registro existente.

Depois leia o que o script não alcança: registros que descolaram da realidade (um ADR `accepted` descrevendo algo que o código não faz mais) e registros acima do orçamento de tamanho. Reporte agrupado em **erros** (quebram as regras) e **suspeitas** (precisam de decisão humana). Corrija os erros sob pedido; nunca reescreva o corpo de um `accepted` para "consertar" o descolamento — isso é supersede.

## Modo: Bootstrap

Quando `docs/ADR/` não existe, crie exatamente estes arquivos e nada além:

- `README.md` — cópia de `assets/README.md`, as regras em forma legível.
- `template.md` — cópia de `assets/template.md`.
- `layers.md` — cópia de `assets/layers.md`: o registro de camadas, com a tabela vazia. Ele cresce por ADR, não por edição avulsa.
- `0001-usar-adrs-para-decisoes-de-arquitetura.md` — cópia de `assets/0001-usar-adrs-para-decisoes-de-arquitetura.md`, já `accepted` e `layer: stack`, servindo também de exemplo preenchido. Troque `AAAA-MM-DD` pela data de hoje.
- `index.md` — **gerado**, nunca escrito à mão: `python3 <skill-dir>/scripts/audit.py docs/ADR --index`.

Nada de scaffolding extra (sem pasta por status, sem `CHANGELOG`, sem `index` manual). Cada arquivo a mais é mais uma coisa para manter em sincronia, e o acervo já tem as duas fontes de verdade de que precisa: o front-matter dos registros e o `layers.md`.

Ajuste os caminhos do README se o acervo, por algum motivo, não ficar em `docs/ADR/`.

## Modo: Oferta

Quando uma decisão cara de reverter está sendo tomada na conversa e não existe registro, ofereça uma vez, em uma linha, numa pausa natural — depois que o trabalho entrega, não no meio dele:

> "Isso bate nos critérios de ADR (caro de reverter). Quer que eu registre em `docs/ADR`?"

Se a resposta for não, deixe pra lá e não levante de novo para aquela decisão. Interromper a entrega para fazer campanha por documentação é como documentação vira motivo de rejeição.

## Idioma

ADRs são escritos em **português**, seguindo o `CLAUDE.md` deste repositório. Os títulos de seção seguem `assets/template.md`. As chaves de front-matter, os valores de `status` e os slugs de `layer` ficam em **inglês**, para o formato continuar compatível com ferramenta e para casar com a regra do `CLAUDE.md` de que código é em inglês.
