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
        We use the last 3 months (Oct-Dec 2025) as test data and randomly sub-sample the train to 1 million and test data 250k rows. We follow TabReD and use random sub-sampling. The idea behind this instead of a time-based subsampling is to keep data from various time periods and model the distribution shift across the full time horizon.
    """
    year = "2025"
    domain = "finance"
    source = "GOV Website"
    source_url = "https://www.consumerfinance.gov/data-research/consumer-complaints/"
    license = "U.S. Government Works"
    data_tags = ("Spatial",)
    download_description = """
        The CFPB removed the complaint narratives from the live database download on 2026-09-14 and archived every
        previously published complaint in its FOIA reading room as CCDB exports (one zip per period, exported
        2026-09-14, with the narratives and the company responses as of that date):
        https://www.consumerfinance.gov/foia-requests/foia-electronic-reading-room/cfpb-consumer-complaint-database-narratives-archive/
        We use the exports up to December 2025 (downloaded 2026-10-01) and keep the zips as they are:

        mkdir -p local-data-warehouse/consumer_complaints/foia_archive && cd local-data-warehouse/consumer_complaints/foia_archive
        for f in 1_December_2011_through_April_2018 \
            2_May_2018_through_April_2021 \
            3_May_2021_through_October_2022 \
            4_November_2022_through_August_2023 \
            5_September_2023_through_March_2024 \
            6_April_2024_through_July_2024 \
            7_August_2024_through_October_2024 \
            8_November_2024_through_December_2024 \
            9_January_2025_through_February_2025 \
            10_March_2025_through_April_2025 \
            11_May_2025_through_June_2025 \
            12_July_2025_through_August_2025 \
            13_September_2025_through_October_2025 \
            14_November_2025_through_December_2025; do
            wget https://files.consumerfinance.gov/f/documents/CCDB_Export_${f}.zip
        done
    """
    bibtex = r"""
        @misc{cfpb2025ConsumerComplaintDatabase,
          author       = {{Consumer Financial Protection Bureau}},
          title        = {Consumer Complaint Database},
          year         = {2025},
          howpublished = {\url{https://www.consumerfinance.gov/data-research/consumer-complaints/}},
          note         = {Narratives archive (FOIA reading room), exported 2026-09-14. Accessed: 2026-10-01},
        }
    """
    curation_comments = """
        The dataset on Kaggle (https://www.kaggle.com/datasets/selener/consumer-complaint-database) has data from up until 2019. We use the government data up to the end of 2025.

        - Source history: the CFPB stopped publishing complaint narratives on 2026-08-14 and removed them from the live download on 2026-09-14; the live file no longer has the narrative or the consent column. We therefore build from the FOIA narratives archive (exported 2026-09-14). Its labels are settled: an earlier build from the 2026-01-23 download filtered out complaints still "In progress" (7% of Oct, 14% of Nov and 70% of Dec 2025), which biased the test months towards quickly closed complaints.
        - Compared with the 2026-01-23 download, the archive has the same labels for all 3.49M shared complaints, 64,743 more closed complaints (mostly Nov-Dec 2025), Windows line endings in 2017-2020 narratives (normalised) and fewer fully masked ZIP codes ("XXXXX": 1.8% instead of 4.8%).
        - We stop at 2025-12-31. Complaints received in 2026 rarely have a published narrative (3.5% in March, 1.5% in July, none in August 2026, against 16% in November 2025), so they are a small and differently selected sample.

        - Context and descriptions of the features can be found here: https://cfpb.github.io/api/ccdb/fields.html
        - "Company public response" is not free text but selected "from a set list of options".
        - Following TexTabBench, we focus on predicting the type of closure a complaint got, that is the "Company response to consumer" column. We want to predict if a complaint will be closed with just an explanation, with non-monetary relief, or with monetary relief.
        - We filter the data to only include entries after consumer disputations were discontinued as this represent a shift in protocol. This filters all data before April 24th 2017.
        - We filter all cases where the "Consumer consent provided?" is in progress or got an untimely response.
        - We filter all rows without a published complaint narrative (only complaints whose consumer consented to sharing it have one; the archive has no consent column). This ensures the data contains text sentences.
        - We drop "Company public response" as it leaks the target variable.
        - We only allow complaints from US states (no territories or international complaints) and remove cases with missing states.
        - The data has unresolved spatial information in the ZIP code. Some ZIPs are censored (ending in "XXX" or full removed "XXXXXX").
        - We add a feature for "Low population area", which determines that the ZIP is censored.
        - The tags filed contains only three non-nan labels, of which one is a duplicate of the others. We created two categorical features from it instead.
        - We drop duplicates (2% of the data) as the data should not contain naturally occurring duplicates and this likely results from some overlap in data collection or data entry or faulty re-submissions. We investigated some of the duplicates and they appear to be identical complaints. There exist duplicates with different target labels, we also drop these as we have no way to determine what the correct label is (all copies are dropped).
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

        We create one test split by using all data from 2025-10-01 to 2025-12-31 as test split. This represents a refit horizon of 3 months.
        We use all data before as training data.
    """
    time_horizon = 3
    time_horizon_unit = "months"
    temporal_splits = TemporalSplits(window=None, unit="days", cutoffs=("2025-10-01",))
    subsample_to_budget = True
    accepted_check_warnings = {
        "dataset_pure_feature_value": "Block, Inc. (Cash App) closes 99.8% of its complaints with an explanation "
        "throughout 2019-2025: a company response policy, and the company is known when the complaint is filed.",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        files = sorted((raw_dir / "foia_archive").glob("CCDB_Export_*.zip"))
        assert len(files) == 14, f"Expected the 14 CCDB exports up to December 2025, found {len(files)}."
        df = pd.concat([pd.read_csv(f, dtype=str) for f in files], ignore_index=True)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Only keep entries after consumer disputes were discontinued (2017-04-24) as this represent a shift in protocol and closure
        # - Note this filters one of the classes from TexTabBench completely as it was an "old" label
        # - The archive has no "Consumer disputed?" column; in the full download it is "N/A" exactly from 2017-04-24 on.
        received = pd.to_datetime(df["Date received"])
        df = df[(received >= "2017-04-24") & (received <= "2025-12-31")]
        # Filter to complaints that include sentences (a narrative is only published with the consumer's consent)
        df = df[df["Consumer complaint narrative"].notna()]
        # The archive writes Windows line endings in 2017-2020 narratives; the live download used "\n".
        df["Consumer complaint narrative"] = df["Consumer complaint narrative"].str.replace("\r\n", "\n", regex=False)
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
        # We drop duplicates as the data should not contain naturally occurring duplicates; copies that disagree on the
        # target are all dropped.
        target = self.task_metadata.target_column_name
        features = list(df.columns.difference([target]))
        df = df.drop_duplicates()
        df = df[~df.duplicated(subset=features, keep=False)]
        df = df.sort_values("Date received", kind="stable").reset_index(drop=True)
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
