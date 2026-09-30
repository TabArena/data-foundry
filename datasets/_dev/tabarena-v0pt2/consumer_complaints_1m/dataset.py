"""Curated dataset definition for `consumer_complaints_1m` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits


class ConsumerComplaints1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "consumer_complaints_1m"
    version_of = "consumer_complaints"
    version_comment = """
        We use the last 3 months as test data randomly sub-sample the train to 1 million and test data 250k rows. We follow TabReD and use random sub-sampling. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
    """
    year = "2025"
    domain = "finance"
    source = "GOV Website"
    source_url = "https://www.consumerfinance.gov/data-research/consumer-complaints/"
    license = "U.S. Government Works"
    data_tags = ("Spatial",)
    download_description = """
        We utilize the newest data (acquired on 23/01/2026) from the government website. We use the following commands to download and organize the data:

        wget https://files.consumerfinance.gov/ccdb/complaints.csv.zip && unzip complaints.csv.zip && rm complaints.csv.zip
        mkdir -p local-data-warehouse/consumer_complaints && mv complaints.csv local-data-warehouse/consumer_complaints
    """
    bibtex = r"""
        @misc{cfpb2025ConsumerComplaintDatabase,
          author       = {{Consumer Financial Protection Bureau}},
          title        = {Consumer Complaint Database},
          year         = {2025},
          howpublished = {\url{https://www.consumerfinance.gov/data-research/consumer-complaints/}},
          note         = {Accessed: 2026-01-23},
        }
    """
    curation_comments = """
        The dataset on Kaggle (https://www.kaggle.com/datasets/selener/consumer-complaint-database) has data from up until 2019. We use the newest version from the government website with data up until 2025.

        - Context and descriptions of the features can be found here: https://cfpb.github.io/api/ccdb/fields.html
        - "Company public response" is not free text but selected "from a set list of options".
        - Following TexTabBench, we focus on predicting the type of closure a complaint got, that is the "Company response to consumer" column. We want to predict if a complaint will be closed with just an explanation, with non-monetary relief, or with monetary relief.
        - We filter the data to only include entries after consumer disputations were discontinued as this represent a shift in protocol. This filters all data before April 24th 2017.
        - We filter all cases where the "Consumer consent provided?" is in progress or got an untimely response.
        - We filter all rows that do not include consent to share their complaint narrative. This ensures the data contains text sentences.
        - We drop "Company public response" as it leaks the target variable.
        - We only allow complaints from US states (no territories or international complaints) and remove cases with missing states.
        - The data has unresolved spatial information in the ZIP code. Some ZIPs are censored (ending in "XXX" or full removed "XXXXXX").
        - We add a feature for "Low population area", which determines that the ZIP is censored.
        - The tags filed contains only three non-nan labels, of which one is a duplicate of the others. We created two categorical features from it instead.
        - We drop duplicates (2% of the data) as the data should not contain naturally occurring duplicates and this likely results from some overlap in data collection or data entry or faulty re-submissions. We investigated some of the duplicates and they appear to be identical complaints. There exist duplicates with different target labels, we also drop these as we have no way to determine what the correct label is.
        - We drop constant columns, the complaint ID, and when the complaint was send to the company (as it does not related to the target task)
    """

    # Task
    target = "Company response to consumer"
    problem_type = "multiclass_classification"
    time_on = "Date received"

    # Splits
    splits_comment = """
        We try to create splits that simulate a model deployed to solve the task.

        - The official data is updated daily but companies have 180 days to respond to a new complaint.
        - We could simulate a model that is refitted daily, but this would need many splits. Moreover, data from just a few days is likely not enough to create a robust test set.
        - Thus, we instead simulate a model that is refit every three months and then deployed.
        - This introduces the unrealistic downside of data shift across a month that would not exist in a real-world model.

        We create one test split by using all data after 2025-09-0101 as test splits. This represents a refit horizon of ca. 3 months.
        We use all data before as training data.
    """
    time_horizon = 3
    time_horizon_unit = "months"
    temporal_splits = TemporalSplits(window=None, unit="days", cutoffs=("2025-09-01",))
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "complaints.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Only keep entries after responses were discontinued as this represent a shift in protocol and closure (so data after April 2017)
        # - Note this filters one of the classes from TexTabBench completely as it was an "old" label
        df = df[df["Consumer disputed?"].isna()]
        df = df.drop(columns=["Consumer disputed?"])
        # Filter to complaints that include sentences and have consent
        df = df[df["Consumer consent provided?"] == "Consent provided"]
        df = df.drop(columns=["Consumer consent provided?"])
        # Filter to only keep relevant rows that got closed
        df = df[
            df["Company response to consumer"].isin(
                ["Closed with explanation", "Closed with non-monetary relief", "Closed with monetary relief"]
            )
        ]
        # Drop leakage variable
        df = df.drop(columns=["Timely response?", "Company public response"])
        # Remove non-us states
        non_state = [
            "AA",
            "AE",
            "AP",
            "AS",
            "DC",
            "FM",
            "GU",
            "MH",
            "MP",
            "PR",
            "PW",
            "VI",
            "UNITED STATES MINOR OUTLYING ISLANDS",
        ]
        df = df[~(df["State"].isin(non_state) | df["State"].isna())]
        # if the ZIP ends with XXX, it means the complaints originates from a place with less than 20k people.
        df["Low population area"] = "False"
        df.loc[(df["ZIP code"].str.contains("XX") & (df["ZIP code"] != "XXXXX")), "Low population area"] = "True"
        df.loc[df["ZIP code"] == "XXXXX", "Low population area"] = np.nan
        # Resolve Multi-Tags feature into two categorical features
        assert list(np.unique(df["Tags"].astype(str))) == [
            "Older American",
            "Older American, Servicemember",
            "Servicemember",
            "nan",
        ]
        tags_nan_mask = df["Tags"].isna()
        tags_is_older_american = df["Tags"].str.contains("Older American", na=False)
        tags_is_servicemember = df["Tags"].str.contains("Servicemember", na=False)
        df["Tag: Older American"] = "False"
        df["Tag: Servicemember"] = "False"
        df.loc[tags_is_older_american, "Tag: Older American"] = "True"
        df.loc[tags_is_servicemember, "Tag: Servicemember"] = "True"
        df.loc[tags_nan_mask, ["Tag: Older American", "Tag: Servicemember"]] = np.nan
        df = df.drop(columns=["Tags"])
        # Drop column
        df = df.drop(
            columns=[
                "Submitted via",  # only web after our preprocessing
                "Complaint ID",  # we have new-ness of complaint from other columns, so this does not tell anything new
                "Date sent to company",  # just shows processing delay from CFPB and not related to the target. Otherwise, almost always identical to "Date received".
            ]
        )
        as_string_type = [
            "Company",  # categorical based on feature description but given that we can have new companies in the future, it cannot be a "normal" categorical feature
            "Consumer complaint narrative",
            "ZIP code",
        ]
        for c in as_string_type:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        df["Date received"] = pd.to_datetime(df["Date received"])
        # We drop duplicates as the data should not contain naturally occurring duplicates.
        df = df.drop_duplicates(subset=df.columns.difference([self.task_metadata.target_column_name]))
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Product",
                "Sub-product",
                "Issue",
                "Sub-issue",
                "State",
                "Low population area",
                "Tag: Older American",
                "Tag: Servicemember",
            ],
        )
