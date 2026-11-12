"""The review page of the review-added-datasets skill: the collector of the reviews, the report parser, the page.

The scripts live in the skill, not in the package, so they are imported from their files. A missing script fails
the module: the reviews in the records (``## Review``) and the working copy's cross-dataset file are checked here.
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
from data_foundry.curation.record import CurationRecord
from data_foundry.curation.store import load_record, save_record
from data_foundry.v2.splits import Temporal, TemporalSplits

pytest.importorskip("markdown_it", reason="the review page needs markdown-it-py (the `curation` extra)")

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / ".claude" / "skills" / "review-added-datasets" / "scripts"
SCRIPT = SCRIPTS / "build_review_page.py"
COLLECTOR = SCRIPTS / "collect_reviews.py"
TEMPLATE = SCRIPTS.parent / "assets" / "review_page.html"
ROOT = REPO / "datasets" / "_dev" / "tabarena-v0pt2"
RECORDS = REPO / "curation" / "records"
FIXTURE = Path(__file__).parent / "fixtures" / "review_page_report.md"
REVIEW_FILES = Path(__file__).parent / "fixtures" / "review_files"
"""The example of references/review_file_format.md (two records with a review, the cross-dataset file): collected, it
gives FIXTURE."""
CHURN_SECTION = (
    "### churn_telco_south_asia_duplicate\n"
    + FIXTURE.read_text().split("### churn_telco_south_asia_duplicate\n", 1)[-1]
)
"""The fixture report's last record section, to the end of the report."""
AIRFOIL = "records/airfoil_self_noise.md"
"""The example record of an added dataset, with its review."""
PANEL_BLOCK = "**Review panel:**" + load_record(REVIEW_FILES / AIRFOIL).review.split("**Review panel:**", 1)[1]
"""The review panel block of the example review, as written."""


def _add_comment(record: Path, line: str) -> None:
    """Append a line to a record's ``## Comments`` through the store API (the review follows the comments)."""
    rec = load_record(record)
    rec.comments = f"{rec.comments}\n\n{line}" if rec.comments else line
    save_record(rec, record.parent)


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


def test_collector_takes_a_review_file_with_no_issue_when_a_panel_ran(crv, brp, tmp_path):
    """A review can find nothing for the curator: a review with a panel and no issue collects and builds (0 issues),
    one without a panel, an issue or a field row stops the collector.
    """
    file = AIRFOIL
    text = (REVIEW_FILES / file).read_text()
    fields = text[text.index("**Record fields that disagree") : text.index("**Record judgment:**")]
    issues = text[text.index("**Issues for the curator:**") : text.index("**Review panel:**")]
    no_issue = text.replace(fields, "").replace(issues, "")
    root, records, _ = _broken_copy(tmp_path / "a", file, text, no_issue)
    by_name = {e.name: e for e in crv.collect(root, records).entries}
    assert (by_name["airfoil_self_noise"].numbers, by_name["airfoil_self_noise"].fields) == ([], [])
    out = tmp_path / "report.md"
    # A new dataset's round marks its metric, so the record stays for its verdict; without that it is settled.
    assert _collect_fixture(crv, root, records, out, "--metric-marks", "airfoil_self_noise") == 0
    assert brp.parse_report(out)["records"]["airfoil_self_noise"]["items"] == []
    assert _collect_fixture(crv, root, records, out) == 0
    assert "airfoil_self_noise" not in brp.parse_report(out)["records"]

    no_panel = no_issue[: no_issue.index("**Review panel:**")]
    root, records, _ = _broken_copy(tmp_path / "b", file, text, no_panel)
    with pytest.raises(crv.ReviewFileError, match="no issue, no record field and no review panel"):
        crv.collect(root, records)


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
    # The review panel is carried into the report as written, after the issues.
    assert by_name["airfoil_self_noise"].panel == PANEL_BLOCK
    assert by_name["airfoil_self_noise"].panel_sections == ["Claim audit", "Mediator"]
    assert "Review panel" not in by_name["airfoil_self_noise"].issues
    report = out.read_text()
    assert PANEL_BLOCK + "\n\n### churn_telco_south_asia_duplicate" in report
    assert report.index("**Issues for the curator:**") < report.index("**Review panel:**")
    # The record's block ends before the later CC comment.
    other = by_name["churn_telco_south_asia_duplicate"]
    assert (other.folder, other.cell, other.numbers) == (None, "not added; duplicate", [1])
    assert "CC (" not in other.issues
    assert collected.across_items == 1


def test_collector_names_filter(crv, tmp_path):
    """--names keeps only the named records and stops on a name without a review."""
    out = tmp_path / "report.md"
    root, records = REVIEW_FILES / "working_copy", REVIEW_FILES / "records"
    assert _collect_fixture(crv, root, records, out, "--names", "airfoil_self_noise") == 0
    assert "### churn_telco_south_asia_duplicate" not in out.read_text()
    assert _collect_fixture(crv, root, records, out, "--names", "no_such_record") == 1


def test_collector_leaves_out_a_settled_record(crv, brp, tmp_path):
    """A record with every issue resolved and no field row leaves the page by default (it ships by default; Lennart,
    2026-11-08); --keep-settled keeps it, and so does an issue whose last closing turn is Deferred. Its metric keeps it
    only when the round marks it (--metric-marks) and the record has no CC line that it is checked (Lennart,
    2026-11-10).
    """
    file = AIRFOIL
    text = (REVIEW_FILES / file).read_text()
    fields = text[text.index("**Record fields that disagree") : text.index("**Record judgment:**")]
    panel = text.index("**Review panel:**")
    closing = "   **Deferred (2026-11-05):** parked.\n\n   **Resolved (2026-11-08, Lennart):** kept.\n\n"
    settled = text[:panel].rstrip("\n") + "\n\n" + closing + text[panel:]
    root, records, _ = _broken_copy(tmp_path, file, text, settled.replace(fields, ""))
    out = tmp_path / "report.md"

    assert _collect_fixture(crv, root, records, out) == 0
    assert "### airfoil_self_noise" not in out.read_text()  # the round does not ask about the metric
    for marks in ("airfoil_self_noise", "all"):
        assert _collect_fixture(crv, root, records, out, "--metric-marks", marks) == 0
        report = out.read_text()
        assert "### airfoil_self_noise" in report  # the round marks the metric, which is not checked yet
        assert "**Metric marks:** " + ("all." if marks == "all" else "`airfoil_self_noise`.") in report
    assert _collect_fixture(crv, root, records, out, "--metric-marks", "no_such_record") == 1

    record = records / "airfoil_self_noise.md"
    _add_comment(record, "CC (2026-11-08, Lennart): the declared metric (`rmse`) is checked, as declared.")
    assert _collect_fixture(crv, root, records, out, "--metric-marks", "airfoil_self_noise") == 0
    report = out.read_text()
    assert "### airfoil_self_noise" not in report
    assert "**Settled, left out (they ship by default):** `airfoil_self_noise`." in report
    assert "### churn_telco_south_asia_duplicate" in report

    assert _collect_fixture(crv, root, records, out, "--keep-settled") == 0
    assert "### airfoil_self_noise" in out.read_text()

    # Only settled records named: the report keeps the items across datasets alone, and the builder reads it.
    assert _collect_fixture(crv, root, records, out, "--names", "airfoil_self_noise") == 0
    report = out.read_text()
    assert "## Across datasets" in report
    assert "## Per dataset" not in report
    assert "### airfoil_self_noise" not in report
    parsed = brp.parse_report(out)
    assert (parsed["rows"], len(parsed["crosscut"])) == ([], 1)

    # Deferred last: the record is parked, not settled.
    record.write_text(record.read_text().replace(closing, "   **Deferred (2026-11-08):** parked.\n\n"))
    assert _collect_fixture(crv, root, records, out) == 0
    assert "### airfoil_self_noise" in out.read_text()


def test_a_retired_record_keeps_its_review(crv, tmp_path):
    """A dataset retired from the working copy (its folder gone, ``v2_path`` cleared) keeps its review in its record:
    the collector reads it without a folder, from the outcome's ``added``.
    """
    shutil.copytree(REVIEW_FILES, tmp_path / "files")
    root, records = tmp_path / "files" / "working_copy", tmp_path / "files" / "records"
    rec = load_record(records / "airfoil_self_noise.md")
    rec.v2_path = None
    save_record(rec, records)
    collected = crv.collect(root, records, ["airfoil_self_noise"])
    assert [(e.name, e.folder, e.numbers) for e in collected.entries] == [
        ("airfoil_self_noise", "airfoil_self_noise", [1])
    ]


def test_collector_refuses_a_review_file_in_a_folder_and_an_open_issues_block(crv, tmp_path):
    """The review lives in the record: a REVIEW.md in a dataset folder, or an open-issues block left in a record's
    comments, stops the collector and names the move script.
    """
    shutil.copytree(REVIEW_FILES, tmp_path / "files")
    root, records = tmp_path / "files" / "working_copy", tmp_path / "files" / "records"
    (root / "airfoil_self_noise").mkdir(exist_ok=True)
    (root / "airfoil_self_noise" / "REVIEW.md").write_text("# airfoil_self_noise\n\n**Outcome:** added.\n")
    with pytest.raises(crv.ReviewFileError, match=re.escape("move_reviews_to_records.py")):
        crv.collect(root, records)
    (root / "airfoil_self_noise" / "REVIEW.md").unlink()
    _add_comment(records / "airfoil_self_noise.md", "**Open issues (AI, 2026-11-11):** not added.\n\n1. **Q?** x.")
    with pytest.raises(crv.ReviewFileError, match="open-issues block in the comments"):
        crv.collect(root, records)


def _broken_copy(tmp_path: Path, file: str, old: str, new: str) -> tuple[Path, Path, Path]:
    """A copy of the example review files (records and cross-dataset file) with one change, and the changed file."""
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
            AIRFOIL,
            "     scale a practitioner models it on.\n",
            "     scale a practitioner models it on.\n**Split:** x\n",
            48,
            "label",
        ),
        (
            AIRFOIL,
            "     scale a practitioner models it on.\n",
            "     scale a practitioner models it on.\n1. **Again.**\n",
            48,
            "twice",
        ),
        (AIRFOIL, "**Outcome:** added.", "**Outcome:** added as `x`.", 16, "names"),
        (AIRFOIL, "year`: record", "year`: rec", 22, "field row"),
        (AIRFOIL, "**Main points:**", "**Points:**", None, "Main points"),
        (
            AIRFOIL,
            "## Review\n\n",
            "## Review\n\nIntro.\n",
            16,
            "text before",
        ),
        ("records/churn_telco_south_asia_duplicate.md", "not added; duplicate", "duplicate", 16, "`not added`"),
        ("working_copy/REVIEW.md", "# Across datasets\n", "# Across datasets\nIntro.\n", 2, "only `### <section>`"),
        # The review panel: one per file, the last block, every <details> closed.
        (
            AIRFOIL,
            "issue 1.\n\n</details>\n",
            "issue 1.\n\n</details>\n\n**Review panel:** ship.\n",
            67,
            "a second `**Review panel:**` block",
        ),
        (
            AIRFOIL,
            "issue 1.\n\n</details>\n",
            "issue 1.\n\n</details>\n\n**Issues for the curator:**\n",
            67,
            "after `**Review panel:**`",
        ),
        (
            AIRFOIL,
            "| holds | |\n\n</details>\n",
            "| holds | |\n\n",
            52,
            "is not closed",
        ),
        (AIRFOIL, "issue 1.\n\n</details>\n", "issue 1.\n", 61, "not closed"),
        (
            AIRFOIL,
            "</details>\n\n<details><summary>Mediator",
            "</details>\n\nStray.\n\n<details><summary>Mediator",
            61,
            "text outside a section",
        ),
        (
            AIRFOIL,
            "**Review panel:** ship (mediator).",
            "**Review panel:**\n\nship (mediator).",
            49,
            "no summary",
        ),
    ],
)
def test_collector_errors_name_the_file_and_line(crv, tmp_path, file, old, new, line, message):
    """A review that breaks the format stops the collector with the record (or the cross-dataset file) and the line."""
    root, records, path = _broken_copy(tmp_path, file, old, new)
    with pytest.raises(crv.ReviewFileError, match=re.escape(message)) as error:
        crv.collect(root, records)
    assert str(error.value).startswith(f"{path}, line {line}:" if line else f"{path}:")


def test_collector_keeps_fenced_code_in_the_panel(crv, tmp_path):
    """Inside a fence, a panel's lines are text: a `#` comment or a `</details>` neither breaks nor closes it."""
    fenced = "```python\n# the check\nprint('</details>')\n```\n\nShip."
    root, records, _ = _broken_copy(tmp_path, AIRFOIL, "Ship. The advocate", fenced)
    entry = next(e for e in crv.collect(root, records).entries if e.name == "airfoil_self_noise")
    assert entry.panel_sections == ["Claim audit", "Mediator"]
    assert "# the check" in entry.panel


def test_working_copy_review_files_collect_and_parse(crv, brp, tmp_path):
    """The committed reviews (the records' ``## Review``) follow the format, no dataset folder holds a review file, and
    every issue reaches the page.
    """
    assert crv.folder_review_files(ROOT) == []
    collected = crv.collect(ROOT, RECORDS)
    with_review = [
        p.stem for p in sorted(RECORDS.glob("*.md")) if not p.name.startswith("_") and "\n## Review\n" in p.read_text()
    ]
    assert [e.name for e in collected.entries] == with_review
    if not collected.entries:
        return
    out = tmp_path / "report.md"
    out.write_text(crv.render_report(collected, title="Open review issues", date="2026-10-19"))
    crv.check_report(out, collected)
    report = brp.parse_report(out)
    assert [row["name"] for row in report["rows"]] == [e.name for e in collected.entries]
    for e in collected.entries:
        assert report["rows"][[r["name"] for r in report["rows"]].index(e.name)]["outcome"] == e.cell
        assert [it["n"] for it in report["records"][e.name]["items"]] == e.numbers


def test_fixture_report_builds_the_page(brp, tmp_path):
    """The fixture report gives the expected records, items, fields and ids, and the page embeds the data."""
    if not (ROOT / "airfoil_self_noise" / "dataset.py").is_file() or not _in_git():
        pytest.skip("needs the working copy's airfoil_self_noise and a git checkout")
    assert brp.main([str(FIXTURE), "--out", str(tmp_path), "--root", str(ROOT), "--title", "Fixture Review"]) == 0
    data = json.loads((tmp_path / "data.json").read_text())
    page = (tmp_path / "review_page.html").read_text()

    # The page's order is review_order (priority, then the fewest open marks), not the report's.
    assert sorted(d["name"] for d in data["datasets"]) == ["airfoil_self_noise", "churn_telco_south_asia_duplicate"]
    assert data["datasets"] == sorted(data["datasets"], key=brp.review_order)
    by_name = {d["name"]: d for d in data["datasets"]}
    added, other = by_name["airfoil_self_noise"], by_name["churn_telco_south_asia_duplicate"]
    assert (added["openMarks"], other["openMarks"]) == (2, 1)
    assert (added["cat"], added["folder"], added["retired"]) == ("added", "airfoil_self_noise", False)
    assert added["code"] == (ROOT / "airfoil_self_noise" / "dataset.py").read_text()
    assert added["readme"] is not None
    assert [b["key"] for b in added["blocks"]] == ["outcome", "judgment"]
    assert [(it["n"], it["resolved"]) for it in added["items"]] == [(1, False)]
    assert "Keep the target in decibels?" in added["items"][0]["titleHtml"]
    assert added["fields"] == [{"key": "year", "field": "year", "record": "2014", "definition": "1989"}]
    assert added["panel"]["recommendation"] == "ship (mediator)"
    assert [s["title"] for s in added["panel"]["sections"]] == ["Claim audit", "Mediator"]
    assert other["panel"] is None

    # The use case comes from the definition's task_summary.
    expected = brp.load_definition(ROOT / "airfoil_self_noise" / "dataset.py").task_summary.fields()
    assert added["summary"]["source"] == "definition"
    assert added["summary"]["question"] == expected["question"]
    assert added["summary"]["fields"]["use_case"] == expected["use_case"]

    # The metric comes from the definition's declared Metric, resolved for its problem type.
    cls = brp.load_definition(ROOT / "airfoil_self_noise" / "dataset.py")
    if isinstance(getattr(cls, "metric", None), brp.Metric):
        spec = cls.metric.spec(cls.problem_type)
        assert added["metric"]["source"] == "definition"
        assert (added["metric"]["name"], added["metric"]["origin"]) == (spec["name"], spec["origin"])
        assert added["metric"]["reason"] == spec["reason"]

    # Not added: no folder, no definition. A record that triage has since set to No is shown as "decided".
    record = (RECORDS / "churn_telco_south_asia_duplicate.md").read_text().split("---")[1]
    suggestion = str(yaml.safe_load(record).get("suggestion") or "")
    assert other["cat"] == ("decided" if suggestion.startswith("No") else "notadded")
    assert (other["folder"], other["code"], other["summary"], other["metric"]) == (None, None, None, None)
    assert [(it["n"], it["resolved"]) for it in other["items"]] == [(1, False)]

    assert [[it["id"] for it in s["items"]] for s in data["crosscut"]] == [["x0-0"]]
    assert data["crosscut"][0]["items"][0]["resolved"] is False
    assert data["title"] == "Fixture Review"
    assert data["generated"] == "2026-10-01"
    assert "2 curation records" in data["subtitle"]

    assert "<title>Fixture Review</title>" in page
    assert 'ctab("panel", "Panel")' in page
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
        (
            "     scale a practitioner models it on.\n",
            "     scale a practitioner models it on.\n1. **Again.** Twice.\n",
            "### airfoil_self_noise",
            "appear twice",
        ),
        ("issue 1.\n\n</details>\n", "issue 1.\n", "<details><summary>Mediator", "not closed"),
        ("<details><summary>Claim audit", "<details open><summary>Claim audit", "<details open>", "on one line"),
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


def test_report_panel_becomes_page_data(brp, tmp_path):
    """The builder reads the panel into summary, recommendation and sections; a record without one has none."""
    text = FIXTURE.read_text().replace("Ship. The advocate", "**Split:** agreed.\n\nShip. The advocate", 1)
    path = tmp_path / "report.md"
    path.write_text(text)
    records = brp.parse_report(path)["records"]
    airfoil, churn = records["airfoil_self_noise"], records["churn_telco_south_asia_duplicate"]
    assert churn["panel"] is None
    assert brp._panel(churn["panel"]) is None
    # The panel is the last block: a label-like line inside it stays in it, and the issues end before it.
    assert list(airfoil["blocks"]) == ["outcome", "judgment"]
    assert [it["n"] for it in airfoil["items"]] == [1]
    assert "Review panel" not in airfoil["items"][0]["body_md"]

    panel = brp._panel(airfoil["panel"])
    assert sorted(panel) == ["recommendation", "sections", "summary"]
    assert panel["recommendation"] == "ship (mediator)"
    assert panel["summary"].startswith("<p>ship (mediator). Claim audit: 2 claims, 2 hold.")
    claims, mediator = panel["sections"]
    assert claims["title"] == "Claim audit"
    assert "<table>" in claims["html"]
    assert "<details" not in claims["html"]
    assert mediator["title"] == "Mediator"
    assert "<strong>Split:</strong> agreed." in mediator["html"]


def test_review_order(brp):
    """Priority 5 first, records without one last; within one priority the fewest open marks, then the name."""
    rows = [
        {"name": "b", "priority": 3, "openMarks": 4},
        {"name": "none", "priority": None, "openMarks": 0},
        {"name": "a", "priority": 3, "openMarks": 4},
        {"name": "quick", "priority": 3, "openMarks": 1},
        {"name": "top", "priority": 5, "openMarks": 9},
    ]
    assert [r["name"] for r in sorted(rows, key=brp.review_order)] == ["top", "quick", "a", "b", "none"]


def test_template_has_the_panel_tab_and_keeps_the_store():
    """The Panel tab follows Decisions; the store's collections and the mark fields are unchanged."""
    page = TEMPLATE.read_text()
    assert 'const CTABS = ["usecase", "decisions", "panel", "details", "code", "report", "record"];' in page
    assert 'data-act="openpanel"' in page
    # The rail groups the records by priority, in the order the builder sorted them.
    assert '<li class="grp" aria-hidden="true">' in page
    # Ship verdicts with nothing open leave their priority group for the "To ship" group at the end.
    assert 'const groupLabel = (g) => (g === "ship" ? "To ship" : prioLabel(g));' in page
    assert '["reviews", "crosscut"].forEach((coll) => {' in page
    assert "const S = { reviews: {}, crosscut: {} };" in page
    # The Use case tab shows the declared split and the declared metric under the task summary, each with a mark; the
    # metric only when the round marks it.
    assert 'panel("usecase", useCaseHtml(d) + splitHtml(d) + metricHtml(d))' in page
    assert 'if (!d.metricMark) return "";' in page
    assert "const hasMetricMark = (d) => !!d.metricMark && " in page
    assert 'data-note="split"' in page
    assert "if (out.split && !out.split.d" in page


def test_split_from_the_readme_and_the_definition(brp):
    """The split comes from the README's front matter and Splits section, the Forced tags and the split notes."""
    readme = """---
task:
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: Date
  group_on: null
  grouping: null
splits:
  n_repeats: 3
  n_folds: 1
  random_state: 4267
  time_horizon: 42
  time_horizon_unit: days
  time_gap: 1
  time_gap_unit: days
  n_train: {min: 10, max: 20}
  n_test: {min: 5, max: 6}
---

## Splits

Six weeks ahead, as the competition asks.

3 repeat(s) x 1 fold(s) with seed 4267; train 10 to 20 rows, test 5 to 6 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 20 | 6 |

## Bundle checks
"""
    comments = """
        - We drop the customers column.
        - The split follows the competition's
          temporal test window.
    """
    got = brp._split(readme, ["Tabular", "ForcedIIDFromTemporal"], comments)
    assert (got["regime"], got["time_on"], got["time_horizon"], got["n_folds"]) == ("temporal", "Date", 42, 1)
    assert got["forced"] == ["ForcedIIDFromTemporal"]
    assert "Six weeks ahead" in got["noteHtml"]
    assert "repeat(s)" not in got["noteHtml"]
    assert got["tableHtml"].count("<tr>") == 2
    assert got["notes"] == ["The split follows the competition's temporal test window."]

    default = readme.replace("Six weeks ahead, as the competition asks.", "Default splits.")
    assert brp._split(default, [], None)["noteHtml"] == ""
    assert brp._split("no front matter", [], None) is None

    code = 'class X:\n    data_tags = ("ForcedIIDFromTemporal",)\n    curation_comments = "- a split note"\n'
    assert brp._literal_from_source(code, "data_tags") == ("ForcedIIDFromTemporal",)
    assert brp._literal_from_source(code, "curation_comments") == "- a split note"
    assert brp._literal_from_source(code, "metric") is None


def test_metric_marks_come_from_the_report_header(brp):
    """The header's metric-marks line names the records whose metric the page shows and marks; none without it."""
    lines = ["Open review issues ...", "", "**Metric marks:** `a`, `b_c`.", "", "## Summary per record"]
    assert brp._metric_marks(lines) == {"a", "b_c"}
    assert brp._metric_marks(["**Metric marks:** all."]) is None
    assert brp._metric_marks(["Open review issues ...", "## Summary", "**Metric marks:** `a`."]) == set()


def test_metric_from_the_definition_and_the_readme(brp):
    """The metric spec comes from the definition's Metric (all fields) or, failing that, the README frontmatter."""

    class Definition:
        problem_type = "binary_classification"
        metric = brp.Metric.fallback(reason="the paper reports accuracy, precision and recall side by side")
        scoring_columns = ()

    got = brp._metric_from_class(Definition)
    assert (got["name"], got["origin"], got["source"]) == ("roc_auc", "fallback", "definition")
    assert got["reason"].startswith("the paper reports")
    assert got["scoring_columns"] == []

    Definition.metric = "roc_auc"  # not a Metric: nothing from the class
    assert brp._metric_from_class(Definition) is None

    front = brp._metric_from_front({"metric": "mae", "metric_origin": "source", "scoring_columns": ["era"]})
    assert (front["name"], front["origin"], front["source"]) == ("mae", "source", "readme")
    assert front["scoring_columns"] == [{"column": "era"}]
    assert brp._metric_from_front({}) is None


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


def test_thread_splits_the_original_from_the_turns(brp):
    """An item's text splits into the original and one turn per label."""
    text = (
        "The item proposes a change.\n"
        "**Lennart (2026-10-21, discuss):** Why?\n"
        "**Answer (AI, 2026-10-21):** Because the rule says so.\n"
        "Second line of the answer.\n"
        "**Resolved (2026-10-22, Lennart):** done."
    )
    out = brp._thread(text)
    assert "proposes a change" in out["html"]
    assert "Why?" not in out["html"]
    who = [(t["who"], t["kind"], t["date"]) for t in out["thread"]]
    assert who == [
        ("curator", "note", "2026-10-21"),
        ("ai", "answer", "2026-10-21"),
        ("closed", "resolved", "2026-10-22"),
    ]
    assert out["thread"][0]["mark"] == "discuss"
    assert out["thread"][0]["by"] == "Lennart"
    assert "Second line" in out["thread"][1]["html"]
    assert brp._thread("No turns here.")["thread"] == []


def test_render_hides_footnotes_and_notes_for_the_ai(brp):
    """Footnotes are numbered by first reference and closed in a box; the notes for the AI get a closed box too."""
    text = (
        "* **Problem:** a later reference[^b] and an earlier one[^a].\n\n"
        "**Notes for the AI:** drop `x`[^a].\n\n"
        "[^a]: **LEAK-31** (Should): keep with a note.\n"
        "[^b]: **SPLIT-15** (Should): as many windows\n"
        "  as folds."
    )
    out = brp.render(text)
    assert out.index('data-fn="1"') < out.index("earlier one")  # [^b] is referenced first, so it is 1
    assert '<details class="ainotes"><summary>Notes for the AI</summary>' in out
    assert "drop <code>x</code>" in out
    assert "Rules and references (2)" in out
    assert "as many windows as folds" in out
    assert "[^" not in out
    assert "LEAK-31" not in out.split("<details")[0]
    assert brp.render("No footnote [^z] here.") == "<p>No footnote [^z] here.</p>\n"


def test_collector_warns_about_issues_out_of_shape(crv):
    """An open issue without its bullets or options table, or with a rule ID in its text, is named; a closed one not."""
    entry = crv.Entry(name="x", folder="x", source=Path("x"), outcome="added", points="", cell="added")
    entry.issues = (
        "1. **Old shape?** Per LEAK-10 the column goes.\n\n"
        "2. **Closed?** Per LEAK-10.\n   **Resolved (2026-11-01, Andrej):** done.\n"
    )
    assert crv.shape_warnings(entry) == [
        "x issue 1: no Problem, Options, Recommendation, options table",
        "x issue 1: rule IDs in the text (LEAK-10); move them to footnotes",
    ]
    entry.issues = (
        "1. **No implemented row?**\n\n   * **Problem:** p.\n   * **Options:**\n\n     | | Option |\n     |---|---|\n"
        "     | A | x |\n     | B | y |\n\n   * **Recommendation:** A.\n"
    )
    assert crv.shape_warnings(entry) == [
        "x issue 1: no row marked (implemented), which the page's As implemented locks in"
    ]
    fixture = crv.collect(REVIEW_FILES / "working_copy", REVIEW_FILES / "records")
    assert [w for e in fixture.entries for w in crv.shape_warnings(e)] == []


def test_extra_crosscut_items_keep_their_turns_out_of_the_notes(brp, tmp_path):
    """A notes block in an extra item's original text ends at the first turn, so the curator's note stays visible."""
    path = tmp_path / "extra.yaml"
    path.write_text(
        "- title: S\n  items:\n    - id: x-1\n      title: T\n      md: |\n"
        "        * **Problem:** p.\n\n        **Notes for the AI:** n.\n\n"
        "        **Andrej (2026-11-02, discuss):** Why?\n"
    )
    item = brp._extra_crosscut(path)[0]["items"][0]
    assert "Why?" not in item["html"]
    assert [(t["who"], t["by"]) for t in item["thread"]] == [("curator", "Andrej")]


def test_issue_text_folds_the_details_between_problem_and_options(brp):
    """The problem stays in view, the other bullets go into a closed Details box, the options and the recommendation
    follow it; footnotes are numbered across all three parts.
    """
    text = (
        "* **Problem:** short[^a].\n"
        "* **Experiments:** 0.62 against 0.61[^b].\n"
        "* **Consistency:** like qsar.\n"
        "* **Options:**\n\n  | | Option |\n  |---|---|\n  | A | keep (implemented) |\n\n"
        "* **Recommendation:** A. **Decision:** A?\n\n"
        "[^a]: one.\n[^b]: two."
    )
    out = brp._thread(text)["html"]
    assert out.index("short") < out.index('<details class="idetails">') < out.index("0.62") < out.index("<table")
    assert "<summary>Details: experiments, consistency</summary>" in out
    assert out.index("<table") < out.index("Recommendation")
    assert 'data-fn="2"' in out.split('<details class="fnotes">')[0]
    assert "idetails" not in brp._thread("* **Asked:** x.\n* **Found:** y.")["html"]  # no problem bullet: no fold


def test_options_table_shows_points_as_bullets_and_tags_rows(brp):
    """An options table gets its own class, a cell's points separated by `;` become bullets (not inside code, not in
    the option's name), and the implemented and the recommended rows get a tag each; other tables stay as they are.
    """
    text = (
        "* **Problem:** p.\n"
        "* **Options:**\n\n  | | Option | What it does | Pro | Con |\n  |---|---|---|---|---|\n"
        "  | A | Keep; as is (implemented) | one change | simple; cheap | `a; b` stays |\n"
        "  | B | Drop | two | fair | costly; slow |\n\n"
        "* **Recommendation:** B: because. **Decision:** A or B?"
    )
    out = brp._thread(text)["html"]
    assert '<table class="opttab">' in out
    rows = out.split("<tr")
    impl, rec = rows[2], rows[3]
    assert 'class="impl"' in impl
    assert "otag impl" in impl
    assert "(implemented)" not in impl
    assert '<span class="oname">Keep; as is</span>' in impl
    assert '<td class="c-pro"><ul><li>simple</li><li>cheap</li></ul></td>' in impl
    assert '<td class="c-con"><code>a; b</code> stays</td>' in impl
    assert 'class="rec"' in rec
    assert "otag rec" in rec
    assert "<li>costly</li>" in rec
    assert "opttab" not in brp.render("| a | b |\n|---|---|\n| x; y | z |")
    # Each row carries its letter and a hidden tag the page shows on the row a mark locks in.
    assert 'data-key="A"' in impl
    assert '<span class="otag pick" hidden></span>' in impl


def test_ai_turn_choices_become_answer_buttons(brp):
    """An AI turn's lettered bullets leave its text as choices (continuation lines joined), with the "give the letter"
    sentence; a turn with one lettered line or none keeps its text and has no choices.
    """
    text = (
        "* **Problem:** p.\n**Consistency check (AI, 2026-11-05):** what sets it apart?\n"
        "- (a) the fact,\n  written down;\n- (b) drop it.\n\n"
        "Give the letter in the note; nothing is applied until\nthen.\n"
    )
    turn = brp._thread(text)["thread"][-1]
    assert [c["key"] for c in turn["choices"]] == ["a", "b"]
    assert turn["choices"][0]["html"] == "the fact, written down"
    assert "(a)" not in turn["html"]
    assert "Give the letter" not in turn["html"]
    assert "nothing is applied" not in turn["html"]
    plain = brp._thread("* **Problem:** p.\n**Answer (AI, 2026-11-05):** yes; (a) inline is no choice.\n")["thread"][-1]
    assert plain["choices"] == []
    assert "(a) inline" in plain["html"]


def test_ai_turn_in_issue_shape_renders_like_an_issue(brp):
    """A consistency check in the issue shape (passed as the collector does, the issue's indent removed) keeps its
    options table (rows tagged, the recommended one too), renders its footnotes, and its rows are the answer buttons.
    """
    text = (
        "* **Problem:** p.\n"
        "**Consistency check (AI, 2026-11-05):** what sets it apart?\n\n"
        "* **Problem:**\n  - It differs from a precedent[^cc-x].\n"
        "* **Options:**\n\n  | | Option | What it does | Pro | Con |\n  |---|---|---|---|---|\n"
        "  | a | Record the fact | a Cases row | consistent | none found |\n"
        "  | b | Drop it | the rows leave | like the precedent | rows lost; a cut |\n\n"
        "* **Recommendation:** a, the fact holds. **Decision:** a or b?\n\n"
        "[^cc-x]: **LEAK-10** (Must): the rule.\n"
    )
    turn = brp._thread(text)["thread"][-1]
    assert [c["key"] for c in turn["choices"]] == ["a", "b"]
    assert turn["choices"][0]["html"] == "Record the fact"
    assert '<table class="opttab">' in turn["html"]
    assert 'data-key="a"' in turn["html"]
    assert "otag rec" in turn["html"].split('data-key="b"')[0]
    assert 'class="fnotes"' in turn["html"]
    assert "LEAK-10" not in turn["html"].split('class="fnotes"')[0]


def test_metric_is_resolved_by_the_records_cc_line(brp, tmp_path):
    """The metric counts as resolved once the record says the declared metric is checked (the latest such line)."""
    rec = tmp_path / "x.md"
    rec.write_text(
        "---\nunique_name: x\n---\n\n## Comments\n\nCC (2026-10-21, Lennart): the declared metric documents it.\n"
    )
    assert brp._metric_checked(rec) is None
    rec.write_text(
        rec.read_text() + "\nCC (2026-11-04, Lennart): the declared metric is checked and stays as declared.\n"
        "\nCC (2026-11-05, Lennart): the declared metric (RMSE) is checked and stays as declared.\n"
    )
    assert brp._metric_checked(rec)["date"] == "2026-11-05"
    assert brp._metric_checked(tmp_path / "missing.md") is None


def test_the_split_is_marked_only_when_the_round_asks(crv, brp, tmp_path):
    """The split, like the metric, keeps a settled record on the page only when --split-marks names it, until the
    record's CC line says the declared split is checked; the report's header names the records, and the page's
    split box and mark are gated on them.
    """
    file = AIRFOIL
    text = (REVIEW_FILES / file).read_text()
    fields = text[text.index("**Record fields that disagree") : text.index("**Record judgment:**")]
    issues = text[text.index("**Issues for the curator:**") : text.index("**Review panel:**")]
    root, records, _ = _broken_copy(tmp_path, file, text, text.replace(fields, "").replace(issues, ""))
    out = tmp_path / "report.md"
    assert _collect_fixture(crv, root, records, out) == 0
    assert "### airfoil_self_noise" not in out.read_text()
    assert _collect_fixture(crv, root, records, out, "--split-marks", "airfoil_self_noise") == 0
    assert "**Split marks:** `airfoil_self_noise`." in out.read_text()
    assert brp.parse_report(out)["split_marks"] == {"airfoil_self_noise"}
    assert _collect_fixture(crv, root, records, out, "--split-marks", "no_such_record") == 1

    record = records / "airfoil_self_noise.md"
    assert brp._split_checked(record) is None
    _add_comment(record, "CC (2026-11-12, Lennart): the declared split (iid, 3 x 3 folds) is checked, as declared.")
    assert brp._split_checked(record)["date"] == "2026-11-12"
    assert _collect_fixture(crv, root, records, out, "--split-marks", "airfoil_self_noise") == 0
    assert "### airfoil_self_noise" not in out.read_text()

    page = TEMPLATE.read_text()
    assert "const hasSplitMark = (d) => !!d.splitMark && " in page
    assert "&& !d.splitChecked;" in page
    assert 'if (!d.splitMark) return "";' in page


def test_thread_gives_the_ai_turn_the_curator_replies_to(brp):
    """An issue whose last turn is the AI's carries an `askId` (the page counts it unmarked until a reply names it);
    a new AI turn gets a new id; an issue whose last turn is the curator's or a closing label has none.
    """
    base = "* **Problem:** p.\n"
    asked = brp._thread(base + "**Lennart (2026-11-05, change):** why?\n**Answer (AI, 2026-11-05):** because.\n")
    again = brp._thread(base + "**Answer (AI, 2026-11-05):** because, and more.\n")
    assert asked["askId"]
    assert again["askId"]
    assert asked["askId"] != again["askId"]
    assert brp._thread(base + "**Answer (AI, 2026-11-05):** a.\n**Lennart (2026-11-05, ok):** fine.\n")["askId"] == ""
    assert brp._thread(base + "**Resolved (2026-11-05, Lennart):** done.\n")["askId"] == ""
    assert brp._thread(base)["askId"] == ""


def test_issue_options_name_what_each_mark_locks_in(brp):
    """The page's mark buttons read the options of the first options table (not an experiment table before it): the
    letters and names, the implemented row ("As implemented") and the recommended one.
    """
    text = (
        "* **Problem:** p.\n* **Experiments:**\n\n  | Model | score |\n  |---|---|\n  | x | 1 |\n\n"
        "* **Options:**\n\n  | | Option | What it does | Pro | Con |\n  |---|---|---|---|---|\n"
        "  | A | Keep `x` (implemented) | one | a | b |\n  | B | Drop it | two | c | d |\n\n"
        "* **Recommendation:** B: because. **Decision:** A or B?\n"
        "**Lennart (2026-11-05, change):** see C | in a pipe\n"
    )
    thread = brp._thread(text)
    assert [o["key"] for o in thread["options"]] == ["A", "B"]
    assert thread["options"][0]["nameHtml"] == "Keep <code>x</code>"
    assert (thread["implemented"], thread["recommended"]) == ("A", "B")
    none = brp._thread("* **Problem:** p.\n* **Options:**\n\n  | | Option |\n  |---|---|\n  | A | x |\n  | B | y |\n")
    assert (none["implemented"], [o["key"] for o in none["options"]]) == ("", ["A", "B"])
    assert brp._thread("Plain text.")["options"] == []


def test_collector_warns_about_a_problem_out_of_shape(crv):
    """A problem is at most PROBLEM_BULLETS bullets of one sentence each; its length in words is free, and neither
    the footnote markers nor a full stop inside a number end a sentence.
    """

    def warnings(problem: str) -> list[str]:
        entry = crv.Entry(name="x", folder="x", source=Path("x"), outcome="added", points="", cell="added")
        entry.issues = (
            f"1. **Q?**\n\n   * **Problem:**{problem}\n   * **Options:**\n\n     | | Option |\n     |---|---|\n"
            "     | A | x (implemented) |\n\n   * **Recommendation:** A.\n\n   [^1]: r.\n"
        )
        return crv.shape_warnings(entry)

    long_sentence = " ".join(["word"] * 80) + " scores 0.62.[^1]"
    assert warnings(f" {long_sentence}") == []
    assert warnings("\n     - First, at 0.5.\n     - Second.[^1]\n     - Third?") == []
    assert warnings("\n     - One. Two.\n     - Three.") == [
        "x issue 1: no one sentence per problem bullet (1 with more)"
    ]
    assert warnings("\n" + "".join(f"     - Point {i}.\n" for i in range(4))) == [
        "x issue 1: no short problem (4 bullets, at most 3)"
    ]


def _iid_split(brp, tags, comments):
    readme = "---\ntask:\n  split_regime: iid\nsplits:\n  n_repeats: 3\n  n_folds: 3\n---\n"
    return brp._split(readme, tags, comments)


def _record(tmp_path, *tags):
    record = tmp_path / "r.md"
    record.write_text("---\ntags:\n" + "".join(f"- '{t}'\n" for t in tags) + "---\n")
    return record


def test_the_split_box_shows_the_basis_and_the_records_facts(brp, tmp_path):
    """The time basis, its `Time basis:` line and the record's collection facts reach the split box, as information."""
    split = _iid_split(brp, ["IID", "DelayedTarget"], "- Time basis: all clients scored in September 2005.\n- x")
    brp._time_facts(split, _record(tmp_path, "Samples: One Moment", "Target: Later", "Entities: Recur", "Tiny Data"))
    assert split["time"]["basis"] == "DelayedTarget"
    assert "September 2005" in split["time"]["lineHtml"]
    assert split["time"]["facts"] == ["Samples: One Moment", "Target: Later", "Entities: Recur"]


def test_a_forced_tag_is_shown_as_the_time_basis(brp, tmp_path):
    """A forced tag is the time basis the split box shows."""
    split = _iid_split(brp, ["IID", "ForcedIIDFromTemporal"], None)
    brp._time_facts(split, _record(tmp_path, "Samples: Over Time", "Time: Lost"))
    assert split["time"]["basis"] == "ForcedIIDFromTemporal"
    assert split["time"]["facts"] == ["Samples: Over Time", "Time: Lost"]


def test_the_horizon_block_and_its_sign_off(crv, brp, tmp_path):
    """A review's Horizon block is carried to the page; with --horizon-marks the record waits for the CC line that
    the declared horizon is checked (Lennart, 2026-11-10: new temporal datasets get the sign-off, like the metric).
    """
    file = AIRFOIL
    text = (REVIEW_FILES / file).read_text()
    horizon = "**Horizon:** a week, the refit cadence the source names.\n\n- **Gap:** one day, the label delay.\n\n"
    with_horizon = text.replace("**Issues for the curator:**", horizon + "**Issues for the curator:**")
    fields = text[text.index("**Record fields that disagree") : text.index("**Record judgment:**")]
    issues = with_horizon[with_horizon.index("**Issues for the curator:**") : with_horizon.index("**Review panel:**")]
    only_horizon = with_horizon.replace(fields, "").replace(issues, "")
    root, records, _ = _broken_copy(tmp_path, file, text, only_horizon)
    entry = {e.name: e for e in crv.collect(root, records).entries}["airfoil_self_noise"]
    assert entry.horizon.startswith("a week, the refit cadence")
    out = tmp_path / "report.md"
    assert _collect_fixture(crv, root, records, out) == 0
    assert "### airfoil_self_noise" not in out.read_text()  # nothing marked: settled
    assert _collect_fixture(crv, root, records, out, "--horizon-marks", "airfoil_self_noise") == 0
    report = out.read_text()
    assert "**Horizon marks:** `airfoil_self_noise`." in report
    assert "**Horizon:** a week, the refit cadence" in report
    parsed = brp.parse_report(out)
    assert parsed["horizon_marks"] == {"airfoil_self_noise"}
    assert "a week" in parsed["records"]["airfoil_self_noise"]["blocks"]["horizon"]
    record = records / "airfoil_self_noise.md"
    _add_comment(record, "CC (2026-11-10, Lennart): the declared horizon (7-day windows) is checked.")
    assert brp._horizon_checked(record)["by"] == "Lennart"
    assert _collect_fixture(crv, root, records, out, "--horizon-marks", "airfoil_self_noise") == 0
    assert "### airfoil_self_noise" not in out.read_text()


def test_temporal_from_the_definition(brp):
    """The declared windows the horizon box shows come from the definition's Temporal."""

    class Definition:
        temporal = Temporal(on="t", splits=TemporalSplits(window=7, unit="days", n_windows=3, gap=1))
        splits_comment = """
            A model refit every week.
        """

    got = brp._temporal_from_class(Definition)
    assert (got["on"], got["window"], got["unit"], got["n_windows"], got["gap"]) == ("t", 7, "days", 3, 1)
    assert got["comment"] == "A model refit every week."
    assert "cutoffs" not in got
    Definition.temporal = None
    assert brp._temporal_from_class(Definition) is None


HORIZON_BLOCK = """\
* **Verdict:** keep the 7-day windows (medium confidence): TabReD's own test length.
* **Length:** no source states a refit cadence.
* **Gap:** none needed.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | 7 days (implemented) | today's windows | 3 of 1.19M-1.49M rows | TabReD's length | no cadence stated |
  | B | 1 day | 41 candidates | 41 of about 200k rows | a daily refit | no source |

* **Recommendation:** A: the source's own length. **Decision:** A or B?
"""


def test_the_horizon_is_an_issue_of_its_own(brp, tmp_path):
    """The Horizon block becomes issue H: the verdict in view, the declared windows, length and gap in the closed
    Details box, the options and the recommendation below it; resolved by the CC line that the horizon is checked.
    """
    temporal = {"on": "t", "window": 7, "unit": "days", "n_windows": 3, "comment": "One week."}
    record = tmp_path / "rec.md"
    record.write_text("---\nunique_name: rec\n---\n\n## Comments\n\nCC (2026-11-09, Lennart): other.\n")
    item = brp._horizon_item(HORIZON_BLOCK, temporal, record)
    assert (item["n"], item["resolved"]) == ("H", False)
    assert [o["key"] for o in item["options"]] == ["A", "B"]
    assert (item["implemented"], item["recommended"]) == ("A", "A")
    html = item["html"]
    assert html.index("keep the 7-day windows") < html.index('<details class="idetails">') < html.index("opttab")
    details = html[html.index('<details class="idetails">') : html.index("</details>")]
    assert "time column <code>t</code>" in details
    assert "no source states a refit cadence" in details
    assert "Details: declared, length, gap" in details
    assert '<col class="c-test">' in html  # the size of each option's test windows
    record.write_text(record.read_text() + "\nCC (2026-11-10, Lennart): the declared horizon (7 days) is checked.\n")
    assert brp._horizon_item(HORIZON_BLOCK, temporal, record)["resolved"] is True
    assert brp._horizon_item(HORIZON_BLOCK, None, record) is None


@pytest.fixture(scope="module")
def mover():
    """The script that moves a folder's review into its record, imported as a module."""
    return _import("move_reviews_to_records", SCRIPTS / "move_reviews_to_records.py")


def test_the_move_puts_a_folder_review_into_its_record(mover, tmp_path):
    """A folder's REVIEW.md moves into its record's ``## Review``: the title goes, relative links follow the move, the
    file is deleted; pointers to it in the comments and the definition are rewritten, history and the cross-dataset
    file stay; a second review for the same record is refused; ``--check`` lists what would move.
    """
    root, records = tmp_path / "copy", tmp_path / "records"
    folder = root / "toy_1m"
    folder.mkdir(parents=True)
    (folder / "dataset.py").write_text('NOTES = "kept as decided (REVIEW.md issue 3)"\n')
    (folder / "REVIEW.md").write_text(
        "# toy\n\n**Outcome:** added as `toy_1m`. See [the definition](dataset.py).\n\n"
        "**Main points:** none.\n\n**Issues for Lennart:**\n\n1. **Keep it?** Yes.\n"
    )
    (root / "REVIEW.md").write_text("# Across datasets\n")
    comments = (
        "CC (2026-11-01, Lennart): REVIEW.md issue 2, B.\n\n"
        "**Assessment (AI, 2026-10-22):** REVIEW.md removed (nothing left open); "
        "the rule went to the working copy's REVIEW.md."
    )
    save_record(
        CurationRecord(unique_name="toy", name="toy", v2_path="copy/toy_1m/dataset.py", comments=comments), records
    )
    args = ["--root", str(root), "--records", str(records)]
    assert mover.main([*args, "--check"]) == 1
    assert mover.main(args) == 0
    assert mover.main([*args, "--check"]) == 0
    assert not (folder / "REVIEW.md").exists()
    assert (root / "REVIEW.md").exists()
    record = load_record(records / "toy.md")
    assert record.review.startswith("**Outcome:** added as `toy_1m`.")
    assert "[the definition](../copy/toy_1m/dataset.py)" in record.review
    assert "CC (2026-11-01, Lennart): Review issue 2, B." in record.comments
    assert "REVIEW.md removed (nothing left open)" in record.comments
    assert "the working copy's REVIEW.md" in record.comments
    assert (folder / "dataset.py").read_text() == 'NOTES = "kept as decided (Review issue 3)"\n'
    (folder / "REVIEW.md").write_text("# toy\n\n**Outcome:** added as `toy_1m`.\n")
    with pytest.raises(ValueError, match="already has a review"):
        mover.main(args)
