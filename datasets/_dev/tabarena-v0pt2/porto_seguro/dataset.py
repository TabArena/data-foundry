"""Curated dataset definition for `porto_seguro` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class PortoSeguro(AbstractCuratedDataset):
    # Dataset
    unique_name = "porto_seguro"
    year = "2017"
    domain = "insurance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/c/porto-seguro-safe-driver-prediction"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c porto-seguro-safe-driver-prediction -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/porto_seguro && mv train.csv local-data-warehouse/porto_seguro/
    """
    bibtex = r"""
        @misc{Howard2017PortoSegurosSafeDriverPrediction,
          author = {Addison Howard and Adriano Moala and Walter Reade},
          title  = {Porto Seguro’s Safe Driver Prediction},
          year   = {2017},
          howpublished = {\url{https://kaggle.com/competitions/porto-seguro-safe-driver-prediction}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - Following the expert solutions on Kaggle, we drop *calc features.
        - In general, the 2nd and 3rd place did a lot of interesting feature engineering for interactions. We do not copy these as the data is clean as it is.
        - We drop the index as it seems to be uninformative for this dataset.
        - There exist only 6 duplicates in the training data. We drop them as the portion is too small to be meaningful.
    """

    # Task
    target = "target"
    problem_type = "binary_classification"
    metric = "normalized_gini_coefficient"  # see https://www.kaggle.com/c/ClaimPredictionChallenge/discussion/703

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Create real nan values
        df = df.replace(-1, np.nan)
        # Drop *calc features
        calc_features = [col for col in df.columns if "calc" in col]
        df = df.drop(columns=calc_features)
        # Drop index
        df = df.drop(columns=["id"])
        # Dtypes
        as_cat_type = [col for col in df.columns if col.endswith(("cat", "bin"))]
        df[as_cat_type] = df[as_cat_type].astype("category")
        df[self.task_metadata.target_column_name] = df[self.task_metadata.target_column_name].astype("category")
        # Drop duplicates w/o target
        df = df.drop_duplicates(subset=[col for col in df.columns if col != self.task_metadata.target_column_name])
        return df


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
