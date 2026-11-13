"""Curated dataset definition for `credit_card_clients_default` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode, set_missing

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "EDUCATION": ["high school", "university", "graduate school"],
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "EDUCATION": {"1": "graduate school", "2": "university", "3": "high school"},
    "MARRIAGE": {"1": "married", "2": "single", "3": "others"},
    "SEX": {"1": "male", "2": "female"},
}


class CreditCardClientsDefault(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a credit card holder miss next month's payment?",
        use_case=(
            "For example, a card issuer at the end of a month estimates each client's chance of defaulting on the "
            "next payment, to adjust credit limits or start collection early."
        ),
        row=(
            "One credit card client of a bank in Taiwan, with six months of history from April to September 2005 "
            "(30,000 clients)."
        ),
        predicted="Whether the client defaults on the payment of the following month (22% do).",
        known=(
            "The credit limit, sex, education, marital status and age, and for each of the six months the repayment "
            "status (paid on time or months of delay), the bill amount and the amount paid."
        ),
        split="Random clients of the same bank and the same months.",
        fit="approximate",
        fit_reason=(
            "The file is one snapshot: every client is scored for the same month, so training and test share that "
            "month's conditions, where a bank trains on earlier months and scores the next."
        ),
    )

    # Dataset
    unique_name = "credit_card_clients_default"
    domain = "finance"
    data_tags = ("DelayedTarget",)
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C55S3H",
            license="CC BY 4.0",
            year="2016",
            bibtex="""
                @article{yeh2009comparisons,
                  title={The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients},
                  author={Yeh, I-Cheng and Lien, Che-hui},
                  journal={Expert systems with applications},
                  volume={36},
                  number={2},
                  pages={2473--2480},
                  year={2009},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/credit_card_clients_default/ && wget -P local-data-warehouse/credit_card_clients_default/ https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip && unzip local-data-warehouse/credit_card_clients_default/default+of+credit+card+clients.zip -d local-data-warehouse/credit_card_clients_default/ && rm local-data-warehouse/credit_card_clients_default/default+of+credit+card+clients.zip
    """
    curation_comments = """
        - We rename the target variable and restore the original class names.
        - We drop the "ID" column.
        - Anomaly: the data has temporal features but the task is time-invariant.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); 1 of them decoded from the source's codes
          into its words (`CODE_LABELS`, 2026-11-01); 1 hold a state outside the scale, placed by the curator's rule
          (missing when the column has no other missing value, else the lowest level; a state that is simply not on the
          scale, such as Other, is missing); codes that mean unknown are missing (CLEAN-10).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 1 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order; 2 unordered codes carry their words: `MARRIAGE`, `SEX`.
        - Exception to CLEAN-14 (2026-11-04, Andrej): the six repayment status columns `PAY_0` and `PAY_2` to `PAY_6`
          keep the codes -2 and 0 as numbers, though the UCI codebook defines only -1 (paid duly) and 1 to 9 (months
          of delay). The fact that sets them apart: they are each column's most common values (-2, -1 and 0 hold
          9-16%, 19-20% and 49-57% of the rows; -2 and 0 together 58-72%), so the rule (an undocumented code is
          missing) would blank most of each column and merge two states into one missing value. Their common reading
          is -2 card not used that month, -1 paid in full, 0 minimum paid with the balance revolving, an order of rising
          use of credit below the months of delay (default rate by September's code: -2 13%, -1 17%, 0 13%, 1 month
          late 34%, 2 months 69%). The code 1 (one month late) occurs in 12.3% of the rows for September but in at
          most 0.1% for the five earlier months, where 2 is 9-13%: the earlier months record a short delay
          differently, alike in both classes.
        - Time basis: DelayedTarget: one extract of 30,000 card holders of one Taiwanese bank, scored after the
          September 2005 statement with the same six months of history for every client (April to September 2005); the
          target is default on the next month's payment, one month closed for every client. Every client was scored at
          the same statement and its outcome is the same month's payment, so no test row is later than a training row
          and the random split is IID. The client ID is not a time order (the first two quarters of IDs cannot be told
          apart, ROC AUC 0.504). The credit limit and the demographics carry no date. Not tested: a later month.
    """

    # Task
    target = "DefaultOnPaymentNextMonth"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="area ratio of the lift (cumulative gains) chart; error rate reported alongside",
        reference="Yeh & Lien 2009, Expert Systems with Applications 36(2):2473-2480",
        definition=(
            "area ratio = area between model gains curve and baseline / area between ideal curve and baseline = Gini "
            "= 2*ROC AUC - 1, so ranking equals roc_auc"
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "default of credit card clients.xls", skiprows=[0])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["ID"])
        target_feature = "DefaultOnPaymentNextMonth"
        df = df.rename(columns={"default payment next month": target_feature})
        df[target_feature] = df[target_feature].map({1: "Yes", 0: "No"})
        # codes outside a scale that mean unknown, and states outside it placed as missing (CLEAN-10,
        # CLEAN-14): don't know, refused, not asked, other
        df = set_missing(
            df,
            {
                "EDUCATION": [0, 5, 6, 4],
            },
        )
        # codes the codebook leaves without words, or a question that did not apply (CLEAN-10)
        df = set_missing(df, {"MARRIAGE": [0.0]})
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "SEX",
                "MARRIAGE",
                "EDUCATION",
            ],
        )
