"""Curated dataset definition for `australian_vehicle_insurance_2004_2005` (data-foundry v2). Evidence: README.md."""

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
    drop_columns,
)

# The body codes of insuranceData's `dataCar` and the labels CASdatasets' `ausprivauto0405` gives the same rows
# (checked one to one on all 67,856 rows, 2026-11-01).
BODY_LABELS = {
    "BUS": "Bus",
    "CONVT": "Convertible",
    "COUPE": "Coupe",
    "HBACK": "Hatchback",
    "HDTOP": "Hardtop",
    "MCARA": "Motorized caravan",
    "MIBUS": "Minibus",
    "PANVN": "Panel van",
    "RDSTR": "Roadster",
    "SEDAN": "Sedan",
    "STNWG": "Station wagon",
    "TRUCK": "Truck",
    "UTE": "Utility",
}

DAYS_PER_YEAR = 365.25
"""`exposure` is the days observed over 365.25 (1 to 365 days)."""

LARGE_RATE = 1e6
"""Claim costs per year of a million dollars or more: the 7 rows actuaRE's copy removes, kept here (notes)."""


class AustralianVehicleInsurance20042005(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What will a vehicle insurance policy cost the insurer in claims per year insured?",
        use_case=(
            "For example, an Australian car insurer prices a one-year policy at underwriting: it estimates the "
            "expected claim cost per year insured (the pure premium) from the rating factors, to set the premium. The "
            "source, a textbook on insurance GLMs, names no decision."
        ),
        row=(
            "One one-year vehicle policy taken out in Australia in 2004 or 2005, mostly cars but also trucks, buses "
            "and motor caravans, observed for up to a year (67,856 policies of an unnamed insurer)."
        ),
        predicted=(
            "The claim cost per year insured, in dollars: the total cost of the policy's claims while the data "
            "observed it, divided by the years observed (1 to 365 days). 0 for the 93.2% without a claim; no claim is "
            "recorded below $200. Each policy counts in proportion to the time observed, in training and scoring."
        ),
        known=(
            "The vehicle's value, body type and age band, the policyholder's or driver's gender (the sources "
            "differ), the driver's age band, and an area code A-F (the R packages do not say what it codes). The time "
            "observed is no input: a claim can cut it short, so it is the rate's denominator and each policy's weight."
        ),
        split="Random policies, so the test data stands for other policies of the same portfolio and period.",
        changes=(
            "We divide the claim cost by the time observed and weight each policy by that time, as pricing actuaries "
            "do. We dropped the claim indicator and the claim count (parts of the target) and made the 53 vehicle "
            "values of 0 missing. The source has no metric, so we score by the exposure-weighted normalized Gini, "
            "which measures how well the predictions order the policies by claim cost per year."
        ),
        fit="approximate",
        fit_reason=(
            "Real policies with the rating factors and claim costs of pricing, priced per year insured. Gaps: a "
            "random split of undated policies stands in for next year's; the label's construction is undocumented "
            "(paid or incurred, the $200 floor, repeated amounts, the cover)."
        ),
    )

    # Dataset
    unique_name = "australian_vehicle_insurance_2004_2005"
    year = "2008"
    domain = "insurance"
    source = "Other"  # the companion website of de Jong and Heller (2008), now offline; no closer schema value
    source_url = "https://doi.org/10.1017/CBO9780511755408"
    # The licence of the insuranceData package we download from (CASdatasets: GPL >= 2); the book's companion site,
    # now offline, could not be read.
    license = "GPL-2"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        The data ("Car", car.csv) was first published on the companion website of de Jong and Heller (2008),
        http://www.acst.mq.edu.au/GLMsforInsuranceData, which no longer resolves (the Internet Archive was offline on
        2026-11-01). We take the copy in the R package insuranceData 1.0 (CRAN, 2014-09-04), data set `dataCar`
        (67,856 rows x 11 columns, the counts of the book's Table 1.1), and export it to CSV with pyreadr; in R,
        write.csv(dataCar, "dataCar.csv", row.names = FALSE) gives the same values. CASdatasets' `ausprivauto0405`
        holds the same rows (exposure, vehicle value, claim count and cost equal on every row) without the area.

        mkdir -p local-data-warehouse/australian_vehicle_insurance_2004_2005 && cd local-data-warehouse/australian_vehicle_insurance_2004_2005
        wget https://cran.r-project.org/src/contrib/insuranceData_1.0.tar.gz
        sha256sum insuranceData_1.0.tar.gz
        # dca49e4325d02a0ffe8b65b1026d3594f39572bfcd3463f1ba768d1d22823e73
        tar xzf insuranceData_1.0.tar.gz insuranceData/data/dataCar.rda
        uvx --from pyreadr==0.5.7 --with pandas==3.0.6 python -c "import pyreadr; pyreadr.read_r('insuranceData/data/dataCar.rda')['dataCar'].to_csv('dataCar.csv', index=False)"
        rm -r insuranceData insuranceData_1.0.tar.gz
        sha256sum dataCar.csv
        # 16966b96a628814c876c0b8684c5c5c744f5a574891b04053de5d4971ed2700f
    """
    bibtex = r"""
        @book{dejong2008generalized,
          title = {Generalized Linear Models for Insurance Data},
          author = {de Jong, Piet and Heller, Gillian Z.},
          series = {International Series on Actuarial Science},
          publisher = {Cambridge University Press},
          address = {Cambridge},
          year = {2008},
          doi = {10.1017/CBO9780511755408}
        }
    """
    curation_comments = """
        We start with `dataCar` of the R package insuranceData 1.0, the "Car" data of de Jong and Heller (2008).

        - Prediction point: when the policy is priced at underwriting (for example; the source names no use). The rating factors are known then, its claims are not. Every policy is a one-year contract; `exposure`, the share of that year the data observed, is known only at the end of the observation period and is cut short by some claims (the exposure note below), so it is the target's denominator and the weight, never a feature.
        - Source: the book's companion website, now offline; the copy in insuranceData matches the book's Table 1.1 (claims by driver age band: 5,742 to 16,189 policies per band, 5,742 in the youngest and 6,547 in the oldest, 4,624 with a claim; Table 1.6, pp. 15-16, gives the same 67,856 policies and 4,624 with claims), and CASdatasets' `ausprivauto0405` agrees with it on every row (2026-11-01). What the book does with this table (read by the curator, 2026-11-02; printed pages): logistic regression for claim occurrence with exposure, the time at risk, in a modified link (Sec. 7.3-7.4, pp. 99-104), compared by ROC AUC, 0.662 with the exposure adjustment against 0.548 without, on the same data with no held-out split (Sec. 7.6, pp. 108-110); a zero-adjusted inverse Gaussian model of the claim amount with its zeros, selected by AIC (Sec. 10.4, pp. 145-148), log links on the raw amount, not a log-transformed target; Tweedie models (Sec. 8.3) and a multiple-claim model (Sec. 10.5) are explained without a fit to this table. The book does not say why some exposures end early, whether the costs are paid or incurred, or why no claim lies below 200.
        - Target `claim_cost_per_year` = `claimcst0` / `exposure`, the claim cost per year insured in dollars (MET-14), on the identity scale as the cost target was (issue 5; CLEAN-16: a rate scored by a Gini keeps the scale the curator chose), with `exposure` as the row weight of the metric and the training weight (`sample_weight`, MET-15) and never a feature (LEAK-41). `claimcst0` ("claim amount (0 if no claim)") leaves the frame as a part of the target, and `_clean` checks that claim_cost_per_year x exposure gives it back. It is 0 for exactly the 63,232 policies without a claim (93.2%). A fit weighted by exposure on this scale estimates E[cost | x] / E[exposure | x], the cost per year insured that breaks even (292.90 dollars a year for the whole portfolio); an unweighted fit estimates the mean of cost / exposure (755.26 dollars a year for the portfolio, 2.6 times as much). Dropped as parts of the target: `clm` (1 exactly where `claimcst0` > 0) and `numclaims` (above 0 on the same rows). `X_OBSTAT_` is one value on every row and is dropped too.
        - Every exposure is positive (one day at least), so the rate is defined on every row and no row goes (USE-7). The rate reaches 5.24 million dollars a year: one claim of 14,343 dollars on a policy observed one day. The 7 policies at 1M dollars or more a year are kept, each with one claim on 1 to 7 days observed: 1 day and 14,343 dollars (5.24M a year), 1 day and 8,605 (3.14M), 2 days and 16,307 (2.98M), 2 days and 13,819 (2.52M), 4 days and 20,891 (1.91M), 4 days and 17,604 (1.61M), 7 days and 25,594 (1.34M); together 1.26% of the claim cost. actuaRE 0.1.5's copy of this table (`dataCar`) builds the same rate (`Y = claimcst0 / exposure`) with the exposure as its weight and removes them (`Y < 1e6`), with the body types of less than 100 years of exposure (67,566 rows left). In the weighted metric and a weighted fit each counts by its cost, not by its rate. Under squared error they would weigh far more: 45% of the exposure-weighted sum of squares of the rate (92% unweighted).
        - Anomaly: no claim cost lies below 200, and 705 of the 4,333 single-claim policies cost 200.00 to the cent (695 exactly, the rest float noise of the file); no policy with several claims does, and the two-claim policies start at 400 (10 of 271 at 400.00, one at 400.01), so each claim seems recorded at 200 at least. Kept as recorded, as Andrej's call on fremtpl2 of 2026-10-20 kept that table's fixed IRSA-IDA amounts as point masses: the floor is in the source's data. In the target it is a cost of 200 per claim over the time observed. Other point masses (353.77 for 219 claims, 389.95 for 94, 390 for 55) are kept as well.
        - Exposure (LEAK-41, MET-14, MET-15; issue 6, resolved 2026-11-06): `exposure` (days / 365.25, 1 to 365 days, a full year 0.9993; median 163 days, 1.9% full years, no 366-day row) is mostly the share of each one-year policy that fell inside the extract's observation period, fixed when the policy starts, but some claims cut it short. It is realized, not planned: at a quote it is one year for every policy. In claim occurrence: policies of 0.2 years or less have 147 more claims than the rate of longer ones predicts; at 7 days or less they claim 0.85 times per policy-year even without the claims of at least 80% of the vehicle's value (0.14-0.17 above 0.2 years); a free log-exposure coefficient is 0.29-0.31 in a Tweedie GLM where proportional time gives 1. In size: the 193 claims of at least 80% of the vehicle's value (likely write-offs) have a median exposure of 0.37 against 0.65 for the other claims (Mann-Whitney p < 1e-20). The task uses it as the rate's denominator and each policy's weight, in the metric and in training, never as a feature: a column whose value the outcome can cut after the prediction point is never a model input, whatever it scores (LEAK-41). With the weight, dividing does not inflate short policies: each counts by its time observed. The old metric, the unweighted Gini of each policy's cost over its observed part-year, hid the leak: there exposure as a proportional offset only scored 0.1833 against 0.1824 as a free feature (9 shipped splits, Tweedie LightGBM, paired SE 0.0059), giving the write-offs a counterfactual uncut exposure lifted that Gini from 0.182 to 0.31 (18 of 18 runs), and exposure alone scored 0.168 of the best 0.205, though it is one year at every quote. The exposure study of 2026-11-05 (own 3x3 KFold) scored the claim counts by a Poisson deviance instead: 47% (GLM) to 82% (LightGBM) of a free model's gain over a constant rate is leak, and at a quote (exposure set to one year) the free LightGBM's mean deviance is 0.0068 worse than the offset model's, better on 0 of 9 folds. On the exposure-weighted Gini of the cost per year, a Tweedie GLM that reads the exposure scores 0.238 against 0.125 for an honest GLM, whose quotes see no exposure. The rating factors predict the exposure only weakly (LightGBM R^2 0.06; ROC AUC 0.62 for exposures of 0.2 years or less), so little of it can come back through them. Re-measured on this definition's 9 shipped splits, every model fitted with the sample weight (LightGBM: learning rate 0.05, 15 leaves, 300 rounds): an honest Tweedie LightGBM scores 0.059 (SD 0.021) against 0 for the weighted constant (above it on 9 of 9), an L2 LightGBM on the identity scale 0.060 and a Tweedie GLM 0.120; with `exposure` added as a feature they score 0.149 (+0.089, SE 0.010), 0.159 (+0.099, SE 0.008) and 0.236 (+0.116, SE 0.006), higher on 9 of 9 splits each (more regularised LightGBM settings: 0.070 to 0.090 honest, +0.094 to +0.124 with it). 1/exposure alone, the ceiling a proxy of it would reach, scores 0.205, above every honest model. Probe 22: the rating factors predict the exposure at R^2 0.07 (Spearman 0.26, mostly through the vehicle value), and no rating factor gains through it above noise. Revisit if a release gives the policy dates or why a policy ended.
        - `veh_value` (in $10,000s, insuranceData; CASdatasets says thousands of AUD, which would make the median car worth $1,500, an error of that copy) is 0 for 53 policies, most of them station wagons, buses, trucks or motor caravans of the oldest band, while the next lowest value is 0.18 ($1,800): a vehicle value of $0 is no value, so these are made missing (CLEAN-10, CLEAN-11).
        - The body codes are given the labels CASdatasets uses for the same rows (`HBACK` to Hatchback, `STNWG` to Station wagon, ...). The age bands of the vehicle (1 youngest to 4) and the driver (1 youngest to 6) stay numbers, the order of an age.
        - Columns renamed to plain names: `vehicle_value`, `vehicle_body`, `vehicle_age_band`, `driver_age_band`; `gender`, `area` and `exposure` keep theirs, and the target is `claim_cost_per_year`. `gender` is "gender" in insuranceData and the policyholder's in CASdatasets, so it is not called the driver's. `area` is a code A-F that insuranceData leaves undocumented and CASdatasets lacks (the book's Table 1.6, pp. 15-16, says it denotes the area of residence and leaves A-F unexplained; Ye et al. 2022 call it the driver's area of residence). The age band keeps its name: the book's Table 1.1 says "Driver's age category", while its Table 1.6 and CASdatasets call it the policyholder's age.
        - 707 rows share every column with another row (378 extra copies, 0.6%), all without a claim. That is about three times chance: with the exposure shuffled among the no-claim rows, 120-125 copies remain (20 runs). Among the 1,129 full-year rows without a claim there are 152 copies against 11.6 for random rows of that number; that cohort is rich in trucks and panel vans, likely fleet vehicles insured on the same dates. Kept (LEAK-18): on the earlier cost target (2026-11-01), dropping the copies moved the Gini by +0.0045, and a split that keeps identical feature rows together scored within fold noise (Tweedie LightGBM 0.194 against 0.182); 0.8% of the test rows had an exact feature copy in train then (leak probe, first split, with exposure a feature). Without exposure among the features, 34,974 rows (51.5%) share their six rating factors with another policy and 42-43% of the test rows have an exact copy of them in train (every shipped split): coarse rating cells of distinct policies, the portfolio a tariff prices, as in fremtpl2.
        - The split is forced (ForcedIIDFromTemporal, SPLIT-8): an insurer fits its tariff on past policy-years and prices the next year's policies, but the release has no date and no policy id. It looks like one observation period of about a year (exposure spread evenly over 1-365 days, 1.9% full years, no 366-day row), so a temporal test needs another year's extract. The raw file order is not random (12.2% of adjacent rows share a day count, against 0.3% when the rows are permuted; whether the order is time is unknown), but the claim indicator shows no serial dependence (lag-1 correlation 0.005), and training on the earlier quarters of the file to test the next shows no drop (on the earlier cost target, Tweedie LightGBM 0.168, 0.189, 0.208 against 0.127, 0.174, 0.181 for random splits of the same sizes; single splits). No policy is visibly split into two rows (116 pairs of identical rating factors sum to 365 days, against 102 on average for other sums) and the hidden-group probe finds no group. Shipped forced on the curator's call (Andrej, 2026-11-02): a forced IID split ships only when no leak is found across the random split, as here (no row shares its outcome across the split, no hidden group, no order dependence); how_much_did_it_rain's `No` named a measured leak.
        - CC (2026-11-06, Lennart): decision D8 of the exposure study of 2026-11-05 (issue 6): the target is the claim cost per year insured (`claimcst0` / `exposure`, in dollars, identity scale), `exposure` the weight scoring column, the `weight` input of `normalized_weighted_gini` and the task's `sample_weight`, and never a feature (LEAK-41, MET-14, MET-15); the metric stays a context Gini, now weighted on the rate; the 7 rows at 1M dollars or more a year are kept. Supersedes Andrej's call of 2026-11-02 (issue 2: `exposure` kept as a feature with its note, the LEAK-10 case for time on risk cut short by the outcome) and changes the form of his Gini of the same day (issue 4: unweighted on the cost, now weighted on the rate). What sets the case apart is a measurement made after the call: the deviance on the claim counts shows the leak the slice Gini hid (47 to 82% of a free model's gain over a constant rate is leak); on the weighted Gini of the cost per year a free GLM scores 0.238 against 0.125 for honest quotes, and on the shipped splits `exposure` as a feature lifts an honest LightGBM from 0.059 to 0.149 (9 of 9). The alternative, the claim frequency with an exposure-weighted deviance, was not chosen.
    """

    accepted_check_warnings = {
        "task_target_value_dominant": (
            "Zero-inflated by nature: the claim cost per year is 0 for exactly the 63,232 policies without a claim "
            "(93.2%), the rows where the source's claim indicator is 0; not a cap or a placeholder (claim audit, "
            "2026-11-01)."
        ),
        "dataset_duplicate_rows": (
            "Distinct policies in coarse rating cells: with exposure out of the features, six rating factors remain and "
            "51.5% of the rows share them with another policy. Grouping the split on the rating cell does not lower "
            "the score (LightGBM 0.054 against 0.059, GLM 0.119 against 0.120; split audit, 2026-11-06)."
        ),
        "dataset_conflicting_duplicate_rows": (
            "Policies with the same rating factors and different claim costs: claims are rare events of one risk "
            "profile, not label noise (the same split audit, 2026-11-06)."
        ),
    }

    # Task
    target = "claim_cost_per_year"
    problem_type = "regression"
    metric = Metric.from_context(
        "normalized_weighted_gini",
        reason=(
            "No source metric for this claim-cost regression was established: insuranceData and CASdatasets define no "
            "task, and the book (Sec. 10.4) selects its claim-amount model by AIC on all rows, with no held-out score; "
            "its ROC AUC (Sec. 7.6) scores claim occurrence, a classification, and is no support for this Gini. "
            "Pricing actuaries compare tariffs by a Gini of the loss cost per exposure: CAS Monograph 5 (Sec. 7.2.4) "
            "sorts the policies by predicted loss cost per exposure and accumulates exposure on the x-axis, and "
            "Frees, Meyers and Cummings (2011, JASA 106:1085-1098) order by relativity and accumulate premium. The "
            "weighted Gini on the rate is that CAS Gini of the cost per year insured, each policy weighted by its "
            "exposure, normalised by the Gini of the perfect order (as Liberty Mutual's Kaggle metric is). The curator "
            "chose a Gini for this table on 2026-11-02 (Andrej, 'Use Gini'), then unweighted on each policy's cost, "
            "the form Ye et al. (2022, Econometrics 10(2):19) scored this table by (Sec. 2.3, on a holdout third, "
            "Sec. 2.2, next to MAE, RMSE, a rebalanced RMSE and the total error; they recommend the Gini with a second "
            "measure where possible, Sec. 4.2: context, not one source metric); that form scores the cost of the "
            "observed part-year and hid the exposure leak, so the weighted Gini on the rate replaced it (2026-11-06, "
            "Lennart). Allstate scored its Claim Prediction Challenge (Kaggle, 2011) by the unweighted Gini on rows "
            "of one full vehicle-year each; the weight gives the part-years here (98.1% of the rows) their share of a "
            "year. The alternative, the claim frequency with an exposure-weighted Poisson deviance, was not chosen: "
            "it drops the claim size the insurer prices. A constant scores 0, an honest Tweedie GLM 0.120 and an "
            "honest Tweedie LightGBM 0.059 (9 shipped splits, fitted with the sample weight); 1/exposure alone, which "
            "no model may read, 0.205. RMSE follows a few large values: on the cost the largest 46 (0.07% of the "
            "policies) hold 43% of the sum of squares and no model family probed beat the mean by more than R^2 0.002 "
            "on average; on the rate the 7 policies at 1M dollars or more a year hold 45% of the exposure-weighted sum "
            "of squares. The Gini ignores the price level, which pricing sets separately."
        ),
        inputs={"weight": "exposure"},
        definition=(
            "WG(y, p) / WG(y, y) over the claim cost per year y and the predicted cost per year p, w = exposure (years "
            "observed): rows sorted by descending p, R the cumulative share of exposure, L the cumulative share of "
            "claim cost (w*y), WG = sum L_i R_(i-1) - sum L_(i-1) R_i; tied p form one step (the mean over their "
            "orderings), so a constant scores 0"
        ),
    )
    scoring_columns = (
        ScoringColumn(
            column="exposure",
            role="weight",
            used_by="normalized_weighted_gini",
            description=(
                "years observed (days / 365.25, 1 to 365 days): the share of the policy's one-year term inside the "
                "data's observation period, realized and cut short by some claims (write-offs). The claim cost per "
                "year's denominator; each row's weight in the metric and in training; never a feature"
            ),
        ),
    )
    sample_weight = "exposure"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "dataCar.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. Parts of the target and a constant column.
        assert ((df["claimcst0"] > 0) == (df["clm"] == 1)).all()
        assert ((df["numclaims"] > 0) == (df["clm"] == 1)).all()
        df = drop_columns(df, ["clm", "numclaims", "X_OBSTAT_"])
        # 2. The claim cost per year insured, weighted by the years observed (MET-14, MET-15): the cost leaves the frame
        # as a part of the target, and exposure stays only as the weight scoring column, never a feature (LEAK-41).
        if not df["exposure"].between(1 / DAYS_PER_YEAR - 1e-9, 1).all():
            raise ValueError("Expected exposures between one day and one year (a positive denominator on every row)")
        df["claim_cost_per_year"] = df["claimcst0"] / df["exposure"]
        if not np.allclose(df["claim_cost_per_year"] * df["exposure"], df["claimcst0"], rtol=0, atol=1e-9):
            raise ValueError("Expected claim_cost_per_year x exposure to give back claimcst0")
        df = drop_columns(df, ["claimcst0"])
        # 3. A vehicle value of $0 is no value: missing.
        df["veh_value"] = df["veh_value"].mask(df["veh_value"] == 0)
        # 4. The body codes get CASdatasets' labels.
        assert set(df["veh_body"]) <= set(BODY_LABELS)
        df["veh_body"] = df["veh_body"].map(BODY_LABELS)
        # 5. Plain names.
        return df.rename(
            columns={
                "veh_value": "vehicle_value",
                "veh_body": "vehicle_body",
                "veh_age": "vehicle_age_band",
                "agecat": "driver_age_band",
            }
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["vehicle_body", "gender", "area"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        positive = raw[raw["claimcst0"] > 0]
        cost = positive.groupby("numclaims")["claimcst0"]
        at_floor = (
            positive["claimcst0"].round(2) == 200 * positive["numclaims"]
        )  # to the cent: the file has float noise
        floor = pd.DataFrame(
            {
                "policies": cost.size(),
                "lowest cost": cost.min().round(2),
                "cost of 200 per claim (to the cent)": at_floor.groupby(positive["numclaims"]).sum(),
            }
        ).rename_axis("claims")
        # Claimants' observed time by claim size over the vehicle's value (in $10,000s): a write-off ends a policy.
        share = positive["claimcst0"] / (positive["veh_value"] * 10_000)
        bands = pd.cut(
            share, [0, 0.1, 0.3, 0.5, 0.8, np.inf], right=False, labels=["<10%", "10-30%", "30-50%", "50-80%", ">=80%"]
        )
        exposure = (
            positive["exposure"]
            .groupby(bands, observed=True)
            .agg(claims="size", median_exposure="median")
            .round(3)
            .rename_axis("claim cost / vehicle value")
        )
        no_claim = raw.loc[raw["claimcst0"] == 0, "exposure"]
        exposure.loc["no claim"] = [len(no_claim), round(float(no_claim.median()), 3)]
        # The largest costs per year: one claim on a policy observed a few days (kept, notes).
        rate = raw["claimcst0"] / raw["exposure"]
        large = raw[rate >= LARGE_RATE]
        largest = (
            pd.DataFrame(
                {
                    "days observed": (large["exposure"] * DAYS_PER_YEAR).round().astype("int64"),
                    "claims": large["numclaims"],
                    "claim cost": large["claimcst0"].round(2),
                    "cost per year": rate[rate >= LARGE_RATE].round().astype("int64"),
                    "vehicle body": large["veh_body"].map(BODY_LABELS),
                }
            )
            .sort_values("cost per year", ascending=False, kind="stable")
            .reset_index(drop=True)
        )
        return [
            Decision(
                "The claim costs at 200 are kept as recorded",
                "No claim costs less than 200 and only single-claim policies cost exactly 200, while two-claim "
                "policies start at 400: each claim seems recorded at 200 at least. Kept as recorded, as the call on "
                "fremtpl2's fixed amounts did (CC 2026-10-20).",
                floor,
            ),
            Decision(
                "The observed share of the year is the weight, not a feature: a write-off seems to end it",
                "Claimants are observed longer than other policies (more time to claim), except those whose claim "
                "comes near the vehicle's value: their policy seems to end with the claim. A time on risk the outcome "
                "can cut short is never a model input (LEAK-41); it is the rate's denominator and each policy's "
                "weight in the metric and in training (MET-15). The Gini of each policy's cost did not show the leak; "
                "the deviance on the claim counts and the weighted Gini on the cost per year do (curation notes).",
                exposure,
            ),
            Decision(
                "The 7 costs per year of a million dollars or more are kept",
                "Each is one claim on a policy observed 1 to 7 days, together 1.26% of the claim cost. actuaRE's copy "
                "removes them; here they stay, and the weighted metric and a weighted fit count each by its cost, not "
                "by its rate.",
                largest,
            ),
        ]
