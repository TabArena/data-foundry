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
            "The newest 2,880 cars form 9 test windows of 320 cars in ID order, each trained on all earlier cars: "
            "the newest on 3,884 cars (92%), the oldest on 1,324 (32%); the three oldest train on less than half the "
            "cars."
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
          Why it may leave (CLEAN-11, amended 2026-10-21): it is a single extreme target in the training period only. The car took 265.3 s against a next highest of 169.9 s (mean 100.7 s, sd 12.7 s), and it is car 883 of 4,209 in ID order, among the oldest cars that every test window trains on (the oldest window trains on the first 1,324 cars of the cleaned data). The competition host does not name the row; it leaves as the field's expert default for a single extreme testing time (CLEAN-11 allows the source's words or the experts' default, case by case; Lennart, 2026-10-21).
        - We drop X5 as it leaks time group information in temporal splits (besides having a full categorical-value distribution shift with a temporal split).
        - We tread the ID as a time_index.
        - There are exactly 4 rows that have value that is not equal to "d" in column "X4". This indicates some kind of sub-group or data different. Given the lack of semantics and anonymity, we cannot parse the meaning of "X4". Thus, to avoid this being an indicator of data leakage, we remove these rows and subsequently drop "X4" as well.
        - Of the coded categories (X0-X8) we keep X0, X1, X2, X3, X6 and X8 and drop only X5 (time marker) and X4 (near constant). X3, X6 and X8 were once dropped "to be safe"; a check on the competition's file (2026-11-06) found no time pattern in them: their link to the ID decile (Cramér's V, shuffled IDs in brackets) is X3 0.176 (0.047), X6 0.055 (0.050), X8 0.086 (0.076), close to the kept X0 to X2 (0.108 to 0.138 against 0.078 to 0.106), against X5 0.928 (0.080); no level of the three is confined to a part of the ID range, and each X8 level spans the IDs from the first to the last hundred. Adding them changed the R² of untuned LightGBM by +0.0015 (standard error 0.0039) over the 9 windows then shipped, so they stay as columns of the car's configuration (columns leave for what they are, not for being unexplained; Andrej, 2026-11-11). The 0/1 options from X10 on stay, except X11, which is constant (11 other constant options, such as X93, stay).
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
        The car ID is the only order: the competition ships no dates, does not confirm that the IDs follow the order of testing, and held out its own test cars at random. Each test window is a run of 320 consecutive cars in ID order, trained on every earlier car. No source gives a length: 320 is the arithmetic of the first curation's scikit-learn TimeSeriesSplit (the cars after the first 1,000, cut into ten parts), and it is kept (CC 2026-11-11) because the floor admits nine windows of 320, which test 2,880 cars, against 2,097 for nine windows of 233 cars over the newest half; nine is the count an IID task of this size gets (3 x 3). The windows walk back from the newest; with no dates there is no season or period to choose between. Newest first, they test the cars with IDs 7,801-8,417, 7,140-7,798, 6,487-7,139, 5,875-6,486, 5,223-5,873, 4,581-5,221, 3,920-4,579, 3,308-3,919 and 2,628-3,306, 320 each. Train is every earlier car: 3,884, 3,564, 3,244, 2,924, 2,604, 2,284, 1,964, 1,644 and 1,324 cars (92.4%, 84.8%, 77.2%, 69.6%, 61.9%, 54.3%, 46.7%, 39.1% and 31.5%). The three oldest windows train on less than half the cars: IDs 3,920-4,579 (46.7%), 3,308-3,919 (39.1%) and 2,628-3,306 (31.5%); the six newest train on half or more. No gap is needed: a car's testing time is known when it leaves the bench, and no row carries a date to measure a longer delay.
    """
    temporal = Temporal(
        on="time_index",
        splits=TemporalSplits(window=320, unit="rows", n_windows=9),
    )
    accepted_check_warnings = {
        "splits_train_under_half": (
            "Signed off (Lennart, 2026-11-11, review issue 1, A): the three oldest windows train on 46.7%, 39.1% "
            "and 31.5% of the cars, beside six on 54.3% to 92.4%; SPLIT-14's two tiers admit them."
        ),
    }

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
