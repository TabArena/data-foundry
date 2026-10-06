"""Curated dataset definition for `airfoil_self_noise` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping


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
    curation_comments = """
        - The 1,503 rows are 106 wind-tunnel runs: one airfoil section (6 chord lengths) at one angle of attack and one free-stream velocity (4), each a measured one-third-octave spectrum of 8 to 19 frequency bands. The raw file stores each run as one consecutive block, and the suction-side displacement thickness is constant within a run (it is computed from the run's settings). We add the run as the group column `run`.
        - Grouped by run since 2026-10-06 (IID before): a model is used for an airfoil configuration that was not measured, while a random split gave a test row 62% of its run's other bands in train, so models filled gaps in spectra they had seen. R^2, 5 x 3 folds, random against grouped by run: extra trees 0.946 / 0.850, LightGBM 0.937 / 0.840, random forest 0.926 / 0.830, kNN-5 0.755 / 0.629, ridge 0.510 / 0.490. Not grouped by chord length: a new airfoil size is a harder extrapolation than a new run.
    """

    # Task
    target = "scaled-sound-pressure"
    problem_type = "regression"
    grouping = Grouping(
        on="run",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a wind-tunnel run: one NACA 0012 airfoil section (chord length) at one angle of attack and one free-stream velocity; its rows are the bands of the run's measured one-third-octave sound spectrum (8 to 19 per run, 106 runs; Brooks et al. 1989). The use case is predicting the self-noise of an airfoil configuration that was not measured, and a measured run comes with its whole spectrum, so the test runs are new to the model. Each row is one prediction, made from its band's frequency and the run's settings.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the wind-tunnel run: all bands of a measured spectrum stay on one side, so a model predicts the spectrum of a configuration it has not seen. Runs with the same airfoil, angle or velocity in other combinations can be on both sides.
    """

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
        # a run is one airfoil at one angle and one velocity; the file stores it as one block of frequency bands
        settings = ["chord-length", "attack-angle", "free-stream-velocity"]
        df["run"] = df.groupby(settings, sort=False).ngroup().map("run_{:03d}".format)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=("attack-angle", "run"),
        )
