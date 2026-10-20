# Guia da entrevista

Perguntas por etapa, opções para oferecer quando o usuário não sabe, defaults (sempre marcados como hipótese) e checagens antes de gerar. Use como base; adapte ao vocabulário do usuário. As perguntas de cada etapa são feitas uma de cada vez, nesta ordem, pulando as que o material do usuário já respondeu. Cada uma vai com 2 a 4 alternativas montadas do contexto e a recomendada em primeiro, marcada "(Recomendado)"; as opções e defaults abaixo são a matéria-prima dessas alternativas. Em cada etapa, feche com resumo de 3 a 6 linhas e confirmação.

## Etapa 1: problema e oportunidade

Perguntas
- Qual é o produto, em duas ou três frases, e qual resultado de negócio ele precisa produzir?
- O sistema é novo, substitui algo que existe hoje (planilha, processo manual, sistema legado) ou se integra a algo existente? Descreva o que esse algo faz hoje, não como é feito.
- O que está ruim hoje? Agrupe em 3 a 5 dores com nome. Para cada uma, peça um exemplo recente com número aproximado (horas perdidas por semana, reais por mês, erros por lote, clientes perdidos).
- O que já foi tentado e não resolveu?
- Para cada dor: o que o produto faz de diferente do que existe? É o diferencial, não a lista de funcionalidades.

Se não tem número, peça ordem de grandeza (dezenas, centenas, milhares) e registre como hipótese. Dor sem número vira opinião; a seção 2 precisa de pelo menos um número por dor.

## Etapa 2: público

Perguntas
- Quem usa? Liste os perfis e o que diferencia cada um pelo que faz e precisa: frequência, dispositivo, nível técnico, o que quer resolver.
- Esses perfis têm jornadas diferentes no produto, ou é o mesmo uso com permissões diferentes?
- O que é comum a todos (dispositivo, tolerância a cadastro, horário de uso)?

Se o usuário não sabe o público, ofereça: usuário final externo; operador interno; administrador ou gestor. Não force quantidade: público homogêneo tem 1 ou 2 perfis, e nesse caso o "Perfil comportamental" só entra se houver mais de um perfil.

## Etapa 3: objetivos e metas

Para cada objetivo: verbo de ação, métrica que o representa, meta com número e prazo. Objetivo → métrica → meta é uma linha da tabela; linha incompleta não entra. De 3 a 5 objetivos.

Se o usuário tem o objetivo mas não a métrica, ofereça 2 ou 3 métricas plausíveis para o tipo de objetivo:
- reduzir esforço: horas por semana, passos por tarefa, tempo até concluir
- reduzir erro: taxa de erro por lote, retrabalho por mês, tickets de suporte
- crescer: cadastros por mês, conversão, retenção em 30 dias
- confiabilidade: incidentes por mês, tempo de recuperação

Requisitos não funcionais, como meta observável sem citar tecnologia. Se o usuário não sabe, use os defaults abaixo e marque hipótese.

| Categoria | Pergunta | Default (hipótese) |
|---|---|---|
| Performance | Quanto tempo o usuário tolera esperar nas ações principais? | ações comuns respondem em até 1 segundo para 95 por cento dos casos; relatórios e exportações em até 10 segundos |
| Disponibilidade | Quando o sistema pode ficar fora? Custa quanto por hora parado? | 99.9 por cento mensal para público externo; 99.5 por cento para uso interno |
| Segurança e autorização | Quem pode ver e alterar o quê? O que é sensível? | identificação obrigatória; permissão por papel; alterações sensíveis registradas com autor, valor anterior e horário |
| Compatibilidade | Em que dispositivos, navegadores e idiomas? | navegadores dos últimos 2 anos, desktop e celular; português do Brasil |
| Compliance | Há norma aplicável (LGPD, setor regulado, contrato)? | dados pessoais tratados conforme a LGPD |
| Acessibilidade | Há exigência legal ou de público? | fluxos principais operáveis por teclado e leitor de tela |

Performance e disponibilidade entram sempre, nem que como hipótese: sem elas ninguém sabe o que é "lento" nem o que é "caiu". As outras entram quando o produto pede.

## Etapa 4: escopo

- Liste os requisitos funcionais por nome curto (verbo + objeto: "Agendar horário", "Aprovar reembolso"). Ainda sem detalhar: é a lista que a etapa 5 vai percorrer.
- O que fica explicitamente fora desta versão, mesmo que alguém vá pedir? Agrupe por categoria (pagamento, plataforma, operação, integrações).

Sinais para dividir um RF: dois gatilhos diferentes; dois perfis com fluxos diferentes; mais de 8 passos na experiência. Sinais para juntar: dois RFs que nunca são implementados separados e não trocam dado entre si. O alvo é 5 a 15 RFs.

Teste cada item de fora de escopo contra os objetivos e os RFs listados: fora de escopo que impede um objetivo é contradição e precisa ser resolvida agora.

Se o projeto é novo e nenhum RF cuida de acesso e papéis, pergunte se o produto tem login e quem pode o quê. Se tem, isso é um RF de fundação, e provavelmente o primeiro.

## Etapa 5: requisitos funcionais

Para cada requisito, nesta ordem:
1. Descrição em uma frase: o que o sistema faz.
2. Capacidades: limites com número (tamanho, quantidade, prazo), formatos, regras de negócio com a condição explícita. Se o usuário não sabe o número, proponha um e marque hipótese.
3. Experiência: fluxo passo a passo do gatilho ao resultado, com campos, validações, ordem, feedback visual, estados (vazio, carregando, sucesso) e mensagens. Para RF sem interação direta, gatilho, o que o sistema faz e o que fica visível depois.
4. Tratamento de erros, só se o RF é crítico: 3 a 5 cenários com a mensagem exata e o que acontece com o dado. Crítico é o que envolve acesso, dinheiro, dado persistente, operação sensível, longa ou irreversível. Pergunta de corte: "se falhar em silêncio, o usuário perde dado, dinheiro ou segurança?".
5. Escopo mínimo e adições, só se há capacidades de prioridade diferente dentro do RF: o que é indispensável para o RF cumprir o propósito, e o que entra depois.
6. Prioridade: 1 (o produto não funciona sem isso), 2 (agrega valor significativo), 3 (melhoria incremental). Refere-se ao escopo mínimo quando ele existe.

Peça a lista inteira antes (etapa 4); depois detalhe um por um e confirme cada bloco. Se o usuário descreve um RF que depende de outro ainda não listado, registre o novo e volte.

Histórias de usuário saem desta etapa também: para cada RF, 2 a 6 histórias "Como <perfil>, quero <ação concreta> para <resultado>", agrupadas por RF, nunca por perfil. Histórias descrevem interação com o produto, não objetivos abstratos.

## Etapa 6: contratos e dependências

Derive e apresente para confirmação, não pergunte do zero.

- Para cada par de RFs em que um usa dado que o outro cria, proponha o Consome (no consumidor, com os campos) e o Fornece (no produtor, com "usado por"). Autenticação e sessão não entram: são infraestrutura.
- Para cada RF, proponha a lista "Depende de": todo Consome mais as dependências de infraestrutura (acesso, cadastro base). Só diretas. Pergunte apenas: "Está correto? Falta ou sobra alguma dependência?".
- Proponha quais RFs são de fundação (montam a base que todos usam) e por quê. Em projeto existente, normalmente nenhum.
- Liste as dependências externas (serviço de terceiro, outro time, dado legado), descritas pelo que fazem, e que RFs cada uma trava.
- Mostre as ondas e o caminho crítico, e confira se a prioridade é coerente: RF 1 dependendo de RF 3 é sinal de que o 3 está errado.

Se o usuário traz decisão técnica ("vai ser em tal linguagem", "vamos usar tal banco"), agradeça, anote em "decisões pendentes de ADR" para o relatório final e não a ponha no PRD.

## Etapa 7: aceitação

Por RF: critérios de uma frase, verificáveis por alguém de fora do time, derivados das capacidades e dos erros, cobrindo sucesso e falha. Exemplo bom: "Horário tomado entre a escolha e a confirmação devolve o cliente ao passo 4 com a lista atualizada". Exemplo ruim: "agendamento funciona bem".

Integração entre requisitos: para cada Consome, um ou mais critérios que testam que o dado chega de um RF ao outro e produz o efeito esperado, citando os dois IDs. Apresente a lista derivada e pergunte só o que falta.

## Antes de gerar

Confirme cada item; o que falhar volta para a etapa correspondente.

- Cada dor tem ao menos um número e uma resposta na oportunidade.
- Cada objetivo tem verbo, métrica e meta com número e prazo.
- Requisitos não funcionais incluem performance e disponibilidade com número, mesmo como hipótese.
- Cada RF tem descrição, Capacidades com número, Experiência em passos e prioridade; Tratamento de erros nos críticos; Escopo mínimo só onde há prioridades misturadas, e Adições só onde há Escopo mínimo.
- Cada RF tem histórias na seção 5 e critérios na seção 9.
- Todo Consome fecha com um Fornece que nomeia o consumidor, e vice-versa; todo campo do Consome está no Fornece.
- Depende de contém todo Consome; nenhum RF 1 depende de RF 3; não há ciclo; não há aresta transitiva sem Consome que a justifique.
- Tabela em ordem topológica com desempate pelo menor ID; ondas calculadas da tabela; caminho crítico com o número certo de ondas; Mermaid com exatamente as arestas da tabela.
- Fundação listada na ordem da tabela, com a nota nas ondas; sem fundação, sem nota.
- Cada Consome tem ao menos um critério de integração citando os dois RFs.
- Nenhum item fora de escopo contradiz um requisito ou objetivo.
- Nada no PRD cita linguagem, framework, banco, protocolo ou hospedagem, salvo integração obrigatória descrita pelo que faz.
- Toda hipótese está marcada com `(hipótese)`.
- Nenhum travessão "—" no texto.
