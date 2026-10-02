"""Curated dataset definition for `student_portuguese_performance` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class StudentPortuguesePerformance(AbstractCuratedDataset):
    # Dataset
    unique_name = "student_portuguese_performance"
    year = "2008"
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
    """

    # Task
    target = "G3"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "student-por.csv", sep=";")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["G1", "G2"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
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
