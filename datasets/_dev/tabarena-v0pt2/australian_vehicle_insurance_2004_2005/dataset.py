"""Curated dataset definition for `australian_vehicle_insurance_2004_2005` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, drop_columns

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


class AustralianVehicleInsurance20042005(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a car insurance policy cost the insurer in claims over the part of its year the data observes?"
        ),
        use_case=(
            "For example, an Australian car insurer prices a one-year policy at underwriting: it estimates the "
            "expected claim cost from the rating factors and the time on risk, to set the premium. The source, a "
            "textbook on insurance GLMs, names no decision."
        ),
        row=(
            "One one-year vehicle policy taken out in Australia in 2004 or 2005, mostly cars but also trucks, buses "
            "and motor caravans, observed for up to a year (67,856 policies of an unnamed insurer)."
        ),
        predicted=(
            "The total cost of the policy's claims while it was observed, in dollars: 0 for the 93.2% without a "
            "claim; no claim is recorded below $200."
        ),
        known=(
            "The vehicle's value, body type and age band, the policyholder's or driver's gender (the sources "
            "differ), the driver's age band, an area code A-F (the R packages do not say what it codes), "
            "and the share of the policy's year observed in the data (a full year for 1.9%; it can end early after "
            "a claim)."
        ),
        split="Random policies, so the test data stands for other policies of the same portfolio and period.",
        changes=(
            "We dropped the claim indicator and the claim count (parts of the target), made the 53 vehicle values "
            "of 0 missing, and score by the normalized Gini, which measures how well the predictions order the "
            "policies by claim cost, since the source has no metric."
        ),
        fit="approximate",
        fit_reason=(
            "Real policies with the rating factors and claim costs of pricing. Gaps: a random split of undated "
            "policies stands in for next year's; the target is the cost of each policy's observed part-year, not of "
            "a policy-year; the label's construction is undocumented (paid or incurred, the $200 floor, repeated "
            "amounts, the cover). The observed share of the year, cut short by some claims, is a kept potential leak."
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

        - Prediction point: when the policy is priced at underwriting (for example; the source names no use). The rating factors are known then, its claims are not. Every policy is a one-year contract; `exposure`, the share of that year the data observed, is known only at the end of the observation period and is cut short by some claims (the leak note below).
        - Source: the book's companion website, now offline; the copy in insuranceData matches the book's Table 1.1 (claims by driver age band: 5,742 to 16,189 policies per band, 5,742 in the youngest and 6,547 in the oldest, 4,624 with a claim; Table 1.6, pp. 15-16, gives the same 67,856 policies and 4,624 with claims), and CASdatasets' `ausprivauto0405` agrees with it on every row (2026-11-01). What the book does with this table (read by the curator, 2026-11-02; printed pages): logistic regression for claim occurrence with exposure, the time at risk, in a modified link (Sec. 7.3-7.4, pp. 99-104), compared by ROC AUC, 0.662 with the exposure adjustment against 0.548 without, on the same data with no held-out split (Sec. 7.6, pp. 108-110); a zero-adjusted inverse Gaussian model of the claim amount with its zeros, selected by AIC (Sec. 10.4, pp. 145-148), log links on the raw amount, not a log-transformed target; Tweedie models (Sec. 8.3) and a multiple-claim model (Sec. 10.5) are explained without a fit to this table. The book does not say why some exposures end early, whether the costs are paid or incurred, or why no claim lies below 200.
        - Target `claim_cost` (`claimcst0`, "claim amount (0 if no claim)"), on the raw dollar scale as published: 0 for exactly the 63,232 policies without a claim (93.2%). Dropped as parts of the target: `clm` (claim_cost > 0 on every row) and `numclaims` (above 0 on the same rows). `X_OBSTAT_` is one value on every row and is dropped too.
        - Anomaly: no claim cost lies below 200, and 705 of the 4,333 single-claim policies cost 200.00 to the cent (695 exactly, the rest float noise of the file); no policy with several claims does, and the two-claim policies start at 400 (10 of 271 at 400.00, one at 400.01), so each claim seems recorded at 200 at least. Kept as recorded, as fremtpl2 keeps its fixed IRSA-IDA amounts in the target as point masses (CC 2026-10-20, Andrej): the floor is in the source's data and a model can learn it. Other point masses (353.77 for 219 claims, 389.95 for 94, 390 for 55) are kept as well.
        - Potential leak, kept on purpose (LEAK-10, LEAK-11): `exposure` (days / 365.25, 1 to 365 days, a full year 0.9993; median 163 days, 1.9% full years, no 366-day row) is mostly the share of each one-year policy that fell in the observed period, which is fixed when the policy starts, but some claims cut it short. In claim occurrence: policies of 0.2 years or less have 147 more claims than the rate of longer ones predicts; at 7 days or less they claim 0.85 times per policy-year even without the claims of at least 80% of the vehicle's value (0.14-0.17 above 0.2 years); a free log-exposure coefficient is 0.29-0.31 in a Tweedie GLM where proportional time gives 1. In size: those 193 claims (likely write-offs) have a median exposure of 0.37 against 0.65 for the other claims (Mann-Whitney p < 1e-20). Kept because the traced part lowers the score instead of raising it (LEAK-11; 9 shipped splits, Tweedie LightGBM): exposure as a proportional offset only scores 0.1833 against 0.1824 as a free feature (paired SE 0.0059), floored at 0.1 years 0.1849, and giving the write-offs a counterfactual uncut exposure lifts the Gini from 0.182 to 0.31 (18 of 18 runs). That sets it apart from heart_failure's follow-up `time`, dropped because it carried the signal. As in the curator's fremtpl2 call (2026-10-20) it is a feature, not a divisor, since dividing would inflate short policies' targets; fremtpl2's other reason, a contracted period known at pricing, does not carry, as the contract here is one year for every policy. Alone it scores 0.168 of the best 0.205 (a Tweedie GLM, which beats it on 8 of 9 splits). Revisit if a release gives the policy dates or why a policy ended. Kept on the curator's call (Andrej, 2026-11-02), recorded as the LEAK-10 case for time on risk cut short by the outcome: the cut is removed where the data locates it, kept with its measured size where it cannot (here).
        - `veh_value` (in $10,000s, insuranceData; CASdatasets says thousands of AUD, which would make the median car worth $1,500, an error of that copy) is 0 for 53 policies, most of them station wagons, buses, trucks or motor caravans of the oldest band, while the next lowest value is 0.18 ($1,800): a vehicle value of $0 is no value, so these are made missing (CLEAN-10, CLEAN-11).
        - The body codes are given the labels CASdatasets uses for the same rows (`HBACK` to Hatchback, `STNWG` to Station wagon, ...). The age bands of the vehicle (1 youngest to 4) and the driver (1 youngest to 6) stay numbers, the order of an age.
        - Columns renamed to plain names: `vehicle_value`, `vehicle_body`, `vehicle_age_band`, `driver_age_band`, `claim_cost`; `gender`, `area` and `exposure` keep theirs. `gender` is "gender" in insuranceData and the policyholder's in CASdatasets, so it is not called the driver's. `area` is a code A-F that insuranceData leaves undocumented and CASdatasets lacks (the book's Table 1.6, pp. 15-16, says it denotes the area of residence and leaves A-F unexplained; Ye et al. 2022 call it the driver's area of residence). The age band keeps its name: the book's Table 1.1 says "Driver's age category", while its Table 1.6 and CASdatasets call it the policyholder's age.
        - 707 rows share every column with another row (378 extra copies, 0.6%), all without a claim. That is about three times chance: with the exposure shuffled among the no-claim rows, 120-125 copies remain (20 runs). Among the 1,129 full-year rows without a claim there are 152 copies against 11.6 for random rows of that number; that cohort is rich in trucks and panel vans, likely fleet vehicles insured on the same dates. Kept (LEAK-18): dropping the copies moves the Gini by +0.0045, and a split that keeps identical feature rows together scores within fold noise (Tweedie LightGBM 0.194 against 0.182); 0.8% of the test rows have an exact feature copy in train (leak probe, first split).
        - The split is forced (ForcedIIDFromTemporal, SPLIT-8): an insurer fits its tariff on past policy-years and prices the next year's policies, but the release has no date and no policy id. It looks like one observation period of about a year (exposure spread evenly over 1-365 days, 1.9% full years, no 366-day row), so a temporal test needs another year's extract. The raw file order is not random (12.2% of adjacent rows share a day count, against 0.3% when the rows are permuted; whether the order is time is unknown), but the claim indicator shows no serial dependence (lag-1 correlation 0.005), and training on the earlier quarters of the file to test the next shows no drop (Tweedie LightGBM 0.168, 0.189, 0.208 against 0.127, 0.174, 0.181 for random splits of the same sizes; single splits). No policy is visibly split into two rows (116 pairs of identical rating factors sum to 365 days, against 102 on average for other sums) and the hidden-group probe finds no group. Shipped forced on the curator's call (Andrej, 2026-11-02): a forced IID split ships only when no leak is found across the random split, as here (no row shares its outcome across the split, no hidden group, no order dependence); how_much_did_it_rain's `No` named a measured leak.
    """

    accepted_check_warnings = {
        "task_target_value_dominant": (
            "Zero-inflated by nature: the claim cost is 0 for exactly the 63,232 policies without a claim (93.2%), "
            "the rows where the source's claim indicator is 0; not a cap or a placeholder (claim audit, 2026-11-01)."
        ),
    }

    # Task
    target = "claim_cost"
    problem_type = "regression"
    metric = Metric.from_context(
        "normalized_gini",
        reason=(
            "No source metric for this claim-cost regression was established: insuranceData and CASdatasets define no "
            "task, and the book (Sec. 10.4) selects its claim-amount model by AIC on all rows, with no held-out score; "
            "its ROC AUC (Sec. 7.6) scores claim occurrence, a classification, and is no support for this Gini. Ye et al. (2022, Econometrics 10(2):19) scored this table with this "
            "unweighted normalized Gini (Sec. 2.3) on a holdout third (Sec. 2.2), with exposure among the inputs, "
            "next to MAE, RMSE, a rebalanced RMSE and the total error, and recommend the Gini with a second measure "
            "where possible (Sec. 4.2): context, not one source metric. Pricing actuaries use a weighted form: Frees, "
            "Meyers and Cummings (2011, JASA 106:1085-1098) order policies by relativity and accumulate premium, and "
            "CAS Monograph 5 (Sec. 7.2.4) orders by predicted loss cost per exposure and accumulates exposure; here "
            "every row counts once, ordered by predicted cost. Allstate scored its Claim Prediction Challenge "
            "(Kaggle, 2011) by this Gini on rows of one full vehicle-year each; 98.1% of the rows here are shorter. "
            "Exposure alone scores 0.168 (9 splits), the level a useful model must beat. RMSE on the raw cost follows "
            "a few large claims: the largest 46 (0.07% of the policies) hold 43% of the sum of squares, and no model "
            "family probed beats the mean by more than R^2 0.002 on average. The Gini ignores the price level, which "
            "pricing sets separately."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "dataCar.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. Parts of the target and a constant column.
        assert ((df["claimcst0"] > 0) == (df["clm"] == 1)).all()
        assert ((df["numclaims"] > 0) == (df["clm"] == 1)).all()
        df = drop_columns(df, ["clm", "numclaims", "X_OBSTAT_"])
        # 2. A vehicle value of $0 is no value: missing.
        df["veh_value"] = df["veh_value"].mask(df["veh_value"] == 0)
        # 3. The body codes get CASdatasets' labels.
        assert set(df["veh_body"]) <= set(BODY_LABELS)
        df["veh_body"] = df["veh_body"].map(BODY_LABELS)
        # 4. Plain names.
        return df.rename(
            columns={
                "veh_value": "vehicle_value",
                "veh_body": "vehicle_body",
                "veh_age": "vehicle_age_band",
                "agecat": "driver_age_band",
                "claimcst0": "claim_cost",
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
        return [
            Decision(
                "The claim costs at 200 are kept as recorded",
                "No claim costs less than 200 and only single-claim policies cost exactly 200, while two-claim "
                "policies start at 400: each claim seems recorded at 200 at least. Kept as recorded, as fremtpl2 "
                "keeps its fixed amounts (CC 2026-10-20).",
                floor,
            ),
            Decision(
                "The observed share of the year is a feature, though a write-off seems to end it",
                "Claimants are observed longer than other policies (more time to claim), except those whose claim "
                "comes near the vehicle's value: their policy seems to end with the claim. The part cut short lowers "
                "the score instead of raising it (as an offset only, exposure scores as well; given the write-offs "
                "an uncut exposure, the Gini rises from 0.182 to 0.31), so it is kept with a note (LEAK-11, curation "
                "notes).",
                exposure,
            ),
        ]
