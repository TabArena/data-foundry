"""The one parser of a curation record's ``## Review``: a dataset's review, open and settled, with every turn.

The format is ``.claude/skills/review-added-datasets/references/review_file_format.md``. A review is a sequence of
labelled blocks (``**Outcome:**``, ``**Main points:**``, the record-field rows, ``**Record judgment:**``,
``**Horizon:**``, ``**Issues for <curator>:**`` and ``**Review panel:**``); :func:`read_review` reads one record's
section into a :class:`Review`, and :func:`read_reviews` every record's. A review that breaks the format raises
:class:`ReviewFormatError`, which names the record file and the line in it.

The review page (``review_page.py`` of the review-added-datasets skill), the decision register and the priority
factors read reviews through this module only; it needs no markdown renderer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from data_foundry.curation.store import load_record

REVIEW_FILE = "REVIEW.md"
"""A review file, which the working copy no longer holds: a dataset's review is its record's ``## Review`` section."""
REVIEW_HEADING = re.compile(r"^## Review[ \t]*\r?$", re.MULTILINE)
OPEN_BLOCK = re.compile(r"^\*\*Open issues \(AI, (\d{4}-\d{2}-\d{2})\):\*\*\s*(.*)$")
"""The open-issues block a record without a folder kept in its comments until 2026-11-11 (retired)."""

LABEL = re.compile(r"^\*\*([^*]+?):\*\*\s*(.*)$")
BLOCKS = ("outcome", "points", "fields", "judgment", "horizon", "issues", "panel")
"""The blocks of a review, in the order they appear."""
LABELS = {
    "Outcome": "outcome",
    "Main points": "points",
    "Record fields that disagree with the definition": "fields",
    "Record judgment": "judgment",
    "Horizon": "horizon",
    "Review panel": "panel",
}
ISSUES_LABEL = re.compile(r"^Issues(?: for [^*:]+)?$")
FIELD_ROW = re.compile(r"^- `([a-z_]+)`: record `([^`]+)`, definition `([^`]+)`\.?$")
ISSUE_START = re.compile(r"^(\d+)\. (.*)$")
FENCE = re.compile(r"^\s*(```|~~~)")
SENTENCE_END = re.compile(r"(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)(?<!\bSec)[.?!]\s+(?=[A-Za-z`(\"])")
"""The end of a sentence: a full stop before the next word, which may be a lowercase name."""
FULL_STOP = re.compile(r"\.(?=\s|$)")
"""The end of the panel's recommendation: its first full stop."""

CLOSED = re.compile(r"\*\*(Resolved|Deferred)\b[^*]*\*\*")
"""An issue with a bold "Resolved ..." or "Deferred ..." label (or a title that starts so) is closed."""
CLOSED_TITLE = re.compile(r"^(Resolved|Deferred)\b")
CLOSING = re.compile(r"\*\*(Resolved|Deferred) \(")
"""A closing turn; the last one says whether an item is parked (Deferred) or settled (Resolved)."""
TURN = re.compile(
    r"^(?:- )?\*\*(?:(?P<ai>Answer|Consistency check) \(AI, (?P<ai_date>\d{4}-\d{2}-\d{2})\)[^*]*"
    r"|(?P<close>Resolved|Deferred) \((?P<close_date>\d{4}-\d{2}-\d{2})(?:, (?P<close_who>[^)]+))?\)"
    r"|(?P<who>[A-Z][a-z]+) \((?P<who_date>\d{4}-\d{2}-\d{2})(?:, (?P<mark>[^)]+))?\)):\*\*\s*",
)
"""A turn of the conversation on an issue, at the start of a line: the AI's answer or consistency check, the
curator's note, or the label that closes it."""

FOOTNOTE_DEF = re.compile(r"^\[\^([\w.-]+)\]:\s?(.*)$")
FOOTNOTE_REF = re.compile(r"\[\^([\w.-]+)\]")
AI_NOTES = re.compile(r"^\*\*Notes for the AI:\*\*\s*(.*)$")
PANEL_LABEL = re.compile(r"^\*\*Review panel:\*\*\s*(.*)$")
DETAILS_OPEN = re.compile(r"^<details>\s*<summary>(.+?)</summary>$")
DETAILS_CLOSE = re.compile(r"^</details>$")
MD_ROW = re.compile(r"^\s*\|(.*)\|\s*$")
RECOMMENDED = re.compile(r"\*\*Recommendation:\*\*\s*\**([A-Za-z])\b")
IMPLEMENTED = re.compile(r"\s*\((?:implemented|as implemented)\)", re.IGNORECASE)

RULE_ID = re.compile(r"\b(?:SEL|USE|LEAK|SPLIT|PROV|TP|CLEAN|EV|MET)-\d+\b")
SHAPE_PARTS = ("**Problem:**", "**Options:**", "**Recommendation:**")
HORIZON_PARTS = ("**Verdict:**", "**Options:**", "**Recommendation:**")
HORIZON_SIZE_COLUMN = re.compile(r"^\s*\|[^\n]*\|\s*Test windows\s*\|", re.MULTILINE)
"""A horizon's options table names the size of the test windows each option tests (Lennart, 2026-11-11)."""
PROBLEM_BULLETS = 3
"""The bullets a problem may have, each one sentence: it is the issue's short description (Andrej, 2026-11-03)."""
PROBLEM = re.compile(r"^[*-] \*\*Problem:\*\*(.*?)(?=^[*-] \*\*|^\S|\Z)", re.MULTILINE | re.DOTALL)

CHECKED = {
    what: re.compile(
        rf"^CC \((?P<date>\d{{4}}-\d{{2}}-\d{{2}}), (?P<who>[^)]+)\): the declared {what}\b.*?\bis checked\b.*$",
        re.MULTILINE,
    )
    for what in ("metric", "horizon", "split")
}
"""The record's CC line that the curator checked the declared metric, horizon or split (the mark, applied)."""


class ReviewFormatError(ValueError):
    """A review does not follow the format; the message names the file and the line."""

    def __init__(self, path: Path, index: int | None, message: str) -> None:
        """Name the file and the line (``index`` counts from 0; None for the whole file) in the message."""
        self.path, self.index, self.detail = path, index, message
        where = f"{path}, line {index + 1}" if index is not None else str(path)
        super().__init__(f"{where}: {message}")


class PanelFormatError(ValueError):
    """A review panel block does not follow the format; ``index`` counts from the block's label line (0)."""

    def __init__(self, index: int, message: str) -> None:
        """Keep the line within the block, for the caller to name the line in its file."""
        super().__init__(message)
        self.index = index
        self.message = message


@dataclass
class Turn:
    """One turn after an issue's original text: the AI's answer, the curator's note, or the closing label."""

    who: str
    """``ai``, ``curator`` or ``closed``."""
    kind: str
    """``answer`` or ``consistency check`` (AI), ``note`` (curator), ``resolved`` or ``deferred`` (closed)."""
    date: str
    by: str = ""
    mark: str = ""
    text: str = ""
    """The turn's markdown after its label, its continuation lines dedented."""


@dataclass
class Issue:
    """A numbered issue: its number (the key of the curator's mark), title and text."""

    number: int
    title: str
    text: str
    """The markdown after the title: the original text, then the turns."""
    line: int | None = None
    """The index of the issue's first line in the record file."""

    @property
    def closed(self) -> bool:
        """A ``Resolved`` or ``Deferred`` label in the text, or a title that starts with either word."""
        return bool(CLOSED.search(self.text) or CLOSED_TITLE.match(self.title))

    @property
    def state(self) -> str:
        """``open``, ``resolved`` or ``deferred`` (parked: the last closing label, or the title, says Deferred)."""
        closings = CLOSING.findall(self.text)
        if self.title.startswith("Deferred") or (closings and closings[-1] == "Deferred"):
            return "deferred"
        return "resolved" if self.closed else "open"

    @property
    def original(self) -> str:
        """The text before the first turn."""
        return split_turns(self.text)[0]

    @property
    def turns(self) -> list[Turn]:
        """The turns after the original text, in order."""
        return split_turns(self.text)[1]


@dataclass
class FieldRow:
    """A record field that disagrees with the definition."""

    key: str
    record: str
    definition: str


@dataclass
class PanelSection:
    """One role's ``<details>`` section of the review panel."""

    title: str
    text: str


@dataclass
class Panel:
    """The review panel: its summary (the first sentence is its recommendation) and one section per role."""

    text: str
    """The block as written, label included."""
    summary: str
    recommendation: str
    sections: list[PanelSection] = field(default_factory=list)


@dataclass
class Review:
    """A record's ``## Review``, parsed."""

    name: str
    source: Path
    folder: str | None
    """The dataset folder (from ``v2_path``, or for a retired dataset from the outcome); None when not added."""
    outcome: str
    points: str
    fields: list[FieldRow] = field(default_factory=list)
    judgment: str = ""
    horizon: str = ""
    """The ``**Horizon:**`` block: the argument for a temporal task's test windows the curator signs off."""
    issues_label: str = "Issues"
    issues: list[Issue] = field(default_factory=list)
    panel: Panel | None = None

    @property
    def cell(self) -> str:
        """The outcome's first sentence, which sets the record's category on the page."""
        return first_sentence(self.outcome)

    @property
    def numbers(self) -> list[int]:
        """The issue numbers, in file order."""
        return [issue.number for issue in self.issues]


# --------------------------------------------------------------------------- markdown pieces
def first_sentence(text: str) -> str:
    """The text up to the first full stop that ends a sentence, without it."""
    flat = " ".join(text.split())
    m = SENTENCE_END.search(flat)
    return flat[: m.start()] if m else flat


def dedent(lines: list[str]) -> str:
    """The lines without the common indentation of the non-blank ones."""
    body = [ln for ln in lines if ln.strip()]
    if not body:
        return ""
    pad = min(len(ln) - len(ln.lstrip(" ")) for ln in body)
    return "\n".join(ln[pad:] if len(ln) >= pad else ln for ln in lines)


def split_turns(text: str) -> tuple[str, list[Turn]]:
    """An issue's text split into the original (everything before the first turn label) and the turns."""
    body: list[str] = []
    raw: list[tuple[Turn, list[str]]] = []
    for line in text.splitlines():
        m = TURN.match(line)
        if m is None:
            (raw[-1][1] if raw else body).append(line)
            continue
        if m["ai"]:
            turn = Turn("ai", m["ai"].lower(), m["ai_date"])
        elif m["close"]:
            turn = Turn("closed", m["close"].lower(), m["close_date"], by=m["close_who"] or "")
        else:
            turn = Turn("curator", "note", m["who_date"], by=m["who"], mark=m["mark"] or "")
        raw.append((turn, [line[m.end() :]]))
    for turn, lines in raw:
        turn.text = "\n".join([lines[0], dedent(lines[1:])]) if len(lines) > 1 else lines[0]
    return "\n".join(body), [turn for turn, _ in raw]


def cut_notes(text: str) -> tuple[str, str, list[tuple[str, str]]]:
    """``text`` without its footnote definitions and its ``**Notes for the AI:**`` block, then that block and the
    definitions (id, markdown) in file order.

    A definition is a line ``[^id]: text`` at the start of a line, with its indented continuation lines. The notes
    block runs from its label to the end of the text. Fenced code is left alone.
    """
    body: list[str] = []
    notes: list[str] = []
    defs: list[tuple[str, list[str]]] = []
    fenced = in_def = in_notes = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        m = None if fenced else FOOTNOTE_DEF.match(line)
        if m:
            defs.append((m.group(1), [m.group(2)]))
            in_def = True
            continue
        if in_def and line.startswith((" ", "\t")) and line.strip():
            defs[-1][1].append(line.strip())
            continue
        in_def = False
        n = None if fenced else AI_NOTES.match(line)
        if n:
            in_notes = True
            notes.append(n.group(1))
        elif in_notes:
            notes.append(line)
        else:
            body.append(line)
    return "\n".join(body), "\n".join(notes).strip(), [(k, " ".join(v)) for k, v in defs]


def options(text: str) -> dict:
    """An issue's options from its first options table (a header with an ``Option`` column): each row's key and
    option name (markdown), the key of the row marked ``(implemented)`` and the key the ``**Recommendation:**`` names.
    Empty when the text has no such table.
    """
    tables: list[list[list[str]]] = [[]]
    for line in text.splitlines():
        m = MD_ROW.match(line)
        if m:
            tables[-1].append([c.strip() for c in re.split(r"(?<!\\)\|", m.group(1))])
        elif tables[-1]:
            tables.append([])
    rows = next((t for t in tables if t and "option" in (h.lower() for h in t[0])), [])
    if not rows:
        return {"options": [], "implemented": "", "recommended": ""}
    col = [h.lower() for h in rows[0]].index("option")
    found, implemented = [], ""
    for cells in rows[2:]:
        if len(cells) <= col or not cells[0]:
            continue
        key, name = re.sub(r"[*`]", "", cells[0]).strip(), cells[col]
        if IMPLEMENTED.search(name):
            name, implemented = IMPLEMENTED.sub("", name), implemented or key
        found.append({"key": key, "name": name.strip()})
    rec = RECOMMENDED.search(text)
    return {"options": found, "implemented": implemented, "recommended": rec.group(1) if rec else ""}


def split_issues(text: str) -> tuple[str, list[Issue]]:
    """The numbered top-level items of an issues block (``N. `` at the start of a line), with the text before them."""
    intro: list[str] = []
    raw: list[tuple[int, list[str]]] = []
    for line in text.splitlines():
        m = ISSUE_START.match(line)
        if m:
            raw.append((int(m.group(1)), [m.group(2)]))
        elif raw:
            raw[-1][1].append(line)
        else:
            intro.append(line)
    issues = []
    for n, lines in raw:
        first, rest = lines[0], lines[1:]
        m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", first)
        if m:
            title, lead = m.group(1).strip(), m.group(2).strip()
        else:
            title, lead = first.strip(), ""
            cut = re.search(r"(?<=[.?!])\s", title)
            if cut and cut.start() < 140:
                title, lead = title[: cut.start()], title[cut.start() :].strip()
            elif len(title) > 140:
                title, lead = title[:137].rsplit(" ", 1)[0] + "…", title
        issues.append(Issue(n, title.rstrip(":").strip(), (lead + "\n" + dedent(rest)).strip()))
    return "\n".join(intro).strip(), issues


# --------------------------------------------------------------------------- the review panel
@dataclass
class _OpenSection:
    at: int
    title: str
    body: list[str]
    fenced: bool = False


def _panel_summary(lines: list[str]) -> tuple[str, int]:
    """The panel's summary paragraph (it starts on the label line) and the index of the line after it."""
    m = PANEL_LABEL.match(lines[0]) if lines else None
    if m is None:
        raise PanelFormatError(0, "the panel starts with its label `**Review panel:**`")
    i = 1
    while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("<details"):
        i += 1
    summary = "\n".join([m.group(1), *lines[1:i]]).strip()
    if not summary:
        raise PanelFormatError(0, "no summary: the panel's recommendation and summary follow the label on its line")
    return summary, i


def _open_section(line: str, k: int, current: _OpenSection | None) -> _OpenSection:
    if current is not None:
        raise PanelFormatError(current.at, "this `<details>` is not closed: end it with `</details>` first")
    opened = DETAILS_OPEN.match(line.strip())
    if opened is None or not opened.group(1).strip():
        raise PanelFormatError(k, "a section opens with `<details><summary>Role</summary>` on one line")
    return _OpenSection(k, opened.group(1).strip(), [])


def _close_section(k: int, current: _OpenSection | None) -> PanelSection:
    if current is None:
        raise PanelFormatError(k, "`</details>` without its `<details><summary>Role</summary>`")
    if not "".join(current.body).strip():
        raise PanelFormatError(current.at, f"the `{current.title}` section is empty; leave it out")
    return PanelSection(current.title, dedent(current.body).strip())


def _panel_sections(lines: list[str], start: int) -> list[PanelSection]:
    """The ``<details>`` sections from ``start`` on; inside a fence, ``<details>`` lines are text."""
    sections: list[PanelSection] = []
    current: _OpenSection | None = None
    for k in range(start, len(lines)):
        line, stripped = lines[k], lines[k].strip()
        if current is not None and (current.fenced or FENCE.match(line)):
            current.fenced = current.fenced != bool(FENCE.match(line))
            current.body.append(line)
        elif stripped.startswith("<details"):
            current = _open_section(line, k, current)
        elif DETAILS_CLOSE.match(stripped):
            sections.append(_close_section(k, current))
            current = None
        elif current is not None:
            current.body.append(line)
        elif stripped:
            raise PanelFormatError(
                k,
                "text outside a section; after the summary paragraph come only `<details><summary>Role</summary>` "
                "... `</details>` sections",
            )
    if current is not None:
        fence = " (a code fence in it is not closed)" if current.fenced else ""
        raise PanelFormatError(current.at, f"this `<details>` is not closed with `</details>`{fence}")
    return sections


def split_panel(lines: list[str]) -> Panel:
    """The review panel block, ``lines[0]`` being its label line: the summary, the recommendation, the sections.

    The summary is the first paragraph (it starts on the label line); its first sentence, up to the first full stop,
    is the panel's recommendation. Then come only ``<details><summary>Role</summary>`` ... ``</details>`` sections,
    one per role, each with markdown inside.

    Raises:
        PanelFormatError: The block does not follow the format; its ``index`` counts from the label line.
    """
    summary, start = _panel_summary(lines)
    sections = _panel_sections(lines, start)
    flat = " ".join(summary.split())
    cut = FULL_STOP.search(flat)
    return Panel("\n".join(lines), summary, flat[: cut.start()] if cut else flat, sections)


# --------------------------------------------------------------------------- the blocks of a review
@dataclass
class _Block:
    """A labelled block: its label, the index of its label line, that line's rest, the lines below."""

    label: str
    start: int
    head: str
    lines: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join([self.head, *self.lines]).strip()


def _check_order(path: Path, index: int, label: str, key: str, blocks: dict[str, _Block]) -> None:
    """A block label at ``index`` comes once, in the order of the format, and never after the review panel."""
    if "panel" in blocks and key != "panel":
        raise ReviewFormatError(path, index, f"`**{label}:**` after `**Review panel:**`; the panel is the last block")
    if key in blocks:
        raise ReviewFormatError(path, index, f"a second `**{label}:**` block")
    if blocks and BLOCKS.index(key) < BLOCKS.index(next(reversed(blocks))):
        raise ReviewFormatError(path, index, f"`**{label}:**` comes before the blocks above it (see the format)")


def _read_blocks(path: Path, lines: list[str], offset: int) -> dict[str, _Block]:
    """The labelled blocks of a review (line ``k`` is line ``offset + k`` of the file), checked for order, repeats
    and stray text.
    """
    blocks: dict[str, _Block] = {}
    current: _Block | None = None
    fenced = False
    for k, line in enumerate(lines):
        i = offset + k
        # Fenced code in the review panel is the panel's text, whatever its lines start with.
        if current is not None and current.label == "Review panel" and (fenced or FENCE.match(line)):
            fenced = fenced != bool(FENCE.match(line))
            current.lines.append(line)
            continue
        m = LABEL.match(line)
        label = m.group(1).strip() if m else ""
        key = LABELS.get(label) or ("issues" if m and ISSUES_LABEL.match(label) else None)
        if key is None:
            if line.startswith("#"):
                raise ReviewFormatError(path, i, "a heading inside the review; a review holds only its labelled blocks")
            if current is None and line.strip():
                raise ReviewFormatError(path, i, "text before `**Outcome:**`")
            if current is not None:
                current.lines.append(line)
            continue
        _check_order(path, i, label, key, blocks)
        if key in ("fields", "issues") and m.group(2).strip():
            raise ReviewFormatError(path, i, f"the `**{label}:**` label stands alone; its rows follow below it")
        current = blocks[key] = _Block(label, i, m.group(2))
    return blocks


def _parse_fields(path: Path, block: _Block | None) -> list[FieldRow]:
    """The record-field rows: ``- `field`: record `x`, definition `y`.``, one per field."""
    if block is None:
        return []
    bullets: list[tuple[int, str]] = []
    for k, line in enumerate(block.lines, start=block.start + 1):
        if line.startswith("- "):
            bullets.append((k, line))
        elif bullets and line.startswith((" ", "\t")) and line.strip():
            bullets[-1] = (bullets[-1][0], bullets[-1][1] + " " + line.strip())
        elif line.strip():
            raise ReviewFormatError(path, k, "a field row is a bullet ``- `field`: record `x`, definition `y`.``")
    out: list[FieldRow] = []
    for k, line in bullets:
        m = FIELD_ROW.match(line)
        if m is None:
            raise ReviewFormatError(path, k, "a field row reads ``- `field`: record `x`, definition `y`.``")
        if any(f.key == m.group(1) for f in out):
            raise ReviewFormatError(path, k, f"`{m.group(1)}` twice; the page stores one mark per field")
        out.append(FieldRow(*m.groups()))
    return out


def _parse_issues(path: Path, block: _Block) -> list[Issue]:
    """The issues block's issues, numbered once each, with no text before the first."""
    start = block.start + 1
    for k, line in enumerate(block.lines):
        if line.startswith("#"):
            raise ReviewFormatError(path, start + k, "a heading inside the issues; a review holds no heading")
    intro, issues = split_issues("\n".join(block.lines))
    if intro:
        first = next(k for k, ln in enumerate(block.lines) if ln.strip())
        raise ReviewFormatError(path, start + first, "text before the first issue; each issue starts with `N. `")
    at = [start + k for k, ln in enumerate(block.lines) if ISSUE_START.match(ln)]
    seen: set[int] = set()
    for issue, line in zip(issues, at, strict=True):
        issue.line = line
        if issue.number in seen:
            raise ReviewFormatError(path, line, f"issue {issue.number} appears twice; the marks are stored by number")
        seen.add(issue.number)
    return issues


def _parse_panel(path: Path, lines: list[str], block: _Block | None, offset: int) -> Panel | None:
    if block is None:
        return None
    panel = [lines[block.start - offset], *block.lines]
    while panel and not panel[-1].strip():
        panel.pop()
    try:
        return split_panel(panel)
    except PanelFormatError as error:
        raise ReviewFormatError(path, block.start + error.index, error.message) from error


def _check_outcome(path: Path, index: int, cell: str, name: str, folder: str | None) -> None:
    """The first sentence sets the page's category and, for a folder that is not the unique name, names it."""
    if folder is None:
        if not cell.startswith("not added"):
            raise ReviewFormatError(path, index, "the lead of a record without a folder starts with `not added`")
        return
    if not cell.startswith("added"):
        raise ReviewFormatError(path, index, "the outcome starts with `added` (the dataset has a folder)")
    named = re.search(r"added as `([^`]+)`", cell)
    if folder != name and (named is None or named.group(1) != folder):
        raise ReviewFormatError(path, index, f"the folder is not the unique name: start with ``added as `{folder}` ``")
    if folder == name and named is not None and named.group(1) != folder:
        raise ReviewFormatError(path, index, f"the outcome names the folder `{named.group(1)}`, not {folder}/")


def parse_review(text: str, *, name: str, folder: str | None, path: Path, offset: int = 0) -> Review:
    """One dataset's review from the text of its ``## Review`` section (without the heading).

    ``path`` names the record in errors, and line ``k`` of ``text`` is line ``offset + k`` of that file.

    Raises:
        ReviewFormatError: The review does not follow the format.
    """
    lines = text.splitlines()
    blocks = _read_blocks(path, lines, offset)
    for key, label in (("outcome", "Outcome"), ("points", "Main points")):
        if key not in blocks:
            raise ReviewFormatError(path, None, f"no `**{label}:**` block; it is required")
        if not blocks[key].text:
            raise ReviewFormatError(path, blocks[key].start, f"no text in the `**{label}:**` block")
    fields = _parse_fields(path, blocks.get("fields"))
    issues = _parse_issues(path, blocks["issues"]) if "issues" in blocks else []
    if not issues and not fields and "panel" not in blocks and "horizon" not in blocks:
        # A panel that found nothing for the curator leaves a review with no issue; without a panel it is a stray.
        raise ReviewFormatError(
            path, None, "no issue, no record field and no review panel; a settled issue stays, labelled Resolved"
        )
    panel = _parse_panel(path, lines, blocks.get("panel"), offset)
    review = Review(
        name=name,
        source=path,
        folder=folder,
        outcome=blocks["outcome"].text,
        points=" ".join(blocks["points"].text.split()),
        fields=fields,
        judgment=blocks["judgment"].text if "judgment" in blocks else "",
        horizon=blocks["horizon"].text if "horizon" in blocks else "",
        issues_label=blocks["issues"].label if "issues" in blocks else "Issues",
        issues=issues,
        panel=panel,
    )
    _check_outcome(path, blocks["outcome"].start, review.cell, name, folder)
    return review


# --------------------------------------------------------------------------- records
def _record_folder(v2_path: str | None, name: str, review: str) -> str | None:
    """The record's dataset folder: from ``v2_path``; for a retired dataset (no ``v2_path``), the folder its outcome
    names (``added as `<folder>` ``, else the unique name); None for a record that was not added.
    """
    if v2_path:
        return Path(v2_path).parent.name
    lead = review.lstrip().removeprefix("**Outcome:**").lstrip()
    named = re.match(r"added as `([^`]+)`", lead)
    if named:
        return named.group(1)
    return name if lead.startswith("added") else None


def read_review(path: Path) -> Review | None:
    """The ``## Review`` section of the record at ``path``, or None when it has none.

    Raises:
        ReviewFormatError: The review breaks the format (the line counts in the record file), or the record's
            comments still hold an open-issues block.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    record = load_record(path)
    lines = text.splitlines()
    block = next((ln for ln in (record.comments or "").splitlines() if OPEN_BLOCK.match(ln)), None)
    if block is not None:
        at = lines.index(block) if block in lines else None
        raise ReviewFormatError(path, at, "an open-issues block in the comments: move it into the record's `## Review`")
    heading = REVIEW_HEADING.search(text)
    if heading is None or not record.review:
        return None
    # The section's text starts at its first non-blank line after the heading.
    after = text.count("\n", 0, heading.end()) + 1
    while after < len(lines) and not lines[after].strip():
        after += 1
    name = path.stem
    folder = _record_folder(record.v2_path, name, record.review)
    return parse_review(record.review, name=name, folder=folder, path=path, offset=after)


def review_files(root: Path) -> list[Path]:
    """A ``REVIEW.md`` anywhere in the working copy: none may exist, a dataset's review is in its record."""
    return sorted(Path(root).rglob(REVIEW_FILE))


def read_reviews(records: Path, root: Path | None = None, names: list[str] | None = None) -> list[Review]:
    """The reviews of the records in ``records``, sorted by unique name; ``names`` keeps only those.

    ``root``, the working copy, is checked for a stray ``REVIEW.md``.

    Raises:
        ReviewFormatError: A review breaks the format, the working copy holds a review file, or a name has no review.
    """
    records = Path(records)
    for folder, what in ((root, "the working copy"), (records, "the records")):
        if folder is not None and not Path(folder).is_dir():
            raise ReviewFormatError(Path(folder), None, f"no such folder ({what}); run from the repository root")
    stray = review_files(root) if root is not None else []
    if stray:
        raise ReviewFormatError(
            stray[0], None, "a review file in the working copy: a dataset's review lives in its record's `## Review`"
        )
    found: dict[str, Review] = {}
    for path in sorted(records.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        if not REVIEW_HEADING.search(text) and "**Open issues (AI," not in text:
            continue
        review = read_review(path)
        if review is not None:
            found[review.name] = review
    if names is not None:
        unknown = sorted(set(names) - set(found))
        if unknown:
            raise ReviewFormatError(records, None, f"no review in the records of {unknown}")
        found = {n: r for n, r in found.items() if n in names}
    return [found[n] for n in sorted(found)]


def checked(path: Path, what: str) -> dict | None:
    """The record's latest CC line that the declared ``what`` (``metric``, ``horizon`` or ``split``) is checked, as
    ``{"date", "by", "line"}``; None without one. The review is not read: it may quote such a line.
    """
    if not Path(path).is_file():
        return None
    record = load_record(path)
    found = list(CHECKED[what].finditer("\n".join(filter(None, (record.comments, record.reference)))))
    if not found:
        return None
    m = found[-1]
    return {"date": m["date"], "by": m["who"], "line": m.group(0)}


def is_settled(
    review: Review,
    records: Path,
    metric_marks: set[str] | frozenset[str] | None = frozenset(),
    horizon_marks: set[str] | frozenset[str] | None = frozenset(),
    split_marks: set[str] | frozenset[str] | None = frozenset(),
) -> bool:
    """Whether nothing on ``review`` waits for the curator: every issue resolved (none left deferred), no record-field
    row, no triage verdict to verify, and, for a dataset with a folder whose metric the round marks (``metric_marks``,
    ``None`` for every record), the record's CC line that the declared metric is checked; likewise for the horizon
    (``horizon_marks``) and the split (``split_marks``). Such a record ships by default and leaves the page (Lennart,
    2026-11-08); its review stays in the record. A metric, a horizon or a split the round does not ask about never
    keeps a record on the page (Lennart, 2026-11-10).
    """
    if review.fields or any(issue.state != "resolved" for issue in review.issues):
        return False
    record = Path(records) / f"{review.name}.md"
    if not record.is_file():
        return False
    # A record that triage decided (No) waits for the curator's check, unless it was added: a dataset retired after
    # its review keeps the review in its record, settled.
    if review.folder is None:
        return not str(load_record(record).suggestion or "").startswith("No")
    for what, marks in (("metric", metric_marks), ("horizon", horizon_marks), ("split", split_marks)):
        if (marks is None or review.name in marks) and checked(record, what) is None:
            return False
    return True


# --------------------------------------------------------------------------- the issue shape (warnings)
def _problem_shape(text: str) -> list[str]:
    """What a problem's text misses of its shape: at most three bullets, one sentence each (the text after the lead
    counts as one bullet).
    """
    text = FOOTNOTE_REF.sub("", text)
    lead, *rest = re.split(r"^\s*[*-] ", text, flags=re.MULTILINE)
    bullets = [b for b in [lead, *rest] if b.strip()]
    out = []
    if len(bullets) > PROBLEM_BULLETS:
        out.append(f"short problem ({len(bullets)} bullets, at most {PROBLEM_BULLETS})")
    long = sum(bool(SENTENCE_END.search(" ".join(b.split()))) for b in bullets)
    if long:
        out.append(f"one sentence per problem bullet ({long} with more)")
    return out


def _horizon_warnings(review: Review) -> list[str]:
    """What the ``**Horizon:**`` block misses of its issue shape (the page shows it as the issue H)."""
    if not review.horizon or CLOSING.search(review.horizon):  # a settled horizon keeps the shape it had
        return []
    body, _, _ = cut_notes(review.horizon)
    missing = [p.strip("*:") for p in HORIZON_PARTS if p not in body]
    if "**Options:**" in body and not options(body)["implemented"]:
        missing.append("row marked (implemented): today's length")
    if "**Options:**" in body and not HORIZON_SIZE_COLUMN.search(body):
        missing.append("`Test windows` column (the size of each option's test windows)")
    return [f"{review.name} horizon: no {', '.join(missing)} (the page shows it as issue H)"] if missing else []


def shape_warnings(review: Review) -> list[str]:
    """What the open issues of ``review`` miss of the issue shape: the bullets, the options table with its row marked
    ``(implemented)``, and rule IDs kept out of the text for the curator (they go into footnotes or the notes for the
    AI).

    A warning, not an error: closed issues and old reviews keep the shape they were written in.
    """
    out = []
    for issue in review.issues:
        if issue.closed:
            continue
        body, _, _ = cut_notes(issue.original)
        missing = [p.strip("*:") for p in SHAPE_PARTS if p not in body]
        if not re.search(r"^\s*\|.*\|\s*$", body, re.MULTILINE):
            missing.append("options table")
        elif (opts := options(body))["options"] and not opts["implemented"]:
            missing.append("row marked (implemented), which the page's As implemented locks in")
        problem = PROBLEM.search(body)
        if problem:
            missing += _problem_shape(problem.group(1))
        ids = sorted(set(RULE_ID.findall(body + " " + issue.title)))
        if missing:
            out.append(f"{review.name} issue {issue.number}: no {', '.join(missing)}")
        if ids:
            listed = ", ".join(ids)
            out.append(f"{review.name} issue {issue.number}: rule IDs in the text ({listed}); move them to footnotes")
    return out + _horizon_warnings(review)
