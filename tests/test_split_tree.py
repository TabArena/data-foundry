"""The decision tree of SPLIT-36 names only splits, tags and definitions that exist.

`split_tree.md` is walked from a record's data collection type (SPLIT-34) to a leaf whose title is
"Split · justification". This test reads the file and checks that it has one section per collection type, that every
leaf's split is random, grouped or temporal with a tag that fits it, and that every definition it names as an example
or a departure has a v0.2 folder or, for one added on main after this branch, a record.
"""

from __future__ import annotations

import re

import pytest
from data_foundry.curation._paths import resolve_curation_root
from data_foundry.curation.consistency import COLLECTION_TYPES
from data_foundry.schema import FORCED_TIME_TAGS, GROUP_BASIS_TAGS, TIME_BASIS_TAGS

REPO = resolve_curation_root().parent
TREE = REPO / ".claude/skills/knowledge-curation/references/split_tree.md"
V02 = REPO / "datasets/_dev/tabarena-v0pt2"
RECORDS = REPO / "curation/records"
LEAF = re.compile(r"→ \*\*(Random|Grouped|Temporal) · (`(\w+)`)?([^*]*)\*\*")
TAGS = {
    "Random": {*TIME_BASIS_TAGS, "ForcedIIDFromTemporal", *GROUP_BASIS_TAGS},
    "Grouped": {*TIME_BASIS_TAGS, "ForcedGroupedFromTemporal"},
}


@pytest.fixture(scope="module")
def text() -> str:
    """The tree file."""
    return TREE.read_text()


def test_one_section_per_collection_type(text: str) -> None:
    """The tree's sections are SPLIT-34's seven types, in its order."""
    sections = [
        h.strip()
        for h in re.findall(r"^## (.+)$", text, re.M)
        if h.strip().lower() in {t.lower() for t in COLLECTION_TYPES}
    ]
    assert [s.lower() for s in sections] == [t.lower() for t in COLLECTION_TYPES]


def test_every_leaf_names_a_split_and_a_fitting_tag(text: str) -> None:
    """A random or grouped leaf carries a time basis or forced tag that fits its split; a temporal leaf carries none."""
    leaves = LEAF.findall(text)
    assert len(leaves) > 40
    bad = []
    for split, _, tag, rest in leaves:
        if split == "Temporal":
            if tag or not rest.strip():
                bad.append(f"Temporal · {tag}{rest}")
        elif tag not in TAGS[split]:
            bad.append(f"{split} · {tag}{rest}")
    assert not bad, bad
    assert set(FORCED_TIME_TAGS) <= {t for _, _, t, _ in leaves}


def test_named_definitions_exist(text: str) -> None:
    """Every example and departure is a v0.2 definition folder, or a definition's record."""
    names = set()
    for line in re.findall(r"Examples: ([^.]+)\.", text):
        names |= {n.strip() for n in line.split(",")}
    names |= set(re.findall(r"^\| ([a-z0-9_]+) \|", text, re.M))
    missing = sorted(
        n
        for n in names
        if not (V02 / n / "dataset.py").exists() and not (RECORDS / f"{n.removesuffix('_1m')}.md").exists()
    )
    assert names
    assert not missing, missing
