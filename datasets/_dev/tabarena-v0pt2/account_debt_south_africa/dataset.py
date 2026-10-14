"""Curated dataset definition for `account_debt_south_africa` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

# The columns the bad-debt label is set from: debt aged 90 days or more, write-offs, and their ratio to the billing.
DEBT_COLUMNS = ["total90debt", "totalwriteoff", "debtbillingratio"]

# The payments of the two years at whose end the label is read: they decide how the arrears built up.
PAYMENT_COLUMNS = ["totalreceipting", "avgreceipting", "collectionratio"]

# A run of at least this many consecutive rows of the file without any debt aged 90+ days or write-off is a segment
# whose debt (or payments) was not recorded. The seven such runs hold 1,185 to 8,762 rows; the longest run outside
# them holds 334 rows of accounts that pay (curation_comments).
NO_DEBT_RUN_ROWS = 1_000

# The field names of the Kaggle data card ("Content") for the columns we keep.
RENAME = {
    "accountcategory": "AccCategory",
    "propertyvalue": "PropertyValue",
    "propertysize": "PropertySize",
    "totalbilling": "TotalBilling",
    "avgbilling": "AverageBilling",
    "totalelecbill": "TotalElectricityBill",
    "hasidno": "HasIDNo",
    "baddebt": "BadDebt",
}


def _has_debt(raw: pd.DataFrame) -> pd.Series:
    """Whether an account has debt aged 90 days or more or a write-off."""
    return (raw["total90debt"] > 0) | (raw["totalwriteoff"] > 0)


def no_debt_runs(raw: pd.DataFrame) -> pd.DataFrame:
    """The runs of at least ``NO_DEBT_RUN_ROWS`` consecutive rows (file order) without any debt or write-off."""
    has_debt = _has_debt(raw).to_numpy().astype(int)
    edges = np.diff(np.r_[1, has_debt, 1])
    starts, ends = np.flatnonzero(edges == -1), np.flatnonzero(edges == 1)
    long = ends - starts >= NO_DEBT_RUN_ROWS
    return pd.DataFrame({"first_row": starts[long], "rows": (ends - starts)[long]})


def in_no_debt_run(raw: pd.DataFrame) -> np.ndarray:
    """A mask over the rows of ``raw`` (file order): True inside one of the runs of :func:`no_debt_runs`."""
    runs = no_debt_runs(raw)
    mask = np.zeros(len(raw), dtype=bool)
    for first, n in zip(runs["first_row"], runs["rows"]):
        mask[first : first + n] = True
    return mask


class AccountDebtSouthAfrica(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Has a municipal billing account turned into bad debt?",
        use_case=(
            "A South African municipality scores its accounts to forecast how many, and how much, will turn into bad "
            "debt, and where to direct collection."
        ),
        row="One billing account of one of eight municipalities, summarised over two years.",
        predicted=(
            "Whether the account is a bad debt (debt overdue 90 days or more, or written off) at the end of those two"
            " years; 56% are."
        ),
        known=(
            "The account type, the property's value and size, whether an ID number is on file, and what was billed "
            "over the two years (in total, per bill, for electricity), not what was paid."
        ),
        split="Random accounts of the same municipalities at the same time.",
        changes=(
            "We drop the three debt columns that define the label, the payments of the same two years, and stretches "
            "of the file where no debt was recorded."
        ),
        fit="approximate",
        fit_reason=(
            "The file is one snapshot: the status at its date stands in for the forecast the data card describes (fit"
            " on one snapshot, score the next), and the features cover the same two years as the label."
        ),
    )

    # Dataset
    unique_name = "account_debt_south_africa"
    year = "2020"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/dmsconsultingsa/municipal-debt-risk-analysis"
    license = "CC0-1.0"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We download version 1 of the Kaggle dataset (the only version, 4 June 2020). It holds one file,
        MunicipalDebtAnalysis.csv (138,509 rows, md5 d5fa5aaf696e31a65eebb0532fa4568d). OpenML 43838
        (Municipal-Debt-Risk-Analysis) is a copy of the same rows in the same order.

        mkdir -p local-data-warehouse/account_debt_south_africa && cd local-data-warehouse/account_debt_south_africa && kaggle datasets download dmsconsultingsa/municipal-debt-risk-analysis/1 && unzip municipal-debt-risk-analysis.zip && rm municipal-debt-risk-analysis.zip && cd ../../
    """
    bibtex = r"""
        @misc{rawlins2020municipal,
          author = {Rawlins, Dylan},
          title = {Municipal Debt Risk Analysis},
          year = {2020},
          howpublished = {\url{https://www.kaggle.com/datasets/dmsconsultingsa/municipal-debt-risk-analysis}},
          note = {Kaggle dataset, DMS Technologies}
        }
    """
    curation_comments = """
        We start with MunicipalDebtAnalysis.csv (138,509 accounts of eight South African municipalities) from version 1 of the Kaggle dataset.

        - Prediction point: an account at the date of the extract, with its category, property, ID number on file and billing of the two years before; the label is its bad-debt status then.
        - We drop `total90debt`, `totalwriteoff` and `debtbillingratio`: they set the label (decision table).
        - We drop the 27,938 rows (20.2%) of seven runs of 1,185-8,762 consecutive file rows without any debt aged 90+ days or write-off, where debt was not recorded: none of their billed never-payers is a bad debt, against 91.5% outside (decision table; `NO_DEBT_RUN_ROWS` = 1,000).
        - Anomaly: a 186-row run (from row 91,971) of billed never-payers without bad debts stays; a lower threshold would also drop two runs of paying accounts (218 and 334 rows).
        - We follow the uploader's cohort and drop 8,700 accounts with no net billing in the two years, whose debt predates the window, or with negative payments.
        - We drop the payment totals `totalreceipting`, `avgreceipting` and `collectionratio`: the status is read at the end of the two years they sum (decision table). ROC AUC 0.952 with them, 0.874 without.
        - We drop `accountcategoryid` and `acccatabbr` (the category again), rename to the data card's names, and set a `PropertyValue` or `PropertySize` of 0 to missing.
        - Potential leak, kept on purpose: `TotalElectricityBill`, which the data card adds as "a means to recover debt" (a cut-off for arrears). Its signal is mostly whether the municipality bills electricity at all; among billed accounts it is the same share of the bill for bad debts and others (median 0.33), so cut-offs within the window leave no trace. ROC AUC 0.874 with it, 0.865 without.
        - Potential leak, kept on purpose: `HasIDNo`, by the data card a property of the holder ("often not captured properly or at all"). Accounts with one are bad debts more often (Residential 64% against 47%), so it may be captured when debt is pursued. ROC AUC 0.874 with it, 0.872 without.
        - We keep the 6,355 exact duplicate rows (6.2%), plausibly distinct accounts with the same property record or flat charge; without the copied test rows, ROC AUC falls from 0.874 to 0.867.
        - Anomaly: the file ends with a run of category Unknown (rows 134,192-138,276; 2,396 curated rows), mostly billed 1-3 times in two years; its never-payers with 1-3 bills are bad debts at 53% (86% elsewhere). Debt is recorded there, so it stays.
        - IID, forced: the file is one extract without dates, so the task (bad-debt status at the extract) stands in for the data card's forecast, a model trained on one snapshot scoring the next.
        - A municipality scores its own accounts, so its level is known information. The eight municipalities have no column; held out by file position, ROC AUC falls from 0.877 (random) to 0.843 (blocks of 2,500 rows) and 0.786 (thirds of the file).
    """

    # Task
    target = "BadDebt"
    problem_type = "binary_classification"

    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Kept on purpose: plausibly distinct accounts with the same property record or the same flat charge (162 "
            "accounts billed R6 in six R1 lines); the file has no account id to tell copies from accounts. Without "
            "the copied test rows, LightGBM ROC AUC on the first split falls from 0.874 to 0.867 (curation_comments)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "MunicipalDebtAnalysis.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. Runs of the file without any recorded debt (computed in file order, before any other filter).
        df = df[~in_no_debt_run(df)]
        # 2. The uploader's cohort: accounts billed in the two years, without negative payment totals.
        df = df[(df["totalbilling"] > 0) & (df["totalreceipting"] >= 0)]
        # 3. The columns that set the label, the payments of the same window, and two more encodings of the category.
        df = drop_columns(df, [*DEBT_COLUMNS, *PAYMENT_COLUMNS, "accountcategoryid", "acccatabbr"])
        df = df.rename(columns=RENAME)
        # 4. A market value or a size of 0: none on file.
        for col in ("PropertyValue", "PropertySize"):
            df[col] = df[col].mask(df[col] == 0)
        df["BadDebt"] = df["BadDebt"].map({1: "Yes", 0: "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["AccCategory"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        import matplotlib.pyplot as plt

        has_debt = _has_debt(raw)
        rule = pd.crosstab(
            has_debt.map({True: "debt aged 90+ days or write-off", False: "neither"}).rename("account"),
            raw["baddebt"].map({1: "bad debt", 0: "not a bad debt"}).rename("label"),
        )

        runs = no_debt_runs(raw)
        billed_never_paid = (raw["totalbilling"] > 0) & (raw["totalreceipting"] == 0)
        mask = in_no_debt_run(raw)
        rows = []
        for first, n in zip(runs["first_row"], runs["rows"]):
            part = slice(first, first + n)
            rows.append(
                {
                    "rows of the file": f"{first:,}-{first + n - 1:,}",
                    "rows": n,
                    "bad debts": int(raw["baddebt"].iloc[part].sum()),
                    "billed, never paid": f"{billed_never_paid.iloc[part].mean():.1%}",
                    "bad-debt rate of those": f"{raw['baddebt'].iloc[part][billed_never_paid.iloc[part]].mean():.1%}",
                    "ID number on file": f"{raw['hasidno'].iloc[part].mean():.1%}",
                }
            )
        outside = ~mask
        rows.append(
            {
                "rows of the file": "all other rows",
                "rows": int(outside.sum()),
                "bad debts": int(raw["baddebt"][outside].sum()),
                "billed, never paid": f"{billed_never_paid[outside].mean():.1%}",
                "bad-debt rate of those": f"{raw['baddebt'][outside & billed_never_paid].mean():.1%}",
                "ID number on file": f"{raw['hasidno'][outside].mean():.1%}",
            }
        )

        # the curated rows before the column drops: the bad-debt rate by the share of the window's billing paid
        kept = raw[~mask]
        kept = kept[(kept["totalbilling"] > 0) & (kept["totalreceipting"] >= 0)]
        band = pd.cut(
            kept["collectionratio"],
            bins=[-np.inf, 0, 0.5, 0.875, 1.05, np.inf],
            labels=["0 (never paid)", "0-0.5", "0.5-0.875", "0.875-1.05", "above 1.05"],
        ).rename("paid / billed in the two years")
        payments = (
            kept.groupby(band, observed=True)["baddebt"]
            .agg(rows="size", rate="mean")
            .round(3)
            .rename(columns={"rate": "bad-debt rate"})
        )

        fig, ax = plt.subplots(figsize=(8, 3))
        position = np.arange(len(raw))
        ax.plot(position, has_debt.astype(float).rolling(500, center=True, min_periods=1).mean(), lw=0.8)
        for first, n in zip(runs["first_row"], runs["rows"]):
            ax.axvspan(first, first + n, color="tab:red", alpha=0.25, lw=0)
        ax.set_xlabel("row of MunicipalDebtAnalysis.csv")
        ax.set_ylabel("share with debt 90+ days\nor write-off (500 rows)")
        ax.set_ylim(0, 1)
        fig.tight_layout()

        return [
            Decision(
                "Debt aged 90+ days and write-offs set the label: dropped",
                "Every account with debt aged 90 days or more or a write-off is a bad debt, and all but 371 others "
                "are not. `total90debt`, `totalwriteoff` and `debtbillingratio` are dropped (the uploader's notebook "
                "drops them too).",
                rule,
            ),
            Decision(
                "The payments of the same two years: dropped",
                "The label is read at the end of the two years whose payments `totalreceipting`, `avgreceipting` and "
                "`collectionratio` sum. The bad-debt rate falls from 91.5% for accounts that paid nothing to 14.7% "
                "for accounts that paid 87.5-105% of their billing (curated rows, before the column drops).",
                payments,
            ),
            Decision(
                "Seven runs of the file without any recorded debt: dropped",
                "Inside the runs no account that was billed and never paid is a bad debt; outside them most are. "
                "Debt was not recorded there. Rows of the file are counted from 0 after the header.",
                pd.DataFrame(rows),
            ),
            Decision(
                "Where the runs lie in the file",
                "The share of accounts with debt along the file (rolling over 500 rows); the dropped runs are shaded.",
                fig,
            ),
        ]
