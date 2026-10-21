"""Curated dataset definition for `african_credit_scoring_challenge` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    SplitPlan,
    TaskSummary,
    Temporal,
    drop_columns,
)

LABEL_SETTLED_DAYS = 30
"""A loan's label counts as known this many days after its due date (curation comments, "Unsettled labels")."""

N_WINDOWS = 9
"""Test windows: the 3 x 3 splits an IID task of this size would get."""

RECENT_WINDOWS = 3
"""Of them, windows of WINDOW_DAYS at the end of the data; the others cut the end of the Type_1 lending of 2022."""

WINDOW_DAYS = 30
"""The longest test window: a lender refits at least once a month (splits comment)."""


def _labelled_rows(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """The rows of Train.csv kept for the task, still with the loan id (`_clean` drops it)."""
    df = raw["train"].rename(columns={"target": "default"})
    df["default"] = df["default"].map({1: "Yes", 0: "No"})
    for col in ("disbursement_date", "due_date"):
        df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")
    pull = df["disbursement_date"].max()  # the data pull: the file ends with the loans of its last day

    # Rows whose lender funds less than one unit of the loan are never labelled 1: they hide about 90-130 defaults
    # under the label 0 (curation comments)
    df = df[df["Amount_Funded_By_Lender"] >= 0.5].copy()

    # One row funds more than the loan (2,627.1 of 2,249; share 1.168): its funded amount and share are unknown
    impossible = df["Amount_Funded_By_Lender"] > df["Total_Amount"]
    df.loc[impossible, ["Amount_Funded_By_Lender", "Lender_portion_Funded"]] = np.nan

    # Labels not yet settled at the data pull
    return df[df["due_date"] + pd.Timedelta(days=LABEL_SETTLED_DAYS) <= pull]


class AfricanCreditScoringChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a borrower in Kenya default on a loan that has just been paid out?",
        use_case=(
            "When a loan is disbursed, a lender scores the customer's risk of default from the loan's terms and the "
            "customer's settled earlier loans, and refits the model at least once a month on the loans whose outcome "
            "it knows."
        ),
        row=(
            "One lender's part of one loan in Kenya, October 2021 to October 2024 (a loan with two lenders gives two "
            "rows); 54,163 of the 58,953 rows are from July to November 2022, mostly 7-day loans of one product."
        ),
        predicted=(
            "The loan's default, recorded on each lender row as it stood when the data was pulled (about 2% of rows; "
            "the two rows of a loan share the label in 2,132 of 2,134 loans). A label counts as settled 30 days after "
            "the due date; the source states no other horizon."
        ),
        known=(
            "The customer (as an id, so the same customer's settled earlier loans can be in training), new or repeat "
            "customer, the lender, the loan product, amount and duration, the disbursement and due dates, the "
            "lender's funded amount and share."
        ),
        split=(
            "Nine test windows of at most 30 days: six at the end of the 2022 lending of the main product and three "
            "at the end of the data in 2024. Each trains on the loans whose label had settled before the window "
            "starts."
        ),
        changes=(
            "We drop the amounts to repay, which grow after a default, the rows of lenders funding less than one unit"
            " (labelled no default whatever happened) and the loans not settled at the data pull, and we split by "
            "disbursement date where the competition split rows at random."
        ),
        fit="approximate",
        fit_reason=(
            "The lender's funded amount and share are values at the data pull (lenders can buy each other out), kept "
            "as they show no link to the outcome within a loan product. The customer's history is known only through "
            "labels settled before each window, while a lender learns of a repayment the day it is made. How the "
            "loans were sampled is not stated."
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

        - Prediction point: when a loan is disbursed, with the customer's settled earlier loans known.
        - We rename target to default. The competition scored F1, which we declare (TP-6).
        - We add no count of a loan's other lender rows: built from the rows present at the data pull, which buy-outs can change, it cannot be dated to disbursement. Test.csv (no labels) is read only for decision table 2.
        - We drop ID and tbl_loan_id (identifiers) and country_id (Kenya in every row).
        - We drop Total_Amount_to_Repay and Lender_portion_to_be_repaid: recorded at the data pull, they grow with a defaulted loan's days past due (decision table).
        - We drop the 8,899 rows whose lender funds less than one unit (Amount_Funded_By_Lender below 0.5): none is labelled 1, where about 105 would be expected at the rate of their months, and for the same customers and months 1.04% of them carry a default-size repay charge against 0.40% of the customers' other loans. They are labelled 0 whatever the customer did and hide about 90-130 defaults (decision table).
        - Unsettled labels: recent defaults include late payments paid later (decision table, counted per loan). A label counts as settled 30 days after the due date, a conservative cut rather than a measured end of settlement, and we drop the 802 rows due less than 30 days before the data pull.
        - Temporal split on disbursement_date: 9 test windows of at most 30 days, each training on the loans settled before it starts (splits comment).
        - customer_id stays as a categorical: an entity's own history is legitimate under a temporal split (ieee_fraud_detection's uid). A default usually ends a customer's history, which made "the customer's last loan" a winning rule in the competition's random split; here a training side holds only settled loans.
        - lender_id, loan_type and New_versus_Repeat are categoricals. New_versus_Repeat differs between a loan's two rows in 133 of the 2,134 two-row loans, so we read it per lender.
        - disbursement_date and due_date are datetimes; we keep due_date, disbursement_date plus duration, as a source column.
        - We do not join economic_indicators.csv: for Kenya alone it is a function of the year, with no values for 2024.
        - Duplicates: the 275 extra copies of identical rows have their own tbl_loan_id and share a date; we keep them as separate loans.
        - Anomaly: 54,163 of the 58,953 rows are from July to November 2022 (1.16% defaults), mostly Type_1 7-day loans. The source does not say how the loans were sampled.
        - One row funds 2,627.1 of a loan of 2,249 (share 1.168): we set its Amount_Funded_By_Lender and Lender_portion_Funded to missing.
        - Potential leak, kept on purpose: Amount_Funded_By_Lender and Lender_portion_Funded are values at the data pull, and lenders can buy each other out (host). Within a loan product they show no link to the outcome (ROC AUC 0.46 and 0.49 alone on the Type_1 rows); the link over all rows is the mix of products. Kept like kick's unverified host fields; revisit if the host documents when shares are recorded.
        - Note: the task probes flag no_spread, drift_baseline and unstable; we keep the task under task_probes.md rules 1-3 and 9 (weak separation on windows of 20-56 default rows; the drift is in log loss; LightGBM falls just below the class shares on the oldest 2024 window only, skill -0.03, and beats them on the other 4 probed windows). Re-check against tuned runs.
        - Licence: the Zindi rules call the data "private property of the client"; the Kaggle copy is a participant's upload.
    """

    # Task
    target = "default"
    problem_type = "binary_classification"
    metric = "f1"  # the competition's metric

    # Splits: the end of the Type_1 lending and the newest 90 days (`_make_splits`)
    splits_comment = """
        A lender scores each loan when it is disbursed and refits on the loans whose outcome it knows, at least once a month: no test window is longer than 30 days, the declared horizon. A loan's label counts as known 30 days after its due date, so each training side holds the loans whose due date lies more than 30 days before the window starts; loans disbursed in the weeks before a window, and longer loans still running, are not in that window's training side. The windows cover the two periods with enough loans for such windows, newest first: three 30-day windows at the end of the data (2024-07-11 to 2024-10-08, all but 9 rows Type_7 loans; 500-677 rows, 296-394 loans and 32-56 default rows each) and six windows of about equal numbers of rows at the end of the Type_1 lending, from 2022-10-20 (the first day by which half of all rows have a settled label) to 2022-12-01 (the last Type_1 loan; 5-10 days, 1,812-2,206 rows and 20-31 default rows each). A row is one lender's part of a loan, so a two-lender loan counts twice. The 1,901 rows between (2022-12-02 to 2024-07-10, about 100 a month of changing products) are too few for 30-day test windows and are training data only, apart from 6 long loans that settle on or after the first day of the newest window and so are in no split. The 2024 windows test a new product: Type_7 loans, first lent on 2023-07-27, with 98-688 Type_7 rows on their training sides and 12-44% of their test rows from a customer seen in training. Their labels are 30-119 days past due at the data pull; counted per loan, 2024 loans 31-45 days past due default at 7.2% (15 of 209) against 5.8-9.8% in each later bucket and 11.8-20.4% before 30 days (decision table 3), so the 30-day cut is conservative at this edge, not a measured end of settlement. The 2022 windows leave out the 8-18% of the rows of their dates whose lender funds less than one unit (curation comments). Nine windows of equal numbers of rows from 2022-10-20 (the v1 notebook's equal buckets) would test 2022-12-16 to 2024-07-10 as one window: one model for 573 days, with 28% of the window's rows in products that have no training row. Windows of equal numbers of distinct dates, as in kick, would put all 9 windows between March 2023 and October 2024 (112 to 872 rows and 9 to 72 default rows each) and leave 95% of the rows for training only.
    """
    temporal = Temporal(on="disbursement_date", horizon=WINDOW_DAYS, horizon_unit="days")
    accepted_check_warnings = {
        "dataset_pure_feature_value": "The hits are 11 disbursement dates of 13-30 July 2022, the due dates of those "
        "7-day loans (9 dates from 21 July to 5 August) and the due date 2022-09-19 (608 rows, 3 defaults). July 2022 "
        "was the first month of the Type_1 product, and its Type_1 rows default at 0.37% against 0.88-1.49% in "
        "August-November (1.99% overall). Default-size repay charges are as rare there (0.42%), so the low rate "
        "belongs to the period, which a model sees at disbursement, and does not hide defaults. None of these rows "
        "is a test row, and all but 4 (60- and 90-day Type_4 loans of 27-28 July) are on every training side.",
        "splits_rows_unused": "6 loans of 60-365 days, disbursed on 2023-09-19 and from 2024-06-11 to 2024-06-15, "
        "settle from 2024-09-09 (the first day of the newest window) to 2024-10-18: no window may train on them, and "
        "they were disbursed before the oldest 2024 window starts (2024-07-11).",
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {"train": pd.read_csv(raw_dir / "Train.csv"), "test": pd.read_csv(raw_dir / "Test.csv")}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        return drop_columns(
            _labelled_rows(raw),
            [
                "ID",  # "ID_" + customer_id + tbl_loan_id + lender_id
                "country_id",  # Kenya in every row of Train.csv
                "tbl_loan_id",  # a loan sequence number (Spearman 0.9999 with the disbursement date)
                # recorded at the data pull: a default's amount grows with its days past due (penalties)
                "Total_Amount_to_Repay",
                "Lender_portion_to_be_repaid",  # = Total_Amount_to_Repay x Lender_portion_Funded, rounded
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["customer_id", "lender_id", "loan_type", "New_versus_Repeat"],
            datetime={"disbursement_date": "%Y-%m-%d", "due_date": "%Y-%m-%d"},
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # `df` is sorted by disbursement date. A loan enters a training side once its label is settled.
        date = df["disbursement_date"]
        settled = df["due_date"] + pd.Timedelta(days=LABEL_SETTLED_DAYS)
        # The newest RECENT_WINDOWS windows: WINDOW_DAYS each, back from the last day of the data
        end = date.max() + pd.Timedelta(days=1)
        step = pd.Timedelta(days=WINDOW_DAYS)
        windows = [(end - step * (i + 1), end - step * i) for i in range(RECENT_WINDOWS)]
        # The others: about equal numbers of rows, cut at day boundaries, from the first day before which half of all
        # rows have a settled label to the end of the Type_1 lending
        days = date.drop_duplicates().to_numpy()
        n_settled = np.searchsorted(np.sort(settled.to_numpy(), kind="stable"), days, side="left")
        assert (n_settled >= len(df) / 2).any(), "no day has half of the rows settled before it"
        first = days[np.argmax(n_settled >= len(df) / 2)]
        type_1_end = date[df["loan_type"] == "Type_1"].max() + pd.Timedelta(days=1)
        assert type_1_end <= windows[-1][0], "the Type_1 windows overlap the newest windows"
        rows = np.flatnonzero((date >= first) & (date < type_1_end))
        n = N_WINDOWS - RECENT_WINDOWS
        starts = date.iloc[rows[0] + len(rows) * np.arange(n) // n].drop_duplicates().to_list()
        windows += list(zip(starts[::-1], [type_1_end, *starts[:0:-1]], strict=True))
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
                "Test windows: the end of the Type_1 lending and the newest 90 days, none longer than 30 days",
                "Three 30-day windows end on 2024-10-08; six windows of about equal numbers of rows run from "
                "2022-10-20, the first day by which half of all rows have a settled label, to the last Type_1 loan "
                "(2022-12-01). A row is one lender's part of a loan. The rows between are training data only.",
                windows,
            ),
        ]
