---
unique_name: diabetes_130_us
name: Diabetes130US
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Inferred'
- 'Target: Later'
- 'Entities: Recur'
original_source: UCI
year: '2014'
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=4541
- https://doi.org/10.24432/C5230J
notebook_path: datasets/beyond_iid/old_iid/diabetes_130_us/diabetes_130_us.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/diabetes_130_us/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Cleaned to the paper's cohort: first encounter per patient, no deaths or hospice discharges.** Strack et al. 2014 (BioMed Research International, 781670), Sec. 2.3: "we considered only the first encounter for each patient as the primary admission" and "we removed all encounters that resulted in either discharge to a hospice or patient death, to avoid biasing our analysis", leaving 69,984 encounters. Our definition already kept the first encounter per patient (each patient's encounters appear in encounter_id order in the raw file; the sort is now explicit) but kept 1,084 "Expired" encounters (all "No": the dead cannot be readmitted; pure-value scan 2026-09-30) and 461 hospice discharges (16 readmitted). Now: discharge codes 11, 13, 14, 19, 20, 21 removed; 69,973 rows (paper: 69,984). Also "?" and "NULL" are now missing values.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Not sure if date is available, encounter_id might be sorted by date. Generally an interesting tabular data task. Same patients are in the dataset - need to account for that with preprocessing. Task has temporal nature, but features should be time invariant

Lennart: After preprocessing (handling duplicated patiens, handling one-hot encoded categories, ...)

Andrej: Requires proper preprocessing and handling of duplicate patients before inclusion

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — the first publication is an explanatory logistic regression with no predictive score.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 4 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `age`, `weight`, `max_glu_serum`, `A1Cresult` (the README lists their levels); left unordered: `metformin` (a level outside the scale is a state of its own); `repaglinide` (a level outside the scale is a state of its own); `nateglinide` (a level outside the scale is a state of its own); `chlorpropamide` (a level outside the scale is a state of its own); `glimepiride` (a level outside the scale is a state of its own); `glipizide` (a level outside the scale is a state of its own); `glyburide` (a level outside the scale is a state of its own); `pioglitazone` (a level outside the scale is a state of its own); `rosiglitazone` (a level outside the scale is a state of its own); `acarbose` (a level outside the scale is a state of its own); and 3 more.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 13 columns with a state outside the scale ordered, the state placed by the rule.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship, tagging the random split ForcedIIDFromTemporal: encounter_id orders each patient's stays in time and tracks recording changes across the file, while the 30-day label is not censored at the end. Priority 3: gap 0, use case 0, source 1, shape 1, risk -0.

CC (2026-11-11, Andrej): **Every stay, split in windows of encounter order; the 30-day target kept.** Review page marks, issues 1 (d) and 2 (A).
- Split: `encounter_id` is the Health Facts warehouse's running number of encounters and runs as a calendar across all hospitals (the distance to a patient's next stay tells a `<30` label from a `>30` one, ROC AUC 0.89, and gives 9.3 years over the file for 1999-2008), so the task gets 9 windows of 5,519 stays on `time_index` = encounter_id // 6, each trained on every earlier stay (50.0% to 94.4%), no gap (fixed 30-day horizon; a 30-day gap changed 0.654 to 0.652).
- Rows: every stay instead of the first per patient (99,343 stays of 69,990 patients; deaths and hospice discharges still out). In windows the first stays are a group that narrows over time (30-day rate 9.9% down to 6.4%), every stay holds at 10.8% to 11.3%; a hospital scores every discharge and knows a returning patient's earlier stays. This replaces the first-stay part of the cohort decision of 2026-09-30.
- Cost against random folds (untuned LightGBM, ROC AUC): 0.654 against 0.662 over every stay, 0.625 against 0.643 on the first stays.
- Target: 30 days against the rest stays; `>30` has no horizon (the oldest stays were followed about nine years longer) and the three classes add nothing to the 30-day ranking (0.644 against 0.643).
- The 130 hospitals are not recoverable (no copy has a hospital id; recording habits mark 14.6% of the stays).
- `problem_type` corrected to Binary Classification (it was Multiclass Classification; the definition predicts `<30` against the rest).

CC (2026-11-11, Andrej): **Temporal split kept; tags `Time: Inferred` and `Entities: Recur`.** Asked whether returning patients make the split something between temporal and random, or need a new split type.
- The order is a calendar for every stay, not only within a patient: troglitazone (withdrawn March 2000) is only in the first 0.1% of stays in encounter order, the combination drugs appear in the order of their approval (2002 at 40% and 85%, 2005 at 97%), rosiglitazone falls in the newest fifth (2007 safety warning), and first stays alone show the recording change (payer code missing in all of the oldest fifth).
- Returning patients (22% to 37% of the test stays) are a fact of the data, recorded as `Entities: Recur`; SPLIT-13 makes them part of the task, since a hospital scores every next discharge. No new split type: the cut is in time either way.
- `Time: Dated` corrected to `Time: Inferred`: the stays carry no dates, only the running encounter number.

## Review

**Outcome:** added. The Diabetes 130-US hospitals table (UCI 296, https://doi.org/10.24432/C5230J; Strack et al.,
"Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records",
BioMed Research International 2014:781670, https://doi.org/10.1155/2014/781670): every hospital stay of diabetic
patients at 130 US hospitals, 1999-2008 (99,343 stays of 69,990 patients since 2026-11-11; the first stay of 69,973
patients before), and whether they were readmitted within 30 days; 9 windows in encounter order, the order being a
calendar across hospitals (issue 1 d, decided 2026-11-11; random splits before), ROC AUC (fallback).
Reviewed on 2026-11-04 without a panel, from the gathered evidence (the record, the CHANGELOG, a model run on TabArena
v0.1's copy) and two checks. Validity: the cohort follows the paper (first stay per patient, no deaths or hospice
discharges; Lennart, 2026-09-30); every feature is recorded by discharge and none is the outcome; but the encounter
order carries time, which the random split ignores (issue 1); the 30-day label is not cut short at the end of the file
(checked). Value: on TabArena v0.1's copy (71,518 rows, deaths and hospice stays still in) the benchmark methods spread
from 1 - ROC AUC 0.317 (TabPFN-3.5) over a median of 0.339 to 0.352 for default logistic regression and 0.458 for
default k-nearest neighbours; the v0.2 cohort was not run, and a hard task (ROC AUC near 0.68) with a real spread is
expected to stay. Quality: missing codes, decoded ids and the drug-change scales settled (2026-09-30 to 2026-10-31).
Weighed: a large clinical database with a documented cohort +, a real spread +, no dates and a cohort that shifts along
the encounter order -.

**Main points:** Issue 4: Keep `time_index` as a model input? Decided on 2026-11-11: every stay in 9 windows of encounter order (issue 1 d) and the 30-day
target (issue 2 A); `problem_type` set to Binary Classification. Issue 3 (same day): the split stays temporal with
returning patients in the test, the order dated by the drugs, record tags `Time: Inferred` and `Entities: Recur`.
Nothing open.

**Record judgment:** valid. The cohort decision of 2026-09-30 is settled and matches the paper (69,973 rows against
69,984). The TabArena notes ("encounter_id might be sorted by date", "task has temporal nature") are borne out by issue
1.

**Issues for Andrej:**

1. **Tag the random split as forced from temporal, now that the encounter order turns out to carry time?**

   * **Problem:**
     - The definition says the stays carry no dates, but `encounter_id` orders each patient's stays in time and tracks
       changes in the recording across the file.
     - A hospital trains a readmission model on past discharges and scores the next ones, so the task is temporal by
       its use case, and a hidden time index does not make it random[^1a].
     - Keep the random split untagged, tag it as forced from temporal with a note, or split in encounter order?
   * **Background:** the curation notes already saw "a distribution shift based on the original order", with
     `payer_code` driving it, and let the shuffle remove it. The forced tag tells a benchmark user that the random
     score stands in for a temporal one[^1b].
   * **Experiments:** on the raw UCI file (checks, no model):
     - Within a patient: of 30,248 pairs of consecutive stays in `encounter_id` order, the later stay counts more
       inpatient visits in the year before in 22,304 and fewer in 2,983; after a readmission within 30 days, more in 94%.
     - Across the file (tenths of the v0.2 cohort in `encounter_id` order): no payer code in the oldest two tenths,
       then 75%, 33% to 13% missing; at most 9 diagnoses per stay until the newest fifth, then up to 16; readmission
       rate 9.0% to 10.5% in the first seven tenths, 8.2%, 7.9% and 5.5% in the newest three.
     - Censoring: over all 101,766 stays the 30-day readmission rate stays at 10% to 11.5% to the end of the file,
       while readmission after more than 30 days falls from 36% to 26%; so the 30-day label is complete, and the
       cohort's drop comes from first stays late in the file being patients new to the system.
   * **Unknown:** whether the order is calendar time or the order in which hospitals entered the database; the release
     has neither dates nor hospital ids, so windows by order could test a change of hospital as much as of time.
   * **Consistency:** follows the snapshot and relative-date tables that ship random but tagged (mobile_churn,
     bank_customer_churn, home_credit_default_risk).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, untagged (implemented) | 3 x 3 random folds | none found | presents a temporal task as random; the notes call the order shift an anomaly |
     | B | Random, tagged forced | `ForcedIIDFromTemporal`; a note gives the order evidence and says a dated release would allow windows | follows the rule; keeps the paper's cohort and all rows | the score still mixes ten years of care |
     | C | Windows in encounter order | rows sorted by `encounter_id`, three windows from the newest half | tests on later stays, as a hospital would | the order may be hospital loading, not time; first stays late in the file are a shifted group |

   * **Recommendation:** B: the order is clearly time within a patient but not proven as a calendar across hospitals,
     so the forced tag with the evidence is the safe statement. **Decision:** untagged (A), tagged forced (B) or
     windows in encounter order (C)?

   **Notes for the AI:** on B, `data_tags = ("ForcedIIDFromTemporal",)` as in `bank_customer_churn`; replace the
   `Anomaly:` note on the order with the evidence above and "encounter_id is chronological within a patient and tracks
   recording changes across the file; a release with dates would allow windows"; `fit_reason` keeps its sentence on
   1999-2008; `dataset check`. On C, a row-order time index from the sorted `encounter_id` (kept as split metadata,
   never a feature), three windows of a sixth of the rows from the newest half, and the drift of the newest first stays
   in the notes. Record field: `problem_type` per the field row.

   [^1a]: **SPLIT-7** (Must): a missing or hidden timestamp does not make a task IID. **SPLIT-22** (Should): the raw file
     order can be the time order without a timestamp.
   [^1b]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime that keeps the rows, tagged as forced from temporal, saying what a dated window would change.

   **Andrej (2026-11-05, discuss):** We need more analysis on this: Is it possible to recover the 130 hospitals somehow?

   Also, how much does the temporal order matter for prediction?

   How were the duplicated patients treated in previous versions of the benchmark?

   **Answer (AI, 2026-11-06):** Split in windows of encounter order and keep every stay of a patient, now that the
   order is shown to be a calendar across all hospitals?

   * **Problem:**
     - `encounter_id` is the Health Facts warehouse's running number of encounters, and the readmission labels show it
       runs as a calendar across all hospitals (9.3 years from the first stay to the last, for the source's 1999-2008),
       so the release has a time axis and the forced tag recommended on 2026-11-04 no longer fits[^1c].
     - In windows, the paper's first stay per patient becomes a group that changes with time (the 30-day rate falls
       to 6.4% in the newest window, against 9.9% in the oldest half), while over every stay it holds at 10.8% to 11.3%.
     - Windows over first stays, windows over every stay, or one of the random options?
   * **The order is a calendar (decisive):**
     - `encounter_id` is 6 times a running number (6n + 2 for the newest 11% of stays, after a change of the id
       scheme), and the number ends at 73,977,870, close to the paper's 74,036,643 encounters in the whole database;
       `patient_nbr` is 9 times a running patient number in the same way.
     - The distance in that number from a stay to the same patient's next stay tells a `<30` label from a `>30` one
       (ROC AUC 0.89; 0.92 to 0.96 within each of the first four fifths of the file). Thirty days span about 400,000
       numbers early in the file and 1,100,000 late, as the warehouse grew; summed over the file, the 30-day scale
       gives 9.3 years from the first stay to the last (9.1 to 9.6 over 20 bootstrap draws).
     - Had hospitals been loaded one after another, 30 days at one hospital would span far fewer numbers, and many
       stays readmitted after more than 30 days would show shorter distances than stays readmitted within 30 days;
       under 0.2% are shorter than the median 30-day distance in the first four fifths (2.1% in the last).
     - The change of the id scheme falls on the first stay with more than 9 diagnoses (estimated year 7.4): one change
       of the warehouse at one point in time, not a hospital.
   * **First question, the 130 hospitals:** not recoverable, neither exactly nor as clusters a split could rest on.
     - No copy has a hospital id: not UCI, OpenML 4541 or 43874, nor the R package `readmission`. The paper
       names 130 hospitals and delivery networks for the extract (its regions add up to 120) and says the 70,000
       admissions of its cohort came from 54 hospitals.
     - Neither id carries the hospital: the running numbers interleave the hospitals (above), and a patient's number
       follows when they first appeared (Spearman 0.51 with their first stay).
     - Recording habits are hospital properties but mark few hospitals. Health Facts keeps a patient's stays within one
       health system, and a patient's next stay repeats a habit far more often than the next row in encounter order
       (another patient on the same days): weight recorded 93% against 4.7% (3.1% of all stays), admission source
       coded as unknown 95% against 16% (6.9%), glucose tested 89% against 12% (5.3%), race missing 74% against 4.6%
       (2.2%). At least one of these flags marks 14.6% of the cohort; the rest carry none, so clusters on habits would
       be a guess[^1d].
     - Health Facts (Cerner, now Oracle) knows each stay's hospital, as the paper's counts by region and bed size
       show; only its licensees, such as the authors at Virginia Commonwealth University, could add it.
     - For the use case it would be a feature, not a reason to split differently: a hospital scores its own next
       discharges, so the hospital of a new stay is known, as it is for every training stay.
   * **Second question, how much the order matters:** 0.018 to 0.025 ROC AUC on the v0.2 cohort, three to four times
     the spread between random splits, and a third of that over every stay; the models keep their order.
     - Three windows of 11,662 first stays from the newest half (estimated years 4.9 to 5.7, 5.7 to 7.0 and 7.0 to
       9.3), each trained on all earlier stays, against random splits of the same sizes (3 draws per window); small
       fixed models, so only the differences count (the benchmark methods reached up to 0.68, median 0.66, on v0.1's
       copy):

       | Rows | Model | Random 3 x 3 | Windows | Windows, mean | Random, same sizes | Cost |
       |---|---|---|---|---|---|---|
       | First stays (v0.2) | LightGBM | 0.642 | 0.634, 0.617, 0.625 | 0.625 | 0.643 | -0.018 |
       | First stays (v0.2) | Logistic regression | 0.651 | 0.649, 0.623, 0.633 | 0.635 | 0.654 | -0.019 |
       | First stays (v0.2) | TabPFN 3.5, 10,000 training rows | 0.661 (3 folds) | 0.642, 0.626, 0.638 | 0.635 | 0.660 | -0.025 |
       | Every stay (99,343) | LightGBM | 0.661 | 0.646, 0.659, 0.658 | 0.654 | 0.662 | -0.007 |
       | Every stay (99,343) | Logistic regression | not run | 0.657, 0.655, 0.664 | 0.659 | 0.664 | -0.005 |

     - TabPFN ran on 10,000 training rows and 8,000 test rows per split, one random draw per window; on the same rows
       it leads LightGBM and logistic regression by 0.02 to 0.04 in random folds, in windows and in the random splits
       of window size alike (windows: 0.635 against 0.601 and 0.612).
     - A model tells the newest half of the cohort from the oldest with ROC AUC 0.92, `payer_code` giving a third of
       the gain; without payer code, diagnosis count and glucose test (the recording changes) still 0.87, on specialty,
       admission source, discharge and diagnoses; random halves 0.50.
     - The position in the file as a feature adds 0.006 to LightGBM on random splits (0.642 to 0.648).
     - A gap of 30 days before each window, for the labels not yet known at its start, changes nothing (0.625 with and
       without; over every stay 0.652 and 0.654)[^1f].
     - Within a patient: v0.2 keeps one stay per patient, so no patient crosses a split. Over every stay, a random
       split puts 38% of the test patients in training and scores as a split by patient does (0.661 both): a
       patient's other stays leak nothing these features can use.
   * **Third question, earlier versions:** first stay only, deaths kept, random folds, no grouping.
     - TabArena v0.1 (OpenML dataset 46922, task 363630, 71,518 rows) and BeyondArena ran one notebook, with the same
       container checksum: `df = df.drop_duplicates(subset="patient_nbr")`, noted as "We drop duplicated patients based
       on the "patient_nbr" feature to avoid target leakage." The file lists each patient's stays in encounter order,
       so this kept the first stay. Stays ending in death or a hospice stayed in (1,084 and 461), and the split was
       3 x 3 random stratified folds, tagged `IID`.
     - v0.2 keeps the same first stay (the sort is now explicit) and drops deaths and hospice discharges, as the paper
       does (69,973 rows)[^1g].
     - Other copies: OpenML 4541, the record's source link, holds all 101,766 stays with the three-way `readmitted` as
       target and both ids as ordinary features; Fairlearn's copy (OpenML 43874) holds all stays with the 30-day
       target and no patient id; TableShift, without a hospital as well, holds out emergency-room admissions as its
       shifted domain.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random, untagged (implemented) | 69,973 first stays; 3 x 3 random folds | the paper's cohort; as v0.1 | ignores a time axis the release has |
     | b | Random, tagged forced from temporal | as a, with `ForcedIIDFromTemporal` and the evidence in a note | the paper's cohort; says the score stands in for a temporal one | the tag is for a release that cannot give windows, and this one can |
     | c | Windows of first stays | 69,973 first stays in encounter order; 3 windows from the newest half | the paper's cohort; tests on later stays, as a hospital would | late first stays are patients without an earlier stay, a group that narrows over the years; 30-day rate 9.3%, 8.3%, 6.4% in the windows |
     | d | Windows of every stay | 99,343 stays (deaths and hospice still out); 3 windows from the newest half; a patient's earlier stays train as history | every discharge, as the use case scores them; a steady 30-day rate (11.3%, 11.2%, 10.8%); 29,370 more rows | departs from the paper's cohort and from the decision of 2026-09-30; 23% of the test stays have a patient seen in training |

   * **Recommendation:** d: a hospital scores every discharge and knows a returning patient's earlier stays, and only
     every stay gives windows whose rate does not move with the cohort rule; the paper kept first stays for the
     independence its logistic regression assumes, not for the task[^1e]. **Decision:** a, b, c or d?

   **Notes for the AI:** on d: `_clean` drops the first-stay filter, keeps the sort and applies the death and hospice
   filter to every stay (99,343 rows, 69,990 patients); a `time_index` of `encounter_id // 6` as the `Temporal`
   column, `TemporalSplits(unit="rows", ...)` with 3 windows of 16,557 rows, or 9 of about 5,500 as
   loan_default_prediction_imperial_college has for the same size (SPLIT-15); no gap, with the measured 0.002 in the
   notes (SPLIT-10 as amended on 2026-11-05: a fixed 30-day horizon). `patient_nbr` stays out of the features; adding a
   patient's earlier stays as features (their count in the file, the last stay's label) is what USE-10 allows, a step
   to measure separately. task_summary: `row`, `split`, `changes`, `fit_reason` (the order is time; every stay);
   curation notes: replace the `Anomaly:` bullet with the calendar evidence above and the first-stay bullet with the
   reason for every stay; README regenerated; `dataset check`; CHANGELOG. On c: the same `Temporal` over the first
   stays (3 windows of 11,662 rows or 9 of about 3,900) and the narrowing first-stay group in the notes. On b: as the
   notes for the AI above. The record's `problem_type` follows its field row in every case.

   [^1c]: **SPLIT-22** (Should): the raw file order can be the time order without a timestamp; keep it. **SPLIT-7**
     (Must): a hidden timestamp does not make a task IID. **SPLIT-8** (Must) forces a split only when the release
     cannot give the windows **SPLIT-14** (Must) asks for: at least 3, none trained on less than half of the data.
   [^1d]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data, never on a
     similarity cluster. **SPLIT-25** (Must): when the real groups matter and cannot be recovered, retire rather than
     group on a guess, and note that the authors could be asked. **SPLIT-4** (Must): if new rows keep having the value,
     the column is a feature and the split stays.
   [^1e]: **USE-11** (Must): when the use case is the first event of each entity, one row per entity makes it an IID
     task; take one row per entity only when the use case is that row, as it loses rows and signal. **USE-10** (Must)
     and **LEAK-34** (Must): a known entity's own history under a temporal split is legitimate.
   [^1f]: **SPLIT-10** (Should; amended 2026-11-05): no gap where a fixed outcome horizon removes the selection by the
     outcome; the notes give what the newest training labels add at equal training size.
   [^1g]: **LEAK-22** (Must): when the cohort holds rows that cannot have the outcome, follow the paper's cohort.

   **Answer (AI, 2026-11-06):** With three valid windows a random split here is no longer forced: windows of every stay (d), windows of first stays (c), or random first stays with no time-basis tag (a)?

   * **Problem:**
     - The release carries a global time order (`encounter_id`, a calendar across all hospitals, answer above) and a hospital scores its next discharges, and a random split leaves that time unused with no time-basis tag to name, since the first stays' 30-day rate moves and the windows cost 0.018 ROC AUC[^1h].
     - Option b falls away: the forced tag stands for a forward use case with no usable time or too few periods, while this release gives three windows with every training side above half of the rows[^1i].
     - Windows of every stay, windows of first stays, or the random first stays with no time-basis tag?
   * **Measured cost** (the runs of the answer above; three windows from the newest half, each trained on every earlier row; untuned models, ROC AUC):
     - First stays: the newest window scores 0.625 against 0.642 on the random folds (LightGBM; logistic regression 0.633 against 0.651), and the three windows 0.625 on average against 0.643 for random splits of the same sizes.
     - Every stay: the newest window scores 0.658 against 0.661 on random folds (LightGBM; the three windows 0.654 against 0.662).
   * **How the target moves:** the 30-day rate of first stays falls from 9.9% in the oldest half to 9.3%, 8.3% and 6.4% in the three windows (oldest first); over every stay it holds at 11.3%, 11.2% and 10.8%.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random first stays (implemented), no time-basis tag | 69,973 first stays, 3 x 3 random folds; no use-case prototype named (`StationaryRelation` is not shown: the first stays' 30-day rate falls from 9.9% to 6.4% and the windows cost 0.018; three valid windows, so no forced tag) | the paper's cohort; the compromise is stated with its size | 0.017 above the newest window; leaves a recovered calendar unused |
     | c | Windows of first stays | 69,973 first stays in encounter order; 3 windows from the newest half | the paper's cohort; tests later stays, as a hospital would | the first-stay group narrows over the years (30-day rate 9.3% to 6.4%) |
     | d | Windows of every stay | 99,343 stays (deaths and hospice still out) in encounter order; 3 windows from the newest half | every discharge, as the use case scores them; a steady 30-day rate; costs 0.003 against random | departs from the paper's cohort and from the decision of 2026-09-30 |

   * **Recommendation:** d, as above: the time is there, and only every stay gives windows whose rate does not move with the cohort rule; a remains possible, now as a split with no time-basis tag rather than a forced one. **Decision:** a, c or d?

   **Notes for the AI:** on c or d, as in the notes above; a temporal split carries no time-basis tag; record tag `Non-IID (Temporal)` and `required_split` `Temporal (NON-IID)`. On a: no time-basis tag in `data_tags` (the data has no date column, so no `meta_time_present_unused` to accept); the curation note "- Time order: `encounter_id`, the Health Facts warehouse's running number of encounters, orders the stays in time across all hospitals (1999-2008); the split leaves it unused: the newest of three windows in encounter order scores ROC AUC 0.625 against 0.642 on random folds (untuned LightGBM; logistic regression 0.633 against 0.651)", followed by the reason of your decision; replace the `Anomaly:` note as in the notes for b; `dataset check`. Under every option the record gets the tags `Samples: Over Time` and `Time: Dated`.

   [^1h]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection facts and, where one fits, the definition's use-case prototype with its `Time basis:` line.
   [^1i]: **SPLIT-8** (Must, reworded 2026-11-05 and 2026-11-06): the forced tags cover a forward use case whose release has no usable time or too few periods for the windows **SPLIT-14** (Must) asks for (at least 3, none trained on less than half of the data).

   **Andrej (2026-11-11, discuss):** Reply (d): Windows of every stay.

   **Resolved (2026-11-11, Andrej):** d: windows of every stay. Applied as the notes for d draft:

   * `_clean` keeps every stay (no first-stay filter; deaths and hospice still out): 99,343 stays of 69,990
     patients. `time_index` = `encounter_id // 6` is the `Temporal` column; `patient_nbr` stays out.
   * 9 windows of 5,519 stays (the SPLIT-15 choice of the notes, as loan_default_prediction_imperial_college), each
     trained on every earlier stay, no gap:

     | Window (newest first) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
     |---|---|---|---|---|---|---|---|---|---|
     | Train share | 94.4% | 88.9% | 83.3% | 77.8% | 72.2% | 66.7% | 61.1% | 55.6% | 50.0% |
     | 30-day rate | 11.3% | 10.4% | 10.6% | 11.4% | 11.1% | 11.0% | 11.0% | 11.7% | 11.1% |
     | Test stays with the patient in training | 37% | 30% | 31% | 33% | 31% | 31% | 28% | 27% | 22% |

   * task_summary (`row`, `split`, `changes`, `fit_reason`), `splits_comment` and curation notes updated (calendar
     evidence replaces the `Anomaly:` bullet, every-stay reason replaces the first-stay bullet); README regenerated;
     `dataset check` passed (0 errors, 0 warnings, 27 checks); `acarbose` gains the level Down, which only 3 later stays hold. Record: `required_split` Temporal (NON-IID), tag
     `Non-IID (Temporal)`, CC line; `Samples: Over Time` and `Time: Dated` were already there.
   * Not done, a step to measure separately: a patient's earlier stays as features (USE-10).

2. **Keep the target as readmission within 30 days, or use more of the source's three outcomes?**

   * **Problem:**
     - Only the source's `<30` has one horizon for every stay: `>30` counts a first readmission at any later time up to
       the end of the database's records, which the release does not date, so `>30` and `NO` mix how a patient fared
       with how long their stay was followed.
     - The candidates are 30 days against the rest (implemented, the paper's), the three classes, the three levels in
       order, any readmission against none, and a time to readmission.
     - Which target should the task predict?
   * **Background:** the codebook defines `readmitted` as "Days to inpatient readmission. Values: “<30” if the
     patient was readmitted in less than 30 days, “>30” if the patient was readmitted in more than 30 days, and “No”
     for no record of readmission"; the paper's outcome is readmission "within 30 days of discharge", the rest
     "covers both readmission after 30 days and no readmission at all", found "by examination of all patient records
     in the database to determine the first inpatient visit after discharge", and "30 days was chosen based on
     criteria often used by funding agencies" (Strack et al. 2014, Table 1 and Sec. 2.3). Medicare's Hospital
     Readmissions Reduction Program has penalised hospitals for excess readmissions within 30 days since October
     2012. Under every option, readmissions outside the patient's health system are missing ("data from
     out-of-network providers is not captured", Sec. 2.1). Shares in the v0.2 cohort: 59.3% `NO`, 31.8% `>30`, 9.0%
     `<30`.
   * **Effect on the task:** the use case decides at discharge who gets a call or an early visit, which acts on the
     next weeks, the span the 30-day measures were set for. A target with `>30` in it also scores how long a stay was
     followed, which a model can only read from where the stay sits in time, and a later window holds fewer `>30`
     than the model trained on.
   * **Experiments:** v0.2 cohort, 3 x 3 random folds (spread between splits about 0.005), small fixed LightGBM and
     logistic regression (LR); log-loss skill is 1 minus the log loss over the log loss of the training class shares;
     windows as in issue 1 (3 from the newest half, against random splits of the same sizes):

     | Target | Score | LightGBM | LR | Encounter position as a feature adds | Log-loss skill in the windows, against random |
     |---|---|---|---|---|---|
     | A, 30 days | ROC AUC | 0.643 | 0.652 | +0.006 | 0.021 against 0.035 |
     | A, 30 days | log-loss skill | 0.034 | 0.043 | | |
     | B, three classes | ROC AUC, each class against the rest, mean | 0.654 | 0.653 | | |
     | B, three classes | ROC AUC of P(`<30`) for 30 days | 0.644 | 0.651 | | |
     | B, three classes | log-loss skill | 0.053 | 0.053 | | 0.020 against 0.054 |
     | C, three levels in order | concordance of the expected level (B's model) | 0.652 (0.652) | 0.649 (0.648) | | |
     | C, three levels in order | ranked probability score (B's model; class shares 0.162) | 0.150 (0.150) | 0.151 (0.151) | | |
     | D, any readmission | ROC AUC | 0.668 | 0.664 | +0.025 | 0.026 against 0.065 |
     | D, any readmission | log-loss skill | 0.065 | 0.060 | | |

     - The labels reach past the extract: over every stay, `<30` holds at 10.5% to 12% in each estimated year (the
       calendar of issue 1) and is 8.8% in the file's last month, so the 30-day label is complete to the end; `>30`
       is 28% to 42% in the first seven estimated years and 25% to 30% in the last three, a shorter follow-up or
       another mix of hospitals, which the release cannot separate.
     - In the newest window any readmission is 28% of the stays, against 43% in its training rows, and its log-loss
       skill falls to 0.006 (0.059 at random); the three classes to 0.004 (0.052), 30 days to 0.030 (0.039).
     - The extra class does not help the 30-day ranking: P(`<30`) of a three-class model ranks as the binary model
       does (0.644 against 0.643 for LightGBM, 0.651 against 0.652 for LR, 0.660 against 0.661 for TabPFN 3.5 on
       10,000 training rows and 3 folds). The order adds nothing measurable either:
       two cumulative binary models (any readmission, then 30 days) give the same concordance and ranked probability
       score as the unordered three classes.
     - `<30` against `NO`, leaving out the `>30` stays, scores 0.688 and 0.690, higher only because the stays in
       between are gone; it chooses rows by their future and is no option.
     - A time to readmission needs days or dates, and the release has three bins; a time-to-event model could learn
       only the 30-day boundary, which A already is.
   * **Consistency:** the paper, TabArena v0.1, BeyondArena, Fairlearn's copy (OpenML 43874), TableShift and the R
     package `readmission` all predict 30 days; OpenML 4541 ships the three classes as its default target. Where
     follow-up ends on one date, our rule takes an outcome within a fixed horizon over the rows followed that long,
     as for cirrhosis_patient_survival_prediction[^2b]; here only the 30 days are such a horizon.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Within 30 days (implemented) | binary, 9.0% positive; ROC AUC (fallback) | one horizon for every stay, complete to the end of the file; the decision the use case and Medicare's penalties act on; the paper's target and every other copy's but one | the weakest signal of the options (ROC AUC 0.64 to 0.65); leaves the later readmissions unused |
     | B | Three classes | `NO`, `>30`, `<30`; multiclass log loss (fallback) | the source's whole label; OpenML 4541's target | `>30` has no horizon and its share moves with time; adds nothing to the 30-day ranking |
     | C | Three levels in order | `NO` < `>30` < `<30` as an ordered target; a ranked probability score, a new custom metric | uses the order of the levels | the order adds nothing measurable over B; the same horizon problem |
     | D | Any readmission | `<30` or `>30` against `NO`, 40.7% positive; ROC AUC (fallback) | the strongest signal (ROC AUC 0.67) | the oldest stays were followed about nine years longer than the newest; the position in time adds 0.025 ROC AUC; a readmission years later is not what the discharge decision acts on |
     | E | Time to readmission | a survival target | would use the timing | not possible: no days, no dates, three bins |

   * **Recommendation:** A: only the 30-day label has one horizon for every stay and is complete to the end of the
     file, it is the one a discharge decision acts on, and the richer labels add signal mostly about how long a stay
     was followed and none to the 30-day ranking[^2a]. **Decision:** A, B, C, D or E?

   **Notes for the AI:** on A: a bullet in the curation notes that the three-way `readmitted` was considered and why
   it stays binary (no horizon for `>30`, the numbers above); the record's `problem_type` follows its field row.
   On B: the target is `readmitted` unchanged, `problem_type` multiclass, `log_loss` as the fallback (MET-8); the
   task summary's `predicted` and the record's `problem_type` (Multiclass) follow; LEAK-4's probes run on the
   three classes. On C: an ordered target with levels `NO`, `>30`, `<30` (the ordinal convention of CLEAN-14) and a
   ranked probability score as a custom metric with its reference implementation (MET-13). On D: target
   `readmitted != "NO"`, ROC AUC. Under issue 1's option d the target counts per stay; the measurements above are on
   the first stays.

   [^2a]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it, and check how the
     source built its label before accepting it.
   [^2b]: **LEAK-23** (Must): a target over only the rows with the event, with follow-up ending on one date, becomes an
     outcome within a fixed horizon, over the rows followed that long (cirrhosis_patient_survival_prediction).
     **LEAK-24** (Must): a target right-censored in the newest periods is cut where follow-up is complete.

   **Andrej (2026-11-05, discuss):** Regarding the target type, let's discuss the options as a separate point since I
   believe this is not trivial and we could do a lot there.

   **Answer (AI, 2026-11-06):**

   * **Opened as its own point, as you asked:** this issue 2 holds the target-type options with their measured scores
     (above); issue 1 stays on the split.
   * **The decisive fact:** only the 30-day label has one horizon for every stay; `>30` is a readmission at any later
     time, and with no dates the oldest stays were followed about nine years longer than the newest.
   * **Measured** (v0.2 cohort, 3 x 3 random folds, LightGBM / logistic regression): A 30 days ROC AUC 0.643 / 0.652;
     B three classes macro ROC AUC 0.654 / 0.653, its 30-day probability ranks as A does (0.644 / 0.651); C ordered,
     the same as B; D any readmission 0.668 / 0.664, but its skill falls from 0.059 to 0.006 in the newest window.
   * **Choose:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Within 30 days (implemented) | binary, 9.0% positive | one horizon for every stay; the decision the use case acts on | the weakest signal |
     | B | Three classes | `NO`, `>30`, `<30` | the source's whole label | `>30` has no horizon; adds nothing to the 30-day ranking |
     | C | Three levels in order | `NO` < `>30` < `<30`, a custom ordinal metric | uses the order | nothing measurable over B; the same horizon problem |
     | D | Any readmission | `<30` or `>30` against `NO` | the strongest signal | follow-up length varies by years; breaks down in the newest window |
     | E | Time to readmission | a survival target | would use the timing | not possible: no dates |

   * **Recommendation:** A.

   **Andrej (2026-11-11, ok):** Reply (A): Within 30 days.

   **Resolved (2026-11-11, Andrej):** A: the target stays readmission within 30 days (binary, ROC AUC fallback). A
   curation-notes bullet records why the three-way `readmitted` stays binary (no horizon for `>30`, the numbers
   above); the record's `problem_type` is now Binary Classification. Under issue 1 d the target counts per stay
   (11.4% positive over every stay).

3. **Is the split really temporal, when returning patients make part of the test something seen before, or does it
   need a split type between temporal and random?**

   * **Problem:**
     - Under issue 1 d, 22% to 37% of each window's test stays belong to a patient with earlier stays in training, so
       the split could read as repeated entities appearing later rather than as time.
     - The calendar evidence of issue 1 rests on returning patients (the distance to a patient's next stay), so it
       cannot by itself tell a calendar from an order within each patient.
   * **Experiments:** on the raw UCI file, stays in `encounter_id` order with deaths and hospice discharges removed
     (99,343 stays; checks, no model):

     | Evidence | Real date | Position in encounter order |
     |---|---|---|
     | troglitazone | withdrawn March 2000 | 3 stays, all in the first 0.1% |
     | glipizide-metformin | approved October 2002 | from 40% |
     | metformin-rosiglitazone | approved October 2002 | from 85% |
     | metformin-pioglitazone | approved August 2005 | at 97% |
     | rosiglitazone | 2007 safety warning | about 770 stays a tenth, then 319 and 222 in the newest two tenths |
     | pioglitazone | approved July 1999 | 370 stays in the oldest tenth, rising to about 850 |
     | first stays only, payer code missing | recording change | 100% in the oldest two tenths, 9% to 19% in the newest four |

     The drugs and the first stays use neither the label nor a returning patient, so the order is a calendar across
     every stay. Share of stays that are a patient's first: 82% in the oldest tenth, 62% in the newest.
   * **Answer:** the split is temporal; the returning patients are a separate fact of the data. The split type says
     how train and test are cut (here in time); whether a test entity was seen in training is recorded as
     `Entities: Recur` (SPLIT-32), and SPLIT-13 decides it: part of the task when the model predicts for known
     entities. A hospital scores every next discharge, new and returning patients alike, so the mix is the use
     case[^3a]. The split between temporal and random that this suggests would be time plus holding the test entities
     out of training, a temporal split grouped by entity; it fits a use case of new entities only, not this one. No
     new split type.
   * **Consistency:** many temporal tasks have the same mix (clients in alfa_battle_2_0_task_2 and
     lt_vehicle_loan_default_prediction, policyholders in the Spanish motor and Wisconsin insurance tables, stores in
     rossmann_store_sales, stations in airqo and bias_correction), but only 10 records carry `Entities: Recur`
     (cross-dataset item on the page).
   * **Record:** `Time: Dated` was wrong under SPLIT-32: the stays carry no date, only the running encounter number,
     which is `Time: Inferred`; `Entities: Recur` was missing.

   [^3a]: **SPLIT-13** (Should): look for grouped structure inside a temporal task; an entity that recurs across the
     cutoff is part of the task when the model predicts for known entities, and a question when the use case is a new
     entity.

   **Andrej (2026-11-11, chat):** For diabetes 130 we mark the split as temporal, but it is more like repeated entities
   appearing later sometimes; not really temporal and not random, but something in between. Should we define a new
   split type?

   **Resolved (2026-11-11, Andrej):** temporal split kept, no new split type. Applied: record tags `Time: Inferred`
   (was `Time: Dated`) and `Entities: Recur`, a CC line; the curation notes' time-order bullet gains the drug dating,
   `splits_comment` says why the split stays temporal and not grouped (SPLIT-13). Not done: the window scores split by
   returning and new patients, which would measure the mix rather than describe it.

4. **Keep `time_index`, a reconstructed order, as a model input?**

   * **Problem:**
     - `time_index` is the warehouse's running encounter number (`encounter_id // 6`); it orders the temporal split and is a model input by default.
     - california_house_prices_2020, labour_inspection_compliance and wine_quality keep their reconstructed order out of the inputs (`feature=False`), because the actor does not hold it when predicting[^lk-4].
     - Here the actor does: the encounter number is assigned when the stay begins, so the hospital holds it at discharge, when readmission is predicted.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as input (implemented) | `time_index` stays a feature | the actor holds it; a model can use a trend over time | the test windows lie beyond the training range of the index, where a trend extrapolates poorly |
     | B | Split order only (`feature=False`) | `time_index` orders the windows and is dropped from the inputs | no model leans on an artificial index | drops what the actor holds at prediction |

   * **Recommendation:** A. **Decision:** A or B?

   **Notes for the AI:** on B, declare `Temporal(..., feature=False)` (the time-column-as-split-metadata change of #98) and add a CC line.

   [^lk-4]: **LEAK-10** (Must): every feature has to have existed, and be held by the actor, at the prediction time of its row; a time column that only orders the split is declared no input.


## Reference

Beata Strack, Jonathan P. DeShazo, Chris Gennings, Juan L. Olmo, Sebastian Ventura, Krzysztof J. Cios, and John N. Clore, “ Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records,” BioMed Research International, vol. 2014, Article ID 781670, 11 pages, 2014.
