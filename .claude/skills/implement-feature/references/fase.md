# Fase: briefing do subagente e commit

## Sumário

1. Briefing do subagente
2. O que o subagente faz
3. Falhas
4. Retorno
5. Commit

## 1. Briefing do subagente

O subagente só sabe o que o briefing diz. Copie o bloco abaixo, preencha os colchetes e mande inteiro: ele traz as regras da seção 2 para dentro do prompt, porque o subagente não carrega esta skill.

```
Você implementa a fase [N] de [M] do plano de [RF-NNN Nome | fundação] neste repositório.
Pasta da feature: [docs/features/<pasta>/]

Fase [N]: [título]
[passos da fase, copiados do plan.md com a numeração]

Fases anteriores (já no working tree ou commitadas):
[por fase: título, arquivos principais criados, desvios que afetam esta fase; ou "nenhuma"]

Pré-requisitos do contrato que esta fase deve produzir, quando for ela que cria o lugar deles:
[handles de Estado persistido, caminhos de Entradas estáticas e linhas de Configuração da ficha;
 ou "nenhum nesta fase"]

Leia antes de editar:
1. plan.md inteiro, para saber o que é desta fase e o que é das próximas.
2. spec.md: as seções que esta fase toca (Componentes, Contratos de interface, Modelo de dados,
   Tratamento de erros, Estratégia de testes) e Regras e fluxos. A spec manda na estrutura.
3. contract.md inteiro: Pré-requisitos e todos os itens. Os itens mandam no comportamento
   observável (status, corpo, efeito persistido, código de erro, texto da tela).
4. [Num RF: docs/features/fundacao/spec.md, seção "Convenções para as features".
    Na fundação: a seção dela mesma.] É onde estão seed, fixture, configuração de teste e mocks.
5. CLAUDE.md e, quando a fase mexer em comando ou ambiente, CONTRIBUTING.md.
Abra o código existente sob demanda, quando a fase precisar dele; não varra o repositório.

[As regras da seção 2 de references/fase.md, coladas aqui.]

Responda no formato da seção 4 de references/fase.md, [colado aqui].
```

## 2. O que o subagente faz

**Implementa os passos da fase, e só eles.** Passo de fase seguinte não se adianta: a fase seguinte vai ler o plano e esperar encontrar o terreno como o plano descreve.

**Desempate entre contrato e spec.** Quando a spec e um item do contrato falam da mesma coisa observável de fora e discordam, siga o item e registre "spec dizia X, item ID exige Y, segui Y". Estrutura interna (caminho, nome de classe, decomposição, coluna que nenhum item observa) segue a spec. Quando a realidade diverge (coluna com outro nome, arquivo noutro caminho), adapte o mínimo e registre. Divergência pequena não para a fase.

**Produz os pré-requisitos com a convenção do projeto.** Estado persistido vira factory ou seed no lugar que as Convenções indicam, com o handle no nome; entrada estática vira arquivo no caminho exato do contrato, com a propriedade que ele declara (duração, formato, chave que não está no JWKS); configuração vira chave no arquivo de configuração de teste, sem segredo real. O contrato descreve o que precisa ser verdade, não como criar: o como é da convenção.

**Escreve os testes que a Estratégia de testes da spec pede** junto do código da fase, no lugar e no nível que ela indica. Teste acompanha o passo; não existe fase de testes.

**Valida pelo `Makefile`.** `make lint` e `make test` ao fim da fase; `make build` quando a fase mexe no que é compilado. Na fase que cria os `scripts/<alvo>.sh`, eles passam a valer a partir daí; antes disso o alvo avisa e passa, e isso não é validação. Quando a fase cria uma superfície (rota, migração, comando, worker, tela), exercite-a uma vez de verdade: suba o que for preciso, chame a rota, rode a migração, abra a tela. Tela se confere num navegador, com a ferramenta que o projeto já usa; sem ferramenta de navegador no projeto, registre como pendência, não como feito.

**Documentação do repositório.** Se a fase muda um comando, uma variável de ambiente ou o jeito de subir o projeto, atualize `README.md` ou `CONTRIBUTING.md` na mesma fase. Se o que você construiu contradiz o HLD ou um ADR (um componente que precisou existir, uma interface que não cabe), não edite: registre em Pendências com a skill dona (`/hld-writer`, `/adr-writer`).

**Pare e devolva, sem improvisar,** quando a fase pedir tecnologia que nenhum ADR aceito nem a spec preveem, quando um passo for impossível como escrito, ou quando faltar decisão de produto. Devolva o status `precisa de decisão` com a pergunta pronta, as alternativas e a sua recomendação.

**Não faz:** commit, `git add`, criação de branch, edição de `docs/product/`, `docs/architecture/` ou da pasta `docs/features/` da feature, nem stub em código de produção.

## 3. Falhas

| Tipo | O que é | O que fazer |
|---|---|---|
| Real | Lint, tipos ou teste falham por código desta execução | Ler o erro, corrigir, rodar de novo. Até 3 tentativas; depois, status `falhou` com o erro |
| Do ambiente | A validação não consegue rodar aqui (Docker parado, credencial externa ausente, comando inexistente) | Não conta como tentativa. Registrar com o comando e a mensagem e seguir com o que dá |
| Anterior | Falha que já existia antes desta execução, em código que ela não tocou | Não conta como tentativa e não se corrige aqui. Registrar com a evidência (falha também sem as mudanças da fase) |

Aviso sem código de saída diferente de zero não é falha.

## 4. Retorno

```
Status: pronta | falhou | precisa de decisão
Arquivos: <caminhos criados ou alterados, um por linha>
Pré-requisitos produzidos: <handle ou caminho: onde ficou>
Validação: <comando: resultado, para cada comando rodado>
Superfícies exercitadas: <o que foi chamado ou aberto e o que se observou>
Desvios: <desempates e adaptações, um por linha>
Falhas do ambiente: <comando: mensagem>
Falhas anteriores: <teste: evidência>
Pendências: <o que ficou por fazer, ou divergência com HLD/ADR e a skill dona>
Pergunta: <só com status "precisa de decisão": pergunta, alternativas, recomendação>
```

## 5. Commit

Feito por você, o orquestrador, só com a autorização do Passo 1 e depois de conferir a validação. Para o formato, veja `CONTRIBUTING.md` seção "Mensagens de commit": tipo e escopo em inglês, descrição em português, em minúsculas, no imperativo, sem ponto final e com até 72 caracteres no cabeçalho. O hook `commit-msg` confere.

```
feat(<escopo>): <o resultado da fase, como no título do plano>

Fase <N> de <M> do plano de <RF-NNN | fundação>: passos <a> a <b>.
<desvio que quem revisa precisa saber, se houver>

Refs: <RF-NNN | fundacao>
Plan-Phase: <N>
```

- **Tipo**: `feat` para o comportamento do RF; na fundação, pelo conteúdo da fase (`build` para monorepo e ferramentas, `feat` para a API que passa a responder, `ci` para workflow).
- **Escopo**: o componente ou pacote principal da fase, em inglês e minúsculas (`api`, `worker`, `database`, `web`, `monorepo`).
- **Rodapés**: `Refs:` e `Plan-Phase:` são o que o `preparar.py` lê para pular fases já feitas numa retomada. Sem eles a retomada refaz a fase.
- Adicione os arquivos pelo nome, a partir da lista do retorno conferida com `git status`. Arquivo alterado que não é desta fase fica fora do commit.
- Hook falhou: corrija a mensagem e faça um commit novo. Nunca use `--no-verify` nem `--amend` num commit que não é desta execução.
