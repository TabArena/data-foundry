r"""Collect the open review issues of the working copy into one report for build_review_page.py.

Usage, from the repository root::

    .venv/bin/python .claude/skills/review-added-datasets/scripts/collect_reviews.py \
        --root datasets/_dev/tabarena-v0pt2 --out <report.md> [--names a,b] [--title <text>] [--date <YYYY-MM-DD>]
        [--records curation/records]

Reads every ``<root>/<folder>/REVIEW.md`` (the open issues of one dataset), the optional ``<root>/REVIEW.md`` (items
across datasets) and the ``**Open issues (AI, <date>):**`` block of the records without a folder, and writes one
report that ``build_review_page.py`` turns into the review page. The format of these files and of the report is
``references/review_file_format.md``; a file that breaks it stops the collector with the file and the line. The
report is checked with the builder's own parser before the collector reports success.

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
FORMAT = HERE.parent / "references" / "review_file_format.md"

TITLE_RE = re.compile(r"^# ([a-z0-9_]+)\s*$")
LABEL_RE = re.compile(r"^\*\*([^*]+?):\*\*\s*(.*)$")
BLOCKS = ("outcome", "points", "fields", "judgment", "issues")
"""The blocks of a REVIEW.md, in the order they appear."""
LABELS = {
    "Outcome": "outcome",
    "Main points": "points",
    "Record fields that disagree with the definition": "fields",
    "Record judgment": "judgment",
}
ISSUES_LABEL = re.compile(r"^Issues(?: for [^*:]+)?$")
FIELD_RE = re.compile(r"^- `([a-z_]+)`: record `([^`]+)`, definition `([^`]+)`\.?$")
OPEN_BLOCK_RE = re.compile(r"^\*\*Open issues \(AI, (\d{4}-\d{2}-\d{2})\):\*\*\s*(.*)$")
ISSUE_START = re.compile(r"^\d+\. ")
SENTENCE_END = re.compile(r"\.(?=\s|$)")


class ReviewFileError(ValueError):
    """A review file does not follow ``references/review_file_format.md``."""

    def __init__(self, path: Path, index: int | None, message: str) -> None:
        """Name the file and the line (``index`` counts from 0; None for the whole file) in the message."""
        where = f"{path}, line {index + 1}" if index is not None else str(path)
        super().__init__(f"{where}: {message}")


@dataclass
class Entry:
    """One record on the page: from its folder's REVIEW.md or from the open-issues block of its record."""

    name: str
    folder: str | None
    source: Path
    outcome: str
    points: str
    cell: str
    judgment: str = ""
    issues_label: str = "Issues"
    issues: str = ""
    numbers: list[int] = field(default_factory=list)
    fields: list[tuple[str, str, str]] = field(default_factory=list)


@dataclass
class Collected:
    """Everything the report holds: the records, sorted by unique name, and the cross-dataset sections."""

    entries: list[Entry]
    across: str = ""
    across_items: int = 0

    @property
    def n_folders(self) -> int:
        """The records that come from a REVIEW.md."""
        return sum(1 for e in self.entries if e.folder)


@dataclass
class _Block:
    """A labelled block of a REVIEW.md: its label, the index of its label line, that line's rest, the lines below."""

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
    for k, it in enumerate(items):
        if it["resolved"]:
            raise ReviewFileError(
                path,
                at[k],
                f"issue {it['n']} is closed (Resolved or Deferred); a settled issue leaves the file, its decision goes "
                "to the definition and the record",
            )
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
    for i in range(1, len(lines)):
        line = lines[i]
        m = LABEL_RE.match(line)
        label = m.group(1).strip() if m else ""
        key = LABELS.get(label) or ("issues" if m and ISSUES_LABEL.match(label) else None)
        if key is None:
            if line.startswith("#"):
                raise ReviewFileError(path, i, "a heading after the title; a REVIEW.md holds only its labelled blocks")
            if current is None and line.strip():
                raise ReviewFileError(path, i, "text before `**Outcome:**`")
            if current is not None:
                current.lines.append(line)
            continue
        if key in blocks:
            raise ReviewFileError(path, i, f"a second `**{label}:**` block")
        if current is not None and BLOCKS.index(key) < BLOCKS.index(next(reversed(blocks))):
            raise ReviewFileError(path, i, f"`**{label}:**` comes before the blocks above it (see the format)")
        if key in ("fields", "issues") and m.group(2).strip():
            raise ReviewFileError(path, i, f"the `**{label}:**` label stands alone; its rows follow below it")
        current = blocks[key] = _Block(label, i, m.group(2))
    return blocks


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


def parse_review_file(path: Path, folder: str) -> Entry:
    """One dataset's REVIEW.md.

    Raises:
        ReviewFileError: The file does not follow ``references/review_file_format.md``.
    """
    lines = path.read_text().splitlines()
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
    if not numbers and not fields:
        raise ReviewFileError(path, None, "no open issue and no record field; delete the file")
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
        issues_label=blocks["issues"].label if "issues" in blocks else "Issues",
        issues=issues,
        numbers=numbers,
        fields=fields,
    )


def parse_record_block(path: Path, name: str) -> Entry | None:
    """The ``**Open issues (AI, <date>):**`` block of a record's comments, or None when it has none.

    Raises:
        ReviewFileError: The block does not follow ``references/review_file_format.md``.
    """
    lines = path.read_text().splitlines()
    starts = [i for i, ln in enumerate(lines) if OPEN_BLOCK_RE.match(ln)]
    if not starts:
        return None
    if len(starts) > 1:
        raise ReviewFileError(path, starts[1], "a second open-issues block; a record has one")
    at = starts[0]
    if not any(OPEN_BLOCK_RE.match(ln) for ln in (load_record(path).comments or "").splitlines()):
        raise ReviewFileError(path, at, "the open-issues block is not in the record's `## Comments`")
    i = at + 1
    while i < len(lines) and lines[i].strip():
        i += 1
    lead, first = [OPEN_BLOCK_RE.match(lines[at]).group(2), *lines[at + 1 : i]], i
    while i < len(lines):
        if lines[i].strip() and not lines[i].startswith((" ", "\t")) and not ISSUE_START.match(lines[i]):
            break
        i += 1
    issues, numbers = _check_issues(path, first, lines[first:i])
    if not numbers:
        raise ReviewFileError(path, at, "no numbered issue after the lead; remove the block when nothing is open")
    outcome = " ".join(" ".join(lead).split())
    cell = _first_sentence(outcome)
    _check_outcome(path, at, cell, name, None)
    return Entry(
        name=name,
        folder=None,
        source=path,
        outcome=outcome,
        points=outcome[len(cell) :].lstrip(". ") or cell,
        cell=cell,
        issues=issues,
        numbers=numbers,
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


def _folder_entries(root: Path, records: Path) -> dict[str, Entry]:
    """The REVIEW.md of each folder of the working copy, checked against its record."""
    entries: dict[str, Entry] = {}
    for path in sorted(root.glob(f"*/{REVIEW_FILE}")):
        folder = path.parent.name
        if folder.startswith(("_", ".")):
            continue
        entry = parse_review_file(path, folder)
        record = records / f"{entry.name}.md"
        if not record.is_file():
            raise ReviewFileError(path, 0, f"no curation record {record}")
        v2_path = load_record(record).v2_path
        if v2_path and Path(v2_path).parent.name != folder:
            raise ReviewFileError(path, 0, f"the record's v2_path is {v2_path}, not in the folder {folder}/")
        if entry.name in entries:
            raise ReviewFileError(path, 0, f"`{entry.name}` has a second REVIEW.md ({entries[entry.name].source})")
        entries[entry.name] = entry
    return entries


def _record_entries(root: Path, records: Path, folders: dict[str, Entry]) -> dict[str, Entry]:
    """The open-issues blocks of the records without a folder."""
    entries: dict[str, Entry] = {}
    for record in sorted(records.glob("*.md")):
        if record.name.startswith("_") or "**Open issues (AI," not in record.read_text():
            continue
        entry = parse_record_block(record, record.stem)
        if entry is None:
            continue
        if entry.name in folders:
            raise ReviewFileError(record, None, f"its open issues belong in {folders[entry.name].source} only")
        v2_path = load_record(record).v2_path
        if v2_path and (root / Path(v2_path).parent.name).is_dir():
            raise ReviewFileError(record, None, f"its folder exists; move the open issues to its {REVIEW_FILE}")
        entries[entry.name] = entry
    return entries


def collect(root: Path, records: Path, names: list[str] | None = None) -> Collected:
    """Read the review files of the working copy ``root`` and the records in ``records``.

    Raises:
        ReviewFileError: A file breaks the format, or a REVIEW.md and its record disagree.
    """
    for folder, option in ((root, "--root"), (records, "--records")):
        if not folder.is_dir():
            raise ReviewFileError(folder, None, f"no such folder; run from the repository root or pass {option}")
    entries = _folder_entries(root, records)
    entries.update(_record_entries(root, records, entries))
    if names is not None:
        unknown = sorted(set(names) - set(entries))
        if unknown:
            raise ReviewFileError(root, None, f"no review file or open-issues block for {unknown}")
        entries = {n: e for n, e in entries.items() if n in names}
    across, n_across = parse_across(root / REVIEW_FILE) if (root / REVIEW_FILE).is_file() else ("", 0)
    return Collected(entries=[entries[n] for n in sorted(entries)], across=across, across_items=n_across)


def _cell(text: str) -> str:
    return re.sub(r"(?<!\\)\|", r"\\|", text)


def _plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def render_report(collected: Collected, *, title: str, date: str) -> str:
    """The report in the format build_review_page.py reads."""
    entries = collected.entries
    n_records = len(entries) - collected.n_folders
    sources = [
        f"the REVIEW.md of {_plural(collected.n_folders, 'dataset')}",
        f"the open issues of {_plural(n_records, 'record')} without a folder",
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
    out += ["", "## Per dataset"]
    for e in entries:
        out += ["", f"### {e.name}", "", f"**Outcome:** {e.outcome}"]
        if e.judgment:
            out += ["", f"**Record judgment:** {e.judgment}"]
        if e.numbers:
            out += ["", f"**{e.issues_label}:**", "", e.issues]
    return "\n".join(out) + "\n"


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
    n_items = sum(len(s["items"]) for s in report["crosscut"])
    if n_items != collected.across_items:
        raise ReviewFileError(
            path, None, f"the page would show {n_items} cross-dataset items, not {collected.across_items}"
        )


def main(argv: list[str] | None = None) -> int:
    """Collect the review files, write the report and check it with the builder's parser."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"), help="The working copy.")
    parser.add_argument("--out", type=Path, required=True, help="The report to write (markdown).")
    parser.add_argument("--records", type=Path, default=Path("curation/records"), help="The curation records.")
    parser.add_argument("--names", help="Comma-separated unique names: collect only these records.")
    parser.add_argument("--title", default="Open review issues", help="The report's title (the page shows it).")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="The date in the title (YYYY-MM-DD).")
    args = parser.parse_args(argv)
    try:
        dt.date.fromisoformat(args.date)
    except ValueError:
        parser.error(f"--date {args.date!r} is not YYYY-MM-DD")
    names = [n.strip() for n in args.names.split(",") if n.strip()] if args.names else None
    try:
        collected = collect(args.root, args.records, names)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(render_report(collected, title=args.title, date=args.date))
        check_report(args.out, collected)
    except (ReviewFileError, brp.ReportFormatError) as error:
        print(f"error: {error}\nThe format: {FORMAT}", file=sys.stderr)
        return 1
    entries = collected.entries
    print(
        f"records {len(entries)} ({collected.n_folders} with a REVIEW.md, {len(entries) - collected.n_folders} "
        f"without a folder), issues {sum(len(e.numbers) for e in entries)}, "
        f"field rows {sum(len(e.fields) for e in entries)}, cross-dataset items {collected.across_items}"
    )
    print(f"{args.out} written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
