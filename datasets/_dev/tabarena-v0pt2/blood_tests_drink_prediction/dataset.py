"""Curated dataset definition for `blood_tests_drink_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class BloodTestsDrinkPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "blood_tests_drink_prediction"
    year = "1996"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C54G67"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/60/liver+disorders.zip &&  unzip liver+disorders.zip bupa.data && rm liver+disorders.zip
        mkdir -p local-data-warehouse/blood_tests_drink_prediction && mv bupa.data local-data-warehouse/blood_tests_drink_prediction/
    """
    bibtex = r"""
        @misc{UCILiverDisorders2016,
          title        = {Liver Disorders},
          author       = {{UCI Machine Learning Repository}},
          year         = {2016},
          howpublished = {\url{https://doi.org/10.24432/C54G67}},
          note         = {Dataset}
        }
    """
    curation_comments = """
        The task is framed as a liver disorder prediction task, but we only have data bout the amount of drinks consumed. So instead, we will frame it as a task to predict the number of drinks based on the blood work data. This is a proxy for the original task, where later based on the number of drinks the liver disorder was determined.

        - We drop the selector column, as we ignore the original train/test split, and will create our own splits.
        - The data contains natural duplicates, so we keep them.
        - We log1p scale the target.
    """

    # Task
    target = "drinks"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(
            raw_dir / "bupa.data",
            header=None,
            names=["mcv", "alkphos", "sgpt", "sgot", "gammagt", "drinks", "selector"],
        )
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["selector"])
        df["drinks"] = np.log1p(df["drinks"])
        return df
