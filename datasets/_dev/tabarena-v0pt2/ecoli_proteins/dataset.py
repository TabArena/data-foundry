"""Curated dataset definition for `ecoli_proteins` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class EcoliProteins(AbstractCuratedDataset):
    # Dataset
    unique_name = "ecoli_proteins"
    year = "1996"
    domain = "biology & life sciences"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5388M"
    license = "CC BY 4.0"
    download_description = """
        wget https://archive.ics.uci.edu/static/public/39/ecoli.zip && unzip ecoli.zip && rm ecoli.zip ecoli.names
        mkdir -p local-data-warehouse/ecoli_proteins && mv ecoli.data local-data-warehouse/ecoli_proteins/
    """
    bibtex = """
        @inproceedings{horton1996probabilistic,
          title={A probabilistic classification system for predicting the cellular localization sites of proteins.},
          author={Horton, Paul and Nakai, Kenta},
          booktitle={Ismb},
          volume={4},
          pages={109--115},
          year={1996},
          organization={St. Louis, Missouri, USA}
        }
    """
    curation_comments = """
        We start with the dataset from UCI.

        - We drop the sequence name column, which is a unique identifier.
        - We drop three classes with less than 10 samples each: omL (5), imL (2), and imS (3).
        - We drop "chg", which becomes constant after our preprocessing steps.
    """

    # Task
    target = "class"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        feature_names = [
            "Sequence Name",
            "mcg",
            "gvh",
            "lip",
            "chg",
            "aac",
            "alm1",
            "alm2",
            "class",
        ]
        df = pd.read_csv(raw_dir / "ecoli.data", header=None, names=feature_names, sep=r"\s+")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(
            columns=[
                "Sequence Name",  # avoid leakage from look the name and otherwise unique identifier.
                "chg",  # constant after preprocessing
            ]
        )
        # Drop samples with classes with too little data (less than 10 samples)
        df = df[~df["class"].isin(["omL", "imL", "imS"])]
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "lip",
            ],
        )
