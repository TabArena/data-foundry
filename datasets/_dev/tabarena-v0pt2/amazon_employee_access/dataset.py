"""Curated dataset definition for `amazon_employee_access` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class AmazonEmployeeAccess(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will an employee's request for access to a company resource be granted?",
        use_case=(
            "When an Amazon employee asks for access to a computer resource, the company predicts from the employee's"
            " role whether access would be granted, to cut manual grants and revokes (the competition's stated aim)."
        ),
        row=(
            "One access request of an Amazon employee, from the competition's labelled file (32,769 requests, "
            "collected 2010-2011 as the competition states)."
        ),
        predicted="Whether the request was approved (94% were).",
        known=(
            "The requested resource, the employee's manager, and the employee's role (two levels of role grouping, "
            "department, title, role family and role code), all as anonymous codes."
        ),
        split=(
            "Random requests, so the test data stands for new requests within the same organisation; the same "
            "manager, role or resource can appear on both sides."
        ),
        fit="direct",
        fit_reason=(
            "The role and the resource are known when a request arrives, and approval is the decision to automate. "
            "The requests carry no dates, so the split cannot follow time; the competition's test held other "
            "employees."
        ),
    )

    # Dataset
    unique_name = "amazon_employee_access"
    year = "2013"
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
    metric = Metric.source(
        "roc_auc",
        original="Area Under Receiver Operating Characteristic Curve",
        reference=(
            "https://www.kaggle.com/competitions/amazon-employee-access-challenge (Kaggle API evaluationMetric)"
        ),
        definition="ROC AUC of the probability that access is approved (ACTION)",
    )

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
