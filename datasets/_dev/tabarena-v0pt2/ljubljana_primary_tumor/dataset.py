"""Curated dataset definition for `ljubljana_primary_tumor` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class LjubljanaPrimaryTumor(AbstractCuratedDataset):
    # Dataset
    unique_name = "ljubljana_primary_tumor"
    year = "1987"  # from the cite date on UCI...
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5WK5Q"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/83/primary+tumor.zip && unzip primary+tumor.zip primary-tumor.data && rm primary+tumor.zip && mkdir -p local-data-warehouse/ljubljana_primary_tumor && mv primary-tumor.data local-data-warehouse/ljubljana_primary_tumor/
    """
    bibtex = """
        @misc{Zwitter1987primarytumor,
          author       = {Zwitter, M. and Soklic, M.},
          title        = {{Primary Tumor}},
          year         = {1987},
          howpublished = {UCI Machine Learning Repository},
          note         = {{DOI}: https://doi.org/10.24432/C5WK5Q}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - We encode missing values as np.nan instead of "?".
        - We reverse the ordinal encoding of all features, adding the text back to the categories.
        - We drop classes with less than 10 samples to have sufficient data per class for a robust benchmark task. In reality, this would call for collecting more data on these classes, or treating it as an individual few-shot prediction task.
        - The data contains many duplicates (10%), which seems to be naturally occurring given the limited amount of features. Moreover, the duplicates sometimes have different targets. We keep the duplicates. While this might bias evaluation a bit, it represents the real-world task with ambiguous features better.
    """

    # Task
    target = "class"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "class",
            "age",
            "sex",
            "histologic-type",
            "degree-of-diffe",
            "bone",
            "bone-marrow",
            "lung",
            "pleura",
            "peritoneum",
            "liver",
            "brain",
            "skin",
            "neck",
            "supraclavicular",
            "axillar",
            "mediastinum",
            "abdominal",
        ]
        df = pd.read_csv(raw_dir / "primary-tumor.data", header=None, names=columns, na_values="?")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        domains = {
            "class": [
                "lung",
                "head & neck",
                "esophasus",
                "thyroid",
                "stomach",
                "duoden & sm.int",
                "colon",
                "rectum",
                "anus",
                "salivary glands",
                "pancreas",
                "gallblader",
                "liver",
                "kidney",
                "bladder",
                "testis",
                "prostate",
                "ovary",
                "corpus uteri",
                "cervix uteri",
                "vagina",
                "breast",
            ],
            "age": ["<30", "30-59", ">=60"],
            "sex": ["male", "female"],
            "histologic-type": ["epidermoid", "adeno", "anaplastic"],
            "degree-of-diffe": ["well", "fairly", "poorly"],
        }
        # yes/no attributes
        yes_no_cols = [
            "bone",
            "bone-marrow",
            "lung",
            "pleura",
            "peritoneum",
            "liver",
            "brain",
            "skin",
            "neck",
            "supraclavicular",
            "axillar",
            "mediastinum",
            "abdominal",
        ]
        for c in yes_no_cols:
            domains[c] = ["yes", "no"]
        for col, vals in domains.items():
            df[col] = df[col].map({i + 1: v for i, v in enumerate(vals)})
        # We drop classes with less than 10 samples
        df = df[df["class"].isin(df["class"].value_counts()[df["class"].value_counts() >= 10].index)]
        as_cat_type = list(domains.keys())
        df[as_cat_type] = df[as_cat_type].astype("category")
        return df
