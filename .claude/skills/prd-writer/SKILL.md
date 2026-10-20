---
name: prd-writer
description: Conduz uma entrevista estruturada (em blocos por etapa) e gera o PRD do sistema em `docs/PRD.md`, em português, em 9 seções: resumo executivo, problema e oportunidade, público-alvo, objetivos com métricas e requisitos não funcionais, histórias de usuário, requisitos funcionais numerados (RF-001...) com contratos Consome/Fornece, capacidades com número, experiência e tratamento de erros, fora de escopo, mapa de dependências (tabela topológica, requisitos de fundação, ondas de execução, Mermaid) e critérios de aceitação por RF e de integração entre RFs. Gera junto o `docs/prd_progress.json`, o arquivo de progresso que as skills de implementação leem e atualizam, com merge que preserva o estado de cada RF quando o PRD é revisado. O PRD não fala de stack; decisões técnicas vão para ADRs. Use esta skill sempre que o usuário quiser escrever, montar, revisar ou atualizar um PRD, "documento de requisitos", "spec do produto", "definir o que o sistema faz", "levantar requisitos", "quebrar em features", "mapear o que depende do quê" ou "o que dá pra fazer em paralelo", mesmo que não diga a palavra PRD; também quando ele colar um brief ou uma ideia de sistema e pedir para "estruturar isso" antes de implementar, ou quando `docs/PRD.md` já existir e ele quiser mudar um requisito, escopo, dependência ou critério.
---

# PRD Writer

O PRD responde quatro perguntas para quem vai construir e para quem vai conferir depois: **por que o sistema existe, o que ele precisa fazer, como saberemos que está pronto e em que ordem construir**. Tudo nesta skill serve a isso.

Ele é escrito para ser **executado requisito por requisito**, por pessoas ou por agentes. Por isso cada RF diz o que consome de outros RFs e o que fornece a eles, a seção 8 ordena tudo em ondas que podem ser feitas em paralelo, e o `prd_progress.json` registra o estado de cada RF ao longo da implementação. Um RF que um agente não consiga implementar sem perguntar nada é um RF bem escrito.

Ele fala de **produto**: regras, fluxos, limites com número, metas observáveis. Não fala de stack. Linguagem, banco, framework, protocolo, hospedagem e arquitetura ficam fora, porque o PRD precisa continuar verdadeiro quando a stack mudar, e porque essas escolhas já têm casa neste repositório: `docs/HLD.md` via `/hld-writer` e `docs/ADR/` via `/adr-writer`. Quando o usuário disser "vamos usar X" no meio da entrevista, anote como **decisão pendente de ADR** no relatório final e não no PRD. A exceção é quando a tecnologia é o próprio produto ou uma restrição imposta de fora (integração obrigatória com o ERP da empresa, por exemplo): aí ela entra como dependência externa, descrita pelo que faz, não por como é feita.

## Modos

| Situação | Modo |
|---|---|
| Pedido de PRD sem material, ou com uma ideia em poucas frases | **Entrevista** |
| Usuário entregou um brief razoavelmente completo e pediu para não ser entrevistado, ou está rodando sem interação | **Direto** |
| `docs/PRD.md` já existe e o pedido é mudar algo | **Revisão** |

Em qualquer modo, comece lendo `assets/template.md` (esqueleto obrigatório da saída) e `references/entrevista.md` (perguntas por etapa, opções para oferecer, defaults e checagens). Leia os dois antes da primeira pergunta: a entrevista é guiada pelo que o template vai precisar, não o contrário. `references/progresso.md` descreve o arquivo de progresso; leia quando chegar em Finalizar ou quando o pedido tocar nele.

## Passo 0: destino e contexto

O PRD do sistema vive em **`docs/PRD.md`** na raiz do repositório (`git rev-parse --show-toplevel`), e o arquivo de progresso ao lado, em **`docs/prd_progress.json`**. Um só arquivo, um só lugar: é o que `CLAUDE.md`, HLD, ADRs e issues vão referenciar por `RF-NNN`. Se o PRD existe, isto é **Revisão**, não um PRD novo. Se o usuário pediu outro caminho, use e diga que está fora do padrão.

Antes da primeira pergunta, olhe o repositório: há código, `docs/`, `README`, ADRs em `docs/ADR/`? Resuma em uma linha ("projeto novo, sem contexto" ou "projeto existente com X, Y, Z") e aproveite o que encontrar: nomes já usados, regras de negócio já implementadas, integrações existentes, papéis de usuário. Em projeto existente, o PRD descreve o que vai ser adicionado ou mudado, não reconta o que já funciona. O que o repositório já decidiu de stack não entra no PRD; entra no relatório final como contexto.

## Modo: Entrevista

Sete etapas. Em cada uma: faça **um bloco de perguntas** (não uma por vez e não trinta de uma vez), use `AskUserQuestion` quando as respostas são enumeráveis (prioridade, tipo de público, qual de duas regras) e texto livre quando não são, depois **resuma em 3 a 6 linhas** o que entendeu e peça confirmação antes de seguir. O resumo é o que evita descobrir na etapa 6 que a etapa 1 foi mal entendida.

| Etapa | O que precisa sair dela |
|---|---|
| 1. Problema e oportunidade | Produto em três frases, contexto de implantação (novo, substitui ou integra algo), 3 a 5 categorias de dor com número aproximado, o que já foi tentado, e o que o produto faz de diferente para cada dor |
| 2. Público | Perfis distintos pelo que fazem e precisam, não por cargo; quantos o produto realmente tem (1 ou 2 se o público é homogêneo), e o que é comum a todos |
| 3. Objetivos e metas | Cada objetivo com verbo, métrica e meta com número e prazo; requisitos não funcionais como meta observável (performance e disponibilidade sempre; segurança, compatibilidade, compliance e acessibilidade quando o produto pede) |
| 4. Escopo | Lista dos requisitos funcionais por nome, e o que fica explicitamente fora, agrupado por categoria. É aqui que se decide quantos RFs o PRD tem |
| 5. Requisitos funcionais | Um por um: o que faz em uma frase, capacidades com limites e regras numeradas, experiência passo a passo, erros quando o RF é crítico, escopo mínimo quando há capacidades de prioridade diferente, prioridade 1 a 3. É a etapa longa; vá por RF e confirme cada bloco |
| 6. Contratos e dependências | Você deriva e apresenta para confirmação: quem consome o quê de quem, o que cada RF fornece, de que RFs cada um depende, quais são de fundação, e as dependências externas que travam RFs |
| 7. Aceitação | Critérios por RF cobrindo sucesso e falha, e critérios de integração derivados dos Consome |

Na etapa 6, não pergunte "do que RF-003 depende?"; proponha "RF-003 consome de RF-002 o catálogo de serviços com duração e preço, então depende dele. Confere?". O usuário corrige melhor do que inventa. O mesmo vale para a etapa 7.

Regras da conversa:

- **Quando o usuário não sabe, ofereça 2 ou 3 opções plausíveis** e marque a escolhida como `(hipótese)`. Os defaults de `references/entrevista.md` existem para isso. Nunca preencha em silêncio.
- **Inconsistência para a entrevista.** Objetivo sem RF que o entregue, item fora de escopo que um RF precisa, RF de prioridade 1 dependendo de um de prioridade 3, dois RFs que dependem um do outro: aponte e peça correção antes de continuar.
- **Não invente detalhes de negócio.** Se o usuário não deu, é lacuna ou hipótese, nunca fato. Detalhe de produto que o time pode decidir sozinho (passo da grade de horários, tamanho máximo de upload) pode ser preenchido com um número razoável marcado `(hipótese)`: o RF precisa de número para ser implementável.
- **Decisão técnica vai para o relatório, não para o PRD.** Agradeça, anote como pendente de ADR e siga.
- Perguntas simples, uma ideia por pergunta, sem travessão "—" no texto. A regra do travessão vale também para o PRD gerado. Colchetes são reservados aos placeholders do template, que o validador procura; variável em mensagem de exemplo vai entre sinais de menor e maior ("Olá <nome>").

## Modo: Direto

Quando o brief já veio, não encene a entrevista. Mapeie o material sobre as sete etapas, preencha o que está lá, complete o resto com os defaults marcados `(hipótese)` e **liste as lacunas no relatório final** em vez de perguntar uma a uma. Se houver uma ou duas perguntas cuja resposta muda o PRD inteiro (um público ou vários com jornadas diferentes, produto novo ou adição a um sistema existente, regra de cobrança), faça só essas, e só se houver alguém para responder.

## Modo: Revisão

1. Leia o `docs/PRD.md` atual inteiro e o `docs/prd_progress.json`, se existir, antes de perguntar qualquer coisa. O progresso diz o que já foi implementado: mudar um RF `done` custa retrabalho, e isso o usuário precisa ouvir antes de decidir.
2. Altere só o que o pedido toca. RF novo recebe o próximo `RF-NNN` livre; número nunca é reutilizado, mesmo que um requisito saia, porque issues, commits e o arquivo de progresso já podem citá-lo. RF removido some das seções 5, 6, 8 e 9 de uma vez e fica listado em "Fora de escopo" com o número e uma linha de motivo: meia remoção é pior que nenhuma.
3. Refaça contratos, tabela, ondas, Mermaid e critérios de integração: quase toda mudança de RF muda quem consome o quê e a ordem de construção.
4. Suba a versão no cabeçalho (`0.1.0` → `0.2.0` para RF novo ou removido, `0.1.1` para ajuste de texto, capacidade ou critério) e a data.
5. Valide, rode o `progress.py` (o merge preserva o estado dos RFs que continuam e marca `removed` os que saíram) e reporte o que mudou, incluindo RFs já implementados que o pedido tocou.

## Anatomia de um requisito funcional

Cada RF na seção 6 tem uma frase de descrição e blocos nesta ordem, omitindo os que não se aplicam: **Consome**, **Fornece**, **Escopo mínimo**, **Adições de escopo completo**, **Capacidades**, **Experiência**, **Tratamento de erros**. Capacidades e Experiência são obrigatórios. O validador conhece exatamente esses rótulos.

**Consome e Fornece são o contrato de integração.** Consome lista o que este RF precisa de outros RFs, por ID, nomeando os objetos de negócio e seus campos principais ("agendamento com cliente, telefone, data, horário e status"), sem tipos de programação. Fornece lista o que este RF entrega e quem usa, `(usado por RF-004, RF-006)`, agrupando num item só quando o mesmo dado serve a vários. Os dois lados precisam fechar: todo Consome tem um Fornece correspondente que nomeia o consumidor, e todo campo citado no Consome aparece no Fornece, ou com o mesmo nome ou sob um termo claramente mais amplo. Autenticação e sessão não entram em nenhum dos dois: são dependência de infraestrutura, e vivem só na tabela da seção 8. Só dado funcional, que flui de um RF para outro, entra no contrato.

**Escopo mínimo existe para RF com capacidades de prioridade diferente.** Quando parte do RF é essencial e parte é melhoria, Escopo mínimo lista o conjunto sem o qual o RF não cumpre seu propósito, e Adições de escopo completo lista o resto. A prioridade na tabela da seção 8 se refere ao escopo mínimo. RF em que tudo tem a mesma prioridade não tem esses blocos.

**Capacidades têm número.** Tamanho máximo, quantidade, prazo, formato, regra de negócio com a condição explícita. "Upload de vídeo" não é capacidade; "vídeo de até 2 GB em MP4 ou MOV, até 20 por dia por conta" é. Se o usuário não deu o número, proponha um e marque `(hipótese)`: um RF sem número não é implementável, e o número errado é mais barato de corrigir que a pergunta que nunca foi feita.

**Experiência é o fluxo em passos**, com campos, validações, ordem, feedback visual, estados (vazio, carregando, sucesso) e mensagens. Para RF sem interação direta (processamento, integração, regra automática), descreva o gatilho, o que o sistema faz e o que fica visível para alguém depois; as histórias desse RF começam com "Como o sistema, quero ...".

**Tratamento de erros entra só em RF crítico**, com 3 a 5 cenários e a mensagem exata de cada um. Crítico é o RF que envolve autenticação ou autorização, dinheiro, criação, alteração ou exclusão de dado persistente, operação sensível, ou operação longa ou irreversível em que a falha parcial é possível. A pergunta que decide: "se este RF falhar em silêncio, o usuário perde dado, dinheiro ou segurança?". Se sim, o bloco entra. Se a falha só pede recarregar a tela (navegação, listagem, filtro, busca em dado já carregado), não entra.

## Mapa de dependências e paralelismo

A seção 8 transforma o PRD em plano de execução sem falar de stack. É derivada, apresentada para confirmação, e o validador a recalcula inteira. As regras:

- **Tabela** com `#`, Requisito, Prioridade e Depende de. "B depende de A" quando B não funciona sem A implementado antes: dependência de dado (que também aparece em Consome) ou de infraestrutura (autenticação, por exemplo). A coluna Depende de é sempre um superconjunto do Consome. Só dependência direta: se A → B → C, não escreva A → C, salvo quando C consome dado de A diretamente. "Faz sentido fazer depois" não é dependência; é preferência, e preferência não vai na tabela. A tabela só tem semântica E; se um RF funciona com qualquer uma de duas alternativas, escolha a principal e registre a outra na descrição do RF.
- **Ordem da tabela é topológica**, com desempate pelo menor ID: toda dependência aparece em linha acima, e o leitor nunca encontra referência para frente. O validador imprime a ordem esperada quando a tabela sai dela.
- **Sem ciclos.** Ciclo significa que dois RFs são um só ou que um deles precisa ser dividido, ou que uma das arestas é conveniência de interface e não necessidade de dado. Resolva antes de escrever.
- **Prioridade** é 1, 2 ou 3 (legenda fixa no template) e se refere ao escopo mínimo quando ele existe. **Prioridade herda para trás**: se um RF 1 depende de um RF 3, o RF 3 não é 3. Corrija na etapa de requisitos.
- **Requisitos de fundação** são os que montam a base compartilhada do projeto: acesso e papéis, estrutura inicial, o que todo RF posterior usa sem citar em Consome. O critério é o propósito principal do RF, não o fato de ele criar alguma estrutura de passagem: uma tela de painel que inaugura uma área do produto continua sendo RF de produto. Em projeto novo, fundação é implementada em sequência mesmo quando cai na mesma onda, porque mexe nos mesmos arquivos de base; por isso a nota nas ondas. Em projeto existente e maduro, a subseção normalmente não existe, e a nota também não.
- **Ondas** são calculadas mecanicamente: onda 1 são os RFs sem dependência; cada RF fica em `1 + maior onda entre as suas dependências`. Dentro da onda, prioridade crescente e depois ID. Tudo que está na mesma onda pode ser construído em paralelo, e isso é a resposta a "o que dá pra fazer junto". Diga também o **caminho crítico**, a cadeia mais longa, porque é ela que define o prazo mínimo.
- **Mermaid `graph TD`** com uma aresta por linha da tabela, nem mais nem menos; nó `RF001["RF-001 Nome curto"]`. A tabela é a fonte de verdade; o diagrama é visualização. Mermaid porque renderiza no GitHub e ainda é texto greppável para quem não renderiza.
- **Dependências externas** (provedor de pagamento, serviço de mensagens, outro time, dado legado) não são nós: ficam listadas ao fim da seção 8, descritas pelo que fazem, com `(trava RF-NNN)` dizendo que RFs param enquanto não chegam.

## Critérios de aceitação

Por RF, critérios verificáveis por alguém de fora do time, cobrindo sucesso e falha, derivados das capacidades e dos erros previstos. Depois de todos, o bloco **Integração entre requisitos**: um ou mais critérios para cada Consome, testando que o dado declarado chega de fato de um RF ao outro e produz o efeito esperado, citando os dois IDs na frase. É o que transforma "cada feature passou" em "o produto funciona". RF sem Consome não gera critério de integração; PRD sem nenhum Consome tem o bloco com uma linha "não se aplica".

## Estilo e orçamento

O PRD é lido por quem vai implementar sob pressão de prazo, inclusive por agentes que vão implementar um RF de cada vez. Tamanho não é rigor, mas RF vago custa mais caro que RF longo.

| Seção | Orçamento |
|---|---|
| Documento inteiro | 300 a 700 linhas; acima disso, há produto demais para um PRD só |
| Requisitos funcionais | 5 a 15. Menos que 3 é agrupamento grosso demais; mais que 20 é mais de uma entrega ou capacidades a consolidar |
| Resumo executivo | 2 a 3 parágrafos |
| Categorias de dor | 3 a 5, com 3 a 4 bullets cada e número sempre que possível |
| Perfis de usuário | quantos o produto tiver de fato; 1 ou 2 para público homogêneo |
| Objetivos | 3 a 5, cada um com métrica e meta numérica |
| Histórias por RF | quantas o RF pedir; interação concreta, agrupadas por RF, nunca por perfil |
| Tratamento de erros | 3 a 5 cenários, só em RF crítico |
| Cada critério de aceitação | 1 frase verificável |

Três hábitos fazem quase todo o trabalho:

**Verificável ou fora.** "Funciona bem" e "deve ser rápido" não são critério nem requisito. "Lista de horários livres aparece em até 1 segundo para 95 por cento das consultas" é. Mesma régua para metas (número e prazo), capacidades (limite com unidade) e requisitos não funcionais (um alvo que dê para medir sem saber a stack).

**Hipótese é marcada, sempre, e na linha em que ocorre.** Tudo que você completou sem o usuário dizer leva `(hipótese)` no fim da linha, nessa forma literal, porque é ela que o validador conta e que o leitor procura; variantes como "(hipótese sobre o prazo)" se perdem. Vale para regra de negócio que alguém precisa confirmar (o que conta como falta, quem aprova) e para número que você propôs. Passou de 30 marcações, você está decidindo demais pelo usuário: corte ou pergunte. O relatório final lista todas as hipóteses, as que mais mudam o produto primeiro.

**Requisito que o usuário não pediu é exceção, e vem avisado.** Às vezes falta um RF sem o qual uma meta não se mede (um painel de indicadores) ou um fluxo não fecha (cadastrar antes de listar) ou a base não existe (acesso e papéis). Acrescente, marque `(hipótese)` no nome e destaque no relatório final em uma lista própria, "requisitos que eu adicionei", para o usuário aprovar ou cortar. Requisito inventado sem aviso é a forma mais cara de hipótese: vira trabalho.

## Finalizar

1. Rode a checagem de consistência de `references/entrevista.md` (seção "Antes de gerar").
2. Preencha `assets/template.md` sem mudar títulos, numeração, ordem ou negritos: o validador e quem lê dependem dessa estrutura. Subseção opcional que não se aplica (Perfil comportamental com um perfil só, Requisitos de fundação, Dependências externas) sai inteira, com a nota das ondas junto no caso da fundação. Escreva o PRD inteiro de uma vez; não peça aprovação seção por seção.
3. Valide: `python3 <skill-dir>/scripts/validate.py docs/PRD.md`. Ele checa as 9 seções, placeholders, blocos obrigatórios de cada RF, contratos Consome/Fornece fechados nos dois lados, tabela topológica sem ciclo nem órfão, Consome dentro de Depende de, prioridade que herda para trás, fundação e nota, ondas recalculadas, caminho crítico, Mermaid igual à tabela, histórias e critérios para todo RF e critério de integração para todo Consome. Corrija e rode de novo, até 3 vezes; se ainda houver erro, pare e mostre ao usuário o que sobrou em vez de forçar.
4. Gere o progresso: `python3 <skill-dir>/scripts/progress.py docs/PRD.md`. Ele deriva os RFs da seção 8 e aplica o contrato de merge de `references/progresso.md`; não escreva esse JSON à mão. Se ele avisar que preservou um arquivo corrompido ou se recusar por schema mais novo, repasse ao usuário.
5. Pergunte ao usuário, em uma linha, se quer o PRD também em JSON (chaves em inglês, valores em português). Se quiser, ou se estiver rodando sem interação e o pedido mencionou JSON: `python3 <skill-dir>/scripts/validate.py docs/PRD.md --json docs/PRD.json`. O script deriva o JSON do Markdown, então os dois nunca divergem.
6. Reporte: caminho do PRD e do progresso; RFs por onda com o caminho crítico; requisitos de fundação; requisitos que você adicionou sem o usuário pedir; hipóteses (as que mais mudam o produto primeiro); lacunas abertas; dependências externas que travam RFs; e decisões de stack que apareceram e precisam virar ADR.
