"""Curated dataset definition for `airfoil_self_noise` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class AirfoilSelfNoise(AbstractCuratedDataset):
    # Dataset
    unique_name = "airfoil_self_noise"
    year = "2014"
    domain = "physics & astronomy"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5VW2C"
    license = "CC BY 4.0"
    download_description = """
        mkdir -p local-data-warehouse/airfoil_self_noise/ && wget -P local-data-warehouse/airfoil_self_noise/ https://archive.ics.uci.edu/static/public/291/airfoil+self+noise.zip && unzip local-data-warehouse/airfoil_self_noise/airfoil+self+noise.zip -d local-data-warehouse/airfoil_self_noise/
    """
    bibtex = """
        @techreport{brooks1989airfoil,
          title={Airfoil self-noise and prediction},
          author={Brooks, Thomas F and Pope, D Stuart and Marcolini, Michael A},
          year={1989}
        }
    """
    curation_comments = "N/A"

    # Task
    target = "scaled-sound-pressure"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "airfoil_self_noise.dat", header=None, sep=r"\s+")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df.columns = [
            "frequency",
            "attack-angle",
            "chord-length",
            "free-stream-velocity",
            "suction-side-displacement-thickness",
            self.target,
        ]
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=("attack-angle",),
        )
