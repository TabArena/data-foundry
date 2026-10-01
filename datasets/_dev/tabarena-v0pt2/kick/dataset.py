"""Curated dataset definition for `kick` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TemporalSplits, drop_columns


class Kick(AbstractCuratedDataset):
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
        - We assign the categorical features "WheelTypeID", "BYRNO", and "VNZIP1" to category dtype, as they are given as numbers.
        - Potential leak, kept on purpose: missing "WheelType" may be filled in (blanked) when a car is kicked back. It is missing for about 25% of bad buys in every month but for only 1.5% of good cars, erratically (Sep-Oct 2010: 1 good vs 218 bad cars). Dropping WheelType and WheelTypeID lowers LightGBM ROC AUC on our temporal splits from 0.757 to 0.691. We keep both because this is how the company released the data for the competition (WheelType is missing in 4.5% of the Kaggle test rows vs 4.3% of train) and the field's recording process is not documented.
    """

    # Task
    target = "IsBadBuy"
    problem_type = "binary_classification"
    time_on = "PurchDate"

    # Splits: 9 equal windows of purchase dates (the 3x3 an IID dataset of this size would get), keeping at
    # least half of all dates for training.
    temporal_splits = TemporalSplits(window=None, unit="unique", n_windows=9, min_train_fraction=0.5)
    time_horizon = 28
    time_horizon_unit = "days"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "training.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        return drop_columns(raw, ["RefId"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=(
                # given as numbers
                "WheelTypeID",
                "BYRNO",
                "VNZIP1",
                "PRIMEUNIT",
                "AUCGUART",
                "WheelType",
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
