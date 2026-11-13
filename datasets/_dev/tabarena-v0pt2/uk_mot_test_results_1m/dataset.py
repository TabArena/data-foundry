"""Curated dataset definition for `uk_mot_test_results_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

RESULT_2023 = "dft_test_result_2023.csv"
"""The 2023 test results (pipe-separated, unzipped from dft_test_result_2023.zip): history only."""

ITEM_2023 = "dft_test_item_2023.csv"
"""The 2023 test items (pipe-separated, unzipped from dft_test_item_2023.zip): history only."""

MONTHS = tuple(f"{y}{m:02d}" for y in (2024, 2025) for m in range(1, 13))
RESULT_EXTRACTS = tuple(f"dft_test_result_extracts_{m[:4]}/dft_test_result_extract_{m}.csv" for m in MONTHS)
ITEM_EXTRACTS = tuple(f"dft_test_item_extracts_{m[:4]}/dft_test_item_extract_{m}.csv" for m in MONTHS)
"""The monthly extracts of 2024 and 2025 (comma-separated, quotes escaped with a backslash), added on 22 June 2026."""

ITEM_DETAIL = "dft_item_detail_extract.csv"
ITEM_GROUP = "dft_item_group_extract.csv"
PREPARED_FILE = "mot_initial_tests_2024h2_2025_sample.parquet"

TASK_START = "2024-07-01"
"""The first test date of the task: the history starts on 2023-01-01, so every task row has HISTORY_DAYS of it."""

TASK_END = "2025-12-31"
HISTORY_DAYS = 547
"""The history looks back 547 days (about 18 months; 2023-01-01 to 2024-07-01): the vehicle's latest normal test in
that span is its previous test."""

SAMPLE_FRACTION = 0.25
SAMPLE_SEED = 42
"""A task row is kept when a seeded hash of its test id falls below SAMPLE_FRACTION: a uniform quarter of the task
rows, so the frame fits in memory and each monthly test window still holds more than 500k rows."""

DAY_KEY = 100_000
"""A vehicle's tests are keyed vehicle_id * DAY_KEY + day (days since 1970-01-01, below 100,000 until 2243)."""

RESULTS = ("P", "F", "PRS", "ABA", "ABR", "ABRVE")
RESULT_WORDS = {
    "P": "Passed",
    "F": "Failed",
    "PRS": "Pass with rectification at station",
    "ABA": "Abandoned",
    "ABR": "Aborted",
    "ABRVE": "Aborted by VE",
}
"""Test outcomes (dft_mdr_test_outcome_extract.csv; user guide v5.1, "Test Outcomes")."""

RESULT_OF_CODE = {i: RESULT_WORDS[code] for i, code in enumerate(RESULTS)}
"""The words of a result stored as its position in RESULTS (the history columns of the prepared file)."""

ITEM_TYPES = ("F", "P", "M", "A")
"""Item types: a fail item, a PRS item (failing, repaired within the hour), a minor defect, an advisory."""

AREAS = {
    "brakes": ("Brakes", "Motorcycle brakes"),
    "tyres": ("Tyres", "Motorcycle tyres"),
    "wheels": ("Road Wheels", "Motorcycle wheels"),
    "lamps_electrical": (
        "Lamps, reflectors and electrical equipment",
        "Motorcycle lamps and reflectors",
        "Motorcycle audible warning (Horn)",
    ),
    "suspension": ("Suspension", "Motorcycle suspension"),
    "steering": ("Steering", "Motorcycle steering"),
    "body_structure": ("Body, chassis, structure", "Motorcycle structure and attachments"),
    "visibility": ("Visibility",),
    "noise_emissions_leaks": ("Noise, emissions and leaks",),
    "seat_belts": ("Seat belts and supplementary restraint systems", "Seat belt installation check"),
    "identification": ("Identification of the vehicle",),
    "other": (),
}
"""The top-level sections of the post-May-2018 test item tree (dft_item_group_extract.csv), the car and motorcycle
names of one area merged; every other section (speedometer, buses' supplementary tests, items not tested,
non-component advisories) and an unknown item counts as `other`."""

ITEM_COLUMNS = (
    *(f"previous_{name}_items" for name in ("fail", "prs", "minor", "advisory", "dangerous")),
    *(f"previous_{area}_items" for area in AREAS),
)

TASK_COLUMNS = (
    "test_id",
    "vehicle_id",
    "test_date",
    "test_class_id",
    "test_result",
    "test_mileage",
    "postcode_area",
    "make",
    "model",
    "colour",
    "fuel_type",
    "cylinder_capacity",
    "first_use_date",
)
"""The columns of a task row read from its extract; `completed_date` (the time the result was recorded) is not."""

TEST_CLASSES = {
    "1": "1 motorcycle up to 200 cc",
    "2": "2 motorcycle",
    "3": "3 three-wheeler up to 450 kg",
    "4": "4 car or light vehicle",
    "5": "5 passenger vehicle 13+ seats",
    "7": "7 goods vehicle 3,000-3,500 kg",
}
"""Test classes (user guide v5.1, "Test Classes"), the class number kept in front of a short form of the guide's
words."""

MAKE_NAMES = {
    "HARLEY DAVIDSON": "HARLEY-DAVIDSON",
    "MERCEDES": "MERCEDES-BENZ",
    "MERCEDES BENZ": "MERCEDES-BENZ",
    "LANDROVER": "LAND ROVER",
    "VOLKSWAGON": "VOLKSWAGEN",
}
"""One spelling per make where a common make is written two ways (HARLEY DAVIDSON beside HARLEY-DAVIDSON, MERCEDES
beside MERCEDES-BENZ) or misspelled; every other make is kept as written."""

FUEL_TYPES = {
    "PE": "Petrol",
    "DI": "Diesel",
    "HY": "Hybrid Electric (Clean)",
    "HYBRID ELECTRIC (CLEAN)": "Hybrid Electric (Clean)",
    "EL": "Electric",
    "ELECTRIC": "Electric",
    "ED": "Electric Diesel",
    "LP": "Liquefied Petroleum Gas (LPG)",
    "GB": "Gas Bi-Fuel",
    "GA": "Gas",
    "GD": "Gas Diesel",
    "CN": "Compressed Natural Gas (CNG)",
    "LN": "Liquefied Natural Gas (LNG)",
    "FC": "Fuel Cells",
    "ST": "Steam",
    "OT": "Other",
}
"""Fuel type codes (dft_mdr_fuel_type_extract.csv); the 2024 and 2025 extracts also write two of them as words."""


def _read_csv(path: Path, columns: tuple[str, ...], *, pipe: bool):
    """Read the named columns of one MOT csv with pyarrow (text as dictionaries, dates as dates)."""
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.csv as pacsv

    types = {
        "test_id": pa.int64(),
        "vehicle_id": pa.int64(),
        "test_date": pa.date32(),
        "test_mileage": pa.int64(),
        "cylinder_capacity": pa.int64(),
        "first_use_date": pa.date32(),
        "rfr_id": pa.int32(),
    }
    with path.open() as fh:
        header = fh.readline().strip().split("|" if pipe else ",")
    cols = list(dict.fromkeys(c for c in columns if c in header))
    # The 2023 files are pipe-separated with literal quote characters in model names; the extracts quote text with
    # commas and escape a quote inside it with a backslash (MODEL "SWB 88\"").
    parse = pacsv.ParseOptions(delimiter="|", quote_char=False) if pipe else pacsv.ParseOptions(escape_char="\\")
    table = pacsv.read_csv(
        path,
        read_options=pacsv.ReadOptions(block_size=1 << 26),
        parse_options=parse,
        convert_options=pacsv.ConvertOptions(
            include_columns=cols, column_types={c: types.get(c, pa.string()) for c in cols}
        ),
    )
    return pa.table(
        {c: pc.dictionary_encode(table[c]) if pa.types.is_string(table[c].type) else table[c] for c in cols}
    )


def _codes(column, values: tuple[str, ...]) -> np.ndarray:
    """The position of each value in `values` (int8), -1 when missing or not listed."""
    import pyarrow as pa
    import pyarrow.compute as pc

    idx = pc.index_in(column.cast(pa.string()), value_set=pa.array(values))
    return np.asarray(pc.fill_null(idx, -1).to_numpy(zero_copy_only=False), dtype=np.int8)


def _keep_sample(test_id: np.ndarray) -> np.ndarray:
    """Whether a seeded splitmix64 hash of the test id falls below SAMPLE_FRACTION (independent of the row order)."""
    with np.errstate(over="ignore"):
        z = test_id.astype(np.uint64) + np.uint64(0x9E3779B97F4A7C15) * np.uint64(SAMPLE_SEED + 1)
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        z = z ^ (z >> np.uint64(31))
    return (z >> np.uint64(11)).astype(np.float64) / float(2**53) < SAMPLE_FRACTION


def _area_lookup(raw_dir: Path) -> np.ndarray:
    """An array from rfr_id to the index of its area in AREAS (post-May-2018 items; others `other`)."""
    detail = pd.read_csv(raw_dir / ITEM_DETAIL, dtype=str, keep_default_na=False)
    group = pd.read_csv(raw_dir / ITEM_GROUP, dtype=str, keep_default_na=False)
    detail = detail[detail["rfr_deficiency_category"] != "Pre-EU Directive"]
    sections = group[["test_item_id", "test_class_id", "item_name"]].rename(
        columns={"test_item_id": "test_item_set_section_id", "item_name": "section"}
    )
    detail = detail.merge(sections, on=["test_item_set_section_id", "test_class_id"], how="left")
    area_of_section = {s: i for i, names in enumerate(AREAS.values()) for s in names}
    other = list(AREAS).index("other")
    lookup = np.full(int(detail["rfr_id"].astype(int).max()) + 1, other, dtype=np.int8)
    for rfr_id, section in zip(detail["rfr_id"].astype(int), detail["section"], strict=True):
        lookup[rfr_id] = area_of_section.get(section, other)
    return lookup


def _latest_before(
    key: np.ndarray, tid: np.ndarray, done: np.ndarray, mask: np.ndarray, query: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """For each query key (vehicle_id * DAY_KEY + day), the row of the vehicle's latest test in `mask` dated before
    that day, and whether one exists. Tests of one day are ordered by the time recorded, then the test id.
    """
    rows = np.flatnonzero(mask)
    order = np.lexsort((tid[rows], done[rows], key[rows]))
    rows = rows[order]
    sorted_key = key[rows]
    pos = np.searchsorted(sorted_key, query, side="left") - 1
    at = np.maximum(pos, 0)
    found = (pos >= 0) & (sorted_key[at] // DAY_KEY == query // DAY_KEY)
    return found, rows[at]


def prepare_initial_tests(raw_dir: Path) -> None:
    """Sample the task rows and build each one's history from the vehicle's earlier tests and their items."""
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.parquet as pq

    pa.set_cpu_count(2)
    pa.set_io_thread_count(2)
    start = (np.datetime64(TASK_START) - np.datetime64("1970-01-01")).astype(np.int64)
    end = (np.datetime64(TASK_END) - np.datetime64("1970-01-01")).astype(np.int64)
    skinny = ("test_id", "vehicle_id", "test_date", "test_type", "test_result", "test_mileage", "completed_date")

    # 1. Every test of 2023-2025 (the history), and a seeded quarter of the task rows: normal tests (NT) with a
    #    result of P, F or PRS, dated TASK_START to TASK_END.
    parts: dict[str, list[np.ndarray]] = {k: [] for k in ("tid", "veh", "day", "nt", "res", "mil", "done")}
    task_tables = []
    files = [(raw_dir / RESULT_2023, True)] + [(raw_dir / f, False) for f in RESULT_EXTRACTS]
    for path, pipe in files:
        table = _read_csv(path, skinny if pipe else (*skinny, *TASK_COLUMNS), pipe=pipe)
        tid = table["test_id"].to_numpy()
        day = np.asarray(table["test_date"].cast(pa.int32()).to_numpy(), dtype=np.int32)
        nt = np.asarray(pc.equal(table["test_type"].cast(pa.string()), "NT").to_numpy(zero_copy_only=False))
        res = _codes(table["test_result"], RESULTS)
        mil = np.asarray(pc.fill_null(table["test_mileage"], 0).to_numpy(), dtype=np.int64)
        if "completed_date" in table.column_names:  # the time the result was recorded (2024 on): a tie-break only
            text = pc.utf8_slice_codeunits(table["completed_date"].cast(pa.string()), 0, 19)
            stamp = pc.strptime(text, format="%Y-%m-%dT%H:%M:%S", unit="s")
            done = np.asarray(pc.fill_null(stamp.cast(pa.int64()), 0).to_numpy(), dtype=np.int64)
        else:
            done = np.zeros(len(tid), dtype=np.int64)
        for key, value in zip(parts, (tid, table["vehicle_id"].to_numpy(), day, nt, res, mil, done), strict=True):
            parts[key].append(value)
        if not pipe:
            task = nt & (res >= 0) & (res <= 2) & (day >= start) & (day <= end) & _keep_sample(tid)
            task_tables.append(table.select(list(TASK_COLUMNS)).filter(pa.array(task)))
        del table
    tid, veh, day, nt, res, mil, done = (np.concatenate(parts[k]) for k in parts)
    del parts
    task = pa.concat_tables(task_tables, promote_options="permissive").unify_dictionaries().combine_chunks()
    del task_tables
    q_veh = task["vehicle_id"].to_numpy()
    q_day = np.asarray(task["test_date"].cast(pa.int32()).to_numpy(), dtype=np.int64)
    query = q_veh * DAY_KEY + q_day

    # 2. The previous test: the vehicle's latest normal test dated before the test date (not the same day), within
    #    HISTORY_DAYS. Ties on one day go to the test recorded last (then the larger test id).
    key = veh * DAY_KEY + day
    found, prev = _latest_before(key, tid, done, nt, query)
    prev_day = day[prev].astype(np.int64)
    has_prev = found & (q_day - prev_day <= HISTORY_DAYS)

    # 3. The last retest (or appeal) after the previous test and before the test date: did the vehicle pass after it?
    found_rt, last_rt = _latest_before(key, tid, done, ~nt, query)
    has_rt = has_prev & found_rt & (day[last_rt] >= prev_day)

    history = {
        "previous_test_result": np.where(has_prev, res[prev], -1).astype(np.int8),
        "days_since_previous_test": np.where(has_prev, q_day - prev_day, -1).astype(np.int32),
        "previous_test_mileage": np.where(has_prev, mil[prev], -1).astype(np.int64),
        "previous_retest_result": np.where(has_rt, res[last_rt], -1).astype(np.int8),
    }
    prev_tid = np.where(has_prev, tid[prev], -1)
    del tid, veh, day, nt, res, mil, done, key, prev, last_rt

    # 4. The previous test's items: counts by type (fail, PRS, minor, advisory, dangerous) and by area of the test.
    needed = np.unique(prev_tid[has_prev])
    counts = np.zeros((len(ITEM_COLUMNS), len(needed)), dtype=np.int32)
    lookup = _area_lookup(raw_dir)
    other = list(AREAS).index("other")
    files = [(raw_dir / ITEM_2023, True)] + [(raw_dir / f, False) for f in ITEM_EXTRACTS]
    for path, pipe in files:
        items = _read_csv(path, ("test_id", "rfr_id", "rfr_type_code", "dangerous_mark"), pipe=pipe)
        item_tid = items["test_id"].to_numpy()
        pos = np.minimum(np.searchsorted(needed, item_tid), len(needed) - 1)
        hit = needed[pos] == item_tid
        pos = pos[hit]
        kind = _codes(items["rfr_type_code"], ITEM_TYPES)[hit]
        mark = pc.fill_null(items["dangerous_mark"].cast(pa.string()), "")
        danger = np.asarray(pc.equal(mark, "D").to_numpy(zero_copy_only=False))[hit]
        rfr = np.asarray(items["rfr_id"].to_numpy(), dtype=np.int64)[hit]
        area = np.where(rfr < len(lookup), lookup[np.minimum(rfr, len(lookup) - 1)], other)
        for k in range(len(ITEM_TYPES)):
            counts[k] += np.bincount(pos[kind == k], minlength=len(needed)).astype(np.int32)
        counts[len(ITEM_TYPES)] += np.bincount(pos[danger], minlength=len(needed)).astype(np.int32)
        for a in range(len(AREAS)):
            counts[len(ITEM_TYPES) + 1 + a] += np.bincount(pos[area == a], minlength=len(needed)).astype(np.int32)
        del items
    at = np.minimum(np.searchsorted(needed, prev_tid), len(needed) - 1)
    for k, name in enumerate(ITEM_COLUMNS):
        history[name] = np.where(has_prev, counts[k][at], -1).astype(np.int32)

    out = task
    for name, values in history.items():
        out = out.append_column(name, pa.array(values))
    pq.write_table(out, raw_dir / PREPARED_FILE)


class UkMotTestResults1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a vehicle fail its MOT test as it was presented, before any repair at the test station?",
        use_case=(
            "DVSA's enforcement officers use a predictive vehicle failure model: for each MOT test it gives the "
            "chance that the vehicle fails, and officers target testers and garages whose recorded results run "
            "against it again and again (DVSA digital blog, 2019). The model is refit monthly, for example."
        ),
        row=(
            "One normal (initial) MOT test in Great Britain, July 2024 to December 2025, with a result of pass, fail "
            "or pass after rectification: a random quarter (13.3 million) of the 53.2 million such tests in DVSA's "
            "anonymised MOT data. Retests are no rows."
        ),
        predicted=(
            "Whether the vehicle failed the initial test: a fail, or a pass after its defects were repaired at the "
            "station within the hour, which DVSA counts as an initial failure too (27.7% of the tests)."
        ),
        known=(
            "The test date, vehicle class, postcode area of the test station, odometer reading, make, model, colour, "
            "fuel, engine size and date of first use, and the vehicle's previous MOT test of the last 18 months: its "
            "result, date and mileage, its defects and advisories by type and by area, and the result of a retest "
            "after it."
        ),
        split=(
            "Each of October, November and December 2025 is a test month (500,000 tests each); training is a random "
            "million tests from July 2024 to the month before, as for a model refit monthly."
        ),
        changes=(
            "We keep initial tests with a result, use retests and the tests of 2023 only as the vehicles' history, "
            "build each vehicle's previous-test history, drop the test's own defects and the time it ended, and keep "
            "a random quarter of the tests."
        ),
        fit="direct",
        fit_reason=(
            "Everything is known when a test starts, and the label is the result the tester recorded, which DVSA "
            "audits. No tester or station id ships, as the use needs: the model estimates a vehicle's expected result "
            "independent of who tests it. The history stops at 18 months, where DVSA sees the full record."
        ),
    )

    # Dataset
    unique_name = "uk_mot_test_results_1m"
    version_of = "uk_mot_test_results"
    version_comment = """
        The task holds 53,239,257 initial tests from July 2024 to December 2025, and every train side 44.7M to 51.0M of them, above the 1M-row budget, so the dataset ships only as this version (definitions.md, Lennart 2026-10-21). `_prepare_raw_files` builds every task row's history from all tests first, then keeps a seeded quarter of the task rows (a splitmix64 hash of the test id below 0.25, seed 42: 13,311,677 rows), so the frame fits in memory; each monthly window still holds 564,611 to 845,719 of them. Then the v2 split protocol samples per test window: each window keeps a random 500k of its rows, and its train side is a random 1M of all earlier rows, drawn in one random order for all windows so the train sides overlap; the frame keeps only the rows a split uses. The sample is random over the 15 to 17 months before a window rather than the latest tests, so the train sides cover every season.
    """
    year = "2026"  # the snapshot we pin: the 2024 and 2025 extracts were added on 22 June 2026 (PROV-9)
    domain = "industry & manufacturing"  # vehicle roadworthiness; transport has no value of its own (as fmcsa)
    source = "GOV Website"
    source_url = "https://open.data.dvsa.gov.uk/mot-anonymised/index.html"
    license = "OGL-UK-3.0"  # Open Government Licence v3.0, stated on the DVSA and data.gov.uk pages
    data_tags = ("Spatial",)
    download_description = """
        DVSA's "MOT Anonymised" files on the DVSA open data portal (data.gov.uk lists the same dataset), downloaded
        without a login on 2026-11-09: the 2023 test results and items (added 29 February 2024; history only), the
        monthly extracts of 2024 and 2025 (added 22 June 2026), and the test item lookups. The portal also holds an
        older release of 2024 ("MOT testing data results (2024)", March 2025), which the June 2026 extracts replace.
        The 2023 zips use Deflate64, which Python's zipfile cannot read; unzip can. The extract zips store their CSVs
        uncompressed (about 4.3 to 4.8 GB each).

        mkdir -p local-data-warehouse/uk_mot_test_results && cd local-data-warehouse/uk_mot_test_results
        B=https://edh-dvsa-data-gov-uk-files-prod.s3.eu-west-1.amazonaws.com
        for f in dft_test_result_2023.zip dft_test_item_2023.zip dft_test_result_extracts_2024.zip \\
                 dft_test_item_extracts_2024.zip dft_test_result_extracts_2025.zip dft_test_item_extracts_2025.zip \\
                 dft_item_detail_extract.csv dft_item_group_extract.csv dft_mdr_test_outcome_extract.csv \\
                 dft_mdr_test_type_extract.csv dft_mdr_fuel_type_extract.csv mot-testing-data-user-guide-v5.1.odt; do
          wget -c "$B/$f"
        done
        unzip -p dft_test_result_2023.zip > dft_test_result_2023.csv
        unzip -p dft_test_item_2023.zip > dft_test_item_2023.csv
        for f in dft_test_result_extracts_2024.zip dft_test_item_extracts_2024.zip dft_test_result_extracts_2025.zip \\
                 dft_test_item_extracts_2025.zip; do
          unzip -o "$f"
        done
    """
    bibtex = r"""
        @misc{dvsa_anonymised_mot_tests,
          author = {{Driver and Vehicle Standards Agency}},
          title = {Anonymised {MOT} tests and results},
          year = {2026},
          howpublished = {\url{https://open.data.dvsa.gov.uk/mot-anonymised/index.html}},
          note = {Open Government Licence v3.0}
        }
    """
    curation_comments = """
        We start with DVSA's anonymised MOT test results and test items: the 2023 files (pipe-separated, 42.2M tests) and the monthly extracts of 2024 and 2025 (85.4M tests), from the DVSA open data portal.

        - Prediction point: the start of an MOT test, with the vehicle presented, its odometer read and its MOT record on file. DVSA's blog ("Getting smart on MOT fraud", Neil Barlow, 10 June 2019) describes "expanding the risk ratings algorithm to include a 'predictive vehicle failure model'" to "help our officers to better understand the likelihood of a vehicle passing or failing its MOT", and to "target testers who repeatedly record results contrary to the prediction" (USE-1).
        - Target: `initial_fail` is Yes for a fail (F) or a pass with rectification at the station (PRS: "Vehicle begins the test in a fail condition", user guide v5.1), No for a pass (P); the guide's initial failure rate counts both (USE-5). 27.7% of the rows.
        - Note: the label is the result the tester recorded, the very thing DVSA audits for errors and fraud. Any model DVSA fits learns from the same recorded results, so this noise is part of the task.
        - Rows: normal tests (NT) with a result of P, F or PRS dated 1 July 2024 to 31 December 2025 (53,239,257). Abandoned and aborted tests (ABA, ABR, ABRVE; 0.6% of normal tests) have no result. Retests (RT; 14.4M in 2024-2025) and appeals (ES, EI) follow a failure: they are no rows and serve as history only.
        - History (USE-10, LEAK-34; CLEAN-19, the history aggregated to one row per test): the vehicle (`vehicle_id`, "based upon the Registration and VIN") has its previous test, its latest normal test dated before the test date within 547 days (about 18 months). The 2023 files feed only this history, so every row has 18 months of it; 92.3% of the rows have a previous test (median gap 364 days; 98.4% of the 2025 tests with an earlier one since 2023 have it within 547 days). It gives the previous result (23.5% of the rows fail after a pass, 42.3% after a fail, 18.5% with none), the days since, the mileage, the counts of its items by type (fail, PRS, minor, advisory, dangerous) and by area of the post-2018 test item tree (car and motorcycle sections of one area merged; the other sections, 3.4% of items, as `other`), and the result of the last retest after it. A test dated the same day as the row is not read. A re-derivation with plain filters on 300 random rows matched every value. The history adds 0.019 to 0.021 ROC AUC to LightGBM (0.701 to 0.704 with it, 0.681 to 0.683 without; 300 trees on a random 400k of each train side, the three shipped windows), and the full model beats the previous result alone (0.596 to 0.599) by about 0.105 (TP-10, leg 1).
        - Dropped as the outcome (LEAK-10): the test's own items (its defects and advisories), and `completed_date`, the time the result was recorded (2024 on), which ends the test. Dropped as identifiers: the test and vehicle ids (the history stands for the vehicle).
        - Missing: an odometer reading of 0 or blank ("not possible to obtain a reading", guide; 0.23% of the task rows, 43.9% of which fail: kept, an unreadable odometer is a state of the vehicle as presented) and 999,999 (153 rows); a first use date of 1971-01-01 ("unknown date of manufacture", guide; 284 rows), before 1900 (55, years such as 13 or 1015) or after the test (1); a cylinder capacity of 0 (1,584), under 25 cc (787) or 30,000 cc and above (63) (CLEAN-11); make (135) and model (142,915) UNCLASSIFIED ("do not have a valid record", guide); colour NOT STATED (595).
        - Mileage stays as recorded: the guide says readings in kilometres were converted to miles from the 2022 data on, and of the 28.9M pairs of a 2025 test and the vehicle's previous test 300 to 430 days before, 0.06% fall at the kilometre-to-mile ratio and 0.23% go down (CLEAN-21).
        - Decoded: the test class into the guide's words (with the class number), the fuel codes into the lookup's words (the extracts also write two as words: HYBRID ELECTRIC (CLEAN), 525,574 task rows, and ELECTRIC), and the results of the history. The postcode area of the station stays a code (XX merges areas with fewer than five stations; 3,757 rows). The make (11,191 spellings, 58 cover 99% of the rows; most of the rest are models written into the make field) is categorical, with one name for the common makes written two ways (`MAKE_NAMES`: HARLEY DAVIDSON, 0.06% of the rows, and MERCEDES, 0.02%) and a few misspellings; the model (54,868 values, often with trim words) is text. HYBRID ELECTRIC (CLEAN) is merged into HY (CLEAN-12): it is the same fuel, written as words by a different recording path of the extracts, not a different kind of vehicle; the words fail 16.8% of the time against 13.0% for the code, a difference of recording path or cohort (untested) that the fuel column is not meant to carry.
        - Protocol line (LEAK-9): a fold uses only its own train rows; test rows are predicted without any other test row or later-dated row. A vehicle can have two tests in one test month (a failure presented again as a new normal test), and the later row's previous-test fields give the earlier row's result away to a method that reads the other test rows (554 to 671 test rows a window, 90% to 94% of them fails). Rows dated after the window (in the frame for the October and November folds, in neither their train nor their test side) do the same: a participant who links a test row to the vehicle's later rows linked 657, 1,509 and 1,586 test rows (December, November, October folds), 38,728 of the 38,734 labels so read right, for +0.0014 to +0.0027 ROC AUC (review panel, 2026-11-09). No re-split and no rows dropped: the protocol line covers it.
        - Note: test months are sampled about 8 times more densely than training months: the row budget keeps 500k of a window's tests but 1M of the 15 to 17 months before it, so test windows stay whole in shape as in chicago_taxi; the Yes rate stays in band (0.277 in training, 0.275 to 0.284 in the windows; SPLIT-14).
        - Note: `test_mileage` is the odometer read at the start of the test, when the vehicle is presented, so it is known at the prediction point (LEAK-10 holds).
        - Note: make, model, colour, fuel, cylinder capacity and first use date may be the vehicle record as of the June 2026 extract rather than as at the test date (CLEAN-1); they change rarely for one vehicle.
        - Note: 23,731 vehicle-days hold two or more initial tests with a result (47,516 task rows, 0.09%; mostly a fail, then a pass on a new test after repairs the same day). The history reads earlier days only, so the second test does not see the first (the 2023 files have no time of day to order them); in the sample, 266 such pairs share every input, distinct tests rather than copies (LEAK-18, LEAK-20).
        - Anomaly: the 2025 extract ends on 30 December 2025 (no tests dated the 31st, against 41,349 on 31 December 2024), so the December window lacks its last day.
        - Not downloaded: 2005-2022 (the history needs 18 months) and the March 2025 release of 2024, which the June 2026 extracts replace (the screening found its January file larger than a month).
    """

    # Task
    target = "initial_fail"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "No source metric: the DVSA portal and data.gov.uk pages, the MOT testing data user guide v5.1 and DVSA's "
            "blog on its predictive vehicle failure model (Neil Barlow, 'Getting smart on MOT fraud', 10 June 2019) "
            "state no evaluation metric, and no competition or paper defines the task (one web search). The use "
            "ranks tests: officers look for the tests and testers whose recorded results run against the predicted "
            "chance of failure, so ROC AUC on the probabilities (MET-8)."
        )
    )

    # Splits
    splits_comment = """
        A model refit each month: each of October, November and December 2025 is a test window (newest first), trained on the tests from 1 July 2024 to the day before the window; a vehicle tested in a window usually had its previous test a year earlier, which its history fields carry (USE-10). No gap: a result is entered when the test ends, the same day, and the history reads only tests dated before the test date. Before sampling, each train side holds 84% to 96% of the frame's rows (SPLIT-14's floor is 50%) and spans 15 to 17 months, so every season. Each window keeps a random 500k of its 564,611 to 845,719 sampled tests; each train side is a random 1M of the earlier sampled tests (one random order for all windows).
    """
    temporal = Temporal(on="test_date", splits=TemporalSplits(window=1, unit="months", n_windows=3))
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        prepare_initial_tests(raw_dir)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow.parquet as pq

        return pq.read_table(raw_dir / PREPARED_FILE).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame(index=raw.index)

        # 1. The target: a fail at the initial test, F or PRS (defects repaired within the hour before the result was
        #    entered), as DVSA's initial failure rate counts it; P is No. The rows are normal tests with one of the
        #    three results (`prepare_initial_tests`).
        result = raw["test_result"].astype(str)
        df[self.target] = np.where(result.isin(["F", "PRS"]), "Yes", "No")

        # 2. The test: its date (the split key), the vehicle's test class and the postcode area of the test station
        #    (XX merges the areas with fewer than five active stations; kept as a level).
        df["test_date"] = pd.to_datetime(raw["test_date"])
        df["test_class"] = raw["test_class_id"].astype("string").map(TEST_CLASSES)
        df["postcode_area"] = raw["postcode_area"].astype("string")

        # 3. The vehicle as presented: the odometer reading (0 means no reading, 999,999 the top of a six-digit
        #    odometer: missing), make (one name per make) and model (UNCLASSIFIED: no valid record, missing), colour
        #    (NOT STATED: missing), fuel (codes and the two spellings in words decoded), cylinder capacity (0, under
        #    25 cc and 30,000 cc or more are impossible: missing) and the date of first use (1971-01-01 codes an
        #    unknown date; before 1900 or after the test date is impossible: missing).
        df["test_mileage"] = _mileage(raw["test_mileage"])
        make = raw["make"].astype("string")
        df["make"] = make.replace(MAKE_NAMES).mask(make == "UNCLASSIFIED")
        model = raw["model"].astype("string")
        df["model"] = model.mask(model == "UNCLASSIFIED")
        colour = raw["colour"].astype("string")
        df["colour"] = colour.mask(colour == "NOT STATED")
        df["fuel_type"] = raw["fuel_type"].astype("string").map(FUEL_TYPES)
        cc = raw["cylinder_capacity"].astype(float)
        df["cylinder_capacity"] = cc.where((cc >= 25) & (cc < 30_000))
        first_use = pd.to_datetime(raw["first_use_date"])
        bad = (first_use == "1971-01-01") | (first_use < "1900-01-01") | (first_use > df["test_date"])
        df["first_use_date"] = first_use.mask(bad)

        # 4. The vehicle's history as of the test date (built in `prepare_initial_tests`; -1 marks no previous normal
        #    test in the 547 days before the test date, or no retest after it): the previous test's result, the days
        #    since it, its mileage, the result of the last retest after it, and its items by type and by area.
        prev = raw["previous_test_result"].astype(int)
        df["previous_test_result"] = prev.map(RESULT_OF_CODE)
        df["days_since_previous_test"] = raw["days_since_previous_test"].astype(float).mask(prev < 0)
        df["previous_test_mileage"] = _mileage(raw["previous_test_mileage"]).mask(prev < 0)
        retest = raw["previous_retest_result"].astype(int)
        df["previous_retest_result"] = retest.map(RESULT_OF_CODE)
        for col in ITEM_COLUMNS:
            df[col] = raw[col].astype(float).mask(prev < 0)
        return df

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        fail = df[self.target].astype(str).eq("Yes")
        previous = df["previous_test_result"].astype("string").fillna("none in the 547 days before")
        table = (
            fail.groupby(previous)
            .agg(rows="size", fail_share="mean")
            .sort_values("rows", ascending=False, kind="stable")
            .assign(fail_share=lambda t: t["fail_share"].round(3))
        )
        table.index.name = "previous normal test"
        return [
            Decision(
                "The vehicle's previous test is a feature (a known vehicle's own dated history)",
                "Vehicles come back every year, and DVSA holds their MOT record when a test starts (USE-10, LEAK-34): "
                "the failure share of the rows the splits use, by the result of the vehicle's previous normal test.",
                table,
            )
        ]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "test_class",
                "postcode_area",
                "make",
                "colour",
                "fuel_type",
                "previous_test_result",
                "previous_retest_result",
            ],
            string=["model"],
            datetime={"test_date": "%Y-%m-%d", "first_use_date": "%Y-%m-%d"},
        )


def _mileage(miles: pd.Series) -> pd.Series:
    """An odometer reading in miles; 0 (no reading), 999,999 (the top of a six-digit odometer) and a negative value
    (no previous test) are missing.
    """
    miles = miles.astype(float)
    return miles.where((miles > 0) & (miles < 999_999))
