"""Curated dataset definition for `in_vehicle_coupon_recommendation` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    anonymize_ids,
    decode,
)

RESPONDENT_COLUMNS = [
    "gender",
    "age",
    "maritalStatus",
    "has_children",
    "education",
    "occupation",
    "income",
    "car",
    "Bar",
    "CoffeeHouse",
    "CarryAway",
    "RestaurantLessThan20",
    "Restaurant20To50",
]
"""Answers to the survey's first part (demographics and habits), asked once per respondent."""


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "age": [
        "below 21",
        "21 to 25",
        "26 to 30",
        "31 to 35",
        "36 to 40",
        "41 to 45",
        "46 to 49",
        "50 or older",
    ],  # open-ended
    "education": [
        "Some High School",
        "High School Graduate",
        "Some college - no degree",
        "Associates degree",
        "Bachelors degree",
        "Graduate degree (Masters or Doctorate)",
    ],
    "income": [
        "Less than $12500",
        "$12500 - $24999",
        "$25000 - $37499",
        "$37500 - $49999",
        "$50000 - $62499",
        "$62500 - $74999",
        "$75000 - $87499",
        "$87500 - $99999",
        "$100000 or More",
    ],  # open-ended
    "Bar": ["never", "less1", "1~3", "4~8", "gt8"],  # open-ended
    "CoffeeHouse": ["never", "less1", "1~3", "4~8", "gt8"],  # open-ended
    "CarryAway": ["never", "less1", "1~3", "4~8", "gt8"],  # open-ended
    "RestaurantLessThan20": ["never", "less1", "1~3", "4~8", "gt8"],  # open-ended
    "Restaurant20To50": ["never", "less1", "1~3", "4~8", "gt8"],  # open-ended
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "age": {
        "below21": "below 21",
        "21": "21 to 25",
        "26": "26 to 30",
        "31": "31 to 35",
        "36": "36 to 40",
        "41": "41 to 45",
        "46": "46 to 49",
        "50plus": "50 or older",
    },
}


class InVehicleCouponRecommendation(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a driver accept a coupon for a nearby venue offered in the car?",
        use_case=(
            "An in-vehicle recommender decides whether to show a driver a coupon for a nearby bar, coffee house, "
            "take-away or restaurant, for a new user it has no history for."
        ),
        row=(
            "One imagined driving scenario with a coupon offer, answered by one Amazon Mechanical Turk respondent "
            "(12,684 answers of 587 respondents, mostly 22 each)."
        ),
        predicted="Whether the respondent says they would accept the coupon; 56.8% say yes.",
        known=(
            "The scenario (destination, passengers, weather, temperature, time of day, coupon type and expiry, "
            "distance to the venue and whether it lies on the way), the person's profile (sex, age, family, "
            "education, job, income) and how often they say they visit such venues."
        ),
        split="Whole respondents are held out, so the test data stands for new users.",
        changes=(
            "We rebuild the respondent from the file's blocks of identical profiles and hold out whole respondents; "
            "with random rows a model learned each person's habit of saying yes (ROC AUC 0.83 against 0.76)."
        ),
        fit="approximate",
        fit_reason=(
            "The answers are stated intentions about imagined trips, given in one survey sitting by Mechanical Turk "
            "volunteers, not coupons accepted by the drivers of a recommender, and the respondents are rebuilt from "
            "the file order (587 against the paper's 652 surveys)."
        ),
    )

    # Dataset
    unique_name = "in_vehicle_coupon_recommendation"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Other",  # the authors' ResearchGate deposit, cited in Wang et al. (2017) Sec. 6; UCI 603 is a copy
            url="https://www.researchgate.net/publication/318645502_in-vehicle_coupon_recommendation",
            license="CC BY 4.0",
            year="2017",
            bibtex="""
                @article{wang2017bayesian,
                  title={A bayesian framework for learning rule sets for interpretable classification},
                  author={Wang, Tong and Rudin, Cynthia and Doshi-Velez, Finale and Liu, Yimin and Klampfl, Erica and MacNeille, Perry},
                  journal={Journal of Machine Learning Research},
                  volume={18},
                  number={70},
                  pages={1--37},
                  year={2017}
                }
            """,
        ),
        Source(
            role="copy",
            platform="UCI",
            url="https://doi.org/10.24432/C5GS4P",
            license="CC BY 4.0",
            name="UCI 603",
        ),
    )
    download_description = """
        We download UCI's copy (https://doi.org/10.24432/C5GS4P) of the data the authors deposited on ResearchGate,
        and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/in_vehicle_coupon_recommendation/ && wget -P local-data-warehouse/in_vehicle_coupon_recommendation/ https://archive.ics.uci.edu/static/public/603/in+vehicle+coupon+recommendation.zip && unzip local-data-warehouse/in_vehicle_coupon_recommendation/in+vehicle+coupon+recommendation.zip -d local-data-warehouse/in_vehicle_coupon_recommendation/
    """
    curation_comments = """
        - We renamed the target feature and its value to be more descriptive.
        - We removed text data from the "time" feature to make it numeric.
        - We drop constant columns.
        - We fixed a typo in the feature names.
        - `direction_opp` dropped (2026-11-11, Andrej, review issue 1; CLEAN-5): it is 1 minus `direction_same` in all
          12,684 rows, a copy of the same flag. The nested distance flags `toCoupon_GEQ15min` and `toCoupon_GEQ25min`
          stay separate (CLEAN-13).
        - Anomaly: the data has many binned numeric features that are treated as categorical features with text describing the bins.
        - Anomaly: the numeric features in the dataset are low-cardinality (<25)
        - Time basis: Timeless: each row is one scenario of a fixed questionnaire, answered in the same sitting as the
          profile (Wang et al. 2017, Sec. 6.2), so nothing in a row arrives later and no answer is in the future of
          another. The file has no timestamp; its order is the questionnaire versions (Coffee House coupons fall from
          38-43% of the first three deciles to 13.5% of the last), and the acceptance drift that remains after the
          scenario cells are removed is 3-4 percentage points over the file (Spearman -0.034, 2026-11-06). Not tested: a
          later cohort of drivers, and whether a stated yes becomes a redemption.
        - We simulate a cold-start model (as used before a recommender has any history for a user): predict whether a person accepts a coupon from their profile, stated habits and the scenario, for people not seen in training. The data is a survey (Wang et al. 2017, Sec. 6.2): each MTurk respondent first gave demographics and preferences, then answered hypothetical driving scenarios (22 per person in the file, 19 fixed questionnaire versions), all in one sitting and without timestamps, so there is no real interaction history for a warm-start setting. A random split puts about two-thirds of each person's other answers in train, which lets a model learn that person's tendency to say yes (ROC AUC 0.83 random vs 0.76 grouped; leak audit 2026-09-24).
        - The respondent id is not shipped with the data. The raw file lists each respondent's answers as a consecutive block with identical first-part answers, so a block of the same profile is one respondent: 587 blocks, 517 of them with 22 rows, against 652 accepted surveys in the paper, so a few blocks likely merge two adjacent respondents with identical profiles, which only makes the grouping stricter. The paper reports out-of-sample AUC from 5-fold testing (Table 3) without saying whether folds were split by respondent; a random split would be a warm start.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 8 columns are ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); 1 of them decoded from the source's codes
          into its words (`CODE_LABELS`, 2026-11-01).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 1 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order.
    """

    # Task
    target = "AcceptCoupon"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC (out-of-sample, 5-fold, Table 3)",
        reference=(
            "Wang et al. (2017), A Bayesian framework for learning rule sets for interpretable "
            "classification, JMLR 18(70), Sec. 6.2 and Table 3"
        ),
        definition="Area under the ROC curve on AcceptCoupon.",
    )
    grouping = Grouping(
        on="respondent",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a survey respondent; its rows are the coupon offers in about 20 driving scenarios, answered in one sitting (Wang et al. 2017). The use case is an in-vehicle recommender for a new user (cold start), so each offer is one prediction, made from its own row; without timestamps, a warm start cannot be simulated.
        """,
    )

    data_tags = ("Timeless",)

    # Splits
    splits_comment = """
        Grouped splits on the survey respondent: all answers of one person stay on one side, so the task is a cold-start
        model that predicts a new person's response from their profile, stated habits and the driving scenario.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/in-vehicle-coupon-recommendation.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # The raw file lists each respondent's answers as one consecutive block with the same first-part answers;
        # a block is one respondent (or, rarely, two adjacent respondents with identical answers)
        profile = df[RESPONDENT_COLUMNS].astype("string").fillna("nan").agg("|".join, axis=1)
        block = (profile != profile.shift()).cumsum()
        df["respondent"] = anonymize_ids(block.astype(str))
        target_feature = "AcceptCoupon"
        df = df.rename(columns={"Y": target_feature})
        df[target_feature] = df[target_feature].map({0: "No", 1: "Yes"})
        # Transform time to 24-hour format to be fully numeric.
        df["time"] = (
            df["time"]
            .apply(lambda x: int(x.replace("AM", "")) if "AM" in x else int(x.replace("PM", "")) + 12)
            .astype(int)
        )
        # Drop the constant column, and `direction_opp`, which is 1 - `direction_same` in every row (CLEAN-5)
        df = df.drop(columns=["toCoupon_GEQ5min", "direction_opp"])
        df = df.rename(columns={"passanger": "passenger"})
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "respondent",
                "expiration",
                "destination",
                "passenger",
                "weather",
                "coupon",
                "gender",
                "age",
                "maritalStatus",
                "has_children",
                "education",
                "occupation",
                "income",
                "car",
                "Bar",
                "CoffeeHouse",
                "CarryAway",
                "RestaurantLessThan20",
                "Restaurant20To50",
                "toCoupon_GEQ15min",
                "toCoupon_GEQ25min",
                "direction_same",
            ],
        )
