---
unique_name: indian_liver_patient_dataset
name: ilpd
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2012'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5D02C
notebook_path: datasets/beyond_iid/new_iid/indian_liver_patient_dataset/indian_liver_patient_dataset.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/indian_liver_patient_dataset/dataset.py
source_row: 747
type_adapter_id: curation-record-v1
---

## Comments

CC: "There was a custom train/test split. Task might be rather a toy task and not of practical use. Unclear current SOTA for the domain but in itself fine and not too old"

Make sure to add indicator variable for clipping of 90

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag (untuned skills +0.47 to +0.50) does not hold for tuned methods. On BeyondArena LimiX-2 reaches ROC AUC 0.771 and the median method 0.750, with 4 of 29 methods tied with the best.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The UCI page defines no task metric and the cited paper (Ramana et al. 2012) is a statistical comparison of the USA and India patient groups, not a benchmark with a declared score; later uses report accuracy only.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_liver_elastography_fibrosis` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 means a liver patient (UCI)).

CC (2026-11-11, Andrej): the five Review issues, settled on the marks of 2026-11-11, applied to this branch, whose definition was the one from before them. Issue 1 (discuss, reply a = the issue's B, "You need to do more digging about the source and whether those are real patient measurements."): kept; `fit_reason` now says a physician labelled the records while the criterion stays unstated and the lab values contradict it for part of them, and a `curation_comments` bullet carries the provenance checks (hand-transcribed lab reports, the 751-record parent, the contradicting counts, the number-format probe at ROC AUC 0.50). Issue 2, B: in `_clean` both bilirubin values go missing in the 3 rows where direct exceeds total, and the albumin-to-globulin ratio in the 8 rows where it differs from `ALB / (TP - ALB)` by more than 0.2; the rows stay. Issue 3, B: `drop_duplicates()`, 583 to 570 rows (406 liver patients, 164 others). Issue 4 (discuss, reply a, "Measure it."): `data_tags = ("ForcedIIDFromTemporal",)` with a `Time basis:` bullet; holding out by file position costs nothing. Issue 5, B: `Samples: Over Time` and `Time: Lost` on the record's `tags`. `dataset check`: 0 errors, 0 warnings, 0 info.

## Review

**Outcome:** added. The ILPD file (UCI, 2012): 583 records from north-east Andhra Pradesh, India, with age, sex and
eight liver blood tests, and whether the record is of a liver patient (416) or not (167). Reviewed without a panel,
from the gathered evidence: the record, Andrej's check of 2026-10-15, the number-format sweep of 2026-10-27, the
model runs on the shipped BeyondArena data (the same rows) and a check of 2026-11-04. The AI recommends keeping
it after changes. Validity is open (issue 1): the label has no stated criterion, hospital or period, a share of the
lab values contradicts it, and the two groups were collected apart (fit approximate, `Selection Bias`); the probe that
decided hepatitis_c_prediction, a recording difference between the groups, finds none here (number format alone ROC
AUC 0.50). 13 records are in the file twice with the same label, which no chance match explains, and a lookup of the
copies lifts ROC AUC by 0.02, more than the gap between TabPFN 3.5 and logistic regression (issue 3; LEAK-18).
Value: tuned methods spread (Lennart, 2026-10-06; TabPFN 3.5 0.766 against logistic regression 0.748, better on 52 of
60 splits), which keeps a dataset unless an earlier rule applies (TP-3). Quality: 12 impossible values (issue 2).
Weighed: a real liver-panel table whose methods separate, against a label of unknown basis.

**Main points:** all issues settled 2026-11-11: kept with a note (issue 1: real lab reports labelled by a physician;
criterion, hospital and period unknown); random split tagged forced from temporal, measured by file position (issue
4); the 13 repeated records dropped (issue 3), 11 impossible values set to missing (issue 2), collection facts added
(issue 5).

**Record judgment:** a real liver-panel table with an undocumented label; the spread between methods is real, the
basis of the label is not known. The data-scouting run of 2026-10-31 screened `nhanes_liver_elastography_fibrosis`
(AI-filled, unverified): liver stiffness measured in a national survey, a documented target for a related question.

**Issues for Andrej:**

1. **An undocumented label that the lab values contradict: keep, or retire as hepatitis_c_prediction was?**

   * **Problem:**
     - UCI says only that the patients were "diagnosed", with no criterion, hospital or period, and the cited paper
       (Ramana et al. 2012) compares Indian and US patient groups without saying how the records were labelled.
     - The lab values contradict the label for many records: of the 167 "non-patients" 85 have low albumin and 18
       high bilirubin or liver enzymes, and 55 of the 416 patients have normal bilirubin, ALT, AST and albumin.
     - Keep the label with a note, or retire the dataset?
   * **Background:** albumin, a blood protein made by the liver, is low below 3.5 g/dL; bilirubin, a breakdown
     product the liver clears, is raised above 2 mg/dL; ALT and AST are liver enzymes, counted here as raised above
     three times the upper normal limit. UCI: https://doi.org/10.24432/C5D02C. The cited paper: Ramana BV, Babu MSP,
     Venkateswarlu NB. A critical comparative study of liver patients from USA and INDIA: an exploratory analysis.
     International Journal of Computer Science Issues. 2012;9(3):506.
   * **Effect on the task:** the label may mark which collection a record came from (a liver clinic or elsewhere)
     more than whether the liver is diseased, and a model then learns the collection; how much is not known.
   * **Experiments:**
     - Andrej's check of 2026-10-15 (the shipped splits, 20 x 3): TabPFN 3.5 ROC AUC 0.766, logistic regression on
       the log values 0.748 (ahead on 52 of 60 splits, paired standard error 0.002), random forest 0.739.
     - The test that showed for hepatitis_c_prediction that the groups came from separate collections, the number
       format of every float column per class, ran over the shipped data on 2026-10-27: the format alone gives ROC
       AUC 0.502, and the values with their format 0.737 against 0.739 for the values alone. No recording difference
       between the groups shows; the 4 missing values (all in the albumin-to-globulin ratio) are too few to mark one.
     - Model runs on the shipped data: the 40 benchmark methods reach ROC AUC 0.727 to 0.774 (TabPFN 3.5
       0.767, logistic regression 0.737 to 0.744), and its best model without the copies of issue 3 uses an
       indicator for age under 30: the records without liver disease are younger.
   * **Curators:** Lennart (CC 2026-10-06) kept it because tuned methods spread; Andrej (2026-10-15) disputes the
     keep because nobody documents how the label was assigned.
   * **Consistency:** hepatitis_c_prediction was retired on 2026-10-27 for two separately collected groups scored as
     one label, where the recording difference was measured; here the same test finds none. A source that is
     plausible but unclear in a detail stays with a note[^1a], and a task whose tuned methods spread stays[^1b];
     against that, the target must be an observed outcome or an expert annotation[^1c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as defined (implemented) | ships as is, fit approximate | methods spread | the contradicting values are not documented |
     | B | Keep with a note | `fit_reason` and `curation_comments` name the undocumented label and the contradicting values | the gap is stated; no recording difference found | a label of unknown basis stays |
     | C | Retire | `No (Retired)`, `Selection Bias` kept, the reason in a CC line | no undocumented label in the benchmark | rests on circumstantial evidence, against the spread between methods |

   * **Recommendation:** B: the test that decided hepatitis_c_prediction finds no separate recording here, so what is
     left is an unclear label definition, which the fit names rather than retires[^1d]. **Decision:** as is (A), keep
     with a note (B) or retire (C)?

   **Notes for the AI:** on B, add to `fit_reason` "the label's criterion is not stated, and the lab values
   contradict it for part of the records" and a `curation_comments` bullet with the counts above and the format
   probe; re-run `dataset check`. On C: `suggestion: No (Retired)`, a dated CC line, the folder removed with a
   CHANGELOG entry and `v2_path` cleared.

   [^1a]: **PROV-2** (Should): a source that is plausible but unclear in a detail stays, with a note of what to
     clarify.
   [^1b]: **TP-3** (Must): if tuned methods spread, keep the dataset (a rule of an earlier part still wins).
   [^1c]: **SEL-3** (Must): the target is an observed outcome or an expert annotation.
   [^1d]: **USE-8** (Must): a label definition the sources do not settle is a known gap and makes the fit approximate.
     **EV-6** (Should): a claim is proven by a test that could have refuted it.

   **Andrej (2026-11-11, discuss):** You need to do more digging about the source and whether those are real patient
   measurements.

   **Answer (AI, 2026-11-11):** keep with a note (B), now that the values check out as real lab reports labelled by a
   physician?

   * **Problem:**
     - The values behave like transcribed hospital lab slips: the albumin-to-globulin ratio is computed from albumin
       and total protein and cut to one decimal, ages and enzymes heap on round numbers, and nothing looks generated.
     - A physician labelled the records: the authors' 2011 paper thanks Dr. Bevera Lakshmana Rao "for his help during
       the collection of data and in labeling samples", and the 2012 paper thanks him, Dr. S. Sridhar, K. Ravi Kanth and
       B. Sai Prasad "for providing the data".
     - Still unknown: the hospital, the period, the criterion, and why 583 of the 751 records of the 2011 paper (which
       also had indirect bilirubin and globulin) were published.
   * **Background:**
     - The authors are computer scientists at AITAM, Tekkali (Srikakulam district, north-east Andhra Pradesh) and
       Andhra University, Visakhapatnam; neither paper names a hospital or an ethics approval, and the physician has no
       trace online. The 2012 paper calls the others "non-liver patients", not healthy people.
     - The "non-patients" have a median albumin of 3.4 g/dL (51% below 3.5), so they look like other hospital patients
       rather than healthy controls: the label separates liver patients from other patients tested.

     | Check (570 rows after issues 2 and 3) | Result | Reads as |
     |---|---|---|
     | A/G against ALB / (TP - ALB) | 471 of 566 equal it cut to 1 decimal, 519 cut or rounded, 553 within 0.1; 8 off by more than 0.2 | ratio computed on the report; a few typos |
     | Direct against total bilirubin | direct below total in 567, above in 3 (e.g. 9.0 against 1.8) | typos |
     | Albumin against total protein | below in all rows | consistent |
     | Ages ending in 0 or 5 (Whipple index, 23 to 62) | 165 (100 = none; 175+ = very rough) | reported ages, typical of the region |
     | ALP, ALT, AST ending in 0 or 5 (20% expected) | 39%, 29%, 26% | hand-recorded values |
     | Units and ranges | bilirubin 0.4 to 75 mg/dL, enzymes 10 to 4,929 IU/L, protein 2.7 to 9.6 g/dL, albumin 0.9 to 5.5 g/dL | clinical units; the extremes occur in acute hepatitis |
     | Pairs differing in one value only | 0 (also 0 in 50 tables with shuffled columns) | no interpolated rows |
     | Exact copies | 13 pairs, each on adjacent rows of the UCI file (rows 19/20 to 201/202) | entered twice, not generated |
     | Non-patients' labs | median albumin 3.4, bilirubin 0.8 mg/dL, ALT 27 IU/L | other patients, not healthy |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep with a note (the issue's B) | `fit_reason` and a `curation_comments` bullet: real lab reports, labelled by a physician on an unstated criterion, the others are other patients, a subset of 751 records | the measurements are real and the label has a named expert | the criterion and the selection of 583 of 751 stay unknown |
     | b | Retire (the issue's C) | `No (Retired)`, folder removed | no label of unstated criterion | discards a real, expert-labelled table whose methods spread |
     | c | Keep as is (the issue's A) | nothing | none | the gap is not written down |

   * **Recommendation:** a: the data are real patient measurements and the label an expert annotation, which the
     target rule accepts; the unstated criterion is a gap to name, not a reason to retire[^1e]. **Decision:** a, b or c?

   [^1e]: **SEL-3** (Must): the target is an observed outcome or an expert annotation. **PROV-2** (Should): a source
     that is plausible but unclear in a detail stays, with a note of what to clarify. **USE-8** (Must): an unsettled
     label definition is a known gap and makes the fit approximate. Sources: Ramana BV, Babu MSP, Venkateswarlu NB. A
     critical study of selected classification algorithms for liver disease diagnosis. IJDMS. 2011;3(2):101-114,
     https://www.airccse.org/journal/ijdms/papers/3211ijdms07.pdf; Ramana BV, Babu MSP, Venkateswarlu NB. A critical
     comparative study of liver patients from USA and INDIA: an exploratory analysis. IJCSI. 2012;9(3):506-516,
     https://www.ijcsi.org/papers/IJCSI-9-3-2-506-516.pdf.

   **Andrej (2026-11-11, discuss):** Reply (a): Keep with a note (the issue's B). You need to do more digging about the
   source and whether those are real patient measurements.

   **Answer (AI, 2026-11-11):** further digging finds the authors' collection protocol but still no hospital; nothing
   points to synthetic data.

   * The UCI page names no institution, hospital, criterion or method; creators Ramana and Venkateswarlu, donated 20
     May 2012.
   * Ramana's later UGC project at AITAM, Tekkali (two 2021 papers) describes how he collects such data: in each region
     of Andhra Pradesh "one growth center ... where hospital facilities are available to diagnose LFT", the records
     "collected and annotated" there. Visakhapatnam is the north-coastal centre, ILPD's region.
   * Those are new collections (499, 600 and 243 records, other ranges), not ILPD; they too name no hospital, label
     criterion or ethics approval.
   * So ILPD is most likely liver function test records from hospitals around Visakhapatnam, labelled by a physician;
     the checks above (computed ratios, digit heaping, copies on adjacent rows) fit real hand-transcribed reports.

     | Source | Adds |
     |---|---|
     | Ramana et al. 2011 (IJDMS) | 751 records, physician Dr. B. Lakshmana Rao labelled them |
     | Ramana et al. 2012 (IJCSI) | 583 records, north-east Andhra Pradesh, four people thanked "for providing the data" |
     | UCI page | no institution or method |
     | Ramana 2021 (Psychology and Education 57(5):375-392) | protocol: hospital LFT centres per region, data "collected and annotated" |

   Sources: https://archive.ics.uci.edu/dataset/225; https://www.adityatekkali.edu.in/research/reports/6934_16_SERO_UGC_VENKATA_RAMANA_BENDI_IT.pdf
   (UGC report with both 2021 papers).

   **Resolved (2026-11-11, Andrej):** a (the issue's B): `fit_reason` now says a physician labelled the records, but
   the label's criterion is not stated and the lab values contradict it for part of the records; a
   `curation_comments` bullet gives the provenance checks, the 751-record parent, the contradicting counts and the
   format probe. Kept; `Selection Bias` stays. `dataset check` passes.

2. **Only if kept: set 12 impossible values to missing?**

   * **Problem:**
     - Direct bilirubin is part of total bilirubin, yet it is the larger of the two in 3 rows.
     - The albumin-to-globulin ratio follows from albumin and total protein (globulin is total protein minus albumin),
       yet in 9 rows the published ratio differs from that by more than 0.2.
     - Set these values to missing, or keep them as published?
   * **Effect on the task:** small; wrong values in a few rows.
   * **Background:** the record's old note on ages clipped at 90 concerns 1 row; a note is enough.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as published (implemented) | 583 rows unchanged | the file as published | 12 impossible values stay |
     | B | Set them to missing | both bilirubin values of the 3 rows and the ratio of the 9 rows missing, rows kept; one `curation_comments` bullet | no impossible value | a few lines of code and a new checksum |

   * **Recommendation:** B, if issue 1 keeps the dataset[^2a]. **Decision:** keep (A) or set to missing (B)?

   **Notes for the AI:** on B, in `_clean` set `TB` and `DB` to missing where `DB` > `TB`, and `A/G` where it differs
   from `ALB / (TP - ALB)` by more than 0.2; a `curation_comments` bullet (also the one age clipped at 90); re-run
   `dataset check`.

   [^2a]: **CLEAN-11** (Should): impossible values become missing, and the row stays.

   **Andrej (2026-11-11, change):** Option B: Set them to missing.

   **Resolved (2026-11-11, Andrej):** B: in `_clean` both bilirubin values are missing in the 3 rows where direct
   exceeds total, and the albumin-to-globulin ratio in the 8 rows (9 before the drop of issue 3; one pair was a copy)
   where it differs from `ALB / (TP - ALB)` by more than 0.2; rows kept, a `curation_comments` bullet (also the one
   age clipped at 90). `dataset check` passes (0 errors, 0 warnings).

3. **Drop the second copy of the 13 records that are in the file twice?**

   * **Problem:**
     - 13 records appear twice, identical in age, sex and all eight blood tests and with the same label each time,
       and the definition keeps them as natural duplicates.
     - With ten columns, most of many values, no copy arises by chance: none of 500 tables with each column shuffled
       on its own held a single repeated row.
     - Drop one copy of each pair (570 rows), or keep all 583?
   * **Effect on the task:** on a random split 3 to 10 of the 195 test rows (6 on average) have their copy among the
     training rows and are ranked by recall of the copy's label, which a new patient never offers.
   * **Experiments:** model runs on the shipped data found the copies and used them: a shrunk logistic and
     naive Bayes blend on the log blood tests reached ROC AUC 0.762, and the same blend ranking a row with a training
     copy by the copy's label 0.782, ahead of the best of 40 benchmark methods (0.774). The copies are worth 0.02 ROC
     AUC, more than the gap between TabPFN 3.5 and logistic regression. The check of 2026-11-04 confirmed the 13 pairs
     on the shipped frame (10 pairs of liver patients, 3 of others) and the chance count of 0.
   * **Consistency:** follows obesity_estimation (10 exact copies dropped, 2026-10-14) and audiology_diagnosis (27
     copies dropped)[^3a]; the same question is open on blood_tests_drink_prediction (issue 3 there).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all rows (implemented) | 583 rows, 13 records twice | the file as published | about 6 test rows per split are recalled, not predicted; the lookup moves the ranking |
     | B | Drop the second copy | 570 rows; the note on natural duplicates replaced by the check | each record once | a new checksum, a rebuild |

   * **Recommendation:** B: with ten measured values per record, a repeat is a copy, not a second patient[^3b].
     **Decision:** keep (A) or drop the copies (B)?

   **Notes for the AI:** on B, `df = df.drop_duplicates()` in `_clean` (the 13 pairs are rows 26/165, 72/283,
   108/495, 132/398, 139/532, 153/207, 170/419, 218/278, 235/239, 349/437, 476/496, 483/522 and 526/579 of the
   BeyondArena container), replace "the data contains a few (n=13) duplicates, that are likely naturally occurring"
   with the check, re-run `dataset check` (the `dataset_duplicate_rows` warning goes), CHANGELOG entry.

   [^3a]: **LEAK-19** (Should): exact copies with the same label are dropped rather than grouped on the duplicate key.
   [^3b]: **LEAK-18** (Should): many degrees of freedom and an exact match: a collection artefact, drop it and give the
     share; few features and plausible repeats: natural, keep them and say so.

   **Answer (AI, 2026-11-06):**

   * **Verdict:** entity fix, copies on an exact key: each pair is one record entered twice, so it goes down to one
     row (B)[^3e1].
     - Link far above chance: 13 pairs equal in all ten values, against none in 500 tables with each column shuffled.
     - The label travels with the link: the same label in 13 of 13 pairs, and the copy's label lifts ROC AUC by 0.02
       beyond what a model reads from the values.
     - No order: no date or visit number, and the copies sit 4 to 393 rows apart in the file.
   * **What the drop does to the label:** 13 rows go (2.2%): 10 liver patients (2.4% of 416) and 3 others (1.8% of
     167). The patient share moves from 71.4% (416 of 583) to 71.2% (406 of 570).
     - **Question:** does the label still stand for the use case? The AI thinks so: the shares barely move, and the
       open doubt about the label is issue 1's, not this drop's.
   * **Recommendation:** unchanged, B. **Decision:** keep (A) or drop the copies (B)?

   [^3e1]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one verdict (natural,
     entity fix, temporal fix or not recoverable); copies of one record go down to one row per unit, and every drop
     gives the share dropped and the label shares before and after. **LEAK-42** (Should; draft PR #62): three tests
     set the verdict: a link above a chance rate that keeps the data's structure, a label that travels with the link
     beyond what the shared features predict, and an order.

   **Andrej (2026-11-11, change):** Agree. Option B: Drop the second copy.

   **Resolved (2026-11-11, Andrej):** B: `drop_duplicates()` in `_clean`, 583 to 570 rows (406 liver patients, 164
   others); the note on natural duplicates replaced by the check. In the UCI file each pair sits on adjacent rows (19/20
   to 201/202), a record entered twice; the 4 to 393 rows apart above were positions in the shuffled container.
   `dataset check` passes, the `dataset_duplicate_rows` warning is gone.

4. **Time basis: if kept, name the random split a `StationaryRelation`?**

   * **Problem:**
     - Each record holds age, sex and one liver blood panel with the diagnosis it accompanies, so the target is a present state; neither UCI nor the cited paper gives the hospital, the period or how the two groups were drawn, and the file keeps no date and no order that could be time.
     - The record has no collection facts yet (issue 5), and with the time lost a stationary relation can only be argued: how liver disease shows in bilirubin, enzymes and albumin does not move over a few years, beyond the share of patients and the referral practice.
     - Name the random split a `StationaryRelation`, argued from the source, or a `ForcedIIDFromTemporal`?
   * **Background:**
     - The file was donated to UCI on 20 May 2012 (Ramana et al. 2012); its order mixes the classes: 226 label runs over 583 rows, a lag-1 correlation of the label of 0.054 and a patient share of 0.64 to 0.84 in every tenth (arrival study, 2026-11-04).
     - The prototypes, by the rule's questions: liver disease comes and goes, so not `Timeless`; the use case refers later patients, so not a `Snapshot`; the records share no prediction moment, so not a `DelayedTarget`; a present state read from the same panel, so a `StationaryRelation`[^4a].
   * **Unknown:** whether the two groups were collected in different periods or places; then the label would mark the collection rather than the liver, as in hepatitis_c_prediction. The number-format probe finds no recording difference between them (ROC AUC 0.502, issue 1), which is the only test the file allows.
   * **Effect on the task:** none on the data or the scores; the tag and its line state why a random split stands for the use case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, `StationaryRelation` (implemented) | the shipped split; once PR #50 is in, the tag and a `Time basis:` line | the diagnosis and every feature come from one panel | argued from a source that states neither period nor design |
     | B | Random split, `ForcedIIDFromTemporal` | the same split, tagged as forced from temporal[^4b] | says that later patients are not tested | nothing found that moves the relation; the file has no time for the leak test the forced tag asks for |

   * **Recommendation:** A, if issue 1 keeps the dataset: the label and the panel come together, and no order or date suggests a period. **Decision:** A or B?

   **Notes for the AI:** on A, once PR #50 is in: `data_tags = ("StationaryRelation",)` and a curation bullet `- Time
   basis: StationaryRelation: each record is one liver panel with the diagnosis it accompanies, from north-east Andhra
   Pradesh over an unstated period (UCI, 2012). The file keeps no date and its order mixes the classes (226 label runs
   over 583 rows), so this is argued from the source, not measured; whether the two groups were collected in different
   periods is unknown.` No `splits_comment` change. On B, `data_tags = ("ForcedIIDFromTemporal",)` and a bullet saying
   that dated records would allow a split by period.

   [^4a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     collection facts, and a definition can name the use-case prototype it follows with a `Time basis:` line. A
     present state read through a relation that time does not move, beyond prevalence and practice, is a
     `StationaryRelation`, measured on a dated source and argued from the source when the time is lost.
   [^4b]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime, tagged as forced from temporal, after a leak test across the split; the definition says
     what a timestamp would change.

   **Answer (AI, 2026-11-06):** `StationaryRelation` now needs a measurement: if kept, name the random split forced from
   temporal (a, the issue's B), or leave it without a prototype (b)?

   * **Problem:**
     - On the item "One meaning for `StationaryRelation`, measured or argued?" you wrote "I want this to be always
       measured": the tag now needs a dated source on which the target and its relation to the features are shown flat,
       so option A, argued from the source, no longer exists[^4s].
     - Neither UCI nor the cited paper gives the period, the file keeps no date and no order that tracks time, and no
       parent source dates the records (none published), so the relation cannot be measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split, `ForcedIIDFromTemporal` | the issue's B: the tag and a `Time basis:` line saying the records span an unstated period and the time is lost; dated records would test later patients and whether the two groups were collected in different periods | the regime the rules give a forward use case whose time is lost | the leak test can check repeats and hidden groups, not periods |
     | b | Random split, no prototype | a `Time basis:` line saying why none fits, no tag | claims nothing | `dataset check` keeps noting the missing basis |

   * **Recommendation:** a, if issue 1 keeps the dataset. **Decision:** a or b?

   [^4s]: **SPLIT-32** (Should; Andrej, 2026-11-06): a `StationaryRelation` is always measured on a dated source; where
     time is lost it cannot be, and a forward use case takes the forced tag. **SPLIT-8** (Must): the forced split ships
     after its leak test, and its line names the reason and what a dated release would change.

   **Andrej (2026-11-11, discuss):** Measure it.

   **Answer (AI, 2026-11-11):** holding out by file position, the only order the file keeps, costs nothing: name the
   random split forced from temporal with this test in its line (a)?

   * **Problem:**
     - The file order is the closest thing to time (the copies of issue 3 sit on adjacent rows, as in entry order), so
       the test holds out the last third and each third of the 570 rows, as for account_debt_south_africa.
     - The last third scores as well as random test sets of the same size, for every model; only the middle third is
       harder, and it differs in case mix (younger, lower bilirubin, fewer patients), not in the relation.
     - The position is not a known date, so this does not measure a `StationaryRelation`; it is the leak test the
       forced tag asks for.

     | ROC AUC (570 rows, test 190) | logistic (log labs) | random forest | TabPFN 3.5 |
     |---|---|---|---|
     | Random, same size (20 repeats, mean ± sd) | 0.751 ± 0.021 | 0.730 ± 0.018 | 0.754 ± 0.022 |
     | First two thirds to last third | 0.779 | 0.760 | 0.753 |
     | First third held out | 0.760 | 0.733 | 0.749 |
     | Middle third held out | 0.710 | 0.686 | 0.698 |

     | Third of the file | 1 | 2 | 3 |
     |---|---|---|---|
     | Patient share | 0.747 | 0.674 | 0.716 |
     | Mean age | 48.2 | 41.6 | 44.7 |

     Telling the last third from the rest by its features: ROC AUC 0.60 (logistic and forest), a mild case-mix drift.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split, `ForcedIIDFromTemporal` | the tag and a `Time basis:` line: time lost, held out by file position the scores hold (table above); dated records would test later patients | measured as far as the file allows | the file order is not a stated date |
     | b | Random split, no prototype | a `Time basis:` line saying why none fits | claims nothing | `dataset check` keeps noting the missing basis |

   * **Recommendation:** a, if issue 1 keeps the dataset. **Decision:** a or b?

   Script and results: `~/claude_jobs/marks_1111/indian_liver_patient_dataset/order.py`, `order.csv` (CPU job 1377367).

   **Andrej (2026-11-11, discuss):** Reply (a): Random split, ForcedIIDFromTemporal. Measure it.

   **Answer (AI, 2026-11-11):** measured again with folds along the file order: the order carries batches of similar
   patients, not label runs, and holding it out costs nothing beyond the random spread.

   * Neighbouring rows resemble each other in age and labs (lag-1 correlation 0.10 to 0.26, every one beyond 2,000
     shuffles), so the file was entered in batches; the label does not run in blocks (0.03, p = 0.42).
   * Contiguous 5-fold scores sit inside the range of ten shuffled 5-folds for all three models.

     | ROC AUC (570 rows) | logistic (log labs) | random forest | TabPFN 3.5 |
     |---|---|---|---|
     | Shuffled 5-fold, 10 repeats: mean (min to max) | 0.754 (0.743 to 0.760) | 0.731 (0.711 to 0.746) | 0.755 (0.734 to 0.766) |
     | Contiguous 5-fold (file order) | 0.753 | 0.731 | 0.740 |

   Script and results: `~/claude_jobs/marks_1111/indian_liver_patient_dataset/r2/order2.py`, `order2.csv`,
   `order2.csv.ac.csv` (CPU job 1378044).

   **Resolved (2026-11-11, Andrej):** a: `data_tags = ("ForcedIIDFromTemporal",)` and a `Time basis:` bullet in
   `curation_comments` (time lost; held out by file position the scores stay within the random spread; a dated
   release would test later patients and whether the two groups came from different periods). `dataset check` passes.

5. **Correct the record's collection facts?**

   * **Problem:**
     - The record carries no collection fact, while every other record of this batch says how its samples arrived.
     - The records are patients seen over an unstated period in north-east Andhra Pradesh, and the file keeps no date, visit number or order that tracks time.
     - Add `Samples: Over Time` and `Time: Lost`?
   * **Background:** an extract of hospital records is a series of patients seen over time, not one moment; no target fact, since the diagnosis comes with the panel[^5a].
   * **Effect on the task:** none; the facts describe the source.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No facts (implemented) | the record unchanged | none found | the record does not say how the samples arrived |
     | B | `Samples: Over Time` and `Time: Lost` | two tags added | states the arrival as far as the source shows it | the period itself stays unknown |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, add `'Samples: Over Time'` and `'Time: Lost'` to the record's `tags`, and `Andrej` to
   `checked_by` if absent.

   [^5a]: **SPLIT-32** (Should): the record describes the source by independent collection facts: `Samples: One
     Moment` for one extract, census, scrape or exam round, `Samples: Over Time` when the samples arose over a period;
     `Time: Lost` when neither the release nor its source keeps or lets us recover the time; no target fact when the
     target exists with the features.

   **Andrej (2026-11-11, change):** Option B: Samples: Over Time and Time: Lost.

   **Resolved (2026-11-11, Andrej):** B: `Samples: Over Time` and `Time: Lost` added to the record's `tags` (also in
   the PR #50 worktree's copy of the record); `Andrej` already in `checked_by`.

## Reference

The original dataset was first proposed by Ramana et al. (2012) as a critical comparison of patients across USA and India:
Ramana, Bendi & Surendra, M & Babu, Prasad & Bala Venkateswarlu, Nagasuri. (2012). A Critical Comparative Study of Liver Patients from USA and INDIA: An Exploratory Analysis. International Journal of Computer Science. 9.
