"""Curated dataset definition for `allstate_claims_severity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class AllstateClaimsSeverity(AbstractCuratedDataset):
    # Dataset
    unique_name = "allstate_claims_severity"
    year = "2016"
    domain = "insurance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/allstate-claims-severity"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c allstate-claims-severity -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/allstate_claims_severity && mv train.csv local-data-warehouse/allstate_claims_severity/
    """
    bibtex = r"""
        @misc{Ferguson2016AllstateClaimsSeverity,
          author = {Dana Ferguson and Meg Risdal and NoTrick and Sara R. Sillah and Tim Emmerling and Will Cukierski},
          title  = {Allstate Claims Severity},
          year   = {2016},
          howpublished = {\url{https://kaggle.com/competitions/allstate-claims-severity}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized.
        - Top Kaggle solutions did not perform any relevant preprocessing.
        - We drop the ID column, as it does not contain any signal.
        - The data contains 1 duplicate row when ignoring the target. We drop this artifact.
        - We log scale the target.
    """

    # Task
    target = "loss"
    problem_type = "regression"
    metric = "mae"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        cat_features = [c for c in list(df) if c.startswith("cat")]
        df[cat_features] = df[cat_features].astype("category")
        df = df.drop(columns=["id"])
        # Drop duplicates w/o target column
        df = df.drop_duplicates(subset=[c for c in df.columns if c != self.task_metadata.target_column_name])
        # log scale the target
        df[self.task_metadata.target_column_name] = np.log(df[self.task_metadata.target_column_name])
        return df


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
