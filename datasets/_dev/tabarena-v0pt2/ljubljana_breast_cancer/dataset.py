"""Curated dataset definition for `ljubljana_breast_cancer` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class LjubljanaBreastCancer(AbstractCuratedDataset):
    # Dataset
    unique_name = "ljubljana_breast_cancer"
    year = "1988"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C51P4M"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/14/breast+cancer.zip && unzip breast+cancer.zip breast-cancer.data && rm breast+cancer.zip && mkdir -p local-data-warehouse/ljubljana_breast_cancer && mv breast-cancer.data local-data-warehouse/ljubljana_breast_cancer/
    """
    bibtex = """
        @misc{Zwitter1988BreastCancer,
          author       = {Zwitter, Matjaz and Soklic, Milan},
          title        = {{Breast Cancer}},
          year         = {1988},
          howpublished = {UCI Machine Learning Repository},
          note         = {{DOI}: https://doi.org/10.24432/C51P4M}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - We encode missing values as np.nan instead of "?".
        - We reverse the discretization of several numeric features and make them integers again.
        - We keep duplicates as they seem naturally occurring.
    """

    # Task
    target = "Class"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "Class",
            "age",
            "menopause",
            "tumor-size",
            "inv-nodes",
            "node-caps",
            "deg-malig",
            "breast",
            "breast-quad",
            "irradiat",
        ]
        df = pd.read_csv(raw_dir / "breast-cancer.data", header=None, names=columns, na_values="?")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw

        def interval_midpoint(x):
            """Convert strings like '10-19' -> 14 (mean of boundaries, rounded),
            '?' / NaN -> NaN, already-numeric -> as-is.
            """
            if pd.isna(x):
                return np.nan
            if isinstance(x, (int, float, np.integer, np.floating)):
                return x

            s = str(x).strip()
            if s in {"?", ""}:
                return np.nan

            m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", s)
            if not m:
                return np.nan  # or return s if you prefer to keep non-interval values

            a = int(m.group(1))
            b = int(m.group(2))
            return (a + b) / 2

        for c in ["age", "tumor-size", "inv-nodes"]:
            df[c] = df[c].map(interval_midpoint)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "menopause",
                "node-caps",
                "breast",
                "breast-quad",
                "irradiat",
            ],
        )
