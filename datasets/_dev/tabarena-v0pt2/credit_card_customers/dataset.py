"""Curated dataset definition for `credit_card_customers` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, drop_columns

RAW_FILE = "BankChurners.csv"
"""The one file of the Kaggle dataset sakshigoyal7/credit-card-customers (version 1, 2020-11-19)."""

NAIVE_BAYES_PREFIX = "Naive_Bayes_Classifier_Attrition_Flag_"
"""The two last columns of the file: posteriors of a naive Bayes classifier fit with the label."""

CATEGORICAL = ["Gender", "Education_Level", "Marital_Status", "Income_Category", "Card_Category"]


class CreditCardCustomers(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a bank's credit card customer close the card account?",
        use_case=(
            "At a snapshot date, a bank scores each credit card customer for the risk of closing the account, from "
            "the profile and the last 12 months of card activity, so that a manager can contact the customer first."
        ),
        row=(
            "One credit card customer of a bank at one snapshot (10,127 customers), from a teaching case of "
            "Analyttica's LEAPS training platform; the bank, place and period are not stated."
        ),
        predicted=(
            "Whether the customer closed the account (16% did), with no stated horizon. When the closing happened "
            "relative to the 12-month window is not stated, and the source does not say whether closures by the "
            "issuer count."
        ),
        known=(
            "Age, gender, dependents, education, marital status, income band, card type, months with the bank, number"
            " of products, and the last 12 months of activity: inactive months, contacts with the bank, credit limit,"
            " revolving balance, transaction amount and count, and the change from Q1 to Q4. The transaction count"
            ' equals the Q4 plus the Q1 count in every row, so the source\'s "12 months" and "quarters" cannot'
            " both hold."
        ),
        split=(
            "Random customers of the same snapshot, a forced choice: a bank would train on an earlier snapshot and "
            "score the next, but the file has no dates and each customer appears once."
        ),
        changes=(
            "We drop the masked client number and the two columns of a naive Bayes classifier fitted with the label, "
            "which the file ships."
        ),
        fit="approximate",
        fit_reason=(
            "A teaching case's snapshot stands in for a bank's own customers: the first source (Analyttica's LEAPS "
            "case 11) is offline, no bank, place or period is named, and the columns show marks of generated data."
        ),
    )

    # Dataset
    unique_name = "credit_card_customers"
    year = "2020"
    domain = "business & marketing"
    source = "Other"  # sample case 11 of Analyttica's LEAPS training platform (2020-04-19), now offline
    source_url = "https://leaps.analyttica.com/sample_cases/11"
    license = "CC0-1.0"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We download the Kaggle dataset sakshigoyal7/credit-card-customers (version 1, uploaded on 2020-11-19, never
        updated; CC0-1.0), a copy of the data of sample case 11 of Analyttica's LEAPS platform (dated 2020-04-19; the
        uploader: "I got this dataset from a website with the URL as https://leaps.analyttica.com/home"). LEAPS is
        offline and the case material is not archived. The Kaggle dataset holds one file. Kaggle does not version-pin a
        download, so check the hash. Zenodo record
        10.5281/zenodo.4322342 (2020-12-15, uploader zhyli, CC BY 4.0) holds the same file byte for byte and is the
        pinned alternative.
        BankChurners.csv: sha256 c91b525a2a6755a1b0b80dad1d0d008ca97ec4df34552c8f47ffa12b6184b779

        mkdir -p local-data-warehouse/credit_card_customers && cd local-data-warehouse/credit_card_customers
        kaggle datasets download sakshigoyal7/credit-card-customers && unzip credit-card-customers.zip
        rm credit-card-customers.zip
        # or, pinned:
        wget -O BankChurners.csv "https://zenodo.org/records/4322342/files/BankChurners.csv?download=1"
    """
    bibtex = """
        @misc{goyal2020creditcard,
          author = {Goyal, Sakshi},
          title = {Credit Card customers: Predict Churning customers},
          year = {2020},
          howpublished = {\\url{https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers}},
          note = {Kaggle dataset, version 1. The uploader took the data from sample case 11 of Analyttica's LEAPS
            platform (\\url{https://leaps.analyttica.com/sample_cases/11}), now offline}
        }
    """
    curation_comments = """
        We start with BankChurners.csv from the Kaggle dataset sakshigoyal7/credit-card-customers, taken from sample case 11 of Analyttica's LEAPS training platform ("Predict Customer Attrition Using Naive Bayes Classification").

        - Prediction point: at a snapshot date, the bank scores each credit card customer from the profile and the card activity of the last 12 months for the risk of closing the card account, so that a manager can contact the customer first.
        - Potential leak, kept on purpose: the source does not say when the accounts closed relative to the 12-month window (Kaggle topic 203290 asked; no answer). If the window ends at the closure, the activity columns describe the closing itself. Some rows suggest it: the 7 customers without a transaction in Q4 and the 54 with 6 bank contacts are all attrited, and 55% of the attrited customers have a revolving balance of 0, against 19% of the others. Most attrited customers still transact in Q4 (median Q4/Q1 count ratio 0.53, existing customers 0.72), so the window does not run months past the closure. The signal starts before the last quarter: the Q1 count alone (9-12 months back) gives ROC AUC 0.819, the same as the Q4 count alone, and the profile, Credit_Limit and the Q1 count give 0.895. The rows that look like the closing itself are 61 (the 54 with 6 contacts and the 7 without a Q4 transaction). LightGBM reaches ROC AUC 0.980 on the 6 activity columns alone, 0.63 on the 10 profile columns (age, gender, dependents, education, marital status, income, card type, months on book, number of products, credit limit) and 0.994 on all. Kept: a falling activity before the closure is the signal the use case asks for. Revisit if the LEAPS case material turns up.
        - Target: Attrition_Flag, Attrited Customer ("if the account is closed", column description) or Existing Customer.
        - Dropped: CLIENTNUM, a masked client number, and the two Naive_Bayes_Classifier_Attrition_Flag_* columns, the posteriors of a naive Bayes classifier fit with the label (the record says "Remove NB features").
        - Features: the other 19 columns as published. Gender, Education_Level, Marital_Status, Income_Category and Card_Category are categorical, the rest numeric. "Unknown" stays a category: the data card lists it as a value, and for Income_Category it is not missing at random (second decision).
        - Anomaly: Avg_Open_To_Buy is Credit_Limit minus Total_Revolving_Bal and Avg_Utilization_Ratio is Total_Revolving_Bal / Credit_Limit in every row, so neither is a 12-month average as the data card says. Kept as published.
        - Potential leak, kept on purpose: Credit_Limit is clipped at the 5th and 95th percentiles of all 10,127 rows (507 rows at 1,438.3, 508 at 34,516) and Total_Revolving_Bal at its top (508 at 2,517), percentiles that include our test folds; Avg_Open_To_Buy and Avg_Utilization_Ratio are computed from the clipped values and carry both clips. The source platform is offline. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way.
        - Anomaly: Months_on_book is 36 for 24% of the rows, most likely filled in for a missing value; the true 36s cannot be told apart, so the value is kept.
        - Anomaly: the columns show marks of generated data (first decision). Total_Ct_Chng_Q4_Q1 splits Total_Trans_Ct into two whole counts in every row, so Total_Trans_Ct is not a 12-month count of four quarters; the tenure in months follows the age in years, no woman has an income above $60K, and Total_Trans_Amt falls in separated clusters whose class mix changes from cluster to cluster. The source cannot be traced to say whether the data are real; kept, and the curator decides.
        - IID split, forced (ForcedIIDFromTemporal, SPLIT-8): a deployed model trains on one snapshot, whose closures are known, and scores the next; the file is one undated snapshot, each row a different client, no client repeats and no duplicate rows. The cost of the missing time axis cannot be measured: the file order follows Total_Trans_Amt (Spearman 0.82), so a hold-out by file order measures a sort, and thirds by CLIENTNUM give ROC AUC 0.993, the same as a random split. Recover the dates if the LEAPS case material turns up.
        - Note: no task-probe flag, but CatBoost with default settings reaches ROC AUC 0.9943 on the 9 splits, 3 of them at or above the 0.995 of the `solved` flag, so tuned methods may tie at the ceiling.
    """

    # Task
    target = "Attrition_Flag"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Kaggle dataset, not a competition; the description names no metric and the LEAPS case material (Naive "
            "Bayes classification) is offline"
        )
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # the masked client number, and the two naive Bayes posteriors fit with the label
        naive_bayes = [c for c in df.columns if c.startswith(NAIVE_BAYES_PREFIX)]
        assert len(naive_bayes) == 2, naive_bayes
        return drop_columns(df, ["CLIENTNUM", *naive_bayes])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=CATEGORICAL)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        import matplotlib.pyplot as plt

        attrited = raw[self.target].eq("Attrited Customer")

        income = pd.crosstab(raw["Gender"], raw["Income_Category"])
        income = income[["Less than $40K", "$40K - $60K", "$60K - $80K", "$80K - $120K", "$120K +", "Unknown"]]

        fig, (left, right) = plt.subplots(1, 2, figsize=(10, 3.8))
        imputed = raw["Months_on_book"].eq(36)
        left.scatter(raw.loc[~imputed, "Customer_Age"], raw.loc[~imputed, "Months_on_book"], s=3, alpha=0.3)
        left.scatter(raw.loc[imputed, "Customer_Age"], raw.loc[imputed, "Months_on_book"], s=3, alpha=0.3)
        left.set(xlabel="Customer_Age (years)", ylabel="Months_on_book", title="Tenure in months follows age in years")
        bins = range(0, 19_000, 250)
        for flag, label in ((False, "Existing Customer"), (True, "Attrited Customer")):
            right.hist(raw.loc[attrited.eq(flag), "Total_Trans_Amt"], bins=bins, alpha=0.6, label=label)
        right.set(xlabel="Total_Trans_Amt (last 12 months)", ylabel="customers", title="Separated amount clusters")
        right.legend()
        fig.tight_layout()

        return [
            Decision(
                "Kept, although the columns show marks of generated data",
                "Outside the 2,463 rows at 36 months, the tenure in months follows the age in years: it is never "
                "above Customer_Age - 4 and rarely below Customer_Age - 20 (slope 1.006, r 0.89). Total_Trans_Amt "
                "falls in separated clusters whose class mix changes from cluster to cluster: 3,000-5,000 holds 98% "
                "existing customers, 6,000-7,000 68% attrited, and the 746 customers above 12,000 include no "
                "attriter. The 12-month count is the Q4 plus the Q1 count in every row, and inactive months are "
                "unrelated to it. Within each class, 8 of the 91 pairs of numeric columns differ in Spearman "
                "correlation by 0.3 or more, none changes sign, and most of the 8 follow from the zero balances "
                "and the Q4 drop of the attrited customers. The source cannot be traced to say whether the data are "
                "real; the curator decides.",
                fig,
            ),
            Decision(
                "Unknown kept as a category",
                "The data card lists Unknown as a value. It is not missing at random: no woman has an income above "
                "$60K, and Income_Category is Unknown for 1,060 women and 52 men.",
                income,
            ),
        ]
