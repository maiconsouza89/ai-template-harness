# Entrevista docs-init: marketplace de mídia em telas

Data: 2026-10-21. Entrevistado: Maicon Souza. Formato: uma pergunta por vez, com alternativas e uma
recomendada. Objetivo declarado pelo usuário: testar a skill docs-init com um produto real,
gerando a documentação neste repositório, na branch `feat/docs-prd-rastreavel`.

Nome do produto: [A CONFIRMAR: qual é o nome do produto?]. Nome de trabalho nos documentos:
"Marketplace de Telas".

## Contexto do repositório

- O repositório é o `ai-template-harness`, template agnóstico de stack. Não há código do produto:
  nenhum manifesto, nenhuma entidade, nenhuma integração existente.
- `docs/` tinha só `README.md` (convenções) e `adr/` com os ADRs 0001 a 0009 do próprio template.
  Os ADRs do produto entram a partir do 0010, no mesmo índice.
- Tudo abaixo vem da entrevista. Nada foi inferido do código.

## Produto

Descrição literal do usuário:

> Um marketplace de mídia digital em telas de estabelecimentos comerciais.
> De um lado, donos de bares, academias, clínicas e lojas com TVs ociosas.
> Do outro, negócios locais que querem anunciar perto de quem compra.
> O exibidor cadastra o local e as telas; o anunciante cria a campanha com um criativo.
> O anunciante paga via Pix, a plataforma retém 30% e repassa 70% ao exibidor.
> O repasse é proporcional ao que foi exibido de verdade, não ao que foi prometido.
> Uma conta só serve para anunciar e para exibir, para fortalecer a rede.
> Visão de longo prazo: um mapa de locais com telas, no espírito do PlugShare,
> com avaliações, fotos e check-ins

### Problema

- Aceito: as duas dores, sem número.
  - Exibidor: tem TV ligada ou ociosa no local sem gerar receita.
    [A CONFIRMAR: quantas TVs ociosas ou quanto o exibidor deixa de ganhar por mês?]
  - Anunciante local: não tem mídia acessível perto de quem compra.
    [A CONFIRMAR: quanto o anunciante local gasta hoje com mídia e com qual retorno?]
- Como o problema é resolvido hoje: [A CONFIRMAR: o que exibidor e anunciante usam hoje no lugar do produto?]

### Usuários e papéis

- Exibidor: dono de bar, academia, clínica ou loja com TV. É o lado principal, o primeiro a atrair
  ("sem telas não há o que vender").
- Anunciante: negócio local que quer anunciar perto de quem compra.
- Exibidor e anunciante usam a mesma conta (conta única).
- Admin da plataforma: papel interno, modera criativos e trata exceções de pagamento e repasse.
- Frequentador (só no RF-011, visão): pessoa que avalia locais e faz check-in.

### Estágio

Ideia, rumo ao MVP. Nada construído.

### Objetivos (aceitos com metas em lacuna)

1. Ativar telas: N telas exibindo em X meses. [A CONFIRMAR: quantas telas e em quanto tempo?]
2. Vender campanhas: N campanhas pagas via Pix em X meses. [A CONFIRMAR: quantas campanhas e em quanto tempo?]
3. Repassar pela exibição real: 100% dos repasses calculados por exibição comprovada, pagos até
   D+N. O 100% é regra de negócio dita pelo usuário. [A CONFIRMAR: prazo do repasse; a hipótese do RF-009 é D+2 úteis após o fechamento semanal]

Métricas de sucesso: as mesmas dos objetivos (pergunta separada pulada porque os objetivos já
trazem a métrica).

### Requisitos não funcionais (aceitos com lacunas)

- Desempenho: tempo de resposta da web. [A CONFIRMAR: quantos segundos o usuário tolera esperar?]
- Disponibilidade do player na TV: decidido no RF-007 que o player exibe a partir de cache
  offline quando a internet cai.
- Disponibilidade da plataforma: [A CONFIRMAR: qual % ou janela de indisponibilidade é aceitável?]
- Acesso: cada conta vê só os seus locais, telas, campanhas e repasses; o admin vê tudo.
- Dispositivos: web responsiva para conta e admin; player na TV.
  [A CONFIRMAR: o player roda em Android TV, Smart TV ou navegador?] (o usuário respondeu "não sei ainda")
- Idioma: pt-BR.
- Norma: LGPD (dados pessoais, CPF/CNPJ e chave Pix). Conteúdo exibido em local público.
  [A CONFIRMAR: quais conteúdos são vetados?]

### Restrições

- Pagamento só via Pix.
- Prazo: [A CONFIRMAR: há prazo para o MVP?]
- Orçamento: [A CONFIRMAR: há orçamento definido?]

### Fora de escopo (aceito)

- Pagamento: cartão, boleto e parcelamento (só Pix). Nota fiscal automática.
  [A CONFIRMAR: quem emite a nota fiscal dos 30% da plataforma?]
- Plataforma: app nativo iOS/Android para a conta (web responsiva basta). Hardware próprio (usa a
  TV do exibidor).
- Produto: leilão ou preço dinâmico por tela; segmentação por público (só por local); medição de
  audiência por câmera ou sensor; criativo em vídeo com som. [A CONFIRMAR: vídeo mudo entra no MVP?]
- Integrações: redes de DOOH e agências externas.

## Requisitos

Lista aceita: 11 RFs propostos, mais o RF-012 criado na rodada de contratos para quebrar um ciclo.
Números marcados `(hipótese)` foram propostos pelo entrevistador e aceitos pelo usuário.

### RF-001 Acessar a conta

- Descrição: a pessoa cria uma conta única que serve para anunciar e para exibir.
- Capacidades:
  1. Cadastro: nome, e-mail e senha. Sem CPF/CNPJ no cadastro (ajuste do usuário): o documento é
     pedido no primeiro pagamento (RF-006) e no primeiro repasse (RF-009).
  2. Senha com no mínimo 8 caracteres (hipótese).
  3. Confirmação de e-mail por link válido por 24 h (hipótese).
  4. Recuperação de senha por link válido por 1 h (hipótese).
  5. A mesma conta acessa as áreas Anunciar e Exibir sem novo cadastro.
  6. Papel admin só é atribuído por outro admin.
  7. Bloqueio por 15 min após 5 senhas erradas (hipótese).
- Experiência: cadastro > e-mail de confirmação > login > painel com abas Anunciar e Exibir.
- Erros: e-mail já usado; link expirado (oferece reenviar); senha errada; conta bloqueada (mostra
  a hora de liberação).
- Prioridade: 1.
- Histórias:
  - Como dono de bar, quero me cadastrar uma vez para exibir e também anunciar meu bar.
  - Como anunciante, quero recuperar a senha para voltar à minha campanha.
  - Como admin, quero promover outro admin para dividir a moderação.

### RF-002 Cadastrar local e telas

- Descrição: o exibidor cadastra seus locais e as telas de cada local.
- Ajuste do usuário: "integrar com a API Places do google para facilitar o cadastro, trazendo os
  dados pré preenchidos". O exibidor busca o estabelecimento e o formulário vem preenchido (nome,
  endereço, coordenadas, categoria, horário, foto); ele edita o que quiser. Se o local não for
  encontrado, o cadastro é manual.
- Ajuste do usuário na rodada do RF-004: o preço por inserção é definido pelo exibidor, por tela,
  com piso da plataforma. [A CONFIRMAR: qual é o valor do piso por inserção?]
- Capacidades:
  1. Local: nome, categoria (bar, academia, clínica, loja, outro), endereço com CEP,
     latitude/longitude, horário de funcionamento, foto. Pré-preenchidos pela Google Places API.
  2. Fluxo médio de pessoas por dia, declarado pelo exibidor. [A CONFIRMAR: o fluxo é obrigatório?]
  3. Tela: nome, posição no local, orientação (horizontal/vertical), horário em que fica ligada,
     preço por inserção definido pelo exibidor, não abaixo do piso da plataforma.
  4. Até 10 telas por local (hipótese).
  5. O local só aparece para anunciantes com ao menos 1 tela pareada (RF-003) e ativa.
  6. O exibidor pode pausar tela ou local; a pausa não cancela campanhas já pagas.
     [A CONFIRMAR: o que acontece com as campanhas pagas de uma tela pausada?]
- Experiência: aba Exibir > Novo local > busca do estabelecimento (Places) ou endereço por CEP >
  confirma o pino no mapa > horário > Adicionar tela > pareamento (RF-003).
- Prioridade: 1.
- Histórias:
  - Como dona de academia, quero cadastrar 3 TVs para vender espaço em todas.
  - Como exibidor, quero pausar uma tela em manutenção para não ser cobrado por falha.

### RF-003 Parear tela com o player

- Descrição: o exibidor liga o player na TV e o vincula a uma tela cadastrada.
- Ajuste do usuário: "adicionar opção de também fazer a leitura de QRCode para fazer o
  pareamento, pois na maioria dos casos o exibidor estará conectado pelo celular". O player mostra
  QR Code e código ao mesmo tempo.
- Capacidades:
  1. Player: [A CONFIRMAR: app Android TV, app Smart TV ou página no navegador da TV?]
  2. Ao abrir sem vínculo, o player mostra um QR Code e um código de 6 caracteres (hipótese).
  3. QR e código expiram em 10 min (hipótese).
  4. O exibidor lê o QR no celular já logado, ou digita o código na tela cadastrada (RF-002), e o
     player passa a exibir a programação dela.
  5. Uma tela tem no máximo 1 player ativo; parear outro desvincula o anterior.
  6. Status da tela: online se o player deu sinal nos últimos 5 min (hipótese), senão offline.
- Erros: código ou QR expirado (o player gera outro); código inexistente; tela já pareada (pede
  confirmação para substituir).
- Prioridade: 1.
- Histórias:
  - Como dono de bar, quero parear minha TV lendo um QR Code no celular para começar a ganhar.
  - Como exibidor, quero ver se a tela está online para saber se estou exibindo.

### RF-004 Criar campanha com criativo

- Descrição: o anunciante monta a campanha escolhendo criativo, telas e período, e vê o preço
  antes de enviar.
- Ajustes do usuário: preço definido pelo exibidor (ver RF-002); "criativo pode ser em forma
  paisagem ou retrato" (o anunciante envia uma versão paisagem, uma retrato ou as duas; cada uma
  vai só para telas da mesma orientação).
- Capacidades:
  1. Criativo: imagem JPG ou PNG, 1920x1080 (paisagem) ou 1080x1920 (retrato), até 5 MB
     (hipótese). [A CONFIRMAR: vídeo mudo entra no MVP?]
  2. Inserção = 15 s na tela (hipótese).
  3. Busca de telas por endereço e raio de até 5 km (hipótese), com filtro por categoria.
  4. Período: data de início e fim, de 7 a 90 dias (hipótese); início no mínimo 2 dias após o
     envio (hipótese), para caber a moderação.
  5. Frequência: 4 inserções por hora ligada, por tela (hipótese).
  6. Preço = soma, por tela, de inserções previstas x preço por inserção definido pelo exibidor.
     O preço da tela fica gravado na campanha no momento da compra.
  7. Cada versão do criativo vai só para telas com a mesma orientação.
- Estados: rascunho > em moderação (RF-005) > aguardando pagamento (RF-006) > agendada > em
  exibição > encerrada. Paga depois de aprovada, para não haver estorno por reprovação.
- Prioridade: 1.
- Histórias:
  - Como dona de padaria, quero anunciar nas academias a 2 km para atingir o bairro.
  - Como anunciante, quero ver o preço antes de enviar para caber no orçamento.

### RF-005 Moderar criativo

- Descrição: o admin aprova ou reprova cada criativo antes de a campanha ir a pagamento.
- Capacidades:
  1. Fila de criativos em moderação, mais antigo primeiro.
  2. Decisão em até 24 h úteis (hipótese).
  3. Reprovação exige motivo de uma lista, mais texto livre opcional.
     [A CONFIRMAR: quais são as regras de conteúdo vetado?]
  4. O anunciante é avisado por e-mail e no painel; pode trocar o criativo e reenviar.
  5. Aprovada, a campanha vai para aguardando pagamento (RF-006).
  6. O exibidor pode bloquear categorias de anunciante nas suas telas.
     [A CONFIRMAR: o bloqueio de categorias pelo exibidor entra no MVP?]
- Erros: criativo reprovado 3 vezes seguidas (hipótese) na mesma campanha vai para revisão manual
  da conta.
- Prioridade: 1.
- Histórias:
  - Como admin, quero reprovar um criativo com motivo para o anunciante corrigir.
  - Como dono de clínica, quero a garantia de que nada impróprio passa na minha TV.
- Nota do usuário: "futuramente haverá moderação por sistema de IA" (vai para o Depois do roadmap).

### RF-006 Pagar campanha via Pix

- Descrição: o anunciante paga a campanha aprovada por Pix e ela fica agendada.
- As capacidades de crédito (6 e 7 da proposta original) foram movidas para o RF-012 na rodada de
  contratos.
- Capacidades:
  1. CPF ou CNPJ pedido no primeiro pagamento (saiu do cadastro, RF-001).
  2. Cobrança Pix com QR Code e copia e cola, válida por 30 min (hipótese).
  3. Confirmação automática pelo provedor. [A CONFIRMAR: qual PSP ou banco processa o Pix?]
  4. A plataforma recebe 100% e guarda a parte do exibidor até o repasse (RF-009).
  5. Sem pagamento até 24 h antes do início (hipótese), a campanha volta a rascunho.
- Erros: QR expirado (gera outro); pagamento em duplicidade (estorno Pix automático); valor
  divergente (vai para o admin); provedor fora do ar (mantém a campanha como está e avisa).
- Prioridade: 1.
- Histórias:
  - Como anunciante, quero pagar por Pix no celular para a campanha começar logo.
- Observação aceita: a plataforma retém e repassa dinheiro de terceiros.
  [A CONFIRMAR: reter e repassar exige split do PSP ou licença de subcredenciador?]

### RF-007 Exibir campanha na tela

- Descrição: o player exibe nas telas pareadas as campanhas agendadas para elas.
- Capacidades:
  1. O player busca a programação a cada 15 min (hipótese) e baixa os criativos novos.
  2. Programação e criativos das próximas 24 h (hipótese) ficam em cache local.
  3. Sem internet, segue exibindo o cache.
  4. Inserções distribuídas igualmente na hora, alternando campanhas.
  5. Sem campanha no horário, exibe conteúdo padrão.
     [A CONFIRMAR: o conteúdo padrão é anúncio da plataforma, do exibidor ou tela preta?]
  6. Respeita o horário ligado da tela (RF-002) e a pausa do exibidor.
- Erros: criativo corrompido no download (baixa de novo, não exibe o quebrado); cache vencido sem
  internet (exibe padrão e marca a tela offline).
- Prioridade: 1.
- Histórias:
  - Como exibidor, quero que a TV continue exibindo se o wi-fi cair para não perder repasse.
  - Como anunciante, quero que meu anúncio passe na frequência que comprei.

### RF-008 Registrar exibições comprovadas

- Descrição: o player registra cada inserção exibida e a plataforma valida o que conta para
  repasse e relatório.
- Capacidades:
  1. Registro por inserção: tela, campanha, criativo, início, duração, id do player.
  2. Registro assinado pelo player, para não ser forjado fora dele.
  3. Envio em lote a cada 15 min (hipótese); sem internet, guarda até 7 dias (hipótese).
  4. Conta como comprovada só se: duração completa (15 s), dentro do período da campanha e do
     horário ligado da tela, sem duplicidade.
  5. Registro que chega após 7 dias é descartado (hipótese).
  6. O admin vê os registros rejeitados e o motivo.
- Erros: lote com assinatura inválida (rejeita e alerta o admin); relógio do player errado (usa a
  hora do servidor no envio); inserções acima do contratado (não contam).
- [A CONFIRMAR: como provar que a TV estava ligada, e não só o player?]
- Prioridade: 1.
- Histórias:
  - Como exibidor, quero que cada inserção exibida conte para receber o justo.
  - Como anunciante, quero pagar só pelo que passou de verdade.

### RF-009 Repassar 70% ao exibidor pelo exibido

- Descrição: a plataforma calcula quanto cada exibidor ganhou pelas inserções comprovadas e paga
  70% por Pix.
- Capacidades:
  1. Valor por inserção comprovada (RF-008) = preço da tela gravado na campanha no momento da
     compra (RF-004).
  2. O exibidor recebe 70%; a plataforma retém 30%.
  3. Fechamento semanal, de segunda 00h a domingo 23h59 (hipótese).
  4. Pagamento por Pix até D+2 úteis após o fechamento (hipótese).
  5. Pede CPF/CNPJ e chave Pix do mesmo titular no primeiro repasse (saiu do RF-001).
  6. Saldo abaixo de R$ 20 (hipótese) acumula para a semana seguinte.
  7. Extrato por tela e campanha: inserções comprovadas, rejeitadas e valor.
- Erros: chave Pix inválida ou de outro titular (retém e avisa); Pix recusado pelo banco (tenta 3
  vezes (hipótese), depois vai para o admin); contestação do exibidor (abre caso para o admin com o
  extrato).
- Prioridade: 1.
- Histórias:
  - Como dono de bar, quero receber toda semana no Pix pelo que minha TV exibiu.
  - Como exibidor, quero ver o extrato por tela para entender quanto cada uma rende.
  - Como admin, quero tratar contestações com os registros de exibição em mãos.

### RF-010 Acompanhar resultados da campanha

- Descrição: o anunciante acompanha o que foi exibido da campanha e quanto virou crédito.
- Capacidades:
  1. Painel por campanha: inserções previstas, comprovadas e % entregue.
  2. Quebra por local/tela e por dia.
  3. Atualizado a cada 1 h (hipótese).
  4. Valor consumido e previsão de crédito (não exibido) a cada momento.
  5. Ao encerrar: resumo final e crédito gerado (RF-012).
  6. Exportar relatório em PDF ou CSV.
  7. Alerta por e-mail se uma tela da campanha ficar offline mais de 24 h (hipótese).
- Experiência: aba Anunciar > Minhas campanhas > campanha > gráfico diário, tabela por tela >
  Exportar.
- Prioridade: 2.
- Histórias:
  - Como anunciante, quero ver quantas vezes meu anúncio passou em cada local para decidir onde
    renovar.
  - Como anunciante, quero saber quanto vai virar crédito antes de a campanha acabar.

### RF-011 Explorar mapa de locais

- Descrição: qualquer pessoa explora um mapa dos locais com telas, com avaliações, fotos e
  check-ins. Visão de longo prazo, "no espírito do PlugShare".
- Capacidades:
  1. Mapa com pinos dos locais ativos (RF-002), filtro por categoria.
  2. Ficha do local: fotos, telas, nota média.
  3. Conta logada avalia o local de 1 a 5 com comentário de até 500 caracteres (hipótese).
  4. Check-in no local, só a até 200 m dele (hipótese).
  5. Fotos enviadas pela comunidade passam pela moderação do admin.
  6. [A CONFIRMAR: o mapa é público sem login ou só para contas?]
  7. [A CONFIRMAR: para que serve o check-in: recompensa, prova de audiência ou ranking?]
- Prioridade: 3. Não serve a nenhum objetivo do MVP; aceito como visão.
- Histórias:
  - Como anunciante, quero ver no mapa os locais perto do meu negócio para planejar.
  - Como frequentador, quero avaliar a academia e ver fotos antes de ir.

### RF-012 Gerar e usar crédito do não exibido

- Origem: capacidades 6 e 7 da proposta do RF-006, aceitas pelo usuário ("sobra vira crédito"),
  movidas para um RF próprio na rodada de contratos para quebrar o ciclo RF-006 > RF-007 > RF-008 >
  RF-006.
- Descrição: ao fim da campanha, o valor pago que não foi exibido vira crédito na conta do
  anunciante, usado nos próximos pagamentos.
- Capacidades:
  1. Ao encerrar a campanha, crédito = valor pago - valor das inserções comprovadas.
  2. O crédito fica no saldo da conta.
  3. No pagamento, o crédito cobre a campanha toda ou em parte; o resto vai por Pix (RF-006).
- Prioridade: 1.
- Histórias:
  - Como anunciante, quero que o não exibido volte como crédito para não perder dinheiro.

## Contratos e dependências

Tabela aceita pelo usuário ("Aceitar com RF-012"):

| RF | Consome (de quem) | Depende de |
|---|---|---|
| RF-001 | nada | nenhum (fundação) |
| RF-002 | nada | RF-001 |
| RF-003 | Tela (RF-002) | RF-001, RF-002 |
| RF-004 | Local, Tela com preço (RF-002) | RF-001, RF-002 |
| RF-005 | Campanha (RF-004) | RF-001, RF-004 |
| RF-006 | Campanha com preço (RF-004), Aprovação (RF-005) | RF-001, RF-004, RF-005 |
| RF-007 | Campanha (RF-004), Pagamento (RF-006), Vínculo do player (RF-003), horário e pausa da tela (RF-002) | RF-002, RF-003, RF-004, RF-006 |
| RF-008 | Inserções exibidas (RF-007), chave do player (RF-003), Campanha (RF-004) | RF-003, RF-004, RF-007 |
| RF-009 | Exibição comprovada (RF-008), Pagamento (RF-006), preço gravado (RF-004) | RF-001, RF-004, RF-006, RF-008 |
| RF-010 | Exibição comprovada (RF-008), Campanha (RF-004), Crédito (RF-012) | RF-004, RF-008, RF-012 |
| RF-011 | Local (RF-002) | RF-001, RF-002 |
| RF-012 | Pagamento (RF-006), Exibição comprovada (RF-008) | RF-006, RF-008 |

Fornece (derivado da tabela; campos a detalhar pelo prd-writer a partir das capacidades):

- RF-002 fornece Local (id, nome, categoria, coordenadas, horário) e Tela (id, local, orientação,
  horário ligada, preço por inserção, status ativa ou pausada) para RF-003, RF-004, RF-007, RF-011.
- RF-003 fornece Vínculo do player (player, tela, chave de assinatura, status online) para RF-007,
  RF-008.
- RF-004 fornece Campanha (id, anunciante, criativos por orientação, telas, preço por inserção
  gravado por tela, período, frequência, preço total, estado) para RF-005, RF-006, RF-007, RF-008,
  RF-009, RF-010.
- RF-005 fornece Aprovação (campanha, decisão, motivo) para RF-006.
- RF-006 fornece Pagamento (campanha, valor pago, data, estado) para RF-007, RF-009, RF-012.
- RF-007 fornece Inserções exibidas (tela, campanha, criativo, início, duração, player) para RF-008.
- RF-008 fornece Exibição comprovada (tela, campanha, início, duração, status comprovada ou
  rejeitada, motivo) para RF-009, RF-010, RF-012.
- RF-012 fornece Crédito (conta, saldo, campanha de origem, valor) para RF-010.

Ondas calculadas: 1: RF-001 | 2: RF-002 | 3: RF-003, RF-004, RF-011 | 4: RF-005 | 5: RF-006 |
6: RF-007 | 7: RF-008 | 8: RF-009, RF-012 | 9: RF-010.

Fundação: RF-001 (conta única e papéis; todos dependem dele).

Dependências externas:

- Google Places API: busca e pré-preenchimento do local. Trava RF-002.
- PSP Pix: cobrança, confirmação por webhook, estorno e pagamento de repasse.
  [A CONFIRMAR: qual PSP?] Trava RF-006, RF-009, RF-012.
- Serviço de envio de e-mail: confirmação, avisos de moderação e alertas.
  [A CONFIRMAR: qual serviço?] Trava RF-001, RF-005, RF-010.
- Serviço de mapa: pino no cadastro e mapa de locais. Trava RF-002, RF-011.

## Critérios de aceitação

Aceito: o prd-writer deriva de 2 a 4 critérios por RF (sucesso e falha) a partir das capacidades e
dos erros aprovados, mais um critério de integração para cada Consome. Amostra aceita:

- RF-003: QR lido pelo celular logado pareia a tela; código com 11 min é recusado.
- RF-006: Pix pago muda a campanha para agendada em até 1 min (hipótese); QR expirado não confirma.
- RF-008: inserção de 10 s não conta; lote com assinatura inválida é rejeitado.
- Integração RF-005 > RF-006: aprovar o criativo libera a cobrança Pix; reprovado não gera Pix.
- Integração RF-008 > RF-009: 100 inserções comprovadas a R$ 1 geram repasse de R$ 70.
- Integração RF-008 > RF-012: campanha de R$ 100 com R$ 80 comprovados gera R$ 20 de crédito.
- Integração RF-012 > RF-010: o crédito aparece no resumo final da campanha.

## Roadmap

Aceito pelo usuário. Nada em andamento (estágio ideia).

- Agora (ondas 1 a 4, prioridade 1):
  - Base e oferta: RF-001, RF-002, RF-003.
  - Venda: RF-004, RF-005.
- Próximo (ondas 5 a 9):
  - Pagamento e exibição: RF-006, RF-007.
  - Prova e dinheiro: RF-008, RF-009, RF-012.
  - Transparência: RF-010 (prioridade 2).
- Depois:
  - Mapa com avaliações e check-ins: RF-011.
  - Moderação de criativos por IA (sem RF; nota do usuário no RF-005).
- Adiado ou removido: nada.
- Caminho crítico proposto: RF-001 > RF-002 > RF-004 > RF-005 > RF-006 > RF-007 > RF-008 > RF-012 > RF-010.

## Arquitetura

Aceito: monólito modular com player separado.

1. Web (conta e admin): SPA ou SSR responsiva, áreas Anunciar, Exibir e Admin.
2. API/backend em monólito modular, com módulos: contas, locais/telas, campanhas, moderação,
   pagamentos, exibições, repasses/crédito.
3. Player na TV: baixa a programação, cache offline, assina e envia registros de exibição.
   [A CONFIRMAR: plataforma do player] (resposta: "não sei ainda").
4. Jobs agendados: validação de exibições, fechamento semanal de repasse, crédito no fim da
   campanha.
5. Banco relacional (dinheiro e estados).
6. Storage de objetos com CDN para criativos.

Comunicação:

- Web e player para a API por HTTPS (REST).
- PSP Pix para a API por webhook.
- API para Google Places, e-mail e mapa por HTTP.
- Jobs leem o mesmo banco.

Escolhas de stack: nada decidido. [A CONFIRMAR: linguagem, framework, banco, cloud e PSP Pix]

Não perguntado (fica em lacuna): deploy, observabilidade, autenticação técnica, entidades
detalhadas, retenção de dados, pontos frágeis.

## Decisões

Candidatos a ADR. Motivo marcado como "do usuário" quando ele o disse; "proposto e aceito" quando
veio da recomendação do entrevistador e foi escolhido.

1. Conta única para anunciar e exibir. Motivo do usuário: "para fortalecer a rede". Status:
   vigente.
2. Repasse proporcional ao exibido de verdade, 70% ao exibidor e 30% retidos. Motivo do usuário:
   "proporcional ao que foi exibido de verdade, não ao que foi prometido". Alternativas: não
   citadas. Status: vigente.
3. Pré-preencher o cadastro de local com a Google Places API. Motivo do usuário: "facilitar o
   cadastro". Alternativas: não citadas. Status: vigente.
4. Preço por inserção definido pelo exibidor, com piso da plataforma. Motivo: [A CONFIRMAR: por
   que o exibidor define o preço?]. Alternativas descartadas: tabela única definida pela
   plataforma (era a recomendada); pacotes fechados. Status: vigente.
5. Moderação humana do criativo pelo admin, antes do pagamento. Motivo proposto e aceito: o
   conteúdo aparece em local público de terceiros; pagar só depois de aprovar evita estorno.
   Alternativas descartadas: aprovação também pelo exibidor; moderação automática. Evolução
   prevista: moderação por IA. Status: vigente.
6. Valor não exibido vira crédito na conta. Motivo proposto e aceito: fecha a conta com o repasse
   pelo exibido e mantém o dinheiro na rede. Alternativas descartadas: estorno Pix ao fim; cobrar
   só o exibido (Pix comum não tem pré-autorização). Status: vigente.
7. Pareamento do player por QR Code e por código. Motivo do usuário: "na maioria dos casos o
   exibidor estará conectado pelo celular". Status: vigente.
8. Player com cache offline. Motivo proposto e aceito: wi-fi de bar e academia oscila; sem cache o
   exibidor perde receita. Alternativa descartada: só online (streaming). Status: vigente.
9. Prova de exibição por registro assinado do player com regras de validação. Motivo proposto e
   aceito: não exige hardware e é auditável. Alternativas descartadas: foto periódica do exibidor;
   captura de tela por amostragem. Status: vigente, com lacuna sobre provar TV ligada.
10. Repasse semanal. Motivo proposto e aceito: o pequeno exibidor precisa ver o dinheiro cedo para
    confiar. Alternativas descartadas: mensal; ao fim da campanha. Status: vigente.
11. Monólito modular com player separado. Motivo proposto e aceito: time pequeno entrega mais
    rápido no MVP; o player é separado porque roda na TV. Alternativas descartadas:
    microsserviços; backend como serviço (Firebase/Supabase). Status: vigente.
12. Pagamento só via Pix. Motivo: [A CONFIRMAR: por que só Pix?]. Status: vigente (restrição).

## Hipóteses aceitas

Números propostos pelo entrevistador e aceitos:

- RF-001: senha mínima de 8 caracteres; link de confirmação de 24 h; link de recuperação de 1 h;
  bloqueio de 15 min após 5 erros.
- RF-002: até 10 telas por local.
- RF-003: código de 6 caracteres; expiração de 10 min; online se sinal nos últimos 5 min.
- RF-004: imagem até 5 MB; inserção de 15 s; raio de até 5 km; período de 7 a 90 dias; início no
  mínimo 2 dias após o envio; 4 inserções por hora por tela.
- RF-005: decisão em até 24 h úteis; 3 reprovações seguidas levam a revisão manual.
- RF-006: QR válido por 30 min; volta a rascunho sem pagamento até 24 h antes do início;
  confirmação em até 1 min (critério de aceitação).
- RF-007: busca de programação a cada 15 min; cache das próximas 24 h.
- RF-008: envio a cada 15 min; guarda até 7 dias offline; descarte após 7 dias.
- RF-009: fechamento semanal de segunda a domingo; pagamento até D+2 úteis; saldo mínimo de R$ 20;
  3 tentativas de Pix.
- RF-010: atualização a cada 1 h; alerta após 24 h offline.
- RF-011: comentário de até 500 caracteres; check-in a até 200 m.

## Lacunas

- Nome do produto.
- Números das dores (exibidor e anunciante) e como o problema é resolvido hoje.
- Metas e prazos dos objetivos 1, 2 e 3.
- RNFs: tempo de resposta tolerado; disponibilidade da plataforma; plataforma do player.
- Prazo e orçamento do MVP.
- Quem emite a nota fiscal dos 30%.
- Vídeo mudo no MVP.
- Fluxo de pessoas obrigatório no cadastro do local.
- Destino das campanhas pagas de uma tela pausada.
- Valor do piso de preço por inserção e motivo do preço pelo exibidor.
- Regras de conteúdo vetado; bloqueio de categorias pelo exibidor no MVP.
- PSP Pix; exigência de split ou licença de subcredenciador.
- Conteúdo padrão quando não há campanha.
- Como provar que a TV estava ligada.
- Mapa público ou só para contas; finalidade do check-in.
- Serviço de e-mail.
- Stack: linguagem, framework, banco, cloud.
- Deploy, observabilidade, retenção de dados e LGPD em detalhe.
- Motivo de aceitar só Pix.
