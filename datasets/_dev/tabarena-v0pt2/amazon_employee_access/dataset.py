"""Curated dataset definition for `amazon_employee_access` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary


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
            "department, title and role family), all as anonymous codes."
        ),
        split=(
            "Random requests, so the test data stands for new requests within the same organisation; the same "
            "manager, role or resource can appear on both sides."
        ),
        fit="direct",
        fit_reason=(
            "The role and the resource are known when a request arrives, and approval is the decision to automate. "
            "The requests carry no dates, so the split cannot follow time; Kaggle's test requests come from the "
            "same requesters: 88.6% from a requester profile of its training file."
        ),
    )

    # Dataset
    unique_name = "amazon_employee_access"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/c/amazon-employee-access-challenge",
            license="Public Domain",
            year="2013",
            bibtex=r"""
                @misc{hamner2013amazon,
                  author       = {Ben Hamner and kenmonta and Will Cukierski},
                  title        = {Amazon.com - Employee Access Challenge},
                  year         = {2013},
                  howpublished = {\url{https://www.kaggle.com/competitions/amazon-employee-access-challenge}},
                  note         = {Kaggle competition},
                }
            """,
        ),
    )
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        mkdir -p local-data-warehouse/amazon_employee_access/ && kaggle competitions download -c amazon-employee-access-challenge -f train.csv -p local-data-warehouse/amazon_employee_access/ && unzip local-data-warehouse/amazon_employee_access/train.csv.zip -d local-data-warehouse/amazon_employee_access/ && rm local-data-warehouse/amazon_employee_access/train.csv.zip
    """
    curation_comments = """
        - We only use the training data from Kaggle.
        - We renamed the target "ACTION" to "ResourceApproved" and mapped binary values to "Yes"/"No".
        - Anomaly: the data might contain sub-groups related to managers and resources.
        - Anomaly: likely, similar to the test data, each sample represents a unique employee.
        - We drop `ROLE_CODE`: it maps one to one onto `ROLE_TITLE` (343 values each, every title one code and every
          code one title), an exact copy of another column under other labels (Andrej, 2026-11-10).
        - Time basis: ForcedIIDFromTemporal: access requests made one by one over 2010 and 2011 (the competition's
          text); the release keeps no request date and Kaggle's training file is shuffled (denial rate flat over its
          tenths, chi-squared p = 0.45), so random requests stand in for the requests to come. UCI 216's dated access
          history uses other ids and cannot date them; a dated release would allow a split by request date.
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
        # ROLE_CODE is a one-to-one relabelling of ROLE_TITLE (343 values each)
        df = df.drop(columns=["ROLE_CODE"])
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
            ],
        )
