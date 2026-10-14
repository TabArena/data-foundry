"""Curated dataset definition for `blood_transfusion` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


class BloodTransfusion(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a past blood donor give blood at the next collection?",
        use_case=(
            "Before a blood drive, a blood transfusion service decides which donors in its database to contact, from "
            "their donation history (the source studies such targeting with a recency-frequency model)."
        ),
        row=(
            "One donor of the Blood Transfusion Service Center in Hsin-Chu City, Taiwan, drawn at random from its "
            "donor database (748 donors); its bus collects blood at a university about every three months."
        ),
        predicted="Whether the donor gave blood in March 2007.",
        known=(
            "Months since the last and since the first donation, the number of donations and the total volume of "
            "blood donated."
        ),
        split="Random donors of the same database and the same month.",
        fit="approximate",
        fit_reason=(
            "One month's outcome stands in for a forecast: the model is trained and tested on donors of the same "
            "March 2007 collection, whereas a service would train on earlier drives. With four history counts, 29% of"
            " the rows repeat another row, some with the other label."
        ),
    )

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
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})
        return df
