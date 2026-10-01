"""Curated dataset definition for `qsar_fish_toxicity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class QsarFishToxicity(AbstractCuratedDataset):
    # Dataset
    unique_name = "qsar_fish_toxicity"
    year = "2015"
    domain = "biology & life sciences"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5JG7B"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/qsar_fish_toxicity/ && wget -P local-data-warehouse/qsar_fish_toxicity/ https://archive.ics.uci.edu/static/public/504/qsar+fish+toxicity.zip && unzip local-data-warehouse/qsar_fish_toxicity/qsar+fish+toxicity.zip -d local-data-warehouse/qsar_fish_toxicity/
    """
    bibtex = r"""
        @article{cassotti2015similarity,
          title={A similarity-based QSAR model for predicting acute toxicity towards the fathead minnow (Pimephales promelas)},
          author={Cassotti, Matteo and Ballabio, Davide and Todeschini, Roberto and Consonni, Viviana},
          journal={SAR and QSAR in Environmental Research},
          volume={26},
          number={3},
          pages={217--243},
          year={2015},
          publisher={Taylor \& Francis}
        }
    """
    curation_comments = """
        - We assigned descriptive column names following the original dataset documentation.
        - Anomaly: the data contains a lot of duplicates (15%) when ignoring the target feature.
    """

    # Task
    target = "LC50"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/qsar_fish_toxicity.csv", sep=";", header=None)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "LC50"
        df.columns = [
            "CIC0",
            "SM1_Dz(Z)",
            "GATS1i",
            "NdsCH",
            "NdssC",
            "MLOGP",
            target_feature,
        ]
        return df
