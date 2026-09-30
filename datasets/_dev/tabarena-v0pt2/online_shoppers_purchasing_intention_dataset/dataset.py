"""Curated dataset definition for `online_shoppers_purchasing_intention_dataset` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class OnlineShoppersPurchasingIntentionDataset(AbstractCuratedDataset):
    # Dataset
    unique_name = "online_shoppers_purchasing_intention_dataset"
    year = "2017"
    domain = "business & marketing"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5F88Q"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/online_shoppers_purchasing_intention_dataset/ && wget -P local-data-warehouse/online_shoppers_purchasing_intention_dataset/ http://archive.ics.uci.edu/static/public/468/online+shoppers+purchasing+intention+dataset.zip && unzip local-data-warehouse/online_shoppers_purchasing_intention_dataset/online+shoppers+purchasing+intention+dataset.zip -d local-data-warehouse/online_shoppers_purchasing_intention_dataset/ && rm local-data-warehouse/online_shoppers_purchasing_intention_dataset/online+shoppers+purchasing+intention+dataset.zip
    """
    bibtex = """
        @article{sakar2019real,
          title={Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM recurrent neural networks},
          author={Sakar, C Okan and Polat, S Olcay and Katircioglu, Mete and Kastro, Yomi},
          journal={Neural Computing and Applications},
          volume={31},
          number={10},
          pages={6893--6908},
          year={2019},
          publisher={Springer}
        }
    """
    curation_comments = """
        - Anomaly: the data contains time-based features that were preprocessed to create a time-invariant predictive task.
    """

    # Task
    target = "Revenue"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/online_shoppers_intention.csv")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Month",
                "OperatingSystems",
                "Browser",
                "Region",
                "TrafficType",
                "VisitorType",
                "Weekend",
            ],
        )
