"""Curated dataset definition for `allstate_claims_severity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class AllstateClaimsSeverity(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How much will an insurance claim cost?",
        use_case=(
            "Allstate, a US personal insurer, estimates the cost of a claim when it is filed, to improve its claims "
            "service (the competition's description); for example, to send costly claims to experienced handlers."
        ),
        row=(
            "One insurance claim at Allstate (188,317 claims, the competition's training file; the period is not "
            "stated)."
        ),
        predicted=(
            "The cost of the claim, shipped on a log scale for modelling; scored by MAE on the loss as published. The "
            "currency is not stated."
        ),
        known=(
            "130 anonymized attributes of the claim, 116 categorical and 14 numeric; their meaning and when they are "
            "recorded are not given."
        ),
        split=(
            "Random claims, so the test data stands for other claims of the same period; the file has no claim dates."
        ),
        fit="approximate",
        fit_reason=(
            "The attributes are anonymized, so we cannot check that each is known when a claim is filed, and without "
            "claim dates random claims stand in for the claims to come."
        ),
    )

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
        - We log scale the target, the scale a practitioner models a claim cost on; the metric is the competition's
          MAE on the loss as published, computed after the inverse (`target_transform="log"`, MET-3).
    """

    # Task
    target = "loss"
    problem_type = "regression"
    metric = Metric.source(
        "mae",
        original="Mean Absolute Error",
        reference="https://www.kaggle.com/competitions/allstate-claims-severity (Kaggle API evaluationMetric)",
        definition="mean absolute error of the claim loss in dollars, on the raw scale",
        target_transform="log",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["id"])
        # Drop duplicates w/o target column
        df = df.drop_duplicates(subset=[c for c in df.columns if c != self.task_metadata.target_column_name])
        # log scale the target (the metric inverts it: target_transform="log")
        df[self.task_metadata.target_column_name] = np.log(df[self.task_metadata.target_column_name])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[c for c in df.columns if c.startswith("cat")])
