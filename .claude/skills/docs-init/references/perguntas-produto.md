# Banco de perguntas: produto

Antes de cada rodada, confira o que o repositório já responde e pule essas perguntas. Reformule as perguntas com o vocabulário que o usuário usou nas respostas anteriores. Cada pergunta é feita sozinha, com 2 a 4 alternativas montadas a partir do que já se sabe e uma recomendada; o campo "Outro" fica para resposta livre, "não sei" ou "pular".

A partir da rodada 3, prefira **propor e pedir confirmação** a perguntar aberto: monte a lista, o requisito ou o contrato a partir do que o usuário já disse, coloque a proposta no `preview` da opção recomendada e ofereça aceitar, ajustar pelo "Outro" ou cortar. O usuário corrige uma proposta mais rápido e melhor do que escreve do zero.

## Rodada 1: contexto
1. Em uma frase, o que o produto ou sistema faz e para quem?
2. Qual problema ele resolve e como esse problema é resolvido hoje, sem ele? Peça um número por dor (horas por semana, reais por mês, erros por lote); sem número, ordem de grandeza.
3. Quem são os usuários (papéis) e qual deles é o principal? Eles têm jornadas diferentes ou é o mesmo uso com permissões diferentes?
4. Em que estágio está: ideia, MVP, produção, legado em manutenção?

## Rodada 2: objetivos
5. Quais são os 2 ou 3 objetivos mais importantes para os próximos meses? Cada um com verbo, métrica e meta com número e prazo.
6. Como você mede se deu certo? Métricas, mesmo que aproximadas.
7. Requisitos não funcionais como meta observável: quanto tempo o usuário tolera esperar; quando o sistema pode ficar fora; quem pode ver e alterar o quê; dispositivos e idiomas; norma aplicável (LGPD, setor regulado). Performance e disponibilidade entram sempre; sem número, ficam como lacuna.
8. Restrições: prazo, orçamento, regulatório, compatibilidade com algo existente?

## Rodada 3: escopo
9. Lista de requisitos funcionais candidatos, por nome curto (verbo + objeto: "Agendar horário", "Aprovar reembolso"), montada do que foi dito nas rodadas 1 e 2. Uma pergunta com a lista inteira no `preview`; o usuário corta, acrescenta ou renomeia. Alvo: 5 a 15. Sinais para dividir um RF: dois gatilhos diferentes, dois perfis com fluxos diferentes, mais de 8 passos. Sinais para juntar: dois RFs que nunca são implementados separados e não trocam dado.
10. Em projeto novo sem RF de acesso e papéis: o produto tem login e quem pode o quê? Se tem, é um RF de fundação, provavelmente o primeiro.
11. O que explicitamente está fora de escopo, agrupado por categoria (pagamento, plataforma, operação, integrações). Teste cada item contra os objetivos: fora de escopo que impede um objetivo é contradição e se resolve agora.

## Rodada 4: um requisito por vez
Uma pergunta por RF da lista confirmada, com a proposta completa no `preview`:
- descrição em uma frase;
- capacidades com número (tamanho, quantidade, prazo, formato, regra com condição explícita), cada número que você propôs marcado `(hipótese)`;
- experiência passo a passo, do gatilho ao resultado, com campos, validações, estados e mensagens;
- tratamento de erros só se o RF é crítico (acesso, dinheiro, dado persistente, operação sensível, longa ou irreversível), 3 a 5 cenários com mensagem;
- escopo mínimo e adições, só se há capacidades de prioridade diferente dentro do RF;
- prioridade 1 (o produto não funciona sem), 2 (agrega valor significativo) ou 3 (melhoria incremental);
- 2 a 6 histórias "Como <papel>, quero <ação concreta> para <resultado>".

Opções: aceitar como está (recomendada quando a proposta vem das respostas), ajustar pelo "Outro", cortar o RF. Se o usuário descreve um RF que depende de outro ainda não listado, registre o novo e volte à lista. Esta rodada não tem teto de perguntas: é uma por RF.

## Rodada 5: contratos e dependências
Derive e apresente para confirmação, não pergunte do zero.
12. Para cada par de RFs em que um usa dado que o outro cria: Consome (no consumidor, com os campos) e Fornece (no produtor, com "usado por"). Autenticação e sessão não entram.
13. Para cada RF, "Depende de": todo Consome mais dependências de infraestrutura (acesso, cadastro base). Só diretas. Pergunte só: "falta ou sobra alguma dependência?". RF 1 dependendo de RF 3 é sinal de que a prioridade do 3 está errada.
14. Quais RFs são de fundação (montam a base que todos usam) e por quê. Em projeto existente, normalmente nenhum.
15. Dependências externas (serviço de terceiro, outro time, dado legado), descritas pelo que fazem, e que RFs cada uma trava.

## Rodada 6: aceitação
16. Por RF, critérios de uma frase, verificáveis por alguém de fora do time, derivados das capacidades e dos erros, cobrindo sucesso e falha. Proponha e peça só o que falta.
17. Integração entre requisitos: para cada Consome, um critério que testa que o dado chega de um RF ao outro e produz o efeito esperado, citando os dois IDs.

## Rodada 7: roadmap
Com a tabela de dependências em mãos, calcule as ondas (onda 1 são os RFs sem dependência; cada RF fica em 1 mais a maior onda das suas dependências) e proponha os horizontes:
18. Agora: RFs de prioridade 1 das primeiras ondas. O que já está em andamento?
19. Próximo: o resto da prioridade 1 e a prioridade 2 já priorizada.
20. Depois: prioridade 3 e ideias sem compromisso.
21. Algo adiado ou descartado recentemente, e por quê?

## Antes de gerar
Resolva na entrevista, não no documento:
- Objetivo sem RF que o entregue; RF que não serve a nenhum objetivo.
- Item fora de escopo que um RF precisa.
- RF de prioridade 1 dependendo de RF de prioridade 3.
- Dois RFs que dependem um do outro.
- Dor sem número e sem lacuna registrada.

## Sinais de que a rodada pode ser encerrada
- O usuário repete informações já dadas.
- As respostas passaram a ser "não sei" ou "pular" em sequência.
- Você consegue descrever o produto em um parágrafo sem lacunas grandes.
