---
unique_name: mic
name: MIC
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- Clinical Study
original_source: Other
year: '2020'
collection_period: 1992-1995
required_split:
- Random (IID)
problem_type: Multiclass Classification
source_links:
- https://www.openml.org/search?type=data&id=45648
- https://doi.org/10.24432/C53P5M
notebook_path: datasets/beyond_iid/old_iid/mic/mic.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/mic/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: predict at admission, dropping the 9 ICU day-1..3 columns.** The dataset description (Golovenkin et al., Leicester data 2020, doi 10.25392/leicester.data.12045261.v3, "Problems to solve") defines four prediction times; at admission all inputs except columns 93-95 and 100-105 (R_AB_1..3_n, NA_R_1..3_n, NOT_NA_1..3_n) may be used, at the end of day 3 all of them. The notebook used day 3, but LET_IS ("Lethal outcome (cause)", column 124) counts any in-hospital death, so a patient who died before day 2 or 3 has no records for those days: 126 of the 138 rows missing a day-3 field died (91%, base rate 16%); 74 of the 110 cardiogenic-shock deaths miss day-2 and day-3 fields, against 10 of 1,428 survivors. Golovenkin et al. 2020 (GigaScience 9:giaa128) list these variables as "in the ICU in the second/third day of the hospital period" (Table 1) and refer to the Leicester description for the task. Dropping them: death AUC 0.93 -> 0.91 (leak audit 2026-09-24). ZSN_A (chronic heart failure, anamnesis) is missing for 54 rows, 93% of them deaths (flag AUC 0.59): an admission-time field, kept.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Myocardial infarction complications Database - Almost no description or source info on OpenML. Likely from: https://scholar.google.de/citations?view_op=view_citation&hl=de&user=Gms_lDcAAAAJ&citation_for_view=Gms_lDcAAAAJ:olpn-zPbct0C;

Seems to be a preprocessed version from 10.24432/C53P5M UCI
Contains EEG data? Several outputs

Hospital mortality prediction at different time points with details which (time-invariant) features are allowed. Relevant task.

Potential issue: EEG data?

Lennart: Maybe a valid predictive task but might contain non-tabular source data

Andrej: use UCI versionNeeds some preprocessing and is rather small, but otherwise is a good dataset.

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Thromboembolism (lethal outcome 5) has 12 rows, 4 in every test fold of about 567. They are 0.7% of the test rows and 4.8% of a random forest's log loss (0.58 against 0.71 for the class shares). Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The deposit lists prediction problems and time points but no evaluation metric; the GigaScience paper studies trajectories, not prediction scores.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 11 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `INF_ANAM`, `STENOK_AN`, `FK_STENOK`, `IBS_POST`, `GB`, `DLIT_AG`, `ant_im`, `lat_im`, `inf_im`, `post_im`, `TIME_B_S` (the README lists their levels); left unordered: `ZSN_A` (a partial order).

CC (2026-11-01, Lennart): marks on the review board of PR #37: ZSN_A stays unordered as a partial order (two lines of severity), noted in the definition.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `gusto_i_mi_mortality` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 11 coded columns carry their words; 2 scores are numbers (FK_STENOK, GB).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): counts with a cut end are numbers: INF_ANAM.

CC (2026-11-01, Lennart): counts with a cut end stay ordered categories of the source's levels, the cut end a level of its own (CLEAN-14): the lossless form, chosen from the context rather than by model runs; the same day's numbers with censoring flags are reverted.

CC (2026-11-17, Andrej): the declared split (random, 10x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. Care drifts measurably within the file and has changed since; both are facts against.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below (issue 1, A, 2026-11-18).

**Main points:** The BeyondArena v0.2 review's issues are in this review from 2026-11-25 as 6, 7, 8, 9; the parked ones are open again. Better-data check (2026-11-25, issue 5): Add GUSTO-I (gusto_i_mi_mortality) next to mic and let issue 6 decide mic on its own data: GUSTO-I is the clean, 24-times-larger death task, but it does not separate methods (LightGBM 0.826 against logistic regression 0.826 ROC AUC, splines best on 15 of 15 folds), so it cannot stand in for mic's multiclass task. Earlier: `ForcedIIDFromTemporal` stays (issue 1, A, 2026-11-18). Nothing is left open.

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: Krasnoyarsk 1992-1995, no admission date, file sorted by outcome; order within each block shows drift but the blocks share no calendar.
     - Use: Cardiologists estimate lethal complications at admission for later MI patients, 30 years after.
     - Mechanism: Admission ECG, history and labs to in-hospital death and its cause; mortality given them depends on reperfusion care, which changed (primary PCI) and already drifted inside the file.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | mic's own within-block order | Trental 15%->35% in ICU; first vs second half AUC 0.82/0.58/0.72; last fifth of each block vs random fifth | not flat: death ROC AUC 0.77 vs 0.84 (SD 0.02) | same data |
     | 2_month_survival_rate_prediction (SUPPORT) | v3 stationary-relation test, phase I 1989-91 -> phase II 1992-94, death ROC AUC forward vs contemporaneous | flat (LightGBM gap 0.0008, TabPFN gap 0.0027) | clinical prognosis of hospitalised patients from admission physiology, one 3-year step |
     | Rogers WJ et al., 'Trends in presenting characteristics and hospital mortality among patients with STEMI and NSTEMI in the NRMI, 1990 to 2006', Am Heart J 2008;156:1026-1034 | in-hospital MI mortality 1990-2006 | not flat: mortality fell with reperfusion | same outcome and era |

   * **For a stationary use case:**
     - SUPPORT's admission prognosis was flat over a 3-year step.
   * **Against:**
     - structure in the file order: drift in care and a 0.07 ROC AUC cost on each block's last fifth.
     - changed treatments (PCI, drugs) since the 1990s.
     - 30-year span.
   * **Earlier views:**
     - CC 2026-11-17 (Andrej): random 10x3 checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | structure in the file order: drift in care and a 0.07 ROC AUC cost on each block's last fifth; changed treatments (PCI, drugs) since the 1990s |

   * **Recommendation:** A, care drifts measurably within the file and has changed since; both are facts against. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (Care drifts measurably within the file and has changed since; both are facts against.)

5. **Which dataset carries death after a heart attack: mic alone, GUSTO-I next to it, or GUSTO-I instead?**

   * **Problem:**
     - The open unknown is filled: on GUSTO-I's 40,830 patients untuned LightGBM on all 28 inputs scores what a logistic regression does (ROC AUC 0.826 and 0.826, log loss 0.2011 against 0.1997), a regression with splines beats both on every fold, and the five classic predictors alone reach 0.810.
     - mic still carries the parked blank-history leak (issue 6: 60 patients with a blank history, 54 dead; blanks alone predict death at 0.78, and still at 0.74 after dropping the 60), and it is the only open data with causes of death and complications.
     - Keep mic alone (A), add GUSTO-I next to it (B), replace mic by GUSTO-I (C), or retire mic with no replacement (D)?
   * **Background:** mic in v0.2: 1,699 patients of one Krasnoyarsk hospital (1992-1995), 102 admission inputs, 8-class lethal outcome (271 deaths), log loss, random split tagged forced from temporal (issues 7 and 8, settled). issue 6 is parked: the AI answers of 2026-11-04 to 11-10 found the blanks follow the block a patient was filed in (deaths filed together); filling was withdrawn on Andrej's note, and the last answer (2026-11-10) recommended retiring mic, with keeping the 35 near-complete columns as the fallback. issue 9 (2026-11-11) searched the candidates and recommended B; its table stands and is shortened here:

     | Dataset | Patients (deaths) | Inputs | Outcome | Split it allows | Access | Concerns | Verdict |
     |---|---|---|---|---|---|---|---|
     | mic (Krasnoyarsk, 1992-1995) | 1,700 (271) | 102 at admission | death by cause, 8 classes | random, forced from temporal | CC BY 4.0 | blank-history leak (issue 6); small | - |
     | GUSTO-I trial, 15 countries, 1990-1993 (hbiostat.org/data/repo/gusto.rda) (checked) | 40,830 (2,851, 7.0%) | 28: age, sex, Killip class, blood pressure, pulse, infarct site, ST leads, history, risk factors, height, weight, trial arm, region | death by day 30, binary | random, or grouped by region or site group (16 / 48 / 121 levels) | open, "Permission is granted to anyone ... reference the original paper" | no method spread (below); trial cohort of the thrombolysis era; 4 duplicate rows; `tpa` blank by arm (redundant with `tx`) | better data for death; not a replacement for the task |
     | MIMIC-IV / eICU AMI cohorts | about 4,700-12,000 | EHR | in-hospital death | dated | credentialed, no redistribution | a cohort to build | not available |
     | WHAS500, Vellore NSTEMI, Alkmaar, registries | 149-313,825 | - | death | - | small, unreleased or on application | - | not better or not available |

   * **Effect on the task:** GUSTO-I answers only the death part of mic's task, on clean and larger data; the eight classes (cause of death and complications) exist only in mic. On GUSTO-I a few strong, smooth predictors carry most of the information (Lee et al.: about 90% in five), so a well-specified regression is the reference and flexible models gain nothing; a benchmark entry there rewards calibration and smoothness, not interactions. How issue 6 bears on each option: A and B keep mic, so issue 6 must still be settled, and every variant tested so far either leaves a blank signal (drop the 60: 0.74) or removes the ECG, blood tests and blood pressures (35 columns: no blanks, death AUC 0.75-0.80); B adds a death task that has no such leak next to it. C and D retire mic, which closes issue 6 as retired (the recommendation of 2026-11-10); C then keeps a myocardial-infarction death task in the benchmark, D does not.
   * **Experiments:** 2026-11-25. GUSTO-I: `gusto.rda` from hbiostat.org (downloaded 2026-11-11), read with pyreadr; inputs without `day30`, `tpa` and the site-group ids; 5-fold x 3 repeats, random and grouped by site group (`grps`, 121 groups); logistic regression (one-hot categories, standardised numbers, optionally cubic splines with 4 knots), LightGBM defaults. mic: the 1,700 patients of the source file, issue 6's variants, the same folds as in issue 6 (5-fold x 3); logistic regression with missing indicators, LightGBM defaults.

     GUSTO-I, death by day 30:

     | Model | ROC AUC, random | Log loss, random | ROC AUC, grouped by site | Log loss, grouped | Folds better than LR, all (AUC; log loss) |
     |---|---|---|---|---|---|
     | LR, five predictors (age, systolic BP, pulse, Killip, location) | 0.810 | 0.2059 | 0.810 | 0.2060 | 0 of 15; 0 of 15 |
     | LR, five predictors, splines | 0.817 | 0.2036 | 0.817 | 0.2037 | 0 of 15; 0 of 15 |
     | LR, all features | 0.826 | 0.1996 | 0.826 | 0.1997 | - |
     | LR, all features, splines | 0.830 | 0.1985 | 0.830 | 0.1985 | 15 of 15; 13-14 of 15 |
     | LightGBM, five predictors | 0.810 | 0.2072 | 0.810 | 0.2074 | 0 of 15; 0 of 15 |
     | LightGBM, all features | 0.827 | 0.2010 | 0.826 | 0.2011 | 5-9 of 15; 3-4 of 15 |

     mic under issue 6's variants (death ROC AUC from a binary model; 8-class log loss):

     | Variant | Patients (deaths) | Inputs | Death AUC, LR | Death AUC, LightGBM | Log loss, LR | Log loss, LightGBM |
     |---|---|---|---|---|---|---|
     | as shipped | 1,700 (271) | 101 | 0.893 | 0.912 | 0.603 | 1.017 |
     | drop the 60 | 1,640 (217) | 101 | 0.873 | 0.895 | 0.567 | 0.955 |
     | 35 near-complete columns, 78 patients dropped | 1,622 (248) | 35 | 0.800 | 0.760 | 0.589 | 1.083 |

     Untuned LightGBM overfits mic's 8-class log loss (about 1.0 against 0.6); the benchmark's tuned models do not, so mic's spread is read on death AUC: gradient boosting leads by 0.02 with the blanks or without the 60, and trails by 0.04 once no blank is left.
   * **Consistency:** the batch's pattern: a better dataset from another source is its own record, and the old one keeps the verdict its own data earn[^better]; here as for website_phishing, the old dataset carries its own parked problem (issue 6), decided apart from the new record. A task where a simple model is the answer is not by itself a reason to turn it down: the Cleveland heart-disease dataset is disputed because an untrained 6-point score comes close to a logistic regression and the best model; on GUSTO-I the five predictors stay 0.02 below the full model.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep mic alone (implemented) | no new record built; mic as issue 6 decides | no work; keeps the only open multiclass outcome after a heart attack | the clean death data stays unbuilt; issue 6's leak is the task's only check on death |
     | B | Add GUSTO-I next to mic | build gusto_i_mi_mortality (binary, ROC AUC or log loss, split by region or random); mic stays as issue 6 decides | 40,830 patients, no blank pattern, open permission; grouped split by region costs nothing; a leak-free check on mic's death signal | no method spread (LR = LightGBM; splines best); thrombolysis era; issue 6 still to settle |
     | C | Replace mic by GUSTO-I | as B, and issue 6 closes with mic retired | one clean heart-attack task instead of a small leaky one | loses the causes of death and complications; trades a task that separates methods (0.02 on death AUC) for one that does not |
     | D | Retire mic, no replacement | issue 6 closes with mic retired, GUSTO-I not built | nothing to build | no heart-attack task left in the benchmark |

   * **Recommendation:** B: the 2026-11-11 recommendation holds; GUSTO-I is the clean, large death task and its lack of spread is the domain's (a few smooth predictors), not a defect, while mic keeps the multiclass outcome it alone has; whether mic stays is issue 6's decision, not this one's. C if issue 6 retires mic and one heart-attack task is enough. **Decision:** A, B, C or D?

   **Notes for the AI:** on B or C: move gusto_i_mi_mortality to Yes with a CC (<date>, Andrej): line and Andrej in checked_by; add https://hbiostat.org/data/repo/gusto.rda and the hbiostat permission text (https://hbiostat.org/data) to source_links and the record; /add-dataset from that file: target `day30`; drop `tpa` (blank for the SK+tPA arm, redundant with `tx`) and keep `tx` (randomised, known at admission); `sho`, `hig`, `dia`, `hyp`, `hrt`, `ttr` are derived flags of the paper's model (check against Lee et al. before keeping them next to their sources); 4 duplicate rows; split random or grouped by `regl` (16 regions; site group `grps` gave the same scores); note 40,830 of 41,021 enrolled; tags Samples: Over Time, Time: Lost, Clinical Study; the thrombolysis-era cohort as an Outdated question for the reviewer. On C also retire mic through issue 6 (record No (Retired), Class-dependent Recording, CC line, folder removed, CHANGELOG). On D, issue 6's retirement only. On A, nothing here. Evidence: the run's evidence folder (scripts/gusto_spread.py, scripts/mic_spread.py, spread_1411436.log, mic_spread.out, gusto.csv read from dl_gusto/gusto.rda); earlier: the run's evidence folder, the run's evidence folder Sources: Lee et al. 1995 https://doi.org/10.1161/01.cir.91.6.1659.

   [^better]: Selection pattern "Small or dated, and the task is still done today" with PROV-4 (Must): a better dataset from another source is its own record, not a duplicate, and the old one keeps the verdict its own data earn until the curator decides.

6. **Drop the 60 patients whose medical history is blank, 90% of them dead?**

   * **Problem:**
     - On 2026-09-30 Lennart kept `ZSN_A` (chronic heart failure in the history) although its blank marks death (93% of
       54 rows), reading it as a field known at admission.
     - The history blocks follow the same pattern: in 60 patients the heart-failure item, the arrhythmia history or the
       conduction-disorder history is blank, and 54 of them died (base rate 16%), while their admission ECG and blood
       pressure were recorded at least as often as for the others.
     - A field left blank because the outcome came first is a leak, which is why the day-1 to day-3 records were
       dropped[^1a]; drop these patients, or keep the blanks?
   * **Background:** "anamnesis" is the history the doctors take at admission (earlier heart attacks, angina, heart
     failure, rhythm and conduction disorders, diabetes, lung disease). A patient in shock may not be able to give it,
     which would make a blank a real admission state; a chart left incomplete because the patient died would not.
   * **Experiments:** on the 1,699 shipped patients (checks, no model):
     - Blank sections: `ZSN_A` 54 rows, 92.6% dead; the arrhythmia history (`nr_*`) 21 rows, 90.5%; the conduction
       history (`np_*`) 18 rows, 100%; any of the three 60 rows, 90% dead, 6 survivors. Blank history items per patient:
       0.58 among the dead, 0.02 among survivors.
     - Of the 60, only 25% were in cardiogenic shock and 22% (ZSN_A rows) in pulmonary oedema on admission, and 43%
       died before the day-2/3 records, so about half lived past day 3 with the history still blank; the admission ECG
       is blank for 5% of them against 9% of the others.
     - Dropping them leaves 1,639 patients, 13.2% dead: cardiogenic shock 88 (from 110), rupture 49 (54), ventricular
       fibrillation 21 (27), asystole 19 (27), heart failure 17 (23), pulmonary oedema 14 (18), thromboembolism 9 (12).
   * **Effect on the task:** a model learns "history not filled in, so the patient dies", which a model at admission
     could use only if the blank already existed then; in model runs the models read these blank sections.
   * **Consistency:** follows gallstone_disease, whose rows recorded through a second route that models recognised were
     dropped (2026-10-26/27), and the day-1 to day-3 drop here; departs from Lennart's call on `ZSN_A` of 2026-09-30.
   * **Unknown:** when the history was written (at admission or from the chart afterwards); the source does not say.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | all 1,700 patients; blanks stay missing | Lennart's call; a blank can be a real admission state | a recording pattern that follows death stays readable |
     | B | Keep, with a note | as A, plus a `Potential leak, kept on purpose:` note with the numbers | documents the risk | the pattern stays readable |
     | C | Drop the 60 patients | rows whose `ZSN_A`, `nr_*` or `np_*` history is blank are dropped; 1,639 of the 1,699 shipped patients remain | removes the strongest death-linked blanks; follows gallstone | loses 54 of 271 deaths; thromboembolism falls to 9 patients |
     | D | Drop the history columns | `ZSN_A` and the `nr_*` and `np_*` blocks dropped | keeps every patient | loses real admission history for all patients; other history blanks remain |

   * **Recommendation:** C: the blanks follow death in patients whose ECG and blood pressure were taken and half of whom
     lived past day 3, so they mark a record left incomplete rather than an admission state; if you read the blank as
     an admission state, B. **Decision:** keep (A), keep with a note (B), drop the 60 patients (C) or drop the history
     columns (D)?

   **Notes for the AI:** on C, in `_clean` after the decoding, drop the rows where `ZSN_A` is missing or every column
   of the `nr_*` block or of the `np_*` block is missing; curation note with the numbers above; `changes` and `row`
   in the task summary (about 1,640 patients; count them on the v0.2 frame, which holds patient 1 too); a
   `Class-dependent Recording` marker on the record if you agree it is one; `dataset check`; re-run `task_probes.py`
   for `few_minority` (thromboembolism). On B, the note's text: "Potential leak, kept on purpose: the history section
   (`ZSN_A`, `nr_*`, `np_*`) is blank for 60 patients, 54 of whom died ...". CC line in the record either way.

   **Andrej (2026-11-04, discuss):** So the issue is that we are faced with a dataset with entries collected over time and our goal is to reconstruct the state of the dataset that was truly there at admission while keeping as much information as possible. How can we do this?

   **Answer (AI, 2026-11-04):**

   * **Question:** how to get back to what was known at admission while losing as little as possible.
   * **What settles it:** the file is three blocks put together by outcome, and each block was recorded with its own
     pattern of blanks:
     - patients 1-1,020: survivors, 35% with a non-lethal complication; patients 1,021-1,426: survivors, 97% with a
       complication; patients 1,427-1,700: 271 deaths and 3 coded "0" (the codebook's "unknown").
     - Among survivors alone, the blanks tell the second block from the first (out-of-fold AUC 0.72); they tell the
       death block from the complication block at 0.76-0.78.
     - So a blank says which block a patient was filed in. It is not a state at admission, and it is not limited to
       the 60 patients or to the history.
   * **The values are fine by time:** the source's description dates every column. History items are "in the
     anamnesis", the ECG and drugs "at the time of admission" or "in the ICU"; only the 9 day-1 to day-3 columns are
     barred at admission, and they are already dropped. What is left to fix is the blanks, not the values.
   * **Where the death signal in the blanks sits** (blanks alone, out of fold, death AUC; 0.5 = none):
     - all 102 inputs 0.78; history 0.64; ICU blood pressure 0.59; infarct location on the ECG 0.58; blood tests
       0.57; emergency-team blood pressure and drugs 0.56; ECG rhythm 0.54; ICU drugs 0.50.
     - Blank history is not explained by how sick the patient was: given the admission risk from the other inputs,
       it still multiplies the odds of death by 23. Within the death block, blank-history patients died before day 2
       or 3 as often as the others (48% against 46%).
     - Blank ICU blood pressure is not a ward triage: 187 of those 267 blanks (70%) sit in patients 1-408 of the
       first survivor block (53% and 40% blank in its first two fifths, 7% in the rest), and only 4 deaths have one.
     - Every patient has at least one blank, so dropping incomplete rows is not possible.
   * **Variants tested** (5-fold x 3 repeats; gradient boosting and logistic regression with missing indicators; log
     loss of the 8 classes from the logistic regression; on the 1,700 patients of the source file):

     | Variant | Rows (deaths) | Cells filled | Blanks alone: death AUC | Death AUC, boosting | Log loss, LR |
     |---|---|---|---|---|---|
     | as shipped | 1,700 (271) | 0 | 0.78 | 0.90 | 0.604 |
     | drop the 60 patients | 1,640 (217) | 0 | 0.74 | 0.89 | 0.567 (other rows) |
     | history blanks set to "none" | 1,700 (271) | 892 | 0.72 | 0.89 | 0.609 |
     | history columns dropped | 1,700 (271) | 0 (30 columns gone) | 0.72 | 0.87 | 0.592 |
     | every coded blank set to its most common level | 1,700 (271) | 7,566 | 0.65 | 0.88 | 0.607 |
     | every blank filled (coded: most common level; measurements: median) | 1,700 (271) | 11,903 (7% of cells) | none left | 0.87 | 0.622 |

     - The two near-empty columns, family history `IBS_NASL` (96% blank) and `KFK_BLOOD` (99.8% blank), are dropped
       in the last two rows.
     - For the binary items "most common level" is the "no" of the codebook (most are 95-99% "no"). For a few
       multi-level codes it is a guess: time to hospital's most common level holds 23% of patients.
     - Filling every blank costs 0.03 of death AUC and 0.018 of log loss: that is what the blanks were worth.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | all blanks stay | no invented values | blanks alone predict death at 0.78 |
     | B | Drop the 60 patients | the earlier recommendation | removes the strongest blanks | blanks still predict death at 0.74; loses 54 of 271 deaths |
     | C | History blanks set to "none" | 892 cells of 30 history items get the codebook's "none" | keeps every patient and column; the history signal goes (0.52) | blanks elsewhere still predict death at 0.72 |
     | D | Every coded blank set to its most common level | 7,566 cells; near-empty `IBS_NASL` dropped | removes the coded-field signal | blank blood tests and blood pressure still give 0.65 |
     | E | Every blank filled, no indicator | as D, plus median for the measurements; `KFK_BLOOD` dropped | the only variant that leaves no blank pattern; all patients and deaths kept | 7% of cells invented; a guessed level for some multi-level codes; models lose the blank handling the benchmark otherwise tests |
     | F | Retire | record `No (Retired)` with `Class-dependent Recording` | no invented values | loses a real admission task whose values are dated by the source |

   * **Recommendation:** E. The blanks follow the block a patient was filed in, across several groups of fields, so
     only removing all of them gets back to an admission state; the values themselves are dated at admission by the
     source[^a1][^a2]. If 7% invented cells is too much, F. **Decision:** keep (A), drop the 60 (B), fill the history
     (C), fill the coded fields (D), fill every blank (E) or retire (F)?

   **Notes for the AI:** evidence in the run's evidence folder (scripts `exp.py`, `exp2.py`, `exp4.py`,
   `fp.py`; logs `exp*.log`). On E: in `_clean` after the decoding, drop `IBS_NASL` and `KFK_BLOOD`, fill the blanks
   of every coded column with its most common level and of every measurement (`AGE`, the four blood pressures, the
   blood tests) with its median, computed without the label; curation note with the numbers above; `changes` in the
   task summary; a `Class-dependent Recording` marker on the record; `dataset check`; re-run the leak probes on blanks
   and number formats. Untested: whether the values (not only the blanks) also differ by block; the survivor blocks
   differ in complications, so a values-only comparison cannot separate route from case mix. The 3 patients coded 0
   in the death block (1,465, 1,526, 1,690) are "unknown" by the codebook and are scored as survivors; raise it if
   the target is revisited.

   [^a1]: **LEAK-15** (Must): a recording artefact that runs through several features and cannot be undone retires
     the dataset; one that can be undone is fixed. **LEAK-40** (Should): setting cells to missing is no fix when the
     gaps follow the classes, the missing values then mark a class.
   [^a2]: **LEAK-39** (Must): rows of one class recorded through a separate route are dropped when models recognise
     them and the route cannot be aligned; here the route covers every death, so dropping is not open.
   [^1a]: **USE-3** (Must): a value that did not exist at the prediction point is a leak, including a field that is
     blank because the outcome already happened. **LEAK-39** (Must): rows of one class recorded through a separate
     route, found by a recording fingerprint, are dropped when models recognise them and the route cannot be aligned
     with the other rows.

   **Andrej (2026-11-10, change):** Filling blanks doesn't solve the problem since it is still recoverable. We need to understand whether this is a leak. If it is, we need to solve it. Go a bit deeper, how realistic is this use case and how well can we fix class dependent routing, for example by constructing a special split just for this task?

   **Answer (AI, 2026-11-10):**

   * **Finding:** it is a leak, set by how the file was put together. Blank history sits in the death block (54 of 274
     patients) and almost nowhere else (2 of 1,020 and 4 of 406 survivors), and inside any one block a blank says
     nothing about the outcome (table 1).
   * **Not death before the history was taken:** blank-history deaths have a day-2 record as often as other deaths
     (56% against 65%) and a day-3 record (52% against 57%), the same time to hospital, and are spread over the whole
     death block (no batch). More were in shock (25% against 13%), but at the same admission risk the blank still
     multiplies the odds of death by 23 (predicted risk 0.52, observed 0.90).
   * **The use case is real:** the source names admission as its first prediction point, and its authors built such
     predictors. At a real admission the history is asked of every patient, so the blank the file shows does not
     occur in use: a model that learns it does not transfer.
   * **What filling leaves:** the filled cells are no easier to find than real values ("cell equals its fill value":
     death AUC 0.831 filled, 0.840 unfilled). One trace stays: after filling, 6 of the 54 blank-history deaths have
     every history item at its most common level, a pattern no other patient has. Dropping the 60 removes it.
   * **A special split cannot fix it:** the route is the outcome (every death is in the death block), so any split
     has the same link in training and test.
   * **Not fixes:** predicting at day 3 for patients alive at 72 h leaves the blanks at 0.756 (28 of the 34
     blank-history patients still die). Cause of death among the 271 deaths, one route, has no blank signal but no
     signal at all either (table 2). A non-lethal complication on all patients still reads the route (0.55-0.57).

   Table 1: blanks alone, logistic regression, out of fold (0.5 = no signal):

   | Comparison | Outcome | ROC AUC |
   |---|---|---|
   | across blocks | death | 0.778 |
   | across blocks, survivors only | second block (complications) against first | 0.718 |
   | inside the first survivor block | heart failure; any complication | 0.558; 0.572 |
   | inside the complication block | atrial fibrillation; heart failure; reinfarction | 0.471; 0.546; 0.486 |
   | inside the death block | blank history against cardiogenic shock as the cause | 0.449 |

   Table 2: the fixes (5-fold x 3 repeats; death ROC AUC of gradient boosting; log loss of the 8 classes from logistic
   regression with missing indicators):

   | Fix | Patients (deaths) | Blanks alone: death AUC | Trace left | Death AUC | Log loss |
   |---|---|---|---|---|---|
   | none (shipped) | 1,700 (271) | 0.778 | all blanks | 0.901 | 0.604 |
   | drop the 60 patients | 1,640 (217) | 0.736 | other blanks | 0.885 | 0.567 |
   | drop the 30 history columns | 1,700 (271) | 0.719 | other blanks | 0.866 | 0.592 |
   | fill every blank | 1,700 (271) | none | 6 all-"no" histories | 0.873 | 0.622 |
   | drop the 60, fill the rest | 1,640 (217) | none | none found | 0.858 | 0.580 |
   | day 3, alive at 72 h | 1,578 (151) | 0.756 | all blanks | 0.864 | 0.510 |
   | cause of death, deaths only | 271 (271) | log loss 1.654 against 1.674 for the prior | none | - | 1.898 (worse than the prior) |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop the 60, fill the rest | the 60 blank-history patients dropped; `IBS_NASL`, `KFK_BLOOD` dropped; other blanks filled (coded: most common level; measurements: median; 11,040 cells, 6.7%) | no blank pattern and no trace found; the values are dated at admission by the source | loses 54 of 271 deaths; thromboembolism 9 patients; invented cells |
     | B | Fill every blank (the earlier E) | as A without the drop | all deaths kept | 6 patients keep a trace |
     | C | Retire | `No (Retired)` with `Class-dependent Recording` | no invented values | loses a real admission task |
     | D | Day 3, another target or a special split | as tested above | none | the leak stays, or no signal is left |

   * **Recommendation:** A. It is the only variant with no blank pattern and no trace we could find, and the deaths
     left are scored on values the source dates at admission. If 54 dropped deaths and 7% invented cells are too much,
     C. **Decision:** A, B or C?

   **Notes for the AI:** evidence in the run's evidence folder (`explore.py`, `fixes.py`, `fixes2.py`; logs
   `fixes_*.log`, `fixes2_*.log`). On A, in `_clean` after the decoding: drop the rows where `ZSN_A` is missing or
   every `nr_*` or every `np_*` column is missing, drop `IBS_NASL` and `KFK_BLOOD`, fill the remaining blanks (coded
   columns: most common level; `AGE`, the four blood pressures and the blood tests: median, computed without the
   label); `row` and `changes` in the task summary; a curation note with table 2; `Class-dependent Recording` on the
   record; `dataset check`; `task_probes.py` for `few_minority`. On C, retire as records.md says.

   **Andrej (2026-11-10, discuss):** Why do you still fill the blanks? Either it is a leak that can be exploited for which filling is not a solution because it alters the true data distribution. Or it is not a problem so we can leave the blanks. Which is it?

   **Answer (AI, 2026-11-10):**

   * **It is a leak:** the blanks follow the outcome through how the file was put together (deaths filed as one block,
     recorded with their own blanks). Filling is withdrawn; the remedies below fill nothing.
   * **After dropping the 60, the signal is spread over every group of fields** (blanks alone, death ROC AUC): ICU
     blood pressure 0.585, blood tests 0.575, infarct location on the ECG 0.568, ECG rhythm 0.547, history 0.546,
     drugs 0.539, emergency-team blood pressure 0.531. The strongest single columns are `ROE`, the four infarct
     locations and `L_BLOOD` (41-46% dead among the infarct-location blanks).
   * **Dropping more does not remove it:** without the 12 strongest columns, or without every patient blank in them,
     the blanks still give 0.65.
   * **Only one variant leaves no blank:** keep the 35 columns with at most 1% blanks (age, sex, most history,
     complications and drugs on admission) and drop the 78 patients blank there. It loses the ECG, blood tests and
     blood pressures, and death ROC AUC falls from 0.901 to 0.749.
   * Whether the values (not the blanks) also differ by block cannot be tested, since the blocks are the outcomes.

   | Remedy (no filling) | Patients (deaths) | Columns | Blanks alone: death AUC | Death AUC | Log loss |
   |---|---|---|---|---|---|
   | none (shipped) | 1,700 (271) | 102 | 0.778 | 0.901 | 0.604 |
   | drop the 60 | 1,640 (217) | 102 | 0.736 | 0.885 | 0.567 |
   | drop the 60 and the 12 strongest columns | 1,640 (217) | 90 | 0.657 | 0.837 | 0.585 |
   | drop the 60 and every patient blank in those 12 | 1,072 (101) | 102 | 0.646 | 0.839 | 0.480 |
   | keep the 35 columns with at most 1% blanks, drop the 78 patients blank there | 1,622 (248) | 35 | none | 0.749 | 0.589 |
   | retire | - | - | - | - | - |

   Death AUC: gradient boosting; log loss: 8 classes, logistic regression with missing indicators; 5-fold x 3
   repeats, each row on its own patients.

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Retire | `No (Retired)` with `Class-dependent Recording`; folder removed | nothing altered; the artefact runs through every group of fields | loses an admission task |
     | B | Keep the 35 near-complete columns | the other 67 columns dropped, the 78 patients blank in the 35 dropped; no blank left, nothing filled | no blank signal; the true values kept | no ECG, blood tests or blood pressure; death AUC 0.749; the values may still differ by block |
     | C | Drop the 60 only | as tested | smallest change | blanks still give 0.74 |

   * **Recommendation:** A. The leak cannot be removed without either filling or cutting the task down to age,
     history and drugs; B is the fallback if a reduced admission task is worth keeping. **Decision:** A, B or C?

   **Notes for the AI:** evidence in the run's evidence folder (`nofill.py`, `nofill2.py`, logs `nofill_*.log`,
   `nofill2_*.log`). On A, retire as records.md says (record `No (Retired)`, `Class-dependent Recording`, CC line,
   claim released, folder removed). On B, in `_clean` keep the 35 columns (`AGE`, `SEX`, `INF_ANAM`, `GB`,
   `SIM_GIPERT`, `endocr_*`, `zab_leg_*`, the six `*_POST`, `IM_PG_P`, `fibr_ter_*`, the ICU drugs `NITR_S` to
   `TRENT_S_n`) and drop the rows blank in any of them; `row`, `known` and `changes` in the task summary;
   `dataset check`; `task_probes.py` for `few_minority`.

   **Andrej (2026-11-11, discuss):** Park this until we decide whether we use another dataset for this task.

   **Answer (AI, 2026-11-25):** the park ends: the better-data check of 2026-11-25 asks in issue 5 of this review whether another dataset replaces this one, so this issue is open again and waits for a decision. It is written as it stood when it was parked; nothing in it was re-measured today.

   **Note (AI, 2026-11-25):** the BeyondArena v0.2 review's issue 1, parked there on 2026-11-11 and never written into this record; it is kept here under its new number.

7. **Keep random splits, or split by time?**

   * **Problem:**
     - Andrej expects a temporal task, or links among patients of the same day.
     - The source has no admission date, day or ward, and its row order is sorted by outcome, not by time.
     - Keep the random split as it is, or keep it and mark it as forced from a temporal task?
   * **Background:** the source says only "collected in 1992-1995" in one hospital (the Leicester description and
     Golovenkin et al. 2020). No field dates a patient: `TIME_B_S` is the hours from the attack to the hospital.
   * **Experiments:** on the 1,700 patients of the source file (checks; models as batch jobs jobs):
     - Row order: patients 1-1,426 all survived, 1,427-1,700 are 271 deaths and 3 coded "0"; patients 1,021-1,426
       nearly all had a non-lethal complication (97%, against 35% in 1-1,020). A split by row order would put every
       death in the last test fold.
     - Inside each block the order drifts: a model tells the first from the second half at AUC 0.82 in the first
       survivor block, 0.58 in the complication block and 0.72 in the death block (shuffled labels: 0.48-0.51).
       Treatment habits move with it (Trental in the ICU 15% to 35% over the first block).
     - The drifts do not line up across blocks: Trental rises in the first block (15% to 35%) and falls in the death
       block (37% to 2%), so the blocks' positions are not one shared calendar and no time order can be rebuilt.
     - Holding out the last 20% of each block against a random 20% (logistic regression): death AUC 0.77 against
       0.84 (SD 0.02, 30 draws); log loss 0.670 against 0.636 (SD 0.042). Some drift, measured on one cut.
     - Same-day clusters: neighbouring rows are barely more alike than rows 100 apart (21.5% against 22.2% of coded
       fields differ); no two patients share their age and differ in two coded fields or fewer; no duplicates.
   * **Effect on the task:** a random split mixes four years of care; a model used on later patients would meet some
     drift the random split does not test. It cannot be measured on a real time axis here.
   * **Unknown:** the admission dates; the Russian preprint of 1997 (the source's bibliography, item 4) may describe
     how the file was put together.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random (implemented) | random patients, as now | no ordering claim the data cannot back | says nothing about the drift |
     | B | Random, marked forced from temporal | as A, tagged `ForcedIIDFromTemporal`, with a note on the missing dates and the drift | states that real use is on later patients; follows the rule for releases without dates | a tag on a time axis nobody can rebuild |
     | C | Split by row order | contiguous patient numbers as folds | none | the order is by outcome: test folds of only deaths or only survivors |
     | D | Last 20% of each block as test | position inside each block as a stand-in for time | tests the drift found | the blocks are not on one calendar; a time axis of our own invention |

   * **Recommendation:** B. Use at admission is on later patients, so the task is temporal by its use, but the file
     gives no dates and its order is by outcome; the closest regime is random, marked as forced[^2a][^2b].
     **Decision:** random (A), random marked forced from temporal (B), by row order (C) or by position in each block
     (D)?

   **Andrej (2026-11-04, discuss):** I believe this is actually a temporal task or at least some sort of relationships among samples depending on the day should be there

   **Answer (AI, 2026-11-04):**

   * **Question:** is this a temporal task, or are patients of one day linked?
   * **What settles it:** there is no date, and the row order is sorted by outcome (all deaths in the last 274
     rows), so no time order can be rebuilt from the file.
   * **Drift exists, links of one day do not show:** order inside each block predicts its half at AUC 0.58-0.82, but
     the drifts run in opposite directions across blocks; neighbouring rows are as different as distant ones.
   * **Recommendation:** B above, the random split marked as forced from a temporal task, with a note that admission
     dates would allow a real temporal split. **Decision:** A, B, C or D?

   **Notes for the AI:** evidence in the run's evidence folder (`explore_order*.py`, `within.py`,
   `exp3.py`, `exp3.log`). On B: tag `ForcedIIDFromTemporal` on the split, `splits_comment` and a curation note with
   the numbers above, a `CC` line in the record; `dataset check`.

   **Answer (AI, 2026-11-06):** the time framing of this split, from the review of how each dataset's information
   arrives[^2c].

   * Patients arrive one by one over 1992-1995; their inputs are dated at admission by the source, and the outcome
     arrives at death or discharge, after a stay that differs per patient. The record's collection facts say so
     (`Samples: Over Time`, `Time: Lost`, `Target: Varying Delay`), and they hold.
   * The model is used on later patients, and the outcome moves with the care of the period (the drift inside the
     blocks above), while the time is lost. That is the forced case: random, since no patient recurs.
   * B stays the recommendation. B also names a tag; the tag and its `Time basis:` line are now issue 8, so this
     issue decides the split only: random (A or B) or by row order (C or D).

   [^2a]: **SPLIT-7** (Must): a missing timestamp does not make a task IID. **SPLIT-8** (Must): a task temporal by
     its use case whose release cannot give time windows ships in the closest regime, tagged as forced from temporal,
     when a leak test across the split finds none.
   [^2b]: **SPLIT-22** (Should): the raw file order can be the time order without a timestamp; keep it. Here it is
     not: the order follows the outcome.
   [^2c]: **SPLIT-32** (Should): when each sample, feature and target comes into existence is information for the
     split; the record carries the collection facts, and a definition names its use-case prototype or a forced tag.

   **Resolved (2026-11-10, Andrej):** B, random, marked forced from temporal: the split stays random over patients (the
   default split, so no `splits_comment`); the task summary's `split` names the forced split; the drift and leak-test
   numbers above are in the `Time basis:` bullet of issue 8.

   **Note (AI, 2026-11-25):** this issue is the BeyondArena v0.2 review's issue 2 of 2026-11; it was decided there but never written into this record, so it is kept here under its new number.

8. **Time basis: tag the random split as forced from temporal, or call it a stationary relation?**

   * **Problem:**
     - Patients were admitted one by one over 1992-1995 and died or left after a stay of varying length, and the file keeps no date and is sorted by outcome, so the time is lost.
     - The record's collection facts hold (`Samples: Over Time`, `Time: Lost`, `Target: Varying Delay`); the definition splits at random and names no time basis, and issue 7 decides the split itself.
     - Death in hospital follows the care of the period, which drifts inside the blocks, so the five questions give the forced tag rather than a prototype[^3a].
   * **Background:**
     - The five questions: time can affect the outcome (a death after admission, under treatment); the use is on
       later patients, not filling in a past period; the patients share no prediction moment; and the period moves
       the outcome, since care drifts (Trental in the ICU 15% to 35% over the first block) and the last fifth of each
       block scores death ROC AUC 0.77 against 0.84 for a random fifth (issue 7).
     - A stationary relation is a present state (a diagnosis) read through a relation time does not move, and it is
       shown on dated data; death in hospital is a later outcome, and no date exists to show it.
     - The leak test across a random split (issue 7's checks): no duplicates, no recurring patient, no same-day
       clusters (neighbouring rows differ as much as rows 100 apart). The order follows the outcome, which is issue
       1's leak, not one of the split.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | as now | nothing to write | `dataset check` notes a split that is not temporal without a basis; the score's relation to time unstated |
     | B | Forced from temporal | `ForcedIIDFromTemporal` and a `Time basis:` line with the drift and the leak test | says that later patients are the use and the dates are missing; the leak test passes | none found |
     | C | Stationary relation | `StationaryRelation` and a line arguing it | no forced tag | death in hospital is a later outcome that care moves, and the drift inside the blocks argues against it |

   * **Recommendation:** B, while issue 7 keeps a random split. **Decision:** A, B or C?

   **Notes for the AI:** once the time-basis tags are in this working copy, on B: `data_tags = ("ForcedIIDFromTemporal",)` and in
   `curation_comments` the bullet `- Time basis: ForcedIIDFromTemporal: patients admitted one by one in 1992-1995 to
   one hospital, the outcome known at death or discharge; a model at admission is used on later patients. No
   admission date survives and the file is sorted by outcome (survivors, survivors with a complication, deaths), so
   no time order can be rebuilt (Time: Lost). Care drifts inside each block (Trental in the ICU 15% to 35% over the
   first), and the last fifth of each block scores death ROC AUC 0.77 against 0.84 for a random fifth (logistic
   regression). Leak test across the split: no duplicates, no recurring patients, no same-day clusters. Admission
   dates would allow a split by time.`; the `split` sentence names the forced split; `dataset check`. The record's
   facts stay.

   [^3a]: **SPLIT-32** (Should): the five questions; when the samples arrive over time, the period moves the target
     and the time is lost, the split is forced (SPLIT-8) and ships after a leak test; a stationary relation is
     measured on a dated source or argued from a source whose time is lost. **SPLIT-8** (Must): the forced split,
     tagged, after a leak test across the split.

   **Resolved (2026-11-10, Andrej):** B: `data_tags = ("ForcedIIDFromTemporal",)` and the drafted `Time basis:
   ForcedIIDFromTemporal:` bullet in `curation_comments`, with the within-block drift (ROC AUC 0.82, 0.58, 0.72), the
   last-fifth test (0.77 against 0.84) and the leak test. Record facts unchanged.

   **Note (AI, 2026-11-25):** this issue is the BeyondArena v0.2 review's issue 3 of 2026-11; it was decided there but never written into this record, so it is kept here under its new number.

9. **Is there better public data for the same task?**

   * **Problem:**
     - Andrej asked (2026-11-11) whether a better dataset exists for predicting death or complications after a heart attack from admission data.
     - One open dataset is better for death: GUSTO-I, with 24 times the patients, no blank pattern and an explicit permission to use it.
     - No public dataset has mic's multiclass outcome (cause of death and seven complications), and none of the large newer ones is open.
   * **Background:** searched UCI, Kaggle, OpenML, PhysioNet, Dryad, figshare, Mendeley Data, hbiostat.org, R packages
     and data papers on 2026-11-11; the GUSTO-I, WHAS500 and Vellore files were downloaded and counted.

     | Dataset | Patients (events) | Inputs | Outcome | Dates | Access | Better? |
     |---|---|---|---|---|---|---|
     | mic (Krasnoyarsk, 1992-1995) | 1,700 (271 deaths) | 102 at admission | death by cause, 8 classes | none per patient | CC BY 4.0 | - |
     | GUSTO-I trial, 15 countries, 1990-1993 (hbiostat.org/data/repo/gusto.rda; predtools) | 40,830 (2,851 deaths, 7.0%) | 28: age, sex, Killip class, blood pressure, pulse, infarct site, ST leads, history, risk factors, trial arm; region and site group (16 / 48 / 121 levels) | death by day 30 | none per patient | open, "Permission is granted to anyone ... reference the original paper" | yes for death: larger, multinational, no blanks except the arm-defined `tpa`; binary only, as old |
     | MIMIC-IV AMI admissions, Boston, 2008-2019 | about 11,000-12,000 (about 4,700 first ICU stays, 13.6% die) | labs, vitals, drugs from the EHR | in-hospital death | shifted dates | credentialed, no redistribution | no: a cohort to build from a discharge code; record `mimic_iv` is 2nd Tier |
     | eICU-CRD, 208 US hospitals, 2014-2015 | AMI subset not counted | as MIMIC | in-hospital death | relative times | credentialed | no, same as MIMIC |
     | WHAS500, Worcester, 1997/1999/2001 (Hosmer et al.; R smoothHR) | 500 (39 in-hospital deaths) | 13; afib, shock, heart failure and heart block are in-hospital events | in-hospital death; follow-up death | admission and discharge dates | textbook data, licence unstated | no: smaller, the complications are outcomes, not inputs |
     | Vellore NSTEMI, India (Mendeley 10.17632/3gsm2n5knn.1) | 149 (12 in-hospital deaths) | 250 questionnaire items | in-hospital, 1- and 6-month death | none | CC BY 4.0 | no: too small |
     | Alkmaar MI cohort, 2013-2016 (Data in Brief 21:371) | 2,055 (143 death or reinfarction by 6 months) | clinical, 19 admission blood tests, GRACE | 6-month death or reinfarction | - | not released (summary tables only) | not available |
     | Registries: NCDR Chest Pain-MI (313,825), GWTG-CAD, KAMIR (22,875), China AMI | large | rich | in-hospital death | yes | application, no redistribution | not available |

   * **Effect on the task:** GUSTO-I answers the death part of mic's task on clean, larger data; the complications and
     causes of death exist only in mic. GUSTO-I is screened already as its own record (`gusto_i_mi_mortality`, `TBD -> Yes`, priority 3)[^4a];
     hbiostat.org gives it the documented release its record lacked (predtools says only "Internet"). Unknown: whether
     its few strong predictors leave a spread between methods (the paper: about 90% of the information in five inputs).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nothing more (implemented) | candidates listed here; mic stays as issue 6 decides | no work | the better death data stays unbuilt |
     | B | Build GUSTO-I as well | `gusto_i_mi_mortality` goes to /add-dataset from the hbiostat file, independent of mic | 40,830 patients, real admission death task, grouped split by site possible | binary only; one more MI death task if mic is kept |
     | C | Build GUSTO-I as mic's replacement | as B, and retire mic in issue 6 | one clean MI task instead of a leaky small one | loses the complications and causes of death |

   * **Recommendation:** B, whatever issue 6 decides; it becomes C if issue 6 retires mic. **Decision:** nothing more
     (A), build GUSTO-I as well (B) or as mic's replacement (C)?

   **Notes for the AI:** files and counts in the run's evidence folder (`gusto_dl/gusto.rda`,
   `whas_dl/whas500.rda`, `mend_dl/Dataset.xls`). On B or C: move `gusto_i_mi_mortality` to `Yes` with a CC line,
   add `https://hbiostat.org/data/repo/gusto.rda` and the hbiostat permission text to its record (PROV), then
   /add-dataset; the `tpa` blanks are the SK+tPA arm (10,320), 4 duplicate rows. On C also issue 6's retirement.
   Sources: https://hbiostat.org/data (terms), Lee et al. 1995 https://doi.org/10.1161/01.cir.91.6.1659,
   https://physionet.org/content/mimiciv/, https://data.mendeley.com/datasets/3gsm2n5knn,
   https://doi.org/10.1016/j.dib.2018.09.126, https://doi.org/10.1161/CIRCOUTCOMES.124.011259.

   [^4a]: **PROV-4** (Must): a dataset enters once; two records are duplicates only when they end at the same
     original source, so GUSTO-I is its own record, and mic keeps the verdict its own data earns.

   **Deferred (2026-11-11):** parked on Andrej's note ("Park this until we decide whether we use another dataset for this task").

   **Note (AI, 2026-11-25):** the question moved to issue 5 of this review, which restates it with the candidates checked on their files on 2026-11-25; this issue stays parked and that one carries the decision.

## Reference

Trajectories, bifurcations, and pseudo-time in large clinical datasets: applications to myocardial infarction and diabetes data
By S. E. Golovenkin, Jonathan Bac, A. Chervov, E. M. Mirkes, Y. Orlova, E. Barillot, A. Gorban, A. Zinovyev. 2020

Published in GigaScience
