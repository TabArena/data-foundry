"""Curated dataset definition for `hepatitis_survival_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class HepatitisSurvivalPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a patient with hepatitis die?",
        use_case=(
            "For example, a physician estimates a hepatitis patient's prognosis from the examination, blood tests and"
            " liver biopsy, to decide on treatment and follow-up."
        ),
        row=(
            "One patient with hepatitis (155 patients, described by Efron and Gong in 1981; place and period not "
            "stated)."
        ),
        predicted="Whether the patient died (21%) or lived; the follow-up period is not stated.",
        known=(
            "Age and sex, treatment with steroids or antivirals, symptoms and findings (fatigue, malaise, loss of "
            "appetite, liver size and firmness, spleen, spider veins, ascites, varices), blood tests (bilirubin, "
            "liver enzymes, albumin, clotting time) and the biopsy's histology."
        ),
        split="Random patients of the same study, standing for new patients.",
        fit="approximate",
        fit_reason=(
            "The source states neither the follow-up period nor when the findings were recorded relative to the "
            "outcome, and two inputs are treatments whose timing is not stated."
        ),
    )

    # Dataset
    unique_name = "hepatitis_survival_prediction"
    year = "1988"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5Q59J"
    license = "CC BY 4.0"
    download_description = """
        Get the UCI data.

        wget https://archive.ics.uci.edu/static/public/46/hepatitis.zip && unzip hepatitis.zip hepatitis.data && rm hepatitis.zip && mkdir -p local-data-warehouse/hepatitis_survival_prediction && mv hepatitis.data local-data-warehouse/hepatitis_survival_prediction/
    """
    bibtex = """
        @inproceedings{efron1981statistical,
          title={Statistical theory and the computer},
          author={Efron, Bradley and Gong, Gail},
          booktitle={Computer science and statistics: Proceedings of the 13th Symposium on the Interface},
          pages={3--7},
          year={1981},
          organization={Springer}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - We encode missing values as NaN.
        - We convert numeric features to float and categorical features to category dtype.
        - The target stays coded as in the UCI file: 1 = died (32 patients), 2 = lived (123); the names file lists the classes as "DIE, LIVE" in this order.
        - Prediction point: not stated. The inputs (examination, blood tests, biopsy histology) imply the patient's work-up; the UCI names file gives neither when they were recorded nor the follow-up period for death.
    """

    # Task
    target = "class"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "class",
            "age",
            "sex",
            "steroid",
            "antivirals",
            "fatigue",
            "malaise",
            "anorexia",
            "liver_big",
            "liver_firm",
            "spleen_palpable",
            "spiders",
            "ascites",
            "varices",
            "bilirubin",
            "alk_phosphate",
            "sgot",
            "albumin",
            "protime",
            "histology",
        ]
        df = pd.read_csv(raw_dir / "hepatitis.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.replace("?", np.nan)
        as_float_type = ["age", "bilirubin", "alk_phosphate", "sgot", "albumin", "protime"]
        df[as_float_type] = df[as_float_type].astype(float)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "sex",
                "steroid",
                "antivirals",
                "fatigue",
                "malaise",
                "anorexia",
                "liver_big",
                "liver_firm",
                "spleen_palpable",
                "spiders",
                "ascites",
                "varices",
                "histology",
            ],
        )
