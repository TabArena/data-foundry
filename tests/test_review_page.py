"""The review page builder of the review-added-datasets skill: the report parser, the page data and the page."""

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
SCRIPT = REPO / ".claude" / "skills" / "review-added-datasets" / "scripts" / "build_review_page.py"
ROOT = REPO / "datasets" / "_dev" / "tabarena-v0pt2"
FIXTURE = Path(__file__).parent / "fixtures" / "review_page_report.md"
ISSUES = ROOT / "NEW_DATASETS_ISSUES.md"


@pytest.fixture(scope="module")
def brp():
    """The builder script, imported as a module."""
    if not SCRIPT.is_file():
        pytest.skip(f"{SCRIPT} is missing")
    spec = importlib.util.spec_from_file_location("build_review_page", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up there
    spec.loader.exec_module(module)
    return module


def _in_git() -> bool:
    return shutil.which("git") is not None and (REPO / ".git").exists()


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
    record = (REPO / "curation" / "records" / "churn_telco_south_asia_duplicate.md").read_text().split("---")[1]
    suggestion = str(yaml.safe_load(record).get("suggestion") or "")
    assert other["cat"] == ("decided" if suggestion.startswith("No") else "notadded")
    assert (other["folder"], other["code"], other["summary"], other["items"]) == (None, None, None, [])

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
            "### churn_telco_south_asia_duplicate\n",
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


def test_new_datasets_issues_parses(brp):
    """The working copy's run report follows the format."""
    if not ISSUES.is_file():
        pytest.skip(f"{ISSUES} is absent")
    report = brp.parse_report(ISSUES)
    names = [row["name"] for row in report["rows"]]
    assert names
    assert len(names) == len(set(names)) == len(report["records"])
    ids = [it["id"] for s in report["crosscut"] for it in s["items"]]
    assert len(ids) == len(set(ids))
    assert set(report["fields"]) <= set(names)


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
