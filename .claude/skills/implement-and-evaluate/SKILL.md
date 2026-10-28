---
name: implement-and-evaluate
description: Leva um RF-NNN (ou a fundação) de `spec.md`, `plan.md` e `contract.md` até uma avaliação limpa sem a pessoa intervir entre os ciclos - roda `/implement-feature`, depois alterna `/evaluator` (veredito) e `/fix-runner` (correção) até o contrato passar, o orçamento de ciclos acabar ou o laço travar. Com autorização dada no início, fecha o trabalho - merge da `main` no branch, reavaliação, push e PR no formato do repositório, com `Closes #N` da issue do RF. Mantém o diário `docs/features/<pasta>/orquestracao.md`, atualizado a cada ciclo. Use sempre que o usuário quiser implementar e validar de ponta a ponta, "do contrato ao PR", "implementa e avalia o RF-003", "roda o ciclo completo da fundação", "faz até passar", "entrega o RF-002", mesmo sem dizer implement-and-evaluate.
---

# Implement and Evaluate

Orquestra três skills num laço de verificar e corrigir, para que um RF especificado chegue a uma avaliação limpa sem alguém conduzir cada ciclo:

1. **`/implement-feature`**, uma vez, no ciclo 0: fases do plano, pré-requisitos do contrato, prontidão preliminar.
2. **`/evaluator`**, depois de toda mudança de código: o veredito, gravado em `avaliacao.md`.
3. **`/fix-runner`**, a partir do ciclo 1: corrige os itens que a avaliação reprovou ou bloqueou.

Você, aqui, só orquestra: não edita código, contrato, spec nem plano. Escreve o diário, o status do roadmap nos casos da seção "Roadmap" e os commits de registro, e fecha o trabalho com push e PR quando autorizado.

**Onde cada skill roda.** A `/implement-feature` roda **nesta conversa**, pela ferramenta Skill: ela já despacha um subagente por fase, e subagente não pode criar subagente ([documentação do Claude Code](https://code.claude.com/docs/en/sub-agents)). `/evaluator` e `/fix-runner` rodam cada uma num subagente `general-purpose` novo, com os modelos de `references/subagentes.md`: assim cada veredito começa sem a memória de quem implementou, e o contexto daqui continua pequeno ao longo dos ciclos.

## Entrada

O alvo e, opcionalmente, em linguagem natural:

| Pedido | Efeito | Padrão |
|---|---|---|
| "até N ciclos", "sem ciclos de correção", "ciclos sem limite" | Orçamento de ciclos de correção | 3 |
| "pausa entre ciclos" | Espera um ok antes de cada ciclo | autônomo |
| "mantém o ambiente no fim" | Sem sucesso, roda uma última `/evaluator` com "mantém o ambiente" para inspeção | não |

O resto do pedido ("só as fases 1 e 2", "pausa entre fases") vai para a `/implement-feature`. `/evaluator` e `/fix-runner` rodam sempre no padrão, para o veredito e a correção serem reproduzíveis.

## Passo 0: preparar e autorizar

1. **Preparar.** Rode `python3 .claude/skills/implement-feature/scripts/preparar.py <alvo>` e aplique os bloqueios da `/implement-feature` (Passo 0 dela). Bloqueio para tudo aqui: nada de laço sobre uma base que não pode ser implementada.
2. **Trava.** Arquivo `<tmp do sistema>/implement-and-evaluate-<alvo>.lock` com `<PID> <execução>`. PID vivo (`kill -0`): pare, "outra execução de <alvo> em andamento, PID <N>". PID morto: sobrescreva e registre em Avisos. Apague a trava em qualquer saída.
3. **Autorizar**, numa chamada de `AskUserQuestion`, cobrindo a execução inteira (o `CLAUDE.md` exige autorização explícita, e ela vale só para esta execução):
   - **Branch**: na `main`, criar o que a ficha sugere; fora dela, seguir no atual.
   - **Commits**: das fases, das correções e do registro (`avaliacao.md`, `orquestracao.md`, roadmap). Recomendado sim; sem commits o laço não funciona, porque a `/evaluator` avalia o HEAD e a retomada se perde. Com não, pare e sugira rodar as skills uma a uma.
   - **Fechamento**: no sucesso, merge de `origin/main` no branch, push e PR (seção "Fechamento"). Recomendado sim; com não, o laço termina no veredito e imprime os comandos.

   Essa pergunta substitui o Passo 1 da `/implement-feature`: ao invocá-la, diga que branch e commits já foram decididos, com as respostas.
4. **Diário.** Escreva `docs/features/<pasta>/orquestracao.md` com `references/diario.md`, status `em execução`, sobrescrevendo o de execuções anteriores (o histórico fica no git).

## Passo 1: ciclo 0

Invoque `/implement-feature <alvo>` com o resto do pedido. Do relatório dela, guarde status, fases commitadas e o total. Registre no diário.

- Parou antes da primeira fase (bloqueio, decisão pendente): `abortado`. Vá para Finalizar.
- Qualquer outro status, inclusive `incompleto` e `com regressões`: siga para a avaliação. O veredito é da `/evaluator`, não da prontidão preliminar.

## Passo 2: laço de verificação

Guarde `falhou_antes` e `passou_antes`, vazios no começo, e `ciclo = 0`.

**2.1 Avaliar.** Despache a `/evaluator` com o modelo de `references/subagentes.md`. Do retorno: status, itens por veredito e critérios. Registre a linha do ciclo no diário.

**2.2 Decidir**, nesta ordem:

1. `limpo`: **sucesso**. Vá para Fechamento.
2. `pendente` sem nenhum `falhou` nem `bloqueado` (só `manual`): **manual pendente**. Nenhum ciclo de correção resolve revisão de pessoa. Vá para Finalizar.
3. **Travado**: `ciclo ≥ 1`, o conjunto `falhou` igual a `falhou_antes`, nenhum item novo em `passou` e pelo menos um `falhou`. Corrigir de novo do mesmo jeito só gasta orçamento. Vá para Finalizar.
4. **Esgotado**: `ciclo` igual ao orçamento. Vá para Finalizar.
5. Qualquer outro (`reprovado`, `reprovado no gate`, `pendente` com bloqueados, `abortado no passo`, `abortado no item` por serviço que caiu): corrigir.

Atualize `falhou_antes` e `passou_antes`.

**2.3 Corrigir.** `ciclo += 1`. Despache a `/fix-runner` (modelo em `references/subagentes.md`) com os itens `falhou` mais os `bloqueado`, nunca os `manual`. Avaliação abortada sem itens vai com a lista vazia: a `/fix-runner` lê o "Motivo do aborto". Registre no diário.

- `corrigido`: volte a 2.1.
- `validação falhou`: o ciclo foi gasto e não há código novo para avaliar. Volte a 2.2 com os mesmos dados; o travamento ou o orçamento encerram se for o caso.
- `abortado` (correção exigiria mudar o trio, só itens manuais, nada a mudar): **abortado**. Vá para Finalizar.

Com "pausa entre ciclos", espere um ok antes de 2.1 e de 2.3. Texto que não é ok vale como pedido para a próxima `/fix-runner`.

## Fechamento

Só com sucesso e autorização. Siga `references/fechamento.md`: o branch não pode ser a `main`; faça o merge de `origin/main`, com conflito resolvido pela `/fix-runner` no modo conflito; se o merge trouxe código, avalie de novo (resultado não limpo volta ao laço, com o orçamento que sobrou, e um merge só por execução); commit de registro; push; PR existente ou novo, no template do repositório, com `Closes #N` quando houver issue aberta do RF. Conflito sem solução termina em **pr bloqueado**.

Push, PR e merge só acontecem aqui, nunca durante o laço. Nunca `push --force`.

## Finalizar

1. Sem sucesso e com "mantém o ambiente no fim": uma última `/evaluator` com "mantém o ambiente", registrada no diário como informativa.
2. Feche o diário: status final, ciclos, commits, últimos itens reprovados e bloqueados, PR ou o motivo de não ter aberto, avisos.
3. **Roadmap** (só RF): `limpo` a `/evaluator` já marcou `feito`; `manual pendente` não muda. Em `travado`, `esgotado` e `abortado`, acrescente o contexto do laço: `roadmap.py set RF-NNN "em andamento" --motivo "<status> após <N> ciclos; ver orquestracao.md"`. Em `pr bloqueado`, volte o `feito` que a avaliação deu: `roadmap.py set RF-NNN "em andamento" --motivo "conflito com a main sem solução"`.
4. Commit de registro, se autorizado e ainda não feito no Fechamento: `docs(<escopo>): registra avaliação de <RF-NNN | fundação>`, com `avaliacao.md`, `orquestracao.md` e o roadmap, rodapé `Refs:`.
5. Apague a trava.
6. Relatório no chat:

```
Implement and Evaluate: <RF-NNN Nome | fundação>
Status: sucesso | manual pendente | travado | esgotado | abortado | pr bloqueado
Ciclos: <N> (implementação + <N> correções)   Branch: <branch>

Ciclos
  0  implement-feature  <status>        fases <X>/<Y>
  0  evaluator          <status>        passou <P>, falhou <F>, bloqueado <B>, manual <M>
  1  fix-runner         <status>        <sha | sem commit>
  1  evaluator          <status>        ...

PR: aberto <url> | atualizado <url> | não aberto: <motivo e comando para fazer à mão>
Avaliação: docs/features/<pasta>/avaliacao.md
Diário: docs/features/<pasta>/orquestracao.md
Avisos: <linhas>
Próximo passo: <revisar o PR | itens manuais a revisar | o que travou e quem resolve>
```

## Regras que não se negociam

Cada uma existe porque a alternativa já deu errado em algum lugar:

- **Toda mudança de código é seguida de avaliação.** A prontidão da `/implement-feature` e o "corrigido" da `/fix-runner` não são veredito.
- **Itens manuais nunca vão para correção.** São subjetivos; mandar para a `/fix-runner` gasta ciclo à toa.
- **Laço travado para.** Mesmo conjunto de falhas sem nenhum avanço é sinal de que a correção não converge; seguir só queima orçamento e tokens.
- **A `/implement-feature` roda uma vez.** Correção é da `/fix-runner`; reimplementar desfaz commits por fase e confunde a retomada.
- **Autorização da pergunta inicial, e só dela.** Commits, merge, push e PR acontecem porque a pessoa disse sim no Passo 0; com não, a skill para e entrega os comandos.
- **Sem sucesso com pendência.** Diário com item reprovado, bloqueado ou gate vermelho não termina em sucesso.
- **Sem travessão** "—" no diário, nos commits e no PR.
