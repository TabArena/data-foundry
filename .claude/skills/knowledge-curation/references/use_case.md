# The use case and the prediction point

Part 2 of the curation rules, under P3 (a real use case) in [principles.md](principles.md). The rules of earlier parts
win over this file's rules in a conflict; within this file a rule wins over the rules below it of the same strength.
How to weigh, exceptions and amendments: [principles.md](principles.md).

A dataset in the benchmark simulates a decision someone makes with a prediction. This file covers that decision: the
use case, the prediction point, the real-world target, the inputs known at prediction time, how closely the data
mirrors the use case (the fit), and whether the model predicts for a new or a known entity.

## Rules

### The use case

**USE-1 (Must; amended 2026-11-11, Lennart, on lung_adenocarcinoma_metastasis).** A use case is an actor, a moment and a
decision: "a lender, when an application arrives, decides whether to approve it". Write it down before anything else,
and check every column, filter, target and split choice against it. Why: the written prediction point finds columns no
probe flags. How: the use-case checklist under Methods. A label read from the same specimen the features measure, and
settled before they are taken, leaves only a cross-check of a known label and fits no decision. A label found by a
separate work-up is ground truth, also when the rows are a retrospective series of resolved cases, which is how such a
task can be built at all. So is a label written in the specimen's own note that rests on information outside the
specimen (an earlier cancer elsewhere), when the actor decides it with a tool that predicts it from such data: the slide
cannot settle it. Cases: kickstarter; glioma_grading_clinical_and_mutation_features and lung_cancer's histology (label
from the specimen); ljubljana_primary_tumor (label from a separate work-up); lung_adenocarcinoma_metastasis (label
written in the specimen's pathology note but resting on an earlier cancer outside it; the actor's tool is an expression
tissue-of-origin test as a second opinion).

**USE-2 (Must).** A task no decision fits is out. The kinds of labels no decision fits are SEL-4 to SEL-7
in [selection.md](selection.md), and data that serves only a study looking back is SEL-3. A label that stands in for
what the features already measure fits no decision either: once the actor holds the inputs, they act on those. Marker:
`No Good Target / Scientific Discovery` (the fit None, USE-8). Cases: under SEL-3 to SEL-7;
blood_tests_drink_prediction; biomechanical_orthopaedic_prediction (the rest after SEL-5);
early_stage_diabetes_risk_prediction (symptoms that prompt the test themselves).

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
meets the same selected cases), the data mirrors it and the fit is direct; when it does not, the selection is a known
gap and the fit is approximate. Either way `fit_reason` names the selection and the marker stays (Lennart, 2026-10-27).
A selection alone never makes the fit None: a dataset with one is retired only for a reason of its own
(early_stage_diabetes_risk_prediction; Lennart, 2026-11-11).

Marker for None: `No Good Target / Scientific Discovery`. Cases: direct, airfoil_self_noise,
2_month_survival_rate_prediction, kick and homesite_quote_conversion (a strong kept leak),
infrared_thermography_temperature (a selection its setting shares); approximate, account_debt_south_africa (one
snapshot for a forecast), alfa_battle_2_0_task_2 (a label without a stated horizon), coffee_rating_prediction (one
judge for the rating a buyer meets; Lennart, 2026-10-14), differentiated_thyroid_cancer_recurrence (an unverified
label breadth), sarcoma (a closed set of types; its kept preprocessing does not count), superconductivity (a
selection its setting does not share: only superconductors).

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
| USE-1 | lung_cancer, lung_adenocarcinoma_metastasis | lung_cancer's histology retired (2026-11-10, Andrej): resected tumours, whose slide already settles it; the source never predicts it, and clusters a taxonomy instead. The same arrays ship as lung_adenocarcinoma_metastasis (2026-11-11, Andrej) with the study's flag of a possible metastasis from another organ: the source's "key issue in lung tumor diagnosis". 15 of its flags are written in the resected tumour's own pathology note, like the histology, but hedged ("c/w colon met", "?Br MET") and resting on an earlier cancer outside the specimen, which the slide cannot settle; the 8 colon calls come closest to settled and are the easiest part (out-of-fold ROC AUC 0.984). One set of arrays carries a label on each side of the line between a cross-check and a prediction. Written into USE-1 as an amendment (2026-11-11, Lennart, review issue 1, B): the use case names the expression tissue-of-origin test (Pathwork Tissue of Origin, CancerTYPE ID) as the pathologist's second opinion when the stains leave the origin open, a niche tool used mostly for cancers whose origin is unknown; re-read under the amendment, glioma_grading_clinical_and_mutation_features, eucalyptus and tcga_lung_histology stay cross-checks (their labels are settled on the specimen) | applied |
| USE-1, USE-8 | ljubljana_primary_tumor | kept, fit approximate (2026-11-11, Andrej): patients whose primary was found, a retrospective series with the site known for every patient, which is the ground truth the task needs; the site comes from a separate work-up, not from the specimen the features measure, unlike lung_cancer | applied |
| USE-2 | blood_tests_drink_prediction | drinks per day estimated from five blood tests that respond to alcohol: as a stand-in for liver damage the blood tests are the better measure, and as a check of a patient's account the doctor already holds the blood values and can ask; no decision rests on the estimate: retired with `No Good Target / Scientific Discovery` | applied |
| USE-2 | biomechanical_orthopaedic_prediction | `degree_spondylolisthesis` is the slip that defines one of the three classes (one threshold, accuracy 0.974); without it the five other measures still separate disc hernia from normal (ROC AUC 0.889, shuffled labels at most 0.59) and spondylolisthesis from the rest (0.913), so the rest was reassessed as a new task (SEL-5): disc hernia is diagnosed from MRI and symptoms the table lacks, and nobody reads spondylolisthesis from pelvic shape with the slip on the same radiograph. Retired with `No Good Target / Scientific Discovery` (2026-11-05), the reason restated on 2026-11-10 (Andrej) | applied |
| USE-2, USE-8 | early_stage_diabetes_risk_prediction | a symptom questionnaire deciding on a blood-sugar test: a person with the symptoms is tested because of them, and screening without symptoms uses risk factors the table lacks (only age, sex and a yes/no obesity); retired with `No Good Target / Scientific Discovery` and `Not Representative`. Its hospital sample (69% diabetic, 67 of 78 negatives men) keeps `Selection Bias` but alone would have made the fit approximate, as for eryhemato_squamous_disease and hepatitis_c_prediction; the untrained symptom rule (ROC AUC 0.906, below the methods) and the high scores (tuned methods spread) are no reasons (2026-11-11, Lennart; retired by Andrej 2026-10-27) | applied |
| USE-4 | eryhemato_squamous_disease | offered on the 12 clinical features, before the skin biopsy | applied |
| USE-5 | corporate_credit_rating | 17% of the checkable labels were not the issuer rating; retired for a rebuild from the agencies' own histories (2026-10-16) | applied |
| USE-5 | xente_fraud_detection_challenge | the fraud label follows a review applied above about 500k UGX on a shipped input: within the same customers' spans, 109 of 110 rows at 500k-1M are fraud against 16 of 149 at 100k-490k, minutes apart, so a 0 below the step means "not reviewed" as much as "not fraud"; `No` for now with `Data Quality Issue`, to revisit with a second curator's reading or the host's account of how `FraudResult` was set (2026-11-04, Lennart). It differs from ieee_fraud_detection, whose chargeback rule labels every transaction | applied |
| USE-5 | cirrhosis_patient_survival_prediction | time to death over the patients who died became death or transplant within five years, over the patients followed that long | applied |
| USE-5 | diabetes_3 | Efron et al. (2004) describe the label only as "a quantitative measure of disease progression one year after baseline", with no measure, scale, clinic or inclusion rule: kept with fit approximate and a note (2026-10-21, Lennart; USE-5 amended) | applied |
| USE-5 | blood_tests_drink_prediction | the quantity is known (drinks per day), how it was recorded is not: kept with fit approximate; retired later (2026-11-05) on another ground, no decision rests on the prediction | applied |
| USE-5 | mobile_churn | no churn rule and no horizon stated: approximate under the amendment, now that PROV-2 (amended 2026-10-21, Lennart) keeps a sound upload with a source to point to | applied |
| USE-5 | wine_quality, numerai_v5_2_1m, corporate_credit_rating | a rating or grade ships as regression or as classes by the source, checked against common sense and similar use cases, with no general rule: wine_quality's 0-10 grade and numerai's target as regression, as their sources model them; corporate_credit_rating as letter classes with the rare grades merged (carried into corporate_issuer_credit_rating) (2026-10-21, Lennart) | applied |
| USE-6 | brazilian_ecommerce | the delivery date Olist promised at checkout stays an input: it is fixed before the delivery, so it cannot leak; R^2 0.366 with it, 0.332 without (2026-10-15) | applied |
| USE-6 | bias_correction_r_bias_correction_r_2 | the LDAPS weather model's forecast, which the task corrects, is the input | applied |
| USE-6 | 2_month_survival_rate_prediction | the physicians' day-3 survival estimates and DNR orders are not inputs: the source's task is an objective estimate set beside the physician's, who was interviewed only as its comparator (Knaus et al. 1995); differs from breast_cancer_prediction, where the radiologist's BI-RADS reading is the actor's own input (2026-10-26, Lennart) | applied |
| USE-6 | medical_facility_operational_data | the patient's own minutes early (scheduled time minus arrival) is derived and added as `minutes_early`: the front desk knows it at check-in, the prediction point, though the source's features describe the facility's state for the next patient, whoever it is, and use the timestamps only for sorting; untuned LightGBM MAE 15.29 without it, 13.56 with it (-11%, 9 windows, 2 seeds). Differs from 2_month_survival_rate_prediction, whose physician estimates are the comparator the source's task is set beside, not an input of its actor (2026-11-05, Lennart) | applied |
| USE-6 | australian_vehicle_insurance_2004_2005 | `gender` stays a rating factor: sex is known at the quote, and the Tensions row on rating factors (amended 2026-11-09) drops it from an insurance pricing task only where today's law of the data's country bars it; s41 of the Sex Discrimination Act 1984 (Cth) allows it in Australia. A Tweedie GLM gains +0.004 with it (SE 0.001, 7 of 9 splits), boosting nothing above noise. Differs from bemtpl97, frempl_french_motor_personal_line, pricing_game_2017_french_mtpl and spanish_homeowners_motor_insurance_2010_2014, whose sex columns stay out as EU law bars them today, as if the ban had always applied (Andrej, 2026-11-09; dropped 2026-11-08 under the family stance, Lennart) | applied |
| USE-7 | bias_correction_r_bias_correction_r_2 | the three days without an LDAPS run are dropped (2026-10-15, Lennart) | applied |
| USE-7 | nyc_taxi_trip_duration_1m, pkdd_15_taxi_trip_time_prediction_ii_1m | an ETA with the destination named at pickup: a recorded end within 100 m of the start is no destination anyone names, so those trips are dropped in both (nyc reopened to match pkdd, where a 15-second GPS clock turns a return to the start into an end within 100 m); the cut rests on the inputs, not on the travel time (2026-10-26, Lennart) | applied |
| USE-7 | protein_model_quality_rf_pcp | the rosetta62 set's 1,011 relaxed natives (`_rn<pdb>.out.N`, kept in the folder `relaxed_natives/` of the set's archive) leave by identity, like the 4,893 named natives: an energy-minimised experimental structure exists only once the reference is known, so it is no candidate of a new target; they held the best candidate in 55 of 56 proteins (LightGBM 0.355 with them, 0.322 without); the filter is on the file name, never the label; applied through CLEAN-11 (2026-11-05, Lennart) | applied |
| USE-8 | airfoil_self_noise, superconductivity, 2_month_survival_rate_prediction | direct; superconductivity approximate since 2026-10-27 (the selection-bias row below) | applied |
| USE-8 | account_debt_south_africa | approximate: one snapshot stands in for a forecast | applied |
| USE-8 | kick | approximate for a potential leak kept on purpose (missing WheelType, ROC AUC 0.757 with, 0.691 without); reopened by the amendment of 2026-10-21, under which a kept leak alone no longer makes a fit approximate; now direct (next row) | applied |
| USE-8 | kick, homesite_quote_conversion | a strong kept leak stays direct: kick's missing WheelType (ROC AUC +0.066) and homesite's two status-like fields (+0.050) are named in `fit_reason` as kept, not as a gap; qsar_aquatic_toxicity and onlinenewspopularity moved to direct the same way, and perth_house_prices, credit_card_customers, african_credit_scoring_challenge and zillow_prize stay approximate for their other gaps only (Lennart, 2026-10-21) | applied |
| USE-8 | alfa_battle_2_0_task_2 | approximate: a reconstructed time axis or a label without a stated horizon | applied |
| USE-8 | coffee_rating_prediction | approximate: one judge or rating service stands for the rating a buyer meets (2026-10-14, Lennart) | applied |
| USE-8 | house_sales | a remnant kept from after the sale (view, waterfront, the neighbours' areas; about 145 rows changed, RMSE 0.2147 masked against 0.2132 kept) does not make the fit approximate: USE-8 amended (2026-10-21, Lennart) | applied |
| USE-8 | sarcoma | approximate for the closed set of confirmed types (five, four since the merge of 2026-10-22); the source's preprocessing over all patients, kept under LEAK-30, does not count toward the fit (2026-10-21, Lennart) | applied |
| USE-8 | eryhemato_squamous_disease, ljubljana_primary_tumor, superconductivity; infrared_thermography_temperature | a selection bias is judged against the real-world setting: the first three move from direct to approximate, as their settings do not share it (a dermatologist's lichen planus patients, metastases of unknown origin, a screen of mostly non-superconductors); infrared stays direct, its university clinic seeing mostly students; the `Selection Bias` marker stays on all four (2026-10-27, Lennart) | applied |
| USE-8 | differentiated_thyroid_cancer_recurrence | approximate: what counts as recurrence is not verified (all 32 patients of the ATA high-risk class recurred, so it seems to include persistent disease), and the horizon differs between UCI and the cohort paper (2026-10-21, Lennart) | applied |
| USE-8 | qsar_oral_toxicity | approximate: the screening is simulated; held out by scaffold (2026-10-26), 16.3% of the test chemicals have a close training analog (Tanimoto 0.7 or more), 24.7% under a random split (2026-10-21, Lennart; numbers of 2026-10-26). The project's untested chemicals are the screening population: of its 48,135 readable prediction chemicals, 19.8% are in this dataset, and the other 38,598 have a close analog in the training side of scaffold folds for 11.2%, against 15.1% for those folds' test chemicals, so the gap holds (2026-11-11) | applied |
| USE-8 | qsar_bioconcentration | direct: held out by scaffold (SPLIT-31), a test chemical stands for an untested one of a series not yet measured (6.4% have a close training analog, 12.6% under a random split); the authors' nine selected descriptors are dropped (LEAK-31), so no kept leak remains (2026-10-26, Lennart) | applied |
| USE-8 | qsar_fish_toxicity, qsar_aquatic_toxicity | open for the curator: both read `direct` with random tested chemicals as test rows, the setting in which qsar_oral_toxicity read approximate (19.7% against 9.3% with a close analog, 2026-10-21); the releases hold descriptors only, so neither the scaffold split (SPLIT-31) nor the analog share can be computed. Either approximate as oral, with the gap named in `fit_reason`, or direct with the unmeasurable gap recorded as the fact that sets them apart. Either way qsar_fish_toxicity's `fit_reason` should name its kept potential leak (six descriptors chosen by a genetic algorithm on 726 of the 908 chemicals, which overlap the test folds), as qsar_aquatic_toxicity's does (proposed 2026-10-26, AI) | proposed |
| USE-8 | heart_disease | approximate: two of the 13 inputs are tests no longer done (thallium-201 scan, calcium on fluoroscopy, replaced by CT) and Cleveland ran all three tests by study protocol; the referral for angiography is the setting of the use case (the check before a scheduled angiogram), not the gap. The era alone stays direct (2_month_survival_rate_prediction, body_density_prediction, forensic_glass_identification) (2026-10-27, Lennart) | applied |
| USE-8 | lt_vehicle_loan_default_prediction | `Selection Bias`: the approval decision faces every applicant, but the release holds only the loans L&T approved, so the data is a selected subset of what the actor would want; lending_club, home_credit_default_risk, credit_g and give_me_some_credit carry no marker because their releases are the data their own use cases use (Lennart, 2026-11-05: "here we know we would want to use more but dont have it, in the others we have the data we want to use") | applied |
| USE-9 | 5g_energy_consumption | direct: a split by station within one week fills the gap for stations without measurements, rather than standing in weakly for a forecast (2026-10-14, Lennart) | applied |
| USE-9 | chicago_traffic_crashes | approximate: a city road-safety analyst, who ranks sites by expected people killed or seriously injured, replaces the emergency-response analyst, as 50.9% of the rows are desk reports nobody was dispatched to (5.3% injured against 25.5% on scene); every row stays. The better actor is no direct fit: police reports catch about half of serious injuries in trauma-registry linkage, the 'reported, not evident' share steps up in 2023Q4, and the road facts recorded more completely for injury crashes are dropped (LEAK-10). The blind reviewer named the same actor without our notes (2026-11-05, Lennart) | applied |
| USE-10 | corporate_credit_rating | a known entity: 72% of the ratings with an earlier one repeat its class, and the previous rating lifts a random forest's skill from 0.285 to 0.460 | applied |
| USE-10 | in_vehicle_coupon_recommendation | cold start: a recommender before it has data on a new respondent, tested by a grouped split | applied |
| USE-10, LEAK-34 | tunisian_fraud_detection_challenge | a known entity in a retrospective task: the taxpayer's previous adjustment (the label of its most recent earlier fiscal year in the data) and the years since it ship as features, built from the dropped id over strictly earlier years only, so a test row's previous label is always a training label; LightGBM mean RMSE 5.863 to 5.533 on 3 yearly windows by 2 seeds. What sets it apart from lt_vehicle_loan_default_prediction, moved to the decision at disbursement on 2026-11-04: Tunisian in-depth verifications cover several open years (Ministère des Finances FAQ), so ranking past years is the real decision, while a loan cannot be approved after the fact (2026-11-05, Lennart) | applied |
| USE-11 | breast_cancer_prediction | each woman's earliest exam, since screening assesses her at the first exam; IID without grouping (2026-10-15, Lennart) | applied |
| USE-11 | corporate_credit_rating | what one row per entity costs: the latest rating per company scored 0.112 skill, all ratings grouped by company 0.158 | applied |

## In Data Foundry

The use case is written in a definition's `task_summary` with its `fit`, and the prediction point opens its
`curation_comments`: [definitions.md](../../knowledge-data-foundry/references/definitions.md).
