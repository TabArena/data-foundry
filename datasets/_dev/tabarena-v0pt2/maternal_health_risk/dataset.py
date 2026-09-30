"""Curated dataset definition for `maternal_health_risk` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class MaternalHealthRisk(AbstractCuratedDataset):
    # Dataset
    unique_name = "maternal_health_risk"
    year = "2020"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5DP5D"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/maternal_health_risk/ && wget -P local-data-warehouse/maternal_health_risk/ https://archive.ics.uci.edu/static/public/863/maternal+health+risk.zip && unzip local-data-warehouse/maternal_health_risk/maternal+health+risk.zip -d local-data-warehouse/maternal_health_risk/
    """
    bibtex = r"""
        @inproceedings{ahmed2020review,
          title={Review and analysis of risk factor of maternal health in remote area using the Internet of Things (IoT)},
          author={Ahmed, Marzia and Kashem, Mohammod Abul and Rahman, Mostafijur and Khatun, Sabira},
          booktitle={InECCE2019: Proceedings of the 5th International Conference on Electrical, Control \& Computer Engineering, Kuantan, Pahang, Malaysia, 29th July 2019},
          pages={357--365},
          year={2020},
          organization={Springer}
        }
    """
    curation_comments = """
        - Anomaly: the data has a lot of duplicates (55%).
    """

    # Task
    target = "RiskLevel"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/Maternal Health Risk Data Set.csv")
        return df
