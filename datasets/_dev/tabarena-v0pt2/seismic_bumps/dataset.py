"""Curated dataset definition for `seismic_bumps` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class SeismicBumps(AbstractCuratedDataset):
    # Dataset
    unique_name = "seismic_bumps"
    year = "2013"
    domain = "environmental science & climate"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5W902"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/seismic_bumps/ && wget -P local-data-warehouse/seismic_bumps/ https://archive.ics.uci.edu/static/public/266/seismic+bumps.zip && unzip local-data-warehouse/seismic_bumps/seismic+bumps.zip -d local-data-warehouse/seismic_bumps/
    """
    bibtex = r"""
        @article{sikora2010application,
          title={Application of rule induction algorithms for analysis of data collected by seismic hazard monitoring systems in coal mines},
          author={Sikora, Marek and Wr{\'o}bel, {\L}ukasz},
          journal={Archives of Mining Sciences},
          volume={55},
          number={1},
          pages={91--114},
          year={2010}
        }
    """
    curation_comments = """
        - We renamed the target feature and reversed the values' ordinal encoding.
        - We drop the constant columns "nbumps6", "nbumps7", and "nbumps89".
    """

    # Task
    target = "HighEnergySeismicBump"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(f"{raw_dir}/seismic-bumps.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "HighEnergySeismicBump"
        df = df.rename(columns={"class": target_feature})
        df[target_feature] = df[target_feature].map({"1": "Yes", "0": "No"})
        # Drop constant columns
        df = df.loc[:, (df != df.iloc[0]).any()]
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "seismic",
                "seismoacoustic",
                "shift",
                "ghazard",
            ],
        )
