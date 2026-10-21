---
name: adr
description: Cria um novo Architecture Decision Record em docs/adr/ com numeração sequencial e atualiza o índice. Use sempre que o usuário quiser registrar, documentar ou formalizar uma decisão técnica ou de arquitetura, substituir uma decisão anterior, ou disser coisas como "vamos registrar que escolhemos X", "cria um ADR", "documenta essa decisão".
---

# adr

## Fluxo
1. Leia `docs/README.md` (convenções da documentação).
2. Se o usuário já descreveu a decisão, extraia contexto, decisão, motivo e alternativas. Se faltar algo, faça no máximo 4 perguntas, uma de cada vez com `AskUserQuestion`: qual problema motivou, o que foi escolhido, por quê, e quais alternativas foram descartadas. Cada pergunta traz 2 a 4 opções tiradas do que o usuário já disse e do código, com a recomendada em primeiro lugar e " (Recomendado)" no rótulo; "Outro" fica para resposta livre. O usuário corrige uma proposta melhor do que escreve do zero.
3. Pergunte se esta decisão substitui algum ADR existente. Liste os ADRs de `docs/adr/README.md` com status `accepted` como opções, mais "Nenhum" como recomendada quando nada parecer relacionado.
4. Rode `python3 .claude/skills/adr/scripts/new_adr.py "<título>" [--supersedes NNNN]`. O script cria o arquivo e atualiza o índice. Se `docs/adr/` não existir, rode antes `python3 .claude/skills/docs-init/scripts/scaffold.py`. Sem `docs/templates/adr.md`, o script usa o modelo da própria skill.
5. Preencha as seções do arquivo criado com o que foi coletado, inclusive `owners`. Alternativas e consequências não mencionadas ficam como `[A CONFIRMAR: ...]`.
6. Se houver HLD em `docs/architecture/`, adicione o novo ADR na seção "Decisões arquiteturais" dele.
7. Mostre o caminho do arquivo e peça para o usuário revisar antes de mudar o status para `accepted`.

## Regras
- Nunca edite o conteúdo de um ADR `accepted`. Só o status e `superseded_by` podem mudar.
- O ADR nasce como `proposed`. A mudança para `accepted` é decisão do usuário.
- Mantenha o ADR curto. Se o conteúdo crescer, provavelmente parte dele pertence a um FDD ou ao HLD.
- Português do Brasil, frases curtas, sem travessões.
