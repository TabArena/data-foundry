---
unique_name: wids_diabetes_mellitus
name: Diabetes Mellitus
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Duplicate
tags:
- Larger IID Data
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2021'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/widsdatathon2021/data?select=TrainingWiDS2021.csv
notebook_path: datasets/beyond_iid/new_iid/wids_diabetes_mellitus/wids_diabetes_mellitus.ipynb
source_row: 652
type_adapter_id: curation-record-v1
---

## Comments

CC: "Good dataset with many features, can checkout leaderboard and code for some examples of preprocessing and data cleaning"

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC of the WiDS Datathon 2021 evaluation page.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `gcs_eyes_apache`, `gcs_motor_apache`, `gcs_verbal_apache`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `gossis_icu_hospital_mortality` (TBD -> Yes, priority 2); a related task: `gossis_icu_hospital_mortality` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 3 coded columns carry their words.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Do not ship: the label is a diabetes diagnosis the patient already has, an item of the same APACHE comorbidity history whose other items are features, the SEL-7 case of cdc_diabetes and stroke_prediction; if kept, drop the all-rows clipped flags and keep rows with impossible BMI/age as missing. Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-11, Andrej): marks on the BeyondArena v0.2 review page. The seven `_clipped` flags are dropped (computed from the whole table's minimum and maximum; the clipped values stay as published). Rows with an impossible value stay with it set missing: age 0 (30 rows) and a BMI more than 0.01 away from weight over height squared (2,549 rows), in place of dropping 2,800 rows; 130,157 admissions now. Retirement is not decided: Andrej asks for a better task in the same data (open, Review issue 1); the split questions are open (issues 4 and 5).

CC (2026-11-11, Andrej): superseded by `gossis_icu_hospital_mortality` (BeyondArena v0.2 review page, issue 1, c: "Replace the target by in-hospital death"): `No (Retired)` with `Duplicate`, since 130,127 of this table's 130,157 rows are rows of the WiDS 2020 files and the same cohort now ships with in-hospital death, a target nobody knows in the first day; not retired for the known-diagnosis rule (SEL-7). Issues 4 and 5 are moot (the new dataset is split by hospital). The folder and `v2_path` stay until a retirement PR; the claim stays. Found on the way: all 2,549 BMI mismatches set missing on 2026-11-11 sit at GOSSIS's clipping bounds of BMI, weight or height (clipped extremes, not impossible values).

## Review

**Outcome:** added; superseded by `gossis_icu_hospital_mortality` (2026-11-11, Andrej, issue 1 c): the same ICU stays (WiDS 2020) with in-hospital death as the target; that dataset is on this page with its own open issues. Record `No (Retired)`, `Duplicate`; the folder leaves in a retirement PR. Before: The WiDS Datathon 2021 training table
on Kaggle (https://www.kaggle.com/competitions/widsdatathon2021), drawn from MIT's GOSSIS intensive-care data: 127,358
admissions to intensive care units of 204 hospitals, first-day vital signs, labs, admission details and chronic
conditions, and whether the patient has been diagnosed with diabetes mellitus (21.6%); random splits, ROC AUC (the
competition's metric). The AI recommends not shipping it: the label is a diagnosis the patient already has, recorded
in the same comorbidity history whose other items ship as features, the case two earlier records were retired for
(issue 1); if it ships, two cleaning steps should change (issues 2 and 3). Reviewed on 2026-11-04 without a panel, from
the gathered evidence (the record, the definition) and one check on the shipped data; no model run exists for it.
Validity: no feature is the diagnosis itself (checked: no admission diagnosis code holds 90% or more diabetic patients;
the most diabetic one, 702.01, holds 72% of 2,854; the other comorbidity flags hold 8.5% to 26%); but the label is a
known history item, not a condition found by a measurement (issue 1). Value: not measured here; the competition drew a
large field. Quality: seven flags are computed from the whole table's minimum and maximum (issue 2); 2,770 rows with a
BMI that disagrees with height and weight and 30 rows with age 0 are dropped rather than set missing (issue 3).
Weighed: a large real ICU table with a named competition +, a label already known to the patient and its history -,
the same cohort's established mortality task found by the scouting -.

**Main points:** Superseded (issue 1, c, 2026-11-11): in-hospital death of the same cohort ships as
`gossis_icu_hospital_mortality`; this record is `No (Retired)` with `Duplicate`, the folder stays until a retirement PR.
Issues 2 and 3 were applied before; issues 4 and 5 are moot.

**Record judgment:** valid source, disputed target. The record's only comment beyond the AI's is "Good dataset with many
features"; Lennart's marks of 2026-10-31 and 2026-11-01 settle the scales and the target's words. The data scouting
found `gossis_icu_hospital_mortality`, in-hospital death on the WiDS 2020 table of the same GOSSIS data, a different
task, not a duplicate; it would keep the ICU cohort in the benchmark if this one goes.

**Issues for Andrej:**

1. **Retire the dataset, since its label is a diabetes diagnosis the patient already has?**

   * **Problem:**
     - The label is whether the patient "has been diagnosed with diabetes mellitus", an item of the chronic-condition
       history the ICU records in its first day, and the other items of that history (AIDS, cirrhosis, liver failure,
       immunosuppression, leukaemia, lymphoma, metastatic cancer) ship as features.
     - The selection rules treat a past diagnosis taken in the same interview as the features as predicted by nobody,
       since whoever takes the history learns it, and a screening task needs positives that do not know yet, found by
       a measurement such as a lab test[^1a].
     - Retire it, or keep it as the competition's task with a recorded exception?
   * **Background:** the competition frames the use as knowing a patient's chronic conditions in the first day when the
     records are not at hand, and the definition rates the fit direct. In eICU, the US source of GOSSIS, the APACHE
     table holds `diabetes` as a 0/1 flag next to `aids`, `cirrhosis`, `hepaticfailure`, `immunosuppression`,
     `leukemia`, `lymphoma` and `metastaticcancer` (https://eicu-crd.mit.edu/eicutables/apachepredvar/). In practice an
     ICU team asks the patient or family, reads the medication list, or measures HbA1c (long-term blood glucose).
   * **Experiments:** check of 2026-11-04 on the shipped data: no admission diagnosis code with at least 30 patients
     holds 90% or more diabetic patients (the highest, 702.01, 72% of 2,854), and each other comorbidity flag goes with
     a diabetes share of 8.5% to 26% against 21.6% overall, so no feature gives the label away; the signal is in the
     glucose, weight and other first-day measurements.
   * **Consistency:** departs from cdc_diabetes_health_indicators (Lennart, 2026-10-15: "ever told you have diabetes",
     a diagnosis the respondent already has, `No`) and stroke_prediction (2026-10-26, `No`). What sets it apart, the
     AI's best guess: the competition names an actor without the history at the moment of prediction, and the inputs
     are measurements, not answers of the same interview.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 127,358 admissions as now; an exception to the rule recorded with the competition's use case; fit approximate | a large real ICU table and a known competition; the label is not read off a feature | the label is known to the patient and to whoever takes the history; departs from two retirements |
     | B | Retire | `No` with `No Good Target / Scientific Discovery`, a CC line, the folder removed | follows the rule and the two precedents | loses the competition; the cohort stays only if GOSSIS mortality is added |

   * **Recommendation:** B: the label is the patient's recorded history, which the history-taking that fills the
     features also reveals, and a measurement settles it within hours; the same cohort's mortality task can take its
     place. **Decision:** keep with an exception (A) or retire (B)?

   **Notes for the AI:** on B, the record gets `No`, the marker, and a CC line with the facts above; the folder is
   removed and the CHANGELOG notes it. On A, an exception under the rule ("a past diagnosis stays when the source names
   an actor who lacks the history at the prediction point and the inputs are measurements: wids_diabetes_mellitus"),
   `fit="approximate"` and a `fit_reason` naming the known-diagnosis label.

   [^1a]: **SEL-7** (Must): a label the respondent already knows, asked in the same interview as the features (a past
     diagnosis), is predicted by nobody; a screening task needs positives that do not know yet, found by an independent
     measurement such as a lab test. **SEL-2** (Must): when a rule seems to exclude a dataset, check how the prediction is
     made in practice, and let the use case decide.

   **Andrej (2026-11-11, discuss):** I don't think this is a reason to retire the dataset, can't we improve the task to
   be something better?

   **Answer (AI, 2026-11-11):** yes: the same admissions carry in-hospital death, a target nobody knows in the first
   day; WiDS 2020 publishes it for the rows of this table.

   * 130,127 of the 130,157 WiDS 2021 rows are rows of the WiDS 2020 files, matched exactly on 11 columns (the diabetes
     flag agrees in all of them); 90,998 of them are in WiDS 2020's labelled file, with `hospital_death`.
   * WiDS 2020 (91,713 labelled stays, 8.6% died) is the record `gossis_icu_hospital_mortality` (TBD -> Yes, priority 2),
     not built yet; it ships APACHE IVa's death probability, a published baseline to beat.
   * An undiagnosed-diabetes target cannot be made: the table has no HbA1c and no later diagnosis, so no row tells a
     new diabetes from a known one.
   * A narrower diabetes task, the patients who cannot give a history (ventilated, intubated or GCS not assessable),
     keeps the label the issue is about.
   * Measured (LightGBM, 5-fold; job of 2026-11-11):

     | Task | Rows | Positives | Model AUC | Reference |
     |---|---|---|---|---|
     | diabetes, all admissions (as now) | 130,157 | 21.6% | 0.869 | - |
     | diabetes, no history possible (ventilated / intubated / GCS unable) | 43,121 | 22.3% | 0.836 | 0.883 on the other rows |
     | in-hospital death (WiDS 2020) | 91,713 | 8.6% | 0.902 | APACHE IVa 0.863 (81,395 rows) |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep diabetes, exception to the known-diagnosis rule | as now, the rule's exception written down | the competition's task | the label stays a known history item |
     | b | Diabetes for patients who cannot give a history | rows cut to 43,121 ventilated / intubated / GCS-unable stays | the use case at its most literal | still a recorded history; family and records also tell |
     | c | Replace the target by in-hospital death | build `gossis_icu_hospital_mortality` from WiDS 2020 (the same cohort); this record leaves as superseded by it, not for the rule | a target unknown at 24 h, an established task with a clinical baseline | loses the WiDS 2021 competition; PhysioNet's copy is credentialed, Kaggle's needs the 2020 rules accepted (downloaded here) |
     | d | Both | c, and this dataset kept as in a | two tasks on one cohort | the same admissions twice in the benchmark |

   * **Recommendation:** c: in-hospital death is the better task in this data, and the cohort stays in the benchmark.
     **Decision:** a, b, c or d?

   **Andrej (2026-11-11, discuss):** Reply (c): Replace the target by in-hospital death

   **Resolved (2026-11-11, Andrej):** c: Replace the target by in-hospital death: `gossis_icu_hospital_mortality` is
   built from WiDS 2020's labelled file (91,713 stays, 147 hospitals, split by hospital; its own REVIEW.md); this record
   leaves as superseded by it, not for the known-diagnosis rule: `No (Retired)` with `Duplicate` (the same admissions:
   130,127 of 130,157 rows are WiDS 2020 rows), priority removed, a CC line. The folder and `v2_path` stay until a
   retirement PR; the claim stays.

2. **If kept, drop the seven flags that mark a value at the whole table's minimum or maximum?**

   * **Problem:**
     - The definition adds `_clipped` flags to seven blood-pressure and heart-rate columns, true where the value equals
       the minimum or maximum of that column over all rows, test rows included.
     - The cleaning rules compute no feature from statistics over all rows and build a feature only to remove a leak,
       restore lost meaning or turn unusable raw data into usable form[^2a].
     - Drop the flags, or keep them?
   * **Background:** Kaggle participants found that GOSSIS clipped these vital signs at fixed bounds; a model sees the
     bound itself in the value, so the flag repeats what the column holds.
   * **Experiments:** check of 2026-11-04 on the shipped data: six of the seven columns hold 599 to 874 rows at each
     bound (systolic minimum 41 and 160, for example), the signature of clipping; the maximum of `d1_heartrate_min`
     (175) holds 1 row, so its flag marks one unclipped value.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 7 `_clipped` flags | follows the Kaggle participants | a feature from all rows; repeats the value; one flag marks an unclipped row |
     | B | Drop | the 7 flags dropped; the clipped values stay | the data as published; follows the cleaning rules | none found |

   * **Recommendation:** B: the flags add nothing a model cannot read from the value. **Decision:** keep (A) or drop
     (B)?

   **Notes for the AI:** on B, remove the clipping loop in `_clean`, the `_clipped` entries of `categorical`, and the
   curation note; add a note that seven vital-sign columns are clipped at fixed bounds; `dataset check`.

   [^2a]: **CLEAN-7** (Must): never compute a feature value from statistics over all rows. **CLEAN-19** (Should): we
     build a feature only to remove a leak, to restore meaning the source destroyed, or where the raw data cannot be
     used as it is.

   **Resolved (2026-11-11, Andrej):** B: Drop: the seven `_clipped` flags and their loop removed; a note says the vital
   signs are clipped at fixed bounds and ship as published; `dataset check` clean (0 errors, 0 warnings).

3. **If kept, keep the rows with an impossible BMI or age, with that value set missing?**

   * **Problem:**
     - The definition drops 2,770 rows whose BMI differs from weight over height squared (rounded to two decimals) and
       30 rows with age 0, "as it is unclear what the cause of this error is".
     - The cleaning rules set an impossible value to missing and keep the row, since dropping rows by a value can change
       who is in the task[^3a].
     - Keep the rows with BMI or age set missing, or keep dropping them?
   * **Unknown:** the diabetes share of the dropped rows and how many mismatches are only rounding; the raw Kaggle file
     needs the competition's rules accepted, which this account has not, so the check could not run.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop the rows (implemented) | 2,800 rows dropped; 127,358 left | no inconsistent BMI or age in the data | rows leave for one wrong value; their label share is unknown |
     | B | Set missing, keep the rows | BMI set missing where it disagrees, age set missing where it is 0; about 130,158 rows | follows the cleaning rule; keeps every admission | BMI missing for 2% more rows |

   * **Recommendation:** B: one wrong value does not make an admission a non-task row. **Decision:** drop (A) or set
     missing (B)?

   **Notes for the AI:** on B, replace the two row filters by `mask` on `bmi` and `age`; widen the BMI test to a
   tolerance (for example 0.01) so rounding is no mismatch, and report the count; `dataset check` and the new row
   count in `row`.

   [^3a]: **CLEAN-11** (Should): impossible values become missing, and the row stays; a row leaves only when it is no
     task row or a copy.

   **Resolved (2026-11-11, Andrej):** B: Set missing, keep the rows: age 0 set missing (30 rows); BMI set missing where
   it is more than 0.01 from weight over height squared (2,549 rows, 21.3% diabetic against 21.6%; the old exact
   two-decimal test counted 221 rounding cases); 130,157 admissions now (was 127,358); `dataset check` clean, one info:
   8 exact duplicate rows.

4. **Time basis: if kept, name the random split a `StationaryRelation`?**

   * **Problem:**
     - The admissions arose over the two years of eICU (2014-2015), the US source of the WiDS table, and the label is the diabetes history recorded in the first day with the vital signs and labs, so the target is a present state; the release has no admission date or year, and the definition drops the encounter id as carrying no time.
     - The record's facts, `Samples: Over Time` and `Time: Lost`, fit, and with the time lost a stationary relation can only be argued: whether a patient has diabetes and how it shows in first-day glucose and weight do not move within two years, beyond the share of diabetic patients and each hospital's charting.
     - Name the random split a `StationaryRelation`, argued from the source, or a `ForcedIIDFromTemporal`?
   * **Background:**
     - eICU holds over 200,000 unit stays of 139,000 patients admitted in 2014 and 2015 at 208 US hospitals (https://physionet.org/content/eicu-crd/2.0/); Kaggle released 130,157 labelled encounters for WiDS 2021 without dates or patient ids.
     - The prototypes, by the rule's questions: diabetes can begin, so not `Timeless`; the use case is a later admission, so not a `Snapshot`; the admissions share no prediction moment, so not a `DelayedTarget`; a present state recorded in the first day, so a `StationaryRelation`[^4a].
     - Repeat patients, the one way another row could carry a test row's label, are issue 5.
   * **Unknown:** whether `encounter_id` follows the admission order; the raw Kaggle file is not available here (the competition's rules are not accepted on this account), so the definition's statement is unchecked.
   * **Effect on the task:** none on the data or the scores; the tag and its line state why a random split stands for the use case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, `StationaryRelation` (implemented) | the shipped split; once PR #50 is in, the tag and a `Time basis:` line | the label and every feature come from the first day of one stay | argued from the source; the encounter id is unchecked |
     | B | Random split, `ForcedIIDFromTemporal` | the same split, tagged as forced from temporal[^4b] | says that a later year of admissions is not tested | nothing found that moves the relation within two years; the release has no time for the leak test the forced tag asks for |

   * **Recommendation:** A, if issue 1 keeps the dataset: a standing condition recorded with the first-day values of the same stay. **Decision:** A or B?

   **Notes for the AI:** on A, once PR #50 is in: `data_tags = ("StationaryRelation",)` and a curation bullet `- Time
   basis: StationaryRelation: ICU admissions of 2014 and 2015 (eICU, the source of GOSSIS and of this table); the
   diabetes history is recorded in the first day with every feature. The release keeps no admission date, so this is
   argued from the source, not measured; no repeat patient was found (REVIEW.md issue 5).` No `splits_comment` change.
   On B, `data_tags = ("ForcedIIDFromTemporal",)` and a bullet saying that admission dates would allow a split by month.

   [^4a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     collection facts, and a definition can name the use-case prototype it follows with a `Time basis:` line. A
     present state read through a relation that time does not move, beyond prevalence and practice, is a
     `StationaryRelation`, measured on a dated source and argued from the source when the time is lost.
   [^4b]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime, tagged as forced from temporal, after a leak test across the split; the definition says
     what a timestamp would change.

   **Answer (AI, 2026-11-06):** `StationaryRelation` now needs a measurement: if kept, try to date the stays through
   eICU first (a), or name the random split forced from temporal (b, the issue's B)?

   * **Problem:**
     - On the item "One meaning for `StationaryRelation`, measured or argued?" you wrote "I want this to be always
       measured": the tag now needs a dated source on which the target and its relation to the features are shown flat,
       so option A, argued from the source, no longer exists[^4s].
     - The release has no admission date or year. Its parent, eICU, records each stay's discharge year (2014 or 2015),
       but WiDS publishes no key to eICU and eICU needs credentialed access, so a measurement would rest on matching
       stays by their first-day values.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Date through eICU, then decide | credentialed access; WiDS rows matched to eICU stays by first-day values; the diabetes share and the relation compared between 2014 and 2015 | a measurement on the parent | no published key; two years only; a large join for one tag |
     | b | Random split, `ForcedIIDFromTemporal` | the issue's B: the tag and a `Time basis:` line saying the stays came over 2014 and 2015 with no date released; dated stays would test a later year | the regime the rules give a forward use case whose time is lost | the leak test can check repeats (issue 5) and hidden groups, not periods |

   * **Recommendation:** b, if issue 1 keeps the dataset; a only if the eICU match is wanted for other reasons.
     **Decision:** a or b?

   [^4s]: **SPLIT-32** (Should; Andrej, 2026-11-06): a `StationaryRelation` is always measured on a dated source; where
     time is lost it cannot be, and a forward use case takes the forced tag. **SPLIT-8** (Must): the forced split ships
     after its leak test, and its line names the reason and what a dated release would change.

   **Andrej (2026-11-11, discuss):** Try to measure whether the relation is indeed stationary or better whether we even
   can do a temporal split

   **Answer (AI, 2026-11-11):** no temporal split is possible: the data spans one year and no column or order carries
   time.

   * The source says the GOSSIS extract spans "a one-year timeframe" (WiDS 2020 on PhysioNet,
     https://physionet.org/content/widsdatathon2020/1.0.0/); no date, year or day column exists.
   * Three orders were tested within each hospital: the file's row order, `encounter_id` and WiDS 2020's `patient_id`
     (reached through the exact row match of issue 1). None carries time:

     | Order (last 20% per hospital) | Late vs early, adversarial AUC | Diabetes AUC on the late 20% | Label share by quintile |
     |---|---|---|---|
     | file order | 0.500 | 0.870 | 21.4% to 21.7% |
     | `encounter_id` | 0.499 | 0.867 | flat |
     | random 20% (reference) | 0.500 | 0.872 | flat |

   * `encounter_id` and `patient_id` are random: rank correlation with age, label, missing count and death below 0.01.
   * The competition's own test file (10,234 unlabelled stays, not in WiDS 2020, the same ICUs: 264 of its 302 ICU ids)
     differs from training (adversarial AUC 0.78), but by preparation: age never missing (3.8% in training), BMI missing
     9.9% (3.4%). No date shows, and it has no labels.
   * Stationarity can only be measured through eICU (discharge year 2014/2015 per stay), which needs credentialed access
     and has no published key to these rows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split, `ForcedIIDFromTemporal` | the tag and a `Time basis:` line: one year of stays, no date released | the rule's regime for lost time; measured that no order exists | a later period is not tested |
     | b | Date through eICU, then decide | credentialed access, rows matched to eICU stays by first-day values | a real measurement | no key; one year only; a large join for one tag |

   * **Recommendation:** a. **Decision:** a or b?

   **Resolved (2026-11-11, Andrej):** moot under issue 1, c: the dataset leaves; the mortality task takes up the time
   basis in `gossis_icu_hospital_mortality`'s REVIEW.md.

5. **Repeat patients: keep the random split, since no patient shows up twice?**

   * **Problem:**
     - 601 admissions are ICU readmissions and the release has no patient id, so a patient's other stay could sit on the other side of a random split and carry the same lifelong label.
     - On the shipped rows no such pair shows: admissions that share hospital, sex, ethnicity, height, weight and an age within a year are both diabetic in 4.8% of 416 pairs against 4.7% by chance, and the candidates for the 601 readmissions agree on the label less often than random pairs (62% against 66%).
     - Keep the random split, or group by a key built from these columns?
   * **Background:** a diabetes history is the same at every stay of one patient, so true repeats would agree on the label nearly always. A grouped split needs a true id or a key constructed exactly from the data[^5a]; matching demographics is a similarity key.
   * **Experiments:** check of 2026-11-06 on BeyondArena's container (the same 127,358 admissions), counts only:
     - Stay types: 122,066 admissions, 4,691 transfers, 601 readmissions (28% diabetic against 21.6% overall).
     - Pairs with the same hospital, sex, ethnicity, height and weight and an age within one year (keys of 2 to 5 rows): 416; same label 67.3% against 66.1% by chance; given one diabetic, the other is diabetic in 12.8% against 21.6% overall.
     - The 601 readmissions: 327 have another admission of the same hospital, sex, ethnicity and height and an age within a year (3.1 candidates on average), agreeing on the label 61.6% of the time; 54 with a weight within 3 kg agree 55.7%; random pairs agree 66.1%.
   * **Effect on the task:** none measurable: the earlier stays of the readmitted patients do not seem to be in the table, or GOSSIS kept one stay per patient.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split (implemented) | admissions split at random | no repeat patient found; the check is written down | the release cannot prove that none exists |
     | B | Group by a demographic key | hospital, sex, ethnicity, height and age as groups | would hold out a repeat if one existed | a similarity key, which the grouping rule bars; it joins unrelated patients, whose labels agree only by chance |

   * **Recommendation:** A: the label would betray a repeat, and the pairs agree no more than chance. **Decision:** A or B?

   **Notes for the AI:** on A, if issue 1 keeps the dataset, a curation bullet: `- Repeat patients: 601 admissions are
   readmissions and the release has no patient id; admissions that share hospital, sex, ethnicity, height, weight and an
   age within a year agree on the diabetes label no more often than chance (416 pairs, both diabetic 4.8% against 4.7%),
   so no patient is found twice (check of 2026-11-06).` No split change. On B nothing is drafted, since the rule bars
   the key.

   [^5a]: **LEAK-17** (Must): repeated entities in different rows leak the target across the split, even when the rows
     differ; group them. **SPLIT-24** (Must): group on a true group id or on one constructed exactly from the data,
     never on a similarity threshold.

   **Answer (AI, 2026-11-06):**

   * **Verdict:** natural: the label does not travel with any link the data allow, so the random split stays (A) and
     the notes give the check[^5e1].
     - Link: no patient id; the closest key the data allow (hospital, sex, ethnicity, height, weight, age within a
       year) finds 416 pairs.
     - The label does not travel: they agree on diabetes 67.3% of the time against 66.1% for unlinked pairs, and the
       readmissions' candidates 61.6%, where one patient's lifelong diagnosis would agree almost always.
     - No order: the release keeps no admission date.
   * **Recommendation:** unchanged, A.

   [^5e1]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one verdict; natural when
     the look-alikes are distinct units: the random split stays and the notes say so. **LEAK-42** (Should; draft PR
     #62): three tests set the verdict: a link above a chance rate that keeps the data's structure, a label that
     travels with the link beyond what the shared features predict, and an order; a link that carries no label is no
     leak.

   **Andrej (2026-11-11, discuss):** Try to find temporal order or another potential split closer to reality

   **Answer (AI, 2026-11-11):** no order exists (issue 4); the one real alternative is a split by hospital, which costs
   0.017 AUC.

   * The WiDS 2020 organisers split by hospital in the main: 57 of the 66 hospitals of their test file are not in
     training. WiDS 2021 tested on the same ICUs (264 of 302 ICU ids shared).
   * WiDS 2020's `patient_id` is unique per stay (91,713 ids, 91,713 rows), so it finds no repeat patient either.
   * Measured (LightGBM, diabetes, job of 2026-11-11):

     | Split | AUC |
     |---|---|
     | random 5-fold (as now) | 0.869 |
     | random 5-fold, hospital and ICU id dropped | 0.859 |
     | grouped by `hospital_id`, 5-fold (204 hospitals) | 0.852 (sd 0.014) |
     | WiDS 2020's own train / test partition | 0.848 |
     | last 20% per hospital by file order | 0.870 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random (implemented) | admissions split at random | WiDS 2021's own test design (same ICUs) | hospital id is worth 0.010 AUC to a model |
     | B | Grouped by `hospital_id` | `grouping="hospital_id"`; the test hospitals are new | a model used at a hospital it has not seen; WiDS 2020's design | 204 groups, sizes 2 to 4,306 rows; folds vary (sd 0.014) |

   * **Recommendation:** A for the diabetes task, the competition's design; B is the natural split for the mortality
     task of issue 1 (its record already asks for it). **Decision:** A or B?

   **Resolved (2026-11-11, Andrej):** moot under issue 1, c: the dataset leaves; `gossis_icu_hospital_mortality` is
   split by hospital, as this answer suggested for mortality.

## Reference

Karen Matthys, Meredith Lee, NehaGoel, Sharada Kalanidhi, Valerie, and Vani M. WiDS Datathon 2021. https://kaggle.com/competitions/widsdatathon2021, 2021. Kaggle.
