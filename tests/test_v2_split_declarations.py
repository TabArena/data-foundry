"""The declarative splits that replaced custom ``_make_splits`` (2026-11-26) and the additive splits comment.

* ``TemporalSplits(window=None, cutoffs=...)``: windows of unequal length, each running to the next start;
* ``Temporal(label_known_on=...)``: a train side keeps the rows whose label was known before its window;
* ``Temporal(exclude_test_entities_on=...)``: a train side keeps no row of an entity its window tests;
* ``grouped_splits = GroupedSplits(kind="leave_one_group_out")``: one fold per group, which the split checks accept;
* the splits comment: the generated description, then the definition's ``splits_comment``.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from data_foundry.checks.protocol import is_leave_one_group_out
from data_foundry.definition import (
    DatasetDefinitionError,
    GroupedSplits,
    Temporal,
    TemporalSplits,
    get_dataset,
)
from data_foundry.definition.report import read_report
from data_foundry.definition.splits import leave_one_group_out_splits
from tests.helpers import (
    DEFINITION,
    IMPORTS,
    load_definition_from_text,
    temporal_version_body,
    write_definition,
)

DAILY = pd.DataFrame({"t": pd.date_range("2024-01-01", periods=30, freq="D").repeat(2)})
"""60 rows over 30 days, two a day."""


# --- windows of unequal length ----------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("unit", "cutoffs"),
    [
        ("days", ("2024-01-26", "2024-01-21", "2024-01-11")),
        ("unique", tuple(pd.Timestamp(c) for c in ("2024-01-26", "2024-01-21", "2024-01-11"))),
        ("rows", (50, 40, 20)),
    ],
)
def test_windows_without_a_length_run_to_the_next_start(unit: str, cutoffs: tuple) -> None:
    splits = TemporalSplits(window=None, unit=unit, cutoffs=cutoffs).splits(DAILY, "t")
    sizes = [(len(f[0][0]), len(f[0][1])) for f in splits.values()]
    assert sizes == [(50, 10), (40, 10), (20, 20)]  # newest first; each window ends where the newer one starts
    tests = [set(f[0][1]) for f in splits.values()]
    assert not tests[0] & tests[1]
    assert not tests[1] & tests[2]
    assert max(splits[0][0][1]) == len(DAILY) - 1  # the newest runs to the end of the data


def test_windows_without_a_length_keep_their_gap() -> None:
    windows = TemporalSplits(window=None, unit="days", cutoffs=("2024-01-21", "2024-01-11"), gap=3)
    splits = windows.splits(DAILY, "t")
    assert [len(f[0][0]) for f in splits.values()] == [34, 14]  # every row before the start minus 3 days
    assert windows.horizon is None  # unequal windows set no horizon: `Temporal(horizon=...)` states it
    assert windows.gap_length == (3, "days")
    text = windows.describe(len(splits))
    assert "each from its start to the next start, the newest to the end of the data" in text
    assert "(starts: 2024-01-21, 2024-01-11)" in text
    assert "up to a gap of 3 days" in text


# --- train filters ----------------------------------------------------------------------------------------------------
def test_label_known_on_keeps_the_train_rows_whose_label_was_known() -> None:
    df = DAILY.assign(known=DAILY["t"] + pd.to_timedelta(np.arange(60) % 7, unit="D"), key=np.arange(60) % 5)
    df.loc[3, "known"] = pd.NaT  # never known: never trains
    temporal = Temporal(
        on="t", splits=TemporalSplits(window=5, unit="days", n_windows=3), label_known_on="known", horizon=None
    )
    for (train, test), (all_train, _) in zip(
        (f[0] for f in temporal.window_splits(df).values()),
        (f[0] for f in temporal.splits.splits(df, "t").values()),
        strict=True,
    ):
        start = df["t"].iloc[test].min()
        assert set(train) == {i for i in all_train if df["known"].iloc[i] < start}
        assert 3 not in train
    assert temporal.split_columns == ["known"]
    by_function = Temporal(on="t", splits=temporal.splits, label_known_on=lambda frame: frame["known"])
    assert by_function.window_splits(df) == temporal.window_splits(df)
    assert by_function.split_columns == []  # a function reads the frame; nothing to drop


def test_exclude_test_entities_on_drops_the_tested_entities_from_training() -> None:
    df = DAILY.assign(key=pd.Series(np.arange(60) % 7, dtype="float").where(np.arange(60) % 11 != 0))
    temporal = Temporal(
        on="t", splits=TemporalSplits(window=5, unit="days", n_windows=3), exclude_test_entities_on="key"
    )
    for folds, all_folds in zip(
        temporal.window_splits(df).values(), temporal.splits.splits(df, "t").values(), strict=True
    ):
        (train, test), (all_train, _) = folds[0], all_folds[0]
        tested = set(df["key"].iloc[test].dropna())
        assert tested  # the window tests entities, so the filter has something to drop
        # every earlier row whose key the window does not test, a missing key included (it matches nothing)
        assert set(train) == {i for i in all_train if df["key"].iloc[i] not in tested}
        assert df["key"].iloc[train].isna().sum() > 0
    sentence = temporal.describe_train_filters()
    assert sentence == " Each train side keeps no row of an entity of `key` that its window tests."


@pytest.mark.parametrize("zones", [("UTC", None), (None, "UTC"), ("UTC", "Europe/Berlin")])
def test_label_known_on_needs_the_time_zone_of_the_time_column(zones: tuple) -> None:
    on_zone, known_zone = zones
    df = pd.DataFrame({"t": DAILY["t"].dt.tz_localize(on_zone)})
    df["known"] = (DAILY["t"] + pd.Timedelta(days=1)).dt.tz_localize(known_zone)
    temporal = Temporal(on="t", splits=TemporalSplits(window=5, unit="days", n_windows=3), label_known_on="known")
    with pytest.raises(DatasetDefinitionError, match=r"`label_known_on` `known` .* the time column `t` .*cannot be"):
        temporal.window_splits(df)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"label_known_on": "known"}, "filter the train sides of declared windows"),
        ({"exclude_test_entities_on": "key", "horizon": 1, "horizon_unit": "days"}, "declared windows"),
        ({"splits": TemporalSplits(window=1, n_windows=3), "label_known_on": "t"}, "cannot also be"),
        ({"splits": TemporalSplits(window=1, n_windows=3), "exclude_test_entities_on": ""}, "names a column"),
    ],
)
def test_train_filters_need_declared_windows_and_their_own_column(kwargs: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        Temporal(on="t", **kwargs)


def test_a_definition_drops_its_split_columns_after_the_split(tmp_path: Path, warehouse: Path) -> None:
    del warehouse
    body = temporal_version_body(
        "toy_ds",
        windows='TemporalSplits(window=5, unit="days", n_windows=3), label_known_on="known", '
        'exclude_test_entities_on="key"',
    ).replace(
        '        return drop_columns(df, ["row_id"])',
        '        df["known"] = df["t"] + pd.to_timedelta(df["row_id"] % 9, unit="D")\n'
        '        df["key"] = df["row_id"] % 400\n'
        '        return drop_columns(df, ["row_id"])',
    )
    write_definition(tmp_path / "datasets", body=body)
    ds = get_dataset(tmp_path / "datasets", "toy_ds")
    assert {"known", "key"} <= set(ds.df.columns)
    plan = ds.make_splits()
    assert not {"known", "key"} & set(plan.df.columns)  # split inputs only, never model inputs
    frame = ds.df
    for folds, all_folds in zip(plan.splits.values(), ds.temporal.splits.splits(frame, "t").values(), strict=True):
        (train, test), (all_train, _) = folds[0], all_folds[0]
        start = frame["t"].iloc[test].min()
        tested = set(frame["key"].iloc[test])
        expected = {i for i in all_train if frame["known"].iloc[i] < start and frame["key"].iloc[i] not in tested}
        assert expected  # a train side the filters leave rows in
        assert set(train) == expected
    assert "Each train side keeps only the rows whose label was known (by `known`) before its window starts" in (
        plan.comment
    )


# --- leave one group out ----------------------------------------------------------------------------------------------
GROUPED = (
    '    grouping = Grouping(on="site", labels="per_sample", definition="""\n'
    "        One group is a toy site.\n"
    '    """)\n'
    '    grouped_splits = GroupedSplits(kind="leave_one_group_out")\n'
)


def grouped_body(extra: str = GROUPED) -> str:
    return (
        DEFINITION.format(name="toy_ds", comment="Toy data.")
        .replace(IMPORTS, IMPORTS.replace("Metric,", "GroupedSplits, Grouping, Metric,"))
        .replace('    target = "y"\n', f'{extra}    target = "y"\n')
        .replace(
            '        return drop_columns(df, ["row_id"])',
            '        df["site"] = pd.Categorical(\n'
            '            (df["row_id"] % 3).map({0: "north", 1: "south", 2: "east"}),\n'
            '            categories=["south", "north", "east"],\n'
            "        )\n"
            '        return drop_columns(df, ["row_id"])',
        )
    )


@pytest.mark.parametrize("on", ['"site"', '["site"]'])
def test_leave_one_group_out_tests_each_group_once_in_category_order(tmp_path: Path, warehouse: Path, on: str) -> None:
    del warehouse
    write_definition(tmp_path / "datasets", body=grouped_body(GROUPED.replace('on="site"', f"on={on}")))
    ds = get_dataset(tmp_path / "datasets", "toy_ds")
    plan = ds.make_splits()
    site = plan.df["site"].astype(str)
    assert list(plan.splits) == [0]
    assert [site.iloc[test].unique().tolist() for _train, test in plan.splits[0].values()] == [
        ["south"],
        ["north"],
        ["east"],
    ]
    for train, test in plan.splits[0].values():
        assert len(train) + len(test) == len(plan.df)
    opening = "Leave one group out: one repeat of 3 folds, fold i testing the i-th group of `site` "
    assert plan.comment.startswith(opening)
    assert "(south, north, east)" in plan.comment


def test_the_split_checks_accept_a_declared_leave_one_group_out(tmp_path: Path, warehouse: Path) -> None:
    """One repeat of one fold per group is the declared pattern: no `splits_dimensions_off_protocol` to accept."""
    del warehouse
    write_definition(tmp_path / "datasets", body=grouped_body())
    result = get_dataset(tmp_path / "datasets", "toy_ds").check(write_report=False, verbose=False)
    assert "splits_dimensions_off_protocol" not in result.bundle_report.slugs
    splits = result.container.experiment_metadata.splits
    frame = result.container.dataset
    assert is_leave_one_group_out(frame, splits, "site")
    one_fold_short = {0: dict(list(splits[0].items())[:2])}
    assert not is_leave_one_group_out(frame, one_fold_short, "site")  # a group never tested
    halves = {0: {0: (list(range(300)), list(range(300, 600))), 1: (list(range(300, 600)), list(range(300)))}}
    assert not is_leave_one_group_out(frame, halves, "site")  # a test side of several groups


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        ('    grouped_splits = GroupedSplits(kind="leave_one_group_out")\n', "declare `grouping = Grouping"),
        ('    grouped_splits = "leave_one_group_out"\n', "must be a `GroupedSplits"),
    ],
)
def test_grouped_splits_need_a_grouping_and_their_declaration(extra: str, message: str) -> None:
    body = (
        DEFINITION.format(name="toy_logo", comment="x")
        .replace(IMPORTS, IMPORTS.replace("Metric,", "GroupedSplits, Metric,"))
        .replace('    target = "y"\n', f'{extra}    target = "y"\n')
    )
    with pytest.raises(DatasetDefinitionError, match=message):
        load_definition_from_text(body, "toy_logo")


def test_grouped_splits_know_one_kind() -> None:
    with pytest.raises(ValueError, match="is not one of"):
        GroupedSplits(kind="leave_two_out")


def test_leave_one_group_out_splits_sort_plain_values() -> None:
    df = pd.DataFrame({"g": ["b", "a", "c", "a"]})
    splits, groups = leave_one_group_out_splits(df, "g")
    assert groups == ["a", "b", "c"]
    assert splits[0][0] == ([0, 2], [1, 3])
    assert leave_one_group_out_splits(df, ["g"]) == (splits, groups)  # a one-column list is the column


# --- the splits comment -----------------------------------------------------------------------------------------------
def test_the_splits_comment_is_the_description_then_the_reason(tmp_path: Path, warehouse: Path) -> None:
    del warehouse
    body = temporal_version_body("toy_ds").replace(
        '    target = "y"\n', '    splits_comment = "A weekly refit, as the source does."\n    target = "y"\n'
    )
    folder = write_definition(tmp_path / "datasets", body=body)
    ds = get_dataset(tmp_path / "datasets", "toy_ds")
    comment = ds.make_splits().comment
    description, reason = comment.split("\n\n")
    assert description.startswith("Expanding-window temporal splits: 3 test window(s) of 5 days")
    assert "The test windows by `t`, as listed: 2024-01-26 to 2024-01-30 (100 test, 500 train rows);" in description
    assert reason == "A weekly refit, as the source does."
    ds.check(verbose=False)
    assert read_report(folder / "README.md")["splits"]["reason"] == reason  # the review page reads it from here


def test_custom_splits_get_a_description_read_off_the_splits(tmp_path: Path, warehouse: Path) -> None:
    del warehouse
    body = DEFINITION.format(name="toy_ds", comment="Toy data.").replace(
        "    def _feature_types(",
        '    splits_comment = "Half and half, on purpose."\n\n'
        "    def _make_splits(self, df: pd.DataFrame) -> dict:\n"
        "        half = len(df) // 2\n"
        "        return {0: {0: (list(range(half)), list(range(half, len(df))))}}\n\n"
        "    def _feature_types(",
    )
    write_definition(tmp_path / "datasets", body=body)
    comment = get_dataset(tmp_path / "datasets", "toy_ds").make_splits().comment
    assert comment == "Custom splits (`_make_splits`): 1 repeat(s) x 1 folds, 1 splits.\n\nHalf and half, on purpose."
