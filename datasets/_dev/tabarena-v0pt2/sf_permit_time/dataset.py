"""Curated dataset definition for `sf_permit_time` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class SfPermitTime(AbstractCuratedDataset):
    # Dataset
    unique_name = "sf_permit_time"
    year = "2025"
    domain = "business & marketing"
    source = "GOV Website"
    source_url = "https://data.sfgov.org/Housing-and-Buildings/Building-Permits/i98e-djp9"
    license = "Open Data Commons Public Domain Dedication and License"
    download_description = """
        We re-collected the data similar to how the data from Kaggle was created.

        We go to https://data.sfgov.org/Housing-and-Buildings/Building-Permits/i98e-djp9, then we set the query such that we only take data from 1st of January 2015 until 31st of December of 2025, and then download the data as a CSV file. Due to API limits, this must be done manually. Here is the link to the query: https://data.sfgov.org/Housing-and-Buildings/Building-Permits/i98e-djp9/explore/query/SELECT%0A%20%20%60permit_number%60%2C%0A%20%20%60permit_type%60%2C%0A%20%20%60permit_type_definition%60%2C%0A%20%20%60permit_creation_date%60%2C%0A%20%20%60block%60%2C%0A%20%20%60lot%60%2C%0A%20%20%60street_number%60%2C%0A%20%20%60street_number_suffix%60%2C%0A%20%20%60street_name%60%2C%0A%20%20%60street_suffix%60%2C%0A%20%20%60unit%60%2C%0A%20%20%60unit_suffix%60%2C%0A%20%20%60description%60%2C%0A%20%20%60status%60%2C%0A%20%20%60status_date%60%2C%0A%20%20%60filed_date%60%2C%0A%20%20%60issued_date%60%2C%0A%20%20%60completed_date%60%2C%0A%20%20%60first_construction_document_date%60%2C%0A%20%20%60approved_date%60%2C%0A%20%20%60structural_notification%60%2C%0A%20%20%60number_of_existing_stories%60%2C%0A%20%20%60number_of_proposed_stories%60%2C%0A%20%20%60voluntary_soft_story_retrofit%60%2C%0A%20%20%60fire_only_permit%60%2C%0A%20%20%60estimated_cost%60%2C%0A%20%20%60revised_cost%60%2C%0A%20%20%60existing_use%60%2C%0A%20%20%60existing_units%60%2C%0A%20%20%60proposed_use%60%2C%0A%20%20%60proposed_units%60%2C%0A%20%20%60plansets%60%2C%0A%20%20%60tidf_compliance%60%2C%0A%20%20%60existing_occupancy%60%2C%0A%20%20%60proposed_occupancy%60%2C%0A%20%20%60existing_construction_type%60%2C%0A%20%20%60existing_construction_type_description%60%2C%0A%20%20%60proposed_construction_type%60%2C%0A%20%20%60proposed_construction_type_description%60%2C%0A%20%20%60site_permit%60%2C%0A%20%20%60last_permit_activity_date%60%2C%0A%20%20%60application_submission_method%60%2C%0A%20%20%60adu%60%2C%0A%20%20%60primary_address_flag%60%2C%0A%20%20%60supervisor_district%60%2C%0A%20%20%60neighborhoods_analysis_boundaries%60%2C%0A%20%20%60zipcode%60%2C%0A%20%20%60location%60%2C%0A%20%20%60point_source%60%2C%0A%20%20%60reroof%60%2C%0A%20%20%60record_id%60%2C%0A%20%20%60data_as_of%60%2C%0A%20%20%60data_loaded_at%60%0AWHERE%0A%20%20%60approved_date%60%0A%20%20%20%20BETWEEN%20%222015-01-01T16%3A13%3A34%22%20%3A%3A%20floating_timestamp%0A%20%20%20%20AND%20%222025-12-31T16%3A13%3A34%22%20%3A%3A%20floating_timestamp%0AORDER%20BY%20%60approved_date%60%20ASC%20NULL%20LAST/page/filter

        We save the file in the root dir as Building_Permits_20260205.csv
        mkdir -p local-data-warehouse/sf_permit_time && mv Building_Permits_20260205.csv local-data-warehouse/sf_permit_time
    """
    bibtex = r"""
        @misc{SanFrancisco2026BuildingPermits,
          author = {{City and County of San Francisco}},
          title  = {Building Permits},
          year   = {2026},
          howpublished = {\url{https://data.sfgov.org/Housing-and-Buildings/Building-Permits/i98e-djp9/about_data}},
          note   = {DataSF Open Data Portal dataset, Accessed: 2026-02-05}
        }
    """
    curation_comments = """
        We simulate the task of predicting the days (in float) it takes to issue the permit. We add the special use case, that we assume the model is only used to predict for permits that take longer than one day to be issued. We do this, as waiting for one day seems very reasonable. Plus, the data contains several unresolvable data errors when the permit was issued on the same day it was filed.

        - ALthough we donwloaded data
        - We drop miscellaneous permits (those that start with "M") as they are not of interest for our task. Compared to normal permits, these are usually automatically or very quickly approved and thus are not relevant to predict the time it takes to issue the permit. Moreover, the represent a significant distribution shift compared to the rest of the data.
        - We drop the permit type ordinal encoding and the creation date of the permit in the tracking system as other dates are more accurate.
        - A large number of descriptions are from standard phrases (they appear in the same way multiple times). so we add a new column that indicates whether the description is from a standard phrase or not through a categorical variable. We define a standard phrase as a description that appears more than 100 times in the dataset.
        - The 'Current Status' is the last status update of the permit. Note, that for miscellaneous permits, the permit is never completed. We filter to permits that have been issued for our task. Thus, we select all permits that are issued or completed.
        - There are several features that have almost no information (up to only 20 non nan values). We keep this and let the pipeline decide what to do with them.
        - We only keep on permit per primary address (filter based on Primary Address Flag) following https://data.sfgov.org/Housing-and-Buildings/Building-Permits-Deduplicated-on-Primary-Address/f2jc-ivnc
        - We drop all permits without a location, as every permit requires a location by definition, thus these are likely data errors.
    """

    # Task
    target = "DaysToIssue"
    problem_type = "regression"
    time_on = "Filed Date"

    # Splits
    splits_comment = """
        We try to create splits that simulate a model deployed to solve the task.

        The official data is updated daily but has not enough data per day to create large enough test splits. We opt for simulating a model that is refit every year to obtain a robust test set instead.
        This introduces the unrealistic downside of data shift across a month that would not exist in a real-world model. We create 5 test splits by 2020-2025 as test year. For each test split, we use all data before the test month as training data.
    """
    time_horizon = 1
    time_horizon_unit = "years"
    temporal_splits = TemporalSplits(window=1, unit="years", cutoffs=(2020, 2021, 2022, 2023, 2024, 2025))

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "Building_Permits_20260205.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["DaysToIssue"] = (
            pd.to_datetime(df["Issued Date"]) - pd.to_datetime(df["Filed Date"])
        ).dt.total_seconds() / pd.Timedelta(days=1).total_seconds()
        df = df[df["DaysToIssue"] >= 1]
        df = df[~df["Permit Number"].str.startswith("M")]
        df = df[df["Current Status"].isin(["issued", "complete"])]
        df = df[df["Primary Address Flag"] == "Y"]
        df = df[~df["Location"].isna()]
        df["DescriptionIsStandardPhrase"] = df["Description"].isin(
            df["Description"].value_counts(dropna=False)[df["Description"].value_counts(dropna=False) > 100].index
        )
        df["Location_Latitude"] = df["Location"].apply(lambda x: str(x).split("(")[-1].split(" ")[0]).astype(float)
        df["Location_Longitude"] = (
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
        as_string_type = [
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
        ]
        as_datetime_type = ["Filed Date"]
        for c in as_string_type:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        for c in as_datetime_type:
            df[c] = pd.to_datetime(df[c])
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
        )
