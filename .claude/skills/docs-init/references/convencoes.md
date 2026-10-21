# Convenções da documentação

## Estrutura
- Toda a documentação vive em `docs/`, organizada por tipo: product, architecture, adr, features, runbooks, guides.
- Cada pasta tem um README.md que funciona como índice.
- `docs/templates/` guarda os modelos. `docs/_intake/` guarda entrevistas e notas brutas; nada ali é documentação final.
- Documentos do próprio repositório que ficam na raiz de `docs/` (por exemplo `ARCHITECTURE.md`, `SETUP.md`) não seguem estas convenções e não são validados.

## Nomes de arquivo
- kebab-case, sem acentos, sem espaços.
- Prefixo do tipo: `prd-`, `hld-`, `fdd-NNN-`. ADRs usam `NNNN-titulo.md`.
- Números com zeros à esquerda: ADR com 4 dígitos, FDD com 3.

## Frontmatter obrigatório
Todo documento começa com frontmatter YAML contendo pelo menos `title`, `type`, `status`, `date` (ISO AAAA-MM-DD) e `owners`. No roadmap, `updated` faz o papel de `date`. Chaves extras são permitidas e ignoradas pela validação.

Valores de `status` por tipo:
- adr: proposed, accepted, deprecated, superseded
- prd e hld: draft, review, approved, archived
- fdd: draft, review, approved, implemented
- roadmap: active, archived

## Regras por tipo
- ADR é imutável depois de `accepted`. Para mudar uma decisão, crie outro ADR, preencha `supersedes` no novo e `superseded_by` no antigo, e mude o status do antigo para `superseded`.
- PRD aponta para os FDDs que o implementam. FDD aponta para o PRD e para os ADRs que justificam suas escolhas. HLD referencia os ADRs estruturais.
- Roadmap: item sem link para PRD ou FDD é ideia, não compromisso. Nada é apagado; o que sai vai para "Adiado ou removido" com motivo e data.

## Links
- Sempre relativos ao arquivo atual, por exemplo `../adr/0001-usar-postgres.md`.
- Nunca links absolutos para o sistema de arquivos.

## Lacunas
- O que não foi respondido fica no texto como `[A CONFIRMAR: pergunta objetiva]`. A pergunta precisa ser respondível em uma frase.
- Nunca preencha métricas, prazos, nomes de pessoas ou tecnologias que não estejam na entrevista ou no código.

## Diagramas
- Mermaid dentro do próprio Markdown. Imagens só quando Mermaid não resolve, salvas em `docs/architecture/diagrams/`.

## Estilo
- Português do Brasil, frases curtas, sem travessões.
- Títulos de seção do template não devem ser renomeados nem removidos.
