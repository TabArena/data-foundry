"""Curated dataset definition for `fmcsa_roadside_inspection_out_of_service_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

MONTHS = tuple(str(p).replace("-", "") for p in pd.period_range("2023-11", "2026-11", freq="M"))
"""The months of inspection dates in the view on 2026-11-09 (2023-11-08 to 2026-11-06), one file each."""

INSPECTION_FILES = tuple(f"inspections_by_month/inspections_{m}.csv" for m in MONTHS)
UNIT_FILES = tuple(f"units_by_id_prefix/units_{p}.csv" for p in range(80, 90))
"""The Inspections Per Unit view, one file per first two digits of the inspection id (80 to 89)."""
PREPARED_FILE = "inspections_with_history.parquet"

TASK_START = "2024-12-01"
"""The first inspection date of the task: the view starts on 2023-11-08, so every task row has a full year of earlier
inspections for its carrier's and vehicle's history."""

TASK_END = "2026-10-31"
"""The last inspection date of the task: the last whole month before the download (the 31,659 inspections of 1 to 6
November 2026 are a partial month)."""

UPLOAD_FIELDS = (
    "inspection_id",
    "report_number",
    "snet_sequence_id",
    "change_date",
    "mcmis_add_date",
    "upload_date",
    "transaction_date",
    "transaction_code",
    "final_status_date",
    "census_search_date",
    "snet_input_date",
)
"""The ids and processing fields of an inspection record: two records equal in every other column are one inspection
uploaded twice."""

HISTORY_DAYS = 365
"""The carrier and vehicle history counts the inspections of the year before the inspection date."""

DECAL_DAYS = 90
"""A CVSA decal is valid for up to three months, so a decal issued within 90 days is still on the vehicle."""

VIN_PATTERN = r"[A-HJ-NPR-Z0-9]{17}"
"""A valid VIN: 17 characters without I, O and Q (49 CFR 565.13)."""

VIN_YEAR_CODES = "ABCDEFGHJKLMNPRSTVWXY123456789"
"""The tenth VIN character codes the model year in a 30-year cycle: A is 1980 (and 2010), ..., Y 2000, 1 2001, ...,
9 2009 (49 CFR 565.15)."""

UNIT_TYPES = {
    "1": "Bus",
    "2": "Dolly Converter",
    "3": "Full Trailer",
    "4": "Limousine",
    "5": "Motor Coach",
    "6": "Other",
    "7": "Pole Trailer",
    "8": "School Bus",
    "9": "Semi Trailer",
    "10": "Straight Truck",
    "11": "Truck Tractor",
    "12": "Van",
    "14": "Intermodal Chassis",
}
"""MCMIS unit type codes (data dictionary, Inspection Unit table); 13 (ZZ, unknown) is left missing."""

YES_NO = {"Y": "Yes", "N": "No"}

UNKNOWN_STATES = ("NA", "UK", "ZZ")
"""State codes for an unknown place: UK and ZZ in the dictionary's state table, and NA, which it does not list (74 task rows)."""

UNKNOWN_MAKES = ("UNKNOWN", "UNK", "UNKN", "UNKOWN", "NA", "N/A", "NONE")
"""Makes recorded as unknown (1,843 task rows)."""

MAKE_NAMES = {
    "FRHT": "FREIGHTLINER",
    "FREIGHTLIN": "FREIGHTLINER",
    "FTL": "FREIGHTLINER",
    "KW": "KENWORTH",
    "KENW": "KENWORTH",
    "KENWORTH M": "KENWORTH",
    "PTRB": "PETERBILT",
    "INTL": "INTERNATIONAL",
    "INTERNATIO": "INTERNATIONAL",
    "VOLV": "VOLVO",
    "MACK TRUCK": "MACK",
    "ISU": "ISUZU",
    "CHEV": "CHEVROLET",
    "DODG": "DODGE",
    "WSTR": "WESTERN STAR",
    "WESTERN ST": "WESTERN STAR",
    "STERLING T": "STERLING",
    "THMS": "THOMAS",
    "BLUB": "BLUE BIRD",
}
"""One spelling per make for the common ones: states write the four-letter NCIC make code (FRHT) or the name cut to
ten characters (FREIGHTLIN); the codes left as written are rarer (under 21,000 task rows each)."""

HISTORY_COLUMNS = (
    "carrier_inspections_1y",
    "carrier_vehicle_level_1y",
    "carrier_driver_level_1y",
    "carrier_oos_1y",
    "carrier_vehicle_oos_1y",
    "carrier_driver_oos_1y",
    "carrier_violations_1y",
    "carrier_days_since_inspection",
    "vehicle_inspections_1y",
    "vehicle_oos_1y",
    "vehicle_vehicle_oos_1y",
    "vehicle_days_since_inspection",
    "vehicle_decals_90d",
)
"""The history columns `prepare_inspections` builds."""

SHIPPED_HISTORY = tuple(c for c in HISTORY_COLUMNS if c != "vehicle_days_since_inspection")
"""The history columns the task keeps: the days since the vehicle's last inspection let a later test row point at an
earlier test row of the same vehicle and read its outcome from the change of the counts (LEAK-9)."""

RAW_COLUMNS = (
    "insp_date",
    "insp_start_time",
    "insp_end_time",
    "report_state",
    "county_code_state",
    "county_code",
    "location_desc",
    "insp_facility",
    "local_enf_jurisdiction",
    "post_acc_ind",
    "hazmat_placard_req",
    "cargo_tank",
    "gross_comb_veh_wt",
    "alcohol_control_sub",
    "drug_intrdctn_search",
    "registration_date",
    "viol_total",
    "oos_total",
    "driver_oos_total",
    "vehicle_oos_total",
    "hazmat_oos_total",
    "insp_carrier_state",
    "insp_interstate",
    "docket_number",
    "unit_count",
    "unit1_type_id",
    "unit1_make",
    "unit1_license_state",
    "unit1_vin",
    "unit1_decal",
    "unit2_type_id",
    *SHIPPED_HISTORY,
)
"""The columns `_load_raw` reads from the prepared file."""


def _day(col: str):
    """A polars expression: the YYYYMMDD date at the start of a text column, as days since 1970-01-01."""
    import polars as pl

    return pl.col(col).str.slice(0, 8).str.strptime(pl.Date, "%Y%m%d", strict=False).cast(pl.Int64)


def window_sums(entity, start, end, values, query_entity, query_day):
    """For each query, sum the values of its entity's records whose span [start, end] holds the query day.

    A record whose end is before its start counts for no query. Returns one array per value, aligned with the queries.
    """
    span = np.int64(1_000_000)
    end = np.maximum(end, start - 1)
    s_key = entity * span + start
    e_key = entity * span + end
    q_key = query_entity * span + query_day
    s_order = np.argsort(s_key, kind="stable")
    e_order = np.argsort(e_key, kind="stable")
    n_s = np.searchsorted(s_key[s_order], q_key, side="right")
    n_e = np.searchsorted(e_key[e_order], q_key, side="left")
    out = []
    for v in values:
        cs = np.concatenate([[0], np.cumsum(v[s_order], dtype=np.int64)])
        ce = np.concatenate([[0], np.cumsum(v[e_order], dtype=np.int64)])
        out.append(cs[n_s] - ce[n_e])
    return out


def last_event_before(entity, known, event, query_entity, query_day):
    """For each query, the latest event day of its entity's records known on or before the query day, else -1."""
    span = np.int64(1_000_000)
    order = np.lexsort((event, known, entity))
    ent, kn, ev = entity[order], known[order], event[order]
    key = ent * span + kn
    first = np.r_[True, ent[1:] != ent[:-1]]
    offset = (np.cumsum(first) - 1).astype(np.int64) * span
    run_max = np.maximum.accumulate(ev + offset) - offset
    idx = np.searchsorted(key, query_entity * span + query_day, side="right") - 1
    ok = idx >= 0
    ok[ok] = ent[idx[ok]] == query_entity[ok]
    out = np.full(len(query_day), -1, dtype=np.int64)
    out[ok] = run_max[idx[ok]]
    return out


def _number(col: pd.Series) -> pd.Series:
    """The numbers of a text column read as categories (blank or not a number: NaN), without a copy per row."""
    if isinstance(col.dtype, pd.CategoricalDtype):
        values = pd.to_numeric(pd.Series(col.cat.categories), errors="coerce").to_numpy(dtype=float)
        codes = col.cat.codes.to_numpy()
        return pd.Series(np.where(codes >= 0, values[codes], np.nan), index=col.index)
    return pd.to_numeric(col, errors="coerce").astype(float)


def valid_vin(vin: pd.Series) -> pd.Series:
    """Whether each VIN is 17 valid characters and not one character repeated (a placeholder such as 000...0)."""
    vin = vin.astype("string").str.strip().str.upper()
    ok = vin.str.fullmatch(VIN_PATTERN) & ~vin.str.fullmatch(r"(.)\1{16}")
    return ok.fillna(False).astype(bool)


def vin_model_year(vin: pd.Series, inspection_year: pd.Series) -> pd.Series:
    """The model year a valid VIN codes: the latest year of its 30-year cycle not after the inspection year plus one."""
    code = vin.astype("string").str.strip().str.upper().str.slice(9, 10)
    base = code.map({c: 1980 + i for i, c in enumerate(VIN_YEAR_CODES)}).astype("Float64")
    latest = inspection_year.astype("Float64") + 1
    year = base + 30 * ((latest - base) // 30)
    return year.where(valid_vin(vin) & base.notna())


def prepare_inspections(raw_dir: Path) -> None:
    """Join each inspection with its units and build the carrier and vehicle history as of the inspection date."""
    import polars as pl

    insp = pl.concat([pl.read_csv(raw_dir / f, infer_schema=False) for f in INSPECTION_FILES], how="vertical")
    # One inspection uploaded twice: copies in every column but the ids and the processing fields; keep the lowest id,
    # so the history counts the inspection once.
    content = [c for c in insp.columns if c not in UPLOAD_FIELDS]
    insp = insp.sort("inspection_id").unique(subset=content, keep="first", maintain_order=True)
    unit_columns = [
        "inspection_id",
        "insp_unit_type_id",
        "insp_unit_number",
        "insp_unit_make",
        "insp_unit_license_state",
        "insp_unit_vehicle_id_number",
        "insp_unit_decal",
    ]
    units = pl.concat(
        [pl.read_csv(raw_dir / f, infer_schema=False, columns=unit_columns) for f in UNIT_FILES], how="vertical"
    )
    unit1 = (
        units.filter(pl.col("insp_unit_number") == "1")
        .sort("inspection_id", "insp_unit_vehicle_id_number", "insp_unit_type_id", nulls_last=True)
        .unique(subset="inspection_id", keep="first", maintain_order=True)
        .select(
            "inspection_id",
            unit1_type_id=pl.col("insp_unit_type_id"),
            unit1_make=pl.col("insp_unit_make"),
            unit1_license_state=pl.col("insp_unit_license_state"),
            unit1_vin=pl.col("insp_unit_vehicle_id_number"),
            unit1_decal=pl.col("insp_unit_decal"),
        )
    )
    unit2 = (
        units.filter(pl.col("insp_unit_number") == "2")
        .sort("inspection_id", "insp_unit_type_id", nulls_last=True)
        .unique(subset="inspection_id", keep="first", maintain_order=True)
        .select("inspection_id", unit2_type_id=pl.col("insp_unit_type_id"))
    )
    counts = units.group_by("inspection_id", maintain_order=True).agg(unit_count=pl.len())
    insp = (
        insp.join(counts, on="inspection_id", how="left")
        .join(unit1, on="inspection_id", how="left")
        .join(unit2, on="inspection_id", how="left")
        .sort("inspection_id")
    )
    del units, unit1, unit2, counts

    num = insp.select(
        day=_day("insp_date"),
        add=_day("mcmis_add_date"),
        carrier=pl.col("dot_number").cast(pl.Int64, strict=False).fill_null(0),
        one=pl.lit(1, dtype=pl.Int64),
        vehicle_level=pl.col("insp_level_id").is_in(["1", "2", "5"]).cast(pl.Int64),
        driver_level=pl.col("insp_level_id").is_in(["1", "2", "3"]).cast(pl.Int64),
        oos=(pl.col("oos_total").cast(pl.Int64) > 0).cast(pl.Int64),
        vehicle_oos=(pl.col("vehicle_oos_total").cast(pl.Int64) > 0).cast(pl.Int64),
        driver_oos=(pl.col("driver_oos_total").cast(pl.Int64) > 0).cast(pl.Int64),
        violations=pl.col("viol_total").cast(pl.Int64),
        decal=(pl.col("unit1_decal") == "Y").fill_null(False).cast(pl.Int64),
        vin=pl.col("unit1_vin").str.strip_chars().str.to_uppercase(),
    )
    day, add = num["day"].to_numpy(), num["add"].to_numpy()
    hist: dict[str, np.ndarray] = {}

    # Carrier history: the carrier's inspections of the year before the inspection date that were in MCMIS before
    # that date (added on an earlier day), as an inspector's lookup would show them.
    carrier = num["carrier"].to_numpy()
    rec = carrier > 0
    names = ["one", "vehicle_level", "driver_level", "oos", "vehicle_oos", "driver_oos", "violations"]
    sums = window_sums(
        carrier[rec], add[rec] + 1, day[rec] + HISTORY_DAYS, [num[c].to_numpy()[rec] for c in names], carrier, day
    )
    for name, s in zip(names, sums, strict=True):
        label = "inspections" if name == "one" else name
        hist[f"carrier_{label}_1y"] = np.where(rec, s, -1)
    last = last_event_before(carrier[rec], add[rec] + 1, day[rec], carrier, day)
    hist["carrier_days_since_inspection"] = np.where(rec & (last >= 0) & (day - last <= HISTORY_DAYS), day - last, -1)

    # Vehicle history: the same for the power unit's VIN (a valid VIN only), and the CVSA decals issued to it in the
    # 90 days before the inspection date (the decal is on the vehicle, so it counts from the next day on).
    vin = num["vin"].to_pandas()
    valid = valid_vin(vin).to_numpy()
    code = pd.factorize(vin.where(valid), sort=True)[0].astype(np.int64)
    names = ["one", "oos", "vehicle_oos"]
    sums = window_sums(
        code[valid], add[valid] + 1, day[valid] + HISTORY_DAYS, [num[c].to_numpy()[valid] for c in names], code, day
    )
    for name, s in zip(names, sums, strict=True):
        label = "inspections" if name == "one" else name
        hist[f"vehicle_{label}_1y"] = np.where(valid, s, -1)
    last = last_event_before(code[valid], add[valid] + 1, day[valid], code, day)
    hist["vehicle_days_since_inspection"] = np.where(valid & (last >= 0) & (day - last <= HISTORY_DAYS), day - last, -1)
    (decals,) = window_sums(
        code[valid], day[valid] + 1, day[valid] + DECAL_DAYS, [num["decal"].to_numpy()[valid]], code, day
    )
    hist["vehicle_decals_90d"] = np.where(valid, decals, -1)

    out = insp.with_columns([pl.Series(k, v, dtype=pl.Int64) for k, v in hist.items()])
    out.write_parquet(raw_dir / PREPARED_FILE)


class FmcsaRoadsideInspectionOutOfService1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a roadside inspection of a truck or bus put its driver or vehicle out of service, judged when the "
            "vehicle is picked for inspection?"
        ),
        use_case=(
            "An inspector at a weigh station or on the roadside, or FMCSA's inspection selection system that advises "
            "them, ranks the vehicles in front of them by how likely an inspection finds a defect or a driver "
            "violation serious enough to stop the vehicle, and inspects the riskiest first; the model is refit monthly."
        ),
        row=(
            "One roadside inspection of a commercial truck or bus in the US, December 2024 to October 2026 (5,518,542 "
            "inspections from FMCSA's national inspection database; the 1,778,366 that a split uses are kept)."
        ),
        predicted=(
            "Whether the inspection records at least one out-of-service violation: the driver, the vehicle or the "
            "hazardous load is ordered off the road until the problem is fixed."
        ),
        known=(
            "The date, start time and place of the inspection, whether it follows a crash, the vehicle's units, make, "
            "plate state and model year, its hazmat placard and cargo tank, the carrier's home state and authority, "
            "and the carrier's and the vehicle's inspections and out-of-service orders of the year before."
        ),
        split=(
            "Each of August, September and October 2026 is a test month; training is a random million inspections from "
            "December 2024 to a week before the month, as for a model refit monthly on the records uploaded by then."
        ),
        changes=(
            "We drop everything the inspection finds or records later (violation counts, the level performed, the end "
            "time, decals issued, searches), join the vehicle's units and build the carrier's and the vehicle's "
            "history of the year before."
        ),
        fit="direct",
        fit_reason=(
            "The inputs are what an inspector or the selection system knows when it picks a vehicle, and the windows "
            "follow a monthly refit. Labels exist only for vehicles that were inspected, as repayment only for granted "
            "loans; the carrier's size and safety scores of that date are not public, so the history is rebuilt from "
            "the inspections alone."
        ),
    )

    # Dataset
    unique_name = "fmcsa_roadside_inspection_out_of_service_1m"
    version_of = "fmcsa_roadside_inspection_out_of_service"
    version_comment = """
        Every train side holds 4.69M to 5.21M inspections, above the 1M-row budget, so the dataset ships only as this version (definitions.md, Lennart 2026-10-21). We sample per test window (v2 split protocol): each monthly window keeps all of its 246,280 to 263,507 inspections (under 500k), and its train side is a random 1M of all inspections from 1 December 2024 to 7 days before the window, drawn in one random order for all windows so the train sides overlap; the frame keeps only the 1,778,366 rows a split uses. The sample is random rather than the latest inspections, so the train sides cover every season.
    """
    year = "2026"  # the snapshot we pin: the view rolls daily over three years (PROV-9)
    domain = "industry & manufacturing"  # transport has no value of its own; as chicago_taxi_trip_duration_1m
    source = "GOV Website"
    source_url = "https://data.transportation.gov/d/fx4q-ay7w"
    license = "Public Domain"  # a US Government work; data.transportation.gov lists the rights as "public"
    data_tags = ("Spatial",)
    download_description = """
        FMCSA's "Vehicle Inspection File" (fx4q-ay7w) and "Inspections Per Unit" (wt8s-2hbx) on data.transportation.gov,
        read through the Socrata (SODA) API without a login on 2026-11-09: the inspections one CSV per month of the
        inspection date (2023-11 to 2026-11, every column), the units one CSV per first two digits of the inspection id.
        The view rolls daily over the last three years, so a later download holds other months; the API returns rows in
        no fixed order. Check each file's rows against the API's count (`$select=count(*)` with the same `$where`).
        The bulk export (api/views/<id>/rows.csv) streams at about 1 MB/s and is deprecated (sunset 2026-12-22).
        The view drops its oldest day every day, and the history of the first task rows reaches back to December 2023,
        so a download after December 2026 cannot rebuild this dataset: keep the files of this download.

        mkdir -p local-data-warehouse/fmcsa_roadside_inspection_out_of_service/{inspections_by_month,units_by_id_prefix}
        cd local-data-warehouse/fmcsa_roadside_inspection_out_of_service
        for m in $(seq 0 36); do
          ym=$(date -d "2023-11-01 +$m month" +%Y%m)
          curl -s --compressed -G "https://data.transportation.gov/resource/fx4q-ay7w.csv" \\
            --data-urlencode "\\$where=insp_date like '${ym}%'" --data-urlencode '$limit=10000000' \\
            -o "inspections_by_month/inspections_${ym}.csv"
        done
        for p in 80 81 82 83 84 85 86 87 88 89; do
          curl -s --compressed -G "https://data.transportation.gov/resource/wt8s-2hbx.csv" \\
            --data-urlencode "\\$where=inspection_id like '${p}%'" --data-urlencode '$limit=10000000' \\
            -o "units_by_id_prefix/units_${p}.csv"
        done
    """
    bibtex = r"""
        @misc{fmcsa_vehicle_inspection_file,
          author = {{Federal Motor Carrier Safety Administration}},
          title = {Vehicle Inspection File (MCMIS inspection data)},
          year = {2026},
          howpublished = {\url{https://data.transportation.gov/d/fx4q-ay7w}}
        }
    """
    curation_comments = """
        We start with FMCSA's MCMIS "Vehicle Inspection File" (data.transportation.gov fx4q-ay7w: 8,280,108 inspections dated 2023-11-08 to 2026-11-06, 63 columns) and its "Inspections Per Unit" view (wt8s-2hbx: 13,805,288 vehicle units), downloaded through the API on 2026-11-09.

        - Prediction point: the selection of a vehicle for a roadside inspection, before its level is chosen; the model ranks how likely the inspection ends with an out-of-service order (USE-1). FMCSA's Inspection Selection System advises inspectors on the same choice from the carrier's record. The view holds only inspected vehicles: the outcome exists only where an inspection took place, as repayment only for granted loans (no `Selection Bias` marker, selection.md).
        - Target: `out_of_service` is "Yes" when OOS_TOTAL, the inspection's count of out-of-service violations, is above 0 (19.5% of the task's rows). OOS_TOTAL is the sum of the driver, vehicle and hazmat counts on 99.85% of the records; we take it as published.
        - Rows: the inspections of 1 December 2024 to 31 October 2026, 5,518,542 rows. The 13 months before (2,727,675 inspections) only feed the history, so every row has a full year of it; the 31,657 inspections of 1 to 6 November 2026 are a partial month and are left out.
        - Copies: 2,234 records equal another in every column but the ids and the upload fields (one inspection uploaded twice under two ids); we keep the lower id, before the history is built, so the history counts each inspection once.
        - Dropped as recorded during or after the inspection (LEAK-10): the violation and out-of-service counts (all eight), the end time (the duration follows the findings), the registration date (when the repair of the defects was certified; set on 6.8% of records, 34% out of service against 18%), the alcohol and drug checks, the drug-interdiction search and arrests, and the unit's CVSA decal, which is issued only to a vehicle that passed. Not read: the violations view (876r-jsdb), whose rows are the inspection's findings.
        - Dropped as identifiers, names or processing fields: the inspection, report, SafetyNet and upload ids, the DOT and docket numbers (the carrier's history and the docket flag stand for them), the carrier's name, street, city, ZIP, colonia and state id, the shipper's name and shipping paper number, the unit's plate, company number and VIN (its model year is kept), and the status, census-match, version, upload, add, change and final-status dates and codes. REGION holds time-zone codes (CT, PT, ED, ...) instead of the dictionary's FMCSA regions, and SERVICE_CENTER is a region of the state: both repeat the state.
        - Kept as known when the inspection starts: the date and start time (local HHMM; no unknown 9999 among the task's rows), the reporting state (US for federal inspectors), the county, the site as written (`location_desc`, free text, 271k values), the facility (fixed or roadside), the hazmat placard and cargo-tank codes (a blank, no placard or tank recorded, is "Not applicable"; the cargo-tank code NON is "None"), the post-crash flag and whether a local agency inspects.
        - Dropped as recorded during the inspection (LEAK-10): the inspection level. The file holds the level performed, and an inspector may raise a driver-only inspection to a walk-around or full one on seeing a defect (practice described by compliance guides; no FMCSA rule on how a raised level is recorded was found). It is the strongest single input (ROC AUC 0.65 alone; without it LightGBM loses 0.057 to 0.058 ROC AUC, 0.737 to 0.744 against 0.794 to 0.802: 300 trees, a random 400k of each train side, the three shipped windows), and the part due to raised levels cannot be located row by row. So the prediction point is the selection of the vehicle, the decision the Inspection Selection System supports. The history still counts the carrier's past inspections by level.
        - Dropped as of unknown timing (LEAK-10): whether the inspection was done together with a traffic or a size-and-weight enforcement action. The dictionary says only "conducted in conjunction with", not whether the action came before the inspection; the two flags are worth 0.0008 to 0.0024 ROC AUC (same setup), about one standard error.
        - `gross_comb_veh_wt` (pounds) stays as recorded: 29,120 zeros and 13 values of 999,999 are missing. Its values are mostly round (120,000 on 14% of the rows, 117,000, 26,000, 80,000), registered or declared weights rather than a scale reading.
        - Decoded: the facility (F, R), the Y/N flags (U, unknown, is missing) and the unit types (13, unknown, and 15, 25 rows outside the dictionary, are missing). State codes NA, UK and ZZ (no or unknown state) are missing, and so are makes recorded as unknown (1,843 rows).
        - The vehicle: the number of units (1,001 inspections have no unit record), the power unit's (unit 1) type, make, plate state and model year, and the second unit's type. The make is written as a four-letter NCIC code in some records (FRHT) and as the name cut to ten characters in others (FREIGHTLIN); we give the 19 common spellings of 11 makes one name. The model year is the VIN's tenth character, read as the latest year of its 30-year cycle not after the year after the inspection (49 CFR 565.15), for the 99.2% of rows with a valid 17-character VIN.
        - The carrier's history (CLEAN-19, the features a selection system reads): the carrier's (DOT number) inspections of the 365 days before the inspection date that were in MCMIS before that date (added on an earlier day): their number, those at a level that checks the vehicle (1, 2, 5) or the driver (1, 2, 3), those with any, a vehicle or a driver out-of-service order, the violations, and the days since the last one (missing when none in the year: 7.2% of rows). The vehicle's history: the same for the power unit's VIN (inspections, any and vehicle out-of-service orders; the days since its last inspection are dropped, see the protocol below), and the CVSA decals issued to it in the 90 days before the inspection date (a decal stays on the vehicle up to three months). A re-derivation with plain filters on 300 random rows matched every value. Alone, the carrier's past out-of-service share scores ROC AUC 0.579 to 0.590 on the three test windows (the vehicle's 0.510 over all three); the history adds 0.022 to 0.029 to LightGBM (the vehicle's part 0.001 to 0.003), and the model without the level (0.737 to 0.744) beats the carrier's past share by 0.15 to 0.16 (TP-10, leg 1; numbers measured before the level and the flags were dropped, except the last).
        - Protocol (LEAK-9, an evaluation leak): every history count is valid at its own row's inspection date, but a later test row of the same vehicle or carrier reveals an earlier one's outcome through the change of its counts. With the vehicle's days since its last inspection, a participant matched 6% to 19% of test rows to the vehicle's next test row and lifted ROC AUC by 0.010, 0.023 and 0.034 on the three windows (the panel's task gamer); that column is dropped. Each test inspection is predicted from the training rows and its own features only; no feature or model step may use other test rows.
        - Open (LEAK-9, issue 1 of the review): the carrier's history chains the same way. Matching a test row to the carrier's next test row (same carrier state, interstate, docket and reporting state; its last carrier inspection on this row's date; one more inspection in the year) finds 10% to 13% of test rows, out of service at 35% to 37% when the next row's out-of-service count went up against 15% to 17% otherwise, and lifts LightGBM's ROC AUC by 0.0085, 0.0110 and 0.0124 on the three windows (0.7299 to 0.7384, 0.7327 to 0.7437, 0.7243 to 0.7367; a random noise column: 0.0001 or less; 300 trees, a random 300k of each train side, the level, the flags and the vehicle's days since dropped). The gain is above noise, so the protocol line alone does not close it: freezing each window's history at the window start needs a rebuild.
        - Raw files of this download, kept in the local warehouse because the view rolls daily (sha256): `inspections_202311.csv` 4481f8dd8f726bcaf252c401163041e5a75c08f28768875ae6dabbc376ca65e1; `inspections_202312.csv` 854669d573d94e7b6795b24699e3b390deca0569026c44796a09b07745209f63; `inspections_202401.csv` 22c8a60f8f505773fe2d54bbf6b732f20c91f6f4458c4abe062d7fcac5a647c4; `inspections_202402.csv` 5e6321ca373687d5aa2061fbb68ee68a95460a09db76dee809f8672b475119e2; `inspections_202403.csv` 07dc95683c4232272e26de0a53709ad5255cb85a94012029fcdef2d118434b99; `inspections_202404.csv` c1265883163fdbd4a54212768274a61d7cb331077fa656c22a5b84baa9ca65de; `inspections_202405.csv` d4f7c63abec4e31ad6e90fa734c87d16204f544e8f191efe8dcdefd0376e3cf9; `inspections_202406.csv` 22e76bd9845a2020c34d4c455535d966177e01cd0c7fce2207690e655d383aab; `inspections_202407.csv` 1d472ccc491612a89fdb40f8fa0cda6da7ea6e53e8860916b93e15a4eab533cf; `inspections_202408.csv` 9861a1cc90f6509261999bdb00dc58904e9ae386db173b3981869aaa494ad8f5; `inspections_202409.csv` be021f321905341a0296d8086776453cc9a1274b02405d56d956aceb8f7b4ce1; `inspections_202410.csv` ac6369a24d110d390c6904c7278a976fe8fe023ddb59bad59ef42a1c4b4a8453; `inspections_202411.csv` 7961b5d9666fb6286f73ee984ecabb2f1ac5f5abe9576bf82344218daafc03c1; `inspections_202412.csv` 350fe47257a73587bd4f9ed35542c001ccf97ce31ccceda22f9215c13fdf916d; `inspections_202501.csv` cb2622ec4276219f3197c164eac4db950d59faf5729a9863a3bad91c4dec048a; `inspections_202502.csv` bb2354ce17d48b2ae6ab71447f8bebc3d808e611edc95cd44458a38034c1ba0a; `inspections_202503.csv` e232d78ff9236707f14cf38bbdd24e413c2b12d02f3a0a3270f10d9499cf5789; `inspections_202504.csv` 14d1ad46bf683083600427f5a242a093afe90a4a54a7c1b68e1426c559f86359; `inspections_202505.csv` 1faf56e36c3ffe9b5cf37770c53a345cf9a2f70e621093eb6d4cec3b699fa87d; `inspections_202506.csv` 7c94e84bbbb07057e47bd80a1488d41bb78575c2efe60a398a9f3c22a8555f55; `inspections_202507.csv` 4ca77fa6df40a80ff03961488c3a2bf5fad3ae3a1b56e5549cc6acde04ff185d; `inspections_202508.csv` ab5e9d6026614d886d9c9a20b2a51c0b513ff2549b2a94272fc033e1696ef014; `inspections_202509.csv` 45dbdc5b86c833cdc9f80d2bb30f379b2671cd71f2281321d205aa95fc9b9003; `inspections_202510.csv` 54d4accca688ad019715b9860642a0feb4c4c4aa7b67c251c35bb23e7f53f21a; `inspections_202511.csv` 3cb732dd90450d9a812bc479195e441407583251190527972892668298be5665; `inspections_202512.csv` 4c3ee1dd8e4b7b69025ce3e2ef847a54d6ed96b1fa59478a9eb7dbf8d176fb0c; `inspections_202601.csv` 6f9546d34f76a8206794d7bd6587c2a6c864f9e16a8701a88f7b1917bd0de58c; `inspections_202602.csv` af1128b62e672a7bd7f8211390f9ad60e52d26f5b57811e5f12513463db995da; `inspections_202603.csv` dff431b4bbe3b0f8ab788cec5b3aee638ce6a3e1b20460596a61b66d4313b0bf; `inspections_202604.csv` e759ca659dd939be1da2e223067b1acf7eb00f92f2dea0b563f4f9a893bbea41; `inspections_202605.csv` 7caa993bbdc5e5bf678b10548ef00e043b4c46b8b0b228adc84f5601ffcad1db; `inspections_202606.csv` 8e4a9e7746400e4fbf5cd21c7116184757976e5037c3d9f9d6e184eb1e7398b4; `inspections_202607.csv` 7f51d58a370fde4835de6046f3c837ccb6dfa7e57144c5c0e2a2122d280d954b; `inspections_202608.csv` 228d3c51d2b6e2b622c639e3f46c1b00a0b85f431cddd5ccedf9f92bb19122b4; `inspections_202609.csv` 527f09415de122b4f76c38300d65e5cb5e67c9379822683b20cf7faadb198a33; `inspections_202610.csv` 00b7a329db71981cebbce762820f6dc85bfdc9e8d1e028bbf1c3b7ea2f2c3863; `inspections_202611.csv` 2b742ffbb15f7ee8a1c73c859eec31afbb5e772b8ff38851fc20bd99331ae9e0; `units_80.csv` 7d3a8babf707a4b255efbf2633d0be714a880431c2aed9cfe98156d4e2024a11; `units_81.csv` cb3ada9623ab6e31096ec71a14fed49d39fe4a5c77fbdff2a68f2877949130c7; `units_82.csv` 90fa94ef1b0f73833b7c3053e1f79475a55467940b570a1a65141f7279389ff9; `units_83.csv` f94ff39c28931401a42a8810d049f91b20eeee533cc0b976e90820a9993e6a48; `units_84.csv` 5554fc55c3cfbbe4326d53e85a643c019fee0b1a9f31031f92914576fc0af462; `units_85.csv` 2a50aa025eb2b75ae3400a3d9355e45a9127502d6319fb4ef2f0c34048ad65f9; `units_86.csv` febc69b6072ddaeb8ac0fcbf2564d41304aa86c2146df71421efe74c3ec81d21; `units_87.csv` 083430f7f6257bee6cd5691106cac78171d50fbb01f8c7aada82d706d19a1241; `units_88.csv` 8f4c87e4acf25526088afe4368de8a31dd713d1fc8ce87169e0924026d714517; `units_89.csv` 1042ffbf0d3e68979f43cfc043315f4de816058ae70b7fcbd2e666195e4f044f.
        - Not used: the carrier census (fleet size, drivers, cargo) and FMCSA's SMS scores. The public files give their state today, not on the inspection date (LEAK-10), so the history is rebuilt from the inspections alone. Driver data is not public.
        - Potential leak, kept on purpose: records change after upload, and the view holds each record as last changed. The transaction code marks a changed record: 14.3% of the records (703,671 task rows), out of service at 29.2% against 18.0% for unchanged ones (DataQs challenges can add or remove violations). The changed share falls with the age of the month: 12% to 16% in the months of 2025, 8.2% in June 2026, 6.8% in July, 10.4% in August, 6.2% in September and 3.9% in October. So the test months' labels are less corrected than the training rows', and a past inspection that counts in the history shows its outcome as corrected later; which way the test labels move is unknown, since a correction can go either way. The rise of the out-of-service share over the task (16.5% to 21.5%) holds also among records never changed (11.5% and 15.1% early to 20.9%), so it is drift, not a correction artefact. A second download in about three months, compared on the August to October 2026 labels, would show how much they move.
        - Score: ROC AUC pooled over all test inspections. Inspection sites differ in their out-of-service rates, so part of a pooled score can come from telling sites apart rather than ranking the vehicles at one site.
        - Anomaly: 13,371 report numbers are shared by 27,001 inspections that differ in more than their ids (other dates, carriers or outcomes in most): states reuse report numbers. We keep them as distinct inspections.
    """

    # Task
    target = "out_of_service"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "No source metric: the dataset page and the MCMIS data dictionary state no prediction task, and FMCSA's "
            "Inspection Selection System (ISS-CSA algorithm, ai.fmcsa.dot.gov/SMS/HelpFiles/ISS_Algorithm.pdf; not "
            "read in full, the server refuses this machine) ranks carriers by an inspection value from 1 to 100 "
            "without an evaluation metric. The decision is a ranking of vehicles to inspect, so ROC AUC on the "
            "probabilities."
        )
    )

    # Splits
    splits_comment = """
        A model refit each month: each of August, September and October 2026 is a test window (newest first), trained on the inspections from 1 December 2024 to 7 days before the window. The gap is the upload delay: an inspection reaches MCMIS a median of 2 days after it took place, 90% within 7 days and 99% within 56; without a gap 0.41% to 0.58% of each train side was not yet in MCMIS when the window started, with a gap of 7 days 0.06% to 0.16%. The newest month is near complete: from the upload delays of 2025, about 2.1% of October 2026's inspections had not been uploaded by the download (0.8% of August's), and late uploads are out of service less often (15.1% against 18.7%), which moves October's rate by under 0.1 points. Before sampling, each train side holds 85% to 94% of the task's rows (SPLIT-14's floor is 50%). Each window keeps all of its 246,280 to 263,507 inspections; each train side is a random 1M of its 4.69M to 5.21M earlier ones (one random order for all windows).
    """
    temporal = Temporal(
        on="inspection_date", splits=TemporalSplits(window=1, unit="months", n_windows=3, gap=7, gap_unit="days")
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        prepare_inspections(raw_dir)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow.parquet as pq

        # The inspections of the task's months, with the columns the task reads or drops for a reason of its own; the
        # rest of the 63 (ids, names, processing dates) stay in the prepared file. Text as categories, to fit memory.
        table = pq.read_table(
            raw_dir / PREPARED_FILE,
            columns=list(RAW_COLUMNS),
            filters=[("insp_date", ">=", TASK_START.replace("-", "")), ("insp_date", "<=", TASK_END.replace("-", ""))],
        )
        return table.to_pandas(strings_to_categorical=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame(index=raw.index)

        # 1. The target: was the driver, the vehicle or the hazardous load put out of service (any out-of-service
        #    violation; OOS_TOTAL is their sum).
        df[self.target] = np.where(_number(raw["oos_total"]) > 0, "Yes", "No")

        # 2. When and where: the date (the split key), the start time (HHMM, local), the state that reports the
        #    inspection, the county (state and FIPS code) and the site as the inspector wrote it.
        df["inspection_date"] = pd.to_datetime(raw["insp_date"].astype(object), format="%Y%m%d")
        hhmm = _number(raw["insp_start_time"])
        df["start_minute_of_day"] = ((hhmm // 100) * 60 + hhmm % 100) % 1440  # no 9999 (unknown) in the task's rows
        df["report_state"] = raw["report_state"]
        df["county"] = raw["county_code_state"].astype("string") + "-" + raw["county_code"].astype("string")
        df["location_desc"] = raw["location_desc"]

        # 3. The inspection as known when the vehicle is picked: the facility, whether it follows a crash, whether a
        #    local agency inspects, and the load (hazmat placard, cargo tank; blank: none recorded, "Not applicable").
        df["facility"] = raw["insp_facility"].map({"F": "Fixed", "R": "Roadside"})
        for col in ("local_enf_jurisdiction", "post_acc_ind"):
            df[col] = raw[col].map(YES_NO)  # U (unknown) and blanks are missing
        df["hazmat_placard_req"] = raw["hazmat_placard_req"].map(YES_NO).astype(object)
        df.loc[raw["hazmat_placard_req"].isna().to_numpy(), "hazmat_placard_req"] = "Not applicable"
        tank = raw["cargo_tank"].astype(object).replace({"NON": "None"})
        df["cargo_tank"] = tank.where(raw["cargo_tank"].notna().to_numpy(), "Not applicable")
        weight = _number(raw["gross_comb_veh_wt"])
        df["gross_comb_veh_wt"] = np.where((weight > 0) & (weight < 999_999), weight, np.nan)

        # 4. The carrier as recorded on the inspection: home state, interstate, and whether it has a docket (MC, MX
        #    or FF) number, the operating authority of a for-hire carrier.
        df["carrier_state"] = raw["insp_carrier_state"].mask(raw["insp_carrier_state"].isin(UNKNOWN_STATES))
        df["carrier_interstate"] = raw["insp_interstate"].map(YES_NO)
        df["carrier_has_docket"] = np.where(_number(raw["docket_number"]).fillna(0) > 0, "Yes", "No")

        # 5. The vehicle: the number of units, the power unit's type, make (one spelling per make), plate state and
        #    model year (from its VIN), and the second unit's type (the trailer of a combination).
        df["unit_count"] = raw["unit_count"]
        df["unit1_type"] = raw["unit1_type_id"].map(UNIT_TYPES)
        make = raw["unit1_make"].astype("string").str.strip().str.upper()
        make = make.replace(MAKE_NAMES).mask(make.isin(UNKNOWN_MAKES))
        df["unit1_make"] = make
        plate = raw["unit1_license_state"]
        df["unit1_license_state"] = plate.mask(plate.isin(UNKNOWN_STATES))
        df["unit1_model_year"] = vin_model_year(raw["unit1_vin"], df["inspection_date"].dt.year).astype("float64")
        df["unit2_type"] = raw["unit2_type_id"].map(UNIT_TYPES)

        # 6. The carrier's and the vehicle's history as of the inspection date (built in `prepare_inspections`); -1
        #    marks no valid VIN, or no inspection in the year before for the days since the last one.
        for col in SHIPPED_HISTORY:
            df[col] = raw[col].astype("float64").mask(raw[col] < 0)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "report_state",
                "county",
                "facility",
                "local_enf_jurisdiction",
                "post_acc_ind",
                "hazmat_placard_req",
                "cargo_tank",
                "carrier_state",
                "carrier_interstate",
                "carrier_has_docket",
                "unit1_type",
                "unit1_make",
                "unit1_license_state",
                "unit2_type",
            ],
            string=["location_desc"],
            datetime={"inspection_date": "%Y-%m-%d"},
        )
