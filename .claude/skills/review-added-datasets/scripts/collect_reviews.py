r"""Collect the open review issues of the working copy into one report for build_review_page.py.

Usage, from the repository root::

    .venv/bin/python .claude/skills/review-added-datasets/scripts/collect_reviews.py \
        --root datasets/_dev/tabarena-v0pt2 --out <report.md> [--names a,b] [--title <text>] [--date <YYYY-MM-DD>]
        [--records curation/records]

Reads the ``## Review`` section of every curation record (a dataset's review, open and settled: Lennart, 2026-11-11,
the record is the one source of a dataset's curation) and the optional ``<root>/REVIEW.md`` (items across datasets),
and writes one report that ``build_review_page.py`` turns into the review page. The format of a review, of the
cross-dataset file and of the report is ``references/review_file_format.md``; a review that breaks it stops the
collector with the record and the line. A ``REVIEW.md`` in a dataset folder stops it too
(``move_reviews_to_records.py`` moves it into the record), and so does an open-issues block left in a record's
comments (moved by hand into its ``## Review``). The report is checked with the builder's
own parser before the collector reports success.

Needs markdown-it-py (the ``curation`` extra), as the builder does.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from data_foundry.curation.store import load_record

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import build_review_page as brp  # noqa: E402 - the builder sits next to this script, not in a package

REVIEW_FILE = "REVIEW.md"
"""The working copy's cross-dataset review file; a dataset's review is its record's ``## Review`` section."""
REVIEW_SECTION_RE = re.compile(r"^## Review\s*$", re.MULTILINE)
FORMAT = HERE.parent / "references" / "review_file_format.md"

TITLE_RE = re.compile(r"^# ([a-z0-9_]+)\s*$")
LABEL_RE = re.compile(r"^\*\*([^*]+?):\*\*\s*(.*)$")
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
FIELD_RE = re.compile(r"^- `([a-z_]+)`: record `([^`]+)`, definition `([^`]+)`\.?$")
OPEN_BLOCK_RE = re.compile(r"^\*\*Open issues \(AI, (\d{4}-\d{2}-\d{2})\):\*\*\s*(.*)$")
ISSUE_START = re.compile(r"^\d+\. ")
SENTENCE_END = re.compile(r"\.(?=\s|$)")
RULE_ID = re.compile(r"\b(?:SEL|USE|LEAK|SPLIT|PROV|TP|CLEAN|EV|MET)-\d+\b")
SHAPE_PARTS = ("**Problem:**", "**Options:**", "**Recommendation:**")
HORIZON_PARTS = ("**Verdict:**", "**Options:**", "**Recommendation:**")
HORIZON_SIZE_COLUMN = re.compile(r"^\s*\|[^\n]*\|\s*Test windows\s*\|", re.MULTILINE)
"""A horizon's options table names the size of the test windows each option tests (Lennart, 2026-11-11)."""
"""The bullets of a ``**Horizon:**`` block, which the page shows as the issue "H": the verdict in view, the length, the
gap and the time frame in the closed Details box, then the options table and the recommendation."""
PROBLEM_BULLETS = 3
"""The bullets a problem may have, each one sentence: it is the issue's short description (Andrej, 2026-11-03)."""
SENTENCE_END = re.compile(r"(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)(?<!\bSec)[.?!]\s+(?=[A-Za-z`(\"])")
"""The end of a sentence inside a bullet: a full stop before the next word, which may be a lowercase name."""
PROBLEM_RE = re.compile(r"^[*-] \*\*Problem:\*\*(.*?)(?=^[*-] \*\*|^\S|\Z)", re.MULTILINE | re.DOTALL)
"""The bullets every open issue has (``references/review_file_format.md``, "Issues")."""


class ReviewFileError(ValueError):
    """A review file does not follow ``references/review_file_format.md``."""

    def __init__(self, path: Path, index: int | None, message: str) -> None:
        """Name the file and the line (``index`` counts from 0; None for the whole file) in the message."""
        self.path, self.index, self.detail = path, index, message
        where = f"{path}, line {index + 1}" if index is not None else str(path)
        super().__init__(f"{where}: {message}")


@dataclass
class Entry:
    """One record on the page: from the ``## Review`` section of its curation record."""

    name: str
    folder: str | None
    source: Path
    outcome: str
    points: str
    cell: str
    judgment: str = ""
    horizon: str = ""
    """The ``**Horizon:**`` block's text: the argument for a temporal task's test windows the curator signs off."""
    issues_label: str = "Issues"
    issues: str = ""
    numbers: list[int] = field(default_factory=list)
    fields: list[tuple[str, str, str]] = field(default_factory=list)
    panel: str = ""
    """The ``**Review panel:**`` block as written, label included; empty without one."""
    panel_sections: list[str] = field(default_factory=list)
    """The roles of the panel's ``<details>`` sections, in file order."""


@dataclass
class Collected:
    """Everything the report holds: the records, sorted by unique name, and the cross-dataset sections."""

    entries: list[Entry]
    across: str = ""
    across_items: int = 0
    settled: list[str] = field(default_factory=list)
    """Records left out because nothing on them waits for the curator (:func:`is_settled`)."""
    metric_marks: set[str] | None = None
    """The records whose declared metric the curator marks in this round (``None``: every record, ``--metric-marks
    all``); by default none, so the page shows no metric (Lennart, 2026-11-10)."""
    horizon_marks: set[str] | None = None
    """The same for a temporal task's horizon and test windows (``--horizon-marks``; Lennart, 2026-11-10)."""

    @property
    def n_folders(self) -> int:
        """The records with a dataset folder (added); the others were not added."""
        return sum(1 for e in self.entries if e.folder)


@dataclass
class _Block:
    """A labelled block of a review: its label, the index of its label line, that line's rest, the lines below."""

    label: str
    start: int
    head: str
    lines: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join([self.head, *self.lines]).strip()


def _first_sentence(text: str) -> str:
    """The outcome cell: the text up to the first full stop that ends a sentence, without it."""
    flat = " ".join(text.split())
    m = SENTENCE_END.search(flat)
    return flat[: m.start()] if m else flat


def _check_issues(path: Path, start: int, lines: list[str]) -> tuple[str, list[int]]:
    """The issues block as text and its issue numbers, after the checks the page needs.

    ``start`` is the index of the block's first line in the file, for the error messages.
    """
    for k, line in enumerate(lines):
        if line.startswith("#"):
            raise ReviewFileError(path, start + k, "a heading inside the issues; the report would split here")
        if brp._label_of(line) is not None:
            raise ReviewFileError(
                path, start + k, "this line starts with a block label of the report; indent it or reword the label"
            )
    text = "\n".join(lines).strip()
    intro, items = brp._split_items(text)
    if intro:
        first = next(k for k, ln in enumerate(lines) if ln.strip())
        raise ReviewFileError(path, start + first, "text before the first issue; each issue starts with `N. `")
    numbers = [it["n"] for it in items]
    at = [start + k for k, ln in enumerate(lines) if ISSUE_START.match(ln)]
    """The index of each issue's first line, in the order of ``items``."""
    seen: set[int] = set()
    for k, n in enumerate(numbers):
        if n in seen:
            raise ReviewFileError(path, at[k], f"issue {n} appears twice; the marks are stored by number")
        seen.add(n)
    return text, numbers


def _check_outcome(path: Path, index: int, cell: str, name: str, folder: str | None) -> None:
    """The first sentence sets the page's category and, for a folder that is not the unique name, names it."""
    if folder is None:
        if not cell.startswith("not added"):
            raise ReviewFileError(path, index, "the lead of a record without a folder starts with `not added`")
        return
    if not cell.startswith("added"):
        raise ReviewFileError(path, index, "the outcome starts with `added` (the dataset has a folder)")
    named = re.search(r"added as `([^`]+)`", cell)
    if folder != name and (named is None or named.group(1) != folder):
        raise ReviewFileError(path, index, f"the folder is not the unique name: start with ``added as `{folder}` ``")
    if folder == name and named is not None and named.group(1) != folder:
        raise ReviewFileError(path, index, f"the outcome names the folder `{named.group(1)}`, not {folder}/")


def _read_blocks(path: Path, lines: list[str]) -> dict[str, _Block]:
    """The labelled blocks after the title line, checked for order, repeats and stray text."""
    blocks: dict[str, _Block] = {}
    current: _Block | None = None
    fenced = False
    for i in range(1, len(lines)):
        line = lines[i]
        # Fenced code in the review panel is the panel's text, whatever its lines start with.
        if current is not None and current.label == "Review panel" and (fenced or brp.FENCE.match(line)):
            fenced = fenced != bool(brp.FENCE.match(line))
            current.lines.append(line)
            continue
        m = LABEL_RE.match(line)
        label = m.group(1).strip() if m else ""
        key = LABELS.get(label) or ("issues" if m and ISSUES_LABEL.match(label) else None)
        if key is None:
            if line.startswith("#"):
                raise ReviewFileError(path, i, "a heading inside the review; a review holds only its labelled blocks")
            if current is None and line.strip():
                raise ReviewFileError(path, i, "text before `**Outcome:**`")
            if current is not None:
                current.lines.append(line)
            continue
        _check_order(path, i, label, key, blocks)
        if key in ("fields", "issues") and m.group(2).strip():
            raise ReviewFileError(path, i, f"the `**{label}:**` label stands alone; its rows follow below it")
        current = blocks[key] = _Block(label, i, m.group(2))
    return blocks


def _check_order(path: Path, index: int, label: str, key: str, blocks: dict[str, _Block]) -> None:
    """A block label at ``index`` comes once, in the order of the format, and never after the review panel."""
    if "panel" in blocks and key != "panel":
        raise ReviewFileError(path, index, f"`**{label}:**` after `**Review panel:**`; the panel is the last block")
    if key in blocks:
        raise ReviewFileError(path, index, f"a second `**{label}:**` block")
    if blocks and BLOCKS.index(key) < BLOCKS.index(next(reversed(blocks))):
        raise ReviewFileError(path, index, f"`**{label}:**` comes before the blocks above it (see the format)")


def _parse_fields(path: Path, block: _Block | None) -> list[tuple[str, str, str]]:
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
            raise ReviewFileError(path, k, "a field row is a bullet ``- `field`: record `x`, definition `y`.``")
    out: list[tuple[str, str, str]] = []
    for k, line in bullets:
        m = FIELD_RE.match(line)
        if m is None:
            raise ReviewFileError(path, k, "a field row reads ``- `field`: record `x`, definition `y`.``")
        if any(f[0] == m.group(1) for f in out):
            raise ReviewFileError(path, k, f"`{m.group(1)}` twice; the page stores one mark per field")
        out.append(m.groups())
    return out


def _check_panel(path: Path, lines: list[str], block: _Block | None) -> tuple[str, list[str]]:
    """The review panel block as written (label included) and its roles, after the builder's own parser read it."""
    if block is None:
        return "", []
    lines = [lines[block.start], *block.lines]
    while lines and not lines[-1].strip():
        lines.pop()
    try:
        panel = brp.split_panel(lines)
    except brp.PanelFormatError as error:
        raise ReviewFileError(path, block.start + error.index, error.message) from error
    return "\n".join(lines), [s["title"] for s in panel["sections"]]


def parse_review_file(path: Path, folder: str, text: str | None = None) -> Entry:
    """One dataset's review: ``text`` is the record's ``## Review`` with a ``# <unique_name>`` title line in front
    (``path``, the record, names it in errors; without ``text`` the file is read as it is).

    Raises:
        ReviewFileError: The file does not follow ``references/review_file_format.md``.
    """
    lines = (path.read_text() if text is None else text).splitlines()
    title = TITLE_RE.match(lines[0]) if lines else None
    if title is None:
        raise ReviewFileError(path, 0, "the file starts with `# <unique_name>` (the record's name)")
    name = title.group(1)
    blocks = _read_blocks(path, lines)
    for key, label in (("outcome", "Outcome"), ("points", "Main points")):
        if key not in blocks:
            raise ReviewFileError(path, None, f"no `**{label}:**` block; it is required")
        if not blocks[key].text:
            raise ReviewFileError(path, blocks[key].start, f"no text in the `**{label}:**` block")
    fields = _parse_fields(path, blocks.get("fields"))
    issues, numbers = ("", [])
    if "issues" in blocks:
        issues, numbers = _check_issues(path, blocks["issues"].start + 1, blocks["issues"].lines)
    if not numbers and not fields and "panel" not in blocks and "horizon" not in blocks:
        # A panel that found nothing for the curator leaves a file with no issue; without a panel it is a stray file.
        raise ReviewFileError(
            path, None, "no issue, no record field and no review panel; a settled issue stays, labelled Resolved"
        )
    panel, roles = _check_panel(path, lines, blocks.get("panel"))
    outcome = blocks["outcome"].text
    cell = _first_sentence(outcome)
    _check_outcome(path, blocks["outcome"].start, cell, name, folder)
    return Entry(
        name=name,
        folder=folder,
        source=path,
        outcome=outcome,
        points=" ".join(blocks["points"].text.split()),
        cell=cell,
        judgment=blocks["judgment"].text if "judgment" in blocks else "",
        horizon=blocks["horizon"].text if "horizon" in blocks else "",
        issues_label=blocks["issues"].label if "issues" in blocks else "Issues",
        issues=issues,
        numbers=numbers,
        fields=fields,
        panel=panel,
        panel_sections=roles,
    )


def parse_across(path: Path) -> tuple[str, int]:
    """The working copy's REVIEW.md: its ``###`` sections as text and the number of items.

    Raises:
        ReviewFileError: The file holds more than its title and ``###`` sections of ``- `` items.
    """
    lines = path.read_text().splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ReviewFileError(path, 0, "the file starts with a `# <title>` line")
    heads = [i for i, ln in enumerate(lines) if ln.startswith("### ")]
    first = heads[0] if heads else len(lines)
    stray = next((i for i in range(1, first) if lines[i].strip()), None)
    if stray is not None or not heads:
        raise ReviewFileError(path, stray, "after the title come only `### <section>` headings with `- ` items")
    n_items = 0
    for k, h in enumerate(heads):
        end = heads[k + 1] if k + 1 < len(heads) else len(lines)
        body = [i for i in range(h + 1, end) if lines[i].strip()]
        items = [i for i in body if lines[i].startswith("- ")]
        if not items:
            raise ReviewFileError(path, h, "a section without items; each item is a top-level `- ` bullet")
        if body[0] != items[0]:
            raise ReviewFileError(path, body[0], "text before the first item of the section")
        heading = next((i for i in body if lines[i].startswith("#")), None)
        if heading is not None:
            raise ReviewFileError(path, heading, "a heading inside a section; sections are `### ` headings")
        n_items += len(items)
    return "\n".join(lines[first:]).strip(), n_items


def _record_folder(record_path: Path, name: str, review: str) -> str | None:
    """The record's dataset folder: from ``v2_path``; for a retired dataset (no ``v2_path``), the folder its outcome
    names (``added as `<folder>` ``, else the unique name); None for a record that was not added.
    """
    v2_path = load_record(record_path).v2_path
    if v2_path:
        return Path(v2_path).parent.name
    lead = review.lstrip().removeprefix("**Outcome:**").lstrip()
    named = re.match(r"added as `([^`]+)`", lead)
    if named:
        return named.group(1)
    return name if lead.startswith("added") else None


def parse_record_review(path: Path) -> Entry | None:
    """The ``## Review`` section of the record at ``path``, or None when it has none.

    Raises:
        ReviewFileError: The review breaks ``references/review_file_format.md`` (the line counts in the record file),
            or the record's comments still hold an open-issues block.
    """
    text = path.read_text()
    record = load_record(path)
    lines = text.splitlines()
    block = next((ln for ln in (record.comments or "").splitlines() if OPEN_BLOCK_RE.match(ln)), None)
    if block is not None:
        at = lines.index(block) if block in lines else None
        raise ReviewFileError(path, at, "an open-issues block in the comments: move it into the record's `## Review`")
    heading = REVIEW_SECTION_RE.search(text)
    if heading is None or not record.review:
        return None
    header = text[: heading.start()].count("\n")
    name = path.stem
    try:
        return parse_review_file(path, _record_folder(path, name, record.review), f"# {name}\n{record.review}")
    except ReviewFileError as error:
        # Line 0 of the parsed text is the title (the record's `## Review` line); line k is the record's header + 1 + k.
        index = None if error.index is None else header + (error.index + 1 if error.index else 0)
        raise ReviewFileError(path, index, error.detail) from None


def folder_review_files(root: Path) -> list[Path]:
    """A ``REVIEW.md`` in a dataset folder of the working copy: none may exist, the review is in the record."""
    return [p for p in sorted(root.glob(f"*/{REVIEW_FILE}")) if not p.parent.name.startswith(("_", "."))]


def _problem_shape(text: str) -> list[str]:
    """What a problem's text misses of its shape: at most three bullets, one sentence each (the text after the lead
    counts as one bullet).
    """
    text = brp.FOOTNOTE_REF.sub("", text)
    lead, *rest = re.split(r"^\s*[*-] ", text, flags=re.MULTILINE)
    bullets = [b for b in [lead, *rest] if b.strip()]
    out = []
    if len(bullets) > PROBLEM_BULLETS:
        out.append(f"short problem ({len(bullets)} bullets, at most {PROBLEM_BULLETS})")
    long = sum(bool(SENTENCE_END.search(" ".join(b.split()))) for b in bullets)
    if long:
        out.append(f"one sentence per problem bullet ({long} with more)")
    return out


def shape_warnings(entry: Entry) -> list[str]:
    """What the open issues of ``entry`` miss of the issue shape: the bullets, the options table with its row marked
    ``(implemented)``, and rule IDs kept out of the text for the curator (they go into footnotes or the notes for the
    AI).

    A warning, not an error: closed issues and old files keep the shape they were written in.
    """
    out = []
    for it in brp._split_items(entry.issues)[1]:
        if it["resolved"]:
            continue
        lines = it["body_md"].splitlines()
        first_turn = next((k for k, ln in enumerate(lines) if brp.TURN.match(ln)), len(lines))
        body, _, _ = brp._cut_notes("\n".join(lines[:first_turn]))
        missing = [p.strip("*:") for p in SHAPE_PARTS if p not in body]
        if not re.search(r"^\s*\|.*\|\s*$", body, re.MULTILINE):
            missing.append("options table")
        elif (opts := brp._options(body))["options"] and not opts["implemented"]:
            missing.append("row marked (implemented), which the page's As implemented locks in")
        problem = PROBLEM_RE.search(body)
        if problem:
            missing += _problem_shape(problem.group(1))
        ids = sorted(set(RULE_ID.findall(body + " " + it["title_md"])))
        if missing:
            out.append(f"{entry.name} issue {it['n']}: no {', '.join(missing)}")
        if ids:
            out.append(f"{entry.name} issue {it['n']}: rule IDs in the text ({', '.join(ids)}); move them to footnotes")
    return out + _horizon_warnings(entry)


def _horizon_warnings(entry: Entry) -> list[str]:
    """What the ``**Horizon:**`` block of ``entry`` misses of its issue shape (the page shows it as the issue H)."""
    if not entry.horizon or CLOSING_RE.search(entry.horizon):  # a settled horizon keeps the shape it had
        return []
    body, _, _ = brp._cut_notes(entry.horizon)
    missing = [p.strip("*:") for p in HORIZON_PARTS if p not in body]
    if "**Options:**" in body and not brp._options(body)["implemented"]:
        missing.append("row marked (implemented): today's length")
    if "**Options:**" in body and not HORIZON_SIZE_COLUMN.search(body):
        missing.append("`Test windows` column (the size of each option's test windows)")
    return [f"{entry.name} horizon: no {', '.join(missing)} (the page shows it as issue H)"] if missing else []


def collect(root: Path, records: Path, names: list[str] | None = None) -> Collected:
    """Read the review files of the working copy ``root`` and the records in ``records``.

    Raises:
        ReviewFileError: A review breaks the format, or a dataset folder holds a review file.
    """
    for folder, option in ((root, "--root"), (records, "--records")):
        if not folder.is_dir():
            raise ReviewFileError(folder, None, f"no such folder; run from the repository root or pass {option}")
    stray = folder_review_files(root)
    if stray:
        raise ReviewFileError(
            stray[0],
            None,
            "a review file in a dataset folder: the review lives in the record's `## Review` (run "
            "move_reviews_to_records.py)",
        )
    entries: dict[str, Entry] = {}
    for path in sorted(records.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text()
        if "\n## Review\n" not in text and "**Open issues (AI," not in text:
            continue
        entry = parse_record_review(path)
        if entry is not None:
            entries[entry.name] = entry
    if names is not None:
        unknown = sorted(set(names) - set(entries))
        if unknown:
            raise ReviewFileError(records, None, f"no review in the records of {unknown}")
        entries = {n: e for n, e in entries.items() if n in names}
    across, n_across = parse_across(root / REVIEW_FILE) if (root / REVIEW_FILE).is_file() else ("", 0)
    return Collected(entries=[entries[n] for n in sorted(entries)], across=across, across_items=n_across)


CLOSING_RE = re.compile(r"\*\*(Resolved|Deferred) \(")
"""A closing turn; the last one says whether an item is parked (Deferred) or settled (Resolved)."""


def is_settled(
    entry: Entry,
    records: Path,
    metric_marks: set[str] | frozenset[str] | None = frozenset(),
    horizon_marks: set[str] | frozenset[str] | None = frozenset(),
) -> bool:
    """Whether nothing on ``entry`` waits for the curator: every issue resolved (none left deferred), no record-field
    row, no triage verdict to verify, and, for a dataset with a folder whose metric the round marks (``metric_marks``,
    ``None`` for every record), the record's CC line that the declared metric is checked; likewise for the horizon
    (``horizon_marks``). Such a record ships by default and leaves the page (Lennart, 2026-11-08); its review stays
    in the record. A metric or a horizon the round does not ask about never keeps a record on the page (Lennart,
    2026-11-10).
    """
    if entry.fields:
        return False
    for item in brp._split_items(entry.issues)[1]:
        closings = CLOSING_RE.findall(item["body_md"])
        parked = (closings[-1] if closings else "") == "Deferred" or item["title_md"].startswith("Deferred")
        if not item["resolved"] or parked:
            return False
    record = records / f"{entry.name}.md"
    # A record that triage decided (No) waits for the curator's check, unless it was added: a dataset retired after
    # its review keeps the review in its record, settled.
    if not record.is_file() or (entry.folder is None and brp._decided(record)):
        return False
    if not entry.folder:
        return True
    for marks, checked in ((metric_marks, brp._metric_checked), (horizon_marks, brp._horizon_checked)):
        if (marks is None or entry.name in marks) and checked(record) is None:
            return False
    return True


def _settled_lines(collected: Collected) -> list[str]:
    """The report's lines naming the records whose metric the round marks and those left out as settled, or nothing."""
    out = []
    for label, marks in (
        (brp.METRIC_MARKS_LABEL, collected.metric_marks),
        (brp.HORIZON_MARKS_LABEL, collected.horizon_marks),
    ):
        if marks is None:
            out += [f"{label} all.", ""]
        elif marks:
            out += [f"{label} {', '.join(f'`{n}`' for n in sorted(marks))}.", ""]
    if collected.settled:
        names = ", ".join(f"`{n}`" for n in collected.settled)
        out += [f"**Settled, left out (they ship by default):** {names}.", ""]
    return out


def _cell(text: str) -> str:
    return re.sub(r"(?<!\\)\|", r"\\|", text)


def _plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def render_report(collected: Collected, *, title: str, date: str) -> str:
    """The report in the format build_review_page.py reads."""
    entries = collected.entries
    n_records = len(entries) - collected.n_folders
    sources = [
        f"the records' reviews of {_plural(collected.n_folders, 'added dataset')}",
        f"of {_plural(n_records, 'record')} without a folder",
    ]
    if collected.across:
        sources.append("the working copy's REVIEW.md")
    n_issues = sum(len(e.numbers) for e in entries)
    n_fields = sum(len(e.fields) for e in entries)
    out = [
        f"# {title} ({date})",
        "",
        f"Open review issues, collected by `collect_reviews.py` on {date} from {', '.join(sources[:-1])} and "
        f"{sources[-1]}. Edit those files, not this report.",
        "",
        f"**Open:** {_plural(len(entries), 'record')}, {_plural(n_issues, 'issue')}, "
        f"{_plural(n_fields, 'record field')}, {_plural(collected.across_items, 'cross-dataset item')}.",
        "",
        *_settled_lines(collected),
        "## Summary per record",
        "",
        "| Record | Outcome | Main points |",
        "|---|---|---|",
    ]
    out += [f"| [`{e.name}`](#{e.name}) | {_cell(e.cell)} | {_cell(e.points)} |" for e in entries]
    if n_fields:
        out += ["", "## Record fields that disagree with the definition", ""]
        for e in entries:
            if e.fields:
                parts = "; ".join(f"{key} `{rec}`, definition `{dfn}`" for key, rec, dfn in e.fields)
                out.append(f"- `{e.name}`: {parts}.")
    if collected.across:
        out += ["", "## Across datasets", "", collected.across]
    out += _per_dataset_lines(entries)
    return "\n".join(out) + "\n"


def _per_dataset_lines(entries: list[Entry]) -> list[str]:
    """The report's per-record sections, under one heading, or nothing when no record is left."""
    if not entries:
        return []
    out = ["", "## Per dataset"]
    for e in entries:
        out += ["", f"### {e.name}", "", f"**Outcome:** {e.outcome}"]
        if e.judgment:
            out += ["", f"**Record judgment:** {e.judgment}"]
        if e.horizon:
            out += ["", f"**Horizon:** {e.horizon}"]
        if e.numbers:
            out += ["", f"**{e.issues_label}:**", "", e.issues]
        if e.panel:
            out += ["", e.panel]
    return out


def check_report(path: Path, collected: Collected) -> None:
    """Parse the written report with the builder and compare it with what was collected.

    Raises:
        brp.ReportFormatError: The builder cannot parse the report.
        ReviewFileError: The builder sees other issues, fields or items than the collector read.
    """
    report = brp.parse_report(path)
    for e in collected.entries:
        got = [it["n"] for it in report["records"][e.name]["items"]]
        if got != e.numbers:
            raise ReviewFileError(e.source, None, f"the page would show issues {got}, the file has {e.numbers}")
        if len(report["fields"].get(e.name, [])) != len(e.fields):
            raise ReviewFileError(e.source, None, "the page would not show every record field")
        panel = report["records"][e.name]["panel"]
        got_roles = [s["title"] for s in panel["sections"]] if panel else []
        if bool(panel) != bool(e.panel) or got_roles != e.panel_sections:
            raise ReviewFileError(
                e.source, None, f"the page would show the panel sections {got_roles}, the file has {e.panel_sections}"
            )
    n_items = sum(len(s["items"]) for s in report["crosscut"])
    if n_items != collected.across_items:
        raise ReviewFileError(
            path, None, f"the page would show {n_items} cross-dataset items, not {collected.across_items}"
        )


def _marks(value: str | None) -> set[str] | None:
    """The names of a ``--metric-marks`` or ``--horizon-marks`` flag (``None`` for ``all``)."""
    marks = {n.strip() for n in (value or "").split(",") if n.strip()}
    return None if marks == {"all"} else marks


def main(argv: list[str] | None = None) -> int:
    """Collect the review files, write the report and check it with the builder's parser."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"), help="The working copy.")
    parser.add_argument("--out", type=Path, required=True, help="The report to write (markdown).")
    parser.add_argument("--records", type=Path, default=Path("curation/records"), help="The curation records.")
    parser.add_argument("--names", help="Comma-separated unique names: collect only these records.")
    parser.add_argument("--title", default="Open review issues", help="The report's title (the page shows it).")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="The date in the title (YYYY-MM-DD).")
    parser.add_argument(
        "--metric-marks",
        help=(
            "Comma-separated unique names, or `all`: the records whose declared metric is a choice of this round (new "
            "datasets, a proposed metric change). The page shows the metric and a mark on it only for these."
        ),
    )
    parser.add_argument(
        "--horizon-marks",
        help=(
            "Comma-separated unique names, or `all`: the temporal records whose horizon and test windows the curator "
            "signs off in this round (new datasets, or when asked). The page shows them with a mark only for these."
        ),
    )
    parser.add_argument(
        "--keep-settled",
        action="store_true",
        help="Keep the records with nothing left to decide (left out by default: they ship by default).",
    )
    args = parser.parse_args(argv)
    try:
        dt.date.fromisoformat(args.date)
    except ValueError:
        parser.error(f"--date {args.date!r} is not YYYY-MM-DD")
    names = [n.strip() for n in args.names.split(",") if n.strip()] if args.names else None
    metric_marks, horizon_marks = _marks(args.metric_marks), _marks(args.horizon_marks)
    try:
        collected = collect(args.root, args.records, names)
        for flag, marks in (("--metric-marks", metric_marks), ("--horizon-marks", horizon_marks)):
            unknown = sorted((marks or set()) - {e.name for e in collected.entries})
            if unknown:
                print(f"error: {flag} names records without open review: {', '.join(unknown)}", file=sys.stderr)
                return 1
        collected.metric_marks, collected.horizon_marks = metric_marks, horizon_marks
        if not args.keep_settled:
            settled = [e.name for e in collected.entries if is_settled(e, args.records, metric_marks, horizon_marks)]
            collected.entries = [e for e in collected.entries if e.name not in settled]
            collected.settled = settled
        if not collected.entries and not collected.across_items:
            names = ", ".join(collected.settled)
            print(f"nothing left to decide for {names}: no report written (--keep-settled writes one)")
            return 0
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(render_report(collected, title=args.title, date=args.date))
        check_report(args.out, collected)
    except (ReviewFileError, brp.ReportFormatError) as error:
        print(f"error: {error}\nThe format: {FORMAT}", file=sys.stderr)
        return 1
    entries = collected.entries
    print(
        f"records {len(entries)} ({collected.n_folders} with a folder, {len(entries) - collected.n_folders} "
        f"without), issues {sum(len(e.numbers) for e in entries)}, "
        f"field rows {sum(len(e.fields) for e in entries)}, cross-dataset items {collected.across_items}, "
        f"review panels {sum(1 for e in entries if e.panel)}"
    )
    if collected.settled:
        print(
            f"left out {_plural(len(collected.settled), 'settled record')} (--keep-settled keeps them): "
            f"{', '.join(collected.settled)}"
        )
    for warning in (w for e in entries for w in shape_warnings(e)):
        print(f"warning: {warning}", file=sys.stderr)
    print(f"{args.out} written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
