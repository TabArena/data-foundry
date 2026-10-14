"""Curated dataset definition for `cirrhosis_patient_survival_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class CirrhosisPatientSurvivalPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How long after entering the study will a patient with primary biliary cirrhosis die, given that the "
            "patient dies before the study ends?"
        ),
        use_case=(
            "Closest: when a patient with primary biliary cirrhosis is first seen, a hepatologist estimates the time "
            "left to live, for example to time a liver transplant. The data cannot serve it: it holds only the "
            "patients who died before the follow-up ended."
        ),
        row=(
            "One patient of the Mayo Clinic primary biliary cirrhosis study (referred 1974 to 1984) who died before "
            "the follow-up ended in July 1986; 161 patients, 36 of them outside the drug trial."
        ),
        predicted="The time from registration to death, in days on a logarithmic scale.",
        known=(
            "Age, sex, the trial drug (D-penicillamine or placebo; missing outside the trial), physical signs (fluid "
            "in the abdomen, enlarged liver, spider veins, swelling), blood and urine tests (bilirubin, cholesterol, "
            "albumin, copper, liver enzymes, triglycerides, platelets, clotting time) and the histologic stage."
        ),
        split="Random patients among those who died.",
        changes=(
            "We keep only the patients who died and predict their time to death, dropping the patients censored at a "
            "transplant or at the end of follow-up; the source is a survival study that counts them."
        ),
        fit="none",
        fit_reason=(
            "The patients are chosen by their outcome: only deaths before July 1986 are in, so a patient registered "
            "in 1984 enters only with a short survival. At registration nobody knows whether a patient belongs to "
            "this group, so no decision fits. The curator kept the deaths-only target on purpose (2026-09-30)."
        ),
    )

    # Dataset
    unique_name = "cirrhosis_patient_survival_prediction"
    year = "1991"
    domain = "medical & healthcare"
    source = "Other"  # the Mayo Clinic PBC trial data (Fleming and Harrington 1991); UCI 878 is a later copy
    source_url = "https://www.mayo.edu/research/documents/pbchtml/doc-10027635"
    license = "CC BY 4.0"  # stated on UCI 878, the copy we download
    download_description = """
        We get the UCI data.

        wget https://archive.ics.uci.edu/static/public/878/cirrhosis+patient+survival+prediction+dataset-1.zip && unzip cirrhosis+patient+survival+prediction+dataset-1.zip && rm cirrhosis+patient+survival+prediction+dataset-1.zip && mkdir -p local-data-warehouse/cirrhosis_patient_survival_prediction && mv cirrhosis.csv local-data-warehouse/cirrhosis_patient_survival_prediction/
    """
    bibtex = """
        @article{dickson1989prognosis,
          title={Prognosis in primary biliary cirrhosis: model for decision making},
          author={Dickson, E Rolland and Grambsch, Patricia M and Fleming, Thomas R and Fisher, Lloyd D and Langworthy, Alice},
          journal={Hepatology},
          volume={10},
          number={1},
          pages={1--7},
          year={1989},
          publisher={Wiley Online Library}
        }
    """
    curation_comments = """
        We start with the UCI data.

        We note that this is a survival prediction task. But the way we split the data and score the task, it is not treated correctly as a survival prediction task. At the same time, it is randomized control data based on the Drug column. We treat it as a regression task to predict the time-to-death for non-censored patients, including the drug column into the modelling.

        - We drop ID and Status column as they have no relevance after filtering to only non-censored patients.
        - We log transform N_days and rename it to the target "log_days_to_death".
    """

    # Task
    target = "log_days_to_death"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "cirrhosis.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df[df["Status"] == "D"]
        df["log_days_to_death"] = np.log(df["N_Days"])
        df = df.drop(columns=["ID", "Status", "N_Days"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Drug",
                "Ascites",
                "Hepatomegaly",
                "Spiders",
                "Edema",
                "Stage",
                "Sex",
            ],
        )
