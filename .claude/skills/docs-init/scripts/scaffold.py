#!/usr/bin/env python3
"""Cria a árvore de docs/ e os arquivos de índice.

Uso: python3 scaffold.py [--root docs] [--force]

Idempotente: nunca sobrescreve README existente; templates só com --force.
"""

import argparse
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"
# A fonte das convenções é docs/README.md do repositório que contém a skill (.claude/skills/docs-init).
REPO_DOCS_README = SKILL_DIR.parents[2] / "docs" / "README.md"

FOLDERS = [
    "product",
    "architecture",
    "architecture/diagrams",
    "architecture/components",
    "adr",
    "features",
    "runbooks",
    "guides",
    "templates",
    "_intake",
]

# Pastas sem README recebem .gitkeep para o Git versionar a pasta.
KEEP = ["architecture/diagrams"]

INDEX_TABLE = "| Documento | Tipo | Status | Atualizado |\n|---|---|---|---|\n"

READMES = {
    "README.md": """# Documentação

Documentação do projeto organizada por tipo: `product/` (PRD, roadmap), `architecture/` (HLD,
componentes), `adr/` (decisões), `features/` (FDD), `runbooks/`, `guides/`, `templates/` (modelos)
e `_intake/` (entrevistas brutas). Cada pasta tem um `README.md` como índice.

[A CONFIRMAR: este repositório não tem docs/README.md com as convenções; copie o do template
ai-template-harness ou escreva as convenções aqui.]
""",
    "glossary.md": """# Glossário

| Termo | Definição |
|---|---|
""",
    "product/README.md": "# Produto\n\n" + INDEX_TABLE,
    "architecture/README.md": (
        "# Arquitetura\n\n"
        + INDEX_TABLE
        + "\n`components/` guarda um arquivo por serviço ou módulo, com o detalhe que não cabe no HLD.\n"
    ),
    "architecture/components/README.md": (
        "# Componentes\n\n| Componente | Responsabilidade | Doc |\n|---|---|---|\n"
    ),
    "adr/README.md": """# Architecture Decision Records

ADRs são imutáveis depois de aceitos: uma decisão muda por meio de um ADR novo, que preenche
`supersedes`, enquanto o antigo recebe `superseded_by` e o status `superseded`.

| Número | Título | Status | Data |
|---|---|---|---|
""",
    "features/README.md": "# Features\n\n| Número | Feature | Status | PRD |\n|---|---|---|---|\n",
    "runbooks/README.md": (
        "# Runbooks\n\nProcedimentos operacionais passo a passo: deploy, rotação de segredos, "
        "resposta a incidentes, restauração de backup.\n"
    ),
    "guides/README.md": (
        "# Guias\n\nGuias para pessoas: onboarding, ambiente local, como contribuir com cada "
        "parte do sistema.\n"
    ),
    "_intake/README.md": """# Intake

Esta pasta guarda entrevistas e notas brutas, como `entrevista-AAAA-MM-DD.md`. Nada aqui é
documentação final. Os arquivos são a fonte que os subagents usam para escrever PRD, HLD e ADRs,
então registram o que o usuário disse, de forma completa e literal.
""",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Cria a árvore de docs/ e os índices.")
    parser.add_argument("--root", default="docs", help="pasta raiz da documentação (padrão: docs)")
    parser.add_argument("--force", action="store_true", help="sobrescreve os templates já copiados")
    args = parser.parse_args()

    root = Path(args.root)
    if not TEMPLATES_DIR.is_dir():
        print(f"erro: pasta de templates não encontrada: {TEMPLATES_DIR}", file=sys.stderr)
        return 1

    for folder in [""] + FOLDERS:
        path = root / folder if folder else root
        if path.is_dir():
            print(f"pulado: {path}/ já existe")
        else:
            path.mkdir(parents=True)
            print(f"criado: {path}/")

    for folder in KEEP:
        keep = root / folder / ".gitkeep"
        if keep.exists():
            print(f"pulado: {keep} já existe")
        else:
            keep.write_text("", encoding="utf-8")
            print(f"criado: {keep}")

    for template in sorted(TEMPLATES_DIR.glob("*.md")):
        target = root / "templates" / template.name
        if target.exists() and not args.force:
            print(f"pulado: {target} já existe")
            continue
        shutil.copyfile(template, target)
        print(f"criado: {target}")

    for relative, content in READMES.items():
        target = root / relative
        if target.exists():
            print(f"pulado: {target} já existe")
            continue
        if relative == "README.md" and REPO_DOCS_README.is_file():
            shutil.copyfile(REPO_DOCS_README, target)
            print(f"criado: {target} (copiado de {REPO_DOCS_README})")
            continue
        target.write_text(content, encoding="utf-8")
        print(f"criado: {target}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
