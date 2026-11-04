"""The raw state: the lineage of ``process(lineage=True)``, the raw table in ``dataset_io``, and the probes that read
it (10, 19, 20, 21) with ``leak_probes.py --raw``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from data_foundry.v2 import get_dataset

from tests.test_v2_dataset import DEFINITION, warehouse, write_definition  # noqa: F401 - the fixture is used by name

pytest.importorskip("lightgbm")  # curation_probes.leak imports it

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude/skills/knowledge-data-foundry/scripts"
sys.path.insert(0, str(SCRIPTS.parents[1] / "knowledge-curation/scripts"))
sys.path.insert(0, str(SCRIPTS))

import dataset_io  # noqa: E402 - from the skill's script folder, put on the path above
from curation_probes import leak  # noqa: E402

PLAIN_CLEAN = '        return drop_columns(df, ["row_id"])'


def _toy(tmp_path: Path, clean: str = PLAIN_CLEAN):
    """The toy definition of the dataset tests, with its last ``_clean`` line replaced by ``clean``."""
    body = DEFINITION.format(name="toy_ds", comment="x")
    assert PLAIN_CLEAN in body
    write_definition(tmp_path / "datasets", body=body.replace(PLAIN_CLEAN, clean))
    return get_dataset(tmp_path / "datasets", "toy_ds")


def _assert_traced(ds, df: pd.DataFrame, rows: np.ndarray) -> None:
    """The traced rows carry the raw values: every curated row's x1 is the raw x1 at its position."""
    assert df.equals(ds.df)
    np.testing.assert_array_equal(df["x1"].to_numpy(), ds.raw["x1"].to_numpy()[rows])


# Lineage


def test_lineage_by_the_column_through_a_row_filter_and_the_shuffle(tmp_path, warehouse) -> None:  # noqa: F811
    """A row filter and the shuffle keep the column trace: each row maps to its raw row."""
    del warehouse
    ds = _toy(tmp_path, '        df = df.loc[df["x1"] > -1]\n' + PLAIN_CLEAN)
    df, test, lineage = ds.process(lineage=True)
    assert test is None
    assert lineage.note == "traced by the column"
    assert len(lineage.rows) == len(df) < len(ds.raw)
    _assert_traced(ds, df, lineage.rows)
    assert "__raw_row__" not in df.columns


def test_lineage_by_the_index_when_clean_selects_columns(tmp_path, warehouse) -> None:  # noqa: F811
    """A `_clean` that selects columns drops the tag column; the index trace takes over."""
    del warehouse
    ds = _toy(tmp_path, '        return df.loc[df["x1"] < 1, ["x1", "colour", "y"]]')
    df, _test, lineage = ds.process(lineage=True)
    assert lineage.note == "traced by the index"
    _assert_traced(ds, df, lineage.rows)


def test_a_trace_that_changes_what_clean_returns_is_not_used(tmp_path, warehouse) -> None:  # noqa: F811
    """A `_clean` that reads the number of columns gives another frame with the tag column: the index trace is used."""
    del warehouse
    ds = _toy(tmp_path, '        df["n_cols"] = float(df.shape[1])\n' + PLAIN_CLEAN)
    df, _test, lineage = ds.process(lineage=True)
    assert lineage.note == "traced by the index"
    _assert_traced(ds, df, lineage.rows)


def test_no_lineage_when_clean_drops_the_column_and_resets_the_index(tmp_path, warehouse) -> None:  # noqa: F811
    """Neither trace survives: no lineage, the reason given, the dataset unchanged."""
    del warehouse
    ds = _toy(tmp_path, '        return df.loc[df["x1"] < 1, ["x1", "colour", "y"]].reset_index(drop=True)')
    df, _test, lineage = ds.process(lineage=True)
    assert lineage.rows is None
    assert "column does not survive" in lineage.note
    assert "index does not survive" in lineage.note
    assert df.equals(ds.df)  # the dataset itself is unchanged
    data = dataset_io.from_definition(ds, raw=True)
    assert data.raw is not None
    assert data.raw_rows is None
    assert data.raw_note == lineage.note


def test_process_without_lineage_is_unchanged(tmp_path, warehouse) -> None:  # noqa: F811
    """`process()` without lineage returns the dataset and the test frame as before."""
    del warehouse
    ds = _toy(tmp_path)
    df, test = ds.process()
    assert test is None
    assert df.equals(ds.df)


def test_from_definition_gives_the_raw_table_and_the_rows(tmp_path, warehouse) -> None:  # noqa: F811
    """`from_definition(raw=True)` gives the raw table and each row's raw position; the default gives none."""
    del warehouse
    ds = _toy(tmp_path, '        df = df.loc[df["x1"] > -1]\n' + PLAIN_CLEAN)
    data = dataset_io.from_definition(ds, raw=True)
    assert data.raw.shape == ds.raw.shape
    assert data.raw_note == "traced by the column"
    np.testing.assert_array_equal(data.df["x1"].to_numpy(), data.raw["x1"].to_numpy()[data.raw_rows])
    assert dataset_io.from_definition(ds).raw is None  # the raw state only on request


def test_row_positions_follow_a_subsampled_split_frame() -> None:
    """The positions follow a split frame sub-sampled in order, and refuse a reordered one."""
    rng = np.random.default_rng(1)
    processed = pd.DataFrame({"a": rng.integers(0, 3, 200), "b": rng.normal(size=200)})
    keep = np.sort(rng.choice(200, 80, replace=False))
    frame = processed.iloc[keep].reset_index(drop=True)
    np.testing.assert_array_equal(dataset_io._row_positions(frame, processed), keep)
    np.testing.assert_array_equal(dataset_io._row_positions(processed, processed), np.arange(200))
    assert dataset_io._row_positions(frame.iloc[::-1].reset_index(drop=True), processed) is None


# The probes


def test_row_order_flags_a_sorted_target_and_not_a_shuffled_one() -> None:
    """Probe 10 flags a target sorted in the raw order, not a shuffled one."""
    rng = np.random.default_rng(2)
    y = pd.Series(rng.choice(["a", "b", "c"], 3000))
    shuffled = leak.row_order(y, "multiclass_classification")
    assert not shuffled["flag"]
    assert abs(shuffled["next_row_match"] - shuffled["chance"]) < 0.05
    ordered = leak.row_order(y.sort_values().reset_index(drop=True), "multiclass_classification")
    assert ordered["flag"]
    assert ordered["next_row_match"] > 0.99
    numbers = pd.Series(rng.normal(size=2000))
    assert not leak.row_order(numbers, "regression")["flag"]
    assert leak.row_order(numbers.sort_values().reset_index(drop=True), "regression")["spearman_position"] > 0.99


def test_removed_rows_compare_the_target_of_removed_and_kept_rows() -> None:
    """Probe 19 compares the target of the removed rows with the kept ones."""
    y = pd.Series(["no"] * 80 + ["yes"] * 20)
    kept = np.ones(100, dtype=bool)
    kept[80:95] = False  # 15 of the 20 positives removed
    out = leak.removed_rows(y, kept, "binary_classification")
    assert (out["raw_rows"], out["kept"], out["removed"]) == (100, 85, 15)
    assert out["removed_shares"] == {"yes": 1.0}
    assert out["flag"]
    values = pd.Series(np.r_[np.zeros(90), np.full(10, 100.0)])
    kept = np.r_[np.ones(90, dtype=bool), np.zeros(10, dtype=bool)]
    out = leak.removed_rows(values, kept, "regression")
    assert out["removed_median"] == 100.0
    assert out["flag"]
    assert leak.removed_rows(None, kept, "regression") == {"raw_rows": 100, "kept": 90, "removed": 10}


def test_raw_copies_count_groups_and_label_conflicts_without_identifiers() -> None:
    """Probe 21 counts copy groups and label conflicts, with identifier columns left out."""
    raw = pd.DataFrame(
        {
            "id": np.arange(8),
            "a": [1, 1, 1, 2, 2, 3, 4, 4],
            "b": ["x", "x", "x", "y", "y", "z", "w", "w"],
            "y": [0, 0, 1, 1, 1, 0, 0, 0],
        }
    )
    out = leak.raw_copies(raw, "y")
    assert out["identifiers_left_out"] == ["id"]
    assert (out["rows_with_input_copy"], out["copy_groups"], out["groups_with_several_labels"]) == (7, 3, 1)
    assert out["full_row_copies"] == 0  # the id makes every full row unique
    assert leak.raw_copies(raw.drop(columns="id"), "y")["full_row_copies"] == 3


def test_a_dropped_copy_of_the_target_scores_high_alone() -> None:
    """Probe 20 scores a dropped copy of the target near 1 alone, noise near chance."""
    rng = np.random.default_rng(3)
    y = pd.Series(rng.choice(["no", "yes"], 600))
    columns = pd.DataFrame(
        {"outcome_code": y.map({"no": "N", "yes": "Y"}), "noise": rng.normal(size=600), "when": pd.Timestamp(0)}
    )
    pairs = [(np.arange(0, 400), np.arange(400, 600))]
    out = leak.dropped_column_proxies(columns, y, pairs, regression=False, n_jobs=1)
    assert next(iter(out["scores"])) == "outcome_code"
    assert out["scores"]["outcome_code"] > 0.99
    assert out["scores"]["noise"] < 0.7
    assert out["skipped"] == 0
    lines = leak.raw_lines({"dropped_columns": out, "raw_copies": leak.raw_copies(columns, None)})
    assert lines[0].startswith("each dropped raw column alone (probe 20)")


def test_the_cli_runs_the_raw_state_alone(tmp_path, warehouse, capsys) -> None:  # noqa: F811
    """`leak_probes.py --raw` runs the probes of the raw state and no model probe."""
    del warehouse
    _toy(tmp_path, '        df = df.loc[df["x1"] > -1]\n' + PLAIN_CLEAN)
    spec = importlib.util.spec_from_file_location("leak_probes_cli", SCRIPTS / "leak_probes.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    assert cli.main(["toy_ds", "--root", str(tmp_path / "datasets"), "--raw", "--splits", "1", "--n-jobs", "1"]) == 0
    out = capsys.readouterr().out
    assert "lineage: traced by the column" in out
    assert "row order (probe 10)" in out
    assert "rows `_clean` removed (probe 19)" in out
    assert "each dropped raw column alone (probe 20): {'row_id'" in out
    assert "raw copies (probe 21)" in out
    assert "all features:" not in out  # no model probes with --raw
