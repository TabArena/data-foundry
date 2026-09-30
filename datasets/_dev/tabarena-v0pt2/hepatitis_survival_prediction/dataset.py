"""Curated dataset definition for `hepatitis_survival_prediction` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class HepatitisSurvivalPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "hepatitis_survival_prediction"
    year = "1981"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5Q59J"
    license = "CC BY 4.0"
    download_description = """
        Get the UCI data.

        wget https://archive.ics.uci.edu/static/public/46/hepatitis.zip && unzip hepatitis.zip hepatitis.data && rm hepatitis.zip && mkdir -p local-data-warehouse/hepatitis_survival_prediction && mv hepatitis.data local-data-warehouse/hepatitis_survival_prediction/
    """
    bibtex = """
        @inproceedings{efron1981statistical,
          title={Statistical theory and the computer},
          author={Efron, Bradley and Gong, Gail},
          booktitle={Computer science and statistics: Proceedings of the 13th Symposium on the Interface},
          pages={3--7},
          year={1981},
          organization={Springer}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - We encode missing values as NaN.
        - We convert numeric features to float and categorical features to category dtype.
    """

    # Task
    target = "class"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "class",
            "age",
            "sex",
            "steroid",
            "antivirals",
            "fatigue",
            "malaise",
            "anorexia",
            "liver_big",
            "liver_firm",
            "spleen_palpable",
            "spiders",
            "ascites",
            "varices",
            "bilirubin",
            "alk_phosphate",
            "sgot",
            "albumin",
            "protime",
            "histology",
        ]
        df = pd.read_csv(raw_dir / "hepatitis.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.replace("?", np.nan)
        as_float_type = ["age", "bilirubin", "alk_phosphate", "sgot", "albumin", "protime"]
        df[as_float_type] = df[as_float_type].astype(float)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "sex",
                "steroid",
                "antivirals",
                "fatigue",
                "malaise",
                "anorexia",
                "liver_big",
                "liver_firm",
                "spleen_palpable",
                "spiders",
                "ascites",
                "varices",
                "histology",
            ],
        )
