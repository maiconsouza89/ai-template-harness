# Guia da entrevista

Perguntas por etapa, opções para oferecer quando o usuário não sabe, defaults (sempre marcados como hipótese) e checagens antes de gerar. Use como base; adapte ao vocabulário do usuário. Uma ideia por pergunta. Em cada etapa, feche com resumo de 3 a 6 linhas e confirmação.

## Etapa 1: contexto e problema

Perguntas
- Qual é o sistema, em duas ou três frases, e qual resultado de negócio ele precisa produzir?
- Quem usa? Liste os públicos e o que diferencia cada um (papel, frequência de uso, nível técnico).
- O sistema é novo, substitui algo que existe hoje (planilha, processo manual, sistema legado) ou se integra a algo existente? Descreva o que esse algo faz hoje.
- O que está ruim hoje: caro, lento, inseguro, frágil, manual? Peça um exemplo recente com número aproximado (horas perdidas por semana, reais por mês, erros por lote, clientes perdidos).
- O que já foi tentado e não resolveu?

Se o usuário não sabe o público, ofereça: usuário final externo; operador interno; administrador ou gestor. Se não tem número, peça ordem de grandeza (dezenas, centenas, milhares) e registre como hipótese.

## Etapa 2: objetivos e métricas

Para cada objetivo: resultado mensurável, métrica que o representa, meta alvo com prazo. Objetivo → métrica → meta é uma linha da tabela; linha incompleta não entra.

Se o usuário tem o objetivo mas não a métrica, ofereça 2 ou 3 métricas plausíveis para o tipo de objetivo:
- reduzir esforço: horas por semana, passos por tarefa, tempo até concluir
- reduzir erro: taxa de erro por lote, retrabalho por mês, tickets de suporte
- crescer: cadastros por mês, conversão, retenção em 30 dias
- confiabilidade: incidentes por mês, tempo de recuperação

## Etapa 3: escopo

- O que precisa obrigatoriamente estar pronto nesta entrega?
- O que fica explicitamente fora, mesmo que alguém vá pedir?

Teste cada item de fora de escopo contra os objetivos e os requisitos já ditos: fora de escopo que impede um objetivo é contradição e precisa ser resolvida agora.

## Etapa 4: requisitos funcionais

Para cada requisito, nesta ordem:
1. Nome curto (verbo + objeto: "Cadastrar produto", "Aprovar reembolso").
2. Descrição em uma frase: o que o sistema faz.
3. Fluxo principal, passo a passo (3 a 8 passos), do gatilho ao resultado.
4. Variações comuns e exceções.
5. Condições de bloqueio ou erro, e o que o usuário vê em cada uma.
6. Prioridade: alta (sem isso a entrega não serve), media (entrega serve, mas pior), baixa (pode ficar para depois).

Peça a lista de requisitos antes de detalhar; depois detalhe um por um e confirme cada bloco. Se o usuário descreve um requisito que depende de outro ainda não listado, registre o novo e volte.

Sinais para dividir um requisito: fluxo principal com mais de 8 passos; dois gatilhos diferentes; dois públicos com fluxos diferentes.

## Etapa 5: requisitos não funcionais

Colete como meta observável sem citar tecnologia. Se o usuário não sabe, use os defaults abaixo e marque hipótese.

| Categoria | Pergunta | Default (hipótese) |
|---|---|---|
| Performance | Quanto tempo o usuário tolera esperar nas ações principais? | ações comuns respondem em até 1 segundo para 95 por cento dos casos; relatórios e exportações em até 10 segundos |
| Disponibilidade | Quando o sistema pode ficar fora? Custa quanto por hora parado? | 99.9 por cento mensal para público externo; 99.5 por cento para uso interno |
| Segurança e autorização | Quem pode ver e alterar o quê? O que é sensível? | autenticação obrigatória; permissão por papel; alterações sensíveis registradas com autor, valor anterior e horário |
| Auditoria e rastreabilidade | O que precisa ser reconstruído depois do fato? | toda operação que altera dinheiro, estoque ou dado pessoal é rastreável |
| Confiabilidade e integridade | Que dado nunca pode ficar inconsistente? | operações críticas acontecem por inteiro ou não acontecem |
| Compatibilidade | Em que dispositivos, navegadores e idiomas? | navegadores dos últimos 2 anos, desktop e celular; português do Brasil |
| Compliance | Há norma aplicável (LGPD, setor regulado, contrato)? | dados pessoais tratados conforme a LGPD |
| Acessibilidade | Há exigência legal ou de público? | fluxos principais operáveis por teclado e leitor de tela |

Performance e disponibilidade entram sempre, nem que como hipótese: sem elas ninguém sabe o que é "lento" nem o que é "caiu".

## Etapa 6: decisões de produto e dependências

Decisões: que regras de produto já estão dadas (modelo de cobrança, quem aprova, o que é obrigatório no cadastro, política de cancelamento)? Para cada uma: por que, e o que se perde com ela. Decisão sem trade-off provavelmente ainda não foi pensada.

Se o usuário traz decisão técnica ("vai ser em tal linguagem", "vamos usar tal banco"), agradeça, anote em "decisões pendentes de ADR" para o relatório final e não a ponha no PRD.

Dependências, três tipos:
- externa: serviço ou dado de terceiro (gateway de pagamento, API de CEP, emissão de nota)
- organizacional: outro time ou área precisa entregar ou aprovar (design, jurídico, política comercial)
- pré-requisito: algo que precisa existir antes, descrito pelo que faz (base de clientes migrada, cadastro de produtos saneado)

Para cada uma: quem entrega o quê, por quê, e o que trava enquanto não chega. Dependência que trava um RF vira nó `DEP-N` no mapa.

## Etapa 7: riscos

Para cada risco: frase única, probabilidade (baixa, media, alta), impacto concreto, mitigações (uma ou mais), plano de contingência se acontecer mesmo assim.

Se o usuário não enxerga riscos, ofereça os típicos do que foi coletado: dependência externa atrasar; adoção baixa pelo público; dado legado pior que o esperado; regra de negócio mudar no meio; volume maior que o previsto.

## Etapa 8: aceitação e validação

Critérios de aceitação: uma frase cada, verificável por alguém de fora do time, derivada dos RFs de prioridade alta, das metas e dos NFRs. Exemplo bom: "Toda alteração de preço gera registro com quem alterou, preço anterior e horário". Exemplo ruim: "sistema funciona bem".

Validação: que tipos são obrigatórios (testes automatizados das regras críticas, ponta a ponta do fluxo principal, carga na meta de performance, acessibilidade, segurança de permissões) e qual estratégia (roteiro de aceitação com usuário real, validação exploratória interna, piloto com grupo restrito).

## Mapa de dependências

Depois da etapa 8, derive e apresente para confirmação, não pergunte do zero. Para cada par de RFs com relação de dado, fluxo ou regra, proponha a aresta com o motivo. Depois monte as ondas e mostre o caminho crítico. Pergunte apenas: "Está correto? Falta ou sobra alguma dependência?".

## Antes de gerar

Confirme cada item; o que falhar volta para a etapa correspondente.

- Cada objetivo tem métrica e meta com número.
- Cada RF tem nome, descrição, fluxo principal com 3 a 8 passos e prioridade.
- Requisitos não funcionais incluem performance e disponibilidade, mesmo como hipótese.
- Nenhum item fora de escopo contradiz um requisito ou objetivo.
- Toda decisão de produto tem justificativa e trade-off.
- Cada dependência diz quem entrega o quê.
- Cada risco tem probabilidade, impacto, mitigação e contingência.
- Cada critério de aceitação é verificável por alguém de fora.
- Nenhum RF de prioridade alta depende de um RF de prioridade baixa.
- O grafo não tem ciclo nem aresta transitiva; toda aresta tem rótulo.
- Cada RF aparece em exatamente uma onda, e nenhum RF está na mesma onda ou antes de um predecessor.
- Nada no PRD cita linguagem, framework, banco, protocolo ou hospedagem, salvo integração obrigatória descrita pelo que faz.
- Toda hipótese está marcada com `(hipótese)`.
- Nenhum travessão "—" no texto.
