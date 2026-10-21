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

# A run of consecutive rows of the file without any debt aged 90+ days or write-off that holds at least this many
# accounts billed in the two years and never paying is a segment whose debt was not recorded. The eight such runs hold
# 183 to 4,583 of them, every other run at most 13, so any value from 20 to 150 drops the same runs; like any
# threshold, it is set on this file (curation_comments).
NO_DEBT_RUN_BILLED_NEVER_PAID = 100

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


def _billed_never_paid(raw: pd.DataFrame) -> pd.Series:
    """Whether an account was billed in the two years and paid nothing."""
    return (raw["totalbilling"] > 0) & (raw["totalreceipting"] == 0)


def no_debt_runs(raw: pd.DataFrame) -> pd.DataFrame:
    """The runs of consecutive rows (file order) without any debt or write-off that hold many never-payers.

    A run is kept when it holds at least ``NO_DEBT_RUN_BILLED_NEVER_PAID`` accounts billed and never paying.
    """
    has_debt = _has_debt(raw).to_numpy().astype(int)
    edges = np.diff(np.r_[1, has_debt, 1])
    starts, ends = np.flatnonzero(edges == -1), np.flatnonzero(edges == 1)
    cum = np.r_[0, np.cumsum(_billed_never_paid(raw).to_numpy())]
    never_paid = cum[ends] - cum[starts]
    hit = never_paid >= NO_DEBT_RUN_BILLED_NEVER_PAID
    return pd.DataFrame({"first_row": starts[hit], "rows": (ends - starts)[hit], "billed_never_paid": never_paid[hit]})


def in_no_debt_run(raw: pd.DataFrame) -> np.ndarray:
    """A mask over the rows of ``raw`` (file order): True inside one of the runs of :func:`no_debt_runs`."""
    runs = no_debt_runs(raw)
    mask = np.zeros(len(raw), dtype=bool)
    for first, n in zip(runs["first_row"], runs["rows"]):
        mask[first : first + n] = True
    return mask


class AccountDebtSouthAfrica(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a municipal billing account in arrears of 90+ days or written off at the extract?",
        use_case=(
            "A South African municipality scores its accounts to forecast how many will turn into bad debt, and where "
            "to direct collection."
        ),
        row="One billing account of one of eight municipalities, summarised over two years.",
        predicted=(
            "Whether the account is in arrears of 90+ days or written off at the extract, at the end of those two "
            "years (a bad debt); 56% are."
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
            " on one snapshot, score the next), and the features cover the same two years as the label. Most of the "
            "status is inherited: 83.7% of bad debts hold more 90+ debt and write-off than the two years' unpaid "
            "billing, and 69.1% more than their whole billing."
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

        - Prediction point: an account at the date of the extract, with its category, property, ID number on file and billing of the two years before; the label is its status then (arrears of 90+ days or a write-off), mostly debt older than the window (task_summary).
        - We drop `total90debt`, `totalwriteoff` and `debtbillingratio`: they set the label (decision table).
        - We drop the 28,124 rows (20.3%) of eight runs of 186-8,762 consecutive file rows without any debt aged 90+ days or write-off, where debt was not recorded: each holds 183 to 4,583 accounts billed and never paid, none of them a bad debt, against 91.9% of such accounts outside (decision table). Every other run holds at most 13, so `NO_DEBT_RUN_BILLED_NEVER_PAID` = 100 (any value from 20 to 150 selects the same runs; set on this file) keeps the paying runs of 334 and 218 rows.
        - We follow the uploader's cohort and drop 8,699 accounts: 903 with no billing in the two years, 7,721 with a net credit, 121 with negative payment totals (46 overlap).
        - We drop the payment totals `totalreceipting`, `avgreceipting` and `collectionratio`: the status is read at the end of the two years they sum (decision table). ROC AUC 0.952 with them, 0.874 without.
        - Kept on purpose: `TotalBilling` and `AverageBilling` sum the same window, but billing is set by tariff and property. Within file blocks of 2,500 rows and property-value bins, their residuals separate the classes at ROC AUC 0.509 (total), 0.501 (per line) and 0.496 (number of lines), so no outcome-dependent part shows. Revisit if a column of interest or penalties on arrears turns up.
        - We drop `accountcategoryid` and `acccatabbr` (the category again), rename to the data card's names, and set placeholders to missing: a `PropertyValue` of 0 or 1 (25 rows of 1) and a `PropertySize` of 10 square metres or less (5 rows above 0).
        - Potential leak, kept on purpose (open for the curator): `TotalElectricityBill`, which the data card adds as "a means to recover debt" (a cut-off for arrears), so a zero bill may be a consequence of the target (LEAK-10, LEAK-6). Within file blocks where 80% or more of accounts are billed for electricity, the accounts billed none are bad debts at 38.6% against 19.2% (within-block ROC AUC 0.588), also at equal payment status; among billed accounts the median share of the bill is 0.334 for both classes, so no partial cut-off shows. A vacant, unconnected or prepaid property also bills zero; the data cannot tell these apart. ROC AUC 0.874 with it, 0.865 without.
        - Potential leak, kept on purpose: `HasIDNo`, by the data card a property of the holder ("often not captured properly or at all"). Accounts with one are bad debts more often (Residential 64% against 47%), so it may be captured when debt is pursued. ROC AUC 0.874 with it, 0.872 without.
        - We keep the 6,355 exact duplicate rows (6.2%), plausibly distinct accounts with the same property record or flat charge; without the copied test rows, ROC AUC falls from 0.874 to 0.867.
        - Anomaly: the file ends with a run of category Unknown (rows 134,192-138,276; 2,396 curated rows), mostly billed 1-3 times in two years; its never-payers with 1-3 bills are bad debts at 53% (86% elsewhere). Debt is recorded there, so it stays.
        - IID, forced: the file is one extract without dates, so the task (status at the extract) stands in for the data card's forecast, a model trained on one snapshot scoring the next.
        - A municipality scores its own accounts, so its level is known information, but the eight municipalities have no column. Held out by file position, ROC AUC falls from 0.877 (random) to 0.849 (blocks of 2,500 rows) and 0.787 (thirds of the file); file position added as a feature raises the random split to 0.892, the cost of the missing key. We build no key from file blocks (a guess); the municipality key from DMS Technologies would be a feature.
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
        # 4. Placeholders: a market value of 0 or 1, a size of 10 square metres or less (mostly 0): none on file.
        df["PropertyValue"] = df["PropertyValue"].mask(df["PropertyValue"].isin([0, 1]))
        df["PropertySize"] = df["PropertySize"].mask(df["PropertySize"] <= 10)
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
        billed_never_paid = _billed_never_paid(raw)
        mask = in_no_debt_run(raw)
        rows = []
        for first, n in zip(runs["first_row"], runs["rows"]):
            part = slice(first, first + n)
            rows.append(
                {
                    "rows of the file": f"{first:,}-{first + n - 1:,}",
                    "rows": n,
                    "billed, never paid (accounts)": int(billed_never_paid.iloc[part].sum()),
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
                "billed, never paid (accounts)": int(billed_never_paid[outside].sum()),
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
                "Eight runs of the file without any recorded debt: dropped",
                "A run of rows without any debt or write-off is dropped when it holds at least "
                f"{NO_DEBT_RUN_BILLED_NEVER_PAID} accounts that were billed and never paid; every other such run holds "
                "at most 13. Inside the runs no such account is a bad debt; outside them most are. Debt was not "
                "recorded there. Rows of the file are counted from 0 after the header.",
                pd.DataFrame(rows),
            ),
            Decision(
                "Where the runs lie in the file",
                "The share of accounts with debt along the file (rolling over 500 rows); the dropped runs are shaded.",
                fig,
            ),
        ]
