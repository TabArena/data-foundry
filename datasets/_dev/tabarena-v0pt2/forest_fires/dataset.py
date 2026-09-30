"""Curated dataset definition for `forest_fires` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class ForestFires(AbstractCuratedDataset):
    # Dataset
    unique_name = "forest_fires"
    year = "2008"
    domain = "environmental science & climate"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5D88D"
    license = "CC BY 4.0"
    data_tags = ("Spatial", "ForcedIIDFromTemporal")
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/162/forest+fires.zip && unzip forest+fires.zip && rm forest+fires.zip forestfires.names
        mkdir -p local-data-warehouse/forest_fires && mv forestfires.csv local-data-warehouse/forest_fires/
    """
    bibtex = r"""
        @article{cortez2007data,
          title={A data mining approach to predict forest fires using meteorological data},
          author={Cortez, Paulo and Morais, An{\'\i}bal de Jesus Raimundo},
          year={2007},
          publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - The original paper used a IID split. The tasks sounds like it requires a temporal split. However, the data does not contain the original time indices (or order of samples) and just month/day over 3 years. Furthermore, the authors made sure to only use time-invariant features as it seems they wanted to develop a time-invaraint model for deployment and analysis of the data. In other words, this task can be handled by IID splits. Furthermore, the task in the paper was about using algorithms also for feature selection (so scientific discovery).
        - We log1p scale the target as suggest by the authors.
        - The data contains naturally occurring duplicates.
    """

    # Task
    target = "area"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "forestfires.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["area"] = np.log1p(df["area"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "month",
                "day",
            ],
        )
