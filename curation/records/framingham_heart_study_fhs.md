---
unique_name: framingham_heart_study_fhs
name: Framingham Heart Study (FHS)
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
tags:
- New IID
- 'Samples: One Moment'
- 'Target: Later'
- Clinical Study
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2004'
collection_period: 1956-1980
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/christofel04/cardiovascular-study-dataset-predict-heart-disea/data
- https://www.kaggle.com/datasets/aasheesh200/framingham-heart-study-dataset
- https://www.framinghamheartstudy.org/fhs-for-researchers/data-available-overview/
- https://www.nhlbi.nih.gov/science/framingham-heart-study-fhs
- https://www.framinghamheartstudy.org/fhs-risk-functions/hard-coronary-heart-disease-10-year-risk/
v2_path: datasets/_dev/tabarena-v0pt2/framingham_heart_study_fhs/dataset.py
source_row: 667
type_adapter_id: curation-record-v1
---

## Comments

Likely use data from Kaggle

A bit hard to parse what the origin is and where the Kaggle data was downloaded from, but we can use it

**Assessment (AI, 2026-10-07):** All three Kaggle uploads are `framingham.csv` from MIT's 15.071 The Analytics Edge (OCW Spring 2017; aasheesh200 is byte-identical). Its 4,240 rows are the baseline exam (period 1, PREVCHD = 0) of the NHLBI BioLINCC Framingham teaching dataset; all 15 features match row for row. MIT's `TenYearCHD` equals TIMECHD < 10 years in all 4,240 rows, but TIMECHD is the censor date for participants without an event (documentation, p. 4). So 265 of its 644 positives had no CHD: 249 died of other causes and 16 were lost to follow-up. The v2 definition reads the teaching data (CRAN riskCommunicator) and rebuilds the label: 4,224 participants, 379 with CHD. BioLINCC calls teaching data "completely unsuitable for publication purposes".

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case +, source +, shape +, risk - (Issue 3: teaching data perturbed by undocumented anonymisation, unsuitable for publication per BioLINCC). Classic CHD risk task with the label rebuilt (41% of the Kaggle positives were wrong), but it rests on anonymised teaching data.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes, with the anonymised teaching data recorded as a PROV-3 case and the rebuilt label as a PROV-13 repair (curator's calls); the endpoint (ANYCHD or hard CHD) stays a weighing call. Applied: the row names the first exam of about 1956, the use case a patient's first assessment, `known` the missing HDL, `fit_reason` the pre-statin era and what the anonymisation check shows (no added noise; permutation untestable), the endpoint's reason the FHS 10-year CHD risk page instead of MIT's course, plus notes on the terms, relatives and cigsPerDay heaping. Priority 3: gap - (no thin domain, problem type or regime), use case + (the classic FHS risk score, fit direct), source + (BioLINCC documentation), shape + (4,224 participants, 15 features), risk - (anonymisation by undocumented methods that cannot be fully tested, PROV-3).

CC (2026-10-21, Lennart): agree to amend PROV-3 (values the owner perturbed for privacy, with no measurable damage, are kept with a note of what was checked; this dataset is its case), but also add a note about selection bias in the curation record here. Agree to amend PROV-14: the rebuilt label is a repair and stays under this record.

**Assessment (AI, 2026-10-21):** selection bias of the teaching subset. BioLINCC's documentation (2021a, p. 1) calls the file "a subset of the data collected as part of the Framingham study" on 4,434 participants, of the 5,209 enrolled in 1948; NHLBI's teaching page (2005) says "a large subset of the original Framingham cohort participants". How the 4,434 were chosen is not documented. Period 1 is about 1956, some eight years after enrolment, so people who died or left before that exam are likely missing (a survivor selection), and Nahhas (App. A.6) names "random visit selection" among the anonymisation methods. The task therefore stands for this subset of a 1948 town cohort, not for the whole cohort; no test on the file can measure the selection. Noted in the definition's notes (Selection bullet) and in Review issue 3.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: male, currentSmoker, BPMeds, prevalentStroke, prevalentHyp, diabetes.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — the teaching dataset defines no task or metric; the 10-year risk context points to the C statistic, which equals roc_auc here.

CC (2026-10-21, Lennart): SelectArena's copy (`datasets/_dev/feature_selection/framingham_heart_study/`) builds from the Kaggle file with MIT's `TenYearCHD` (265 of its 644 positives had no CHD event within 10 years) and sets the domain "physics & astronomy"; left as is: "We dont care about the select arena copy, ignore it".

CC (2026-10-22, Lennart): issue 2: participants who died of other causes within 10 years stay No. Issues 3 and 7: as the amended PROV-3 and PROV-14 say (kept, a repair under this record). Issue 8: `education` is a categorical code and is encoded as such (its labels). Issue 9: keep one row per participant, with a note that every exam could make a grouped task in the future. Record field `year` takes the definition's value (2004). Issue 1 asked: is MI_FCHD closer to the real task?

**Assessment (AI, 2026-10-22):** applied issues 2, 3, 7, 8, 9: `education` mapped to its four labels as a category; the grouped-variant note added; LEAK-22 now names a competing death after the prediction point as no excluded row (this case). The outcome question answered: hard ASCVD (MI_FCHD or stroke, 301 Yes, logistic regression ROC AUC 0.795) is the outcome of today's treatment thresholds, hard CHD (191 Yes, 0.785) that of ATP III, ANYCHD (379 Yes, 0.743) that of the classic FHS score. dataset check: 0 errors, 0 warnings. Not built yet.

CC (2026-10-22, Lennart): issue 1: (a), hard ASCVD within 10 years, as it matches real-world use now.

**Assessment (AI, 2026-10-22):** target `ascvd_within_10_years`: a first hospitalised myocardial infarction or CHD death, or a stroke, within 10 years (the pooled cohort equations' outcome). The 25 participants with a prior stroke are excluded, as the pooled cohort equations exclude prior ASCVD (all 25 carry STROKE = 1 at day 0, so kept they would be Yes by definition); `prevalentStroke` is then constant and dropped. 4,199 rows and 14 features, 276 Yes (6.6%; 92 per test fold), 218 competing deaths stay No. Logistic regression ROC AUC 0.779 (0.739 for any CHD); task probe linear 0.779, random forest 0.763, LightGBM 0.722, no flags; leak probe clean. dataset check: 0 errors, 0 warnings. REVIEW.md removed (nothing left open). Not built yet.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `education` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_cvd_mortality` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-16, Andrej): time basis `ForcedIIDFromTemporal` instead of `DelayedTarget`, which was dropped before it shipped:
- A shared scoring date with a target window closed for every row makes the random split valid within that date only; one date is one period, too few for three windows, so the split is forced (SPLIT-8).
- The random split stays.

CC (2026-11-18, Andrej): time basis stays `ForcedIIDFromTemporal` (Review issue 2, A, after measuring): the stationary-relation test on the teaching file's three exams reads not flat (ROC AUC -0.032 ± 0.008 on exam 3, -0.015 ± 0.005 on exam 2, trained on earlier exams only); the `Time basis:` line gives it. The full Original Cohort is not used (access by data use agreement only).

CC (2026-11-20, Andrej): random folds over participants stay, a written departure from the measured-not-flat rule (Review issue 3, A): the shipped task holds one exam, so no later period can be held out; with ages matched the shift remains for LightGBM (-0.040 ROC AUC on exam 3) and vanishes for Kumo-Tabular.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below (issues 2 and 3).

**Main points:** Measured on the teaching file's exams: not flat, so `ForcedIIDFromTemporal` stays (issue 2, A,
2026-11-18); the random folds over participants stay as a written departure from the measured-not-flat rule (issue
3, A, 2026-11-20). Nothing is left open.

**Issues for Andrej:**

2. **Measure the relation on the dated periods a parent source holds, before deciding the tag?**

   * **Problem:**
     - Time: The shipped rows are one moment (period 1, ~1956), but the parent BioLINCC teaching file holds three exam periods (~1956, ~1962, ~1968) with TIME and 24-year follow-up, so later exams of event-free participants with 10 years left are a dated comparison.
     - Use: A physician estimates 10-year hard ASCVD risk at a patient's first assessment today, ~70 years after the baseline exam.
     - Mechanism: Classic risk factors to ASCVD: the biology is stable but absolute risk given them fell with statins, antihypertensives and less smoking; Framingham overpredicts in later populations.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | Brindle P et al., 'Predictive accuracy of the Framingham coronary risk score in British men', BMJ 2003;327:1267 (literature, cited from memory: check) | Framingham-predicted vs observed 10-year CHD | not flat: overestimates risk by about half | same score, later population |
     | Davis SE et al., 'Calibration drift in regression and machine learning models for acute kidney injury', JAMIA 2017;24(6):1052-1061 (literature, cited from memory: check) | VA hospital models over 9 years | discrimination stable, calibration drifted | routine-lab clinical risk model used years after fitting |

   * **For a stationary use case:**
     - risk-factor biology and ranking (discrimination) transfers well across cohorts.
   * **Against:**
     - ~70-year span to use.
     - changed treatments (statins, BP drugs) and smoking.
     - calibration drift documented in the literature.
     - a parent holds later periods, so it must be measured, not assumed.
   * **Earlier views:**
     - CC 2026-11-16 (Andrej): ForcedIIDFromTemporal instead of DelayedTarget; one date is one period.
     - Time basis line: 'possible variant (Lennart, 2026-10-22)': every event-free exam of periods 1-3.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | ~70-year span to use; changed treatments (statins, BP drugs) and smoking |
     | C | Measure first | The shipped rows are one moment (period 1, ~1956), but the parent BioLINCC teaching file holds three exam periods (~1956, ~1962, ~1968) with TIME and 24-year follow-up, so later exams of event-free participants with 10 years left are a dated comparison. | The rule asks for a measurement where time exists | Takes a cluster run |

   * **Recommendation:** C, the parent's exams 2 and 3 are dated periods: test period-1-trained models on period-2/3 event-free exams (10-year hard ASCVD) against contemporaneous models; even flat, the 12-year span does not reach today's use, so expect the forced tag to stay. Confidence: medium. **Decision:** A, B or C?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, change):** Option C: Measure first.

   **Answer (AI, 2026-11-18):** measurement requested; the tag stays until its verdict. The BioLINCC teaching file's three exam periods (about 1956, 1962, 1968) are the periods to test.

   **Answer (AI, 2026-11-18):** measured: not flat, so the forced tag stays and no stationary tag is open.

   - The test rebuilt the definition's cohort and 10-year hard-ASCVD label at each exam of the teaching file
     (participants free of CHD and stroke at that exam, event days counted from it, those lost within 10 years
     dropped), the same 14 features, a participant held out across exams, ROC AUC.
   - Trained only on earlier exams, the model scores worse on exam 3 (LightGBM) and exam 2 (Kumo-Tabular) than one
     that also saw half of that exam, beyond two SD and the floor.
   - The exams are also the cohort's age (the same people six and twelve years older), so the drift may be the
     older cohort rather than the calendar; either way later patients are not interchangeable with these.

     | Exam | Rows | Hard ASCVD | LightGBM gap ± SD | Kumo-Tabular gap ± SD | Floor | Verdict |
     |---|---|---|---|---|---|---|
     | 1 (about 1956) | 4,199 | 6.6% | training only | training only | | |
     | 2 (about 1962) | 3,592 | 8.7% | +0.014 ± 0.013 | +0.015 ± 0.005 | 0.002 | not flat (Kumo-Tabular) |
     | 3 (about 1968) | 2,851 | 11.4% | +0.032 ± 0.008 | +0.002 ± 0.007 | 0.002 | not flat (LightGBM) |

   The shipped rows are exam 1 only, one moment, so no period can be held out: `ForcedIIDFromTemporal` stays, and the
   `Time basis:` line can name the measurement. **Decision:** keep the forced tag with that line?

   **Andrej (2026-11-18, discuss):** You mentioned a 70-year span to use. Is it possible to get a larger version of
   this dataset covering the full 70 years?

   **Answer (AI, 2026-11-18):** yes, but only under a data use agreement, not as an open download.

   - NHLBI's BioLINCC holds the full Original Cohort (5,209 people enrolled 1948-1952): the first 32 exams and event
     follow-up through 2018; dbGaP holds it as phs000007. Access is free but needs an approved application (research
     plan, institutional sign-off, a data use agreement).
   - The teaching file we ship is the open, anonymised subset: 3 exams (about 1956, 1962, 1968) and 24 years of
     follow-up, which NHLBI allows to be redistributed.
   - The full cohort could test drift across seven decades (treatments, smoking, diagnostic criteria), but its terms
     bar redistribution, so it could not become the shipped dataset; it could at most back a measurement, run by
     someone with approved access.

   **Andrej (2026-11-18, discuss):** Did someone else maybe upload the data somewhere?

   **Answer (AI, 2026-11-18):** not that I could find, and a copy would not be usable.

   - The public copies (Kaggle's Framingham set, the R package riskCommunicator, R4HCR) are all the teaching subset we
     already ship: 4,434 participants, 3 exams, 24 years of follow-up.
   - No copy of the full Original Cohort (32 exams, follow-up to 2018) turned up on GitHub, Kaggle or data portals.
   - Its terms bar redistribution, so a copy someone uploaded would breach the data use agreement; we could not build
     on it or cite it.
   - The full cohort is reachable only by an approved BioLINCC or dbGaP request; the teaching file's documentation
     also says it was altered for confidentiality.

   **Andrej (2026-11-18, discuss):** Agree.

   **Answer (AI, 2026-11-18):** noted: no full-cohort copy is used. What stays to decide is the tag: keep
   `ForcedIIDFromTemporal` and add the measured result (not flat across exams 1-3) to its `Time basis:` line, as
   recommended. **Decision:** ok to keep the forced tag with that line?

   **Andrej (2026-11-18, discuss):** Agree.

   **Resolved (2026-11-18, Andrej):** A: `ForcedIIDFromTemporal` stays; its `Time basis:` line now ends with "Not taken
   as stationary (Andrej, 2026-11-18)" and the measurement (not flat across the teaching file's exams 1-3: ROC AUC
   -0.032 ± 0.008 on exam 3, -0.015 ± 0.005 on exam 2, floors 0.002; the exams are also the cohort's age). Split and
   data unchanged; no full-cohort copy is used.

3. **Random folds after a measured not-flat relation, which SPLIT-16 rules out?**

   * **Problem:**
     - The stationary-relation test on the parent file's three exams reads not flat (LightGBM on exam 3, Kumo-Tabular on exam 2), and you kept `ForcedIIDFromTemporal` on 2026-11-18.
     - Under the forced step as amended the same day, "measured not flat" leads only to whole periods or `Too Small` (SPLIT-16: no unit or random fallback); the shipped definition holds one exam, so no periods can be built.
     - The record's CC does not name this departure.
   * **Numbers:** stationary-relation test v3, ROC AUC gap of the forward model (trained on earlier exams only), mean ± SD over seeds.

     | Exam tested | LightGBM | Kumo-Tabular | Verdict |
     |---|---|---|---|
     | exam 3 (about 1968) | +0.032 ± 0.008 (floor 0.002), not flat | +0.002 ± 0.007, flat | not flat |
     | exam 2 (about 1962) | +0.014 ± 0.013, inconclusive | +0.015 ± 0.005 (floor 0.002), not flat | not flat |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random folds, `ForcedIIDFromTemporal` (implemented) | The departure from SPLIT-16 is written in the `splits_comment` and the CC | No change to the benchmark | A split the rule rules out for a relation that moves |
     | B | `Too Small` | Retired, or kept only on your call as SPLIT-16 allows | What the rule says | Loses a well-known clinical cohort |

   * **Recommendation:** A with the written departure: the shift was measured on the parent teaching file across exams, not on the one-exam cohort the definition ships, and SPLIT-16 leaves keeping it to your call. **Decision:** A or B?

   **Andrej (2026-11-19, discuss):** Rethink the options.

   **Answer (AI, 2026-11-19):** rethought, with one new measurement: the test compared exams of the same participants, so "later" also meant "six years older"; weighted to the same age mix, the stronger model's gap disappears, LightGBM's stays.

   * **Age-matched rerun:** each exam weighted to the tested exam's age distribution (two-year bands, ages outside it left out); ROC AUC gap of the model trained on earlier exams only, mean ± SD over 5 seeds.

     | Exam tested | Model | Gap, as before | Gap, age-matched | Floor | Verdict, age-matched |
     |---|---|---|---|---|---|
     | exam 3 | LightGBM (ROC AUC 0.65-0.71) | +0.032 ± 0.008 | +0.040 ± 0.009 | 0.002 | not flat |
     | exam 3 | Kumo-Tabular (0.73-0.74) | +0.002 ± 0.007 | +0.007 ± 0.004 | 0.002 | flat |
     | exam 2 | LightGBM | +0.014 ± 0.013 | +0.043 ± 0.023 | 0.002 | inconclusive |
     | exam 2 | Kumo-Tabular | +0.015 ± 0.005 | +0.013 ± 0.011 | 0.002 | flat |

   * **What it shows:** ageing explains Kumo-Tabular's exam-2 gap; LightGBM's exam-3 gap is not ageing. Read by the rule, one model not flat in one exam keeps the verdict not flat.
   * **What the test measures:** the parent teaching file, the same cohort followed to later exams (about 1962 and 1968), not a later cohort; the shipped task scores one exam (about 1956). The rule counts a parent source's periods, so the measurement applies.
   * **The options, rethought:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random folds, `ForcedIIDFromTemporal` (implemented, your call of 2026-11-18) | The departure from the measured-not-flat rule written in `splits_comment` and the CC | A well-known cohort stays; the stronger model reads flat once age is matched | A split the rule rules out after a not-flat measurement |
     | B | `Too Small` | Retired; one cohort at one exam cannot hold periods out | What the rule gives | Loses the dataset |
     | C | A task on the teaching file's three exams | Exams as periods, participants grouped | Tests later exams | Three periods are under the four that 3 repeats need: `Too Small` again |
     | D | Retire as a forced split too risky (`Not Representative`), your call | Retired on a domain reason: risk scores fitted on one era miscalibrate in later ones | Names the reason | Same loss as B, on judgement rather than the test |

   * **Recommendation:** A, with the age-matched numbers in the departure: the remaining gap is one model family's, and the shipped cohort has no later period to test. **Decision:** A, B or D (C only as a new task)?

   **Andrej (2026-11-19, discuss):** Can we do a grouped split on exams?

   **Answer (AI, 2026-11-19):** not without the same people on both sides: the exams are visits of one cohort, so holding an exam out leaves its participants' other visits in training, and removing them leaves almost nothing.

   | Exam held out | Participants | Also seen at another exam | Training rows from the other exams | Without the test exam's participants |
   |---|---|---|---|---|
   | exam 1 (about 1956) | 4,215 | 3,647 | 6,453 | 0 |
   | exam 2 (about 1962) | 3,599 | 3,599 | 7,069 | 664 |
   | exam 3 (about 1968) | 2,854 | 2,854 | 7,814 | 2,154 |

   (Participants free of heart disease and stroke at the exam, in the teaching file, before the 10-year outcome filter.)

   * With the shared participants left in, a test participant's earlier or later visit is in training: entity leakage, which the forced step rules out for groups; and three exams are under the four periods 3 repeats need.
   * The shipped task scores one exam (exam 1); a split on exams needs the task rebuilt on all three exams (option C of the earlier answer).

   **Recommendation:** unchanged, A (keep, with the departure and the age-matched numbers written). **Decision:** A, B or D?

   **Andrej (2026-11-20, discuss):** Can we do a grouped split on participants?

   **Answer (AI, 2026-11-20):** the shipped split already is one: the task holds one row per participant (the exam-1 cohort with its 10-year outcome), so random folds over rows hold every participant out whole, and grouping by participant would give the same folds.

   * Grouping by participant matters only in a task that stacks a participant's exams (option C: the three exams as rows); there it keeps a participant's visits on one side, but the exams then still sit on both sides, so it would not test a later exam or cohort, which the test found shifts.
   * So a participant-grouped split does not change the issue: the choice stays A (keep, with the written departure and the age-matched numbers), B (`Too Small`) or D (retire as too risky).

   **Recommendation:** A. **Decision:** A, B or D?

   **Andrej (2026-11-20, discuss):** I don't get it. List all options again with the train and test sizes and split types

   **Answer (AI, 2026-11-20):** the shipped task is one exam per participant (4,199 people at the baseline exam, about 1956, each with their 10-year outcome). The question is only how to split those, or whether to rebuild the task on later exams too.

   | | Option | Task rows | Split type | Splits | Train | Test | Tag |
   |---|---|---|---|---|---|---|---|
   | A | Keep (implemented) | 4,199, one per participant | random 3 x 3 folds (each participant on one side) | 9 | 2,799-2,800 (66.7%) | 1,399-1,400 | `ForcedIIDFromTemporal`, the departure written |
   | B | Retire as `Too Small` | | | | | | |
   | C1 | Rebuild on all three exams, grouped by participant | about 10,650 (exam 1 4,199, exam 2 about 3,600, exam 3 about 2,850) | grouped 3 x 3 folds over 4,215 participants | 9 | about 7,100 (66.7%) | about 3,550 | `ForcedGroupedFromTemporal` |
   | C2 | Rebuild on all three exams, hold out the newest exam | about 10,650 | one window: exams 1-2 train, exam 3 test | 1 | about 7,800 (73%), or 2,154 without exam-3 participants | about 2,850 | temporal |
   | D | Retire as too risky (your call) | | | | | | `Not Representative` |

   * **What each tests:** A and C1 test new people examined in the same years; neither tests a later period, which the stationarity test says differs (LightGBM loses 0.032-0.040 ROC AUC on exam 3 when trained on earlier exams, also after age matching; Kumo-Tabular is flat after age matching). C2 is the only one that tests a later exam, but it is one window (three are the minimum), and its training holds the test participants' own earlier visits unless they are removed (then 2,154 rows).
   * **Why the rules flag A:** a relation measured not flat may not be split at random; it needs whole periods held out (four for 3 repeats) or windows. With one baseline exam, neither exists, so the rules give B; keeping A is a written departure.

   **Recommendation:** A, with the departure and the age-matched numbers written: the remaining shift is one model family's, the shipped cohort has no later period to test, and C1/C2 would build a different task. **Decision:** A, B, C1, C2 or D?

   **Andrej (2026-11-20, discuss):** Test whether C1 would be a stationary relation. This might be a similar case as with the horce colic dataset, where there is a temporal component that vanishs once we group the repeating entities.

   **Answer (AI, 2026-11-20):** the test already ran in C1's setting, with the repeating participants grouped, and the temporal component does not vanish for LightGBM: unlike horse_colic, the relation reads not flat with participants held out whole.

   * **How the test treats participants:** in every comparison the test half's participants leave every training side (`units` = the participant id), so a model trained on earlier exams never sees a test participant's earlier visit; this is the grouping C1 uses.
   * **Results** (ROC AUC gap of a model trained on earlier exams against one trained on the tested exam, participants held out whole, 5 seeds):

     | Exam tested | Model | Gap | Age-matched gap | Floor | Verdict (age-matched) |
     |---|---|---|---|---|---|
     | exam 3 | LightGBM | +0.032 ± 0.008 | +0.040 ± 0.009 | 0.002 | not flat |
     | exam 3 | Kumo-Tabular | +0.002 ± 0.007 | +0.007 ± 0.004 | 0.002 | flat |
     | exam 2 | LightGBM | +0.014 ± 0.013 | +0.043 ± 0.023 | 0.002 | inconclusive |
     | exam 2 | Kumo-Tabular | +0.015 ± 0.005 | +0.013 ± 0.011 | 0.002 | flat |

   * **Compared with horse_colic:** there, with cases grouped, the pooled test reads flat for Kumo-Tabular and no run is not flat; here, LightGBM on exam 3 stays clearly not flat (+0.040, twenty floors), so by the rule one model not flat keeps the verdict not flat. Kumo-Tabular reads flat once age is matched, so the shift is partly the cohort's ageing, but not all of it for LightGBM.
   * **What it means for C1:** C1 (all three exams, grouped by participant, random folds) would hold later and earlier exams on both sides of each fold, a relation that moves between exams for one model family; the rules give it no random-over-periods split.

   **Recommendation:** A, unchanged. **Decision:** A, B, C1, C2 or D?

   **Andrej (2026-11-20, ok):** As implemented (A).

   **Resolved (2026-11-20, Andrej):** A: the 3 x 3 random folds over the 4,199 participants stay, `ForcedIIDFromTemporal`; the `Time basis:` line now names the departure from the rule that a relation measured not flat is never split at random, with the age-matched numbers (LightGBM -0.040 on exam 3, Kumo-Tabular flat) and the reason: one exam, no later period to hold out. Not rebuilt.

## Reference

https://www.nhlbi.nih.gov/sites/default/files/media/docs/risk-assessment.pdf
