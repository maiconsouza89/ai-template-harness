# CLAUDE.md

As instruções do projeto estão em @AGENTS.md (fonte única, lida por qualquer agente).

Específico do Claude Code:

- Preferências pessoais não versionadas vão em `CLAUDE.local.md` (já ignorado pelo Git).
- Regras por caminho, quando a stack existir, vão em `.claude/rules/`.
- Para registrar, auditar ou substituir um ADR, use a skill `/adr-writer` (`.claude/skills/adr-writer/`);
  ela segue as regras de `docs/ADR/README.md` e roda o mesmo `audit.py` de `make check-adr`.
