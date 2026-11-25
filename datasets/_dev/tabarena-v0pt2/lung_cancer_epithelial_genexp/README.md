---
report_format: data-foundry-report-v2
unique_name: lung_cancer_epithelial_genexp
container_format: 2
checksum: v2:d75740bb668e5543526eed1025c298525d053a428d6fe57c950e585cc47682c0
build:
  uuid: 01a111fa-e441-7be0-b4cb-2b1c80c2c167
  checksum: v2:9108c0046efd8a3e052dd8570cc2bbe16449de9df488bfeb5f5d205f03e38493
  built_at: '2026-10-06T16:10:55+00:00'
  path: lung_cancer_epithelial_genexp/01a111fa-e441-7be0-b4cb-2b1c80c2c167
  data_foundry_version: 0.0.5
  git_sha: 8fbc4745ab8de19d5bc0c98a89b008f5d779909f-dirty
  libraries:
    python: 3.11.14
    pandas: 2.3.3
    numpy: 2.1.3
    pyarrow: 20.0.0
    scikit-learn: 1.7.2
    polars: 1.41.1
build_stale: true
data:
  n_rows: 163
  n_features: 22223
  dtypes:
    category: 8
    float64: 22216
    int64: 1
  n_test_dataset_rows: null
task:
  target: DiagnosedCancer
  problem_type: binary_classification
  metric: roc_auc
  metric_origin: fallback
  scoring_columns: null
  split_regime: grouped_non_iid
  stratify_on: DiagnosedCancer
  time_on: null
  group_on: scan_period
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 6
    test_groups_per_fold:
      min: 2
      max: 2
splits:
  n_repeats: 20
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 108
    max: 109
  n_test:
    min: 54
    max: 55
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos: []
  accepted:
    task_group_count_low: 'Six scan periods by design (2026-11-12, Andrej): the 163
      arrays cannot form forward windows of a usable size, and periods of about half
      a year of scans keep each period''s scan signature on one side; each test fold
      holds 54 or 55 arrays.'
    groups_test_groups_few: 'Two periods per test fold is what six periods allow;
      each fold still scores 54 or 55 arrays one by one. The signal carries across
      held-out periods: on the 163 arrays with the clinical findings, untuned LightGBM
      (ROC AUC 0.668 to 0.917, mean 0.793) and logistic regression (0.650 to 0.905,
      mean 0.769) beat chance on all 14 test pairs that occur (run of 2026-11-13).
      The repeats reuse the same pairs, so the spread across repeats is descriptive.'
decisions: []
---

# lung_cancer_epithelial_genexp

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Binary classification of `DiagnosedCancer`, scored with `roc_auc` on grouped splits by `scan_period`. 163 rows and 22,223 features. Source: GOV Website (2006).

Built as `01a111fa-e441-7be0-b4cb-2b1c80c2c167` on 2026-10-06, but `dataset.py` has changed since: it now gives checksum `v2:d75740bb668e5543526eed1025c298525d053a428d6fe57c950e585cc47682c0`, so the build is stale. See [Build](#build).

## In brief

**Question.** Does a smoker with suspected lung cancer have it, judging from gene activity in cells brushed from the airway?

**Use case.** During bronchoscopy for suspected lung cancer, a pulmonologist brushes cells from the normal-looking airway and uses their gene expression to judge whether the patient has cancer and needs further invasive tests (Spira et al. 2007).

**One row.** One smoker undergoing bronchoscopy for suspected lung cancer (163 patients of the extended GEO release GSE4115 whose arrays passed the authors' quality control).

**Predicted.** Whether the patient was finally diagnosed with lung cancer (48% were); the time to the final diagnosis is not stated.

**Known at prediction time.** The measured activity of about 22,000 gene probes (Affymetrix microarrays) in the brushed airway cells, and 8 clinical findings known before the brushing: age, sex, race, smoking status, pack-years, coughing up blood, and from the chest CT a mass over 3 cm and enlarged lymph nodes.

**What the test data stands for.** Grouped by scan period: the arrays fall into six periods of their scan order (about half a year of scans each), and a test period is never in training, so a model meets arrays of a period it has not seen.

**Our changes to the source.** We use the extended release of 192 patients, not the paper's 129, and drop the 5 without a diagnosis and the 24 arrays that failed the authors' quality control. The split holds out whole scan periods (sixths of the sample number, which follows the scan order). The 8 clinical findings join the expression; the bronchoscopy's own result and the study's later risk rating stay out.

> **Use case fit: direct (the rows, features and split mirror the use case).** The sample is taken at the bronchoscopy, before the diagnosis is known, and the clinical findings are there at that point too; a held-out patient is a new one. The clinical findings predict better than the expression, which adds a little to them. The task is small, with 163 patients and far more genes than patients.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/lung_cancer_epithelial_genexp.md`](../../../../curation/records/lung_cancer_epithelial_genexp.md)
- The original source: <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4115>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/lung_cancer_epithelial_genexp/`. To get them:

```text
We download the original gene expression data from the GEO records.

mkdir -p local-data-warehouse/lung_cancer_epithelial_genexp/ && wget -P local-data-warehouse/lung_cancer_epithelial_genexp/ https://ftp.ncbi.nlm.nih.gov/geo/series/GSE4nnn/GSE4115/matrix/GSE4115_series_matrix.txt.gz && gzip -d local-data-warehouse/lung_cancer_epithelial_genexp/GSE4115_series_matrix.txt.gz
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/lung_cancer_epithelial_genexp   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/lung_cancer_epithelial_genexp   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | GOV Website: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4115 |
| year | 2006 |
| domain | medical & healthcare |
| license | Public Domain |
| data_tags | Non-IID, Grouped, ForcedGroupedFromTemporal |
| reference | spira2007airway |
| rows x columns | 163 x 22,225 |
| task.target | DiagnosedCancer |
| task.problem_type | binary_classification |
| task.metric | roc_auc |
| task.split_regime | grouped_non_iid |
| task.stratify_on | DiagnosedCancer |
| task.group_on | scan_period |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `roc_auc` (standard; takes proba; higher is better) |
| origin | fallback: the default for the problem type: the source defines no metric the task would use in practice |
| definition | area under the ROC curve |
| reason | Spira et al. 2007 report accuracy with sensitivity and specificity of the 80-gene predictor (83/80/84%); the clinical claim rests on sensitivity and NPV, no single metric or threshold. roc_auc is the binary fallback. |

<details>
<summary>Feature types: 8 categorical, 0 string, 0 datetime</summary>

- categorical (8): `scan_period`, `sex`, `race`, `smoking_status`, `haemoptysis`, `lymphadenopathy`, `mass_over_3cm`, `DiagnosedCancer`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{spira2007airway,
  title={Airway epithelial gene expression in the diagnostic evaluation of smokers with suspect lung cancer},
  author={Spira, Avrum and Beane, Jennifer E and Shah, Vishal and Steiling, Katrina and Liu, Gang and Schembri, Frank and Gilman, Sean and Dumas, Yves-Martine and Calner, Paul and Sebastiani, Paola and others},
  journal={Nature medicine},
  volume={13},
  number={3},
  pages={361--366},
  year={2007},
  publisher={Nature Publishing Group US New York}
}
```

</details>

## Sample rows

The first 5 of 163 rows of the final frame (random rows: the frame is shuffled); 12 of 22,225 columns, the target first. Cells are cut at 40 characters.

| DiagnosedCancer | 1007_s_at | 1053_at | 117_at | 121_at | 1255_g_at | 1294_at | 1316_at | 1320_at | 1405_i_at | 1431_at | 1438_at |
|---|---|---|---|---|---|---|---|---|---|---|---|
| No | 10.2997 | 4.44334 | 5.80902 | 8.25995 | 3.57021 | 7.71609 | 5.04596 | 4.24673 | 6.34377 | 3.23305 | 6.60546 |
| Yes | 10.3747 | 4.3794 | 5.46601 | 7.77881 | 3.65197 | 7.14061 | 4.84792 | 4.04368 | 5.63206 | 3.19457 | 6.68302 |
| Yes | 10.4313 | 4.38455 | 5.50215 | 7.98956 | 3.652 | 7.19341 | 4.92118 | 4.19848 | 4.86397 | 3.13989 | 6.57728 |
| Yes | 9.93224 | 4.43235 | 5.82058 | 7.94284 | 3.51844 | 7.35428 | 5.20462 | 4.33307 | 5.58149 | 3.6294 | 6.76051 |
| Yes | 10.4429 | 4.23708 | 5.71135 | 8.02954 | 3.65482 | 7.3255 | 5.0946 | 4.30711 | 4.92736 | 3.53331 | 6.53288 |

## Curation notes

- We start with an extended dataset of 192 patients. The original reference uses 129 samples as "Individuals without final diagnoses as of May 2005 were excluded from this primary dataset". We remove 5 samples without a clear label ("Smoker with suspect lung cancer Sample"), yielding a dataset of 187 samples.
- Quality control (2026-11-13, Andrej): we drop the 24 arrays for which GEO gives no clinical characteristics, leaving 163 (78 cancer). The series says "23 of these samples were then filtered for quality control reasons", and these 24 correlate worse with the median profile (median 0.93 against 0.98), so they are most likely the arrays the authors removed; GEO gives no list. They were 19 cancer and 5 not (79%, against 48% among the rest; Fisher exact p = 0.004), all from the submission of 2006-01-29, so a failed array mostly meant cancer, and with the clinical findings in, trees read their empty fields as cancer. Kept as test-only rows they would cost every model 0.05 to 0.13 ROC AUC, scored as no cancer as a block, and a clinic never reads an array that failed its quality control.
- We use "Sample_title" from the metadata as labels for the prediction task.
- Scan period (2026-11-12, Andrej): each title carries a sample number (56 to 328), which is the scan order. The CEL files of 31 arrays survive in linked GEO copies (28 in GSE19027), and their scan dates, April 2003 to January 2006, follow the number at Spearman 0.997. We cut the rank of the number among the 163 kept arrays into six periods of 27 or 28 arrays (`scan_period`, the split's group) and do not ship the number itself.
- Time basis: ForcedGroupedFromTemporal: the arrays were scanned over almost three years in the order of their sample number. Arrays of one period share a scan signature (within each class the expression tells the later from the earlier arrays at ROC AUC 0.90 to 0.98), and the cancer share moves from 4% to 70% between periods, so random folds let a model read a period's cancer share: held-out periods score 0.05 to 0.14 ROC AUC lower than random folds at equal training size (on all 187 arrays, before the quality-control drop; on the 163 kept ones older-to-newer halves score 0.05 (LR) and 0.10 (LightGBM) below random halves). Forward windows cannot be scored with 163 arrays (three windows of 27; on the 187 arrays the oldest of three windows of 31 ranked below chance whatever trained), so whole periods are held out, and training includes later periods. The relation itself did not drift measurably: 56 training arrays near the test period or far from it score the same (LR +0.003, LightGBM +0.008). Not tested: patients scanned after every training array, as a forward window would test.
- Clinical findings (2026-11-13, Andrej): the 8 findings GEO gives for 163 arrays join the expression: `age`, `sex`, `race`, `smoking_status`, `pack_years`, `haemoptysis`, `lymphadenopathy` (hilar or mediastinal nodes over 1 cm on the chest CT) and `mass_over_3cm` (on the chest CT), the variables of the clinical model of Beane et al. 2008 (Cancer Prevention Research 1(1):56-64, https://doi.org/10.1158/1940-6207.CAPR-08-0011). They are known at the bronchoscopy, and none is the diagnosis, which came from pathology or follow-up. On the 163 arrays and the grouped splits (logistic regression, ROC AUC): clinical only 0.819, expression only 0.744, both 0.834 (expression adds +0.015, SE 0.006; +0.036 on the 118 non-diagnostic bronchoscopies); untuned LightGBM 0.800, 0.742 and 0.767. All 8 are complete for the 163 kept arrays.
- Left out on purpose: `bronch_status`, whether this bronchoscopy's cytopathology gave the diagnosis (40 of 78 cancers, 5 of 85 others), which arrives after the brushing and is the diagnosis for half the cancers; `subjective_assessment`, a risk rating made for the study afterwards by three pulmonologists blinded to the outcome (ROC AUC 0.897 alone), which no clinic records; `biomarker_score`, the 80-gene predictor fitted on the labels; `cancer_status` and `sample_id`, the label and the title's number.
- Potential leak, kept on purpose: GSE4115 holds RMA values, which quantile-normalise all arrays processed together, so a sample's values depend on the others (per-sample medians vary by an SD of only 0.053 log2 over 187 samples); there are no CEL files to redo it per sample. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if raw arrays appear.

## Splits

Stratified grouped 3-fold cross-validation over the six scan periods with 20 repeats: each test fold holds two
whole periods (54 or 55 arrays), and no period sits on both sides. The periods by sample number among the 163
arrays that passed quality control: 56-98 (28 arrays, scanned April-May 2003, 4% cancer), 99-139 (27, October
2003, 41%), 140-177 (27, March-April 2004, 59%), 181-226 (27, July-December 2004, 70%), 228-273 (27,
February-March 2005, 63%) and 274-328 (27, May 2005 to January 2006, 52%; most of the prospective five-centre
set); the scan months are those of the dated arrays in each range. Six periods allow at most 15 distinct test
pairs (14 occur over the 20 repeats), so the repeats recur and fold scores spread wider than under random folds
(fold SD about 0.09 ROC AUC against 0.05). Grouping replaced random patients on 2026-11-12 (Andrej):
random folds scored 0.05 to 0.14 ROC AUC higher than held-out periods at equal training size
(curation notes).

20 repeat(s) x 3 fold(s) with seed 4267; train 108 to 109 rows, test 54 to 55 rows.

<details>
<summary>Show all 60 splits</summary>

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 109 | 54 |
| 0 | 1 | 108 | 55 |
| 0 | 2 | 109 | 54 |
| 1 | 0 | 109 | 54 |
| 1 | 1 | 109 | 54 |
| 1 | 2 | 108 | 55 |
| 2 | 0 | 109 | 54 |
| 2 | 1 | 108 | 55 |
| 2 | 2 | 109 | 54 |
| 3 | 0 | 108 | 55 |
| 3 | 1 | 109 | 54 |
| 3 | 2 | 109 | 54 |
| 4 | 0 | 108 | 55 |
| 4 | 1 | 109 | 54 |
| 4 | 2 | 109 | 54 |
| 5 | 0 | 109 | 54 |
| 5 | 1 | 108 | 55 |
| 5 | 2 | 109 | 54 |
| 6 | 0 | 108 | 55 |
| 6 | 1 | 109 | 54 |
| 6 | 2 | 109 | 54 |
| 7 | 0 | 108 | 55 |
| 7 | 1 | 109 | 54 |
| 7 | 2 | 109 | 54 |
| 8 | 0 | 109 | 54 |
| 8 | 1 | 109 | 54 |
| 8 | 2 | 108 | 55 |
| 9 | 0 | 108 | 55 |
| 9 | 1 | 109 | 54 |
| 9 | 2 | 109 | 54 |
| 10 | 0 | 108 | 55 |
| 10 | 1 | 109 | 54 |
| 10 | 2 | 109 | 54 |
| 11 | 0 | 108 | 55 |
| 11 | 1 | 109 | 54 |
| 11 | 2 | 109 | 54 |
| 12 | 0 | 109 | 54 |
| 12 | 1 | 108 | 55 |
| 12 | 2 | 109 | 54 |
| 13 | 0 | 108 | 55 |
| 13 | 1 | 109 | 54 |
| 13 | 2 | 109 | 54 |
| 14 | 0 | 109 | 54 |
| 14 | 1 | 108 | 55 |
| 14 | 2 | 109 | 54 |
| 15 | 0 | 108 | 55 |
| 15 | 1 | 109 | 54 |
| 15 | 2 | 109 | 54 |
| 16 | 0 | 108 | 55 |
| 16 | 1 | 109 | 54 |
| 16 | 2 | 109 | 54 |
| 17 | 0 | 108 | 55 |
| 17 | 1 | 109 | 54 |
| 17 | 2 | 109 | 54 |
| 18 | 0 | 108 | 55 |
| 18 | 1 | 109 | 54 |
| 18 | 2 | 109 | 54 |
| 19 | 0 | 108 | 55 |
| 19 | 1 | 109 | 54 |
| 19 | 2 | 109 | 54 |

</details>

## Group structure

One group is a scan period: a sixth of the arrays in the order of the sample number in their GEO titles
(27 or 28 arrays), which follows the scan dates (April 2003 to January 2006, from the CEL headers of 31
arrays in linked GEO copies). The arrays of one period share a scan signature and the cancer share differs
between periods (4% to 70%), so a random split lets a model read the period's share. A pulmonologist
brushes a new patient's airway after every array a model was trained on, and the release cannot form
forward windows of a usable size, so whole periods are held out (forced from temporal). The source's
authors recruited the patients from January 2003 to April 2005 at four medical centres and validated on a
set collected prospectively from June 2005 to January 2006 at five (Spira et al. 2007; Beane et al. 2008).
Each array is one prediction, made from its own expression.

| field | value |
|---|---|
| group column | `scan_period` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 6 |
| rows per group (min / median / max) | 27 / 27.0 / 28 |
| largest group | 17.2% of the rows |
| test groups per fold | 2 |
| groups of two or more rows with a single label | 0.0% |
| nearest neighbour in the same group | 58.9% of the rows (chance: 16.2%) |
| label variance explained by the group | 0.20 (shuffled groups: 0.03) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Bundle checks

0 error(s), 0 warning(s), 0 info (28 checks run, plus the dataset's own checks).


Accepted on purpose:

- `task_group_count_low`: Six scan periods by design (2026-11-12, Andrej): the 163 arrays cannot form forward windows of a usable size, and periods of about half a year of scans keep each period's scan signature on one side; each test fold holds 54 or 55 arrays.
- `groups_test_groups_few`: Two periods per test fold is what six periods allow; each fold still scores 54 or 55 arrays one by one. The signal carries across held-out periods: on the 163 arrays with the clinical findings, untuned LightGBM (ROC AUC 0.668 to 0.917, mean 0.793) and logistic regression (0.650 to 0.905, mean 0.769) beat chance on all 14 test pairs that occur (run of 2026-11-13). The repeats reuse the same pairs, so the spread across repeats is descriptive.

## Data checks

### Feature summary

<details>
<summary>Show the table (22,225 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| DiagnosedCancer | category | 0 | 0 | 2 | No, Yes |
| scan_period | category | 0 | 0 | 6 | period_1, period_2, period_3, period_4, period_5, period_6 |
| sex | category | 0 | 0 | 2 | male, female |
| race | category | 0 | 0 | 2 | Caucasian, other |
| smoking_status | category | 0 | 0 | 2 | quit less than 10 years, quit for 10 years or greater |
| haemoptysis | category | 0 | 0 | 2 | no, yes |
| lymphadenopathy | category | 0 | 0 | 2 | no, yes |
| mass_over_3cm | category | 0 | 0 | 2 | no, yes |
| 1007_s_at | float64 | 0 | 0 | 163 | 10.2997, 10.3747, 10.4313, 9.9322, 10.4429, 10.0164, 10.0359, 9.8478, 9.4108, 1… |
| 1053_at | float64 | 0 | 0 | 163 | 4.4433, 4.3794, 4.3846, 4.4323, 4.2371, 4.2715, 4.2379, 4.2311, 4.5571, 4.209 |
| 117_at | float64 | 0 | 0 | 163 | 5.809, 5.466, 5.5022, 5.8206, 5.7114, 5.5741, 5.3908, 6.0464, 6.1339, 5.628 |
| 121_at | float64 | 0 | 0 | 163 | 8.2599, 7.7788, 7.9896, 7.9428, 8.0295, 7.8893, 8.0463, 8.4421, 8.1474, 8.1587 |
| 1255_g_at | float64 | 0 | 0 | 163 | 3.5702, 3.652, 3.652, 3.5184, 3.6548, 3.535, 3.7184, 4.1278, 3.4777, 3.7093 |
| 1294_at | float64 | 0 | 0 | 163 | 7.7161, 7.1406, 7.1934, 7.3543, 7.3255, 7.22, 7.2224, 7.3253, 7.6868, 7.5689 |
| 1316_at | float64 | 0 | 0 | 163 | 5.046, 4.8479, 4.9212, 5.2046, 5.0946, 4.9722, 5.1997, 5.274, 5.1409, 5.2191 |
| 1320_at | float64 | 0 | 0 | 163 | 4.2467, 4.0437, 4.1985, 4.3331, 4.3071, 4.1067, 4.2932, 4.3896, 4.2952, 4.1455 |
| 1405_i_at | float64 | 0 | 0 | 163 | 6.3438, 5.6321, 4.864, 5.5815, 4.9274, 6.0663, 5.9223, 7.3326, 6.4197, 5.8336 |
| 1431_at | float64 | 0 | 0 | 163 | 3.233, 3.1946, 3.1399, 3.6294, 3.5333, 3.1318, 3.3025, 3.4299, 3.5447, 3.3906 |
| 1438_at | float64 | 0 | 0 | 163 | 6.6055, 6.683, 6.5773, 6.7605, 6.5329, 6.4293, 6.5085, 6.8042, 6.7408, 6.7956 |
| 1487_at | float64 | 0 | 0 | 163 | 7.5499, 7.4098, 7.4771, 7.2215, 7.362, 7.3185, 7.2717, 7.413, 7.4747, 7.5652 |
| 1494_f_at | float64 | 0 | 0 | 163 | 6.662, 6.5273, 6.9349, 7.1682, 6.5461, 6.3637, 6.8696, 7.2973, 6.7568, 6.7455 |
| 1598_g_at | float64 | 0 | 0 | 163 | 8.5696, 8.163, 8.0326, 8.6194, 8.524, 8.3507, 8.0895, 8.5679, 8.5019, 8.7379 |
| 160020_at | float64 | 0 | 0 | 163 | 7.5277, 7.0123, 7.0804, 7.2539, 7.6603, 7.2417, 7.4508, 7.7807, 7.6774, 7.6801 |
| 1729_at | float64 | 0 | 0 | 163 | 7.7427, 7.9521, 7.9587, 7.7171, 7.6443, 7.5073, 7.3945, 7.2648, 7.2142, 7.5811 |
| 1773_at | float64 | 0 | 0 | 163 | 4.8113, 4.7133, 4.7104, 4.5695, 4.8599, 4.673, 4.724, 4.8216, 4.7524, 4.9039 |
| 177_at | float64 | 0 | 0 | 163 | 5.0489, 5.164, 5.1377, 4.9246, 5.1713, 4.9898, 4.8996, 5.0787, 4.8589, 5.0549 |
| 179_at | float64 | 0 | 0 | 163 | 8.5949, 8.4914, 8.6218, 8.5955, 8.8598, 8.4518, 8.4947, 8.7966, 8.8667, 8.7135 |
| 1861_at | float64 | 0 | 0 | 163 | 6.0385, 6.7965, 6.7702, 6.269, 5.8409, 6.2254, 5.2542, 5.7122, 5.5583, 5.7258 |
| 200000_s_at | float64 | 0 | 0 | 163 | 8.038, 8.5756, 8.4572, 8.1556, 8.4079, 8.2889, 8.234, 7.6629, 8.0245, 8.2036 |
| 200001_at | float64 | 0 | 0 | 163 | 9.4919, 10.1519, 10.1996, 9.2812, 10.0106, 9.9204, 9.3245, 9.0457, 9.8144, 8.98… |
| 200002_at | float64 | 0 | 0 | 163 | 10.4306, 10.2621, 10.2577, 9.5748, 8.9624, 10.38, 9.744, 9.7076, 9.6861, 9.7201 |
| 200003_s_at | float64 | 0 | 0 | 163 | 11.325, 10.6917, 10.8343, 10.6676, 10.3785, 11.0426, 10.5081, 10.8377, 10.6957,… |
| 200004_at | float64 | 0 | 0 | 163 | 9.5692, 9.7554, 9.649, 8.7307, 9.4786, 10.0513, 9.613, 8.8072, 9.141, 9.1896 |
| 200005_at | float64 | 0 | 0 | 163 | 9.4156, 9.1766, 9.3433, 9.0315, 9.0263, 9.5323, 9.1513, 8.6169, 8.8478, 9.2709 |
| 200006_at | float64 | 0 | 0 | 163 | 10.1277, 10.3497, 10.234, 9.8633, 9.8461, 10.416, 9.8358, 9.8017, 9.2831, 10.03… |
| 200007_at | float64 | 0 | 0 | 163 | 10.415, 10.5975, 10.8367, 9.9904, 10.7911, 11.1272, 9.9434, 9.7676, 10.0094, 9.… |
| 200008_s_at | float64 | 0 | 0 | 163 | 6.1587, 7.64, 8.4665, 5.7737, 7.6236, 7.7525, 7.0155, 6.1221, 7.1285, 5.9964 |
| 200009_at | float64 | 0 | 0 | 163 | 9.7031, 9.8417, 10.0944, 9.5395, 9.6486, 10.2384, 9.5293, 9.6134, 9.4008, 9.3584 |
| 200010_at | float64 | 0 | 0 | 163 | 10.8027, 10.5119, 10.6488, 10.0954, 10.0931, 11.0169, 10.2164, 10.1956, 10.4835… |
| 200011_s_at | float64 | 0 | 0 | 163 | 8.2132, 8.9151, 8.9201, 7.8901, 8.7289, 8.7327, 9.0895, 8.236, 7.9906, 8.3499 |
| 200012_x_at | float64 | 0 | 0 | 163 | 11.7916, 11.515, 11.3954, 11.4871, 10.7575, 11.7958, 11.2025, 11.767, 11.3767, … |
| 200013_at | float64 | 0 | 0 | 163 | 10.686, 10.5778, 10.7134, 10.1296, 10.0315, 11.2819, 10.0382, 10.4952, 10.5266,… |
| 200014_s_at | float64 | 0 | 0 | 163 | 8.4758, 8.8598, 8.4285, 7.4965, 8.1717, 8.6867, 8.1242, 7.8058, 7.4284, 7.8352 |
| 200015_s_at | float64 | 0 | 0 | 163 | 8.1793, 8.862, 8.8641, 7.7068, 8.3297, 8.9951, 8.2911, 7.7514, 7.9186, 7.2812 |
| 200016_x_at | float64 | 0 | 0 | 163 | 10.7352, 10.5872, 10.7203, 10.0537, 10.1909, 11.0689, 10.1507, 10.1116, 9.9669,… |
| 200017_at | float64 | 0 | 0 | 163 | 10.7699, 10.5656, 10.0708, 10.2664, 10.2694, 11.0373, 10.224, 10.7749, 10.5533,… |
| 200018_at | float64 | 0 | 0 | 161 | 11.0596, 11.2335, 11.5166, 11.463, 11.3259, 11.7763, 11.1775, 11.5161, 11.3049,… |
| 200019_s_at | float64 | 0 | 0 | 162 | 10.5149, 11.0628, 11.0191, 10.8455, 10.0736, 10.9021, 10.3572, 10.3604, 10.6408… |
| 200020_at | float64 | 0 | 0 | 163 | 8.2025, 8.3314, 8.3539, 8.1927, 7.4446, 8.018, 8.0514, 7.6515, 6.8923, 8.1789 |
| 200021_at | float64 | 0 | 0 | 162 | 11.3236, 11.5171, 11.5175, 11.6761, 11.5577, 11.7345, 11.8592, 11.5137, 12.0809… |
| 200022_at | float64 | 0 | 0 | 163 | 11.1351, 10.7826, 10.9601, 10.3118, 10.1671, 10.9771, 10.6172, 10.5857, 10.7005… |
| 200023_s_at | float64 | 0 | 0 | 163 | 9.321, 9.2492, 9.3342, 8.8361, 8.8211, 9.3287, 8.8602, 9.546, 9.1846, 9.35 |
| 200024_at | float64 | 0 | 0 | 163 | 10.9826, 10.7415, 10.7036, 10.2059, 10.0256, 11.0844, 10.2433, 10.5099, 10.4634… |
| 200025_s_at | float64 | 0 | 0 | 163 | 11.9506, 11.2202, 11.0529, 11.4379, 11.0658, 11.8869, 11.1497, 12.0178, 11.5616… |
| 200026_at | float64 | 0 | 0 | 162 | 11.3617, 11.4359, 11.4499, 10.9376, 10.721, 12.057, 11.0627, 11.8456, 11.2043, … |
| 200027_at | float64 | 0 | 0 | 163 | 9.051, 9.7746, 9.6648, 8.7983, 9.0944, 9.7621, 9.1059, 9.0403, 8.5368, 8.8242 |
| 200028_s_at | float64 | 0 | 0 | 162 | 9.1699, 9.6653, 9.8157, 9.4808, 8.9281, 9.0427, 9.0211, 9.2558, 9.211, 9.6392 |
| 200029_at | float64 | 0 | 0 | 162 | 11.5172, 11.7242, 11.7558, 11.4606, 11.1968, 11.9029, 11.4089, 11.2676, 11.6051… |
| 200030_s_at | float64 | 0 | 0 | 163 | 10.518, 10.4478, 10.6175, 9.6453, 10.0935, 10.5071, 10.4921, 9.7708, 10.4638, 9… |
| 200031_s_at | float64 | 0 | 0 | 163 | 11.8118, 11.4662, 11.4439, 11.532, 11.2614, 12.0726, 11.2635, 12.1989, 11.4421,… |

(22,165 more rows not shown)

</details>

### Target distribution

| DiagnosedCancer | count | pct |
|---|---|---|
| No | 85 | 52.15 |
| Yes | 78 | 47.85 |

### Numeric features

<details>
<summary>Show the table (22,217 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| 1007_s_at | 163 | 10.278 | 0.282725 | 9.13149 | 10.7954 |
| 1053_at | 163 | 4.38739 | 0.119028 | 4.11243 | 4.74895 |
| 117_at | 163 | 5.62663 | 0.211971 | 5.24417 | 6.27472 |
| 121_at | 163 | 8.08015 | 0.177386 | 7.58614 | 8.44209 |
| 1255_g_at | 163 | 3.68796 | 0.128341 | 3.36704 | 4.16674 |
| 1294_at | 163 | 7.43962 | 0.226687 | 6.82063 | 8.15805 |
| 1316_at | 163 | 5.09808 | 0.167917 | 4.73199 | 5.63877 |
| 1320_at | 163 | 4.22181 | 0.136694 | 3.89971 | 4.69608 |
| 1405_i_at | 163 | 5.95693 | 0.794927 | 4.43108 | 8.44508 |
| 1431_at | 163 | 3.35399 | 0.123291 | 3.0233 | 3.81646 |
| 1438_at | 163 | 6.70354 | 0.191735 | 6.28559 | 7.39865 |
| 1487_at | 163 | 7.40195 | 0.170447 | 6.94765 | 7.82346 |
| 1494_f_at | 163 | 6.78767 | 0.273074 | 6.19033 | 7.71131 |
| 1598_g_at | 163 | 8.34767 | 0.24779 | 7.66515 | 8.95029 |
| 160020_at | 163 | 7.45513 | 0.230014 | 6.89697 | 8.01011 |
| 1729_at | 163 | 7.68167 | 0.207965 | 6.82887 | 8.1082 |
| 1773_at | 163 | 4.82842 | 0.144938 | 4.47853 | 5.27567 |
| 177_at | 163 | 5.00056 | 0.137223 | 4.63744 | 5.35405 |
| 179_at | 163 | 8.62408 | 0.196627 | 8.12364 | 9.13547 |
| 1861_at | 163 | 6.12937 | 0.362762 | 5.25424 | 7.01817 |
| 200000_s_at | 163 | 8.28833 | 0.334579 | 7.34103 | 9.01148 |
| 200001_at | 163 | 9.82936 | 0.418074 | 7.98349 | 10.5851 |
| 200002_at | 163 | 9.81963 | 0.432848 | 8.41077 | 10.8817 |
| 200003_s_at | 163 | 10.7087 | 0.284844 | 9.86529 | 11.3839 |
| 200004_at | 163 | 9.62163 | 0.415455 | 7.5443 | 10.3389 |
| 200005_at | 163 | 9.16818 | 0.300151 | 8.1439 | 9.79134 |
| 200006_at | 163 | 10.0614 | 0.315802 | 8.87649 | 10.6887 |
| 200007_at | 163 | 10.3648 | 0.357503 | 8.84806 | 11.1272 |
| 200008_s_at | 163 | 7.27737 | 0.855551 | 5.75758 | 9.10185 |
| 200009_at | 163 | 9.73583 | 0.337529 | 8.27593 | 10.4026 |
| 200010_at | 163 | 10.3749 | 0.372816 | 9.34353 | 11.1853 |
| 200011_s_at | 163 | 8.75981 | 0.335591 | 7.83338 | 9.53933 |
| 200012_x_at | 163 | 11.3402 | 0.316192 | 10.4215 | 12.025 |
| 200013_at | 163 | 10.3899 | 0.365249 | 9.42068 | 11.2819 |
| 200014_s_at | 163 | 8.20013 | 0.417285 | 6.67825 | 9.19647 |
| 200015_s_at | 163 | 8.3178 | 0.509018 | 6.54724 | 9.31131 |
| 200016_x_at | 163 | 10.3437 | 0.316175 | 9.05839 | 11.0689 |
| 200017_at | 163 | 10.4459 | 0.283894 | 9.51197 | 11.1489 |
| 200018_at | 163 | 11.314 | 0.281122 | 10.5761 | 11.8776 |
| 200019_s_at | 163 | 10.6654 | 0.312626 | 9.60368 | 11.3268 |
| 200020_at | 163 | 8.06615 | 0.367901 | 6.89228 | 8.80659 |
| 200021_at | 163 | 11.6981 | 0.247882 | 10.9577 | 12.4347 |
| 200022_at | 163 | 10.6914 | 0.308193 | 9.80517 | 11.3698 |
| 200023_s_at | 163 | 9.09545 | 0.340628 | 7.90313 | 9.74303 |
| 200024_at | 163 | 10.5387 | 0.381889 | 9.51322 | 11.2939 |
| 200025_s_at | 163 | 11.3703 | 0.326053 | 10.4039 | 12.0903 |
| 200026_at | 163 | 11.2421 | 0.290334 | 10.2448 | 12.057 |
| 200027_at | 163 | 9.28942 | 0.375663 | 8.16571 | 9.99088 |
| 200028_s_at | 163 | 9.36296 | 0.305684 | 8.20522 | 9.92116 |
| 200029_at | 163 | 11.5259 | 0.255512 | 10.5236 | 12.127 |
| 200030_s_at | 163 | 10.3133 | 0.355901 | 9.03667 | 11.046 |
| 200031_s_at | 163 | 11.4922 | 0.290129 | 10.5957 | 12.272 |
| 200032_s_at | 163 | 11.1834 | 0.301625 | 10.3086 | 11.8223 |
| 200033_at | 163 | 9.71782 | 0.548788 | 6.55831 | 10.6018 |
| 200034_s_at | 163 | 9.99013 | 0.451556 | 8.3369 | 10.9073 |
| 200035_at | 163 | 8.02789 | 0.224513 | 7.27665 | 8.59534 |
| 200036_s_at | 163 | 10.2023 | 0.452228 | 9.09409 | 11.2394 |
| 200037_s_at | 163 | 7.7327 | 0.406029 | 5.40219 | 8.59236 |
| 200038_s_at | 163 | 10.741 | 0.32787 | 9.56897 | 11.4352 |
| 200039_s_at | 163 | 8.63298 | 0.296012 | 7.66959 | 9.46423 |

(22,157 more rows not shown)

</details>

### Categorical features

<details>
<summary>Show the table (19 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| DiagnosedCancer | 1 | No | 85 | 52.15 |
| DiagnosedCancer | 2 | Yes | 78 | 47.85 |
| haemoptysis | 1 | no | 148 | 90.8 |
| haemoptysis | 2 | yes | 15 | 9.2 |
| lymphadenopathy | 1 | no | 120 | 73.62 |
| lymphadenopathy | 2 | yes | 43 | 26.38 |
| mass_over_3cm | 1 | no | 115 | 70.55 |
| mass_over_3cm | 2 | yes | 48 | 29.45 |
| race | 1 | Caucasian | 110 | 67.48 |
| race | 2 | other | 53 | 32.52 |
| scan_period | 1 | period_1 | 28 | 17.18 |
| scan_period | 2 | period_2 | 27 | 16.56 |
| scan_period | 3 | period_3 | 27 | 16.56 |
| scan_period | 4 | period_4 | 27 | 16.56 |
| scan_period | 5 | period_5 | 27 | 16.56 |
| sex | 1 | male | 122 | 74.85 |
| sex | 2 | female | 41 | 25.15 |
| smoking_status | 1 | quit less than 10 years | 130 | 79.75 |
| smoking_status | 2 | quit for 10 years or greater | 33 | 20.25 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a111fa-e441-7be0-b4cb-2b1c80c2c167 |
| checksum | v2:9108c0046efd8a3e052dd8570cc2bbe16449de9df488bfeb5f5d205f03e38493 |
| built_at | 2026-10-06T16:10:55+00:00 |
| path | lung_cancer_epithelial_genexp/01a111fa-e441-7be0-b4cb-2b1c80c2c167 |
| data_foundry_version | 0.0.5 |
| git_sha | 8fbc4745ab8de19d5bc0c98a89b008f5d779909f-dirty |
| libraries | {'python': '3.11.14', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
| stale | yes: the definition now gives checksum `v2:d75740bb668e5543526eed1025c298525d053a428d6fe57c950e585cc47682c0` |
