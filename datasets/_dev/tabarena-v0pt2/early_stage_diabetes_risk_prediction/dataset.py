"""Curated dataset definition for `early_stage_diabetes_risk_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class EarlyStageDiabetesRiskPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "early_stage_diabetes_risk_prediction"
    year = "2019"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5VG8H"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/529/early+stage+diabetes+risk+prediction+dataset.zip && unzip early+stage+diabetes+risk+prediction+dataset.zip && rm early+stage+diabetes+risk+prediction+dataset.zip && mkdir -p local-data-warehouse/early_stage_diabetes_risk_prediction && mv diabetes_data_upload.csv local-data-warehouse/early_stage_diabetes_risk_prediction/
    """
    bibtex = """
        @inproceedings{islam2019likelihood,
          title={Likelihood prediction of diabetes at early stage using data mining techniques},
          author={Islam, MM Faniqul and Ferdousi, Rahatara and Rahman, Sadikur and Bushra, Humayra Yasmin},
          booktitle={Computer Vision and Machine Intelligence in Medical Image Analysis: International Symposium, ISCMM 2019},
          pages={113--125},
          year={2019},
          organization={Springer}
        }
    """
    curation_comments = """
        We use the data as is from UCI.

        - Note, the dataset contains a lot of naturally occurring duplicates (50%). We drop them to avoid too extreme duplicated-based data leakage biasing the evaluation.
    """

    # Task
    target = "class"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "diabetes_data_upload.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop_duplicates()
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[c for c in df.columns if c not in ("Age", self.target)])
