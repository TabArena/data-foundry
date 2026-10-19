"""The review page of the review-added-datasets skill: the collector of the review files, the report parser, the page.

The scripts live in the skill, not in the package, so they are imported from their files. A missing script fails
the module: the review files of the working copy are checked here.
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

pytest.importorskip("markdown_it", reason="the review page needs markdown-it-py (the `curation` extra)")

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / ".claude" / "skills" / "review-added-datasets" / "scripts"
SCRIPT = SCRIPTS / "build_review_page.py"
COLLECTOR = SCRIPTS / "collect_reviews.py"
ROOT = REPO / "datasets" / "_dev" / "tabarena-v0pt2"
RECORDS = REPO / "curation" / "records"
FIXTURE = Path(__file__).parent / "fixtures" / "review_page_report.md"
REVIEW_FILES = Path(__file__).parent / "fixtures" / "review_files"
"""The example of references/review_file_format.md: collected, it gives FIXTURE."""
CHURN_SECTION = (
    "### churn_telco_south_asia_duplicate\n"
    + FIXTURE.read_text().split("### churn_telco_south_asia_duplicate\n", 1)[-1]
)
"""The fixture report's last record section, to the end of the report."""


def _import(name: str, path: Path):
    if not path.is_file():
        pytest.fail(f"{path} is missing", pytrace=False)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up there
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def brp():
    """The builder script, imported as a module."""
    return _import("build_review_page", SCRIPT)


@pytest.fixture(scope="module")
def crv(brp):  # noqa: ARG001 - the builder is loaded first: the collector imports it
    """The collector script, imported as a module (it imports the builder)."""
    return _import("collect_reviews", COLLECTOR)


def _in_git() -> bool:
    return shutil.which("git") is not None and (REPO / ".git").exists()


def _collect_fixture(crv, root: Path, records: Path, out: Path, *extra: str) -> int:
    args = ["--root", str(root), "--records", str(records), "--out", str(out)]
    return crv.main([*args, "--title", "Added datasets: issues", "--date", "2026-10-01", *extra])


def test_collector_writes_the_fixture_report(crv, tmp_path):
    """The example review files collect into the fixture report, which the builder parses."""
    out = tmp_path / "report.md"
    assert _collect_fixture(crv, REVIEW_FILES / "working_copy", REVIEW_FILES / "records", out) == 0
    assert out.read_text() == FIXTURE.read_text()

    collected = crv.collect(REVIEW_FILES / "working_copy", REVIEW_FILES / "records")
    by_name = {e.name: e for e in collected.entries}
    assert sorted(by_name) == ["airfoil_self_noise", "churn_telco_south_asia_duplicate"]
    assert (by_name["airfoil_self_noise"].folder, by_name["airfoil_self_noise"].numbers) == ("airfoil_self_noise", [1])
    assert by_name["airfoil_self_noise"].fields == [("year", "2014", "1989")]
    # The record's block ends before the later CC comment.
    other = by_name["churn_telco_south_asia_duplicate"]
    assert (other.folder, other.cell, other.numbers) == (None, "not added; duplicate", [1])
    assert "CC (" not in other.issues
    assert collected.across_items == 1


def test_collector_names_filter(crv, tmp_path):
    """--names keeps only the named records and stops on a name without review file."""
    out = tmp_path / "report.md"
    root, records = REVIEW_FILES / "working_copy", REVIEW_FILES / "records"
    assert _collect_fixture(crv, root, records, out, "--names", "airfoil_self_noise") == 0
    assert "### churn_telco_south_asia_duplicate" not in out.read_text()
    assert _collect_fixture(crv, root, records, out, "--names", "no_such_record") == 1


def _broken_copy(tmp_path: Path, file: str, old: str, new: str) -> tuple[Path, Path, Path]:
    """A copy of the example review files with one change, and the changed file."""
    shutil.copytree(REVIEW_FILES, tmp_path / "files")
    path = tmp_path / "files" / file
    text = path.read_text()
    assert old in text
    path.write_text(text.replace(old, new, 1))
    return tmp_path / "files" / "working_copy", tmp_path / "files" / "records", path


@pytest.mark.parametrize(
    ("file", "old", "new", "line", "message"),
    [
        (
            "working_copy/airfoil_self_noise/REVIEW.md",
            "1. **Keep",
            "1. **Resolved (2026-10-02): keep",
            15,
            "is closed (Resolved or Deferred)",
        ),
        ("working_copy/airfoil_self_noise/REVIEW.md", "   alternative.\n", "alternative.\n**Split:** x\n", 17, "label"),
        (
            "working_copy/airfoil_self_noise/REVIEW.md",
            "   alternative.\n",
            "   alternative.\n1. **Again.**\n",
            17,
            "twice",
        ),
        ("working_copy/airfoil_self_noise/REVIEW.md", "**Outcome:** added.", "**Outcome:** added as `x`.", 3, "names"),
        ("working_copy/airfoil_self_noise/REVIEW.md", "year`: record", "year`: rec", 9, "field row"),
        ("working_copy/airfoil_self_noise/REVIEW.md", "**Main points:**", "**Points:**", None, "Main points"),
        (
            "working_copy/airfoil_self_noise/REVIEW.md",
            "# airfoil_self_noise\n",
            "# airfoil_self_noise\nIntro.\n",
            2,
            "text before",
        ),
        ("records/churn_telco_south_asia_duplicate.md", "not added; duplicate", "duplicate", 12, "`not added`"),
        ("working_copy/REVIEW.md", "# Across datasets\n", "# Across datasets\nIntro.\n", 2, "only `### <section>`"),
    ],
)
def test_collector_errors_name_the_file_and_line(crv, tmp_path, file, old, new, line, message):
    """A review file that breaks the format stops the collector with the file and the line."""
    root, records, path = _broken_copy(tmp_path, file, old, new)
    with pytest.raises(crv.ReviewFileError, match=re.escape(message)) as error:
        crv.collect(root, records)
    assert str(error.value).startswith(f"{path}, line {line}:" if line else f"{path}:")


def test_working_copy_review_files_collect_and_parse(crv, brp, tmp_path):
    """The committed REVIEW.md files and open-issue blocks follow the format, and every issue reaches the page."""
    collected = crv.collect(ROOT, RECORDS)
    on_disk = sorted(p for p in ROOT.glob("*/REVIEW.md") if not p.parent.name.startswith(("_", ".")))
    assert collected.n_folders == len(on_disk)
    if not collected.entries:
        return
    out = tmp_path / "report.md"
    out.write_text(crv.render_report(collected, title="Open review issues", date="2026-10-19"))
    crv.check_report(out, collected)
    report = brp.parse_report(out)
    assert [row["name"] for row in report["rows"]] == [e.name for e in collected.entries]
    for e in collected.entries:
        assert report["rows"][[r["name"] for r in report["rows"]].index(e.name)]["outcome"] == e.cell
        assert all(not it["resolved"] for it in report["records"][e.name]["items"])


def test_fixture_report_builds_the_page(brp, tmp_path):
    """The fixture report gives the expected records, items, fields and ids, and the page embeds the data."""
    if not (ROOT / "airfoil_self_noise" / "dataset.py").is_file() or not _in_git():
        pytest.skip("needs the working copy's airfoil_self_noise and a git checkout")
    assert brp.main([str(FIXTURE), "--out", str(tmp_path), "--root", str(ROOT), "--title", "Fixture Review"]) == 0
    data = json.loads((tmp_path / "data.json").read_text())
    page = (tmp_path / "review_page.html").read_text()

    assert [d["name"] for d in data["datasets"]] == ["airfoil_self_noise", "churn_telco_south_asia_duplicate"]
    added, other = data["datasets"]
    assert (added["cat"], added["folder"], added["retired"]) == ("added", "airfoil_self_noise", False)
    assert added["code"] == (ROOT / "airfoil_self_noise" / "dataset.py").read_text()
    assert added["readme"] is not None
    assert [b["key"] for b in added["blocks"]] == ["outcome", "judgment"]
    assert [(it["n"], it["resolved"]) for it in added["items"]] == [(1, False)]
    assert "Keep the target in decibels?" in added["items"][0]["titleHtml"]
    assert added["fields"] == [{"key": "year", "field": "year", "record": "2014", "definition": "1989"}]

    # The use case comes from the definition's task_summary.
    expected = brp.load_definition(ROOT / "airfoil_self_noise" / "dataset.py").task_summary.fields()
    assert added["summary"]["source"] == "definition"
    assert added["summary"]["question"] == expected["question"]
    assert added["summary"]["fields"]["use_case"] == expected["use_case"]

    # Not added: no folder, no definition. A record that triage has since set to No is shown as "decided".
    record = (RECORDS / "churn_telco_south_asia_duplicate.md").read_text().split("---")[1]
    suggestion = str(yaml.safe_load(record).get("suggestion") or "")
    assert other["cat"] == ("decided" if suggestion.startswith("No") else "notadded")
    assert (other["folder"], other["code"], other["summary"]) == (None, None, None)
    assert [(it["n"], it["resolved"]) for it in other["items"]] == [(1, False)]

    assert [[it["id"] for it in s["items"]] for s in data["crosscut"]] == [["x0-0"]]
    assert data["crosscut"][0]["items"][0]["resolved"] is False
    assert data["title"] == "Fixture Review"
    assert data["generated"] == "2026-10-01"
    assert "2 curation records" in data["subtitle"]

    assert "<title>Fixture Review</title>" in page
    assert re.search(r"__(TITLE|SUBTITLE|DATA)__", page) is None
    embedded = page.split('<script type="application/json" id="data">', 1)[1].split("</script>", 1)[0]
    assert json.loads(embedded) == data


@pytest.mark.parametrize(
    ("old", "new", "line_of", "message"),
    [
        (
            CHURN_SECTION,
            "",
            "| [`churn_telco_south_asia_duplicate`]",
            "no `### churn_telco_south_asia_duplicate` section",
        ),
        ("year `2014`, definition `1989`.", "year 2014.", "- `airfoil_self_noise`", "field not understood"),
        ("### Framework (`src/data_foundry/v2/`)\n", "### Framework\nSome intro.\n", "Some intro.", "before the first"),
        ("   alternative.\n", "   alternative.\n1. **Again.** Twice.\n", "### airfoil_self_noise", "appear twice"),
    ],
)
def test_report_format_errors_name_the_line(brp, tmp_path, old, new, line_of, message):
    """A report that breaks the format stops the parser with the line and the section."""
    text = FIXTURE.read_text()
    assert old in text
    broken = text.replace(old, new, 1)
    path = tmp_path / "report.md"
    path.write_text(broken)
    line = next(i for i, ln in enumerate(broken.splitlines(), 1) if ln.startswith(line_of))
    with pytest.raises(brp.ReportFormatError, match=re.escape(message)) as error:
        brp.parse_report(path)
    assert f"line {line} " in str(error.value)


def test_shared_notes_follow_the_records_line(brp, tmp_path):
    """A shared section covers the records its `Records:` line names, and the line is not shown."""
    text = (
        FIXTURE.read_text()
        + "\n### Notes on both\nRecords: `airfoil_self_noise`, `churn_telco_south_asia_duplicate`\n\nShared.\n"
    )
    path = tmp_path / "report.md"
    path.write_text(text)
    shared = brp.parse_report(path)["shared"]
    assert sorted(shared) == ["airfoil_self_noise", "churn_telco_south_asia_duplicate"]
    assert shared["airfoil_self_noise"] == [{"title": "Notes on both", "md": "\nShared."}]


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_a_definition_removed_on_a_squash_merged_branch_is_found(brp, tmp_path):
    """A folder added and removed on a side branch (squash-merged into main) is not in HEAD's history."""

    def git(*args):
        brp._git(tmp_path, *args)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "Test")
    (tmp_path / "keep.txt").write_text("main\n")
    git("add", "keep.txt")
    git("commit", "-q", "-m", "start")
    git("checkout", "-q", "-b", "side")
    (tmp_path / "gone").mkdir()
    (tmp_path / "gone" / "dataset.py").write_text("code\n")
    git("add", "gone/dataset.py")
    git("commit", "-q", "-m", "add")
    git("rm", "-q", "gone/dataset.py")
    git("commit", "-q", "-m", "remove")
    git("checkout", "-q", "main")

    commit, removed_on = brp._last_commit_with(tmp_path, "gone/dataset.py")
    assert brp._show(tmp_path, commit, "gone/dataset.py") == "code\n"
    assert removed_on is not None
    assert brp._last_commit_with(tmp_path, "never/dataset.py") is None
