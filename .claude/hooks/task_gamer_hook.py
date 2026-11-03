"""Claude Code hook: keep the ``task-gamer`` agent inside its participant kit.

Wired in ``.claude/settings.json`` as a ``PreToolUse`` hook on every tool. It acts only on calls whose hook input names
the agent (``agent_type == "task-gamer"``); the main session and the other agents pass untouched. The gamer works as a
benchmark participant: it may read and write inside a folder whose path has a ``participant_kit`` component (written
by ``clean_room.py --participant``) and search the web, and nothing else: no repository file, no skill, no record, no
memory. A call that leaves the kit is denied with the reason, which the agent sees.

The checks are a guard against browsing, not against a determined escape: a Python script can still build a path the
check does not see. The agent's brief forbids that; a report that cites our files is discarded
(``review_panel.md``). For the gamer the hook fails closed: an error denies the call.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

AGENT = "task-gamer"
KIT = "participant_kit"
FILE_TOOLS = {"Read", "Write", "Edit", "NotebookEdit"}
SEARCH_TOOLS = {"Glob", "Grep"}
WEB_TOOLS = {"WebFetch", "WebSearch"}
# Absolute paths a command may name outside the kit: the interpreter, system binaries and devices.
SYSTEM_PATH = re.compile(r"^(/usr/|/bin/|/dev/null$|/dev/std|/proc/(cpuinfo|meminfo)$|.*/\.venv/bin/python[0-9.]*$)")
# Names that only lead to our notes, rules or code, a parent folder, or a second change of folder.
FORBIDDEN = re.compile(
    r"\.claude|CLAUDE\.md|AGENTS\.md|curation|datasets/_dev|data_foundry|\.git\b|\bgit\b|(^|\s)~(/|\s|$)|\$HOME"
    r"|(^|[\s/'\"])\.\.(\s|$|/|['\"])|\b(cd|pushd|chdir)\b"
)
ABSOLUTE = re.compile(r"(?<![\w.$-])(/[^\s'\"`;|&<>(){}]+)")
WEB_URL = re.compile(r"https?://[^\s'\"`]+")  # downloads into the kit are fine; file:// stays a path
LEADING_CD = re.compile(r"^\s*cd\s+(['\"]?)(/[^'\"\s;&|]+)\1\s*(&&|;|\n)")


def in_kit(path: str | None) -> bool:
    """Whether an absolute ``path`` lies in a participant kit."""
    if not path:
        return False
    normal = Path(os.path.normpath(path))  # normpath folds "..", Path does not
    return normal.is_absolute() and KIT in normal.parts


def check_bash(command: str) -> str | None:
    """Why ``command`` leaves the kit, or ``None``."""
    match = LEADING_CD.match(command)
    if not match or not in_kit(match.group(2)):
        return f"start every command with `cd <your {KIT} folder> &&`."
    command = command[: match.end()] + WEB_URL.sub("<url>", command[match.end() :])
    for path in ABSOLUTE.findall(command):
        if not in_kit(path) and not SYSTEM_PATH.match(path):
            return f"the command names {path}, which is outside your kit."
    # The allowed paths may contain any name (the repository's own folder), so they are blanked before the names check.
    rest = ABSOLUTE.sub("<path>", command[match.end() :])
    if hit := FORBIDDEN.search(rest):
        return f"the command names {hit.group(0).strip()!r}, which leads outside your kit."
    return None


def check_search(args: dict) -> str | None:
    """Why a Glob or Grep call leaves the kit, or ``None``."""
    if not in_kit(args.get("path")):
        return f"give `path` as your {KIT} folder (or a folder in it)."
    pattern = str(args.get("pattern", ""))
    return "the pattern leaves your kit." if pattern.startswith("/") or ".." in pattern else None


def check(tool: str, args: dict) -> str | None:
    """Why the gamer's call of ``tool`` with ``args`` is denied, or ``None`` to let it run."""
    if tool in WEB_TOOLS:
        return None
    if tool in FILE_TOOLS:
        path = args.get("file_path") or args.get("notebook_path")
        return None if in_kit(path) else f"{path} is outside your {KIT} folder."
    if tool in SEARCH_TOOLS:
        return check_search(args)
    if tool == "Bash":
        return check_bash(str(args.get("command", "")))
    return f"{tool} is not available to you."


def deny(reason: str) -> dict:
    """The hook's answer that blocks the call."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Sandbox: {reason} You work only with the files of your participant kit.",
        }
    }


def main() -> int:
    """Read the hook's JSON from stdin and print a denial, if any."""
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return 0
    if payload.get("agent_type") != AGENT:
        return 0
    try:
        reason = check(str(payload.get("tool_name", "")), payload.get("tool_input") or {})
    except Exception as exc:  # noqa: BLE001 - for the gamer the hook fails closed
        reason = f"the sandbox check failed ({exc})."
    if reason:
        print(json.dumps(deny(reason)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
