"""Curated dataset definition for `mercedes_benz_greener_manufacturing` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TemporalSplits


class MercedesBenzGreenerManufacturing(AbstractCuratedDataset):
    # Dataset
    unique_name = "mercedes_benz_greener_manufacturing"
    year = "2017"
    domain = "industry & manufacturing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing"
    license = "Kaggle Competition Rules"
    data_tags = ("Non-IID", "Anonymized")
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c mercedes-benz-greener-manufacturing -f train.csv.zip && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/mercedes_benz_greener_manufacturing && mv train.csv local-data-warehouse/mercedes_benz_greener_manufacturing/
    """
    bibtex = r"""
        @misc{Novy2017MercedesBenzGreenerManufacturing,
          author = {Alexander Novy and CH1Mercedes and Christian Drescher and Christian Pfaundler and KOESIM and Will Cukierski},
          title  = {Mercedes-Benz Greener Manufacturing},
          year   = {2017},
          howpublished = {\url{https://kaggle.com/competitions/mercedes-benz-greener-manufacturing}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - There is generally weird behavior related to the ID and potentially a time column (see X5 here https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing/discussion/34949). However, it is hard to parse the exact details due to anonymization. We generally take from this that the data is sorted sequentially by ID and that there may be time dependencies. Also checkout https://www.kaggle.com/code/sudalairajkumar/simple-exploration-notebook-mercedes which shows relation between index and y, showing that y goes up with higher index and it shows that X5 (the time group feature), has the highest importance. Plus, it has one outlier.
        - We remove the one outlier from y.
        - We drop X5 as it leaks time group information in temporal splits (besides having a full categorical-value distribution shift with a temporal split).
        - We tread the ID as a time_index.
        - Some of the other constructed features (X0-X8) may leak across time as well. We remove all of them for which we do not have an explanation from experts on Kaggle.
        - There are exactly 4 rows that have value that is not equal to "d" in column "X4". This indicates some kind of sub-group or data different. Given the lack of semantics and anonymity, we cannot parse the meaning of "X4". Thus, to avoid this being an indicator of data leakage, we remove these rows and subsequently drop "X4" as well.
        - We drop other constructed features from up to X10 for which we have no information about them and they may leak group information across rows.
    """

    # Task
    target = "y"
    problem_type = "regression"
    time_on = "time_index"

    # Splits
    splits_comment = """
        This is a small temporal dataset. Thus, we could refit often and we could simulate that a model was often refit, basically, if possible, after each time_index (akin to LOO). As this would create too many splits with too small test sizes for a robust signal, we opt for less splits. Moreover, as we want to have sufficient train data signal, we start with the first 1000 samples of the data as fixed train data. The rest is than gradually split to create 9 test splits using a sklearn TimeSeriesSplit.
    """
    time_horizon = 320
    time_horizon_unit = "steps"
    temporal_splits = TemporalSplits(window=320, unit="rows", n_windows=9)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Remove on huge y outlier that seems like a clear shift case
        df = df[df["y"] < 180]
        # Handle constructed features: ['X0', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X8']
        #   - X0,X1,X2 likely only uses information per row
        #   - X4 has 4 rows that are not "d", we drop these rows to avoid leakage and later drop X4
        #   - X5, time group feature that leaks group time info in temporal splits
        #   - X8 seems to leak group information across rows by having value assigned based on sampling from the distribution of all data, so we drop it as well
        #   - We have no further information about X3 and X6, so we drop them as well to be safe, given the trend of other constructed features leaking info across rows.
        #   - We drop X11 as it is a constant feature after preprocessing.
        df = df[df["X4"] == "d"]
        df = df.drop(columns=["X5", "X8", "X4", "X3", "X6", "X11"])
        df = df.rename(columns={"ID": "time_index"})
        # All X features are binary/categorical
        as_cat_type = [c for c in list(df) if c.startswith("X")]
        df[as_cat_type] = df[as_cat_type].astype("category")
        return df
