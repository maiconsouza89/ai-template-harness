---
name: hld-writer
description: Conduz uma entrevista estruturada (em blocos por etapa) e gera o HLD (High-Level Design) do sistema em `docs/HLD.md`, em português, com objetivo técnico, arquitetura geral e diagrama de componentes (Mermaid), componentes e responsabilidades, fluxos de requisição e de dados, modelo de dados em alto nível, interfaces públicas com protocolo e SLA, escalabilidade e disponibilidade com metas, segurança, observabilidade, riscos arquiteturais, rastreabilidade com os RF-NNN do PRD e ADRs associados ou pendentes. É o documento do "como" técnico que fica entre o PRD (`/prd-writer`) e os ADRs (`/adr-writer`); também exporta o HLD em JSON. Use esta skill sempre que o usuário quiser escrever, montar, revisar ou atualizar um HLD, "desenho da solução", "arquitetura do sistema", "design técnico", "visão de arquitetura", "documento de arquitetura", "como o sistema vai ser construído", "quais componentes e como se integram", "topologia", mesmo que não diga a palavra HLD; também quando ele colar um PRD, um brief técnico ou uma lista de tecnologias e pedir para "desenhar a arquitetura", "estruturar a solução" ou "definir os componentes" antes de implementar, ou quando `docs/HLD.md` já existir e ele quiser mudar componente, interface, fluxo ou meta.
---

# HLD Writer

O HLD responde quatro perguntas para quem vai implementar e para quem vai operar: **como a solução se divide em componentes, como eles conversam, onde o dado vive e o que garante que isso escala, resiste, é seguro e é observável**. Tudo nesta skill serve a isso.

Ele fala do **como** técnico. Não reconta a regra de negócio: isso é o PRD em `docs/PRD.md`, e o HLD o cita por `RF-NNN`. Também não é o lugar de justificar cada escolha de tecnologia: isso é ADR em `docs/ADR/`, e o HLD aponta para o número. A divisão de trabalho neste repositório é **PRD diz o quê, HLD diz como, ADR diz por quê**. Quando o usuário trouxer uma tecnologia na entrevista, ela entra no HLD com a coluna "Decisão" preenchida: o ADR que já existe, ou `pendente de ADR` com a decisão listada no fim do documento e no relatório final. Tecnologia sem decisão registrada é a primeira coisa que o leitor de daqui a seis meses vai questionar.

## Modos

| Situação | Modo |
|---|---|
| Pedido de HLD sem material, ou com uma ideia em poucas frases | **Entrevista** |
| Usuário entregou um brief técnico razoavelmente completo (ou há PRD) e pediu para não ser entrevistado, ou está rodando sem interação | **Direto** |
| `docs/HLD.md` já existe e o pedido é mudar algo | **Revisão** |

Em qualquer modo, comece lendo `assets/template.md` (esqueleto obrigatório da saída) e `references/entrevista.md` (perguntas por etapa, opções para oferecer, defaults e checagens). Leia os dois antes da primeira pergunta: a entrevista é guiada pelo que o template vai precisar, não o contrário.

## Passo 0: destino e insumos

O HLD do sistema vive em **`docs/HLD.md`** na raiz do repositório (`git rev-parse --show-toplevel`). Um só arquivo, um só lugar: é o que ADRs, issues e código vão referenciar. Se o arquivo existe, isto é **Revisão**, não um HLD novo. Se o usuário pediu outro caminho (um HLD por módulo, por exemplo), use e diga que está fora do padrão.

Antes de perguntar qualquer coisa, leia o que já existe:

- **`docs/PRD.md`**, se existir. É de onde saem os RFs que a arquitetura precisa atender e os requisitos não funcionais que viram metas (disponibilidade, performance, segurança, compliance). Anote a versão para o cabeçalho. O `Responsável` é quem o usuário indicar; sem indicação, use o nome do `git config user.name` marcado `(hipótese)` ou escreva `a definir`. Se não existir, diga em uma linha que `/prd-writer` gera um, e continue: o HLD pode nascer sem PRD, mas a seção de rastreabilidade vai dizer isso em vez de fingir cobertura.
- **`docs/ADR/index.md`**, se existir. Toda tecnologia ou padrão que já tem ADR entra no HLD com o número; o que não tem vira pendência. Não reabra uma decisão `accepted` na entrevista: cite-a.

## Modo: Entrevista

Onze etapas, uma por seção do template. Em cada uma: faça **um bloco de perguntas** (não uma por vez e não trinta de uma vez), use `AskUserQuestion` quando as respostas são enumeráveis (ambiente de implantação, exposição de interface, probabilidade de risco) e texto livre quando não são, depois **resuma em 3 a 6 linhas** o que entendeu e peça confirmação antes de seguir. O resumo é o que evita descobrir na etapa 10 que a etapa 2 foi mal entendida.

| Etapa | O que precisa sair dela |
|---|---|
| 1. Contexto e objetivo técnico | Objetivo técnico em poucas frases, problemas técnicos do estado atual com número, sistemas conectados e direção do dado |
| 2. Arquitetura geral | Topologia, ambiente de implantação, tecnologias (cada uma com ADR ou pendência), padrões adotados e por quê |
| 3. Componentes | Lista de componentes com nome estável, responsabilidades, dependências, papel nos dados (persiste, cacheia, orquestra) |
| 4. Fluxos | 2 a 5 fluxos ponta a ponta, do gatilho ao efeito observável; fluxo de dados entre componentes; persistência e consistência |
| 5. Modelo de dados | 4 a 10 entidades, relações com regra, fonte de verdade por entidade, cache, versionamento e retenção |
| 6. Interfaces públicas | Cada interface com tipo, protocolo, exposição e SLA ou limite |
| 7. Escalabilidade e disponibilidade | Volume atual e esperado, estratégia de crescimento, técnicas, metas com número (disponibilidade, RTO, RPO, capacidade) |
| 8. Segurança | Autenticação, autorização, proteção de dados e PII, gestão de segredos |
| 9. Observabilidade | Logs, métricas, tracing, dashboards e alertas ligados às metas |
| 10. Riscos arquiteturais | Probabilidade, impacto, mitigações (lista) e contingência |
| 11. ADRs e próximos passos | ADRs que já cobrem o HLD, decisões pendentes com critério, próximos passos até implementar |

Depois da etapa 11 vem a **rastreabilidade**, que você deriva e apresenta para confirmação (ver abaixo). Não pergunte "qual componente atende RF-003?"; proponha "RF-003 é atendido pelo Serviço de agenda e pela API pública, no fluxo Cliente agenda. Confere?". O usuário corrige melhor do que inventa.

Regras da conversa:

- **Quando o usuário não sabe, ofereça 2 ou 3 opções plausíveis** e marque a escolhida como `(hipótese)`. Os defaults de `references/entrevista.md` existem para isso. Nunca preencha em silêncio.
- **Inconsistência para a entrevista.** Meta de disponibilidade que a topologia não entrega (um banco sem réplica e 99.99 por cento), componente que aparece num fluxo e não na lista, interface externa sem autenticação: aponte e peça correção antes de continuar.
- **Não invente detalhes.** Se o usuário não deu, é lacuna ou hipótese, nunca fato.
- **Não reabra decisão aceita.** ADR `accepted` em `docs/ADR/` é cenário dado. Se o usuário quiser mudar, isso é um ADR novo com `supersedes`, via `/adr-writer`, não uma linha do HLD.
- Perguntas simples, uma ideia por pergunta, sem travessão "—" no texto. A regra do travessão vale também para o HLD gerado.

## Modo: Direto

Quando o brief ou o PRD já veio, não encene a entrevista. Mapeie o material sobre as onze etapas, preencha o que está lá, marque `(hipótese)` o que você completou com os defaults e **liste as lacunas no relatório final** em vez de perguntar uma a uma. Se houver uma ou duas perguntas cuja resposta muda o HLD inteiro (cloud ou on-premises por restrição legal, um serviço ou vários, dado sensível ou não), faça só essas, e só se houver alguém para responder.

## Modo: Revisão

1. Leia o `docs/HLD.md` atual inteiro, e o `docs/PRD.md` se existir, antes de perguntar qualquer coisa.
2. Altere só o que o pedido toca. Componente ou interface removida sai da tabela, do diagrama, dos fluxos e da rastreabilidade de uma vez: meia remoção é pior que nenhuma.
3. Refaça a rastreabilidade: quase toda mudança de componente ou interface muda quem atende qual RF.
4. Se a mudança troca uma tecnologia ou padrão com ADR `accepted`, pare e diga que isso pede ADR novo (`/adr-writer`), e só então atualize o HLD apontando para ele.
5. Suba a versão no cabeçalho (`0.1.0` → `0.2.0` para componente, interface ou tecnologia que entra ou sai; `0.1.1` para ajuste de texto ou meta) e a data.
6. Valide e reporte o que mudou.

## Diagrama e rastreabilidade

Dois artefatos fazem o HLD ser lido em vez de arquivado.

**Diagrama de componentes.** Um bloco Mermaid `graph LR` na seção Arquitetura geral, com os componentes da tabela dentro de um `subgraph` do sistema, os sistemas externos fora dele com forma diferente (`{{ }}`), armazenamentos como `[( )]` e uma aresta por dependência. Os nomes dos nós são os mesmos da tabela de componentes, porque o validador cruza os dois e porque o leitor vai procurar o nome do diagrama na tabela. Mermaid porque renderiza no GitHub e ainda é texto greppável para quem não renderiza. Se um fluxo cruzar fronteira assíncrona e for difícil de seguir em lista, um `sequenceDiagram` dentro do fluxo é bem-vindo, mas é opcional.

**Rastreabilidade com o PRD.** Uma tabela que diz, para cada `RF-NNN`, que componentes, interfaces e fluxo o atendem, e uma lista que diz, para cada requisito não funcional do PRD, que seção e meta do HLD o cobre. É o que transforma "a arquitetura parece boa" em "a arquitetura cobre o que foi pedido". RF sem componente é lacuna da arquitetura; componente sem RF é escopo que ninguém pediu, e vai para o relatório final. Sem PRD, a seção abre com uma linha dizendo que não há PRD, e os requisitos tomados do brief entram na mesma tabela numerados como `RB-NN` (requisito do brief), para serem trocados pelos `RF-NNN` quando o PRD existir. Um prefixo só, sempre esse, para que o leitor e o validador saibam que aquilo não veio de um PRD.

## Estilo e orçamento

O HLD é lido por quem vai implementar e por quem vai operar às 3 da manhã. Tamanho não é rigor.

| Seção | Orçamento |
|---|---|
| Documento inteiro | 250 a 600 linhas; acima disso, há detalhe de implementação que pertence ao código ou a um documento de componente |
| Componentes | 3 a 12. Menos que isso raramente precisa de HLD; mais que isso é mais de um sistema |
| Fluxos | 2 a 5, com 3 a 8 passos cada |
| Entidades | 4 a 10 principais; o esquema completo é do código |
| Interfaces | só as que algo de fora do componente consome |
| Cada risco | probabilidade, impacto, 1 a 3 mitigações, 1 contingência |
| Célula de tabela | 1 a 3 frases; o que não cabe vai para o fluxo ou para o modelo de dados |

Três hábitos fazem quase todo o trabalho:

**Mensurável ou fora.** "Altamente disponível" e "escala bem" não são meta. "99.9 por cento mensal na API externa, RTO de 1 hora, RPO de 15 minutos" é. Mesma régua para SLA de interface (p95 em milissegundos, vazão), para observabilidade (que métrica, que limiar dispara alerta) e para segurança (qual mecanismo, onde).

**Hipótese é marcada, sempre, e na linha em que ocorre.** Tudo que você completou sem o usuário dizer leva `(hipótese)` no fim da linha, nessa forma literal, porque é ela que o validador conta e que o leitor procura; variantes como "(hipótese sobre o volume)" se perdem. Vale para número que você inventou (SLA, limite, retenção) e vale em dobro quando o HLD muda algo que o brief ou o PRD disse: reordenar o pipeline, trocar síncrono por assíncrono, dividir um componente. Mudança dessas é hipótese marcada no próprio texto, não só no relatório, porque quem lê o HLD daqui a um mês não vai ler o relatório. Quem lê precisa separar o que o time decidiu do que o documento sugeriu. Passou de 30 marcações, você está desenhando demais pelo usuário: corte ou pergunte. O relatório final lista todas as hipóteses, agrupadas por seção, as que mais mudam a arquitetura primeiro.

**Toda tecnologia aponta para uma decisão.** A tabela de tecnologias tem a coluna "Decisão" e ela nunca fica vazia: ou é `ADR-NNNN` que existe em `docs/ADR/`, ou é `pendente de ADR` com a decisão repetida em "Decisões pendentes de ADR" com as opções em jogo e o critério de escolha. O HLD não é o lugar de argumentar por que PostgreSQL e não outro banco; é o lugar de dizer que o banco é PostgreSQL e onde está o argumento.

## Finalizar

1. Rode a checagem de consistência de `references/entrevista.md` (seção "Antes de gerar").
2. Preencha `assets/template.md` sem mudar títulos, ordem ou negritos: o validador e quem lê dependem dessa estrutura. Seção sem conteúdo real não fica com placeholder; fica com uma linha dizendo que não se aplica e por quê.
3. Valide: `python3 <skill-dir>/scripts/validate.py docs/HLD.md`. Ele checa seções, placeholders esquecidos, componentes fora do diagrama (e vice-versa), tecnologias sem decisão, interfaces sem protocolo ou exposição, metas sem número, riscos incompletos e RFs da rastreabilidade que não existem no PRD. Corrija até sair sem erro.
4. Pergunte ao usuário, em uma linha, se quer o HLD também em JSON (chaves em inglês, valores em português). Se quiser, ou se estiver rodando sem interação e o pedido mencionou JSON: `python3 <skill-dir>/scripts/validate.py docs/HLD.md --json docs/HLD.json`. O script deriva o JSON do Markdown, então os dois nunca divergem. Chaves e enumerações (`deployment`, `probability`) ficam em inglês por contrato do esquema; todo o resto é o texto em português do HLD.
5. Reporte: caminho do arquivo, componentes e interfaces (quantidade), RFs cobertos e RFs sem componente, componentes sem RF, decisões pendentes de ADR (as que mais travam a implementação primeiro), hipóteses (as que mais mudam a arquitetura primeiro) e lacunas abertas.
