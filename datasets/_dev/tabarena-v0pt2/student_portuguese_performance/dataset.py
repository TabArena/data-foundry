"""Curated dataset definition for `student_portuguese_performance` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, decode

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Medu": ["none", "primary education (4th grade)", "5th to 9th grade", "secondary education", "higher education"],
    "Fedu": ["none", "primary education (4th grade)", "5th to 9th grade", "secondary education", "higher education"],
    "traveltime": ["<15 min", "15 to 30 min", "30 min to 1 hour", ">1 hour"],  # open-ended
    "studytime": ["<2 hours", "2 to 5 hours", "5 to 10 hours", ">10 hours"],  # open-ended
    "failures": ["no failures", "1 failure", "2 failures", "3 or more failures"],  # open-ended
    "famsize": ["less or equal to 3", "greater than 3"],
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "Medu": {
        "0": "none",
        "1": "primary education (4th grade)",
        "2": "5th to 9th grade",
        "3": "secondary education",
        "4": "higher education",
    },
    "Fedu": {
        "0": "none",
        "1": "primary education (4th grade)",
        "2": "5th to 9th grade",
        "3": "secondary education",
        "4": "higher education",
    },
    "traveltime": {"1": "<15 min", "2": "15 to 30 min", "3": "30 min to 1 hour", "4": ">1 hour"},
    "studytime": {"1": "<2 hours", "2": "2 to 5 hours", "3": "5 to 10 hours", "4": ">10 hours"},
    "failures": {"0": "no failures", "1": "1 failure", "2": "2 failures", "3": "3 or more failures"},
    "school": {"GP": "Gabriel Pereira", "MS": "Mousinho da Silveira"},
    "address": {"U": "urban", "R": "rural"},
    "famsize": {"LE3": "less or equal to 3", "GT3": "greater than 3"},
    "Pstatus": {"T": "living together", "A": "apart"},
}


# Scores and ratings with no words per level: numbers, as the source ships them (CLEAN-14).
SCORES = ["famrel", "freetime", "goout", "Dalc", "Walc", "health"]


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
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 6 columns are ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); 6 of them decoded from the source's codes
          into its words (`CODE_LABELS`, 2026-11-01).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 6 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order; 3 unordered codes carry their words: `school`, `address`, `Pstatus`;
          6 scores with no words per level are numbers (`SCORES`): `famrel`, `freetime`, `goout`, `Dalc`, `Walc`,
          `health`.
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
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        # scores with no words per level are numbers (CLEAN-14)
        df[SCORES] = df[SCORES].astype("object").apply(pd.to_numeric)
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
