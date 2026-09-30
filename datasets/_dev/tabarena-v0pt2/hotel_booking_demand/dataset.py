"""Curated dataset definition for `hotel_booking_demand` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.curation_recommendations import get_recommended_splits_dimensions
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, SplitPlan


class HotelBookingDemand(AbstractCuratedDataset):
    # Dataset
    unique_name = "hotel_booking_demand"
    year = "2019"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://www.sciencedirect.com/science/article/pii/S2352340918315191#s0005"
    license = "CC BY 4.0"
    download_description = """
        mkdir -p local-data-warehouse/hotel_booking_demand
        wget -P local-data-warehouse/hotel_booking_demand/ https://ars.els-cdn.com/content/image/1-s2.0-S2352340918315191-mmc2.zip
        unzip local-data-warehouse/hotel_booking_demand/1-s2.0-S2352340918315191-mmc2.zip -d local-data-warehouse/hotel_booking_demand/
        rm local-data-warehouse/hotel_booking_demand/1-s2.0-S2352340918315191-mmc2.zip
    """
    bibtex = """
        @article{antonio2019hotel,
          title={Hotel booking demand datasets},
          author={Antonio, Nuno and de Almeida, Ana and Nunes, Luis},
          journal={Data in brief},
          volume={22},
          pages={41--49},
          year={2019},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We concatenate the two datasets H1 (resort hotels) and H2 (city hotels). We add a column "hotel" to indicate the hotel type.
        - Note: The paper shares several thoughts on data curation, looking at them can be insightful for understanding the data and its limitations.
        - We remove 26.80% duplicates from the data. It is nearly impossible that so many bookings have are booked the same time (# days) in advance on the exact same date for the exact same date. As the paper mentioned that the data was joined from multiple databases, it can be assumed that many duplicates are a data collection artifact, rather than systematic. Therefore, although some duplicates might occur realistically, we remove all duplicates to avoid data leakage.
        - We remove all bookings with a "LeadTime" of 0, assuming that bookings that are booked and canceled on the same day cannot be predicted.
        - Note: The data would allow for a second target to predict no shows.
        - We reconstruct the arrival date from the three columns "ArrivalDateYear", "ArrivalDateMonth", and "ArrivalDateDayOfMonth".
        - We create a "booking_date" column by subtracting the "LeadTime" from the "arrival_date". This is necessary to further define the prediction point in time and to filter the data to avoid data leakage.
        - To define train/test splits, we define 9 points in time each starting on the 1st of a month. Using the available time stamps we separate bookings that lie in the future, and were not canceled yet as the test data.
        - To account for the fact that, the available bookings suddenly stop at the latest month, the latest prediction point is set to three months before the end of the recorded period. This is necessary to avoid an unrealistic distribution shift in the test data, as the later prediction points don't include bookings  for later time points that would typically be available.
        - To make sure that the training data reflects the forecasting horizon, we remove all historical bookings that were canceled more than three months in advance. Note that we made this choice based on assumptions without actually testing the impact of this decision. It would be interesting to test the impact of this decision on prediction performance.
        - Bookings that have arrival dates in the future, but were already canceled at the given prediction point are included in the train data.
        - After splitting, we remove "ReservationStatus" and "ReservationStatusDate" to avoid data leakage.
        - Anomaly: The first recorded month for the city hotels shows an unusually high amount of cancellations.
    """

    # Task
    target = "IsCanceled"
    problem_type = "binary_classification"
    time_on = "arrival_date"

    # Splits
    splits_comment = r"""
        To define train/test splits, we define 9 points in time each starting on the 1st of a month. Using the available time stamps we separate bookings that lie in the future, and were not canceled yet as the test data. \
            To account for the fact that, the available bookings suddenly stop at the latest month, the latest prediction point is set to three months before the end of the recorded period. This is necessary to avoid an unrealistic distribution shift in the test data, as the later prediction points don't include bookings  for later time points that would typically be available. \
            To make sure that the training data reflects the forecasting horizon, we remove all historical bookings that were canceled more than three months in advance. Note that we made this choice based on assumptions without actually testing the impact of this decision. It would be interesting to test the impact of this decision on prediction performance. \
            Bookings that have arrival dates in the future, but were already canceled at the given prediction point are included in the train data.
    """
    time_horizon = 1
    time_horizon_unit = "months"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        h1 = pd.read_csv(raw_dir / "H1.csv")
        h2 = pd.read_csv(raw_dir / "H2.csv")
        return {"h1": h1, "h2": h2}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        h1, h2 = raw["h1"], raw["h2"]
        h1["hotel"] = "resort"
        h2["hotel"] = "city"
        # Merge data
        df = pd.concat([h1, h2], ignore_index=True).reset_index(drop=True)
        # Restore arrival date
        df["arrival_date"] = pd.to_datetime(
            df["ArrivalDateYear"].astype(str)
            + "-"
            + df["ArrivalDateMonth"]
            + "-"
            + df["ArrivalDateDayOfMonth"].astype(str)
        )
        df["ReservationStatusDate"] = pd.to_datetime(df["ReservationStatusDate"])
        # Drop all duplicates
        df = df.drop_duplicates().reset_index(drop=True)
        df = df.loc[df["LeadTime"] > 0].reset_index(drop=True)
        # Create booking date column
        df["booking_date"] = df["arrival_date"] - pd.to_timedelta(df["LeadTime"], unit="d")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Country",
                "ArrivalDateMonth",
                "Meal",
                "MarketSegment",
                "DistributionChannel",
                "ReservedRoomType",
                "AssignedRoomType",
                "DepositType",
                "Agent",
                "Company",
                "CustomerType",
                "ReservationStatus",
                "hotel",
            ],
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        n_repeats, n_splits, none_or_test_size = get_recommended_splits_dimensions(  # if the data was IID
            dataset=df,
        )
        print(f"Recommended splits: n_repeats={n_repeats}, n_splits={n_splits}, test_size={none_or_test_size}")

        df = df.drop(columns=["ReservationStatusDate", "ReservationStatus"])

        date_col = self.task_metadata.time_on
        target_col = self.task_metadata.target_column_name

        df = df.sort_values(by=date_col).reset_index(drop=True)

        # New approach: We define points in time
        test_sets_year_month = [
            # (2017, 8),
            # (2017, 7),
            # (2017, 6),
            (2017, 5),
            (2017, 4),
            (2017, 3),
            (2017, 2),
            (2017, 1),
            (2016, 12),
            (2016, 11),
            (2016, 10),
            (2016, 9),
            # (2016, 8),
            # (2016, 7),
            # (2016, 6),
            # (2016, 5),
            # (2016, 4),
            # (2016, 3),
            # (2016, 2),
            # (2016, 1)
        ]

        used_in_train = set()
        used_in_test = set()
        used_data = set()

        splits = {}
        for split, (year, month) in enumerate(test_sets_year_month):
            pred_date = pd.to_datetime(f"{year}-{month}-01")
            # a) Define the prediction point in time and filter the data accordingly to avoid data leakage.
            # Remove all bookings that were made after the chosen point (including the ones on the same day)
            df_use = df.loc[df["booking_date"] <= pred_date].copy()

            # # b) Define the test set.
            # Use all remaining bookings that have a reservation date after the chosen date as test data.
            # test_df = df_use.loc[df_use["arrival_date"]>=pred_date].copy()
            # Use all remaining bookings that have a reservation date after the chosen date, but less than three months into the future, as test data.
            test_df = df_use.loc[
                (df_use["arrival_date"] > pred_date) & (df_use["arrival_date"] < pred_date + pd.DateOffset(months=3))
            ].copy()

            # Remove all cancelations from the test data that were made prior to the prediction point and use them as train data.
            test_df = test_df.loc[test_df["ReservationStatusDate"] > pred_date]

            # c) Define the train set.
            # We use all remaining data as training data.
            train_df = df_use.drop(test_df.index)

            # d) Remove all historical bookings that were canceled more than three months in advance, to reflect our forecasting horizon.
            train_df = train_df.loc[(train_df["ReservationStatusDate"] - train_df["arrival_date"]).dt.days > -90]

            train_idx = train_df.index.tolist()
            test_idx = test_df.index.tolist()

            splits[split] = {0: [train_idx, test_idx]}

            used_in_train.update(train_idx)
            used_in_test.update(test_idx)
            used_data.update(train_idx)
            used_data.update(test_idx)

            print(f"\n=== Step {split} ===")
            print("Train size:", len(train_idx), "| Test size:", len(test_idx))
            print("Train target mean:", df.loc[train_idx, target_col].astype(int).mean())
            print("Test target mean:", df.loc[test_idx, target_col].astype(int).mean())

            assert len(set(train_idx).intersection(set(test_idx))) == 0, "Train and test indices overlap!"
            assert test_df["arrival_date"].max() < pred_date + pd.DateOffset(months=3), (
                "Test data contains bookings that are more than three months in the future!"
            )

        print(f"{len(used_data) / df.shape[0]:.4f} of the samples are used.")
        print(f"{len(used_in_train) / df.shape[0]:.4f} of the samples are used in training")
        print(f"{len(used_in_test) / df.shape[0]:.4f} of the samples are used in testing.")

        return SplitPlan(splits=splits, df=df)
