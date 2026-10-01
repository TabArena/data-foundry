"""Curated dataset definition for `telemonitoring_parkinsons_biomedical_voice_measurements` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class TelemonitoringParkinsonsBiomedicalVoiceMeasurements(AbstractCuratedDataset):
    # Dataset
    unique_name = "telemonitoring_parkinsons_biomedical_voice_measurements"
    year = "2007"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C59C74"
    license = "CC BY 4.0"
    data_tags = ("Non-IID", "Grouped", "WrongDomain")
    download_description = """
        We get the 2009 data from the UCI repository.

        wget https://archive.ics.uci.edu/static/public/174/parkinsons.zip && unzip parkinsons.zip telemonitoring/parkinsons_updrs.data && mv telemonitoring/parkinsons_updrs.data parkinsons_updrs.data && rm -rf parkinsons.zip telemonitoring && mkdir -p local-data-warehouse/telemonitoring_parkinsons_biomedical_voice_measurements && mv parkinsons_updrs.data local-data-warehouse/telemonitoring_parkinsons_biomedical_voice_measurements/
    """
    bibtex = """
        @article{tsanas2009accurate,
          title={Accurate telemonitoring of Parkinson’s disease progression by non-invasive speech tests},
          author={Tsanas, Athanasios and Little, Max and McSharry, Patrick and Ramig, Lorraine},
          journal={Nature Precedings},
          pages={1--1},
          year={2009},
          publisher={Nature Publishing Group UK London}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        We aim to simulate the task of predicting the UPDRS score of Parkinson's patients based on their voice measurements over time. This represents the task of only getting the voice measurements to judge the UPDRS. We assume we have no measurement of a patient to make this call. Thus, we have a grouped data task, where we have to holdout entire patients over time. We thus test for one patients multiple time points and repeated measurements at once.

        - We use total_UPDRS as target. Note that real UPDRS values were were obtained at baseline, three-month and six-month trial period and all other weekly cases were interpolated. Thus, the ground truth is not perfect and just an estimate based on knowing the future. We reduce it to three values (first, medium <130 days, last), as we have no other ground truth.
        - We have several measurements per day for each patient when they were measured. We have some edge cases with negative test time as they got measured before the study started.
    """

    # Task
    target = "total_UPDRS"
    problem_type = "regression"
    group_on = "subject#"
    group_labels = "per_sample"
    group_time_on = "test_time"

    # Splits
    splits_comment = """
        We create a default group-label-per-sample split. We thus simulate the use case that someone fits a model and deploys it to predict the UPDRS score of a new patient based on their voice measurements for some time, ignoring the trajectory of the patient itself. We thus have to hold out entire patients and test for one patients multiple time points and repeated measurements at once.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "parkinsons_updrs.data")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(
            columns=[
                "motor_UPDRS",
            ]
        )
        # cast here: the groupby and the sort below run on the categorical subject ids
        df["subject#"] = df["subject#"].astype("category")

        def select_rows(x):
            # Anchor times
            first_time = x.iloc[0]["test_time"]
            last_time = x.iloc[-1]["test_time"]

            before_130 = x[x["test_time"] < 130]
            last_before_130_time = before_130.iloc[-1]["test_time"]

            # Collect times to keep
            times_to_keep = {first_time, last_time}
            times_to_keep.add(last_before_130_time)

            # Keep all rows with matching test_time
            return x[x["test_time"].isin(times_to_keep)]

        df = df.groupby("subject#", group_keys=False).apply(select_rows).reset_index(drop=True)
        df = df.sample(frac=1, random_state=42).sort_values(by=["subject#", "test_time"]).reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["sex", "subject#"])


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
