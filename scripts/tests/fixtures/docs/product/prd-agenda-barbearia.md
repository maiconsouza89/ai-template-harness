---
title: Agenda da Barbearia
type: prd
status: draft
date: 2026-10-21
owners: [Maicon Souza]
related: [roadmap.md]
---

# PRD: Agenda da Barbearia

## 1. Resumo executivo

A Agenda da Barbearia é um sistema de agendamento para barbearias pequenas, de 1 a 5 cadeiras, em que o cliente marca horário pelo celular sem instalar nada e o dono enxerga a agenda de todos os barbeiros em um lugar só. Ele substitui a combinação de mensagens no celular e agenda de papel que hoje faz o dono perder horários e passar quase uma hora por dia respondendo cliente.

O valor central é devolver tempo ao dono e reduzir o não-comparecimento: o cliente escolhe serviço, barbeiro e horário livre, recebe lembretes automáticos com opção de cancelar e, depois de faltar duas vezes em 60 dias, só agenda pagando sinal. O dono cadastra serviços e barbeiros, vê a agenda do dia, marca manualmente quem liga e registra falta com um toque.

Em alto nível: a barbearia cadastra o que oferece e quem atende; o cliente agenda por uma página pública; o sistema confirma, lembra e libera o horário quando há cancelamento; o dono acompanha e corrige pelo painel.

## 2. Problema e oportunidade

### O problema

**Horários perdidos por desencontro e falta**
- 8 a 10 horários por semana ficam vazios por desencontro de combinação ou não-comparecimento
- Em uma barbearia de 3 cadeiras isso representa cerca de 10 por cento da capacidade semanal
- A agenda compartilhada já foi tentada e os clientes não a usaram

**Dono preso no atendimento por mensagem**
- Quase 1 hora por dia respondendo mensagens de marcação, remarcação e confirmação
- As respostas atrasam quando o dono está atendendo, e o cliente marca em outro lugar
- Não há registro confiável de quem marcou o quê; a agenda de papel não bate com as conversas

**Falta de consequência para quem falta**
- Cerca de 1 em cada 5 faltas é de cliente reincidente, que volta a marcar sem nenhuma restrição
- O dono não sabe quantas faltas cada cliente tem; a contagem é de memória
- Sem sinal, o custo da falta é inteiro da barbearia

### A oportunidade

- **Horários perdidos.** Agenda em tempo real com horários livres calculados a partir do serviço e do barbeiro, lembretes 24 h e 2 h antes com cancelamento em um toque, e liberação imediata do horário cancelado.
- **Dono preso no atendimento.** O cliente marca sozinho pela página pública; o dono só entra para quem liga, e vê tudo em um painel único do dia.
- **Falta sem consequência.** Contagem automática de faltas por cliente e exigência de sinal depois da segunda falta em 60 dias, regra que o dono não precisa lembrar nem aplicar na mão.

## 3. Público-alvo

### Usuários primários

**Dono da barbearia**
- Administra 1 a 5 cadeiras, atende também, usa o celular como ferramenta principal
- Quer parar de responder mensagem e saber quem vem hoje
- Decide regras: serviços, preços, horários e o que acontece com quem falta

**Barbeiro**
- Vê só a própria agenda do dia e da semana
- Marca atendimento concluído ou falta ao fim de cada horário
- Pouca paciência para telas: precisa resolver em 1 ou 2 toques

**Cliente final**
- Marca pelo celular, sem instalar nada e sem criar conta
- Quer escolher o barbeiro de sempre ou "qualquer um" e ver o horário livre na hora
- Recebe lembrete e cancela pelo mesmo canal quando não pode ir

### Perfil comportamental

- Todos usam celular como dispositivo principal; desktop é exceção para o dono
- Baixa tolerância a cadastro longo: nome e telefone bastam para o cliente
- Horário comercial estendido: das 8 h às 21 h, inclusive sábado

## 4. Objetivos e métricas

### Objetivos de produto

| Objetivo | Métrica | Meta |
| --- | --- | --- |
| **Reduzir** o não-comparecimento | faltas por semana sobre agendamentos confirmados | cair pela metade em 3 meses a partir do piloto |
| **Tirar** o dono do atendimento por mensagem | tempo diário do dono em marcação por mensagem | de cerca de 1 h para até 15 min por dia em 2 meses |
| **Fazer** o cliente agendar sozinho | parcela dos agendamentos feitos pelo cliente na página pública | pelo menos 70 por cento em 3 meses |
| **Ocupar** os horários cancelados | parcela de horários cancelados com antecedência que são reocupados | pelo menos 30 por cento em 3 meses |

### Requisitos não funcionais

Performance
- A lista de horários livres de um dia aparece em até 1 segundo para 95 por cento das consultas
- Confirmação de agendamento em até 2 segundos

Disponibilidade
- 99.5 por cento de disponibilidade mensal entre 7 h e 22 h, todos os dias

Segurança e autorização
- Dono e barbeiro entram com identificação própria; barbeiro só vê e altera a própria agenda
- Cliente não tem conta: acessa o próprio agendamento por link individual com prazo de validade
- Toda alteração de agendamento registra quem fez, quando e o valor anterior

Compatibilidade
- Navegadores de celular dos últimos 2 anos; desktop para o painel do dono; português do Brasil

Compliance
- Nome e telefone do cliente tratados conforme a LGPD; exclusão sob pedido em até 15 dias

## 5. Histórias de usuário

### RF-001 Acesso de dono e barbeiro
- Como dono, quero entrar com e-mail e senha para administrar minha barbearia
- Como dono, quero convidar um barbeiro por link para que ele acesse só a própria agenda
- Como barbeiro, quero redefinir minha senha por e-mail para recuperar o acesso sozinho

### RF-002 Cadastro da barbearia, serviços e barbeiros
- Como dono, quero cadastrar serviços com nome, duração e preço para que o cliente saiba o que escolher
- Como dono, quero cadastrar barbeiros com horário de trabalho por dia da semana para que só horários reais apareçam
- Como dono, quero desativar um serviço ou barbeiro sem apagar o histórico

### RF-003 Agendamento pelo cliente
- Como cliente, quero escolher serviço, barbeiro ou "qualquer um", dia e horário livre para marcar sem falar com ninguém
- Como cliente, quero confirmar com nome e telefone, sem criar conta
- Como cliente, quero receber a confirmação com um link para ver e alterar o meu horário

### RF-004 Agenda do dia e marcação manual
- Como dono, quero ver a agenda do dia de todos os barbeiros em uma tela só
- Como dono, quero marcar um horário para o cliente que ligou
- Como barbeiro, quero marcar um atendimento como concluído ou como falta em um toque

### RF-005 Cancelamento e remarcação pelo cliente
- Como cliente, quero cancelar ou remarcar pelo link do agendamento até 2 horas antes
- Como cliente, quero ver os horários livres ao remarcar sem refazer o agendamento do zero
- Como o sistema, quero liberar o horário cancelado imediatamente para outro cliente

### RF-006 Lembretes automáticos
- Como o sistema, quero enviar lembrete 24 horas e 2 horas antes do horário para reduzir faltas
- Como cliente, quero cancelar pelo próprio lembrete quando não puder ir
- Como dono, quero ver se o lembrete foi entregue ou falhou

### RF-007 Controle de faltas e sinal
- Como o sistema, quero contar as faltas de cada cliente nos últimos 60 dias
- Como o sistema, quero exigir sinal de um cliente com 2 faltas em 60 dias antes de confirmar o agendamento
- Como dono, quero ver quem está na lista de sinal obrigatório e perdoar uma falta quando fizer sentido

## 6. Requisitos funcionais

### RF-001 Acesso de dono e barbeiro
O sistema identifica dono e barbeiro com credencial própria e limita cada um ao que pode ver e fazer.

**Capacidades:**
- Dois papéis: dono (tudo da barbearia) e barbeiro (só a própria agenda)
- Dono cria a barbearia no primeiro acesso; cada barbearia tem exatamente 1 dono nesta versão
- Convite de barbeiro por link com validade de 7 dias (hipótese)
- Redefinição de senha por e-mail com link válido por 1 hora (hipótese)
- Sessão expira após 30 dias sem uso no celular (hipótese)

**Experiência:**
- Tela de entrada com e-mail e senha; erro genérico "e-mail ou senha incorretos" sem dizer qual
- Primeiro acesso do dono: nome da barbearia, telefone e endereço, depois vai direto ao cadastro de serviços
- Barbeiro abre o link do convite, define senha e cai na própria agenda do dia
- Link "esqueci a senha" pede o e-mail e sempre responde "se o e-mail existir, enviamos o link"

**Tratamento de erros:**
- Link de convite expirado: "Este convite venceu. Peça um novo ao dono da barbearia."
- Link de redefinição usado duas vezes: "Este link já foi usado. Peça outro."
- 5 tentativas erradas em 10 minutos: bloqueio por 15 minutos com aviso do tempo restante (hipótese)
- Barbeiro tentando abrir agenda de outro: tela "Você não tem acesso a esta agenda" e registro no histórico

### RF-002 Cadastro da barbearia, serviços e barbeiros
O dono mantém o catálogo de serviços e a equipe com os horários de trabalho que alimentam a agenda.

**Fornece:**
- Catálogo de serviços ativos com nome, duração em minutos e preço (usado por RF-003, RF-004)
- Barbeiros ativos com horário de trabalho por dia da semana e intervalos (usado por RF-003, RF-004)

**Capacidades:**
- Serviço: nome até 40 caracteres, duração de 10 a 180 minutos em múltiplos de 5, preço em reais com 2 casas
- Até 30 serviços e 5 barbeiros por barbearia nesta versão (hipótese)
- Horário de trabalho por dia da semana, com até 2 intervalos por dia; folga é dia sem horário
- Serviço ou barbeiro desativado some das opções do cliente, mas continua nos agendamentos passados
- Barbeiro pode ter folga avulsa em uma data específica, que bloqueia novos agendamentos naquele dia

**Experiência:**
- Lista de serviços com nome, duração e preço; botão "novo serviço" abre formulário de 3 campos
- Lista de barbeiros com foto opcional, nome e resumo do horário ("seg a sex 9h às 19h, sáb 8h às 14h")
- Edição de horário em grade por dia da semana; salvar mostra "horário atualizado" e já vale para novos agendamentos
- Desativar pede confirmação e avisa quantos agendamentos futuros aquele barbeiro tem

**Tratamento de erros:**
- Desativar barbeiro com agendamentos futuros: lista os agendamentos e pede para remarcar ou cancelar antes
- Duração fora do intervalo: "Duração deve ficar entre 10 e 180 minutos, em múltiplos de 5"
- Horário com fim antes do início: "O fim do expediente precisa ser depois do início"
- Falha ao salvar: formulário mantém os valores e mostra "Não foi possível salvar. Tente de novo."

### RF-003 Agendamento pelo cliente
O cliente escolhe serviço, barbeiro, dia e horário livre em uma página pública e confirma com nome e telefone.

**Consome:**
- RF-002: catálogo de serviços ativos com duração e preço; barbeiros ativos com horário de trabalho

**Fornece:**
- Agendamento com cliente (nome, telefone), serviço, barbeiro, data, horário, duração e status (usado por RF-004, RF-005, RF-006, RF-007)

**Escopo mínimo:**
- Escolha de serviço, barbeiro ou "qualquer um", dia e horário; confirmação com nome e telefone; link individual

**Adições de escopo completo:**
- Lembrar nome e telefone no mesmo celular para a próxima vez
- Sugerir o barbeiro do último atendimento

**Capacidades:**
- Horários livres calculados a partir da duração do serviço, do horário de trabalho do barbeiro e dos agendamentos existentes, em passos de 15 minutos (hipótese)
- "Qualquer barbeiro" escolhe o barbeiro livre com menos agendamentos no dia (hipótese)
- Agendamento permitido de 1 hora a 30 dias à frente (hipótese)
- Telefone brasileiro com DDD, 10 ou 11 dígitos; nome de 2 a 60 caracteres
- Cliente com sinal obrigatório (regra de RF-007) só confirma depois de pagar o sinal
- Link individual do agendamento válido até 24 horas depois do horário marcado

**Experiência:**
- Página pública da barbearia com nome, endereço e botão "agendar"
- Passo 1: serviço (nome, duração, preço); passo 2: barbeiro com foto ou "qualquer um"; passo 3: calendário com dias disponíveis; passo 4: horários livres do dia em botões
- Passo 5: nome e telefone; botão "confirmar" mostra resumo e o link do agendamento
- Horário que acabou de ser ocupado por outro cliente some da lista ao atualizar
- Estado sem horário livre: "Sem horários neste dia. Veja o próximo dia disponível: quinta, 14/11"

**Tratamento de erros:**
- Horário tomado entre a escolha e a confirmação: "Esse horário acabou de ser preenchido. Escolha outro." e volta ao passo 4 com a lista atualizada
- Telefone inválido: "Digite um telefone com DDD, por exemplo (11) 99999-9999"
- Cliente com sinal obrigatório fechou a cobrança sem pagar: agendamento fica "aguardando sinal" por 15 minutos e depois é descartado (hipótese)
- Falha ao confirmar: "Não conseguimos confirmar. Seu horário não foi reservado. Tente de novo."

### RF-004 Agenda do dia e marcação manual
Dono e barbeiro veem a agenda e registram atendimentos manuais, conclusões e faltas.

**Consome:**
- RF-002: barbeiros ativos com horário de trabalho; catálogo de serviços ativos
- RF-003: agendamentos com cliente, serviço, barbeiro, data, horário, duração e status

**Fornece:**
- Marcação de não-comparecimento com cliente (telefone), data e quem marcou (usado por RF-007)

**Capacidades:**
- Visão do dia com uma coluna por barbeiro e os horários em blocos proporcionais à duração
- Dono vê todos; barbeiro vê só a própria coluna
- Marcação manual pelo dono com os mesmos limites de RF-003, mas sem exigir sinal e sem limite de 30 dias (hipótese)
- Status possíveis do agendamento: confirmado, concluído, falta, cancelado
- Falta só pode ser marcada a partir de 15 minutos depois do horário marcado (hipótese)
- Navegação para qualquer dia; semana do barbeiro em lista

**Experiência:**
- Abre no dia de hoje, rolagem horizontal entre barbeiros no celular
- Toque em um bloco abre o cartão do agendamento com nome, telefone, serviço e os botões "concluído", "falta", "cancelar"
- Toque em um espaço livre abre "marcar para cliente" com nome, telefone, serviço e duração já preenchida
- Bloco muda de cor por status; falta fica marcada em vermelho com o horário em que foi registrada
- Barra do topo mostra quantos atendimentos, quantas faltas e quantos horários livres no dia

**Tratamento de erros:**
- Marcar falta antes da janela: "Só é possível marcar falta a partir das 14:15"
- Marcação manual em horário ocupado: "Esse horário já está preenchido" e o bloco ocupado pisca
- Cancelamento manual de agendamento já concluído: ação indisponível com aviso "Atendimento concluído não pode ser cancelado"
- Falha ao salvar status: o bloco volta ao estado anterior e mostra "Não foi possível salvar"

### RF-005 Cancelamento e remarcação pelo cliente
O cliente cancela ou remarca pelo link do próprio agendamento dentro da janela permitida.

**Consome:**
- RF-003: agendamento com cliente, serviço, barbeiro, data, horário e status, acessado pelo link individual

**Fornece:**
- Link de cancelamento e remarcação com o prazo limite de 2 horas antes do horário (usado por RF-006)

**Capacidades:**
- Cancelar ou remarcar até 2 horas antes do horário; depois disso o link mostra o agendamento sem ações
- Remarcar mantém serviço e barbeiro e reabre a escolha de dia e horário
- Horário cancelado volta à lista de livres imediatamente
- Cancelamento dentro da janela não conta como falta

**Experiência:**
- Página do agendamento com resumo e dois botões: "remarcar" e "cancelar"
- Cancelar pede confirmação "Cancelar o horário de quinta às 14h?" e mostra "Horário cancelado" com botão para agendar de novo
- Remarcar mostra o calendário com os horários livres do mesmo barbeiro; confirmar atualiza o mesmo agendamento
- Fora da janela: botões escondidos e aviso "Cancelamento só até 2 horas antes. Fale com a barbearia: (11) 3333-3333"

**Tratamento de erros:**
- Link expirado ou inválido: "Este link não é mais válido" com o telefone da barbearia
- Remarcação para horário que acabou de ser tomado: mesma recuperação de RF-003
- Agendamento já cancelado pelo dono: "Este horário já foi cancelado pela barbearia"
- Falha ao salvar: "Não foi possível cancelar. Seu horário continua marcado. Tente de novo."

### RF-006 Lembretes automáticos
O sistema envia lembretes antes do horário, com atalho para cancelar, e registra se foram entregues.

**Consome:**
- RF-003: agendamento com telefone do cliente, serviço, barbeiro, data e horário
- RF-005: link de cancelamento e remarcação com prazo limite

**Capacidades:**
- Dois lembretes por agendamento: 24 horas antes e 2 horas antes; o de 2 horas sai só se o agendamento ainda estiver confirmado
- Agendamento feito com menos de 24 horas de antecedência recebe só o lembrete de 2 horas
- Mensagem com nome da barbearia, serviço, barbeiro, dia, horário e o link de cancelamento
- Canal: o aplicativo de mensagens que o cliente já usa, por um provedor externo (hipótese); dependência externa listada na seção 8
- Até 3 tentativas de envio com intervalo de 5 minutos; depois registra falha (hipótese)
- Status do lembrete por agendamento: enviado, entregue, falhou

**Experiência:**
- Cliente recebe a mensagem e, ao tocar no link, cai na página de RF-005
- No cartão do agendamento (RF-004), dono vê os dois lembretes com status e horário
- Falha de entrega aparece com ícone de alerta para o dono ligar

**Tratamento de erros:**
- Provedor de mensagens fora do ar: lembretes ficam na fila e são reenviados por até 1 hora; depois marcam "falhou" (hipótese)
- Telefone recusado pelo provedor: status "falhou" com motivo "número inválido" e aviso ao dono
- Agendamento cancelado entre a fila e o envio: lembrete é descartado
- Dois lembretes iguais na fila: o sistema envia um só

### RF-007 Controle de faltas e sinal
O sistema conta faltas por cliente e exige sinal de quem faltou 2 vezes nos últimos 60 dias.

**Consome:**
- RF-003: agendamentos com telefone do cliente e status
- RF-004: marcação de não-comparecimento com cliente, data e quem marcou

**Escopo mínimo:**
- Contagem de faltas por telefone nos últimos 60 dias; lista de sinal obrigatório; bloqueio da confirmação sem sinal

**Adições de escopo completo:**
- Dono perdoa uma falta com motivo
- Relatório mensal de faltas por barbeiro

**Capacidades:**
- Cliente identificado pelo telefone; 2 faltas em 60 dias corridos colocam o cliente na lista de sinal obrigatório
- Sinal de 30 por cento do preço do serviço, mínimo de R$ 10, cobrado por link de pagamento de um provedor externo (hipótese)
- Sinal pago é abatido do serviço; cliente que falta com sinal pago perde o sinal
- Cliente sai da lista quando completa 60 dias sem falta ou quando o dono perdoa
- Dono pode desligar a regra de sinal para a barbearia inteira

**Experiência:**
- Em RF-003, cliente da lista vê no passo 5: "Para confirmar, pague o sinal de R$ 15. Ele é descontado do serviço." e o botão vira "pagar sinal"
- Pagamento confirmado leva ao resumo do agendamento com "sinal pago"
- Painel do dono: lista de clientes com sinal obrigatório, faltas e datas, botão "perdoar"

**Tratamento de erros:**
- Provedor de pagamento indisponível: "Não conseguimos gerar a cobrança. Tente em alguns minutos ou ligue para a barbearia."
- Pagamento não confirmado em 15 minutos: agendamento descartado e horário liberado, com aviso ao cliente
- Confirmação de pagamento chegando depois do descarte: sinal estornado em até 5 dias úteis e aviso ao dono (hipótese)
- Dono perdoa falta de cliente que não está na lista: ação indisponível

## 7. Fora de escopo

**Pagamento**
- Pagamento online do serviço inteiro (só o sinal nesta versão)
- Carteira ou crédito pré-pago

**Fidelização e marketing**
- Programa de fidelidade e descontos
- Envio de promoções pelo canal de lembretes

**Plataforma**
- Aplicativo nativo para celular (a página pública cobre o celular)
- Múltiplas unidades de uma mesma barbearia

**Operação**
- Comissão e fechamento financeiro por barbeiro
- Estoque de produtos

## 8. Dependências entre requisitos

Uma linha "B depende de A" significa: B não funciona sem A implementado antes. A coluna "Depende de" é um superconjunto dos blocos Consome. A ordem de construção (ondas, caminho crítico e diagrama) é derivada desta tabela e vive no roadmap, em "Ordem de execução".

| # | Requisito | Prioridade | Depende de |
| --- | --- | --- | --- |
| RF-001 | Acesso de dono e barbeiro | 1 | nenhum |
| RF-002 | Cadastro da barbearia, serviços e barbeiros | 1 | RF-001 |
| RF-003 | Agendamento pelo cliente | 1 | RF-002 |
| RF-004 | Agenda do dia e marcação manual | 1 | RF-002, RF-003 |
| RF-005 | Cancelamento e remarcação pelo cliente | 1 | RF-003 |
| RF-006 | Lembretes automáticos | 1 | RF-003, RF-005 |
| RF-007 | Controle de faltas e sinal | 2 | RF-003, RF-004 |

### Requisitos de fundação

Estes requisitos montam a infraestrutura compartilhada do projeto. Em um projeto novo, eles são implementados em sequência, antes ou junto de qualquer requisito que dependa deles.

- **RF-001 Acesso de dono e barbeiro**: base do projeto, papéis, sessão e a entidade barbearia que todos os outros usam

### Níveis de prioridade

- **1** = Essencial: o produto não funciona sem isso
- **2** = Importante: agrega valor significativo
- **3** = Desejável: melhoria incremental

### Dependências externas

- **Canal de mensagens para o cliente**: provedor que entrega mensagens no aplicativo que o cliente já usa, com confirmação de entrega; sem ele não há lembrete (trava RF-006)
- **Cobrança do sinal por link**: provedor que gera link de pagamento e confirma o pagamento; sem ele a regra de sinal fica desligada (trava RF-007)

## 9. Critérios de aceitação

### RF-001 Acesso de dono e barbeiro
- [ ] Dono cria a barbearia no primeiro acesso e entra com e-mail e senha
- [ ] Barbeiro convidado por link define senha e vê só a própria agenda
- [ ] Barbeiro que tenta abrir a agenda de outro vê "Você não tem acesso a esta agenda"
- [ ] Senha errada mostra erro genérico sem dizer se o e-mail existe

### RF-002 Cadastro da barbearia, serviços e barbeiros
- [ ] Serviço salvo com nome, duração entre 10 e 180 minutos e preço aparece para o cliente
- [ ] Horário de trabalho salvo limita os horários livres daquele barbeiro
- [ ] Desativar barbeiro com agendamentos futuros é bloqueado até remarcar ou cancelar
- [ ] Duração fora do intervalo é recusada com a mensagem especificada

### RF-003 Agendamento pelo cliente
- [ ] Cliente conclui um agendamento em 5 passos informando só nome e telefone
- [ ] Lista de horários livres respeita duração do serviço, expediente do barbeiro e agendamentos existentes
- [ ] Horário tomado entre a escolha e a confirmação devolve o cliente ao passo 4 com a lista atualizada
- [ ] Telefone sem DDD é recusado com a mensagem especificada

### RF-004 Agenda do dia e marcação manual
- [ ] Dono vê uma coluna por barbeiro com os blocos do dia; barbeiro vê só a própria
- [ ] Marcação manual em espaço livre cria agendamento confirmado sem exigir sinal
- [ ] Falta só pode ser marcada 15 minutos depois do horário e fica registrada com quem marcou
- [ ] Marcar em horário ocupado é recusado

### RF-005 Cancelamento e remarcação pelo cliente
- [ ] Cancelar até 2 horas antes libera o horário imediatamente e não conta como falta
- [ ] Com menos de 2 horas, os botões somem e o aviso com o telefone aparece
- [ ] Remarcar mantém serviço e barbeiro e atualiza o mesmo agendamento
- [ ] Link inválido mostra "Este link não é mais válido"

### RF-006 Lembretes automáticos
- [ ] Agendamento com 3 dias de antecedência recebe lembrete 24 h e 2 h antes
- [ ] Agendamento feito com 5 horas de antecedência recebe só o lembrete de 2 h
- [ ] Agendamento cancelado antes do envio não recebe lembrete
- [ ] Falha de entrega aparece no cartão do agendamento para o dono

### RF-007 Controle de faltas e sinal
- [ ] Cliente com 2 faltas em 60 dias vê a cobrança do sinal no passo 5 e só confirma depois de pagar
- [ ] Cliente com 2 faltas em 61 dias agenda sem sinal
- [ ] Sinal não pago em 15 minutos descarta o agendamento e libera o horário
- [ ] Dono perdoa uma falta e o cliente sai da lista

### Integração entre requisitos
- [ ] Serviço e barbeiro cadastrados em RF-002 aparecem como opções em RF-003 com a duração correta
- [ ] Barbeiro e serviço de RF-002 aparecem nas colunas e na marcação manual de RF-004
- [ ] Agendamento confirmado em RF-003 aparece no bloco correto da agenda de RF-004
- [ ] Link do agendamento criado em RF-003 abre a página de cancelamento de RF-005
- [ ] Agendamento de RF-003 gera os dois lembretes de RF-006 com dia, horário e barbeiro corretos
- [ ] Lembrete de RF-006 leva ao link de cancelamento de RF-005 com o prazo correto
- [ ] Telefone do agendamento de RF-003 é o que RF-007 usa para contar faltas
- [ ] Falta marcada em RF-004 entra na contagem de RF-007 no mesmo dia
