"""Tests for the time-recovery probe (``curation_probes.time_recovery``) and its command-line rendering."""

from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from data_foundry.collections import CollectionEntry, DatasetCollection, LocalWarehouseSource
from data_foundry.examples import get_toy_container_path

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
        ("order_dt", True),
    ],
)
def test_names_that_say_a_time_and_names_that_say_a_duration(probe, name, is_time):
    """Names that say a time and names that say a duration."""
    series = pd.Series(["a", "b"] * 5)
    assert (probe._is_time_like(name, series) is not None) is is_time


@pytest.mark.parametrize(
    ("name", "values", "is_time"),
    [
        ("edge_dt", [30.0, 46.0, 63.0, 95.0, 146.0], False),  # a solver metric: dt as a delta t
        ("three_year_gross_profit_to_total_assets", [0.02, 0.16, -1.3, 0.35, 2.1], False),  # a ratio
        ("transaction_date", [2012.917, 2013.5, 2012.25, 2013.0, 2012.75], True),  # a fractional year
        ("wave", [1, 2, 3, 1, 2], True),
    ],
)
def test_a_time_word_on_numbers_that_cannot_be_a_time(probe, name, values, is_time):
    """A time word on numbers that cannot be a time (fractions outside 1900-2100, ``dt`` on numbers) does not count."""
    assert (probe._is_time_like(name, pd.Series(values)) is not None) is is_time


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
    assert "class_block_drift" not in result["flags"]


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


def _panel(companies: int = 80, years: int = 40, seed: int = 10) -> pd.DataFrame:
    """Company-years stored year block by year block: each company's ratios move little from one year to the next."""
    rng = np.random.default_rng(seed)
    base = rng.normal(size=(companies, 12))
    weak = rng.random(companies) < 0.06  # these companies are bankrupt in most years
    rows = []
    for _year in range(years):
        ratios = base + rng.normal(scale=0.1, size=base.shape)
        bankrupt = np.where(weak, rng.random(companies) < 0.8, rng.random(companies) < 0.01)
        rows.append(np.column_stack([ratios, bankrupt.astype(int)]))
    df = pd.DataFrame(np.vstack(rows), columns=[f"ratio_{i}" for i in range(12)] + ["y"])
    df["y"] = df["y"].astype(int)
    return df


def test_rows_that_repeat_one_block_later_are_flagged(probe):
    """Rows that repeat one block later are flagged, with the block length and the target one block later."""
    result = probe.check_frame(_panel(), "y", "binary_classification")
    blocks = result["periodic_blocks"]
    assert "periodic_blocks" in result["flags"]
    assert blocks["lag"] == 80
    assert blocks["target"]["same_class_one_block"] > blocks["target"]["same_class_half_block"] + 0.2


def test_shuffled_company_years_have_no_period(probe):
    """Shuffled company-years have no period, and neither does a file sorted by one feature."""
    df = _panel().sample(frac=1, random_state=0).reset_index(drop=True)
    assert "periodic_blocks" not in probe.check_frame(df, "y", "binary_classification")["flags"]
    by_ratio = df.sort_values("ratio_0").reset_index(drop=True)
    assert "periodic_blocks" not in probe.check_frame(by_ratio, "y", "binary_classification")["flags"]


def _admissions(patients: int = 3000, seed: int = 11) -> pd.DataFrame:
    """A patient's admissions in consecutive rows: age and sex repeat, the episode goes up by one, a death ends the
    run.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for _patient in range(patients):
        age, sex = int(rng.integers(20, 90)), rng.choice(["Male", "Female"])
        for episode in range(1, int(rng.choice([1, 1, 1, 2, 2, 3, 4])) + 1):
            dead = rng.random() < 0.08
            rows.append({"age": age, "sex": sex, "episode": episode, "outcome": "Dead" if dead else "Alive"})
            age += int(rng.random() < 0.2)
            if dead:
                break
    return pd.DataFrame(rows)


def test_one_patients_admissions_in_consecutive_rows_are_flagged(probe):
    """One patient's admissions in consecutive rows are flagged, with the deaths on a run's last row."""
    df = _admissions()
    result = probe.check_frame(df, "outcome", "binary_classification")
    runs = result["entity_runs"]
    assert "entity_runs" in result["flags"]
    assert runs["counter"] == "episode"
    assert set(runs["fixed_fields"]) == {"age", "sex"}
    assert runs["runs_from_start"] == 3000
    assert runs["class_on_last_row"]["Dead"] == 1.0
    assert runs["class_on_last_row"]["Alive"] < runs["last_row_share"]


def test_shuffled_admissions_and_a_visit_count_are_not_runs(probe):
    """Shuffled admissions are not runs, and neither is a count that has no order."""
    df = _admissions().sample(frac=1, random_state=0).reset_index(drop=True)
    assert "entity_runs" not in probe.check_frame(df, "outcome", "binary_classification")["flags"]
    counts = _frame()
    counts["children"] = np.random.default_rng(12).integers(0, 5, len(counts))
    assert "entity_runs" not in probe.check_frame(counts, "y", "binary_classification")["flags"]


def _two_sources(seed: int = 13) -> pd.DataFrame:
    """A file sorted by class whose 'Yes' block is two collections put one after the other."""
    rng = np.random.default_rng(seed)
    no = rng.random((1500, 20)) < 0.3
    yes = np.vstack([rng.random((700, 20)) < 0.15, rng.random((700, 20)) < 0.55])
    columns = [f"permission_{i}" for i in range(20)]
    df = pd.DataFrame(np.vstack([no, yes]).astype(int), columns=columns).astype("category")
    df["y"] = ["No"] * 1500 + ["Yes"] * 1400
    return df


def test_a_class_block_of_two_collections_is_flagged(probe):
    """A class block made of two collections is flagged on top of the sorted order."""
    result = probe.check_frame(_two_sources(), "y", "binary_classification")
    assert {"sorted_by_target", "class_block_drift"} <= set(result["flags"])
    assert result["class_block_drift"]["Yes"]["drifting"] == 20
    assert result["class_block_drift"]["No"]["drifting"] == 0


def test_a_class_block_of_one_collection_is_not_flagged(probe):
    """A class-sorted file whose blocks are each one collection raises ``sorted_by_target`` alone."""
    df = _two_sources()
    df.iloc[1500:] = df.iloc[1500:].sample(frac=1, random_state=0).to_numpy()  # mix the two collections
    result = probe.check_frame(df, "y", "binary_classification")
    assert "sorted_by_target" in result["flags"]
    assert "class_block_drift" not in result["flags"]


def test_a_class_block_sorted_by_one_feature_is_one_piece(probe):
    """A class block sorted by one feature (donors by age) drifts, names the sort, and raises no flag."""
    rng = np.random.default_rng(14)
    age = rng.integers(20, 80, 2000)
    creatinine = age * 0.02 + rng.normal(size=2000)
    df = pd.DataFrame({"age": age, "creatinine": creatinine, "y": ["No"] * 1200 + ["Yes"] * 800})
    df.iloc[:1200] = df.iloc[:1200].sort_values("age").to_numpy()
    result = probe.check_frame(df, "y", "binary_classification")
    assert result["class_block_drift"]["No"]["drifting"] == 2
    assert result["class_block_drift"]["No"]["sorted_by"] == ["age"]
    assert "class_block_drift" not in result["flags"]


def test_a_column_of_few_values_in_long_runs_sorts_a_block(probe):
    """Sex in two long runs sorts a block; the same values shuffled, or a code on too few rows, do not."""
    rng = np.random.default_rng(0)
    runs = pd.Series(["f"] * 300 + ["m"] * 300)
    assert probe._sorts_by_level(runs)
    assert not probe._sorts_by_level(runs.sample(frac=1, random_state=0).reset_index(drop=True))
    rare = pd.Series(["a"] * 590 + ["b"] * 10)
    assert not probe._sorts_by_level(rare)
    assert not probe._sorts_by_level(pd.Series(rng.integers(0, 50, 600)))


def test_an_order_that_is_not_the_sources_is_not_read(probe):
    """With ``order_known=False`` (a built container) the row-order checks do not run; the value checks do."""
    df = _two_sources()
    df["visit_date"] = pd.date_range("2020-01-01", periods=len(df), freq="h")
    result = probe.check_frame(df, "y", "binary_classification", order_known=False)
    assert result["order_source"] == "none"
    assert not {"order", "periodic_blocks", "entity_runs", "class_block_drift"} & set(result)
    assert result["flags"] == ["time_column"]


@pytest.fixture(scope="module")
def cli():
    """The command line, ``time_probes.py``, with its folders on the path."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("time_probes_cli", SCRIPTS / "time_probes.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_command_line_renders_one_line(probe, cli):
    """The command line renders one line."""
    result = {"name": "toy", "regime": "iid"} | probe.check_frame(_frame(), "y", "binary_classification")
    line = cli.render(result)
    assert line.startswith("toy (iid, 2000 rows)")
    assert "flags []" in line
    assert cli.render({"name": "t", "skipped": "temporal split"}) == "t: skipped (temporal split)"
    runs = {"name": "toy", "regime": "iid"} | probe.check_frame(_admissions(), "outcome", "binary_classification")
    assert "runs on episode: 3000 runs" in cli.render(runs)
    built = probe.check_frame(_frame(), "y", "binary_classification", order_known=False)
    shuffled = {"name": "toy", "regime": "iid"} | built
    assert "row order not read" in cli.render(shuffled)


def test_built_reads_the_collection_cache_without_a_local_build(cli, tmp_path, monkeypatch):
    """``--built`` takes the README's build from the local warehouse, else a collection's cached copy."""
    toy = get_toy_container_path()
    collection = DatasetCollection(
        name="Toy",
        description="the toy container",
        entries=(CollectionEntry(unique_name=toy.parent.name, uuid=toy.name),),
        source=LocalWarehouseSource(base_dir=toy.parents[1]),
    )
    monkeypatch.setattr(cli, "list_collections", lambda: ["Toy"])
    monkeypatch.setattr(cli, "get_collection", lambda _name: collection)
    monkeypatch.setenv("DATA_FOUNDRY_CACHE", str(tmp_path / "cache"))
    monkeypatch.setenv("DATA_FOUNDRY_WAREHOUSE", str(tmp_path / "warehouse"))
    result = cli.probe(toy.parent.name, tmp_path / "definitions", built=True)
    assert result["origin"] == "built (Toy)"
    assert result["order_source"] == "none"

    built = tmp_path / "warehouse" / toy.parent.name / toy.name
    shutil.copytree(toy, built)
    readme = tmp_path / "definitions" / toy.parent.name / "README.md"
    readme.parent.mkdir(parents=True)
    readme.write_text(f"---\nbuild:\n  path: {toy.parent.name}/{toy.name}\n---\n")
    assert cli.built_container(toy.parent.name, tmp_path / "definitions")[1] == "built"
    with pytest.raises(FileNotFoundError):
        cli.built_container("no_such_dataset", tmp_path / "definitions")
