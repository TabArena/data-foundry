"""Curated dataset definition for `mercedes_benz_greener_manufacturing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary, Temporal, TemporalSplits


class MercedesBenzGreenerManufacturing(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will a car with a given set of options take to pass the test bench?",
        use_case=(
            "For example, Mercedes-Benz plans its test bench by predicting how long each car configuration will take "
            "to pass testing; the competition aimed to cut the time cars spend on the bench."
        ),
        row=("One Mercedes-Benz car that passed the test bench, ordered by its ID (4,204 cars; dates not stated)."),
        predicted="The time the car took to pass testing, in seconds (72 to 170, mean about 101).",
        known=(
            "The car's options, anonymized, as three coded categories and several hundred yes/no options (the "
            "source's examples are four-wheel drive or a head-up display)."
        ),
        split=(
            "The first 1,000 cars are always in training; the rest form 9 test windows of 320 cars in ID order, each "
            "trained on all earlier cars."
        ),
        changes=(
            "We order the cars by ID and test on later ones; we drop the coded category that marks time groups, other"
            " coded categories of unknown meaning, 4 unusual rows and one outlier testing time."
        ),
        fit="approximate",
        fit_reason=(
            "The car ID stands in for the order of testing, which the source does not confirm, and without dates the "
            "time a test window spans is unknown."
        ),
    )

    # Dataset
    unique_name = "mercedes_benz_greener_manufacturing"
    year = "2017"
    domain = "industry & manufacturing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
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
        - Of the coded categories (X0-X8) we keep X0, X1 and X2, which likely use only their own row, and drop X8, whose values seem drawn from the distribution of all rows, and X3 and X6, about which nothing is known. The 0/1 options from X10 on stay, except X11, which is constant (11 other constant options, such as X93, stay).
    """

    # Task
    target = "y"
    problem_type = "regression"

    # Splits
    splits_comment = """
        This is a small temporal dataset. Thus, we could refit often and we could simulate that a model was often refit, basically, if possible, after each time_index (akin to LOO). As this would create too many splits with too small test sizes for a robust signal, we opt for less splits. Moreover, as we want to have sufficient train data signal, we start with the first 1000 samples of the data as fixed train data. The rest is than gradually split to create 9 test splits using a sklearn TimeSeriesSplit.
    """
    temporal = Temporal(
        on="time_index",
        splits=TemporalSplits(window=320, unit="rows", n_windows=9),
    )

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
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # All X features are binary/categorical
        return FeatureTypes(categorical=[c for c in df.columns if c.startswith("X")])
