"""Curated dataset definition for `student_portuguese_performance` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode

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
        predicted=(
            "The final grade, from 0 to 20 (mean 11.9); 15 students have a 0, likely students who left before the "
            "final assessment."
        ),
        known=(
            "School, sex, age, home (urban or rural, family size, parents' education, jobs and cohabitation), the "
            "reason for the school, study time, past class failures, support and paid classes, activities, plans for "
            "higher education, internet, free time, going out, alcohol and health."
        ),
        split="Random students of the same two schools.",
        changes=(
            "We drop the first- and second-period grades, so the grade is predicted from background and habits alone."
        ),
        fit="approximate",
        fit_reason=(
            "Most features are background known early, but the habits questionnaire covers the same school year as the "
            "grade, and when it was answered is not stated, so some answers may come after an early prediction "
            "point."
        ),
    )

    # Dataset
    unique_name = "student_portuguese_performance"
    domain = "education"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5TG7T",
            license="CC BY 4.0",
            year="2014",
            bibtex="""
                @article{silva2008using,
                  title={Using data mining to predict secondary school student performance},
                  author={Silva, Alice},
                  year={2008}
                }
            """,
        ),
    )
    download_description = """
        We get the portuguese data from the UCI repository. The math version is mostly duplicates from portuguese.

        wget https://archive.ics.uci.edu/static/public/320/student+performance.zip && unzip student+performance.zip student.zip && unzip student.zip student-por.csv && rm student+performance.zip student.zip
        mkdir -p local-data-warehouse/student_portuguese_performance && mv student-por.csv local-data-warehouse/student_portuguese_performance/
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
        - Time basis: DelayedTarget: one cohort, the 2005-2006 school year at two public schools of the Alentejo; the
          use case predicts early in the year from background and habits, and the target is the final grade at the
          year's end, one date closed for every student. Every student belongs to the same school year and is graded on
          the same date, so no test row is later than a training row and the random split is IID. The questionnaire's
          date in the year is not stated. Not tested: the next school year.
        - `absences` is dropped (2026-11-09, Andrej, review issue 4): the school report's count comes from after an
          early prediction point, and its zero records the outcome: all 15 students with a final grade of 0 have zero
          recorded absences, and none of the 405 students with any absence has a 0. Dropping it costs 0.004 R2 (TabPFN,
          60 splits).
        - 15 final grades of 0 (2026-11-09, Andrej, review issue 2): all with zero recorded absences, 14 at Mousinho da
          Silveira, each with a first-period grade above 0, so they likely mark students who left before the final
          assessment. Kept: the source does not say so, and students who leave are part of the support decision.
        - No class, teacher or school year is recorded (2026-11-11, Andrej, review issue 5): 649 students of one school
          year (2005-2006) at two schools (Gabriel Pereira 423, Mousinho da Silveira 226), so classmates sit on both sides
          of the random split, and a teacher's grading can reach a test student through classmates in training. How much
          cannot be measured without a class id. Kept random: the use case is a school supporting its own students, whose
          classmates it knows; two schools are too few groups for a grouped split.
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
        # absences: the school report's count, 0 for every student without a final grade (review issue 4)
        df = df.drop(columns=["G1", "G2", "absences"])
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
