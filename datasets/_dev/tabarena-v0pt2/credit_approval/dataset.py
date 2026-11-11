"""Curated dataset definition for `credit_approval` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary


class CreditApproval(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Should this credit card application be approved?",
        use_case=(
            "For example, when a credit card application arrives, the lender decides whether to approve it, here by "
            "imitating its past decisions."
        ),
        row=(
            "One credit card application (690, published by Quinlan in 1987); the lender, country and period are not "
            "stated."
        ),
        predicted=("Its class, + or - (44% are +), usually read as approved or rejected; the source gives no meaning."),
        known=(
            "Fourteen attributes of the applicant and the application, six numeric and eight categorical, whose names "
            "and values were replaced by symbols to keep the data confidential."
        ),
        split=(
            "Random applications, so the test data stands for new applications to the same lender in the same period."
        ),
        fit="approximate",
        fit_reason=(
            "The attributes are disguised, so we cannot check that each is known when an application arrives, and the"
            " label is a past decision of unstated meaning rather than repayment."
        ),
    )

    # Dataset
    unique_name = "credit_approval"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5FS30",
            license="CC BY 4.0",
            year="1987",
            bibtex="""
                @article{quinlan1987simplifying,
                  title={Simplifying decision trees},
                  author={Quinlan, J. Ross},
                  journal={International journal of man-machine studies},
                  volume={27},
                  number={3},
                  pages={221--234},
                  year={1987},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    data_tags = ("ForcedIIDFromTemporal", "Anonymized")
    download_description = """
        We get the credit screening data from UCI.

        wget https://archive.ics.uci.edu/static/public/27/credit+approval.zip && unzip credit+approval.zip  crx.data && rm credit+approval.zip  && mkdir -p local-data-warehouse/credit_approval && mv crx.data  local-data-warehouse/credit_approval/
    """
    curation_comments = """
        We get the data from UCI.

        - Provenance: `crx.data` of UCI Credit Approval (id 27, Quinlan 1987; the source is confidential, so lender and country are unknown). The same 690 applications are UCI's Statlog (Australian Credit Approval) (id 143) with recoded values and filled-in missing values; the Japanese Credit Screening data (id 28, 125 rows) in the same zip is a different dataset we do not use.
        - We encode A14 as numeric, following the description of it being a continuous feature.
        - We drop `A4`, a relabelled copy of `A5`: u is always g (519 rows), y always p (163), l always gg (2), and the same 6 rows are missing in both. Statlog's recoding of these applications (Australian Credit) also lacks this column.
        - Time basis: ForcedIIDFromTemporal: credit card applications decided by a bank over a period Quinlan does not state; `crx.data` has no date or id and is ordered in blocks of one class (assembly, not time), so random applications stand in for the applications to come. A dated release would allow a split by application date.
    """

    # Task
    target = "A16"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Quinlan 1987 and the Statlog Australian credit study score error rate without a cost matrix or "
            "threshold; the approve / decline use case gives no equal-cost hard-label decision. Original rejected: "
            "error rate (accuracy). roc_auc is the binary fallback."
        )
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "A1",
            "A2",
            "A3",
            "A4",
            "A5",
            "A6",
            "A7",
            "A8",
            "A9",
            "A10",
            "A11",
            "A12",
            "A13",
            "A14",
            "A15",
            "A16",
        ]
        df = pd.read_csv(raw_dir / "crx.data", header=None, names=columns, na_values="?")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["A14"] = pd.to_numeric(df["A14"], errors="coerce")
        # A4 (u, y, l) maps one to one onto A5 (g, p, gg), missing in the same rows: an exact copy.
        df = df.drop(columns=["A4"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "A1",
                "A5",
                "A6",
                "A7",
                "A9",
                "A10",
                "A12",
                "A13",
            ],
        )
