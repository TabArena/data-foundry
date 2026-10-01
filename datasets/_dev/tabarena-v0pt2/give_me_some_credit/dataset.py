"""Curated dataset definition for `give_me_some_credit` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class GiveMeSomeCredit(AbstractCuratedDataset):
    # Dataset
    unique_name = "give_me_some_credit"
    year = "2011"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/GiveMeSomeCredit/overview"
    license = "Public"
    download_description = """
        We download the data from Kaggle and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/give_me_some_credit/ && cd local-data-warehouse/give_me_some_credit && kaggle competitions download -c GiveMeSomeCredit && cd ../../ && unzip local-data-warehouse/give_me_some_credit/GiveMeSomeCredit.zip -d local-data-warehouse/give_me_some_credit/ && rm local-data-warehouse/give_me_some_credit/GiveMeSomeCredit.zip
    """
    bibtex = """
        @misc{cukierski2011credit,
            author = {Credit Fusion and Will Cukierski},
            title = {Give Me Some Credit},
            year = {2011},
            howpublished = {url{https://kaggle.com/competitions/GiveMeSomeCredit}},
            note = {Kaggle}
        }
    """
    curation_comments = """
        - We renamed the target feature and its value to be more descriptive.
    """

    # Task
    target = "FinancialDistressNextTwoYears"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/cs-training.csv", index_col=0, na_values="NA")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "FinancialDistressNextTwoYears"
        df = df.rename(columns={"SeriousDlqin2yrs": target_feature})
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})
        return df
