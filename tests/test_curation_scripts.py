"""The curation scripts of the knowledge-data-foundry skill: coverage, priority factors, clean room, decision register.

The scripts live in the skill, not in the package, so they are imported from their files. They run here on small
records written to ``tmp_path``; the clean room's end-to-end test needs the raw files of ``airfoil_self_noise`` and
skips without them. The probes run on small generated frames, a task with a training weight (a claims rate over the
years insured) included.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest
from data_foundry.curation.record import CurationRecord
from data_foundry.curation.store import save_record
from data_foundry.schema import ScoringColumn
from data_foundry.v2 import get_dataset
from data_foundry.v2.metrics import Metric, score
from sklearn.metrics import mean_poisson_deviance

from tests.test_v2_dataset import DEFINITION, warehouse, write_definition  # noqa: F401 - the fixture is used by name

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


def test_priority_feature_type_counts(priority):
    """The README's type counts parse with and without an ordinal count and before any special features."""
    line = "<summary>Feature types: {}</summary>"
    assert priority.feature_type_counts(line.format("2 categorical, 0 string, 1 datetime")) == {
        "categorical": 2,
        "string": 0,
        "datetime": 1,
    }
    special = "7 categorical, 3 ordinal, 0 string, 0 datetime, smiles `SMILES`"
    counts = priority.feature_type_counts(line.format(special))
    assert counts == {"categorical": 7, "ordinal": 3, "string": 0, "datetime": 0}
    assert priority.feature_type_counts("no such line") is None


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


def test_prediction_point_line_takes_a_clause_or_a_sentence(clean_room):
    """A clause gets the lead-in; a whole sentence (airqo's) is kept, not prefixed a second time."""
    assert clean_room.prediction_point_line("the policy is quoted.") == (
        "- Prediction point: the prediction is made when the policy is quoted."
    )
    sentence = "The prediction is made for an hour after that hour has been recorded."
    assert clean_room.prediction_point_line(sentence) == (
        "- Prediction point: the prediction is made for an hour after that hour has been recorded."
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


def test_probe_input_drops_the_scoring_columns(clean_room):
    """The probes never see a scoring column as a feature; one that is also the group or time column stays."""
    df = pd.DataFrame({"y": [1.0, 2.0], "x": [0, 1], "era": ["a", "b"], "g": ["u", "v"]})
    scoring = [
        ScoringColumn(column="era", role="group", used_by="mean_group_pearsonr", description="the era"),
        ScoringColumn(column="g", role="group", used_by="par_k", description="the instance"),
    ]
    task = SimpleNamespace(target_column_name="y", group_on="g", time_on=None, scoring_columns=scoring)
    out, dropped = clean_room.dataset_io._without_scoring_columns(df, task)
    assert list(out.columns) == ["y", "x", "g"]
    assert dropped == ("era",)
    plain = SimpleNamespace(target_column_name="y", group_on=None, time_on=None)  # format 1: no scoring columns
    assert clean_room.dataset_io._without_scoring_columns(df, plain)[0] is df


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


def test_participant_markdown_adds_the_prediction_point_and_metric(clean_room):
    """The kit's task.md: the clean room's facts, the prediction point, the metric, the groups, the files."""
    data = _probe_input(clean_room, "grouped_non_iid", grouping=SimpleNamespace(on="g"))
    task = {
        "metric": {"name": "rmse", "prediction": "value", "params": {}, "greater_is_better": False},
        "grouping": {"prediction_unit": "row", "aggregation": None, "context": "none"},
        "scoring_columns": [],
    }
    text = clean_room.participant_markdown(data, ["https://example.org/data"], task, "the policy is quoted.")
    assert "- Prediction point: the prediction is made when the policy is quoted." in text
    assert "- Metric: `rmse` on a `value` prediction; lower is better." in text
    assert "The group column is not a feature." in text
    assert "holds every row" in text
    assert text.index("## Files") < text.index("## Source links")


def test_participant_kit_path_is_checked(clean_room, tmp_path):
    """The sandbox hook allows only paths with a participant_kit component, so the script refuses any other."""
    with pytest.raises(SystemExit, match="participant_kit"):
        clean_room.write_participant("x", tmp_path / "kit", root=tmp_path, records=tmp_path, prediction_point="now")


def test_participant_score_aggregates_per_group(clean_room, tmp_path):
    """score.py scores one prediction per group when the task says so, as the package's scorer does."""
    kit = tmp_path / "participant_kit"
    kit.mkdir()
    frame = pd.DataFrame({"g": list("aabbcc"), "x": range(6), "y": [1.0, 1.0, 2.0, 2.0, 4.0, 4.0]})
    frame.to_parquet(kit / "data.parquet")
    rows = [(0, 0, "train", i) for i in (0, 1)] + [(0, 0, "test", i) for i in (2, 3, 4, 5)]
    pd.DataFrame(rows, columns=["repeat", "fold", "side", "row"]).to_parquet(kit / "splits.parquet")
    grouping = {"on": "g", "labels": "per_group", "time_on": None, "prediction_unit": "group", "aggregation": "mean"}
    task = {
        "target": "y",
        "group_columns": ["g"],
        "grouping": {**grouping, "context": "none"},
        "metric": {"name": "rmse", "kind": "standard", "prediction": "value", "params": {}, "inputs": {}},
    }
    (kit / "task.json").write_text(json.dumps(task))
    (kit / "metrics.py").write_text(clean_room.METRICS_PY.read_text())
    (kit / "score.py").write_text(clean_room.SCORE_PY)
    spec = importlib.util.spec_from_file_location("kit_score", kit / "score.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.features() == ["x"]
    assert module.splits() == [("r0f0", [0, 1], [2, 3, 4, 5])]
    # Group b: mean 3.0 against 2.0; group c: mean 4.0 against 4.0. Two groups, not four rows.
    value = module.score(np.array([2.0, 2.0, 4.0, 4.0]), np.array([2.0, 4.0, 3.0, 5.0]), [2, 3, 4, 5])
    assert value == pytest.approx(np.sqrt((1.0**2 + 0.0**2) / 2))


HEPATITIS_RAW = REPO / "local-data-warehouse" / "hepatitis_c_prediction" / "hcvdat0.csv"


@pytest.mark.skipif(not HEPATITIS_RAW.exists(), reason="the raw files of hepatitis_c_prediction are not downloaded")
def test_participant_kit_on_hepatitis(clean_room, tmp_path):
    """The real definition: every row, the shipped splits, a metric without our notes, and a score.py that runs."""
    out = tmp_path / "participant_kit"
    clean_room.write_participant(
        "hepatitis_c_prediction",
        out,
        root=REPO / "datasets" / "_dev" / "tabarena-v0pt2",
        records=REPO / "curation" / "records",
        prediction_point="a laboratory physician reads a blood panel",
    )
    names = sorted(p.name for p in out.iterdir())
    assert names == ["data.parquet", "metrics.py", "score.py", "splits.parquet", "task.json", "task.md", "work"]
    task = json.loads((out / "task.json").read_text())
    assert task["metric"]["name"] == "log_loss"
    assert "reason" not in task["metric"]
    assert "origin" not in task["metric"]
    splits = pd.read_parquet(out / "splits.parquet")
    assert set(splits["side"]) == {"train", "test"}
    assert splits["row"].max() < len(pd.read_parquet(out / "data.parquet"))
    for note in ("donor rows", "round", "MET-2", "hepatitis_c_prediction"):  # curation comments, metric reason, name
        assert note not in (out / "task.md").read_text()
    run = subprocess.run([sys.executable, "-I", "score.py"], cwd=out, capture_output=True, text=True, check=True)
    assert run.stdout.startswith("r0f0: train ")


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


def _register_fixture(tmp_path: Path) -> tuple[Path, Path]:
    records = tmp_path / "records"
    _record(
        records,
        "keep_scaled",
        suggestion="Yes",
        comments="CC (2026-10-01, Lennart): Kept: the features are min-max scaled over all rows, no strong leak.",
        review=(
            "**Outcome:** added.\n\n**Issues for Lennart:**\n\n"
            "1. **Keep the target in decibels?** The source reports dB (LEAK-3).\n   More evidence here.\n\n"
            "2. Drop the duplicate rows. They are copies.\n\n**Record judgment:** valid."
        ),
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
    return records, _knowledge(tmp_path)


def test_collect_reads_the_three_sources(register, tmp_path):
    """Comments, the issues of a record's review and Cases rows become decisions with their kinds, authors and IDs."""
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
    records, knowledge = _register_fixture(tmp_path)
    out = tmp_path / "register.json"
    args = ["--records", str(records), "--knowledge", str(knowledge), "--json", str(out)]
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


@pytest.fixture(scope="module")
def task_probe():
    """curation_probes.task, imported through task_probes.py (which puts the probe library on the path).

    The task probes need LightGBM, which the CI environment does not install; the tests skip without it.
    """
    pytest.importorskip("lightgbm")
    return _import("task_probes").task


def test_task_probe_cap_keeps_the_newest_rows_of_a_temporal_train_side(task_probe):
    """A temporal train side keeps its newest rows; any other keeps random rows; a small side is kept whole."""
    rng = np.random.default_rng(0)
    train = np.arange(100, 1100)
    times = np.zeros(1100)
    times[train] = rng.permutation(1000)  # row order is not time order
    newest = task_probe.cap_train(train, 300, times, rng)
    assert len(newest) == 300
    assert list(newest) == sorted(newest)
    assert set(times[newest]) == set(range(700, 1000))
    sampled = task_probe.cap_train(train, 300, None, rng)
    assert len(sampled) == 300
    assert set(sampled) <= set(train)
    assert times[sampled].min() < 700  # random rows reach back in time
    assert task_probe.cap_train(train, 5_000, times, rng) is train


def test_task_probe_compares_the_best_family_with_the_dummy_on_the_declared_metric(task_probe):
    """The best family by the declared metric against the dummy, paired by split: a loss gives its relative gain, a
    score not; a split scored by only one of the two is left out (fremtpl2: `no_signal` from R^2 near 0.01 while the
    declared deviance shows a gain on every split).
    """
    loss = task_probe.vs_dummy(
        [{"metric": 0.60}, {"metric": 0.61}, {"metric": 0.59}],
        [{"metric": 0.62}, {"metric": 0.62}, {"metric": 0.61}],
        -1,
    )
    assert loss["beats_dummy_share"] == 1.0
    assert loss["gain_mean"] == pytest.approx(0.05 / 3)
    assert loss["relative_gain"] == pytest.approx((0.05 / 3) / (1.85 / 3))
    assert loss["gain_se"] > 0
    gini = task_probe.vs_dummy([{"metric": 0.12}, {"metric": None}], [{"metric": 0.0}, {"metric": 0.0}], 1)
    assert gini == {"gain_mean": pytest.approx(0.12), "gain_se": 0.0, "beats_dummy_share": 1.0}
    assert task_probe.vs_dummy([{"metric": None}], [{"metric": 0.5}], -1) is None


def test_task_probe_run_on_a_capped_temporal_task(task_probe):
    """A drifting temporal task capped below its train side: the keys are stable and the dummy uses every train row."""
    rng = np.random.default_rng(1)
    n = 1_200
    t = np.arange(n)
    x = rng.normal(size=n)
    y = (rng.random(n) < 1 / (1 + np.exp(-(x + 3 * t / n - 2)))).astype(int)  # the base rate drifts up
    df = pd.DataFrame({"t": t.astype(float), "x": x, "noise": rng.normal(size=n), "y": y})
    splits = [(np.arange(0, 800), np.arange(800, 1_000)), (np.arange(0, 1_000), np.arange(1_000, 1_200))]
    result = task_probe.run(df, "y", "binary_classification", splits, time_on="t", max_rows=300, n_jobs=1)
    assert {"scores", "best", "flags", "flag_rules", "per_split", "single_feature", "splits_probed"} <= set(result)
    assert {"dummy", "drift", "linear", "random_forest", "lightgbm", "single_feature"} <= set(result["scores"])
    assert result["splits_probed"] == 2
    full_share = y[:800].mean()  # the dummy predicts the whole train side's class share, not the capped rows'
    expected = -(y[800:1_000] * np.log(full_share) + (1 - y[800:1_000]) * np.log(1 - full_share)).mean()
    assert result["per_split"]["dummy_loss"][0] == pytest.approx(expected, abs=1e-4)


@pytest.fixture(scope="module")
def leak_probe():
    """curation_probes.leak, imported through leak_probes.py; it needs LightGBM, so the tests skip without it."""
    pytest.importorskip("lightgbm")
    return _import("leak_probes").leak


def test_leak_probe_written_decimals(leak_probe):
    """Decimals as written: trailing zeros do not count, interpolated values carry many, missing stays missing."""
    values = pd.Series([2.5, 3.0, 0.215, np.nan, 27.28571429, 0.001, 1234.5])
    got = leak_probe.written_decimals(values)
    assert got.isna().tolist() == [False, False, False, True, False, False, False]
    assert got.dropna().tolist() == [1, 0, 3, 8, 3, 1]


def test_leak_probe_straight_line_fills(leak_probe):
    """A run of interpolated cells and a single fine-step fill are found; a single round step is not."""
    values = pd.Series([5.0, 7.3, 8.2, 9.1, 10.0, 4.4, 1.0, 1.215, 1.43, 3.0, 1.0, 1.5, 2.0, 0.3])
    assert list(np.flatnonzero(leak_probe.straight_line_fills(values))) == [2, 3, 7]


def test_leak_probe_fill_counts_per_class(leak_probe):
    """In a class-sorted table, fills in one class's block are counted for that class only."""
    rng = np.random.default_rng(0)
    a = rng.normal(20, 5, 60).round(1)
    a[10:20] = np.linspace(a[9], a[20], 12)[1:-1]  # ten cells filled between rows 9 and 20
    raw = pd.DataFrame({"y": [0] * 30 + [1] * 30, "a": a, "b": rng.normal(size=60)})
    assert leak_probe.fill_counts(raw, "y") == {"a": {"0": 10, "1": 0}}


def test_leak_probe_run_scores_the_number_format(leak_probe):
    """One class written in whole numbers, the other to one decimal: the format alone gives the class away."""
    rng = np.random.default_rng(2)
    n = 400
    y = np.repeat([0, 1], n // 2)
    x = rng.normal(50, 10, n)
    x = np.where(y == 1, x.round(0), x.round(1) + 0.05 * (x.round(1) % 1 == 0))
    df = pd.DataFrame({"x": x, "noise": rng.normal(size=n).round(3), "y": y})
    idx = rng.permutation(n)
    splits = [(idx[:300], idx[300:]), (idx[100:], idx[:100])]
    result = leak_probe.run(df, "y", "binary_classification", splits, n_splits=2, n_jobs=1)
    assert result["format_alone"] > 0.95
    assert next(iter(result["format_single"])) == "x"


def test_leak_probe_run_leaves_out_aware_datetimes(leak_probe):
    """A timezone-aware datetime column (airqo's `created_at`) is not a LightGBM input, as a naive one is not."""
    rng = np.random.default_rng(3)
    n = 300
    df = pd.DataFrame(
        {
            "x": rng.normal(size=n),
            "w": rng.normal(size=n),
            "v": rng.normal(size=n),
            "naive": pd.date_range("2021-01-01", periods=n, freq="h"),
            "aware": pd.date_range("2021-01-01", periods=n, freq="h", tz="Africa/Nairobi"),
            "y": rng.integers(0, 2, n),
        }
    )
    splits = [(np.arange(200), np.arange(200, n))]
    result = leak_probe.run(df, "y", "binary_classification", splits, n_splits=1, n_jobs=1)
    assert result["features_probed"] == 3


# --------------------------------------------------------------------------- the training weight and probe 22
RATE_TASK = """    target = "rate"
    problem_type = "regression"
    metric = Metric.source(
        "mean_poisson_deviance",
        reference="https://example.org/eval",
        params={"min_prediction": 1e-4},
        inputs={"weight": "exposure"},
    )
    scoring_columns = (
        ScoringColumn(column="exposure", role="weight", used_by="mean_poisson_deviance", description="years insured"),
    )
    sample_weight = "exposure"
"""
RATE_CLEAN = """        df["exposure"] = (df["row_id"] % 12 + 1) / 12
        df["rate"] = df["y"] / df["exposure"]
        return drop_columns(df, ["row_id", "y"])"""


def _rate_toy(root: Path):
    """The dataset tests' toy definition as a claims rate: ``y`` claims over 1 to 12 months insured, the time insured
    its training weight and the metric's row weight.
    """
    body = DEFINITION.format(name="toy_ds", comment="x")
    for old, new in (
        (
            '    target = "y"\n    problem_type = "binary_classification"\n'
            '    metric = Metric.fallback(reason="the toy data is generated; it has no source metric")\n',
            RATE_TASK,
        ),
        ('        df["y"] = df["y"].map({0: "no", 1: "yes"})\n        return drop_columns(df, ["row_id"])', RATE_CLEAN),
        ("import AbstractCuratedDataset,", "import ScoringColumn, AbstractCuratedDataset,"),
    ):
        assert old in body
        body = body.replace(old, new)
    write_definition(root, body=body)
    return get_dataset(root, "toy_ds")


def _rate_frame(n: int = 500, seed: int = 0) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """Claims per year insured: counts over 1 to 12 months, the time insured the training weight; ``g`` groups of 5."""
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    exposure = rng.integers(1, 13, n) / 12
    claims = rng.poisson(0.4 * np.exp(0.5 * x) * exposure)
    colour = pd.Categorical(rng.choice(["red", "blue"], n))
    df = pd.DataFrame({"x": x, "colour": colour, "g": np.arange(n) // 5, "rate": claims / exposure})
    return df, exposure, claims


def _poisson_metric(exposure: np.ndarray) -> dict:
    """A claims rate's metric as the probe library takes it: the Poisson deviance weighted by the time insured."""
    spec = Metric.source(
        "mean_poisson_deviance", reference="x", params={"min_prediction": 1e-4}, inputs={"weight": "exposure"}
    )
    return {
        "name": "mean_poisson_deviance",
        "greater_is_better": False,
        "prediction": "value",
        "floor": 1e-4,
        "row_weight": "exposure",
        "score": lambda y_true, y_pred, rows: score(spec, y_true, y_pred, weight=exposure[rows]),
    }


@pytest.fixture(scope="module")
def group_probe():
    """curation_probes.groups, imported through group_probes.py; it needs LightGBM."""
    pytest.importorskip("lightgbm")
    return _import("group_probes").groups


def test_probe_input_carries_the_training_weight_and_the_metric(clean_room, tmp_path, warehouse):  # noqa: F811
    """`from_definition` and `from_container` give the definition's sample weight row by row, never as a feature,
    with the declared metric, its inputs and a scorer that weights the rows as the benchmark does.
    """
    del warehouse
    dataset_io = clean_room.dataset_io
    ds = _rate_toy(tmp_path / "datasets")
    plan = ds.make_splits()
    data = dataset_io.from_definition(ds, plan)
    exposure = plan.df["exposure"].to_numpy()
    assert data.weight_column == "exposure"
    np.testing.assert_array_equal(data.weights, exposure)
    assert "exposure" not in data.df.columns
    assert "exposure" not in data.feature_cols
    rows = data.flat_splits()[0][1]
    np.testing.assert_array_equal(data.metric_inputs(rows)["weight"], exposure[rows])
    metric = data.declared_metric()
    assert (metric["name"], metric["greater_is_better"], metric["floor"]) == ("mean_poisson_deviance", False, 1e-4)
    assert metric["row_weight"] == "exposure"
    y, pred = data.df["rate"].to_numpy()[rows], np.full(len(rows), 0.3)
    expected = mean_poisson_deviance(y, pred, sample_weight=exposure[rows])
    assert metric["score"](y, pred, rows) == pytest.approx(expected)
    assert score(data.metric, y, pred, **data.metric_inputs(rows)) == pytest.approx(expected)
    rebuilt = dataset_io.from_container(ds.to_container(), "rebuilt")
    assert rebuilt.weight_column == "exposure"
    np.testing.assert_array_equal(rebuilt.weights, exposure)


def test_probes_fit_with_the_training_weight(task_probe, leak_probe, group_probe, monkeypatch):
    """A claims rate weighted by the time insured: every model of the task, leak and group probes is fitted with the
    training rows' weights, and the dummy is the portfolio rate sum(N) / sum(v), not the mean of the rates.
    """
    df, exposure, claims = _rate_frame()
    fitted: list[bool] = []
    fit = task_probe.weights.fit

    def recording_fit(model, X, y, weight=None):
        fitted.append(weight is not None and len(weight) == len(X))
        return fit(model, X, y, weight)

    monkeypatch.setattr(task_probe.weights, "fit", recording_fit)
    idx = np.random.default_rng(1).permutation(len(df))
    train, test = np.sort(idx[:350]), np.sort(idx[350:])
    rows = df.drop(columns="g")
    result = task_probe.run(
        rows, "rate", "regression", [(train, test)], sample_weight=exposure, metric=_poisson_metric(exposure), n_jobs=1
    )
    rate, portfolio = df["rate"].to_numpy(), claims[train].sum() / exposure[train].sum()
    assert abs(rate[train].mean() - portfolio) > 0.01  # the unweighted mean is another dummy
    dummy = result["scores"]["dummy"]
    assert dummy["rmse_mean"] == pytest.approx(
        np.sqrt(np.average((rate[test] - portfolio) ** 2, weights=exposure[test]))
    )
    constant = np.full(len(test), portfolio)
    assert dummy["metric_mean"] == pytest.approx(
        mean_poisson_deviance(rate[test], constant, sample_weight=exposure[test])
    )
    assert dummy["at_floor_mean"] == 0.0
    assert {"metric_mean", "at_floor_mean"} <= set(result["scores"]["lightgbm"])
    assert result["weighted"]
    assert result["declared_metric"]["name"] == "mean_poisson_deviance"
    assert {"gain_mean", "gain_se", "beats_dummy_share", "relative_gain"} <= set(result["declared_metric"]["vs_dummy"])
    assert fitted
    assert all(fitted)  # the families and the single-feature fits
    fitted.clear()
    assert leak_probe.run(rows, "rate", "regression", [(train, test)], sample_weight=exposure, n_jobs=1)["weighted"]
    assert fitted
    assert all(fitted)
    fitted.clear()
    folds = [(np.flatnonzero(df["g"] % 3 != k), np.flatnonzero(df["g"] % 3 == k)) for k in range(3)]
    group_probe.run(df, "rate", "regression", ["g"], [folds], per_group_labels=False, n_jobs=1, sample_weight=exposure)
    assert fitted
    assert all(fitted)  # kNN takes no weight: `fit` is handed it and fits without it


def _motor_book(n: int = 3_000, seed: int = 0) -> tuple[pd.DataFrame, np.ndarray]:
    """A toy motor book scored as claims per year insured. Half the first claims cancel the policy, so the time
    insured carries the outcome. The earned premium (the annual premium times the time insured) encodes it; the
    quote-time risk score predicts it too, through the claims and the lapses of the riskier drivers.
    """
    rng = np.random.default_rng(seed)
    risk = rng.normal(size=n)
    rate = 1.5 * np.exp(0.5 * risk)  # claims per year
    first = rng.exponential(1 / rate)
    planned = rng.uniform(0.5, 1.0, n)
    lapse = np.where(rng.random(n) < 0.4 / (1 + np.exp(-2 * risk)), rng.uniform(0.2, 1, n) * planned, np.inf)
    end = np.minimum(planned, lapse)
    claimed = first < end
    cut = claimed & (rng.random(n) < 0.5)  # the claim cancels the policy
    exposure = np.maximum(np.where(cut, first, end), 0.02)
    claims = np.where(claimed, 1 + np.where(cut, 0, rng.poisson(rate * np.maximum(end - first, 0))), 0)
    earned = 400 * np.exp(0.5 * risk + rng.normal(0, 0.3, n)) * exposure
    region = pd.Categorical(rng.choice(["n", "s", "e", "w"], n))
    frame = pd.DataFrame({"risk": risk, "region": region, "earned_premium": earned, "rate": claims / exposure})
    return frame, exposure


def _thirds(n: int, seed: int) -> list[tuple[np.ndarray, np.ndarray]]:
    folds = np.array_split(np.random.default_rng(seed).permutation(n), 3)
    return [(np.sort(np.concatenate(folds[:k] + folds[k + 1 :])), np.sort(folds[k])) for k in range(3)]


def test_weight_proxy_flags_an_earned_premium(leak_probe, clean_room):
    """Probe 22 flags the earned premium, which stands in for the time insured and loses all its gain once the time
    insured is a feature. The quote-time risk score predicts the time insured too and reports its weight-mediated
    part, a smaller share of its gain (with the time insured, the earned premium gives the premium, and so the risk,
    back); whether it stays is the timing call the reading names (LEAK-41).
    """
    df, exposure = _motor_book()
    spec = Metric.source(
        "mean_poisson_deviance", reference="x", params={"min_prediction": 1e-4}, inputs={"weight": "exposure"}
    ).spec("regression")
    data = clean_room.dataset_io.ProbeInput(
        df=df,
        target="rate",
        problem_type="regression",
        regime="iid",
        splits={0: dict(enumerate(_thirds(len(df), 100)))},
        grouping=None,
        time_on=None,
        origin="definition",
        weights=exposure,
        weight_column="exposure",
        metric=spec,
        scoring=pd.DataFrame({"exposure": exposure}),
    )
    result = leak_probe.weight_proxy(
        data.df,
        data.target,
        data.problem_type,
        data.flat_splits(),
        data.weights,
        sample_weight=data.weights,
        metric=data.declared_metric(),
        weight_name="exposure",
        seeds=(0, 1),
        top=3,
        n_estimators=50,
        fit_params={"objective": "poisson"},
        n_jobs=1,
        report=False,
    )
    model = result["weight_model"]
    assert next(iter(model["top_features"])) == "earned_premium"
    assert model["top_features"]["risk"] > 0.1  # the risk score predicts the time insured
    assert result["leak_reference"]["mean"] == pytest.approx(result["honest"]["mean"] - result["with_weight"]["mean"])
    assert result["leak_reference"]["mean"] > 0  # lower is better: the weight as a feature lowers the deviance
    assert "earned_premium" in result["flags"]
    checked = result["features_checked"]
    risk = checked["risk"]["weight_mediated"]
    assert risk["runs"] == 6
    assert np.isfinite(risk["mean"])
    assert np.isfinite(risk["sd"])
    assert checked["earned_premium"]["mediated_share"] > 0.9
    assert checked["risk"]["mediated_share"] < checked["earned_premium"]["mediated_share"] - 0.05
    assert "timing call (LEAK-41)" in result["reading"]
    lines = leak_probe.weight_proxy_lines(result)
    assert any(line.lstrip().startswith("earned_premium") and line.endswith("flag") for line in lines)
    json.dumps(result)  # what --out writes


def test_weight_proxy_scores_one_over_the_weight_for_a_gini(leak_probe):
    """For a Gini metric (higher is better), a ranking metric, probe 22 scores 1/weight alone as the prediction, and
    keeps the gains in the metric's direction.
    """
    df, exposure = _motor_book(n=900, seed=1)
    spec = Metric.source("ordered_lorenz_gini", reference="x", params={"per_unit": True}, inputs={"weight": "exposure"})
    metric = {
        "name": "ordered_lorenz_gini",
        "greater_is_better": True,
        "prediction": "value",
        "gini": True,
        "score": lambda y_true, y_pred, rows: score(spec, y_true, y_pred, weight=exposure[rows]),
    }
    train, test = _thirds(len(df), 7)[0]
    result = leak_probe.weight_proxy(
        df,
        "rate",
        "regression",
        [(train, test)],
        exposure,
        metric=metric,
        seeds=(0,),
        top=1,
        n_estimators=30,
        n_jobs=1,
        report=False,
    )
    rate = df["rate"].to_numpy()
    inverse = score(spec, rate[test], 1 / exposure[test], weight=exposure[test])
    assert result["weight_alone"]["as"] == "1/weight"
    assert result["weight_alone"]["mean"] == pytest.approx(inverse)
    assert result["greater_is_better"]
    assert result["leak_reference"]["mean"] == pytest.approx(result["with_weight"]["mean"] - result["honest"]["mean"])
    lines = leak_probe.weight_proxy_lines(result)
    assert any(line.startswith("  1/weight alone as the prediction:") for line in lines)
    assert not any("ceiling" in line for line in lines)


def test_weight_proxy_fits_the_target_on_the_weight_alone_for_a_deviance(leak_probe):
    """For a level-sensitive metric (a Poisson deviance) probe 22 scores a fit of the target on the weight alone, with
    the fits' own objective, not 1/weight as the prediction (X2, LEAK-41). In the toy book a claim can cut the time
    insured short, so the weight alone beats the weighted constant.
    """
    df, exposure = _motor_book(n=1_500, seed=2)
    result = leak_probe.weight_proxy(
        df,
        "rate",
        "regression",
        _thirds(len(df), 3),
        exposure,
        sample_weight=exposure,
        metric=_poisson_metric(exposure),
        weight_name="exposure",
        seeds=(0, 1),
        top=1,
        n_estimators=50,
        fit_params={"objective": "poisson"},
        n_jobs=1,
        report=False,
    )
    alone = result["weight_alone"]
    assert alone["as"] == "fit"
    assert alone["runs"] == 6  # every split and seed
    assert not result["greater_is_better"]
    assert alone["mean"] < result["constant"]["mean"]  # lower is better: the weight alone carries the outcome
    lines = leak_probe.weight_proxy_lines(result)
    fitted = [
        line for line in lines if line.startswith("  a fit of the target on the weight alone (objective poisson)")
    ]
    assert len(fitted) == 1
    assert "the weighted constant's" in fitted[0]
    assert not any("ceiling" in line for line in lines)


def test_weight_proxy_fits_a_gini_scored_rate_with_its_actuarial_objective(leak_probe):
    """Under a metric that is no deviance (a Gini), probe 22's default fit of a weighted rate is actuarial: Poisson
    when the rate times the weight is a whole count, Tweedie at power 1.5 for a cost, L2 without a training weight
    (pricing_game_2016_french_fleet: its two arms had both been L2, 2026-11-06).
    """
    del leak_probe  # the fixture skips without LightGBM
    script = _import("leak_probes")
    gini = {"name": "normalized_weighted_gini", "params": {}}
    weight = np.array([0.5, 1.0, 0.25, 1.0])
    counts = np.array([1.0, 0.0, 1.0, 2.0]) / weight
    costs = np.array([120.5, 0.0, 33.3, 0.0]) / weight
    assert script.fit_params("metric", gini, counts, weight) == {"objective": "poisson"}
    assert script.fit_params("metric", gini, costs, weight) == {"objective": "tweedie", "tweedie_variance_power": 1.5}
    assert script.fit_params("metric", gini, costs, None) is None
    assert script.fit_params("metric", gini, -costs, weight) is None
    assert script.fit_params("l2", gini, costs, weight) is None
    poisson = {"name": "mean_poisson_deviance", "params": {"min_prediction": 1e-4}}
    assert script.fit_params("metric", poisson) == {"objective": "poisson"}
    tweedie = {"name": "mean_tweedie_deviance", "params": {"power": 1.8, "min_prediction": 1e-4}}
    expected = {"objective": "tweedie", "tweedie_variance_power": 1.8}
    assert script.fit_params("metric", tweedie, costs, weight) == expected


def test_leak_probes_command_runs_the_weight_proxy(leak_probe, tmp_path, warehouse, capsys):  # noqa: F811
    """`leak_probes.py --weight-proxy` reads the task's sample weight and metric from the definition and, by default,
    fits a Poisson deviance's rate with the Poisson objective; `--objective l2` asks for the L2 fit.
    """
    del warehouse, leak_probe  # the fixture skips without LightGBM
    root = tmp_path / "datasets"
    _rate_toy(root)
    out = tmp_path / "out"
    script = _import("leak_probes")
    argv = ["toy_ds", "--root", str(root), "--weight-proxy", "--splits", "1", "--seeds", "2", "--n-jobs", "1"]
    assert script.main([*argv, "--out", str(out)]) == 0
    result = json.loads((out / "toy_ds.json").read_text())["weight_proxy"]
    assert (result["weight"], result["metric"], result["objective"]) == ("exposure", "mean_poisson_deviance", "poisson")
    assert result["metric_row_weight"] == "exposure"
    assert result["trained_with_sample_weight"]
    printed = capsys.readouterr().out
    assert "weight proxy (probe 22) of `exposure`" in printed
    assert "run again with --objective l2" in printed
    assert script.main([*argv, "--objective", "l2", "--out", str(out)]) == 0
    assert json.loads((out / "toy_ds.json").read_text())["weight_proxy"]["objective"] == "L2"


# --------------------------------------------------------------------------- probe 23: the leak tests of a forced split
def _stacked_book(*, shock_sd: float, unit_sd: float = 0.0, units: int = 300, seed: int = 0) -> pd.DataFrame:
    """Units seen once a year over 2001 to 2005, stacked: the target is a row feature, a static attribute of the unit,
    a shock of the year shared by every unit (``shock_sd``) and an effect of the unit (``unit_sd``), plus noise.
    """
    rng = np.random.default_rng(seed)
    years = np.arange(2001, 2006)
    unit = np.repeat(np.arange(units), len(years))
    year = np.tile(years, units)
    attribute = rng.normal(size=units)[unit]
    x = rng.normal(size=len(unit))
    shock = rng.normal(0, shock_sd, len(years))[year - years[0]] if shock_sd else 0.0
    effect = rng.normal(0, unit_sd, units)[unit] if unit_sd else 0.0
    y = x + 0.5 * attribute + shock + effect + rng.normal(size=len(unit))
    return pd.DataFrame({"unit": unit, "year": year, "x": x, "attribute": attribute, "y": y})


def _by_unit(frame: pd.DataFrame, repeats: int = 2) -> list[tuple[np.ndarray, np.ndarray]]:
    """Three folds grouped by unit, ``repeats`` times: the forced grouped split of stacked periods."""
    out = []
    for r in range(repeats):
        fold = np.random.default_rng(10 + r).permutation(frame["unit"].max() + 1)[frame["unit"].to_numpy()] % 3
        out += [(np.flatnonzero(fold != k), np.flatnonzero(fold == k)) for k in range(3)]
    return out


@pytest.mark.parametrize(("shock_sd", "flagged"), [(1.0, True), (0.0, False)])
def test_period_outcome_flags_a_shock_of_the_period_shared_across_the_split(leak_probe, shock_sd, flagged):
    """Probe 23 (a): a shift of the target shared by every row of a year reaches a test row through the training rows
    of its year, when the split is grouped by unit over stacked years; a model trained without that year's rows loses
    it. Without such a shift the year's own rows gain nothing above noise.
    """
    frame = _stacked_book(shock_sd=shock_sd)
    codes, labels, kind = leak_probe.outcome_periods(frame["year"])
    assert (labels, kind) == (["2001", "2002", "2003", "2004", "2005"], "yearly")
    result = leak_probe.period_outcome(
        frame,
        "y",
        "regression",
        _by_unit(frame),
        codes,
        labels=labels,
        group_cols=["unit"],
        period_name="year",
        period_kind=kind,
        seeds=(0,),
        n_estimators=60,
        n_jobs=1,
        report=False,
    )
    assert result["splits"] == 6
    assert set(result["per_period"]) == set(labels)
    assert bool(result["flags"]) is flagged
    if flagged:
        assert result["flags"] == ["pooled", "within"]
        assert result["pooled"]["mean"] > 0.05
        assert result["pooled"]["positive"] == 6
    else:
        assert abs(result["pooled"]["mean"]) < 0.02
    lines = leak_probe.period_outcome_lines(result)
    assert lines[0].startswith("period outcome (probe 23) on `year` (yearly, 5 periods: 2001, 2002")
    assert "SPLIT-8" in lines[-1]
    json.dumps(result)  # what --out writes


def test_shared_units_flags_a_unit_on_both_sides_of_a_forced_split(leak_probe):
    """Probe 23 (b): with a random split of stacked years, a unit's other years sit in training, found by the exact
    profile of the inputs without the year, and a lookup of their target gains above noise. Grouped by unit, no test
    row's unit is in training, by the group column or by its profile, and no lookup is fitted.
    """
    frame = _stacked_book(shock_sd=0.0, unit_sd=1.0, units=400).drop(columns="x")
    rows = np.random.default_rng(1).permutation(len(frame))
    by_row = [(np.sort(np.setdiff1d(rows, part)), np.sort(part)) for part in np.array_split(rows, 3)]
    kwargs = {"group_cols": ["unit"], "without": "year", "seeds": (0, 1), "n_estimators": 60, "n_jobs": 1}
    random = leak_probe.shared_units(frame, "y", "regression", by_row, report=False, **kwargs)
    profile, other_years = "the exact profile of the 2 model inputs", "the exact profile without `year`"
    assert random["units"][profile]["matched"] == 0.0  # one row per unit and year
    assert random["units"][profile]["lookup_gain"] is None
    assert random["units"][other_years]["matched"] > 0.9
    assert random["flags"] == [other_years]
    grouped = leak_probe.shared_units(
        frame, "y", "regression", _by_unit(frame, repeats=1), unit_cols=["unit"], report=False, **kwargs
    )
    assert {unit["matched"] for unit in grouped["units"].values()} == {0.0}
    assert grouped["flags"] == []
    assert all(unit["lookup_gain"] is None for unit in grouped["units"].values())
    assert "`unit`: 0.0% of the test rows of 3 splits (0) have" in "\n".join(leak_probe.shared_units_lines(grouped))


def _fleets(*, twins: int = 0, groups: int = 600, seed: int = 0) -> pd.DataFrame:
    """Fleets of 1 to 6 vehicles: every vehicle of a fleet has the fleet's classes (``a``, ``b``, ``c`` on a coarse
    grid, so some fleets share them by chance) and its claim level. With ``twins``, that many fleets are a copy of
    another: one client under two contract numbers, with its classes and its level.
    """
    rng = np.random.default_rng(seed)
    a, b, c = (rng.integers(0, 20, groups) for _ in range(3))
    level = rng.normal(0, 1, groups)
    first = np.arange(0, 2 * twins, 2)
    a[first + 1], b[first + 1], c[first + 1], level[first + 1] = a[first], b[first], c[first], level[first]
    g = np.repeat(np.arange(groups), rng.integers(1, 7, groups))
    y = 0.05 * a[g] + level[g] + rng.normal(0, 0.5, len(g))
    return pd.DataFrame({"g": g, "a": a[g], "b": b[g], "c": c[g], "y": y})


@pytest.mark.parametrize(("twins", "flagged"), [(0, False), (150, True)])
def test_shared_units_on_a_grouped_split_reads_no_group_of_its_own(leak_probe, twins, flagged):
    """Probe 23 (b) on fleets split by contract: the vehicles of a fleet repeat their profile and share its claim
    level, but no level crosses fleets, so a lookup of the exact profile gains nothing (the training side's lookup is
    drawn by contract and never reads the row's own fleet, as a test row's never does). One client under two contract
    numbers is a shared unit across the split, and its lookup gains on the test rows that have one.
    """
    frame = _fleets(twins=twins)
    result = leak_probe.shared_units(
        frame,
        "y",
        "regression",
        _by_unit(frame.rename(columns={"g": "unit"})),
        unit_cols=["g"],
        group_cols=["g"],
        seeds=(0, 1),
        n_estimators=60,
        n_jobs=1,
        report=False,
    )
    assert result["lookup_folds"] == "by group"
    assert result["units"]["`g`"]["matched"] == 0.0
    profile = result["units"]["the exact profile of the 3 model inputs"]
    assert profile["matched"] > 0.03  # fleets that share their classes by chance, or twins
    assert bool(result["flags"]) is flagged
    assert abs(profile["change_without_lookup"]["mean"]) < 0.02  # the rows without a lookup keep their score
    if flagged:
        assert profile["gain_with_lookup"]["mean"] > 0.05
    line = next(x for x in leak_probe.shared_units_lines(result) if "the exact profile" in x)
    assert "on the test rows with one, changes the rest by" in line


def test_lookup_folds_by_group_never_read_a_rows_own_group(leak_probe):
    """The training side's out-of-fold lookup: drawn by group, a fleet whose profile no other fleet has gets no
    lookup; drawn by row, it reads its own fleet's other vehicles (the artefact of 2026-11-08 on
    pricing_game_2016_french_fleet).
    """
    groups = np.repeat(np.arange(200), 4)
    units = groups.copy()  # each fleet's profile is its own
    values = np.random.default_rng(0).normal(size=(len(units), 1))
    tr, te = np.arange(600), np.arange(600, 800)
    on_tr, on_te = leak_probe._lookup(units, values, np.ones(len(units)), tr, tr, te, np.random.default_rng(0), groups)
    assert np.isnan(on_tr).all()
    assert np.isnan(on_te).all()
    by_row, _ = leak_probe._lookup(units, values, np.ones(len(units)), tr, tr, te, np.random.default_rng(0))
    assert np.isfinite(by_row).mean() > 0.9


def test_outcome_periods_and_period_columns(leak_probe):
    """The periods of probe 23: dates cut at the coarsest calendar period with three or more, many years merged into
    runs of consecutive years, a category's own order kept; the period column found by dates, then years (fewest values
    first), then by name, never from a word inside a longer name.
    """
    dates = pd.Series(pd.to_datetime(["2011-03-01", "2012-07-15", "2013-01-02", "2013-11-30"]))
    codes, labels, kind = leak_probe.outcome_periods(dates)
    assert (list(codes), labels, kind) == ([0, 1, 2, 2], ["2011", "2012", "2013"], "yearly")
    codes, labels, kind = leak_probe.outcome_periods(np.repeat(np.arange(1990, 2020), 10), max_periods=6)
    assert len(labels) == 6
    assert labels[0] == "1990 to 1994"
    assert kind == "yearly, merged into 6 runs"
    assert list(np.unique(codes)) == list(range(6))
    months = pd.Series(pd.Categorical(["mar", "jan", "feb", "jan"], categories=["jan", "feb", "mar"], ordered=True))
    assert leak_probe.outcome_periods(months)[1] == ["jan", "feb", "mar"]
    with pytest.raises(ValueError, match="one period"):
        leak_probe.outcome_periods([2020] * 5)
    frame = pd.DataFrame(
        {
            "Model_Year": np.arange(1980, 2000).repeat(3),
            "Calendar_Year": np.tile([2005, 2006, 2007], 20),
            "AMT_REQ_CREDIT_BUREAU_YEAR": np.arange(60) % 5,
            "month": np.arange(60) % 3,
            "start": pd.date_range("2020-01-01", periods=60, freq="W"),
            "y": np.arange(60),
        }
    )
    found = leak_probe.period_columns(frame, exclude=["y"])
    assert [c for c, _ in found] == ["start", "Calendar_Year", "Model_Year", "month"]
    assert [why for _, why in found][:2] == ["dates", "years"]


def test_leak_probes_command_runs_the_forced_split_tests(leak_probe, tmp_path, warehouse, capsys):  # noqa: F811
    """`leak_probes.py --forced-split` runs probe 23 on a split tagged forced from temporal, on the year column it
    finds, and says why it does not run on any other split; the default run of a forced split ends with it.
    """
    del warehouse, leak_probe  # the fixture skips without LightGBM
    root = tmp_path / "datasets"
    body = DEFINITION.format(name="toy_ds", comment="x")
    old = '        df["y"] = df["y"].map({0: "no", 1: "yes"})\n'
    assert old in body
    body = body.replace(old, old + '        df["year"] = 2001 + df["row_id"] % 4\n')
    write_definition(
        root, body=body.replace('    target = "y"\n', '    data_tags = ("ForcedIIDFromTemporal",)\n    target = "y"\n')
    )
    script = _import("leak_probes")
    out = tmp_path / "out"
    argv = ["toy_ds", "--root", str(root), "--forced-split", "--forced-splits", "2", "--seeds", "1", "--n-jobs", "1"]
    assert script.main([*argv, "--out", str(out)]) == 0
    result = json.loads((out / "toy_ds.json").read_text())["forced_split"]
    assert result["tags"] == ["ForcedIIDFromTemporal"]
    assert result["period_outcome"]["period"] == "year"
    assert result["period_outcome"]["splits"] == 2
    assert "the exact profile without `year`" in result["shared_units"]["units"]
    printed = capsys.readouterr().out
    assert "period outcome (probe 23): the periods of `year` (years)" in printed
    assert "shared units (probe 23)" in printed
    default = [a for a in argv if a != "--forced-split"]
    assert script.main([*default, "--splits", "1", "--max-single-features", "2", "--out", str(out)]) == 0
    result = json.loads((out / "toy_ds.json").read_text())
    assert "all_features" in result
    assert result["forced_split"]["tags"] == ["ForcedIIDFromTemporal"]
    assert "period outcome (probe 23) on `year`" in capsys.readouterr().out
    write_definition(root)
    assert script.main(argv) == 0
    assert "forced split (probe 23): not run (the split is not tagged" in capsys.readouterr().out


def test_clean_rooms_name_the_training_weight(clean_room, tmp_path, warehouse):  # noqa: F811
    """The participant kit's task.json and task.md name the sample weight, which ships in scoring.parquet; the blind
    reviewer's clean room ships it as the last column of data.parquet, labelled in task.md.
    """
    del warehouse
    root, records = tmp_path / "datasets", tmp_path / "records"
    _rate_toy(root)
    kit = tmp_path / "participant_kit"
    clean_room.write_participant("toy_ds", kit, root=root, records=records, prediction_point="the policy is quoted")
    task = json.loads((kit / "task.json").read_text())
    assert task["sample_weight"] == "exposure"
    assert task["scoring_columns"] == ["exposure"]
    line = "- Training weight: `exposure`, in `scoring.parquet`; fit models with it as the row weight."
    assert line in (kit / "task.md").read_text()
    assert "exposure" in pd.read_parquet(kit / "scoring.parquet").columns
    assert "exposure" not in pd.read_parquet(kit / "data.parquet").columns
    room = tmp_path / "room"
    clean_room.write("toy_ds", room, root=root, records=records, max_rows=10_000, built=False)
    assert list(pd.read_parquet(room / "data.parquet").columns)[-1] == "exposure"
    text = (room / "task.md").read_text()
    assert "- Training weight: `exposure`, the task's training weight, not a feature" in text
    assert "x 4 columns (target and training weight included)" in text


@pytest.fixture(scope="module")
def dtype_probe():
    """curation_probes.dtypes, imported through dtype_probes.py."""
    pytest.importorskip("joblib")
    return _import("dtype_probes").dtypes


def _flags(table: pd.DataFrame) -> dict[str, list[str]]:
    return dict(zip(table["column"], table["flags"], strict=True))


def test_dtype_probe_flags_a_count_typed_categorical(dtype_probe):
    """bank_marketing's case: a count typed categorical, named a count by the codebook and shaped like one."""
    rng = np.random.default_rng(0)
    n = 2_000
    df = pd.DataFrame(
        {
            "campaign": pd.Categorical(np.minimum(rng.geometric(0.35, n), 40)),
            "city": pd.Categorical(rng.choice([3073, 3046, 6056, 98103], n)),
            "job": pd.Categorical(rng.choice(["admin.", "services", "retired"], n)),
            "num_children": pd.Categorical(rng.choice(["0", "1", "2", "3", ".b"], n)),
            "flag_n": pd.Categorical(rng.choice([0, 1], n)),
            "balance": rng.normal(1_000, 300, n).round(),
            "zip_code": rng.choice([10115, 20095, 80331], n),
            "ward_best": rng.integers(1, 130, n).astype(float),
            "y": rng.integers(0, 2, n),
        }
    )
    codebook = {
        "campaign": {"type": "Integer", "description": "number of contacts performed during this campaign"},
        "zip_code": {"type": "Categorical", "description": None},
    }
    table = dtype_probe.column_table(df, exclude=["y"], codebook=codebook)
    flags = _flags(table)
    assert flags["campaign"] == ["quantity_words", "codebook_numeric", "count_like"]
    assert flags["city"] == ["numeric_levels"]
    assert flags["job"] == []
    assert flags["balance"] == []
    assert flags["flag_n"] == []
    assert flags["num_children"] == ["quantity_words"]  # a count with a proxy missing code among its levels
    assert table.set_index("column").loc["num_children", "other_levels"] == [".b"]
    assert flags["zip_code"] == ["codebook_categorical", "code_name"]
    assert flags["ward_best"] == ["code_name"]  # a ward number within its municipality (GitHub issue #48)
    assert "y" not in flags
    assert list(dtype_probe.flagged(table)["column"]) == ["campaign", "num_children", "zip_code", "ward_best", "city"]


def test_dtype_probe_flagged_with_nothing_flagged(dtype_probe):
    """No flag gives an empty table, not the rows back (pandas adopts the index of a Series set on an empty frame)."""
    table = dtype_probe.column_table(pd.DataFrame({"a": [1.5, 2.5, 3.5], "b": pd.Categorical(["x", "y", "x"])}))
    assert dtype_probe.flagged(table).empty


def test_dtype_probe_reads_the_uci_and_openml_codebooks(dtype_probe):
    """UCI's variable table, its numbered free text when the table has no names, and OpenML's feature list."""
    uci = {"data": {"variables": [{"name": "campaign", "type": "Integer", "description": "number of contacts"}]}}
    assert dtype_probe.codebook_from_uci(uci) == {"campaign": {"type": "Integer", "description": "number of contacts"}}
    info = "41 molecular descriptors:\n25) B03[C-Cl]: Presence/absence of C - Cl\n26) N-073: Ar2NH / Ar3N / R..N..R\n"
    unnamed = {"data": {"variables": [{"name": " ", "type": " "}], "additional_info": {"variable_info": info}}}
    book = dtype_probe.codebook_from_uci(unnamed)
    assert book["N-073"] == {"type": None, "description": "Ar2NH / Ar3N / R..N..R"}
    assert dtype_probe.match_codebook(["N073_chemical_substructure", "nN"], book) == {
        "N073_chemical_substructure": book["N-073"]
    }
    day = {"day": {"type": "Categorical", "description": "day of the week"}}
    assert dtype_probe.match_codebook(["days_since_prev_obs"], day) == {}  # a prefix only up to a separator
    assert dtype_probe.match_codebook(["day_name"], day) == {"day_name": day["day"]}
    openml = {"data_features": {"feature": [{"name": "V13", "data_type": "numeric"}]}}
    assert dtype_probe.codebook_from_openml(openml) == {"V13": {"type": "numeric", "description": None}}
    assert dtype_probe.codebook_api_url("https://archive.ics.uci.edu/dataset/222/bank+marketing").endswith("id=222")
    assert dtype_probe.codebook_api_url("https://www.openml.org/search?type=data&id=1461").endswith("/1461")
    assert dtype_probe.codebook_api_url("https://www.kaggle.com/c/porto-seguro") is None


def test_dtype_probe_flags_scales_and_open_ends(dtype_probe):
    """Bands and open ends look like a scale; an ordered category raises only its open end; colours raise nothing."""
    df = pd.DataFrame(
        {
            "experience": pd.Categorical(["<1", "1", "2", ">20", "3"]),
            "bar": pd.Categorical(["never", "less1", "1~3", "4~8", "gt8"]),
            "quality": pd.Categorical(["Ex", "Gd", "TA", "Fa", "Po"]),
            "colour": pd.Categorical(["red", "blue", "green", "red", "blue"]),
            "mi": pd.Categorical(
                ["0", "1", "2", "3 or more", "1"], categories=["0", "1", "2", "3 or more"], ordered=True
            ),
        }
    )
    flags = _flags(dtype_probe.column_table(df))
    assert flags["experience"][:2] == ["ordinal_like", "open_end"]
    assert flags["bar"][:2] == ["ordinal_like", "open_end"]
    assert flags["quality"] == ["ordinal_like"]
    assert flags["colour"] == []
    assert flags["mi"] == ["open_end"]
