"""Curated dataset definition for `cirrhosis_patient_survival_prediction` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class CirrhosisPatientSurvivalPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "cirrhosis_patient_survival_prediction"
    year = "1984"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5R02G"
    license = "IID"
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
