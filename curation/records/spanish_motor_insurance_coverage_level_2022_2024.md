---
unique_name: spanish_motor_insurance_coverage_level_2022_2024
name: A detailed dataset of motor insurance policies with coverage-specific financial information (Spanish insurer, 2022-2024, Mendeley)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
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
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
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

CC (2026-11-03, Andrej): the check warning `task_target_value_dominant` accepted: "for these tasks this is natural and a core challenge" (zero-inflated target).

CC (2026-11-06, Lennart): REVIEW.md issue 6 resolved by decision D10 of the exposure study of 2026-11-05: `actual_exposure` is the training weight (`sample_weight`, MET-15) as well as the Gini's weight, every premium is annualised and `total_exposure` leaves the features (LEAK-41); the log1p target and the weighted Gini stay. Applied after the weighted re-measure of the same day found no remaining column whose cancellation signal pays on the declared metric (the premium mark, the year's last record, first-year cancellation from the features; the numbers are in the definition's notes and REVIEW.md issue 6). Supersedes Andrej's calls of 2026-11-02: keep the corrected `total_exposure` as the model feature with the 5,653 first-year cuts an approved limitation (REVIEW.md issues 2 and 3), since LEAK-41's partial-correction clause, adopted after that call, takes a length corrected on some rows and realized on others out of the features whatever it scores (the exposure study's +0.0032 for the cuts under weighted Tweedie, 7 of 9 of its own folds, did not hold on the shipped splits: -0.0012 net, SE 0.0006, 3 of 9); keep the premiums as published ("Keep both with explicit potential-leak notes; do not round the premiums", issue 4), since an earned premium carries the cut and annualising removes it (Spearman 0.024 with the time on risk among the first-year cancellations), while the premiums stay unrounded and the year's last record stays with its note; keep the task without a training weight (issue 5), since the training-weight API now exists (`sample_weight`), and with it and the annual premiums both weighted fits beat the premium alone (0.317 against 0.298).

**Assessment (AI, 2026-11-06):** on the CC of 2026-11-06 above (D10, Lennart), which stays as written: the re-review panel of the same day found that the annualised premiums still carry the time on risk in their decimals. The annual tariffs sit on a 5-decimal grid, so a part-year's annualised premium falls back on it while a full year keeps 11 to 15 decimals; the decimal counts rank the 32,626 located cancellations at ROC AUC 0.965, and read as features they gain +0.0035 under weighted Tweedie (SE 0.0017, 8 of 9 splits). So the CC's "no remaining column whose cancellation signal pays" and "annualising removes it" hold for the premiums' values, not for their decimals. Rounding them to the cent removes the mark (AUC 0.565) at no measurable cost (-0.0005 under Tweedie, +0.0005 under L2, SE 0.0006, 9 splits x 10 seeds), but it changes "the premiums stay unrounded" and Andrej's "do not round the premiums" (issue 4), so it waits for the curator (REVIEW.md issue 7), whose CC line will correct this one.

**Assessment (AI, 2026-11-06):** review panel (full, re-review under LEAK-41, MET-14 to MET-16): ship after changes, once the annualised premiums are rounded to the cent; disputed: cent rounding now or on the curator's yes (settled: the curator's, issue 7), whether the premiums' gain through any cancellation sends option A of issue 6 back (settled: no, +0.0013 under Tweedie after rounding, SE 0.0008, 10 seeds, below the panel's bar), whether `business_type` needs its note before shipping or is a weak keep (settled: the note now, the column stays); for the curator: issues 7 and 8.

**Assessment (AI, 2026-11-06):** the panel's changes that need no decision are in the definition (rows, target, weight, split and metric unchanged): the texts that said no premium carries the time on risk now name the decimals' mark (issue 7); `business_type`, read from the year's last record, has its note (probe 22: 41% of the fit of the time on risk, gain through it -0.0040 under Tweedie and -0.0118 under L2; against its 1 January value the last value gains +0.0002 and -0.0014); the premiums' gain through any cancellation is +0.0010 under Tweedie with 10 seeds (SE 0.0006; 3 seeds gave +0.0020); `splits_comment` is re-measured (the 2024 window 0.300 to 0.316 against 0.309 and 0.311 on the folds' 2024 rows; the leak test across the split +0.0045 to +0.010 pooled, within each year, carried by no column), which supersedes the split figures of the 2026-11-02 Assessment above (row Gini on the old target); the metric reason cites CAS Monograph 5 for the exposure-weighted Gini and Frees, Meyers and Cummings for the premium-based one; `bonus_score` is an ordered category (bad < neutral < good); the planned time on risk of late starts moved from `fit_reason` to the notes.

**Assessment (AI, 2026-11-06):** correction to the panel line above: the panel did not dispute the cent rounding (both briefs and both rebuttals leave it to the curator's yes, as review issue 7 asks); for the curator: review issues 7 and 8.

CC (2026-11-08, Lennart): the annualised premiums are rounded to the cent (REVIEW.md issue 7 (B), "Round to the cent"): unrounded, their decimals marked a part-year (ROC AUC 0.965 for the located cancellations, 0.565 rounded). This corrects the CC of 2026-11-06 (D10, "every premium is annualised ... while the premiums stay unrounded"): every premium is annualised and rounded to the cent, and that CC's "no remaining column whose cancellation signal pays" held for the premiums' values, not for their decimals. It changes the wording of Andrej's call of 2026-11-02 ("do not round the premiums", REVIEW.md issue 4) on a fact found after it, the decimals' mark; his reason concerned the prices, which the cent rounding keeps.

CC (2026-11-08, Lennart): `payment_frequency` is an ordered category, fewest payments a year first: annual < semiannual < quarterly (REVIEW.md issue 8 (C), "Ordered in all three"), with the same order by payments a year in pricing_game_2016_french_fleet and pricing_game_2017_french_mtpl, so the three pricing tables stay alike.

**Assessment (AI, 2026-11-08):** both CC lines above applied in the definition. Re-run on the rebuilt frame (premiums rounded to the cent; untuned LightGBM; the run folder of the exposure review, `apply_2026-11-08`): the eight premiums' decimal counts and cent-grid flags rank the 32,626 located cancellations among the 169,919 policy-years in force from 1 January at ROC AUC 0.565 (0.965 on the unrounded frame, same script, folds grouped by policy), and no grid from 1 EUR to 1e-5 separates them (AUC at most 0.501); the decimal counts as features gain +0.0001 under weighted Tweedie (SE 0.0017, 5 of 9) and -0.0012 under weighted L2 (SE 0.0013, 3 of 9), against +0.0035 and -0.0052 before (9 splits x 2 seeds). The premiums' values still mark a located cancellation at ROC AUC 0.795 from the shipped features (0.81 unrounded, 0.62 without the premiums; first shipped repeat), the flat-amount trace kept with its note. Probe 22 (3 splits x 3 seeds): the time on risk from the features at R^2 0.340 (0.350 before), 1/time on risk alone 0.070, no feature whose gain goes through it under weighted Tweedie or L2. Task probe (5 of 9 splits): LightGBM 0.3187 on the declared metric (0.3165 before), no flags. `dataset check`: 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (`normalized_weighted_gini`) is checked, as declared on the PR #47 review board.

## Reference

Espinosa, P., Lledó, J., Atance, D. (2026). A detailed dataset of motor insurance policies with coverage-specific
financial information. Data in Brief 66:112883. https://doi.org/10.1016/j.dib.2026.112883
Data: Mendeley Data, https://doi.org/10.17632/sw4jmdb2sm.1 (CC BY 4.0).

Lead: curator's list of exposure-scaled insurance tables (Chubb comparison), 2026-10-20; not in the v4 workbook.
