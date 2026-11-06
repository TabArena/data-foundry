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
CATEGORICAL = ["policy_type", *LABELS, "vehicle_brand"]


class SpanishMotorInsuranceCoverageLevel20222024(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a Spanish car insurance policy cost the insurer in claims per year on risk in one calendar year, "
            "from its covers and premiums, the driver, the vehicle and its time on risk that year?"
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
            "time on risk): 0 for 88.1% of the policy-years. Shipped as log1p, scored on the cost per year by a Gini "
            "weighted by the time on risk."
        ),
        known=(
            "The type of cover and the premium of each cover, how the premium is paid, new or renewed business, the "
            "claim-history class, the driver's age and age when licensed, the vehicle (value, seats, weight per "
            "horsepower, brand, fuel), the area, the year and the share of the year the policy is in force (a full "
            "year for a policy carried over from the year before)."
        ),
        split=(
            "Whole policies are held out with all their years, so the test data stands for policies the model has "
            "not seen (52.4% of the policy-years are a policy's first year in the file, while a real next year's book "
            "is mostly renewals); three calendar years cannot give the three yearly test windows a pricing model "
            "refit each year would need."
        ),
        changes=(
            "We dropped the policy's status at year end and the claim counts and per-cover costs (parts of the "
            "target), dropped 49 policy-years with no time on risk, gave the cancelled years of policies in force "
            "from 1 January their full year and annual premiums, and renamed the column the source calls the "
            "vehicle's age: it holds the years since the driver was licensed."
        ),
        fit="approximate",
        fit_reason=(
            "Real policy-years with an insurer's rating factors and premiums, but held-out policies of the same years "
            "stand in for next year's book. Kept potential leaks: each row is the year's last record (a change after "
            "a claim can show), a cancellation in a new policy's first year cuts its time on risk and premiums, and a "
            "cancelled year's annualised premiums lack the renewal price an active year's blend in."
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
        - Target `log1p_incurred_per_exposure_year`: the year's claim cost per year on risk, `total_incurred` ("the total cost incurred by the insurer as a result of claims, including both paid amounts and outstanding reserves", the sum of the seven covers' costs on every row) over the time on risk as recorded, on the log1p scale; the metric is computed on the cost per year (`target_transform="log1p"`, MET-3). The curator's call (Andrej, 2026-11-02, REVIEW.md issue 3): "Use exposure-weighted Gini on annualised claim costs for this dataset [...] Ensure predictions and observed costs are compared on the same annualised scale", so the models predict a cost per year and are scored against the observed cost per year. The recorded time on risk ships as the scoring column `actual_exposure` (the annualising base and the metric's weight), never a feature. 88.1% of the policy-years cost 0, among them 8,543 (2.4%) with a claim recorded at zero cost. Some of these may be negative cover amounts left out of the sum (maybe: a zero cost sits on 35.8% of the third-party property claims, at most 1.5% on the other covers). Short years give large rates (5.5% of the rows have less than 0.1 years on risk; the largest rate is 3.7 million per year, from 571,128 over 0.153 years), but they hold 0.8% of the cost the weighted Gini counts.
        - Why log1p and not the raw amount (MET-3; frempl_french_motor_personal_line ships log1p, australian_vehicle_insurance_2004_2005 the raw amount): the benchmark's models fit squared error by default, and on the raw amounts that fit chases the largest claims (the largest is 571,128, 0.8% of all claim cost; the 50 largest hold 75% of the sum of squares). Untuned LightGBM ranks policies at a Gini of 0.426 / 0.412 / 0.397 on log1p, 0.353 / 0.365 / 0.363 on the raw amounts, and 0.411 / 0.406 / 0.392 with a Tweedie loss on the amounts, the actuarial loss (first three shipped splits). The Gini is computed on the amount either way.
        - Only the claim part carries much signal (the hurdle check of task_probes.md, same splits): a claim is ranked at ROC AUC 0.70 to 0.71, while a severity model on the claimants reaches R^2 0.023 to 0.025 on log costs and below 0 on the costs, and the true claim indicator times the claimants' mean explains 5% to 9% of the variance of the amount. A hurdle model (claim probability times severity) ranks at a Gini of 0.359 to 0.367, below the direct log1p model.
        - Dropped as parts of the target: the ten claim counts and the incurred cost of each cover (`liability_incurred` and its two parts, `property_incurred`, `theft_incurred`, `fire_incurred`, `glass_incurred`, `legal_protection_incurred`, `occupants_incurred`).
        - `policy_status` dropped: "whether the policy was active (A) or cancelled (C) at calendar year" end (Table 1; "at the time of analysis" in the variable sheet), set after the prediction point (LEAK-10). No cancelled policy-year has a later year in the file, and cancelled policy-years claim more in less time (13.9% with a claim at a mean exposure of 0.53, against 11.7% at 0.73). Added back to the shipped features it raises the Gini of untuned LightGBM by 0.007 to 0.027 (first three shipped splits).
        - `liability_exposure` dropped: equal to `total_exposure` on every row.
        - 49 policy-years with `total_exposure` 0 dropped: no time on risk and a premium of 0, all cancelled; they are no year a policy is priced for (USE-7). One of them has a claim of 180.11.
        - `vehicle_age` renamed `years_licensed`, `age_driving_licence` renamed `age_at_licence`. Table 2 calls the first the "Age of the insured vehicle" and the second the "Year in which the insured obtained the driving licence" (the text: "the number of years since"), but `driver_age` = `vehicle_age` + `age_driving_licence` (to within a year) on 99.92% of the rows; within a policy the first moves from one year to the next as the driver's age does (+1 for 68% of the policies, 0 for 32%) while the second stays the same for 88%; and the second sits at 18 to 28 for most drivers: the first is the years since licensing and the second the age at licensing. The vehicle's own age is not in the release.
        - `power_to_weight_ratio` renamed `weight_to_power_ratio`: Table 2 calls it the "Weight-to-power ratio of the vehicle (kg per horsepower)", and the values agree (about 2.5 for supercars, 64.8 for microcars).
        - Impossible values made missing (CLEAN-11): an age at licence below 15 (34 rows; Spain's youngest licence, for mopeds, is at 15) with its years licensed, a weight per horsepower of 0 (3 rows; the authors required it "strictly positive"), and a liability premium of 0 (23 rows of policies with other covers: the cover is compulsory, and the premiums were "verified to ensure strictly positive numeric values").
        - The codes of `business_type`, `payment_frequency`, `bonus_score`, `fuel_type`, `municipality_type` and `circulation_area` get the labels of Tables 1 and 2; all of them, `policy_type` (TP, TPG, CC, COMP_E, COMP_N) and `vehicle_brand` (68 brands) are categorical. The ages, the year, `seats`, the vehicle value, the weight per horsepower, the eight premiums and `total_exposure` stay numbers; the 513 missing vehicle values and 1,287 missing fuel types stay missing.
        - Note: `total_exposure`, as corrected below ("the time during each calendar year in which the corresponding policy is exposed to risk") is a feature, as in the curator's call for fremtpl2 and the AI's suggested call of 2026-10-30: the period is known when a policy is priced (a GLM offset), and a model given it can learn what an offset imposes. But a time on risk cut short by a cancellation is known only when the policy ends, and cancelled policy-years claim almost twice as often per exposure-year (0.50 claims against 0.28 to 0.31). The models get the corrected time on risk, not the recorded one (`actual_exposure`, the scoring column), on the curator's call: "Keep corrected total_exposure as the model feature; do not also expose original exposure to the model."
        - Cancelled years of policies in force from 1 January get a full year on risk (LEAK-10, LEAK-7). A portfolio policy, and any policy with a row the year before, is in force from 1 January: exposure 1 on 89,817 of 89,882 active portfolio years and on 47,403 of 47,411 active new-business years that follow a row of the same policy (the new-business flag stays on into a policy's second calendar year). So a time on risk below a year gives its cancellation away: 18,784 of the 18,849 portfolio years and 13,842 of the 13,850 of those new-business years below a year are cancelled. For these 32,626 years the exposure is set to 1 and each earned premium to the annual premium (premium / exposure). Measured before 2026-11-02 on the year's cost and the row Gini: kept as published, the portfolio cut raises the Gini of untuned LightGBM by 0.0085 (SE 0.0018, higher on 9 of 9 shipped splits), since the flag tells a cut from a late start; the new-business cut lowers it (0.408 against 0.412, 9 splits; 0.323 against 0.352 on the 61,253 new-business years that follow a row of the same policy, lower on 7 of 9), since it looks like a late start.
        - Potential leak, kept on purpose: in a new-business policy's first year in the file a cancellation cuts the exposure and the earned premiums too (5,653 years), but a cut cannot be told from a late start, since the release has no start date. The curator kept the cancellation corrections and this limitation when the metric changed (Andrej, 2026-11-02: "Retain the existing cancellation corrections and the approved limitation for the 5,653 ambiguous first-year cancellations"). Cancellation there is ranked at ROC AUC 0.86 from the features (0.77 without the exposure and premiums). Measured on the year's cost and the row Gini before 2026-11-02: where a cut is traced but looks like a late start (the carried-over new-business years above) it lowered the Gini, and replacing the 5,653 cuts by an estimate of the uncut time (from the policy number, which follows first appearance; for this check only) raises the Gini by 0.0065 (SE 0.0011, 9 of 9 splits; 0.0067 net of a control on random active first-year rows): no consistent score gain detected on the cut in the tested comparisons. Removing it everywhere (exposure dropped, premiums annualised) scores 0.362 / 0.338 / 0.345 against 0.426 / 0.412 / 0.397 (first three splits) and takes the time on risk from about 168,000 policies that started after 1 January. Kept as published; LEAK-10 leaves such a keep to the curator's case-by-case call, and the curator kept it (Andrej, 2026-11-02), recorded as the LEAK-10 case for time on risk cut short by the outcome: the located cut removed, the unlocated one kept with its measured size. Revisit if a release gives the start date or the contracted term.
        - Note: the premiums are kept (USE-6: the insurer's own price, known when the policy is written, which a model refines). They are earned premiums, the annual premium times the exposure (the median premium per exposure-year is about 350 in every exposure band), and a premium of 0 means the cover is absent. On the declared metric the total premium per year on risk alone scores 0.314 / 0.288 / 0.290 (first three shipped splits; 0.277 to 0.316 over the 9), and untuned LightGBM on the log1p target 0.310 / 0.287 / 0.267 (3 seeds), below the premium on each; LightGBM with a Tweedie loss fit with the time on risk as sample weight scores 0.292 to 0.341 (mean 0.320 against the premium's 0.298, 9 splits). Under the earlier row Gini on the year's cost, LightGBM beat the premium on each of the first three splits (0.426 / 0.412 / 0.397 against 0.397 / 0.388 / 0.368). The insurer's price is the core of the task, not a lookup (TP-4); how a model uses the time on risk decides whether it beats it (REVIEW.md issue 5).
        - Potential leak, kept on purpose: the annualised premiums of a cancelled year still differ from an active year's. An active calendar year blends the price before the anniversary with the renewal price set at it, which can move with the year's claims; a year cancelled before its anniversary shows one price. Among the full-year rows, cancellation is ranked from the premiums and the corrected time on risk at ROC AUC 0.79 (on the earlier frame, from all shipped features 0.774 to 0.778, 0.62 without the premiums, 0.685 with the premiums rounded to whole euros). No consistent score gain detected in the tested comparisons: on the declared metric, giving the located cancellation status to the model outright changes the Gini by -0.004 / -0.006 / -0.012 (untuned LightGBM, 3 seeds, first three splits), and rounding the premiums lowered the earlier Gini by 0.002 (SE 0.001, 9 splits). Neither is a bound on what the trace is worth: rounding also removes legitimate price information and leaves cancellation readable. The premiums stay as published, unrounded (Andrej, 2026-11-02: "Keep both with explicit potential-leak notes; do not round the premiums"). Revisit if records from the actual prediction point become available: the first record of each year, in the raw rows the authors hold, would remove it.
        - Potential leak, kept on purpose: each row is the year's last record of the policy, so an attribute changed during the year can show its state after a claim. Between consecutive years of a policy without a claim in the first, the policy type changes for 2.6% of those with a claim in the second year and 1.7% of those without, the brand for 2.2% and 1.6%, the vehicle value for 3.1% and 2.1%, the bonus class worsens for 0.28% and 0.03%, and the premium per exposure-year moves by +1.4% against +0.4% on average (the median is 0 in both). No consistent score gain detected in the tested comparisons (on the year's cost and the row Gini, before 2026-11-02), which is no proof that nothing leaks: giving the 8,115 renewal years whose type, brand or bonus class changed last year's values scores 0.429 / 0.412 / 0.392 against 0.426 / 0.412 / 0.397 as shipped (0.411 against 0.412 on average, within fold noise), and reverting the 12,855 changed vehicle cells 0.414 against 0.412 on average (untuned LightGBM, first three splits), as in house_sales. Kept on the curator's call (Andrej, 2026-11-02). Revisit if records from the actual prediction point become available: the first record of each year, which would remove it, is in the raw rows the authors hold.
        - Note: 26 policy-years repeat every feature of another policy's row of the same year (a fleet of identical cars, or two policies of one holder, under two ids); kept as distinct policies (LEAK-18).
        - Anomaly: the CICOS agreement settles some claims at "pre-agreed amounts between participating insurers regardless of actual damage" (Limitations): 7,576 of the 42,263 positive costs (17.9%) are exactly 882 (all in 2022), 1,012 (2023) or 1,114 (2024), one flat amount per year, and a few are twice that. Kept as recorded; the year stays a feature.
        - Anomaly: nearly every other claim amount sits on a grid of 0.0115 EUR, a cent times 1.15: all the amounts of bodily injury and of the six other covers and 91.7% of the rest of third-party property damage, against 4% to 22% on a cent grid for most covers; 2023's flat 1,012 is 880 x 1.15 and sits on it too. The amounts may carry a factor of 1.15 from the anonymisation that the flat amounts of 2022 and 2024 did not get (maybe; the article does not say). The Gini ignores a common factor. The ten claim costs below 1 EUR (1 to 46 cents, each with a recorded claim) are recorded amounts on this grid and stay; an eleventh, 6.5e-14, is float residue and changes no score.
        - Note: `insured_id` is the authors' recoded policy number, "constant across the analysed years"; it is the group column, never a feature.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.from_context(
        "normalized_weighted_gini",
        reason=(
            "The data article reports no model and no evaluation (Data in Brief 66:112883, read in full on PMC, "
            "PMC13234478), and the Mendeley record defines no task. In insurance pricing, models are compared by the "
            "Gini index of an ordered Lorenz curve of losses, and an actuary weighs each policy by its time on risk "
            "and orders by the cost per year (Frees, Meyers and Cummings 2011, JASA 106:1085-1098; Liberty Mutual's "
            "Kaggle competition of 2014 scored this weighted Gini, its weight `var11`). Chosen by the curator for this "
            'table (Andrej, 2026-11-02: "Use exposure-weighted Gini on annualised claim costs"): 49% of the rows are '
            "part-years, and the row Gini on the year's cost rewarded reading the time on risk, which alone scored "
            "0.177 to 0.221 against 0.393 to 0.445 for untuned LightGBM; weighted, it scores -0.035 to 0.010. Here "
            "policy-years are sorted by the predicted cost per year and the observed cost per year is weighted by "
            "the recorded time on risk (`actual_exposure`, a scoring column), so a policy-year counts with its time "
            "on risk. RMSE on the amount follows a few large claims (the 50 largest of 354,091 policy-years hold 75% "
            "of the year costs' sum of squares). The Gini sees neither the level nor the spread of the predicted "
            "costs; pricing sets the level separately."
        ),
        inputs={"weight": "actual_exposure"},
        target_transform="log1p",
    )
    scoring_columns = (
        ScoringColumn(
            column="actual_exposure",
            role="weight",
            used_by="normalized_weighted_gini",
            description=(
                "the policy-year's time on risk as recorded (`total_exposure` of the release, in years): the target "
                "is the cost over it, and the Gini weighs each policy-year by it. Never a feature: for cancelled "
                "years it gives the cancellation away, so the models get the corrected `total_exposure` instead."
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
        would change: a renewal would be a known policy whose last-year claims are a feature (+0.001 to +0.007 Gini
        on renewal rows, first three splits), and the score would be the 2024 window's. On that window untuned
        LightGBM reaches a normalized Gini of 0.385 (bootstrap SE 0.021), against 0.375 to 0.405 on the 2024 rows of
        the first three folds, so the forced split is no more optimistic for the newest year than the valid window.
        The pooled score (0.393 to 0.445 over the 9 splits) mixes years: within the same folds 2022 and 2023 rows
        rank more easily than 2024 rows, which comes from the years, not from shared policies. Random policy-years
        score about the same as the grouped folds (Gini 0.415 against 0.412, mean of 3 folds), so the grouping
        follows the use case, not a measured gap (SPLIT-4). This is not the forced IID split rejected for
        how_much_did_it_rain: whole policies are held out, so no test row shares a policy's outcomes with training,
        and the cost of the window is measured. A leak test across the split finds none (first three splits): 30
        exact feature copies across it share no outcome, the outcomes of training rows with the same car and driver
        under another id add +0.0011 Gini (a shifted-key control +0.0010), the training side's mean outcome of the
        row's year adds 0.0000 and of year x area +0.0009, and no feature is built from another row's outcome. The
        year stays a feature (the flat claim amount of the CICOS agreement changes each year). A release with more
        years or dates should get a temporal split. Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine").
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE, sep=";")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. The target is the sum of the covers' costs; the claim counts and the covers' costs are its parts.
        assert np.allclose(df["total_incurred"], df[COVERS_INCURRED].sum(axis=1), atol=0.01)
        # 2. The liability exposure is a copy of the total exposure.
        assert df["liability_exposure"].equals(df["total_exposure"])
        # 3. Policy-years with no time on risk are no year a policy is priced for.
        df = df[df["total_exposure"] > 0].copy()
        # The time on risk as recorded, before step 4: the base of the cost per year on risk and the metric's weight
        # (a scoring column, never a feature).
        df["actual_exposure"] = df["total_exposure"]
        # 4. A portfolio policy, and any policy with a row the year before (the new-business flag stays on into a
        #    policy's second calendar year), is in force from 1 January (exposure 1 on 99.9% of the active ones), so a
        #    time on risk below a year gives its cancellation away. For the cancelled ones the exposure is set to a
        #    full year and each earned premium to the annual premium.
        carried = df.groupby("insured_id")["year"].transform("min") < df["year"]
        late = df["policy_status"].eq("C") & (df["business_type"].eq("P") | carried)
        premiums = [c for c in df.columns if c.endswith("_premium")]
        df.loc[late, premiums] = df.loc[late, premiums].div(df.loc[late, "total_exposure"], axis=0)
        df.loc[late, "total_exposure"] = 1.0
        df = drop_columns(df, [*CLAIM_PARTS, "policy_status", "liability_exposure"])
        # 5. The source's `vehicle_age` is the years since licensing and `age_driving_licence` the age at licensing;
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
        # 6. Impossible values: a licence before 15 (with its years licensed), a weight per horsepower of 0 and a
        #    premium of 0 for the compulsory liability cover.
        early = df["age_at_licence"] < 15
        df[["age_at_licence", "years_licensed"]] = df[["age_at_licence", "years_licensed"]].mask(early)
        df["weight_to_power_ratio"] = df["weight_to_power_ratio"].mask(df["weight_to_power_ratio"] == 0)
        df["liability_premium"] = df["liability_premium"].mask(df["liability_premium"] == 0)
        # 7. The codes get their labels (Tables 1 and 2).
        for col, labels in LABELS.items():
            assert set(df[col].dropna()) <= set(labels), col
            df[col] = df[col].map(labels)
        # 8. The target: the year's cost per year on risk, over the recorded time on risk, on the log1p scale (the
        #    metric inverts it: target_transform="log1p").
        df[TARGET] = np.log1p(df.pop("total_incurred") / df["actual_exposure"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=CATEGORICAL)

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
                "Cancelled years of policies in force from 1 January get a full year on risk",
                "A portfolio policy, and any policy in a later year in the file, is in force from 1 January, so its "
                "time on risk falls below a year only when it is cancelled, and cancelled years claim almost twice as "
                "often per exposure-year. For them the exposure is set to a full year and the premiums to annual "
                "premiums. In a new-business policy's first year in the file a cut cannot be told from a late start, "
                "so its values stay (curation notes).",
                exposure,
            ),
        ]
