"""Curated dataset definition for `sf_permit_time` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Temporal, TemporalSplits


class SfPermitTime(AbstractCuratedDataset):
    # Dataset
    unique_name = "sf_permit_time"
    year = "2025"
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
        We simulate the task of predicting the days (in float) it takes to issue the permit. We add the special use case, that we assume the model is only used to predict for permits that take longer than one day to be issued. We do this, as waiting for one day seems very reasonable. Plus, the data contains several unresolvable data errors when the permit was issued on the same day it was filed.

        - We only keep permits filed before 2024. The data only holds permits that were issued by the download date, so recent filings miss their slowest permits: the share of permits still open is 1.8-5.3% for 2015-2021 but 10.2% for 2023, 11.1% for 2024 and 21.5% for 2025, and the p90 of the days to issue falls from about 300 days to 147 (2024) and 97 (2025). A check against the portal eight months later (October 2026) showed the 2024 and 2025 tails still growing (2025 p90: 97 -> 160 days), while 2023 had nearly settled (216 -> 222).
        - We drop miscellaneous permits (those that start with "M") as they are not of interest for our task. Compared to normal permits, these are usually automatically or very quickly approved and thus are not relevant to predict the time it takes to issue the permit. Moreover, the represent a significant distribution shift compared to the rest of the data.
        - We drop the permit type ordinal encoding and the creation date of the permit in the tracking system as other dates are more accurate.
        - A large number of descriptions are from standard phrases (they appear in the same way multiple times). so we add a new column that indicates whether the description is from a standard phrase or not through a categorical variable. We define a standard phrase as a description that appears more than 100 times in the dataset.
        - The 'Current Status' is the last status update of the permit. Note, that for miscellaneous permits, the permit is never completed. We filter to permits that have been issued for our task. Thus, we select all permits that are issued or completed.
        - There are several features that have almost no information (up to only 20 non nan values). We keep this and let the pipeline decide what to do with them.
        - We only keep on permit per primary address (filter based on Primary Address Flag) following https://data.sf.gov/Housing-and-Buildings/Building-Permits-Deduplicated-on-Primary-Address/f2jc-ivnc
        - We drop all permits without a location, as every permit requires a location by definition, thus these are likely data errors.
    """

    # Task
    target = "DaysToIssue"
    problem_type = "regression"

    # Splits
    splits_comment = """
        We try to create splits that simulate a model deployed to solve the task.

        The official data is updated daily but has not enough data per day to create large enough test splits. We simulate a model that is refit every six months and tested on the next six months, walking back from the last kept filing date (end of 2023) until the training data would fall below 50% of the rows. This gives 9 half-year test windows from the second half of 2019 to the second half of 2023. For each test split, we use all permits filed before the test window as training data.
    """
    temporal = Temporal(
        on="Filed Date",
        splits=TemporalSplits(window=6, unit="months", min_train_fraction=0.5),
    )
    accepted_check_warnings = {
        "dataset_constant_column": "The flagged columns are Y-or-missing flags (e.g. Fire Only Permit: Y in 12,204 rows); "
        "missing means the flag is not set, so they are not constant.",
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
        df["DescriptionIsStandardPhrase"] = df["Description"].isin(
            df["Description"].value_counts(dropna=False)[df["Description"].value_counts(dropna=False) > 100].index
        )
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
