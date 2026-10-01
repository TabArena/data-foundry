"""Curated dataset definition for `online_shoppers_purchasing_intention_dataset` (data-foundry v2). Evidence: README.md."""

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
        - We keep only the sessions from June to December (6,875 of 12,330). "PageValues" is meant as a historical Google Analytics metric per page, stored and updated at regular intervals, averaged over the pages a session visits (Sakar et al. 2019, Sec. 2.1). In February, March and May, however, every one of the 560 buyers has PageValues > 0 and PageValues alone separates buyers with ROC AUC 0.974, so these values most likely include the session's own purchase (the page-value table was probably computed over that period). From June on, 27% of buyers have PageValues = 0 and its AUC is 0.814, as expected for a historical page metric. We keep PageValues and drop the early months; this cannot be proven from the data, as a change in site tracking would leave a similar pattern.
        - We drop "SpecialDay": it is non-zero only in February and May, so it is constant on the kept months.
        - We keep the IID split: each session belongs to a different user, sampled over one year (Sakar et al. 2019, Sec. 2.1), and only the month is known.
    """

    # Task
    target = "Revenue"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/online_shoppers_intention.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw[~raw["Month"].isin(["Feb", "Mar", "May"])]
        return df.drop(columns=["SpecialDay"]).reset_index(drop=True)

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
