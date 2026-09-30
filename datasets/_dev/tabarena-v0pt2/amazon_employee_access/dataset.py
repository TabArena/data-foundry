"""Curated dataset definition for `amazon_employee_access` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class AmazonEmployeeAccess(AbstractCuratedDataset):
    # Dataset
    unique_name = "amazon_employee_access"
    year = "2010"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/c/amazon-employee-access-challenge"
    license = "Public Domain"
    download_description = """
        mkdir -p local-data-warehouse/amazon_employee_access/ && kaggle competitions download -c amazon-employee-access-challenge -f train.csv -p local-data-warehouse/amazon_employee_access/ && unzip local-data-warehouse/amazon_employee_access/train.csv.zip -d local-data-warehouse/amazon_employee_access/ && rm local-data-warehouse/amazon_employee_access/train.csv.zip
    """
    bibtex = r"""
        @misc{hamner2013amazon,
          author       = {Ben Hamner and kenmonta and Will Cukierski},
          title        = {Amazon.com - Employee Access Challenge},
          year         = {2013},
          howpublished = {\url{https://www.kaggle.com/competitions/amazon-employee-access-challenge}},
          note         = {Kaggle competition},
        }
    """
    curation_comments = """
        - We only use the training data from Kaggle.
        - We renamed the target "ACTION" to "ResourceApproved" and mapped binary values to "Yes"/"No".
        - Anomaly: the data might contain sub-groups related to managers and resources.
        - Anomaly: likely, similar to the test data, each sample represents a unique employee.
    """

    # Task
    target = "ResourceApproved"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "ResourceApproved"
        df = df.rename(columns={"ACTION": target_feature})
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "RESOURCE",
                "MGR_ID",
                "ROLE_ROLLUP_1",
                "ROLE_ROLLUP_2",
                "ROLE_DEPTNAME",
                "ROLE_TITLE",
                "ROLE_FAMILY_DESC",
                "ROLE_FAMILY",
                "ROLE_CODE",
            ],
        )
