"""Curated dataset definition for `fiat_500` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class Fiat500(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="At what price is a used Fiat 500 listed?",
        use_case=(
            "For example, a seller in Italy sets the asking price of a used Fiat 500, or a buyer checks whether a "
            "listing is overpriced, by comparison with current listings."
        ),
        row=(
            "One used Fiat 500 listed on the Italian site automobile.it (1,538 listings, uploaded to Kaggle in 2020; "
            "the date of the crawl is not stated)."
        ),
        predicted="The listed price, from 2,500 to 11,100; the currency is not stated.",
        known=(
            "The trim (lounge, pop or sport), engine power, age in days, mileage, number of previous owners, and the "
            "location as latitude and longitude."
        ),
        split="Random listings of the same crawl, standing for new listings in the same market.",
        fit="direct",
        fit_reason=(
            "The features are what a listing shows, and a held-out listing is a car to price. The target is the "
            "asking price, not the sale price, and the listings come from one crawl."
        ),
    )

    # Dataset
    unique_name = "fiat_500"
    year = "2020"
    domain = "technology & internet"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows"
    license = "CC0: Public Domain"
    download_description = """
        kaggle datasets download paolocons/another-fiat-500-dataset-1538-rows -p local-data-warehouse/fiat_500/ && unzip local-data-warehouse/fiat_500/another-fiat-500-dataset-1538-rows.zip -d local-data-warehouse/fiat_500/ && rm local-data-warehouse/fiat_500/another-fiat-500-dataset-1538-rows.zip
    """
    bibtex = r"""
        @misc{paolocons2020fiat,
          author       = {Kaggle User Paolocons},
          title        = {Another Dataset on Used Fiat 500 (1538 Rows)},
          year         = {2020},
          howpublished = {\url{https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows}},
          note         = {Kaggle dataset},
        }
    """
    curation_comments = """
        We start with automobile_dot_it_used_fiat_500_in_Italy_dataset_filtered.csv from Kaggle and use it as is.

        - One row is one used Fiat 500 listed for sale in Italy, from "a query done on an website specialized in used cars" (data card); the file name names automobile.it. The target is the listed price.
        - Currency: not stated.
        - Crawl date: not stated. The file was uploaded on 2020-04-07, and age_in_days counts "from the time the dataset has been created" (data card).
        - Filter: not stated. The file name ends in "_filtered", but neither the data card nor the author's notebooks say what was removed.
    """

    # Task
    target = "price"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/automobile_dot_it_used_fiat_500_in_Italy_dataset_filtered.csv")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "model",
            ],
        )
