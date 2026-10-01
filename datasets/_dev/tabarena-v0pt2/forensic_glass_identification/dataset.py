"""Curated dataset definition for `forensic_glass_identification` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class ForensicGlassIdentification(AbstractCuratedDataset):
    # Dataset
    unique_name = "forensic_glass_identification"
    year = "1987"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5WW2P"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/42/glass+identification.zip && unzip glass+identification.zip && rm glass+identification.zip glass.names glass.tag Index
        mkdir -p local-data-warehouse/forensic_glass_identification && mv glass.data local-data-warehouse/forensic_glass_identification/
    """
    bibtex = """
        @misc{German1987glass,
          author       = {German, B.},
          title        = {{Glass Identification}},
          year         = {1987},
          howpublished = {UCI Machine Learning Repository},
          note         = {{DOI}: https://doi.org/10.24432/C5WW2P}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - We drop the ID column, as it is a just a row identifier and does not contain any useful information for modeling.
        - The data contains one naturally occurring duplicate.
    """

    # Task
    target = "Type_of_glass"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = ["Id", "RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "Type_of_glass"]
        df = pd.read_csv(raw_dir / "glass.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["Id"])
        return df
