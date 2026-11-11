"""Curated dataset definition for `hepatitis_survival_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode


class HepatitisSurvivalPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a patient with hepatitis die?",
        use_case=(
            "For example, a physician estimates a hepatitis patient's prognosis from the examination and blood tests,"
            " to decide on treatment and follow-up."
        ),
        row=(
            "One patient with chronic hepatitis seen at Stanford Medical School before 1982 (155 patients, described "
            "by Efron and Gong in 1983)."
        ),
        predicted="Whether the patient died (21%) or lived; the follow-up period is not stated.",
        known=(
            "Age and sex, treatment with steroids or antivirals, symptoms and findings (fatigue, malaise, loss of "
            "appetite, liver size and firmness, spleen, spider veins, ascites, varices), blood tests (bilirubin, "
            "liver enzymes, albumin, clotting time) and the physician's prognosis."
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
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5Q59J",
            license="CC BY 4.0",
            year="1988",
            bibtex=r"""
                @article{efron1983leisurely,
                  title={A leisurely look at the bootstrap, the jackknife, and cross-validation},
                  author={Efron, Bradley and Gong, Gail},
                  journal={The American Statistician},
                  volume={37},
                  number={1},
                  pages={36--48},
                  year={1983},
                  publisher={Taylor \& Francis},
                  doi={10.1080/00031305.1983.10483087}
                }
            """,
        ),
    )
    download_description = """
        Get the UCI data.

        wget https://archive.ics.uci.edu/static/public/46/hepatitis.zip && unzip hepatitis.zip hepatitis.data && rm hepatitis.zip && mkdir -p local-data-warehouse/hepatitis_survival_prediction && mv hepatitis.data local-data-warehouse/hepatitis_survival_prediction/
    """
    curation_comments = """
        We start with the data from UCI.

        - We encode missing values as NaN.
        - We convert numeric features to float and categorical features to category dtype.
        - The target stays coded as in the UCI file: 1 = died (32 patients), 2 = lived (123); the names file lists the classes as "DIE, LIVE" in this order.
        - Prediction point: not stated. The inputs (examination, blood tests, physician's prognosis) imply the patient's work-up; the UCI names file gives neither when they were recorded nor the follow-up period for death.
        - The target (2026-11-01, CLEAN-25): `class` ships its classes as words (1 means the patient died (UCI: 1 DIE, 2
          LIVE)). Binary: "Yes" is the event, the class that sorts second, so it is the metrics' positive class.
        - `physician_prognosis` (UCI: `histology`; 2026-11-10, Andrej, review issue 2): Diaconis and Efron (1983) print this column for patients 149-155 as the physician's prognosis (live or die), not a biopsy result, so we rename it. The values stay as recorded (1, 2). The UCI file codes the missing prognoses as 2 ("live"): in the 11 rows Efron and Gong (1983) print, 4 prognoses are missing and all 4 are 2. Code 1 has 7 deaths in 85 patients and code 2 has 25 in 70, which runs backwards for a prognosis, so the codes cannot be read with confidence. Reference: Diaconis P, Efron B. Computer-intensive methods in statistics. Sci Am. 1983;248(5):116-130. doi:10.1038/scientificamerican0583-116
        - The yes/no columns (2026-11-10, Andrej, review issue 3): `steroid`, `antivirals`, `fatigue`, `malaise`, `anorexia`, `liver_big`, `liver_firm`, `spleen_palpable`, `spiders`, `ascites` and `varices` are coded 1 = yes, 2 = no, as in Diaconis and Efron's table (1983), the reverse of the order the UCI names file lists ("no, yes"). For example, 14 of the 20 patients with `ascites` = 1 died, against 17 of 130 with 2. The values stay as recorded.
    """

    # Task
    target = "class"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Efron & Gong 1981/1986 study how to estimate the error rate of Gregory's logistic rule on these 155 patients: a statistics-methods paper, not a decision; 32 deaths, so accuracy is coarse. Original rejected: error rate. roc_auc is the binary fallback.",
    )

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
            "physician_prognosis",
        ]
        df = pd.read_csv(raw_dir / "hepatitis.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.replace("?", np.nan)
        as_float_type = ["age", "bilirubin", "alk_phosphate", "sgot", "albumin", "protime"]
        df[as_float_type] = df[as_float_type].astype(float)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"1": "Yes", "2": "No"}})
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
                "physician_prognosis",
            ],
        )
