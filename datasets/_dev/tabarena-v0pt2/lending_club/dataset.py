"""Curated dataset definition for `lending_club` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    SplitPlan,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
    set_missing,
)

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "emp_length": [
        "< 1 year",
        "1 year",
        "2 years",
        "3 years",
        "4 years",
        "5 years",
        "6 years",
        "7 years",
        "8 years",
        "9 years",
        "10+ years",
    ],  # open-ended
}


# Test windows: October-December 2015, April-June 2015 and October-December 2014 (review issue 1, Lennart,
# 2026-11-11); `_make_splits` builds them and then drops the repeat borrowers of each window from its training side.
SPLIT_WINDOWS = TemporalSplits(window=3, unit="months", cutoffs=("2015-10-01", "2015-04-01", "2014-10-01"))

# Fields LendingClub first reported in December 2015: empty before, 49.2% filled in December 2015, so no training
# side holds a value of them (curation notes).
FIRST_REPORTED_DEC_2015 = [
    "all_util",
    "il_util",
    "inq_fi",
    "inq_last_12m",
    "max_bal_bc",
    "mths_since_rcnt_il",
    "open_acc_6m",
    "open_il_12m",
    "open_il_24m",
    "open_act_il",
    "open_rv_12m",
    "open_rv_24m",
    "total_bal_il",
    "total_cu_tl",
]


class LendingClub(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a three-year LendingClub loan be repaid?",
        use_case=(
            "When a loan application arrives at LendingClub, a model scores the borrower's default risk before the "
            "company sets its own grade and interest rate, to decide whether to grant the loan."
        ),
        row=("One 36-month loan issued by LendingClub in the US, April 2008 to December 2015 (609,544 loans)."),
        predicted="Whether the loan defaulted (14%) or was fully paid over its three-year term.",
        known=(
            "The borrower's income, debt-to-income ratio, FICO score, job title and years employed, home ownership, "
            "state and partial zip code; the loan amount, purpose and free-text description; and the credit-bureau "
            "history (accounts, balances, delinquencies, inquiries)."
        ),
        split=(
            "Three quarters are test windows, each trained on all loans issued before it except those of borrowers "
            "who take a loan in the window: the newest, October to December 2015, then April to June 2015 and "
            "October to December 2014."
        ),
        changes=(
            "We keep only the 36-month loans issued up to 2015, whose outcomes are all known; we add credit-bureau "
            "fields from LendingClub's full file and leave out the company's grade and interest rate."
        ),
        fit="approximate",
        fit_reason=(
            "The features are known at application, but the training side holds outcomes of loans issued just before "
            "each window, which a model refit then would not yet have; a full three-year gap would leave too little "
            "data."
        ),
    )

    # Dataset
    unique_name = "lending_club"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="Other",  # LendingClub's own download portal (gone); we read the archived copy on Zenodo
            url="https://www.lendingclub.com",
            license=None,  # LendingClub's terms of use; the CC0 of the Kaggle file is its uploader's
            year="2018",
            bibtex="""
                @article{sanz2025credit,
                  title={Credit Risk Meets Large Language Models: Building a Risk Indicator from Loan Descriptions in P2P Lending},
                  author={Sanz-Guerrero, Mario and Arroyo, Javier},
                  journal={Inteligencia Artificial},
                  volume={28},
                  number={75},
                  pages={220--247},
                  year={2025}
                }
            """,
        ),
        Source(
            role="part",
            platform="Other",
            url="https://doi.org/10.5281/zenodo.11295916",
            license="CC BY 4.0",
            year="2024",
            name="the loan-granting cut of arXiv:2401.16458 on Zenodo, the base table",
            files=("LC_loans_granting_model_dataset.csv?download=1",),
        ),
        Source(
            role="part",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/wordsforthewise/lending-club",
            license="CC0: Public Domain",  # set by its uploader
            name="All Lending Club loan data, joined in by loan id",
            files=("accepted_2007_to_2018Q4.csv.gz",),
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        It seems the official download portal from https://www.lendingclub.com is gone. So we can only utilize artifacts from the past, which seem to go up to 2018.
        Old script and source: https://github.com/nateGeorge/preprocess_lending_club_data

        From all the artifacts we found online, this seems to be the newest: https://www.kaggle.com/datasets/wordsforthewise/lending-club/data
        And the following paper (https://arxiv.org/abs/2401.16458) curated this dataset https://zenodo.org/records/11295916 for tabular-text learning.

        Other artifacts:
        - https://www.kaggle.com/datasets/adarshsng/lending-club-loan-data-csv
        - https://www.kaggle.com/datasets/imsparsh/lending-club-loan-dataset-2007-2011

        wget https://zenodo.org/records/11295916/files/LC_loans_granting_model_dataset.csv?download=1
        mkdir -p local-data-warehouse/lending_club && mv LC_loans_granting_model_dataset.csv?download=1 local-data-warehouse/lending_club
        kaggle datasets download wordsforthewise/lending-club -f accepted_2007_to_2018Q4.csv.gz && mv accepted_2007_to_2018Q4.csv.gz local-data-warehouse/lending_club/
    """
    curation_comments = """
        We start with the data from Sanz-Guerrero et al. (2025), which is already preprocessed for this task and used for tabular-text learning. It lacks many variables of the original data that can be added without changing the task or leaking the label, so we merge them in from the original data.

        - The description is often empty or a standard phrase, so a model must handle text that is mostly missing or uninformative. This is common in real-world tabular-text data, and we want it in the benchmark.
        - We reverse the ordinal encoding of the target.
        - We reverse the name change of "revenue" back to "annual_inc".
        - We drop rows where "application_type" is missing, as these rows have consistent missing values across features and likely are a data loading artifact.
        - We keep only the 36-month loans issued up to 2015, the only loans whose labels are complete, and drop the 60-month loans (about a third of the 2014-2015 volume) and all loans issued from 2016 on. The data of Sanz-Guerrero et al. (2025) holds only the loans that had finished (fully paid or charged off) by the 2018Q4 snapshot, so a loan still being repaid is missing.
        - In accepted_2007_to_2018Q4.csv.gz, at least 99.8% of the 36-month loans up to 2015Q4 are finished, but only 57-93% per quarter in 2016, and only 63-97% per quarter of the 60-month loans from 2014 on. The missing loans are mostly good ones, so later or longer loans would skew the labels towards early defaults and early payoffs (default rate among finished loans: 15-16% in 2013, 20% in 2015, 24-26% in 2016).
        - `term` is used only for this selection and is not a feature (it is part of the company's own assessment, see the merged features). Until 2026-10 the `lending_club_1m` version tested on 2016 and the v1 `lending_club` notebook on 2016-2018.
        - We leave out the joint-applicant fields of the original data (sec_app_*, revol_bal_joint): they are filled only from 2017 on, so they are empty for the loans we keep.
        - We leave out 14 credit-report fields LendingClub first reported in December 2015 (2026-11-11, Andrej):
          `all_util`, `il_util`, `inq_fi`, `inq_last_12m`, `max_bal_bc`, `mths_since_rcnt_il`, `open_acc_6m`,
          `open_il_12m`, `open_il_24m`, `open_act_il`, `open_rv_12m`, `open_rv_24m`, `total_bal_il`, `total_cu_tl`. They
          are empty for every loan issued before December 2015 and filled for 49.2% of December's 36-month loans, so no
          training side holds a value, and in the newest test window they only mark the month (default 15.6% whether
          filled or empty; counted on LendingClub's file joined to the loans of Sanz-Guerrero et al.).
        - Loans per issue year in the cleaned data (from the v1 exploration, counted 2026-10-22): 836 (2008), 4,716 (2009), 8,466 (2010), 12,747 (2011), 41,953 (2012), 99,018 (2013), 161,028 (2014), 280,780 (2015); 46% of the rows are from 2015, the year of the two newer test windows (the oldest is 2014 Q4).
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); codes that mean unknown are missing
          (CLEAN-10).
    """
    accepted_check_warnings = {
        "meta_license_unknown": (
            "LendingClub published the loans under its terms of use, without a licence; the Zenodo cut is CC BY 4.0 "
            "and the Kaggle file CC0, set by its uploader."
        ),
        "splits_train_under_half": (
            "Signed off (Lennart, 2026-11-11, review issue 1, b): October to December 2014 trains on 45.9% of the "
            "loans, beside October to December 2015 and April to June 2015 on 85.5% and 62.8%; SPLIT-14's two tiers "
            "admit it."
        ),
        "splits_rows_unused": (
            "By design: a training loan whose borrower key matches a test loan of every window is left out of all "
            "three training sides."
        ),
    }

    # Task
    target = "Default"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Sanz-Guerrero & Arroyo 2025 tune by balanced accuracy for its 'more stable behaviour' and test"
            " AUC second with DeLong tests; balanced accuracy fixes no decision threshold or costs for "
            "approving a loan (MET-6). Original rejected: balanced accuracy. roc_auc is the binary fallback"
            " (the paper's tested metric)."
        ),
    )

    # Splits
    splits_comment = """
        We try to create splits that simulate a model deployed to solve the task.

        Each test window is one calendar quarter, a model refit every quarter. LendingClub released its loan files by
        calendar quarter ("complete loan data for all loans issued through the previous completed calendar quarter"),
        and no source names a refit cadence: Sanz-Guerrero and Arroyo (2025) shuffle the loans into 5 folds, so the
        quarter matches the release, not a stated cadence (CC 2026-11-11), and a month of loans is a small test set.
        The 3 test windows (CC 2026-11-11), newest first: October to December 2015, the newest quarter, in which 14
        new credit-bureau fields (all_util, inq_fi, open_acc_6m, ...) appear; April to June 2015; and October to
        December 2014, a quarter of another year. They hold 88,667, 64,222 and 49,197 loans, and each trains on all
        loans issued before it: 520,877, 383,088 and 279,567 loans (85.5%, 62.8% and 45.9% of the 609,544). October
        to December 2014 trains on less than half the loans (45.9%), beside 85.5% and 62.8%. The windows are spread
        over two years instead of walking back from the newest: 46% of the loans were issued in 2015, so before 2015
        only 2014 Q4, Q3 and Q2 keep 30% of the loans for training (45.9%, 39.2% and 33.0%), and 2014 Q4 adds the
        other year at the smallest cost in training data. July to September and January to March 2015 are not
        tested. The default rate barely moves between the windows (14.8%, 15.4% and 14.6%; on the train sides 13.8%,
        13.3% and 12.8%). The outcome of a loan issued shortly before a window was only known later (by 2018), so the
        train side holds labels a deployed model would not have had yet; a gap of a full 36-month term would remove
        this but leave too little data.

        Exception to SPLIT-10 (2026-10-21, Lennart): a loan's outcome is known only when it ends, up to 36 months after
        issue, and the data has no outcome dates; a 36-month gap leaves 3.9-8.8% of the rows for training in the three
        windows and a 12-month gap 22.5-45.9%, under the floor (even a 6-month gap leaves only the newest window at
        half: 62.8%, 45.9% and 33.0%; for the windows of 2026-10-21 the figures were 5-9%, 33-46% and 46% for the
        oldest). Serves SPLIT-14 (Must). The unmatured labels fall under SPLIT-10 (principles.md, Tensions).

        Repeat borrowers (2026-11-11, Andrej): each training side leaves out the loans of borrowers who take a loan in
        the test quarter, as alfa_battle_2_0_task_2 does. The release has no borrower id, so the borrower is the exact
        match of the month of the earliest credit line, the 3-digit ZIP code, the state and the lower-cased employer
        title (`borrower_key`, built in `_clean`, not a feature). A test loan whose borrower's earlier loan defaulted
        defaults at 77% and 59% in the two windows measured (April-June 2015: 317 loans; October-December 2015: 391),
        against 9% after a repaid earlier loan and 15% without one; a lender does not grant a new loan on a
        charged-off one, so that earlier default was most likely recorded after the test loan was issued, a label a
        refit at the quarter's start could not know. The filter removes 3,642 and 5,213 training loans (0.8% to 1.0%)
        in those two windows, where 3,481 and 4,942 test loans have a match. LightGBM (400 trees) with the matched
        training loans dropped against as many dropped at random: ROC AUC 0.685 against 0.685 (April-June 2015) and
        0.686 against 0.688 (October-December 2015); on the matched test loans 0.680 against 0.702 and 0.676 against
        0.706. The counts were measured on the windows April-June, July-September and October-December 2015, the
        definition of the time (the third set is not a window here); October-December 2014 is not measured, as this
        branch has none of the raw files.
    """
    temporal = Temporal(on="issue_d", horizon=3, horizon_unit="months")  # the windows: `SPLIT_WINDOWS`

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        original_df = pd.read_csv(raw_dir / "accepted_2007_to_2018Q4.csv.gz")
        df = pd.read_csv(raw_dir / "LC_loans_granting_model_dataset.csv?download=1")
        return {"original_df": original_df, "df": df}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        original_df, df = raw["original_df"], raw["df"]
        # 0 for fully paid loans and a 1 for defaulted loans.
        df["Default"] = df["Default"].map({0: "Fully Paid", 1: "Defaulted"})
        df = df.rename(columns={"revenue": "annual_inc"})
        new_features_from_original = original_df[
            [
                "id",
                "term",  # only to keep the 36-month loans (see `_clean`); dropped, not a feature
                # known when the loan is granted, so it can be used as a feature without data leakage.
                #   This, however, would create a different task, in that we want to train a model that the company uses after their own risk assessment but before granting the loan.
                #   Given that these values and grades are often determined by an internal model of the company, they might also introduce an unknown bias.
                #   We stick to treating the task as a pre-assessment modelling. An alternative version could also function as a "stacking" model that takes the output of the company's internal model as an input.
                #   The variables for this task are:
                # "term",
                # "int_rate",
                # "installment",
                # "grade",
                # "sub_grade",
                # "verification_status",
                # Known at the start / from data source even without the company assessing the risk, so it can be used no matter the use case.
                "emp_title",
                "disbursement_method",
                "acc_now_delinq",
                "acc_open_past_24mths",
                # annual_inc	annual_inc_joint -> were already merged by prior work
                # fico_range_high fico_range_low -> transformed before into avg fico
                "application_type",
                "avg_cur_bal",
                "bc_open_to_buy",
                "bc_util",
                "chargeoff_within_12_mths",
                "collections_12_mths_ex_med",
                "delinq_2yrs",
                "delinq_amnt",
                "earliest_cr_line",
                "inq_last_6mths",
                "mo_sin_old_il_acct",
                "mo_sin_old_rev_tl_op",
                "mo_sin_rcnt_rev_tl_op",
                "mo_sin_rcnt_tl",
                "mort_acc",
                "mths_since_last_delinq",
                "mths_since_last_major_derog",
                "mths_since_last_record",
                "mths_since_recent_bc",
                "mths_since_recent_bc_dlq",
                "mths_since_recent_inq",
                "mths_since_recent_revol_delinq",
                "num_accts_ever_120_pd",
                "num_actv_bc_tl",
                "num_actv_rev_tl",
                "num_bc_sats",
                "num_bc_tl",
                "num_il_tl",
                "num_op_rev_tl",
                "num_rev_accts",
                "num_rev_tl_bal_gt_0",
                "num_sats",
                "num_tl_120dpd_2m",
                "num_tl_30dpd",
                "num_tl_90g_dpd_24m",
                "num_tl_op_past_12m",
                "open_acc",
                "pct_tl_nvr_dlq",
                "percent_bc_gt_75",
                "pub_rec",
                "pub_rec_bankruptcies",
                "revol_bal",
                "revol_util",
                "tax_liens",
                "tot_coll_amt",
                "tot_cur_bal",
                "tot_hi_cred_lim",
                "total_acc",
                "total_bal_ex_mort",
                "total_bc_limit",
                "total_il_high_credit_limit",
                "total_rev_hi_lim",
                # Not merged: the 14 fields of FIRST_REPORTED_DEC_2015 (first reported in December 2015: empty
                #   before, 49.2% filled in December 2015).
                # dti dti_joint -> already merged by prior work via max
                # Not merged: the joint-applicant fields (revol_bal_joint, sec_app_*) are filled only from 2017 on,
                #   so they are empty for the 36-month loans issued up to 2015 that we keep.
            ]
        ]
        # Merge new features into the curated version of the dataset.
        df = df.merge(new_features_from_original, on="id", how="left")
        del new_features_from_original, original_df
        # Rows with a missing application_type have consistently missing features (a loading artefact).
        df = df[~df["application_type"].isna()]
        # Labels are complete only for the 36-month loans issued up to 2015: the data holds the loans that had
        # finished by the 2018Q4 snapshot, so later or longer loans are missing while they were being repaid.
        issued = pd.to_datetime(df["issue_d"], format="%b-%Y")
        df = df[(df["term"].str.strip() == "36 months") & (issued < "2016-01-01")]
        # The borrower, for `_make_splits`: there is no borrower id, so the exact match of four stable fields (the
        # month of the earliest credit line, 3-digit ZIP code, state, employer title); not a feature.
        title = df["emp_title"].astype("string").str.strip().str.lower()
        key = df["earliest_cr_line"].astype("string") + "|" + df["zip_code"].astype("string") + "|"
        key = key + df["addr_state"].astype("string") + "|" + title
        df["borrower_key"] = key.where(title.notna() & (title != "") & df["earliest_cr_line"].notna())
        df = drop_columns(
            df,
            [
                "id",  # meaningless identifier
                "experience_c",  # constant after preprocessing
                "term",  # used only for the selection above
                "disbursement_method",  # a single value ("Cash") for the loans we keep
            ],
        )
        # codes outside a scale that mean unknown, and states outside it placed as missing (CLEAN-10,
        # CLEAN-14): don't know, refused, not asked, other
        df = set_missing(
            df,
            {
                "emp_length": ["NI"],
            },
        )
        return df

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # The declared windows, then each training side without the loans of borrowers who take a loan in the
        # window: their earlier default was recorded after the test loan was issued (splits comment).
        windows = SPLIT_WINDOWS.splits(df, self.temporal.on)
        key = df["borrower_key"]
        splits = {}
        for repeat, folds in windows.items():
            train, test = (np.asarray(side) for side in folds[0])
            test_keys = key.iloc[test].dropna().unique()
            same_borrower = key.iloc[train].isin(test_keys).to_numpy()
            splits[repeat] = {0: (train[~same_borrower].tolist(), test.tolist())}
        return SplitPlan(splits=splits, df=drop_columns(df, ["borrower_key"]))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=(
                "home_ownership_n",
                "application_type",
                "emp_length",
                "Default",
                "purpose",
            ),
            string=("emp_title", "addr_state", "zip_code", "title", "desc"),
            datetime={"issue_d": "%b-%Y", "earliest_cr_line": "%b-%Y"},  # sec_app_earliest_cr_line is not merged
        )
