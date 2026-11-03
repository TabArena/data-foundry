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
# The year we predict, and the year before it, which only gives the history an insurer holds at the renewal.
YEAR, HISTORY_YEAR = 2006, 2005
# A car of the year before: same household, model year and submodel (`Vehicle` is no stable id, see the notes).
VEHICLE_KEY = ["Household_ID", "Model_Year", "Blind_Submodel"]
TARGET = "log1p_claim_amount"


class AllstateClaimPredictionChallenge1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much will an insured vehicle cost Allstate in bodily-injury liability claims in 2006, on the scale "
            "Allstate adjusted the amounts to, from the vehicle's characteristics and the household's record of 2005?"
        ),
        use_case=(
            "For example, Allstate rating a vehicle for bodily-injury liability cover at the 2006 renewal: the "
            "vehicle's expected claim cost ranks its risk and sets the vehicle part of the premium, with the "
            "household's record of the year before, as an insurer prices a renewal. The competition names the target "
            "and the features, not the decision."
        ),
        row=(
            "One vehicle insured by Allstate in 2006 (4.4 million vehicle-years of 2.8 million households in the "
            "competition's labelled file, of which whole households holding 1.5 million vehicle-years are sampled); "
            "the rows of 2005 give only the history."
        ),
        predicted=(
            "The vehicle's bodily-injury liability claim payments in 2006, adjusted by Allstate to remove known "
            "non-vehicle effects by a rule it did not disclose, so in no currency: 0 for 99.29% of the vehicle-years. "
            "Shipped as log1p, scored on the amount."
        ),
        known=(
            "The vehicle's model year and blinded make, model and submodel, 18 anonymised vehicle characteristics, 5 "
            "anonymised characteristics of the policy, and from 2005: the household's vehicles and claims, how many "
            "of its cars were already insured, and this car's claims (missing for a new household)."
        ),
        split=(
            "All vehicles of a household stay on one side, so the test data stands for households not seen in "
            "training, from the same year; the competition scored 2008 and 2009, whose claims were never published."
        ),
        changes=(
            "We kept the 2006 rows with the household's and the car's 2005 record as counts; dropped 2007, whose large "
            "claims look unsettled, and one exact copy; sampled whole households to the row budget; dropped the row "
            "number, the vehicle's number in the household, the year and Cat10 to Cat12, which behave like random "
            "draws; and coded the source's missing values as missing."
        ),
        fit="approximate",
        fit_reason=(
            "Vehicle and policy attributes and the household's record of the year before, as at the renewal. But the "
            "amounts' adjustment is undisclosed, no exposure is published, unseen vehicle series go untested, and 72% "
            "of the rows have a missing value the application never has. Kaggle's winners reached a Gini of 0.20 on "
            "2009 against our 0.02 to 0.10 per fold, mostly because this Gini turns on a few large claims."
        ),
    )

    # Dataset
    unique_name = "allstate_claim_prediction_challenge_1m"
    version_of = "allstate_claim_prediction_challenge"
    version_comment = """
        We sub-sample the 2006 rows to 1.5M by whole households and use grouped 3-fold cross-validation, so every fold trains on about 1M and tests on about 500k rows (v2 split protocol). The households are drawn at random, not stratified (a regression target), so the claim rate stays that of 2006. The 2005 history is built on the full file before the sampling.
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
        We start with train_set.csv of the Kaggle competition (13,184,290 vehicle-years of 2005 to 2007; the 4,314,865 test rows of 2008 and 2009 were never labelled publicly) and keep the 4,447,729 vehicle-years of 2006 (2,844,270 households, 31,690 claims), with 2005 as their history (decision 1; Andrej, 2026-11-03: "2006 renewal book with the 2005 history (counts)").

        - Prediction point: when a vehicle's year of bodily-injury liability cover is rated at the 2006 renewal. The vehicle and the policy's characteristics and the household's record of 2005 are known then; the year's claims are not. The features are anonymised vehicle and policy characteristics (data page); their timing cannot be checked further (LEAK-38).
        - The 2005 history (LEAK-10, LEAK-34): `household_vehicles_2005` and `household_claims_2005` (the household's vehicle-years and the ones with a claim; missing for the 27.4% of rows whose household is new), `vehicle_insured_2005` (the car was insured in 2005: same household, model year and submodel, as `Vehicle` is no stable id), `vehicle_claims_2005` (that car's vehicle-years with a claim; missing when it was not insured) and `household_vehicles_carried` (the household's cars of 2006 insured in 2005, all on the policy at the renewal). In 2006 a household that claimed in 2005 claims at 1.50%, a known household without a claim at 0.78%, a new household at 0.50%; a car that claimed in 2005 at 1.89%. The rating date within the year is not published, so a 2005 claim reported after an early 2006 renewal counts as known; the share cannot be measured (as in spanish_homeowners_motor_insurance_2010_2014). On 1.5M rows of 2006 sampled as shipped, the history lifts untuned LightGBM's ranking of claims from 0.112-0.117 to 0.126-0.137 (normalized Gini on claim yes/no); on the amount the change stays within the noise (0.025-0.104 either way).
        - The 2005 claim amounts are not a feature: the file gives them as read years after the renewal, and bodily-injury amounts keep growing for years (the 2007 claims above 2,000 are a third as frequent as in 2005, decision 2), so they hold more than the insurer saw at the renewal. spanish_homeowners_motor_insurance_2010_2014 keeps its previous-year home claim cost, a short-tail cover. Their gain here was within the noise (+0.001 to +0.014).
        - Target `log1p_claim_amount`, log1p of `Claim_Amount`: the vehicle's claim payments of the year, "adjusted to control for known non-vehicle effects" (data page) by an undisclosed rule, so "it isn't actually in units of any major currency" (Allstate, forum thread 928; USE-5). Scored on the amount (`target_transform="log1p"`, MET-3), as in frempl_french_motor_personal_line; the competition's normalized Gini on the amount (Andrej, 2026-11-03, issue 4: A).
        - 99.29% of the 2006 rows are 0 (none negative; Huangfu 2015, Sec. 2.0, p. 6: "only 95,605 non-zero values (about 0.73%) among the 13,184,290 records"). Little signal, decided by a few large claims (median claim 46.6, 99th percentile 2,210): on 1.5M rows of 2006 sampled as shipped, untuned LightGBM with the history scores a normalized Gini of 0.046 to 0.103 over nine folds of three random household splits (mean 0.070, standard deviation 0.019); random predictions have a standard deviation of 0.019 to 0.032 per fold.
        - Kaggle's leaderboard (0.2016 for the winner on 2009) is far above these folds. Most of the gap is the claims' tail: scored on claim yes/no instead of the amount, the same predictions reach about twice the Gini, and the tail of Kaggle's test years cannot be measured, as their amounts were never published. Tuning, ensembles and twice the training rows are the rest (review, issue 4).
        - The 2007 rows are dropped (LEAK-24, MET-2; decision 2; confirmed by Andrej on 2026-11-03; 2007 can come back with settled amounts): at the same claim rate and median claim as 2005 and 2006, their large claims are missing. Claims above 2,000 are 0.43% of the 2007 claims against 1.31% and 1.26%, in every band of vehicle age and each of the three largest makes, and the shortfall grows toward the tail (2007 against 2005: 1.01 at the median, 0.65 at the 99th and 0.59 at the 99.9th percentile). Large bodily-injury claims are paid over years and the release gives no valuation date, so the 2007 payments are probably incomplete.
        - Missing values: the source's "?" becomes missing. 71.6% of the 2006 rows have one; Cat2 (36.9% missing) is missing by model year (decision 3). The source removed such records from its test file and asked that models not use missingness, as "when the model is applied, all of the features will be collected" (forum thread 826), so the benchmark tests rows the application never sees (USE-8). On the 2005-2006 build, missingness carried no outcome beyond the vehicle type (a leave-one-out test by the review panel), random draws in place of the missing values scored no better, and training on complete rows only scored worse, so the rows stay; complete rows only would drop most vehicles built before 2000.
        - No exposure is published: a row is a vehicle in a calendar year, and some are part years (vehicles of model year 2007 can only have been insured for part of 2006; 1.4% of the rows, claiming at 0.25% against 0.71% overall). The target is the year's payments, not a rate per year insured.
        - One exact copy dropped (household 6365215's vehicle 4 in 2006, twice). Once the vehicle number and Cat10 to Cat12 are gone, 32,324 rows of 2006 (0.73%) repeat another row of the same household in every column, such as two vehicles of one type on one policy; a household is on one side of every fold, so they never straddle a split.
        - `Row_ID` (the file's row number) and `Vehicle` dropped: the vehicle's number within its household "may not apply to the same vehicle from year to year" (data page), and its values run over every vehicle the household insured at any time in the year, including cars added after the rating, among them replacements after the row's own crash (LEAK-10). The household's count of vehicles in the year was dropped for the same reason (vehicles already insured the year before claim at 1.05% when the count rose, 0.77% otherwise); the 2005 counts take its place. `Calendar_Year` has one value and goes.
        - Cat10, Cat11 and Cat12 dropped (PROV-3, CLEAN-22): the same vehicle keeps its value from one year to the next only as often as a random redraw would, and their Cramér's V with every other column and with the claim is at most 0.0024, so they are not the vehicle characteristics the data page names.
        - `Household_ID` is the group column, never a feature.
        - Dtypes: the blinded make, model and submodel (74, 1,230 and 2,550 levels in 2006), Cat1 to Cat9, OrdCat, NVCat and the flag `vehicle_insured_2005` categorical (CLEAN-14); the rest numeric. OrdCat, the "ordered categorical vehicle variable" (data page), is categorical as the ordinals of liberty_mutual_fire_peril_loss_cost and pricing_game_2017_french_mtpl: its claim rates over the levels 1 to 7 (0.21%, 0.80%, 0.57%, 0.70%, 0.63%, 0.57%, 0.14%) show no risk order.
        - Note: NVCat and NVVar1 to NVVar4 are the policy's non-vehicle characteristics, for which the host expected no "main effects" but "interactions with the vehicle variables" (data page). Kept.
        - Potential leak, kept on purpose (LEAK-30, weak): Var1 to Var8 and NVVar1 to NVVar4 are "mean 0 stdev 1" (data dictionary), yet over the labelled file their means are -0.065 to +0.019 and their standard deviations 0.97 to 1.04, so the host scaled them over a population we do not know, which may have taken in the test years. The yearly means of Var1 to Var8 rise from 2005 to 2007 (Var2 from -0.154 to +0.013) as the fleet's model-year mix changes; NVVar1 to NVVar4 do not rise. One shift and one scale per column; the unscaled values were never published.
        - Note: 82.9% of the 2006 rows share every feature with a row of another household (one vehicle type, policy profile and history): natural repeats, kept (LEAK-18).
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
            One group is a household, "a household identification number that allows year-to-year tracking of each household" (data page): its rows are its insured vehicles of 2006 (2,844,270 households, 1 to 18 rows, 1.56 on average), which share the household's 2005 record. The competition trained on 2005-2007 and scored 2008 and 2009. One target year cannot give the windows of a temporal split (see the splits), so whole households are held out: a test household is new to the model, and its history comes from 2005, as for every row. Each vehicle-year is one prediction from its own row. The label is one per vehicle-year, so it can differ within a household; 98.2% of the households with two or more rows have no claim or claims of one amount, because claims are rare.
        """,
    )
    splits_comment = """
        Default splits, grouped by household (Household_ID): 3 folds over 1.5M rows of whole households drawn at random from the 4.4M of 2006 (claim rate 0.71%, as in that year), each training on about 1M and testing on about 500k rows with about 3,500 claims. The task is temporal by its use case: the competition gave 2005-2007 for training and scored 2008 (public leaderboard) and 2009 (final ranking), whose claims were never published. With 2007 dropped (its large claims look unsettled) and 2005 used as the history of 2006, one labelled target year is left, so no window of a temporal split exists and the task ships under SPLIT-8 (ForcedGroupedFromTemporal): the folds hold out whole households, whose vehicles share the household's record, so random rows would put a household's other cars on both sides. Before the history was built, trained on 2005 and scored on 2006 the rows reached 0.064, inside the range of the folds by household (0.022 to 0.054 then, 0.046 to 0.103 now with the history), so the forced split shows no cost this noise can measure. What the folds do not test: vehicle series not seen in training (0.02% of test rows on the earlier folds), and a rating at a known date within the year. A release with dates beyond 2007 should get a temporal split. Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine"; 2026-11-03: the 2006 renewal book).
    """

    # Splits
    subsample_to_budget = True
    accepted_check_warnings = {
        "splits_rows_never_tested": (
            "The v2 protocol caps each test fold at 500k rows; the folds by household overshoot by whole "
            "households, so 240 of the 1.5M rows are trimmed from a test fold (2026-11-01)."
        ),
        "groups_labels_constant": (
            "The label is one per vehicle-year and claims are rare (0.71%), so 98.2% of the households with two or "
            "more rows of 2006 have a single label (2026-11-03)."
        ),
        "task_target_value_dominant": (
            "A zero-inflated target, not a cap or a placeholder: 0 is a vehicle-year without a bodily-injury claim, "
            "99.29% of the 2006 rows (see the curation notes; 2026-11-03)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # 2.7 GB of text: read with polars (POLARS_MAX_THREADS caps it), the text columns as categories.
        raw = pl.read_csv(raw_dir / "train_set.csv", infer_schema_length=100_000)
        return raw.with_columns(pl.col(TEXT_COLUMNS).cast(pl.Categorical)).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The rows of 2006; 2005 gives the history only, and 2007 lacks the large claims (decision 2).
        before = raw[raw["Calendar_Year"] == HISTORY_YEAR]
        df = raw[raw["Calendar_Year"] == YEAR].copy()
        # 2. The one row that repeats another in every column but Row_ID (a household's vehicle-year twice).
        df = df[~df.duplicated(subset=[c for c in df.columns if c != "Row_ID"], keep="first")]
        # 3. The 2005 history, known at the 2006 renewal: the household's cars and claims, and this car's claims.
        #    Counts only: the 2005 amounts were read years after the renewal (issue 3). Missing for a new household,
        #    and the car's claims for a car not insured in 2005.
        before = before.assign(claim=before["Claim_Amount"] > 0)
        household = before.groupby("Household_ID", observed=True)["claim"].agg(
            household_vehicles_2005="size", household_claims_2005="sum"
        )
        vehicle = before.groupby(VEHICLE_KEY, observed=True)["claim"].sum().rename("vehicle_claims_2005")
        df = df.merge(household, left_on="Household_ID", right_index=True, how="left", validate="many_to_one")
        df = df.merge(vehicle, left_on=VEHICLE_KEY, right_index=True, how="left", validate="many_to_one")
        df["vehicle_insured_2005"] = df["vehicle_claims_2005"].notna().astype("int8")
        df["household_vehicles_carried"] = df.groupby("Household_ID", observed=True)["vehicle_insured_2005"].transform(
            "sum"
        )
        # 4. The source's missing value "?" (data page) becomes missing; the categories sorted, so the codes do not
        #    depend on the order of first appearance in the file. OrdCat's levels 1 to 7 show no risk order.
        for col in CATEGORICAL:
            levels = sorted(str(v) for v in df[col].cat.categories if v != "?")
            df[col] = df[col].cat.set_categories(levels)
        # 5. The target on the log1p scale (the metric inverts it: target_transform="log1p").
        assert (df["Claim_Amount"] >= 0).all()
        df[TARGET] = np.log1p(df.pop("Claim_Amount"))
        # 6. The file's row number; the vehicle's number within the household, which "may not apply to the same
        #    vehicle from year to year" (data page) and carries the household's vehicles of the whole year; the year,
        #    one value now; Cat10 to Cat12. Household_ID stays as the group column.
        return drop_columns(df.reset_index(drop=True), ["Row_ID", "Vehicle", "Calendar_Year", *RANDOM_LIKE])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[*CATEGORICAL, "vehicle_insured_2005"])

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
        # From here on the target year and its history.
        kept = raw[raw["Calendar_Year"] == YEAR]
        claim = kept["Claim_Amount"] > 0
        claim_df = df[TARGET] > 0
        # The 2006 claim rate by the household's and the car's 2005 record.
        known = df["household_vehicles_2005"].notna()
        classes = {
            "household claimed in 2005": known & (df["household_claims_2005"] > 0),
            "household known, no claim in 2005": known & (df["household_claims_2005"] == 0),
            "new household": ~known,
            "car claimed in 2005": df["vehicle_claims_2005"].fillna(0) > 0,
            "car insured in 2005, no claim": df["vehicle_claims_2005"] == 0,
            "car not insured in 2005": df["vehicle_insured_2005"].astype(int) == 0,
        }
        history = pd.DataFrame(
            {
                "vehicle-years": {k: int(m.sum()) for k, m in classes.items()},
                "share of rows (%)": {k: round(100 * m.mean(), 2) for k, m in classes.items()},
                "claim rate 2006 (%)": {k: round(100 * claim_df[m].mean(), 3) for k, m in classes.items()},
            }
        ).rename_axis("2005 record")
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
                "2006 rows, with 2005 as their history",
                "An insurer rates a renewal on the household's record of the year before; with 2007 dropped, 2006 is "
                "the one year that has one, so its rows are the task and 2005 gives the counts of vehicles and claims "
                "(LEAK-10: counts only, the 2005 amounts were read years later). One target year has no window for a "
                "temporal split, so whole households are held out (SPLIT-8).",
                history,
            ),
            Decision(
                "The 2007 rows are dropped",
                "The claim rate and the median claim are stable over the years, the upper tail of 2007 is not: large "
                "bodily-injury claims are paid over years, and the release gives no date at which the amounts were "
                "read, so the 2007 payments are probably incomplete (LEAK-24).",
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
