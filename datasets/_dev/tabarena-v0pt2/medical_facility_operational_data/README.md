---
report_format: data-foundry-report-v2
unique_name: medical_facility_operational_data
container_format: 2
checksum: v2:cd3448c5aa9e945c0eee4a574564841df7ce29187b04aa004e8aec131375c5a1
build:
  uuid: 01a18629-f249-7ee4-b713-033fd2de1d79
  checksum: v2:ff6dbfb16def447738e6df8805220dc831c23aea18a5a2b485851864f6b1f5d3
  built_at: '2026-10-29T05:37:42+00:00'
  path: medical_facility_operational_data/01a18629-f249-7ee4-b713-033fd2de1d79
  data_foundry_version: 0.0.5
  git_sha: 6d189a922994ddb0221c8249d07552d4df8af88b
  libraries:
    python: 3.12.3
    pandas: 3.1.0
    numpy: 2.5.4
    pyarrow: 26.0.0
    scikit-learn: 1.7.2
    polars: 2.0.0
build_stale: true
data:
  n_rows: 82001
  n_features: 88
  dtypes:
    category: 6
    float64: 51
    int64: 32
  n_test_dataset_rows: null
task:
  target: Wait
  problem_type: regression
  metric: mae
  metric_origin: source
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: arrival_order
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 9
  n_folds: 1
  random_state: 4267
  time_horizon: 14
  time_horizon_unit: days
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 41048
    max: 77557
  n_test:
    min: 1140
    max: 1540
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  - dataset_conflicting_duplicate_rows
  - meta_time_horizon_unit
  accepted:
    splits_rows_unused: 'By design (Lennart, 2026-11-05, issue 8): the nine 14-day
      windows start at the nine equal-count points of the arrival instants and do
      not tile the period, so the 2,921 visits after the newest window''s last day
      are in no split; every visit before it is in a training side.'
decisions:
- 'One meaning of the target: the scheduled facilities F1-F3'
- Summaries of an empty set are missing
---

# medical_facility_operational_data

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `Wait`, scored with `mae` on temporal splits by `arrival_order`. 82,001 rows and 88 features. Source: Other (2020).

Built as `01a18629-f249-7ee4-b713-033fd2de1d79` on 2026-10-29, but `dataset.py` has changed since: it now gives checksum `v2:cd3448c5aa9e945c0eee4a574564841df7ce29187b04aa004e8aec131375c5a1`, so the build is stale. See [Build](#build).

## In brief

**Question.** How many minutes after its scheduled time will this patient's imaging exam start at this facility?

**Use case.** At patient arrival, imaging operations staff estimate the exam-start delay against the appointment from the current workflow and the known appointment plan.

**One row.** One of 82,001 visits of the three scheduled facilities F1-F3, with the facility as context.

**Predicted.** The exam start minus the scheduled time, in minutes, signed: an exam that starts early has a negative delay.

**Known at prediction time.** Facility, how many minutes before or after the appointment this patient arrived, the current queue and resource state, histories of completed exams, the source's time features, counts of booked visits from the schedule and the source's per-exam-type delay and duration estimates, whose making is not documented. This patient's exam type is not an input.

**What the test data stands for.** Nine two-week windows of later visits in time order, as the source tests two weeks after six months of training; each window trains on all visits whose exam had begun before it. The anonymised timestamps are one shift of the real clock for all facilities, and every window has thousands of training visits of each facility.

**Our changes to the source.** Only the scheduled facilities: the walk-in facility F4 measures another quantity (the wait from arrival) and is left out. The raw timestamps are dropped; their arrival rank is the time column and an input. How many minutes before the appointment this patient arrived, which the source's features lack, is derived from them and added as an input. Summaries of an empty set, 0 in the source, are missing.

> **Use case fit: approximate (a stand-in with a known gap).** The source's own delay task on the facilities' own records, in real time order, with this patient's arrival against the appointment added. The gap: the source's aggregation removed this patient's exam type, contrast and inpatient status, so the other inputs describe the facility's state for whoever comes next. Kept on purpose as potential leaks: the expected-delay table, of undocumented origin, and the schedule fields, which reflect the final schedule.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`REVIEW.md`](REVIEW.md) | The open questions for the curator, removed once they are settled. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/medical_facility_operational_data.md`](../../../../curation/records/medical_facility_operational_data.md)
- The original source: <https://medicalanalytics.group/operational-data-challenge/>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/medical_facility_operational_data/`. To get them:

```text
Primary author release, linked by Pianykh et al. (2020), Nature Machine Intelligence:
https://medicalanalytics.group/operational-data-challenge/
mkdir -p local-data-warehouse/medical_facility_operational_data
curl -L --fail 'https://medicalanalytics.group/wp-content/uploads/2020/04/codeanddata.zip' -o local-data-warehouse/medical_facility_operational_data/author-codeanddata.zip
unzip -p local-data-warehouse/medical_facility_operational_data/author-codeanddata.zip CodeAndData/Data/WaitData.Published.xlsx > local-data-warehouse/medical_facility_operational_data/WaitData.Published.xlsx
Author archive SHA256 307f5991208b33e60615ef9c145bb7c30dff3bdbccab292d60c86460e8f01c80.
Workbook SHA256 153cff36b4bbf2d972f415c00a786ae5d5e65557ae23b0379fd33efb69060f2e.
This workbook is byte-identical to Kaggle mirror version 1, updated 2021-02-10:
https://www.kaggle.com/api/v1/datasets/download/weirdolucifer/medical-facility-operational-data?datasetVersionNumber=1
Mirror archive SHA256 d2427f01c225122fd406bcd28d55e78439e60a1465f7514caf22e593ebd9f256.
Read the four worksheets F1-F4; the definition keeps the scheduled facilities F1-F3. Counts differ from the related PLOS analytical cohort; exact cohort equivalence is not claimed.
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/medical_facility_operational_data   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/medical_facility_operational_data   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://medicalanalytics.group/operational-data-challenge/ |
| year | 2020 |
| domain | medical & healthcare |
| license | CC0 1.0 (Harvard Dataverse doi:10.7910/DVN/X4SJWS, author deposit by Pianykh, 2020-05-24) |
| data_tags | Non-IID, Temporal, Anonymized |
| reference | Pianykh2020,Crowley2020 |
| rows x columns | 82,001 x 89 |
| task.target | Wait |
| task.problem_type | regression |
| task.metric | mae |
| task.split_regime | temporal_non_iid |
| task.time_on | arrival_order |

**Metric**

| field | value |
|---|---|
| name | `mae` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | Mean absolute error in minutes: the challenge's goal is an MAE reduction against the intercept model; the author code (WTModel.m) and Crowley et al. (2020) evaluate it per facility. |
| reference | https://medicalanalytics.group/operational-data-challenge/ |
| definition | Source MAE formula in minutes on all held-out visits within each window, summarized by the standard equal mean of nine window MAEs. The source does not prescribe cross-facility or across-window weighting; no facility normalization is applied. |

<details>
<summary>Feature types: 6 categorical, 0 string, 0 datetime</summary>

- categorical (6): `facility`, `IsLast`, `IsFirst`, `NoneInProgress`, `NoneCompleted`, `NoneInLine`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{Pianykh2020,
  author = {Pianykh, Oleg S. and Guitron, Steven and Parke, Darren and Zhang, Chengzhao and Pandharipande, Pari and Brink, James and Rosenthal, Daniel},
  title = {Improving healthcare operations management with machine learning},
  journal = {Nature Machine Intelligence}, volume = {2}, pages = {266--273}, year = {2020},
  doi = {10.1038/s42256-020-0176-3}
}
@article{Crowley2020,
  author = {Crowley, Colm and Guitron, Steven and Son, Joseph and Pianykh, Oleg S.},
  title = {Modeling workflows: Identifying the most predictive features in healthcare operational processes},
  journal = {PLOS ONE}, volume = {15}, number = {6}, pages = {e0233810}, year = {2020},
  doi = {10.1371/journal.pone.0233810}
}
```

</details>

## Sample rows

The first 5 of 82,001 rows of the final frame (the oldest rows: the frame is sorted by `arrival_order`); 12 of 89 columns, the target first. Cells are cut at 40 characters.

| Wait | SumHowEarlyWaiting | AvgHowEarlyWaiting | LineCount0Strict | SumWaits | LineCount0 | LineCount1 | LineCount2 | LineCount3 | LineCount4 | FlowCount2 | FlowCount4 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 0 | nan | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 26 | 0 | nan | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 18 | 18 | 1 | 26 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 9 | 0 | nan | 0 | 0 | 0 | 1 | 2 | 1 | 1 | 2 | 2 |
| 6 | 0 | nan | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |

## Curation notes

We start with worksheets F1-F3 of the authenticated author workbook WaitData.Published.xlsx (all four sheets are read; F4 is left out).

- Prediction point: arrival, before the exam starts. Wait is the exam start minus the scheduled time, signed, and agrees with the source timestamps within one minute in every row. Valid negatives and zeros stay, without log transform, clipping or rescaling.
- One meaning of the target (Lennart, 2026-11-04): only the scheduled facilities F1-F3 (82,001 visits). F4's Wait is another quantity, the wait from arrival of walk-in patients (USE-5, as rain_in_australia; Crowley et al. 2020 model delay and wait separately); a dataset of its own is a separate decision. AvgWaitForDay exists only on F4 and goes with it.
- Facility is the source worksheet ID, kept as context; neutral F1-F3 labels, as the author code and the PLOS cohort disagree on the modality names. No unseen-facility generalization is claimed.
- Dtypes: counts and sums numeric; facility and the four yes/no flags categorical. DayOfWeek (1-7) and Month (1-12) ship as numbers and stay numbers, like DayOfYear (CLEAN-14, the cycle rule of 2026-11-01).
- The three raw timestamps are dropped. The arrival and start timestamps order the rows and decide which labels are known; their dense arrival-order rank is the time column and an input (known at arrival; dropping it changes LightGBM's MAE by +0.12, mean of the nine 14-day windows and 2 seeds, higher in 16 of 18 fits). The sheets list the visits in exactly reverse arrival order. The scheduled timestamp goes after `minutes_early` is derived from it (next bullet). Superseded 2026-11-05: until then this patient's own minutes early (correlation -0.605 with Wait) left with it, as in the source's patient-agnostic features ("the next patient, whoever it will be", Crowley et al. 2020).
- CC (2026-11-05, Lennart): add `minutes_early` (issue 6, A; USE-6, CLEAN-19): this patient's scheduled time minus arrival time in minutes, positive when the patient arrives early and negative when late, derived before `x_ScheduledDTTM` is dropped; the inputs go from 87 to 88. It is known at check-in, the prediction point: the appointment is in the plan and the arrival is now. CLEAN-19's ground is "restores meaning the source destroyed": the anonymisation shifted every timestamp by one clock and kept the difference, while the source treats its timestamps as "only for sorting" and its features describe the next patient, whoever it is. No value is missing; it runs from -328 to +522 minutes (median 20.8; late in 27.2%, 6.6% and 9.3% of F1-F3 visits), and since every exam begins after its arrival, Wait is at least minus `minutes_early` in all 82,001 rows. Untuned LightGBM (L1 loss, 500 trees) on this frame and the nine 14-day windows: MAE 15.47 without it and 13.70 with it (-11%, mean of 9 windows, 2 seeds, lower in all 18 fits; the training median scores 21.63; on the earlier 42-53-day windows 15.29 and 13.56). This sets it apart from protein_model_quality_rf_pcp, kept with no new features (2026-11-04): there the signal of a built feature was weak and the dataset is marked `Outdated`; here one input the actor reads at check-in lowers the error by a ninth. The fit stays approximate: this patient's exam type stays lost in the source's aggregation (USE-8).
- The anonymisation is one shift of the real clock for all facilities: in every row the fictitious arrival time of day is the source's StartTime plus 60 minutes, DayOfWeek differs from the fictitious weekday by one constant offset and DayOfYear from the fictitious day of the year by 2 or 3 days (leap years), and the facilities agree on all 459 days shared by all three (694 shared by at least two), with 0 conflicts. So the common arrival order is the real order across facilities, to the minute.
- Potential leak, kept on purpose (LEAK-10, LEAK-6): the schedule fields (`AheadCount`, `IsFirst`, `IsLast`, `FutFlowCount2/4`, `NumScheduledNextSlot`, `NumScheduledNextW2`, `SumTimeToCompleteNextSlot`, `SumTimeToCompleteNextW2`) describe the final schedule, not the plan at arrival: they match the scheduled visits that took place in 99.9-100% of rows (`IsLast` in 2,166 of 2,166), so no-shows are missing and later add-ons are included (32.1% of rows have an add-on booked within the next hour). Dropping all nine changes LightGBM's MAE by +0.05 (mean of the nine 14-day windows and 2 seeds; -0.06 to +0.14 per fit, higher in 15 of 18; a window's MAE differs by 0.05 between seeds on average; +0.14 and R^2 0.660 to 0.644 with the leak probe's L2 model, where `AheadCount` alone is worth +0.11); on the earlier windows seven of them were worth +0.08 to +0.16 (2 seeds x 3 windows; seed noise about 0.07). They stay because the effect is weak and booking-version snapshots are not supplied; revisit if the authors supply them.
- CC (2026-11-05, Lennart): the nine schedule fields stay (issue 11, A), as an application of LEAK-10's clause on values read at a later pull (answer (a)): the late cells cannot be located row by row, so the whole-field worth is an upper bound on the late part, and it sits within about two seed SDs (+0.08 to +0.16 against 0.07 on the earlier windows; +0.05 against 0.05 on the 14-day windows), so the late part shows no gain.
- Potential leak, kept on purpose (LEAK-38; Lennart, 2026-11-04: "keep them"): `ExpectedDelayNextExam` and the sums built from it (`SumDelayWaitingByExamCode`) are one fixed table of expected delay per exam type (49, 215 and 195 values at F1-F3, reused over the whole period), of undocumented origin and reference period. The risk is a table fit over all rows, test windows included (LEAK-27, LEAK-32): the values correlate 0.44, 0.70 and 0.77 (F1-F3) with the mean Wait of their rows without equalling it (median gap 2.7, 4.9 and 8.8 minutes). They do not match the realised delays (a median gap of 6.0-11.7 minutes for a patient waiting alone), and dropping them changes LightGBM's MAE by -0.005 minutes (mean of the nine 14-day windows and 2 seeds, higher in 7 of 18 fits; 0.01-0.02 on the earlier windows), within seed noise. The duration estimates `SumTimeToComplete*` appear to come from the same undocumented estimator family. Revisit if the authors document the table.
- CC (2026-11-05, Lennart): the expected-delay table stays under LEAK-38 as amended on this dataset and tunisian_fraud_detection_challenge (issue 9, D, scope (a)): fields that may be post-outcome, anonymised or named, whose timing the source leaves undocumented and no test can establish, in data the data owner released for its own challenge, stay with this note and are named in `fit_reason` as kept (USE-8). The authors released this workbook for their own operational data challenge, and `fit_reason` names the table.
- Potential leak, kept on purpose (LEAK-9, an evaluation leak): every queue field is history at its own row's arrival, but later rows reveal earlier rows' targets. With one exam in progress, `SumDelayInProgress` equals that patient's Wait (14,150 of 14,150 rows), and `SumWaits`, `LineCount0` and `SumHowEarlyWaiting` rebuild the line. A participant who reads the later test rows of a window lowers MAE from 13.85 to 6.83 (-51%, lower in all 9 windows: default LightGBM against the task gamer's decode, on this frame and the 14-day windows); the features of the next arrivals alone give 11.52. On the 2026-11-04 frame, without `minutes_early`, the figures are 15.65, 8.70 and 13.72 (15.57, 8.70 and 13.64 on the earlier windows). Each test visit is predicted from the training rows and its own features only; no feature or model step may use other test rows. The columns stay: dropping them removes honest signal, and the counts still leak through lead features.
- CC (2026-11-05, Lennart): the protocol line stays as implemented (issue 7, A), under LEAK-9 as amended on this dataset (answer (c)): an evaluation leak is fixed in the scoring or by a protocol line the benchmark checks, and a method that learns from the test block is called out and not benchmarked ("we investigate models, and would find out if they do transductive learning which we can call out and not benchmark"). The benchmark-side check is listed in the working copy's `BENCHMARK_CHANGES_TODO.md`.
- mintime and maxtime stay. The dictionary's daily-wait wording is contradicted by exact identities with the exams in progress (zero with none, both equal SumInProgress with one, min+max equals it with two, no count/sum envelope violations): they are elapsed times of the active exams, not the day's extremes.
- Operational history is not the current patient's target: no recent-history field changes between arrivals without a completed exam, and linked completed exams support the signed end-minus-scheduled histories; exact updater/default rules remain incompletely documented.
- `OutpatientWaitingCount` equals `LineCount0` + 1 in 80,886 of 82,001 rows and `MalesWaitingCount` exceeds `LineCount0` in 9,376, so both appear to count the arriving patient: attributes known before arrival, no leak. `MalesWaitingCount` is not in Table 1 of Crowley et al. (2020).
- Codebook: Table 1 of Crowley et al. (2020) names the source features. The window suffixes read as 2/4 = 30/60 minutes, W1-W3 = 30/60/120 minutes and K1-K3 = 2/4/8 customers (our inference from Table 1, not a source statement). Superseded 2026-11-05: the data show K1-K3 = the day's last 5/10/15 completed exams and confirm W1-W3 = 30/60/120 minutes (the CC line on issue 10 below).
- Zeros stand in for statistics of empty sets (CLEAN-10), kept as the source ships them: `AvgHowEarlyWaiting` and `AvgWaitByTaskTypeLine` are 0 in all 13,454 empty-line rows, `AvgAgePeopleWaiting` is 0 for an empty line at F1 but a repeated constant at F2 and F3, `AvgDelayForDay` is 0 in 5,898 rows before any exam began, and `MostRecent1-5`, `Median5` and `AvgWaitLastK1-3Customers` are 0 when nothing is completed (`Median5` in 10,040 rows), though 0 is also a valid delay. The flags `NoneInLine` and `NoneCompleted` mark these rows. Superseded 2026-11-05: these values are missing now (next bullet); `AvgDelayForDay` has no begun exam in 5,774 rows (5,898 counted the rows with none completed), and `NoneCompleted` marks `Median5` = 0, not "nothing completed".
- CC (2026-11-05, Lennart): summaries of an empty set set to missing (issue 10, B; CLEAN-10, as ashrae's and rain_in_australia's cloud cover 9 and house_sales's `yr_renovated` 0). The source writes 0 for an average, a median or a recent delay over an empty set, and 0 is also a valid delay. The sums (`Sum*`) stay 0, their true value. Each condition is derived in `_clean` from the data there; 186,047 cells in 16 columns, every one a 0 except the `AvgAgePeopleWaiting` constants (counts per column in the README's decision table):
  - Empty line, `NoneInLine` (equal to `LineCount0` = 0 in every row): `AvgHowEarlyWaiting`, `AvgWaitByTaskTypeLine` and `AvgAgePeopleWaiting`, 13,454 rows each (9,776, 2,991 and 687 at F1-F3). `AvgAgePeopleWaiting` held 0 at F1 and, at F2 and F3, six repeated constants (37.0586 in 1,952 rows, 94.8172 in 377) and 160 zeros; in the 68,547 rows with a line these constants occur once and 0 never. The 407 zeros kept in `AvgHowEarlyWaiting` are real: a whole-minute mean of minutes early near 0.
  - Nothing completed today, `NumCompletedToday` = 0 (9,779 rows): `Median5` and `AvgWaitLastK1-3Customers`; `MostRecentk` where fewer than k exams are completed today (9,779, 12,379, 14,965, 17,318 and 19,412 rows for k = 1-5), where it is 0 in every row. The flag `NoneCompleted` is not the condition: it equals `Median5` = 0 in all 82,001 rows and so also marks 261 rows with completed exams whose recent delays have a median within half a minute of 0, a real value. The zeros kept (261 in `Median5`, 379-566 per `MostRecentk`) are real delays of 0.
  - `AvgWaitLastK1-3Customers` is the sum of the day's last 5, 10 or 15 completed delays divided by 5, 10 or 15 and cut to a whole minute (exact in every row we can test: all rows for K1, rows with at most five completed for K2 and K3). With 1 to 14 completed exams it is that sum over K, defined and kept as the source ships it; with none it averages nothing. Its zeros kept (636, 1,190 and 1,677) come from cutting small sums.
  - `AvgDelayForDay` is the mean Wait of the day's exams begun strictly before the arrival (to 0.01 minutes in all but one of the 76,227 rows with one): missing in the 5,774 rows with none, counted from the timestamps before they are dropped. Its 323 zeros kept have begun exams (322 with a mean Wait of exactly 0, one a stray 0 against a mean of -4.1).
  - `AvgWaitLastW1-3` is the mean start-minus-arrival time of the exams begun in the 30, 60 or 120 minutes up to the arrival, both ends included (within a minute in 97% of rows), not of completed exams: with no completion in the window it is nonzero in 41-50% of rows. Missing where no other exam began in the window (12,841, 8,253 and 5,848 rows), all of which held 0; the 175, 88 and 28 zeros kept have begun exams with a mean near 0.
  - A 0 can be a real value in every blanked column except `AvgWaitByTaskTypeLine` and `AvgAgePeopleWaiting`, so no column is blanked on its zeros alone.
  - Effect: untuned LightGBM (L1 loss, 500 trees) on this frame and the nine 14-day windows scores MAE 13.681 with the source's values and 13.698 with the missing values (+0.017, mean of 9 windows and 2 seeds, lower in 6 of 18 fits; a window's MAE differs by 0.05 between seeds on average; on the earlier windows 13.565 and 13.577): no measurable change. The flags stay as inputs.
- Source MAE is deliberate in the author challenge (its goal is an MAE reduction against the intercept model) and in the paper's comparisons, which evaluate it per facility (author code WTModel.m; Crowley et al. 2020, Tables 2 and 6). We score per-visit MAE in each window and the equal mean of the nine window scores (Myunghwan, 2026-10-28), not an official source aggregation. The author code labels an RMSE calculation MSE; our RMSE uses the standard definition.
- CC (2026-11-05, Lennart): the declared metric (the source's MAE in minutes, per window, the equal mean of the nine windows) is checked and stays as declared.
- CC (2026-11-05, Lennart): the source's two-week test windows (issue 8, B, choice (b); SPLIT-12, SPLIT-19): nine 14-day windows, each from the first whole day at or after the start of one of the nine equal-count windows shipped before (42 to 53 days long), so the folds stay nine and the test visits go from 40,995 to 12,408. The training side stays expanding (the source trained on six months; here 50.1% to 94.6% of the visits, so SPLIT-14's floor and its three windows hold). The day comes from the arrival timestamp in `_clean`, since the time column is the arrival rank, and leaves with the timestamps in `_make_splits`. The planned exception to SPLIT-19 is dropped: the split follows the source. The longer windows had cost nothing measurable (two-week windows 14.40 against 14.42 on the same weeks). The MAE figures in these notes are re-measured on the new windows, with the earlier figures beside them.
- All source negatives, repeated operational states and missing values remain.

## Splits

Expanding windows in the common arrival order of F1-F3, newest window first. The source trains on six months
and tests on "a further consecutive two weeks" (Crowley et al. 2020), so each test window is 14 whole days.
The nine windows start on the first whole day at or after nine points that divide the distinct arrival instants
after the training floor into equal parts; before the first, at least half of all visits have arrived and begun
their exams. They start 44 to 53 days apart and do not tile the period: 12,408 test visits in all, 1,140 to
1,540 per window, and the 2,921 visits after the newest window are in no split. Each window trains on every
visit that arrived and began its exam before its first day: 41,048 to 77,557 of 82,001 (50.1% to 94.6%). No
exam begins on a later day than its arrival, and no visit arrives between 22:00 and 07:00, so a day boundary
cuts no visit. Every window has training visits of each facility (at least 24,478 of F1, 8,339 of F2 and 8,231
of F3) and 217 to 688 test visits of each. The timestamps are one shift of the real clock for all facilities,
so the order is real time. F3 starts later than F1 and F2: about eight months and 8,231 visits of F3 history
precede the oldest window. Each test visit is predicted from the training rows and its own features only; no
feature or model step may use other test rows. No held-out-facility or new-patient guarantee is asserted.

9 repeat(s) x 1 fold(s) with seed 4267; train 41,048 to 77,557 rows, test 1,140 to 1,540 rows. Prediction horizon: 14 days.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 77557 | 1523 | 0 | 77068 | 77069 | 78577 |
| 1 | 0 | 72990 | 1540 | 0 | 72529 | 72530 | 74062 |
| 2 | 0 | 68369 | 1465 | 0 | 67943 | 67944 | 69403 |
| 3 | 0 | 63880 | 1230 | 0 | 63476 | 63477 | 64697 |
| 4 | 0 | 59285 | 1140 | 0 | 58908 | 58909 | 60043 |
| 5 | 0 | 54797 | 1367 | 0 | 54448 | 54449 | 55807 |
| 6 | 0 | 50194 | 1403 | 0 | 49885 | 49886 | 51282 |
| 7 | 0 | 45576 | 1346 | 0 | 45300 | 45301 | 46637 |
| 8 | 0 | 41048 | 1394 | 0 | 40811 | 40812 | 42189 |

## Decisions

### 1. One meaning of the target: the scheduled facilities F1-F3

Ship the signed exam-start delay against the appointment of F1-F3, with facility as context. F4's Wait is the walk-in wait from arrival, another quantity, and is left out (Lennart, 2026-11-04).

| facility | shipped | target meaning | visits | negative targets | zero targets | median minutes | p99 minutes | standard deviation minutes |
|---|---|---|---|---|---|---|---|---|
| F1 | True | start minus scheduled | 42766 | 16052 | 1360 | 4 | 53 | 18.2968 |
| F2 | True | start minus scheduled | 15652 | 4397 | 269 | 12 | 94 | 30.988 |
| F3 | True | start minus scheduled | 23583 | 8432 | 244 | 12 | 113.18 | 48.2991 |
| F4 | False | start minus arrival | 48430 | 0 | 547 | 6 | 32 | 6.65419 |

### 2. Summaries of an empty set are missing

The source writes 0 for an average, median or recent delay over an empty set, and 0 is also a valid delay. Those values are missing now; the zeros that remain are real values. The sums stay 0 (Lennart, 2026-11-05; CLEAN-10).

| column | empty set | set to missing | zeros kept as values |
|---|---|---|---|
| AvgHowEarlyWaiting | empty line (`NoneInLine`) | 13454 | 407 |
| AvgWaitByTaskTypeLine | empty line (`NoneInLine`) | 13454 | 0 |
| AvgAgePeopleWaiting | empty line (`NoneInLine`) | 13454 | 0 |
| Median5 | no exam completed today (`NumCompletedToday` = 0) | 9779 | 261 |
| AvgWaitLastK1Customers | no exam completed today (`NumCompletedToday` = 0) | 9779 | 636 |
| AvgWaitLastK2Customers | no exam completed today (`NumCompletedToday` = 0) | 9779 | 1190 |
| AvgWaitLastK3Customers | no exam completed today (`NumCompletedToday` = 0) | 9779 | 1677 |
| MostRecent1 | fewer than 1 exams completed today | 9779 | 379 |
| MostRecent2 | fewer than 2 exams completed today | 12379 | 563 |
| MostRecent3 | fewer than 3 exams completed today | 14965 | 566 |
| MostRecent4 | fewer than 4 exams completed today | 17318 | 562 |
| MostRecent5 | fewer than 5 exams completed today | 19412 | 542 |
| AvgDelayForDay | no exam of the day begun before the arrival | 5774 | 323 |
| AvgWaitLastW1 | no other exam begun in the 30 minutes up to the arrival | 12841 | 175 |
| AvgWaitLastW2 | no other exam begun in the 60 minutes up to the arrival | 8253 | 88 |
| AvgWaitLastW3 | no other exam begun in the 120 minutes up to the arrival | 5848 | 28 |

## Bundle checks

0 error(s), 0 warning(s), 3 info (27 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 6 exact duplicate row(s) (0.0% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)
- **info** `dataset_conflicting_duplicate_rows`: 108 row(s) (0.1%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)
- **info** `meta_time_horizon_unit`: `time_horizon_unit='days'` implies calendar time, but `time_on='arrival_order'` has dtype int64, so the horizon cannot be cross-checked. (hint: Fine when the numeric values themselves are calendar units (e.g. a year column); otherwise use `time_horizon_unit='steps'` for a plain numeric time index.)

Accepted on purpose:

- `splits_rows_unused`: By design (Lennart, 2026-11-05, issue 8): the nine 14-day windows start at the nine equal-count points of the arrival instants and do not tile the period, so the 2,921 visits after the newest window's last day are in no split; every visit before it is in a training side.

## Data checks

### Feature summary

<details>
<summary>Show the table (89 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| IsLast | category | 0 | 0 | 2 | 0, 1 |
| IsFirst | category | 0 | 0 | 2 | 0, 1 |
| NoneInProgress | category | 0 | 0 | 2 | 0, 1 |
| NoneCompleted | category | 0 | 0 | 2 | 0, 1 |
| NoneInLine | category | 0 | 0 | 2 | 0, 1 |
| facility | category | 0 | 0 | 3 | F1, F3, F2 |
| MostRecent5 | float64 | 19412 | 23.67 | 467 | 31.0, 30.0, 29.0, 34.0, 33.0, 28.0, 35.0, 27.0, 24.0, 43.0 |
| MostRecent4 | float64 | 17318 | 21.12 | 476 | 33.0, 34.0, 30.0, 31.0, 35.0, 28.0, 32.0, 36.0, 26.0, 25.0 |
| MostRecent3 | float64 | 14965 | 18.25 | 466 | 28.0, 30.0, 31.0, 36.0, 24.0, 34.0, 25.0, 32.0, 26.0, 33.0 |
| AvgHowEarlyWaiting | float64 | 13454 | 16.41 | 325 | 33.0, 28.0, 38.0, 32.0, 24.0, 26.0, 23.0, 27.0, 30.0, 20.0 |
| AvgWaitByTaskTypeLine | float64 | 13454 | 16.41 | 1765 | 16.0, 17.0, 16.5, 16.3333, 18.0, 58.0, 61.0, 16.6667, 16.25, 56.0 |
| AvgAgePeopleWaiting | float64 | 13454 | 16.41 | 53296 | 61.1773, 27.0281, 53.4155, 67.551, 68.1533, 56.2327, 47.0938, 40.0219, 56.9829,… |
| AvgWaitLastW1 | float64 | 12841 | 15.66 | 196 | 8.0, 10.0, 9.0, 7.0, 6.0, 11.0, 12.0, 13.0, 14.0, 5.0 |
| MostRecent2 | float64 | 12379 | 15.1 | 477 | 31.0, 30.0, 27.0, 24.0, 29.0, 33.0, 34.0, 35.0, 36.0, 37.0 |
| Median5 | float64 | 9779 | 11.93 | 251 | 31.0, 35.0, 30.0, 34.0, 29.0, 33.0, 36.0, 28.0, 32.0, 25.0 |
| MostRecent1 | float64 | 9779 | 11.93 | 467 | 29.0, 31.0, 25.0, 34.0, 36.0, 32.0, 28.0, 30.0, 37.0, 33.0 |
| AvgWaitLastK1Customers | float64 | 9779 | 11.93 | 223 | 33.0, 36.0, 35.0, 34.0, 37.0, 32.0, 29.0, 39.0, 38.0, 30.0 |
| AvgWaitLastK2Customers | float64 | 9779 | 11.93 | 170 | 33.0, 32.0, 34.0, 36.0, 35.0, 38.0, 37.0, 31.0, 29.0, 30.0 |
| AvgWaitLastK3Customers | float64 | 9779 | 11.93 | 146 | 35.0, 34.0, 33.0, 32.0, 37.0, 36.0, 0.0, 1.0, 38.0, 31.0 |
| AvgWaitLastW2 | float64 | 8253 | 10.06 | 183 | 9.0, 12.0, 10.0, 11.0, 14.0, 13.0, 8.0, 17.0, 15.0, 16.0 |
| AvgWaitLastW3 | float64 | 5848 | 7.13 | 147 | 12.0, 14.0, 13.0, 11.0, 10.0, 9.0, 16.0, 15.0, 8.0, 17.0 |
| AvgDelayForDay | float64 | 5774 | 7.04 | 19295 | 1.0, -1.0, 2.0, 0.0, -2.0, 3.0, -3.0, 4.0, -6.0, 5.0 |
| SumHowEarlyWaiting | float64 | 0 | 0 | 1151 | 0.0, 29.0, 30.0, 33.0, 24.0, 28.0, 39.0, 21.0, 23.0, 38.0 |
| LineCount0Strict | float64 | 0 | 0 | 15 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 |
| SchFlowCount2 | float64 | 0 | 0 | 9 | 4.0, 3.0, 0.0, 5.0, 2.0, 1.0, 6.0, 7.0, 8.0 |
| SchFlowCount4 | float64 | 0 | 0 | 14 | 8.0, 0.0, 7.0, 2.0, 9.0, 6.0, 3.0, 10.0, 4.0, 5.0 |
| FutFlowCount2 | float64 | 0 | 0 | 9 | 4.0, 3.0, 5.0, 2.0, 1.0, 0.0, 6.0, 7.0, 8.0 |
| FutFlowCount4 | float64 | 0 | 0 | 14 | 8.0, 7.0, 2.0, 9.0, 6.0, 3.0, 10.0, 4.0, 5.0, 1.0 |
| DelayCount | float64 | 0 | 0 | 62 | 0.0, 1.0, 2.0, 5.0, 3.0, 6.0, 4.0, 7.0, 8.0, 9.0 |
| DelayCountLastHour | float64 | 0 | 0 | 15 | 0.0, 2.0, 1.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 |
| NeuroCount | float64 | 0 | 0 | 8 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0 |
| AbdominalCount | float64 | 0 | 0 | 16 | 0.0, 1.0, 2.0, 3.0, 5.0, 4.0, 6.0, 7.0, 8.0, 9.0 |
| VascularCount | float64 | 0 | 0 | 7 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 |
| CardiacCount | float64 | 0 | 0 | 5 | 0.0, 1.0, 2.0, 3.0, 4.0 |
| AfterSlot | float64 | 0 | 0 | 128 | 3.0, 2.0, 5.0, 12.0, 9.0, 7.0, 4.0, 1.0, 11.0, 14.0 |
| StartTime | float64 | 0 | 0 | 710 | 9.7833, 9.0, 8.45, 9.85, 12.9333, 9.9667, 8.0, 9.5667, 9.0333, 9.45 |
| StartTime2 | float64 | 0 | 0 | 710 | 95.7136, 81.0, 71.4025, 97.0225, 167.2711, 99.3344, 64.0, 91.5211, 81.6011, 89.… |
| StartTime3 | float64 | 0 | 0 | 710 | 936.3981, 729.0, 603.3511, 955.6716, 2163.3729, 990.0331, 512.0, 875.5518, 737.… |
| StartTime4 | float64 | 0 | 0 | 1063 | 9161.0941, 6561.0, 9413.3655, 5098.317, 4096.0, 9867.3292, 8376.1114, 6658.7404… |
| SumWaitByTaskTypeLine | float64 | 0 | 0 | 914 | 0.0, 16.0, 32.0, 33.0, 17.0, 48.0, 49.0, 50.0, 58.0, 64.0 |
| DelayedInLine | float64 | 0 | 0 | 12 | 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 |
| SumDelayWaitingByExamCode | float64 | 0 | 0 | 25434 | 0.0, 6.4225, 6.2071, 5.7546, 5.9743, 12.6296, 12.3969, 12.1771, 11.9617, 12.1814 |
| ExpectedDelayNextExam | float64 | 0 | 0 | 446 | 6.4225, 6.2071, 19.2911, 15.272, 6.4456, 6.8852, 5.9743, 8.0056, 16.9882, 8.4003 |
| DayOfWeek | float64 | 1 | 0 | 7 | 4.0, 3.0, 6.0, 5.0, 2.0, 7.0, 1.0 |
| Month | float64 | 1 | 0 | 12 | 5.0, 7.0, 6.0, 4.0, 11.0, 3.0, 1.0, 12.0, 2.0, 10.0 |
| DayOfYear | float64 | 1 | 0 | 346 | 137.0, 198.0, 206.0, 177.0, 347.0, 200.0, 333.0, 142.0, 130.0, 136.0 |
| NumAddOnsToday | float64 | 0 | 0 | 14 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 |
| NumAddOnsLastW2 | float64 | 0 | 0 | 8 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0 |
| NumScheduledNextSlot | float64 | 0 | 0 | 9 | 2.0, 1.0, 4.0, 5.0, 3.0, 6.0, 7.0, 0.0, 8.0 |
| NumScheduledNextW2 | float64 | 0 | 0 | 14 | 1.0, 0.0, 2.0, 3.0, 5.0, 4.0, 6.0, 7.0, 8.0, 9.0 |
| SumTimeToCompleteNextSlot | float64 | 0 | 0 | 249 | 37.0, 30.0, 33.0, 36.0, 17.0, 16.0, 35.0, 50.0, 34.0, 32.0 |
| SumTimeToCompleteNextW2 | float64 | 0 | 0 | 402 | 0.0, 37.0, 16.0, 30.0, 50.0, 32.0, 36.0, 35.0, 14.0, 47.0 |
| WithContrastCountWaiting | float64 | 0 | 0 | 14 | 0.0, 3.0, 4.0, 2.0, 5.0, 1.0, 6.0, 7.0, 8.0, 9.0 |
| WithAndWithoutContrastCountWaiting | float64 | 0 | 0 | 7 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 |
| WithContrastCountInProgress | float64 | 0 | 0 | 7 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 |
| WithAndWithoutContrastCountInProgress | float64 | 0 | 0 | 6 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0 |
| minutes_early | float64 | 0 | 0 | 11317 | 6.4333, 9.25, 6.9833, 5.8167, 3.8667, 8.1667, 13.9167, 8.8167, 13.5667, 14.9833 |
| Wait | int64 | 0 | 0 | 507 | 4, 0, 5, 6, 3, 1, 2, -1, -2, 7 |
| SumWaits | int64 | 0 | 0 | 756 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 13 |
| LineCount0 | int64 | 0 | 0 | 18 | 1, 2, 0, 3, 4, 5, 6, 7, 8, 9 |

(29 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 37.5 | -1.478 | nan | 1040.43 | nan | log1p | 422021 | 427320 | exponential |

### Numeric features

<details>
<summary>Show the table (83 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| Wait | 82001 | 6.97979 | 32.2558 | -497 | 360 |
| SumHowEarlyWaiting | 82001 | 136.015 | 173.928 | -156 | 1563 |
| AvgHowEarlyWaiting | 68547 | 42.7501 | 31.3921 | -87 | 523 |
| LineCount0Strict | 82001 | 2.01637 | 2.05357 | 0 | 14 |
| SumWaits | 82001 | 83.1375 | 112.069 | 0 | 1032 |
| LineCount0 | 82001 | 2.78581 | 2.46296 | 0 | 17 |
| LineCount1 | 82001 | 2.77344 | 2.48147 | 0 | 18 |
| LineCount2 | 82001 | 2.73788 | 2.50143 | 0 | 17 |
| LineCount3 | 82001 | 2.64865 | 2.52503 | 0 | 18 |
| LineCount4 | 82001 | 2.54752 | 2.5417 | 0 | 15 |
| FlowCount2 | 82001 | 2.68606 | 1.82105 | 0 | 10 |
| FlowCount4 | 82001 | 5.12443 | 3.2517 | 0 | 15 |
| SchFlowCount2 | 82001 | 2.86826 | 1.84324 | 0 | 8 |
| SchFlowCount4 | 82001 | 5.37032 | 3.40964 | 0 | 13 |
| FutFlowCount2 | 82001 | 3.13906 | 1.70164 | 0 | 8 |
| FutFlowCount4 | 82001 | 6.10212 | 3.03621 | 0 | 13 |
| DelayCount | 82001 | 14.1087 | 11.6735 | 0 | 61 |
| DelayCountLastHour | 82001 | 3.20639 | 2.52633 | 0 | 14 |
| mintime | 82001 | 8.52741 | 13.3064 | 0 | 279 |
| maxtime | 82001 | 28.5619 | 29.1102 | 0 | 311 |
| AheadCount | 82001 | 24.49 | 17.31 | 0 | 75 |
| ThoracicCount | 82001 | 1.24339 | 2.3096 | 0 | 14 |
| PediatricCount | 82001 | 0.0100365 | 0.101136 | 0 | 2 |
| NeuroCount | 82001 | 0.373386 | 0.790582 | 0 | 7 |
| AbdominalCount | 82001 | 3.03824 | 2.79505 | 0 | 15 |
| VascularCount | 82001 | 0.369495 | 0.673303 | 0 | 6 |
| CardiacCount | 82001 | 0.0397068 | 0.245762 | 0 | 4 |
| MSKCount | 82001 | 0.372105 | 0.672264 | 0 | 6 |
| NumScannersUsedToday | 82001 | 3.64775 | 2.15295 | 0 | 6 |
| SumInProgress | 82001 | 55.0849 | 56.1263 | 0 | 808 |
| BeforeSlot | 82001 | 15.8715 | 17.8732 | 0 | 418 |
| AfterSlot | 82001 | 16.2121 | 13.1638 | 0 | 342 |
| Median5 | 72222 | 35.083 | 21.9409 | -347 | 207 |
| MostRecent1 | 72222 | 35.7265 | 37.3766 | -492 | 371 |
| MostRecent2 | 69622 | 35.9244 | 37.721 | -415 | 342 |
| MostRecent3 | 67036 | 36.0451 | 37.2155 | -492 | 323 |
| MostRecent4 | 64683 | 35.7863 | 37.2462 | -415 | 357 |
| MostRecent5 | 62589 | 35.9488 | 37.687 | -405 | 340 |
| StartTime | 82001 | 11.4573 | 2.77544 | 6.38333 | 20.2333 |
| StartTime2 | 82001 | 138.974 | 65.3644 | 40.7469 | 409.388 |
| StartTime3 | 82001 | 1772.66 | 1205.88 | 260.101 | 8283.28 |
| StartTime4 | 82001 | 23586.1 | 20565.9 | 1660.31 | 167598 |
| SumWaitByTaskTypeLine | 82001 | 132.956 | 173.159 | 0 | 1065 |
| AvgWaitByTaskTypeLine | 68547 | 40.3024 | 24.0591 | 7 | 132 |
| SumTimeToCompleteInProgress | 82001 | 142.773 | 116.118 | 0 | 1251 |
| DelayedInLine | 82001 | 1.72724 | 1.20924 | 0 | 11 |
| SumDelayWaitingByExamCode | 82001 | 33.4861 | 39.8889 | -212.812 | 259.544 |
| SumDelayWaitingInLine | 82001 | -52.8986 | 99.2158 | -1005 | 449 |
| SumDelayInProgress | 82001 | 8.24878 | 52.6282 | -601 | 346 |
| ExpectedDelayNextExam | 82001 | 11.6125 | 6.14981 | -229 | 74 |
| AvgAgePeopleWaiting | 68547 | 57.7491 | 13.8869 | 8.69268 | 100.832 |
| DayOfWeek | 82000 | 4.03935 | 1.39802 | 1 | 7 |
| Month | 82000 | 6.34576 | 3.45506 | 1 | 12 |
| DayOfYear | 82000 | 177.655 | 105.543 | 2 | 365 |
| InProgressSize | 82001 | 2.65998 | 1.92038 | 0 | 13 |
| AvgWaitLastK1Customers | 72222 | 33.0492 | 22.9994 | -121 | 139 |
| AvgWaitLastK2Customers | 72222 | 30.366 | 20.3016 | -65 | 120 |
| AvgWaitLastK3Customers | 72222 | 27.5395 | 18.6168 | -43 | 104 |
| NumCompletedToday | 82001 | 20.0404 | 16.8937 | 0 | 75 |
| NumCompletedInLastW1 | 82001 | 2.44247 | 1.93168 | 0 | 15 |

(23 more rows not shown)

</details>

### Categorical features

<details>
<summary>Show the table (13 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| IsFirst | 1 | 0 | 78719 | 96 |
| IsFirst | 2 | 1 | 3282 | 4 |
| IsLast | 1 | 0 | 79835 | 97.36 |
| IsLast | 2 | 1 | 2166 | 2.64 |
| NoneCompleted | 1 | 0 | 71961 | 87.76 |
| NoneCompleted | 2 | 1 | 10040 | 12.24 |
| NoneInLine | 1 | 0 | 68547 | 83.59 |
| NoneInLine | 2 | 1 | 13454 | 16.41 |
| NoneInProgress | 1 | 0 | 70113 | 85.5 |
| NoneInProgress | 2 | 1 | 11888 | 14.5 |
| facility | 1 | F1 | 42766 | 52.15 |
| facility | 2 | F3 | 23583 | 28.76 |
| facility | 3 | F2 | 15652 | 19.09 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a18629-f249-7ee4-b713-033fd2de1d79 |
| checksum | v2:ff6dbfb16def447738e6df8805220dc831c23aea18a5a2b485851864f6b1f5d3 |
| built_at | 2026-10-29T05:37:42+00:00 |
| path | medical_facility_operational_data/01a18629-f249-7ee4-b713-033fd2de1d79 |
| data_foundry_version | 0.0.5 |
| git_sha | 6d189a922994ddb0221c8249d07552d4df8af88b |
| libraries | {'python': '3.12.3', 'pandas': '3.1.0', 'numpy': '2.5.4', 'pyarrow': '26.0.0', 'scikit-learn': '1.7.2', 'polars': '2.0.0'} |
| stale | yes: the definition now gives checksum `v2:cd3448c5aa9e945c0eee4a574564841df7ce29187b04aa004e8aec131375c5a1` |
