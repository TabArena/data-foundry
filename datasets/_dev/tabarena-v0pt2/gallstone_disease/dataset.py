"""Curated dataset definition for `gallstone_disease` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class GallstoneDisease(AbstractCuratedDataset):
    # Dataset
    unique_name = "gallstone_disease"
    year = "2023"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.1097/md.0000000000037258"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/1150/gallstone-1.zip && unzip gallstone-1.zip && rm gallstone-1.zip && unzip dataset-uci.zip && rm dataset-uci.zip && mkdir -p local-data-warehouse/gallstone_disease && mv dataset-uci.xlsx local-data-warehouse/gallstone_disease/
    """
    bibtex = r"""
        @article{esen2024early,
          title={Early prediction of gallstone disease with a machine learning-based method from bioimpedance and laboratory data},
          author={Esen, {\.I}rfan and Arslan, Hilal and Esen, Selin Akt{\"u}rk and G{\"u}l{\c{s}}en, Mervenur and K{\"u}ltekin, Nimet and {\"O}zdemir, O{\u{g}}uzhan},
          journal={Medicine},
          volume={103},
          number={8},
          pages={e37258},
          year={2024},
          publisher={LWW}
        }
    """
    curation_comments = """
        We use the data without any further curation.
    """

    # Task
    target = "Gallstone Status"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "dataset-uci.xlsx", sheet_name="dataset", engine="calamine")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Coronary Artery Disease (CAD)",
                "Hypothyroidism",
                "Gender",
                "Comorbidity",
                "Hyperlipidemia",
                "Diabetes Mellitus (DM)",
            ],
        )
