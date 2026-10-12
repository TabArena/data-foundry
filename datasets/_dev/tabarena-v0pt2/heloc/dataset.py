"""Curated dataset definition for `heloc` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class Heloc(AbstractCuratedDataset):
    # Dataset
    unique_name = "heloc"
    year = "2018"
    domain = "finance"
    source = "Other"  # FICO's Explainable Machine Learning Challenge (heloc_dataset_v1); the Kaggle file is a copy
    source_url = "https://community.fico.com/s/explainable-machine-learning-challenge"
    license = "Public"
    download_description = """
        We download the data from Kaggle and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/heloc/ && cd local-data-warehouse/heloc && kaggle datasets download averkiyoliabev/home-equity-line-of-creditheloc && cd ../../ && unzip local-data-warehouse/heloc/home-equity-line-of-creditheloc.zip -d local-data-warehouse/heloc/ && rm local-data-warehouse/heloc/home-equity-line-of-creditheloc.zip
    """
    bibtex = r"""
        @misc{averkiyoliabev2021heloc,
          author       = {Kaggle User Averkiyoliabev},
          title        = {Home Equity Line of Credit (HELOC)},
          year         = {2021},
          howpublished = {\url{https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = """
        - Anomaly: the dataset has time-related features. However, the task and features are preprocessed to be time-invariant.
    """

    # Task
    target = "RiskPerformance"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/heloc_dataset_v1 (1).csv")
        return df
