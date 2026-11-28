"""The review page of the review-added-datasets skill and the parser of the records' reviews it reads.

The parser is ``data_foundry.curation.review``; the page script lives in the skill, not in the package, so it is
imported from its file. A missing script fails the module: the reviews in the records (``## Review``) are checked here.
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

import pytest

from data_foundry.curation import review as rv
from data_foundry.curation.store import load_record, save_record
from data_foundry.definition.splits import Temporal, TemporalSplits

pytest.importorskip("markdown_it", reason="the review page needs markdown-it-py (the `curation` extra)")

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / ".claude" / "skills" / "review-added-datasets" / "scripts" / "review_page.py"
TEMPLATE = SCRIPT.parents[1] / "assets" / "review_page.html"
ROOT = REPO / "datasets" / "_dev" / "tabarena-v0pt2"
RECORDS = REPO / "curation" / "records"
REVIEW_FILES = Path(__file__).parent / "fixtures" / "review_files"
"""The example of references/review_file_format.md: two records with a review."""
AIRFOIL = "records/airfoil_self_noise.md"
"""The example record of an added dataset, with its review."""
PANEL_BLOCK = "**Review panel:**" + load_record(REVIEW_FILES / AIRFOIL).review.split("**Review panel:**", 1)[1]
"""The review panel block of the example review, as written."""


def _add_comment(record: Path, line: str) -> None:
    """Append a line to a record's ``## Comments`` through the store API (the review follows the comments)."""
    rec = load_record(record)
    rec.comments = f"{rec.comments}\n\n{line}" if rec.comments else line
    save_record(rec, record.parent)


@pytest.fixture(scope="module")
def rp():
    """The page script, imported as a module."""
    if not SCRIPT.is_file():
        pytest.fail(f"{SCRIPT} is missing", pytrace=False)
    spec = importlib.util.spec_from_file_location("review_page", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up there
    spec.loader.exec_module(module)
    return module


def _in_git() -> bool:
    return shutil.which("git") is not None and (REPO / ".git").exists()


def _empty_root(tmp_path: Path) -> Path:
    """An empty working copy: the example reviews live in the records, not in dataset folders."""
    root = tmp_path / "working_copy"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _copy_files(tmp_path: Path) -> tuple[Path, Path]:
    """A copy of the example records with an empty working copy next to them."""
    shutil.copytree(REVIEW_FILES, tmp_path / "files")
    return _empty_root(tmp_path / "files"), tmp_path / "files" / "records"


def _broken_copy(tmp_path: Path, file: str, old: str, new: str) -> tuple[Path, Path, Path]:
    """A copy of the example records with one change, and the changed file."""
    root, records = _copy_files(tmp_path)
    path = tmp_path / "files" / file
    text = path.read_text()
    assert old in text
    path.write_text(text.replace(old, new, 1))
    return root, records, path


def _on_page(rp, root: Path, records: Path, *extra: str) -> tuple[list[str], list[str]]:
    """The records the page would show and the settled ones it leaves out."""
    args = rp.make_parser().parse_args(["check", "--root", str(root), "--records", str(records), *extra])
    reviews, _, settled = rp.select(args)
    return [r.name for r in reviews], settled


def _check(rp, root: Path, records: Path, *extra: str) -> int:
    return rp.main(["check", "--root", str(root), "--records", str(records), *extra])


def _parts(text: str) -> tuple[str, str]:
    """The record-field block and the issues block of the example review."""
    fields = text[text.index("**Record fields that disagree") : text.index("**Record judgment:**")]
    issues = text[text.index("**Issues for the curator:**") : text.index("**Review panel:**")]
    return fields, issues


def test_a_review_with_no_issue_when_a_panel_ran(rp, tmp_path):
    """A review can find nothing for the curator: a review with a panel and no issue is read (0 issues), one without
    a panel, an issue or a field row stops the parser.
    """
    text = (REVIEW_FILES / AIRFOIL).read_text()
    fields, issues = _parts(text)
    no_issue = text.replace(fields, "").replace(issues, "")
    root, records, _ = _broken_copy(tmp_path / "a", AIRFOIL, text, no_issue)
    by_name = {r.name: r for r in rv.read_reviews(records)}
    assert (by_name["airfoil_self_noise"].numbers, by_name["airfoil_self_noise"].fields) == ([], [])
    # A new dataset's round marks its metric, so the record stays for its verdict; without that it is settled.
    assert "airfoil_self_noise" in _on_page(rp, root, records, "--metric-marks", "airfoil_self_noise")[0]
    assert "airfoil_self_noise" in _on_page(rp, root, records)[1]

    no_panel = no_issue[: no_issue.index("**Review panel:**")]
    root, records, _ = _broken_copy(tmp_path / "b", AIRFOIL, text, no_panel)
    with pytest.raises(rv.ReviewFormatError, match="no issue, no record field and no review panel"):
        rv.read_reviews(records)


def test_the_example_reviews_parse():
    """The example reviews give their outcome, issues with their states and turns, field rows and panel."""
    reviews = rv.read_reviews(REVIEW_FILES / "records")
    by_name = {r.name: r for r in reviews}
    assert sorted(by_name) == ["airfoil_self_noise", "churn_telco_south_asia_duplicate"]
    airfoil = by_name["airfoil_self_noise"]
    assert (airfoil.folder, airfoil.numbers, airfoil.cell) == ("airfoil_self_noise", [1], "added")
    assert airfoil.points == "The target is in decibels; keep it?"
    assert [(f.key, f.record, f.definition) for f in airfoil.fields] == [("year", "2014", "1989")]
    assert airfoil.judgment.startswith("valid.")
    assert airfoil.issues_label == "Issues for the curator"
    issue = airfoil.issues[0]
    assert (issue.title, issue.state, issue.turns, issue.line) == ("Keep the target in decibels?", "open", [], 27)
    body, notes, footnotes = rv.cut_notes(issue.original)
    assert "**Problem:**" in body
    assert notes.startswith("on B, set `target_transform`")
    assert [k for k, _ in footnotes] == ["1"]
    assert rv.options(body)["implemented"] == "A"
    # The review panel is the last block, as written, and the issues end before it.
    assert airfoil.panel.text == PANEL_BLOCK
    assert airfoil.panel.recommendation == "ship (mediator)"
    assert [s.title for s in airfoil.panel.sections] == ["Claim audit", "Mediator"]
    assert "Review panel" not in issue.text
    # The record without a folder: its review ends before the later CC comment.
    other = by_name["churn_telco_south_asia_duplicate"]
    assert (other.folder, other.cell, other.numbers, other.panel) == (None, "not added; duplicate", [1], None)
    assert "CC (" not in other.issues[0].text
    assert [w for r in reviews for w in rv.shape_warnings(r)] == []


def test_issue_states_and_turns():
    """An issue is open, resolved, or deferred when its last closing turn (or its title) says so; turns carry who,
    when and the mark.
    """
    text = (
        "1. **Open?**\n   * **Problem:** p.\n   **Lennart (2026-11-05, discuss):** why?\n"
        "   **Answer (AI, 2026-11-06):** because.\n\n"
        "2. **Resolved?**\n   x.\n\n   **Deferred (2026-11-05):** parked.\n\n"
        "   **Resolved (2026-11-08, Lennart):** kept.\n"
        "3. **Parked?**\n   x.\n   **Deferred (2026-11-08):** parked.\n"
        "4. **Deferred: the window**\n   x.\n"
    )
    _, issues = rv.split_issues(text)
    assert [i.state for i in issues] == ["open", "resolved", "deferred", "deferred"]
    turns = issues[0].turns
    assert [(t.who, t.kind, t.date, t.by, t.mark) for t in turns] == [
        ("curator", "note", "2026-11-05", "Lennart", "discuss"),
        ("ai", "answer", "2026-11-06", "", ""),
    ]
    assert issues[0].original == "* **Problem:** p."
    assert issues[1].turns[-1].by == "Lennart"


def test_names_filter(rp, tmp_path):
    """--names keeps only the named records and stops on a name without a review."""
    root, records = _empty_root(tmp_path), REVIEW_FILES / "records"
    assert _on_page(rp, root, records, "--names", "airfoil_self_noise")[0] == ["airfoil_self_noise"]
    assert _check(rp, root, records, "--names", "no_such_record") == 1


def test_a_settled_record_leaves_the_page(rp, tmp_path):
    """A record with every issue resolved and no field row leaves the page by default (it ships by default; Lennart,
    2026-11-08); --keep-settled keeps it, and so does an issue whose last closing turn is Deferred. Its metric keeps it
    only when the round marks it (--metric-marks) and the record has no CC line that it is checked (Lennart,
    2026-11-10).
    """
    text = (REVIEW_FILES / AIRFOIL).read_text()
    fields, _ = _parts(text)
    panel = text.index("**Review panel:**")
    closing = "   **Deferred (2026-11-05):** parked.\n\n   **Resolved (2026-11-08, Lennart):** kept.\n\n"
    settled = text[:panel].rstrip("\n") + "\n\n" + closing + text[panel:]
    root, records, _ = _broken_copy(tmp_path, AIRFOIL, text, settled.replace(fields, ""))

    shown, left_out = _on_page(rp, root, records)
    assert ("airfoil_self_noise" not in shown, left_out) == (True, ["airfoil_self_noise"])
    for marks in ("airfoil_self_noise", "all"):
        assert "airfoil_self_noise" in _on_page(rp, root, records, "--metric-marks", marks)[0]
    assert _check(rp, root, records, "--metric-marks", "no_such_record") == 1

    record = records / "airfoil_self_noise.md"
    _add_comment(record, "CC (2026-11-08, Lennart): the declared metric (`rmse`) is checked, as declared.")
    shown, left_out = _on_page(rp, root, records, "--metric-marks", "airfoil_self_noise")
    assert (shown, left_out) == (["churn_telco_south_asia_duplicate"], ["airfoil_self_noise"])
    assert "airfoil_self_noise" in _on_page(rp, root, records, "--keep-settled")[0]

    # Only settled records named: nothing is left to review, so no page is written.
    out = tmp_path / "page"
    args = ["build", "--root", str(root), "--records", str(records), "--out", str(out), "--names", "airfoil_self_noise"]
    assert rp.main(args) == 0
    assert not out.exists()

    # Deferred last: the record is parked, not settled.
    record.write_text(record.read_text().replace(closing, "   **Deferred (2026-11-08):** parked.\n\n"))
    assert "airfoil_self_noise" in _on_page(rp, root, records)[0]


def test_a_retired_record_keeps_its_review(tmp_path):
    """A dataset retired from the working copy (its folder gone, ``v2_path`` cleared) keeps its review in its record:
    the parser reads it without a folder, from the outcome's ``added``.
    """
    _root, records = _copy_files(tmp_path)
    rec = load_record(records / "airfoil_self_noise.md")
    rec.v2_path = None
    save_record(rec, records)
    reviews = rv.read_reviews(records, ["airfoil_self_noise"])
    assert [(r.name, r.folder, r.numbers) for r in reviews] == [("airfoil_self_noise", "airfoil_self_noise", [1])]


@pytest.mark.parametrize(
    ("file", "old", "new", "line", "message"),
    [
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
        (AIRFOIL, "## Review\n\n", "## Review\n\nIntro.\n", 16, "text before"),
        ("records/churn_telco_south_asia_duplicate.md", "not added; duplicate", "duplicate", 16, "`not added`"),
        # The review panel: one per review, the last block, every <details> closed.
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
        (AIRFOIL, "| holds | |\n\n</details>\n", "| holds | |\n\n", 52, "is not closed"),
        (AIRFOIL, "issue 1.\n\n</details>\n", "issue 1.\n", 61, "not closed"),
        (
            AIRFOIL,
            "</details>\n\n<details><summary>Mediator",
            "</details>\n\nStray.\n\n<details><summary>Mediator",
            61,
            "text outside a section",
        ),
        (AIRFOIL, "**Review panel:** ship (mediator).", "**Review panel:**\n\nship (mediator).", 49, "no summary"),
        (AIRFOIL, "<details><summary>Claim audit", "<details open><summary>Claim audit", 52, "on one line"),
    ],
)
def test_format_errors_name_the_record_and_line(tmp_path, file, old, new, line, message):
    """A review that breaks the format stops the parser with the record and the line."""
    _root, records, path = _broken_copy(tmp_path, file, old, new)
    with pytest.raises(rv.ReviewFormatError, match=re.escape(message)) as error:
        rv.read_reviews(records)
    assert str(error.value).startswith(f"{path}, line {line}:" if line else f"{path}:")


def test_a_label_line_inside_an_issue_stays_in_the_issue(tmp_path):
    """A bold label that is not a block of the review (``**Split:**``) is text of the issue it stands in."""
    old = "     scale a practitioner models it on.\n"
    _root, records, _ = _broken_copy(tmp_path, AIRFOIL, old, old + "**Split:** x\n")
    airfoil = next(r for r in rv.read_reviews(records) if r.name == "airfoil_self_noise")
    assert airfoil.issues[0].text.endswith("**Split:** x")


def test_fenced_code_stays_in_the_panel(tmp_path):
    """Inside a fence, a panel's lines are text: a `#` comment or a `</details>` neither breaks nor closes it."""
    fenced = "```python\n# the check\nprint('</details>')\n```\n\nShip."
    _root, records, _ = _broken_copy(tmp_path, AIRFOIL, "Ship. The advocate", fenced)
    airfoil = next(r for r in rv.read_reviews(records) if r.name == "airfoil_self_noise")
    assert [s.title for s in airfoil.panel.sections] == ["Claim audit", "Mediator"]
    assert "# the check" in airfoil.panel.text


def test_working_copy_reviews_parse():
    """The committed reviews (the records' ``## Review``) follow the format (no review file: test_records_integrity)."""
    reviews = rv.read_reviews(RECORDS)
    with_review = [
        p.stem for p in sorted(RECORDS.glob("*.md")) if not p.name.startswith("_") and "\n## Review\n" in p.read_text()
    ]
    assert [r.name for r in reviews] == with_review


def test_the_example_reviews_build_the_page(rp, tmp_path):
    """The example reviews give the expected records, items, fields and ids, and the page embeds the data."""
    if not (ROOT / "airfoil_self_noise" / "dataset.py").is_file() or not _in_git():
        pytest.skip("needs the working copy's airfoil_self_noise and a git checkout")
    where = ["--root", str(ROOT), "--records", str(REVIEW_FILES / "records")]
    args = ["build", *where, "--out", str(tmp_path), "--title", "Fixture Review", "--date", "2026-10-01"]
    assert rp.main(args) == 0
    data = json.loads((tmp_path / "data.json").read_text())
    page = (tmp_path / "review_page.html").read_text()

    # The page's order is review_order (priority, then the fewest open marks).
    assert sorted(d["name"] for d in data["datasets"]) == ["airfoil_self_noise", "churn_telco_south_asia_duplicate"]
    assert data["datasets"] == sorted(data["datasets"], key=rp.review_order)
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
    cls = rp.load_definition(ROOT / "airfoil_self_noise" / "dataset.py")
    expected = cls.task_summary.fields()
    assert added["summary"]["source"] == "definition"
    assert added["summary"]["question"] == expected["question"]
    assert added["summary"]["fields"]["use_case"] == expected["use_case"]

    # The metric comes from the definition's declared Metric, resolved for its problem type.
    if isinstance(getattr(cls, "metric", None), rp.Metric):
        spec = cls.metric.spec(cls.problem_type)
        assert added["metric"]["source"] == "definition"
        assert (added["metric"]["name"], added["metric"]["origin"]) == (spec["name"], spec["origin"])
        assert added["metric"]["reason"] == spec["reason"]

    # Not added: no folder, no definition.
    assert other["cat"] == "notadded"
    assert (other["folder"], other["code"], other["summary"], other["metric"]) == (None, None, None, None)
    assert [(it["n"], it["resolved"]) for it in other["items"]] == [(1, False)]

    assert "crosscut" not in data
    assert data["title"] == "Fixture Review"
    assert data["generated"] == "2026-10-01"
    assert "2 curation records" in data["subtitle"]
    assert "1 added dataset and 1 record without a folder" in data["headerHtml"]

    assert "<title>Fixture Review</title>" in page
    assert 'ctab("panel", "Panel")' in page
    assert re.search(r"__(TITLE|SUBTITLE|DATA)__", page) is None
    embedded = page.split('<script type="application/json" id="data">', 1)[1].split("</script>", 1)[0]
    assert json.loads(embedded) == data


def test_panel_becomes_page_data(rp, tmp_path):
    """The panel's summary, recommendation and sections reach the page; a label-like line inside it stays in it."""
    old, new = "Ship. The advocate", "**Split:** agreed.\n\nShip. The advocate"
    _root, records, _ = _broken_copy(tmp_path, AIRFOIL, old, new)
    by_name = {r.name: r for r in rv.read_reviews(records)}
    airfoil, churn = by_name["airfoil_self_noise"], by_name["churn_telco_south_asia_duplicate"]
    assert rp._panel(churn.panel) is None
    assert airfoil.numbers == [1]
    panel = rp._panel(airfoil.panel)
    assert sorted(panel) == ["recommendation", "sections", "summary"]
    assert panel["recommendation"] == "ship (mediator)"
    assert panel["summary"].startswith("<p>ship (mediator). Claim audit: 2 claims, 2 hold.")
    claims, mediator = panel["sections"]
    assert claims["title"] == "Claim audit"
    assert "<table>" in claims["html"]
    assert "<details" not in claims["html"]
    assert mediator["title"] == "Mediator"
    assert "<strong>Split:</strong> agreed." in mediator["html"]


def _review(issues: str) -> rv.Review:
    """A review of the record ``x`` with the given issues block."""
    return rv.Review(
        name="x", source=Path("x"), folder="x", outcome="added", points="", issues=rv.split_issues(issues)[1]
    )


def test_shape_warnings_name_issues_out_of_shape():
    """An open issue without its bullets or options table, or with a rule ID in its text, is named; a closed one not."""
    review = _review(
        "1. **Old shape?** Per LEAK-10 the column goes.\n\n"
        "2. **Closed?** Per LEAK-10.\n   **Resolved (2026-11-01, Andrej):** done.\n"
    )
    assert rv.shape_warnings(review) == [
        "x issue 1: no Problem, Options, Recommendation, options table",
        "x issue 1: rule IDs in the text (LEAK-10); move them to footnotes",
    ]
    review = _review(
        "1. **No implemented row?**\n\n   * **Problem:** p.\n   * **Options:**\n\n     | | Option |\n     |---|---|\n"
        "     | A | x |\n     | B | y |\n\n   * **Recommendation:** A.\n"
    )
    assert rv.shape_warnings(review) == [
        "x issue 1: no row marked (implemented), which the page's As implemented locks in"
    ]


def test_shape_warnings_name_a_problem_out_of_shape():
    """A problem is at most PROBLEM_BULLETS bullets of one sentence each; its length in words is free, and neither
    the footnote markers nor a full stop inside a number end a sentence.
    """

    def warnings(problem: str) -> list[str]:
        return rv.shape_warnings(
            _review(
                f"1. **Q?**\n\n   * **Problem:**{problem}\n   * **Options:**\n\n     | | Option |\n     |---|---|\n"
                "     | A | x (implemented) |\n\n   * **Recommendation:** A.\n\n   [^1]: r.\n"
            )
        )

    long_sentence = " ".join(["word"] * 80) + " scores 0.62.[^1]"
    assert warnings(f" {long_sentence}") == []
    assert warnings("\n     - First, at 0.5.\n     - Second.[^1]\n     - Third?") == []
    assert warnings("\n     - One. Two.\n     - Three.") == [
        "x issue 1: no one sentence per problem bullet (1 with more)"
    ]
    assert warnings("\n" + "".join(f"     - Point {i}.\n" for i in range(4))) == [
        "x issue 1: no short problem (4 bullets, at most 3)"
    ]


def test_metric_is_resolved_by_the_records_cc_line(rp, tmp_path):
    """The metric counts as resolved once the record says the declared metric is checked (the latest such line)."""
    rec = tmp_path / "x.md"
    rec.write_text(
        "---\nunique_name: x\nname: x\n---\n\n## Comments\n\n"
        "CC (2026-10-21, Lennart): the declared metric documents it.\n"
    )
    assert rp._checked(rec, "metric") is None
    rec.write_text(
        rec.read_text() + "\nCC (2026-11-04, Lennart): the declared metric is checked and stays as declared.\n"
        "\nCC (2026-11-05, Lennart): the declared metric (RMSE) is checked and stays as declared.\n"
    )
    assert rp._checked(rec, "metric")["date"] == "2026-11-05"
    assert rp._checked(tmp_path / "missing.md", "metric") is None


def test_the_split_is_marked_only_when_the_round_asks(rp, tmp_path):
    """The split, like the metric, keeps a settled record on the page only when --split-marks names it, until the
    record's CC line says the declared split is checked; the page's split box and mark are gated on it.
    """
    text = (REVIEW_FILES / AIRFOIL).read_text()
    fields, issues = _parts(text)
    root, records, _ = _broken_copy(tmp_path, AIRFOIL, text, text.replace(fields, "").replace(issues, ""))
    assert "airfoil_self_noise" not in _on_page(rp, root, records)[0]
    assert "airfoil_self_noise" in _on_page(rp, root, records, "--split-marks", "airfoil_self_noise")[0]
    assert _check(rp, root, records, "--split-marks", "no_such_record") == 1

    record = records / "airfoil_self_noise.md"
    assert rv.checked(record, "split") is None
    _add_comment(record, "CC (2026-11-12, Lennart): the declared split (iid, 3 x 3 folds) is checked, as declared.")
    assert rv.checked(record, "split")["date"] == "2026-11-12"
    assert "airfoil_self_noise" not in _on_page(rp, root, records, "--split-marks", "airfoil_self_noise")[0]

    page = TEMPLATE.read_text()
    assert "const hasSplitMark = (d) => !!d.splitMark && " in page
    assert "&& !d.splitChecked;" in page
    assert 'if (!d.splitMark) return "";' in page


def test_the_horizon_block_and_its_sign_off(rp, tmp_path):
    """A review's Horizon block is read; with --horizon-marks the record waits for the CC line that the declared
    horizon is checked (Lennart, 2026-11-10: new temporal datasets get the sign-off, like the metric).
    """
    text = (REVIEW_FILES / AIRFOIL).read_text()
    horizon = "**Horizon:** a week, the refit cadence the source names.\n\n- **Gap:** one day, the label delay.\n\n"
    with_horizon = text.replace("**Issues for the curator:**", horizon + "**Issues for the curator:**")
    fields, issues = _parts(with_horizon)
    root, records, _ = _broken_copy(tmp_path, AIRFOIL, text, with_horizon.replace(fields, "").replace(issues, ""))
    airfoil = {r.name: r for r in rv.read_reviews(records)}["airfoil_self_noise"]
    assert airfoil.horizon.startswith("a week, the refit cadence")
    assert "airfoil_self_noise" not in _on_page(rp, root, records)[0]  # nothing marked: settled
    assert "airfoil_self_noise" in _on_page(rp, root, records, "--horizon-marks", "airfoil_self_noise")[0]
    record = records / "airfoil_self_noise.md"
    _add_comment(record, "CC (2026-11-10, Lennart): the declared horizon (7-day windows) is checked.")
    assert rv.checked(record, "horizon")["by"] == "Lennart"
    assert "airfoil_self_noise" not in _on_page(rp, root, records, "--horizon-marks", "airfoil_self_noise")[0]


def test_the_horizon_is_an_issue_of_its_own(rp, tmp_path):
    """The Horizon block becomes issue H: the verdict in view, the declared windows, length and gap in the closed
    Details box, the options and the recommendation below it; resolved by the CC line that the horizon is checked.
    """
    temporal = {"on": "t", "window": 7, "unit": "days", "n_windows": 3, "comment": "One week."}
    record = tmp_path / "rec.md"
    record.write_text("---\nunique_name: rec\nname: rec\n---\n\n## Comments\n\nCC (2026-11-09, Lennart): other.\n")
    item = rp._horizon_item(HORIZON_BLOCK, temporal, record)
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
    assert rp._horizon_item(HORIZON_BLOCK, temporal, record)["resolved"] is True
    assert rp._horizon_item(HORIZON_BLOCK, None, record) is None


def test_review_order(rp):
    """Priority 5 first, records without one last; within one priority the fewest open marks, then the name."""
    rows = [
        {"name": "b", "priority": 3, "openMarks": 4},
        {"name": "none", "priority": None, "openMarks": 0},
        {"name": "a", "priority": 3, "openMarks": 4},
        {"name": "quick", "priority": 3, "openMarks": 1},
        {"name": "top", "priority": 5, "openMarks": 9},
    ]
    assert [r["name"] for r in sorted(rows, key=rp.review_order)] == ["top", "quick", "a", "b", "none"]


def test_template_has_the_panel_tab_and_keeps_the_store():
    """The Panel tab follows Decisions; the store's collections and the mark fields are unchanged."""
    page = TEMPLATE.read_text()
    assert 'const CTABS = ["usecase", "decisions", "panel", "details", "code", "report", "record"];' in page
    assert 'data-act="openpanel"' in page
    # The rail groups the records by priority, in the order the builder sorted them.
    assert '<li class="grp" aria-hidden="true">' in page
    # Ship verdicts with nothing open leave their priority group for the "To ship" group at the end.
    assert 'const groupLabel = (g) => (g === "ship" ? "To ship" : prioLabel(g));' in page
    assert 'db.collection("reviews").onSnapshot(' in page
    assert "const S = { reviews: {} };" in page
    assert "crosscut" not in page
    assert 'data-tab="across"' not in page
    # The Use case tab shows the declared split and the declared metric under the task summary, each with a mark; the
    # metric only when the round marks it.
    assert 'panel("usecase", useCaseHtml(d) + splitHtml(d) + metricHtml(d))' in page
    assert 'if (!d.metricMark) return "";' in page
    assert "const hasMetricMark = (d) => !!d.metricMark && " in page
    assert 'data-note="split"' in page
    assert "if (out.split && !out.split.d" in page


def test_split_from_the_readme_and_the_definition(rp):
    """The split comes from the README's front matter (its reason too) and Splits section, the Forced tags and the
    split notes; a README written before the reason key takes the definition's `splits_comment`.
    """
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
  reason: Six weeks ahead, as the competition asks.
  n_train: {min: 10, max: 20}
  n_test: {min: 5, max: 6}
---

## Splits

Expanding-window temporal splits: 3 test window(s) of 42 days.

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
    got = rp._split(readme, ["Tabular", "ForcedIIDFromTemporal"], comments)
    assert (got["regime"], got["time_on"], got["time_horizon"], got["n_folds"]) == ("temporal", "Date", 42, 1)
    assert got["forced"] == ["ForcedIIDFromTemporal"]
    assert "Six weeks ahead" in got["noteHtml"]
    assert "repeat(s)" not in got["noteHtml"]
    assert got["tableHtml"].count("<tr>") == 2
    assert got["notes"] == ["The split follows the competition's temporal test window."]

    assert "Expanding-window" not in got["noteHtml"]
    no_reason = readme.replace("  reason: Six weeks ahead, as the competition asks.", "  reason: null")
    assert rp._split(no_reason, [], None, splits_comment="ignored: the key says none")["noteHtml"] == ""
    before_the_key = readme.replace("  reason: Six weeks ahead, as the competition asks.\n", "")
    assert rp._split(before_the_key, [], None)["noteHtml"] == ""
    note = rp._split(before_the_key, [], None, splits_comment="\n        Six weeks ahead.\n    ")["noteHtml"]
    assert "Six weeks ahead" in note
    assert rp._split("no front matter", [], None) is None

    code = 'class X:\n    data_tags = ("ForcedIIDFromTemporal",)\n    curation_comments = "- a split note"\n'
    assert rp._literal_from_source(code, "data_tags") == ("ForcedIIDFromTemporal",)
    assert rp._literal_from_source(code, "curation_comments") == "- a split note"
    assert rp._literal_from_source(code, "metric") is None


def test_header_names_the_marks_and_the_settled_records(rp):
    """The Summary view's header names the records whose metric, horizon or split the round marks, and the settled
    records left out; a mark the round does not set is not named.
    """
    marks = rp.Marks(metric={"a", "b_c"}, horizon=None)
    assert (marks.asks("metric", "a"), marks.asks("metric", "z"), marks.asks("horizon", "z")) == (True, False, True)
    assert not marks.asks("split", "a")
    header = rp.header_markdown([], marks, ["done"], "2026-11-26")
    assert "**Metric marks:** `a`, `b_c`." in header
    assert "**Horizon marks:** all." in header
    assert "Split marks" not in header
    assert "**Settled, left out (they ship by default):** `done`." in header


def test_metric_from_the_definition_and_the_readme(rp):
    """The metric spec comes from the definition's Metric (all fields) or, failing that, the README frontmatter."""

    class Definition:
        problem_type = "binary_classification"
        metric = rp.Metric.fallback(reason="the paper reports accuracy, precision and recall side by side")
        scoring_columns = ()

    got = rp._metric_from_class(Definition)
    assert (got["name"], got["origin"], got["source"]) == ("roc_auc", "fallback", "definition")
    assert got["reason"].startswith("the paper reports")
    assert got["scoring_columns"] == []

    Definition.metric = "roc_auc"  # not a Metric: nothing from the class
    assert rp._metric_from_class(Definition) is None

    front = rp._metric_from_front({"metric": "mae", "metric_origin": "source", "scoring_columns": ["era"]})
    assert (front["name"], front["origin"], front["source"]) == ("mae", "source", "readme")
    assert front["scoring_columns"] == [{"column": "era"}]
    assert rp._metric_from_front({}) is None


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_a_definition_removed_on_a_squash_merged_branch_is_found(rp, tmp_path):
    """A folder added and removed on a side branch (squash-merged into main) is not in HEAD's history."""

    def git(*args):
        rp._git(tmp_path, *args)

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

    commit, removed_on = rp._last_commit_with(tmp_path, "gone/dataset.py")
    assert rp._show(tmp_path, commit, "gone/dataset.py") == "code\n"
    assert removed_on is not None
    assert rp._last_commit_with(tmp_path, "never/dataset.py") is None


def test_thread_splits_the_original_from_the_turns(rp):
    """An item's text splits into the original and one turn per label."""
    text = (
        "The item proposes a change.\n"
        "**Lennart (2026-10-21, discuss):** Why?\n"
        "**Answer (AI, 2026-10-21):** Because the rule says so.\n"
        "Second line of the answer.\n"
        "**Resolved (2026-10-22, Lennart):** done."
    )
    out = rp._thread(text)
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
    assert rp._thread("No turns here.")["thread"] == []


def test_render_hides_footnotes_and_notes_for_the_ai(rp):
    """Footnotes are numbered by first reference and closed in a box; the notes for the AI get a closed box too."""
    text = (
        "* **Problem:** a later reference[^b] and an earlier one[^a].\n\n"
        "**Notes for the AI:** drop `x`[^a].\n\n"
        "[^a]: **LEAK-31** (Should): keep with a note.\n"
        "[^b]: **SPLIT-15** (Should): as many windows\n"
        "  as folds."
    )
    out = rp.render(text)
    assert out.index('data-fn="1"') < out.index("earlier one")  # [^b] is referenced first, so it is 1
    assert '<details class="ainotes"><summary>Notes for the AI</summary>' in out
    assert "drop <code>x</code>" in out
    assert "Rules and references (2)" in out
    assert "as many windows as folds" in out
    assert "[^" not in out
    assert "LEAK-31" not in out.split("<details")[0]
    assert rp.render("No footnote [^z] here.") == "<p>No footnote [^z] here.</p>\n"


def test_issue_text_folds_the_details_between_problem_and_options(rp):
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
    out = rp._thread(text)["html"]
    assert out.index("short") < out.index('<details class="idetails">') < out.index("0.62") < out.index("<table")
    assert "<summary>Details: experiments, consistency</summary>" in out
    assert out.index("<table") < out.index("Recommendation")
    assert 'data-fn="2"' in out.split('<details class="fnotes">')[0]
    assert "idetails" not in rp._thread("* **Asked:** x.\n* **Found:** y.")["html"]  # no problem bullet: no fold


def test_options_table_shows_points_as_bullets_and_tags_rows(rp):
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
    out = rp._thread(text)["html"]
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
    assert "opttab" not in rp.render("| a | b |\n|---|---|\n| x; y | z |")
    # Each row carries its letter and a hidden tag the page shows on the row a mark locks in.
    assert 'data-key="A"' in impl
    assert '<span class="otag pick" hidden></span>' in impl


def test_ai_turn_choices_become_answer_buttons(rp):
    """An AI turn's lettered bullets leave its text as choices (continuation lines joined), with the "give the letter"
    sentence; a turn with one lettered line or none keeps its text and has no choices.
    """
    text = (
        "* **Problem:** p.\n**Consistency check (AI, 2026-11-05):** what sets it apart?\n"
        "- (a) the fact,\n  written down;\n- (b) drop it.\n\n"
        "Give the letter in the note; nothing is applied until\nthen.\n"
    )
    turn = rp._thread(text)["thread"][-1]
    assert [c["key"] for c in turn["choices"]] == ["a", "b"]
    assert turn["choices"][0]["html"] == "the fact, written down"
    assert "(a)" not in turn["html"]
    assert "Give the letter" not in turn["html"]
    assert "nothing is applied" not in turn["html"]
    plain = rp._thread("* **Problem:** p.\n**Answer (AI, 2026-11-05):** yes; (a) inline is no choice.\n")["thread"][-1]
    assert plain["choices"] == []
    assert "(a) inline" in plain["html"]


def test_ai_turn_in_issue_shape_renders_like_an_issue(rp):
    """A consistency check in the issue shape (as the parser passes it, the issue's indent removed) keeps its
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
    turn = rp._thread(text)["thread"][-1]
    assert [c["key"] for c in turn["choices"]] == ["a", "b"]
    assert turn["choices"][0]["html"] == "Record the fact"
    assert '<table class="opttab">' in turn["html"]
    assert 'data-key="a"' in turn["html"]
    assert "otag rec" in turn["html"].split('data-key="b"')[0]
    assert 'class="fnotes"' in turn["html"]
    assert "LEAK-10" not in turn["html"].split('class="fnotes"')[0]


def test_thread_gives_the_ai_turn_the_curator_replies_to(rp):
    """An issue whose last turn is the AI's carries an `askId` (the page counts it unmarked until a reply names it);
    a new AI turn gets a new id; an issue whose last turn is the curator's or a closing label has none.
    """
    base = "* **Problem:** p.\n"
    asked = rp._thread(base + "**Lennart (2026-11-05, change):** why?\n**Answer (AI, 2026-11-05):** because.\n")
    again = rp._thread(base + "**Answer (AI, 2026-11-05):** because, and more.\n")
    assert asked["askId"]
    assert again["askId"]
    assert asked["askId"] != again["askId"]
    assert rp._thread(base + "**Answer (AI, 2026-11-05):** a.\n**Lennart (2026-11-05, ok):** fine.\n")["askId"] == ""
    assert rp._thread(base + "**Resolved (2026-11-05, Lennart):** done.\n")["askId"] == ""
    assert rp._thread(base)["askId"] == ""


def test_issue_options_name_what_each_mark_locks_in(rp):
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
    thread = rp._thread(text)
    assert [o["key"] for o in thread["options"]] == ["A", "B"]
    assert thread["options"][0]["nameHtml"] == "Keep <code>x</code>"
    assert (thread["implemented"], thread["recommended"]) == ("A", "B")
    none = rp._thread("* **Problem:** p.\n* **Options:**\n\n  | | Option |\n  |---|---|\n  | A | x |\n  | B | y |\n")
    assert (none["implemented"], [o["key"] for o in none["options"]]) == ("", ["A", "B"])
    assert rp._thread("Plain text.")["options"] == []


def _iid_split(rp, tags, comments, basis_reason=None):
    readme = "---\ntask:\n  split_regime: iid\nsplits:\n  n_repeats: 3\n  n_folds: 3\n---\n"
    return rp._split(readme, tags, comments, basis_reason)


def _record(tmp_path, *tags):
    record = tmp_path / "r.md"
    record.write_text("---\ntags:\n" + "".join(f"- '{t}'\n" for t in tags) + "---\n")
    return record


def test_the_split_box_shows_the_basis_and_the_records_facts(rp, tmp_path):
    """The time basis, its reason and the record's collection facts reach the split box, as information."""
    split = _iid_split(rp, ["IID", "ForcedIIDFromTemporal"], "- x", "all scored in\n    September 2005.")
    rp._time_facts(
        split, _record(tmp_path, "Samples: One Moment", "Target: Fixed Delay", "Entities: Recur", "Tiny Data")
    )
    assert split["time"]["basis"] == "ForcedIIDFromTemporal"
    assert "September 2005" in split["time"]["lineHtml"]
    assert split["time"]["facts"] == ["Samples: One Moment", "Target: Fixed Delay", "Entities: Recur"]


def test_a_forced_tag_is_shown_as_the_time_basis(rp, tmp_path):
    """A forced tag is the time basis the split box shows."""
    split = _iid_split(rp, ["IID", "ForcedIIDFromTemporal"], None)
    rp._time_facts(split, _record(tmp_path, "Samples: Over Time", "Time: Lost"))
    assert split["time"]["basis"] == "ForcedIIDFromTemporal"
    assert split["time"]["facts"] == ["Samples: Over Time", "Time: Lost"]


def test_temporal_from_the_definition(rp):
    """The declared windows the horizon box shows come from the definition's Temporal."""

    class Definition:
        temporal = Temporal(on="t", splits=TemporalSplits(window=7, unit="days", n_windows=3, gap=1))
        splits_comment = """
            A model refit every week.
        """

    got = rp._temporal_from_class(Definition)
    assert (got["on"], got["window"], got["unit"], got["n_windows"], got["gap"]) == ("t", 7, "days", 3, 1)
    assert got["comment"] == "A model refit every week."
    assert "cutoffs" not in got
    Definition.temporal = None
    assert rp._temporal_from_class(Definition) is None


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
