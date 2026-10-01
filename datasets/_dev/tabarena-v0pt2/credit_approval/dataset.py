"""Curated dataset definition for `credit_approval` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class CreditApproval(AbstractCuratedDataset):
    # Dataset
    unique_name = "credit_approval"
    year = "1987"
    domain = "finance"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5FS30"
    license = "CC BY 4.0"
    download_description = """
        We get the credit screening data from UCI.

        wget https://archive.ics.uci.edu/static/public/27/credit+approval.zip && unzip credit+approval.zip  crx.data && rm credit+approval.zip  && mkdir -p local-data-warehouse/credit_approval && mv crx.data  local-data-warehouse/credit_approval/
    """
    bibtex = """
        @article{quinlan1987simplifying,
          title={Simplifying decision trees},
          author={Quinlan, J. Ross},
          journal={International journal of man-machine studies},
          volume={27},
          number={3},
          pages={221--234},
          year={1987},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We get the data from UCI.

        - We encode A14 as numeric, following the description of it being a continuous feature.
    """

    # Task
    target = "A16"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "A1",
            "A2",
            "A3",
            "A4",
            "A5",
            "A6",
            "A7",
            "A8",
            "A9",
            "A10",
            "A11",
            "A12",
            "A13",
            "A14",
            "A15",
            "A16",
        ]
        df = pd.read_csv(raw_dir / "crx.data", header=None, names=columns, na_values="?")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["A14"] = pd.to_numeric(df["A14"], errors="coerce")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "A1",
                "A4",
                "A5",
                "A6",
                "A7",
                "A9",
                "A10",
                "A12",
                "A13",
            ],
        )
