# Banco de perguntas: arquitetura

Antes de cada rodada, leia o código: estrutura de pastas, manifestos, docker-compose, arquivos de infraestrutura, variáveis de ambiente. Apresente ao usuário o que você inferiu e pergunte só o que o código não mostra. Cada pergunta é feita sozinha, com alternativas tiradas do código e das respostas anteriores e uma recomendada; "Outro" fica para resposta livre, "não sei" ou "pular".

## Rodada 1: visão
1. Quais são os principais componentes ou serviços e o que cada um faz?
2. Como eles se comunicam: HTTP, filas, eventos, banco compartilhado?
3. Quais sistemas externos ou serviços de terceiros estão envolvidos?

## Rodada 2: dados
4. Quais são as entidades centrais do domínio?
5. Onde os dados ficam (bancos, caches, filas, storage) e por quê?
6. Há dados sensíveis, requisitos de retenção ou LGPD?

## Rodada 3: qualidade e operação
7. Requisitos de desempenho, disponibilidade e escala. Números, se tiver.
8. Como são feitos deploy, observabilidade e autenticação?
9. Quais são os pontos frágeis ou dívidas técnicas conhecidas?

## Rodada 4: decisões
10. Quais escolhas técnicas foram feitas conscientemente (linguagem, banco, mensageria, cloud, framework) e por quê?
11. Alguma dessas decisões já foi revertida ou está em discussão?
12. Houve alternativas avaliadas e descartadas? Quais e por quê?

## Como registrar candidatos a ADR
Para cada escolha mencionada, anote: contexto (qual problema), decisão (o que foi escolhido), motivo (por quê), alternativas (se citadas), status (vigente, em discussão, revertida). Se faltar motivo ou alternativas, registre como lacuna em vez de supor.
