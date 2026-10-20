"""The custom agents in ``.claude/agents/`` load, and the skills name only agents that exist.

The screening and add-dataset skills hand work to these agents by name; a renamed or deleted agent file would otherwise
break a workflow silently.
"""

from __future__ import annotations

import re
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


def test_pipeline_names_existing_agents():
    """Every agent the pipeline's agent table names has a file, and every file is named there."""
    section = PIPELINE.read_text(encoding="utf-8").split("## Agents", 1)[1]
    named = set(re.findall(r"`([a-z]+(?:-[a-z]+)*)`", section))
    files = {p.stem for p in AGENTS.glob("*.md")}
    assert named == files
