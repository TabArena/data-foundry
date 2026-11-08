"""Curated dataset definition for `spanish_motor_insurance_coverage_level_2022_2024` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    ScoringColumn,
    TaskSummary,
    drop_columns,
)

RAW_FILE = "Dataset of motor insurance portfolio.csv"
TARGET = "log1p_incurred_per_exposure_year"
# The claim counts and the incurred cost of each cover: parts of the target (total_incurred is the sum of the covers'
# costs, total_claims the sum of their counts).
CLAIM_PARTS = [
    "total_claims",
    "liability_claims",
    "liability_property_claims",
    "liability_injury_claims",
    "property_claims",
    "theft_claims",
    "fire_claims",
    "glass_claims",
    "legal_protection_claims",
    "occupants_claims",
    "liability_incurred",
    "liability_property_incurred",
    "liability_injury_incurred",
    "property_incurred",
    "theft_incurred",
    "fire_incurred",
    "glass_incurred",
    "legal_protection_incurred",
    "occupants_incurred",
]
COVERS_INCURRED = [
    "liability_incurred",
    "property_incurred",
    "theft_incurred",
    "fire_incurred",
    "glass_incurred",
    "legal_protection_incurred",
    "occupants_incurred",
]
# The coded categories of Tables 1 and 2 of the data article, with their labels.
LABELS = {
    "business_type": {"NB": "new business", "P": "portfolio"},
    "payment_frequency": {"A": "annual", "S": "semiannual", "Q": "quarterly"},
    "bonus_score": {"G": "good", "N": "neutral", "B": "bad"},
    "fuel_type": {"D": "diesel", "G": "gasoline"},
    "municipality_type": {"I": "inland", "C": "coastal", "IS": "islands"},
    "circulation_area": {"U": "urban", "R": "rural"},
}
# The claim-history class is an ordered scale with a word for every level (the variable sheet: a favourable claims
# history, a neutral profile, a poor claims history), lowest first (CLEAN-14). The payment frequency is ordered by the
# number of payments a year, fewest first (1, 2, 4; REVIEW.md issue 8).
ORDINAL = {
    "bonus_score": ["bad", "neutral", "good"],
    "payment_frequency": ["annual", "semiannual", "quarterly"],
}
CATEGORICAL = ["policy_type", *(c for c in LABELS if c not in ORDINAL), "vehicle_brand"]


class SpanishMotorInsuranceCoverageLevel20222024(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a Spanish car insurance policy cost the insurer in claims per year on risk in one calendar "
            "year, from its covers and annual premiums, the driver and the vehicle?"
        ),
        use_case=(
            "A Spanish motor insurer pricing a policy: when a policy is written or renewed, it estimates the claim "
            "cost of the year from the rating factors, to rank the risk and set the premium. The data article names "
            "actuarial pricing as the reuse it supports."
        ),
        row=(
            "One car insurance policy in one calendar year, 2022 to 2024, at an unnamed Spanish insurer (354,091 "
            "policy-years of 185,677 policies, as the year's last record of the policy); 69% are flagged new business."
        ),
        predicted=(
            "The year's claim cost over all seven covers, paid plus reserved, in euros per year on risk (the recorded "
            "time on risk): 0 for 88.1% of the policy-years. Shipped as log1p, scored on the cost per year by a Gini; "
            "each policy-year counts in proportion to its time on risk, in training and scoring."
        ),
        known=(
            "The type of cover and the annual premium of each cover, how the premium is paid, new or renewed "
            "business, the claim-history class, the driver's age and age when licensed, the vehicle (value, seats, "
            "weight per horsepower, brand, fuel), the area and the year. The time on risk is no input: a cancellation "
            "can cut it short, so it is the rate's denominator and each policy-year's weight."
        ),
        split=(
            "Whole policies are held out with all their years, so the test data stands for policies the model has "
            "not seen (52.4% of the policy-years are a policy's first year in the file, while a real next year's book "
            "is mostly renewals); three calendar years cannot give the three yearly test windows a pricing model "
            "refit each year would need."
        ),
        changes=(
            "We divide the year's claim cost by the time on risk, which weights each policy-year and is no input; we "
            "annualise each earned premium, to the cent; we drop the policy's status at year end, the target's parts "
            "(claim counts, per-cover costs) and 49 policy-years with no time on risk, and rename the column the "
            "source calls the vehicle's age: it holds the years since licensing."
        ),
        fit="approximate",
        fit_reason=(
            "Real policy-years with the insurer's rating factors and premiums, but held-out policies of the same "
            "years stand in for next year's book. Kept, with no measured gain: the year's last record (a change after "
            "a claim can show) and an active year's premium blending in the renewal price, which a year cancelled "
            "before its anniversary lacks."
        ),
    )

    # Dataset
    unique_name = "spanish_motor_insurance_coverage_level_2022_2024"
    year = "2026"
    domain = "insurance"
    source = "Other"  # Mendeley Data, the repository of the data article; no closer schema value
    source_url = "https://doi.org/10.17632/sw4jmdb2sm.1"
    license = "CC BY 4.0"
    data_tags = ("ForcedGroupedFromTemporal",)
    download_description = """
        Version 1 of the Mendeley Data record (DOI 10.17632/sw4jmdb2sm.1, published 2026-02-16, CC BY 4.0) holds two
        files: the portfolio (semicolon-separated CSV, 354,140 rows x 47 columns) and the variable descriptions. The
        file links below come from the record's API
        (https://data.mendeley.com/public-api/datasets/sw4jmdb2sm/files?folder_id=root&version=1), which also gives
        the SHA-256 of each file (checked against these links on 2026-11-01, after they had failed for a few minutes);
        "Download All" on https://data.mendeley.com/datasets/sw4jmdb2sm/1 gives the same files.

        mkdir -p local-data-warehouse/spanish_motor_insurance_coverage_level_2022_2024 && cd local-data-warehouse/spanish_motor_insurance_coverage_level_2022_2024
        wget -O "Dataset of motor insurance portfolio.csv" https://data.mendeley.com/public-files/datasets/sw4jmdb2sm/files/3dc64675-b6bd-4e8e-bfba-b64e585c6599/file_downloaded
        wget -O "Descriptive of variables.xlsx" https://data.mendeley.com/public-files/datasets/sw4jmdb2sm/files/b34f32d4-cbe8-4a4e-bd09-9b59796e7fa3/file_downloaded
        sha256sum "Dataset of motor insurance portfolio.csv" "Descriptive of variables.xlsx"
        # 6a47d19d5278a049ea0aeaf39c955cc26068639bdc58cb4523b201e740f0faf4  Dataset of motor insurance portfolio.csv
        # cde44e797a7fd34de29199c78c9301d6f00ed94fd725b4fe8e67e6c2c4cc2e41  Descriptive of variables.xlsx
    """
    bibtex = r"""
        @article{espinosa2026motor,
          title = {A detailed dataset of motor insurance policies with coverage-specific financial information},
          author = {Espinosa, Priscila and Lled{\'o}, Josep and Atance, David},
          journal = {Data in Brief},
          volume = {66},
          pages = {112883},
          year = {2026},
          doi = {10.1016/j.dib.2026.112883},
          note = {Data: Mendeley Data, version 1, doi:10.17632/sw4jmdb2sm.1}
        }
    """
    curation_comments = """
        We start with "Dataset of motor insurance portfolio.csv" of Mendeley Data sw4jmdb2sm, version 1 (Espinosa, Lledó and Atance 2026, Data in Brief 66:112883).

        - Prediction point: when a policy is written or renewed for the year and the insurer prices it. The covers, the premiums, the driver, the vehicle and the claim-history class are known then; the year's claims are not. Data Description: "Each observation corresponds to an insured individual for a given year" (1 January 2022 to 31 December 2024).
        - What the authors did (Experimental Design): of 653,943 raw rows, "only the last available record for each insured and year was retained. After this process, the number of observations was reduced to 354,140", the size of the release, so the later checks removed no row. On negative costs: "In the Spanish insurance market, negative incurred values may occasionally arise due to claim reversals or overprovisioning adjustments during the claims-handling process, a practice that is not standard in all international datasets. To maintain comparability and ensure a consistent actuarial interpretation, observations presenting negative incurred values were therefore excluded from the aggregation of total_incurred." Every incurred column has a minimum of 0, so the target is the sum of the covers' non-negative costs; nothing is set here (the AI's suggested call of 2026-10-30). The raw rows are "available from the authors upon reasonable request".
        - Target `log1p_incurred_per_exposure_year`: the year's claim cost per year on risk, `total_incurred` ("the total cost incurred by the insurer as a result of claims, including both paid amounts and outstanding reserves", the sum of the seven covers' costs on every row) over the time on risk as recorded, on the log1p scale; the metric is computed on the cost per year (`target_transform="log1p"`, MET-3). The curator's call (Andrej, 2026-11-02, REVIEW.md issue 3): "Use exposure-weighted Gini on annualised claim costs for this dataset [...] Ensure predictions and observed costs are compared on the same annualised scale", so the models predict a cost per year and are scored against the observed cost per year. The recorded time on risk ships as the scoring column `actual_exposure`: the annualising base, the metric's weight and the training weight (`sample_weight`, MET-15), never a feature (LEAK-41). 88.1% of the policy-years cost 0, among them 8,543 (2.4%) with a claim recorded at zero cost. Some of these may be negative cover amounts left out of the sum (maybe: a zero cost sits on 35.8% of the third-party property claims, at most 1.5% on the other covers). Short years give large rates (5.5% of the rows have less than 0.1 years on risk; the largest rate is 3.7 million per year, from 571,128 over 0.153 years), but they hold 0.8% of the cost the weighted Gini counts.
        - Why log1p and not the raw amount (MET-3, CLEAN-16; frempl_french_motor_personal_line ships log1p, australian_vehicle_insurance_2004_2005 the raw amount): the benchmark's models fit squared error by default, and on the raw amounts that fit chases the largest claims (the largest is 571,128, 0.8% of all claim cost; the 50 largest hold 75% of the sum of squares). The curator kept the log1p scale with the rate (Lennart, 2026-11-06). A fit weighted by the time on risk on this scale estimates the exposure-weighted mean of log1p(cost per year), not the cost per year: among active policy-years it rises from 0.117 below 0.1 years on risk to 1.074 for a full year while the cost per year stays at 221 to 336, so it ranks well only while the time on risk is no input (given it as a feature, the weighted L2 fit loses 0.035 on the declared metric, 0 of 9 splits). On the shipped features both weighted fits score alike: 0.3166 for L2 on log1p and 0.3165 for Tweedie on the cost per year, the actuarial loss (untuned LightGBM, 9 shipped splits x 3 seeds). Before 2026-11-02, on the year's cost and the row Gini, untuned LightGBM ranked at 0.426 / 0.412 / 0.397 on log1p, 0.353 / 0.365 / 0.363 on the raw amounts and 0.411 / 0.406 / 0.392 with a Tweedie loss (first three shipped splits). The Gini is computed on the cost per year either way.
        - Only the claim part carries much signal (the hurdle check of task_probes.md, same splits): a claim is ranked at ROC AUC 0.70 to 0.71, while a severity model on the claimants reaches R^2 0.023 to 0.025 on log costs and below 0 on the costs, and the true claim indicator times the claimants' mean explains 5% to 9% of the variance of the amount. A hurdle model (claim probability times severity) ranks at a Gini of 0.359 to 0.367, below the direct log1p model.
        - Dropped as parts of the target: the ten claim counts and the incurred cost of each cover (`liability_incurred` and its two parts, `property_incurred`, `theft_incurred`, `fire_incurred`, `glass_incurred`, `legal_protection_incurred`, `occupants_incurred`).
        - `policy_status` dropped: "whether the policy was active (A) or cancelled (C) at calendar year" end (Table 1; "at the time of analysis" in the variable sheet), set after the prediction point (LEAK-10). No cancelled policy-year has a later year in the file, and cancelled policy-years claim more in less time (13.9% with a claim at a mean exposure of 0.53, against 11.7% at 0.73). Added back to the shipped features as a flag it raises the declared metric by 0.019 (weighted Tweedie) and 0.011 (weighted L2 on log1p), 9 of 9 splits (untuned LightGBM, 3 seeds; before 2026-11-02 the row Gini by 0.007 to 0.027).
        - `liability_exposure` dropped: equal to `total_exposure` on every row.
        - 49 policy-years with `total_exposure` 0 dropped: no time on risk and a premium of 0, all cancelled; they are no year a policy is priced for (USE-7). One of them has a claim of 180.11.
        - `vehicle_age` renamed `years_licensed`, `age_driving_licence` renamed `age_at_licence`. Table 2 calls the first the "Age of the insured vehicle" and the second the "Year in which the insured obtained the driving licence" (the text: "the number of years since"), but `driver_age` = `vehicle_age` + `age_driving_licence` (to within a year) on 99.92% of the rows; within a policy the first moves from one year to the next as the driver's age does (+1 for 68% of the policies, 0 for 32%) while the second stays the same for 88%; and the second sits at 18 to 28 for most drivers: the first is the years since licensing and the second the age at licensing. The vehicle's own age is not in the release.
        - `power_to_weight_ratio` renamed `weight_to_power_ratio`: Table 2 calls it the "Weight-to-power ratio of the vehicle (kg per horsepower)", and the values agree (about 2.5 for supercars, 64.8 for microcars).
        - Impossible values made missing (CLEAN-11): an age at licence below 15 (34 rows; Spain's youngest licence, for mopeds, is at 15) with its years licensed, a weight per horsepower of 0 (3 rows; the authors required it "strictly positive"), and a liability premium of 0 (23 rows of policies with other covers: the cover is compulsory, and the premiums were "verified to ensure strictly positive numeric values").
        - The codes of `business_type`, `payment_frequency`, `bonus_score`, `fuel_type`, `municipality_type` and `circulation_area` get the labels of Tables 1 and 2. `bonus_score` is an ordered category, bad < neutral < good (CLEAN-14, as bemtpl97's `coverage`; 2026-11-06): the variable sheet gives a word for every level ("a favourable claims history", "a neutral profile", "a poor claims history"). `payment_frequency` is an ordered category by the number of payments a year, fewest first: annual < semiannual < quarterly (1, 2 or 4), the same order as in pricing_game_2016_french_fleet and pricing_game_2017_french_mtpl (Lennart, 2026-11-08, REVIEW.md issue 8). `policy_type` (TP, TPG, CC, COMP_E, COMP_N), `vehicle_brand` (68 brands) and the other four coded columns are unordered categories. The ages, the year, `seats`, the vehicle value, the weight per horsepower and the eight annual premiums stay numbers; the 513 missing vehicle values and 1,287 missing fuel types stay missing.
        - Exposure (LEAK-41, MET-14, MET-15; REVIEW.md issue 6, resolved 2026-11-06): `total_exposure`, "the time during each calendar year in which the corresponding policy is exposed to risk", is realized: the days in force over 365 (on a 1/365 grid in all three years), shorter when a policy starts during the year or is cancelled. A start is known when the policy is priced, a cancellation is not, and cancelled policy-years claim almost twice as often per exposure-year (0.50 for the located cancellations below and 0.55 for the first-year ones, against 0.30 for full years and 0.27 for late starts). A portfolio policy, and any policy with a row the year before, is in force from 1 January: exposure 1 on 89,817 of 89,882 active portfolio years and on 47,403 of 47,411 active new-business years that follow a row of the same policy (the new-business flag stays on into a policy's second calendar year). So there a time on risk below a year gives the cancellation away (32,626 located cancellations: 18,784 of the 18,849 portfolio years and 13,842 of the 13,850 of those new-business years below a year are cancelled), while in a new-business policy's first year in the file a cut cannot be told from a late start (5,653 cancelled years), since the release has no start date. The task: the recorded time on risk is the cost per year's denominator, the metric's row weight and the training weight (`actual_exposure`, `sample_weight`), never a feature. The corrected copy the models had until 2026-11-06 (a full year for the located cancellations, the cut left on the 5,653) is dropped too: a length corrected on some rows and realized on others is no input (LEAK-41). Measured on the shipped features (untuned LightGBM weighted by the time on risk, Tweedie on the cost per year and L2 on log1p, 9 shipped splits x 3 seeds): the recorded time on risk as a free feature gains 0.0325 under Tweedie (9 of 9; it misleads the L2 fit, -0.035), and 1/time on risk alone scores 0.075, the ceiling of a proxy; the corrected copy gained 0.0176 under Tweedie (9 of 9) and lost 0.0216 under L2. None of that gain is measured on the 5,653 cuts (replacing them by an estimate of the uncut time from the policy number, which follows first appearance, for this check only: -0.0002, SE 0.0006, 3 of 9; -0.0012 net of a control on random active first-year rows): it is the planned time on risk of policies that start during the year, which the release cannot separate from a cut. So a policy that starts during the year has no planned time on risk among its inputs (moved here from `fit_reason` on 2026-11-06): no gap in the fit, since a tariff prices the year insured, a pricing actuary does not rate on the planned length, and the time on risk sits in the weight (USE-8). Revisit if a release gives the start date or the contracted term: the time from the start to 31 December would ship as its own column (LEAK-7).
        - Premiums annualised (LEAK-41): the release's premiums are earned premiums, the annual premium times the time on risk, cancelled years included. The earned total premium follows the time on risk (Spearman 0.83 among active part-years, 0.74 among the first-year cancellations, 0.78 among the located cancellations) and its ratio to it does not (0.034, 0.024, -0.053); the median ratio is 340 to 355 in every band of the time on risk for active policy-years, and flat within each payment frequency too, so a cancelled quarter is not charged in full. Each premium is divided by the recorded time on risk and rounded to the cent: the price of a year on risk. The located cancellations had the division before 2026-11-06; the other policy-years now get it, so no premium carries the time on risk in its level. The rounding (Lennart, 2026-11-08, REVIEW.md issue 7) takes it out of the decimals, found by the re-review of 2026-11-06: the annual tariffs sit on a 5-decimal grid, and the division puts a part-year's premium back on that grid while a full year, a blend of two prices, keeps 11 to 15 decimals. Unrounded, `total_premium` had at most 5 decimals on 39.5% of the located cancellations against 1.0% of the active full years in force from 1 January (on the late starts 0.5% before the division, 44% after); among the policy-years in force from 1 January the eight premiums' decimal counts and cent-grid flags ranked the located cancellations at ROC AUC 0.965 (folds grouped by policy), and the decimal counts as features gained +0.0035 under weighted Tweedie (SE 0.0017, ahead on 8 of 9 splits, 2 seeds) and -0.0052 under weighted L2. LEAK-41 takes out a value whose precision marks the cut whatever it scores. Re-run on the rounded frame (2026-11-08): the same check gives 0.565, no grid from 1 EUR to 1e-5 separates the located cancellations (AUC at most 0.501), and the decimal counts gain +0.0001 under Tweedie (SE 0.0017, 5 of 9) and -0.0012 under L2 (SE 0.0013, 3 of 9); probe 22 finds no feature whose gain goes through the time on risk under either fit. Against the unrounded premiums the score changes by -0.0005 under Tweedie and +0.0005 under L2 (SE 0.0006, 9 splits x 10 seeds). A premium of 0 means the cover is absent.
        - Note: the premiums are kept (USE-6: the insurer's own price, known when the policy is written, which a model refines; TP-4: the core of the task, not a lookup). On the declared metric the annual total premium alone scores 0.2975 (0.277 to 0.316 over the 9 shipped splits); untuned LightGBM on all features scores 0.3166 fit by L2 on log1p (ahead of the premium on 9 of 9 splits) and 0.3165 by Tweedie (8 of 9), both weighted by the time on risk, and the eight premiums add 0.043 to 0.052 to it. Before 2026-11-06, with earned premiums, the corrected time on risk as a feature and no training weight, an untuned L2 fit scored below the premium on each of the first three splits (0.310 / 0.287 / 0.267 against 0.314 / 0.288 / 0.290; REVIEW.md issue 5).
        - Potential leak, kept on purpose: an active calendar year's annual premium blends the price before the anniversary with the renewal price set at it, which can move with the year's claims, while a year cancelled before its anniversary shows one price. The two covers priced at a few flat amounts a year carry it: in 2023 the occupants premium of 51% of the located cancellations equals one of the 20 commonest amounts of that year's first years, against 7.7% of active full years (30% against 0.3% in 2024). So the premiums still mark a located cancellation among the policy-years in force from 1 January: ROC AUC 0.795 from the shipped features, the premiums rounded to the cent (0.81 unrounded, 0.62 without the premiums; first shipped repeat, 2026-11-08), and on the unrounded premiums 0.79 rounded to 3 significant digits, 0.72 in 10% bands, 0.68 with those two covers as presence flags, 0.67 with the year before's premiums in renewal years. It does not pay on the declared metric (LEAK-41's test, both weighted fits, 9 splits x 3 seeds): against the year before's premiums, known on 1 January, this year's premiums gain -0.0006 (Tweedie) and -0.0010 (L2) through the located cancellation and 0.0000 and +0.0009 through the time on risk; the two flat covers' gain over presence flags (0.0097 and 0.0117) goes through neither (-0.0016 and -0.0023 through the located cancellation, -0.0023 and +0.0006 through the time on risk). Through any cancellation, located or not, this year's premiums as shipped, rounded to the cent, gain +0.0013 under Tweedie (SE 0.0008, 5 of 9) and -0.0002 under L2 (SE 0.0011), and unrounded +0.0010 (SE 0.0006, 7 of 9) and +0.0005 (9 splits x 10 seeds; 3 seeds gave +0.0020). Both stay below two SEs, within one run's seed SD (0.007), at 3% to 4% of the free time on risk's gain. The premiums keep their values (Andrej, 2026-11-02: "do not round the premiums"): the cent rounding of the bullet above (Lennart, 2026-11-08) takes out the decimals' mark and keeps every price to the cent, and rounding to 3 significant digits leaves this mark and changes no score. Revisit if records from the actual prediction point become available: the first record of each year, in the raw rows the authors hold, would remove it.
        - Potential leak, kept on purpose: each row is the year's last record of the policy, so an attribute changed during the year can show its state after a claim. Between consecutive years of a policy without a claim in the first, the policy type changes for 2.6% of those with a claim in the second year and 1.7% of those without, the brand for 2.2% and 1.6%, the vehicle value for 3.1% and 2.1%, the bonus class worsens for 0.28% and 0.03%, and the premium per exposure-year moves by +1.4% against +0.4% on average (the median is 0 in both). No consistent score gain detected in the tested comparisons, which is no proof that nothing leaks: setting the attributes of the 11,875 renewal years with a change (type, brand, bonus class, vehicle, payment, area; 6.1% of renewal years without a claim, 8.5% with one) back to the year before's values changes the declared metric by +0.0001 (weighted L2) and -0.0006 (weighted Tweedie, SE 0.0009; the last record ahead on 6 of 9 splits), as in house_sales; before 2026-11-02 the row Gini moved by -0.001 (type, brand or bonus class) and +0.002 (vehicle cells). A renewal year's annual premium is worth 0.012 more than the year before's under both fits, none of it through the cancellation or the time on risk; how much of it is a renewal price reacting to the year's own claims cannot be told without the anniversary date. Kept on the curator's call (Andrej, 2026-11-02). `business_type` is read from the year's last record too: in a policy's second calendar year it turns from new business to portfolio during the year, at a date tied to the start, so a year cancelled early stays new business more often (cancelled second years are new business 3 to 10 points more often within each band of the start, 0.51 against 0.43 overall). Probe 22 (re-run on 2026-11-08, the premiums rounded to the cent) fits the time on risk from the features at R^2 0.340, 42% of that fit's gain from `business_type`, whose gain through the time on risk is +0.0014 under weighted Tweedie (SD 0.0084) and -0.0135 under weighted L2 (SD 0.0071), no gain above noise (1/time on risk alone 0.070 there, 0.075 over the 9 splits). Against its value on 1 January (the year before's last record, on the rows that follow a row of the policy; 76,597 differ), the year's last value gains +0.0002 under Tweedie (SE 0.0004, ahead on 5 of 9 splits) and -0.0014 under L2 (SE 0.0007, 3 of 9), and through any cancellation -0.0002 and -0.0010 (9 splits x 10 seeds, 2026-11-06): no gain, so it stays with this note under the same call (LEAK-10's second clause, LEAK-41's report). Revisit if records from the actual prediction point become available: the first record of each year, which would remove it, is in the raw rows the authors hold.
        - Note: in a new-business policy's first year in the file a cancellation (5,653 years) cuts the time on risk, now only the weight (the proportional part, LEAK-7, MET-14), and the earned premiums, which annualising undoes (Spearman 0.024 with the time on risk). The features still rank such a cancellation at ROC AUC 0.77 without the premiums (0.80 with them), mostly from the payment frequency (14.8% of quarterly payers' first years are cancelled, 2.1% of annual payers') and the year (5.8% in 2022, where a policy's first year in the file can be its second calendar year, against 1.6% and 1.5%), both known when the policy is priced (USE-6). Their gain does not go through the cancellation: leaving out the payment frequency, the year or the vehicle value costs the same with the cancellation flag among the features as without (differences +0.0008, -0.0020 and -0.0003 under weighted Tweedie, within 0.0007 under L2), though the flag itself would add 0.014 (0.010 under L2).
        - Note: 26 policy-years repeat every feature of another policy's row of the same year (a fleet of identical cars, or two policies of one holder, under two ids); kept as distinct policies (LEAK-18).
        - Anomaly: the CICOS agreement settles some claims at "pre-agreed amounts between participating insurers regardless of actual damage" (Limitations): 7,576 of the 42,263 positive costs (17.9%) are exactly 882 (all in 2022), 1,012 (2023) or 1,114 (2024), one flat amount per year, and a few are twice that. Kept as recorded; the year stays a feature.
        - Anomaly: nearly every other claim amount sits on a grid of 0.0115 EUR, a cent times 1.15: all the amounts of bodily injury and of the six other covers and 91.7% of the rest of third-party property damage, against 4% to 22% on a cent grid for most covers; 2023's flat 1,012 is 880 x 1.15 and sits on it too. The amounts may carry a factor of 1.15 from the anonymisation that the flat amounts of 2022 and 2024 did not get (maybe; the article does not say). The Gini ignores a common factor. The ten claim costs below 1 EUR (1 to 46 cents, each with a recorded claim) are recorded amounts on this grid and stay; an eleventh, 6.5e-14, is float residue and changes no score.
        - Note: `insured_id` is the authors' recoded policy number, "constant across the analysed years"; it is the group column, never a feature.
        - CC (2026-11-06, Lennart): REVIEW.md issue 6 resolved by decision D10 of the exposure study of 2026-11-05: `actual_exposure` is the training weight (`sample_weight`, MET-15) as well as the Gini's weight, every premium is annualised and `total_exposure` leaves the features (LEAK-41); the log1p target and the weighted Gini stay. Applied after the weighted re-measure of the same day found no remaining column whose cancellation signal pays on the declared metric (the premium mark, the year's last record, first-year cancellation from the features; the numbers are in the definition's notes and REVIEW.md issue 6). Supersedes Andrej's calls of 2026-11-02: keep the corrected `total_exposure` as the model feature with the 5,653 first-year cuts an approved limitation (REVIEW.md issues 2 and 3), since LEAK-41's partial-correction clause, adopted after that call, takes a length corrected on some rows and realized on others out of the features whatever it scores (the exposure study's +0.0032 for the cuts under weighted Tweedie, 7 of 9 of its own folds, did not hold on the shipped splits: -0.0012 net, SE 0.0006, 3 of 9); keep the premiums as published ("Keep both with explicit potential-leak notes; do not round the premiums", issue 4), since an earned premium carries the cut and annualising removes it (Spearman 0.024 with the time on risk among the first-year cancellations), while the premiums stay unrounded and the year's last record stays with its note; keep the task without a training weight (issue 5), since the training-weight API now exists (`sample_weight`), and with it and the annual premiums both weighted fits beat the premium alone (0.317 against 0.298).
        - CC (2026-11-08, Lennart): the annualised premiums are rounded to the cent (REVIEW.md issue 7, "Round to the cent"): unrounded, their decimals marked a part-year (ROC AUC 0.965 for the located cancellations, 0.565 rounded; the decimal counts as features +0.0035 under weighted Tweedie before, +0.0001 after), and the rounding changes the score by -0.0005 under Tweedie and +0.0005 under L2 (SE 0.0006). This corrects the CC of 2026-11-06 above (D10): every premium is annualised and rounded to the cent, not left unrounded ("while the premiums stay unrounded"), and its "no remaining column whose cancellation signal pays" held for the premiums' values, not for their decimals. It changes the wording of Andrej's call of 2026-11-02 ("do not round the premiums", REVIEW.md issue 4) on a fact found after it, the decimals' mark; the prices he kept stay, to the cent.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.from_context(
        "normalized_weighted_gini",
        reason=(
            "The data article reports no model and no evaluation (Data in Brief 66:112883, read in full on PMC, "
            "PMC13234478), and the Mendeley record defines no task. Pricing actuaries compare tariffs by a Gini of "
            "the loss cost per exposure: CAS Monograph 5 (Goldburd, Khare and Tevet, Sec. 7.2.4) sorts the policies "
            "by predicted loss cost per exposure and accumulates exposure on the x-axis, while Frees, Meyers and "
            "Cummings (2011, JASA 106:1085-1098) order by the relativity to the premium and accumulate premium. The "
            "weighted Gini is that CAS form, normalised by the Gini of the perfect order as in Liberty Mutual's Kaggle "
            "competition of 2014, whose weight `var11` was a size of the risk; here the weight is the time on risk, "
            'chosen by the curator for this table (Andrej, 2026-11-02: "Use exposure-weighted Gini on annualised '
            'claim costs"): 49% of the rows are part-years, and the row Gini on the cost of the year rewarded reading '
            "the time on risk, which alone scored 0.177 to 0.221 against 0.393 to 0.445 for untuned LightGBM; "
            "weighted, the corrected time on risk (a feature until 2026-11-06) scored -0.035 to 0.010. Here "
            "policy-years are sorted by the predicted cost per year and the observed cost per year is weighted by the "
            "recorded time on risk (`actual_exposure`, a scoring column), so a policy-year counts with its time on "
            "risk, and every model trains with that weight (`sample_weight`, MET-15). On the 9 shipped splits 1/time "
            "on risk alone, the ceiling of a proxy of the weight, scores 0.075, the annual total premium alone 0.298 "
            "and untuned LightGBM 0.317 (both weighted fits). RMSE on the amount follows a few large claims (the 50 "
            "largest of 354,091 policy-years hold 75% of the year costs' sum of squares). The Gini sees neither the "
            "level nor the spread of the predicted costs; pricing sets the level separately."
        ),
        inputs={"weight": "actual_exposure"},
        target_transform="log1p",
    )
    sample_weight = "actual_exposure"
    scoring_columns = (
        ScoringColumn(
            column="actual_exposure",
            role="weight",
            used_by="normalized_weighted_gini",
            description=(
                "the policy-year's time on risk as recorded (`total_exposure` of the release: days in force over 365, "
                "in years), realized: shorter when the policy starts or is cancelled during the year. The cost per "
                "year's denominator; each row's weight in the metric and in training (`sample_weight`); never a "
                "feature, since for a cancelled year it gives the cancellation away (LEAK-41)"
            ),
        ),
    )
    accepted_check_warnings = {
        "task_target_value_dominant": (
            "88.1% zeros: policy-years without a claim cost (Andrej, 2026-11-03: zero-inflated targets are natural for these tasks and a core challenge)."
        ),
    }
    grouping = Grouping(
        on="insured_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a policy: `insured_id`, the authors' recoded policy number, "constant across the analysed years" (Data Description), with one row for each calendar year it was in force (67,751 policies with one year, 67,438 with two, 50,488 with three). The use case prices a policy for the year. 52.4% of the policy-years are a policy's first year in the file; the new-business flag (69% of the rows) stays on into a policy's second calendar year, and 62.7% of the 2024 rows had a row the year before. A tariff is fit on past years and applied to the next, but three calendar years give one valid temporal window (2024, trained on 2022-2023) where SPLIT-14 asks for three, so the policy-years are split by policy instead (SPLIT-8, ForcedGroupedFromTemporal): a test policy is one the model has seen in no year. Each policy-year is one prediction, made from its own row. A holder with several policies (several cars) has several ids, which the release cannot join.
        """,
    )
    splits_comment = """
        Grouped 3-fold splits by policy (`insured_id`), forced from temporal (SPLIT-8): every year of a policy stays on
        one side. A pricing model is refit each year and applied to the next year's policies, but the release holds
        three calendar years and no finer date, so a split by year gives one window that keeps half the rows for
        training (2024, 47.5% of the rows, against 2022-2023), where SPLIT-14 asks for three. What a dated window
        would change: a renewal would be a known policy whose last-year claims are a feature (+0.001 to +0.007 on
        renewal rows, first three splits; row Gini, before 2026-11-02), and the score would be the 2024 window's.
        Measured on the shipped definition (2026-11-06; untuned LightGBM weighted by the time on risk, fit by L2 on
        log1p and by Tweedie on the cost per year): the 2024 window scores 0.300 to 0.307 (L2) and 0.305 to 0.316
        (Tweedie) over 3 seeds, bootstrap SE 0.011 to 0.012, against 0.274 to 0.333 and 0.292 to 0.332 (means 0.309
        and 0.311) on the 2024 rows of the 9 splits' folds, so the forced split is no more optimistic for the newest
        year than the valid window. The pooled score (0.28 to 0.34 over the 9 splits) mixes years: within the same
        folds 2023 rows rank more easily than 2024 rows (0.326 against 0.309 under L2) and 2022 rows a little
        (0.317), which comes from the years, not from shared policies. Random policy-years score about the same as
        the grouped folds (0.318 against 0.315 under L2, 0.314 against 0.317 under Tweedie), so the grouping follows
        the use case, not a measured gap (SPLIT-4). This is not the forced IID split rejected for
        how_much_did_it_rain: whole policies are held out, so no test row shares a policy's outcomes with training,
        and the cost of the window is measured. The leak test across the split, in the form used for
        wisconsin_local_government_property_insurance_fund (each test year scored by a model trained without that
        year's training rows, against one trained without as many random rows; 9 splits), finds a small shared
        period: the test year's own training rows add +0.010 under L2 (SE 0.002, 9 of 9) and +0.0045 under Tweedie
        (SE 0.003, 6 of 9) pooled, at most +0.029 in one year (2022 under L2, SE 0.010, 7 of 9), and +0.006 and
        +0.008 with the year out of the features. It sits within each year (the cost per exposure-year is flat at 285
        to 302 a year): the year's own mapping from prices and factors to cost, not a year's claim level as there
        (+0.113). No column carries it; at most 3% of the score and within the window's SE, it is the forced split's
        optimism over a model that cannot see its year. Before 2026-11-02 (row Gini, first three splits): 30 exact
        feature copies across the split shared no outcome (the leak probe of 2026-11-06 finds copies for 0.0% of the
        test rows), the outcomes of training rows with the same car and driver under another id added +0.0011 (a
        shifted-key control +0.0010), and the training side's mean outcome of the row's year added 0.0000 and of year
        x area +0.0009; no feature is built from another row's outcome. The year stays a feature (the flat claim
        amount of the CICOS agreement changes each year). A release with more
        years or dates should get a temporal split. Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine").
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # round_trip: pandas 2's default parser reads some of the 15-digit decimals a few units off in the last
        # place; the exact parse (pandas 3's default) keeps the frame and its checksum the same under both
        return pd.read_csv(raw_dir / RAW_FILE, sep=";", float_precision="round_trip")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. The target is the sum of the covers' costs; the claim counts and the covers' costs are its parts.
        assert np.allclose(df["total_incurred"], df[COVERS_INCURRED].sum(axis=1), atol=0.01)
        # 2. The liability exposure is a copy of the total exposure.
        assert df["liability_exposure"].equals(df["total_exposure"])
        # 3. Policy-years with no time on risk are no year a policy is priced for.
        df = df[df["total_exposure"] > 0].copy()
        # 4. The time on risk as recorded, in years: the denominator of the cost per year, the metric's row weight and
        #    the training weight. A cancellation cuts it short, so it is a scoring column, never a feature (LEAK-41).
        df = df.rename(columns={"total_exposure": "actual_exposure"})
        # 5. The premiums are earned pro rata, the annual premium times the time on risk (cancelled years included),
        #    so each is annualised: divided by the time on risk, which takes the time on risk out of its level
        #    (LEAK-41). Then rounded to the cent: a part-year's quotient falls back on the tariff's 5-decimal grid
        #    while a full year keeps 11 to 15 decimals, so the unrounded decimals mark the cut (REVIEW.md issue 7).
        premiums = [c for c in df.columns if c.endswith("_premium")]
        df[premiums] = df[premiums].div(df["actual_exposure"], axis=0).round(2)
        df = drop_columns(df, [*CLAIM_PARTS, "policy_status", "liability_exposure"])
        # 6. The source's `vehicle_age` is the years since licensing and `age_driving_licence` the age at licensing;
        #    `power_to_weight_ratio` holds kilograms per horsepower (Table 2: "Weight-to-power ratio").
        df = df.rename(
            columns={
                "vehicle_age": "years_licensed",
                "age_driving_licence": "age_at_licence",
                "power_to_weight_ratio": "weight_to_power_ratio",
            }
        )
        gap = df["driver_age"] - df["years_licensed"] - df["age_at_licence"]
        assert gap.isin([0, 1]).mean() > 0.999
        # 7. Impossible values: a licence before 15 (with its years licensed), a weight per horsepower of 0 and a
        #    premium of 0 for the compulsory liability cover.
        early = df["age_at_licence"] < 15
        df[["age_at_licence", "years_licensed"]] = df[["age_at_licence", "years_licensed"]].mask(early)
        df["weight_to_power_ratio"] = df["weight_to_power_ratio"].mask(df["weight_to_power_ratio"] == 0)
        df["liability_premium"] = df["liability_premium"].mask(df["liability_premium"] == 0)
        # 8. The codes get their labels (Tables 1 and 2).
        for col, labels in LABELS.items():
            assert set(df[col].dropna()) <= set(labels), col
            df[col] = df[col].map(labels)
        # 9. The target: the year's cost per year on risk, over the recorded time on risk, on the log1p scale (the
        #    metric inverts it: target_transform="log1p"); the cost per year times the time on risk gives back the cost.
        cost = df.pop("total_incurred")
        df[TARGET] = np.log1p(cost / df["actual_exposure"])
        assert np.allclose(np.expm1(df[TARGET]) * df["actual_exposure"], cost, rtol=1e-9, atol=1e-6)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=CATEGORICAL, ordinal=ORDINAL)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        r = raw[raw["total_exposure"] > 0].sort_values(["insured_id", "year"], kind="stable")
        has_later = r.groupby("insured_id")["year"].shift(-1).notna()
        status = (
            r.assign(has_later_year=has_later, claim=r["total_incurred"] > 0)
            .groupby("policy_status")
            .agg(
                policy_years=("year", "size"),
                share_with_a_later_year=("has_later_year", "mean"),
                share_with_a_claim=("claim", "mean"),
                mean_exposure=("total_exposure", "mean"),
            )
            .round(3)
            .rename(index={"A": "active (A)", "C": "cancelled (C)"})
        )
        gap = raw["driver_age"] - raw["vehicle_age"] - raw["age_driving_licence"]
        identity = gap.isin([0, 1]).mean()
        steps = (
            r.groupby("insured_id")[["vehicle_age", "age_driving_licence", "driver_age"]]
            .diff()
            .dropna()
            .clip(-1, 2)
            .apply(lambda s: s.value_counts(normalize=True))
            .fillna(0)
            .round(3)
            .rename(index={-1: "-1 or less", 2: "2 or more"})
            .rename_axis("change from one year to the next (share of policies)")
        )
        cancelled = r["policy_status"].eq("C").map({True: "cancelled", False: "active"})
        first = r.groupby("insured_id")["year"].transform("min").eq(r["year"]).map({True: "first", False: "later"})
        by_status = r.groupby([r["business_type"].map(LABELS["business_type"]), first, cancelled])
        exposure = by_status.agg(
            policy_years=("year", "size"),
            share_below_a_year=("total_exposure", lambda e: (e < 0.9999).mean()),  # float noise at 1 is a year
            exposure=("total_exposure", "sum"),
            claims=("total_claims", "sum"),
        )
        exposure["claims_per_exposure_year"] = exposure.pop("claims") / exposure.pop("exposure")
        exposure = exposure.round(3).rename_axis(["business type", "policy's year in the file", "status at year end"])
        kind = np.select(
            [r["policy_status"].ne("C"), r["business_type"].eq("P") | first.eq("later")],
            ["active", "cancelled, in force from 1 January"],
            "cancelled in a new-business first year",
        )
        bands = [0, 0.1, 0.25, 0.5, 0.75, 0.9999, 1.0001]  # float noise at 1 is a year
        names = ["below 0.1", "0.1 to 0.25", "0.25 to 0.5", "0.5 to 0.75", "0.75 to 1", "a full year"]
        annual = (
            r.assign(
                kind=kind,
                band=pd.cut(r["total_exposure"], bands, labels=names),
                annual=r["total_premium"] / r["total_exposure"],
            )
            .groupby(["kind", "band"], observed=True)
            .agg(
                policy_years=("year", "size"),
                median_earned_total_premium=("total_premium", "median"),
                median_annual_total_premium=("annual", "median"),
            )
            .round(1)
            .rename_axis(["status at year end", "time on risk (years)"])
        )
        return [
            Decision(
                "The policy's status at year end is dropped",
                "`policy_status` is set when the year ends: no cancelled policy-year has a later year, and cancelled "
                "policy-years claim more in less time.",
                status,
            ),
            Decision(
                "`vehicle_age` holds the years since licensing",
                f"The driver's age is the sum of `vehicle_age` and `age_driving_licence` (to within a year) on "
                f"{identity:.2%} of the rows; within a policy the first moves from one year to the next as the "
                "driver's age does, while the second mostly stays the same, so the first is renamed `years_licensed` "
                "and the second `age_at_licence`.",
                steps,
            ),
            Decision(
                "The time on risk is the weight, never a feature",
                "A portfolio policy, and any policy in a later year in the file, is in force from 1 January, so its "
                "time on risk falls below a year only when it is cancelled, and cancelled years claim almost twice as "
                "often per exposure-year; in a new-business policy's first year in the file a cut cannot be told from "
                "a late start. So the recorded time on risk is the cost per year's denominator and each policy-year's "
                "weight in the metric and in training, and no column carries it as a feature (LEAK-41, curation "
                "notes).",
                exposure,
            ),
            Decision(
                "Every earned premium is annualised, to the cent",
                "The premiums are earned pro rata: the earned total premium follows the time on risk, while the "
                "premium per year on risk (the earned premium over the time on risk) stays level across its bands, "
                "for active and cancelled policy-years alike. Each premium is divided by the time on risk, so no "
                "premium carries it in its level (LEAK-41), and rounded to the cent, so none carries it in its "
                "decimals: unrounded, a part-year's annual premium falls back on the tariff's 5-decimal grid while a "
                "full year keeps 11 to 15 decimals, and the decimals ranked the located cancellations at ROC AUC "
                "0.965; rounded, 0.565 (REVIEW.md issue 7).",
                annual,
            ),
        ]
