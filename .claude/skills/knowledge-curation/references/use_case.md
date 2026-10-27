# The use case and the prediction point

Part 2 of the curation rules, under P3 (a real use case) in [principles.md](principles.md). The rules of earlier parts
win over this file's rules in a conflict; within this file a rule wins over the rules below it of the same strength.
How to weigh, exceptions and amendments: [principles.md](principles.md).

A dataset in the benchmark simulates a decision someone makes with a prediction. This file covers that decision: the
use case, the prediction point, the real-world target, the inputs known at prediction time, how closely the data
mirrors the use case (the fit), and whether the model predicts for a new or a known entity.

## Rules

### The use case

**USE-1 (Must).** A use case is an actor, a moment and a decision: "a lender, when an application arrives, decides
whether to approve it". Write it down before anything else, and check every column, filter, target and split choice
against it. Why: the written prediction point finds columns no probe flags. How: the use-case checklist under Methods.
Cases: kickstarter.

**USE-2 (Must).** A task no decision fits is out. The kinds of labels no decision fits are SEL-4 to SEL-7 in
[selection.md](selection.md), and data that serves only a study looking back is SEL-3. Marker:
`No Good Target / Scientific Discovery` (the fit None, USE-8). Cases: under SEL-3 to SEL-7.

### The prediction point

**USE-3 (Must).** Name the prediction point: when the model is used and what is known then. A value that did not
exist at that point is a leak (LEAK-10, [leak_checks.md](leak_checks.md)), including a field that is blank because the
outcome already happened and a feature computed over a window that ends at the outcome. Typical prediction points are
under Patterns. Cases: kickstarter.

**USE-4 (Must; narrows USE-3).** When the features include measurements from a stage after the decision the task
models (a biopsy after the clinical examination, a lab result after triage), offer the task at the stage the source
describes. [task_probes.md](task_probes.md) TP-6 keeps its own wording on a valid task against its best version.
Cases: eryhemato_squamous_disease.

### The real-world target

**USE-5 (Must).** Predict what the actor would act on, at the resolution they act on it. Check how the source built its
label before accepting it. A target the source defined badly can often be redefined into the real one. A label from a
named publication whose construction is undocumented (the quantity, its scale or the rule that sets it) and cannot be
checked may ship with `fit="approximate"` and a note naming the gap; decide the details case by case. Whether a rating
or grade ships as a number or as classes is decided case by case too: by how the source models and scores it, checked
against common sense and the practice of similar use cases (Lennart, 2026-10-21). A label checked and found to be
another quantity than the one the actor acts on still fails (Lennart, 2026-10-21, diabetes_3). Cases:
corporate_credit_rating, cirrhosis_patient_survival_prediction, diabetes_3, blood_tests_drink_prediction.

### Inputs known at prediction time

**USE-6 (Must).** Anything known at the prediction point is a legitimate input, including a number the company itself
computed. A company's own estimate made before the outcome is an input, and the model refines it; a forecast the task
corrects is the task's input. Why: dropping it changes the task into "predict without the company's estimate". Cases:
brazilian_ecommerce, bias_correction_r_bias_correction_r_2.

**USE-7 (Must).** A row that lacks the input the prediction acts on is no task row: drop it rather than keep it as
missing. Missing values of the other inputs stay missing. Why: nobody corrects a forecast that does not exist. Cases:
bias_correction_r_bias_correction_r_2 (Lennart, 2026-10-15), nyc_taxi_trip_duration_1m and
pkdd_15_taxi_trip_time_prediction_ii_1m (a 100 m radius around the pickup, 2026-10-26).

### How closely the data mirrors the use case

**USE-8 (Must).** Write how closely the data mirrors the use case, its fit:

* Direct: the rows, the features, the label's timing and the split mirror the use case.
* Approximate: a stand-in with a known gap, named as such: one snapshot standing in for a forecast, a reconstructed
  time axis, a label definition the sources do not settle (no stated horizon, or a breadth or horizon that cannot be
  verified), one judge or rating service standing for the rating a buyer meets, a task changed a lot to avoid a leak.
* None: no decision fits (USE-2). The dataset goes back to triage.

A potential leak kept on purpose does not by itself make a fit approximate, however much signal it carries (a weak
LEAK-30 keep, a remnant measured to carry no signal, or fields worth ROC AUC +0.066 as in kick): the fit is that of
the task without the leak, and the leak is named in the notes ([leak_checks.md](leak_checks.md)) and in `fit_reason`
as kept, not as a gap. The fit becomes approximate only when avoiding the leak needed a large change to the task
(Lennart, 2026-10-21, sarcoma, house_sales; a strong kept leak: Lennart, 2026-10-21, kick,
homesite_quote_conversion). An unverified label definition is a known gap and makes the fit
approximate (Lennart, 2026-10-21, differentiated_thyroid_cancer_recurrence).

A selection bias does not by itself make a fit approximate either (`Selection Bias`, [selection.md](selection.md),
"Selection bias"). Judge it against the real-world setting of the use case: when that setting has the same bias (it
meets the same selected cases), the data mirrors it and the fit is direct; `fit_reason` still names the selection
(Lennart, 2026-10-27).

Marker for None: `No Good Target / Scientific Discovery`. Cases: direct, airfoil_self_noise, superconductivity,
2_month_survival_rate_prediction, kick and homesite_quote_conversion (a strong kept leak); approximate, account_debt_south_africa
(one snapshot for a forecast), alfa_battle_2_0_task_2 (a label without a stated horizon), coffee_rating_prediction
(one judge for the rating a buyer meets; Lennart, 2026-10-14), differentiated_thyroid_cancer_recurrence (an unverified
label breadth), sarcoma (a closed set of types; its kept preprocessing does not count).

**USE-9 (Should; narrows USE-8).** Before settling on approximate, ask whether the data as shipped mirrors another
well-defined use case that practitioners have, where the features are known and the label is not. If it does, that is
the use case and the fit is direct. Weigh it together with the factor against it under Weighed factors: a use case
rephrased only to excuse a gap. Cases: 5g_energy_consumption (Lennart, 2026-10-14).

### Recurring entities and the cold start

**USE-10 (Must).** Decide from the use case whether the entity the model predicts for is new or known, before choosing
the split (SPLIT-3, [splits.md](splits.md)). For a known entity, its history is legitimate: the split is temporal and
the previous outcome is a feature. A cold start predicts for an entity without history (a shadow rating of a new
borrower, a recommender before it has data on a person), and a grouped split tests it. Cases: corporate_credit_rating,
in_vehicle_coupon_recommendation.

**USE-11 (Must; narrows USE-10).** When the use case is the first event of each entity, one row per entity makes it an
IID task without grouping. Take one row per entity only when the use case is that row: it loses rows and signal.
Cases: breast_cancer_prediction (Lennart, 2026-10-15), corporate_credit_rating.

### A leak in a real task

**USE-12 (Must).** A leak in the features is no reason to reject a task whose use case is real. The remedy for a leak
is to fix it and keep the task; [leak_checks.md](leak_checks.md) decides how.

## Weighed factors

* **An entity seen before** (+ for a known entity, USE-10): most real predictions are for entities seen before. An
  agency reviews every rating at least once a year; a bank scores its existing customers.
* **A use case rephrased only to excuse a gap** (−, against a direct fit under USE-9): do not rephrase a use case only
  to excuse a gap. A credit model scores future applicants, so a random split of undated applications stays
  approximate.

## Patterns

Quick ways to apply the rules; a pattern never overrides a rule, and the dataset at hand wins over the pattern.

* Typical prediction points (USE-3): at launch (kickstarter), at admission (mic), at quote time (homesite), at checkout
  (brazilian_ecommerce), before the stay ends, photometric classification (sdss_17), cold start for a new respondent
  (in_vehicle_coupon_recommendation).
* A credit rating → the issuer rating (USE-5). An agency rates the company and each of its debt instruments
  separately; the decision a lender or an investor takes rests on the issuer rating (S&P issuer credit rating, Moody's
  corporate family rating, Fitch issuer default rating), not on whichever instrument rating a file happened to keep.

## Methods

### Writing the use case (USE-1)

Take the use case from the source (the paper, the competition, the data card) when it states one; otherwise write the
most plausible one and say "for example". Then write down:

1. what one row is, with its population, place and period;
2. what is predicted, by when after the prediction point, in what classes or unit;
3. what is known at the prediction point, and nothing recorded later;
4. what the test data stands for (new customers, the next two weeks, configurations never measured, unseen patients).

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.

| Rule | Dataset | Decision (date, curator) | Kind |
|---|---|---|---|
| USE-1, USE-3 | kickstarter | once the task was "predict at launch", the written prediction point found `staff_pick`, awarded mid-campaign, which no probe flagged (2026 leak audit) | applied |
| USE-1, USE-5 | nba_players_2016_2019 | `No` + `No Good Target / Scientific Discovery`, `Not Representative`: no actor, moment or decision fits (the prediction point moved twice to fit the data, 25 of 35 features are end-of-season values), and the score ranks the whole ballot where the actor acts on its 2 or 3 starters; more seasons would be a rebuild of our own and fix neither (2026-10-26, Lennart) | applied |
| USE-1 | glioma_grading_clinical_and_mutation_features | `No` + `No Good Target / Scientific Discovery`: the grade is the pathologist's diagnosis, made before the DNA is sequenced, so a model can only cross-check a label that already exists; a cross-check of a known label is no use case, and the source names no clinical setting (2026-10-26, Lennart) | applied |
| USE-4 | eryhemato_squamous_disease | offered on the 12 clinical features, before the skin biopsy | applied |
| USE-5 | corporate_credit_rating | 17% of the checkable labels were not the issuer rating; retired for a rebuild from the agencies' own histories (2026-10-16) | applied |
| USE-5 | cirrhosis_patient_survival_prediction | time to death over the patients who died became death or transplant within five years, over the patients followed that long | applied |
| USE-5 | diabetes_3 | Efron et al. (2004) describe the label only as "a quantitative measure of disease progression one year after baseline", with no measure, scale, clinic or inclusion rule: kept with fit approximate and a note (2026-10-21, Lennart; USE-5 amended) | applied |
| USE-5 | blood_tests_drink_prediction | the quantity is known (drinks per day), how it was recorded is not: kept with fit approximate | applied |
| USE-5 | mobile_churn | no churn rule and no horizon stated: approximate under the amendment, now that PROV-2 (amended 2026-10-21, Lennart) keeps a sound upload with a source to point to | applied |
| USE-5 | wine_quality, numerai_v5_2_1m, corporate_credit_rating | a rating or grade ships as regression or as classes by the source, checked against common sense and similar use cases, with no general rule: wine_quality's 0-10 grade and numerai's target as regression, as their sources model them; corporate_credit_rating as letter classes with the rare grades merged (carried into corporate_issuer_credit_rating) (2026-10-21, Lennart) | applied |
| USE-6 | brazilian_ecommerce | the delivery date Olist promised at checkout stays an input: it is fixed before the delivery, so it cannot leak; R^2 0.366 with it, 0.332 without (2026-10-15) | applied |
| USE-6 | bias_correction_r_bias_correction_r_2 | the LDAPS weather model's forecast, which the task corrects, is the input | applied |
| USE-6 | 2_month_survival_rate_prediction | the physicians' day-3 survival estimates and DNR orders are not inputs: the source's task is an objective estimate set beside the physician's, who was interviewed only as its comparator (Knaus et al. 1995); differs from breast_cancer_prediction, where the radiologist's BI-RADS reading is the actor's own input (2026-10-26, Lennart) | applied |
| USE-7 | bias_correction_r_bias_correction_r_2 | the three days without an LDAPS run are dropped (2026-10-15, Lennart) | applied |
| USE-7 | nyc_taxi_trip_duration_1m, pkdd_15_taxi_trip_time_prediction_ii_1m | an ETA with the destination named at pickup: a recorded end within 100 m of the start is no destination anyone names, so those trips are dropped in both (nyc reopened to match pkdd, where a 15-second GPS clock turns a return to the start into an end within 100 m); the cut rests on the inputs, not on the travel time (2026-10-26, Lennart) | applied |
| USE-8 | airfoil_self_noise, superconductivity, 2_month_survival_rate_prediction | direct | applied |
| USE-8 | account_debt_south_africa | approximate: one snapshot stands in for a forecast | applied |
| USE-8 | kick | approximate for a potential leak kept on purpose (missing WheelType, ROC AUC 0.757 with, 0.691 without); reopened by the amendment of 2026-10-21, under which a kept leak alone no longer makes a fit approximate; now direct (next row) | applied |
| USE-8 | kick, homesite_quote_conversion | a strong kept leak stays direct: kick's missing WheelType (ROC AUC +0.066) and homesite's two status-like fields (+0.050) are named in `fit_reason` as kept, not as a gap; qsar_aquatic_toxicity and onlinenewspopularity moved to direct the same way, and perth_house_prices, credit_card_customers, african_credit_scoring_challenge and zillow_prize stay approximate for their other gaps only (Lennart, 2026-10-21) | applied |
| USE-8 | alfa_battle_2_0_task_2 | approximate: a reconstructed time axis or a label without a stated horizon | applied |
| USE-8 | coffee_rating_prediction | approximate: one judge or rating service stands for the rating a buyer meets (2026-10-14, Lennart) | applied |
| USE-8 | house_sales | a remnant kept from after the sale (view, waterfront, the neighbours' areas; about 145 rows changed, RMSE 0.2147 masked against 0.2132 kept) does not make the fit approximate: USE-8 amended (2026-10-21, Lennart) | applied |
| USE-8 | sarcoma | approximate for the closed set of confirmed types (five, four since the merge of 2026-10-22); the source's preprocessing over all patients, kept under LEAK-30, does not count toward the fit (2026-10-21, Lennart) | applied |
| USE-8 | differentiated_thyroid_cancer_recurrence | approximate: what counts as recurrence is not verified (all 32 patients of the ATA high-risk class recurred, so it seems to include persistent disease), and the horizon differs between UCI and the cohort paper (2026-10-21, Lennart) | applied |
| USE-8 | qsar_oral_toxicity | approximate: the screening is simulated; held out by scaffold (2026-10-26), 16.3% of the test chemicals have a close training analog (Tanimoto 0.7 or more) against 11.0% of the project's untested chemicals (24.7% under a random split; 19.7% against 9.3% before the extension) (2026-10-21, Lennart; numbers of 2026-10-26) | applied |
| USE-8 | qsar_bioconcentration | direct: held out by scaffold (SPLIT-31), a test chemical stands for an untested one of a series not yet measured (6.4% have a close training analog, 12.6% under a random split); the authors' nine selected descriptors are dropped (LEAK-31), so no kept leak remains (2026-10-26, Lennart) | applied |
| USE-8 | qsar_fish_toxicity, qsar_aquatic_toxicity | open for the curator: both read `direct` with random tested chemicals as test rows, the setting in which qsar_oral_toxicity read approximate (19.7% against 9.3% with a close analog, 2026-10-21); the releases hold descriptors only, so neither the scaffold split (SPLIT-31) nor the analog share can be computed. Either approximate as oral, with the gap named in `fit_reason`, or direct with the unmeasurable gap recorded as the fact that sets them apart. Either way qsar_fish_toxicity's `fit_reason` should name its kept potential leak (six descriptors chosen by a genetic algorithm on 726 of the 908 chemicals, which overlap the test folds), as qsar_aquatic_toxicity's does (proposed 2026-10-26, AI) | proposed |
| USE-9 | 5g_energy_consumption | direct: a split by station within one week fills the gap for stations without measurements, rather than standing in weakly for a forecast (2026-10-14, Lennart) | applied |
| USE-10 | corporate_credit_rating | a known entity: 72% of the ratings with an earlier one repeat its class, and the previous rating lifts a random forest's skill from 0.285 to 0.460 | applied |
| USE-10 | in_vehicle_coupon_recommendation | cold start: a recommender before it has data on a new respondent, tested by a grouped split | applied |
| USE-11 | breast_cancer_prediction | each woman's earliest exam, since screening assesses her at the first exam; IID without grouping (2026-10-15, Lennart) | applied |
| USE-11 | corporate_credit_rating | what one row per entity costs: the latest rating per company scored 0.112 skill, all ratings grouped by company 0.158 | applied |

## In Data Foundry

The use case is written in a definition's `task_summary` with its `fit`, and the prediction point opens its
`curation_comments`: [definitions.md](../../knowledge-data-foundry/references/definitions.md).
