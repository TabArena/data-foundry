"""Curated dataset definition for `sf_permit_time` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    Splits,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

SECONDS_PER_DAY = 86_400
# Half-year test windows; train is the permits filed at least six months before the window starts
WINDOWS = TemporalSplits(window=6, unit="months", gap=6, min_train_fraction=0.5)
# The start of the oldest test window: descriptions are counted over the permits filed before it, known in every window
PHRASE_HISTORY_END = pd.Timestamp("2020-01-01")
STANDARD_PHRASE_COUNT = 100  # a description filed more than this many times by then is a standard phrase


def _issued(df: pd.DataFrame) -> pd.Series:
    """The issue date, rebuilt from the filing date and the target (the log of the days to issue).

    Both dates in the raw file are whole seconds, so rounding to the second gives the raw issue date back.
    """
    days = np.exp(df["DaysToIssue"])
    return (df["Filed Date"] + pd.to_timedelta(days * SECONDS_PER_DAY, unit="s")).dt.round("s")


def _label_known_windows(df: pd.DataFrame) -> tuple[Splits, pd.DataFrame]:
    """The windows of `WINDOWS`, each training only on the permits issued before it starts.

    Returns the splits and, per window, the training rows kept and left out (the evidence in `_decisions`).
    """
    filed, issued = df["Filed Date"], _issued(df)
    splits, rows = {}, []
    for split, folds in WINDOWS.splits(df, "Filed Date").items():
        train, test = (np.asarray(side) for side in folds[0])
        start = filed.iloc[test].min().normalize().replace(day=1)
        known = (issued.iloc[train] < start).to_numpy()
        splits[split] = {0: (train[known].tolist(), test.tolist())}

        still_open = issued >= start
        one, six, twelve = (start - pd.DateOffset(months=m) for m in (1, 6, 12))
        filed_1_6 = (filed >= six) & (filed < one)
        filed_6_12 = (filed >= twelve) & (filed < six)
        rows.append(
            {
                "window start": f"{start:%Y-%m}",
                "test rows": len(test),
                "train rows": int(known.sum()),
                "train rows left out (issued after the start)": int((~known).sum()),
                "still open at the start: filed 1-6 months before": f"{still_open[filed_1_6].mean():.0%}",
                "filed 6-12 months before": f"{still_open[filed_6_12].mean():.0%}",
            }
        )
    return splits, pd.DataFrame(rows).set_index("window start")


class SfPermitTime(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("How many days will San Francisco take to issue a building permit that has just been filed?"),
        use_case=(
            "For example, at filing the city's permit office or the applicant estimates how long the permit will "
            "take, to plan staff or the construction schedule."
        ),
        row=(
            "One building permit filed in San Francisco from 2015 to 2023 and issued by the download in February "
            "2026, without the quick miscellaneous permits (99,847 permits)."
        ),
        predicted=("The days from filing to issue, on a log scale; one permit in ten takes more than 315 days."),
        known=(
            "The permit type and description, the address and location, the existing and proposed use, occupancy and "
            "construction type, stories and units, the estimated cost, the plan sets, how it was submitted, and flags"
            " such as site permit or fire-only."
        ),
        split=(
            "Each test window is a half-year of filings, 2020 to 2023; training is the permits filed at least six "
            "months earlier and issued before the window starts, as for a model refit every six months."
        ),
        changes=(
            "We keep filings before 2024, as later ones still miss their slow permits, drop dates and fields recorded"
            " after filing, and leave a six-month gap before each test window."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is known at filing, and the windows mirror a refit with the permits issued by "
            "then. Permits never issued are not in the data, so the task is the wait of a permit that gets issued."
        ),
    )

    # Dataset
    unique_name = "sf_permit_time"
    year = "2026"  # the snapshot we pin; the source grows over time
    domain = "business & marketing"
    source = "GOV Website"
    source_url = "https://data.sf.gov/Housing-and-Buildings/Building-Permits/i98e-djp9"
    license = "Open Data Commons Public Domain Dedication and License"
    download_description = """
        We re-collected the data similar to how the data from Kaggle was created.

        We download the Building Permits table from the San Francisco open data portal
        (https://data.sf.gov/Housing-and-Buildings/Building-Permits/i98e-djp9; formerly data.sfgov.org), filtered to
        permits filed from 1st of January 2015 until 31st of December 2025 (`filed_date`), as a CSV file. Due to API
        limits, this must be done manually in the portal's query editor. Our copy was downloaded on 2026-02-05 (the
        latest issued date in it is 2026-02-04); the table changes daily, so a new download gives different data.

        We save the file in the root dir as Building_Permits_20260205.csv
        mkdir -p local-data-warehouse/sf_permit_time && mv Building_Permits_20260205.csv local-data-warehouse/sf_permit_time
    """
    bibtex = r"""
        @misc{SanFrancisco2026BuildingPermits,
          author = {{City and County of San Francisco}},
          title  = {Building Permits},
          year   = {2026},
          howpublished = {\url{https://data.sf.gov/Housing-and-Buildings/Building-Permits/i98e-djp9/about_data}},
          note   = {DataSF Open Data Portal dataset, Accessed: 2026-02-05}
        }
    """
    curation_comments = """
        We start with the Building Permits table of the San Francisco open data portal (permits filed 2015 to 2025, downloaded 2026-02-05).

        - Prediction point: at filing. Target: the log of the days from Filed Date to Issued Date, for permits issued at least one day after filing; waiting a day is no burden, and same-day permits hold unresolvable data errors.
        - Cohort: permits filed before 2024. The download holds only permits issued by then, so recent filings miss their slowest permits: 1.8-5.3% are still open for 2015-2021, 10.2% for 2023 and 21.5% for 2025. In October 2026 the 2023 tail had settled (p90 216 -> 222 days), the 2025 one had not (97 -> 160).
        - Cohort: no miscellaneous permits (numbers starting with "M"); they are approved automatically or very fast and shift the distribution.
        - Cohort: issued or complete permits (Current Status), one per primary address (Primary Address Flag, as in the portal's deduplicated table) and with a location; a permit without one is a data error.
        - We drop the dates recorded after filing (Issued, Completed, First Construction Document, approved_date, Current Status and Last Permit Activity dates), Current Status, Revised Cost (most likely set at plan review), the ordinal codes of Permit Type and the construction types, Permit Creation Date (a system log date), ADU (deprecated from 2025), Record ID, Permit Number and the portal's load metadata.
        - Location (WKT "POINT (lon lat)") becomes longitude and latitude. DescriptionIsStandardPhrase marks descriptions filed more than 100 times before 2020, the start of the oldest test window, so it counts no filing of a test window (until 2026-10-19 it counted the whole table). Nearly empty columns (some with 20 values) stay for the pipeline to handle.
        - Split: training holds only the permits issued before the window starts, after a six-month gap (splits_comment, decision table). At a window start 3.0-6.7% of the earlier permits are still open (median 310-520 days to issue); with their labels and the filing time as a number, LightGBM learned the 2020 slowdown from permits issued during the test window (RMSE 1.19 instead of 1.52 on 2020-H2). A one-month gap, as in brazilian_ecommerce, is too short: 21-34% of the permits filed 1-6 months before a window are still open, and LightGBM trained on the rest predicts 0.58 log days too fast.
        - Anomaly: Current Status is read at the download, so the status filter also drops 4,316 permits that were issued and later expired (2,764), cancelled (1,093), reinstated, suspended or revoked (4.1% of the cohort). We keep the filter.
    """

    # Task
    target = "DaysToIssue"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason="The source is the City of San Francisco's open-data Building Permits table (DataSF), with no prediction task or metric; the task (time to issue at filing) is ours. For a waiting time of days to years the error that matters is relative to the time, so RMSLE on the days.",
        target_transform="log",
    )

    # Splits
    splits_comment = """
        A model refit at the start of each half-year predicts the days to issue of the permits filed in the next six months. It trains on the permits filed at least six months before the refit that were issued by then. The days to issue are known only once a permit is issued and have a long tail (p90 315 days), so many recent permits are still open at a refit and the issued ones are the fast ones. The gap leaves out the newest filings, and older permits still open at the refit are left out of that window's training rows (decision table). The test windows walk back from the second half of 2023, the newest filings kept (see curation_comments), while the training side keeps at least 50% of the rows: 8 windows, 2020-H1 to 2023-H2, newest first, with 52,851 to 89,314 training rows. The convention's 9 windows for a dataset of this size do not fit above the 50% floor with the gap.
    """
    temporal = Temporal(on="Filed Date", horizon=6, horizon_unit="months", gap=6, gap_unit="months")
    accepted_check_warnings = {
        "dataset_constant_column": "The flagged columns are Y-or-missing flags (e.g. Fire Only Permit: Y in 12,204 rows); "
        "missing means the flag is not set, so they are not constant.",
        "splits_rows_unused": "193 permits filed before 2020 (1,306 to 3,428 days to issue) are in no split: they were "
        "filed before the oldest test window and were still open when the newest one started.",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "Building_Permits_20260205.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["DaysToIssue"] = (
            pd.to_datetime(df["Issued Date"]) - pd.to_datetime(df["Filed Date"])
        ).dt.total_seconds() / pd.Timedelta(days=1).total_seconds()
        df = df[df["DaysToIssue"] >= 1]
        df = df[pd.to_datetime(df["Filed Date"]) < "2024-01-01"]
        df = df[~df["Permit Number"].str.startswith("M")]
        df = df[df["Current Status"].isin(["issued", "complete"])]
        df = df[df["Primary Address Flag"] == "Y"]
        df = df[~df["Location"].isna()]
        # Standard phrases: descriptions filed more than 100 times before the oldest test window, so no window's flag
        # depends on its own or later filings
        counts = df.loc[pd.to_datetime(df["Filed Date"]) < PHRASE_HISTORY_END, "Description"].value_counts(dropna=False)
        df["DescriptionIsStandardPhrase"] = df["Description"].isin(counts.index[counts > STANDARD_PHRASE_COUNT])
        # Location is WKT "POINT (longitude latitude)"
        df["Location_Longitude"] = df["Location"].apply(lambda x: str(x).split("(")[-1].split(" ")[0]).astype(float)
        df["Location_Latitude"] = (
            df["Location"].apply(lambda x: str(x).split("(")[-1].split(" ")[-1][:-1]).astype(float)
        )
        df = df.drop(
            columns=[
                "Permit Creation Date",  # Just a log date from the system.
                "Permit Type",  # Ordinal encoding of "Permit Type Definition"
                "Current Status",  # repeat information from other columns, also leaks into the future
                "Current Status Date",  # leaks into the future and the target
                "Completed Date",  # completed happens after issuing, so this is after our task and outside of the control of the government body that issues the permit. Moreover, it leaks the target variable.
                "First Construction Document Date",  # same as above
                "approved_date",  # often the same value as issued date depending on the type of permit, thus leakage
                "Issued Date",  # Target leakage
                "Revised Cost",  # Also only available after the permit is issued most likely (after project review)
                "Existing Construction Type",  # Ordinal encoding of "Existing Construction Type Description"
                "Proposed Construction Type",  # Ordinal encoding of "Proposed Construction Type Description"
                "Last Permit Activity Date",  # target leakage
                "ADU",  # Deprecated column from 2025 onwards
                "Primary Address Flag",  # constant after filter above
                "Record ID",  # Unique ID
                "data_as_of",  # metadata from logging system
                "data_loaded_at",  # metadata from logging system
                "Location",  # resolved above
                "Permit Number",  # meaningless ID given other info
            ]
        )
        # Whole numbers that pandas reads as int or as float (with missing values); as nullable integers their strings
        # read "1625", "94116", not "1625.0", "94116.0".
        for c in ["Street Number", "Unit", "Zipcode"]:
            df[c] = df[c].astype("Int64")
        # Log scale the target
        df["DaysToIssue"] = np.log(df["DaysToIssue"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Permit Type Definition",
                "DescriptionIsStandardPhrase",
                "Structural Notification",
                "Voluntary Soft-Story Retrofit",
                "Fire Only Permit",
                "TIDF Compliance",
                "Existing Construction Type Description",
                "Proposed Construction Type Description",
                "Site Permit",
                "Application Submission Method",
                "supervisor_district",
                "neighborhoods_analysis_boundaries",
                "point_source",
                "reroof",
            ],
            string=[
                "Block",
                "Lot",
                "Street Number",
                "Street Number Suffix",
                "Street Name",
                "Street Suffix",
                "Unit",
                "Unit Suffix",
                "Description",
                "Existing Use",
                "Proposed Use",
                "Existing Occupancy",
                "Proposed Occupancy",
                "Zipcode",
            ],
            datetime=["Filed Date"],
        )

    def _make_splits(self, df: pd.DataFrame) -> Splits:
        """Half-year windows after a six-month gap; train keeps only the permits issued before the window starts."""
        splits, windows = _label_known_windows(df)
        oldest = pd.Timestamp(windows.index.min())
        assert oldest >= PHRASE_HISTORY_END, f"the oldest window starts {oldest:%Y-%m}, before the phrase history ends"
        return splits

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        _, windows = _label_known_windows(df)
        return [
            Decision(
                "Training rows are permits filed six months or more before the window and issued before it starts",
                "The days to issue are known only once a permit is issued, and many permits filed shortly before a "
                "window are still open when it starts; the issued ones are the fast ones. The six-month gap leaves "
                "out the newest filings, and the older permits still open at the start are left out of that "
                "window's training rows.",
                windows,
            )
        ]
