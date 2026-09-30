"""Curated dataset definition for `churn` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class Churn(AbstractCuratedDataset):
    # Dataset
    unique_name = "churn"
    year = "2005"
    domain = "technology & internet"
    source = "OpenML"
    source_url = (
        "https://github.com/EpistasisLab/pmlb/tree/master/datasets/churn"  # also https://www.openml.org/d/40701
    )
    license = "Public Domain"
    data_tags = ("Spatial",)
    download_description = """
        curl -L -o churn.tsv.gz "https://media.githubusercontent.com/media/EpistasisLab/pmlb/master/datasets/churn/churn.tsv.gz" && mkdir -p local-data-warehouse/churn/ && mv churn.tsv.gz local-data-warehouse/churn/ && gzip -d local-data-warehouse/churn/churn.tsv.gz
    """
    bibtex = r"""
        @misc{marcoulides2005churn,
          title={Discovering knowledge in data: An introduction to data mining},
          author={Marcoulides, George A},
          year={2005},
          publisher={Taylor \& Francis}
        }
    """
    curation_comments = """
        - The original source is lost, so we use https://github.com/EpistasisLab/pmlb/tree/master/datasets/churn (or https://www.openml.org/d/40701)
        - We dropped the "phone_number" feature as it seems to be an index in the original data.
        - We renamed the target variable to "CustomerChurned" and mapped binary variables to "Yes"/"No"
    """

    # Task
    target = "CustomerChurned"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/churn.tsv", sep="\t")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df.columns = df.columns.str.replace(" ", "_")
        df.rename(columns={"target": "CustomerChurned"}, inplace=True)
        df.drop(columns=["phone_number"], inplace=True)
        df["CustomerChurned"] = df["CustomerChurned"].map({1: "Yes", 0: "No"})
        df["international_plan"] = df["international_plan"].map({1: "Yes", 0: "No"})
        df["voice_mail_plan"] = df["voice_mail_plan"].map({1: "Yes", 0: "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "state",
                "area_code",
                "international_plan",
                "voice_mail_plan",
            ],
        )
