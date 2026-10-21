# Documentação

Toda a documentação do projeto vive nesta pasta, organizada por tipo. Documentos do próprio
repositório (como `ARCHITECTURE.md`, `SETUP.md` ou `TESTING.md`) ficam na raiz de `docs/`; os
documentos do produto ficam nas subpastas abaixo.

## Estrutura

| Pasta | O que guarda |
|---|---|
| `product/` | PRDs e o roadmap |
| `architecture/` | HLD, diagramas e um documento por componente em `components/` |
| `adr/` | Architecture Decision Records, um por decisão |
| `features/` | Feature Design Documents (FDD), um por feature |
| `runbooks/` | Procedimentos operacionais |
| `guides/` | Guias para pessoas: onboarding, como fazer X |
| `templates/` | Modelos de cada tipo de documento |
| `_intake/` | Entrevistas e notas brutas; nada aqui é documentação final |

Cada pasta tem um `README.md` que funciona como índice. O `glossary.md` define os termos do domínio.

## Como navegar

Comece pelo PRD em `product/` para entender o que o produto faz e por quê. O HLD em
`architecture/` mostra como ele é construído. Cada escolha técnica tem um ADR em `adr/`, e cada
feature em desenvolvimento tem um FDD em `features/`. O roadmap em `product/roadmap.md` diz o que
está em andamento.

## Como criar um documento novo

- Documentação do zero ou atualização geral: skill `docs-init` ("documenta esse projeto").
- Decisão técnica: skill `adr` ("cria um ADR para X").
- Design de uma feature: skill `fdd` ("cria o FDD da feature Y").
- Auditoria: skill `docs-review` ("revisa a documentação").

Sem as skills, copie o modelo de `templates/` e siga as convenções.

## Convenções principais

1. Todo documento começa com frontmatter YAML: `title`, `type`, `status`, `date` e `owners`.
2. Nomes em kebab-case sem acento; ADR é `NNNN-titulo.md`, FDD é `fdd-NNN-titulo.md`.
3. ADR aceito é imutável: outra decisão vira um ADR novo com `supersedes` e `superseded_by`.
4. O que não se sabe fica no texto como `[A CONFIRMAR: pergunta objetiva]`, nunca como suposição.
5. Links sempre relativos ao arquivo atual; diagramas em Mermaid dentro do Markdown.
