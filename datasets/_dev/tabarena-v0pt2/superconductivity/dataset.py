"""Curated dataset definition for `superconductivity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class Superconductivity(AbstractCuratedDataset):
    # Dataset
    unique_name = "superconductivity"
    year = "2018"
    domain = "physics & astronomy"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C53P47"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/superconductivity/ && wget -P local-data-warehouse/superconductivity/ https://archive.ics.uci.edu/static/public/464/superconductivty+data.zip && unzip local-data-warehouse/superconductivity/superconductivty+data.zip -d local-data-warehouse/superconductivity/ && rm local-data-warehouse/superconductivity/superconductivty+data.zip
    """
    bibtex = """
        @article{hamidieh2018data,
          title={A data-driven statistical model for predicting the critical temperature of a superconductor},
          author={Hamidieh, Kam},
          journal={Computational Materials Science},
          volume={154},
          pages={346--354},
          year={2018},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - Anomaly: the data has a lot of duplicates (29%) when ignoring the target feature
    """

    # Task
    target = "critical_temp"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/train.csv")
        return df
