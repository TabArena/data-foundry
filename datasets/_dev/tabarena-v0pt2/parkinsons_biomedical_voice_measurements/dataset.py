"""Curated dataset definition for `parkinsons_biomedical_voice_measurements` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping


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
        @article{little2009suitability,
          title={Suitability of dysphonia measurements for telemonitoring of {Parkinson's} disease},
          author={Little, Max A. and McSharry, Patrick E. and Hunter, Eric J. and Spielman, Jennifer and Ramig, Lorraine O.},
          journal={IEEE Transactions on Biomedical Engineering},
          volume={56},
          number={4},
          pages={1015--1022},
          year={2009},
          doi={10.1109/TBME.2008.2005954}
        }

        @article{little2007exploiting,
          title={Exploiting nonlinear recurrence and fractal scaling properties for voice disorder detection},
          author={Little, Max A. and McSharry, Patrick E. and Roberts, Stephen J. and Costello, Declan A. E. and Moroz, Irene M.},
          journal={BioMedical Engineering OnLine},
          volume={6},
          pages={23},
          year={2007},
          doi={10.1186/1475-925X-6-23}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - We decode the group ID and session ID (time index per patient) from the name column.
    """

    # Task
    target = "status"
    problem_type = "binary_classification"
    grouping = Grouping(
        on="patient_id",
        labels="per_group",
        time_on="session_number",
        prediction_unit="group",
        aggregation="mean",
        context="all_rows",
        definition="""
            One group is a subject; its rows are about six sustained phonations (32 subjects). The use case is telediagnosis, "classifying subjects as healthy or PD" from their voice (Little et al. 2009), so one prediction per subject from the mean over its phonations, all of which are known. Little et al. scored phonations with a bootstrap that did not group by subject; Sakar & Kursun 2010 introduced leave-one-individual-out for this data. `session_number` counts a subject's recordings up.
        """,
    )

    # Splits
    splits_comment = """
        We create a default grouped split with label-per-group to judge if model can learn to predict the state of a patient given a set of recordings.
    """
    accepted_check_warnings = {
        "groups_test_groups_few": "32 subjects give 10-11 test subjects per fold; kept because the signal across "
        "subjects is real (2026-10-01, scripts/v2/group_probes.py: per-subject ROC AUC 0.82 for a logistic regression "
        "on 3 repeats, permutation test across subjects p = 0.01).",
        "task_group_time_on_few_unique": "`session_number` counts a subject's recordings up (1-7): it orders them "
        "within a subject, which is all `time_on` records (decided 2026-10-01).",
    }

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
        df = (
            df.sample(frac=1, random_state=42)
            .sort_values(by=["patient_id", "session_number"], kind="stable")
            .reset_index(drop=True)
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["patient_id"])
