"""Tests for the time-recovery probe (``curation_probes.time_recovery``) and its command-line rendering."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("scipy")

REPO = Path(__file__).resolve().parents[1]
LIBRARY = REPO / ".claude" / "skills" / "knowledge-curation" / "scripts"
SCRIPTS = REPO / ".claude" / "skills" / "knowledge-data-foundry" / "scripts"


@pytest.fixture(scope="module")
def probe():
    """``curation_probes.time_recovery``, with the library folder on the path."""
    if str(LIBRARY) not in sys.path:
        sys.path.insert(0, str(LIBRARY))
    return importlib.import_module("curation_probes.time_recovery")


def _frame(n: int = 2000, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({"x1": rng.normal(size=n), "x2": rng.integers(0, 5, n), "y": rng.integers(0, 2, n)})


def test_a_shuffled_table_raises_no_flag(probe):
    """A shuffled table raises no flag."""
    result = probe.check_frame(_frame(), "y", "binary_classification")
    assert result["flags"] == []


def test_a_date_column_is_found(probe):
    """A date column is found."""
    df = _frame()
    df["visit_date"] = pd.date_range("2020-01-01", periods=len(df), freq="h")
    df["admission_year"] = 2015
    df.loc[: len(df) // 2, "admission_year"] = 2016
    result = probe.check_frame(df, "y", "binary_classification")
    assert {"visit_date", "admission_year"} <= set(result["time_columns"])
    assert "time_column" in result["flags"]


@pytest.mark.parametrize(
    ("name", "is_time"),
    [
        ("visit_date", True),
        ("period", True),
        ("Month", True),
        ("year_of_sale", True),
        ("duration_months", False),
        ("age_years", False),
        ("age_in_days", False),
        ("capillary_refill_time", False),
        ("default payment next month", False),
        ("stage", False),
    ],
)
def test_names_that_say_a_time_and_names_that_say_a_duration(probe, name, is_time):
    """Names that say a time and names that say a duration."""
    series = pd.Series(["a", "b"] * 5)
    assert (probe._is_time_like(name, series) is not None) is is_time


def test_a_dropped_raw_date_is_found(probe):
    """A dropped raw date is found."""
    df = _frame()
    raw = df.assign(Date=pd.date_range("2001-01-01", periods=len(df), freq="D").astype(str))
    raw["Date"] = pd.to_datetime(raw["Date"])
    result = probe.check_frame(df, "y", "binary_classification", raw=raw)
    assert "Date" in result["dropped_time_columns"]
    assert "time_dropped" in result["flags"]


def test_a_file_sorted_by_class_is_not_a_clock(probe):
    """A file sorted by class is not a clock."""
    df = _frame().sort_values("y", kind="stable").reset_index(drop=True)
    result = probe.check_frame(df, "y", "binary_classification")
    assert "order_drift" not in result["flags"]
    assert "sorted_by_target" in result["flags"]


def test_a_few_valued_lab_value_is_not_a_period(probe):
    """A few valued lab value is not a period."""
    df = _frame(300)
    rng = np.random.default_rng(6)
    df["creatinine"] = np.round(rng.choice(np.linspace(0.5, 4.4, 39), len(df)), 2)
    df["y"] = (df["creatinine"] > 2).astype(int)
    assert "period_values" not in probe.check_frame(df, "y", "binary_classification")["flags"]


def test_a_target_drifting_with_the_order_is_flagged(probe):
    """A target drifting with the order is flagged."""
    df = _frame()
    rng = np.random.default_rng(1)
    df["y"] = (rng.random(len(df)) < np.linspace(0.05, 0.6, len(df))).astype(int)
    result = probe.check_frame(df, "y", "binary_classification")
    assert "order_drift" in result["flags"]


def test_the_raw_order_is_used_when_rows_are_traced(probe):
    """The raw order is used when rows are traced."""
    df = _frame()
    rng = np.random.default_rng(2)
    rate = np.linspace(0.05, 0.6, len(df))
    raw_rows = rng.permutation(len(df))  # the frame is shuffled; the raw order is the time order
    df["y"] = (rng.random(len(df)) < rate[raw_rows]).astype(int)
    result = probe.check_frame(df, "y", "binary_classification", raw_rows=raw_rows)
    assert result["order_source"] == "raw"
    assert "order_drift" in result["flags"]


def test_an_id_handed_out_in_sequence_is_flagged(probe):
    """An id handed out in sequence is flagged."""
    df = _frame()
    rng = np.random.default_rng(3)
    df["encounter_id"] = rng.permutation(len(df)) * 7 + 1000
    rate = np.interp(df["encounter_id"], [df["encounter_id"].min(), df["encounter_id"].max()], [0.05, 0.6])
    df["y"] = (rng.random(len(df)) < rate).astype(int)
    result = probe.check_frame(df, "y", "binary_classification")
    assert "encounter_id" in result["id_orders"]
    assert "id_drift" in result["flags"]


def test_an_amount_is_not_an_id(probe):
    """An amount is not an id."""
    df = _frame()
    df["credit_amount"] = np.random.default_rng(7).permutation(len(df)) * 3 + 250  # unique, but not in row order
    df["y"] = (df["credit_amount"] > df["credit_amount"].median()).astype(int)
    assert "credit_amount" not in probe.check_frame(df, "y", "binary_classification")["id_orders"]


def test_a_dropped_id_is_read_from_the_raw_table(probe):
    """A dropped id is read from the raw table."""
    df = _frame()
    rng = np.random.default_rng(8)
    raw_rows = rng.permutation(len(df))
    raw = df.iloc[np.argsort(raw_rows)].reset_index(drop=True)
    raw["record_no"] = rng.permutation(len(df)) + 840000
    record = raw["record_no"].to_numpy()[raw_rows]
    rate = np.interp(record, [record.min(), record.max()], [0.05, 0.6])
    df["y"] = (rng.random(len(df)) < rate).astype(int)
    result = probe.check_frame(df, "y", "binary_classification", raw=raw.drop(columns="y"), raw_rows=raw_rows)
    assert "record_no (dropped)" in result["id_orders"]
    assert "id_drift" in result["flags"]


def test_macro_figures_that_encode_the_period_are_flagged(probe):
    """Macro figures that encode the period are flagged."""
    df = _frame(3000)
    rng = np.random.default_rng(4)
    year = rng.integers(0, 6, len(df))
    df["unemployment"] = np.array([10.8, 13.9, 9.4, 16.2, 15.5, 12.4])[year]
    df["inflation"] = np.array([1.4, -0.3, 2.6, 0.5, 3.7, 0.6])[year]
    df["y"] = (rng.random(len(df)) < np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])[year]).astype(int)
    result = probe.check_frame(df, "y", "binary_classification")
    assert result["period_values"]["columns"] == ["unemployment", "inflation"]
    assert result["period_values"]["levels"] == 6
    assert "period_values" in result["flags"]


def test_a_regression_target_drifting_with_the_order_is_flagged(probe):
    """A regression target drifting with the order is flagged."""
    df = _frame()
    rng = np.random.default_rng(5)
    df["y"] = np.linspace(0, 3, len(df)) + rng.normal(size=len(df))
    result = probe.check_frame(df, "y", "regression")
    assert "order_drift" in result["flags"]


def test_the_command_line_renders_one_line(probe):
    """The command line renders one line."""
    spec = importlib.util.spec_from_file_location("time_probes_cli", SCRIPTS / "time_probes.py")
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = {"name": "toy", "regime": "iid"} | probe.check_frame(_frame(), "y", "binary_classification")
    line = module.render(result)
    assert line.startswith("toy (iid, 2000 rows)")
    assert "flags []" in line
    assert module.render({"name": "t", "skipped": "temporal split"}) == "t: skipped (temporal split)"
