"""Curated dataset definition for `miami_housing` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import arff
import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class MiamiHousing(AbstractCuratedDataset):
    # Dataset
    unique_name = "miami_housing"
    year = "2016"  # data from 2016, curated in 2021
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.openml.org/d/43093"
    license = "CC BY-NC-SA"
    data_tags = ("Spatial",)
    download_description = """
        wget https://www.openml.org/data/download/22047757/miami2016.arff && mkdir -p local-data-warehouse/miami_housing && mv miami2016.arff local-data-warehouse/miami_housing/
    """
    bibtex = """
        @article{bourassa2021big,
          title={Big data, accessibility and urban house prices},
          author={Bourassa, Steven C and Hoesli, Martin and Merlin, Louis and Renne, John},
          journal={Urban Studies},
          volume={58},
          number={15},
          pages={3176--3195},
          year={2021},
          publisher={SAGE Publications Sage UK: London, England}
        }
    """
    curation_comments = """
        - We log scale the target.
        - We drop duplicated homes (non-unique identifiers and location) (~1% of the data).
        - We drop the ID column "PARCELNO".
        - Anomaly: while the original paper describes data with 57k samples, we only have 13k on OpenML or Kaggle.
    """

    # Task
    target = "SALE_PRC"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(f"{raw_dir}/miami2016.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop_duplicates(subset=["PARCELNO"])
        df = df.drop(columns=["PARCELNO"])
        df[self.task_metadata.target_column_name] = np.log(df[self.task_metadata.target_column_name])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "avno60plus",
            ],
        )
