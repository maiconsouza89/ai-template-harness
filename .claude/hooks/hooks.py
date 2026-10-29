"""Hooks do Claude Code deste repositório. Lê o JSON do evento no stdin.

Uso (via run.sh, chamado por .claude/settings.json):
  python3 hooks.py push       PreToolUse do Bash: bloqueia git push forçado
  python3 hooks.py subagent   SubagentStop: roda make lint e make test se o subagente editou código

Exit 2 bloqueia e o stderr vira a mensagem que o Claude recebe; exit 0 deixa seguir.
Documentação: https://code.claude.com/docs/en/hooks
"""

import json
import os
import re
import shlex
import subprocess
import sys

# Caracteres que o shell trata como operador: separam comandos (`;`, `&&`, `|`, linha nova),
# abrem subshell ou substituição (`(`, `$(`, crase) e redirecionam. Viram tokens próprios.
OPERATORS = "();<>|&`\n"
# Fallback para aspas desbalanceadas, quando o shlex desiste.
SEGMENT = re.compile(r"&&|\|\||\$\(|[;|&\n()`]")
# Comandos que executam o seguinte (`sudo git push`) e as opções deles que levam valor.
WRAPPERS = {"command", "env", "exec", "nice", "nohup", "sudo", "time", "{"}
WRAPPER_OPTS_WITH_VALUE = {"-u", "-g", "-C", "-n"}
SHELLS = {"sh", "bash", "dash", "zsh", "ksh"}
# Opções globais do git que levam valor antes do subcomando (`git -C dir push`).
GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
# Ferramentas que editam arquivo; edição por Bash (sed -i) não aparece aqui.
EDIT_TOOLS = {"Edit", "Write", "NotebookEdit"}
# Linhas finais da saída do make que voltam ao subagente: o erro costuma estar no fim.
TAIL_LINES = 40


def forced(tokens):
    """True se os tokens depois de `push` forçam a reescrita do remoto."""
    for t in tokens:
        if t in ("--force", "-f") or t.startswith("--force-with-lease") or t.startswith("--force-if-includes"):
            return True
        if re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*", t):  # -f agrupado com outras curtas, como -uf
            return True
        if t.startswith("+"):  # refspec com + força aquela referência
            return True
    return False


def segments(command):
    """Comandos simples de `command`, cada um como lista de palavras já sem aspas."""
    try:
        lex = shlex.shlex(command, posix=True, punctuation_chars=OPERATORS)
        lex.whitespace = " \t\r"  # linha nova é separador de comando, não espaço
        lex.whitespace_split = True
        tokens = list(lex)
    except ValueError:  # aspas desbalanceadas: corta pelos operadores e tira as aspas à mão
        return [[t.strip("\"'") for t in s.split()] for s in SEGMENT.split(command)]
    out, current = [], []
    for t in tokens:
        if t == "$" or all(c in OPERATORS for c in t):
            out.append(current)
            current = []
        else:
            current.append(t)
    out.append(current)
    return out


def strip_prefix(tokens):
    """Tira VAR=valor e comandos que executam o seguinte (`sudo -u x`, `env`, `command`)."""
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", t):
            i += 1
        elif os.path.basename(t) in WRAPPERS:
            i += 1
            while i < len(tokens) and tokens[i].startswith("-"):
                i += 2 if tokens[i] in WRAPPER_OPTS_WITH_VALUE else 1
        else:
            break
    return tokens[i:]


def push_command(command, depth=0):
    for tokens in segments(command):
        tokens = strip_prefix(tokens)
        if not tokens:
            continue
        name = os.path.basename(tokens[0])
        # `sh -c "git push -f"`: o push vem como string; confere o que ela executa.
        if name in SHELLS and depth < 3:
            for j, t in enumerate(tokens[1:-1], start=1):
                if re.fullmatch(r"-[a-zA-Z]*c[a-zA-Z]*", t):
                    found = push_command(tokens[j + 1], depth + 1)
                    if found:
                        return found
            continue
        if name != "git":  # git por caminho completo (/usr/bin/git) também conta
            continue
        i = 1
        while i < len(tokens) and tokens[i].startswith("-"):
            i += 2 if tokens[i] in GIT_OPTS_WITH_VALUE else 1
        if i < len(tokens) and tokens[i] == "push" and forced(tokens[i + 1:]):
            return " ".join(tokens)
    return None


def hook_push(event):
    command = (event.get("tool_input") or {}).get("command") or ""
    found = push_command(command)
    if found:
        print(
            f"bloqueado: `{found}` reescreve o histórico do remoto, e a regra do repositório é nunca "
            "forçar push. Resolva com merge ou um commit novo. Se a pessoa pediu o push forçado, "
            "ela roda à mão com `! git push ...`.",
            file=sys.stderr,
        )
        return 2
    return 0


def edited_code(transcript, root):
    """Caminhos editados pelo subagente fora de docs/ (documentação não passa por lint e test)."""
    paths = []
    try:
        lines = open(transcript, encoding="utf-8")
    except OSError:
        return paths
    with lines:
        for line in lines:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            message = entry.get("message")
            content = message.get("content") if isinstance(message, dict) else None
            for item in content if isinstance(content, list) else []:
                if not isinstance(item, dict) or item.get("type") != "tool_use" or item.get("name") not in EDIT_TOOLS:
                    continue
                path = (item.get("input") or {}).get("file_path") or (item.get("input") or {}).get("notebook_path")
                if not path:
                    continue
                rel = os.path.relpath(path, root) if os.path.isabs(path) else path
                if not rel.startswith("docs" + os.sep):
                    paths.append(rel)
    return paths


def hook_subagent(event):
    if event.get("stop_hook_active"):
        return 0  # já bloqueou uma vez: deixa encerrar, para falha que não é do subagente não virar laço
    cwd = event.get("cwd") or os.getcwd()
    try:
        root = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return 0
    if not edited_code(event.get("agent_transcript_path") or "", root):
        return 0
    for target in ("lint", "test"):
        run = subprocess.run(["make", target], cwd=root, capture_output=True, text=True)
        if run.returncode != 0:
            tail = "\n".join((run.stdout + run.stderr).strip().split("\n")[-TAIL_LINES:])
            print(
                f"`make {target}` falhou depois das suas edições. Corrija e rode `make lint` e "
                f"`make test` de novo antes de encerrar. Se a falha já existia antes e não é do "
                f"seu código, registre como falha anterior no retorno, com a evidência.\n\n{tail}",
                file=sys.stderr,
            )
            return 2
    return 0


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0  # entrada que não é JSON: o hook não é o lugar de travar a sessão
    hooks = {"push": hook_push, "subagent": hook_subagent}
    if len(sys.argv) != 2 or sys.argv[1] not in hooks:
        print(f"uso: hooks.py {{{'|'.join(hooks)}}}", file=sys.stderr)
        return 1
    return hooks[sys.argv[1]](event)


if __name__ == "__main__":
    sys.exit(main())
