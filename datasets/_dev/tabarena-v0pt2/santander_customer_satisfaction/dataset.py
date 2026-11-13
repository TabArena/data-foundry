"""Curated dataset definition for `santander_customer_satisfaction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode


class SantanderCustomerSatisfaction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a bank customer dissatisfied?",
        use_case=(
            "Santander wants to identify dissatisfied customers early in their relationship, to act before they leave"
            " (the competition's stated aim)."
        ),
        row=("One customer of Santander bank (71,080 customers); the country and period are not stated."),
        predicted=("Whether the customer is dissatisfied (3.8% are); how and when this was measured is not stated."),
        known=(
            "About 300 anonymised numbers whose meanings are not given, plus the count of zeros in the row, which we "
            "add."
        ),
        split="Random customers, so the test data stands for other customers of the same time.",
        changes=(
            "We add the count of zeros per row, as top competition solutions did, and drop repeated rows and columns."
        ),
        fit="approximate",
        fit_reason=(
            "The label has no stated definition or horizon, and whether the anonymised features were recorded before "
            "it is not stated. The competition's winners used a random split, as here."
        ),
    )

    # Dataset
    unique_name = "santander_customer_satisfaction"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/santander-customer-satisfaction",
            license="Kaggle Competition Rules",
            year="2016",
            bibtex=r"""
                @misc{Jimenez2016SantanderCustomerSatisfaction,
                  author = {Soraya Jimenez and Will Cukierski},
                  title  = {Santander Customer Satisfaction},
                  year   = {2016},
                  howpublished = {\url{https://kaggle.com/competitions/santander-customer-satisfaction}},
                  note   = {Kaggle competition}
                }
            """,
        ),
    )
    data_tags = ("Anonymized", "Retrospective")
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c santander-customer-satisfaction -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/santander_customer_satisfaction && mv train.csv local-data-warehouse/santander_customer_satisfaction/
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - We remove duplicated columns and zero-variance columns.
        - We add a zero-count feature (number of zeros per row). #1 Kaggle experts also applied a lot of other features and feature selection but each experts used something different (https://www.kaggle.com/competitions/santander-customer-satisfaction/writeups/1-leustagos-3rd-place-solution).
        - We drop duplicates as their origin is unclear and they could create data leaks when splitting the training data.
        - We replace -999999 in var3 with with nan.
        - We keep the data otherwise as it. Several columns might be categorical and contain encoded nan values but we are not able to determine this due to anonymization.
        - The target (2026-11-01, CLEAN-25): `TARGET` ships its classes as words (1 is the event). Binary: "Yes" is the
          event, the class that sorts second, so it is the metrics' positive class.
        - Time basis: Retrospective: one extract of Santander's customers (period not stated; competition 2016), with
          windows of the last month to three months ending at it; the label is a state the host does not define or
          date, read as dissatisfaction at the extract, which the use case fills in for customers not yet known to be
          dissatisfied. No exit trace in the last month: customers whose current account emptied in the last month are
          dissatisfied at 3.1%, against 1.8% for those who kept a balance (training file). Not tested: customers of a
          later extract, or a label taken after the extract.
    """

    # Task
    target = "TARGET"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="Area Under Receiver Operating Characteristic Curve",
        reference=("https://www.kaggle.com/competitions/santander-customer-satisfaction (Kaggle API evaluationMetric)"),
        definition="Area under the ROC curve of TARGET = 1.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # remove duplicated columns
        df = df.loc[:, ~df.T.duplicated()]
        # remove zero-variance columns
        df = df.loc[:, df.nunique(dropna=False) > 1]
        # add zero-count feature
        numeric_cols = df.drop(columns=["ID", "TARGET"])
        df["zero_count"] = (numeric_cols == 0).sum(axis=1)
        df = df.drop(columns=["ID"])
        # Drop duplicates w/o target col
        df = df.drop_duplicates(subset=df.columns.difference([self.task_metadata.target_column_name]))
        # Replace -999999 with np.nan
        df["var3"] = df["var3"].replace(-999999, np.nan)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the ind_var columns are indicators by their name (0/1): categorical (CLEAN-14); the other anonymized
        # features stay numeric
        del df
        flags = [
            "ind_var1_0",
            "ind_var1",
            "ind_var5_0",
            "ind_var5",
            "ind_var6_0",
            "ind_var6",
            "ind_var8_0",
            "ind_var8",
            "ind_var12_0",
            "ind_var12",
            "ind_var13_0",
            "ind_var13_corto_0",
            "ind_var13_corto",
            "ind_var13_largo_0",
            "ind_var13_largo",
            "ind_var13_medio_0",
            "ind_var13",
            "ind_var14_0",
            "ind_var14",
            "ind_var17_0",
            "ind_var17",
            "ind_var18_0",
            "ind_var19",
            "ind_var20_0",
            "ind_var20",
            "ind_var24_0",
            "ind_var24",
            "ind_var25_cte",
            "ind_var26_0",
            "ind_var26_cte",
            "ind_var25_0",
            "ind_var30_0",
            "ind_var30",
            "ind_var31_0",
            "ind_var31",
            "ind_var32_cte",
            "ind_var32_0",
            "ind_var33_0",
            "ind_var33",
            "ind_var34_0",
            "ind_var37_cte",
            "ind_var37_0",
            "ind_var39_0",
            "ind_var40_0",
            "ind_var40",
            "ind_var41_0",
            "ind_var44_0",
            "ind_var44",
            "ind_var7_emit_ult1",
            "ind_var7_recib_ult1",
            "ind_var10_ult1",
            "ind_var10cte_ult1",
            "ind_var9_cte_ult1",
            "ind_var9_ult1",
            "ind_var43_emit_ult1",
            "ind_var43_recib_ult1",
        ]
        return FeatureTypes(categorical=flags)
