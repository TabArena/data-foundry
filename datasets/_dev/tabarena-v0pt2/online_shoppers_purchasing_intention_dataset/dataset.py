"""Curated dataset definition for `online_shoppers_purchasing_intention_dataset` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, decode

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Month": ["June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}


class OnlineShoppersPurchasingIntentionDataset(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a visit to an online shop end in a purchase?",
        use_case=(
            "While a visitor browses, the online shop estimates whether the visit will end in a purchase, to decide "
            'whether to show an offer or other content (the source\'s "real-time prediction").'
        ),
        row=(
            "One visit to an online shop, each by a different user, sampled over one year; we keep June to December "
            "(6,875 visits)."
        ),
        predicted="Whether the visit ended in a purchase (1,348 of 6,875 visits, 20%).",
        known=(
            "How many administrative, informational and product pages the visit opened and how long it spent on them,"
            " the pages' bounce, exit and value figures from the shop's analytics, the month, weekend, new or "
            "returning visitor, operating system, browser, region and traffic source."
        ),
        split="Random visits of the same months.",
        changes=(
            "We keep only June to December: before June every buyer's page value is above zero and alone separates "
            "buyers almost perfectly, which suggests it counts the visit's own purchase."
        ),
        fit="approximate",
        fit_reason=(
            "Each row summarises the finished visit, while the shop must act during it, and whether the page values "
            "still carry the visits' own purchases cannot be proven (alone they reach ROC AUC 0.814 on the kept "
            "months)."
        ),
    )

    # Dataset
    unique_name = "online_shoppers_purchasing_intention_dataset"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5F88Q",
            license="CC BY 4.0",
            year="2018",
            bibtex="""
                @article{sakar2019real,
                  title={Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM recurrent neural networks},
                  author={Sakar, C Okan and Polat, S Olcay and Katircioglu, Mete and Kastro, Yomi},
                  journal={Neural Computing and Applications},
                  volume={31},
                  number={10},
                  pages={6893--6908},
                  year={2019},
                  publisher={Springer}
                }
            """,
        ),
    )
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/online_shoppers_purchasing_intention_dataset/ && wget -P local-data-warehouse/online_shoppers_purchasing_intention_dataset/ http://archive.ics.uci.edu/static/public/468/online+shoppers+purchasing+intention+dataset.zip && unzip local-data-warehouse/online_shoppers_purchasing_intention_dataset/online+shoppers+purchasing+intention+dataset.zip -d local-data-warehouse/online_shoppers_purchasing_intention_dataset/ && rm local-data-warehouse/online_shoppers_purchasing_intention_dataset/online+shoppers+purchasing+intention+dataset.zip
    """
    curation_comments = """
        - Anomaly: the data contains time-based features that were preprocessed to create a time-invariant predictive task.
        - We keep only the sessions from June to December (6,875 of 12,330). "PageValues" is meant as a historical Google Analytics metric per page, stored and updated at regular intervals, averaged over the pages a session visits (Sakar et al. 2019, Sec. 2.1). In February, March and May, however, every one of the 560 buyers has PageValues > 0 and PageValues alone separates buyers with ROC AUC 0.974, so these values most likely include the session's own purchase (the page-value table was probably computed over that period). From June on, 27% of buyers have PageValues = 0 and its AUC is 0.814, as expected for a historical page metric. We keep PageValues and drop the early months; this cannot be proven from the data, as a change in site tracking would leave a similar pattern.
        - We drop "SpecialDay": it is non-zero only in February and May, so it is constant on the kept months.
        - We keep the IID split: each session belongs to a different user, sampled over one year (Sakar et al. 2019, Sec. 2.1), and only the month is known.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`).
        - The target (2026-11-01, CLEAN-25): `Revenue` ships its classes as words (True means revenue). Binary: "Yes" is
          the event, the class that sorts second, so it is the metrics' positive class.
        - Time basis: ForcedIIDFromTemporal: the visit month (June to December of one year) is in the data and the shop
          scores later visits; not split by month, because only December can train on half of the visits (June to
          November, 75%; November would train on 31%) and the file order within a month is not the order of days, so
          three windows do not exist; testing December on June to November costs 0.009 ROC AUC at equal training
          size (untuned LightGBM 0.889 against 0.898; logistic regression +0.002). Each session belongs to a
          different user (Sakar et al. 2019, Sec. 2.1). Not tested: later months, and the shift in the purchase share
          between months (10% in June to 25% in November).
    """

    # Task
    target = "Revenue"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Sakar et al. 2019 report accuracy, TPR, TNR and F1 (F1 stressed over accuracy, full text paywalled); no "
            "fixed threshold or costs. Original rejected: F1. roc_auc is the binary fallback."
        )
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/online_shoppers_intention.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw[~raw["Month"].isin(["Feb", "Mar", "May"])]
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"False": "No", "True": "Yes"}})
        return df.drop(columns=["SpecialDay"]).reset_index(drop=True)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "Month",
                "OperatingSystems",
                "Browser",
                "Region",
                "TrafficType",
                "VisitorType",
                "Weekend",
            ],
        )
