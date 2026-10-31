"""Curated dataset definition for `hotel_booking_demand` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, SplitPlan, TaskSummary, Temporal

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "DepositType": ["No Deposit     ", "Refundable     ", "Non Refund     "],
    "Meal": ["SC       ", "BB       ", "HB       ", "FB       "],
    "ArrivalDateMonth": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
}


class HotelBookingDemand(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a booking that arrives in the next three months be cancelled?",
        use_case=(
            "For example, on the first of each month a hotel's revenue manager estimates which bookings arriving in "
            "the next three months will be cancelled, to set overbooking and forecast occupancy."
        ),
        row=(
            "One booking at a resort hotel or a city hotel in Portugal, arrivals from July 2015 to August 2017; "
            "repeated records and same-day bookings are removed."
        ),
        predicted=(
            "Whether the booking is cancelled (29% of all bookings, 12.5% of the test bookings of the newest split)."
        ),
        known=(
            "The booking: hotel, booking and arrival dates, nights, guests, meal plan, country, market segment, "
            "channel, agent or company, room type, deposit type, customer type, daily rate, special requests, days on"
            " the waiting list, and the guest's earlier bookings and cancellations."
        ),
        split=(
            "Nine prediction dates, the first of each month from September 2016 to May 2017. The test data is the "
            "bookings made by then that arrive within three months and are not yet cancelled; training is the "
            "bookings that arrived before the date."
        ),
        changes=(
            "Training holds only bookings that arrived before the prediction date (the future bookings known then are"
            " all cancelled) and none cancelled over three months ahead; we drop fields recorded up to check-in "
            "(booking changes, assigned room, parking)."
        ),
        fit="approximate",
        fit_reason=(
            "The values are a snapshot of the day before arrival, up to three months after the prediction date, so "
            "changes made in between may remain; the hotels often learn the country only at check-in."
        ),
    )

    # Dataset
    unique_name = "hotel_booking_demand"
    year = "2018"
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
        - Training holds only bookings that arrived before the prediction point. Future bookings already cancelled at that point are left out: the future bookings known then are all cancelled ones, so they would teach "future arrival = cancelled" (see the splits comment).
        - After splitting, we remove "ReservationStatus" and "ReservationStatusDate" to avoid data leakage.
        - Anomaly: The first recorded month for the city hotels shows an unusually high amount of cancellations.
        - Cancellations rise over the period (from the v1 exploration, counted 2026-10-22 on the cleaned data, by arrival year): city 23.5% (2015, from July), 30.3% (2016), 35.1% (2017, to August); resort 20.7%, 23.7%, 30.3%, with a summer peak (resort 31-38% in July-August 2016 and 2017). The city anomaly above is July 2015 with 61% cancelled. LeadTime has a long tail: median 57 days, p90 209, max 737.
        - ReservationStatus equals the target (Canceled or No-Show for every cancelled booking, Check-Out for every other one), and ReservationStatusDate tells it too: every booking whose last status change is after the arrival date was not cancelled (57,364), every one changed before arrival was (22,250; median 41 days before arrival, 28% more than 90 days before). Both are dropped after splitting (from the v1 exploration, counted 2026-10-22).
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 3 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`); 1 are calendar or compass cycles, in their usual order
          (the wrap is not shown); 1 hold a state outside the scale, placed by the curator's rule (missing when the
          column has no other missing value, else the lowest level; a state that is simply not on the scale, such as
          Other, is missing).
    """

    # Task
    target = "IsCanceled"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="The data paper publishes the data without a prediction task or metric; the authors' earlier cancellation-prediction papers used other (non-public) data and reported several metrics (accuracy, precision, AUC), none set as the task's metric.",
    )

    # Splits
    splits_comment = r"""
        To define train/test splits, we define 9 points in time each starting on the 1st of a month. Using the available time stamps we separate bookings that lie in the future, and were not canceled yet as the test data. \
            To account for the fact that, the available bookings suddenly stop at the latest month, the latest prediction point is set to three months before the end of the recorded period. This is necessary to avoid an unrealistic distribution shift in the test data, as the later prediction points don't include bookings  for later time points that would typically be available. \
            To make sure that the training data reflects the forecasting horizon, we remove all historical bookings that were canceled more than three months in advance. Note that we made this choice based on assumptions without actually testing the impact of this decision. It would be interesting to test the impact of this decision on prediction performance. \
            Training data holds only bookings that arrive before the prediction point. Bookings with a future arrival that were already cancelled at the prediction point are left out: the future bookings known at that point are only the cancelled ones, so they taught "arrival in the test window = cancelled" (100% of 867 such rows on the newest split, against 12.5% cancelled in the test set; leak audit 2026-09-24 and an independent probe, 2026-08-20). \
            We drop BookingChanges, AssignedRoomType and RequiredCarParkingSpaces: per the data paper (Antonio et al. 2019, Table 1) they are recorded until check-in or cancellation, and no cancelled booking has a parking space. Note that the data paper takes every variable as of "the day prior to each booking's arrival", later than our prediction point (up to three months before arrival), so small post-prediction changes may remain in other columns.
    """
    temporal = Temporal(
        on="arrival_date",
        horizon=3,
        horizon_unit="months",
    )
    accepted_check_warnings = {
        "dataset_duplicate_rows": "Rows identical after dropping the post-outcome columns are separate bookings with "
        "the same attributes (e.g. several rooms of one group); exact source duplicates were already removed.",
        "splits_rows_unused": "By design: each prediction point uses bookings made before it; rows outside every "
        "window (e.g. bookings cancelled more than three months ahead) are in no split.",
    }

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
        # Drop all duplicates
        df = df.drop_duplicates().reset_index(drop=True)
        df = df.loc[df["LeadTime"] > 0].reset_index(drop=True)
        # Create booking date column
        df["booking_date"] = df["arrival_date"] - pd.to_timedelta(df["LeadTime"], unit="d")
        # Recorded after the prediction point (Antonio et al. 2019, Table 1): changes "until the moment of check-in or
        # cancellation", the room assigned by hotel operations, and parking spaces (never > 0 for a cancelled booking)
        df = df.drop(columns=["BookingChanges", "AssignedRoomType", "RequiredCarParkingSpaces"])
        for col in ["Agent", "Company"]:  # "NULL" (space-padded) means no agent / no company
            df[col] = df[col].astype(str).str.strip().replace("NULL", np.nan)
        # the paper: "Undefined/SC - no meal package": one level
        df["Meal"] = df["Meal"].replace({"Undefined": "SC       "})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "Country",
                "ArrivalDateMonth",
                "Meal",
                "MarketSegment",
                "DistributionChannel",
                "ReservedRoomType",
                "DepositType",
                "Agent",
                "Company",
                "CustomerType",
                "ReservationStatus",
                "hotel",
                "IsRepeatedGuest",  # a 0/1 flag (CLEAN-14)
            ],
            datetime=["arrival_date", "ReservationStatusDate", "booking_date"],
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        date_col = self.task_metadata.time_on
        target_col = self.task_metadata.target_column_name

        df = df.sort_values(by=date_col, kind="stable").reset_index(drop=True)

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

            # Remove all cancelations from the test data that were made prior to the prediction point (training leaves
            # them out too, see c).
            test_df = test_df.loc[test_df["ReservationStatusDate"] > pred_date]

            # c) Define the train set.
            # We use all remaining data as training data.
            train_df = df_use.drop(test_df.index)
            # Only bookings whose arrival lies before the prediction point: a future booking is known to be cancelled
            # at pred_date only if it was cancelled, so keeping them makes "future arrival = cancelled" a pure rule
            train_df = train_df.loc[train_df["arrival_date"] < pred_date]

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

        # After splitting, drop the outcome columns (their date is the cancellation or check-out date)
        return SplitPlan(splits=splits, df=df.drop(columns=["ReservationStatusDate", "ReservationStatus"]))
