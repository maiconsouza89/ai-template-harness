---
title: Marketplace de Telas
type: prd
status: draft
date: 2026-10-21
owners: [Maicon Souza]
related: ["../architecture/hld-visao-geral.md", "roadmap.md"]
---

# PRD: Marketplace de Telas

Nome do produto: [A CONFIRMAR: qual é o nome do produto?]. "Marketplace de Telas" é o nome de trabalho.

## 1. Resumo executivo

O Marketplace de Telas é um marketplace de mídia digital em telas de estabelecimentos comerciais. De um lado estão donos de bares, academias, clínicas e lojas com TVs ociosas, os exibidores. Do outro estão negócios locais que querem anunciar perto de quem compra, os anunciantes.

O exibidor cadastra o local e as telas e pareia o player na TV. O anunciante monta uma campanha com um criativo, escolhe as telas e o período e paga via Pix. A plataforma retém 30% e repassa 70% ao exibidor. O repasse é proporcional ao que foi exibido de verdade, não ao que foi prometido: o que não foi exibido volta ao anunciante como crédito.

Uma conta única serve para anunciar e para exibir, para fortalecer a rede. A visão de longo prazo é um mapa de locais com telas, no espírito do PlugShare, com avaliações, fotos e check-ins. O produto está no estágio de ideia, rumo ao MVP.

## 2. Problema e oportunidade

### O problema

**Exibidor sem receita da TV**
- Tem TV ligada ou ociosa no local sem gerar receita. [A CONFIRMAR: quantas TVs ociosas ou quanto o exibidor deixa de ganhar por mês?]
- O que o exibidor usa hoje no lugar do produto: [A CONFIRMAR: o que exibidor e anunciante usam hoje no lugar do produto?]

**Anunciante local sem mídia acessível**
- Não tem mídia acessível perto de quem compra. [A CONFIRMAR: quanto o anunciante local gasta hoje com mídia e com qual retorno?]

### A oportunidade

- **Exibidor sem receita da TV.** O produto transforma a TV ociosa em receita, com repasse semanal proporcional ao que foi exibido de verdade.
- **Anunciante local sem mídia acessível.** O produto oferece telas perto do cliente, com preço visível antes de enviar a campanha, pagamento por Pix e relatório do que foi exibido.

## 3. Público-alvo

### Usuários primários

**Exibidor**
- Dono de bar, academia, clínica ou loja com TV.
- É o lado principal e o primeiro a atrair: sem telas não há o que vender.
- Quer receber pelo que sua TV exibiu e ter garantia de que nada impróprio passa nela.

**Anunciante**
- Negócio local que quer anunciar perto de quem compra.
- Quer ver o preço antes de enviar, pagar por Pix e saber o que foi exibido.

**Admin da plataforma**
- Papel interno.
- Modera criativos e trata exceções de pagamento e repasse.

**Frequentador (só no RF-011, visão de longo prazo)**
- Pessoa que avalia locais e faz check-in.
- Quer ver fotos e notas de um local antes de ir.
- Não anuncia nem exibe: usa só o mapa.

### Perfil comportamental

- Exibidor e anunciante usam a mesma conta. A pessoa alterna entre as áreas Anunciar e Exibir.
- Exibidor e anunciante acessam principalmente pelo celular.

## 4. Objetivos e métricas

### Objetivos de produto

| Objetivo | Métrica | Meta |
| --- | --- | --- |
| **Ativar** telas | Telas exibindo | [A CONFIRMAR: quantas telas e em quanto tempo?] |
| **Vender** campanhas | Campanhas pagas via Pix | [A CONFIRMAR: quantas campanhas e em quanto tempo?] |
| **Repassar** pela exibição real | Repasses calculados por exibição comprovada | 100% dos repasses por exibição comprovada; prazo de pagamento [A CONFIRMAR: qual o prazo do repasse em dias após o fechamento?] |

### Requisitos não funcionais

Performance
- Tempo de resposta da web: [A CONFIRMAR: quantos segundos o usuário tolera esperar?]
- O player da TV segue exibindo a programação em cache quando a internet cai (RF-007).

Disponibilidade
- Disponibilidade da plataforma: [A CONFIRMAR: qual % ou janela de indisponibilidade é aceitável?]

Segurança e autorização
- Cada conta vê só os seus locais, telas, campanhas e repasses. O admin vê tudo.
- Papel admin só é atribuído por outro admin.
- Registros de exibição são assinados pelo player (RF-008).

Compatibilidade
- Web responsiva para conta e admin, em pt-BR.
- Player na TV: [A CONFIRMAR: o player roda em Android TV, Smart TV ou navegador?]

Compliance
- Dados pessoais, CPF/CNPJ e chave Pix tratados conforme a LGPD. Detalhes de retenção e exclusão: [A CONFIRMAR: qual o prazo de retenção e de exclusão sob pedido?]
- O conteúdo é exibido em local público. [A CONFIRMAR: quais conteúdos são vetados?]

Acessibilidade
- [A CONFIRMAR: há requisito de acessibilidade para a web?]

## 5. Histórias de usuário

### RF-001 Acessar a conta
- Como dono de bar, quero me cadastrar uma vez para exibir e também anunciar meu bar
- Como anunciante, quero recuperar a senha para voltar à minha campanha
- Como admin, quero promover outro admin para dividir a moderação

### RF-002 Cadastrar local e telas
- Como dona de academia, quero cadastrar 3 TVs para vender espaço em todas
- Como exibidor, quero pausar uma tela em manutenção para não ser cobrado por falha
- Como exibidor, quero buscar meu estabelecimento e receber o formulário preenchido para cadastrar mais rápido

### RF-003 Parear tela com o player
- Como dono de bar, quero parear minha TV lendo um QR Code no celular para começar a ganhar
- Como exibidor, quero ver se a tela está online para saber se estou exibindo

### RF-004 Criar campanha com criativo
- Como dona de padaria, quero anunciar nas academias a 2 km para atingir o bairro
- Como anunciante, quero ver o preço antes de enviar para caber no orçamento

### RF-005 Moderar criativo
- Como admin, quero reprovar um criativo com motivo para o anunciante corrigir
- Como dono de clínica, quero a garantia de que nada impróprio passa na minha TV

### RF-006 Pagar campanha via Pix
- Como anunciante, quero pagar por Pix no celular para a campanha começar logo

### RF-007 Exibir campanha na tela
- Como exibidor, quero que a TV continue exibindo se o wi-fi cair para não perder repasse
- Como anunciante, quero que meu anúncio passe na frequência que comprei

### RF-008 Registrar exibições comprovadas
- Como exibidor, quero que cada inserção exibida conte para receber o justo
- Como anunciante, quero pagar só pelo que passou de verdade

### RF-009 Repassar 70% ao exibidor pelo exibido
- Como dono de bar, quero receber toda semana no Pix pelo que minha TV exibiu
- Como exibidor, quero ver o extrato por tela para entender quanto cada uma rende
- Como admin, quero tratar contestações com os registros de exibição em mãos

### RF-010 Acompanhar resultados da campanha
- Como anunciante, quero ver quantas vezes meu anúncio passou em cada local para decidir onde renovar
- Como anunciante, quero saber quanto vai virar crédito antes de a campanha acabar

### RF-011 Explorar mapa de locais
- Como anunciante, quero ver no mapa os locais perto do meu negócio para planejar
- Como frequentador, quero avaliar a academia e ver fotos antes de ir

### RF-012 Gerar e usar crédito do não exibido
- Como anunciante, quero que o não exibido volte como crédito para não perder dinheiro
- Como o sistema, quero gerar o crédito ao encerrar a campanha para que o anunciante o use nos próximos pagamentos

## 6. Requisitos funcionais

### RF-001 Acessar a conta
A pessoa cria uma conta única que serve para anunciar e para exibir.

**Fornece:**
- Conta: identificador, nome, e-mail e papel (usuário ou admin), com as áreas Anunciar e Exibir disponíveis na mesma conta (usado por RF-002)

**Capacidades:**
- Cadastro com nome, e-mail e senha. O CPF/CNPJ não é pedido no cadastro: é pedido no primeiro pagamento (RF-006) e no primeiro repasse (RF-009).
- Senha com no mínimo 8 caracteres (hipótese)
- Link de confirmação de e-mail válido por 24 h e link de recuperação de senha válido por 1 h (hipótese)
- Bloqueio da conta por 15 min após 5 senhas erradas (hipótese)
- A mesma conta acessa as áreas Anunciar e Exibir sem novo cadastro.
- Papel admin só é atribuído por outro admin.

**Experiência:**
- Cadastro: a pessoa informa nome, e-mail e senha. O sistema valida o formato do e-mail e o tamanho da senha na hora, mostra a mensagem abaixo do campo e envia o e-mail de confirmação.
- Confirmação: ao abrir o link, a pessoa vê "E-mail confirmado" e segue para o login.
- Login: e-mail e senha levam ao painel com as abas Anunciar e Exibir. Em conta nova, cada aba mostra o estado vazio com a primeira ação (criar campanha ou cadastrar local).
- Recuperação: a pessoa informa o e-mail e recebe o link. Ao definir a nova senha, vê "Senha alterada" e entra no login.
- Admin: o admin promove outra conta pelo e-mail dela e vê a confirmação da alteração.

**Tratamento de erros:**
- E-mail já usado: "Este e-mail já tem conta. Entre ou recupere a senha." Nenhuma conta nova é criada.
- Link expirado: "Este link expirou." com o botão "Enviar novo link".
- Senha errada: "E-mail ou senha incorretos." sem revelar qual dos dois falhou.
- Conta bloqueada: "Conta bloqueada até <hora>. Tente de novo depois desse horário."

### RF-002 Cadastrar local e telas
O exibidor cadastra seus locais e as telas de cada local, com o formulário pré-preenchido pela busca do estabelecimento.

**Consome:**
- RF-001: conta com identificador e papel, para vincular o local ao exibidor

**Fornece:**
- Local: identificador, nome, categoria, coordenadas e horário de funcionamento (usado por RF-003, RF-004, RF-007, RF-011)
- Tela: identificador, local, orientação, horário em que fica ligada, preço por inserção e status (ativa ou pausada) (usado por RF-003, RF-004, RF-007, RF-011)

**Capacidades:**
- Local com nome, categoria (bar, academia, clínica, loja ou outro), endereço com CEP, latitude e longitude, horário de funcionamento e foto. A busca do estabelecimento na Google Places API pré-preenche os campos e o exibidor edita o que quiser.
- Se o estabelecimento não é encontrado, o cadastro é manual.
- Fluxo médio de pessoas por dia, declarado pelo exibidor. [A CONFIRMAR: o fluxo de pessoas é obrigatório no cadastro do local?]
- Tela com nome, posição no local, orientação (horizontal ou vertical), horário em que fica ligada e preço por inserção definido pelo exibidor.
- O preço por inserção não pode ficar abaixo do piso da plataforma. [A CONFIRMAR: qual é o valor do piso por inserção?]
- Até 10 telas por local (hipótese)
- O local só aparece para anunciantes com ao menos 1 tela pareada (RF-003) e ativa.
- O exibidor pode pausar uma tela ou um local. A pausa não cancela campanhas já pagas. [A CONFIRMAR: o que acontece com as campanhas pagas de uma tela pausada?]

**Experiência:**
- Na aba Exibir, o exibidor clica em "Novo local".
- Busca o estabelecimento pelo nome (Places) ou informa o endereço por CEP. O formulário vem preenchido com nome, endereço, coordenadas, categoria, horário e foto.
- Confirma o pino no mapa e ajusta o horário de funcionamento.
- Clica em "Adicionar tela" e informa nome, posição, orientação, horário ligada e preço por inserção. Abaixo do piso, o campo mostra "O preço mínimo é <piso> por inserção."
- Ao salvar, vê "Tela cadastrada" e segue para o pareamento (RF-003).
- Estado vazio: sem locais, a aba mostra "Cadastre seu primeiro local" com o botão "Novo local".
- Pausar: cada tela e cada local têm a ação "Pausar" e a ação "Retomar", com a confirmação do efeito.

### RF-003 Parear tela com o player
O exibidor liga o player na TV e o vincula a uma tela cadastrada, por QR Code ou por código.

**Consome:**
- RF-002: tela com identificador, local e status

**Fornece:**
- Vínculo do player: player, tela, chave de assinatura e status online ou offline (usado por RF-007, RF-008)

**Capacidades:**
- Plataforma do player. [A CONFIRMAR: o player é app Android TV, app Smart TV ou página no navegador da TV?]
- Ao abrir sem vínculo, o player mostra ao mesmo tempo um QR Code e um código de 6 caracteres (hipótese)
- O QR Code e o código expiram em 10 min (hipótese)
- A tela fica online se o player deu sinal nos últimos 5 min (hipótese)
- O exibidor lê o QR no celular já logado, ou digita o código na tela cadastrada (RF-002). O player passa a exibir a programação dela.
- Uma tela tem no máximo 1 player ativo. Parear outro desvincula o anterior.

**Experiência:**
- A TV abre o player e mostra "Para parear, leia o QR Code ou digite o código <código> na sua conta".
- No celular, o exibidor logado lê o QR e escolhe a tela, ou abre a tela cadastrada e digita o código.
- O player troca para "Tela pareada" e começa a exibir a programação.
- Na lista de telas, cada tela mostra o status online ou offline.
- Tela com player já ativo: o sistema pede confirmação para substituir.

**Tratamento de erros:**
- Código ou QR expirado: o app mostra "Código expirado" e o player gera outro automaticamente.
- Código inexistente: "Código não encontrado. Confira o código na TV."
- Tela já pareada: "Esta tela já tem um player. Deseja substituir?" O vínculo antigo só é desfeito se o exibidor confirmar.

### RF-004 Criar campanha com criativo
O anunciante monta a campanha escolhendo criativo, telas e período, e vê o preço antes de enviar.

**Consome:**
- RF-002: local com nome, categoria, coordenadas e horário; tela com orientação, horário ligada, preço por inserção e status

**Fornece:**
- Campanha: identificador, anunciante, criativos por orientação, telas, preço por inserção gravado por tela, período, frequência, preço total e estado (usado por RF-005, RF-006, RF-007, RF-008, RF-009, RF-010)

**Capacidades:**
- Criativo em imagem JPG ou PNG, de 1920x1080 (paisagem) ou 1080x1920 (retrato), até 5 MB (hipótese)
- O anunciante envia uma versão paisagem, uma retrato ou as duas. Cada versão vai só para telas da mesma orientação.
- Vídeo mudo. [A CONFIRMAR: vídeo mudo entra no MVP?]
- Cada inserção dura 15 s na tela (hipótese)
- Busca de telas por endereço e raio de até 5 km, com filtro por categoria (hipótese)
- Período com data de início e fim, de 7 a 90 dias (hipótese)
- O início deve ser no mínimo 2 dias depois do envio, para caber a moderação (hipótese)
- Frequência de 4 inserções por hora ligada, por tela (hipótese)
- Preço = soma, por tela, das inserções previstas vezes o preço por inserção definido pelo exibidor. O preço de cada tela fica gravado na campanha no momento da compra.
- Estados da campanha: rascunho, em moderação (RF-005), aguardando pagamento (RF-006), agendada, em exibição e encerrada. O pagamento vem depois da aprovação, para não haver estorno por reprovação.

**Experiência:**
- Na aba Anunciar, o anunciante clica em "Nova campanha".
- Envia o criativo. O sistema valida formato, dimensões e tamanho e mostra a prévia na orientação enviada.
- Busca telas por endereço e raio, filtra por categoria e marca as telas desejadas. Telas de orientação sem criativo ficam desabilitadas com o aviso "Envie a versão <orientação> para usar esta tela".
- Escolhe início e fim. Datas fora do limite mostram "Escolha um período de 7 a 90 dias, começando daqui a 2 dias ou mais."
- O preço total aparece e se atualiza a cada mudança, com a quebra por tela.
- Ao clicar em "Enviar para moderação", a campanha muda para em moderação.
- Estado vazio: sem campanhas, a aba mostra "Crie sua primeira campanha".

### RF-005 Moderar criativo
O admin aprova ou reprova cada criativo antes de a campanha ir a pagamento.

**Consome:**
- RF-004: campanha com identificador, anunciante, criativos por orientação e estado

**Fornece:**
- Aprovação: campanha, decisão (aprovada ou reprovada) e motivo (usado por RF-006)

**Capacidades:**
- Fila de criativos em moderação, do mais antigo para o mais novo.
- Decisão em até 24 h úteis (hipótese)
- Reprovação exige motivo de uma lista, mais texto livre opcional. [A CONFIRMAR: quais são as regras de conteúdo vetado?]
- O anunciante é avisado por e-mail e no painel. Pode trocar o criativo e reenviar.
- Criativo reprovado 3 vezes seguidas na mesma campanha vai para revisão manual da conta (hipótese)
- Aprovada, a campanha vai para aguardando pagamento (RF-006).
- O exibidor pode bloquear categorias de anunciante nas suas telas. [A CONFIRMAR: o bloqueio de categorias pelo exibidor entra no MVP?]

**Experiência:**
- O admin abre a fila, vê o criativo na orientação enviada e os dados da campanha.
- Clica em "Aprovar" ou em "Reprovar". Na reprovação, escolhe o motivo da lista e, se quiser, escreve um texto.
- A campanha sai da fila e o anunciante recebe o aviso.
- Estado vazio: "Nenhum criativo aguardando moderação."
- Para o anunciante, a campanha mostra o estado e, se reprovada, o motivo com o botão "Trocar criativo".

### RF-006 Pagar campanha via Pix
O anunciante paga a campanha aprovada por Pix e ela fica agendada.

**Consome:**
- RF-004: campanha com identificador, anunciante, preço total e período
- RF-005: aprovação com campanha e decisão

**Fornece:**
- Pagamento: campanha, valor pago, data e estado (usado por RF-007, RF-009, RF-012)

**Capacidades:**
- CPF ou CNPJ pedido no primeiro pagamento do anunciante.
- Cobrança Pix com QR Code e copia e cola, válida por 30 min (hipótese)
- Confirmação automática pelo provedor, refletida na campanha em até 1 min (hipótese)
- Provedor do Pix. [A CONFIRMAR: qual PSP ou banco processa o Pix?]
- A plataforma recebe 100% do valor e guarda a parte do exibidor até o repasse (RF-009). [A CONFIRMAR: reter e repassar exige split do PSP ou licença de subcredenciador?]
- Campanha sem pagamento até 24 h antes do início volta a rascunho (hipótese)
- Só campanha aprovada gera cobrança.

**Experiência:**
- Na campanha em aguardando pagamento, o anunciante clica em "Pagar com Pix". Se for o primeiro pagamento, informa CPF ou CNPJ.
- Vê o QR Code, o copia e cola e o tempo restante.
- Ao confirmar o pagamento, a tela mostra "Pagamento confirmado" e a campanha passa a agendada.
- Se o saldo de crédito cobrir parte do valor, o desconto aparece antes da cobrança (RF-012).

**Tratamento de erros:**
- QR expirado: "Cobrança expirada" com o botão "Gerar novo Pix". Nenhum valor é cobrado.
- Pagamento em duplicidade: estorno Pix automático e aviso "Recebemos um pagamento repetido e devolvemos o valor."
- Valor divergente: a campanha não é agendada e o caso vai para o admin. O anunciante vê "Estamos verificando seu pagamento."
- Provedor fora do ar: a campanha fica como está e o anunciante vê "Pix indisponível no momento. Tente novamente em alguns minutos."

### RF-007 Exibir campanha na tela
O player exibe nas telas pareadas as campanhas agendadas para elas.

**Consome:**
- RF-002: tela com horário em que fica ligada e status (ativa ou pausada)
- RF-003: vínculo do player com player, tela e status online
- RF-004: campanha com criativos por orientação, telas, período e frequência
- RF-006: pagamento com campanha e estado

**Fornece:**
- Inserções exibidas: tela, campanha, criativo, início, duração e player (usado por RF-008)

**Capacidades:**
- O player busca a programação a cada 15 min e baixa os criativos novos (hipótese)
- Programação e criativos das próximas 24 h ficam em cache local (hipótese)
- Sem internet, o player segue exibindo o cache.
- Só campanhas com pagamento confirmado, dentro do período, entram na programação.
- As inserções são distribuídas igualmente dentro da hora, alternando campanhas.
- Sem campanha no horário, o player exibe conteúdo padrão. [A CONFIRMAR: o conteúdo padrão é anúncio da plataforma, do exibidor ou tela preta?]
- O player respeita o horário ligado da tela (RF-002) e a pausa do exibidor.
- Criativo corrompido no download é baixado de novo e nunca é exibido quebrado.
- Cache vencido sem internet: o player exibe o conteúdo padrão e a tela passa a offline.

**Experiência:**
- Gatilho: o player liga na TV e busca a programação.
- O sistema baixa os criativos, monta a sequência da hora e exibe cada inserção em tela cheia.
- Depois, o exibidor vê a tela online na sua conta e o anunciante vê a campanha em exibição.
- Sem programação, a TV mostra o conteúdo padrão.

### RF-008 Registrar exibições comprovadas
O player registra cada inserção exibida e a plataforma valida o que conta para repasse e relatório.

**Consome:**
- RF-007: inserções exibidas com tela, campanha, criativo, início, duração e player
- RF-003: vínculo do player com player, tela e chave de assinatura
- RF-004: campanha com período, telas e frequência

**Fornece:**
- Exibição comprovada: tela, campanha, início, duração, status (comprovada ou rejeitada) e motivo (usado por RF-009, RF-010, RF-012)

**Capacidades:**
- Registro por inserção com tela, campanha, criativo, início, duração e identificador do player.
- O registro é assinado pelo player, para não ser forjado fora dele.
- Envio em lote a cada 15 min. Sem internet, o player guarda os registros por até 7 dias, e o registro que chega após 7 dias é descartado (hipótese)
- Conta como comprovada só a inserção com duração completa (15 s), dentro do período da campanha e do horário ligado da tela, sem duplicidade.
- Inserções acima do contratado não contam.
- O admin vê os registros rejeitados e o motivo.
- Prova de que a TV estava ligada, e não só o player. [A CONFIRMAR: como provar que a TV estava ligada, e não só o player?]

**Experiência:**
- Gatilho: o player envia o lote de registros.
- O sistema confere a assinatura e aplica as regras de validação a cada registro, marcando como comprovada ou rejeitada com o motivo.
- O admin vê a lista de rejeitados com o motivo e filtra por tela e campanha.
- Exibidor e anunciante veem o resultado no extrato (RF-009) e no painel (RF-010).

**Tratamento de erros:**
- Lote com assinatura inválida: o lote é rejeitado por inteiro e o admin recebe um alerta.
- Relógio do player errado: o sistema usa a hora do servidor no momento do envio.
- Inserções acima do contratado: ficam registradas como rejeitadas com o motivo "acima do contratado" e não contam.

### RF-009 Repassar 70% ao exibidor pelo exibido
A plataforma calcula quanto cada exibidor ganhou pelas inserções comprovadas e paga 70% por Pix.

**Consome:**
- RF-008: exibição comprovada com tela, campanha, início, duração e status
- RF-006: pagamento com campanha, valor pago e estado
- RF-004: campanha com preço por inserção gravado por tela

**Capacidades:**
- Valor por inserção comprovada = preço da tela gravado na campanha no momento da compra (RF-004).
- O exibidor recebe 70% e a plataforma retém 30%.
- Fechamento semanal, de segunda 00h a domingo 23h59 (hipótese)
- Pagamento por Pix até D+2 úteis após o fechamento (hipótese)
- CPF ou CNPJ e chave Pix do mesmo titular são pedidos no primeiro repasse.
- Saldo abaixo de R$ 20 acumula para a semana seguinte (hipótese)
- Extrato por tela e campanha com inserções comprovadas, rejeitadas e valor.
- Só entra no repasse a campanha com pagamento confirmado.

**Experiência:**
- Na aba Exibir, "Repasses" mostra o saldo da semana, os pagamentos feitos e o extrato por tela e campanha.
- No primeiro repasse, o exibidor informa CPF ou CNPJ e chave Pix. Sem esses dados, o repasse fica retido e o painel avisa "Cadastre sua chave Pix para receber".
- Após o pagamento, o exibidor recebe o aviso "Repasse de <valor> enviado".
- Estado vazio: "Você ainda não tem repasses."
- O exibidor pode contestar um valor pelo extrato, e o admin recebe o caso com os registros de exibição.

**Tratamento de erros:**
- Chave Pix inválida ou de outro titular: o repasse fica retido e o exibidor vê "Sua chave Pix não confere com seu documento. Corrija para receber."
- Pix recusado pelo banco: o sistema tenta 3 vezes (hipótese). Depois, o caso vai para o admin e o exibidor vê "Estamos resolvendo seu repasse."
- Contestação do exibidor: abre um caso para o admin com o extrato, e o exibidor vê "Contestação recebida".

### RF-010 Acompanhar resultados da campanha
O anunciante acompanha o que foi exibido da campanha e quanto virou crédito.

**Consome:**
- RF-008: exibição comprovada com tela, campanha, início, duração e status
- RF-004: campanha com telas, período, frequência e preço total
- RF-012: crédito com campanha de origem e valor

**Capacidades:**
- Painel por campanha com inserções previstas, comprovadas e percentual entregue.
- Quebra por local, tela e dia.
- Atualização a cada 1 h (hipótese)
- Valor consumido e previsão de crédito (não exibido) a cada momento.
- Ao encerrar, resumo final com o crédito gerado (RF-012).
- Exportação do relatório em PDF ou CSV.
- Alerta por e-mail se uma tela da campanha ficar offline por mais de 24 h (hipótese)

**Experiência:**
- Na aba Anunciar, o anunciante abre "Minhas campanhas" e escolhe uma campanha.
- Vê o gráfico diário e a tabela por tela, com previsto, comprovado e percentual.
- Clica em "Exportar" e escolhe PDF ou CSV.
- Campanha ainda sem exibição: "Os resultados aparecem após a primeira exibição."
- Campanha encerrada: o resumo final mostra o valor exibido e o crédito gerado.

### RF-011 Explorar mapa de locais
Qualquer pessoa explora um mapa dos locais com telas, com avaliações, fotos e check-ins. É a visão de longo prazo, no espírito do PlugShare.

**Consome:**
- RF-002: local com nome, categoria, coordenadas e horário, e telas ativas

**Capacidades:**
- Mapa com pinos dos locais ativos (RF-002) e filtro por categoria.
- Ficha do local com fotos, telas e nota média.
- A conta logada avalia o local de 1 a 5 com comentário de até 500 caracteres, e o check-in só vale a até 200 m do local (hipótese)
- Fotos enviadas pela comunidade passam pela moderação do admin.
- Acesso ao mapa. [A CONFIRMAR: o mapa é público sem login ou só para contas?]
- Finalidade do check-in. [A CONFIRMAR: para que serve o check-in: recompensa, prova de audiência ou ranking?]

**Experiência:**
- A pessoa abre o mapa, vê os pinos e filtra por categoria.
- Ao tocar em um pino, abre a ficha com fotos, telas e nota média.
- Logada, avalia com nota e comentário e faz check-in quando está perto do local.
- Fora do raio, o check-in mostra "Você precisa estar perto do local para fazer check-in."
- Local sem avaliações: "Seja o primeiro a avaliar."

### RF-012 Gerar e usar crédito do não exibido
Ao fim da campanha, o valor pago que não foi exibido vira crédito na conta do anunciante, usado nos próximos pagamentos.

**Consome:**
- RF-006: pagamento com campanha, valor pago e estado
- RF-008: exibição comprovada com campanha, duração e status

**Fornece:**
- Crédito: conta, saldo, campanha de origem e valor (usado por RF-010)

**Capacidades:**
- Ao encerrar a campanha, crédito = valor pago menos o valor das inserções comprovadas.
- O crédito fica no saldo da conta do anunciante.
- No pagamento de uma campanha, o crédito cobre o valor todo ou em parte. O resto é cobrado por Pix pelo fluxo do RF-006.
- Crédito só abate pagamentos futuros. [A CONFIRMAR: o crédito expira ou pode ser resgatado em dinheiro?]

**Experiência:**
- Gatilho: a campanha encerra.
- O sistema calcula o crédito e soma ao saldo da conta.
- O anunciante vê o saldo na aba Anunciar e o crédito gerado no resumo da campanha (RF-010).
- Ao pagar uma campanha, o saldo é aplicado antes da cobrança Pix, e a tela mostra o valor abatido e o valor restante.
- Saldo zerado: a tela de pagamento não mostra a linha de crédito.

**Tratamento de erros:**
- Campanha encerrada sem exibição comprovada: o crédito é igual ao valor pago.
- Crédito maior que o valor da campanha: o saldo restante fica na conta e nenhuma cobrança Pix é gerada.
- Falha ao gerar o crédito no encerramento: o sistema tenta de novo e avisa o admin; o anunciante vê "Estamos calculando seu crédito."

## 7. Fora de escopo

**Pagamento**
- Cartão, boleto e parcelamento: só Pix.
- Nota fiscal automática. [A CONFIRMAR: quem emite a nota fiscal dos 30% da plataforma?]

**Plataforma**
- App nativo iOS ou Android para a conta: a web responsiva basta.
- Hardware próprio: o produto usa a TV do exibidor.

**Produto**
- Leilão ou preço dinâmico por tela.
- Segmentação por público: a segmentação é só por local.
- Medição de audiência por câmera ou sensor.
- Criativo em vídeo com som. [A CONFIRMAR: vídeo mudo entra no MVP?]

**Integrações**
- Redes de DOOH e agências externas.

## 8. Dependências entre requisitos

Uma linha "B depende de A" significa: B não funciona sem A implementado antes. A coluna "Depende de" é um superconjunto dos blocos Consome. A ordem de construção (ondas, caminho crítico e diagrama) é derivada desta tabela e vive no roadmap, em "Ordem de execução".

| # | Requisito | Prioridade | Depende de |
| --- | --- | --- | --- |
| RF-001 | Acessar a conta | 1 | nenhum |
| RF-002 | Cadastrar local e telas | 1 | RF-001 |
| RF-003 | Parear tela com o player | 1 | RF-002 |
| RF-004 | Criar campanha com criativo | 1 | RF-002 |
| RF-005 | Moderar criativo | 1 | RF-004 |
| RF-006 | Pagar campanha via Pix | 1 | RF-004, RF-005 |
| RF-007 | Exibir campanha na tela | 1 | RF-002, RF-003, RF-004, RF-006 |
| RF-008 | Registrar exibições comprovadas | 1 | RF-003, RF-004, RF-007 |
| RF-009 | Repassar 70% ao exibidor pelo exibido | 1 | RF-004, RF-006, RF-008 |
| RF-011 | Explorar mapa de locais | 3 | RF-002 |
| RF-012 | Gerar e usar crédito do não exibido | 1 | RF-006, RF-008 |
| RF-010 | Acompanhar resultados da campanha | 2 | RF-004, RF-008, RF-012 |

### Requisitos de fundação

Estes requisitos montam a infraestrutura compartilhada do projeto. Em um projeto novo, eles são implementados em sequência, antes ou junto de qualquer requisito que dependa deles.

- **RF-001 Acessar a conta**: monta a conta única e os papéis (usuário e admin) que todos os demais requisitos usam.

### Níveis de prioridade

- **1** = Essencial: o produto não funciona sem isso
- **2** = Importante: agrega valor significativo
- **3** = Desejável: melhoria incremental

### Dependências externas

- **Google Places API**: entrega a busca de estabelecimentos e os dados para pré-preencher o cadastro do local (trava RF-002)
- **PSP Pix**: cria a cobrança, confirma o pagamento por webhook, faz o estorno e paga o repasse. [A CONFIRMAR: qual PSP?] (trava RF-006, RF-009, RF-012)
- **Serviço de envio de e-mail**: envia confirmação de conta, avisos de moderação e alertas. [A CONFIRMAR: qual serviço?] (trava RF-001, RF-005, RF-010)
- **Serviço de mapa**: mostra o pino no cadastro e o mapa de locais (trava RF-002, RF-011)

## 9. Critérios de aceitação

### RF-001 Acessar a conta
- [ ] Cadastro com nome, e-mail e senha de 8 caracteres ou mais envia o e-mail de confirmação, e o link válido permite o login.
- [ ] A mesma conta acessa as áreas Anunciar e Exibir sem novo cadastro.
- [ ] Após 5 senhas erradas, a conta fica bloqueada por 15 minutos e a mensagem mostra a hora de liberação.
- [ ] Link de confirmação com mais de 24 horas é recusado e oferece reenviar.

### RF-002 Cadastrar local e telas
- [ ] Buscar um estabelecimento no Places preenche nome, endereço, coordenadas, categoria, horário e foto, e todos os campos podem ser editados.
- [ ] Sem resultado na busca, o cadastro manual salva o local.
- [ ] Preço por inserção abaixo do piso é recusado com a mensagem do piso.
- [ ] A 11ª tela de um mesmo local é recusada.

### RF-003 Parear tela com o player
- [ ] QR lido pelo celular logado pareia a tela e o player passa a exibir a programação dela.
- [ ] Código com 11 minutos é recusado e o player gera outro.
- [ ] Parear um segundo player em tela já pareada só desvincula o anterior após a confirmação.
- [ ] Tela sem sinal do player há mais de 5 minutos aparece como offline.

### RF-004 Criar campanha com criativo
- [ ] Criativo JPG ou PNG de 1920x1080 ou 1080x1920 até 5 MB é aceito, e outro formato ou tamanho é recusado com mensagem.
- [ ] O preço total exibido é a soma, por tela, das inserções previstas vezes o preço por inserção.
- [ ] Período com menos de 7 dias, mais de 90 dias ou início em menos de 2 dias é recusado.
- [ ] Criativo paisagem só é associado a telas horizontais, e retrato a telas verticais.

### RF-005 Moderar criativo
- [ ] Aprovar um criativo move a campanha para aguardando pagamento e avisa o anunciante.
- [ ] Reprovar exige motivo da lista; sem motivo a decisão não é salva.
- [ ] Após 3 reprovações seguidas na mesma campanha, a conta vai para revisão manual.
- [ ] A fila mostra o criativo mais antigo primeiro.

### RF-006 Pagar campanha via Pix
- [ ] Pix pago muda a campanha para agendada em até 1 minuto.
- [ ] QR expirado não confirma pagamento e permite gerar outro Pix.
- [ ] Pagamento em duplicidade gera estorno automático do valor repetido.
- [ ] Campanha sem pagamento até 24 horas antes do início volta a rascunho.

### RF-007 Exibir campanha na tela
- [ ] Com a internet desligada, o player segue exibindo a programação em cache.
- [ ] Fora do horário ligado da tela ou com a tela pausada, nenhuma campanha é exibida.
- [ ] Criativo corrompido no download não é exibido e é baixado de novo.
- [ ] Campanha sem pagamento confirmado não entra na programação.

### RF-008 Registrar exibições comprovadas
- [ ] Inserção de 10 segundos não conta como comprovada.
- [ ] Lote com assinatura inválida é rejeitado por inteiro e o admin é alertado.
- [ ] Registro que chega após 7 dias é descartado.
- [ ] O admin vê cada registro rejeitado com o motivo.

### RF-009 Repassar 70% ao exibidor pelo exibido
- [ ] No fechamento semanal, o exibidor recebe 70% do valor das inserções comprovadas, por Pix, até D+2 úteis.
- [ ] Saldo abaixo de R$ 20 não é pago e acumula para a semana seguinte.
- [ ] Chave Pix de outro titular retém o repasse e avisa o exibidor.
- [ ] O extrato mostra, por tela e campanha, inserções comprovadas, rejeitadas e valor.

### RF-010 Acompanhar resultados da campanha
- [ ] O painel mostra inserções previstas, comprovadas e percentual entregue por tela e por dia.
- [ ] O relatório exporta em PDF e em CSV.
- [ ] Tela da campanha offline por mais de 24 horas gera e-mail de alerta ao anunciante.
- [ ] Campanha sem nenhuma exibição mostra o estado vazio, sem erro.

### RF-011 Explorar mapa de locais
- [ ] O mapa mostra só locais ativos e o filtro por categoria remove os demais pinos.
- [ ] Avaliação com comentário acima de 500 caracteres é recusada.
- [ ] Check-in a 201 metros do local é recusado; a 200 metros ou menos é aceito.

### RF-012 Gerar e usar crédito do não exibido
- [ ] Campanha encerrada gera crédito igual ao valor pago menos o valor das inserções comprovadas.
- [ ] Campanha totalmente exibida não gera crédito.
- [ ] Crédito menor que o valor da próxima campanha abate o valor e o resto é cobrado por Pix.
- [ ] Crédito maior que o valor da campanha cobre tudo, não gera Pix e mantém o saldo restante.

### Integração entre requisitos
- [ ] Conta criada em RF-001 permite cadastrar local e telas em RF-002 na aba Exibir; sem login, o cadastro é recusado.
- [ ] Tela cadastrada em RF-002 aparece para pareamento em RF-003, e o pareamento atualiza o status online da tela.
- [ ] Local e tela com preço de RF-002 aparecem na busca de RF-004, e telas pausadas ou sem player pareado não aparecem.
- [ ] Campanha enviada em RF-004 aparece na fila de moderação de RF-005 com seus criativos.
- [ ] Aprovar o criativo em RF-005 libera a cobrança Pix em RF-006; criativo reprovado não gera Pix.
- [ ] Campanha com preço total de RF-004 gera em RF-006 uma cobrança Pix de mesmo valor.
- [ ] Campanha paga em RF-006 entra na programação do player em RF-007; campanha não paga não entra.
- [ ] Horário ligado e pausa de RF-002 são respeitados por RF-007.
- [ ] Vínculo do player de RF-003 é a origem da programação buscada em RF-007.
- [ ] Período, criativos e frequência de RF-004 definem o que RF-007 exibe.
- [ ] Inserção exibida em RF-007 chega a RF-008 e vira registro comprovado ou rejeitado.
- [ ] Chave de assinatura de RF-003 valida os lotes recebidos em RF-008.
- [ ] Período e telas de RF-004 definem em RF-008 se a inserção está dentro do contratado.
- [ ] 100 inserções comprovadas em RF-008 a R$ 1 geram em RF-009 um repasse de R$ 70.
- [ ] Pagamento confirmado em RF-006 é condição para a campanha entrar no repasse de RF-009.
- [ ] Preço por inserção gravado em RF-004 é o usado por RF-009 no cálculo do repasse, mesmo que o exibidor mude o preço depois.
- [ ] Exibição comprovada em RF-008 aparece no painel de RF-010 em até 1 hora.
- [ ] Campanha de RF-004 aparece em RF-010 com previsto, comprovado e percentual.
- [ ] O crédito gerado em RF-012 aparece no resumo final da campanha em RF-010.
- [ ] Local de RF-002 aparece como pino em RF-011 apenas com tela ativa.
- [ ] Campanha de R$ 100 paga em RF-006 com R$ 80 comprovados em RF-008 gera R$ 20 de crédito em RF-012.
- [ ] Valor pago em RF-006 é a base do crédito calculado em RF-012.
