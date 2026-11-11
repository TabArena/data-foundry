#!/usr/bin/env python
"""Move each dataset's ``REVIEW.md`` into the ``## Review`` section of its curation record.

A dataset's review (the outcome, the horizon, the numbered issues with every turn, the review panel) lives in its
record, ``curation/records/<unique_name>.md``, so the record is the one source of the dataset's curation (Lennart,
2026-11-11). This script moves what a branch still has in folder files, for example after a rebase onto the change:

* every ``<root>/<folder>/REVIEW.md`` goes into the record its title names (``# <unique_name>``, the folder checked
  against the record's ``v2_path``), without the title line, and the file is deleted;
* the review's relative links are re-pointed from the folder to the records;
* the pointers to those files in the records' comments and the definitions' texts are rewritten: "REVIEW.md issue 3"
  becomes "Review issue 3", "its `REVIEW.md`" becomes "its Review" (lines that tell of a file being removed, and the
  working copy's cross-dataset ``REVIEW.md``, stay as written).

Usage::

    .venv/bin/python .claude/skills/review-added-datasets/scripts/move_reviews_to_records.py [--check]
        [--root datasets/_dev/tabarena-v0pt2] [--records curation/records]

``--check`` changes nothing: it lists the files that would move and exits 1 when there is one.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import warnings
from pathlib import Path

from data_foundry.curation.store import load_record, save_record

REVIEW_FILE = "REVIEW.md"
TITLE_RE = re.compile(r"^# (\S+)\s*$")

KEEP_RE = re.compile(
    r"working copy(?:'s)? `?REVIEW\.md`?|cross-dataset `?REVIEW\.md`?|root `?REVIEW\.md`?"
    r"|`?REVIEW\.md`?(?: issues? [\d, and]+)?,? (?:which |that )?(?:is |was |are |were )?(?:settled and )?"
    r"(?:removed|deleted|gone)|(?:the folder's )?`?REVIEW\.md`? goes"
)
"""Kept as written: the working copy's cross-dataset ``REVIEW.md``, which stays a file, and history that tells of a
review file or issue being removed ("REVIEW.md removed (nothing left open)")."""

POINTERS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"the folder's `?REVIEW\.md`?"), "the record's Review"),
    (re.compile(r"\bno `?REVIEW\.md`?"), "no review"),
    (re.compile(r"`?REVIEW\.md`?(?= (?:issues?|horizon|Horizon)\b)"), "Review"),
    (re.compile(r"\b(its|their|the|this|his) `?REVIEW\.md`?"), r"\1 Review"),
    (re.compile(r"(\w)'s `?REVIEW\.md`?"), r"\1's Review"),
    (re.compile(r"\bin `?REVIEW\.md`?"), "in the Review"),
    (re.compile(r"`?REVIEW\.md`?"), "the Review"),
)
"""Pointer forms, tried in order on each line; the last catches the rest."""


def rewrite_pointers(text: str) -> tuple[str, list[tuple[str, str]]]:
    """``text`` with its pointers to a dataset's ``REVIEW.md`` rewritten, and the changed lines (old, new)."""
    out, changed = [], []
    for line in text.split("\n"):
        new = line
        if "REVIEW.md" in line:
            kept: list[str] = []

            def hold(m: re.Match[str], kept: list[str] = kept) -> str:
                kept.append(m.group(0))
                return f"\x00{len(kept) - 1}\x00"

            new = KEEP_RE.sub(hold, line)
            for pattern, repl in POINTERS:
                new = pattern.sub(repl, new)
            new = re.sub(r"\x00(\d+)\x00", lambda m, kept=kept: kept[int(m.group(1))], new)
        if new != line:
            changed.append((line, new))
        out.append(new)
    return "\n".join(out), changed


LINK_RE = re.compile(r"(?<!!)(\[[^\]]*\]\()([^)\s#]+)((?:#[^)\s]*)?(?:\s+\"[^\"]*\")?\))")
"""A markdown link with a target; an image or an anchor-only link is left alone."""


def relink(text: str, old_dir: Path, new_dir: Path) -> str:
    """``text`` with each relative link re-pointed from ``old_dir`` (the folder) to ``new_dir`` (the records)."""

    def fix(m: re.Match[str]) -> str:
        target = m.group(2)
        if re.match(r"^[a-z][a-z0-9+.-]*:", target):
            return m.group(0)
        new = Path(os.path.relpath((old_dir / target).resolve(), new_dir.resolve())).as_posix()
        return m.group(1) + new + m.group(3)

    return LINK_RE.sub(fix, text)


def review_files(root: Path) -> list[Path]:
    """The ``REVIEW.md`` of each dataset folder (the working copy's own cross-dataset file is not one)."""
    return [p for p in sorted(root.glob(f"*/{REVIEW_FILE}")) if not p.parent.name.startswith(("_", "."))]


def move(path: Path, records: Path) -> str:
    """Move one folder's review into its record; return the record's name.

    Raises:
        ValueError: The file has no title, its record is missing or points at another folder, the record already has a
            review, or the review holds a ``## `` heading (the record's next section would cut it).
    """
    text = path.read_text()
    lines = text.split("\n")
    title = TITLE_RE.match(lines[0]) if lines else None
    if title is None:
        raise ValueError(f"{path}: the first line is not `# <unique_name>`")
    name = title.group(1)
    record_path = records / f"{name}.md"
    if not record_path.is_file():
        raise ValueError(f"{path}: no record {record_path}")
    record = load_record(record_path)
    if record.v2_path and Path(record.v2_path).parent.name != path.parent.name:
        raise ValueError(f"{path}: the record's v2_path is {record.v2_path}")
    if record.review:
        raise ValueError(f"{path}: {record_path} already has a review; merge the two by hand")
    body = "\n".join(lines[1:]).strip()
    heading = next((ln for ln in body.split("\n") if ln.startswith("## ")), None)
    if heading is not None:
        raise ValueError(f"{path}: a `## ` heading inside the review ({heading!r})")
    record.review = relink(body, path.parent, records)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # a claim warning: the move keeps the content, whoever holds the dataset
        save_record(record, records)
    path.unlink()
    return name


def _show(source: str, changed: list[tuple[str, str]]) -> None:
    for old, new in changed:
        print(f"{source}: {old.strip()[:100]}\n  -> {new.strip()[:100]}")


def rewrite_records(records: Path) -> int:
    """Rewrite the pointers in every record's comments; return the number of changed lines."""
    n_lines = 0
    for record_path in sorted(records.glob("*.md")):
        if record_path.name.startswith("_"):
            continue
        record = load_record(record_path)
        if not record.comments or "REVIEW.md" not in record.comments:
            continue
        record.comments, changed = rewrite_pointers(record.comments)
        if changed:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                save_record(record, records)
            n_lines += len(changed)
            _show(record_path.name, changed)
    return n_lines


def rewrite_definitions(root: Path) -> int:
    """Rewrite the pointers in every definition of the working copy; return the number of changed lines."""
    n_lines = 0
    for definition in sorted(root.glob("*/dataset.py")):
        text = definition.read_text()
        if "REVIEW.md" not in text:
            continue
        new, changed = rewrite_pointers(text)
        if changed:
            definition.write_text(new)
            n_lines += len(changed)
            _show(f"{definition.parent.name}/dataset.py", changed)
    return n_lines


def main(argv: list[str] | None = None) -> int:
    """Move the reviews and rewrite the pointers (or, with `--check`, list what would move)."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--records", type=Path, default=Path("curation/records"))
    parser.add_argument("--check", action="store_true", help="list what would move; exit 1 when there is any")
    args = parser.parse_args(argv)

    files = review_files(args.root)
    if args.check:
        for path in files:
            print(f"would move {path}")
        return 1 if files else 0

    moved = [move(path, args.records) for path in files]
    print(f"moved {len(moved)} review(s) into their records")

    n_lines = rewrite_records(args.records) + rewrite_definitions(args.root)
    print(f"rewrote {n_lines} line(s) that pointed to a REVIEW.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
