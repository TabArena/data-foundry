"""Curated dataset definition for `spanish_motor_insurance_2015_2018` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

RAW_FILE = "Motor vehicle insurance data.csv"
TARGET = "log1p_cost_claims_year"
DATES = [
    "Date_start_contract",
    "Date_last_renewal",
    "Date_next_renewal",
    "Date_birth",
    "Date_driving_licence",
    "Date_lapse",
]
# The claims cut-off: the data "includes claims up to 2018" (Sec. 3), so a year that starts in 2018 is cut short.
COMPLETE_BEFORE = pd.Timestamp("2018-01-01")
# The codes of the variable sheet ("Descriptive of the variables.xlsx"), with their labels.
LABELS = {
    "Distribution_channel": {0: "agent", 1: "broker"},
    "Type_risk": {1: "motorbike", 2: "van", 3: "passenger car", 4: "agricultural vehicle"},
    "Area": {0: "rural", 1: "urban"},
    "Second_driver": {0: "no", 1: "yes"},
    "Type_fuel": {"P": "petrol", "D": "diesel"},
}


def _parse_and_order(raw: pd.DataFrame) -> pd.DataFrame:
    """The dates parsed, the rows of a policy in time order, each row's position `k` among them and their count `n`."""
    df = raw.copy()
    for col in DATES:
        df[col] = pd.to_datetime(df[col], format="%d/%m/%Y")
    df = df.sort_values(["ID", "Date_last_renewal"], kind="stable")
    by_policy = df.groupby("ID", sort=False)
    df["k"] = by_policy.cumcount()
    df["n"] = by_policy["ID"].transform("size")
    df["prev_claims"] = by_policy["N_claims_year"].shift(1)
    return df


def _covered(df: pd.DataFrame) -> pd.Series:
    """A year with cover: a renewal not taken up has its lapse on or before the year's start, so no day at risk."""
    return df["Date_lapse"].isna() | (df["Date_lapse"] > df["Date_last_renewal"])


def _whole_years(since: pd.Series, at: pd.Series) -> pd.Series:
    """Completed years from `since` to `at`, by the calendar (a renewal on the anniversary counts the full year)."""
    before = (at.dt.month < since.dt.month) | ((at.dt.month == since.dt.month) & (at.dt.day < since.dt.day))
    return at.dt.year - since.dt.year - before.astype(int)


class SpanishMotorInsurance20152018(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a Spanish motor policy cost the insurer in claims in its first year, from the vehicle, the "
            "driver and the quoted premium?"
        ),
        use_case=(
            "A Spanish motor insurer writing a new contract for a customer with no other policy at the insurer refines "
            "its quoted premium: it estimates the first year's claim cost from the rating factors and the quote, to "
            "find the risks the quote prices too high or too low. The data article names pricing mechanisms for new "
            "business among the uses."
        ),
        row=(
            "One policy's first year of cover in the release, at an unnamed Spanish non-life insurer, for a customer "
            "with one policy in force: a new contract written from November 2015 to December 2017, or for an older "
            "contract its year renewed from November 2015 to November 2016 (25,665 policies; cars, vans, motorbikes "
            "and farm vehicles)."
        ),
        predicted=(
            "The year's claim cost, payments plus reserves, in euros: 0 for 67% of the policies. Shipped as log1p, "
            "scored on the amount."
        ),
        known=(
            "The vehicle (type, age, power, engine size, value, doors, fuel, size and weight), the driver's age and "
            "years licensed, a second driver, rural or urban area, the sales channel, the contract's age and the "
            "year's premium."
        ),
        split=(
            "Five monthly windows, August to December 2017, each trained on the policy-years that had ended by the "
            "window's start, so the test data stands for the new contracts of a coming month, priced from the "
            "claims the insurer already knows in full."
        ),
        changes=(
            "We keep only each policy's first year in the release (the later yearly rows hold a shrinking remnant "
            "of its claims) and only customers with one policy in force (a customer's concurrent policies claim "
            "together). We drop renewals never in force, years starting in 2018 (claims stop then) and the columns "
            "read at the policy's end (claim history, lapses, seniority, payment method)."
        ),
        fit="approximate",
        fit_reason=(
            "Real new contracts with the insurer's rating factors and premium. But the cover bought, the driver's "
            "claims history and the territory are missing; the carry-over of claims between years is undocumented; "
            "customers with several policies are left out; 1,236 years cut short by a lapse count as full (the cut "
            "is known only at the end); the sample's design is not described. The 2019 vehicle value is kept on "
            "purpose."
        ),
    )

    # Dataset
    unique_name = "spanish_motor_insurance_2015_2018"
    year = "2023"
    domain = "insurance"
    source = "Other"  # Mendeley Data, the repository the authors published in; no closer schema value
    source_url = "https://doi.org/10.17632/5cxyb5fp4f.2"
    license = "CC BY 4.0"
    data_tags = ()
    download_description = """
        Version 2 of the Mendeley Data record (DOI 10.17632/5cxyb5fp4f.2, published 2024-07-30, CC BY 4.0) holds
        three files: the portfolio (semicolon-separated CSV, 105,555 rows x 30 columns), the variable descriptions
        and a sample of claims by type. The file links come from the record's API
        (https://data.mendeley.com/public-api/datasets/5cxyb5fp4f/files?folder_id=root&version=2), which also gives
        each file's SHA-256 (checked on 2026-11-01). Version 1 (10.17632/5cxyb5fp4f.1, 2023-08-10) has the same rows;
        it holds "00/01/1900" in 3,416 cells of Distribution_channel, which version 2 sets to 0. A copy sits on
        openICPSR (project 193182).

        mkdir -p local-data-warehouse/spanish_motor_insurance_2015_2018 && cd local-data-warehouse/spanish_motor_insurance_2015_2018
        wget -O "Motor vehicle insurance data.csv" https://data.mendeley.com/public-files/datasets/5cxyb5fp4f/files/e83f1f20-b93e-4971-97a4-5c9a2b7baeef/file_downloaded
        wget -O "Descriptive of the variables.xlsx" https://data.mendeley.com/public-files/datasets/5cxyb5fp4f/files/965e3003-666a-4965-a7a2-ec5130ad1ad2/file_downloaded
        wget -O "sample type claim.csv" https://data.mendeley.com/public-files/datasets/5cxyb5fp4f/files/f06af09a-39fa-41e2-9ac1-31a70535531e/file_downloaded
        sha256sum "Motor vehicle insurance data.csv" "Descriptive of the variables.xlsx" "sample type claim.csv"
        # 00061a64e355a7f9bbd06f1bcd3f0846b1f849955119a812acf2bc7781ee293a  Motor vehicle insurance data.csv
        # 8b451e1898ca42e7092d4011c8e7071235fdc6e859a4e24070960580df433cc2  Descriptive of the variables.xlsx
        # d35d967d66563ea291fd6d450cbfdf52f5118c5e7b3625b7b3a9bfa5a9361c3d  sample type claim.csv
    """
    bibtex = r"""
        @article{seguragisbert2025motor,
          title = {Dataset of an actual motor vehicle insurance portfolio},
          author = {Segura-Gisbert, Jorge and Lled{\'o}, Josep and Pav{\'i}a, Jose M.},
          journal = {European Actuarial Journal},
          volume = {15},
          pages = {241--253},
          year = {2025},
          doi = {10.1007/s13385-024-00398-0},
          note = {Data: Mendeley Data, version 2, doi:10.17632/5cxyb5fp4f.2; version 1 published 10 August 2023}
        }
    """
    curation_comments = """
        We start with "Motor vehicle insurance data.csv" of Mendeley Data 5cxyb5fp4f, version 2 (Lledó and Pavía; described by Segura-Gisbert, Lledó and Pavía 2025, European Actuarial Journal 15:241-253, read through the publisher's open-access page, CC BY 4.0).

        - Prediction point: the start of a policy's year of cover, when the insurer prices it: for a new contract the day it is written, for an older contract its renewal. The vehicle, the driver and the year's premium are known then; the year's claims are not. Sec. 3: "Each row represents an insurance policy that is automatically renewed annually"; the rows of a policy are consecutive years (each starts on the previous row's next renewal).
        - Year: version 1 of the Mendeley record was published on 10 August 2023 with the same rows; version 2 (30 July 2024) sets 3,416 cells of Distribution_channel that read "00/01/1900" to 0.
        - Years without cover are dropped (USE-7): 5,069 first rows of complete years (12.0%) are an older contract's renewal that never came into force, with `Date_lapse` on the year's start (4,971) or before it (98). Each is its policy's last row, no day of it is at risk, and it holds 14 claims (0.3%). The rule reads the dates, not the label (LEAK-25), as spanish_motor_insurance_coverage_level_2022_2024 drops its years without time at risk.
        - Only each policy's first row in the release is kept (37,090 of the 58,990 complete years with cover). The later rows hold almost no new claim: after a year without claims, 0.9% of the next years have one (133 of 14,980), against 33% of the first rows of older contracts and 38% of new contracts; after a year with claims, the count is below the previous year's in 99.9% of the next years (6,911 of 6,920). 96.5% of the later rows' claim cost sits on rows that follow a year with claims, and the previous year's claim count alone ranks the later rows at a normalized Gini of 0.86. So a later row's cost is a shrinking remnant of the first year's claims (likely the same claims still open, with that year's payments and reserves), not the year's new risk; the source does not explain it, and the 2022-2024 release of the same group shows 17.4% after a claim-free year, so the defect is this release's. The first rows behave like a year's claims: for older contracts the claim share stays at 32-35% in every renewal month from November 2015 to November 2016. (USE-5, PROV-13: the authors offer "the pre-cleaned raw data", Sec. 1, which might show the claims by year.)
        - Years that start in 2018 are dropped (35,815 rows, 11,343 of them first rows): the data "includes claims up to 2018" and "the most recent claims exhibit a run-off with pending developments" (Sec. 3), so a year renewed in 2018 is cut short; the claim share of first rows falls from 28-39% for new contracts written in each month of 2017 to 0.5% for those written in October and November 2018 (LEAK-24, the record's suggested call).
        - Only customers with one policy in force are kept (`Policies_in_force` 1, "policies held by the insured in the insurance entity during the reference period"; 25,665 of 37,090 rows), and the column, then constant, goes (USE-5). A policy's claims move with those of the same customer's other policies running at the same time: among 2,493 first rows that have such a policy in the sample (a customer matched on birth and licence dates), 80% claim when that policy claims and 6% when it does not, 1,519 of 1,532 such pairs insure different vehicles, and the link grows with the days the two years overlap, while the same customer's years more than 180 days apart give 21% against 12%. Claims per row grow with the count (0.64, 0.95, 1.28, 1.76 and 3.15 for one to five or more policies) while the cost per claimant stays at 730-910, so the costs are not one claim split across policies; the release cannot tell claims booked across a customer's policies from customers who claim together (EV-1). With every first year kept, a model's gain over the premium came almost entirely from the count. The count covers the calendar year, so customers who add a policy later in the year go too; they claim at the same rate as the rest (31.2% against 31.2%), so the filter does not select on the outcome. Revisit if the authors show that claims are booked per policy (PROV-13).
        - Target `log1p_cost_claims_year`, log1p of `Cost_claims_year` ("Total cost of claims for the insurance policy during the current year"; Sec. 3: "The Cost_claims_year variable includes both payments and reserves"), the scale a model of a skewed amount is fit on; the metric is computed on the amount (`target_transform="log1p"`, MET-3), as in frempl_french_motor_personal_line and spanish_motor_insurance_coverage_level_2022_2024. No negative amounts; the smallest positive cost is 40.05. 67.2% of the rows cost 0, exactly those with `N_claims_year` 0.
        - Why log1p and not the raw amount (MET-3): untuned LightGBM ranks the 5 shipped windows at a mean Gini of 0.116 fit on log1p, about the 0.121 of a Tweedie loss on the amount (the actuarial loss) and above the 0.073 of squared error on the amount. The Gini is computed on the amount either way.
        - Only the claim part carries signal (the hurdle check of task_probes.md, 5 shipped windows): a claim is ranked at ROC AUC 0.56 to 0.62, while a severity model on the claimants reaches R^2 -0.12 to -0.04 on log costs and below 0 on the costs, and the true claim indicator times the claimants' mean explains 8% to 19% of the variance of the amount. A hurdle model (claim probability times severity) ranks at a mean Gini of 0.115, the direct log1p model at 0.116.
        - Dropped as parts of the target: `N_claims_year` (the year's claim count, 0 exactly where the cost is 0).
        - Dropped as measured after the prediction point (LEAK-10): `N_claims_history` ("throughout the entire duration of the insurance policy"; it also counts the customer's other policies: for new contracts it exceeds the sum of the policy's rows for 58% of multi-policy customers and 6% of single-policy ones) and `R_Claims_history` (it over the policy's whole years in force), one value for every row of a policy; `Lapse` (the customer's lapses "in the current year of maturity") and `Date_lapse` (the contract's termination date, one value for every row of a policy, used only to find the years without cover); `Max_policies` and `Max_products` (the most policies or products the customer "has ever had", one value for every row of a policy). As published, these columns lift an untuned LightGBM from a normalized Gini of 0.13 to 0.84 (the 5 shipped windows).
        - `Seniority` dropped, not rebuilt. It is one value for every row of a policy: for customers with one policy, the years from the contract's start to the policy's last next renewal (to the nearest year for 92% of them), so it counts the years the policy will still run. Subtracting the rows still to come gives the seniority at each row's start, but the rebuild leaks where the rule fails: among new contracts of single-policy customers, the 442 rows the rebuild puts at 1 instead of 0 have a claim in 65%, against 32% for the 8,344 at 0. The contract's age at the year's start (`contract_years`) stays.
        - `Payment` dropped (LEAK-10): the "Last payment method of the reference policy" (variable sheet), one value for every row of a policy, so it may be read after the year, and it shows a pattern that cannot be traced: among policies that renewed, 40% of the first years with a claim are paid half-yearly, against 26% of those without one (a switch after a claim, or half-yearly payers without a claim lapsing more often). That dropping it changes no score is no reason to keep a late value (zillow_prize, melbourne_housing_market).
        - The dates become ages at the year's start, in completed years by the calendar (a renewal on the contract's anniversary counts the full year): `driver_age` (from `Date_birth`), `years_licensed` (from `Date_driving_licence`), `contract_years` (from `Date_start_contract`) and `vehicle_age` (the year's calendar year minus `Year_matriculation`). `Date_last_renewal` is the time column `period_start`. `Date_next_renewal` (one year later), `ID` (the "combination of policyholder and product", in the data article's words; one row per policy now) and the raw dates are dropped.
        - Impossible values made missing (CLEAN-11): a driving licence dated after the year's start (12 rows, their `years_licensed`) and a contract dated after it (8 rows, their `contract_years`; 5 of them start in 2017, the only first rows after November 2016 that are not new contracts).
        - A block without vehicle data (CLEAN-10): 30 rows (29 motorbikes, 1 farm vehicle) have a power of 0 horsepower and no fuel type; the power is made missing and the fuel stays missing.
        - The codes get the labels of the variable sheet: `Distribution_channel` (agent, broker), `Type_risk` (motorbike, van, passenger car, agricultural vehicle), `Area` (rural, urban; urban is over 30,000 inhabitants), `Second_driver` (no, yes) and `Type_fuel` (petrol, diesel); all categorical. `Length` is missing for every motorbike, 135 of the 139 farm vehicles, 180 cars and 62 vans; it stays missing. `N_doors` is 0 for motorbikes, as recorded.
        - Note: `Premium`, the year's net premium (Sec. 3: "after deducting taxes but including both internal (administrative) and external (commercial) expenses"), is kept: the insurer's own price, set when the year starts (USE-6), and the natural core of the task, not a lookup (TP-4). The premium alone ranks the 5 windows at a mean Gini of 0.234; of the models tried, ridge and logistic regression reach 0.230, a LightGBM tuned on an inner time split 0.176 and untuned LightGBM 0.116, and the premium matches or beats the best of them in 3 of the 5 windows (not in August and October 2017). It does not follow the year's claims: after a claim-free year the median change of the premium to the next year is +0.5% whether or not the new year has a claim, against +2.0% after a year with claims (all rows of the release).
        - Potential leak, kept on purpose: `Value_vehicle` is the "Market value of the vehicle on 31/12/2019" (variable sheet), a valuation after every year in the data. It is a property of the vehicle, the same in every row of a policy, and not of the policy's claims: the vehicle's type, age, power, engine size, doors, fuel, size and weight explain 97% of the log value, and the rest does not rank the policies with a claim (ROC AUC 0.497; 0.492 for a cost over 2,000), so it does not move with the claims. Without it, untuned LightGBM ranks the 5 windows at 0.140, against 0.116 with it, inside one window's noise. Revisit if the source gives the value at each renewal.
        - Note: two rows are identical in every column (two policies, claim-free, written in February 2016, training side only): distinct policies (a fleet of identical vehicles, or two policies of one holder), kept (LEAK-18).
        - Anomaly: 1,726 positive costs (8.8% of all positive costs in the release, 258 of the 264 at this amount in the claim-type sample are "negligence") are exactly 882, and 91 are 1,764: a flat amount, as the CICOS agreement between Spanish insurers sets (spanish_motor_insurance_coverage_level_2022_2024 has 882 in 2022). Kept as recorded.
        - Anomaly: 77 of the 139 farm vehicles share one of four combinations of engine size, weight and value (27, 22, 15 and 13 rows), each across vehicles registered from 1978 to 1998 or later, and every farm vehicle has 0 doors: fill values, not measurements (CLEAN-10). Kept as recorded; farm vehicles are 0.5% of the rows.
        - Anomaly: the claim share of new contracts' first years is 34-43% for those written from November 2015 to March 2016 and 24-34% for those of 2017, complete years both; a claim from the latest months may still be unreported (Sec. 3, run-off). Kept; the time column stays a feature.
        - Note: the sample's design is not described ("A sample dataset has been created from a Spanish insurance company specialized in non-life insurance", Sec. 3), and claims include travel assistance and complaints (the claim-type sample: travel assistance 56% of 7,366 typed claims), which fits a claim share near a third.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.from_context(
        "normalized_gini",
        reason=(
            "The data article describes the data and reports no model and no evaluation (European Actuarial Journal "
            "15:241-253, Secs. 1-7, read on the publisher's open-access page), and the Mendeley record defines no "
            "task. In insurance pricing, models are compared by the Gini index of an ordered Lorenz curve of losses: "
            "Frees, Meyers and Cummings (2011, JASA 106:1085-1098) order the policies by the ratio of a score to the "
            "premium, and the insurers' own Kaggle competitions (Allstate 2011; Liberty Mutual 2014, with weights) "
            "took the form declared here: the losses ordered by the prediction, each policy weighted 1. RMSE on the "
            "amount follows a few large claims (the largest cost is 260,853, 3.5% of all claim cost in the rows). The "
            "Gini ignores the price level, which pricing sets separately."
        ),
        target_transform="log1p",
    )
    temporal = Temporal(
        on="period_start", splits=TemporalSplits(window=1, unit="months", gap=12, min_train_fraction=0.5)
    )
    splits_comment = """
        A new-business price is refit on the policy-years whose claims are known and applied to the next contracts:
        5 test windows of one calendar month, December 2017 back to August 2017, newest first, each trained on the
        policy-years that had ended by the window's start, that is those that started at least twelve months before
        it (58-79% of the rows; the newest window trains on November 2015 to November 2016). A year's claims are
        known only when it ends, hence the 12-month gap (SPLIT-10); July 2017 would train on less than half of the
        rows (SPLIT-14). The 3,127 rows that start from December 2016 to July 2017 fall in every window's gap and
        are in no split. The test windows hold new contracts only (393 to 569 a month, 117 to 195 with a claim);
        the older contracts' first years in the release start before December 2016 and train only. Every model tried
        ranks November and December 2017 at -0.06 to 0.13 (October: up to 0.46), with no sign of run-off in their
        labels; they stay (SPLIT-21). One window's Gini has a bootstrap standard error of 0.08 to 0.11. Without the
        gap, untuned LightGBM ranks the same windows at a mean Gini of 0.141, against 0.116 with it.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE, sep=";")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. Dates parsed, the rows of each policy in time order; they are consecutive years of cover.
        df = _parse_and_order(raw)
        nxt = df.groupby("ID", sort=False)["Date_last_renewal"].shift(-1)
        assert (nxt.dropna() == df.loc[nxt.notna(), "Date_next_renewal"]).all()
        # 2. The year's claim count is 0 exactly where its cost is 0 (a part of the target); no negative cost.
        assert (df["N_claims_year"].eq(0) == df["Cost_claims_year"].eq(0)).all()
        assert (df["Cost_claims_year"] >= 0).all()
        # 3. Only years with cover, only complete years (claims stop at the end of 2018) and only each policy's first
        #    row: the later rows hold a shrinking remnant of the first year's claims, not the year's new claims.
        df = df[_covered(df) & (df["k"] == 0) & (df["Date_last_renewal"] < COMPLETE_BEFORE)]
        # 4. Only customers with one policy in force: the claims of a customer's concurrent policies move together.
        df = df[df["Policies_in_force"] == 1].copy()
        # 5. Ages at the start of the year, in completed years.
        start = df["Date_last_renewal"]
        contract = _whole_years(df["Date_start_contract"], start)
        df["contract_years"] = contract.mask(contract < 0)  # a contract dated after the year's start: missing
        df["driver_age"] = _whole_years(df["Date_birth"], start)
        licensed = _whole_years(df["Date_driving_licence"], start)
        df["years_licensed"] = licensed.mask(licensed < 0)  # a licence dated after the year's start: missing
        df["vehicle_age"] = start.dt.year - df["Year_matriculation"]
        # 6. The block without vehicle data: a power of 0 horsepower (and no fuel type).
        df["Power"] = df["Power"].mask(df["Power"] == 0)
        # 7. The codes get their labels (variable sheet).
        for col, labels in LABELS.items():
            assert set(df[col].dropna()) <= set(labels), col
            df[col] = df[col].map(labels)
        # 8. Columns measured at the end of the policy or read late, the claim count, the count of policies (now 1),
        #    the dates turned into ages, the ID.
        df = df.rename(columns={"Date_last_renewal": "period_start"})
        df = drop_columns(
            df,
            [
                "N_claims_year",
                "N_claims_history",
                "R_Claims_history",
                "Lapse",
                "Date_lapse",
                "Max_policies",
                "Max_products",
                "Seniority",
                "Payment",
                "Policies_in_force",
                "Date_start_contract",
                "Date_next_renewal",
                "Date_birth",
                "Date_driving_licence",
                "Year_matriculation",
                "ID",
                "k",
                "n",
                "prev_claims",
            ],
        )
        # 9. The target on the log1p scale (the metric inverts it: target_transform="log1p").
        df[TARGET] = np.log1p(df.pop("Cost_claims_year"))
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=list(LABELS), datetime=["period_start"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        rows = _parse_and_order(raw)
        rows = rows[_covered(rows)]
        complete = rows[rows["Date_last_renewal"] < COMPLETE_BEFORE]
        later = complete[complete["k"] >= 1]
        remnant = pd.crosstab(
            later["prev_claims"].clip(0, 5).astype(int).rename("previous year's claims (5 = 5 or more)"),
            later["N_claims_year"].clip(0, 5).astype(int).rename("this year's claims (5 = 5 or more)"),
        )
        kind = np.where(
            rows["k"] >= 1,
            "later row",
            np.where(
                rows["Date_start_contract"] == rows["Date_last_renewal"],
                "first row, new contract",
                "first row, older contract",
            ),
        )
        quarter = rows["Date_last_renewal"].dt.to_period("Q").astype(str).rename("year starts in")
        share = (
            rows.assign(kind=kind, claim=rows["N_claims_year"] > 0)
            .groupby([quarter, "kind"])["claim"]
            .mean()
            .unstack()
            .round(3)
        )
        share.columns.name = "share with a claim"
        first = complete[complete["k"] == 0]
        cost = first["Cost_claims_year"]
        by_count = (
            first.assign(claim=cost > 0, claimant_cost=cost.where(cost > 0))
            .groupby(first["Policies_in_force"].clip(upper=5).rename("policies in force (5 = 5 or more)"))
            .agg(
                rows=("claim", "size"),
                share_with_a_claim=("claim", "mean"),
                claims_per_row=("N_claims_year", "mean"),
                cost_per_claimant=("claimant_cost", "mean"),
            )
            .round(3)
        )
        return [
            Decision(
                "Only each policy's first year in the release is a task row",
                "Among the later rows of complete years, a year after a claim-free year almost never has a claim, "
                "and a year after one with claims has fewer claims than it in 99.9% of the rows: the later rows "
                "hold a remnant of the first year's claims. Rows: the later rows with a complete year and cover.",
                remnant,
            ),
            Decision(
                "Years that start in 2018 are dropped",
                "Claims stop at the end of 2018, so the claim share falls for years that start in 2018; it also "
                "shows the gap between a policy's first row and its later rows in every quarter. Rows with cover.",
                share,
            ),
            Decision(
                "Only customers with one policy in force are kept",
                "The claims per row grow with the customer's policies in force while the cost per claimant stays "
                "flat: the claims of a customer's concurrent policies move together. Rows: the first rows of "
                "complete years with cover; the task keeps those with one policy.",
                by_count,
            ),
        ]
