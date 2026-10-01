"""Curated dataset definition for `lending_club_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TemporalSplits, drop_columns


class LendingClub1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "lending_club_1m"
    version_of = "lending_club"
    version_comment = """
        To sub-sample this dataset, we only take the first year to obtain 814751 train and 276431.
    """
    year = "2018"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://zenodo.org/records/11295916"
    license = "CC0: Public Domain"  # On Kaggle, likely not true TOS from the website.
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
    bibtex = """
        @article{sanz2025credit,
          title={Credit Risk Meets Large Language Models: Building a Risk Indicator from Loan Descriptions in P2P Lending},
          author={Sanz-Guerrero, Mario and Arroyo, Javier},
          journal={Inteligencia Artificial},
          volume={28},
          number={75},
          pages={220--247},
          year={2025}
        }
    """
    curation_comments = """
        We start withe data from Sanz-Guerrero et al. (2025). This data is already well preprocessed and curated for the task and used for tabular-text learning. However, we noticed a lot variables from the original data are missing that can be added to the task without invalidating the task or introducing data leakage. Thus, we also merge new features from the original data into the version from Sanz-Guerrero et al. (2025).

        - This is a datasets where the description is very often empty or a standard phrase. So the model needs to be able to handle cases with a lot of missing data in the text modality, and also cases where the text is rarely informative. This is a common case in real-world tabular-text datasets, and it is important to have it represented in our benchmark.
        - We reverse the ordinal encoding of the target.
        - We reverse the name change of "revenue" back to "annual_inc".
        - We also create a sec_app_fico_n like the fico_n from anz-Guerrero et al. (2025).
        - We drop rows where "application_type" is missing as these rows have consistent missing values across features and likely represent some data loading artifact.
        - We drop the joint-applicant fields (sec_app_*, *_joint): they are only filled from 2017 on, and this version keeps the loans up to 2016, so they are empty here.
    """

    # Task
    target = "Default"
    problem_type = "binary_classification"
    time_on = "issue_d"

    # Splits
    splits_comment = """
        We try to create splits that simulate a model deployed to solve the task.

        The official data is updated monthly but has not enough data per month to create large enough test
        splits. We opt for simulating a model that is refit every year to obtain a robust test set instead.
        This introduces the unrealistic downside of data shift across a year that would not exist in a
        real-world model. We create 1 test split (2016). We use all data before the test year as training
        data. The split is sub-sampled to the row budget of 1M train and 250k test rows.
    """
    temporal_splits = TemporalSplits(window=1, unit="years", cutoffs=("2016",))
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        original_df = pd.read_csv(raw_dir / "accepted_2007_to_2018Q4.csv.gz")
        df = pd.read_csv(raw_dir / "LC_loans_granting_model_dataset.csv?download=1")
        return {"original_df": original_df, "df": df}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        original_df, df = raw["original_df"], raw["df"]
        # 0 for fully paid loans and a 1 for defaulted loans.
        df["Default"] = df["Default"].map({0: "Fully Paid", 1: "Defaulted"})
        df = df.rename(columns={"revenue": "annual_inc"})
        # Transform     "sec_app_fico_range_low"    "sec_app_fico_range_high", to sec_app_fico_n
        original_df["sec_app_fico_n"] = (
            original_df["sec_app_fico_range_low"] + original_df["sec_app_fico_range_high"]
        ) / 2
        new_features_from_original = original_df[
            [
                "id",
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
                "all_util",
                "sec_app_fico_n",
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
                "il_util",
                "inq_fi",
                "inq_last_12m",
                "inq_last_6mths",
                "max_bal_bc",
                "mo_sin_old_il_acct",
                "mo_sin_old_rev_tl_op",
                "mo_sin_rcnt_rev_tl_op",
                "mo_sin_rcnt_tl",
                "mort_acc",
                "mths_since_last_delinq",
                "mths_since_last_major_derog",
                "mths_since_last_record",
                "mths_since_rcnt_il",
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
                "open_acc_6m",
                "open_il_12m",
                "open_il_24m",
                "open_act_il",
                "open_rv_12m",
                "open_rv_24m",
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
                "total_bal_il",
                "total_bc_limit",
                "total_cu_tl",
                "total_il_high_credit_limit",
                "total_rev_hi_lim",
                "revol_bal_joint",
                "sec_app_earliest_cr_line",
                "sec_app_inq_last_6mths",
                "sec_app_mort_acc",
                "sec_app_open_acc",
                "sec_app_revol_util",
                "sec_app_open_act_il",
                "sec_app_num_rev_accts",
                "sec_app_chargeoff_within_12_mths",
                "sec_app_collections_12_mths_ex_med",
                "sec_app_mths_since_last_major_derog",
                "sec_app_fico_range_low",
                "sec_app_fico_range_high",  # dti dti_joint -> already merged by prior work via max
            ]
        ]
        # Merge new features into the curated version of the dataset.
        df = df.merge(new_features_from_original, on="id", how="left")
        del new_features_from_original, original_df
        # Rows with a missing application_type have consistently missing features (a loading artefact).
        df = df[~df["application_type"].isna()]
        # The joint-applicant fields (sec_app_*, *_joint) are only filled from 2017 on, and this version keeps
        # the loans up to 2016 (see the splits), so here they are empty.
        issued = pd.to_datetime(df["issue_d"], format="%b-%Y")
        empty_before_2017 = [c for c in df.columns if df.loc[issued.dt.year < 2017, c].isna().all()]
        df = drop_columns(
            df,
            [
                "id",  # meaningless identifier
                "experience_c",  # constant after preprocessing
                *empty_before_2017,
            ],
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=(
                "home_ownership_n",
                "application_type",
                "disbursement_method",
                "emp_length",
                "Default",
                "purpose",
            ),
            string=("emp_title", "addr_state", "zip_code", "title", "desc"),
            datetime={"issue_d": "%b-%Y", "earliest_cr_line": "%b-%Y"},  # sec_app_earliest_cr_line is dropped
        )
