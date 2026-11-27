"""The split decision tree of SPLIT-36 (``split_tree.md``), read into questions, leaves and links.

The tree is markdown kept for people to read. This module is its one reader: the tests check the tree's logic with it
(every answer ends in a question, a leaf or a step, no step loops, the IDs are unique, a definition's ``split_leaf``
names a leaf whose split it ships), and the review-split-tree skill draws its page from it. The grammar, in short (the
skill's SKILL.md has it in full):

* A section (``## <name>``) is a collection type (SPLIT-34), a shared step (its name ends in "step"), or text.
* A tree section opens with intro paragraphs, then its first question, then one bullet list of answers.
* A question is ``**<text>?** [<ID>] _(<kind>; reads <what>)_``; an answer is a bullet ``- <answer> → <next>``, its own
  answers as sub-bullets two spaces in; ``<next>`` is a question, a leaf or a link.
* A leaf is ``**<Random|Grouped|Temporal|Retire> · <tag and qualifier>** [L-<ID>]. <body>`` ending with
  ``Examples: a, b.`` or ``No v0.2 definition reaches it yet.``
* A link is ``**<section name>**``, optionally followed by ``(<note>; here: a, b)``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from data_foundry.curation._paths import skills_dir
from data_foundry.curation.consistency import COLLECTION_TYPES
from data_foundry.schema import FORCED_TIME_TAGS, GROUP_BASIS_TAGS, TIME_BASIS_TAGS, current_tag

TREE_FILE = "knowledge-curation/references/split_tree.md"
"""The tree, relative to the skills directory."""

FAMILIES = ("Random", "Grouped", "Temporal", "Retire")
"""A leaf's split family: an IID split, a ``grouping``, a ``temporal`` declaration, or a dataset to retire."""

KINDS = ("use case", "data and documentation", "measurement", "person decides")
"""What answers a question: the use case, the raw rows and the source, a number computed, or only a person."""

UNREACHED = "No v0.2 definition reaches it yet."
DEPARTURES = "Definitions that ship another split"

_QUESTION_ID = re.compile(r"[A-Z]+\.[a-z0-9-]+")
_LEAF_ID = re.compile(r"L-[A-Z]+\.[a-z0-9-]+")
_BULLET = re.compile(r"^( *)- (.*)$")
_LEAF = re.compile(r"^(" + "|".join(FAMILIES) + r") · (?:`(\w+)`)?\s*(.*)$", re.S)
_ANNOTATION = re.compile(r"^_\((.*)\)_$", re.S)


@dataclass
class Leaf:
    """Where a walk ends: the split family, the tag that justifies it, and the definitions that reach it."""

    id: str
    section: str
    title: str
    family: str
    tag: str | None
    body: str
    examples: list[str] = field(default_factory=list)
    reached: bool = True


@dataclass
class Link:
    """An answer that continues at another section: a shared step, or another collection type."""

    target: str
    section: str
    note: str = ""
    here: list[str] = field(default_factory=list)


@dataclass
class Question:
    """A question, the kind of evidence that answers it, and its answers in order."""

    id: str
    section: str
    text: str
    kind: str
    reads: str
    answers: list[tuple[str, Node]] = field(default_factory=list)


Node = Question | Leaf | Link


@dataclass
class Section:
    """A ``## `` section: a collection type or a step with its first question, or a text section."""

    name: str
    kind: str
    intro: list[str]
    root: Question | None
    text: str


@dataclass
class SplitTree:
    """The parsed tree: its sections in order and the departures table."""

    sections: dict[str, Section]
    departures: list[dict[str, str]]

    def nodes(self) -> list[Node]:
        """Every question, leaf and link, section by section, depth first; links are not followed."""
        out: list[Node] = []

        def walk(node: Node) -> None:
            out.append(node)
            if isinstance(node, Question):
                for _, child in node.answers:
                    walk(child)

        for section in self.sections.values():
            if section.root is not None:
                walk(section.root)
        return out

    def questions(self) -> list[Question]:
        """Every question."""
        return [n for n in self.nodes() if isinstance(n, Question)]

    def leaves(self) -> list[Leaf]:
        """Every leaf."""
        return [n for n in self.nodes() if isinstance(n, Leaf)]

    def links(self) -> list[Link]:
        """Every link to a step or another type."""
        return [n for n in self.nodes() if isinstance(n, Link)]

    def leaf(self, leaf_id: str) -> Leaf | None:
        """The leaf with this ID, or None."""
        return next((leaf for leaf in self.leaves() if leaf.id == leaf_id), None)

    def section_named(self, name: str) -> Section | None:
        """The section a link names, matched without case."""
        return next((s for s in self.sections.values() if s.name.lower() == name.lower()), None)

    def leaves_from(self, section: str) -> list[Leaf]:
        """The leaves a walk from ``section`` can end at: its own and those of the sections its links lead to."""
        seen: set[str] = set()
        out: list[Leaf] = []

        def visit(name: str) -> None:
            if name in seen:
                return
            seen.add(name)
            for node in self.nodes():
                if node.section != name:
                    continue
                if isinstance(node, Leaf):
                    out.append(node)
                elif isinstance(node, Link) and (target := self.section_named(node.target)) is not None:
                    visit(target.name)

        visit(section)
        return out


def tree_path() -> Path:
    """Where the repository keeps the tree."""
    return skills_dir() / TREE_FILE


def load(path: Path | str | None = None) -> SplitTree:
    """Read and parse the tree file (the repository's by default)."""
    return parse(Path(path or tree_path()).read_text())


def parse(text: str) -> SplitTree:
    """Parse the tree's markdown; raises ValueError, naming the place, on anything outside the grammar."""
    chunks = re.split(r"(?m)^## ", text)[1:]
    names = [c.partition("\n")[0].strip() for c in chunks]
    types = {t.lower() for t in COLLECTION_TYPES}
    sections: dict[str, Section] = {}
    for name, chunk in zip(names, chunks):
        body = chunk.partition("\n")[2]
        kind = "type" if name.lower() in types else "step" if name.lower().endswith(" step") else "text"
        if kind == "text":
            sections[name] = Section(name, kind, [], None, body.strip())
            continue
        sections[name] = _parse_section(name, kind, body, names)
    departures = _parse_table(sections[DEPARTURES].text) if DEPARTURES in sections else []
    return SplitTree(sections, departures)


def _parse_section(name: str, kind: str, body: str, names: list[str]) -> Section:
    """A tree section: intro paragraphs, the first question, then its answers."""
    lines = body.strip("\n").split("\n")
    first_bullet = next((i for i, line in enumerate(lines) if line.startswith("- ")), None)
    if first_bullet is None:
        raise ValueError(f"section {name!r}: no list of answers")
    paragraphs = [" ".join(p.split()) for p in re.split(r"\n\s*\n", "\n".join(lines[:first_bullet])) if p.strip()]
    if not paragraphs:
        raise ValueError(f"section {name!r}: no first question")
    root = _node(paragraphs[-1], name, names, f"section {name!r}")
    if not isinstance(root, Question):
        raise ValueError(f"section {name!r}: it opens with a question, not {root!r}")
    root.answers = _answers(lines[first_bullet:], 0, name, names)
    return Section(name, kind, paragraphs[:-1], root, body.strip())


def _answers(lines: list[str], indent: int, section: str, names: list[str]) -> list[tuple[str, Node]]:
    """The bullets at one indentation, each with the lines below it."""
    items: list[list[str]] = []
    for line in lines:
        if not line.strip():
            continue
        m = _BULLET.match(line)
        if m and len(m[1]) == indent:
            items.append([m[2]])
        elif items and len(line) - len(line.lstrip()) > indent:
            items[-1].append(line)
        else:
            raise ValueError(f"section {section!r}: a line outside the list of answers: {line.strip()[:80]!r}")
    out = []
    for item in items:
        head = [item[0]]
        rest = item[1:]
        sub = next((i for i, line in enumerate(rest) if _BULLET.match(line)), len(rest))
        head += [line.strip() for line in rest[:sub]]
        answer, arrow, follows = " ".join(" ".join(head).split()).partition(" →")
        if not arrow:
            raise ValueError(f"section {section!r}: an answer without an arrow: {answer[:80]!r}")
        node = _node(follows.strip(), section, names, f"section {section!r}, answer {answer!r}")
        if isinstance(node, Question):
            node.answers = _answers(rest[sub:], indent + 2, section, names)
            if not node.answers:
                raise ValueError(f"section {section!r}: the question {node.id} has no answers")
        elif rest[sub:]:
            raise ValueError(f"section {section!r}: answers below a leaf or a link, after {answer!r}")
        out.append((answer.strip(), node))
    return out


def _node(text: str, section: str, names: list[str], where: str) -> Node:
    """What follows an arrow, or a section's first paragraph: a question, a leaf or a link."""
    m = re.match(r"\*\*(.+?)\*\*\s*(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{where}: no bold question, leaf or link: {text[:80]!r}")
    bold, tail = m[1].strip(), m[2].strip()
    if leaf := _LEAF.match(bold):
        return _leaf(leaf, tail, section, where)
    if bold.lower() in {n.lower() for n in names}:
        return _link(bold, tail, section, where)
    idm = re.match(r"\[([^\]]+)\]\s*(.*)$", tail, re.S)
    if not idm or not _QUESTION_ID.fullmatch(idm[1]):
        raise ValueError(f"{where}: the question {bold[:60]!r} has no ID like [DB.meets], or names no section")
    am = _ANNOTATION.match(idm[2].strip())
    if not am:
        raise ValueError(f"{where}: the question {idm[1]} has no `_(<kind>; reads ...)_` annotation")
    kind = next((k for k in KINDS if am[1].startswith(k)), "")
    return Question(idm[1], section, bold, kind, am[1].strip())


def _leaf(m: re.Match[str], tail: str, section: str, where: str) -> Leaf:
    """A leaf: its ID, body and examples."""
    idm = re.match(r"\[([^\]]+)\]\.?\s*(.*)$", tail, re.S)
    if not idm or not _LEAF_ID.fullmatch(idm[1]):
        raise ValueError(f"{where}: the leaf {m[0][:60]!r} has no ID like [L-DB.unit]")
    body = idm[2].strip()
    examples: list[str] = []
    em = re.search(r"Examples:\s*(.+?)\.?$", body, re.S)
    if em:
        examples = [e.strip() for e in em[1].split(",") if e.strip()]
        body = body[: em.start()].strip()
    reached = UNREACHED not in body
    if reached == (not examples):
        raise ValueError(f"{where}: the leaf {idm[1]} ends with `Examples: ...` or `{UNREACHED}`, one of them")
    body = body.replace(UNREACHED, "").strip()
    return Leaf(idm[1], section, m[0].replace("`", ""), m[1], m[2], body, examples, reached)


def _link(target: str, tail: str, section: str, where: str) -> Link:
    """A link and its brackets: a note (the time key), and the definitions that take it after ``here:``."""
    if not tail:
        return Link(target, section)
    pm = re.match(r"\((.*)\)$", tail, re.S)
    if not pm:
        raise ValueError(f"{where}: after a link only `(<note>; here: a, b)`: {tail[:80]!r}")
    inner, here = pm[1].strip(), []
    hm = re.search(r"(?:^|;\s*)here:\s*(.+)$", inner, re.S)
    if hm:
        here = [n.strip() for n in hm[1].split(",") if n.strip()]
        inner = inner[: hm.start()].strip()
    return Link(target, section, inner, here)


def _parse_table(text: str) -> list[dict[str, str]]:
    """The rows of the first markdown table in a text section, keyed by its header."""
    rows = [line for line in text.split("\n") if line.startswith("|")]
    if len(rows) < 2:
        return []
    header = [h.lower() for h in _cells(rows[0])]
    return [dict(zip(header, _cells(row))) for row in rows[2:]]


def _cells(row: str) -> list[str]:
    """The cells of one table row."""
    return [c.strip() for c in row.strip().strip("|").split("|")]


def fitting_tags(family: str) -> set[str]:
    """The tags a leaf of this family may carry in its title: none for a temporal or retired leaf."""
    iid, grouped = FORCED_TIME_TAGS
    return {
        "Random": {*TIME_BASIS_TAGS, iid, *GROUP_BASIS_TAGS},
        "Grouped": {*TIME_BASIS_TAGS, grouped},
    }.get(family, set())


def placement_problems(leaf: Leaf | None, leaf_id: str, split: str, tags: set[str]) -> list[str]:
    """Why a definition that names ``leaf_id`` in ``split_leaf`` does not ship that leaf's split.

    Args:
        leaf: The tree's leaf of that ID, or None when the tree has none.
        leaf_id: The ID the definition names.
        split: What the definition ships: ``random``, ``grouped`` or ``temporal``.
        tags: The definition's time-basis, forced and group-basis tags; an old name counts as its new one.
    """
    if leaf is None:
        return [f"`split_leaf = {leaf_id!r}` names no leaf of the split tree"]
    if leaf.family == "Retire":
        return [f"{leaf_id} retires the dataset; a definition in the working copy does not ship it"]
    family = {"Random": "random", "Grouped": "grouped", "Temporal": "temporal"}[leaf.family]
    found = []
    if split != family:
        found.append(f"{leaf_id} is a {family} split, the definition ships a {split} one")
    if leaf.tag and leaf.tag not in {current_tag(t) for t in tags}:
        found.append(f"{leaf_id} carries `{leaf.tag}`, the definition {sorted(tags) or 'none'}")
    return found
