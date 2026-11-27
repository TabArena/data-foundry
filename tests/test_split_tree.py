"""The decision tree of SPLIT-36 (`split_tree.md`): its logic, its IDs and the definitions it names.

The tree is read by `data_foundry.curation.split_tree`, the reader the review page uses too. These tests check that
the tree is closed (every answer ends in a question, a leaf or a link to a section that exists, and following links
never loops), that its IDs are unique and belong to their section, that every leaf names a split with a tag that fits,
that the questions only a person answers are marked so, and that the definitions it names exist and ship their leaf's
split: its examples, and every definition that records its leaf in `split_leaf`.
"""

from __future__ import annotations

import re

import pytest
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.consistency import COLLECTION_TYPES
from data_foundry.curation.split_tree import (
    KINDS,
    Leaf,
    Link,
    Question,
    SplitTree,
    fitting_tags,
    load,
    parse,
    placement_problems,
)
from data_foundry.curation.store import load_all
from data_foundry.schema import FORCED_TIME_TAGS
from data_foundry.time_basis import ALLOW_UNSTRUCTURED, tags_of
from data_foundry.v2 import discover_definitions

REPO = resolve_curation_root().parent
V02 = REPO / "datasets/_dev/tabarena-v0pt2"
RECORDS = REPO / "curation/records"
PERSON_QUESTIONS = {"CAT.exception", "ORDER.exception", "CAT.small", "ORDER.small", "FORCED.reason", "FORCED.risk"}
"""The questions "Who answers" names: the windows exception, a small table's flat reading signed off, the two reasons
SPLIT-32 allows, the leakage risk."""


@pytest.fixture(scope="module")
def tree() -> SplitTree:
    """The repository's tree."""
    return load()


@pytest.fixture(scope="module")
def definitions() -> dict:
    """The working copy's definition classes by folder name."""
    return discover_definitions(V02, strict=False) if V02.is_dir() else {}


def shipped(cls: type) -> tuple[str, set[str]]:
    """What a definition ships: its split (``random``, ``grouped``, ``temporal``) and its basis tags."""
    split = "temporal" if cls.temporal is not None else "grouped" if cls.grouping is not None else "random"
    tags = set(tags_of(cls.time_basis, cls.group_basis)) | (set(cls.data_tags) & set(FORCED_TIME_TAGS))
    return split, tags


def test_types_in_split_34_order(tree: SplitTree) -> None:
    """The tree has one section per SPLIT-34 type, in its order, and the shared steps after them."""
    types = [s.name.lower() for s in tree.sections.values() if s.kind == "type"]
    assert types == [t.lower() for t in COLLECTION_TYPES]
    kinds = [s.kind for s in tree.sections.values() if s.kind != "text"]
    assert kinds == sorted(kinds, key=lambda k: k == "step"), "the steps follow the types"


def test_ids_unique_and_of_their_section(tree: SplitTree) -> None:
    """Every question and leaf ID is unique, and a section's IDs share its first question's prefix."""
    ids = [n.id for n in tree.nodes() if not isinstance(n, Link)]
    assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})
    for section in tree.sections.values():
        if section.root is None:
            continue
        prefix = section.root.id.split(".")[0]
        wrong = [
            n.id
            for n in tree.nodes()
            if not isinstance(n, Link) and n.section == section.name and n.id.removeprefix("L-").split(".")[0] != prefix
        ]
        assert not wrong, f"{section.name}: {wrong} do not start with {prefix}"


def test_every_link_resolves_and_every_step_is_used(tree: SplitTree) -> None:
    """A link names a type or a step of the tree, and every step is linked from somewhere."""
    targets = []
    for link in tree.links():
        section = tree.section_named(link.target)
        assert section is not None, f"{link.section}: no section {link.target!r}"
        assert section.kind != "text", f"{link.section}: {link.target!r} is no type or step"
        targets.append(section.name)
    unused = [s.name for s in tree.sections.values() if s.kind == "step" and s.name not in targets]
    assert not unused, unused


def test_links_never_loop(tree: SplitTree) -> None:
    """Following links from any section reaches leaves: no section leads back to itself."""
    edges: dict[str, set[str]] = {name: set() for name in tree.sections}
    for link in tree.links():
        edges[link.section].add(tree.section_named(link.target).name)

    def visit(name: str, path: tuple[str, ...]) -> None:
        assert name not in path, f"the links loop: {' → '.join([*path, name])}"
        for nxt in edges[name]:
            visit(nxt, (*path, name))

    for name in edges:
        visit(name, ())


def test_questions_have_a_kind_and_answers(tree: SplitTree) -> None:
    """Every question says what answers it and has two answers or more, each once."""
    for q in tree.questions():
        assert q.kind in KINDS, f"{q.id}: the annotation opens with none of {KINDS}"
        labels = [a for a, _ in q.answers]
        assert len(labels) >= 2, f"{q.id}: answers {labels}"
        assert len(set(labels)) == len(labels), f"{q.id}: answers {labels}"


def test_person_questions_are_marked(tree: SplitTree) -> None:
    """The questions only a person answers are of that kind, and "Who answers" names each of them."""
    person = {q.id for q in tree.questions() if q.kind == "person decides"}
    assert person == PERSON_QUESTIONS
    who = tree.sections["Who answers"].text
    assert not [i for i in person if f"[{i}]" not in who], "Who answers names every person question"


def test_every_leaf_names_a_split_and_a_fitting_tag(tree: SplitTree) -> None:
    """A random or grouped leaf carries a tag that fits its split; a temporal or retire leaf carries none."""
    bad = [leaf.title for leaf in tree.leaves() if leaf.tag and leaf.tag not in fitting_tags(leaf.family)]
    bad += [leaf.title for leaf in tree.leaves() if leaf.family in {"Random", "Grouped"} and not leaf.tag]
    assert not bad, bad
    assert set(FORCED_TIME_TAGS) <= {leaf.tag for leaf in tree.leaves()}


def test_named_definitions_exist(tree: SplitTree) -> None:
    """Every example, every `here:` name and every departure is a v0.2 definition folder or a record."""
    names = {n for leaf in tree.leaves() for n in leaf.examples}
    names |= {n for link in tree.links() for n in link.here}
    names |= {row["definition"] for row in tree.departures}
    missing = sorted(
        n for n in names if not (V02 / n).is_dir() and not (RECORDS / f"{n.removesuffix('_1m')}.md").exists()
    )
    assert names
    assert not missing, missing


def test_at_most_three_examples(tree: SplitTree) -> None:
    """A leaf keeps up to three examples; `split_leaf` records every other placement."""
    assert not [leaf.id for leaf in tree.leaves() if len(leaf.examples) > 3]


def test_departures_name_a_leaf(tree: SplitTree) -> None:
    """Every row of the departures table names a leaf of the tree, and the definition is no example of it.

    The table may be empty: a resolved departure leaves it.
    """
    for row in tree.departures:
        leaf = tree.leaf(row["leaf"])
        assert leaf is not None, row
        assert row["definition"] not in leaf.examples, f"{row['definition']} departs from {leaf.id}"


@pytest.mark.skipif(
    ALLOW_UNSTRUCTURED, reason="the definitions still move to the split rules; the tree names where they land"
)
def test_examples_ship_their_leaf(tree: SplitTree, definitions: dict) -> None:
    """An example ships its leaf's split and tag.

    Checked once every definition has moved to the split rules, which the change that completes the move marks by
    setting `ALLOW_UNSTRUCTURED` false: the examples name where the definitions land.
    """
    bad = []
    for leaf in tree.leaves():
        if leaf.family == "Retire":
            continue
        for name in leaf.examples:
            cls = definitions.get(name)
            if cls is None:
                continue
            split, tags = shipped(cls)
            bad += [f"{name}: {p}" for p in placement_problems(leaf, leaf.id, split, tags)]
    assert not bad, bad


def test_every_definition_names_its_leaf(definitions: dict) -> None:
    """Every definition of the working copy names the leaf its split comes from in `split_leaf` (SPLIT-36)."""
    assert definitions
    assert not sorted(name for name, cls in definitions.items() if getattr(cls, "split_leaf", None) is None)


def test_split_leaf_lies_on_the_walk_from_the_collection_type(tree: SplitTree, definitions: dict) -> None:
    """A definition's leaf is one the walk from its record's collection type can end at, a leaf the tree does not call
    unreached; a leaf's example names that leaf.
    """
    types = {}
    for record in load_all(records_dir()):
        found = [t for t in record.tags or [] if t in COLLECTION_TYPES]
        if len(found) == 1:
            types[record.unique_name] = found[0]
    departs = {(row["definition"], row["leaf"]) for row in tree.departures}
    examples = {name: leaf.id for leaf in tree.leaves() for name in leaf.examples}
    bad = []
    for name, cls in definitions.items():
        leaf_id = getattr(cls, "split_leaf", None)
        if leaf_id is None or (name, leaf_id) in departs:
            continue
        kind = types.get(name.removesuffix("_1m"))
        section = tree.section_named(kind) if kind else None
        if section is not None and leaf_id not in {leaf.id for leaf in tree.leaves_from(section.name)}:
            bad.append(f"{name}: {leaf_id} is not on the walk from {kind}")
        leaf = tree.leaf(leaf_id)
        if leaf is not None and not leaf.reached:
            bad.append(f"{name}: {leaf_id} says no v0.2 definition reaches it")
        if name in examples and examples[name] != leaf_id:
            bad.append(f"{name}: the example of {examples[name]} names {leaf_id}")
    assert not bad, bad


def test_split_leaf_names_the_split_shipped(tree: SplitTree, definitions: dict) -> None:
    """A definition's `split_leaf` is a leaf of the tree whose split and tag it ships, or a listed departure."""
    departs = {(row["definition"], row["leaf"]) for row in tree.departures}
    bad = []
    for name, cls in definitions.items():
        leaf_id = getattr(cls, "split_leaf", None)
        if leaf_id is None or (name, leaf_id) in departs:
            continue
        split, tags = shipped(cls)
        bad += [f"{name}: {p}" for p in placement_problems(tree.leaf(leaf_id), leaf_id, split, tags)]
    assert not bad, bad


TINY = """# Tree

## How to walk it

Text.

## Panel data

The same units observed again.

**Fill in, or predict after it?** [PAN.when] _(use case; reads the use case)_
- fill in → **Fill-in step** (here: some_definition)
- after it →
  **Shared calendar?** [PAN.calendar] _(data and documentation; reads the raw rows)_
  - yes → **Temporal · whole periods** [L-PAN.periods]. Windows of whole periods. Examples: a_definition.
  - no → **Grouped · `UnseenGroup` (units)** [L-PAN.units]. Whole units held out. No v0.2 definition reaches it yet.

## Fill-in step

**Labels later?** [FILL.later] _(person decides; an agent answers no)_
- yes → **Random · `RetrospectiveFillIn`** [L-FILL.random]. Random. Examples: b_definition, c_definition.
- no → **Retire · Too Small** [L-FILL.retire]. Retired. No v0.2 definition reaches it yet.
"""


def test_parse_reads_the_grammar() -> None:
    """A small tree in the grammar reads into its questions, leaves and links."""
    tree = parse(TINY)
    assert [s.kind for s in tree.sections.values()] == ["text", "type", "step"]
    root = tree.sections["Panel data"].root
    assert isinstance(root, Question)
    assert root.kind == "use case"
    assert [a for a, _ in root.answers] == ["fill in", "after it"]
    link = root.answers[0][1]
    assert isinstance(link, Link)
    assert (link.target, link.here) == ("Fill-in step", ["some_definition"])
    leaf = tree.leaf("L-PAN.units")
    assert isinstance(leaf, Leaf)
    assert (leaf.tag, leaf.reached) == ("UnseenGroup", False)
    assert tree.leaf("L-FILL.random").examples == ["b_definition", "c_definition"]
    assert tree.questions()[-1].kind == "person decides"


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (("[L-PAN.periods]", ""), "has no ID"),
        (("- yes → **Temporal", "- yes **Temporal"), "without an arrow"),
        ((" _(use case; reads the use case)_", ""), "annotation"),
        (("**Fill-in step**", "**Nowhere step**"), "names no section"),
        ((" Examples: a_definition.", ""), "one of them"),
    ],
)
def test_parse_names_what_breaks_the_grammar(change: tuple[str, str], message: str) -> None:
    """The reader stops at an answer without an arrow, a node without an ID, a leaf without examples or a reach note."""
    with pytest.raises(ValueError, match=re.escape(message)):
        parse(TINY.replace(*change))


def test_placement_problems() -> None:
    """A definition's split and tag against its leaf; an old tag name counts as its new one."""
    leaf = parse(TINY).leaf("L-FILL.random")
    assert placement_problems(leaf, leaf.id, "random", {"Retrospective"}) == []
    assert placement_problems(leaf, leaf.id, "grouped", {"RetrospectiveFillIn"}) == [
        "L-FILL.random is a random split, the definition ships a grouped one"
    ]
    assert "names no leaf" in placement_problems(None, "L-X.y", "random", set())[0]
