# Documentação

Toda a documentação do produto vive nesta pasta, organizada por tipo. Como trabalhar no
repositório (ambiente, verificações, fluxo, commits, release) fica na raiz, em `CONTRIBUTING.md`
e `README.md`; aqui ficam o produto e as decisões. Este arquivo é a fonte única das convenções:
as skills e os subagents o leem antes de escrever.

## Estrutura

| Pasta | O que guarda |
|---|---|
| `product/` | PRDs e o roadmap |
| `architecture/` | HLD, `diagrams/` e um documento por componente em `components/` |
| `adr/` | Architecture Decision Records, um por decisão |
| `features/` | Feature Design Documents (FDD), um por feature |
| `runbooks/` | Procedimentos operacionais |
| `guides/` | Guias para pessoas: onboarding, como fazer X |
| `templates/` | Modelos de cada tipo de documento |
| `_intake/` | Entrevistas e notas brutas; nada aqui é documentação final |

Cada pasta tem um `README.md` que funciona como índice; `make check-docs` avisa quando um documento
não está no índice da sua pasta. O `glossary.md` define os termos do domínio. A skill `docs-init`
cria essa árvore; o repositório do template versiona só `adr/`.

## Como navegar

Comece pelo PRD em `product/` para entender o que o produto faz e por quê. O HLD em
`architecture/` mostra como ele é construído. Cada escolha técnica tem um ADR em `adr/`, e cada
feature em desenvolvimento tem um FDD em `features/`. O roadmap em `product/roadmap.md` diz o que
está em andamento.

## Como criar um documento

- Documentação do zero ou atualização geral: skill `docs-init` ("documenta esse projeto").
- Decisão técnica: skill `adr` ("cria um ADR para X").
- Design de uma feature: skill `fdd` ("cria o FDD da feature Y").
- Auditoria: skill `docs-review` ("revisa a documentação").

Sem as skills, copie o modelo de `templates/`, siga as convenções e acrescente a linha no índice da
pasta.

## Nomes de arquivo

- kebab-case, sem acentos, sem espaços.
- Prefixo do tipo: `prd-`, `hld-`, `fdd-NNN-`. ADRs usam `NNNN-titulo.md`.
- Números com zeros à esquerda: ADR com 4 dígitos, FDD com 3. Número nunca é reutilizado.

## Frontmatter obrigatório

Todo documento começa com frontmatter YAML contendo pelo menos `title`, `type`, `status`, `date`
(ISO AAAA-MM-DD) e `owners`. No roadmap, `updated` faz o papel de `date`. Chaves extras são
permitidas e ignoradas pela validação.

Valores de `status` por tipo:

- adr: proposed, accepted, deprecated, superseded
- prd e hld: draft, review, approved, archived
- fdd: draft, review, approved, implemented
- roadmap: active, archived

## Regras por tipo

- ADR é imutável depois de `accepted`. Para mudar uma decisão, crie outro ADR, preencha
  `supersedes` no novo e `superseded_by` no antigo, e mude o status do antigo para `superseded`.
  O ADR nasce `proposed`; quem aceita é uma pessoa.
- PRD aponta para os FDDs que o implementam. FDD aponta para o PRD e para os ADRs que justificam
  suas escolhas. HLD referencia os ADRs estruturais.
- Roadmap: item sem link para PRD ou FDD é ideia, não compromisso. Nada é apagado; o que sai vai
  para "Adiado ou removido" com motivo e data.

## Links e diagramas

- Links sempre relativos ao arquivo atual, por exemplo `../adr/0001-usar-postgres.md`. Nunca
  caminhos absolutos do sistema de arquivos.
- Diagramas em Mermaid dentro do próprio Markdown. Imagens só quando Mermaid não resolve, salvas
  em `architecture/diagrams/`.

## Lacunas

- O que não foi respondido fica no texto como `[A CONFIRMAR: pergunta objetiva]`. A pergunta
  precisa ser respondível em uma frase. A validação conta as marcas.
- Nunca preencha métricas, prazos, nomes de pessoas ou tecnologias que não estejam na entrevista
  ou no código.

## Estilo

- Português do Brasil, frases curtas, sem travessões.
- Títulos de seção do template não devem ser renomeados nem removidos.
