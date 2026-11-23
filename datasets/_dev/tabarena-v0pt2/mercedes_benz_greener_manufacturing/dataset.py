"""Curated dataset definition for `mercedes_benz_greener_manufacturing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, Temporal, TemporalSplits


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
            "The car's options, anonymized, as six coded categories and several hundred yes/no options (the "
            "source's examples are four-wheel drive or a head-up display)."
        ),
        split=(
            "The newest 2,097 cars form 9 test windows of 233 cars in ID order, each trained on all earlier cars: "
            "the newest on 3,971 cars (94%), the oldest on 2,107 (50%)."
        ),
        changes=(
            "We order the cars by ID and test on later ones; we drop the coded category that marks time groups, a "
            "near-constant coded category with its 4 unusual rows, and one outlier testing time."
        ),
        fit="approximate",
        fit_reason=(
            "The car ID stands in for the order of testing, which the source does not confirm, and without dates the "
            "time a test window spans is unknown."
        ),
    )

    # Dataset
    unique_name = "mercedes_benz_greener_manufacturing"
    domain = "industry & manufacturing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing",
            license="Kaggle Competition Rules",
            year="2017",
            bibtex=r"""
                @misc{Novy2017MercedesBenzGreenerManufacturing,
                  author = {Alexander Novy and CH1Mercedes and Christian Drescher and Christian Pfaundler and KOESIM and Will Cukierski},
                  title  = {Mercedes-Benz Greener Manufacturing},
                  year   = {2017},
                  howpublished = {\url{https://kaggle.com/competitions/mercedes-benz-greener-manufacturing}},
                  note   = {Kaggle competition}
                }
            """,
        ),
    )
    data_tags = ("Anonymized",)
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c mercedes-benz-greener-manufacturing -f train.csv.zip && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/mercedes_benz_greener_manufacturing && mv train.csv local-data-warehouse/mercedes_benz_greener_manufacturing/
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized, so feature meanings are unknown.
        - There is generally weird behavior related to the ID and potentially a time column (see X5 here https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing/discussion/34949). However, it is hard to parse the exact details due to anonymization. We generally take from this that the data is sorted sequentially by ID and that there may be time dependencies. Also checkout https://www.kaggle.com/code/sudalairajkumar/simple-exploration-notebook-mercedes which shows relation between index and y, showing that y goes up with higher index and it shows that X5 (the time group feature), has the highest importance. Plus, it has one outlier.
        - We remove the one outlier from y.
          Why it may leave (CLEAN-11, amended 2026-10-21): it is a single extreme target in the training period only. The car took 265.3 s against a next highest of 169.9 s (mean 100.7 s, sd 12.7 s), and it is car 883 of 4,209 in ID order, among the oldest cars that every test window trains on (the oldest window trains on the first 2,107 cars of the cleaned data). The competition host does not name the row; it leaves as the field's expert default for a single extreme testing time (CLEAN-11 allows the source's words or the experts' default, case by case; Lennart, 2026-10-21).
        - We drop X5 as it leaks time group information in temporal splits (besides having a full categorical-value distribution shift with a temporal split).
        - We tread the ID as a time_index.
        - There are exactly 4 rows that have value that is not equal to "d" in column "X4". This indicates some kind of sub-group or data different. Given the lack of semantics and anonymity, we cannot parse the meaning of "X4". Thus, to avoid this being an indicator of data leakage, we remove these rows and subsequently drop "X4" as well.
        - Of the coded categories (X0-X8) we keep X0, X1, X2, X3, X6 and X8 and drop only X5 (time marker) and X4 (near constant). X3, X6 and X8 were once dropped "to be safe"; a check on the competition's file (2026-11-06) found no time pattern in them: their link to the ID decile (Cramér's V, shuffled IDs in brackets) is X3 0.176 (0.047), X6 0.055 (0.050), X8 0.086 (0.076), close to the kept X0 to X2 (0.108 to 0.138 against 0.078 to 0.106), against X5 0.928 (0.080); no level of the three is confined to a part of the ID range, and each X8 level spans the IDs from the first to the last hundred. Adding them changed the R² of untuned LightGBM by +0.0015 (standard error 0.0039) over the 9 windows of 320 cars then shipped, so they stay as columns of the car's configuration (columns leave for what they are, not for being unexplained; Andrej, 2026-11-11). The 0/1 options from X10 on stay, except X11, which is constant (11 other constant options, such as X93, stay).
    """

    # Task
    target = "y"
    problem_type = "regression"
    metric = Metric.source(
        "r2",
        original="R^2 score (coefficient of determination)",
        reference="https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing/overview/evaluation",
        definition="Coefficient of determination of the test time y",
    )

    # Splits
    splits_comment = """
        The car ID is the only order: the competition ships no dates, does not confirm that the IDs follow the order of testing, and held out its own test cars at random. Each test window is a run of 233 consecutive cars in ID order, trained on every earlier car (Andrej, 2026-11-19). No source gives a length (the 320 cars used until then were the arithmetic of the first curation's scikit-learn TimeSeriesSplit): half the cars come before ID 4,230, so nine windows, the count an IID task of this size gets (3 x 3), all train on half the cars or more only at 233 cars each, which fill the newest half (2,097 test cars). The windows walk back from the newest; with no dates there is no season or period to choose between. Newest first, they test the cars with IDs 7,973-8,417, 7,499-7,972, 7,005-7,498, 6,539-7,004, 6,111-6,538, 5,630-6,103, 5,163-5,627, 4,701-5,162 and 4,230-4,699, 233 each. Train is every earlier car: 3,971, 3,738, 3,505, 3,272, 3,039, 2,806, 2,573, 2,340 and 2,107 cars (94.5%, 88.9%, 83.4%, 77.8%, 72.3%, 66.8%, 61.2%, 55.7% and 50.1%). No gap is needed: a car's testing time is known when it leaves the bench, and no row carries a date to measure a longer delay.
        How the data arrives (Andrej, 2026-11-06): the bench time is known when the car leaves the bench, minutes after its configuration is fixed, so a model refit at a window's start knows every earlier car. The ID is taken as the testing order; the dropped code X5 forms 29 levels in 31 contiguous runs of IDs, about 200 cars each in this file, likely production periods. A window's first cars share their block with the newest training cars, but the block explains about 1% of the variance of the bench time (block means 96.1 to 102.6 s). A configuration tested again (15% to 27% of a window's test cars, with the six coded categories kept) is the car's known history, not a leak.
    """
    split_leaf = "L-ORDER.windows"
    temporal = Temporal(
        on="time_index",
        splits=TemporalSplits(window=233, unit="rows", n_windows=9),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Remove on huge y outlier that seems like a clear shift case
        df = df[df["y"] < 180]
        # Handle constructed features: ['X0', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X8']
        #   - X0,X1,X2 likely only use information per row
        #   - X4 has 4 rows that are not "d", we drop these rows to avoid leakage and later drop X4
        #   - X5, time group feature that leaks group time info in temporal splits
        #   - X3, X6, X8 stay: a check found no time pattern in them (see curation_comments)
        #   - We drop X11 as it is a constant feature after preprocessing.
        df = df[df["X4"] == "d"]
        df = df.drop(columns=["X5", "X4", "X11"])
        df = df.rename(columns={"ID": "time_index"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # All X features are binary/categorical
        return FeatureTypes(categorical=[c for c in df.columns if c.startswith("X")])
