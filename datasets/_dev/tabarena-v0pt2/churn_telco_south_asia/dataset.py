"""Curated dataset definition for `churn_telco_south_asia` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary

RAW_FILE = "South Asian Wireless Telecom Operator (SATO 2015).csv"
"""The one file of the Kaggle dataset mahreen/sato2015; OpenML 44227 holds the same values."""


class ChurnTelcoSouthAsia(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a mobile subscriber leave the operator?",
        use_case=(
            "After two months of usage, a South Asian mobile operator scores each subscriber for the risk of leaving,"
            " to target retention offers."
        ),
        row=(
            "One subscriber of a South Asian wireless operator, with usage over August and September 2015: 1,000 who "
            "left and 1,000 who stayed, chosen by design (Ahmed et al. 2017)."
        ),
        predicted=(
            "Whether the subscriber churned (half did, by design); when the churn was observed is not documented."
        ),
        known=(
            "Time on the network and the two months' totals of revenue (overall, SMS, data, within and outside the "
            "network), data volume, calls and complaints, plus each month's service type (2G, 3G) and the other "
            "network called most."
        ),
        split=(
            "Random subscribers, so the test data stands for other subscribers of the same operator over the same two"
            " months."
        ),
        fit="approximate",
        fit_reason=(
            "Possibly problematic, kept for now: neither paper says when the churn was observed. We read it as "
            "following the two months; if it fell inside them, the usage totals end at the outcome and the task "
            "detects leaving instead of predicting it. The 50% churn share is set by design."
        ),
    )

    # Dataset
    unique_name = "churn_telco_south_asia"
    year = "2017"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/mahreen/sato2015"
    license = "CC0-1.0"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We download the Kaggle dataset mahreen/sato2015, uploaded on 2017-10-11 by the Kaggle user mahreen (OpenML
        lists the creator as MAHREENAHMED), whose data card cites the paper that introduced the data. It holds one
        file (CC0-1.0); Kaggle does not version-pin a download, so check the hash. OpenML 44227
        (https://www.openml.org/d/44227, file 22106812) holds the same 2,000 rows with identical values and serves as
        the fallback.
        South Asian Wireless Telecom Operator (SATO 2015).csv: sha256 70f135b52bd31c3b5b42473d0fcb42651727a9680af0644735f4176c87cda8fe

        mkdir -p local-data-warehouse/churn_telco_south_asia && cd local-data-warehouse/churn_telco_south_asia
        kaggle datasets download mahreen/sato2015 && unzip sato2015.zip && rm sato2015.zip
    """
    bibtex = """
        @inproceedings{ahmed2017mcs,
          title = {{MCS}: Multiple classifier system to predict the churners in the telecom industry},
          author = {Ahmed, Mehreen and Siddiqi, Imran and Afzal, Hammad and Khan, Behram},
          booktitle = {2017 Intelligent Systems Conference (IntelliSys)},
          pages = {678--683},
          year = {2017},
          organization = {IEEE},
          doi = {10.1109/IntelliSys.2017.8324367}
        }
    """
    curation_comments = """
        We start with South Asian Wireless Telecom Operator (SATO 2015).csv (2,000 rows, 14 columns) from the Kaggle dataset mahreen/sato2015 (CC0-1.0), the data of Ahmed et al. (IntelliSys 2017). OpenML 44227 is the same file.

        - Prediction point: after two months of usage (August and September 2015), the operator scores each subscriber for the risk of churning, to target retention offers.
        - Potential leak, kept on purpose (Lennart, 2026-10-15): this task may be problematic. When the churn was observed is not documented; neither paper says (IntelliSys 2017, Sec. III; Neural Computing and Applications 2020, Sec. 3.1). If the churners left inside August-September, the two months' totals end at the outcome and a model detects leaving instead of predicting it, the reason iranian_churn was retired. We keep it for now and read the churn as after the window: the near-inactive subscribers are almost all churners, but a random forest reaches ROC AUC 0.805 on those with more than 5 calls (0.815 on all). Revisit if the authors or the operator date the churn.
        - Cohort: 1,000 churners and 1,000 active subscribers by design, so the 50% base rate is artificial; ROC AUC, the metric here, does not depend on it.
        - IID split: each row is a different subscriber over the same two months; the file holds no time index or id, and no two rows share a feature vector.
        - The split is forced (ForcedIIDFromTemporal, SPLIT-8): the operator would train on subscribers of an earlier window, whose churn is known, and score the next, but the release holds one window of two usage months. A dated earlier window would test whether a model still ranks churners after usage and the network mix shift (the September move to ufone below); the cost cannot be measured here. Recover further windows if the authors release them.
        - Target: Class renamed churn_status (Churned, Active).
        - aug_user_type, sep_user_type (2G, 3G, Other), aug_fav_a and sep_fav_a (the other network called most in each month) are categorical; the other nine columns stay numeric.
        - Anomaly: Aggregate_ONNET_REV plus Aggregate_OFFNET_REV is a median 22 times Aggregate_Total_Rev, so their unit is not rupees and is not documented; kept as published. Every complaint count is at least 1 (an offset or the cohort; kept).
        - Anomaly: network_age (days on the network) is negative for 5 churners (-8 to -2, consecutive raw rows); impossible, so missing.
        - Anomaly: the raw file joins extracts, each sorted by network_age; six short runs hold churners only (54 rows). Each run of 60 rows or more scores ROC AUC 0.757 to 0.888 when held out, so the split stays IID.
        - Anomaly: aug_fav_a is "0" for 59 subscribers, an undocumented code (September has none). All 59 have off-net revenue and at least 8 calls, so it is not "no call to another network" but an unknown network: missing.
        - Note: the September favourite network moves towards ufone, among active subscribers more (decision table). The share rises with calls in both classes (lowest to highest fifth: 0.40 to 0.93 active, 0.18 to 0.80 churned), so it follows activity, not a recording that differs by class.
        - Note: churn_telco_south_asia_duplicate (DSN Telecoms Churn 2018) is this file with renamed networks.
        - Year: 2017, the first publication; the data were collected in 2015.
    """

    # Task
    target = "churn_status"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The first publication (closed access, abstract elided) could not be read; no metric "
            "verified. Cohort is 50/50 by design, so accuracy (the likely reported number) would be close"
            " in spirit, but AUC is insensitive to the artificial base rate as the curation notes say."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.rename(columns={"Class": self.target})
        # days on the network cannot be negative (5 churners, -8 to -2): missing
        df["network_age"] = df["network_age"].where(df["network_age"] >= 0)
        # "0" is not a network: an undocumented code for subscribers who did call other networks, so unknown
        df["aug_fav_a"] = df["aug_fav_a"].mask(df["aug_fav_a"].eq("0"))
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["aug_user_type", "sep_user_type", "aug_fav_a", "sep_fav_a"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        months = pd.DataFrame(
            {
                f"{month} favourite, {status}": df.loc[df[self.target].eq(status), column].value_counts(dropna=False)
                for status in ("Active", "Churned")
                for month, column in (("August", "aug_fav_a"), ("September", "sep_fav_a"))
            }
        ).fillna(0)
        months = months.astype("int64")
        months.index = months.index.astype("string").fillna("missing")
        return [
            Decision(
                "Favourite networks kept, although September shifts towards ufone",
                "Both classes move towards ufone from August to September, the active subscribers more. The share rises "
                "with the number of calls in both classes, and at equal calls both keep their August network equally "
                "often, so the shift follows activity, not a recording that differs by class.",
                months,
            ),
        ]
