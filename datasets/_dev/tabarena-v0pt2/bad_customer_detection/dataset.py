"""Curated dataset definition for `bad_customer_detection` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "education": [
        "Incomplete secondary education",
        "Secondary education",
        "Secondary special education",
        "Incomplete higher education",
        "Higher education",
        "PhD degree",
    ],
}


class BadCustomerDetection(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a customer who takes a consumer loan turn out to be a bad customer?",
        use_case=(
            "The source states no use case; it presents the data as an example of imbalanced classes. For example, a "
            "lender decides when an application arrives whether to grant a loan for a phone, an appliance or a "
            "service."
        ),
        row=(
            "One consumer loan, with the kind of product or service it pays for (1,723 loans; the lender, country and"
            " period are not stated)."
        ),
        predicted=(
            "Whether the customer is marked a bad client (11% are); what makes a client bad, and by when, is not "
            "stated."
        ),
        known=(
            "The loan (amount, term, a month number, the kind of product bought) and the customer (age, sex, "
            "education, income, family status, children, region, phone operator, and whether already a client)."
        ),
        split="Random loans, so the test data stands for new customers of the same lender and period.",
        fit="approximate",
        fit_reason=(
            "The features are what an application holds, but the label has no stated definition or horizon, and the "
            "source names no lender, place or period."
        ),
    )

    # Dataset
    unique_name = "bad_customer_detection"
    year = "2020"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/podsyp/is-this-a-good-customer"
    license = "Public Domain"
    download_description = """
        Download the dataset from Kaggle using the Kaggle API.

        mkdir -p local-data-warehouse/bad_customer_detection/ && cd local-data-warehouse/bad_customer_detection && kaggle datasets download podsyp/is-this-a-good-customer && unzip is-this-a-good-customer.zip && rm is-this-a-good-customer.zip && cd ../../
    """
    bibtex = """
        @misc{Podsyp2020IsThisAGoodCustomer,
          title={Is This a Good Customer?},
          author={Podsyp},
          year={2020},
          publisher={Kaggle},
          url={https://www.kaggle.com/datasets/podsyp/is-this-a-good-customer}
        }
    """
    curation_comments = """
        - We renamed the values of the target variable to be more descriptive.
        - Note: The original source of the data is still to be clarified (open item in the curation record).
        - Ordinal scales (2026-10-30, CLEAN-14): 1 columns typed as ordered categories in the order of the source's
          codebook (`ORDINAL_LEVELS`).
    """

    # Task
    target = "bad_customer"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Kaggle dataset (not a competition) with no stated task metric; the original source is unknown (open item in the record)",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "clients.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "bad_customer"
        df.rename(columns={"bad_client_target": target_feature}, inplace=True)
        df[target_feature] = df[target_feature].map({0: "No", 1: "Yes"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "sex",
                "education",
                "product_type",
                "having_children_flg",
                "region",
                "family_status",
                "phone_operator",
                "is_client",
            ],
        )
