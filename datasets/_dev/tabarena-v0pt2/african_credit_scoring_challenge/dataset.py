"""Curated dataset definition for `african_credit_scoring_challenge` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    SplitPlan,
    TaskSummary,
    Temporal,
    drop_columns,
)

LABEL_SETTLED_DAYS = 30
"""A loan's label counts as known this many days after its due date (curation comments, "Unsettled labels")."""

N_WINDOWS = 6
"""Test windows at the end of the Type_1 lending: more would leave some with 8 default rows (splits comment)."""

WINDOW_DAYS = 7
"""The declared horizon: the test windows hold about a week of loans each (6-11 days; splits comment)."""

PRODUCT = "Type_1"
"""The one product the task keeps: one lender's 7-day loans of July to December 2022 (CC 2026-10-26)."""


def _earlier_loans(raw: dict[str, pd.DataFrame]) -> pd.Series:
    """Per loan id: the customer's loans in the release disbursed on an earlier day, any product (no label read)."""
    kenya = raw["test"][raw["test"]["country_id"] == "Kenya"]  # the competition's random 18% of the same dates
    loans = pd.concat([raw["train"], kenya]).drop_duplicates("tbl_loan_id")  # a two-lender loan has two rows
    date = pd.to_datetime(loans["disbursement_date"], format="%Y-%m-%d")
    earlier = date.groupby(loans["customer_id"]).rank(method="min") - 1
    return pd.Series(earlier.astype(int).to_numpy(), index=loans["tbl_loan_id"].to_numpy())


def _labelled_rows(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """The rows of Train.csv kept for the task, still with the loan id (`_clean` drops it)."""
    df = raw["train"].rename(columns={"target": "default"})
    df["default"] = df["default"].map({1: "Yes", 0: "No"})
    for col in ("disbursement_date", "due_date"):
        df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")
    pull = df["disbursement_date"].max()  # the data pull: the file ends with the loans of its last day

    # The customer's history at disbursement, counted before any row is dropped (curation comments)
    df["earlier_loans"] = df["tbl_loan_id"].map(_earlier_loans(raw))

    # Rows whose lender funds less than one unit of the loan are never labelled 1: they hide about 90-130 defaults
    # under the label 0 (curation comments)
    df = df[df["Amount_Funded_By_Lender"] >= 0.5].copy()

    # The main product only: one lender's 7-day loans, July to December 2022 (curation comments)
    df = df[df["loan_type"] == PRODUCT].copy()

    # One row funds more than the loan (2,627.1 of 2,249; share 1.168): its funded amount and share are unknown
    impossible = df["Amount_Funded_By_Lender"] > df["Total_Amount"]
    df.loc[impossible, ["Amount_Funded_By_Lender", "Lender_portion_Funded"]] = np.nan

    # Labels not yet settled at the data pull
    return df[df["due_date"] + pd.Timedelta(days=LABEL_SETTLED_DAYS) <= pull]


class AfricanCreditScoringChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a repeat borrower in Kenya default on a 7-day loan that has just been paid out?",
        use_case=(
            "When a 7-day loan of its main product is disbursed, a Kenyan lender scores the customer's risk of default "
            "from the loan's terms and the customer's settled earlier loans, and refits the model at least once a "
            "month on the loans whose outcome it knows."
        ),
        row=(
            "One loan of the lender's main product (Type_1, 7 days) in Kenya, July to December 2022; a loan funded "
            "together with a second lender gives two rows. 99.5% are repeat customers."
        ),
        predicted=(
            "The loan's default, as it stood when the data was pulled in October 2024, long after every loan was due "
            "(about 1% of rows)."
        ),
        known=(
            "The customer (as an id, so the same customer's settled earlier loans can be in training), the number of "
            "the customer's earlier loans in the data, new or repeat customer, the loan amount, the disbursement and "
            "due dates, the lender's funded amount and share."
        ),
        split=(
            "Six test windows of 5-10 days at the end of the product's lending, October to December 2022. Each trains "
            "on the loans whose label had settled before the window starts."
        ),
        changes=(
            "We keep only the main product, add the customer's number of earlier loans, drop the amounts to repay, "
            "which grow after a default, and the rows of lenders funding less than one unit (labelled no default "
            "whatever happened), and split by disbursement date where the competition split rows at random and also "
            "tested a second country."
        ),
        fit="approximate",
        fit_reason=(
            "The customer's history is known only through labels settled before each window, while a lender learns of"
            " a repayment the day it is made. How the loans were sampled is not stated. The competition's test of a "
            "second country (Ghana, unlabelled) and of new applicants is not part of the task."
        ),
    )

    # Dataset
    unique_name = "african_credit_scoring_challenge"
    year = "2024"
    domain = "finance"
    source = "Zindi"
    source_url = "https://zindi.africa/competitions/african-credit-scoring-challenge"
    license = "Zindi Competition Rules"
    download_description = """
        The Zindi data page needs a login. We download a Kaggle copy of the competition files that a participant
        (Kaggle user thelastsmilodon, 32nd place) uploaded on 2025-01-14, two days after submissions closed, with the
        licence "other" and no description. Its Train.csv, Test.csv, economic_indicators.csv and
        VariableDefinitions.txt have the byte sizes the Zindi data page lists (8,785,708, 2,379,732, 7,930 and 1,539).
        The upload has no version, so we record the SHA-256 of our files (first 16 hex digits): Train.csv
        20d437430408084a, Test.csv 8d31edd85335c681, economic_indicators.csv bc49ee02a535465a, VariableDefinitions.txt
        0cc43fb6c53d6503.

        mkdir -p local-data-warehouse/african_credit_scoring_challenge
        uvx --from kaggle==2.2.2 kaggle datasets download thelastsmilodon/african-credit-scoring-challenge-data -p local-data-warehouse/african_credit_scoring_challenge
        unzip local-data-warehouse/african_credit_scoring_challenge/african-credit-scoring-challenge-data.zip -d local-data-warehouse/african_credit_scoring_challenge/
        rm local-data-warehouse/african_credit_scoring_challenge/african-credit-scoring-challenge-data.zip
    """
    bibtex = r"""
        @misc{Zindi2024AfricanCreditScoringChallenge,
          author = {{Zindi}},
          title = {African Credit Scoring Challenge},
          year = {2024},
          howpublished = {\url{https://zindi.africa/competitions/african-credit-scoring-challenge}},
          note = {Zindi competition, 2024-11-29 to 2025-01-12}
        }
    """
    curation_comments = """
        We start with Train.csv of the Zindi African Credit Scoring Challenge, from a Kaggle copy of the competition files.

        - Prediction point: when a loan is disbursed, with the customer's earlier loans and their settled outcomes known.
        - We keep only the loans of the main product, Type_1 (Lennart, CC 2026-10-26): one lender's 7-day loans of 2022-07-12 to 2022-12-01, 52,826 rows after the lender-amount filter, 520 defaults (0.98%), 5,040 customers, 99.5% repeat loans. The file mixes this product with a few hundred loans a month of changing products (2021-2024) and a new product, Type_7, from July 2023; the other products default at about 10%, share 1.4% of their customers with Type_1, and are too few for test windows of their own. A mixed task would score telling the products apart rather than ranking the customers of one product (untuned LightGBM ROC AUC 0.68 on the mixed 2022 windows against 0.60 on Type_1 alone).
        - Not reproduced: the competition's test file also held 3,525 loans from Ghana (products absent from Train.csv, no labels released) and a random 18% of the Kenyan loans of the same dates; the competition's goal of models that "generalise well" to a new country cannot be tested here, and the Ghana part was won by a hand-written rule (issue 7 of the review, 2026-10-26).
        - Within Type_1, lender_id, loan_type and duration are constant, and we drop them.
        - We rename target to default.
        - We add earlier_loans, the number of the customer's loans in the release disbursed on an earlier day (Train.csv and the Kenyan rows of Test.csv, any product, one count per loan id), known at disbursement and built without labels (CLEAN-19, a history aggregated per prediction; Lennart, CC 2026-10-26). The models reach the customer's history only through customer_id otherwise (CatBoost falls from 0.66 to 0.55 ROC AUC without it); the count alone ranks defaults at 0.72 on the six windows (0.61-0.83 per window), above every model on the source's columns. It counts only loans in the release, so it grows over the first months of the data (median 9). A count of the customer's earlier defaults settled before disbursement is 0 in every row (a default ends the customer's history in the product), so it is not added.
        - We add no count of a loan's other lender rows: built from the rows present at the data pull, which buy-outs can change, it cannot be dated to disbursement. Test.csv (no labels) is read only for earlier_loans and decision table 2.
        - We drop ID and tbl_loan_id (identifiers) and country_id (Kenya in every row).
        - We drop Total_Amount_to_Repay and Lender_portion_to_be_repaid: recorded at the data pull, they grow with a defaulted loan's days past due (decision table).
        - We drop the 8,899 rows whose lender funds less than one unit (Amount_Funded_By_Lender below 0.5): none is labelled 1, where about 105 would be expected at the rate of their months, and for the same customers and months 1.04% of them carry a default-size repay charge against 0.40% of the customers' other loans. They are labelled 0 whatever the customer did and hide about 90-130 defaults (decision table).
        - Unsettled labels: recent defaults include late payments paid later (decision table, counted per loan). A label counts as settled 30 days after the due date, a conservative cut rather than a measured end of settlement, and each training side holds only the loans settled before its window starts; every Type_1 loan was due long before the data pull.
        - Temporal split on disbursement_date: 6 test windows of at most 30 days, each training on the loans settled before it starts (splits comment).
        - customer_id stays as a categorical: an entity's own history is legitimate under a temporal split (ieee_fraud_detection's uid). A default usually ends a customer's history, which made "the customer's last loan" a winning rule in the competition's random split; here a training side holds only settled loans.
        - New_versus_Repeat is a categorical, read per row: it can differ between a loan's two rows.
        - disbursement_date and due_date are datetimes; we keep due_date, disbursement_date plus duration, as a source column.
        - We do not join economic_indicators.csv: for Kenya alone it is a function of the year, with no values for 2024.
        - Duplicates: the 267 extra copies of identical rows have their own tbl_loan_id and share a date; we keep them as separate loans.
        - Anomaly: the source does not say how the loans were sampled.
        - One row funds 2,627.1 of a loan of 2,249 (share 1.168): we set its Amount_Funded_By_Lender and Lender_portion_Funded to missing.
        - Potential leak, kept on purpose: Amount_Funded_By_Lender and Lender_portion_Funded are values at the data pull, and lenders can buy each other out (host). On the Type_1 rows they show no link to the outcome (ROC AUC 0.46 and 0.49 alone). Kept like kick's unverified host fields; revisit if the host documents when shares are recorded.
        - Metric (Lennart, CC 2026-10-26, under MET-4's overrule clause): ROC AUC instead of Zindi's leaderboard F1. Zindi asked for a model that "accurately predicts the probability of loan default" and had its top 10 build a "credit scoring function, using their model's outputs and probabilities ... binning model outputs into risk categories", so the lender's decision is a risk grade, not one hard label; the leaderboard's F1 was gamed by a hand-written rule worth +0.07-0.10; and on our windows, with about 20 defaults each, one more caught default moves F1 by about 0.05 (untuned LightGBM F1 0.00-0.16 per window).
        - Licence: the Zindi rules call the data "private property of the client"; the Kaggle copy is a participant's upload.
    """

    # Task
    target = "default"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Original rejected (MET-4's overrule clause, Lennart 2026-10-26): Zindi's leaderboard F1 on hard 0/1 "
            "labels. The host's goal is default probabilities binned into risk grades, the forum shows the F1 was "
            "gamed, and with about 20 defaults per window one default moves F1 by about 0.05. roc_auc is the binary "
            "fallback."
        ),
    )

    # Splits: six windows at the end of the Type_1 lending (`_make_splits`)
    splits_comment = """
        A lender scores each loan when it is disbursed and refits on the loans whose outcome it knows, at least once a month; the six windows hold about a week of loans each (6-11 days, the declared horizon 7 days). A loan's label counts as known 30 days after its due date, so each training side holds the loans whose due date lies more than 30 days before the window starts; the loans of the five weeks before a window are not in its training side. Six windows of about equal numbers of rows cover the end of the product's lending, newest first, from the first day by which half of the rows have a settled label to the last Type_1 loan on 2022-12-01; they hold 18-22 default rows each, and more windows would leave some with 8. A row is one lender's part of a loan, so a two-lender loan counts twice. The 2022 windows leave out the 8-18% of the rows of their dates whose lender funds less than one unit (curation comments).
    """
    temporal = Temporal(on="disbursement_date", horizon=WINDOW_DAYS, horizon_unit="days")

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {"train": pd.read_csv(raw_dir / "Train.csv"), "test": pd.read_csv(raw_dir / "Test.csv")}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        return drop_columns(
            _labelled_rows(raw),
            [
                "ID",  # "ID_" + customer_id + tbl_loan_id + lender_id
                "country_id",  # Kenya in every row of Train.csv
                "lender_id",  # one lender for the product
                "loan_type",  # the one product kept
                "duration",  # 7 days in every row of the product
                "tbl_loan_id",  # a loan sequence number (Spearman 0.9999 with the disbursement date)
                # recorded at the data pull: a default's amount grows with its days past due (penalties)
                "Total_Amount_to_Repay",
                "Lender_portion_to_be_repaid",  # = Total_Amount_to_Repay x Lender_portion_Funded, rounded
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["customer_id", "New_versus_Repeat"],
            datetime={"disbursement_date": "%Y-%m-%d", "due_date": "%Y-%m-%d"},
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # `df` is sorted by disbursement date. A loan enters a training side once its label is settled.
        date = df["disbursement_date"]
        settled = df["due_date"] + pd.Timedelta(days=LABEL_SETTLED_DAYS)
        # About equal numbers of rows, cut at day boundaries, from the first day before which half of all rows have a
        # settled label to the end of the product's lending
        days = date.drop_duplicates().to_numpy()
        n_settled = np.searchsorted(np.sort(settled.to_numpy(), kind="stable"), days, side="left")
        assert (n_settled >= len(df) / 2).any(), "no day has half of the rows settled before it"
        first = days[np.argmax(n_settled >= len(df) / 2)]
        end = date.max() + pd.Timedelta(days=1)
        rows = np.flatnonzero(date >= first)
        starts = date.iloc[rows[0] + len(rows) * np.arange(N_WINDOWS) // N_WINDOWS].drop_duplicates().to_list()
        windows = list(zip(starts[::-1], [end, *starts[:0:-1]], strict=True))
        splits = {}
        for i, (start, stop) in enumerate(windows):  # newest first
            test = np.flatnonzero((date >= start) & (date < stop))
            splits[i] = {0: (np.flatnonzero(settled < start).tolist(), test.tolist())}
        return SplitPlan(splits=splits)

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        train = raw["train"]
        disbursed = pd.to_datetime(train["disbursement_date"], format="%Y-%m-%d")
        due = pd.to_datetime(train["due_date"], format="%Y-%m-%d")
        past_due = (disbursed.max() - due).dt.days  # days past due at the data pull
        outcome = train["target"].map({0: "repaid", 1: "defaulted"})
        charge = train["Total_Amount_to_Repay"] / train["Total_Amount"] - 1  # recorded at the pull (dropped)
        no_share = train["Amount_Funded_By_Lender"] < 0.5

        # 1. The amount to repay grows with the days a defaulted loan is overdue at the pull
        type_7 = train["loan_type"] == "Type_7"
        days = pd.cut(past_due, [0, 30, 60, 120, 240, 480], labels=["1-30", "31-60", "61-120", "121-240", "241-480"])
        accrual = (
            pd.DataFrame({"days past due at the pull": days, "outcome": outcome, "charge": charge})[type_7]
            .groupby(["days past due at the pull", "outcome"], observed=True)["charge"]
            .agg(rows="size", median_charge="median")
            .unstack("outcome")
        )
        accrual.columns = [f"{outcome}: {stat.replace('_', ' ')}" for stat, outcome in accrual.columns]
        accrual = accrual.round(4)

        # 2. A lender that funds less than one unit is never in default: the same customers and months, both kinds
        type_1 = train["loan_type"] == "Type_1"
        period = type_1 & disbursed.between(disbursed[no_share & type_1].min(), disbursed[no_share & type_1].max())
        both = (
            train[period]
            .groupby("customer_id")["Amount_Funded_By_Lender"]
            .agg(lambda s: (s < 0.5).any() and (s >= 0.5).any())
        )
        same = period & train["customer_id"].isin(both.index[both])
        kenya = raw["test"][raw["test"]["country_id"] == "Kenya"]  # later loans may sit in Test.csv
        dates = pd.concat([train, kenya]).groupby("customer_id")["disbursement_date"].max()
        again = pd.to_datetime(dates.reindex(train["customer_id"]).to_numpy(), format="%Y-%m-%d") > due.to_numpy()
        shares = (
            pd.DataFrame(
                {
                    "lender amount": np.where(no_share, "below 0.5 (dropped)", "0.5 or more"),
                    "repay charge": np.where(charge > 0.2, "over 20%", "up to 20%"),
                    "label": train["target"],
                    "again": again,
                }
            )[same]
            .groupby(["lender amount", "repay charge"])
            .agg(loans=("label", "size"), labelled_1=("label", "sum"), again=("again", "mean"))
            .round(3)
        )
        shares.columns = ["loans", "labelled 1", "customer borrowed again after the due date"]

        # 3. Defaults of the newest loans are inflated by late payments that are paid later; one count per loan, as
        # the rows of a two-lender loan share the label
        recent = (disbursed >= "2024-01-01") & (past_due > 0) & ~no_share
        loans = pd.DataFrame({"loan": train["tbl_loan_id"], "past_due": past_due, "label": train["target"]})
        loans = loans[recent].drop_duplicates("loan")
        settle = (
            loans["label"]
            .groupby(
                pd.cut(
                    loans["past_due"],
                    [0, 7, 14, 30, 45, 60, 90, 120, 180, 365],
                    labels=["1-7", "8-14", "15-30", "31-45", "46-60", "61-90", "91-120", "121-180", "181-365"],
                ),
                observed=True,
            )
            .agg(loans="size", defaults="sum", default_rate="mean")
            .rename_axis("days past due at the pull")
            .round(3)
        )

        # 4. The test windows, in rows (one per lender of a loan) and in loans
        kept = _labelled_rows(raw)  # the rows of `df`, with the loan id
        settled_rows = due + pd.Timedelta(days=LABEL_SETTLED_DAYS) <= disbursed.max()
        y = df["default"] == "Yes"
        rows = []
        for i, ((train_rows, test),) in (
            (i, list(folds.values())) for i, folds in self._make_splits(df).splits.items()
        ):
            dates = df["disbursement_date"].iloc[test]
            first, last = dates.min(), dates.max()
            loans = kept[kept["disbursement_date"].between(first, last)]
            seen = df["customer_id"].iloc[test].isin(set(df["customer_id"].iloc[train_rows]))
            rows.append(
                {
                    "window": i,
                    "first day": first.date(),
                    "last day": last.date(),
                    "test rows": len(test),
                    "test loans": loans["tbl_loan_id"].nunique(),
                    "default rows": int(y.iloc[test].sum()),
                    "defaulted loans": loans.loc[loans["default"] == "Yes", "tbl_loan_id"].nunique(),
                    "default rate": round(float(y.iloc[test].mean()), 3),
                    "training rows": len(train_rows),
                    "test rows of a customer in training": round(float(seen.mean()), 2),
                    "rows dropped for the lender amount": round(
                        float(no_share[settled_rows & disbursed.between(first, last)].mean()), 3
                    ),
                }
            )
        windows = pd.DataFrame(rows).set_index("window")

        return [
            Decision(
                "Total_Amount_to_Repay and Lender_portion_to_be_repaid are dropped: recorded after the outcome",
                "A repaid Type_7 row owes a median 3.5% over Total_Amount at 1-240 days past due at the data pull "
                "(2.0% for the 69 rows of 2023); a defaulted one owes more the longer it has been overdue (penalties). "
                "Lender_portion_to_be_repaid is the lender's part of that amount.",
                accrual,
            ),
            Decision(
                "Rows whose lender funds less than one unit are dropped: labelled 0 whatever the customer did",
                "None of the 8,899 rows whose lender funds less than one unit (8,520 with no share) is labelled 1. For "
                "the customers with Type_1 loans of both kinds in the same months, 1.04% of these rows carry a "
                "default-size repay charge (over 20%), against 0.40% of the customers' other loans, where such a "
                "charge means label 1 in 89% of cases; after a charged loan of either kind the customer almost never "
                "borrowed again. The rows hide about 90 defaults of these customers (about 130 in all) under the label "
                "0.",
                shares,
            ),
            Decision(
                "A label counts as settled 30 days after the due date",
                "Of the 2024 loans, counted once per loan, 20.4% of those 1-7 days overdue at the pull are labelled 1 "
                "and 11.8-14.9% of those 8-30 days overdue, against 5.8-9.8% from 31 days on (7.2% at 31-45 days), so "
                "recent defaults include late payments that are paid later. 30 days is a conservative cut, not a "
                "measured end of settlement. Loans due less than 30 days before the pull are dropped, and each "
                "training side holds only loans settled before its window starts.",
                settle,
            ),
            Decision(
                "Test windows: the end of the Type_1 lending, none longer than 30 days",
                "Six windows of about equal numbers of rows run from the first day by which half of the rows have a "
                "settled label to the last Type_1 loan (2022-12-01). A row is one lender's part of a loan.",
                windows,
            ),
        ]
