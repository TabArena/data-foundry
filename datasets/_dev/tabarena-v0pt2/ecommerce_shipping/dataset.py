"""Curated dataset definition for `ecommerce_shipping` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class EcommerceShipping(AbstractCuratedDataset):
    # Dataset
    unique_name = "ecommerce_shipping"
    year = "2021"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/prachi13/customer-analytics"
    license = "Public Domain"
    download_description = """
        kaggle datasets download prachi13/customer-analytics -p local-data-warehouse/ecommerce_shipping/ && unzip local-data-warehouse/ecommerce_shipping/customer-analytics.zip -d local-data-warehouse/ecommerce_shipping/ && rm local-data-warehouse/ecommerce_shipping/customer-analytics.zip
    """
    bibtex = r"""
        @misc{gopalani2021ecommerce,
          author       = {Prachi Gopalani},
          title        = {E-Commerce Shipping Data},
          year         = {2021},
          howpublished = {\url{https://www.kaggle.com/datasets/prachi13/customer-analytics}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = """
        - We dropped the ID column.
        - We renamed the target feature "Reached.on.Time_Y.N" to "ArrivedLate" and mapped binary values to "Yes"/"No".
        - Anomaly: the target and task seems somewhat disconnected from the features. Moreover, some source information on the data is missing and there might be some translation issues.
        - Anomaly: there might be some data issues related to "Warehouse_block" and the value "F" consisting of two block "E" and "F".
    """

    # Task
    target = "ArrivedLate"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/Train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "ArrivedLate"
        df = df.rename(columns={"Reached.on.Time_Y.N": target_feature})
        df = df.drop(columns=["ID"])
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Warehouse_block",
                "Mode_of_Shipment",
                "Product_importance",
                "Gender",
            ],
        )
