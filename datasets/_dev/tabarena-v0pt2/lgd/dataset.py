"""Curated dataset definition for `lgd` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    TaskSummary,
    anonymize_ids,
    drop_columns,
)

TARGET_COPIES = ["Recovery_rate", "y_logistic", "lnrr", "Y_probit"]
"""Transformations of `lgd_time` that the source ships for the book's models: 1 - LGD, logit, log(1 - LGD), probit."""

FLOOR = 0.00001
"""The value the source gives an LGD of zero, so that the logit and probit transforms exist."""

CAP = 0.99999
"""The value the source gives an LGD of one (a total loss)."""


def ltv_runs(ltv: pd.Series) -> pd.Series:
    """Number the runs of consecutive rows with the same loan-to-value ratio, in the file's order."""
    return (ltv != ltv.shift()).cumsum()


class Lgd(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What share of a defaulted loan's outstanding amount will the bank lose?",
        use_case=(
            "When a loan has just defaulted, the bank estimates the share of the outstanding amount it will lose (the"
            " task of the book's chapter 10)."
        ),
        row=(
            'One defaulted loan of a European bank, "slightly modified and anonymized", from the book Credit Risk '
            "Analytics (2,545 loans, 2016; period not stated)."
        ),
        predicted=(
            "The loss as a share of the outstanding amount, from 0 to 1; 28.6% of the loans lose nothing and 5.6% "
            "lose everything."
        ),
        known=("Only the loan-to-value ratio and whether the loan's purpose is renting, as in the book's models."),
        split=(
            "Groups of loans that most likely belong to one borrower are held out whole, so each test loan most likely"
            " comes from a borrower the model has not seen: new borrowers in the same undated period, not next year's"
            " defaults."
        ),
        changes=(
            "We drop the transformations of the loss and the flag that marks loans without loss, and group the loans "
            "by borrower (runs of rows with one loan-to-value ratio)."
        ),
        fit="approximate",
        fit_reason=(
            "The file has no dates, so the split cannot place new defaults after old ones. The 28.6% of loans without"
            " loss are kept as cures (defaults that ended without loss), as the book's Tobit and censored beta code"
            " treat them, but the data page ('event: Indicator variable for a default or cure event; 1 = event, 0 = no"
            " event') leans against that reading."
        ),
    )

    # Dataset
    unique_name = "lgd"
    year = "2016"
    domain = "finance"
    source = "Other"
    source_url = "http://www.creditriskanalytics.net/datasets-private2.html"
    license = (
        "Use only in conjunction with the Credit Risk Analytics textbooks; commercial use prohibited (the agreement "
        "on the book's download form, http://www.creditriskanalytics.net/datasets.html). Note: the site's terms "
        '(http://www.creditriskanalytics.net/terms.html) say "You must not: Republish material from Credit Risk '
        'Analytics [...] Redistribute content from Credit Risk Analytics".'
    )
    download_description = """
        We download lgd.csv from the data page of the book "Credit Risk Analytics" (Baesens, Roesch and Scheule, Wiley
        2016). The book's site asks for a name and an agreement on http://www.creditriskanalytics.net/datasets.html
        before it shows the data page; the file link itself needs no login. The page also offers lgd.sas7bdat: the
        same rows in the same order at full precision (the csv rounds to 10 decimals). A copy of the same lgd.csv sits
        on GitHub (dpicone1/Credit-Risk-Anaytics-The-R-Companion, same sha256). No re-upload was found on OpenML or
        Kaggle (searched by name, 2026-10-07).

        mkdir -p local-data-warehouse/lgd
        wget -O local-data-warehouse/lgd/lgd.csv http://www.creditriskanalytics.net/uploads/1/9/5/1/19511601/lgd.csv

        sha256 of lgd.csv: 2e3f964a88bc97f67a1be712addacc9098100515a0239c73fc883741cbb1e07e

        Pinned alternative, the Wayback Machine's copy of 2017-09-27 (same sha256, so the file is unchanged since then):

        wget -O local-data-warehouse/lgd/lgd.csv "http://web.archive.org/web/20170927093523id_/http://www.creditriskanalytics.net:80/uploads/1/9/5/1/19511601/lgd.csv"
    """
    bibtex = r"""
        @book{baesens2016credit,
          title={Credit Risk Analytics: Measurement Techniques, Applications, and Examples in {SAS}},
          author={Baesens, Bart and R{\"o}sch, Daniel and Scheule, Harald},
          publisher={John Wiley \& Sons},
          address={Hoboken, NJ},
          year={2016},
          isbn={978-1-119-14398-7},
          doi={10.1002/9781119449560}
        }
    """
    curation_comments = """
        We start with lgd.csv from the data page of the book Credit Risk Analytics (Baesens, Roesch and Scheule 2016): 2,545 loans of a European bank, "slightly modified and anonymized" (chapter 1, p. 14).

        - Prediction point: a loan has just defaulted, and the bank estimates the share of the amount outstanding it will lose. The loan-to-value ratio and the purpose are known then.
        - Target: `lgd` (the source's `lgd_time`), a share from 0 to 1, as regression, the book's own task in chapter 10. No log transform: the share has mass points at both bounds. The record asks for binary classification, but the only binary column, `event`, is part of this target.
        - We drop `Recovery_rate`, `y_logistic`, `lnrr` and `Y_probit`, transformations of the LGD.
        - We drop `event`: it is 0 for exactly the 728 loans at the floor, so it says whether there was a loss (decision table).
        - We keep the source's target bounds: an LGD of zero is stored as 0.00001 (28.6% of the loans) and a total loss as 0.99999 (5.6%).
        - We rename `LTV` to `loan_to_value` (a share, although the data page says "in %") and `purpose1` to `purpose_renting`, a categorical 0/1 flag.
        - Grouped by borrower block (`borrower_block`): a run of consecutive rows with one loan-to-value ratio, which occurs in no other run. 70 of the 488 multi-loan runs mix both purposes, so a run holds different loans, most likely of one borrower, and their LGDs are alike (correlation 0.42 within runs net of LTV and file order, 0.35 without the 120 exact repeats, 0.02 between neighbouring runs). A borrower's loans default together, so the losses of the other loans are not known at a new default; each run stays on one side (decision table).
        - Duplicates: the 120 rows that repeat an earlier row of their run and the 397 rows that differ from another loan only in the LGD are loans of one borrower; we keep them, and the grouped split keeps each run on one side.
        - Anomaly: the file's row order carries the outcome without a documented meaning (the median LTV and the mean LGD rise over the first four fifths of the file); with no dates in the file, the split cannot be temporal. Forward windows in file order score a spline R² of 0.138 against 0.210 grouped, an upper bound on what a dated split would cost, since the order is not shown to be time.
        - Note: the data page says "event: Indicator variable for a default or cure event; 1 = event, 0 = no event". Read literally, it puts cures at 1, so it leans against reading `event` = 0 as a cure (a default that ended without loss). The book's R code treats these rows as an LGD of 0 in its Tobit and censored beta models and as "not selected" in its Heckman model. We keep the rows as cures, an open risk on 28.6% of the target until chapter 10 (pp. 271-313) is read: if these loans never defaulted, the 728 rows do not belong in an LGD target.
        - Note: the artefacts for which the book's HMEQ data was retired (homeq_default_prediction) are absent: no run is a jittered copy, and the number format of the LTV does not predict the LGD. LTVs with 6 or 7 decimals are in excess at LTV > 1, but adding that flag to a spline changes R² only from 0.2064 to 0.2057.
        - Note: two features only, as in the book's models. The raw loan-to-value ratio as a monotone fit (skill 0.188) beats a spline on both columns (0.208) on 0 of the 30 shipped splits, so the task is not `Trivial` (task-probe rule 4).
    """

    # Task
    target = "lgd"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "Baesens, Roesch & Scheule 2016 (ch. 10) evaluate LGD models by MSE/RMSE, R^2 and "
            "Pearson/Spearman/Kendall correlations, with no declared winner metric. rmse is the regression "
            "fallback."
        ),
    )
    grouping = Grouping(
        on="borrower_block",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a run of consecutive rows of the source file with the same loan-to-value ratio: 1,958 runs,
            488 of them with 2-7 loans. The loans of a run share one loan-to-value ratio. They are most likely one
            borrower's loans: 70 of the multi-loan runs mix both loan purposes, and their LGDs correlate (0.42 after
            LTV and the file-order trend are removed, 0.35 without the 120 exact repeats, 0.02 between neighbouring
            runs).
            The key equals the LTV value, since no value occurs outside its run. The grouping rests on the consecutive
            blocks of the file's order, not on a hash of the features.
            The book defines LGD by the "default of an obligor" (chapter 1, p. 10), so a borrower's loans default
            together. When the model estimates the LGD of a new default, the losses of the borrower's other loans
            are therefore not known. Each loan is one prediction from its own row.
        """,
    )
    splits_comment = (
        "Grouped splits on the borrower block: all loans that share one loan-to-value ratio (one run in the source "
        "file, most likely one borrower) stay on one side. The test stands for new borrowers in the same undated "
        "period, not next year's defaults: the file has no dates, and forward windows in file order give a spline R² "
        "of 0.138 against 0.210 grouped, an upper bound on that gap since the order is not shown to be time."
    )
    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "120 rows repeat a loan of the same borrower block in every column. 103 sit at the no-loss floor and 16 at "
            "the total-loss cap: loans of one borrower that all cured or were all lost. The other one is a pair with "
            "the same partial loss (0.0109972412, next to 0.0110039 and 0.0110091 in its block). The grouped split "
            "keeps all of them on one side."
        ),
        "dataset_conflicting_duplicate_rows": (
            "With two features, loans of one borrower block share the loan-to-value ratio and often the purpose while "
            "their losses differ (397 rows): separate loans, not label noise. They stay on one side of the grouped "
            "split."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "lgd.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # The file lists the loans that share one loan-to-value ratio as one run of consecutive rows, and no LTV value
        # occurs outside its run: a run is most likely one borrower's loans, the group of the split.
        run = ltv_runs(df["LTV"])
        assert run.groupby(df["LTV"]).nunique().max() == 1, "an LTV value occurs in two runs"
        df["borrower_block"] = anonymize_ids(run.astype(str))
        # `event` is 0 exactly when the LGD sits at the source's floor (no loss): a part of the target. The other four
        # columns are transformations of the LGD.
        assert ((df["event"] == 0) == np.isclose(df["lgd_time"], FLOOR, rtol=0, atol=1e-12)).all()
        df = drop_columns(df, [*TARGET_COPIES, "event"])
        return df.rename(columns={"lgd_time": self.target, "LTV": "loan_to_value", "purpose1": "purpose_renting"})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(categorical=["borrower_block", "purpose_renting"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        run = ltv_runs(raw["LTV"])
        by_run = raw.groupby(run)
        runs = pd.DataFrame(
            {
                "loans": by_run.size(),
                "mixed purpose": by_run["purpose1"].nunique() > 1,
                "loss and no loss": by_run["event"].nunique() > 1,
                "lgd spread": by_run["lgd_time"].std(ddof=0),
            }
        )
        size = runs["loans"].clip(upper=4).map(lambda n: "4-7" if n == 4 else str(n))
        table = runs.groupby(size).agg(
            runs=("loans", "size"),
            rows=("loans", "sum"),
            runs_with_mixed_purpose=("mixed purpose", "sum"),
            runs_with_loss_and_no_loss=("loss and no loss", "sum"),
            mean_sd_of_lgd_in_run=("lgd spread", "mean"),
        )
        table.index.name = "loans in the run"
        table["mean_sd_of_lgd_in_run"] = table["mean_sd_of_lgd_in_run"].round(3)

        level = np.select([np.isclose(raw["lgd_time"], FLOOR), np.isclose(raw["lgd_time"], CAP)], ["floor", "cap"], "")
        level = pd.Series(level, index=raw.index).replace("", "between")
        event = pd.crosstab(raw["event"], level).reindex(columns=["floor", "between", "cap"], fill_value=0)
        event.index.name = "event"
        return [
            Decision(
                "Grouped by borrower block, not IID",
                "The file lists loans with the same loan-to-value ratio as one run of consecutive rows, and many runs "
                "mix both loan purposes: a run is most likely several loans of one borrower. Their losses are alike "
                f"(overall SD of the LGD {raw['lgd_time'].std():.3f}) and are not known when a new default is scored, "
                "so a run stays on one side of the split.",
                table,
            ),
            Decision(
                "`event` is dropped: it says whether the LGD is above the floor",
                "`event` is 0 exactly for the loans whose LGD is stored as 0.00001 (no loss), so it is part of the "
                "target, not a feature. The four other dropped columns are transformations of the LGD.",
                event,
            ),
        ]
