"""Curated dataset definition for `wisconsin_local_government_property_insurance_fund` (data-foundry v2).

Evidence: README.md.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    ScoringColumn,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

# The six entity-type flags and the four alarm-credit flags of PropertyFundInsample.csv; exactly one of each is set.
ENTITY_FLAGS = {
    "TypeCity": "City",
    "TypeCounty": "County",
    "TypeMisc": "Misc",
    "TypeSchool": "School",
    "TypeTown": "Town",
    "TypeVillage": "Village",
}
ALARM_FLAGS = {"AC00": 0, "AC05": 5, "AC10": 10, "AC15": 15}
TARGET = "bc_claims"


def _from_flags(df: pd.DataFrame, flags: dict) -> pd.Series:
    """The one category of a block of 0/1 flags in which every row has exactly one flag set."""
    block = df[list(flags)].to_numpy()
    assert (block.sum(axis=1) == 1).all()
    return pd.Series(np.array(list(flags.values()))[block.argmax(axis=1)], index=df.index)


def _two_years_in_file(df: pd.DataFrame) -> pd.Series:
    """True where the file holds the member's two policy years before the row's year."""
    keys = set(zip(df["PolicyNum"], df["Year"]))
    return pd.Series(
        [(p, y - 1) in keys and (p, y - 2) in keys for p, y in zip(df["PolicyNum"], df["Year"])], index=df.index
    )


def _rating_r2(df: pd.DataFrame) -> float:
    """R^2 of a least-squares fit of log premium on the rating variables (with intercept)."""
    design = np.column_stack(
        [
            np.ones(len(df)),
            df[["LnCoverage", "lnDeduct", "Fire5", "NoClaimCredit"]].to_numpy(float),
            df[list(ENTITY_FLAGS)[1:] + list(ALARM_FLAGS)[1:]].to_numpy(float),
        ]
    )
    log_premium = np.log(df["Premium"].to_numpy(float))
    coef, *_ = np.linalg.lstsq(design, log_premium, rcond=None)
    residual = log_premium - design @ coef
    return float(1 - residual.var() / log_premium.var())


class WisconsinLocalGovernmentPropertyInsuranceFund(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a Wisconsin local government member's building and contents claims cost the state's property "
            "fund in the coming year, from the rating variables the fund holds when it sets the year's premium?"
        ),
        use_case=(
            "The actuaries of Wisconsin's Local Government Property Insurance Fund set each county, city, town, "
            "village, school district or other member's premium relativity for the coming year. A new rating is "
            "adopted when it moves premium toward the members whose claims outrun what they pay now; the source built "
            "such a rating engine for the fund and scored it against the fund's premium."
        ),
        row=(
            "One member's building and contents cover in one year, 2006 to 2010 (5,639 member-years of 1,227 "
            "members; 1,038 members are in all five years)."
        ),
        predicted=(
            "The year's total building and contents claims, in dollars: 0 for 70% of the member-years, up to $12.9 "
            "million. A prediction is scored by how it reorders the members against the fund's premium for the year."
        ),
        known=(
            "The member itself, its type, the year's coverage amount and the deductible it chose, whether its fire protection "
            "class is below 5, its alarm credit, whether it had a claim in the two years before (unknown where the "
            "file does not hold both years), and the year."
        ),
        split=(
            "Each of the policy years 2008, 2009 and 2010 is held out in turn, and the model trains on every earlier "
            "year, as the fund rates the members it knows for the next year. The 2008 window trains on 2006-2007 "
            "alone, 41% of the rows."
        ),
        changes=(
            "We drop the claim count and the other restatements of the year's claims, keep the fund's premium out of "
            "the inputs as the yardstick of the score, and mark the no-claim credit unknown where the file lacks the "
            "member's two earlier years."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs are the rating variables the fund holds at renewal, the label is the year's claims and the "
            "test is the next year, but the training years carry final claim amounts the fund knew only in part when "
            "it rated, and the public file lacks inputs the fund rates on: the endorsements, the member's county and "
            "the full fire class."
        ),
    )

    # Dataset
    unique_name = "wisconsin_local_government_property_insurance_fund"
    year = "2017"
    domain = "insurance"
    source = "GitHub"
    source_url = (
        "https://github.com/OpenActTexts/Loss-Data-Analytics/blob/38859ed741b21d41a26b5abb668e1172c088a216/Data/"
        "PropertyFundInsample.csv"
    )
    license = None  # the shipped first edition states none; the second edition is CC0 (see meta_license_unknown)
    download_description = """
        The open textbook Loss Data Analytics (Open Actuarial Textbooks project, E.W. Frees and co-authors) ships the
        data of its Wisconsin Property Fund case study (Ch. 1) in its GitHub repository. We pin the repository's first
        commit (2017-06-27), whose two files are still the ones on master (commit 32310ad, 2026-11-01).
        PropertyFundInsample.csv holds one row per member and year, 2006-2010; Insample.csv in the same folder is a
        byte-identical copy, and WiscPropFund.csv of the second edition (OpenActTexts/LDAVer2) holds the same rows
        with fewer columns. CLAIMLEVEL.csv holds the individual claims, used only to check the yearly totals.

        mkdir -p local-data-warehouse/wisconsin_local_government_property_insurance_fund && cd local-data-warehouse/wisconsin_local_government_property_insurance_fund
        for f in PropertyFundInsample.csv CLAIMLEVEL.csv; do wget https://raw.githubusercontent.com/OpenActTexts/Loss-Data-Analytics/38859ed741b21d41a26b5abb668e1172c088a216/Data/$f; done
        sha256sum PropertyFundInsample.csv CLAIMLEVEL.csv
        # 436cc782e87b401e34d00c4d5e7cf801c683f7063c5018fc2d067c104e0b1c96  PropertyFundInsample.csv
        # e338a1bd130cb07ffdb2e6a82af8b5eef393cfc703e9a2cf90758c12c5246c95  CLAIMLEVEL.csv
    """
    bibtex = r"""
        @misc{OpenActTexts2017LossDataAnalytics,
          title = {Loss Data Analytics},
          author = {{Open Actuarial Textbooks Project}},
          year = {2017},
          howpublished = {\url{https://github.com/OpenActTexts/Loss-Data-Analytics}},
          note = {Ch. 1, Case Study: Wisconsin Property Fund; data file PropertyFundInsample.csv, first committed on 27 June 2017. The task and its metric: E.W. Frees, G. Lee and L. Yang, Multivariate Frequency-Severity Regression Models in Insurance, Risks 4(1):4, 2016, doi:10.3390/risks4010004}
        }
    """
    curation_comments = """
        We start with PropertyFundInsample.csv of the open textbook Loss Data Analytics (OpenActTexts on GitHub), the building and contents (BC) cover of Wisconsin's Local Government Property Insurance Fund, 2006-2010: a close extract of the sample Frees, Lee and Yang (2016, Risks 4:4, Sec. 5) model (5,639 member-years with 1,679 claimants, against their 5,660 and 1,684).

        - Prediction point: the start of a policy year, when the fund rates the member for the year. The member's type, the year's coverage and deductible, its fire class, its alarm credit and the no-claim credit are known then; the year's claims are not. The fund's rating project wanted "a more accurate and cost efficient rating engine" (Lee 2017, UW-Madison dissertation advised by Frees, Ch. 1).
        - Year: the rows were first published in the textbook's repository on 2017-06-27 (its first commit); Frees, Lee and Yang (2016) analyse them but publish no data, and the fund's project site offers none.
        - `Freq`, `lny` and `yAvg` dropped: the year's claim count (0 exactly where the claims are 0), the log of the claims and the average claim restate the target.
        - `BCcov` and `Deduct` dropped: `LnCoverage` is the log of the coverage in millions (within 5e-10) and `lnDeduct` the log of the deductible, the forms the source models them in (Lee 2017, Table 5.8).
        - `Premium` (the fund's premium for the year) is the base of the metric, a scoring column and never an input. The source's models take the rating variables only (Lee 2017, Table 5.8) and are scored against the premium (Frees, Lee and Yang 2016, Sec. 6.2: "The Gini index is calculated using relativities computed with the actual premium collected by the LGPIF in 2011 as the denominator, with the scores predicted by each model as numerator. This means we are looking for improvements over the original premium scores used by the LGPIF"). The premium is the output of the rating the task replaces: a linear fit on the rating variables explains 98.1-98.5% of the variance of its log within each year (decision 1). As in 2_month_survival_rate_prediction, a comparator of the source is no input (USE-6).
        - The six entity-type flags become `EntityType` and the four alarm-credit flags `AlarmCredit` (0, 5, 10 or 15% credit): exactly one flag of each block is set in every row, so the merge is lossless (CLEAN-13).
        - `PolicyNum`, the member, is an input: the fund rates the members it has insured before (USE-10), and 97.6-98.8% of each test year's members are in its training years. Its first two digits are the entity type. An untuned LightGBM Tweedie scores 0.146, 0.254 and 0.327 with it (test 2008, 2009, 2010) and 0.146, 0.221 and 0.081 without; the gap is in 2010 alone, the window in which one claim is 35% of the year's claims.
        - `NoClaimCredit` is 1 exactly when the member had no claim in the two years before, wherever both years are in the file (1,852 rows against 0, and 0 against 1,375): history known at rating time. Where the file lacks one of the two years it is 0 (all 2,292 rows of 2006-2007 and 119 of the 120 later ones; one member with a gap year has 1), which says only that the history is not in the file, and a linear model would read it as "had a claim". These 2,412 rows are set missing (CLEAN-10, as house_sales). The 2008 window trains on 2006-2007 alone, so its training side holds no known credit and the column informs only the 2009 and 2010 windows.
        - `Fire5` is 1 when the fire protection class (0 to 10) is below 5. The claim-level file, which covers claimants only, shows the unknown class -99 coded as 1 for 48 claimant members (66 member-years). It stays as published: the unknowns can be found only among members with a claim, so blanking them would tell the outcome (LEAK-10 before CLEAN-10). `Fire5` and `NoClaimCredit` hold only 0 and 1 (and missing): categorical.
        - The coverage of a year is set before its claims: the change of log coverage from the year before is +0.059 with a claim in the year and +0.061 without (+0.052 with a claim in the top 10%). It grew about 5% a year in 2007-2009; in 2010 it fell for 67.7% of the members (median -2.6%).
        - Exposure: `Premium` is the rating's output and the base of the Lorenz curve, not an amount at risk. The target is a total and the premium is set at the start of the year (not realized), so MET-15 asks for no training weight, and none is declared; an unweighted fit of the total estimates E[y|x], which the Lorenz curve then divides by the premium. The premium is a scoring column only, never an input (MET-2, the note above). The coverage (`LnCoverage`, the log of the building and contents sum insured, set for the year at renewal) stays a feature, not an offset: the source estimates its coefficient rather than fixing it at 1, as its general definition of an exposure offset would (Frees, Lee and Yang 2016, Sec. 2.2, p. 5; Table 11, p. 19: 0.853 in the negative binomial frequency part and 0.136 in the GB2 severity part, an implied elasticity of the expected claims of about 0.99 before the zero-one inflation); GLMs on this file with coverage, deductible, entity type, no-claim credit, `Fire5`, alarm credit and year give it 1.14 for the claim count (Poisson) and 0.67 for a Tweedie fit of the total (coverage alone: 1.01 and 0.77-0.82); and a feature lets a model learn any elasticity. Rows are member-years with no time at risk. Whether a member joined or left during a year cannot be located row by row; the exit years show no claim shortfall (observed/expected 0.93, z -0.46; permanent exits 0.86, z -0.85), the entry years no excess beyond chance (1.22, z 1.07), and the premium is not prorated in either. 48 members appear in one year only (54 in two, 55 in three, 32 in four, 1,038 in all five).
        - Target `bc_claims`, `y`, the year's total BC claims in dollars; 70.2% of the member-years are 0, none is negative. Dollars rather than the log scale CLEAN-16 defaults to: the metric divides each prediction by the premium, so a prediction's size counts, not only its order; the source models dollars (Tweedie and GB2 models), and the fund prices from expected dollars (MET-3, USE-5). On the three yearly windows (test 2008, 2009, 2010) an untuned LightGBM fit on dollars with a Tweedie loss scores 0.146, 0.254 and 0.327, the same model fit on log1p with squared error -0.049, 0.248 and 0.016, an untuned Tweedie GLM on dollars 0.254, 0.251 and 0.350.
        - Note: the task probes flag no_signal, scored by R^2 on dollars, which follows a few large claims (random forest 0.234, SD 0.28 across the windows; linear 0.032): even the true claim indicator times the training claimants' mean reaches R^2 0.007 to 0.038 on the windows. Both parts carry signal (untuned LightGBM, test 2008, 2009, 2010): a claim is ranked at ROC AUC 0.791, 0.774 and 0.760 (log coverage alone 0.745, 0.738, 0.736), the log claims of the claimants at R^2 0.054, 0.095 and 0.221. The leak probes find nothing: every feature alone at R^2 0.014 or below, no test row with an exact copy of its inputs in training.
        - The totals match the claim-level file: CLAIMLEVEL.csv (6,258 BC claims) sums to the year's claims within $1 for 5,633 of the 5,639 member-years (decision 2); 4 of the 6 others hold claim lines that look duplicated in the claim-level file (82,532.36 = 2 x 41,266.18). `y` is kept as published. The book keeps "only claims that are closed, with obligations fully met" (Ch. 1): a claim still open when the file was made is missing from its year (LEAK-24). There is no extraction date; 2010, the newest year, has the highest share of members with a claim (36.3%), so no shortfall shows.
        - CLAIMLEVEL.csv also names each claimant's county, but only for the 759 members with a claim, so it is not joined: its missingness would tell the outcome.
        - Metric: the source's Gini of the ordered Lorenz curve with the fund's premium as the base (`ordered_lorenz_gini`; Frees, Meyers and Cummings 2011; Frees, Lee and Yang 2016, Sec. 6.2), not normalized, as the source reports it: a prediction that adds nothing to the premium (the premium itself) scores 0.000 in every window, while a constant prediction, which orders the members by the inverse of their premium, is a different baseline: -0.004, -0.124 and 0.061 (test 2008, 2009, 2010). The source argues for it (it measures "the satisfaction of the fund manager with each score", and with "large masses at zero ... traditional metrics are less helpful", Sec. 3), and Lee (2017) concludes by it; the Spearman correlation reported beside it (Sec. 6.1, Table 18) ignores the premium (MET-5). Sorting by coverage alone is the level a model must beat, and a high one. On the three yearly windows (test 2008, 2009, 2010) coverage in dollars scores 0.019, 0.195 and 0.540 (mean 0.251), an untuned Tweedie GLM 0.254, 0.251 and 0.350 (mean 0.285), an untuned LightGBM Tweedie 0.146, 0.254 and 0.327 (mean 0.242); coverage leads only in 2010, the storm year. The best monotone fit of one feature chosen on the training side (log coverage in every window) scores 0.094, 0.141 and 0.461 and beats the GLM only in 2010, so the task is not `Trivial` (TP-4). Before the split changed, models tuned on the training side reached 0.324 (2009) and 0.350 (2010) without `PolicyNum`. These models stand in for the benchmark's tuned methods, which have no results here yet (TP-1).
        - Anomaly: 2010 was a year of severe weather (Lee 2017, Ch. 1): $36.7M of claims against $11.0M-20.5M in 2006-2009, and one water damage claim at a Milwaukee school, $12.9M, is 35% of the year's claims. Kept as recorded; it is in the 2010 window, and that window's score moves with where it is ranked.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.source(
        "ordered_lorenz_gini",
        original=(
            "Gini index of the ordered Lorenz curve with the fund's premium as base: members sorted by the relativity "
            "score / premium, cumulative premium share against cumulative claims share (Frees, Meyers and Cummings "
            "2011, JASA 106:1085-1098), computed with the premium the fund collected as the denominator"
        ),
        reference="https://doi.org/10.3390/risks4010004",
        inputs={"weight": "Premium"},
    )
    scoring_columns = (
        ScoringColumn(
            column="Premium",
            role="weight",
            used_by="ordered_lorenz_gini",
            description=(
                "the fund's building and contents premium for the member-year, the base of the source's Gini: members "
                "are sorted by prediction / Premium and the cumulative share of the claims is set against the "
                "cumulative share of the premium. Never a feature: it is the output of the rating the task replaces."
            ),
        ),
    )
    accepted_check_warnings = {
        "task_time_on_few_unique": (
            "Five policy years, 2006-2010, the whole time axis of the file: the yearly windows train on two to four "
            "earlier years, and the file has no finer time."
        ),
        "meta_license_unknown": (
            "The first edition's repository, which holds the shipped file, has no licence file (GitHub API, "
            "2026-11-01), and its book pages state none. The second edition named in the download description "
            "(OpenActTexts/LDAVer2, WiscPropFund.csv: the same rows with fewer columns) has a CC0-1.0 LICENSE in its "
            "repository (committed 2024-10-03), and its book pages state CC BY 4.0; the rows can be taken from it if "
            "the release needs a stated licence."
        ),
        "task_target_value_dominant": (
            "70.2% zeros: member-years without a building and contents claim (`Freq` 0), real no-claim years and not a "
            "cap or a placeholder; the batch's other zero-inflated targets are accepted on the same ground (Andrej, "
            "2026-11-03)."
        ),
    }
    temporal = Temporal(
        on="Year",
        splits=TemporalSplits(window=1, unit="unique", n_windows=3),
        horizon=1,
        horizon_unit="years",
    )
    splits_comment = """
        Three expanding yearly windows, newest first: test 2010 trained on 2006-2009 (4,529 rows, 80.3%; 1,110 test
        member-years, 403 with a claim), test 2009 on 2006-2008 (3,417 rows, 60.6%; 1,112, 301) and test 2008 on
        2006-2007 (2,292 rows, 40.6%; 1,125, 309). The fund rates the members it knows once a year for the next year,
        and the source tested on the next year, 2011, which is not public. The 2008 window trains on less than SPLIT-14's
        floor of half the rows (a Must): the curator's call (Andrej, 2026-11-02), after the leak test found the year's
        claim level shared across the member folds the definition shipped before ("We found that grouped splits leak, so
        I would recommend to use three splits, one for each year of 2008, 2009, 2010"), open again since 2026-11-05
        (REVIEW.md issue 3). In that window the no-claim credit is unknown on every training row (the file starts in
        2006), so it informs only the two later windows. No test year has a row on its training side, and no gap
        separates the sides: an exception to SPLIT-10 that serves SPLIT-14, since a one-year gap would leave the 2009
        window 2006-2007 and the 2008 window one year. Its earlier precedent, "as in pricing_game_2016_french_fleet", is
        stale (2026-11-06): that case is reopened (its REVIEW.md issue 6) and never covered a window below the floor, so
        if the windows stay the exception needs a fact of its own and a SPLIT-10 Cases row. The training years carry
        final claim amounts, which the fund knew only in part when it rated (fit approximate). Members recur across the
        cutoff, as the fund re-rates them (SPLIT-13, USE-10): 98.8%, 97.6% and 98.6% of the 2008, 2009 and 2010 members
        are in their training years, and `PolicyNum` is an input. The windows differ: the claims were $12.1M, $11.0M
        and $36.7M, and in 2010, a year of severe weather, coverage fell for 67.7% of the members and one claim is 35%
        of the year's claims, so that window's score moves with where that one member is ranked.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "insample": pd.read_csv(raw_dir / "PropertyFundInsample.csv", dtype={"PolicyNum": str}),
            "claims": pd.read_csv(raw_dir / "CLAIMLEVEL.csv", dtype={"PolicyNum": str}),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["insample"].copy()
        assert not df.duplicated(["PolicyNum", "Year"]).any()
        # 1. One category from each block of flags (exactly one flag set per row).
        df["EntityType"] = _from_flags(df, ENTITY_FLAGS)
        df["AlarmCredit"] = _from_flags(df, ALARM_FLAGS)
        # 2. The restatements of the target: the claim count, the log claims, the average claim.
        assert (df["Freq"].eq(0) == df["y"].eq(0)).all()
        # 3. Coverage and deductible in dollars: exact transforms of the log columns the source models.
        assert np.allclose(df["LnCoverage"], np.log(df["BCcov"] / 1e6), atol=1e-8)
        assert np.allclose(df["lnDeduct"], np.log(df["Deduct"]), atol=1e-7)
        df = drop_columns(df, ["Freq", "lny", "yAvg", "BCcov", "Deduct", *ENTITY_FLAGS, *ALARM_FLAGS])
        # 4. The no-claim credit where the file lacks the two earlier years: the 0 there means "history not in the file".
        df["NoClaimCredit"] = df["NoClaimCredit"].astype(float).where(_two_years_in_file(df))
        df["PolicyNum"] = df["PolicyNum"].astype("category")  # the member: the fund rates members it knows (USE-10)
        # 5. The fund's premium stays as the metric's base (a scoring column, never a feature); the target in dollars.
        assert (df["Premium"] > 0).all()
        assert (df["y"] >= 0).all()
        df[TARGET] = df.pop("y")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["PolicyNum", "EntityType", "AlarmCredit", "Fire5", "NoClaimCredit"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        ins = raw["insample"]
        by_year = ins.groupby("Year")
        premium = pd.DataFrame(
            {
                "member-years": by_year.size(),
                "R^2 of log premium on the rating variables": by_year.apply(_rating_r2, include_groups=False),
                "Spearman, premium and claims": by_year.apply(
                    lambda g: g["Premium"].corr(g["y"], method="spearman"), include_groups=False
                ),
                "Spearman, coverage and claims": by_year.apply(
                    lambda g: g["BCcov"].corr(g["y"], method="spearman"), include_groups=False
                ),
            }
        ).round(3)
        claims = raw["claims"].groupby(["PolicyNum", "Year"])["Claim"].sum().rename("claim_lines")
        joined = ins.join(claims, on=["PolicyNum", "Year"]).fillna({"claim_lines": 0.0})
        joined["match"] = (joined["claim_lines"] - joined["y"]).abs() < 1
        totals = joined.groupby("Year").agg(
            **{
                "member-years": ("y", "size"),
                "member-years matching within $1": ("match", "sum"),
                "claims, PropertyFundInsample ($)": ("y", "sum"),
                "claims, CLAIMLEVEL ($)": ("claim_lines", "sum"),
            }
        )
        dollars = ["claims, PropertyFundInsample ($)", "claims, CLAIMLEVEL ($)"]
        totals[dollars] = totals[dollars].round(0).astype("int64")
        years = pd.Index(sorted(ins["Year"].unique()), name="Year")
        history = _two_years_in_file(ins)
        windows = pd.DataFrame(
            {
                "member-years": by_year.size(),
                "share with a claim": by_year["y"].apply(lambda s: (s > 0).mean()).round(3),
                "claims ($M)": (by_year["y"].sum() / 1e6).round(1),
                "largest claim share": (by_year["y"].max() / by_year["y"].sum()).round(3),
                "train share of a window starting here": pd.Series(
                    [(ins["Year"] < y).mean() for y in years], index=years
                ).round(3),
                "members seen in earlier years": pd.Series(
                    [
                        ins.loc[ins["Year"] == y, "PolicyNum"].isin(ins.loc[ins["Year"] < y, "PolicyNum"]).mean()
                        for y in years
                    ],
                    index=years,
                ).round(3),
                "no two earlier years in the file (NoClaimCredit missing)": (~history).groupby(ins["Year"]).sum(),
            }
        )
        return [
            Decision(
                "The fund's premium is the metric's base, never an input",
                "The source scores a new rating against the fund's premium (Frees, Lee and Yang 2016, Sec. 6.2), and "
                "its models take the rating variables only. The premium is close to a function of the shipped rating "
                "variables, and ranks the year's claims about as well as the coverage alone.",
                premium,
            ),
            Decision(
                "The yearly claims agree with the claim-level file",
                "CLAIMLEVEL.csv lists every BC claim; its sum per member and year is compared with `y`.",
                totals,
            ),
            Decision(
                "Three yearly windows, the oldest below half the rows",
                "The test years are 2008, 2009 and 2010, each trained on every earlier year. The 2008 window trains on "
                "2006-2007, under half of the rows (SPLIT-14), on the curator's call of 2026-11-02. 2010, a year of "
                "severe weather, holds the largest claims. The no-claim credit is missing where the file lacks the "
                "member's two earlier years.",
                windows,
            ),
        ]
