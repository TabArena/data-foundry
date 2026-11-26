"""Curated dataset definition for `online_shoppers_purchasing_intention_dataset` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    TimeBasis,
    decode,
)

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
            " the pages' bounce, exit and value figures from the shop's analytics, weekend, new or returning visitor, "
            "operating system, browser, region and traffic source."
        ),
        split=(
            "Each month, June to December, is held out once and predicted from the other six (56% to 96% of the "
            "visits); the month is the group, not an input."
        ),
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
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/online_shoppers_purchasing_intention_dataset/ && wget -P local-data-warehouse/online_shoppers_purchasing_intention_dataset/ http://archive.ics.uci.edu/static/public/468/online+shoppers+purchasing+intention+dataset.zip && unzip local-data-warehouse/online_shoppers_purchasing_intention_dataset/online+shoppers+purchasing+intention+dataset.zip -d local-data-warehouse/online_shoppers_purchasing_intention_dataset/ && rm local-data-warehouse/online_shoppers_purchasing_intention_dataset/online+shoppers+purchasing+intention+dataset.zip
    """
    curation_comments = """
        - Anomaly: the data contains time-based features that were preprocessed to create a time-invariant predictive task.
        - We keep only the sessions from June to December (6,875 of 12,330). "PageValues" is meant as a historical Google Analytics metric per page, stored and updated at regular intervals, averaged over the pages a session visits (Sakar et al. 2019, Sec. 2.1). In February, March and May, however, every one of the 560 buyers has PageValues > 0 and PageValues alone separates buyers with ROC AUC 0.974, so these values most likely include the session's own purchase (the page-value table was probably computed over that period). From June on, 27% of buyers have PageValues = 0 and its AUC is 0.814, as expected for a historical page metric. We keep PageValues and drop the early months; this cannot be proven from the data, as a change in site tracking would leave a similar pattern.
        - We drop "SpecialDay": it is non-zero only in February and May, so it is constant on the kept months.
        - Leave one month out (Andrej, 2026-11-19: "Leave one month out, but this would still be ForcedGrouped"), in
          place of 3 x 3 random folds: only December can train on half the visits in time order and the file order
          within a month is not the order of days, so three time windows do not exist. `Month` is the group column and
          no model input (until 2026-11-19 it was an ordered category): a held-out month is a level the model never
          saw in training, so it would carry nothing but an unseen level.
        - 40 rows repeat another (2026-11-11, Andrej; LEAK-18, LEAK-41): one-page product visits with no time, a bounce
          and no page value, all without purchase; different users per Sakar et al. 2019, kept as natural repeats.
          The link is at chance (37 repeats, 28 to 45 in 200 shuffles of the visitor details, against 40 observed),
          and 0.7% to 0.9% of test rows have an identical row in training.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`).
        - The target (2026-11-01, CLEAN-25): `Revenue` ships its classes as words (True means revenue). Binary: "Yes" is
          the event, the class that sorts second, so it is the metrics' positive class.
    """
    split_leaf = "L-FORCED.periods"
    time_basis = TimeBasis(
        "ForcedGroupedFromTemporal",
        """
        the visits carry their month but no
        year; the stationary-relation test reads not flat (November: LightGBM +0.054 ± 0.007, Kumo-Tabular +0.039
        ± 0.004 ROC AUC, floors 0.003-0.004; the purchase share moves from 10% in June to 25% in November), so whole
        months are held out, each once. The test months are unseen, not later: each fold also trains on the months
        after its test month. That does not raise the score: for August to December, at the same training size,
        training on the other months, earlier and later, scores below training on the earlier months alone (mean over
        the five months -0.005 ROC AUC for LightGBM, -0.009 random forest, -0.014 logistic regression, -0.015 TabPFN;
        10 draws each); only November gains from later months (+0.004 to +0.010).
        """,
        set_by="Andrej",
        on="2026-11-19",
    )

    # Task
    target = "Revenue"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Sakar et al. 2019 report accuracy, TPR, TNR and F1 (F1 stressed over accuracy, full text paywalled); no "
            "fixed threshold or costs. Original rejected: F1. roc_auc is the binary fallback."
        )
    )

    # Splits
    grouping = Grouping(
        on="Month",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a calendar month of visits, June to December of one year (the year is not in the data). The shop scores visits of months its model has not seen, and the purchase share moves from month to month (10% in June to 25% in November), so whole months are held out. Each row is one visit by a different user (Sakar et al. 2019, Sec. 2.1) and one prediction, made from that visit alone.
        """,
    )
    leave_one_group_out = True
    splits_comment = """
        Leave one month out (Andrej, 2026-11-19): seven splits, one repeat, each testing one month and training on the other six. The months and their visits, each with the train side's share of the 6,875 visits: June 288 (95.8%), July 432 (93.7%), August 433 (93.7%), September 448 (93.5%), October 549 (92.0%), November 2,998 (56.4%) and December 1,727 (74.9%). A split by time is out: only December can train on half the visits in time order, and the file order within a month is not the order of days. The month is the group column and no model input. Repeats would give the same seven splits.
    """
    accepted_check_warnings = {
        "splits_dimensions_off_protocol": (
            "Decided (Andrej, 2026-11-19): leave one month out gives exactly seven splits; repeats would give the same "
            "seven."
        ),
        "groups_test_groups_few": (
            "Decided (Andrej, 2026-11-19): the seven months June to December are all the data holds, each held out "
            "once; testing one unseen month at a time is the split, and each fold still scores 288 to 2,998 visits."
        ),
        "groups_largest_share_high": (
            "November is a real month, not a catch-all value: 2,998 of the 6,875 visits (44%) as published; when it is "
            "the test month the model trains on the other six (3,877 visits, 56.4%)."
        ),
    }

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
