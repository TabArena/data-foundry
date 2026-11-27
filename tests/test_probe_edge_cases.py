"""Edge cases of the probe library and its runners: missing dates, durations, few features, untested rows, columns
that are no model input, and rows without a target.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("lightgbm")

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / ".claude" / "skills" / "knowledge-data-foundry" / "scripts"
LIBRARY = REPO / ".claude" / "skills" / "knowledge-curation" / "scripts"
for path in (SCRIPTS, LIBRARY):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import dataset_io  # noqa: E402
from curation_probes import generated, groups, hidden_groups, leak, task, text, time_recovery  # noqa: E402


def _script(name: str):
    """A runner script of ``knowledge-data-foundry/scripts``, imported as a module."""
    spec = importlib.util.spec_from_file_location(f"{name}_edge_cli", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _folds(n: int, k: int = 3, seed: int = 0) -> list[tuple[np.ndarray, np.ndarray]]:
    parts = np.array_split(np.random.default_rng(seed).permutation(n), k)
    return [(np.sort(np.concatenate([parts[j] for j in range(k) if j != i])), np.sort(parts[i])) for i in range(k)]


def _probe_input(df: pd.DataFrame, **kwargs) -> dataset_io.ProbeInput:
    fields = {"target": "y", "problem_type": "binary_classification", "regime": "iid", "grouping": None}
    fields |= {"time_on": None, "origin": "definition", "splits": {0: dict(enumerate(_folds(len(df))))}}
    return dataset_io.ProbeInput(df=df, **(fields | kwargs))


# 1. a missing date stays missing


@pytest.mark.parametrize(
    "values",
    [
        pd.to_datetime(["2020-01-01", None, "2021-01-01", "2022-01-01"]),
        pd.to_datetime(["2020-01-01", None, "2021-01-01", "2022-01-01"]).tz_localize("UTC"),
        pd.PeriodIndex(["2020-01", None, "2021-01", "2022-01"], freq="M"),
        pd.to_timedelta([1, None, 2, 3], unit="D"),
    ],
)
def test_a_missing_time_is_filled_with_the_median_not_a_huge_number(values):
    """``text.features`` fills a missing date, period or duration like a missing number: with the median."""
    X, _, _ = text.features(pd.DataFrame({"t": values}), [])
    observed = text.seconds(pd.Series(values)).dropna()
    assert X["f0"].iloc[1] == pytest.approx(observed.median())
    assert X["f0"].min() >= observed.min()


def test_generated_design_keeps_a_missing_date_missing():
    """The generated-data probe's terms read a missing date as missing (filled later), never as -9.2e9 seconds."""
    df = pd.DataFrame({"d": pd.to_datetime(["2020-01-01", None, "2021-01-01"]), "x": [1.0, 2.0, 3.0]})
    numeric, _ = generated.design(df, [])
    assert np.isnan(numeric["d"].iloc[1])
    assert numeric["d"].iloc[0] == pytest.approx(pd.Timestamp("2020-01-01").timestamp())


# 2-4, 7. the leak probe on few features, an unused class level, nullable booleans and durations


def _binary_frame(n: int = 240, seed: int = 0) -> tuple[pd.DataFrame, np.ndarray]:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    return pd.DataFrame({"x": x, "y": (x + rng.normal(scale=0.5, size=n) > 0).astype(int)}), x


def test_leak_probe_with_one_numeric_feature_skips_the_drop_one_fit():
    """One numeric feature: no drop-one fit (it would leave no column), the rest runs."""
    df, _ = _binary_frame()
    df["s"] = [f"token{i % 7}" for i in range(len(df))]
    result = leak.run(df, "y", "binary_classification", _folds(len(df)), n_splits=1, n_jobs=1)
    assert result["features_probed"] == 1
    assert result["without"] == {}
    assert result["all_features"] > 0.7


def test_leak_probe_without_numeric_features_returns_a_note():
    """Only string columns: no model fit, a note instead of a crash."""
    n = 240
    df = pd.DataFrame({"s": [f"tok{i % 60} word{i % 7}" for i in range(n)], "y": np.arange(n) % 2})
    result = leak.run(df, "y", "binary_classification", _folds(n), n_splits=1, n_jobs=1)
    assert result["features_probed"] == 0
    assert "skipped" in result
    assert "all_features" not in result


def test_distance_auc_ignores_an_unused_category():
    """A binary categorical target with a level no row holds still gets a label-free distance AUC."""
    df, x = _binary_frame()
    df["x2"] = np.random.default_rng(1).normal(size=len(df))
    df["y"] = pd.Categorical(np.where(x > 0, "a", "c"), categories=["a", "b", "c"])
    result = leak.run(df, "y", "binary_classification", _folds(len(df)), n_splits=1, n_jobs=1)
    assert np.isfinite(result["distance_auc"])


def test_neighbour_space_fills_a_missing_nullable_boolean():
    """A nullable boolean with missing values enters the 1-NN space as a filled number."""
    X = pd.DataFrame({"b": pd.array([True, None, False, True], dtype="boolean"), "x": [0.1, 0.2, 0.3, 0.4]})
    Z = leak.neighbour_space(X)
    assert Z.shape == (4, 2)
    assert not np.isnan(Z).any()


def test_leak_probe_runs_with_a_nullable_boolean():
    """The whole leak probe takes a nullable boolean feature with a missing value."""
    df, _ = _binary_frame()
    df["b"] = pd.array(np.random.default_rng(2).random(len(df)) > 0.5, dtype="boolean")
    df.loc[4, "b"] = pd.NA
    result = leak.run(df, "y", "binary_classification", _folds(len(df)), n_splits=1, n_jobs=1)
    assert "nn_agreement" in result


def test_durations_enter_the_task_and_leak_probes_as_seconds():
    """A timedelta column is a model input (seconds, a missing one kept missing) in both probes."""
    df, _ = _binary_frame()
    df["td"] = pd.to_timedelta(np.random.default_rng(3).integers(0, 100, len(df)), unit="D")
    df.loc[5, "td"] = pd.NaT
    assert np.isnan(leak.model_inputs(df[["td"]])["td"].iloc[5])
    folds = _folds(len(df))
    leak_result = leak.run(df, "y", "binary_classification", folds, n_splits=1, n_jobs=1)
    assert leak_result["features_probed"] == 2
    task_result = task.run(df, "y", "binary_classification", folds, n_splits=1, n_jobs=1, text=False)
    assert task_result["features"] == 2


# 5. the group probe scores only the rows a fold tests


def _grouped_frame(n_groups: int = 60, size: int = 5) -> tuple[pd.DataFrame, np.ndarray]:
    rng = np.random.default_rng(0)
    g = np.repeat(np.arange(n_groups), size)
    x = rng.normal(size=len(g))
    return pd.DataFrame({"g": g, "x": x, "noise": rng.normal(size=len(g)), "y": (x > 0).astype(int)}), g


def test_group_probe_scores_only_the_tested_rows():
    """A holdout (one fold) leaves rows untested: they must not enter the learnability score as predictions of 0."""
    df, g = _grouped_frame()
    test = np.flatnonzero(np.isin(g, np.arange(15)))
    holdout = [[(np.setdiff1d(np.arange(len(df)), test), test)]]
    result = groups.run(
        df, "y", "binary_classification", ["g"], holdout, per_group_labels=False, permutations=0, n_jobs=1
    )
    assert result["learnability"]["lightgbm"]["row"] > 0.9
    assert result["learnability"]["lightgbm"]["row"] == pytest.approx(np.mean(result["split_gap"]["grouped"]))


# 6. columns that are no model input stay out of the group, generated, hidden-group and time-recovery probes


def test_group_probe_reads_only_the_feature_columns():
    """``feature_cols`` leaves out a column that is no model input (here a copy of the label)."""
    df, g = _grouped_frame()
    df["label_copy"] = df["y"]
    folds = [
        [(np.flatnonzero(~np.isin(g, part)), np.flatnonzero(np.isin(g, part))) for part in np.split(np.arange(60), 3)]
    ]
    kwargs = {"per_group_labels": False, "permutations": 0, "n_jobs": 1}
    honest = groups.run(df, "y", "binary_classification", ["g"], folds, feature_cols=["noise"], **kwargs)
    assert honest["features"] == 1
    assert honest["learnability"]["lightgbm"]["row"] < 0.75


def test_generated_check_reads_only_the_feature_columns():
    """A label copy left out by ``feature_cols`` makes no rule leaves."""
    rng = np.random.default_rng(0)
    n = 2000
    y = rng.random(n) < 0.2
    df = pd.DataFrame({"a": rng.normal(size=n), "b": rng.normal(size=n), "copy": y.astype(int), "y": y.astype(int)})
    leaky = generated.check_frame(df, "y", "binary_classification", [])
    honest = generated.check_frame(df, "y", "binary_classification", [], feature_cols=["a", "b"])
    assert leaky["pure_minority_share"] > 0.9
    assert honest["pure_minority_share"] < 0.2


def test_hidden_groups_and_time_recovery_read_only_the_feature_columns():
    """A label-dating time column outside ``feature_cols`` is no candidate and no time column."""
    rng = np.random.default_rng(0)
    n = 400
    df = pd.DataFrame({"x": rng.normal(size=n), "z": rng.integers(0, 40, n), "y": rng.integers(0, 2, n)})
    df["label_time"] = pd.Timestamp("2020-01-01") + pd.to_timedelta(np.arange(n), unit="D")
    hidden = hidden_groups.run(df, "y", "binary_classification", n_jobs=1, feature_cols=["x", "z"])
    assert "label_time" not in [c["column"] for c in hidden["scored"]]
    found = time_recovery.check_frame(df, "y", "binary_classification", feature_cols=["x", "z"])
    assert "label_time" not in found["time_columns"]
    assert "label_time" in time_recovery.check_frame(df, "y", "binary_classification")["time_columns"]


def test_runners_pass_the_feature_columns(monkeypatch):
    """Every runner hands ``data.feature_cols`` to its probe."""
    df = pd.DataFrame({"g": [0, 0, 1, 1], "x": [1.0, 2.0, 3.0, 4.0], "t": [1, 2, 3, 4], "y": [0, 1, 0, 1]})
    grouping = type("G", (), {"on": "g", "labels": "per_row", "time_on": None})()
    data = _probe_input(df, grouping=grouping, regime="grouped_non_iid", feature_cols=("x",))
    seen = {}

    def capture(name):
        def record(*_args, **kwargs):
            seen[name] = kwargs.get("feature_cols")
            return {"flags": []}

        return record

    group_cli = _script("group_probes")
    monkeypatch.setattr(group_cli.dataset_io, "definition", lambda *_a, **_k: type("D", (), {"task_metadata": data})())
    monkeypatch.setattr(group_cli.dataset_io, "from_definition", lambda *_a, **_k: data)
    monkeypatch.setattr(group_cli.groups, "run", capture("groups"))
    assert group_cli.main(["toy"]) == 0
    monkeypatch.setattr(dataset_io, "load", lambda *_a, **_k: data)
    generated_cli = _script("generated_probes")
    monkeypatch.setattr(generated_cli.generated, "check_frame", capture("generated"))
    generated_cli.probe("toy", Path(), built=True)
    time_cli = _script("time_probes")
    monkeypatch.setattr(time_cli.time_recovery, "check_frame", capture("time"))
    time_cli.probe("toy", Path(), built=True)
    assert seen == {"groups": ("x",), "generated": ("x",), "time": ("x",)}


# 8. the hidden-groups runner takes the regime from the task


def test_hidden_groups_runner_reads_the_regime_not_the_time_column(monkeypatch):
    """A grouped task that names a time column is grouped: skipped, or run as IID without the time column."""
    df = pd.DataFrame({"g": [0, 0, 1, 1], "t": [1, 2, 3, 4], "x": [1.0, 2.0, 3.0, 4.0], "y": [0, 1, 0, 1]})
    grouping = type("G", (), {"on": "g", "labels": "per_row", "time_on": "t"})()
    data = _probe_input(df, grouping=grouping, regime="grouped_non_iid", time_on="t", feature_cols=("x", "t"))
    cli = _script("hidden_groups")
    monkeypatch.setattr(cli.dataset_io, "load", lambda *_a, **_k: data)
    calls = []
    monkeypatch.setattr(cli.hidden, "run", lambda *_a, **k: calls.append(k) or {})
    skipped = cli.probe("toy", Path(), built=True, n_jobs=1, include_grouped=False)
    assert skipped["regime"] == "grouped"
    assert "skipped" in skipped
    cli.probe("toy", Path(), built=True, n_jobs=1, include_grouped=True)
    assert calls[0]["time_on"] is None
    assert calls[0]["feature_cols"] == ("x", "t")


# 9. rows without a target are dropped where the probes load the data


def test_rows_without_a_target_are_dropped_and_the_splits_moved():
    """The loader drops the rows without a target and moves every split, weight and scoring value with them."""
    df = pd.DataFrame({"x": np.arange(6.0), "y": [0, 1, None, 0, None, 1]})
    splits = {0: {0: (np.array([0, 1, 2]), np.array([3, 4, 5])), 1: (np.array([3, 4, 5]), np.array([0, 1, 2]))}}
    scoring = pd.DataFrame({"era": [10, 11, 12, 13, 14, 15]})
    data = _probe_input(df, splits=splits, weights=np.arange(6.0) + 1, scoring=scoring)
    clean = dataset_io.without_missing_target(data)
    assert clean.df["x"].tolist() == [0.0, 1.0, 3.0, 5.0]
    assert [a.tolist() for a in clean.splits[0][0]] == [[0, 1], [2, 3]]
    assert [a.tolist() for a in clean.splits[0][1]] == [[2, 3], [0, 1]]
    assert clean.weights.tolist() == [1.0, 2.0, 4.0, 6.0]
    assert clean.scoring["era"].tolist() == [10, 11, 13, 15]
    assert clean.target_note.startswith("2 of 6 rows")
    assert dataset_io.without_missing_target(clean) is clean


def test_task_probe_runs_after_the_loader_drops_a_missing_target():
    """The task probe, given the loader's frame, fits a target that had a missing value."""
    df, _ = _binary_frame()
    df["y"] = df["y"].map({0: "a", 1: "b"}).astype(object)
    df.loc[5, "y"] = None
    data = dataset_io.without_missing_target(_probe_input(df))
    result = task.run(data.df, "y", "binary_classification", data.flat_splits(), n_splits=1, n_jobs=1, text=False)
    assert result["rows"] == len(df) - 1


# 10. one encoder for every probe


def test_group_probe_shares_the_task_probe_inputs():
    """The group probe reads its inputs and linear encoding from the shared modules, not from copies."""
    assert groups.features is text.features
    assert groups.linear_inputs is task.linear_inputs
