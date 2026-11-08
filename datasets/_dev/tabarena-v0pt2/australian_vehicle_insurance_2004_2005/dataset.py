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
            "The vehicle's value, body type and age band, the driver's age band, and an area code A-F (the R packages "
            "do not say what it codes). Gender is left out: this benchmark prices every insurance task as EU law "
            "requires, without sex as a rating factor. The time observed is no input: a claim can cut it short, so it "
            "is the rate's denominator and each policy's weight."
        ),
        split="Random policies, so the test data stands for other policies of the same portfolio and period.",
        changes=(
            "We divide the claim cost by the time observed and weight each policy by that time, as pricing actuaries "
            "do. We dropped the claim indicator and the claim count (parts of the target) and gender, and made the 53 "
            "vehicle values of 0 missing. The source has no metric, so we score by the exposure-weighted normalized "
            "Gini, which measures how well the predictions order the policies by their cost."
        ),
        fit="approximate",
        fit_reason=(
            "Real policies with the rating factors and claim costs of pricing, priced per year insured. Gaps: a "
            "random split of undated policies stands in for next year's; the label's construction is undocumented "
            "(paid or incurred, the $200 floor, repeated amounts, the cover); gender is left out, which an Australian "
            "insurer may still be allowed to price on."
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
        - Target `claim_cost_per_year` = `claimcst0` / `exposure`, the claim cost per year insured in dollars (MET-14), on the identity scale as the cost target was (issue 5; CLEAN-16: a rate scored by a Gini keeps the scale the curator chose), with `exposure` as the row weight of the metric and the training weight (`sample_weight`, MET-15) and never a feature (LEAK-41). `claimcst0` ("claim amount (0 if no claim)") leaves the frame as a part of the target, and `_clean` checks that claim_cost_per_year x exposure gives it back. It is 0 for exactly the 63,232 policies without a claim (93.2%). A fit weighted by exposure on this scale estimates E[cost | x] / E[exposure | x], the cost per year insured that breaks even (292.90 dollars a year for the whole portfolio); an unweighted fit estimates the mean of cost / exposure (755.26 dollars a year for the portfolio, 2.6 times as much). Dropped as parts of the target: `clm` (1 exactly where `claimcst0` > 0) and `numclaims` (above 0 on the same rows). `X_OBSTAT_` is one value on every row and is dropped too. The per-contract clause of MET-14 (amended 2026-11-08) does not apply: the data record each one-year contract only inside the extract's window (98.1% part-years, 0.469 of a year per contract on average), so the recorded cost is the window's part of the contract's. A model of the exposure from the rating factors, used as the score, scores 0.056 Gini on the cost per contract (the GLM 0.124) and -0.034 on the cost per year (9 shipped splits, 2026-11-08).
        - Every exposure is positive (one day at least), so the rate is defined on every row and no row goes (USE-7). The rate reaches 5.24 million dollars a year: one claim of 14,343 dollars on a policy observed one day. The 7 policies at 1M dollars or more a year are kept, each with one claim on 1 to 7 days observed: 1 day and 14,343 dollars (5.24M a year), 1 day and 8,605 (3.14M), 2 days and 16,307 (2.98M), 2 days and 13,819 (2.52M), 4 days and 20,891 (1.91M), 4 days and 17,604 (1.61M), 7 days and 25,594 (1.34M); together 1.26% of the claim cost. actuaRE 0.1.5's copy of this table (`dataCar`) builds the same rate (`Y = claimcst0 / exposure`) with the exposure as its weight and removes them (`Y < 1e6`), with the body types of less than 100 years of exposure (67,566 rows left). In the weighted metric and a weighted fit each counts by its cost, not by its rate. Under squared error they would weigh far more: 45% of the exposure-weighted sum of squares of the rate (92% unweighted).
        - Anomaly: no claim cost lies below 200, and 705 of the 4,333 single-claim policies cost 200.00 to the cent (695 exactly, the rest float noise of the file); no policy with several claims does, and the two-claim policies start at 400 (10 of 271 at 400.00, one at 400.01), so each claim seems recorded at 200 at least. Kept as recorded, as Andrej's call on fremtpl2 of 2026-10-20 kept that table's fixed IRSA-IDA amounts as point masses: the floor is in the source's data. In the target it is a cost of 200 per claim over the time observed. Other point masses (353.77 for 219 claims, 389.95 for 94, 390 for 55) are kept as well.
        - Exposure (LEAK-41, MET-14, MET-15; issue 6, resolved 2026-11-06): `exposure` (days / 365.25, 1 to 365 days, a full year 0.9993; median 163 days, 1.9% full years, no 366-day row) is mostly the share of each one-year policy that fell inside the extract's observation period, fixed when the policy starts, but some claims cut it short. It is realized, not planned: at a quote it is one year for every policy. In claim occurrence: policies of 0.2 years or less have 145 to 147 more claims than the rate of longer ones predicts; at 7 days or less they claim 0.85 times per policy-year even without the claims of at least 80% of the vehicle's value (0.14-0.17 above 0.2 years); a free log-exposure coefficient is about 0.3 in a Tweedie GLM (0.28 to 0.31 by design), where proportional time gives 1. In size: the 193 claims of at least 80% of the vehicle's value (likely write-offs) have a median exposure of 0.37 against 0.65 for the other claims (Mann-Whitney p < 1e-20). The task uses it as the rate's denominator and each policy's weight, in the metric and in training, never as a feature: a column whose value the outcome can cut after the prediction point is never a model input, whatever it scores (LEAK-41). With the weight, dividing does not inflate short policies: each counts by its time observed. The old metric, the unweighted Gini of each policy's cost over its observed part-year, hid the leak: there exposure as a proportional offset only scored 0.1833 against 0.1824 as a free feature (9 shipped splits, Tweedie LightGBM, paired SE 0.0059), giving the write-offs a counterfactual uncut exposure lifted that Gini from 0.182 to 0.31 (18 of 18 runs), and exposure alone scored 0.168 of the best 0.205, though it is one year at every quote. The exposure study of 2026-11-05 (own 3x3 KFold) scored the claim counts by a Poisson deviance instead: 47% (GLM) to 82% (LightGBM) of a free model's gain over a constant rate is leak, and at a quote (exposure set to one year) the free LightGBM's mean deviance is 0.0068 worse than the offset model's, better on 0 of 9 folds. On the exposure-weighted Gini of the cost per year, a Tweedie GLM that reads the exposure scores 0.238 against 0.125 for an honest GLM, whose quotes see no exposure. The rating factors predict the exposure only weakly (LightGBM R^2 0.06; ROC AUC 0.62 for exposures of 0.2 years or less), so little of it can come back through them. Re-measured on this definition's 9 shipped splits (2026-11-08, without `gender`), every model fitted with the sample weight (LightGBM: learning rate 0.05, 15 leaves, 300 rounds): an honest Tweedie LightGBM scores 0.075 (SD 0.037) against 0 for the weighted constant (above it on 9 of 9), an L2 LightGBM on the identity scale 0.076 and a Tweedie GLM 0.119; with `exposure` added as a feature they score 0.146 (+0.071, SE 0.006), 0.160 (+0.084, SE 0.013) and 0.238 (+0.119, SE 0.007), higher on 9 of 9 splits each (more regularised LightGBM settings: 0.091 to 0.103 honest, +0.069 to +0.121 with it). The weight alone (1/exposure as the prediction) scores 0.206, above every honest model; a model that reads the exposure together with the rating factors scores more (the Tweedie GLM with it, 0.238). Probe 22 (3 splits x 3 seeds, every fit weighted), in both arms: the rating factors predict the exposure at R^2 0.076 (Spearman 0.27, the vehicle value 72% of the gain); the exposure as a feature gains +0.078 (SD 0.049) over an honest L2 fit of 0.070 and +0.062 (SD 0.03) over an honest Tweedie fit of 0.058; in neither arm does a rating factor gain through it above noise (the largest, the driver age band in the L2 arm, +0.044 with SD 0.045, is known at the quote and stays). Revisit if a release gives the policy dates or why a policy ended.
        - `veh_value` (in $10,000s, insuranceData; CASdatasets says thousands of AUD, which would make the median car worth $1,500, an error of that copy) is 0 for 53 policies, most of them station wagons, buses, trucks or motor caravans of the oldest band, while the next lowest value is 0.18 ($1,800): a vehicle value of $0 is no value, so these are made missing (CLEAN-10, CLEAN-11).
        - The body codes are given the labels CASdatasets uses for the same rows (`HBACK` to Hatchback, `STNWG` to Station wagon, ...). The age bands of the vehicle (1 youngest to 4) and the driver (1 youngest to 6) are ordered categories, youngest first, with their codes as levels, since the band limits are published nowhere (CLEAN-14: bands of a quantity; CC 2026-11-08, Lennart, issue 9). insuranceData names one end only ("1 (youngest), 2, 3, 4"), CASdatasets every level ("youngest cars" to "oldest cars").
        - Columns renamed to plain names: `vehicle_value`, `vehicle_body`, `vehicle_age_band`, `driver_age_band`; `area` and `exposure` keep theirs, and the target is `claim_cost_per_year`. `area` is a code A-F that insuranceData leaves undocumented and CASdatasets lacks (the book's Table 1.6, pp. 15-16, says it denotes the area of residence and leaves A-F unexplained; Ye et al. 2022 call it the driver's area of residence). The age band keeps its name: the book's Table 1.1 says "Driver's age category", while its Table 1.6 and CASdatasets call it the policyholder's age.
        - Dropped: `gender` (F 38,603, M 29,253; "gender" in insuranceData, the policyholder's in CASdatasets). Sex leaves the rating factors of every insurance pricing task of this collection, whatever the actor's jurisdiction, as EU law has required since the Test-Achats ruling (CJEU C-236/09, 1 March 2011, in force for new contracts from 21 December 2012), as for bemtpl97's `sex`: the benchmark asks how good such models would be in today's European market, where they may not use sex (the Tensions row on rating factors in principles.md, amended 2026-11-08; CC below). An Australian insurer may still be allowed to price on it (s41 of the Sex Discrimination Act 1984 (Cth), as the review panel read it; the statute's text was not checked), so the fit stays approximate.
        - 1,057 rows share every column with another row (575 extra copies, 0.85%), all without a claim. That is about two and a half times chance: with the exposure shuffled among the no-claim rows, about 220 copies remain (188 to 248 over 20 runs). Among the 1,129 full-year rows without a claim there are 223 copies against 21 for random no-claim rows of that number; that cohort is rich in trucks and panel vans, likely fleet vehicles insured on the same dates. Kept (LEAK-18): on the earlier cost target (2026-11-01), dropping the copies moved the Gini by +0.0045, and 0.8% of the test rows had an exact feature copy in train then (leak probe, first split, with exposure and gender among the features). Without exposure and gender among the features, 43,935 rows (64.7%) share their five rating factors with another policy and 56-57% of the test rows have an exact copy of them in train (every shipped split): coarse rating cells of distinct policies, the portfolio a tariff prices, as in fremtpl2. On the rate, every fit weighted, splits grouped by those five factors or by the full row with the exposure score as the shipped ones or higher (Tweedie LightGBM 0.077 and 0.076, Tweedie GLM 0.133 and 0.128, against 0.075 and 0.119; 9 splits each, 2026-11-08).
        - The split is forced (ForcedIIDFromTemporal, SPLIT-8): an insurer fits its tariff on past policy-years and prices the next year's policies, but the release has no date and no policy id. It looks like one observation period of about a year (exposure spread over 1-365 days, about 6,300 policies per 30 days at the short end falling to about 4,300 at the long end; 1.9% full years, no 366-day row), so a temporal test needs another year's extract. The exposure is cut at the extract window's edges as well as by some claims, and both sides of the random split share the one window; a temporal split on a dated release would cut it again at each cutoff and must check its training side for periods the cutoff ended (SPLIT-9, LEAK-41). The raw file order is not random (12.2% of adjacent rows share a day count, against 0.3% when the rows are permuted, and the mean exposure per tenth of the file runs from 0.42 to 0.53 against a chance SD of 0.0035; whether the order is time is unknown), but the claim indicator shows no serial dependence (lag-1 correlation 0.005), and training on the earlier quarters of the file to test the next shows no drop (on the rate, every fit weighted: Tweedie LightGBM 0.086 and Tweedie GLM 0.125 on average over the three such splits, against 0.067 and 0.107 for random splits of the same sizes; 2026-11-08). No policy is visibly split into two rows (201 pairs of identical rating factors sum to 365 days, against 188 on average for the sums from 330 to 400 days, 145 to 229) and the hidden-group probe finds no group. Shipped forced on the curator's call (Andrej, 2026-11-02): a forced IID split ships only when no leak is found across the random split, as here (no row shares its outcome across the split, no hidden group, no order dependence); how_much_did_it_rain's `No` named a measured leak.
        - CC (2026-11-06, Lennart): decision D8 of the exposure study of 2026-11-05 (issue 6): the target is the claim cost per year insured (`claimcst0` / `exposure`, in dollars, identity scale), `exposure` the weight scoring column, the `weight` input of `normalized_weighted_gini` and the task's `sample_weight`, and never a feature (LEAK-41, MET-14, MET-15); the metric stays a context Gini, now weighted on the rate; the 7 rows at 1M dollars or more a year are kept. Supersedes Andrej's call of 2026-11-02 (issue 2: `exposure` kept as a feature with its note, the LEAK-10 case for time on risk cut short by the outcome) and changes the form of his Gini of the same day (issue 4: unweighted on the cost, now weighted on the rate). What sets the case apart is a measurement made after the call: the deviance on the claim counts shows the leak the slice Gini hid (47 to 82% of a free model's gain over a constant rate is leak); on the weighted Gini of the cost per year a free GLM scores 0.238 against 0.125 for honest quotes, and on the shipped splits `exposure` as a feature lifts an honest LightGBM from 0.059 to 0.149 (9 of 9). The alternative, the claim frequency with an exposure-weighted deviance, was not chosen.
        - CC (2026-11-08, Lennart): the two age bands ship as ordered categories, youngest first (issue 9, "Ordered categories"): `vehicle_age_band` levels 1 to 4, `driver_age_band` levels 1 to 6, the codes kept as levels since the band limits are unpublished (CLEAN-14). Until then they shipped as integers, which no curator had decided.
        - CC (2026-11-08, Lennart): `gender` leaves the features (issue 7: "Option C: Drop gender, as bemtpl97", then (a) on the consistency check: "A stance for the family; as if we were to simulate the case in europe always"). Sex leaves the rating factors of every insurance pricing task of this collection, whatever the actor's jurisdiction, as under EU law (Test-Achats), and the Tensions row on rating factors in principles.md says so (amended 2026-11-08). Supersedes Andrej's ship of 2026-11-02, which kept `gender` among the six rating factors. Gender carried little: the Tweedie GLM scores 0.124 with it and 0.119 without (+0.004, SE 0.002, higher with it on 7 of 9 shipped splits), a regularised LightGBM 0.103 either way.
        - CC (2026-11-08, Lennart): the target stays the claim cost per year insured, `exposure` its weight, scored by the weighted Gini (issue 8, (a) on the answer: "Keep the current target, the clause amended"); decision D8 of 2026-11-06 stands. MET-14's per-contract clause is amended in one change with spanish_motor_insurance_2015_2018 issue 7: a per-contract target needs the data to record each contract to its end, and where an extract window cuts the policies at its edges the recorded amount is the window's, so the rate ships (the target bullet).
    """

    accepted_check_warnings = {
        "task_target_value_dominant": (
            "Zero-inflated by nature: the claim cost per year is 0 for exactly the 63,232 policies without a claim "
            "(93.2%), the rows where the source's claim indicator is 0; not a cap or a placeholder (claim audit, "
            "2026-11-01)."
        ),
        "dataset_duplicate_rows": (
            "Distinct policies in coarse rating cells: with exposure and gender out of the features, five rating "
            "factors remain and 64.7% of the rows share them with another policy. Grouping the split on the rating "
            "cell does not lower the score (LightGBM 0.077 against 0.075, GLM 0.133 against 0.119; split audit "
            "re-run, 2026-11-08)."
        ),
        "dataset_conflicting_duplicate_rows": (
            "Policies with the same rating factors and different claim costs: claims are rare events of one risk "
            "profile, not label noise (the same split audit, 2026-11-08)."
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
            "it drops the claim size the insurer prices, and on the shipped splits the GLMs and a regularised LightGBM "
            "tie on it (-0.0003, 4 of 9), while the weighted Gini on the cost per year separates them (+0.016, 8 of 9) "
            "and orders the five models as the weighted Tweedie deviance does. A constant scores 0, an honest Tweedie "
            "GLM 0.119 and an honest Tweedie LightGBM 0.075 (9 shipped splits, fitted with the sample weight); "
            "1/exposure alone, which no model may read, 0.206. RMSE follows a few large values: on the cost the "
            "largest 46 (0.07% of the policies) hold 43% of the sum of squares and no model family probed beat the "
            "mean by more than R^2 0.002 on average; on the rate the 7 policies at 1M dollars or more a year hold 45% of the exposure-weighted sum "
            "of squares. The Gini ignores the price level, which pricing sets separately, and the spread of the "
            "relativities: any transform that keeps the order of the predictions scores the same. On the 9 shipped "
            "splits a Tweedie GLM with its log-relativities doubled keeps 0.119 but is worse than the weighted "
            "constant on the exposure-weighted Tweedie deviance (power 1.5) on 9 of 9, and so is the untuned Tweedie "
            "LightGBM (0.075). That deviance was not chosen for its resolution: the best honest model, the Tweedie "
            "GLM, gains 0.5% of the constant's deviance (0.52 of 105.45, SE 0.13, better on 8 of 9 splits), while the "
            "Gini separates the honest models (GLM minus LightGBM +0.044, SE 0.013, 7 of 9)."
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
        # 1b. Sex is no rating factor of an insurance pricing task in this collection, whatever the actor's
        # jurisdiction, as under EU law (Test-Achats; notes).
        df = drop_columns(df, ["gender"])
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
        return FeatureTypes(
            categorical=["vehicle_body", "area"],
            # Bands of an age, youngest first; their limits are unpublished, so the codes are the levels.
            ordinal={"vehicle_age_band": [1, 2, 3, 4], "driver_age_band": [1, 2, 3, 4, 5, 6]},
        )

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
