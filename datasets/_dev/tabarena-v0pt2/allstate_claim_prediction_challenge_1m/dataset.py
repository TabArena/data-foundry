"""Curated dataset definition for `allstate_claim_prediction_challenge_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    TaskSummary,
    drop_columns,
)

# The text columns of train_set.csv, all categories (OrdCat too); the source codes a missing value as "?".
TEXT_COLUMNS = [
    "Blind_Make",
    "Blind_Model",
    "Blind_Submodel",
    *[f"Cat{i}" for i in range(1, 13)],
    "OrdCat",
    "NVCat",
]
# Cat10 to Cat12 behave like random draws (see the notes), so they leave.
RANDOM_LIKE = ["Cat10", "Cat11", "Cat12"]
CATEGORICAL = [c for c in TEXT_COLUMNS if c not in RANDOM_LIKE]
LAST_YEAR = 2006
TARGET = "log1p_claim_amount"


class AllstateClaimPredictionChallenge1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much will an insured vehicle cost Allstate in bodily-injury liability claims over a calendar year, "
            "on the scale Allstate adjusted the amounts to, from the vehicle's characteristics?"
        ),
        use_case=(
            "For example, Allstate rating a vehicle for bodily-injury liability cover when a policy year starts: the "
            "vehicle's expected claim cost ranks its risk and sets the vehicle part of the premium. The competition "
            "names the target and the features, not the decision."
        ),
        row=(
            "One vehicle insured by Allstate in one calendar year, 2005 or 2006 (8.5 million vehicle-years of 3.4 "
            "million households in the competition's labelled file once 2007 is dropped, of which whole households "
            "holding 1.5 million vehicle-years are sampled)."
        ),
        predicted=(
            "The vehicle's bodily-injury liability claim payments in that year, adjusted by Allstate to remove known "
            "non-vehicle effects by a rule it did not disclose, so in no currency: 0 for 99.27% of the vehicle-years. "
            "Shipped as log1p, scored on the amount."
        ),
        known=(
            "The calendar year, the vehicle's model year and blinded make, model and submodel, 18 anonymised vehicle "
            "characteristics, and 5 anonymised characteristics of the policy."
        ),
        split=(
            "All vehicle-years of a household stay on one side, so the test data stands for households not seen in "
            "training, from the same two years; the competition scored 2008 and 2009, whose claims were never "
            "published."
        ),
        changes=(
            "We dropped the 2007 rows, whose large claims look unsettled, and one exact copy of a row; sampled whole "
            "households down to the row budget; dropped the row number, the vehicle's number within the household "
            "and three vehicle columns that behave like random draws (Cat10 to Cat12); and coded the source's missing "
            "values as missing."
        ),
        fit="approximate",
        fit_reason=(
            "Vehicle and policy attributes known at pricing, and the vehicle's own claims. But the amounts' "
            "adjustment is undisclosed and no exposure is published. Held-out households of the same years stand in "
            "for next year's book, so known households (53% in the competition's test file), their claim history "
            "and unseen vehicle series go untested; 73% of the rows have a missing value, which the application "
            "never has."
        ),
    )

    # Dataset
    unique_name = "allstate_claim_prediction_challenge_1m"
    version_of = "allstate_claim_prediction_challenge"
    version_comment = """
        We sub-sample the frame to 1.5M rows by whole households and use grouped 3-fold cross-validation, so every fold trains on about 1M and tests on about 500k rows (v2 split protocol). The households are drawn at random, not stratified (a regression target), so the claim rate stays that of 2005-2006.
    """
    year = "2011"
    domain = "insurance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/ClaimPredictionChallenge"
    license = "Kaggle Competition Rules"
    data_tags = ("ForcedGroupedFromTemporal", "Anonymized")
    download_description = """
        We use train_set.csv of the Kaggle competition (2005-2007); the test rows of 2008 and 2009 were never labelled publicly.

        kaggle competitions download -c ClaimPredictionChallenge -f train_set.zip && unzip train_set.zip && rm train_set.zip
        sha256sum train_set.csv  # e8809676c72e976c659687bc35c0f132c651e77e691b50b9baf7128112019679
        mkdir -p local-data-warehouse/allstate_claim_prediction_challenge && mv train_set.csv local-data-warehouse/allstate_claim_prediction_challenge/
    """
    bibtex = r"""
        @misc{Allstate2011ClaimPredictionChallenge,
          author = {{Allstate Insurance Company}},
          title = {Allstate Claim Prediction Challenge},
          year = {2011},
          howpublished = {\url{https://www.kaggle.com/competitions/ClaimPredictionChallenge}},
          note = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with train_set.csv of the Kaggle competition (13,184,290 vehicle-years of 2005 to 2007; the 4,314,865 test rows of 2008 and 2009 were never labelled publicly) and keep 2005 and 2006: 8,473,402 vehicle-years of 3,445,943 households, 61,838 claims.

        - Prediction point: when a vehicle's year of bodily-injury liability cover is rated. The vehicle and the policy's characteristics are known then; the year's claims are not. The features are anonymised vehicle and policy characteristics (data page); their timing cannot be checked further (LEAK-38).
        - Target `log1p_claim_amount`, log1p of `Claim_Amount`: the vehicle's claim payments of the year, "adjusted to control for known non-vehicle effects" (data page) by an undisclosed rule, so "it isn't actually in units of any major currency" (Allstate, forum thread 928; USE-5). Scored on the amount (`target_transform="log1p"`, MET-3), as in frempl_french_motor_personal_line. Trained on the amount instead, untuned LightGBM scores a normalized Gini of 0.001 to 0.035 on the shipped folds, against 0.022 to 0.054 on the log1p scale; the review panel's own sample of the same definition found no winner (0.038 to 0.068 against 0.050 to 0.089).
        - 99.27% of the rows are 0 (none negative; Huangfu 2015, Sec. 2.0, p. 6: "only 95,605 non-zero values (about 0.73%) among the 13,184,290 records"; 0.72% claims in the shipped 1.5M rows). Only the claim part carries signal, and little of it: on the shipped folds untuned LightGBM reaches a normalized Gini of 0.053 / 0.054 / 0.022 (bootstrap standard error 0.022 to 0.029; random predictions average -0.002 to 0.004 with a standard deviation of 0.019 to 0.025) at R^2 -0.004 to -0.003 on the log1p scale, and ranks claims at ROC AUC 0.56. A regularised LightGBM classifier of whether a claim occurs scores 0.065 / 0.060 / 0.039.
        - The 2007 rows are dropped (LEAK-24, MET-2; decision 2): at the same claim rate and median claim as 2005 and 2006, their large claims are missing. Claims above 2,000 are 0.43% of the 2007 claims against 1.31% and 1.26%, in every band of vehicle age and each of the three largest makes, and the shortfall grows toward the tail (2007 against 2005: 1.01 at the median, 0.65 at the 99th and 0.59 at the 99.9th percentile). Large bodily-injury claims are paid over years and the release gives no valuation date, so the 2007 payments are probably incomplete. Pooled test folds over the three years also rewarded learning each year's claim level from other households: a predictor that knew only the year scored 0.055 to 0.058. On the two kept years the year column is a feature; the model's pooled score exceeds its score within each year by -0.000 to +0.001, and a year-only predictor scores 0.001 to 0.026.
        - Missing values: the source's "?" becomes missing. 73.0% of the shipped rows have one; Cat2 is missing by model year (decision 3). The source removed such records from its test file and asked that models not use missingness, as "when the model is applied, all of the features will be collected" (forum thread 826), so the benchmark tests rows the application never sees (USE-8). Missingness carries no outcome beyond the vehicle type (a leave-one-out test by the review panel). Random draws in place of the missing values score 0.047 / 0.052 / 0.008 against 0.053 / 0.054 / 0.022, complete and incomplete test rows show no consistent gap (0.039 / 0.079 / -0.034 against 0.059 / 0.049 / 0.044), and training on complete rows only scores worse (0.045 / -0.029 / -0.020), so the rows stay; complete rows only would keep 27% of them and few vehicles built before 2000 (47.9% of the 2005-2006 rows, 13.8% of their complete rows, 8.6% of the competition's test file).
        - No exposure is published: a row is a vehicle in a calendar year, and some are part years (vehicles whose model year is the next calendar year can only have been insured for part of it; they claim at 0.20% against 0.73% overall). The target is the year's payments, not a rate per year insured.
        - One exact copy dropped (household 6365215's vehicle 4 in 2006, twice); three vehicle-years that appear twice with differing values are kept. Once the vehicle number and Cat10 to Cat12 are gone, 10,946 shipped rows (0.7%) repeat another row of the same household in every column, such as two vehicles of one type on one policy; a household is on one side of every fold, so they never straddle a split.
        - `Row_ID` (the file's row number) and `Vehicle` dropped: the vehicle's number within its household "may not apply to the same vehicle from year to year" (data page), and its values run over every vehicle the household insured at any time in the year, including cars added after the rating, among them replacements after the row's own crash (LEAK-10). The household's count of vehicles in the year, which an earlier draft built in its place, was dropped for the same reason: vehicles added since the previous year claim at 1.17% when the count rose and at 0.72% otherwise, and the column added 0.015 to 0.020 Gini on the earlier folds.
        - Cat10, Cat11 and Cat12 dropped (PROV-3, CLEAN-22): the same vehicle keeps its value from one year to the next only as often as a random redraw would, and their Cramér's V with every other column and with the claim is at most 0.0024, so they are not the vehicle characteristics the data page names.
        - `Household_ID` is the group column, never a feature.
        - Dtypes: the blinded make, model and submodel (74, 1,237 and 2,569 levels in 2005-2006), Cat1 to Cat9, OrdCat and NVCat categorical; the rest numeric. OrdCat, the "ordered categorical vehicle variable" (data page), is categorical as the ordinals of liberty_mutual_fire_peril_loss_cost and pricing_game_2017_french_mtpl (CLEAN-14): its claim rates over the levels 1 to 7 (0.32%, 0.82%, 0.60%, 0.72%, 0.64%, 0.60%, 0.11%) show no risk order.
        - Note: NVCat and NVVar1 to NVVar4 are the policy's non-vehicle characteristics, for which the host expected no "main effects" but "interactions with the vehicle variables" (data page). Kept.
        - Potential leak, kept on purpose (LEAK-30, weak): Var1 to Var8 and NVVar1 to NVVar4 are "mean 0 stdev 1" (data dictionary), yet over the labelled file their means are -0.065 to +0.019 and their standard deviations 0.97 to 1.04, so the host scaled them over a population we do not know, which may have taken in the test years. The yearly means of Var1 to Var8 rise from 2005 to 2007 (Var2 from -0.154 to +0.013) as the fleet's model-year mix changes; NVVar1 to NVVar4 do not rise. One shift and one scale per column; the unscaled values were never published.
        - Note: 87% of the shipped rows share every feature with a row of another household (one vehicle type and policy profile): natural repeats, kept (LEAK-18).
        - Note: the competition rules say "Participants will not use the data for purposes unrelated to the competition"; a 2022 forum question about the licence (thread 309810) has no answer.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.source(
        "normalized_gini",
        original="Normalized Gini coefficient (the public leaderboard on 2008 and the final ranking on 2009)",
        reference="https://www.kaggle.com/competitions/ClaimPredictionChallenge/overview/evaluation",
        target_transform="log1p",
    )
    grouping = Grouping(
        on="Household_ID",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a household, "a household identification number that allows year-to-year tracking of each household" (data page): its rows are its insured vehicles in each year it is in the file (3,445,943 households in 2005-2006, 1 to 27 rows, 2.5 on average). The competition trained on 2005-2007 and scored 2008 and 2009, where 53% of the test households were also in the training file (forum thread 708). Two labelled years cannot give the windows of a temporal split (see the splits), so whole households are held out instead: a test household is new, and neither of its years is in training. Each vehicle-year is one prediction from its own row. The label is one per vehicle-year, so it can differ within a household; 97.8% of the households with two or more shipped rows have no claim or claims of one amount, because claims are rare.
        """,
    )
    splits_comment = """
        Default splits, grouped by household (Household_ID): 3 folds over 1.5M rows of whole households drawn at random from the 8.5M of 2005-2006 (claim rate 0.72%, as in those years), each training on about 1M and testing on about 500k rows with 3,490 to 3,653 claims. The task is temporal by its use case: the competition gave 2005-2007 for training and scored 2008 (public leaderboard) and 2009 (final ranking), whose claims were never published. Once 2007 is dropped (see the curation notes), no yearly window keeps half the rows for training (the 2006 window trains on 2005 alone, 47.5% of the rows), below the floor of SPLIT-14, so the task ships under SPLIT-8, stacked and grouped by household (ForcedGroupedFromTemporal): households recur across the years (72.6% of the 2006 vehicle-years belong to a household of 2005), and random rows would put a household's other year on both sides. The forced split shows no cost that this noise can measure. On the full release, before 2007 was dropped, untuned LightGBM trained on 2005-2006 scored 0.084 on all 4.7M rows of 2007, against 0.059 to 0.115 on the 2007 rows of the folds by household then shipped. On the shipped rows, trained on 2005 and scored on 2006 it reaches 0.064 (0.042 to 0.101 over random thirds of the test rows), against 0.019 to 0.030 on the shipped folds' 2006 rows and 0.022 to 0.054 on all their rows (bootstrap standard error 0.022 to 0.029). Folds of random rows score -0.008 to 0.082 on the same rows. What the folds do not test: a renewal book where most households are known (53% of the competition's test households were in its training file) and their claim history counts (in the full release, vehicles of households with an earlier claim claim at 1.44%, others at 0.77%); no history feature ships, so nothing leaks either. Nor do they test vehicle series not seen in training: only 0.02% of the test rows have a model or submodel unseen in training. A release with dates beyond 2007 should get a temporal split. A leak test across the folds (2026-11-02) finds none: 84% of the test rows repeat the features of a training row of another household, but a lookup of those rows' mean target scores -0.008 / -0.008 / -0.002, no test claim repeats a training row's features and amount, and no household recurs under another id; taking the test year's rows out of training costs no more than taking out as many random rows (6 of 6 fold-years). Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine").
    """

    # Splits
    subsample_to_budget = True
    accepted_check_warnings = {
        "splits_rows_never_tested": (
            "The v2 protocol caps each test fold at 500k rows; the folds by household overshoot by whole "
            "households, so 240 of the 1.5M rows are trimmed from a test fold (2026-11-01)."
        ),
        "groups_labels_constant": (
            "The label is one per vehicle-year and claims are rare (0.72%), so 97.8% of the households with two or "
            "more rows have a single label; 9,475 of 429,370 have several (2026-11-01)."
        ),
        "task_target_value_dominant": (
            "A zero-inflated target, not a cap or a placeholder: 0 is a vehicle-year without a bodily-injury claim, "
            "99.28% of the shipped rows (see the curation notes; 2026-11-01)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # 2.7 GB of text: read with polars (POLARS_MAX_THREADS caps it), the text columns as categories.
        raw = pl.read_csv(raw_dir / "train_set.csv", infer_schema_length=100_000)
        return raw.with_columns(pl.col(TEXT_COLUMNS).cast(pl.Categorical)).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The years whose claims look complete: 2007 lacks the large claims (decision 2).
        df = raw[raw["Calendar_Year"] <= LAST_YEAR].copy()
        # 2. The one row that repeats another in every column but Row_ID (a household's vehicle-year twice).
        df = df[~df.duplicated(subset=[c for c in df.columns if c != "Row_ID"], keep="first")]
        # 3. The source's missing value "?" (data page) becomes missing; the categories sorted, so the codes do not
        #    depend on the order of first appearance in the file. OrdCat's levels 1 to 7 show no risk order.
        for col in CATEGORICAL:
            levels = sorted(str(v) for v in df[col].cat.categories if v != "?")
            df[col] = df[col].cat.set_categories(levels)
        # 4. The target on the log1p scale (the metric inverts it: target_transform="log1p").
        assert (df["Claim_Amount"] >= 0).all()
        df[TARGET] = np.log1p(df.pop("Claim_Amount"))
        # 5. The file's row number; the vehicle's number within the household, which "may not apply to the same
        #    vehicle from year to year" (data page) and carries the household's vehicles of the whole year; Cat10 to
        #    Cat12. Household_ID stays as the group column.
        return drop_columns(df, ["Row_ID", "Vehicle", *RANDOM_LIKE])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=CATEGORICAL)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        # The claims by year on the whole release: the rate and the size distribution.
        claim_all = raw["Claim_Amount"] > 0
        year_all = raw["Calendar_Year"]
        amounts = raw.loc[claim_all, "Claim_Amount"].groupby(year_all[claim_all])
        tail = pd.DataFrame(
            {
                "claim rate (%)": claim_all.groupby(year_all).mean().mul(100).round(3),
                "claims": claim_all.groupby(year_all).sum(),
                "median claim": amounts.median().round(1),
                "90th percentile": amounts.quantile(0.9).round(1),
                "99th percentile": amounts.quantile(0.99).round(1),
                "99.9th percentile": amounts.quantile(0.999).round(1),
                "claims above 2,000 (%)": (raw.loc[claim_all, "Claim_Amount"] > 2000)
                .groupby(year_all[claim_all])
                .mean()
                .mul(100)
                .round(2),
                "mean claim": amounts.mean().round(1),
            }
        ).rename_axis("Calendar_Year")
        # From here on the kept years only.
        kept = raw[raw["Calendar_Year"] <= LAST_YEAR]
        year = kept["Calendar_Year"]
        claim = kept["Claim_Amount"] > 0
        # Households by year: how many recur from an earlier year of the file.
        first_year = kept.groupby("Household_ID")["Calendar_Year"].transform("min")
        recur = pd.DataFrame(
            {
                "vehicle-years": year.value_counts().sort_index(kind="stable"),
                "share of vehicle-years (%)": year.value_counts(normalize=True)
                .sort_index(kind="stable")
                .mul(100)
                .round(1),
                "households": kept.groupby("Calendar_Year")["Household_ID"].nunique(),
                "share of vehicle-years whose household is in an earlier year": (first_year < year)
                .groupby(year)
                .mean()
                .round(3),
            }
        ).rename_axis("Calendar_Year")
        # Missing values of the shipped text columns by model year, and the claim rate with and without one.
        missing = kept[CATEGORICAL].astype("string").eq("?")
        bucket = (kept["Model_Year"] // 5 * 5).rename("Model_Year (5-year bins)")
        by_model_year = pd.DataFrame(
            {
                "vehicle-years": bucket.value_counts().sort_index(kind="stable"),
                "complete rows": (~missing.any(axis=1)).groupby(bucket).sum(),
                **{
                    f"{c} missing (%)": missing[c].groupby(bucket).mean().mul(100).round(1)
                    for c in ("Cat2", "Cat4", "Cat7")
                },
                "any missing (%)": missing.any(axis=1).groupby(bucket).mean().mul(100).round(1),
                "claim rate, complete rows (%)": claim[~missing.any(axis=1)].groupby(bucket).mean().mul(100).round(3),
                "claim rate, rows with a missing value (%)": claim[missing.any(axis=1)]
                .groupby(bucket)
                .mean()
                .mul(100)
                .round(3),
            }
        )
        return [
            Decision(
                "Grouped by household, not by year",
                "Two labelled years give no window whose train side holds half of the rows (SPLIT-14), so the years "
                "are stacked and whole households are held out (SPLIT-8); households recur across the years, so "
                "random rows would put a household's other year on both sides.",
                recur,
            ),
            Decision(
                "The 2007 rows are dropped",
                "The claim rate and the median claim are stable over the years, the upper tail of 2007 is not: large "
                "bodily-injury claims are paid over years, and the release gives no date at which the amounts were "
                "read, so the 2007 payments are probably incomplete (LEAK-24). Pooled test folds also rewarded "
                "learning each year's claim level (MET-2).",
                tail,
            ),
            Decision(
                "Missing values stay",
                "The source removed the records with a missing value from its test file and asked that models not use "
                "missingness. Cat2 is missing by model year; missingness carries no outcome beyond the vehicle type, "
                "and keeping only complete rows would drop most older vehicles.",
                by_model_year,
            ),
        ]
