"""Curated dataset definition for `ljubljana_breast_cancer` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "tumor-size": ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54"],
    "inv-nodes": ["0-2", "3-5", "6-8", "9-11", "12-14", "15-17", "24-26"],
    "age": ["20-29", "30-39", "40-49", "50-59", "60-69", "70-79"],
}


# Scores and ratings with no words per level: numbers, as the source ships them (CLEAN-14).
SCORES = ["deg-malig"]


class LjubljanaBreastCancer(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a woman's breast cancer come back?",
        use_case=(
            "For example, after surgery an oncologist estimates the chance that the cancer recurs, to plan follow-up "
            "and further treatment."
        ),
        row=(
            "One breast cancer patient of the University Medical Centre, Institute of Oncology, Ljubljana (286 "
            "patients, published 1988); the period is not stated."
        ),
        predicted="Whether the cancer recurred (30% did); the source states no time window.",
        known=(
            "Age, tumour size and number of affected lymph nodes in bands, menopausal "
            "status, whether the tumour broke through a node's capsule, malignancy grade (1-3), breast and quadrant, "
            "and whether radiotherapy was given."
        ),
        split=("Random patients, so the test data stands for new patients of the same clinic and period."),
        fit="approximate",
        fit_reason=(
            "The recurrence has no stated time window, so patients followed for different times are compared. Whether"
            " radiotherapy is known at the prediction point depends on when the estimate is made."
        ),
    )

    # Dataset
    unique_name = "ljubljana_breast_cancer"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C51P4M",
            license="CC BY 4.0",
            year="1988",
            bibtex="""
                @misc{Zwitter1988BreastCancer,
                  author       = {Zwitter, Matjaz and Soklic, Milan},
                  title        = {{Breast Cancer}},
                  year         = {1988},
                  howpublished = {UCI Machine Learning Repository},
                  note         = {{DOI}: https://doi.org/10.24432/C51P4M}
                }
            """,
        ),
    )
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/14/breast+cancer.zip && unzip breast+cancer.zip breast-cancer.data && rm breast+cancer.zip && mkdir -p local-data-warehouse/ljubljana_breast_cancer && mv breast-cancer.data local-data-warehouse/ljubljana_breast_cancer/
    """
    curation_comments = """
        We start with the data from UCI.

        - We encode missing values as np.nan instead of "?".
        - Age, tumour size and the number of affected lymph nodes ship as bands ("40-49"); they are ordered categories of
          the bands (`ORDINAL_LEVELS`). Until 2026-11-01 each band was its midpoint (age 24.5 to 74.5), a number the
          source does not give (CLEAN-14, the curator's rule on bands).
        - We keep duplicates as they seem naturally occurring.
        - `deg-malig`, the degree of malignancy 1-3, has no words per level in the source: a number (`SCORES`;
          2026-11-01, CLEAN-14, the curator's rule).
    """

    # Task
    target = "Class"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Every 1986-1988 paper on the data (Michalski et al., Clark & Niblett, Cestnik et al.) reports "
            "accuracy only, without costs or a threshold; 30% recurrence on 286 rows. Original rejected: "
            "accuracy. roc_auc is the binary fallback."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "Class",
            "age",
            "menopause",
            "tumor-size",
            "inv-nodes",
            "node-caps",
            "deg-malig",
            "breast",
            "breast-quad",
            "irradiat",
        ]
        df = pd.read_csv(raw_dir / "breast-cancer.data", header=None, names=columns, na_values="?")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw

        # scores with no words per level are numbers (CLEAN-14)
        df[SCORES] = df[SCORES].astype("object").apply(pd.to_numeric)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "menopause",
                "node-caps",
                "breast",
                "breast-quad",
                "irradiat",
            ],
        )
