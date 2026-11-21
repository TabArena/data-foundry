"""No definition or record names an internal artefact (knowledge-curation, writing.md, "No internal references").

A definition's text (its notes, its task summary, its comments) is copied into the README that outside readers see, so
it names no scheduler job, no temporary path, no review page or its item numbers and no pull request: a decision is
cited by who made it and when. The records are the internal decision log; they may cite their own `## Review` items and
pull requests, but not job ids, the scheduler or the review page, which is only a temporary view of those items. Home
and run-folder paths are checked for every committed file by ``test_no_local_paths.py``.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS = sorted((ROOT / "datasets").rglob("dataset.py"))
RECORDS = sorted((ROOT / "curation" / "records").glob("*.md"))

IN_BOTH = (
    r"\b[Ss]lurm\b"  # the scheduler
    r"|\bjobs? \d{6,}"  # a job id
    r"|\b[Rr]eview page\b|\bpage v\d+\b"  # the review page and its versions
    r"|\b[Bb]lind split review page\b|\b[Ss]plit [Cc]heck page\b"
)
IN_RECORDS = re.compile(IN_BOTH + r"|\bPR #50\b|\(#50\)|\bon #50\b")  # the pull request that was split up
IN_DEFINITIONS = re.compile(
    IN_BOTH
    + r"|/tmp/"  # a temporary file
    + r"|\b[Ii]ssues? \d+\b|\b[Rr]eview items? \d|\bcross-dataset\s+item\b"  # an item of the review
    + r"|\b(?:PR|[Pp]ull request|[Ii]ssue) #?\d+|\(#\d{2,4}\b"  # a pull request or GitHub issue
)


def _hits(paths: list[Path], pattern: re.Pattern[str]) -> list[str]:
    hits = []
    for path in paths:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if match := pattern.search(line):
                hits.append(f"{path.relative_to(ROOT)}:{number}: {match.group(0)!r} in {line.strip()[:120]!r}")
    return hits


def test_definitions_name_no_internal_artefact():
    """Every definition cites decisions by who and when, not by job, page, review item or pull request."""
    hits = _hits(DEFINITIONS, IN_DEFINITIONS)
    assert not hits, "Internal references in definitions (writing.md, 'No internal references'):\n" + "\n".join(hits)


def test_records_name_no_job_or_review_page():
    """Every record keeps its evidence and decisions without job ids, the scheduler or the review page."""
    hits = _hits(RECORDS, IN_RECORDS)
    assert not hits, "Internal references in records (writing.md, 'No internal references'):\n" + "\n".join(hits)


@pytest.mark.parametrize(
    ("text", "flagged"),
    [
        ("measured on Slurm job 1365902", True),
        ("LightGBM on jobs 1377583/4", True),
        ("(Andrej, 2026-11-03, review issue 6: B)", True),
        ("(Review issue 9, A)", True),
        ("the exposure study (#51; D13)", True),
        ("the proposal of PR #46", True),
        ("BeyondArena v0.2 review page, issue 5, A", True),
        ("page v43", True),
        ("Decided (Lennart, 2026-11-11, cross-dataset item)", True),
        ("/tmp/scratch/x.csv", True),  # noqa: S108
        ('(Andrej, 2026-11-03: "We can keep RMSE in this case")', False),
        ("SPLIT-33 sets nine splits for 8,967 patients", False),
        ("color '#1f77b4'", False),
        ("750 Van Ness Ave #706", False),
        ("the study of issue #70", True),
        ("the 2,000 rows of window 3", False),
    ],
)
def test_definition_pattern(text, flagged):
    """The definition pattern flags jobs, the page, review items, pull requests and temporary paths, nothing else."""
    assert bool(IN_DEFINITIONS.search(text)) is flagged


@pytest.mark.parametrize(
    ("text", "flagged"),
    [
        ("CC (2026-11-10, Andrej): Review issue 2, B: grouped by station", False),
        ("pushed to PR #97", False),
        ("(BeyondArena v0.2 review page, issue 5, A)", True),
        ("once PR #50 is in the working copy", True),
        ("Slurm jobs 1377583/4: ROC AUC 0.786", True),
    ],
)
def test_record_pattern(text, flagged):
    """The record pattern lets a record cite its own review items and pull requests, not jobs or the page."""
    assert bool(IN_RECORDS.search(text)) is flagged
