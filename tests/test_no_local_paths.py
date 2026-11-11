"""No committed file names a local path: a run folder of the local warehouse or a folder in someone's home.

Only one machine has such a folder, so a pointer to it leads nowhere for every other reader; the evidence goes into the
text and a script worth keeping into the repository (knowledge-data-foundry, house rules; Lennart, 2026-11-11). The
BeyondArena notebooks (v1, frozen) keep the paths in their saved outputs and are not checked. Dot folders in a home
(the caches, the Kaggle and gspread credentials) are standard locations, not someone's files, and pass.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = {".md", ".py", ".yaml", ".yml", ".toml", ".txt", ".cfg", ".sh", ".json", ".html", ".css", ".js"}
SKIP = {
    "tests/test_no_local_paths.py",  # the patterns themselves
    "tests/test_claude_agents.py",  # made-up paths outside the task gamer's sandbox, which the hook must refuse
}
LOCAL_PATH = re.compile(
    r"_runs/\d{4}-\d{2}-\d{2}"  # a dated run folder of the warehouse
    r"|claude_jobs"  # a job folder in a home
    r"|(?<![\w.:/-])~/[\w-]"  # a folder in a home, by tilde (a dot folder passes)
    r"|(?<![\w.:/-])/(?:home|Users)/[\w.-]+/"  # a folder in a home, absolute (a URL's /home/ passes)
)


def _committed_files() -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z"],  # noqa: S607
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("not a git checkout")
    names = [n for n in out.split("\0") if n and n not in SKIP]
    return [ROOT / n for n in names if Path(n).suffix in SUFFIXES and (ROOT / n).is_file()]


def test_no_local_paths_in_committed_files():
    """Every committed text file is free of run-folder and home-folder paths."""
    hits = []
    for path in _committed_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if match := LOCAL_PATH.search(line):
                hits.append(f"{path.relative_to(ROOT)}:{number}: {match.group(0)!r} in {line.strip()[:120]!r}")
    assert not hits, (
        "Local paths in committed files (only one machine has them; write the evidence into the text instead):\n"
        + "\n".join(hits)
    )


@pytest.mark.parametrize(
    ("text", "flagged"),
    [
        ("Evidence: `local-data-warehouse/_runs/2026-11-01_scaffold_checks/qsar_tid_11/`.", True),
        ("record `_runs/2026-11-02_pg16_amount_check`", True),
        ("(`~/" + "claude_jobs/dia_review/`)", True),
        ("Run folder: `~/workdir/runs/`", True),
        ('Path("/home/someone/code/data-foundry/local-data-warehouse")', True),
        ("/Users/someone/Downloads/x.csv", True),
        ("the run folder `local-data-warehouse/_runs/<date>_<run>/`", False),
        ("The cache is `~/.cache/data_foundry/<collection>/`", False),
        ("https://sites.wustl.edu/oasisbrains/home/oasis-1/", False),
        ("a home folder (`~/<folder>/`, `/home/<user>/`)", False),
        ("on `/home`, with 1.7 TB free", False),
    ],
)
def test_pattern(text, flagged):
    """The pattern flags dated run folders and home folders, not templates, dot folders or URLs."""
    assert bool(LOCAL_PATH.search(text)) is flagged
