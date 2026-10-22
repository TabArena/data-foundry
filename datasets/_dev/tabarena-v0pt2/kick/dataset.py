"""Curated dataset definition for `kick` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)


class Kick(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question='Is a used car bought at auction a "kick", a purchase with serious problems?',
        use_case=(
            "A used-car dealer decides at the auction whether to buy a car, avoiding cars that would have to be "
            "returned or resold at a loss."
        ),
        row="One car bought at a US auction in 2009-2010.",
        predicted="Whether the purchase turned out to be a bad buy.",
        known=(
            "The car (age, make, model, trim, mileage, colour), its auction and retail price guides, the "
            "purchase price, the auction, the buyer and the warranty cost."
        ),
        split=(
            "The test data is the most recent purchases, in nine windows of purchase dates, with every earlier "
            "purchase for training."
        ),
        changes=(
            "We split by purchase date instead of the competition's random split, in which both sides cover the same "
            "two years."
        ),
        fit="direct",
        fit_reason=(
            "The cars, the features known at the auction and the split by purchase date mirror the dealer's decision. "
            "Four fields that were filled in after the outcome (WheelType, WheelTypeID, PRIMEUNIT, AUCGUART) are "
            "dropped."
        ),
    )

    # Dataset
    unique_name = "kick"
    year = "2011"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/DontGetKicked/overview"
    license = "Public Domain"
    download_description = """
        kaggle competitions download -c dontgetkicked -p local-data-warehouse/kick
        unzip local-data-warehouse/kick/dontgetkicked.zip -d local-data-warehouse/kick/
        rm local-data-warehouse/kick/dontgetkicked.zip
    """
    bibtex = r"""
        @misc{DontGetKicked,
            author = {faysal and Will Adams and Will Cukierski},
            title = {Don't Get Kicked!},
            year = {2011},
            howpublished = {\url{https://kaggle.com/competitions/DontGetKicked}},
            note = {Kaggle}
        }
    """
    curation_comments = """
        - The data is from a Kaggle competition. Its train/test split is neither temporal nor grouped: both cover January 2009 to December 2010 (test is 36-44% of every quarter), and 78.9% of test rows are at an auction location ("Auction" + "VNZIP1") that also occurs in train (72 of 128 test locations); some locations are only in test.
        - The data is temporal and also grouped by auction location. Locations reappear over time, so a grouped split would test unseen auctions, which does not match deployment; a model is deployed on future purchases at mostly known auctions. Therefore, we use temporal evaluation.
        - The test features from the Kaggle competition are available and could be used for unsupervised approaches.
        - We transform "PurchDate" to datetime.
        - We drop the "RefId" column, as it is just an identifier and not useful for modeling.
        - We assign the categorical features "BYRNO" and "VNZIP1" to category dtype, as they are given as numbers.
        - Leak, dropped (LEAK-10; Lennart, 2026-10-22, consistent with expresso_churn_prediction's REGION): "WheelType" and "WheelTypeID" were most likely filled in after the outcome. WheelType is missing for 24.9% of bad buys and 1.5% of good ones, in every band of vehicle age, odometer and price; a model of the missingness from the auction covariates, fit on good buys, predicts 1.2% missing for the bad buys; within auction and purchase date the missing flag alone still separates bad buys (ROC AUC 0.572), while the missing flags of the other columns stay at 0.49-0.54. Its whole value is the flag: LightGBM on the 9 temporal windows (300 trees, mean ROC AUC) 0.750 with the columns, 0.677 without.
        - Leak, dropped (LEAK-10; same decision): "PRIMEUNIT" and "AUCGUART" (filled on the same rows, about 95% missing). From October 2010 they are filled for 32.7% of good buys and 7.8% of bad ones; a model of the fill from the auction covariates, fit on good buys, predicts 42.3% filled for the bad buys; within auction and purchase date the flag gives ROC AUC 0.632. These months fall in the last test windows.
        - The host's test file carries all four fields the same way (WheelType missing for 4.5% of the Kaggle test rows against 4.3% of train; PRIMEUNIT filled for 46.0% in December 2010), so the competition's task had them. We drop them anyway because that test file is a holdout from the same snapshot, taken after the outcomes; at a real auction no car has been kicked back yet. If the recording process is ever documented as known at the auction, they can come back.
    """

    # Task
    target = "IsBadBuy"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="Gini index (Kaggle normalized Gini)",
        reference="https://www.kaggle.com/competitions/DontGetKicked/overview/evaluation",
        definition="Normalized Gini = 2 x ROC AUC - 1 for a binary target; ranks models identically to ROC AUC.",
    )

    # Splits: 9 equal windows of purchase dates (the 3x3 an IID dataset of this size would get), keeping at
    # least half of all dates for training.
    temporal = Temporal(
        on="PurchDate",
        splits=TemporalSplits(window=None, unit="unique", n_windows=9, min_train_fraction=0.5),
        horizon=28,
        horizon_unit="days",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "training.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # WheelType, WheelTypeID, PRIMEUNIT and AUCGUART were filled in after the outcome (LEAK-10, notes)
        return drop_columns(raw, ["RefId", "WheelType", "WheelTypeID", "PRIMEUNIT", "AUCGUART"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=(
                # given as numbers
                "BYRNO",
                "VNZIP1",
                "Trim",
                "SubModel",
                "Color",
                "Transmission",
                "Nationality",
                "Size",
                "TopThreeAmericanName",
                "Auction",
                "Make",
                "Model",
                "VNST",
                "IsBadBuy",
                "IsOnlineSale",  # a 0/1 flag (CLEAN-14)
            ),
            datetime=("PurchDate",),
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        import matplotlib.pyplot as plt

        # An auction location is the auction plus the vehicle's ZIP code (the competition's grouping).
        location = raw["Auction"].astype(str) + raw["VNZIP1"].astype(str)
        dates_per_location = pd.to_datetime(raw["PurchDate"]).groupby(location).nunique()
        reappearing = pd.Series(
            {
                "auction locations": len(dates_per_location),
                "seen on more than one date": int((dates_per_location > 1).sum()),
                "rows at a location seen on more than one date": f"{location.map(dates_per_location).gt(1).mean():.1%}",
            },
            name="value",
        )
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.hist(dates_per_location, bins=40)
        ax.set_xlabel("distinct purchase dates per auction location")
        ax.set_ylabel("locations")
        return [
            Decision(
                "Temporal split, not grouped by auction location",
                "Auction locations (auction and ZIP code) reappear over time, so a grouped split would not match "
                "deployment; a model is deployed on future purchases.",
                reappearing,
            ),
            Decision(
                "Auction locations recur across the whole period",
                "Most locations are seen on many purchase dates, so there is no clean set of unseen locations.",
                fig,
            ),
        ]
