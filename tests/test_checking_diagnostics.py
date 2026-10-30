"""Behavioral checks for release-boundary rates and exact split contamination."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude/skills/knowledge-data-foundry/scripts"
sys.path.insert(0, str(SCRIPTS.parents[1] / "knowledge-curation/scripts"))

from curation_probes import (  # noqa: E402 - resolve the skill library before importing it
    duplicate_contamination as copies,
    label_maturity as maturity,
)


def _load_cli(name):
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(f"diagnostic_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_delayed_events_expose_release_boundary_suppression():
    """A missing-positive tail has a low recent rate and recovers behind a buffer."""
    dates = np.repeat(pd.date_range("2020-01-01", periods=10, tz="UTC"), 4)
    labels = np.tile([1, 0, 0, 0], 10)
    labels[-8:] = 0
    result = maturity.run(
        dates,
        labels,
        reference_start="2020-01-01",
        reference_end="2020-01-09",
        windows=[2, None],
        buffers=[0, 2],
        min_rate_ratio=0.9,
    )
    assert len(result["grid"]) == 4
    assert result["grid"][0]["recent"]["rows"] == 8
    assert result["grid"][0]["rate_ratio"] == 0
    assert result["grid"][0]["meets_rate_criterion"] is False
    assert result["grid"][2]["rate_ratio"] == 1
    assert result["grid"][2]["meets_rate_criterion"] is True
    assert result["grid"][1]["reference_overlap"] is True
    assert "mature" not in result


def test_reference_stability_and_empty_or_zero_event_windows():
    """References retain monthly counts; undefined rate ratios are not passes."""
    result = maturity.run(
        ["2020-01-01", "2020-01-02", "2020-02-01"],
        [0, 0, 1],
        reference_start="2020-01-01",
        reference_end="2020-02-01",
        windows=[1],
        buffers=[0, 100],
        min_rate_ratio=0.9,
    )
    assert result["reference"]["events"] == 0
    assert result["reference_months"][0]["rows"] == 2
    assert result["grid"][0]["rate_ratio"] is None
    assert result["grid"][1]["recent"]["rows"] == 0
    assert result["grid"][1]["meets_rate_criterion"] is None
    json.dumps(result, allow_nan=False)


def test_boundaries_use_utc_calendar_days_and_exclusive_ends():
    """Timezone conversion and exact cutoffs cannot move a row to both windows."""
    result = maturity.run(
        pd.to_datetime(["2020-01-01T23:00:00-02:00", "2020-01-02T23:00:00-02:00"], utc=True),
        [1, 0],
        reference_start="2020-01-02",
        reference_end="2020-01-03",
        windows=[1],
        buffers=[0],
    )
    assert result["reference"]["events"] == 1
    assert result["grid"][0]["recent"]["events"] == 0
    assert result["grid"][0]["reference_overlap"] is False


@pytest.mark.parametrize(
    "kwargs",
    [
        {"windows": [0]},
        {"buffers": [-1]},
        {"windows": [1, 1]},
        {"min_rate_ratio": float("nan")},
        {"reference_end": "2019-01-01"},
    ],
)
def test_maturity_rejects_invalid_configuration(kwargs):
    """Invalid diagnostic definitions fail rather than silently select another window."""
    settings = {"reference_start": "2020-01-01", "reference_end": "2020-01-03", **kwargs}
    with pytest.raises(ValueError, match=r"Windows|buffers|sequence|rate_ratio|reference"):
        maturity.run(["2020-01-01", "2020-01-02"], [0, 1], **settings)


@pytest.mark.parametrize(
    ("dates", "labels"),
    [
        (["2020-01-01", None], [0, 1]),
        (["2020-01-01"], [0, 1]),
        (["2020-01-01", "2020-01-02"], [0, None]),
        (["2020-01-01"] * 3, [0, 1, 2]),
    ],
)
def test_maturity_rejects_missing_or_inapplicable_observations(dates, labels):
    """Missing inputs and a nonbinary label must not become reassuring rate evidence."""
    with pytest.raises(ValueError, match=r"Dates and labels|binary event label"):
        maturity.run(dates, labels, reference_start="2020-01-01", reference_end="2020-01-02")


@pytest.fixture
def profile_data():
    """All overlap categories, including missing categories and conflicting labels."""
    frame = pd.DataFrame(
        {
            "x": pd.Categorical(["A", "A", "A", "B", "C", "C", "D", None, "A", "B", "C", "D", "E", "A", "B", None]),
            "date": pd.to_datetime(["2020-01-01"] * 16, utc=True),
            "y": [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0],
        }
    )
    frame.index = np.arange(100, 116)
    return frame, np.arange(8), np.arange(8, 16)


def test_actual_positions_label_multiplicity_and_repeated_evaluations(profile_data):
    """Inclusive cells overlap, while exclusive cells partition every test appearance."""
    frame, train, test = profile_data
    result = copies.run(frame, "y", [(train, test)] * 2, include_rows=True)
    fold = result["folds"][0]
    assert fold["same_label_matches"] == [2, 0, 2, 1, 0, 1, 1, 1]
    assert fold["different_label_matches"] == [1, 1, 0, 0, 0, 2, 0, 0]
    assert {k: v["rows"] for k, v in fold["exclusive"].items()} == {
        "same_only_1": 3,
        "same_only_2plus": 1,
        "different_only_1": 1,
        "different_only_2plus": 0,
        "mixed_same_and_different": 2,
        "unmatched": 1,
    }
    assert result["aggregate"]["test_evaluations"] == 16
    assert result["aggregate"]["inclusive"]["matched"]["share"] == 7 / 8
    assert sum(v["rows"] for v in result["aggregate"]["exclusive"].values()) == 16
    json.dumps(result, allow_nan=False)


def test_exact_equality_agrees_with_independent_column_comparisons():
    """Typed missing values, strings, dates and numeric categories use cell equality."""
    rng = np.random.default_rng(241)
    frame = pd.DataFrame(
        {
            "category": pd.Categorical(rng.choice([1, 2, None], 80)),
            "text": rng.choice(["1", "01", "NA", None], 80),
            "number": rng.choice([0.0, -0.0, 0.01, np.nan], 80),
            "date": pd.to_datetime(rng.choice(["2020-01-01", "2020-01-02", None], 80)),
            "y": rng.integers(0, 3, 80),
        }
    )
    train, test = np.arange(60), np.arange(60, 80)
    result = copies.run(frame, "y", [(train, test)], include_rows=True)["folds"][0]
    for offset, j in enumerate(test):
        match = np.ones(len(train), dtype=bool)
        for col in frame.columns.drop("y"):
            values, value = frame[col].iloc[train], frame[col].iloc[j]
            match &= (values.isna() if pd.isna(value) else values.eq(value).fillna(value=False)).to_numpy(dtype=bool)
        same = int(np.sum(match & frame.y.iloc[train].eq(frame.y.iloc[j]).to_numpy()))
        assert result["same_label_matches"][offset] == same
        assert result["different_label_matches"][offset] == int(match.sum()) - same


def test_subset_loss_comparison_requires_frame_and_both_split_sides(profile_data):
    """Aligned row losses reproduce the pooled mean; misbound evidence is rejected."""
    frame, train, test = profile_data
    packet = {
        "frame_digest": copies.frame_digest(frame),
        "folds": [
            {"train_indices": train.tolist(), "test_indices": test.tolist(), "losses": [1, 2, 3, 4, 20, 5, 6, 7]},
        ],
    }
    result = copies.run(frame, "y", [(train, test)], losses=packet)
    loss = result["pooled_loss"]
    assert loss["matched"]["rows"] == 7
    assert loss["unmatched"]["mean"] == 20
    assert loss["all"]["sum"] == loss["matched"]["sum"] + loss["unmatched"]["sum"]
    assert loss["all"]["mean"] == 6
    for field in ("train_indices", "test_indices"):
        bad = json.loads(json.dumps(packet))
        bad["folds"][0][field].reverse()
        with pytest.raises(ValueError, match="ordered train and test"):
            copies.run(frame, "y", [(train, test)], losses=bad)
    changed = frame.copy()
    changed.loc[100, "y"] = 1
    with pytest.raises(ValueError, match="exact ordered frame"):
        copies.run(changed, "y", [(train, test)], losses=packet)
    with pytest.raises(ValueError, match="exact ordered frame"):
        copies.run(frame.assign(x=frame.x.astype(str)), "y", [(train, test)], losses=packet)


@pytest.mark.parametrize(
    ("train", "test"), [([0, 0], [1]), ([0], [0]), ([-1], [1]), ([0], [99]), ([0.0], [1]), ([], [1])]
)
def test_invalid_splits_are_not_contamination_evidence(profile_data, train, test):
    """Repeated, overlapping, missing or nonpositional split rows are rejected."""
    with pytest.raises(ValueError, match=r"split side|Split positions|Train and test"):
        copies.run(profile_data[0], "y", [(train, test)])


def test_cli_uses_actual_folds_excludes_metadata_and_keeps_predictive_dates(monkeypatch, tmp_path):
    """The wrapper preserves named split positions and excludes only declared metadata."""
    from types import SimpleNamespace  # noqa: PLC0415

    cli = _load_cli("duplicate_contamination")
    data = SimpleNamespace(
        df=pd.DataFrame(
            {"date": pd.to_datetime(["2020-01-01", "2020-01-02"]), "group": [1, 1], "x": [3, 3], "y": [0, 1]}
        ),
        target="y",
        feature_cols=("date", "x"),
        group_cols=["group"],
        scoring_cols=("weight",),
        origin="built",
        splits={"repeat-A": {"fold-Z": ([0], [1])}},
        flat_splits=lambda: [([0], [1])],
    )
    monkeypatch.setattr(cli.dataset_io, "load", lambda *_a, **_kw: data)
    out = tmp_path / "copies.json"
    assert cli.main(["example", "--built", "--out", str(out)]) == 0
    result = json.loads(out.read_text())
    assert result["features"] == ["date", "x"]
    assert result["aggregate"]["inclusive"]["matched"]["rows"] == 0
    assert result["folds"][0]["repeat"] == "repeat-A"
    assert result["folds"][0]["fold"] == "fold-Z"


def test_maturity_cli_preserves_explicit_positive_label(monkeypatch, tmp_path):
    """String event labels are explicit and the CLI runs against the selected time column."""
    from types import SimpleNamespace  # noqa: PLC0415

    cli = _load_cli("label_maturity")
    data = SimpleNamespace(
        df=pd.DataFrame({"date": pd.to_datetime(["2020-01-01", "2020-01-02"]), "y": ["yes", "no"]}),
        target="y",
        time_on="date",
        problem_type="binary_classification",
        origin="built",
    )
    monkeypatch.setattr(cli.dataset_io, "load", lambda *_a, **_kw: data)
    out = tmp_path / "maturity.json"
    cli.main(
        [
            "example",
            "--built",
            "--reference-start",
            "2020-01-01",
            "--reference-end",
            "2020-01-02",
            "--positive-label",
            '"yes"',
            "--out",
            str(out),
        ]
    )
    result = json.loads(out.read_text())
    assert result["reference"]["events"] == 1
    assert result["positive_label"] == "yes"


def test_string_event_labels_are_never_assumed_to_be_numeric():
    """Canonical Yes/No labels require an explicit event selection, rather than all zeros."""
    with pytest.raises(ValueError, match="positive label"):
        maturity.run(
            ["2020-01-01", "2020-01-02"], ["No", "Yes"], reference_start="2020-01-01", reference_end="2020-01-02"
        )
    cli = _load_cli("label_maturity")
    with pytest.raises(SystemExit, match="2"):
        cli.main(["example", "--reference-start", "2020-01-01", "--reference-end", "2020-01-02"])


@pytest.mark.parametrize("origin", ["definition", "container"])
def test_time_key_that_is_scoring_only_does_not_become_a_predictor(origin):
    """Keep the clock for time diagnostics while retaining the actual model-input list."""
    from types import SimpleNamespace  # noqa: PLC0415

    cli = _load_cli("duplicate_contamination")
    frame = pd.DataFrame({"date": pd.to_datetime(["2020-01-01", "2020-01-02"]), "x": [3, 3], "y": [0, 1]})
    task = SimpleNamespace(
        target_column_name="y",
        group_on=None,
        time_on="date",
        grouping=None,
        scoring_columns=[SimpleNamespace(column="date")],
        problem_type="binary_classification",
        split_regime="temporal_non_iid",
    )
    splits = {0: {0: ([0], [1])}}
    if origin == "definition":
        ds = SimpleNamespace(make_splits=lambda: SimpleNamespace(df=frame, splits=splits), task_metadata=task)
        data = cli.dataset_io.from_definition(ds)
    else:
        container = SimpleNamespace(
            dataset=frame, task_metadata=task, grouping=None, experiment_metadata=SimpleNamespace(splits=splits)
        )
        data = cli.dataset_io.from_container(container, "built")
    assert "date" in data.df
    assert data.feature_cols == ("x",)
    result = copies.run(data.df, data.target, data.flat_splits(), features=data.feature_cols)
    assert result["aggregate"]["inclusive"]["matched"]["rows"] == 1
