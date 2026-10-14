"""Curated dataset definition for `south_africa_coronary_heart_disease` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class SouthAfricaCoronaryHeartDisease(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Does a man from a high-risk region have coronary heart disease, judging from his risk factors?"),
        use_case=(
            "For example, a doctor screening men in a high-risk region estimates their risk of coronary heart disease"
            " from routine risk factors, to decide on prevention."
        ),
        row=(
            "One man from a high-risk region of the Western Cape, South Africa, in a retrospective sample of the "
            "CORIS study with about two men without heart disease per man with it (462 men)."
        ),
        predicted=(
            "Whether the man has coronary heart disease; 34.6% do. There is no time frame, as the cases had their "
            "event before the measurements."
        ),
        known=(
            "Age, family history of heart disease, systolic blood pressure, lifetime tobacco use, LDL cholesterol, "
            "adiposity, obesity, alcohol use and a type-A behaviour score, for the cases measured after their heart "
            "attack."
        ),
        split="Random men of the same sample.",
        fit="approximate",
        fit_reason=(
            "A case-control sample measured after the cases' heart attacks stands in for predicting heart disease "
            "before it happens; some cases had already improved their risk factors. Per the leak audit this weakens "
            "rather than leaks the signal (ROC AUC 0.774 with, 0.778 without blood pressure and obesity)."
        ),
    )

    # Dataset
    unique_name = "south_africa_coronary_heart_disease"
    year = "2001"
    domain = "medical & healthcare"
    source = "Other"  # the data page of The Elements of Statistical Learning; the Kaggle file is a copy
    source_url = "https://hastie.su.domains/ElemStatLearn/"
    license = "CC BY-SA 4.0"
    download_description = """
        We get the data from Kaggle, as it has the best curation and documentation.

        kaggle datasets download waalbannyantudre/south-african-heart-disease-dataset && unzip south-african-heart-disease-dataset.zip && rm south-african-heart-disease-dataset.zip
        mkdir -p local-data-warehouse/south_africa_coronary_heart_disease && mv SAHeart.csv local-data-warehouse/south_africa_coronary_heart_disease/
    """
    bibtex = r"""
        @article{rossouw1983coronary,
          title={Coronary risk factor screening in three rural communities. The CORIS baseline study.},
          author={Rossouw, JE and Du Plessis, JP and Benad{\'e}, AJ and Jordaan, PC and Kotze, JP and Jooste, PL and Ferreira, JJ},
          journal={South African medical journal= Suid-Afrikaanse tydskrif vir geneeskunde},
          volume={64},
          number={12},
          pages={430--436},
          year={1983}
        }
    """
    curation_comments = """
        We start with the data from Kaggle.

        - We remove the row id column.
        - The data is a retrospective sample of males from the CORIS study (cases with coronary heart disease and controls). Hastie, Tibshirani & Friedman (The Elements of Statistical Learning, 2nd ed., Sec. 5.2.2, p. 148) note: "These measurements were made sometime after the patients suffered a heart attack, and in many cases they had already benefited from a healthier diet and lifestyle". Some risk factors of the cases (e.g. sbp, obesity) were therefore measured after the outcome. This weakens their signal rather than leaking the target (dropping sbp and obesity changes ROC AUC from 0.774 to 0.778), so we keep all features.
    """

    # Task
    target = "chd"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "SAHeart.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["row.names"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "famhist",
            ],
        )
