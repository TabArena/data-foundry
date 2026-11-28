"""Curated dataset definition for `kickstarter` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
)


class Kickstarter(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a Kickstarter project reach its funding goal?",
        use_case=(
            "For example, Kickstarter, when a campaign launches, estimates whether it will reach its goal, to decide "
            "which projects to feature."
        ),
        row=(
            "One Kickstarter project that ended funded or failed, launched from April 2009 to 13 November 2025, from "
            "Web Robots' monthly scrapes (pinned January 2026; 185,444 projects)."
        ),
        predicted="Whether it reached its funding goal by its deadline (62.50% did).",
        known=(
            "The goal in US dollars, the creation, launch and deadline dates, the category and subcategory, the "
            "location, the project's name and short description, the creator's name, and whether it had a pre-launch "
            "page."
        ),
        split=(
            "Each test window is half a year of projects by launch date, nine half-years from 2020 to 2025; training "
            "is every project launched more than 60 days (the longest campaign) before the window starts, as for a "
            "model refit every half-year on the campaigns that had ended."
        ),
        changes=(
            "We drop everything recorded after launch (pledges, backers, staff pick, the creator's project profile, "
            "which only funded projects have), convert goals to US dollars at each project's own rate, remove "
            "projects repeated across scrapes (20%), and drop the projects launched in the last 60 days before the "
            "scrape, whose outcomes it holds only for the campaigns that had already ended."
        ),
        fit="approximate",
        fit_reason=(
            "Everything the model sees is known at launch, and later half-years are tested, but the scrapes do not "
            "cover every project: 62.5% of those here are funded, 87% to 97% of the 2009-2013 launches, against the "
            "44% Kickstarter reported in 2012, so failed projects are under-covered, the more so in the older years."
        ),
    )

    # Dataset
    unique_name = "kickstarter"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://webrobots.io/kickstarter-datasets/",
            license=None,  # Web Robots states none for its datasets; its terms cover its scraping service
            year="2026",  # the snapshot we pin; the source grows over time
            bibtex=r"""
                @misc{webrobots2026kickstarter,
                  title        = {Kickstarter Datasets},
                  author       = {{Web Robots}},
                  howpublished = {\url{https://webrobots.io/kickstarter-datasets/}},
                  note         = {Accessed: 2026-01-25},
                  year         = {2026},
                  organization = {Web Robots}
                }
            """,
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        There exists data from Kaggle (https://www.kaggle.com/datasets/yashkantharia/kickstarter-campaign).
        We use data from the original source (https://webrobots.io/kickstarter-datasets/) and downloaded the newest version at the time of writing.

        wget https://s3.amazonaws.com/weruns/forfun/Kickstarter/Kickstarter_2026-01-12T09_37_51_016Z.zip
        mkdir -p local-data-warehouse/kickstarter && mv Kickstarter_2026-01-12T09_37_51_016Z.zip local-data-warehouse/kickstarter && mkdir -p local-data-warehouse/kickstarter/data_files && unzip local-data-warehouse/kickstarter/Kickstarter_2026-01-12T09_37_51_016Z.zip -d local-data-warehouse/kickstarter/data_files
    """
    curation_comments = """
        Similar to the Kaggle task, we aim to predict whether a Kickstarter project will be funded successfully. We simulate predicting at launch: only information known when the campaign starts is used.

        - The data we used only had 2 samples for 2026, so we stick to data until 2025.
        - The scrape's cut (Lennart, 2026-11-11): the scrape of 12 January 2026 holds only projects that had ended (its newest deadline is 12 January 2026 11:00), so the newest launches are missing those still running then, and the missing ones succeed more often (cut the same way a year earlier, 20% of the projects created in 2024 would be missing, 73.9% successful against 66.9% for the rest). A campaign runs at most 60 days by Kickstarter's rule (https://help.kickstarter.com/hc/en-us/articles/115005128434-What-is-the-maximum-project-duration; a few thousand in the data run longer, up to 121 days), so we drop the projects launched from 13 November 2025 11:00 on, 60 days before that deadline: 1,673 projects, 74.2% successful. 185,444 projects remain, 62.50% successful.
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
        - Coverage (Andrej, 2026-11-11; record marker `Selection Bias`): failed projects are under-covered in the older
          years. Kickstarter reported 60,786 launched projects by June 2012, 44% funded (Engadget, 21 June 2012); here
          the 2009-2013 launches are 87% to 97% funded, and the share breaks at 2014, when Web Robots' scrapes start
          (older projects are likely those still listed then). Whether failures are also missing from 2014 on, the
          test windows included, is unknown. Funded share by launch year, counted on the 185,444 rows of this
          definition: 2009 96.5% (113), 2010 90.4% (795), 2011 89.6% (2,474), 2012 89.5% (4,731), 2013 87.3% (5,423),
          then 2014 54.5% (15,155), 2015 47.1% (19,186), rising to 71.1% (23,096) in 2025.
        - The 2009-2013 launches stay (Andrej, 2026-11-11), 13,536 projects, 8% to 14% of each training side: on the
          launch-year windows 2023 to 2025 of that day, with the same test rows, dropping them made logistic
          regression worse (log loss 0.504 to 0.509, ROC AUC 0.819 to 0.817, mean of the three windows) and moved
          LightGBM by about 0.001 ROC AUC, so the old rows are kept.
    """
    accepted_check_warnings = {
        "meta_license_unknown": (
            "Web Robots publishes its Kickstarter scrapes without a licence; its terms and conditions cover its "
            "scraping service, not the datasets (checked 2026-11-10)."
        ),
    }

    # Task
    target = "state"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Web Robots publishes a scraped snapshot with no task; the Kaggle copy is a dataset, not a "
            "competition, so no metric is defined."
        ),
    )

    # Splits
    splits_comment = """
        We simulate a model refit every half-year and used at each campaign's launch. The windows are dated by launch (`launched_at`), the prediction point, not by creation (Lennart, 2026-11-11): a project is created a median of 52 days before its deadline (154 days at the 90th percentile), so dated by creation 1.9% to 3.2% of each train side was still running when its window started.

        The length, half a calendar year, is a convention, not a sourced horizon (Andrej, 2026-11-20): Web Robots publishes monthly scrapes without a task and the Kaggle copy is a dataset, not a competition, so no source gives a horizon or a refit cadence. The year signed off on 2026-11-11 (Lennart) held every season, but its windows 2017 to 2019 trained on 47.0%, 40.2% and 32.4% of the projects; half the projects were launched by mid-2019, so with the gap any window starting before 1 October 2019 trains on under half, at any length. Half-years from 2020 on keep nine windows, every one training on half the projects or more, and across the nine windows both halves of the year are tested. A month would not be too small: 1,500 to 2,200 projects were created in every month of 2024 and of January to September 2025.

        The gap is 60 days, Kickstarter's longest campaign: a refit at a window's start knows the outcome of a campaign only once it has ended, so each train side holds the projects launched more than 60 days before its window. At most one training project per window, a campaign longer than 60 days (up to 121 in the data), had not ended when its window starts. The scrape of 12 January 2026 holds only ended projects, so we drop the launches of its last 60 days (from 13 November 2025 11:00, 1,673 projects) and the newest window, 1 July to 13 November 2025, is complete but for such long campaigns.

        The nine test windows are half-years of launches, every fourth of the twelve from 2020 H1 to 2025 H2 left out (Andrej, 2026-11-20): 2025 H2, 2025 H1, 2024 H1, 2023 H2, 2023 H1, 2022 H1, 2021 H2, 2021 H1 and 2020 H1. Nine is the number of splits a random split of 185,444 projects gets (three repeats of three folds). They cover the pandemic year 2020, the spread of pre-launch pages (from about 41% of the projects created in 2020 to 61% in 2025) and success rates from 60.5% (2020 H1) to 72.5% (2025 H2). The launch years 2017 to 2019, tested until 2026-11-20, are not tested: no window over them trains on half the projects.
    """
    split_leaf = "L-ORDER.windows"
    # `on`: the launch, when the use case predicts; a 60-day gap (the longest campaign) keeps the training outcomes
    # known at the refit, and `_clean` drops the launches of the scrape's last 60 days (Lennart, 2026-11-11).
    temporal = Temporal(
        on="launched_at",
        splits=TemporalSplits(
            window=6,
            unit="months",
            cutoffs=(
                "2025-07-01",
                "2025-01-01",
                "2024-01-01",
                "2023-07-01",
                "2023-01-01",
                "2022-01-01",
                "2021-07-01",
                "2021-01-01",
                "2020-01-01",
            ),
            gap=60,
            gap_unit="days",
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        data_dir = raw_dir / "data_files"
        # Read and concatenate all CSV files
        df = pd.concat((pd.read_csv(csv_file) for csv_file in sorted(data_dir.glob("*.csv"))), ignore_index=True)
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
        as_date_cols = [
            "created_at",
            "launched_at",
            "deadline",
        ]
        for c in as_date_cols:
            df[c] = pd.to_datetime(df[c], unit="s")
        # Drop duplicates
        df = df.drop_duplicates()
        # Drop the 2 samples from 2026
        df = df[df["created_at"].dt.year < 2026]
        # The scrape holds only ended projects (newest deadline 2026-01-12 11:00): drop the launches of its last 60
        # days, the longest campaign, whose outcomes it holds only for the campaigns already ended (1,673 projects)
        df = df[df["launched_at"] < pd.Timestamp("2025-11-13 11:00")]
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "prelaunch_activated",
                "main_category",
                "sub_category",
                "country",
            ],
            string=[
                "blurb",
                "name",
                "creator_name",
                "location_displayable_name",
            ],
            datetime=["created_at", "launched_at", "deadline"],
        )
