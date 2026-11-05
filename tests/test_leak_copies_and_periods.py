"""Leak probes 5 (exact copies by label on every split) and 13 (the target by period), and the model inputs the probe
scripts take from a definition.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("lightgbm")  # curation_probes.leak imports it

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude/skills/knowledge-data-foundry/scripts"
sys.path.insert(0, str(SCRIPTS.parents[1] / "knowledge-curation/scripts"))
sys.path.insert(0, str(SCRIPTS))

import dataset_io  # noqa: E402 - from the skill's script folder, put on the path above
from curation_probes import leak  # noqa: E402


def _cli():
    spec = importlib.util.spec_from_file_location("leak_probes_cli", SCRIPTS / "leak_probes.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Probe 5


@pytest.fixture
def profile_data():
    """Every kind of copy: same label once and twice, another label, both labels, missing values, none."""
    frame = pd.DataFrame(
        {
            "x": pd.Categorical(["A", "A", "A", "B", "C", "C", "D", None, "A", "B", "C", "D", "E", "A", "B", None]),
            "y": [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0],
        }
    )
    return frame, np.arange(8), np.arange(8, 16)


def test_copy_counts_partition_the_test_rows_by_label_and_number_of_copies(profile_data):
    """Test rows 8-15 against train 0-7, where A has two copies of label 0 and one of 1, B one of 1, C two of 0, D one
    of 1, E none, and a missing x one of label 0.
    """
    frame, train, test = profile_data
    counts = leak.copy_counts(leak.profile_codes(frame[["x"]]), frame["y"], [(train, test)] * 2)
    assert counts["test_rows"] == 16  # a row in two repeats counts twice
    assert counts["splits"] == 2
    assert counts["matched"] == pytest.approx(7 / 8)
    # same label only: C (two copies); D, the second B and the missing x (one each)
    assert counts["same_label_only"] == {"one": pytest.approx(3 / 8), "two_or_more": pytest.approx(1 / 8)}
    # another label only: the first B (label 0 against B's 1 in train)
    assert counts["different_label_only"] == {"one": pytest.approx(1 / 8), "two_or_more": 0.0}
    # both labels: the two A rows
    assert counts["both_labels"] == pytest.approx(2 / 8)
    assert counts["matched_per_split"] == [pytest.approx(7 / 8)] * 2
    parts = counts["same_label_only"] | {f"d_{k}": v for k, v in counts["different_label_only"].items()}
    assert sum(parts.values()) + counts["both_labels"] == pytest.approx(counts["matched"])
    json.dumps(counts, allow_nan=False)


def test_profile_codes_agree_with_cell_by_cell_equality():
    """Missing values of any kind equal each other within a column, -0.0 equals 0.0, strings are not numbers."""
    rng = np.random.default_rng(241)
    frame = pd.DataFrame(
        {
            "category": pd.Categorical(rng.choice([1, 2, None], 80)),
            "text": rng.choice(["1", "01", "NA", None], 80),
            "number": rng.choice([0.0, -0.0, 0.01, np.nan], 80),
            "date": pd.to_datetime(rng.choice(["2020-01-01", "2020-01-02", None], 80)),
        }
    )
    codes = leak.profile_codes(frame)
    for i in range(0, 80, 7):
        for j in range(80):
            equal = all(
                (pd.isna(frame[c].iloc[i]) and pd.isna(frame[c].iloc[j])) or frame[c].iloc[i] == frame[c].iloc[j]
                for c in frame.columns
            )
            assert (codes[i] == codes[j]) == equal, (i, j)


def test_run_counts_copies_on_every_split_not_only_the_probed_ones():
    """The second split has copies in train, the first none; only the first is probed with models."""
    rng = np.random.default_rng(3)
    n = 300
    df = pd.DataFrame({"a": rng.normal(size=n), "b": rng.normal(size=n), "y": rng.integers(0, 2, n)})
    df.loc[200:, ["a", "b", "y"]] = df.loc[:99, ["a", "b", "y"]].to_numpy()  # rows 200-299 copy rows 0-99
    first = (np.arange(100, 200), np.arange(200, 300))  # train holds none of the copied rows
    second = (np.arange(0, 200), np.arange(200, 300))  # train holds every original
    result = leak.run(df, "y", "binary_classification", [first, second], n_splits=1, n_jobs=1)
    assert result["exact_copies"]["matched_per_split"] == [0.0, 1.0]
    assert result["exact_copy_share"] == pytest.approx(0.5)
    assert result["exact_copies"]["same_label_only"]["one"] == pytest.approx(0.5)


@pytest.mark.parametrize("origin", ["definition", "container"])
def test_a_scoring_only_time_key_stays_in_the_frame_but_is_no_model_input(origin):
    """The probes keep the clock for probe 13, and the copy profile leaves it out."""
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
        ds = SimpleNamespace(
            make_splits=lambda: SimpleNamespace(df=frame, splits=splits), task_metadata_for=lambda _df: task
        )
        data = dataset_io.from_definition(ds)
    else:
        container = SimpleNamespace(
            dataset=frame, task_metadata=task, grouping=None, experiment_metadata=SimpleNamespace(splits=splits)
        )
        data = dataset_io.from_container(container, "built")
    assert "date" in data.df
    assert data.feature_cols == ("x",)
    counts = leak.copy_counts(leak.profile_codes(data.df[list(data.feature_cols)]), data.df["y"], data.flat_splits())
    assert counts["different_label_only"]["one"] == 1.0  # with the date in the profile it would be no copy


# Probe 13


def _daily(days: int = 900, per_day: int = 40, seed: int = 0):
    rng = np.random.default_rng(seed)
    t = pd.Series(np.repeat(pd.date_range("2018-01-01", periods=days, freq="D"), per_day))
    return rng, t


def test_a_planted_censoring_drop_is_flagged_and_dated():
    """Events of the last 20 days 10% recorded, of the 25 before half: the newest months fall below the band."""
    rng, t = _daily()
    y = (rng.random(len(t)) < 0.2).astype(int)
    age = (t.max() - t).dt.days.to_numpy()
    seen = np.where(age < 20, 0.1, np.where(age < 45, 0.5, 1.0))
    censored = np.where((y == 1) & (rng.random(len(t)) > seen), 0, y)
    result = leak.target_by_period(t, censored, "binary_classification", report=False)
    assert result["period"] == "M"
    assert result["positive"] == 1  # the minority class
    stat = result["statistics"]["rate of 1"]
    assert stat["direction"] == "falls"
    assert stat["trailing_out_of_band"] >= 1
    assert result["flags"] == ["rate of 1"]
    assert "right-censoring" in result["reading"]
    clean = leak.target_by_period(t, y, "binary_classification", report=False)
    assert clean["flags"] == []
    assert "no sign of censoring" in clean["reading"]
    json.dumps(result, allow_nan=False)


def test_durations_cut_by_the_release_end_lose_their_upper_quantile_and_rows():
    """Durations still running at the release are missing: rows, mean and p90 fall in the newest periods."""
    rng, t = _daily()
    duration = rng.exponential(30, len(t))
    done = (t + pd.to_timedelta(duration, unit="D") <= t.max()).to_numpy()
    result = leak.target_by_period(t[done], duration[done], "regression", report=False)
    for name in ("rows per day", "mean", "p90"):
        assert result["statistics"][name]["direction"] == "falls", name
    full = leak.target_by_period(t, duration, "regression", report=False)
    assert full["flags"] == []


def test_a_partial_last_month_and_short_months_are_not_a_drop_in_rows():
    """Rows per covered day: February and a release that ends mid-month leave the row count in band."""
    rng, t = _daily(days=890)  # ends on 2020-06-08
    result = leak.target_by_period(t, rng.integers(0, 2, len(t)), "binary_classification", report=False)
    assert result["coverage_last"] < 0.5
    assert result["statistics"]["rows per day"]["trailing_out_of_band"] == 0


def test_count_and_multiclass_targets_get_their_statistics():
    """A count gets its mean and zero share, a multiclass target the share of each class."""
    rng, t = _daily(days=400)
    counts = leak.target_by_period(t, rng.poisson(0.3, len(t)), "regression", report=False)
    assert list(counts["statistics"]) == ["rows per day", "mean", "zero share"]
    classes = leak.target_by_period(t, rng.choice(list("abc"), len(t)), "multiclass_classification", report=False)
    assert sorted(classes["classes"]) == ["a", "b", "c"]
    assert {f"share of {c}" for c in "abc"} <= set(classes["statistics"])


def test_years_and_integer_periods_are_not_read_as_nanoseconds():
    """Tunisian's fiscal year: integers in the year range are years, other integers ordinal periods."""
    rng = np.random.default_rng(1)
    years = leak.target_by_period(
        np.repeat(np.arange(2005, 2021), 50), rng.normal(size=800), "regression", report=False
    )
    assert (years["time_kind"], years["periods"], years["first"]) == ("year", 16, "2005")
    assert leak.period_times(pd.Series(["2019", "2020"]))[1] == "year"
    assert leak.period_times(pd.Series(pd.Categorical([2019, 2020])))[1] == "year"
    assert leak.period_times(pd.Series([1, 2, 3]))[1] == "integer"


def test_dates_on_the_first_of_january_are_years_counted_per_period():
    """Tunisian's `fiscal_year` stored as a date: years, rows per period, with or without `--period Y`."""
    rng = np.random.default_rng(4)
    dates = pd.to_datetime(pd.Series(rng.integers(2013, 2019, 6000)).astype(str) + "-01-01")
    for freq in (None, "Y"):
        result = leak.target_by_period(dates, rng.normal(size=6000), "regression", freq=freq, report=False)
        assert (result["time_kind"], result["period"], result["periods"]) == ("year", "year", 6)
        assert "rows per period" in result["statistics"]
        assert result["flags"] == []
    assert leak.period_times(pd.Series(pd.to_datetime(["2019-01-01", "2019-01-02"])))[1] == "datetime"


def test_dates_that_label_their_period_are_counted_per_period():
    """Month starts (one date per month): rows per period, not per covered day."""
    rng = np.random.default_rng(5)
    months = pd.Series(pd.date_range("2020-01-01", periods=24, freq="MS"))
    t = months.sample(4800, replace=True, random_state=1).reset_index(drop=True)
    result = leak.target_by_period(t, rng.normal(size=4800), "regression", freq="M", report=False)
    assert "rows per period" in result["statistics"]
    assert result["flags"] == []


def test_a_rank_is_cut_into_equal_count_periods_and_says_so():
    """medical_facility's `arrival_order`: one row per rank, so 40 equal-count periods by its order."""
    rng = np.random.default_rng(6)
    rank = pd.Series(rng.permutation(4000) + 1)
    y = (rng.random(4000) < 0.3).astype(int)
    result = leak.target_by_period(rank, y, "binary_classification", report=False)
    assert (result["period"], result["periods"], result["first"]) == ("binned", 40, "1-100")
    assert "equal-count periods" in result["note"]
    assert "rows per period" not in result["statistics"]  # equal counts by construction
    late = np.where((rank.to_numpy() > 3700) & (rng.random(4000) < 0.8), 0, y)
    assert leak.target_by_period(rank, late, "binary_classification", report=False)["flags"] == ["rate of 1"]
    few = leak.target_by_period(np.repeat(np.arange(1, 13), 100), y[:1200], "binary_classification", report=False)
    assert few["period"] == "integer"  # a month index with many rows per value stays as it is


def test_the_timezone_sets_the_calendar():
    """23:30 at -06:00 is that day on its own clock and the next day in UTC."""
    stamps = pd.Series(pd.to_datetime(["2020-01-01T23:30:00-06:00"]))
    assert leak.period_times(stamps)[0].iloc[0].day == 1
    assert leak.period_times(stamps, tz="UTC")[0].iloc[0].day == 2


@pytest.mark.parametrize(
    ("times", "kwargs", "message"),
    [
        ([True, False] * 50, {}, "boolean"),
        ([1.5, 2.0] * 50, {}, "fractional"),
        (["abc", "def"] * 50, {}, "neither dates"),
        (list(pd.date_range("2020-01-01", periods=90, freq="h")), {}, "fewer than 5 days"),
        (list(np.repeat(np.arange(2001, 2011), 10)), {"positive": "fraud"}, "does not occur"),
        (list(np.repeat(np.arange(2001, 2004), 10)) * 3 + [2003] * 10, {}, "at least 5"),
    ],
)
def test_unusable_inputs_are_rejected_with_the_reason(times, kwargs, message):
    """Booleans, fractions, words, under 5 periods and an absent event class raise, never pass silently."""
    y = np.tile([0, 1], len(times) // 2)
    with pytest.raises(ValueError, match=message):
        leak.target_by_period(times, y, "binary_classification", report=False, **kwargs)


def test_the_cli_runs_probe_13_alone_on_the_task_time_column(monkeypatch, capsys):
    """``--period-only`` runs probe 13 on the task's time column and says why when there is none."""
    cli = _cli()
    rng, t = _daily(days=200)
    df = pd.DataFrame({"when": t, "x": rng.normal(size=len(t)), "y": rng.integers(0, 2, len(t))})
    data = SimpleNamespace(df=df, target="y", problem_type="binary_classification", time_on="when")
    monkeypatch.setattr(cli.dataset_io, "definition", lambda *_a, **_kw: SimpleNamespace(raw=None))
    monkeypatch.setattr(cli.dataset_io, "from_definition", lambda _ds: data)
    args = cli.argparse.Namespace(
        name="example", root=".", time_on=None, period="W", tz=None, positive="1", tail=None, period_only=True
    )
    result = cli.probe(args)
    assert result["target_by_period"]["period"] == "W"
    assert result["target_by_period"]["positive"] == 1
    assert "target by period (probe 13): 29 weekly periods" in capsys.readouterr().out
    data.time_on = None
    assert cli.probe(args)["target_by_period"] is None
    assert "not run (no time column" in capsys.readouterr().out
