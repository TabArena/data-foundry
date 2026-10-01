"""Curated dataset definition for `bad_customer_detection` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class BadCustomerDetection(AbstractCuratedDataset):
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
    """

    # Task
    target = "bad_customer"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "clients.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "bad_customer"
        df.rename(columns={"bad_client_target": target_feature}, inplace=True)
        df[target_feature] = df[target_feature].map({0: "No", 1: "Yes"}).astype("category")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
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
