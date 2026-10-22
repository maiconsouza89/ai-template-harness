---
name: docs-init
description: Entrevista o usuário e cria a documentação base de um projeto (PRD com requisitos RF-NNN e dependências, HLD, ADRs, roadmap com ondas de execução) na pasta docs/. Use sempre que o usuário pedir para documentar um projeto, criar documentação do zero, estruturar ou organizar docs, levantar requisitos, quebrar o produto em features, saber o que depende do quê ou o que dá para fazer em paralelo, ou mencionar PRD, HLD, ADR, FDD ou roadmap, mesmo que peça só "um resumo do projeto", "uma visão geral da arquitetura" ou "registrar as decisões".
---

# docs-init

Objetivo: transformar o que o usuário sabe sobre o projeto em uma primeira versão útil da documentação, deixando explícito o que ainda falta. A primeira versão não precisa estar completa; precisa mostrar com precisão as lacunas.

## Antes de perguntar
1. Verifique se `docs/` existe com as subpastas por tipo (`product/`, `architecture/`, `adr/`). Se existir, leia os READMEs e o frontmatter dos arquivos e trate a execução como atualização, não como criação. Pergunte apenas sobre o que está faltando ou marcado como `[A CONFIRMAR]`.
2. Leia README.md, manifestos (package.json, pyproject.toml, go.mod, pom.xml, Cargo.toml, docker-compose, etc.) e a estrutura de pastas. Anote o que o repositório já responde para não perguntar isso ao usuário.
3. Leia `docs/README.md` (as convenções da documentação) antes de gerar qualquer arquivo. Se não existir, o scaffold o cria.

## Entrevista
- Explique em duas frases o que vai acontecer: algumas rodadas de perguntas curtas, depois a geração dos documentos.
- Faça no máximo 6 perguntas por rodada (a rodada de requisitos é a exceção: uma pergunta por RF), **uma de cada vez**, com `AskUserQuestion`: uma pergunta por chamada, 2 a 4 opções concretas montadas a partir do que já se sabe (o repositório, as respostas anteriores), e a opção que você recomenda em primeiro lugar com " (Recomendado)" no rótulo. A descrição de cada opção diz em uma frase o que ela implica; a da recomendada diz também por que você a escolheu. O usuário reage a uma proposta mais rápido e melhor do que escreve do zero, e a recomendação mostra o seu raciocínio para ele poder discordar com precisão. O campo "Outro" fica aberto para resposta livre; diga na primeira rodada que respostas curtas, "não sei" e "pular" são aceitas ali.
- Perguntas abertas por natureza também ganham alternativas: "o que o produto faz?" vira duas ou três formulações candidatas tiradas do README e do código; sem contexto nenhum, as alternativas são os arquétipos mais comuns e o usuário corrige pelo "Outro".
- Ordem das rodadas: `references/perguntas-produto.md` (contexto, objetivos, escopo, um requisito por vez, contratos e dependências, aceitação, roadmap), depois `references/perguntas-arquitetura.md`. Pule perguntas que o repositório já respondeu e diga ao usuário o que você assumiu a partir do código.
- A partir da rodada de escopo, proponha em vez de perguntar: a lista de requisitos, cada RF com capacidades numeradas, os contratos Consome/Fornece e a tabela de dependências são derivados do que o usuário já disse e apresentados no `preview` para ele confirmar, ajustar ou cortar. Número que você propôs e o usuário aceitou leva `(hipótese)`; o PRD mantém a marca para o leitor saber o que foi decidido por ele e o que foi proposto.
- Sempre que o usuário disser que escolheu X por causa de Y, ou que descartou Z, anote como candidato a ADR com contexto, decisão e motivo.
- "Não sei" vira lacuna registrada, nunca suposição.
- Encerre quando conseguir perguntar sobre trade-offs sem que o básico precise ser explicado, ou quando o usuário pedir para gerar. Antes de gerar, resolva as inconsistências listadas em "Antes de gerar" do banco de perguntas e mostre um resumo do que entendeu: produto em duas frases, lista de RFs com prioridade e dependências, fundação, e o que ficou em lacuna. Peça confirmação. O resumo vai dentro da pergunta de confirmação, no `preview` da opção recomendada: texto escrito antes da chamada fica escondido enquanto o diálogo está aberto.

## Registro
Salve a entrevista em `docs/_intake/entrevista-AAAA-MM-DD.md` com as seções, nesta ordem: Contexto do repositório (o que foi lido no código), Produto (inclui os requisitos não funcionais), Requisitos (um bloco por RF-NNN com nome, descrição, capacidades, experiência, erros, escopo mínimo, prioridade e histórias, exatamente como confirmado), Contratos e dependências (Consome, Fornece, Depende de, fundação, dependências externas), Critérios de aceitação, Roadmap (horizontes), Arquitetura, Decisões (candidatos a ADR), Hipóteses aceitas (cada número proposto por você e aceito), Lacunas (tudo que ficou sem resposta). Esse arquivo é a única fonte que os subagents vão usar, então ele precisa ser completo e literal: registre o que o usuário disse, não a sua interpretação. Sem a seção Requisitos, o `prd-writer` não consegue escrever a seção 6 do PRD.

## Geração
1. Rode `python3 .claude/skills/docs-init/scripts/scaffold.py` para criar a árvore e os READMEs.
2. Delegue em paralelo para os subagents abaixo. Para cada um, passe na mensagem: o caminho da entrevista, o caminho do template em `docs/templates/`, o caminho de `docs/README.md` (convenções) e o caminho do arquivo de saída.
   - `prd-writer`: `docs/product/prd-<nome-kebab>.md`
   - `architecture-writer`: `docs/architecture/hld-visao-geral.md`
   - `adr-extractor`: um arquivo por decisão em `docs/adr/`
3. Com o PRD pronto e validado, gere você mesmo `docs/product/roadmap.md` a partir do template. Rode `python3 .claude/skills/docs-init/scripts/prd_checks.py docs/product/prd-<nome-kebab>.md --ondas` e cole a saída, sem editar, sob `### [PRD: <nome>](prd-<nome-kebab>.md)` na seção "Ordem de execução": ondas, caminho crítico e diagrama são derivados da tabela do PRD, e o validador acusa qualquer divergência. Preencha Agora, Próximo e Depois com a seção Roadmap da entrevista, citando os `RF-NNN` de cada iniciativa na coluna Requisitos e apontando a coluna Docs para a seção do RF no PRD (`prd-<nome>.md#rf-001-nome-do-requisito`). Itens sem PRD ou FDD ficam sem link na coluna Docs.
4. Rode o subagent `docs-reviewer` sobre `docs/`.
5. Rode `python3 .claude/skills/docs-init/scripts/validate.py` e corrija os erros apontados. Ele cobre frontmatter, links e índices de todos os documentos, o conteúdo do PRD (seções, RFs, contratos, tabela de dependências) e a coerência do roadmap com o PRD.
6. Atualize as tabelas de índice dos READMEs de `docs/product/`, `docs/architecture/` e `docs/adr/`.

## Entrega
- Liste os arquivos criados com uma linha sobre cada um.
- Mostre os RFs por onda e o caminho crítico, como estão no roadmap: é a resposta a "o que dá para fazer em paralelo".
- Liste as hipóteses do PRD (as que mais mudam o produto primeiro) e os requisitos que o `prd-writer` acrescentou sem o usuário pedir, para ele aprovar ou cortar.
- Liste as questões em aberto consolidadas pelo `docs-reviewer`, agrupadas por documento. Essa lista é a base para a evolução da documentação.
- Nunca invente fatos. O que não foi respondido fica no documento como `[A CONFIRMAR: pergunta objetiva]`.
- Sugira o próximo passo: responder as questões em aberto, ou criar FDDs com a skill `fdd` para os itens do roadmap que estão em Agora.
- Português do Brasil, frases curtas, sem travessões, nos documentos e nas mensagens.
