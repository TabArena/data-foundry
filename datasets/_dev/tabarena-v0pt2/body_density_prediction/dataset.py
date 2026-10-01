"""Curated dataset definition for `body_density_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class BodyDensityPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "body_density_prediction"
    year = "1985"
    domain = "medical & healthcare"
    source = "Kaggle"  # Other OpenML. Original UCI source is gone.
    source_url = "https://www.kaggle.com/datasets/fedesoriano/body-fat-prediction-dataset"
    license = "None"
    download_description = """
        We download the data from Kaggle.

        kaggle datasets download fedesoriano/body-fat-prediction-dataset && unzip body-fat-prediction-dataset.zip && rm body-fat-prediction-dataset.zip
        mkdir -p local-data-warehouse/body_density_prediction && mv bodyfat.csv local-data-warehouse/body_density_prediction/
    """
    bibtex = r"""
        @article{penrose1985generalized,
          title={Generalized body composition prediction equation for men using simple measurement techniques},
          author={Penrose, Keith W and Nelson, Arnold G and Fisher, Arnold Garth},
          journal={Medicine \& Science in Sports \& Exercise},
          volume={17},
          number={2},
          pages={189},
          year={1985},
          publisher={Ovid Technologies (Wolters Kluwer Health)}
        }
    """
    curation_comments = """
        We start with the data from Kaggle.

        - Note, the task is not about bodyfat prediction as this is determined by a deterministic formula. Instead, the task is to estimate the density (which can be used to get the body fat via the deterministic formula). However, density requires a test. So we aim to predict from data the density such that we can skip this test. Which can make a lot of sense, if the test is too expensive as it requires underwater weighing.
    """

    # Task
    target = "Density"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "bodyfat.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Bodyfat leaks the density
        df = df.drop(columns=["BodyFat"])
        return df
