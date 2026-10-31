"""Curated dataset definition for `student_portuguese_performance` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Medu": [0, 1, 2, 3, 4],
    "Fedu": [0, 1, 2, 3, 4],
    "traveltime": [1, 2, 3, 4],  # open-ended
    "studytime": [1, 2, 3, 4],  # open-ended
    "failures": [0, 1, 2, 3],  # open-ended
    "famrel": [1, 2, 3, 4, 5],
    "freetime": [1, 2, 3, 4, 5],
    "goout": [1, 2, 3, 4, 5],
    "Dalc": [1, 2, 3, 4, 5],
    "Walc": [1, 2, 3, 4, 5],
    "health": [1, 2, 3, 4, 5],
}


class StudentPortuguesePerformance(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What final grade in Portuguese will a secondary-school student get?",
        use_case=(
            "For example, a school predicts each student's final Portuguese grade early in the year from background "
            "and habits, to offer extra support to those likely to fail."
        ),
        row=(
            "One student of the Portuguese-language course at two Portuguese secondary schools (649 students), from "
            "school reports and questionnaires; the school year is not stated."
        ),
        predicted="The final grade, from 0 to 20 (mean 11.9).",
        known=(
            "School, sex, age, home (urban or rural, family size, parents' education, jobs and cohabitation), the "
            "reason for the school, study time, past class failures, support and paid classes, activities, plans for "
            "higher education, internet, free time, going out, alcohol, health and school absences."
        ),
        split="Random students of the same two schools.",
        changes=(
            "We drop the first- and second-period grades, so the grade is predicted from background and habits alone."
        ),
        fit="approximate",
        fit_reason=(
            "Most features are background known early, but the absences and the habits questionnaire cover the same "
            "school year as the grade, and when they were recorded is not stated, so some may come after an early "
            "prediction point."
        ),
    )

    # Dataset
    unique_name = "student_portuguese_performance"
    year = "2014"
    domain = "education"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5TG7T"
    license = "CC BY 4.0"
    download_description = """
        We get the portuguese data from the UCI repository. The math version is mostly duplicates from portuguese.

        wget https://archive.ics.uci.edu/static/public/320/student+performance.zip && unzip student+performance.zip student.zip && unzip student.zip student-por.csv && rm student+performance.zip student.zip
        mkdir -p local-data-warehouse/student_portuguese_performance && mv student-por.csv local-data-warehouse/student_portuguese_performance/
    """
    bibtex = """
        @article{silva2008using,
          title={Using data mining to predict secondary school student performance},
          author={Silva, Alice},
          year={2008}
        }
    """
    curation_comments = """
        We use the data from UCI.

        - We drop G1 and G2 to simulate the task to predict the final grade from the base characteristic.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 11 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`); 11 of them were shipped as numbers.
    """

    # Task
    target = "G3"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="RMSE (regression setup C)",
        reference="Cortez & Silva 2008, Using data mining to predict secondary school student performance, FUBUTEC (UCI 320)",
        definition="Root mean squared error of the predicted final grade G3 (0-20); the paper's classification setups use PCC instead",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "student-por.csv", sep=";")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["G1", "G2"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "school",
                "sex",
                "address",
                "famsize",
                "Pstatus",
                "Mjob",
                "Fjob",
                "reason",
                "guardian",
                "schoolsup",
                "famsup",
                "paid",
                "activities",
                "nursery",
                "higher",
                "internet",
                "romantic",
            ],
        )
