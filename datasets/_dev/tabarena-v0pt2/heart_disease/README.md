---
report_format: data-foundry-report-v2
unique_name: heart_disease
container_format: 2
checksum: v2:823a1b0cb47cafbd573f9d4e43117c13d375f328f9202687847d91249754ad43
build: null
build_stale: false
data:
  n_rows: 797
  n_features: 13
  dtypes:
    category: 9
    float64: 6
  n_test_dataset_rows: null
task:
  target: heart_disease_diagnosis
  problem_type: binary_classification
  metric: roc_auc
  split_regime: grouped_non_iid
  stratify_on: heart_disease_diagnosis
  time_on: null
  group_on: hospital
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 3
    test_groups_per_fold:
      min: 1
      max: 1
splits:
  n_repeats: 1
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 494
    max: 597
  n_test:
    min: 200
    max: 303
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  accepted:
    task_group_count_low: 'Three hospitals by design: the source built its model at
      one hospital and applied it at the others. The fourth hospital (Switzerland)
      is left out because its published file kept only 8 of its 23 patients without
      disease.'
    splits_dimensions_off_protocol: Leave one hospital out gives exactly three splits.
      More repeats would split the same three hospitals the same way, so they would
      add copies, not information.
    groups_test_groups_few: 'Testing on one unseen hospital at a time is the task.
      Each fold still scores 200 to 303 patients one by one (smallest class: 51).
      The signal carries over to unseen hospitals: the linear model beats the class
      shares on all three (task probes), and logistic regression reaches ROC AUC 0.868
      on held-out hospitals (group probes, 2026-10-21). Most of the variation between
      folds comes from Long Beach, the hardest hospital.'
    groups_largest_share_high: Cleveland is a real hospital, one of three, not a catch-all
      value. When it is the test hospital, the model trains on the other two (494
      patients), where two of Cleveland's tests were almost never recorded.
decisions:
- 'Split by hospital: train on two, test on the third'
---

# heart_disease

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Binary classification of `heart_disease_diagnosis`, scored with `roc_auc` on grouped splits by `hospital`. 797 rows and 13 features. Source: UCI (1988).

Not built yet. The current definition gives checksum `v2:823a1b0cb47cafbd573f9d4e43117c13d375f328f9202687847d91249754ad43`.

## In brief

**Question.** Will the angiogram of a patient at a new hospital show a narrowed coronary artery?

**Use case.** A cardiologist estimates a chest-pain patient's chance of coronary artery disease from the history and noninvasive tests with a model built at other hospitals, to decide whether the patient needs angiography, as Detrano et al. (1989) applied their Cleveland model in Budapest, Long Beach and Switzerland.

**One row.** One of 797 patients examined by angiography at one of three hospitals: Cleveland Clinic (303), the Hungarian Institute of Cardiology in Budapest (294) and the VA Medical Center in Long Beach (200); exams of the 1980s, donated in 1988.

**Predicted.** Whether the angiogram shows more than 50% narrowing in any major coronary artery (49% do; 36% to 75% by hospital).

**Known at prediction time.** Age, sex, chest-pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, an exercise test (peak heart rate, chest pain on exercise, the ECG's ST depression and its slope) and, mostly in Cleveland, calcium seen on fluoroscopy and a thallium scan. Not the hospital.

**What the test data stands for.** Whole hospitals are held out: each split trains on two hospitals and tests on the third, so the test data stands for the patients of a hospital the model has never seen.

**Our changes to the source.** We merge three hospitals' files into one table and split by hospital, leave out the Swiss file (its release dropped most patients without disease), and merge the four grades of disease into one class.

> **Use case fit: approximate (a stand-in with a known gap).** The features come from tests done before the angiogram that sets the label, and a held-out hospital is a new one with its own disease rate and test habits. But every patient had already been sent to angiography, so the data shows referred patients, not those a referral is decided for.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`explore.ipynb`](explore.ipynb) | The workbench for looking at the data (`ds = workbench()`), committed without outputs. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/heart_disease.md`](../../../../curation/records/heart_disease.md)
- The original source: <https://doi.org/10.24432/C52P4X>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/heart_disease/`. To get them:

```text
Get the UCI data (the processed files of the three hospitals).

mkdir -p local-data-warehouse/heart_disease && cd local-data-warehouse/heart_disease && wget https://archive.ics.uci.edu/static/public/45/heart+disease.zip && unzip heart+disease.zip processed.cleveland.data processed.hungarian.data processed.va.data && rm heart+disease.zip
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/heart_disease   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/heart_disease   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | UCI: https://doi.org/10.24432/C52P4X |
| year | 1988 |
| domain | medical & healthcare |
| license | CC BY 4.0 |
| data_tags | Non-IID, Grouped |
| reference | detrano1989international |
| rows x columns | 797 x 15 |
| task.target | heart_disease_diagnosis |
| task.problem_type | binary_classification |
| task.metric | roc_auc |
| task.split_regime | grouped_non_iid |
| task.stratify_on | heart_disease_diagnosis |
| task.group_on | hospital |
| task.group_labels | per_sample |

<details>
<summary>Feature types: 9 categorical, 0 string, 0 datetime</summary>

- categorical (9): `hospital`, `sex`, `cp`, `fbs`, `restecg`, `exang`, `slope`, `thal`, `heart_disease_diagnosis`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{detrano1989international,
  title={International application of a new probability algorithm for the diagnosis of coronary artery disease},
  author={Detrano, Robert and Janosi, Andras and Steinbrunn, Walter and Pfisterer, Matthias and Schmid, Johann-Jakob and Sandhu, Sarbjit and Guppy, Kern H and Lee, Stella and Froelicher, Victor},
  journal={The American journal of cardiology},
  volume={64},
  number={5},
  pages={304--310},
  year={1989},
  publisher={Elsevier}
}
```

</details>

## Sample rows

The first 5 of 797 rows of the final frame (random rows: the frame is shuffled); 12 of 15 columns, the target first. Cells are cut at 40 characters.

| heart_disease_diagnosis | age | sex | cp | trestbps | chol | fbs | restecg | thalach | exang | oldpeak | slope |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 52 | 1 | 3 | 140 | 259 | 0 | 1 | 170 | 0 | 0 | nan |
| 0 | 53 | 0 | 2 | 113 | 468 | nan | 0 | 127 | 0 | 0 | nan |
| 1 | 63 | 0 | 4 | 150 | 407 | 0 | 2 | 154 | 0 | 4 | 2 |
| 1 | 54 | 1 | 4 | nan | nan | 0 | 1 | nan | nan | nan | nan |
| 1 | 71 | 1 | 4 | 130 | 221 | 0 | 1 | 115 | 1 | 0 | nan |

## Curation notes

We start with the processed files of three hospitals from UCI's Heart Disease collection, the 14 attributes used in the study.

- Prediction point: before the angiogram, with the history, the resting tests and the exercise test at hand. `ca` (major arteries with calcium seen on cardiac fluoroscopy, 0-3) and `thal` (exercise thallium scan) are noninvasive tests done before the angiogram (Detrano et al. 1986, PMID 3698241 and 3706156), so neither is read from it.
- One study, three tasks merged: the files share the protocol, attributes and label, and a model trained on two hospitals ranks the third's patients nearly as well as one trained there (TabPFN 3.5 ROC AUC 0.888 on Cleveland, 0.906 on Hungary, 0.739 on Long Beach; trained in-site 0.913, 0.914, 0.708). We concatenate the files and keep the hospital as the group column.
- Split by hospital, as in the source: Detrano et al. (1989) derived their model on the Cleveland patients and "applied [it] to" the other hospitals' patients (abstract). A hospital that uses a model built elsewhere brings its own disease rate (36% in Budapest, 46% in Cleveland, 75% in Long Beach, as in the paper) and its own test habits (`ca` and `thal` recorded almost only in Cleveland, no exercise test for 53 Long Beach patients). Held out whole, a hospital is scored on its own patients only. A random split would mix the hospitals in every test fold, and 68% of its positive-negative pairs would compare patients of two hospitals, a comparison no clinician makes. The model is not given the hospital: a new one is unknown.
- Note: the task probes flag `unstable` (the standard error of the best model family's mean skill is 0.094 over the 3 splits). The signal is there at every held-out hospital: the linear model beats the class shares on 3 of 3 (mean ROC AUC 0.838). The spread is between hospitals, Long Beach being the hardest (TabPFN 3.5: 0.888 Cleveland, 0.906 Hungary, 0.739 Long Beach). Kept, as `consumer_complaints_1m` and `apistox` were with 3 and 4 windows.
- Switzerland left out: its UCI file keeps 123 of the paper's 143 patients and only 8 of its 23 without disease (94% diseased against the paper's 84%), so its disease rate is the release's, not the hospital's, and as a held-out hospital it would be scored on 8 patients without disease.
- Missing values: "?" becomes NaN. Cholesterol 0 (49 Long Beach rows) and resting blood pressure 0 (1 row) are impossible and become NaN. Other missing values stay: whether a test was done is known before the angiogram. In Hungary `slope` is missing exactly when there is no ST depression.
- Target: `num` (0 = no narrowing over 50%, 1-4 = disease grades; the Hungarian file holds only 0/1) becomes the binary `heart_disease_diagnosis`, as in the study.
- Codes are kept as in UCI: `sex` 1 = male; `cp` 1 typical angina, 2 atypical angina, 3 non-anginal pain, 4 asymptomatic; `fbs` 1 = fasting blood sugar over 120 mg/dl; `restecg` 0 normal, 1 ST-T wave abnormality, 2 left ventricular hypertrophy; `exang` 1 = angina on exercise; `oldpeak` ST depression on exercise relative to rest; `slope` of the peak-exercise ST segment, 1 up, 2 flat, 3 down; `thal` 3 normal, 6 fixed defect, 7 reversible defect.
- Anomaly: the Hungarian file keeps 294 of the paper's 425 patients (36% diseased against 38%), selection not stated. 6 Long Beach angiograms are dated 7 to 15 days (one 369 days) before the exercise test in the raw file; kept. One Long Beach `oldpeak` is negative.
- Duplicates: two rows repeat another row of the same hospital (one Hungarian, one Long Beach); with 13 coarse attributes these are plausible patients, kept.

## Splits

Leave one hospital out: three splits, each training on two hospitals and testing on the third (Cleveland, Hungary, then Long Beach), one repeat, since repeating a split of three groups into three folds gives the same splits. This follows the source, which built its model at one hospital and tested it at the others; with three hospitals the scores are three numbers and differ by hospital (Long Beach is the hardest).

1 repeat(s) x 3 fold(s) with seed 4267; train 494 to 597 rows, test 200 to 303 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 494 | 303 |
| 0 | 1 | 503 | 294 |
| 0 | 2 | 597 | 200 |

## Group structure

One group is a hospital: Cleveland Clinic, the Hungarian Institute of Cardiology (Budapest) or the VA Medical Center (Long Beach). The source's question is whether a probability model carries over to other hospitals: "This model, derived from the clinical and noninvasive test results of 303 patients undergoing angiography at the Cleveland Clinic in Cleveland, Ohio, was applied to a group of 425 patients undergoing angiography at the Hungarian Institute of Cardiology in Budapest, Hungary (disease prevalence 38%); 200 patients undergoing angiography at the Veterans Administration Medical Center in Long Beach, California (disease prevalence 75%)" (Detrano et al. 1989, abstract). So whole hospitals are held out and the model is not told the hospital. Each row is one patient and one prediction.

| field | value |
|---|---|
| group column | `hospital` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 3 |
| rows per group (min / median / max) | 200 / 294.0 / 303 |
| largest group | 38.0% of the rows |
| test groups per fold | 1 |
| groups of two or more rows with a single label | 0.0% |
| nearest neighbour in the same group | 74.3% of the rows (chance: 34.3%) |
| label variance explained by the group | 0.09 (shuffled groups: 0.00) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. Split by hospital: train on two, test on the third

The source built its model at one hospital and applied it at the others (Detrano et al. 1989), and the hospitals differ in disease rate and in which tests they recorded, as a new hospital would. Trained on two hospitals, TabPFN 3.5 reaches ROC AUC 0.888 on Cleveland, 0.906 on Hungary and 0.739 on Long Beach (LR 0.879, 0.903, 0.693), and its mean predicted probability is off where the disease rate differs (46% against 36% in Hungary, 62% against 75% in Long Beach), the source's own finding.

| hospital | patients | disease_pct | ca_missing_pct | thal_missing_pct | slope_missing_pct | chol_missing_pct | exercise_test_missing_pct |
|---|---|---|---|---|---|---|---|
| Cleveland | 303 | 46 | 1 | 1 | 0 | 0 | 0 |
| Hungary | 294 | 36 | 99 | 90 | 65 | 8 | 0 |
| VA Long Beach | 200 | 74 | 99 | 83 | 51 | 28 | 28 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (26 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 2 exact duplicate row(s) (0.3% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)

Accepted on purpose:

- `task_group_count_low`: Three hospitals by design: the source built its model at one hospital and applied it at the others. The fourth hospital (Switzerland) is left out because its published file kept only 8 of its 23 patients without disease.
- `splits_dimensions_off_protocol`: Leave one hospital out gives exactly three splits. More repeats would split the same three hospitals the same way, so they would add copies, not information.
- `groups_test_groups_few`: Testing on one unseen hospital at a time is the task. Each fold still scores 200 to 303 patients one by one (smallest class: 51). The signal carries over to unseen hospitals: the linear model beats the class shares on all three (task probes), and logistic regression reaches ROC AUC 0.868 on held-out hospitals (group probes, 2026-10-21). Most of the variation between folds comes from Long Beach, the hardest hospital.
- `groups_largest_share_high`: Cleveland is a real hospital, one of three, not a catch-all value. When it is the test hospital, the model trains on the other two (494 patients), where two of Cleveland's tests were almost never recorded.

## Data checks

### Feature summary

<details>
<summary>Show the table (15 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| thal | category | 434 | 54.45 | 3 | 3.0, 7.0, 6.0 |
| slope | category | 292 | 36.64 | 3 | 2.0, 1.0, 3.0 |
| exang | category | 54 | 6.78 | 2 | 0.0, 1.0 |
| fbs | category | 15 | 1.88 | 2 | 0.0, 1.0 |
| restecg | category | 1 | 0.13 | 3 | 0.0, 2.0, 1.0 |
| sex | category | 0 | 0 | 2 | 1.0, 0.0 |
| cp | category | 0 | 0 | 4 | 4.0, 3.0, 2.0, 1.0 |
| hospital | category | 0 | 0 | 3 | Cleveland, Hungary, VA Long Beach |
| heart_disease_diagnosis | category | 0 | 0 | 2 | 0, 1 |
| ca | float64 | 493 | 61.86 | 4 | 0.0, 1.0, 2.0, 3.0 |
| chol | float64 | 79 | 9.91 | 216 | 254.0, 220.0, 211.0, 216.0, 219.0, 223.0, 204.0, 230.0, 246.0, 240.0 |
| trestbps | float64 | 58 | 7.28 | 57 | 120.0, 130.0, 140.0, 110.0, 150.0, 160.0, 125.0, 128.0, 138.0, 112.0 |
| oldpeak | float64 | 56 | 7.03 | 43 | 0.0, 1.0, 2.0, 1.5, 3.0, 1.2, 0.8, 0.6, 0.5, 2.5 |
| thalach | float64 | 54 | 6.78 | 110 | 150.0, 140.0, 130.0, 120.0, 160.0, 170.0, 125.0, 110.0, 142.0, 162.0 |
| age | float64 | 0 | 0 | 49 | 54.0, 58.0, 55.0, 52.0, 57.0, 56.0, 59.0, 48.0, 62.0, 51.0 |

</details>

### Target distribution

| heart_disease_diagnosis | count | pct |
|---|---|---|
| 0 | 403 | 50.56 |
| 1 | 394 | 49.44 |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| age | 797 | 53.2321 | 9.45859 | 28 | 77 |
| trestbps | 739 | 132.627 | 17.7862 | 92 | 200 |
| chol | 718 | 246.833 | 58.5271 | 85 | 603 |
| thalach | 743 | 140.171 | 24.9743 | 69 | 202 |
| oldpeak | 741 | 0.914305 | 1.09314 | -0.5 | 6.2 |
| ca | 304 | 0.661184 | 0.933608 | 0 | 3 |

### Categorical features

<details>
<summary>Show the table (29 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| cp | 1 | 4.0 | 398 | 49.94 |
| cp | 2 | 3.0 | 187 | 23.46 |
| cp | 3 | 2.0 | 170 | 21.33 |
| cp | 4 | 1.0 | 42 | 5.27 |
| exang | 1 | 0.0 | 460 | 57.72 |
| exang | 2 | 1.0 | 283 | 35.51 |
| exang | 3 | &lt;NA> | 54 | 6.78 |
| fbs | 1 | 0.0 | 649 | 81.43 |
| fbs | 2 | 1.0 | 133 | 16.69 |
| fbs | 3 | &lt;NA> | 15 | 1.88 |
| heart_disease_diagnosis | 1 | 0 | 403 | 50.56 |
| heart_disease_diagnosis | 2 | 1 | 394 | 49.44 |
| hospital | 1 | Cleveland | 303 | 38.02 |
| hospital | 2 | Hungary | 294 | 36.89 |
| hospital | 3 | VA Long Beach | 200 | 25.09 |
| restecg | 1 | 0.0 | 466 | 58.47 |
| restecg | 2 | 2.0 | 181 | 22.71 |
| restecg | 3 | 1.0 | 149 | 18.7 |
| restecg | 4 | &lt;NA> | 1 | 0.13 |
| sex | 1 | 1.0 | 613 | 76.91 |
| sex | 2 | 0.0 | 184 | 23.09 |
| slope | 1 | &lt;NA> | 292 | 36.64 |
| slope | 2 | 2.0 | 284 | 35.63 |
| slope | 3 | 1.0 | 170 | 21.33 |
| slope | 4 | 3.0 | 51 | 6.4 |
| thal | 1 | &lt;NA> | 434 | 54.45 |
| thal | 2 | 3.0 | 177 | 22.21 |
| thal | 3 | 7.0 | 150 | 18.82 |
| thal | 4 | 6.0 | 36 | 4.52 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
