"""Statistics of a temporal task's test windows, for the curator's choice of windows (SPLIT-15)."""

from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest
from data_foundry.v2 import get_dataset
from data_foundry.v2.cli import add_dataset_parser
from data_foundry.v2.dataset import NEWEST_PERIOD_RATIO, AbstractCuratedDataset, newest_period_rate
from data_foundry.v2.splits import TemporalSplits, temporal_window_splits, window_bounds
from data_foundry.v2.windows import Window, candidate_windows, window_stats

from tests.test_v2_dataset import temporal_version_body, warehouse, write_definition  # noqa: F401 - the fixture


def three_years(seed: int = 0) -> pd.DataFrame:
    """Six-hourly rows over 2021-2023; `x` jumps every December, `c` gains a level in December 2023, `y` is binary."""
    rng = np.random.default_rng(seed)
    t = pd.date_range("2021-01-01", "2023-12-31 18:00", freq="6h")
    return pd.DataFrame(
        {
            "t": t,
            "x": rng.normal(size=len(t)) + 3 * (t.month == 12),
            "c": pd.Categorical(
                np.where(t >= "2023-12-01", rng.choice(["a", "b", "new"], len(t)), rng.choice(["a", "b"], len(t)))
            ),
            "y": pd.Categorical(rng.choice(["No", "Yes"], len(t), p=[0.8, 0.2])),
        }
    )


def stats(df: pd.DataFrame, windows: list[Window], **kwargs) -> pd.DataFrame:
    """`window_stats` on the toy frame of :func:`three_years`."""
    defaults = {"time_on": "t", "target": "y", "problem_type": "binary_classification", "features": ["x", "c"]}
    return window_stats(df, windows, **(defaults | kwargs))


def test_the_bounds_are_the_splits_as_position_ranges() -> None:
    """`window_bounds` gives the windows of `temporal_window_splits`, as ranges."""
    df = three_years()
    kwargs = {"time_on": "t", "window": 2, "unit": "months", "n_windows": 4, "gap": 1, "gap_unit": "days"}
    splits = temporal_window_splits(df, **kwargs)
    bounds = window_bounds(df, **kwargs)
    assert [(list(range(b.train_stop)), list(range(b.test_start, b.test_stop))) for b in bounds] == [
        folds[0] for folds in splits.values()
    ]


def test_the_candidates_walk_back_while_half_the_rows_train() -> None:
    """The candidates keep SPLIT-14's floor, newest first, as ranges."""
    df = three_years()
    candidates = candidate_windows(
        df, "t", TemporalSplits(window=1, unit="months", n_windows=3), min_train_fraction=0.5
    )
    assert len(candidates) == 17  # August 2022 to December 2023: the train side keeps at least half the rows
    assert all(len(w.train) >= 0.5 * len(df) for w in candidates)
    assert df["t"].iloc[candidates[0].test[0]] == pd.Timestamp("2023-12-01")  # the newest first
    assert isinstance(candidates[0].train, range)  # no index lists
    # By default the candidates reach down to SPLIT-14's lower bound of 30% (amended 2026-11-11).
    lower = candidate_windows(df, "t", TemporalSplits(window=1, unit="months", n_windows=3))
    assert len(lower) == 25
    assert min(len(w.train) for w in lower) >= 0.3 * len(df)


def test_the_statistics_name_the_months_the_target_and_the_drift() -> None:
    """Months, rows, the event share and the drift, the same on a second run."""
    df = three_years()
    table = stats(df, candidate_windows(df, "t", TemporalSplits(window=1, unit="months", n_windows=3)))
    newest, november = table.iloc[0], table.iloc[1]
    assert (newest["period"], november["period"]) == ("Dec 2023", "Nov 2023")
    assert newest["n_test"] == 124
    assert newest["target_test"].startswith("Yes ")  # the event of a binary target: the class that sorts second
    assert newest["psi_max"] > 1  # December's `x` drifts
    assert november["psi_max"] < 0.25  # November's does not
    assert newest["top_drift"].startswith("x (")
    assert newest["unseen_categories"] > 0.2  # `new` exists only in the newest window
    assert stats(df, candidate_windows(df, "t", TemporalSplits(window=1, unit="months", n_windows=3))).equals(table)


def test_regression_multiclass_and_short_windows() -> None:
    """The target by problem type, and the weekdays of a window shorter than a week."""
    df = three_years().assign(z=lambda d: d["x"] * 10, k=lambda d: pd.Categorical(d["c"].astype(str)))
    days = candidate_windows(df, "t", TemporalSplits(window=2, unit="days", n_windows=3))[:2]
    regression = stats(df, days, target="z", problem_type="regression", features=["c"])
    assert regression["target_test"].iloc[0].startswith("mean ")
    assert regression["weekdays"].iloc[0] == "Sat, Sun"  # 30-31 December 2023
    multiclass = stats(df, days, target="k", problem_type="multiclass_classification", features=["x"])
    assert multiclass["target_test"].iloc[0].count("%") == 3
    no_features = stats(df, days, features=[])
    assert np.isnan(no_features["psi_max"]).all()


def test_a_numeric_time_column_shows_its_values() -> None:
    """A numeric time column shows its first and last value in its unit."""
    df = pd.DataFrame({"era": np.repeat(np.arange(1, 201), 5), "x": np.arange(1000.0), "y": np.arange(1000) % 2})
    windows = candidate_windows(df, "era", TemporalSplits(window=20, unit="unique", n_windows=3))
    table = window_stats(
        df, windows, time_on="era", target="y", problem_type="regression", features=["x"], time_unit="weeks"
    )
    assert table["period"].iloc[0] == "181 - 200 (weeks)"
    assert table["psi_max"].iloc[0] > 5  # a trend is all drift


def test_a_definition_marks_its_own_windows(tmp_path: Path, warehouse: Path, capsys: pytest.CaptureFixture) -> None:  # noqa: F811
    """A definition lists its candidates with its own windows marked; the CLI prints them."""
    del warehouse  # 30 days of 20 rows; the definition tests the newest 3 of 5 days
    write_definition(tmp_path / "datasets", "toy_ds_0p19k", body=temporal_version_body())
    ds = get_dataset(tmp_path / "datasets", "toy_ds_0p19k")
    table = ds.window_stats(min_train_fraction=0.5)
    assert list(table["chosen"]) == [True, True, True]  # a 5-day window above the floor: only the three own
    finer = ds.window_stats(window=2, step=2, min_train_fraction=0.5)
    assert finer["chosen"].sum() == 3  # the own windows, listed as rows of their own
    assert len(finer) == 7 + 3
    parser = argparse.ArgumentParser()
    add_dataset_parser(parser.add_subparsers(dest="command"))
    args = parser.parse_args(["dataset", "windows", "toy_ds_0p19k", "--root", str(tmp_path / "datasets")])
    assert args.func(args) == 0
    out = capsys.readouterr().out
    assert "window(s); * marks the definition's own" in out  # down to the 30% bound by default
    assert "psi_max" in out


def test_the_readme_describes_the_test_windows(tmp_path: Path, warehouse: Path) -> None:  # noqa: F811
    """The README's splits section describes the chosen windows."""
    del warehouse
    write_definition(tmp_path / "datasets", "toy_ds_0p19k", body=temporal_version_body())
    get_dataset(tmp_path / "datasets", "toy_ds_0p19k").check(verbose=False)
    readme = (tmp_path / "datasets" / "toy_ds_0p19k" / "README.md").read_text()
    assert "### The test windows" in readme
    assert "dataset windows toy_ds_0p19k" in readme
    assert "| period |" in readme


def test_unseen_categories_read_the_whole_train_side_and_free_text_is_left_out() -> None:
    """A level held by one early train row is seen, though no sample would draw it; free text has no levels."""
    df = three_years()
    rare = df["c"].astype(str).to_numpy()
    rare[5] = "rare"  # one row of January 2021
    rare[-1] = "rare"  # and one in the newest window
    df["c"] = pd.Categorical(rare)
    df["note"] = pd.Series([f"text {i}" for i in range(len(df))], dtype="string")
    windows = candidate_windows(df, "t", TemporalSplits(window=1, unit="months", n_windows=3))[:2]
    table = stats(df, windows, features=["x", "c", "note"], n_rows=50)
    assert table["unseen_categories"].iloc[0] == pytest.approx(1 / 3, abs=0.2)  # `new` only, not `rare`
    assert "note" not in table["top_drift"].iloc[0]
    listed = [Window(train=list(w.train), test=w.test) for w in windows]  # not a range: read whole
    assert (
        stats(df, listed, features=["c"])["unseen_categories"].tolist()
        == stats(df, windows, features=["c"])["unseen_categories"].tolist()
    )


def test_the_floor_counts_rows_also_for_unique_windows() -> None:
    """Windows of distinct time values keep half the rows for training, not half the values (SPLIT-14)."""
    df = pd.DataFrame({"era": np.repeat(np.arange(1, 11), [1, 1, 1, 1, 1, 100, 100, 100, 100, 100])})
    windows = candidate_windows(df, "era", TemporalSplits(window=1, unit="unique", n_windows=3), min_train_fraction=0.5)
    assert [int(df["era"].iloc[w.test[0]]) for w in windows] == [10, 9]  # era 8 trains on 40.4% of the rows
    assert all(len(w.train) >= 0.5 * len(df) for w in windows)


def test_the_floor_findings_ask_for_the_curators_sign_off() -> None:
    """Windows under half warn (the curator signs each off), under 30% warn again, a broken core is an error; the
    shares count every row of the curated frame, not only the container's (SPLIT-14, amended 2026-11-11).
    """

    def findings(train_sizes: list[int], frame_rows: int = 100) -> dict[str, str]:
        splits = {i: {0: (list(range(n)), [n])} for i, n in enumerate(train_sizes)}
        container = SimpleNamespace(experiment_metadata=SimpleNamespace(splits=splits), dataset=range(60))
        definition = SimpleNamespace(temporal=object(), _frame_rows=frame_rows)
        return {r.slug: r.severity for r in AbstractCuratedDataset._floor_findings(definition, container)}

    assert findings([90, 70, 55]) == {}
    assert findings([90, 70, 45]) == {"splits_train_under_half": "warning"}
    assert findings([90, 70, 45, 25]) == {"splits_train_under_half": "warning", "splits_train_under_floor": "warning"}
    assert findings([90, 45, 40])["splits_floor_core"] == "error"  # one window at half or more
    assert findings([45, 70, 60])["splits_floor_core"] == "error"  # the newest under half
    assert findings([90, 70, 45, 40, 35])["splits_floor_core"] == "error"  # more windows under half than above
    assert findings([50, 45, 40], frame_rows=100)["splits_floor_core"] == "error"
    assert findings([55, 52, 45], frame_rows=100) == {"splits_train_under_half": "warning"}


def test_a_newest_period_cut_short_is_found() -> None:
    """The newest 30 days with far fewer rows a day than the spans before flag a download or scrape cut."""
    days = pd.date_range("2023-01-01", "2023-12-31", freq="D")
    steady = pd.Series(np.repeat(days, 50))
    newest, median, ratio = newest_period_rate(steady)
    assert (newest, median, ratio) == (50.0, 50.0, 1.0)
    cut = pd.Series(np.concatenate([np.repeat(days[:-30], 50), np.repeat(days[-30:], 10)]))
    ratio_cut = newest_period_rate(cut)[2]
    assert ratio_cut == pytest.approx(0.2)
    assert ratio_cut < NEWEST_PERIOD_RATIO
    assert newest_period_rate(pd.Series(np.arange(10))) is None  # no date
    assert newest_period_rate(pd.Series(np.repeat(days[:90], 5))) is None  # fewer than four spans
