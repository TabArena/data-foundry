"""Claude Code hook: tell the agent who holds which dataset (the live claims board), and warn before it edits one.

Wired in ``.claude/settings.json``:

* ``SessionStart``: fetches the board and adds it to the session's context: the other curators' claims, your own,
  and yours that expire within two days.
* ``PreToolUse`` on ``Edit|Write|NotebookEdit``: when the file belongs to a dataset (``curation/records/<name>.md``
  or ``datasets/_dev/<copy>/<name>/...``) that another curator holds, shows a warning to the user and to the agent.
  It never allows or denies anything: claims are advisory, and the normal permission flow goes on.

The board is re-fetched at most every 60 s (else the cache of the last fetch is used). The hook fails open: without
the package, a curator name, the network or a board it prints nothing and exits 0.
"""

from __future__ import annotations

import json
import re
import sys

PATTERNS = (
    re.compile(r"/curation/records/([^/]+)\.md$"),
    re.compile(r"/datasets/_dev/[^/]+/([^/_.][^/]*)/"),
)
MAX_NAMES = 60


def dataset_of(path: str) -> str | None:
    """The dataset a file belongs to, or ``None``."""
    path = path.replace("\\", "/")
    for pattern in PATTERNS:
        match = pattern.search(path)
        if match:
            return match.group(1)
    return None


def _names(items: list) -> str:
    names = [c.name for c in items]
    head = ", ".join(names[:MAX_NAMES])
    return head + (f" and {len(names) - MAX_NAMES} more" if len(names) > MAX_NAMES else "")


def session_start(claims) -> dict:
    """The board as context for the agent."""
    board = claims.load(max_age=0)
    me = claims.configured_curator()
    lines = [
        f"Dataset claims (the live board on {board.remote}/{board.branch}, fetched at session start). A claim covers "
        "a dataset's curation record and its v2 folder. Do not work on a dataset another curator holds; ask the user "
        "first. Commands: `data-foundry-curation claims list|claim|release|renew|check`.",
    ]
    if not me:
        lines.append(f"No curator name is set: `git config {claims.CURATOR_GIT_KEY} <Name>` before claiming.")
    others = {h: items for h, items in board.by_holder().items() if h != me}
    mine = [c for c in board.claims.values() if c.holder == me]
    if others:
        lines.append("Claimed by others: " + "; ".join(f"{h} ({len(i)}): {_names(i)}" for h, i in others.items()))
    else:
        lines.append("No other curator holds a claim.")
    if me:
        lines.append(f"Yours ({len(mine)}): {_names(sorted(mine, key=lambda c: c.name))}" if mine else "Yours: none.")
        soon = [c for c in mine if c.seconds_left() < 2 * 86400]
        if soon:
            lines.append(f"Yours expiring within 2 days (renew with `claims renew`): {_names(soon)}")
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(lines)}}


def pre_tool_use(claims, payload: dict) -> dict | None:
    """A warning when the edited file belongs to a dataset someone else holds."""
    name = dataset_of(str((payload.get("tool_input") or {}).get("file_path") or ""))
    if not name:
        return None
    me = claims.configured_curator()
    if not me:
        return None
    try:
        board = claims.load(max_age=60)
    except claims.ClaimsError:
        board = claims.cached_board()
    claim = board.held_by_other(name, me) if board is not None else None
    if claim is None:
        return None
    text = f"Claim warning: {name} is claimed by {claim.describe()}."
    return {
        "systemMessage": text,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": f"{text} Another curator is working on this dataset; stop and ask the user before "
            "changing it further.",
        },
    }


def main() -> int:
    """Read the hook's JSON from stdin and print the answer, if any."""
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        from data_foundry.curation import claims  # noqa: PLC0415 - fail open without the package

        event = payload.get("hook_event_name")
        if event == "SessionStart":
            out = session_start(claims)
        elif event == "PreToolUse":
            out = pre_tool_use(claims, payload)
        else:
            out = None
    except Exception:  # noqa: BLE001 - a hook must never get in the way
        return 0
    if out:
        print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
