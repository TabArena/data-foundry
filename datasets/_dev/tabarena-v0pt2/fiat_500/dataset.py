"""Curated dataset definition for `fiat_500` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class Fiat500(AbstractCuratedDataset):
    # Dataset
    unique_name = "fiat_500"
    year = "2020"
    domain = "technology & internet"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows"
    license = "CC0: Public Domain"
    download_description = """
        kaggle datasets download paolocons/another-fiat-500-dataset-1538-rows -p local-data-warehouse/fiat_500/ && unzip local-data-warehouse/fiat_500/another-fiat-500-dataset-1538-rows.zip -d local-data-warehouse/fiat_500/ && rm local-data-warehouse/fiat_500/another-fiat-500-dataset-1538-rows.zip
    """
    bibtex = r"""
        @misc{paolocons2020fiat,
          author       = {Kaggle User Paolocons},
          title        = {Another Dataset on Used Fiat 500 (1538 Rows)},
          year         = {2020},
          howpublished = {\url{https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = "N/A"

    # Task
    target = "price"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/automobile_dot_it_used_fiat_500_in_Italy_dataset_filtered.csv")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "model",
            ],
        )
