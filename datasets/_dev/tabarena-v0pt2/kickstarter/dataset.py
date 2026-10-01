"""Curated dataset definition for `kickstarter` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class Kickstarter(AbstractCuratedDataset):
    # Dataset
    unique_name = "kickstarter"
    year = "2025"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://webrobots.io/kickstarter-datasets/"
    license = "None"
    data_tags = ("Spatial",)
    download_description = """
        There exists data from Kaggle (https://www.kaggle.com/datasets/yashkantharia/kickstarter-campaign).
        We use data from the original source (https://webrobots.io/kickstarter-datasets/) and downloaded the newest version at the time of writing.

        wget https://s3.amazonaws.com/weruns/forfun/Kickstarter/Kickstarter_2026-01-12T09_37_51_016Z.zip
        mkdir -p local-data-warehouse/kickstarter && mv Kickstarter_2026-01-12T09_37_51_016Z.zip local-data-warehouse/kickstarter && mkdir -p local-data-warehouse/kickstarter/data_files && unzip local-data-warehouse/kickstarter/Kickstarter_2026-01-12T09_37_51_016Z.zip -d local-data-warehouse/kickstarter/data_files
    """
    bibtex = r"""
        @misc{webrobots2026kickstarter,
          title        = {Kickstarter Datasets},
          author       = {{Web Robots}},
          howpublished = {\url{https://webrobots.io/kickstarter-datasets/}},
          note         = {Accessed: 2026-01-25},
          year         = {2026},
          organization = {Web Robots}
        }
    """
    curation_comments = """
        Similar to the Kaggle task, we aim to predict whether a Kickstarter project will be funded successfully. We simulate predicting at launch: only information known when the campaign starts is used.

        - The data we used only had 2 samples for 2026, so we stick to data until 2025.
        - The original data comes in .csv files per scrape data. We first combine all files into one file.
        - We remove all columns that are known only after the outcome and thus could leak information.
        - The fx_rate seems to show the conversion rate at the time of crawling the data and not at the time of the project. Thus, if it is used as on Kaggle, the numbers are wrong. We use the "usd_exchange_rate" to transform the goal into USD currency.
        - We drop the two entries with "disable_communication" as they point to other issues.
        - We drop photo and video based references as we do not include these modalities.
        - We decode the category and creator name  from JSON strings into usable columns.
        - Note, the crawl does only include blurbs and not the full-text descriptions of the projects. Also some blurb repeat from similar projects or orders.
        - We drop the creator's project profile (and its profile blurb): it is only created for funded projects (0 of 69,970 failed projects have a profile blurb), so it leaks the outcome, like spotlight.
        - We drop staff_pick: Kickstarter can award it during the campaign, so it is not known at launch (92.4% of staff picks succeed, against 57% of the other projects).
        - We decode the location display name from the location JSON string, which can include state and city name.
        - The data contains spatial information (city, state, country). We do not decode this but leave it to the pipelines.
        - We found 150 rows without location information. We drop these rows as it is unclear which issue caused this and how the rows' data might be affected by this.
        - We drop duplicates (20%) which seems to have occurred from multiple scrapes of the same project.
    """

    # Task
    target = "state"
    problem_type = "binary_classification"
    time_on = "created_at"  # could also be deadline to get more realistic data with projects for which we know the lab at "real" train time. But with our time splits, created_at is fine as well.

    # Splits
    splits_comment = """
        We try to create splits that simulate a model deployed to solve the task.

        The official data is updated monthly but has not enough data per month to create large enough test splits. We opt for simulating a model that is refit every year to obtain a robust test set.

         We could simulate a model that is refitted every month, but this would need many splits. Moreover, data from just one month is not enough to create a robust test set. We instead simulate a model that is refit every year. This introduces the unrealistic downside of data shift across a month that would not exist in a real-world model. We create 3 test splits by 2023, 2024, and 2025 as test year. For each test split, we use all data before the test month as training data.
    """
    time_horizon = 1
    time_horizon_unit = "years"
    temporal_splits = TemporalSplits(window=1, unit="years", cutoffs=(2023, 2024, 2025))

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        data_dir = raw_dir / "data_files"
        # Read and concatenate all CSV files
        df = pd.concat((pd.read_csv(csv_file) for csv_file in data_dir.glob("*.csv")), ignore_index=True)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Filter to successful or failed projects
        df = df[df["state"].isin(["successful", "failed"])]
        # Drop rows with missing location information
        df = df[~df["location"].isna()]
        # Convert goal to USD
        non_usd_mask = df["currency"] != "USD"
        df.loc[non_usd_mask, "goal"] = df.loc[non_usd_mask, "goal"] * df.loc[non_usd_mask, "usd_exchange_rate"]
        # Use only full country name
        df["country"] = df["country_displayable_name"]
        df = df.drop(columns=["country_displayable_name"])
        # drop disable_communication artifacts
        df = df[df["disable_communication"].eq(False)]
        df = df.drop(columns=["disable_communication"])
        # We do not include images for this benchmark, so we drop the related columns
        df = df.drop(columns=["photo", "video"])
        # Drop other columns
        drop_columns = [
            # Remove target leakage columns
            "backers_count",
            "converted_pledged_amount",
            "is_in_post_campaign_pledging_phase",
            "percent_funded",
            "pledged",
            "static_usd_rate",
            "usd_pledged",
            "usd_type",
            "usd_exchange_rate",
            "state_changed_at",
            "spotlight",
            # Mid-campaign: "Projects We Love" can be awarded while the campaign runs (92% of staff picks succeed)
            "staff_pick",
            # Remove currency related columns not need anymore
            "currency",
            "currency_symbol",
            "currency_trailing_code",
            "current_currency",
            "fx_rate",
            # all unique
            "is_disliked",
            "is_launched",
            "is_liked",
            "is_starrable",
            # We got the date from created_at
            "id",
            # Just formating of name
            "slug",
            # No relation / not needed
            "source_url",
            "urls",
        ]
        df = df.drop(columns=drop_columns)
        # Decode category
        df["main_category"] = df["category"].apply(lambda x: json.loads(x)["name"])
        df["sub_category"] = df["category"].apply(lambda x: json.loads(x).get("parent_name", np.nan))
        df = df.drop(columns=["category"])

        # The creator's project profile (its blurb, colours, links) only exists for funded projects: the profile
        # blurb is present for 34,032 successful and 0 of 69,970 failed projects, so it leaks the outcome
        df = df.drop(columns=["profile"])

        # Decode creator name
        def decode_name(x):
            try:
                data = json.loads(x)
            except json.decoder.JSONDecodeError:
                raw_data = x.split(",")
                raw_data = [e for e in raw_data if e.startswith('"name":')]
                assert len(raw_data) == 1
                name_entry = raw_data[0]
                name_entry = name_entry.replace('"name":"', "").rstrip('"')
                return name_entry
            return data["name"]

        df["creator_name"] = df["creator"].apply(decode_name)
        df = df.drop(columns=["creator"])
        # Decode location
        df["location_displayable_name"] = df["location"].apply(lambda x: json.loads(x)["displayable_name"])
        df = df.drop(columns=["location"])
        # Dtypes
        as_string_cols = [
            "blurb",
            "name",
            "creator_name",
            "location_displayable_name",
        ]
        as_date_cols = [
            "created_at",
            "launched_at",
            "deadline",
        ]
        for c in as_string_cols:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        for c in as_date_cols:
            df[c] = pd.to_datetime(df[c], unit="s")
        # Drop duplicates
        df = df.drop_duplicates()
        # Drop the 2 samples from 2026
        df = df[df["created_at"].dt.year < 2026]
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "prelaunch_activated",
                "main_category",
                "sub_category",
                "country",
            ],
        )
