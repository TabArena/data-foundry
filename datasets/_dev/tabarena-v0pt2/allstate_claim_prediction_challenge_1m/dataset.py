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
    RowBudget,
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


def _year_with_history(raw: pd.DataFrame) -> pd.DataFrame:
    """The vehicle-years of 2006, each once, with the 2005 history an insurer holds at the 2006 renewal (all cars)."""
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
    df["vehicle_insured_2005"] = df["vehicle_claims_2005"].notna()
    df["household_vehicles_carried"] = df.groupby("Household_ID", observed=True)["vehicle_insured_2005"].transform(
        "sum"
    )
    return df


class AllstateClaimPredictionChallenge1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much will a vehicle renewed for 2006 cost Allstate in bodily-injury liability claims that year, on "
            "the scale Allstate adjusted the amounts to, from the vehicle's characteristics and the household's "
            "record of 2005?"
        ),
        use_case=(
            "For example, Allstate rating a vehicle for bodily-injury liability cover at the 2006 renewal: the "
            "vehicle's expected claim cost ranks its risk and sets the vehicle part of the premium, with the "
            "household's record of the year before, as an insurer prices a renewal. The competition names the target "
            "and the features, not the decision."
        ),
        row=(
            "One vehicle on an Allstate policy at the start of 2006, insured in 2005 too: the renewal book, 2.75 "
            "million of the 4.4 million vehicle-years of 2006 in the competition's labelled file, of which whole "
            "households holding 1.5 million are sampled. The cars that joined during 2006 are left out, and the rows "
            "of 2005 give only the history."
        ),
        predicted=(
            "The vehicle's bodily-injury liability claim payments in 2006, adjusted by Allstate to remove known "
            "non-vehicle effects by a rule it did not disclose, so in no currency: 0 for 99.18% of the vehicle-years. "
            "Shipped as log1p, scored on the amount."
        ),
        known=(
            "The vehicle's model year and blinded make, model and submodel, 18 anonymised vehicle characteristics, 5 "
            "anonymised characteristics of the policy, and from 2005: the household's vehicles and claims, how many "
            "of its cars are on the policy at the renewal, and this car's claims."
        ),
        split=(
            "All vehicles of a household stay on one side, so the test data stands for renewing households not seen "
            "in training, from the same year; the competition scored 2008 and 2009, whose claims were never published."
        ),
        changes=(
            "We kept the 2006 cars insured in 2005 (the renewal book) with their 2005 record as counts, without the "
            "cars that joined in 2006; dropped 2007, whose large claims look unsettled, and one exact copy; sampled "
            "whole households to the row budget; dropped the row number, the vehicle's number in the household, the "
            "year and Cat10 to Cat12, which behave like random draws; and coded missing values as missing."
        ),
        fit="approximate",
        fit_reason=(
            "Vehicle and policy attributes and the household's record of the year before, for the renewed cars. But "
            "the amounts' adjustment is undisclosed, no exposure is published, new business and unseen vehicle series "
            "go untested, and 73% of rows have a missing value the application never has. Kaggle's winners reached "
            "0.20 Gini on 2009 against our 0.06 to 0.11 per fold, as this Gini turns on a few large claims."
        ),
    )

    # Dataset
    unique_name = "allstate_claim_prediction_challenge_1m"
    version_of = "allstate_claim_prediction_challenge"
    version_comment = """
        We sub-sample the 2006 renewal book (2.75M rows) to 1.5M by whole households and use grouped 3-fold cross-validation, so every fold trains on about 1M and tests on about 500k rows (v2 split protocol). The households are drawn at random, not stratified (a regression target), so the claim rate stays that of the book. The 2005 history is built on the full file before the filter and the sampling.
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
        We start with train_set.csv of the Kaggle competition (13,184,290 vehicle-years of 2005 to 2007; the 4,314,865 test rows of 2008 and 2009 were never labelled publicly) and keep the renewal book of 2006: the 2,754,936 cars insured in 2005 too, 61.9% of the 4,447,729 vehicle-years of 2006 (1,942,447 households, 22,632 claims), with 2005 as their history (decision 1; Andrej, 2026-11-03: "2006 renewal book with the 2005 history (counts)"; Lennart, 2026-11-08: "Option B: The renewal book.").

        - Prediction point: when a vehicle on the policy at the start of 2006 is rated for its year of bodily-injury liability cover at the 2006 renewal. The vehicle and the policy's characteristics and the household's record of 2005 are known then; the year's claims are not. The features are anonymised vehicle and policy characteristics (data page); their timing cannot be checked further (LEAK-38).
        - The renewal book (MET-14, LEAK-41; Lennart, 2026-11-08, review issue 6: B): the cars that joined during 2006, 38.1% of its vehicle-years (a new household's car, 27.4%, or a car added by a household of 2005, 10.7%), are left out, as their start is not released and they were on risk for part of the year. Followed into 2007, they claim per row in 2006 at 0.46 and 0.54 times their own 2007 rate (0.45 to 0.59 in every band of model-year age, 0.31 to 0.35 for model year 2007, the latest of them), while the cars carried from 2005 claim at 0.98 times theirs (0.91 to 1.11 by band), and 2007 repeats the shares and rates (review panel, 2026-11-08; decision 1). A target per row would price a part year for them, and no rate per year insured can be built without an exposure. The filter reads a fact of 2005, known at the renewal, never whether a car is seen in 2007. Before it, the flag `vehicle_insured_2005` alone scored a normalized Gini of 0.046 to 0.052, half or more of untuned LightGBM's 0.058 to 0.102 on all rows; the flag is now constant and gone. A car added in 2006 with the model year and submodel of a car of 2005 cannot be told apart from it: 38,728 rows of the book (1.41%) share a key that has more rows in 2006 than in 2005 (claiming at 0.69% against 0.82%), and they stay, as dropping them would select on the cars added later in the year. New business is not tested.
        - The 2005 history (LEAK-10, LEAK-34): `household_vehicles_2005` and `household_claims_2005` (the household's vehicle-years and the ones with a claim), `vehicle_claims_2005` (this car's vehicle-years with a claim; the car is matched on household, model year and submodel, as `Vehicle` is no stable id) and `household_vehicles_carried` (the household's cars on the policy at the 2006 renewal, those insured in 2005 too; in the book, its number of rows). None is missing in the book. In 2006 a car whose household claimed in 2005 claims at 1.56%, one whose household did not at 0.81%; a car that claimed in 2005 at 1.89%. The rating date within the year is not published, so a 2005 claim reported after an early 2006 renewal counts as known; the share cannot be measured (as in spanish_homeowners_motor_insurance_2010_2014). On the shipped folds the history lifts untuned LightGBM from 0.097 / 0.079 / 0.056 to 0.106 / 0.091 / 0.061 on the amount, and by 0.001 to 0.003 on claim yes/no, each within one standard deviation of random predictions; `household_vehicles_carried` adds 0.001 to 0.009 of that on 3 of 3 folds (on all rows it had lowered the score by 0.004 to 0.009). On all rows the history had lifted the Gini on claim yes/no from 0.112-0.117 to 0.126-0.137; most of that lift was the shorter term of the cars that joined during 2006.
        - The 2005 claim amounts are not a feature: the file gives them as read years after the renewal, and bodily-injury amounts keep growing for years (the 2007 claims above 2,000 are a third as frequent as in 2005, decision 2), so they hold more than the insurer saw at the renewal. spanish_homeowners_motor_insurance_2010_2014 keeps its previous-year home claim cost, a short-tail cover. Their gain on all rows of 2006 was within the noise (+0.001 to +0.014).
        - Target `log1p_claim_amount`, log1p of `Claim_Amount`: the vehicle's claim payments of the year, "adjusted to control for known non-vehicle effects" (data page) by an undisclosed rule, so "it isn't actually in units of any major currency" (Allstate, forum thread 928; USE-5). Scored on the amount (`target_transform="log1p"`, MET-3), as in frempl_french_motor_personal_line; the competition's normalized Gini on the amount (Andrej, 2026-11-03, issue 4: A).
        - 99.18% of the book's rows are 0 (none negative; Huangfu 2015, Sec. 2.0, p. 6: "only 95,605 non-zero values (about 0.73%) among the 13,184,290 records"). Little signal, decided by a few large claims (median claim 41.8, 99th percentile 2,161): untuned LightGBM scores a normalized Gini of 0.106 / 0.091 / 0.061 on the shipped folds, where a constant scores 0 and random predictions have a standard deviation of 0.023 to 0.025, and 0.022 to 0.106 over nine folds of three random household splits (mean 0.069, standard deviation 0.024). The task probe, on sides capped at 200,000 rows, finds LightGBM above the dummy on 3 of 3 splits (+0.037, SE 0.004) and its linear model and random forest at chance.
        - Kaggle's leaderboard (0.2016 for the winner on 2009) is far above these folds. Most of the gap is the claims' tail: scored on claim yes/no instead of the amount, the same predictions reach about twice the Gini, and the tail of Kaggle's test years cannot be measured, as their amounts were never published. Tuning, ensembles and twice the training rows are the rest (review, issue 4).
        - The 2007 rows are dropped (LEAK-24, MET-2; decision 2; confirmed by Andrej on 2026-11-03; 2007 can come back with settled amounts): at the same claim rate and median claim as 2005 and 2006, their large claims are missing. Claims above 2,000 are 0.43% of the 2007 claims against 1.31% and 1.26%, in every band of vehicle age and each of the three largest makes, and the shortfall grows toward the tail (2007 against 2005: 1.01 at the median, 0.65 at the 99th and 0.59 at the 99.9th percentile). Large bodily-injury claims are paid over years and the release gives no valuation date, so the 2007 payments are probably incomplete.
        - Missing values: the source's "?" becomes missing. 73.0% of the book's rows have one; Cat2 (39.6% missing) is missing by model year (decision 3). The source removed such records from its test file and asked that models not use missingness, as "when the model is applied, all of the features will be collected" (forum thread 826), so the benchmark tests rows the application never sees (USE-8). On the 2005-2006 build, missingness carried no outcome beyond the vehicle type (a leave-one-out test by the review panel), random draws in place of the missing values scored no better, and training on complete rows only scored worse, so the rows stay; complete rows only would drop most vehicles built before 2000.
        - One exact copy dropped (household 6365215's vehicle 4 in 2006, twice). Once the vehicle number and Cat10 to Cat12 are gone, 22,720 rows of the book (0.82%) repeat another row of the same household in every column, such as two vehicles of one type on one policy; a household is on one side of every fold, so they never straddle a split.
        - `Row_ID` (the file's row number) and `Vehicle` dropped: the vehicle's number within its household "may not apply to the same vehicle from year to year" (data page), and its values run over every vehicle the household insured at any time in the year, including cars added after the rating, among them replacements after the row's own crash (LEAK-10). The household's count of vehicles in the year was dropped for the same reason (vehicles already insured the year before claim at 1.05% when the count rose, 0.77% otherwise); the 2005 counts take its place. `Calendar_Year` has one value and goes.
        - Cat10, Cat11 and Cat12 dropped (PROV-3, CLEAN-22): the same vehicle keeps its value from one year to the next only as often as a random redraw would, and their Cramér's V with every other column and with the claim is at most 0.0024, so they are not the vehicle characteristics the data page names.
        - `Household_ID` is the group column, never a feature.
        - Dtypes: the blinded make, model and submodel (73, 1,167 and 2,379 levels in the book), Cat1 to Cat9, OrdCat and NVCat categorical (CLEAN-14); the rest numeric. OrdCat, the "ordered categorical vehicle variable" (data page), is categorical as the ordinals of liberty_mutual_fire_peril_loss_cost and pricing_game_2017_french_mtpl: its claim rates in the book over the levels 1 to 7 (0.14%, 0.91%, 0.71%, 0.81%, 0.74%, 0.66%, 0.24%) show no risk order.
        - Note: NVCat and NVVar1 to NVVar4 are the policy's non-vehicle characteristics, for which the host expected no "main effects" but "interactions with the vehicle variables" (data page). Kept.
        - Potential leak, kept on purpose (LEAK-30, weak): Var1 to Var8 and NVVar1 to NVVar4 are "mean 0 stdev 1" (data dictionary), yet over the labelled file their means are -0.065 to +0.019 and their standard deviations 0.97 to 1.04, so the host scaled them over a population we do not know, which may have taken in the test years. The yearly means of Var1 to Var8 rise from 2005 to 2007 (Var2 from -0.154 to +0.013) as the fleet's model-year mix changes; NVVar1 to NVVar4 do not rise. One shift and one scale per column; the unscaled values were never published.
        - Note: 81.8% of the book's rows share every feature with a row of another household (one vehicle type, policy profile and history): natural repeats, kept (LEAK-18).
        - Note: the competition rules say "Participants will not use the data for purposes unrelated to the competition"; a 2022 forum question about the licence (thread 309810) has no answer.
        - Exposure (LEAK-41, MET-14; 2026-11-06, measured 2026-11-08): the release publishes no exposure; the rows are vehicle-years of the cars on the policy at the start of 2006 (the cars that joined during the year are left out, above), some cut short by a claim. The book's cars gone by 2007 had claimed at 0.98% in 2006, against 0.72% for the cars still insured; among the cars of households that continued into 2007, at 1.39% against 0.72%, as a claim ends the cover (a write-off or a replacement), while the cars whose whole household left claimed at 0.81%. Without dates a cut cannot be told from a non-renewal, so the share cut short is only bounded: at most 39.3% of the book's cars are not seen in 2007 (28.0% with their whole household), and 15.8% of the cars of households that continued are gone (11.4% of the book); without an exposure, the most a price per year would differ cannot be bounded. For these cuts the target stays per contract, the insurer's cost of the cover it wrote (Lennart, 2026-11-08, review issue 7: confirmed): a rate per year would raise the cut rows further, and none can be built. No feature carries the cut: the in-year vehicle count, which the outcome cuts, is already dropped, and `household_vehicles_carried` counts the cars on the policy from 2005 whatever their claims. The Kaggle metric is an unweighted Gini, so no weight is declared. If a later release adds an exposure, it is a realized time on risk: the rate's denominator and weight, never a feature.
        - Note: how mature the labels are (cross-dataset item of 2026-11-09, Andrej): `Claim_Amount` is the year's bodily-injury "claim payments" (description page), adjusted, as read at the release (about 2011, the file's date; no valuation date is given). The file gives no closure date or status, so the share still open at the 2006 renewal cannot be counted; the large claims missing from 2007 (the bullet on 2007) show payments still growing years later. Every fold trains and tests on 2006 rows of one extract, so both sides carry the same maturity (splits_comment).
        - Note: held for training rows only, not shipped (cross-dataset item of 2026-11-09, Andrej): `Vehicle`, the car's number within its household, whose values run over every car the household insured during the year, and the household's count of cars in the year, built from the rows, which counts the cars added after the rating, replacements after a crash among them (10.7% of the 2006 vehicle-years are cars a household of 2005 added during the year). Allstate holds both for the rows of a past year when it fits, but not for a car it rates at the renewal. They would need a training-only role, which the format does not have yet (MET-14, LEAK-41, MET-16), so they stay out for now.
        - CC (2026-11-09, Andrej): the folds test on all rows of the renewal book, the gaps kept as missing (review issue 8, A, as implemented); the missing-values bullet names the mismatch with the competition's complete test rows.
        - CC (2026-11-09, Andrej): the split stays by household over the 2006 book (review issue 9, A, as implemented); the splits comment gives the 2005-to-2006 score as above the household folds of that build and names the training side's year and the maturity of its amounts.
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
            One group is a household, "a household identification number that allows year-to-year tracking of each household" (data page): its rows are its vehicles of the 2006 renewal book (1,942,447 households, 1 to 11 rows, 1.42 on average), which share the household's 2005 record. The competition trained on 2005-2007 and scored 2008 and 2009. One target year cannot give the windows of a temporal split (see the splits), so whole households are held out: a test household is new to the model, and its history comes from 2005, as for every row. Each vehicle-year is one prediction from its own row. The label is one per vehicle-year, so it can differ within a household; 98.2% of the households with two or more rows of the book have no claim or claims of one amount, because claims are rare.
        """,
    )
    splits_comment = """
        Default splits, grouped by household (Household_ID): 3 folds over 1.5M rows of whole households drawn at random from the 2.75M of the 2006 renewal book (claim rate 0.82%, as in the book), each training on about 1M and testing on about 500k rows with 4,006 to 4,210 claims. The task is temporal by its use case: the competition gave 2005-2007 for training and scored 2008 (public leaderboard) and 2009 (final ranking), whose claims were never published. With 2007 dropped (its large claims look unsettled) and 2005 used as the history of 2006, one labelled target year is left, so no window of a temporal split exists and the task ships under SPLIT-8 (ForcedGroupedFromTemporal): the folds hold out whole households, whose vehicles share the household's record, so random rows would put a household's other cars on both sides. Before the history was built, trained on 2005 and scored on 2006 all rows reached 0.064, above the folds by household of that build (0.022 to 0.054) and inside the nine folds of the renewal book (0.022 to 0.106), so the forced split shows no cost this noise can measure. The training rows are the test year's other households, their amounts read at the release (about 2011, the file's date), more developed than Allstate had at the 2006 renewal, when it would have trained on 2005 and earlier; both sides of every fold hold amounts of the same maturity. What the folds do not test: new business (the cars that joined during 2006 are left out), vehicle series not seen in training (0.02% of test rows on the earlier folds), and a rating at a known date within the year. A release with dates beyond 2007 should get a temporal split. Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine"; 2026-11-03: the 2006 renewal book; Lennart, 2026-11-08: only the cars on the policy at the start of 2006; Andrej, 2026-11-09: the split by household stays).
    """

    # Splits
    row_budget = RowBudget(train=1_000_000, test=500_000)
    accepted_check_warnings = {
        "groups_labels_constant": (
            "The label is one per vehicle-year and claims are rare (0.82%), so 98.2% of the households with two or "
            "more rows of the 2006 renewal book have a single label (2026-11-03; restated 2026-11-08)."
        ),
        "task_target_value_dominant": (
            "A zero-inflated target, not a cap or a placeholder: 0 is a vehicle-year without a bodily-injury claim, "
            "99.18% of the rows of the 2006 renewal book (see the curation notes; 2026-11-03; restated 2026-11-08)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # 2.7 GB of text: read with polars (POLARS_MAX_THREADS caps it), the text columns as categories.
        raw = pl.read_csv(raw_dir / "train_set.csv", infer_schema_length=100_000)
        return raw.with_columns(pl.col(TEXT_COLUMNS).cast(pl.Categorical)).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1 to 3. The vehicle-years of 2006 with their 2005 history (see `_year_with_history`).
        df = _year_with_history(raw)
        # 4. The renewal book (decision 1; Lennart, 2026-11-08): only the cars on the policy at the start of 2006,
        #    those insured in 2005 too. The cars that joined during 2006 were on risk for part of it, a term the
        #    release does not give, so their year's payments price no year of cover (MET-14). The filter reads a fact
        #    of 2005, known at the renewal, never whether the car is seen in 2007 (LEAK-41); its flag is then constant
        #    and leaves, and the history is never missing.
        df = df[df.pop("vehicle_insured_2005")].copy()
        # 5. The source's missing value "?" (data page) becomes missing; the categories sorted, so the codes do not
        #    depend on the order of first appearance in the file. OrdCat's levels 1 to 7 show no risk order.
        for col in CATEGORICAL:
            levels = sorted(str(v) for v in df[col].cat.categories if v != "?")
            df[col] = df[col].cat.set_categories(levels)
        # 6. The target on the log1p scale (the metric inverts it: target_transform="log1p").
        assert (df["Claim_Amount"] >= 0).all()
        df[TARGET] = np.log1p(df.pop("Claim_Amount"))
        # 7. The file's row number; the vehicle's number within the household, which "may not apply to the same
        #    vehicle from year to year" (data page) and carries the household's vehicles of the whole year; the year,
        #    one value now; Cat10 to Cat12. Household_ID stays as the group column.
        return drop_columns(df.reset_index(drop=True), ["Row_ID", "Vehicle", "Calendar_Year", *RANDOM_LIKE])

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
        # From here on the target year and its history, every car of 2006 before the renewal book is kept.
        year = _year_with_history(raw)
        claim_year = year["Claim_Amount"] > 0
        # The same cars one year later: their 2007 rows, for the cars whose key has as many rows in 2007 as in 2006.
        after = raw[raw["Calendar_Year"] == YEAR + 1].assign(claim=lambda t: t["Claim_Amount"] > 0)
        later = after.groupby(VEHICLE_KEY, observed=True)["claim"].agg(rows_2007="size", claims_2007="sum")
        year = year.merge(later, left_on=VEHICLE_KEY, right_index=True, how="left")
        followed = year["rows_2007"] == year.groupby(VEHICLE_KEY, observed=True)["Household_ID"].transform("size")
        # The 2006 claim rate by the car's and the household's 2005 record; the renewal book is the first class.
        known, carried = year["household_vehicles_2005"].notna(), year["vehicle_insured_2005"]
        classes = {
            "car insured in 2005 (kept)": carried,
            "car added by a household of 2005 (dropped)": known & ~carried,
            "car of a new household (dropped)": ~known,
            "kept: household claimed in 2005": carried & (year["household_claims_2005"] > 0),
            "kept: household without a claim in 2005": carried & (year["household_claims_2005"] == 0),
            "kept: car claimed in 2005": carried & (year["vehicle_claims_2005"] > 0),
            "kept: car without a claim in 2005": carried & (year["vehicle_claims_2005"] == 0),
        }
        history = pd.DataFrame(
            {
                "vehicle-years": {k: int(m.sum()) for k, m in classes.items()},
                "share of the 2006 rows (%)": {k: round(100 * m.mean(), 2) for k, m in classes.items()},
                "claim rate 2006 (%)": {k: round(100 * claim_year[m].mean(), 3) for k, m in classes.items()},
                "cars followed into 2007": {k: int((m & followed).sum()) for k, m in classes.items()},
                "their 2006 rate / their 2007 rate": {
                    k: round(
                        claim_year[m & followed].mean()
                        / (year.loc[m & followed, "claims_2007"].sum() / year.loc[m & followed, "rows_2007"].sum()),
                        2,
                    )
                    for k, m in classes.items()
                },
            }
        ).rename_axis("2005 record")
        # The missing values of the renewal book, before the sampling.
        kept = year[carried]
        claim = kept["Claim_Amount"] > 0
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
                "The 2006 renewal book, with 2005 as its history",
                "An insurer rates a renewal on the household's record of the year before; with 2007 dropped, 2006 is "
                "the one year that has one, and 2005 gives the counts of vehicles and claims (LEAK-10: counts only, the "
                "2005 amounts were read years later). Only the cars insured in 2005 too stay, the cars on the policy at "
                "the start of 2006 (Lennart, 2026-11-08): the cars that joined during 2006 claim per row at about half "
                "the rate the same cars show in 2007, so they were on risk for part of the year, a term the release "
                "does not give (MET-14). The filter reads a fact of 2005, never whether a car is seen in 2007 "
                "(LEAK-41). One target year has no window for a temporal split, so whole households are held out "
                "(SPLIT-8).",
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
