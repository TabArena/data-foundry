"""Curated dataset definition for `healthcare_insurance_expenses` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class HealthcareInsuranceExpenses(AbstractCuratedDataset):
    # Dataset
    unique_name = "healthcare_insurance_expenses"
    year = "2023"
    domain = "medical & healthcare"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/arunjangir245/healthcare-insurance-expenses/"
    license = "Database Contents License (DbCL) v1.0"
    download_description = """
        kaggle datasets download -d arunjangir245/healthcare-insurance-expenses -p local-data-warehouse/healthcare_insurance_expenses/ --unzip
    """
    bibtex = r"""
        @misc{arunjangir2452023insurance,
          author       = {Kaggle User Arunjangir245},
          title        = {Healthcare Insurance Expenses},
          year         = {2023},
          howpublished = {\url{https://www.kaggle.com/datasets/arunjangir245/healthcare-insurance-expenses/}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = """
        - Unlike in TabArena, we log scale the target as the distribution is very skewed. This is a common practice for price-related targets.
    """

    # Task
    target = "charges"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/insurance.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df[self.task_metadata.target_column_name] = np.log(df[self.task_metadata.target_column_name])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "sex",
                "smoker",
                "region",
            ],
        )
