"""Curated dataset definition for `parkinsons_biomedical_voice_measurements` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class ParkinsonsBiomedicalVoiceMeasurements(AbstractCuratedDataset):
    # Dataset
    unique_name = "parkinsons_biomedical_voice_measurements"
    year = "2007"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C59C74"
    license = "CC BY 4.0"
    data_tags = ("Non-IID", "Grouped", "WrongDomain")  # Maybe also temporal but not of importance for the task.
    download_description = """
        We get the 2007 data from the UCI repository.

        wget https://archive.ics.uci.edu/static/public/174/parkinsons.zip && unzip parkinsons.zip parkinsons.data && rm parkinsons.zip && mkdir -p local-data-warehouse/parkinsons_biomedical_voice_measurements && mv parkinsons.data local-data-warehouse/parkinsons_biomedical_voice_measurements/
    """
    bibtex = """
        @article{little2007exploiting,
          title={Exploiting nonlinear recurrence and fractal scaling properties for voice disorder detection},
          author={Little, Max and Mcsharry, Patrick and Roberts, Stephen and Costello, Declan and Moroz, Irene},
          journal={Nature Precedings},
          pages={1--1},
          year={2007},
          publisher={Nature Publishing Group UK London}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - We decode the group ID and session ID (time index per patient) from the name column.
    """

    # Task
    target = "status"
    problem_type = "binary_classification"
    group_on = "patient_id"
    group_labels = "per_group"
    group_time_on = "session_number"

    # Splits
    splits_comment = """
        We create a default grouped split with label-per-group to judge if model can learn to predict the state of a patient given a set of recordings.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "parkinsons.data")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Split session number from patient ID, split on the last _
        df[["patient_id", "session_number"]] = df["name"].str.rsplit("_", n=1, expand=True)
        df["session_number"] = df["session_number"].astype(int)
        df = df.drop(columns=["name"])
        # cast before the sort below, which orders by category
        df["patient_id"] = df["patient_id"].astype("category")
        df = df.sample(frac=1, random_state=42).sort_values(by=["patient_id", "session_number"]).reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["patient_id"])


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
