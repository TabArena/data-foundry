"""The curation scripts of the knowledge-data-foundry skill: coverage, priority factors, clean room, decision register.

The scripts live in the skill, not in the package, so they are imported from their files. They run here on small
records written to ``tmp_path``; the clean room's end-to-end test needs the raw files of ``airfoil_self_noise`` and
skips without them.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest
from data_foundry.curation.record import CurationRecord
from data_foundry.curation.store import save_record

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / ".claude" / "skills" / "knowledge-data-foundry" / "scripts"


def _import(name: str):
    path = SCRIPTS / f"{name}.py"
    if not path.is_file():
        pytest.fail(f"{path} is missing", pytrace=False)
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))  # clean_room imports its neighbour dataset_io
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up there
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def coverage():
    """benchmark_coverage.py, imported as a module."""
    return _import("benchmark_coverage")


@pytest.fixture(scope="module")
def priority():
    """priority_factors.py, imported as a module."""
    return _import("priority_factors")


@pytest.fixture(scope="module")
def clean_room():
    """clean_room.py, imported as a module."""
    return _import("clean_room")


@pytest.fixture(scope="module")
def register():
    """decision_register.py, imported as a module."""
    return _import("decision_register")


def _record(directory: Path, unique_name: str, **fields) -> CurationRecord:
    record = CurationRecord(unique_name=unique_name, name=unique_name, **fields)
    save_record(record, directory)
    return record


# --------------------------------------------------------------------------- benchmark_coverage
def test_accepted_set(coverage):
    """Accepted: a Yes verdict or DF: Yes, never a retired one."""
    yes = CurationRecord(unique_name="a", name="a", suggestion="Yes")
    disagreement = CurationRecord(unique_name="b", name="b", suggestion="Yes (Disagreement)")
    df_yes = CurationRecord(unique_name="c", name="c", suggestion="No", data_foundry_status=["DF: Yes"])
    retired = CurationRecord(unique_name="d", name="d", suggestion="No (Retired)", data_foundry_status=["DF: Yes"])
    open_ = CurationRecord(unique_name="e", name="e", suggestion="TBD -> Yes")
    assert [coverage.is_accepted(r) for r in (yes, disagreement, df_yes, retired, open_)] == [
        True,
        True,
        True,
        False,
        False,
    ]


def test_coverage_counts_and_thin_values(coverage):
    """Counts per value, thin at max(2, median / 2), zero-count vocabulary values thin, placeholders never."""
    records = [
        *[CurationRecord(unique_name=f"f{i}", name="f", suggestion="Yes", domain="finance") for i in range(6)],
        *[CurationRecord(unique_name=f"m{i}", name="m", suggestion="Yes", domain="medical") for i in range(6)],
        CurationRecord(unique_name="e0", name="e", suggestion="Yes", domain="education"),
        CurationRecord(unique_name="o0", name="o", suggestion="Yes", domain="Other"),
        CurationRecord(unique_name="x0", name="x", suggestion="Yes"),
        CurationRecord(unique_name="n0", name="n", suggestion="No", domain="physics"),
        CurationRecord(
            unique_name="r0", name="r", suggestion="Yes", required_split=["Random (IID)", "Grouped (NON-IID)"]
        ),
    ]
    vocab = {"domain": ["finance", "medical", "education", "physics", "Other", "?"], "required_split": []}
    result = coverage.coverage(records, vocab)
    assert result["accepted"] == 16
    rows = {row["value"]: row for row in result["fields"]["domain"]["values"]}
    assert rows["finance"]["count"] == 6
    assert result["fields"]["domain"]["thin_threshold"] == 3  # half the median of 6, 6, 1 (the real values)
    assert not rows["finance"]["thin"]
    assert rows["education"]["thin"]
    assert rows["education"]["datasets"] == ["e0"]
    assert rows["physics"] == {**rows["physics"], "count": 0, "thin": True}  # vocabulary, no accepted dataset
    assert not rows["Other"]["thin"]
    assert "?" not in rows
    assert not rows["(empty)"]["thin"]
    splits = {row["value"]: row["count"] for row in result["fields"]["required_split"]["values"]}
    assert splits["Random (IID)"] == splits["Grouped (NON-IID)"] == 1  # a record with two regimes counts under each
    text = coverage.render(result)
    assert "| education | 1 |" in text
    assert "max(2, half the median count" in text


def test_coverage_main_writes_json(coverage, tmp_path, capsys):
    """The command line prints the tables and writes the JSON."""
    records = tmp_path / "records"
    _record(records, "a", suggestion="Yes", domain="finance", problem_type="Regression")
    _record(records, "b", suggestion="No", domain="finance")
    vocab = tmp_path / "vocabularies.yaml"
    vocab.write_text("domain:\n- finance\n- education\nproblem_type:\n- Regression\n")
    out = tmp_path / "coverage.json"
    assert coverage.main(["--records", str(records), "--vocab", str(vocab), "--json", str(out)]) == 0
    assert "1 accepted datasets of 2 records" in capsys.readouterr().out
    data = json.loads(out.read_text())
    assert [row["value"] for row in data["fields"]["domain"]["values"] if row["thin"]] == ["finance", "education"]


# --------------------------------------------------------------------------- priority_factors
def _facts(domain="finance", problem="regression", regime="iid", units=5000, features=10, non_numeric=("categorical",)):
    return {
        "domain": domain,
        "problem_type": problem,
        "regime": regime,
        "units": units,
        "features": features,
        "non_numeric": list(non_numeric),
    }


def test_priority_thin_values(priority):
    """A value is thin at max(2, half the median count) or fewer; `other` never is."""
    accepted = (
        [_facts(domain="medical")] * 8
        + [_facts(domain="finance", problem="binary_classification")] * 6
        + [_facts(domain="education", problem="multiclass_classification", regime="grouped_non_iid")] * 2
        + [_facts(domain="other")]
    )
    thin = priority.thin_values(accepted)
    assert thin["domain"] == ["education"]
    assert thin["problem_type"] == ["multiclass_classification"]
    assert thin["regime"] == ["grouped_non_iid"]


def test_priority_score(priority):
    """Gap: a thin domain, problem type or regime; shape: 1,000 units, 5 features and mixed types or non-IID."""
    thin = {"domain": ["education"], "problem_type": [], "regime": ["grouped_non_iid"]}
    assert priority.score(_facts(), thin) == {
        "gap": 0,
        "gap_why": "no thin domain, problem type or regime",
        "shape": 1,
        "shape_why": "5,000 units, 10 features, categorical, iid",
    }
    assert priority.score(_facts(domain="education"), thin)["gap_why"] == "domain education"
    assert priority.score(_facts(regime="grouped_non_iid"), thin)["gap"] == 1
    # Numeric only: a good shape needs a grouped or temporal split instead.
    assert priority.score(_facts(non_numeric=()), thin)["shape"] == 0
    assert priority.score(_facts(non_numeric=(), regime="temporal_non_iid"), thin)["shape"] == 1
    assert priority.score(_facts(units=999), thin)["shape"] == 0
    assert priority.score(_facts(features=4), thin)["shape"] == 0


def test_priority_factors_on_the_working_copy(priority, capsys):
    """The command line measures a named record of the working copy against its accepted definitions."""
    root = REPO / "datasets" / "_dev" / "tabarena-v0pt2"
    if not (root / "airfoil_self_noise" / "README.md").is_file():
        pytest.skip("needs the working copy")
    where = ["--root", str(root), "--records", str(REPO / "curation" / "records")]
    assert priority.main(["airfoil_self_noise", *where]) == 0
    out = capsys.readouterr().out
    assert out.startswith("Thin among the ")
    assert "| `airfoil_self_noise` |" in out
    with pytest.raises(SystemExit, match="no folder for: no_such_record"):
        priority.main(["no_such_record", *where])


# --------------------------------------------------------------------------- clean_room
def _probe_input(clean_room, regime: str, grouping=None, time_on=None):
    df = pd.DataFrame({"x": range(10), "g": list("aabbccddee"), "y": [0.5] * 10})
    splits = {r: {f: ([0, 1], [2, 3]) for f in range(3)} for r in range(2)}
    return clean_room.dataset_io.ProbeInput(
        df=df,
        target="y",
        problem_type="regression",
        regime=regime,
        splits=splits,
        grouping=grouping,
        time_on=time_on,
        origin="definition",
    )


def test_task_markdown_holds_only_the_facts(clean_room):
    """task.md: target, problem type, size, regime with its column, splits, links; the sample is said."""
    data = _probe_input(clean_room, "grouped_non_iid", grouping=SimpleNamespace(on="g"))
    text = clean_room.task_markdown(data, ["https://example.org/data"], rows=1000, sampled=10)
    assert "- Target column: `y`" in text
    assert "- Problem type: regression" in text
    assert "1,000 rows x 3 columns" in text
    assert "grouped by `g` (whole groups are held out)" in text
    assert "2 repeats x 3 folds (6 train/test splits)" in text
    assert "random sample of 10 of the 1,000 rows (seed 0" in text
    assert "- https://example.org/data" in text
    temporal = clean_room.task_markdown(
        _probe_input(clean_room, "temporal_non_iid", time_on="x"), [], rows=10, sampled=None
    )
    assert "temporal on `x`" in temporal
    assert "6 test windows" in temporal
    assert "holds every row" in temporal


def test_source_links_drop_the_notes(clean_room, tmp_path):
    """The record's ``#`` note lines are our notes, so the clean room leaves them out."""
    _record(tmp_path, "ds", suggestion="Yes", source_links=["# canonical: the curator's note", "https://a.org/x"])
    assert clean_room.source_links("ds", tmp_path) == ["https://a.org/x"]
    assert clean_room.source_links("missing", tmp_path) == []


AIRFOIL_RAW = REPO / "local-data-warehouse" / "airfoil_self_noise" / "airfoil_self_noise.dat"


@pytest.mark.skipif(not AIRFOIL_RAW.exists(), reason="the raw files of airfoil_self_noise are not downloaded")
def test_clean_room_on_airfoil(clean_room, tmp_path):
    """The real definition: a sampled frame with the target, and a task.md without our notes."""
    out = tmp_path / "room"
    result = clean_room.write(
        "airfoil_self_noise",
        out,
        root=REPO / "datasets" / "_dev" / "tabarena-v0pt2",
        records=REPO / "curation" / "records",
        max_rows=500,
        built=False,
    )
    assert sorted(p.name for p in out.iterdir()) == ["data.parquet", "task.md"]
    df = pd.read_parquet(out / "data.parquet")
    assert len(df) == 500 == result["sampled"]
    assert "scaled-sound-pressure" in df.columns
    task = (out / "task.md").read_text()
    assert "random sample of 500 of the 1,503 rows" in task
    assert "grouped by `setup`" in task
    assert "https://doi.org/10.24432/C5VW2C" in task
    for note in ("wind tunnel", "wind-tunnel", "engineer", "airfoil_self_noise"):  # task summary, comments, name
        assert note not in task.lower()


# --------------------------------------------------------------------------- decision_register
KNOWLEDGE = {
    "references/leak_checks.md": """# Leaks

**LEAK-3 (Must).** A feature known only after the outcome is dropped.

**LEAK-4 (Should; narrows LEAK-3).** Scaling over all rows is noted, not dropped. See LEAK-9 for more.

```text
**LEAK-99 (Must).** An example inside a code fence defines nothing.
```

## Cases

| Rule | Dataset | Decision (date, curator) | Kind |
|---|---|---|---|
| LEAK-3 | fitness_club | retired, `Trivial` (2026-10-05, Lennart) | applied |
| CLEAN-4 | `case_ds` | kept with a note (2026-10-12) | exception |
""",
    "references/cleaning.md": "- **CLEAN-4 (Should).** Keep the raw codes.\n\n**TP-4 (Must).** Trivial needs proof.\n",
}


def _knowledge(tmp_path: Path) -> Path:
    root = tmp_path / "knowledge"
    for rel, text in KNOWLEDGE.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    return root


def test_rule_ids_defined(register, tmp_path):
    """Definitions at the start of a line count, mentions and fenced examples do not."""
    assert register.rule_ids_defined(_knowledge(tmp_path)) == {"LEAK-3", "LEAK-4", "CLEAN-4", "TP-4"}
    assert register.rule_ids_defined(tmp_path / "missing") == set()


def test_rule_strengths_and_exceptions_to_a_must(register, tmp_path):
    """The strength of each definition is read, and an exception to a plain Must is flagged."""
    knowledge = _knowledge(tmp_path)
    strengths = register.rule_strengths(knowledge)
    assert strengths == {"LEAK-3": "Must", "LEAK-4": "Should; narrows LEAK-3", "CLEAN-4": "Should", "TP-4": "Must"}
    decisions = register.collect(*_register_fixture(tmp_path))
    assert not [f for f in register.flags_for(decisions, strengths) if f.kind == "exception_to_must"]
    flagged = [
        f for f in register.flags_for(decisions, strengths | {"CLEAN-4": "Must"}) if f.kind == "exception_to_must"
    ]
    assert {f.key for f in flagged} == {"CLEAN-4"}
    assert not register._is_must("Must when strong, Should when weak")


def test_rule_ids_in_maps_the_legacy_task_probe_rules(register):
    """``task_probes.md rule N`` is TP-N, ranges and pairs included."""
    assert register.rule_ids_in("see task_probes.md rule 6 and LEAK-3") == ["LEAK-3", "TP-6"]
    assert register.rule_ids_in("task_probes.md rules 1-3") == ["TP-1", "TP-2", "TP-3"]
    assert register.rule_ids_in("`task_probes.md` rules 2 and 4") == ["TP-2", "TP-4"]
    assert register.rule_ids_in("no rule, LEAKY-3 and SEL-") == []


def test_parse_exception_lines(register):
    """An exception needs a Serves part after enough words of reason."""
    text = (
        "CC (2026-10-20, Lennart): kept.\n\n"
        "**Exception to CLEAN-4 (2026-10-20, Lennart):** the clinic records the raw codes the model would see\n"
        "at the desk. Serves P3: the use case needs them.\n\n"
        "**Exception to LEAK-4 (2026-10-21, Mustafa):** kept. Serves P2.\n\n"
        "**Exception to LEAK-3 and LEAK-4 (2026-10-22, Lennart):** the release documents the field as recorded "
        "at intake, before the outcome.\n"
    )
    good, short, missing = register.parse_exception_lines(text)
    assert (good.rule_ids, good.date, good.author, good.serves) == (["CLEAN-4"], "2026-10-20", "Lennart", "P3")
    assert good.problem is None
    assert short.words_before_serves == 1
    assert "fewer than" in short.problem
    assert missing.rule_ids == ["LEAK-3", "LEAK-4"]
    assert missing.serves is None
    assert "no 'Serves" in missing.problem
    assert register.parse_exception_lines("Exception to LEAK-4 in plain text.") == []


@pytest.mark.parametrize(
    ("head", "outcome"),
    [
        ("**No.** Reasons: simulated data", "exclude"),
        ("stays No, and tagged as forecasting", "exclude"),
        ("Retired (No (Retired); AHDS) from TabArena", "exclude"),
        ("Kept after the task-probe review (flag `no_spread`).", "keep"),
        ("Ship (review of the 2026-10-07 run).", "keep"),
        ("Leak fixed by deduplication, split stays IID.", "fix"),
        ("No `Multi-target` tag: one target.", "other"),
        ("This upload was tested during another audit (retired; details there).", "other"),
        ("new record to rebuild x, after that record was retired", "other"),
    ],
)
def test_outcome_keywords(register, head, outcome):
    """The keyword rules read the head; parentheticals cite other records and are left out."""
    assert register.outcome_of(head) == outcome


def _register_fixture(tmp_path: Path) -> tuple[Path, Path, Path]:
    records = tmp_path / "records"
    _record(
        records,
        "keep_scaled",
        suggestion="Yes",
        comments="CC (2026-10-01, Lennart): Kept: the features are min-max scaled over all rows, no strong leak.",
    )
    _record(
        records,
        "retired_scaled",
        suggestion="No (Retired)",
        decision_markers=["Data Quality Issue"],
        comments=(
            "**Assessment (AI, 2026-10-04):** I recommend retiring it.\n\n"
            "CC (2026-10-05, Lennart): retired for now. The release z-scored every feature over all patients."
        ),
    )
    _record(
        records,
        "trivial_out",
        suggestion="No (Retired)",
        comments="CC (2026-10-06, Lennart): Retired as trivial (flag `one_feature`).",
    )
    _record(
        records,
        "trivial_kept",
        suggestion="Yes",
        comments="CC (2026-10-06, Mustafa): Kept: not trivial, the single feature is below the models.",
    )
    for i, name in enumerate(("exc_a", "exc_b", "exc_c")):
        _record(
            records,
            name,
            suggestion="Yes",
            comments=(
                f"**Exception to CLEAN-4 (2026-10-2{i}, Lennart):** the clinic records the raw codes the model would "
                "see at the desk. Serves P3: the use case needs them."
            ),
        )
    _record(
        records,
        "exc_thin",
        suggestion="Yes",
        comments="**Exception to LEAK-4 (2026-10-23, Lennart):** kept anyway. Serves P2: fine.",
    )
    root = tmp_path / "copy"
    (root / "keep_scaled_1m").mkdir(parents=True)
    (root / "keep_scaled_1m" / "REVIEW.md").write_text(
        "# keep_scaled\n\n**Outcome:** added.\n\n**Issues for Lennart:**\n\n"
        "1. **Keep the target in decibels?** The source reports dB (LEAK-3).\n   More evidence here.\n\n"
        "2. Drop the duplicate rows. They are copies.\n\n**Record judgment:** valid.\n"
    )
    return records, root, _knowledge(tmp_path)


def test_collect_reads_the_three_sources(register, tmp_path):
    """Comments, REVIEW.md issues and Cases rows become decisions with their kinds, authors and rule IDs."""
    decisions = register.collect(*_register_fixture(tmp_path))
    kinds = {}
    for d in decisions:
        kinds[d.kind] = kinds.get(d.kind, 0) + 1
    assert kinds == {"cc": 4, "assessment": 1, "exception": 4, "open_issue": 2, "case": 2}
    issues = [d for d in decisions if d.kind == "open_issue"]
    assert [(d.dataset, d.text, d.rule_ids) for d in issues] == [
        ("keep_scaled", "Keep the target in decibels?", ["LEAK-3"]),
        ("keep_scaled", "Drop the duplicate rows.", []),
    ]
    assert issues[1].outcome == "fix"
    assert "duplicate rows" in issues[1].mechanisms
    retired = next(d for d in decisions if d.dataset == "retired_scaled" and d.kind == "cc")
    assert (retired.outcome, retired.author, retired.markers) == ("exclude", "Lennart", ["Data Quality Issue"])
    assert "scaling over all rows" in retired.reason_mechanisms
    assessment = next(d for d in decisions if d.kind == "assessment")
    assert (assessment.author, assessment.date, assessment.outcome) == ("AI", "2026-10-04", "exclude")
    cases = [d for d in decisions if d.kind == "case"]
    assert [(d.dataset, d.rule_ids, d.author, d.outcome, d.case_kind) for d in cases] == [
        ("fitness_club", ["LEAK-3"], "Lennart", "exclude", "applied"),
        ("case_ds", ["CLEAN-4"], "case table", "keep", "exception"),
    ]


def test_flags(register, tmp_path):
    """Drift for one curator's clean switch, opposite outcomes across curators, thin exceptions, amendments."""
    flags = register.flags_for(register.collect(*_register_fixture(tmp_path)))
    by_kind = {}
    for flag in flags:
        by_kind.setdefault(flag.kind, []).append(flag)
    drift = by_kind["drift"]
    assert [f.key for f in drift] == ["mechanism: scaling over all rows"]
    assert "keep up to 2026-10-01, exclude from 2026-10-05" in drift[0].message
    opposite = [f.key for f in by_kind["opposite_outcomes"]]
    assert opposite == ["mechanism: trivial"]  # only the retired side names `one_feature`
    pair = by_kind["opposite_outcomes"][0].pairs[0]
    assert {pair[0].dataset, pair[1].dataset} == {"trivial_kept", "trivial_out"}
    thin = by_kind["exception_without_reason"]
    assert [(f.key, f.decisions[0].dataset) for f in thin] == [("LEAK-4", "exc_thin")]
    amendment = by_kind["amendment_due"]
    assert [f.key for f in amendment] == ["CLEAN-4"]
    assert "on 4 datasets" in amendment[0].message  # three exception lines and one Cases row


def test_selection_keeps_flags_with_a_selected_decision(register, tmp_path):
    """``--since`` shows a flag only when a selected decision takes part; the pairs narrow to those."""
    decisions = register.collect(*_register_fixture(tmp_path))
    selected = register.selector("2026-10-06", None, None)
    kinds = {(f.kind, f.key) for f in register.select_flags(register.flags_for(decisions), selected)}
    assert ("drift", "mechanism: scaling over all rows") not in kinds
    assert ("opposite_outcomes", "mechanism: trivial") in kinds
    by_name = register.selector(None, {"exc_thin"}, None)
    flags = register.select_flags(register.flags_for(decisions), by_name)
    assert [f.kind for f in flags] == ["exception_without_reason"]
    by_rule = register.selector(None, None, "CLEAN-4")
    assert {d.dataset for d in decisions if by_rule(d)} == {"exc_a", "exc_b", "exc_c", "case_ds"}


def test_register_main(register, tmp_path, capsys):
    """The command line prints the register by rule and the flags, and writes the JSON."""
    records, root, knowledge = _register_fixture(tmp_path)
    out = tmp_path / "register.json"
    args = ["--records", str(records), "--root", str(root), "--knowledge", str(knowledge), "--json", str(out)]
    assert register.main(args) == 0
    text = capsys.readouterr().out
    assert "## By rule ID" in text
    assert "### CLEAN-4 (4)" in text
    assert "### 1. exception_without_reason: LEAK-4" in text
    data = json.loads(out.read_text())
    assert data["rule_ids_defined"] == ["CLEAN-4", "LEAK-3", "LEAK-4", "TP-4"]
    assert {f["kind"] for f in data["flags"]} == {
        "exception_without_reason",
        "drift",
        "opposite_outcomes",
        "amendment_due",
    }
    assert all("full" not in d for d in data["decisions"])
