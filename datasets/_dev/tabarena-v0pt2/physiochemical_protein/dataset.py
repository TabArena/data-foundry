"""Curated dataset definition for `physiochemical_protein` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class PhysiochemicalProtein(AbstractCuratedDataset):
    # Dataset
    unique_name = "physiochemical_protein"
    year = "2013"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5QW3H"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/physiochemical_protein/ && wget -P local-data-warehouse/physiochemical_protein/ https://archive.ics.uci.edu/static/public/265/physicochemical+properties+of+protein+tertiary+structure.zip && unzip local-data-warehouse/physiochemical_protein/physicochemical+properties+of+protein+tertiary+structure.zip -d local-data-warehouse/physiochemical_protein/
    """
    bibtex = r"""
        @misc{rana2013protein,
          author       = {Rana, Prashant},
          title        = {Physicochemical Properties of Protein Tertiary Structure},
          year         = {2013},
          howpublished = {\url{https://doi.org/10.24432/C5QW3H}},
          note         = {UCI Machine Learning Repository},
        }
    """
    curation_comments = """
        - We renamed the features to be more semantically meaningful.
    """

    # Task
    target = "ResidualSize"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/CASP.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "ResidualSize"
        df.columns = [
            target_feature,
            "TotalSurfaceArea",
            "NonPolarExposedArea",
            "FracExposedNonPolarResidue",
            "FracExposedNonPolarPart",
            "MassWeightedExposedArea",
            "AvgDeviationExposedArea",
            "EuclideanDistance",
            "SecondaryStructurePenalty",
            "SpatialDistNK",
        ]
        return df
