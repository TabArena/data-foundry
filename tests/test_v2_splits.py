"""Tests for the v2 split protocol (``data_foundry.v2.splits``).

The cross-validation builders are pinned by a checksum of their splits: a change to them would change the splits,
and so the checksum, of every container built since.
"""

from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd
import pytest
from data_foundry import bundle_checks
from data_foundry.schema import PredictiveMLSplitsMetadata, PredictiveMLTaskMetadataV2, RowBudget, TrainSampling
from data_foundry.v2 import splits as protocol
from data_foundry.v2.splits import (
    fit_splits_to_budget,
    grouped_splits,
    iid_splits,
    protocol_checks,
    recommended_dimensions,
    sample_temporal_splits,
    sample_train_positions,
    subsample_train,
)

from tests.test_bundle_checks import make_container, make_iid_frame, make_spec


class Sized:
    """Stands in for a frame of ``n`` rows where only the length is read."""

    def __init__(self, n: int) -> None:
        """Pretend to have ``n`` rows."""
        self._n = n

    def __len__(self) -> int:
        return self._n


def labelled_frame(n: int = 300, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "x": rng.normal(size=n),
            "y": pd.Categorical(rng.choice(["a", "b", "c"], size=n, p=[0.6, 0.3, 0.1])),
            "t": np.arange(n),
        },
    )


def grouped_frame(n_groups: int = 120, *, per_group: bool, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    sizes = rng.integers(1, 12, size=n_groups)
    groups = np.repeat(rng.permutation(n_groups), sizes)  # groups appear out of order, as in real data
    if per_group:
        labels = np.repeat(rng.choice(["a", "b"], size=n_groups, p=[0.7, 0.3]), sizes)
    else:
        labels = rng.choice(["a", "b"], size=len(groups), p=[0.7, 0.3])
    return pd.DataFrame({"g": groups, "y": pd.Categorical(labels), "pos": np.arange(len(groups))})


def splits_digest(splits: dict) -> str:
    """A short checksum of a set of splits."""
    return hashlib.sha256(json.dumps(splits, sort_keys=True).encode()).hexdigest()[:16]


# --- the builders' splits are pinned -----------------------------------------------------------------------------
@pytest.mark.parametrize(("stratify_on", "digest"), [("y", "ea2677f90aa6b34d"), (None, "c60489ba1251853b")])
def test_iid_splits_are_pinned(stratify_on: str | None, digest: str) -> None:
    assert splits_digest(iid_splits(labelled_frame(), n_repeats=3, stratify_on=stratify_on)) == digest


@pytest.mark.parametrize(
    ("per_group", "stratify_on", "digest"),
    [
        (True, "y", "2f2c4213ad60503a"),
        (True, None, "4a779b7fa3701698"),
        (False, "y", "7e8136e69e8bed07"),
        (False, None, "49dd36ae92a01c5a"),
    ],
)
def test_grouped_splits_are_pinned(*, per_group: bool, stratify_on: str | None, digest: str) -> None:
    labels = "per_group" if per_group else "per_sample"
    df = grouped_frame(per_group=per_group)
    got = grouped_splits(df, n_repeats=3, group_on="g", group_labels=labels, stratify_on=stratify_on)
    assert splits_digest(got) == digest


def test_per_group_splits_reject_a_group_with_several_labels() -> None:
    df = grouped_frame(per_group=False)
    with pytest.raises(ValueError, match="several values"):
        grouped_splits(df, n_repeats=1, group_on="g", group_labels="per_group", stratify_on="y")


@pytest.mark.parametrize(
    ("n", "repeats"),
    [
        (100, 20),
        (749, 20),  # 499 on the train side
        (750, 10),
        (3_749, 10),
        (3_750, 3),
        (374_999, 3),
        (375_000, 1),  # 250,000 on the train side
        (5_000_000, 1),
    ],
)
def test_repeats_follow_the_train_side_in_rows(n: int, repeats: int) -> None:
    assert recommended_dimensions(Sized(n)) == (repeats, 3)


def test_per_group_frames_count_groups_at_any_size() -> None:
    small = pd.DataFrame({"g": np.repeat(np.arange(10), 12), "y": 0})  # 120 rows, 10 groups
    assert recommended_dimensions(small, group_on="g", group_labels="per_group") == (20, 3)
    large = pd.DataFrame({"g": np.repeat(np.arange(10), 130_000), "y": 0})  # 1.3M rows, still 10 groups
    assert recommended_dimensions(large, group_on="g", group_labels="per_group") == (20, 3)


# --- fitting the cross-validation to a row budget ---------------------------------------------------------------
def test_fit_splits_to_budget_tests_on_a_sample_of_each_third_and_trains_on_the_rest() -> None:
    df = labelled_frame(n=250)
    splits = iid_splits(df, n_repeats=1, stratify_on="y")
    fitted, sampled = fit_splits_to_budget(df, splits, RowBudget(train=100, test=50), stratify_on="y")
    assert sampled
    for fold, (train, test) in fitted[0].items():
        assert (len(train), len(test)) == (200, 50)  # the train side is not capped: a benchmark sub-samples it
        assert set(test) <= set(splits[0][fold][1])  # a sample of the fold's third
        assert set(train) | set(test) == set(range(250))  # the rows it leaves out train in this fold
        assert not set(train) & set(test)
        assert train == sorted(train)
        share = (df["y"].iloc[splits[0][fold][1]] == "c").mean()
        assert abs((df["y"].iloc[test] == "c").mean() - share) <= 1 / 50  # stratified


def test_fit_splits_to_budget_keeps_whole_groups() -> None:
    df = grouped_frame(n_groups=300, per_group=False)
    splits = grouped_splits(df, n_repeats=1, group_on="g", group_labels="per_sample")
    budget = RowBudget(train=len(df) * 3 // 4, test=len(df) // 6)
    fitted, sampled = fit_splits_to_budget(df, splits, budget, group_on="g")
    assert sampled
    sizes = df["g"].value_counts()
    for train, test in fitted[0].values():
        assert len(train) + len(test) == len(df)  # every row the test sample leaves out trains in the fold
        assert len(test) <= budget.test
        train_groups, test_groups = set(df["g"].iloc[train]), set(df["g"].iloc[test])
        assert not train_groups & test_groups
        for side, groups in ((train, train_groups), (test, test_groups)):
            assert len(side) == sizes[list(groups)].sum()  # whole groups only


def test_fit_splits_to_budget_leaves_a_long_train_side_whole() -> None:
    df = grouped_frame(n_groups=300, per_group=False)
    splits = grouped_splits(df, n_repeats=1, group_on="g", group_labels="per_sample")
    longest = max(len(train) for train, _ in splits[0].values())
    fitted, sampled = fit_splits_to_budget(df, splits, RowBudget(train=longest - 20, test=10_000), group_on="g")
    assert not sampled  # no test side is over its budget; a long train side is for the benchmark to sub-sample
    assert fitted == splits


def test_fit_splits_to_budget_within_budget_changes_nothing() -> None:
    df = labelled_frame()
    splits = iid_splits(df, n_repeats=1, stratify_on="y")
    fitted, sampled = fit_splits_to_budget(df, splits, RowBudget(train=200, test=100), stratify_on="y")
    assert not sampled
    assert fitted == splits


def test_fit_splits_to_budget_at_two_to_one_is_plain_cross_validation() -> None:
    df = labelled_frame(n=1_500)
    splits = iid_splits(df, n_repeats=1, stratify_on="y")
    fitted, sampled = fit_splits_to_budget(df, splits, RowBudget(train=1_000, test=500), stratify_on="y")
    assert not sampled
    assert fitted == splits


# --- temporal sampling per window --------------------------------------------------------------------------------
def daily_frame(n_days: int = 60, per_day: int = 50, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = n_days * per_day
    return pd.DataFrame(
        {
            "t": pd.date_range("2024-01-01", periods=n_days, freq="D").repeat(per_day),
            "y": pd.Categorical(rng.choice(["a", "b"], size=n, p=[0.8, 0.2])),
            "pos": np.arange(n),
        },
    )


def test_temporal_sampling_caps_the_test_windows_and_keeps_all_history() -> None:
    df = daily_frame()
    windows = protocol.temporal_window_splits(df, time_on="t", window=5, unit="days", n_windows=3)
    out, splits, trimmed = sample_temporal_splits(df, windows, stratify_on="y", budget=RowBudget(train=1_000, test=200))
    assert trimmed
    for i, folds in splits.items():
        train, test = folds[0]
        assert len(test) == 200  # each window holds 250 rows
        assert set(out["pos"].iloc[train]) == set(df["pos"].iloc[windows[i][0][0]])  # every earlier row trains
        assert out["t"].iloc[train].max() < out["t"].iloc[test].min()
    used = {i for folds in splits.values() for pair in folds.values() for side in pair for i in side}
    assert used == set(range(len(out)))  # no row is shipped that no split uses
    assert out["pos"].is_monotonic_increasing  # the time order is kept
    original = windows[0][0][1]  # test side of the newest window, before sampling
    share = (df["y"].iloc[original] == "b").mean()
    assert abs((out["y"].iloc[splits[0][0][1]] == "b").mean() - share) <= 1 / 200  # the class share is kept


def test_temporal_sampling_keeps_every_row_an_older_window_leaves_out() -> None:
    df = daily_frame()
    windows = protocol.temporal_window_splits(df, time_on="t", window=5, unit="days", n_windows=3)
    out, _splits, _ = sample_temporal_splits(df, windows, budget=RowBudget(train=1_000, test=200))
    newest_test = set(df["pos"].iloc[windows[0][0][1]])
    # only the newest window's unsampled rows are dropped: an older window's train on in the newer windows
    assert set(df["pos"]) - set(out["pos"]) <= newest_test
    assert len(df) - len(out) == 50


def test_temporal_sampling_by_whole_time_values() -> None:
    df = daily_frame()  # 50 rows a day
    windows = protocol.temporal_window_splits(df, time_on="t", window=5, unit="days", n_windows=3)
    out, splits, trimmed = sample_temporal_splits(
        df, windows, whole_values_of="t", budget=RowBudget(train=1_020, test=120)
    )
    assert trimmed
    assert (out["t"].value_counts() == 50).all()  # a kept day keeps every row
    for i, folds in splits.items():
        train, test = folds[0]
        assert len(test) == 100  # the day that would cross the cap is dropped
        assert len(train) == len(windows[i][0][0])  # the train side keeps every earlier row
        assert out["t"].iloc[train].max() < out["t"].iloc[test].min()
    assert out["pos"].is_monotonic_increasing
    again, same, _ = sample_temporal_splits(df, windows, whole_values_of="t", budget=RowBudget(train=1_020, test=120))
    assert again.equals(out)  # deterministic
    assert same == splits


def test_temporal_sampling_by_time_refuses_stratification_and_oversized_values() -> None:
    df = daily_frame()
    windows = protocol.temporal_window_splits(df, time_on="t", window=5, unit="days", n_windows=3)
    with pytest.raises(ValueError, match="does not stratify"):
        sample_temporal_splits(
            df, windows, whole_values_of="t", stratify_on="y", budget=RowBudget(train=1_000, test=120)
        )
    with pytest.raises(ValueError, match="single time value"):
        sample_temporal_splits(df, windows, whole_values_of="t", budget=RowBudget(train=1_000, test=40))


def test_temporal_windows_gap_in_its_own_unit() -> None:
    minutes = pd.DataFrame({"t": pd.date_range("2024-01-01", periods=10 * 24 * 60, freq="min")})
    splits = protocol.temporal_window_splits(
        minutes, time_on="t", window=2, unit="days", n_windows=3, gap=15, gap_unit="minutes"
    )
    for folds in splits.values():
        train, test = folds[0]
        assert minutes["t"].iloc[test].min() - minutes["t"].iloc[train].max() == pd.Timedelta(minutes=16)
        assert len(test) == 2 * 24 * 60
    days = protocol.temporal_window_splits(minutes, time_on="t", window=2, unit="days", n_windows=3, gap=1)
    assert (
        days[0][0][0]
        == protocol.temporal_window_splits(
            minutes, time_on="t", window=2, unit="days", n_windows=3, gap=1, gap_unit="days"
        )[0][0][0]
    )  # gap_unit equal to the window's unit changes nothing
    assert len(splits[0][0][0]) == len(days[0][0][0]) + 24 * 60 - 15
    with pytest.raises(ValueError, match="needs a calendar unit"):
        protocol.temporal_window_splits(
            minutes, time_on="t", window=2, unit="rows", n_windows=3, gap=1, gap_unit="days"
        )


def test_temporal_sampling_within_budget_changes_nothing() -> None:
    df = daily_frame(n_days=20)
    windows = protocol.temporal_window_splits(df, time_on="t", window=5, unit="days", n_windows=3)
    out, splits, trimmed = sample_temporal_splits(
        df, windows, RowBudget(train=1_000_000, test=500_000), stratify_on="y"
    )
    assert not trimmed
    assert out.equals(df)  # every row is in the newest train side or a test window
    assert splits == windows


# --- the default sampler of a train side ---------------------------------------------------------------------------
def yearly_frame(n_days: int = 900, per_day: int = 4, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = n_days * per_day
    return pd.DataFrame(
        {
            "t": pd.date_range("2022-01-01", periods=n_days, freq="D").repeat(per_day),
            "y": pd.Categorical(rng.choice(["a", "b"], size=n, p=[0.8, 0.2])),
            "g": np.arange(n) // 6,
        },
    )


def test_the_default_draws_a_temporal_train_side_from_its_newest_year() -> None:
    df = yearly_frame()
    positions = np.arange(len(df) - 100)
    kept = sample_train_positions(df, positions, 1_000, time_on="t", stratify_on="y")
    assert len(kept) == 1_000
    newest = df["t"].iloc[positions].max()
    assert df["t"].iloc[kept].min() >= newest - pd.DateOffset(years=1)  # the newest year only
    assert df["t"].iloc[kept].nunique() > 200  # spread over the year, not its newest days
    share = (df["y"].iloc[positions] == "b").mean()
    assert abs((df["y"].iloc[kept] == "b").mean() - share) < 0.03
    assert np.array_equal(kept, sample_train_positions(df, positions, 1_000, time_on="t", stratify_on="y"))


def test_the_default_takes_the_newest_rows_when_the_year_is_short() -> None:
    df = yearly_frame()
    positions = np.arange(len(df))
    kept = sample_train_positions(df, positions, 2_000, time_on="t")  # the newest year holds 1,464 rows
    assert np.array_equal(kept, positions[-2_000:])
    by_day = sample_train_positions(df, positions, 2_002, time_on="t", whole_values_of="t")
    assert (df["t"].iloc[by_day].value_counts() == 4).all()  # whole days only
    assert len(by_day) == 2_000


def test_the_default_on_a_numeric_time_takes_its_year_from_the_time_unit() -> None:
    df = yearly_frame().assign(era=lambda d: (d["t"] - d["t"].iloc[0]).dt.days // 7)  # a weekly era, as numerai's
    positions = np.arange(len(df))
    kept = sample_train_positions(df, positions, 500, time_on="era", time_unit="weeks")
    assert len(kept) == 500
    assert df["era"].iloc[kept].min() > df["era"].max() - 52  # the newest 52 eras
    by_date = sample_train_positions(df, positions, 500, time_on="t")
    assert df["t"].iloc[by_date].min() >= df["t"].max() - pd.DateOffset(years=1)  # the same year by the calendar
    extended = sample_train_positions(df, positions, 2_000, time_on="era", time_unit="weeks")
    assert np.array_equal(extended, positions[-2_000:])  # the year holds fewer: extended back in time
    with pytest.raises(ValueError, match="needs what one step of it counts"):
        sample_train_positions(df, positions, 500, time_on="era")


def test_the_default_without_time() -> None:
    df = yearly_frame()
    grouped = sample_train_positions(df, np.arange(len(df)), 500, group_on="g")
    assert len(grouped) <= 500
    assert (df["g"].iloc[grouped].value_counts() == 6).all()  # whole groups
    within = np.arange(100)
    assert np.array_equal(sample_train_positions(df, within, 500, time_on="t"), within)  # a side within the budget


def test_subsample_train_follows_the_container() -> None:
    df = yearly_frame()
    splits = {0: {0: (list(range(3_000)), list(range(3_000, 3_600)))}}
    meta = PredictiveMLSplitsMetadata(
        splits_comment="s",
        splits=splits,
        row_budget=RowBudget(train=1_000, test=600),
        train_sampling=TrainSampling(default="newest_year", unit="rows", stratify_on="y"),
    )
    task = PredictiveMLTaskMetadataV2(
        target_column_name="y", problem_type="binary_classification", objective_metric=make_spec(), time_on="t"
    )
    container = make_container(df, task_metadata=task, experiment_metadata=meta)
    kept = subsample_train(container, 0, 0)
    assert len(kept) == 1_000
    assert kept == sample_train_positions(df, splits[0][0][0], 1_000, time_on="t", stratify_on="y").tolist()
    assert subsample_train(container, 0, 0, n_rows=5_000) == splits[0][0][0]  # within a larger budget: whole


# --- protocol checks ----------------------------------------------------------------------------------------------
V2_TASK = PredictiveMLTaskMetadataV2(
    target_column_name="target",
    problem_type="binary_classification",
    objective_metric=make_spec(),
    stratify_on="target",
)


def make_v2_container(df: pd.DataFrame, **overrides):
    """A format-2 container (the bundle checks judge it by the v2 protocol)."""
    return make_container(df, **{"task_metadata": V2_TASK, **overrides})


def slugs(container) -> list[str]:
    return [r.slug for r in protocol_checks(container)]


def test_only_a_format_2_container_is_judged_by_the_split_protocol() -> None:
    df = make_iid_frame(60)
    single = PredictiveMLSplitsMetadata(splits_comment="x", splits={0: {0: (list(range(40)), list(range(40, 60)))}})
    v1_slugs = bundle_checks.run_bundle_checks(make_container(df, experiment_metadata=single), verbose=False).slugs
    v2_slugs = bundle_checks.run_bundle_checks(make_v2_container(df, experiment_metadata=single), verbose=False).slugs
    assert "splits_dimensions_off_protocol" not in v1_slugs  # format 1 is frozen: no protocol check is left for it
    assert v2_slugs.count("splits_dimensions_off_protocol") == 1
    assert "splits_test_over_budget" not in v2_slugs  # no budget recorded: no size limit


def test_protocol_checks_pass_the_recommended_splits() -> None:
    df = make_iid_frame(60)
    splits = iid_splits(df, n_repeats=20, stratify_on="target")
    container = make_v2_container(df, experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="x", splits=splits))
    assert slugs(container) == []


def test_protocol_checks_flag_a_single_split() -> None:
    df = make_iid_frame(60)
    single = {0: {0: (list(range(40)), list(range(40, 60)))}}
    container = make_v2_container(df, experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="x", splits=single))
    assert "splits_dimensions_off_protocol" in slugs(container)


@pytest.mark.parametrize(
    ("budget", "sampling", "expected"),
    [
        (None, None, set()),  # no budget, no size limit
        (RowBudget(train=40, test=20), "rows", set()),  # each fold tests on 20 rows
        (RowBudget(train=30, test=20), "rows", set()),  # a train side over the budget is for the benchmark
        (RowBudget(train=40, test=10), "rows", {"splits_test_over_budget"}),
        (RowBudget(train=40, test=20), None, {"splits_train_sampling_missing"}),
    ],
)
def test_protocol_checks_hold_the_container_to_its_row_budget(
    budget: RowBudget | None, sampling: str | None, expected: set[str]
) -> None:
    df = make_iid_frame(60)
    splits = iid_splits(df, n_repeats=20, stratify_on="target")
    train_sampling = None if sampling is None else TrainSampling(default="random", unit=sampling)
    meta = PredictiveMLSplitsMetadata(
        splits_comment="x", splits=splits, row_budget=budget, train_sampling=train_sampling
    )
    findings = {r.slug: r.severity for r in protocol_checks(make_v2_container(df, experiment_metadata=meta))}
    assert {slug for slug in findings if slug.endswith(("_over_budget", "_sampling_missing"))} == expected
    assert findings.get("splits_test_over_budget", "warning") == "warning"
    assert findings.get("splits_train_sampling_missing", "error") == "error"


@pytest.mark.parametrize(("n_windows", "flagged"), [(1, True), (3, False)])
def test_protocol_checks_want_three_temporal_windows(*, n_windows: int, flagged: bool) -> None:
    df = make_iid_frame(60).assign(t=pd.date_range("2024-01-01", periods=60, freq="D"))
    windows = protocol.temporal_window_splits(df, time_on="t", window=5, unit="days", n_windows=n_windows)
    task = PredictiveMLTaskMetadataV2(
        target_column_name="target", problem_type="binary_classification", objective_metric=make_spec(), time_on="t"
    )
    container = make_container(
        df,
        task_metadata=task,
        experiment_metadata=PredictiveMLSplitsMetadata(
            splits_comment="x", splits=windows, time_horizon=5, time_horizon_unit="days"
        ),
    )
    assert ("splits_too_few" in slugs(container)) is flagged


def test_a_missing_build_dependency_names_the_extra() -> None:
    from data_foundry.v2._optional import BUILD_INSTALL, import_build_dependency

    assert import_build_dependency("sklearn.model_selection").__name__ == "sklearn.model_selection"
    with pytest.raises(ImportError, match=r"needs `no_such_package`.*data-foundry\[build\]") as error:
        import_build_dependency("no_such_package.sub")
    assert BUILD_INSTALL in str(error.value)


def test_several_group_columns_make_one_group_per_combination() -> None:
    rng = np.random.default_rng(0)
    df = pd.DataFrame(
        {"a": rng.integers(0, 6, 300), "b": rng.choice(["x", "y", None], 300), "y": rng.integers(0, 2, 300)}
    )
    splits = protocol.grouped_splits(df, n_repeats=2, group_on=["a", "b"], group_labels="per_sample", stratify_on="y")
    key = df[["a", "b"]].astype("string").fillna("nan").agg("|".join, axis=1)
    for folds in splits.values():
        for train, test in folds.values():
            assert not set(key.iloc[train]) & set(key.iloc[test])
    fitted, sampled = protocol.fit_splits_to_budget(df, splits, RowBudget(train=200, test=40), group_on=["a", "b"])
    assert sampled
    for folds in fitted.values():
        for train, test in folds.values():
            assert not set(key.iloc[train]) & set(key.iloc[test])  # the sampled test sides keep combinations whole
    single, _ = protocol.one_group_column(df, "a")
    assert single is df  # one column: the frame and its splits are as before


def test_plain_cutoffs_apply_to_a_time_zone_aware_column() -> None:
    times = pd.date_range("2020-01-01", periods=400, freq="D", tz="Europe/Berlin")
    df = pd.DataFrame({"t": times, "x": np.arange(400)})
    splits = protocol.temporal_window_splits(df, time_on="t", window=1, unit="months", cutoffs=["2020-06", "2021-02"])
    assert df["t"].iloc[splits[0][0][1][0]] == pd.Timestamp("2021-02-01", tz="Europe/Berlin")
    assert df["t"].iloc[splits[1][0][1][0]] == pd.Timestamp("2020-06-01", tz="Europe/Berlin")


@pytest.mark.parametrize(
    ("unit", "window", "cutoffs"),
    [("months", 1, ["2020-03", "2020-06"]), ("unique", 30, ["2020-02-01", "2020-06-01"]), ("rows", 30, [100, 200])],
)
def test_cutoffs_must_test_the_newest_data(unit: str, window: int, cutoffs: list) -> None:
    df = pd.DataFrame({"t": pd.date_range("2020-01-01", periods=400, freq="D")})
    cutoffs = [pd.Timestamp(c) for c in cutoffs] if unit == "unique" else cutoffs
    with pytest.raises(ValueError, match="the newest window is always a test window"):
        protocol.temporal_window_splits(df, time_on="t", window=window, unit=unit, cutoffs=cutoffs)
    whole = protocol.temporal_window_splits(df, time_on="t", window=None, unit=unit, cutoffs=cutoffs)
    assert whole[0][0][1][-1] == len(df) - 1  # a window to the end of the data holds the newest row
