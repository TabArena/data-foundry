"""Curated dataset definition for `hepatitis_c_prediction` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class HepatitisCPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "hepatitis_c_prediction"
    year = "2018"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5D612"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/571/hcv+data.zip && unzip hcv+data.zip && rm hcv+data.zip && mkdir -p local-data-warehouse/hepatitis_c_prediction && mv hcvdat0.csv local-data-warehouse/hepatitis_c_prediction/
    """
    bibtex = """
        @article{hoffmann2018using,
          title={Using machine learning techniques to generate laboratory diagnostic pathways—a case study},
          author={Hoffmann, Georg and Bietenbeck, Andreas and Lichtinghagen, Ralf and Klawonn, Frank},
          journal={Journal of Laboratory and Precision Medicine},
          volume={3},
          number={6},
          year={2018},
          publisher={AME Publishing Company}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - The hepatitis related classes were defined in the paper, but the blood donor class is not mentioned in it. It seems the paper might be related to a different task than the UCI release in the end. But it has the same features. Thus, after looking more into it, we adjust the classes. We drop the "suspect Blood Donor" class as we cannot map it to being part of a reasonable task. We thus treat the task as predicting whether a patient has one of three versions of hepatitis, or is "just" a blood donor.
    """

    # Task
    target = "Category"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "hcvdat0.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["Unnamed: 0"])
        df = df[df["Category"] != "0s=suspect Blood Donor"].reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Sex",
            ],
        )
