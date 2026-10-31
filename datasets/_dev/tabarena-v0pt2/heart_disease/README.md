---
report_format: data-foundry-report-v2
unique_name: heart_disease
container_format: 2
checksum: v2:218986ed81ec360cb322338892a18de2d28f1d64ae969093e1fafff0a23aac34
build: null
build_stale: false
data:
  n_rows: 796
  n_features: 13
  dtypes:
    category: 9
    float64: 6
  n_test_dataset_rows: null
task:
  target: heart_disease_diagnosis
  problem_type: binary_classification
  metric: roc_auc
  metric_origin: fallback
  scoring_columns: null
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
    min: 493
    max: 597
  n_test:
    min: 199
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
      is left out because its published file kept only 8 of its about 27 patients
      without disease.'
    splits_dimensions_off_protocol: Leave one hospital out gives exactly three splits.
      More repeats would split the same three hospitals the same way, so they would
      add copies, not information.
    groups_test_groups_few: 'Testing on one unseen hospital at a time is the task.
      Each fold still scores 199 to 303 patients one by one (smallest class: 51).
      The signal carries over to unseen hospitals: the linear model beats the class
      shares at each of the three (task probes, ROC AUC 0.880, 0.898, 0.732). Most
      of the variation between folds comes from Long Beach, the hardest hospital.'
    groups_largest_share_high: Cleveland is a real hospital, one of three, not a catch-all
      value. When it is the test hospital, the model trains on the other two (493
      patients), where two of Cleveland's tests were rarely recorded (`ca` for 5,
      `thal` for 62).
decisions:
- 'Split by hospital: train on two, test on the third'
---

# heart_disease

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Binary classification of `heart_disease_diagnosis`, scored with `roc_auc` on grouped splits by `hospital`. 796 rows and 13 features. Source: UCI (1988).

Not built yet. The current definition gives checksum `v2:218986ed81ec360cb322338892a18de2d28f1d64ae969093e1fafff0a23aac34`.

## In brief

**Question.** Will the angiogram of a patient at a new hospital show a narrowed coronary artery?

**Use case.** For a chest-pain patient referred for angiography, a cardiologist estimates from the history and the noninvasive tests done before it whether the angiogram will show narrowing, with a model built at other hospitals, to decide whether the angiogram is needed. Detrano et al. (1989) built their model in Cleveland and applied it at other hospitals, to spare patients an unnecessary angiogram (p. 309).

**One row.** One of 796 patients examined by angiography at one of three hospitals: Cleveland Clinic (303), the Hungarian Institute of Cardiology in Budapest (294) and the VA Medical Center in Long Beach (199); exams of 1981 to 1987, donated in 1988.

**Predicted.** Whether the angiogram shows more than 50% narrowing in any major coronary artery (49% do; 36% to 74% by hospital).

**Known at prediction time.** Age, sex, chest-pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, an exercise test (peak heart rate, chest pain on exercise, the ECG's ST depression and its slope) and, mostly in Cleveland, calcium seen on fluoroscopy and a thallium scan. Not the hospital, though which tests were recorded tells the hospitals apart.

**What the test data stands for.** Whole hospitals are held out: each split trains on two hospitals and tests on the third, so the test data stands for the patients of a hospital the model has never seen.

**Our changes to the source.** We merge three hospitals' files into one table and split by hospital, leave out the Swiss file (its release dropped most patients without disease), drop one Long Beach patient entered twice, and merge the four grades of disease into one class.

> **Use case fit: approximate (a stand-in with a known gap).** Every patient had been referred for angiography, as at this check, and the features come from tests done before the angiogram (30 exercise tests dated after it, likely date errors, are kept). But Cleveland ran three tests on every patient by study protocol, and two are no longer used: CT has replaced the thallium-201 scan and calcium seen on fluoroscopy.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
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
| rows x columns | 796 x 15 |
| task.target | heart_disease_diagnosis |
| task.problem_type | binary_classification |
| task.metric | roc_auc |
| task.split_regime | grouped_non_iid |
| task.stratify_on | heart_disease_diagnosis |
| task.group_on | hospital |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `roc_auc` (standard; takes proba; higher is better) |
| origin | fallback: the default for the problem type: the source defines no metric the task would use in practice |
| definition | area under the ROC curve |
| reason | Detrano et al. 1989 score reliability, the mean predicted probability against the disease rate (calibration in the large) and by quintiles (p. 306), and clinical utility, the percent correctly classified over the thresholds 0.2 to 0.8 they call relevant for angiography decisions (p. 307): no single threshold, so a threshold-free metric (MET-7); UCI's heart-disease.names reports accuracy at 0.5, a default. No costs of errors: UCI's costs/ folder holds the prices of the tests, and Statlog's 5:1 heart cost matrix belongs to a later 270-row cut of the Cleveland file, not to this source. ROC AUC per held-out hospital does not score reliability. roc_auc is the binary fallback. |

<details>
<summary>Feature types: 7 categorical, 2 ordinal, 0 string, 0 datetime</summary>

- categorical (7): `hospital`, `sex`, `fbs`, `restecg`, `exang`, `thal`, `heart_disease_diagnosis`
- ordinal (2): `slope (upsloping < flat < downsloping)`, `cp (asymptomatic < non-anginal pain < atypical angina < typical angina)`
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

The first 5 of 796 rows of the final frame (random rows: the frame is shuffled); 12 of 15 columns, the target first. Cells are cut at 40 characters.

| heart_disease_diagnosis | age | sex | cp | trestbps | chol | fbs | restecg | thalach | exang | oldpeak | slope |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Yes | 56 | male | asymptomatic | nan | nan | 0 | left ventricular hypertrophy | nan | nan | nan | nan |
| Yes | 60 | male | non-anginal pain | 140 | 185 | 0 | left ventricular hypertrophy | 155 | 0 | 3 | flat |
| No | 51 | female | non-anginal pain | 110 | 190 | 0 | normal | 120 | 0 | 0 | nan |
| Yes | 46 | male | asymptomatic | 118 | 186 | 0 | normal | 124 | 0 | 0 | nan |
| Yes | 54 | male | atypical angina | 192 | 283 | 0 | left ventricular hypertrophy | 195 | 0 | 0 | upsloping |

## Curation notes

We start with the processed files of three hospitals from UCI's Heart Disease collection, the 13 variables of the Detrano et al. (1989) model and its label (p. 305; pages of Am J Cardiol 64:304-310). UCI's raw 76-attribute files hold the same 294 Hungarian, 200 Long Beach and 123 Swiss patients, so the patients the release dropped are not public.

- Prediction point: after the referral for angiography, before the angiogram, with the history, the resting tests and the exercise test at hand. `ca` (major arteries with calcium seen on cardiac fluoroscopy, 0-3) and `thal` (exercise thallium scan) are noninvasive tests done before the angiogram (Detrano et al. 1986, PMID 3698241 and 3706156; in Cleveland by research protocol, read after the angiogram and without knowledge of its result, p. 305), so neither is read from it. In 30 patients the raw files date the angiogram before the exercise test (Cleveland 11, by 7 to 449 days; Hungary 13, by 1 to 367 days; Long Beach 6, by 7 to 15 days and one by 369), and one Long Beach angiogram is dated 1901; the codebook doubts this date field ("cmo: month of cardiac cath (sp?) (perhaps 'call')"), and the paper has every test within 6 weeks before the angiogram (p. 306). Kept: 15 of the 30 are diseased, and blanking their exercise tests leaves the linear model's ROC AUC at 0.836.
- One study, three tasks merged: the files share the attributes, their coding and the label (though `ca` and `thal` were recorded almost only in Cleveland), and a model trained on the other two hospitals ranks a hospital's patients nearly as well as one trained there (logistic regression ROC AUC 0.880 on Cleveland, 0.898 on Hungary, 0.732 on Long Beach; trained in-site 0.905, 0.905, 0.663; TabPFN 3.5 gave 0.888, 0.906, 0.739 against 0.913, 0.914, 0.708 in the first run, not reproduced since). We concatenate the files and keep the hospital as the group column.
- Split by hospital, the source's design generalised: Detrano et al. built their model on the Cleveland patients and "applied [it] to" the patients of the other hospitals (abstract, p. 305); here every hospital is tested once. A hospital brings its own disease rate (46% in Cleveland, 36% in Budapest, 74% in Long Beach; the paper's Table I gives 46%, 38% and 74%) and its own test habits (`ca` and `thal` recorded almost only in Cleveland, no exercise test for 53 Long Beach patients). Held out whole, a hospital is scored on its own patients only: a random split would compare patients of two hospitals in 68% of its positive-negative pairs, and the hospital's disease rate alone would reach a pooled ROC AUC of 0.65. The model is not given the hospital, but the features tell the hospitals apart (91% accuracy, 85% from which tests are missing); reweighting the training hospitals to one disease rate changes the mean ROC AUC by 0.003 or less.
- Note: three hospitals give three splits, the case in which `covertype` (three areas) went back to a random split. Here the transfer to a new hospital is the source's design, no class drops out (51 or more patients of each class in every test fold), and resampling the patients of each held-out hospital separates 7 of 15 pairs of model families, against 4 to 5 for a random 10 x 3 split. `sepsis_prediction_1m` kept its hospitals as a feature because its use case is the known hospitals.
- Note: the task probes flag `unstable` (standard error of the best family's mean skill 0.105 over the 3 splits). The linear model beats the class shares at every held-out hospital (ROC AUC 0.880, 0.898, 0.732); the spread is Long Beach, the hardest hospital under every split, in-site too. Kept as one atypical group, as `musk` and `pancreatic_cancer_mouse_detection` were; re-check with tuned results after the build.
- Switzerland left out: its UCI file keeps 123 of the paper's 143 patients and only 8 of its about 27 without disease (94% diseased against 81% by the paper's Table I, 85% of 85 in Basel and 74% of 58 in Zurich; the abstract gives 84%; cholesterol 0 in every row), so its disease rate is the release's, not the hospital's, and as a held-out hospital it would be scored on 8 patients without disease.
- Missing values: "?" becomes NaN. Cholesterol 0 (49 Long Beach rows) and resting blood pressure 0 (1 row) are impossible and become NaN. Other missing values stay: whether a test was done is known before the angiogram, and the source's model was built for patients with only some tests (352 logistic regressions, one per clinically relevant set of variables, p. 305). The test hospitals did the thallium scan for a minority (Table II: 41 patients in Long Beach, 33 in Budapest) and the paper lists no fluoroscopy among their data (p. 306), so `ca` and `thal` are missing by the hospitals' practice, not by the release. Recording differs by hospital and is not harmonised: Hungary and Long Beach leave `slope` blank when there is no ST depression (188 of the 190 blanks in Hungary), Cleveland records it (99 rows); `restecg` left ventricular hypertrophy is 49% of Cleveland's patients and 2% of Hungary's. Harmonising `slope` changes the ROC AUC by under 0.003.
- Target: `num` (0 = no narrowing over 50%, 1-4 = disease grades; the Hungarian file holds only 0/1) becomes the binary `heart_disease_diagnosis` (Yes/No), as in the study.
- Codes get their labels from UCI's `heart-disease.names`: `sex`; `cp` typical angina, atypical angina, non-anginal pain, asymptomatic; `restecg` normal, ST-T wave abnormality, left ventricular hypertrophy; `slope` of the peak-exercise ST segment upsloping, flat, downsloping; `thal` normal, fixed defect, reversible defect. `fbs` (fasting blood sugar over 120 mg/dl) and `exang` (angina on exercise) stay 0/1 flags. `oldpeak` is the ST depression on exercise relative to rest; one Long Beach value is negative.
- Anomaly: the Hungarian file keeps 294 of the paper's 425 patients (36% diseased against 38%); the paper took all catheterizations of 1983 to 1987 without prior infarction or valve disease (p. 306), and how the 294 were chosen is not stated.
- Duplicates: the Long Beach pair of equal rows is one patient entered twice (the raw file gives both the same exercise and angiogram dates and the same ten vessel readings, which no other Long Beach pair shares), so one is dropped. The Hungarian pair is two patients (exams in March and May 1986) and stays.
- Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 2 columns are ordered categories in
  the order of the source's codebook (`ORDINAL_LEVELS`).

## Splits

Leave one hospital out: three splits, each training on two hospitals and testing on the third (Cleveland, Hungary, then Long Beach), one repeat, since repeating a split of three groups into three folds gives the same splits. The source built its model in Cleveland and applied it at the other hospitals; leaving each hospital out in turn generalises that design so that every hospital is tested once. With three hospitals the scores are three numbers and differ by hospital (Long Beach is the hardest). Unlike `covertype`'s three areas, the transfer is the source's design and no class drops out (curation notes).

1 repeat(s) x 3 fold(s) with seed 4267; train 493 to 597 rows, test 199 to 303 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 493 | 303 |
| 0 | 1 | 502 | 294 |
| 0 | 2 | 597 | 199 |

## Group structure

One group is a hospital: Cleveland Clinic, the Hungarian Institute of Cardiology (Budapest) or the VA Medical Center (Long Beach). The source's question is whether a probability model carries over to other hospitals: "This model, derived from the clinical and noninvasive test results of 303 patients undergoing angiography at the Cleveland Clinic in Cleveland, Ohio, was applied to a group of 425 patients undergoing angiography at the Hungarian Institute of Cardiology in Budapest, Hungary (disease prevalence 38%); 200 patients undergoing angiography at the Veterans Administration Medical Center in Long Beach, California (disease prevalence 75%); ..." (Detrano et al. 1989, abstract). So whole hospitals are held out and the model is not told the hospital. Each row is one patient and one prediction.

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
| rows per group (min / median / max) | 199 / 294.0 / 303 |
| largest group | 38.1% of the rows |
| test groups per fold | 1 |
| groups of two or more rows with a single label | 0.0% |
| nearest neighbour in the same group | 74.2% of the rows (chance: 34.3%) |
| label variance explained by the group | 0.09 (shuffled groups: 0.00) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. Split by hospital: train on two, test on the third

The source built its model at one hospital and applied it at the others (Detrano et al. 1989, p. 305), and the hospitals differ in disease rate and in which tests they recorded, as a new hospital would. Trained on the other two hospitals, logistic regression reaches ROC AUC 0.880 on Cleveland, 0.898 on Hungary and 0.732 on Long Beach. The paper has the Cleveland model overpredicting disease by 10 points in Budapest and 5 in Long Beach (abstract, p. 307); our models overpredict in Hungary too but underpredict in Long Beach, mostly for its patients without an exercise test. ROC AUC within one hospital does not score this.

| hospital | patients | disease_pct | ca_missing_pct | thal_missing_pct | slope_missing_pct | chol_missing_pct | no_exercise_test |
|---|---|---|---|---|---|---|---|
| Cleveland | 303 | 46 | 1 | 1 | 0 | 0 | 0 |
| Hungary | 294 | 36 | 99 | 90 | 65 | 8 | 0 |
| VA Long Beach | 199 | 74 | 99 | 83 | 51 | 28 | 53 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (26 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 1 exact duplicate row(s) (0.1% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)

Accepted on purpose:

- `task_group_count_low`: Three hospitals by design: the source built its model at one hospital and applied it at the others. The fourth hospital (Switzerland) is left out because its published file kept only 8 of its about 27 patients without disease.
- `splits_dimensions_off_protocol`: Leave one hospital out gives exactly three splits. More repeats would split the same three hospitals the same way, so they would add copies, not information.
- `groups_test_groups_few`: Testing on one unseen hospital at a time is the task. Each fold still scores 199 to 303 patients one by one (smallest class: 51). The signal carries over to unseen hospitals: the linear model beats the class shares at each of the three (task probes, ROC AUC 0.880, 0.898, 0.732). Most of the variation between folds comes from Long Beach, the hardest hospital.
- `groups_largest_share_high`: Cleveland is a real hospital, one of three, not a catch-all value. When it is the test hospital, the model trains on the other two (493 patients), where two of Cleveland's tests were rarely recorded (`ca` for 5, `thal` for 62).

## Data checks

### Feature summary

<details>
<summary>Show the table (15 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| thal | category | 433 | 54.4 | 3 | normal, reversible defect, fixed defect |
| slope | category | 291 | 36.56 | 3 | flat, upsloping, downsloping |
| exang | category | 54 | 6.78 | 2 | 0.0, 1.0 |
| fbs | category | 15 | 1.88 | 2 | 0.0, 1.0 |
| restecg | category | 1 | 0.13 | 3 | normal, left ventricular hypertrophy, ST-T wave abnormality |
| sex | category | 0 | 0 | 2 | male, female |
| cp | category | 0 | 0 | 4 | asymptomatic, non-anginal pain, atypical angina, typical angina |
| hospital | category | 0 | 0 | 3 | Cleveland, Hungary, VA Long Beach |
| heart_disease_diagnosis | category | 0 | 0 | 2 | No, Yes |
| ca | float64 | 492 | 61.81 | 4 | 0.0, 1.0, 2.0, 3.0 |
| chol | float64 | 79 | 9.92 | 216 | 254.0, 220.0, 216.0, 223.0, 230.0, 211.0, 204.0, 219.0, 246.0, 240.0 |
| trestbps | float64 | 58 | 7.29 | 57 | 120.0, 130.0, 140.0, 110.0, 150.0, 160.0, 125.0, 128.0, 138.0, 112.0 |
| oldpeak | float64 | 56 | 7.04 | 43 | 0.0, 1.0, 2.0, 1.5, 3.0, 1.2, 0.8, 0.5, 0.6, 2.5 |
| thalach | float64 | 54 | 6.78 | 110 | 150.0, 140.0, 130.0, 160.0, 120.0, 170.0, 125.0, 110.0, 142.0, 162.0 |
| age | float64 | 0 | 0 | 49 | 54.0, 58.0, 55.0, 57.0, 52.0, 59.0, 56.0, 48.0, 51.0, 62.0 |

</details>

### Target distribution

| heart_disease_diagnosis | count | pct |
|---|---|---|
| No | 403 | 50.63 |
| Yes | 393 | 49.37 |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| age | 796 | 53.2261 | 9.46302 | 28 | 77 |
| trestbps | 738 | 132.603 | 17.7867 | 92 | 200 |
| chol | 717 | 246.872 | 58.5587 | 85 | 603 |
| thalach | 742 | 140.201 | 24.9778 | 69 | 202 |
| oldpeak | 740 | 0.915541 | 1.09336 | -0.5 | 6.2 |
| ca | 304 | 0.661184 | 0.933608 | 0 | 3 |

### Categorical features

<details>
<summary>Show the table (29 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| cp | 1 | asymptomatic | 398 | 50 |
| cp | 2 | non-anginal pain | 186 | 23.37 |
| cp | 3 | atypical angina | 170 | 21.36 |
| cp | 4 | typical angina | 42 | 5.28 |
| exang | 1 | 0.0 | 460 | 57.79 |
| exang | 2 | 1.0 | 282 | 35.43 |
| exang | 3 | &lt;NA> | 54 | 6.78 |
| fbs | 1 | 0.0 | 648 | 81.41 |
| fbs | 2 | 1.0 | 133 | 16.71 |
| fbs | 3 | &lt;NA> | 15 | 1.88 |
| heart_disease_diagnosis | 1 | No | 403 | 50.63 |
| heart_disease_diagnosis | 2 | Yes | 393 | 49.37 |
| hospital | 1 | Cleveland | 303 | 38.07 |
| hospital | 2 | Hungary | 294 | 36.93 |
| hospital | 3 | VA Long Beach | 199 | 25 |
| restecg | 1 | normal | 466 | 58.54 |
| restecg | 2 | left ventricular hypertrophy | 181 | 22.74 |
| restecg | 3 | ST-T wave abnormality | 148 | 18.59 |
| restecg | 4 | &lt;NA> | 1 | 0.13 |
| sex | 1 | male | 612 | 76.88 |
| sex | 2 | female | 184 | 23.12 |
| slope | 1 | &lt;NA> | 291 | 36.56 |
| slope | 2 | flat | 284 | 35.68 |
| slope | 3 | upsloping | 170 | 21.36 |
| slope | 4 | downsloping | 51 | 6.41 |
| thal | 1 | &lt;NA> | 433 | 54.4 |
| thal | 2 | normal | 177 | 22.24 |
| thal | 3 | reversible defect | 150 | 18.84 |
| thal | 4 | fixed defect | 36 | 4.52 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
