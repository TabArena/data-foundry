"""The custom agents in ``.claude/agents/`` load, and the skills name only agents that exist.

The screening and add-dataset skills hand work to these agents by name; a renamed or deleted agent file would otherwise
break a workflow silently.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".claude" / "agents"
PIPELINE = ROOT / ".claude" / "skills" / "knowledge-data-foundry" / "references" / "pipeline.md"


def _front_matter(path: Path) -> dict:
    """The YAML front matter of an agent file."""
    match = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.DOTALL)
    assert match, f"{path.name}: no front matter"
    return yaml.safe_load(match.group(1))


@pytest.mark.parametrize("path", sorted(AGENTS.glob("*.md")), ids=lambda p: p.stem)
def test_agent_front_matter(path):
    """Each agent names itself after its file and says when it is used."""
    meta = _front_matter(path)
    assert meta.get("name") == path.stem
    assert len(meta.get("description", "")) > 40


def test_blind_reviewer_sees_no_project_instructions():
    """The blind reviewer gets neither CLAUDE.md nor the Skill tool, so it judges without our rules."""
    meta = _front_matter(AGENTS / "blind-reviewer.md")
    assert meta.get("omitClaudeMd") is True
    assert "Skill" not in meta.get("tools", "")


def test_task_gamer_sees_no_project_instructions():
    """The task gamer gets neither CLAUDE.md nor the Skill tool; the sandbox hook is wired for every tool."""
    meta = _front_matter(AGENTS / "task-gamer.md")
    assert meta.get("omitClaudeMd") is True
    assert "Skill" not in meta.get("tools", "")
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text())
    wired = [h for entry in settings["hooks"]["PreToolUse"] if "matcher" not in entry for h in entry["hooks"]]
    assert any("task_gamer_hook.py" in h["command"] for h in wired)


def _gamer_call(tool: str, **tool_input) -> str | None:
    """The hook's denial reason for a call of the task gamer, or None when it lets the call run."""
    payload = {"agent_type": "task-gamer", "tool_name": tool, "tool_input": tool_input}
    run = subprocess.run(  # noqa: S603 - our own hook, run on a fixed payload
        [sys.executable, str(ROOT / ".claude" / "hooks" / "task_gamer_hook.py")],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(run.stdout)["hookSpecificOutput"]["permissionDecisionReason"] if run.stdout else None


KIT = "/runs/x/ta_data_curation/panel/participant_kit"


@pytest.mark.parametrize(
    ("tool", "tool_input"),
    [
        ("Read", {"file_path": f"{KIT}/task.md"}),
        ("Write", {"file_path": f"{KIT}/work/a.py"}),
        ("Grep", {"pattern": "x", "path": KIT}),
        ("Bash", {"command": f"cd {KIT} && OMP_NUM_THREADS=2 /r/.venv/bin/python work/a.py"}),
        ("Bash", {"command": f"cd {KIT} && /r/.venv/bin/python - <<EOF\nm = ~df.x.isna()\nprint(df.a / df.b)\nEOF"}),
        ("WebSearch", {"query": "hotel booking demand leak"}),
        (
            "Bash",
            {"command": f"cd {KIT} && curl -sL -o work/paper.html https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/"},
        ),
    ],
)
def test_task_gamer_hook_allows_the_kit(tool, tool_input):
    """Inside the kit, on the web, and with the interpreter, the gamer works freely (the kit path names curation)."""
    assert _gamer_call(tool, **tool_input) is None


@pytest.mark.parametrize(
    ("tool", "tool_input"),
    [
        ("Read", {"file_path": "/repo/CLAUDE.md"}),
        ("Read", {"file_path": f"{KIT}/../../.claude/agents/critic.md"}),
        ("Glob", {"pattern": "**/*.md"}),
        ("Skill", {"skill": "knowledge-curation"}),
        ("Bash", {"command": "cat CLAUDE.md"}),
        ("Bash", {"command": f"cd {KIT} && ls ../.."}),
        ("Bash", {"command": f"cd {KIT} && cd / && ls"}),
        ("Bash", {"command": f"cd {KIT} && cat ~/.claude/x.md"}),
        ("Bash", {"command": f"cd {KIT} && cat /home/u/notes.md"}),
        ("Bash", {"command": f'cd {KIT} && python -c "import data_foundry"'}),
        ("Bash", {"command": f"cd {KIT} && curl -s file:///home/u/notes.md"}),
        ("Bash", {"command": f"cd {KIT} && curl -s https://example.org/x -o /home/u/x"}),
    ],
)
def test_task_gamer_hook_denies_the_rest(tool, tool_input):
    """Any call that leaves the kit is denied with the reason."""
    assert _gamer_call(tool, **tool_input).startswith("Sandbox: ")


def test_task_gamer_hook_ignores_other_agents():
    """The main session and the other agents pass untouched."""
    payload = {"tool_name": "Read", "tool_input": {"file_path": "/repo/CLAUDE.md"}}
    hook = ROOT / ".claude" / "hooks" / "task_gamer_hook.py"
    run = subprocess.run(  # noqa: S603 - our own hook, run on a fixed payload
        [sys.executable, str(hook)], input=json.dumps(payload), capture_output=True, text=True, check=True
    )
    assert run.stdout == ""


def test_pipeline_names_existing_agents():
    """Every agent the pipeline's agent table names has a file, and every file is named there."""
    section = PIPELINE.read_text(encoding="utf-8").split("## Agents", 1)[1]
    named = set(re.findall(r"`([a-z]+(?:-[a-z]+)*)`", section))
    files = {p.stem for p in AGENTS.glob("*.md")}
    assert named == files
