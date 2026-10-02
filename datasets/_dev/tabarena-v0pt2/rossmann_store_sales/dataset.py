"""Curated dataset definition for `rossmann_store_sales` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Temporal, TemporalSplits


class RossmannStoreSales(AbstractCuratedDataset):
    # Dataset
    unique_name = "rossmann_store_sales"
    year = "2015"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/rossmann-store-sales/overview"
    license = "Kaggle License"
    download_description = r"""
        kaggle competitions download -c rossmann-store-sales \
        && mkdir -p local-data-warehouse/rossmann_store_sales \
        && mv rossmann-store-sales.zip local-data-warehouse/rossmann_store_sales \
        && unzip local-data-warehouse/rossmann_store_sales/rossmann-store-sales.zip -d local-data-warehouse/rossmann_store_sales \
        && rm local-data-warehouse/rossmann_store_sales/rossmann-store-sales.zip
    """
    bibtex = r"""
        @misc{kaggle_rossmann_store_sales,
            title        = {Rossmann Store Sales},
            author       = {{Kaggle}},
            howpublished = {\url{https://www.kaggle.com/competitions/rossmann-store-sales/overview}},
            note         = {Kaggle competition page. Accessed: 2026-03-19},
            year         = {2015}
        }
    """
    curation_comments = """
        - We merge the store data with the train data.
        - The data is from a Kaggle competition with a temporal split, so the test data cannot be used for unsupervised approachs.
        - The winning solution is public: https://storage.googleapis.com/kaggle-forum-message-attachments/102102/3454/Rossmann_nr1_doc.pdf.
        - The competition used 48 days for testing. The description says "Rossmann store managers are tasked with predicting their daily sales for up to six weeks in advance". Therefore, we define the same horizon for defining our test splits and add one day between train/test as a planning gap.
        - We transform the date column to datetime format.
        - We exclude days when the store is closed since they all have zero sales and are trivial to predict. We drop the Open column.
        - We assign categorical data type to the Store column and the DayOfWeek column.
        - For the train data, the # of customers per day is given, which is not available at the prediction point for the test data. The 1st-place solution says that one model variation computed recent-history features on the number of customers instead of sales, and also used store-level aggregates such as average sales per customer. However this would mean that we have to define split-specific splits. Since many high performing solutions did not utilize customer information, we drop the column.
        - The StateHoliday column has two encodings for the entry 0, one as number and one as object. We combine them into one category.
    """

    # Task
    target = "Sales"
    problem_type = "regression"

    # Splits
    splits_comment = """
        The description says 'Rossmann store managers are tasked with predicting their daily sales for up to six weeks in advance'.
        Therefore, we define the same horizon for our test splits and add one day between train/test as a planning gap.
    """
    temporal = Temporal(
        on="Date",
        splits=TemporalSplits(window=42, unit="days", n_windows=3, gap=1),
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        """NOTES:
        - We need to do some FE to make the "Customers" column useful. Test how much the full aggregated set differs from the splits.
        """
        train = pd.read_csv(raw_dir / "train.csv")
        store = pd.read_csv(raw_dir / "store.csv")
        return {"train": train, "store": store}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        train, store = raw["train"], raw["store"]
        df = pd.merge(train, store, on="Store", how="left")
        df["Date"] = pd.to_datetime(df["Date"])  # parsed here: the sort below runs on the dates
        df = df[df["Open"] == 1].copy()
        df = df.drop(columns=["Open"])
        # Drop customer information. TODO: Enable split-specific data storage and feature engineering to utilize this information.
        df = df.drop(columns=["Customers"])
        df["StateHoliday"] = df["StateHoliday"].astype(str)
        df = df.sort_values("Date", kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Store",
                "DayOfWeek",
                "StateHoliday",
                "StoreType",
                "Assortment",
                "PromoInterval",
            ],
            datetime=["Date"],
        )
