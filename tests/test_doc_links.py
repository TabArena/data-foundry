"""Every relative link in the skills and the agent-facing docs resolves.

The skills point into each other's files (a workflow skill names the knowledge file to read at each step), so a moved
or renamed file would otherwise break them silently. A link to a markdown heading (``file.md#heading``) must name a
heading of that file, in GitHub's slug form.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    *sorted((ROOT / ".claude" / "skills").rglob("*.md")),
    *sorted((ROOT / ".claude" / "agents").glob("*.md")),
    *(
        ROOT / name
        for name in ("AGENTS.md", "CLAUDE.md", "README.md", "CONTRIBUTING_DATASETS.md", "DATA_FOUNDRY_V1.md")
    ),
    *(ROOT / "datasets" / "_dev" / "tabarena-v0pt2" / name for name in ("README.md", "GETTING_STARTED.md")),
    *sorted((ROOT / "datasets" / "_dev" / "tabarena-v0pt2").glob("*/REVIEW.md")),
]
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
CODE = re.compile(r"`[^`\n]*`")


def _slug(heading: str) -> str:
    """GitHub's anchor for a heading: lowercase, punctuation dropped, spaces to hyphens."""
    text = re.sub(r"[`*_]{1,2}(.+?)[`*_]{1,2}", r"\1", heading.strip()).lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def _anchors(path: Path) -> set[str]:
    """The heading anchors of a markdown file, with GitHub's -1, -2 suffixes for repeated headings."""
    seen: dict[str, int] = {}
    anchors = set()
    for line in FENCE.sub("", path.read_text(encoding="utf-8")).splitlines():
        if match := re.match(r"#{1,6}\s+(.*)", line):
            slug = _slug(match.group(1))
            anchors.add(f"{slug}-{seen[slug]}" if slug in seen else slug)
            seen[slug] = seen.get(slug, 0) + 1
    return anchors


def _links(path: Path) -> list[str]:
    """The link targets of a markdown file, outside code blocks and inline code."""
    text = CODE.sub("", FENCE.sub("", path.read_text(encoding="utf-8")))
    return LINK.findall(text)


@pytest.mark.parametrize("doc", [d for d in DOCS if d.exists()], ids=lambda d: str(d.relative_to(ROOT)))
def test_relative_links_resolve(doc):
    """Each relative link names an existing file or folder, and each heading link an existing heading."""
    broken = []
    for target in _links(doc):
        if re.match(r"[a-z]+:", target) or "<" in target:
            continue
        path_part, _, anchor = target.partition("#")
        dest = (doc.parent / path_part).resolve() if path_part else doc
        if not dest.exists() or (anchor and dest.suffix == ".md" and anchor not in _anchors(dest)):
            broken.append(target)
    assert not broken, f"{doc.relative_to(ROOT)}: broken links {broken}"


def test_docs_are_found():
    """The skills and docs above exist, so the link test covers them."""
    assert (ROOT / ".claude" / "skills" / "knowledge-curation" / "SKILL.md").exists()
    assert (ROOT / ".claude" / "skills" / "knowledge-data-foundry" / "SKILL.md").exists()
    assert (ROOT / ".claude" / "skills" / "README.md").exists()
    assert len(DOCS) > 20
