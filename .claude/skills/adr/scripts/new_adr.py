#!/usr/bin/env python3
"""Cria um ADR numerado a partir de docs/templates/adr.md e atualiza o índice.

Uso: python3 new_adr.py "Título da decisão" [--supersedes NNNN] [--root docs]
"""

import argparse
import datetime
import re
import sys
import unicodedata
from pathlib import Path

ADR_NAME_RE = re.compile(r"^(\d{4})-.*\.md$")
TABLE_HEADER = "| Número | Título | Status | Data |"


def slugify(title: str) -> str:
    text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "decisao"


def next_number(adr_dir: Path) -> int:
    highest = 0
    for path in adr_dir.glob("*.md"):
        match = ADR_NAME_RE.match(path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def set_frontmatter_value(text: str, key: str, value: str) -> str:
    """Troca o valor de uma chave do frontmatter sem tocar nas outras linhas."""
    lines = text.split("\n")
    if lines[0].strip() != "---":
        raise ValueError("arquivo sem frontmatter")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            break
        if re.match(rf"^{re.escape(key)}\s*:", lines[i]):
            lines[i] = f"{key}: {value}"
            return "\n".join(lines)
    raise ValueError(f"chave '{key}' não encontrada no frontmatter")


def render(template: str, number: str, title: str, today: str, supersedes: str) -> str:
    text = template
    text = set_frontmatter_value(text, "title", title)
    text = set_frontmatter_value(text, "number", number)
    text = set_frontmatter_value(text, "status", "proposed")
    text = set_frontmatter_value(text, "date", today)
    text = set_frontmatter_value(text, "supersedes", f"[{supersedes}]" if supersedes else "[]")
    text = re.sub(r"^# ADR-\d{4}: .*$", f"# ADR-{number}: {title}", text, count=1, flags=re.M)
    return text


def update_index(readme: Path, number: str, title: str, filename: str, today: str, superseded: str):
    if not readme.exists():
        print(f"aviso: {readme} não existe; índice não atualizado", file=sys.stderr)
        return
    lines = readme.read_text(encoding="utf-8").split("\n")
    row = f"| {number} | [{title}]({filename}) | proposed | {today} |"
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == TABLE_HEADER)
    except StopIteration:
        print(f"aviso: tabela '{TABLE_HEADER}' não encontrada em {readme}", file=sys.stderr)
        return
    end = start + 1
    while end < len(lines) and lines[end].startswith("|"):
        if superseded and lines[end].startswith(f"| {superseded} |"):
            cells = [c.strip() for c in lines[end].strip().strip("|").split("|")]
            if len(cells) >= 3:
                cells[2] = "superseded"
                lines[end] = "| " + " | ".join(cells) + " |"
        if lines[end].startswith(f"| {number} |"):
            return
        end += 1
    lines.insert(end, row)
    readme.write_text("\n".join(lines), encoding="utf-8")


def supersede(adr_dir: Path, old_number: str, new_number: str) -> Path:
    matches = [p for p in adr_dir.glob(f"{old_number}-*.md")]
    if not matches:
        raise SystemExit(f"erro: ADR {old_number} não encontrado em {adr_dir}")
    old = matches[0]
    text = old.read_text(encoding="utf-8")
    text = set_frontmatter_value(text, "superseded_by", f"[{new_number}]")
    text = set_frontmatter_value(text, "status", "superseded")
    old.write_text(text, encoding="utf-8")
    return old


def main() -> int:
    parser = argparse.ArgumentParser(description="Cria um ADR novo e atualiza o índice.")
    parser.add_argument("title", help="título curto da decisão")
    parser.add_argument("--supersedes", metavar="NNNN", help="número do ADR que esta decisão substitui")
    parser.add_argument("--root", default="docs", help="pasta raiz da documentação (padrão: docs)")
    args = parser.parse_args()

    root = Path(args.root)
    adr_dir = root / "adr"
    template = root / "templates" / "adr.md"
    if not adr_dir.is_dir():
        print(f"erro: pasta {adr_dir} não existe; rode o scaffold.py antes", file=sys.stderr)
        return 1
    if not template.exists():
        print(f"erro: template {template} não encontrado", file=sys.stderr)
        return 1

    supersedes = args.supersedes.zfill(4) if args.supersedes else ""
    number = f"{next_number(adr_dir):04d}"
    today = datetime.date.today().isoformat()
    filename = f"{number}-{slugify(args.title)}.md"
    target = adr_dir / filename
    if target.exists():
        print(f"erro: {target} já existe", file=sys.stderr)
        return 1

    content = render(template.read_text(encoding="utf-8"), number, args.title, today, supersedes)
    if supersedes:
        supersede(adr_dir, supersedes, number)
    target.write_text(content, encoding="utf-8")
    update_index(adr_dir / "README.md", number, args.title, filename, today, supersedes)
    print(target.as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
