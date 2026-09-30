"""Curated dataset definition for `concrete_compressive_strength` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class ConcreteCompressiveStrength(AbstractCuratedDataset):
    # Dataset
    unique_name = "concrete_compressive_strength"
    year = "1998"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5PK67"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/concrete_compressive_strength/ && wget -P local-data-warehouse/concrete_compressive_strength/ https://archive.ics.uci.edu/static/public/165/concrete+compressive+strength.zip && unzip local-data-warehouse/concrete_compressive_strength/concrete+compressive+strength.zip -d local-data-warehouse/concrete_compressive_strength/
    """
    bibtex = """
        @article{yeh1998modeling,
          title={Modeling of strength of high-performance concrete using artificial neural networks},
          author={Yeh, I-C},
          journal={Cement and Concrete research},
          volume={28},
          number={12},
          pages={1797--1808},
          year={1998},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We rename features to be shorter while similar to the original names.
    """

    # Task
    target = "ConcreteCompressiveStrength"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(f"{raw_dir}/Concrete_Data.xls")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "ConcreteCompressiveStrength"
        df.columns = [
            "Cement",
            "BlastFurnaceSlag",
            "FlyAsh",
            "Water",
            "Superplasticizer",
            "CoarseAggregate",
            "FineAggregate",
            "Age",
            target_feature,
        ]
        return df
