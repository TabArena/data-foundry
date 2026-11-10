"""The parent of an example family: exam scores of students, one file per school (generated data).

A parent declares no `target`: it holds what every task of the family shares (the metadata, reading the raw files,
the cleaning, the column types) and is never built. Its children, `exam_scores_math` and `exam_scores_reading`, each
pick one target and one split. `examples/dataset_family.py` generates the raw files and runs the family.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, DataSummary, FeatureTypes, Source


class ExamScores(AbstractCuratedDataset):
    data_summary = DataSummary(
        data="End-of-year exam scores of students at six schools, one file per school. Generated for this example.",
        row="One student: study time, attendance, parents' education, last year's grade, and two exam scores.",
        goals=(
            "Predicting a student's exam scores from what a school knows during the year, to plan support in time; "
            "for students of a known school or of a new one."
        ),
        limits="Six schools and generated values, not real students.",
    )

    unique_name = "exam_scores"
    domain = "education"
    sources = (
        Source(
            role="publication",
            platform="GitHub",
            url="https://github.com/TabArena/data-foundry/tree/main/examples/family",
            license="Apache-2.0",
            year="2026",
            bibtex="""
                @misc{datafoundry2026examscores,
                  author = {{Data Foundry}},
                  title = {Exam scores: an example family of dataset definitions},
                  year = {2026},
                  howpublished = {\\url{https://github.com/TabArena/data-foundry/tree/main/examples/family}}
                }
            """,
        ),
    )
    download_description = """
        Generated, not downloaded: `python examples/dataset_family.py` writes one CSV per school into
        local-data-warehouse/exam_scores/ (a temporary warehouse unless $DATA_FOUNDRY_WAREHOUSE is set).
    """
    curation_comments = """
        We start with one CSV per school, named after the school.

        - The files are stacked in the order of their names; `school` comes from the file name, the key a task holds
          schools out by.
        - Both exam scores stay in the frame: each task keeps its target and drops the other, which is written at
          the same exam and not known when predicting.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        files = sorted(raw_dir.glob("*.csv"))
        return pd.concat([pd.read_csv(f).assign(school=f.stem.replace("_", " ")) for f in files], ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        return raw  # the generated files need no cleaning; a real source would be cleaned here, once for all tasks

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["school"],
            ordinal={"parents_education": ["primary", "secondary", "tertiary"]},
        )
