---
name: prd-writer
description: Conduz uma entrevista estruturada (em blocos por etapa) e gera o PRD do sistema em `docs/PRD.md`, em português, com regras de produto, requisitos funcionais numerados (RF-001...), requisitos não funcionais como metas observáveis, riscos, critérios de aceitação e, no fim, um mapa de dependências entre requisitos (Mermaid) com ondas de implementação dizendo o que pode ser desenvolvido em paralelo. O PRD não fala de stack; decisões técnicas são encaminhadas para ADRs. Use esta skill sempre que o usuário quiser escrever, montar, revisar ou atualizar um PRD, "documento de requisitos", "spec do produto", "definir o que o sistema faz", "levantar requisitos", "mapear o que depende do quê" ou "o que dá pra fazer em paralelo", mesmo que não diga a palavra PRD; também quando ele colar um brief ou uma ideia de sistema e pedir para "estruturar isso" antes de implementar, ou quando `docs/PRD.md` já existir e ele quiser mudar um requisito, escopo ou critério.
---

# PRD Writer

O PRD responde quatro perguntas para quem vai construir e para quem vai conferir depois: **por que o sistema existe, o que ele precisa fazer, como saberemos que está pronto e em que ordem construir**. Tudo nesta skill serve a isso.

Ele fala de **produto**: regras, fluxos, metas observáveis, riscos. Não fala de stack. Linguagem, banco, framework, protocolo, hospedagem e arquitetura ficam fora, porque o PRD precisa continuar verdadeiro quando a stack mudar, e porque essas escolhas já têm casa neste repositório: `docs/adr/` via `/adr-writer`. Quando o usuário disser "vamos usar X" no meio da entrevista, anote como **decisão pendente de ADR** no relatório final e não no PRD. A exceção é quando a tecnologia é o próprio produto ou uma restrição imposta de fora (integração obrigatória com o ERP da empresa, por exemplo): aí ela entra como dependência externa ou requisito, descrita pelo que faz, não por como é feita.

## Modos

| Situação | Modo |
|---|---|
| Pedido de PRD sem material, ou com uma ideia em poucas frases | **Entrevista** |
| Usuário entregou um brief razoavelmente completo e pediu para não ser entrevistado, ou está rodando sem interação | **Direto** |
| `docs/PRD.md` já existe e o pedido é mudar algo | **Revisão** |

Em qualquer modo, comece lendo `assets/template.md` (esqueleto obrigatório da saída) e `references/entrevista.md` (perguntas por etapa, opções para oferecer, defaults e checagens). Leia os dois antes da primeira pergunta: a entrevista é guiada pelo que o template vai precisar, não o contrário.

## Passo 0: destino

O PRD do sistema vive em **`docs/PRD.md`** na raiz do repositório (`git rev-parse --show-toplevel`). Um só arquivo, um só lugar: é o que `CLAUDE.md`, ADRs e issues vão referenciar por `RF-NNN`. Se o arquivo existe, isto é **Revisão**, não um PRD novo. Se o usuário pediu outro caminho, use e diga que está fora do padrão.

## Modo: Entrevista

Oito etapas. Em cada uma: faça **um bloco de perguntas** (não uma por vez e não trinta de uma vez), use `AskUserQuestion` quando as respostas são enumeráveis (prioridade, tipo de público, probabilidade de risco) e texto livre quando não são, depois **resuma em 3 a 6 linhas** o que entendeu e peça confirmação antes de seguir. O resumo é o que evita descobrir na etapa 7 que a etapa 1 foi mal entendida.

| Etapa | O que precisa sair dela |
|---|---|
| 1. Contexto e problema | Produto, público, contexto de implantação (sistema novo, substitui ou se integra a algo existente), objetivo de negócio, dor atual com números aproximados, o que já foi tentado |
| 2. Objetivos e métricas | Cada objetivo com métrica e meta alvo. Objetivo sem número vira desejo, não requisito |
| 3. Escopo | Incluso e fora de escopo. Fora de escopo explícito é o que impede a conversa de "mas eu achei que..." meses depois |
| 4. Requisitos funcionais | Um por um: nome, descrição em uma frase, fluxo principal passo a passo, variações e exceções, erros previstos, prioridade. É a etapa longa; vá por requisito e confirme cada bloco |
| 5. Requisitos não funcionais | Metas observáveis: tempo de resposta percebido, disponibilidade, quem pode fazer o quê, auditoria, compliance, acessibilidade, compatibilidade (dispositivos, navegadores, idiomas) |
| 6. Decisões de produto e dependências | Regras já dadas (com justificativa e trade-off) e o que precisa chegar de fora: outro time, política, aprovação, serviço de terceiro |
| 7. Riscos | Probabilidade, impacto, mitigações (lista) e plano de contingência |
| 8. Aceitação e validação | Checklist verificável de pronto e tipos de validação obrigatórios |

Depois da etapa 8 vem o **mapa de dependências**, que você deriva do que foi coletado e apresenta para confirmação (ver abaixo). Não pergunte "do que RF-003 depende?"; proponha "RF-003 depende de RF-001 porque edita o cadastro que RF-001 cria. Confere?". O usuário corrige melhor do que inventa.

Regras da conversa:

- **Quando o usuário não sabe, ofereça 2 ou 3 opções plausíveis** e marque a escolhida como `(hipótese)`. Os defaults de `references/entrevista.md` existem para isso. Nunca preencha em silêncio.
- **Inconsistência para a entrevista.** Fora de escopo que contradiz um requisito, meta sem métrica, requisito "alta" que depende de um "baixa": aponte e peça correção antes de continuar.
- **Não invente detalhes.** Se o usuário não deu, é lacuna ou hipótese, nunca fato.
- Perguntas simples, uma ideia por pergunta, sem travessão "—" no texto. A regra do travessão vale também para o PRD gerado.

## Modo: Direto

Quando o brief já veio, não encene a entrevista. Mapeie o brief sobre as oito etapas, preencha o que está lá, marque `(hipótese)` o que você completou com os defaults e **liste as lacunas no relatório final** em vez de perguntar uma a uma. Se houver uma ou duas perguntas cuja resposta muda o PRD inteiro (quem é o público, se o sistema é novo ou substitui um existente), faça só essas, e só se houver alguém para responder.

## Modo: Revisão

1. Leia o `docs/PRD.md` atual inteiro antes de perguntar qualquer coisa.
2. Altere só o que o pedido toca. Requisito novo recebe o próximo `RF-NNN` livre; número nunca é reutilizado, mesmo que um requisito saia, porque issues e commits já podem citá-lo. Requisito removido fica listado em "Fora de escopo" com uma linha de motivo.
3. Refaça o mapa de dependências e as ondas: quase toda mudança de requisito muda a ordem de construção.
4. Suba a versão no cabeçalho (`0.1.0` → `0.2.0` para requisito novo ou removido, `0.1.1` para ajuste de texto) e a data.
5. Valide e reporte o que mudou.

## Mapa de dependências e paralelismo

É a seção que transforma o PRD em plano de execução sem falar de stack. Regras para derivá-lo:

- **Nó** = requisito funcional (`RF-NNN`). Dependência externa relevante para a ordem entra como nó `DEP-N` com forma diferente.
- **Aresta A → B** quando B não pode ser construído ou validado sem A. Três motivos, e só esses: **dado** (B lê ou altera algo que A cria), **fluxo** (B é passo posterior obrigatório da mesma jornada) e **regra** (B aplica uma regra que A define). Ponha o motivo no rótulo da aresta. "Faz sentido fazer depois" não é dependência; é preferência, e preferência não vai no grafo.
- **Só dependências diretas.** Se A → B e B → C, não desenhe A → C. Aresta transitiva polui e esconde o caminho crítico.
- **Sem ciclos.** Ciclo significa que dois requisitos são um só ou que um deles precisa ser dividido. Resolva antes de escrever.
- **Ondas**: onda 1 são os RFs sem predecessor; um RF entra na onda n quando todos os seus predecessores estão em ondas menores que n. Tudo que está na mesma onda pode ser desenvolvido em paralelo, e isso é a resposta à pergunta "o que dá pra fazer junto". Diga também o **caminho crítico** (a cadeia mais longa), porque é ele que define o prazo mínimo.
- **Prioridade herda para trás.** Se um RF de prioridade alta depende de um RF de prioridade baixa, o de baixa não é baixa. Sinalize e corrija na etapa de requisitos.

Formato: um bloco Mermaid `graph LR` seguido da tabela de ondas, exatamente como no template. Mermaid porque renderiza no GitHub e ainda é texto greppável para quem não renderiza.

## Estilo e orçamento

O PRD é lido por quem vai implementar sob pressão de prazo. Tamanho não é rigor.

| Seção | Orçamento |
|---|---|
| Documento inteiro | 250 a 500 linhas; acima disso, há requisito que devia ser dividido em outro PRD ou detalhe que é de implementação |
| Requisitos funcionais | 6 a 15. Menos que isso raramente é um sistema; mais que isso é mais de uma entrega |
| Resumo | até 5 frases |
| Cada problema priorizado | 1 linha com impacto e prioridade |
| Fluxo principal de um RF | 3 a 8 passos |
| Cada critério de aceitação | 1 frase verificável |
| Cada risco | probabilidade, impacto, 1 a 3 mitigações, 1 contingência |

Dois hábitos fazem quase todo o trabalho:

**Verificável ou fora.** "Funciona bem" e "deve ser rápido" não são critério nem requisito. "Toda alteração de preço gera registro com quem alterou, valor anterior e horário" é. Mesma régua para metas (número e prazo) e para requisitos não funcionais (um alvo que dê para medir sem saber a stack).

**Hipótese é marcada, sempre, e só quando muda o produto.** Tudo que você completou sem o usuário dizer leva `(hipótese)` no fim da linha. Quem lê precisa separar o que o negócio decidiu do que o documento sugeriu. Mas hipótese é para regra de negócio que alguém precisa confirmar (o que conta como falta, quem aprova, acesso expira ou não), não para detalhe de implementação que o time decide sozinho (tamanho de grade de horário, formato de arquivo, limite de upload). Detalhe desse tipo nem entra no PRD. Passou de 30 marcações, você está decidindo demais pelo usuário: corte. O relatório final lista todas as hipóteses juntas, as que mais mudam o produto primeiro.

**Requisito que o usuário não pediu é exceção, e vem avisado.** Às vezes falta um RF sem o qual uma meta não se mede (um painel de indicadores) ou um fluxo não fecha (cadastrar antes de listar). Acrescente, marque `(hipótese)` no nome e destaque no relatório final em uma lista própria, "requisitos que eu adicionei", para o usuário aprovar ou cortar. Requisito inventado sem aviso é a forma mais cara de hipótese: vira trabalho.

## Finalizar

1. Rode a checagem de consistência de `references/entrevista.md` (seção "Antes de gerar").
2. Preencha `assets/template.md` sem mudar títulos, ordem ou negritos: o validador e quem lê dependem dessa estrutura. Seção sem conteúdo real não fica com placeholder; fica com uma linha dizendo que não se aplica e por quê.
3. Valide: `python3 <skill-dir>/scripts/validate.py docs/PRD.md`. Ele checa seções, requisitos incompletos, placeholders esquecidos, arestas para RFs inexistentes, ciclos e ondas incoerentes. Corrija até sair sem erro.
4. Reporte: caminho do arquivo, quantidade de RFs por onda com o caminho crítico, requisitos que você adicionou sem o usuário pedir, hipóteses (as que mais mudam o produto primeiro), lacunas abertas e decisões de stack que apareceram e precisam virar ADR.
