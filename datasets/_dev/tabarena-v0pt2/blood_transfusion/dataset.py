"""Curated dataset definition for `blood_transfusion` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class BloodTransfusion(AbstractCuratedDataset):
    # Dataset
    unique_name = "blood_transfusion"
    year = "2008"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5GS39"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/blood_transfusion/ && wget -P local-data-warehouse/blood_transfusion/ https://archive.ics.uci.edu/static/public/176/blood+transfusion+service+center.zip && unzip local-data-warehouse/blood_transfusion/blood+transfusion+service+center.zip -d local-data-warehouse/blood_transfusion/
    """
    bibtex = """
        @article{yeh2009knowledge,
          title={Knowledge discovery on RFM model using Bernoulli sequence},
          author={Yeh, I-Cheng and Yang, King-Jang and Ting, Tao-Ming},
          journal={Expert Systems with applications},
          volume={36},
          number={3},
          pages={5866--5871},
          year={2009},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We made feature names more descriptive.
        - We renamed the target and mapped binary values to "Yes"/"No".
        - Anomaly: the data has a lot of duplicates (29%) and several duplicates with different target values.
    """

    # Task
    target = "DonatedBloodInMarch2007"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/transfusion.data")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "DonatedBloodInMarch2007"
        df.columns = [
            "MonthsSinceLastDonation",
            "NumberOfDonations",
            "TotalBloodDonated",
            "MonthsSinceFirstDonation",
            target_feature,
        ]
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})
        return df
