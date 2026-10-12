"""Curated dataset definition for `alvin_smart_money_management_classification_challenge` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, SplitPlan, Temporal, drop_columns

TARGET = "MERCHANT_CATEGORIZED_AS"
TIME = "PURCHASED_AT"
LABEL_TIME = "MERCHANT_CATEGORIZED_AT"
"""When the category was recorded: used to build the splits, then dropped."""

RARE_CLASSES = ("Health", "Loan Repayment", "Education", "Rent / Mortgage")
"""The categories with fewer than 10 rows after deduplication (6, 5, 2 and 2 rows)."""

BUSINESS_WORDS = [
    # legal forms, banks and finance
    "LIMITED", "LTD", "PLC", "ENTERPRISE", "ENTERPRISES", "CORPORATE", "BANK", "PAYBILL", "ACCOUNT", "C2B", "CAPITAL",
    "CREDIT", "RETIREMENT", "LIFE", "NCBA", "KCB", "EQUITY",
    # telecoms, utilities, government and payment services
    "SAFARICOM", "TELKOM", "ZUKU", "KPLC", "NHIF", "KRA", "PESAPAL", "PAYTECH",
    # shops, food and drink
    "SUPERMARKET", "MART", "NAIVAS", "CARREFOUR", "TUSKYS", "SHOP", "MARKET", "BUTCHERY", "PHARMACY", "HARDWARE",
    "APPLIANCES", "JUICES", "WINES", "RESTAURANT", "CAFETERIA", "LUNCHEONETTE", "CATERERS", "PIZZA", "GRILL", "BAR",
    "TAVERN", "JAVA", "KFC",
    # fuel, parking and services
    "TOTAL", "TOTALENERGIES", "RUBIS", "SHELL", "OILIBYA", "ENERGY", "PARKING", "SERVICES", "STUDIO", "CYBER",
    "BARBERSHOP",
    # churches and associations
    "CHURCH", "OFFERING", "CITAM", "ASSOCIATION",
]  # fmt: skip
"""Whole words that mark a payee name as a business."""

BUSINESS_PAYEES = frozenset({
    "ASL TD", "CAPTURE ADVENTURES", "CRAFT - CHUPA CHAP", "FISH BAY", "GALITOS BELLEVUE", "GREAT IMPACT",
    "KILELESHWA SUPERSHINE", "LANGATA CREAMY", "MAMBO ITALIA-LAVINGTON", "OAKS  CORKS - ONLINE", "OUTSKIRTS PLACE",
    "OWETTE DISHES", "PARK N GO", "POA", "REPUBLIQOUR HUB", "SKY-GARDEN", "THE ORIGINS",
})  # fmt: skip
"""The business payees of Train.csv whose name holds none of the business words."""

_BUSINESS = re.compile(r"\b(?:" + "|".join(BUSINESS_WORDS) + r")\b")

PRIVATE_PERSON = "private person"
"""The placeholder for a payee who is a private person."""

WINDOW_DAYS = 21
N_WINDOWS = 3


def _is_business(name: str) -> bool:
    """Whether a payee is a business: its name holds a business word or is a listed business. Every other payee of
    Train.csv is a private person (checked by reading all 218 names).
    """
    return bool(_BUSINESS.search(name)) or name in BUSINESS_PAYEES


def _windows(purchased: pd.Series) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """The test windows ``[start, stop)``, newest first: 21 days each, back from the day after the newest purchase."""
    end = purchased.max().normalize() + pd.Timedelta(days=1)
    return [
        (end - pd.Timedelta(days=WINDOW_DAYS * (k + 1)), end - pd.Timedelta(days=WINDOW_DAYS * k))
        for k in range(N_WINDOWS)
    ]


class AlvinSmartMoneyManagementClassificationChallenge(AbstractCuratedDataset):
    # Dataset
    unique_name = "alvin_smart_money_management_classification_challenge"
    year = "2022"
    domain = "finance"
    source = "Zindi"
    source_url = "https://zindi.africa/competitions/alvin-smart-money-management-classification-challenge/data"
    license = "Zindi Competition Rules"
    download_description = """
        Train.csv of the Zindi competition "Alvin Smart Money Management Classification Challenge" (2022). Zindi needs a
        login, so we take the copy in the GitHub repository The-Fantastics/Alvin-Smart-Money-Management-Classification-
        Challenge-Data (commit 65a25f5, 2022-07-01, during the competition). Its five data files have the byte sizes the
        Zindi API lists for the competition's files (Train.csv: 49,789 bytes, sha256
        12b4293e6e5f1cbc615a3ced3807e86304ddd9371abdbe66c10abf1ef4c10b13; 373 rows and a header). Two other uploads hold
        byte-identical files: the GitHub repository emms204/Alvin-Smart-Money-Management-Classification-Challenge and the
        Kaggle dataset harshbansal27/alvin-smart-money-management (versions 1 and 2). Only Train.csv is read;
        VariableDefinitions.csv is the codebook. Test.csv has no labels, and extra_data.csv has no labels either.

        mkdir -p local-data-warehouse/alvin_smart_money_management_classification_challenge
        cd local-data-warehouse/alvin_smart_money_management_classification_challenge
        BASE=https://raw.githubusercontent.com/The-Fantastics/Alvin-Smart-Money-Management-Classification-Challenge-Data/65a25f550a011b37aba02f69860d9fa4a0a0b758/data
        wget "$BASE/Train.csv" "$BASE/VariableDefinitions.csv"
    """
    bibtex = r"""
        @misc{zindi2022alvin,
          author = {{Zindi} and {Alvin}},
          title = {Alvin Smart Money Management Classification Challenge},
          year = {2022},
          howpublished = {\url{https://zindi.africa/competitions/alvin-smart-money-management-classification-challenge}},
          note = {Zindi competition, 22 June to 24 July 2022}
        }
    """
    curation_comments = """
        We start with Train.csv of the Zindi competition Alvin Smart Money Management Classification Challenge (2022): 373 purchases of 25 users of a Kenyan budgeting app, each with the category its user gave it. Test.csv (no labels) and extra_data.csv (no categories) are not used.

        - Prediction point: a purchase is recorded from its M-PESA SMS receipt, and the app proposes a category from the payee name, the amount, the purchase time, the send-money flag and the user's id and profile. The time the user's category was recorded (MERCHANT_CATEGORIZED_AT) belongs to the label, not to the purchase.
        - A purchase enters a train side only when its category was recorded before the cutoff, and MERCHANT_CATEGORIZED_AT is then dropped. Its values are batch writes that several users share to the microsecond (decision table), and without the filter the windows score better (log loss 1.316 instead of 1.483 for logistic regression), as the left-out purchases were categorised together with test purchases.
        - Split: temporal, as the record asks. The competition's random split puts the same purchase in train and test (Zindi discussion 12159), and Bills & Fees grows from 15% of the purchases before the test windows to 39% of the test purchases.
        - Duplicates: 7 purchases occur twice under two categorisation times and two transaction ids. We keep the earliest record of the 6 with one category and drop both records of the one with two.
        - Health, Loan Repayment, Education and Rent / Mortgage hold fewer than 10 rows each after deduplication and are dropped (decision table); 9 of the 13 categories remain.
        - Payees who are private persons are masked: a name that holds none of BUSINESS_WORDS and is not in BUSINESS_PAYEES becomes "private person" (checked by reading all 218 names). The send-money flag cannot replace this rule: it marks 42 business rows and misses 21 person rows. The mask costs no signal (log loss 1.483 against 1.478 with the names).
        - We drop Transaction_ID (an identifier). USER_ID stays as a categorical feature: 12 of the 25 users have purchases both before and inside the test windows, and a user's earlier categories are history the app has.
        - dtypes: MERCHANT_NAME is text; USER_GENDER and USER_ID are categorical; PURCHASED_AT is a datetime, written in UTC with a "+00" suffix that we remove.
        - Note: 18 of the 218 merchants carry more than one category, since the label is the user's choice; we keep the labels as released.
        - Note: the task is very small for a temporal split. The windows hold 36, 27 and 41 purchases, and four-week windows would leave the oldest train side 34% of the rows. Whether this is Too Small is the curator's call (record).
        - Note: Zindi's rules forbid redistributing the data, uploads to GitHub included (Rules page); the copy we download is such an upload.
    """

    # Task
    target = TARGET
    problem_type = "multiclass_classification"

    # Splits: the windows follow the purchase time; a training row also needs its category recorded before the cutoff.
    temporal = Temporal(on=TIME, horizon=WINDOW_DAYS, horizon_unit="days")
    splits_comment = """
        Expanding-window temporal splits on PURCHASED_AT: 3 test windows of 21 days walking back from the newest purchase (2022-06-06), newest first, covering 5 April to 6 June 2022. A model trained on the categories known at a cutoff proposes categories for the purchases of the next three weeks. Train holds the earlier purchases whose category was recorded before the cutoff (MERCHANT_CATEGORIZED_AT): the earlier purchases categorised after it are left out (31, 23 and 64 rows for the three windows, newest first), as their labels did not exist yet. Three-week windows keep every train side above half of the rows after that filter (the oldest 182 rows, 52%) and hold 27 to 41 test purchases; four-week windows would hold 39 to 52 but leave the oldest train side 120 rows (34%).
    """

    accepted_check_warnings = {
        "splits_rows_unused": "18 purchases (5.1%) made before the oldest window whose category was recorded on 31 May "
        "or 1 June 2022, after the newest cutoff: no window has their label at its cutoff, so they are in no split.",
        "splits_test_class_missing": "Each 21-day window lacks one of the 9 categories (Transport & Fuel, Going out, "
        "Shopping; newest first) and holds 1 to 3 rows of some others; every train side holds all 9 (Emergency fund at "
        "least 5 rows), so log loss is defined. Four-week windows would test more purchases but leave the oldest train "
        "side 34% of the rows.",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Both timestamps are written in UTC with a "+00" suffix.
        for col in (TIME, LABEL_TIME):
            df[col] = df[col].str.removesuffix("+00")
        df = drop_columns(df, ["Transaction_ID"])

        # The same purchase recorded twice: keep the earliest record of a purchase with one category, drop every
        # record of a purchase with two.
        features = [c for c in df.columns if c not in (TARGET, LABEL_TIME)]
        df = df.sort_values(LABEL_TIME, kind="stable", key=lambda s: pd.to_datetime(s, format="ISO8601"))
        df = df.drop_duplicates(subset=[*features, TARGET], keep="first")
        df = df[~df.duplicated(subset=features, keep=False)]

        # Categories with fewer than 10 rows.
        df = df[~df[TARGET].isin(RARE_CLASSES)]

        # Payees who are private persons: one placeholder instead of their names.
        names = df["MERCHANT_NAME"]
        return df.assign(MERCHANT_NAME=names.where(names.map(_is_business), PRIVATE_PERSON))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["USER_GENDER", "USER_ID"],
            string=["MERCHANT_NAME"],
            datetime={TIME: "%Y-%m-%d %H:%M:%S", LABEL_TIME: "ISO8601"},
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        purchased, recorded = df[TIME], df[LABEL_TIME]
        positions = np.arange(len(df))
        splits = {}
        for split, (start, stop) in enumerate(_windows(purchased)):
            test = positions[((purchased >= start) & (purchased < stop)).to_numpy()]
            # Only purchases whose category was recorded before the cutoff: the others had no label yet.
            train = positions[((purchased < start) & (recorded < start)).to_numpy()]
            splits[split] = {0: (train.tolist(), test.tolist())}
        return SplitPlan(splits=splits, df=df.drop(columns=[LABEL_TIME]))

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        frame = self.df  # the curated frame still holds the categorisation time, which the splits drop
        purchased, recorded = frame[TIME], frame[LABEL_TIME]
        windows = []
        for split, (start, stop) in enumerate(_windows(purchased)):
            test = (purchased >= start) & (purchased < stop)
            earlier = purchased < start
            windows.append(
                {
                    "split": split,
                    "test window": f"{start.date()} to {(stop - pd.Timedelta(days=1)).date()}",
                    "test rows": int(test.sum()),
                    "categories in test": int(frame.loc[test, TARGET].nunique()),
                    "earlier purchases": int(earlier.sum()),
                    "train rows (category recorded before the cutoff)": int((earlier & (recorded < start)).sum()),
                    "left out (category recorded later)": int((earlier & (recorded >= start)).sum()),
                }
            )

        batches = pd.to_datetime(raw[LABEL_TIME].str.removesuffix("+00"), format="ISO8601")
        per_batch = (
            raw.assign(recorded=batches)
            .groupby("recorded")
            .agg(
                purchases=("Transaction_ID", "size"),
                users=("USER_ID", "nunique"),
                merchants=("MERCHANT_NAME", "nunique"),
            )
            .sort_values("purchases", ascending=False, kind="stable")
            .head(8)
        )

        raw_kind = raw["MERCHANT_NAME"].map(_is_business).map({True: "business", False: PRIVATE_PERSON})
        kind = df["MERCHANT_NAME"].eq(PRIVATE_PERSON).map({True: PRIVATE_PERSON, False: "business"})
        send_money = "IS_PURCHASE_PAID_VIA_MPESA_SEND_MONEY"
        payees = (
            pd.DataFrame(
                {
                    "payee names in Train.csv": raw.groupby(raw_kind)["MERCHANT_NAME"].nunique(),
                    "purchases in Train.csv": raw.groupby(raw_kind).size(),
                    "of them paid with send money": raw.groupby(raw_kind)[send_money].sum(),
                    "purchases shipped": df.groupby(kind).size(),
                    "of them paid with send money (shipped)": df.groupby(kind)[send_money].sum(),
                }
            )
            .astype(int)
            .rename_axis("payee")
        )

        counts = (
            pd.DataFrame({"rows in Train.csv": raw[TARGET].value_counts(), "rows shipped": df[TARGET].value_counts()})
            .fillna(0)
            .astype(int)
            .sort_values("rows in Train.csv", ascending=False, kind="stable")
        )
        return [
            Decision(
                "Train only on purchases whose category was recorded before the cutoff",
                "The test windows follow the purchase time. An earlier purchase whose category was recorded after the "
                "cutoff had no label at the cutoff, so it is in no train side of that window.",
                pd.DataFrame(windows).set_index("split"),
            ),
            Decision(
                "MERCHANT_CATEGORIZED_AT is a batch write, not a feature",
                "Several users share one categorisation time to the microsecond, so it records when a batch of "
                "categories was written. It is used to filter the training rows and then dropped. The largest batches "
                "of Train.csv:",
                per_batch,
            ),
            Decision(
                "Payees who are private persons are masked",
                "A payee is a business when its name holds a business word or is one of the listed businesses; every "
                "other payee is a private person and its name becomes one placeholder. The send-money flag alone would "
                "miss the persons paid otherwise and mark the businesses paid with send money.",
                payees,
            ),
            Decision(
                "Categories with fewer than 10 rows are dropped",
                "Rows per category in Train.csv and after deduplication and the drop.",
                counts,
            ),
        ]
