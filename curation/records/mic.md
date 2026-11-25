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

**Main points:** Better-data check (2026-11-25, issue 5): Add GUSTO-I (gusto_i_mi_mortality) next to mic and let v0.2-page issue 1 decide mic on its own data: GUSTO-I is the clean, 24-times-larger death task, but it does not separate methods (LightGBM 0.826 against logistic regression 0.826 ROC AUC, splines best on 15 of 15 folds), so it cannot stand in for mic's multiclass task. Earlier: `ForcedIIDFromTemporal` stays (issue 1, A, 2026-11-18). Nothing is left open.

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
     - mic still carries the parked blank-history leak (v0.2-page issue 1: 60 patients with a blank history, 54 dead; blanks alone predict death at 0.78, and still at 0.74 after dropping the 60), and it is the only open data with causes of death and complications.
     - Keep mic alone (A), add GUSTO-I next to it (B), replace mic by GUSTO-I (C), or retire mic with no replacement (D)?
   * **Background:** "v0.2-page issue N" is the issue's number on the BeyondArena v0.2 review page; those parked issues were never written into this record, whose own issue numbers differ. mic in v0.2: 1,699 patients of one Krasnoyarsk hospital (1992-1995), 102 admission inputs, 8-class lethal outcome (271 deaths), log loss, random split tagged forced from temporal (v0.2-page issues 2 and 3, settled). v0.2-page issue 1 is parked: the AI answers of 2026-11-04 to 11-10 found the blanks follow the block a patient was filed in (deaths filed together); filling was withdrawn on Andrej's note, and the last answer (2026-11-10) recommended retiring mic, with keeping the 35 near-complete columns as the fallback. v0.2-page issue 4 (2026-11-11) searched the candidates and recommended B; its table stands and is shortened here:

     | Dataset | Patients (deaths) | Inputs | Outcome | Split it allows | Access | Concerns | Verdict |
     |---|---|---|---|---|---|---|---|
     | mic (Krasnoyarsk, 1992-1995) | 1,700 (271) | 102 at admission | death by cause, 8 classes | random, forced from temporal | CC BY 4.0 | blank-history leak (v0.2-page issue 1); small | - |
     | GUSTO-I trial, 15 countries, 1990-1993 (hbiostat.org/data/repo/gusto.rda) (checked) | 40,830 (2,851, 7.0%) | 28: age, sex, Killip class, blood pressure, pulse, infarct site, ST leads, history, risk factors, height, weight, trial arm, region | death by day 30, binary | random, or grouped by region or site group (16 / 48 / 121 levels) | open, "Permission is granted to anyone ... reference the original paper" | no method spread (below); trial cohort of the thrombolysis era; 4 duplicate rows; `tpa` blank by arm (redundant with `tx`) | better data for death; not a replacement for the task |
     | MIMIC-IV / eICU AMI cohorts | about 4,700-12,000 | EHR | in-hospital death | dated | credentialed, no redistribution | a cohort to build | not available |
     | WHAS500, Vellore NSTEMI, Alkmaar, registries | 149-313,825 | - | death | - | small, unreleased or on application | - | not better or not available |

   * **Effect on the task:** GUSTO-I answers only the death part of mic's task, on clean and larger data; the eight classes (cause of death and complications) exist only in mic. On GUSTO-I a few strong, smooth predictors carry most of the information (Lee et al.: about 90% in five), so a well-specified regression is the reference and flexible models gain nothing; a benchmark entry there rewards calibration and smoothness, not interactions. How v0.2-page issue 1 bears on each option: A and B keep mic, so v0.2-page issue 1 must still be settled, and every variant tested so far either leaves a blank signal (drop the 60: 0.74) or removes the ECG, blood tests and blood pressures (35 columns: no blanks, death AUC 0.75-0.80); B adds a death task that has no such leak next to it. C and D retire mic, which closes v0.2-page issue 1 as retired (the recommendation of 2026-11-10); C then keeps a myocardial-infarction death task in the benchmark, D does not.
   * **Experiments:** 2026-11-25, Slurm. GUSTO-I: `gusto.rda` from hbiostat.org (downloaded 2026-11-11), read with pyreadr; inputs without `day30`, `tpa` and the site-group ids; 5-fold x 3 repeats, random and grouped by site group (`grps`, 121 groups); logistic regression (one-hot categories, standardised numbers, optionally cubic splines with 4 knots), LightGBM defaults. mic: the 1,700 patients of the source file, v0.2-page issue 1's variants, the same folds as in v0.2-page issue 1 (5-fold x 3); logistic regression with missing indicators, LightGBM defaults.

     GUSTO-I, death by day 30:

     | Model | ROC AUC, random | Log loss, random | ROC AUC, grouped by site | Log loss, grouped | Folds better than LR, all (AUC; log loss) |
     |---|---|---|---|---|---|
     | LR, five predictors (age, systolic BP, pulse, Killip, location) | 0.810 | 0.2059 | 0.810 | 0.2060 | 0 of 15; 0 of 15 |
     | LR, five predictors, splines | 0.817 | 0.2036 | 0.817 | 0.2037 | 0 of 15; 0 of 15 |
     | LR, all features | 0.826 | 0.1996 | 0.826 | 0.1997 | - |
     | LR, all features, splines | 0.830 | 0.1985 | 0.830 | 0.1985 | 15 of 15; 13-14 of 15 |
     | LightGBM, five predictors | 0.810 | 0.2072 | 0.810 | 0.2074 | 0 of 15; 0 of 15 |
     | LightGBM, all features | 0.827 | 0.2010 | 0.826 | 0.2011 | 5-9 of 15; 3-4 of 15 |

     mic under v0.2-page issue 1's variants (death ROC AUC from a binary model; 8-class log loss):

     | Variant | Patients (deaths) | Inputs | Death AUC, LR | Death AUC, LightGBM | Log loss, LR | Log loss, LightGBM |
     |---|---|---|---|---|---|---|
     | as shipped | 1,700 (271) | 101 | 0.893 | 0.912 | 0.603 | 1.017 |
     | drop the 60 | 1,640 (217) | 101 | 0.873 | 0.895 | 0.567 | 0.955 |
     | 35 near-complete columns, 78 patients dropped | 1,622 (248) | 35 | 0.800 | 0.760 | 0.589 | 1.083 |

     Untuned LightGBM overfits mic's 8-class log loss (about 1.0 against 0.6); the benchmark's tuned models do not, so mic's spread is read on death AUC: gradient boosting leads by 0.02 with the blanks or without the 60, and trails by 0.04 once no blank is left.
   * **Consistency:** the batch's pattern: a better dataset from another source is its own record, and the old one keeps the verdict its own data earn[^better]; here as for website_phishing, the old dataset carries its own parked problem (v0.2-page issue 1), decided apart from the new record. A task where a simple model is the answer is not by itself a reason to turn it down: the Cleveland heart-disease dataset is disputed because an untrained 6-point score comes close to a logistic regression and the best model; on GUSTO-I the five predictors stay 0.02 below the full model.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep mic alone (implemented) | no new record built; mic as v0.2-page issue 1 decides | no work; keeps the only open multiclass outcome after a heart attack | the clean death data stays unbuilt; v0.2-page issue 1's leak is the task's only check on death |
     | B | Add GUSTO-I next to mic | build gusto_i_mi_mortality (binary, ROC AUC or log loss, split by region or random); mic stays as v0.2-page issue 1 decides | 40,830 patients, no blank pattern, open permission; grouped split by region costs nothing; a leak-free check on mic's death signal | no method spread (LR = LightGBM; splines best); thrombolysis era; v0.2-page issue 1 still to settle |
     | C | Replace mic by GUSTO-I | as B, and v0.2-page issue 1 closes with mic retired | one clean heart-attack task instead of a small leaky one | loses the causes of death and complications; trades a task that separates methods (0.02 on death AUC) for one that does not |
     | D | Retire mic, no replacement | v0.2-page issue 1 closes with mic retired, GUSTO-I not built | nothing to build | no heart-attack task left in the benchmark |

   * **Recommendation:** B: the 2026-11-11 recommendation holds; GUSTO-I is the clean, large death task and its lack of spread is the domain's (a few smooth predictors), not a defect, while mic keeps the multiclass outcome it alone has; whether mic stays is v0.2-page issue 1's decision, not this one's. C if v0.2-page issue 1 retires mic and one heart-attack task is enough. **Decision:** A, B, C or D?

   **Notes for the AI:** on B or C: move gusto_i_mi_mortality to Yes with a CC (<date>, Andrej): line and Andrej in checked_by; add https://hbiostat.org/data/repo/gusto.rda and the hbiostat permission text (https://hbiostat.org/data) to source_links and the record; /add-dataset from that file: target `day30`; drop `tpa` (blank for the SK+tPA arm, redundant with `tx`) and keep `tx` (randomised, known at admission); `sho`, `hig`, `dia`, `hyp`, `hrt`, `ttr` are derived flags of the paper's model (check against Lee et al. before keeping them next to their sources); 4 duplicate rows; split random or grouped by `regl` (16 regions; site group `grps` gave the same scores); note 40,830 of 41,021 enrolled; tags Samples: Over Time, Time: Lost, Clinical Study; the thrombolysis-era cohort as an Outdated question for the reviewer. On C also retire mic through v0.2-page issue 1 (record No (Retired), Class-dependent Recording, CC line, folder removed, CHANGELOG). On D, v0.2-page issue 1's retirement only. On A, nothing here. Evidence: ~/claude_jobs/better_data_1125/work/mic/ (scripts/gusto_spread.py, scripts/mic_spread.py, spread_1411436.log, mic_spread.out, gusto.csv read from dl_gusto/gusto.rda); earlier: ~/claude_jobs/marks_1111/mic/alt/, ~/claude_jobs/marks_1110/mic/. Sources: Lee et al. 1995 https://doi.org/10.1161/01.cir.91.6.1659.

   [^better]: Selection pattern "Small or dated, and the task is still done today" with PROV-4 (Must): a better dataset from another source is its own record, not a duplicate, and the old one keeps the verdict its own data earn until the curator decides.

## Reference

Trajectories, bifurcations, and pseudo-time in large clinical datasets: applications to myocardial infarction and diabetes data
By S. E. Golovenkin, Jonathan Bac, A. Chervov, E. M. Mirkes, Y. Orlova, E. Barillot, A. Gorban, A. Zinovyev. 2020

Published in GigaScience
