"""Curated dataset definition for `thyroid_discordant` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class ThyroidDiscordant(AbstractCuratedDataset):
    # Dataset
    unique_name = "thyroid_discordant"
    year = "1986"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5D010"
    license = "CC BY 4.0"
    download_description = """
        We download the dis.data from the UCI files. All other files are corrupted or versions of the same data as far as we know (see the dataset curation sheet for more information).

        wget https://archive.ics.uci.edu/static/public/102/thyroid+disease.zip && unzip thyroid+disease.zip  dis.data dis.test && rm thyroid+disease.zip && mkdir -p local-data-warehouse/thyroid_discordant && mv dis.data dis.test local-data-warehouse/thyroid_discordant/
    """
    bibtex = """
        @article{quinlan1987simplifying,
          title={Simplifying decision trees},
          author={Quinlan, J. Ross},
          journal={International journal of man-machine studies},
          volume={27},
          number={3},
          pages={221--234},
          year={1987},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We start with the .data file from UCI and add columns and encode nan values.

        - Note, the data contains NaN indicators by default (e.g. TSH_measured). We keep them.
        - We drop/ignore the referral_source columns as it indicates the original of the data and thus might leak information or makes the model learn sub-group related behavior that is not the target/task of interest.
        - We correct the label column by removing the patient IDs.
        - We drop 60 duplicated rows and remove constant columns.
    """

    # Task
    target = "discordant"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "age",
            "sex",
            "on_thyroxine",
            "query_on_thyroxine",
            "on_antithyroid_medication",
            "sick",
            "pregnant",
            "thyroid_surgery",
            "I131_treatment",
            "query_hypothyroid",
            "query_hyperthyroid",
            "lithium",
            "goitre",
            "tumor",
            "hypopituitary",
            "psych",
            "TSH_measured",
            "TSH",
            "T3_measured",
            "T3",
            "TT4_measured",
            "TT4",
            "T4U_measured",
            "T4U",
            "FTI_measured",
            "FTI",
            "TBG_measured",
            "TBG",
            "referral_source",
            "discordant",
        ]
        df = pd.read_csv(raw_dir / "dis.data", header=None, names=columns, na_values=["?"])
        df = pd.concat(
            [df, pd.read_csv(raw_dir / "dis.test", header=None, names=columns, na_values=["?"])], ignore_index=True
        )
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["discordant"] = df["discordant"].str.split(".").str[0]  # remove patient ID from target column
        df = df.drop(
            columns=[
                "referral_source",  # irrelevant here
                "TBG_measured",
                "TBG",  # constant
            ]
        )
        # drop duplicated rows
        df = df.drop_duplicates().reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "sex",
                "on_thyroxine",
                "query_on_thyroxine",
                "on_antithyroid_medication",
                "thyroid_surgery",
                "query_hypothyroid",
                "query_hyperthyroid",
                "pregnant",
                "sick",
                "tumor",
                "lithium",
                "goitre",
                "TSH_measured",
                "T3_measured",
                "TT4_measured",
                "T4U_measured",
                "FTI_measured",
                "psych",
                "I131_treatment",
                "hypopituitary",
            ],
        )
