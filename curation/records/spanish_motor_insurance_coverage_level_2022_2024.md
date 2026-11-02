---
unique_name: spanish_motor_insurance_coverage_level_2022_2024
name: A detailed dataset of motor insurance policies with coverage-specific financial information (Spanish insurer, 2022-2024, Mendeley)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: Other
year: '2026'
domain: insurance
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.17632/sw4jmdb2sm.1
- https://doi.org/10.1016/j.dib.2026.112883
- https://pmc.ncbi.nlm.nih.gov/articles/PMC13234478/
v2_path: datasets/_dev/tabarena-v0pt2/spanish_motor_insurance_coverage_level_2022_2024/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a lead list of exposure-scaled insurance tables, the source pages and papers, and the downloaded data where the notes say so. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 3: a recent, documented portfolio of a Spanish motor insurer,
insured-years 2022-2024 with exposure and incurred cost per cover; two columns need fixing and the three years give one
window.
- Source: Espinosa, Lledó and Atance, Data in Brief 66:112883 (2026), data on Mendeley (doi:10.17632/sw4jmdb2sm.1, CC BY
  4.0). Sec. 3: "Each observation corresponds to an insured individual for a given year", "It contains a total of
  354,140 observations and 47 variables", 1 January 2022 to 31 December 2024; Sec. 4: "The primary dataset originates
  from a Spanish motor insurance company", anonymised before the transfer and again by the authors. One table.
- Use case: the article names the reuse (abstract: "This structure supports reuse in actuarial pricing, risk modelling
  and insurance research"): an insurer setting next year's premium per insured; fit direct. Regime temporal by year with
  insureds recurring (185,678 insureds); the three years give one window above the 50% floor (2024, 47% of rows), short
  of SPLIT-14's three, so SPLIT-8 (forced grouped by insured) unless finer dates turn up.
- Siblings and duplicates: `spanish_motor_insurance_2015_2018` (TBD -> 2nd Tier, priority 3; Lledó's group, 2015-2018):
  no overlap in period or schema; this article cites it only as [9] for a coverage breakdown and does not say whether
  the insurer is the same (PROV-6 or PROV-7, open for the curator, as noted there).
- Papers and pages: the Data in Brief article (PMC13234478) and the Mendeley record.
- Metric: none (the article reports no model or evaluation; read on PMC), so the fallback (`rmse`).
- Earlier AI triage, 2026-10-20, measured: `total_incurred` 0 in 88.1% of rows (own damage 96.0%); untuned LightGBM
  2022-23 -> 2024: AUC 0.69 for a claim, R^2 -0.03 on log1p among positives.
- Risks for /add-dataset: `policy_status` "Indicates whether the policy was active (A) or cancelled (C) at calendar
  year" end, after the prediction point (LEAK-10, drop); `vehicle_age` behaves as years since licensing on 99.9% of rows
  (earlier triage) against Table 2's "Age of the insured vehicle"; which cover is the target (total, or own damage on
  comprehensive policies); the CICOS agreement applies "pre-agreed amounts between participating insurers regardless of
  actual damage" (Limitations), a pile in the positive part; exposure handling and the left-out negative incurred rows
  are the family's insurance-conventions question.
- Priority: gap 0, use case + (the article names actuarial pricing), source + (a data article with a variable table),
  shape + (354,140 insured-years, 47 columns, years), risk - (a year-end status column, a mislabelled age, one window).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning is in `curation/inputs/two_regime_zero_triage_summary.md`, "Policy calls of 2026-10-30"); the curator
has the call.
- Target: `total_incurred` per insured-year (all covers, paid plus reserved): the premium covers the whole policy, and a
  per-cover target would be the same rows with a swapped target (one, not both). Own damage on the comprehensive
  policies is the alternative if the curator wants the Chubb-like property cover.
- `total_exposure`: a feature, as in the `fremtpl2` call.
- Negative amounts: the authors already left out rows with negative incurred amounts (Experimental Design); nothing to
  set, but the README names the selection.
- Metric: normalized Gini as a context metric (MET-11); the article reports no model.
- Drop `policy_status` (LEAK-10); `vehicle_age` renamed to years since licensing; split grouped by insured unless finer
  dates turn up (one temporal window).

CC (2026-10-30, Andrej): `Yes`, priority 4 (the AI screening had `TBD -> Yes`, priority 3; zero-inflated screening
review page).

Anonymised motor portfolio of an unnamed Spanish insurer, 1 January 2022 to 31 December 2024 (Espinosa, Lledó and
Atance, Data in Brief 66:112883, 2026; CC BY 4.0 on Mendeley). It has 354,140 rows for 185,678 insureds (67,172,
118,835 and 168,133 by year), with premiums, claim counts and incurred cost (paid plus reserved) for each of seven
covers. Data Description: "Each observation corresponds to an insured individual for a given year". The authors kept
the last record per insured and year out of 653,943 raw rows and left out rows with negative incurred amounts
(Experimental Design).

Zeros, measured 2026-10-20: `total_incurred` is 0 in 88.1% of rows. Own damage (property + theft + fire) is 0 in
96.0%, and in 86.8% of the comprehensive policies (`COMP_E`, `COMP_N`, the only types with property-damage cover).
8,543 rows report claims at zero cost. Untuned LightGBM, 2022-23 -> 2024 (168,133 rows): AUC 0.69 for any claim
(exposure alone 0.60), R^2 -0.03 on log1p among positives. Own damage on comprehensive policies: AUC 0.68 (0.70 with
the premiums), R^2 -0.07. The severity signal is weak, as in the rest of the family, and the article warns that the
fixed amounts of the CICOS agreement cluster indemnities (Limitations).

Fixes needed. `vehicle_age` is not the vehicle's age: `driver_age` = `vehicle_age` + `age_driving_licence` within a
year on 99.9% of rows, so it is years since licensing, and `age_driving_licence` is the age at licensing (Table 2 and
the text disagree on that column). `policy_status` is set at year end and must go: 13.9% of cancelled insured-years
have a claim at a mean exposure of 0.53, against 11.7% at 0.73 for active ones. For the Chubb-style target, use
`total_exposure` x `vehicle_value` with own-damage, theft and fire incurred on the comprehensive policies; liability
losses do not scale with vehicle value. A separate release by Lledó and Pavía (Mendeley 5cxyb5fp4f, November 2015 to
December 2018, 105,555 rows) is not in the log either, and whether it comes from the same insurer is open.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/spanish_motor_insurance_coverage_level_2022_2024/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping after the panel's changes; only issue 1, the forced grouped split of three years (open against how_much_did_it_rain), could turn it to `No`. The model beats the premium alone on 3 of 3 splits. Changes after the panel: the full-year fix also covers 13,842 cancelled new-business years of policies in force on 1 January, 23 zero liability premiums made missing. Corrections to the notes above: no row with a negative incurred amount was left out (354,140 rows before and after); negative cover amounts are excluded from the sum `total_incurred`, which supersedes the 2026-10-30 Assessment and the text below the CC; the metric is the normalized Gini (context), not the fallback `rmse`; "R^2 -0.03 on log1p among positives" was another split, +0.024 on the shipped grouped folds; no policyholders shared with the 2015-2018 release were found. `required_split` and `tags` wait for your marks on the field rows (issue 1). Priority 3: gap + (insurance thin), use case 0 (fit approximate on the forced split), source + (data article), shape + (354,091 rows, grouped), risk - (the forced split is open; late values kept with notes).

CC (2026-11-02, Andrej): the forced grouped split ships (issue 1 (a); the record takes `Grouped (NON-IID)` and `Non-IID (Grouped)` as the issue says): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none).

CC (2026-11-02, Andrej): the located cancellations stay fixed and the cut time on risk of the 5,653 first-year cancellations is kept with its note (issue 2, (a) written as (b)); recorded as the LEAK-10 case for time on risk cut short by the outcome (leak_checks.md, Mechanisms table): the cut is removed or fixed where the data locates it, kept with its measured size where it cannot.

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split (SPLIT-8 as amended 2026-11-02) finds none (untuned LightGBM, first three shipped splits). Shared rows and hidden groups: 30 of about 354,000 test rows have an exact feature copy in training, with no shared outcome (claim shares 0.11 / 0 / 0.15 against 0.22 / 0 / 0.08 for their copies); about 2.8% of test rows match a training row on car and driver (brand, weight per horsepower, seats, fuel, value, age at licence, area, birth year) under another id, against 2.5% for the same key with the birth year shifted, and those training rows' mean outcome as a feature adds +0.0011 Gini, the same as the shifted-key control (+0.0010); random policy-years score as the grouped folds (Gini 0.408 both, split audit) and the group probe finds no gap (R^2 0.068 IID against 0.066 grouped). Shared period: the training side's mean outcome of the row's year adds 0.0000 Gini (an outcome-free recoding of the year +0.0022, model noise), of year x municipality x area +0.0009 (SE 0.0011) and of year x brand 0.0000; removing the test year's rows from training costs 0.005 Gini more than removing as many random rows (SE 0.005, 4 of 9), though that also removes the year's flat CICOS amount; and the valid 2024 window scores 0.385 against 0.375 to 0.405 on the folds' 2024 rows. Features from other rows' outcomes: none (column audit); `bonus_score` and the premiums carry the policy's own history, whose years all sit on one side. Scripts in the run's leakcheck folder (leak.py, leak2.py, leak3.py).

CC (2026-11-02, Andrej): metric (issue 3): "Use exposure-weighted Gini on annualised claim costs for this dataset. Preserve original actual exposure in a scoring-only column for annualising observed costs and weighting the metric. Keep corrected total_exposure as the model feature; do not also expose original exposure to the model. Retain the existing cancellation corrections and the approved limitation for the 5,653 ambiguous first-year cancellations. Ensure predictions and observed costs are compared on the same annualised scale." Late values (issue 4): keep both with potential-leak notes, premiums not rounded; the evidence is "no consistent score gain detected in the tested comparisons", the rounding change no bound on the leak; revisit if records from the actual prediction point become available.

**Assessment (AI, 2026-11-02):** implemented: target `log1p_incurred_per_exposure_year` (the cost over the recorded time on risk), metric `normalized_weighted_gini` weighted by the scoring column `actual_exposure`, `total_exposure` (corrected) a feature. The time on risk alone scores -0.035 to 0.010 (0.177 to 0.221 under the row Gini). The premium per year alone scores 0.277 to 0.316 and untuned LightGBM on log1p 0.269 to 0.324, below the premium on each of the first three splits; Tweedie fit with the time on risk as sample weight 0.292 to 0.341 (open as REVIEW.md issue 5; the AI recommends keeping the task). Giving the located cancellation status outright changes the Gini by -0.004 to -0.012.

CC (2026-11-02, Andrej): ship. Every issue of the REVIEW is resolved: the exposure-weighted Gini on the cost per year on risk, marked as declared (issue 3, the metric row), both late values kept with notes and the premiums unrounded (4), the task kept although an untuned plain model scores below the premium alone (5).

## Reference

Espinosa, P., Lledó, J., Atance, D. (2026). A detailed dataset of motor insurance policies with coverage-specific
financial information. Data in Brief 66:112883. https://doi.org/10.1016/j.dib.2026.112883
Data: Mendeley Data, https://doi.org/10.17632/sw4jmdb2sm.1 (CC BY 4.0).

Lead: curator's list of exposure-scaled insurance tables (Chubb comparison), 2026-10-20; not in the v4 workbook.
