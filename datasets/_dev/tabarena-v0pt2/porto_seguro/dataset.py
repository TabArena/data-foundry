"""Curated dataset definition for `porto_seguro` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class PortoSeguro(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a car-insurance customer file a claim within the next year?",
        use_case=(
            "The Brazilian insurer Porto Seguro, when pricing a policy, estimates the probability that the driver "
            "will file a claim in the next year, to set fairer prices (the Kaggle competition's goal)."
        ),
        row=(
            "One policy holder of Porto Seguro (595,206 of the competition's training rows; the period is not stated)."
        ),
        predicted="Whether the driver filed a claim (3.6% did).",
        known=(
            "The insurer's anonymised features about the driver, the car and the region, whose meanings are hidden."
        ),
        split="Random policy holders of the same period.",
        changes=("We drop a block of engineered features that the top competition solutions also dropped."),
        fit="direct",
        fit_reason=(
            "The insurer built the task to score drivers ahead of the next year, so the features should be known at "
            "pricing; their meanings are hidden, so this cannot be checked. The policies carry no dates, so test and "
            "training drivers come from the same period."
        ),
    )

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
        - We turn -1 into a missing value: "Values of -1 indicate that the feature was missing from the observation" (the competition's data description).
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
        # Drop duplicates w/o target
        df = df.drop_duplicates(subset=[col for col in df.columns if col != self.task_metadata.target_column_name])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[col for col in df.columns if col.endswith(("cat", "bin"))])
