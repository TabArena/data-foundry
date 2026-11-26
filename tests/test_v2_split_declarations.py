"""The declarative splits that replaced custom ``_make_splits`` (2026-11-26) and the additive splits comment.

* ``TemporalSplits(window=None, cutoffs=...)``: windows of unequal length, each running to the next start;
* ``Temporal(label_known_on=...)``: a train side keeps the rows whose label was known before its window;
* ``Temporal(exclude_test_entities_on=...)``: a train side keeps no row of an entity its window tests;
* ``leave_one_group_out = True``: one fold per group;
* the splits comment: the generated description, then the definition's ``splits_comment``.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from data_foundry.definition import (
    DatasetDefinitionError,
    Temporal,
    TemporalSplits,
    get_dataset,
    splits as protocol,
)
from data_foundry.definition.dataset import splits_reason
from data_foundry.schema import DATA_FOUNDRY_WAREHOUSE_ENV
from tests.test_v2_dataset import (
    DEFINITION,
    IMPORTS,
    load_definition_from_text,
    temporal_version_body,
    write_definition,
)


@pytest.fixture
def warehouse(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A temporary warehouse holding the toy raw file of ``tests.test_v2_dataset``: 600 rows."""
    root = tmp_path / "warehouse"
    rng = np.random.default_rng(0)
    raw = pd.DataFrame(
        {
            "row_id": np.arange(600),
            "x1": rng.normal(size=600),
            "colour": rng.choice(["red", "green", "blue"], size=600),
            "y": rng.integers(0, 2, size=600),
        },
    )
    (root / "toy_ds").mkdir(parents=True)
    raw.to_csv(root / "toy_ds" / "toy.csv", index=False)
    monkeypatch.setenv(DATA_FOUNDRY_WAREHOUSE_ENV, str(root))
    return root


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
    for folds in temporal.window_splits(df).values():
        train, test = folds[0]
        tested = set(df["key"].iloc[test].dropna())
        assert not tested & set(df["key"].iloc[train].dropna())
        assert df["key"].iloc[train].isna().sum() > 0  # a missing key matches nothing and keeps training
    sentence = temporal.describe_train_filters()
    assert sentence == " Each train side keeps no row of an entity of `key` that its window tests."


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
        '        df["key"] = df["row_id"] % 40\n'
        '        return drop_columns(df, ["row_id"])',
    )
    write_definition(tmp_path / "datasets", body=body)
    ds = get_dataset(tmp_path / "datasets", "toy_ds")
    assert {"known", "key"} <= set(ds.df.columns)
    plan = ds.make_splits()
    assert not {"known", "key"} & set(plan.df.columns)  # split inputs only, never model inputs
    for folds in plan.splits.values():
        train, test = folds[0]
        start = ds.df["t"].iloc[test].min()
        assert (ds.df["known"].iloc[train] < start).all()
        assert not set(ds.df["key"].iloc[train]) & set(ds.df["key"].iloc[test])
    assert "Each train side keeps only the rows whose label was known (by `known`) before its window starts" in (
        plan.comment
    )


# --- leave one group out ----------------------------------------------------------------------------------------------
GROUPED = (
    '    grouping = Grouping(on="site", labels="per_sample", definition="""\n'
    "        One group is a toy site.\n"
    '    """)\n'
    "    leave_one_group_out = True\n"
)


def grouped_body(extra: str = GROUPED) -> str:
    return (
        DEFINITION.format(name="toy_ds", comment="Toy data.")
        .replace(IMPORTS, IMPORTS.replace("Metric,", "Grouping, Metric,"))
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


def test_leave_one_group_out_tests_each_group_once_in_category_order(tmp_path: Path, warehouse: Path) -> None:
    del warehouse
    write_definition(tmp_path / "datasets", body=grouped_body())
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
    assert plan.comment.startswith("Leave one group out: one repeat of 3 folds")
    assert "(south, north, east)" in plan.comment


def test_leave_one_group_out_needs_a_grouping() -> None:
    body = DEFINITION.format(name="toy_logo", comment="x").replace(
        '    target = "y"\n', '    leave_one_group_out = True\n    target = "y"\n'
    )
    with pytest.raises(DatasetDefinitionError, match="leave_one_group_out"):
        load_definition_from_text(body, "toy_logo")


def test_leave_one_group_out_splits_sort_plain_values() -> None:
    df = pd.DataFrame({"g": ["b", "a", "c", "a"]})
    splits, groups = protocol.leave_one_group_out_splits(df, "g")
    assert groups == ["a", "b", "c"]
    assert splits[0][0] == ([0, 2], [1, 3])


# --- the splits comment -----------------------------------------------------------------------------------------------
def test_the_splits_comment_is_the_description_then_the_reason(tmp_path: Path, warehouse: Path) -> None:
    del warehouse
    body = temporal_version_body("toy_ds").replace(
        '    target = "y"\n', '    splits_comment = "A weekly refit, as the source does."\n    target = "y"\n'
    )
    write_definition(tmp_path / "datasets", body=body)
    comment = get_dataset(tmp_path / "datasets", "toy_ds").make_splits().comment
    description, reason = comment.split("\n\n")
    assert description.startswith("Expanding-window temporal splits: 3 test window(s) of 5 days")
    assert "The test windows by `t`, as listed: 2024-01-26 to 2024-01-30 (100 test, 500 train rows);" in description
    assert reason == "A weekly refit, as the source does."
    assert splits_reason(comment) == reason


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


@pytest.mark.parametrize(
    ("comment", "reason"),
    [
        ("Default splits.", ""),
        ("Repeated 3-fold cross-validation over the rows: 3 repeat(s) x 3 folds.", ""),
        ("Leave one group out: one repeat of 3 folds.\n\nThree hospitals.\n\nMore.", "Three hospitals.\n\nMore."),
        ("A hand-written comment of a README built before.", "A hand-written comment of a README built before."),
    ],
)
def test_splits_reason_drops_the_generated_description(comment: str, reason: str) -> None:
    assert splits_reason(comment) == reason
