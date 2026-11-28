---
report_format: data-foundry-report-v2
unique_name: cooking_time_1m
container_format: 2
checksum: v2:b77b0506fcb7f4191e23b99f05b654254f0527f961e51b57762e8129a0e7ac3a
build:
  uuid: 01a217f6-0aa0-71e6-8604-d6bdd00e741c
  checksum: v2:b77b0506fcb7f4191e23b99f05b654254f0527f961e51b57762e8129a0e7ac3a
  built_at: '2026-11-26T13:09:22+00:00'
  path: cooking_time_1m/01a217f6-0aa0-71e6-8604-d6bdd00e741c
  data_foundry_version: 0.0.5
  git_sha: e3ddd55462cc45eed6aa71c38abd183086888b36
  libraries:
    python: 3.12.3
    pandas: 2.3.3
    numpy: 2.1.3
    pyarrow: 20.0.0
    scikit-learn: 1.7.2
    polars: 1.41.1
build_stale: false
data:
  n_rows: 11356304
  n_features: 196
  dtypes:
    category: 9
    datetime64[ns]: 1
    float32: 187
  n_test_dataset_rows: null
task:
  target: cooking_time_minutes
  problem_type: regression
  metric: rmse
  metric_origin: source
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: timestamp
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 3
  n_folds: 1
  random_state: 4267
  time_horizon: 7
  time_horizon_unit: days
  time_gap: 1
  time_gap_unit: days
  reason: 'Each test window is one week, TabReD''s own validation and test length:
    TabReD trains on 15 November to 20 December 2023, validates on 21-27 December
    and tests on 28 December to 3 January. TabReD states no refit cadence. A week
    holds every weekday once, and cooking times follow a weekly cycle: Friday and
    Saturday orders cook about 12% longer than Monday to Thursday orders (mean log
    minutes 2.57 to 2.64 against 2.46 to 2.51), more than the shift between the weekly
    windows. The test windows are the newest week and every other week before it (CC
    2026-11-11, as for delivery_eta_1m; it supersedes the three newest weeks of 2026-11-10),
    newest first: 28 December to 3 January, TabReD''s test week, over New Year; 14-20
    December, in the run-up to the holidays; and 4-10 December, a week before the
    run-up. 21-27 December, TabReD''s validation week, is not tested. 4-10 December
    trains on less than half the orders (37.5%), beside 84.8% and 54.2%. The orders
    run from 15 November 2023 to 3 January 2024, so only the weeks from 11 December
    keep half the orders for training (51.9% for a start on 11 December). 4-10 December
    is the last full week before 11-12 December, which hold no orders, and every day
    of it holds 208,774 to 326,051 orders; two weeks before 14 December, 30 November
    to 6 December, would train on 28.9%, under 30%. Cooking times rise toward New
    Year (mean log minutes 2.533, 2.548 and 2.599 in the oldest, middle and newest
    window, against 2.527 to 2.532 in the weeks from 16 November to 6 December), so
    the score covers a week before the run-up, the run-up and the holiday itself,
    but not a week after the holidays (the data end on 3 January). The gap of one
    day is part of the task: a cooking time is known only when the order is cooked
    (up to 2 hours after it is placed), so at a refit the last orders before it have
    no label yet; without the gap 172, 108 and 155 train orders per window (start
    + cooking time) would end after the window start, with it none. The gap removes
    280k, 239k and 278k of the 11.1M, 7.2M and 5.1M earlier orders (2.5 to 5.5%).'
  n_train:
    min: 4797156
    max: 10856304
  n_test:
    min: 500000
    max: 500000
  row_budget:
    train: 1000000
    test: 500000
  train_sampling:
    default: newest_year
    unit: rows
    stratify_on: null
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicates_skipped
  accepted:
    splits_train_under_half: 'Signed off (Lennart, 2026-11-11): 4-10 December trains
      on 37.5% of the orders, beside 28 December-3 January and 14-20 December on 84.8%
      and 54.2%; kept as the curator''s exception to SPLIT-14''s half-data floor (Andrej,
      2026-11-19).'
decisions: []
---

# cooking_time_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `cooking_time_minutes`, scored with `rmse` on temporal splits by `timestamp`. 11,356,304 rows and 196 features. Source: Kaggle (2024).

Built as `01a217f6-0aa0-71e6-8604-d6bdd00e741c` on 2026-11-26. See [Build](#build).

## In brief

**Question.** How long will a restaurant take to cook an order placed through a food delivery app?

**Use case.** When an order is placed, the delivery service estimates the restaurant's cooking time, for example to time the courier and the delivery estimate shown to the customer.

**One row.** One order placed through a food delivery app between 15 November 2023 and 3 January 2024 (TabReD release; the service is not named).

**Predicted.** The time the restaurant took to cook the order, in minutes on a logarithmic scale; orders under one minute are left out.

**Known at prediction time.** 196 anonymised features built from the order's contents and the restaurant's past cooking times (TabReD), including the time of the order.

**What the test data stands for.** Each test window is a week, TabReD's own validation and test length: the newest (28 December 2023 to 3 January 2024) and every other week before it (14-20 December and 4-10 December), up to 500,000 orders each. Training is every order placed at least a day before the window, of which a benchmark fits on a random million.

> **Use case fit: direct (the rows, features and split mirror the use case).** Order contents and past cooking times are known when an order is placed. The features are anonymised, so their timing cannot be checked.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/cooking_time.md`](../../../../curation/records/cooking_time.md)
- The original source: <https://www.kaggle.com/datasets/pcovkrd84mejm/cooking-time>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/cooking_time/`. To get them:

```text
We get the TabRed data from Kaggle.

kaggle datasets download -d pcovkrd84mejm/cooking-time -f cooking_time.parquet && unzip cooking_time.parquet.zip && rm cooking_time.parquet.zip
mkdir -p local-data-warehouse/cooking_time && mv cooking_time.parquet local-data-warehouse/cooking_time/
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/cooking_time_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/cooking_time_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/datasets/pcovkrd84mejm/cooking-time |
| year | 2024 |
| domain | industry & manufacturing |
| license | CC-BY-NC-SA-4.0 |
| data_tags | Non-IID, Temporal, Anonymized |
| reference | rubachev2025tabred |
| rows x columns | 11,356,304 x 197 |
| task.target | cooking_time_minutes |
| task.problem_type | regression |
| task.metric | rmse |
| task.split_regime | temporal_non_iid |
| task.time_on | timestamp |

**Metric**

| field | value |
|---|---|
| name | `rmse` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | RMSE (TabReD regression tasks) |
| reference | Rubachev et al., TabReD, ICLR 2025 (https://arxiv.org/abs/2406.19380), Sec. 4 / App.: RMSE for regression, ROC AUC for classification |
| definition | sqrt(mean((y - yhat)^2)) on the natural-log minutes target |

<details>
<summary>Feature types: 9 categorical, 0 string, 1 datetime</summary>

- categorical (9): `bin_0`, `bin_1`, `bin_2`, `cat_0`, `cat_1`, `cat_2`, `cat_3`, `cat_4`, `cat_5`
- string (0): none
- datetime (1): `timestamp`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{rubachev2025tabred,
  title={TabReD: Analyzing Pitfalls and Filling the Gaps in Tabular Deep Learning Benchmarks},
  author={Rubachev, Ivan and Kartashev, Nikolay and Gorishniy, Yury and Babenko, Artem},
  booktitle={The Thirteenth International Conference on Learning Representations},
  year={2025},
}
```

</details>

## Sample rows

The first 5 of 11,356,304 rows of the final frame (the oldest rows: the frame is sorted by `timestamp`); 12 of 197 columns, the target first. Cells are cut at 40 characters.

| cooking_time_minutes | num_0 | num_1 | num_2 | num_3 | num_4 | num_5 | num_6 | num_7 | num_8 | num_9 | num_10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.45244 | -0.681594 | -3.10233 | 0.444534 | 0.511699 | 0.381675 | -1.04444 | -1.68445 | -1.6642 | -0.00376371 | 1.48053 | 0.413874 |
| 3.14271 | 0.573115 | -3.10233 | 0.913155 | -0.492944 | 0.422712 | -0.87491 | -1.3124 | -1.30316 | -0.0899957 | 1.29196 | 0.38934 |
| 3.42643 | 0.573115 | -3.10233 | 1.35513 | -0.984601 | -1.65409 | -1.63153 | -0.897525 | 0.0464333 | 0.560024 | -1.04171 | -1.55828 |
| 1.81374 | 0.573115 | -3.10233 | 0.489308 | 0.103938 | -0.188562 | -0.0766036 | -0.229802 | -0.446735 | -1.74044 | 0.363174 | -0.20069 |
| 1.95066 | -0.681594 | -3.10233 | -0.823171 | 1.78021 | -0.199602 | -0.19311 | -0.37913 | -0.623922 | -1.27457 | 0.426511 | -0.211743 |

## Curation notes

We start with data from TabRed, which already comes preprocessed.

- Potential leak, kept on purpose: TabReD releases the 186 numeric features only after a quantile transform to a normal distribution (all within ±5.1993, the clip of scikit-learn's QuantileTransformer; 155 reach it); which rows it was fit on is not documented, and the raw features are not published. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if the TabReD authors say the fit used all rows.
- We drop orders with a cooking time under one minute (168 of 12.8M, 26 of them zero or negative), as TabReD's preprocessing does.
- The target is the natural log of the minutes, as in TabReD (the column keeps its name). TabReD's reason: the times are right-skewed, and squared error on the log is close to absolute error on the minutes, the error that matters for the task.
- The row budget: Each test window keeps at most 500k of its rows, drawn at random within the window (v2 split protocol), and each train side holds every earlier order outside the one-day gap; the container keeps every row a split uses. The container records the 1M train budget, and a benchmark sub-samples each train side to 1M rows before a fit (`subsample_train`; by default a random 1M of the newest year before the window). The orders start on 15 November 2023, so the newest year is all of the history and the default is a random 1M of all earlier orders, as in TabReD: a random sample keeps data from all periods of the history.

## Splits

Expanding-window temporal splits: 3 test window(s) of 7 days, starting at 2023-12-28, 2023-12-14, 2023-12-04, newest first; train is all earlier data up to a gap of 1 days. The test windows by `timestamp`, as listed: 2023-12-28 to 2024-01-03 (500,000 test, 10,856,304 train rows); 2023-12-14 to 2023-12-20 (500,000 test, 6,935,762 train rows); 2023-12-04 to 2023-12-10 (500,000 test, 4,797,156 train rows). Each test window keeps at most 500k of its rows, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows (by default rows drawn at random from the newest year before each window, extended back in time until it holds that many rows, `subsample_train`).

Each test window is one week, TabReD's own validation and test length: TabReD trains on 15 November to 20 December 2023, validates on 21-27 December and tests on 28 December to 3 January. TabReD states no refit cadence. A week holds every weekday once, and cooking times follow a weekly cycle: Friday and Saturday orders cook about 12% longer than Monday to Thursday orders (mean log minutes 2.57 to 2.64 against 2.46 to 2.51), more than the shift between the weekly windows. The test windows are the newest week and every other week before it (CC 2026-11-11, as for delivery_eta_1m; it supersedes the three newest weeks of 2026-11-10), newest first: 28 December to 3 January, TabReD's test week, over New Year; 14-20 December, in the run-up to the holidays; and 4-10 December, a week before the run-up. 21-27 December, TabReD's validation week, is not tested. 4-10 December trains on less than half the orders (37.5%), beside 84.8% and 54.2%. The orders run from 15 November 2023 to 3 January 2024, so only the weeks from 11 December keep half the orders for training (51.9% for a start on 11 December). 4-10 December is the last full week before 11-12 December, which hold no orders, and every day of it holds 208,774 to 326,051 orders; two weeks before 14 December, 30 November to 6 December, would train on 28.9%, under 30%. Cooking times rise toward New Year (mean log minutes 2.533, 2.548 and 2.599 in the oldest, middle and newest window, against 2.527 to 2.532 in the weeks from 16 November to 6 December), so the score covers a week before the run-up, the run-up and the holiday itself, but not a week after the holidays (the data end on 3 January). The gap of one day is part of the task: a cooking time is known only when the order is cooked (up to 2 hours after it is placed), so at a refit the last orders before it have no label yet; without the gap 172, 108 and 155 train orders per window (start + cooking time) would end after the window start, with it none. The gap removes 280k, 239k and 278k of the 11.1M, 7.2M and 5.1M earlier orders (2.5 to 5.5%).

3 repeat(s) x 1 fold(s) with seed 4267; train 4,797,156 to 10,856,304 rows, test 500,000 rows. Prediction horizon: 7 days. Gap between train and test: 1 days. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as rows.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 10856304 | 500000 | 2023-11-15 00:00:01 | 2023-12-26 23:59:46 | 2023-12-28 00:00:02 | 2024-01-03 21:47:53 |
| 1 | 0 | 6935762 | 500000 | 2023-11-15 00:00:01 | 2023-12-10 21:55:40 | 2023-12-14 00:00:24 | 2023-12-20 23:59:44 |
| 2 | 0 | 4797156 | 500000 | 2023-11-15 00:00:01 | 2023-12-02 23:59:56 | 2023-12-04 00:01:01 | 2023-12-10 21:54:12 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows cooking_time_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Dec 2023 - Jan 2024 | 500000 | 0.956 | mean 2.591, median 2.615, p10 1.649, p90 3.453 | mean 2.538, median 2.555, p10 1.623, p90 3.401 | 0.221 | num_29 (0.22), num_30 (0.22), num_28 (0.18) | 0.0053 |
| 1 | Dec 2023 | 500000 | 0.611 | mean 2.549, median 2.578, p10 1.613, p90 3.398 | mean 2.542, median 2.566, p10 1.626, p90 3.379 | 0.147 | num_3 (0.15), cat_5 (0.11), num_28 (0.02) | 0.0054 |
| 2 | Dec 2023 | 500000 | 0.422 | mean 2.523, median 2.552, p10 1.613, p90 3.373 | mean 2.532, median 2.557, p10 1.619, p90 3.369 | 0.156 | cat_5 (0.16), num_3 (0.08), num_29 (0.03) | 0.0063 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicates_skipped`: Skipped duplicate-column/row checks: 2,237,191,888 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to run them; nothing else checks duplicate rows and columns.)

Accepted on purpose:

- `splits_train_under_half`: Signed off (Lennart, 2026-11-11): 4-10 December trains on 37.5% of the orders, beside 28 December-3 January and 14-20 December on 84.8% and 54.2%; kept as the curator's exception to SPLIT-14's half-data floor (Andrej, 2026-11-19).

## Data checks

### Feature summary

<details>
<summary>Show the table (197 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| bin_0 | category | 0 | 0 | 2 | 0.0, 1.0 |
| bin_1 | category | 0 | 0 | 2 | 1.0, 0.0 |
| bin_2 | category | 0 | 0 | 2 | 1.0, 0.0 |
| cat_0 | category | 0 | 0 | 57548 | 251, 889, 94, 1327, 1544, 985, 31, 753, 171, 2130 |
| cat_1 | category | 0 | 0 | 21370 | 1, 7, 2, 34, 6, 8, 82, 50, 14, 22 |
| cat_2 | category | 0 | 0 | 10726 | 120, 172, 381, 361, 196, 758, 641, 170, 478, 1091 |
| cat_3 | category | 0 | 0 | 53623 | 827, 121, 916, 86, 1085, 706, 244, 577, 288, 2077 |
| cat_4 | category | 0 | 0 | 3 | 1, 2, 3 |
| cat_5 | category | 0 | 0 | 123693 | 2, 27, 568, 293, 218, 563, 517, 598, 29, 1026 |
| timestamp | datetime64\[ns\] | 0 | 0 | 2.72416e+06 | 2023-11-22 16:01:37, 2023-12-24 13:16:13, 2023-12-01 12:34:33, 2023-12-16 10:51… |
| num_165 | float32 | 1.12431e+07 | 99 | 67 | -0.8644, -1.1794, -0.4143, -0.6425, -0.2796, -1.5347, -0.525, -0.1702, -0.0013,… |
| num_166 | float32 | 1.12431e+07 | 99 | 103699 | 5.1993, -1.724, -0.5588, 0.1312, -1.7726, -0.9817, -1.4526, -0.3541, -2.2167, -… |
| num_167 | float32 | 1.12431e+07 | 99 | 103628 | -1.7482, -0.3166, -0.5869, -1.4736, -1.5792, -0.6065, -2.2313, -1.3712, -1.7478… |
| num_168 | float32 | 1.12431e+07 | 99 | 89164 | -1.7051, 0.2023, -1.7074, -0.3548, -0.5016, 0.2835, 0.1704, -0.6656, -1.2643, -… |
| num_169 | float32 | 1.12431e+07 | 99 | 95682 | -1.9367, -1.852, -1.2333, -1.7537, -1.8038, -1.616, -1.8442, -1.4821, -1.5459, … |
| num_155 | float32 | 5.28048e+06 | 46.5 | 68 | -0.9775, -0.16, 0.2835, 0.5969, 0.8373, 1.0315, 1.1998, 1.3485, 1.4828, 1.6022 |
| num_156 | float32 | 5.28048e+06 | 46.5 | 4.69559e+06 | -1.5437, -1.5439, -1.5441, -1.0793, -0.2959, -1.1999, -0.2959, -1.1078, -1.3025… |
| num_157 | float32 | 5.28048e+06 | 46.5 | 4.34657e+06 | -1.3015, -1.3019, -1.3022, -0.3498, 2.4548, -0.6414, 2.4536, -1.8601, -0.8657, … |
| num_158 | float32 | 5.28048e+06 | 46.5 | 4.44347e+06 | -1.5047, -0.3111, -1.3708, -1.5069, -1.5087, -2.0783, -0.3115, -1.5109, -1.5098… |
| num_159 | float32 | 5.28048e+06 | 46.5 | 3.6155e+06 | 1.5664, 1.5646, 1.0288, 0.9033, 0.4805, 1.5722, 1.9583, -1.4738, 0.9103, -1.4735 |
| num_145 | float32 | 3.14411e+06 | 27.69 | 8595 | -0.4418, -0.7233, 0.0276, -0.1931, -1.0619, 0.4252, 0.2368, -0.8883, -1.4865, -… |
| num_146 | float32 | 3.14411e+06 | 27.69 | 2066 | -0.3335, 0.0201, 0.3058, 0.5307, -0.8022, 0.7547, 1.0422, -1.218, -0.1575, 0.17… |
| num_147 | float32 | 3.14411e+06 | 27.69 | 36456 | 0.2407, 0.5394, 0.7902, -0.1321, -0.5999, 0.9836, 1.1449, -0.0452, 0.3696, 1.38… |
| num_148 | float32 | 3.14411e+06 | 27.69 | 1939 | -0.8571, 0.141, -0.2575, -2.0744, 0.6456, 0.4197, 0.8481, -0.5555, -0.1562, -0.… |
| num_139 | float32 | 3.07383e+06 | 27.07 | 9447 | -0.5687, -0.8409, 0.2757, -0.1132, -0.3282, 0.0905, -1.1694, -1.0021, -1.58, 0.… |
| num_140 | float32 | 3.07383e+06 | 27.07 | 2070 | 0.6364, -0.4626, 0.1587, -0.1132, 0.3696, -0.9185, 0.9877, 1.6395, -1.325, -0.2… |
| num_141 | float32 | 3.07383e+06 | 27.07 | 41142 | 0.1676, 0.4794, 0.7397, -0.2252, 1.1211, 0.9456, -0.7088, -0.1359, 0.3032, 1.37… |
| num_142 | float32 | 3.07383e+06 | 27.07 | 1932 | -0.8571, 0.1346, -0.2627, -2.0854, 0.6425, 0.4156, 0.8553, -0.5584, -0.1626, -0… |
| num_160 | float32 | 2.95504e+06 | 26.02 | 175 | -0.3084, -0.3817, -0.2381, -0.4556, -0.1689, -0.098, -0.0301, 0.0376, -0.612, -… |
| num_161 | float32 | 2.95504e+06 | 26.02 | 6.62514e+06 | 3.0902, 3.0909, 3.0903, 3.0909, 3.092, 3.09, 3.09, 3.0925, 3.0906, 3.0906 |
| num_162 | float32 | 2.95504e+06 | 26.02 | 5.08305e+06 | 3.09, 3.09, 3.09, 3.09, 3.09, 3.0899, 3.0901, 3.0901, 3.09, 3.0902 |
| num_163 | float32 | 2.95504e+06 | 26.02 | 5.92633e+06 | -1.6557, 3.09, 3.0901, 3.09, 3.09, 3.0901, 3.09, -1.6579, -1.5226, 3.09 |
| num_164 | float32 | 2.95504e+06 | 26.02 | 5.28894e+06 | 3.09, 3.09, 3.0902, 3.09, 3.0901, 3.09, 3.0902, 3.09, 3.0904, 3.0901 |
| num_150 | float32 | 2.9195e+06 | 25.71 | 249 | -1.1794, -1.0188, -1.0956, -0.9476, -0.8809, -0.8197, -1.2734, -0.7597, -0.6487… |
| num_151 | float32 | 2.9195e+06 | 25.71 | 6.67717e+06 | 3.0928, 3.0901, 3.0904, 3.0902, 3.0901, 3.094, 3.0925, 3.0905, 3.0903, 3.0907 |
| num_152 | float32 | 2.9195e+06 | 25.71 | 5.26932e+06 | 3.09, 3.09, 3.0899, 3.09, 3.09, 3.09, 3.09, 3.0901, 3.0901, 3.0901 |
| num_153 | float32 | 2.9195e+06 | 25.71 | 5.93813e+06 | -1.652, 3.09, 3.09, 3.09, 3.0902, -1.6539, -1.5193, -1.6555, 3.09, 3.0901 |
| num_154 | float32 | 2.9195e+06 | 25.71 | 5.28677e+06 | 3.0904, 3.09, 3.09, 3.09, 3.0901, 3.09, 3.0903, 3.0902, 3.0903, 3.0904 |
| num_170 | float32 | 2.9195e+06 | 25.71 | 5 | 0.0766, -2.39, -1.6113, -1.7688, -1.9769 |
| num_171 | float32 | 2.9195e+06 | 25.71 | 6.04963e+06 | 3.09, 3.09, 3.09, 3.09, 3.09, 3.09, 3.0901, 3.0899, 3.0901, 3.0901 |
| num_172 | float32 | 2.9195e+06 | 25.71 | 5.99764e+06 | 3.09, 3.09, 3.09, 3.09, 3.09, 3.0901, 3.0902, 3.09, 3.0901, 3.0901 |
| num_173 | float32 | 2.9195e+06 | 25.71 | 5.93789e+06 | -1.6505, 3.09, 3.09, 3.0901, -1.5165, -1.6528, 3.09, -1.6545, 3.09, -2.2018 |
| num_174 | float32 | 2.9195e+06 | 25.71 | 5.82917e+06 | -3.0482, -3.0476, -3.0489, -2.6533, -2.9085, -1.6767, -3.0473, -1.994, -3.0463,… |
| num_175 | float32 | 2.9195e+06 | 25.71 | 3 | 0.0402, -2.39, -1.9792 |
| num_176 | float32 | 2.9195e+06 | 25.71 | 6.03914e+06 | 3.09, 3.09, 3.09, 3.09, 3.09, 3.0901, 3.09, 3.0901, 3.0899, 3.0901 |
| num_177 | float32 | 2.9195e+06 | 25.71 | 6.00816e+06 | 3.09, 3.09, 3.09, 3.09, 3.09, 3.0901, 3.0902, 3.0901, 3.0901, 3.0902 |
| num_178 | float32 | 2.9195e+06 | 25.71 | 5.9396e+06 | -1.6541, -1.6562, -1.5224, -1.658, -2.2098, -0.235, -1.6601, -1.659, -0.2355, -… |
| num_179 | float32 | 2.9195e+06 | 25.71 | 5.81137e+06 | -2.7343, 3.09, 3.09, 3.09, 3.09, -2.7348, 3.09, -2.7322, -2.7393, 3.09 |
| num_180 | float32 | 2.9195e+06 | 25.71 | 5.93781e+06 | -1.6512, 3.09, 3.09, -1.5183, -1.6532, 3.0901, 3.0901, -1.6548, -2.2091, -0.232 |
| num_181 | float32 | 2.9195e+06 | 25.71 | 5.93682e+06 | -1.6502, -1.6524, -1.5151, -1.6542, -2.2045, -0.2327, -1.656, -1.6551, -0.9761,… |
| num_182 | float32 | 2.9195e+06 | 25.71 | 5.9417e+06 | -1.652, -1.6541, -1.5198, -1.6558, -0.2343, -2.2129, -1.6579, -1.6568, -0.2348,… |
| num_183 | float32 | 2.9195e+06 | 25.71 | 5.93741e+06 | -1.6478, 3.09, 3.09, 3.09, 3.09, 3.09, -1.5138, -1.6504, -1.6524, 3.0901 |
| num_131 | float32 | 935 | 0.01 | 34 | -0.585, -0.0025, -1.3956, 0.4738, 0.879, 1.2367, 1.5543, 1.838, 2.0965, 2.326 |
| num_132 | float32 | 935 | 0.01 | 111 | -0.7547, -0.2098, 0.2098, -1.5418, 0.5511, 0.8373, 1.0842, 1.3041, 1.498, 1.6742 |
| num_133 | float32 | 935 | 0.01 | 56030 | -0.0603, -0.2979, -0.6784, 0.9714, 0.0151, -0.1359, 0.141, -0.5178, -0.4047, 1.… |
| num_134 | float32 | 935 | 0.01 | 13879 | -0.6456, -0.7799, -0.2614, 0.0025, 0.3295, -0.0515, -0.4529, 0.6943, 0.3084, 0.… |
| num_135 | float32 | 935 | 0.01 | 122055 | 0.188, 0.3295, -0.174, 0.5021, -0.0226, 1.1329, -0.0728, 0.0691, 1.5019, 0.0226 |
| num_136 | float32 | 935 | 0.01 | 9964 | -1.4828, -1.2154, -0.0615, -0.2188, -1.1047, -0.606, -0.909, -0.8302, -0.763, -… |
| num_137 | float32 | 935 | 0.01 | 1.77532e+06 | -1.3525, -0.4034, -0.8391, -0.797, -0.6943, -0.748, -0.6395, -0.8837, 0.1804, -… |
| num_138 | float32 | 935 | 0.01 | 99 | -0.8571, -0.054, 0.3575, 0.7233, 1.0422, 1.316, 1.5501, 1.7541, 1.9345, 2.0948 |

(137 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | -0.094 | -0.77 | 0.436 | 0.081 | log | 4.38951e+06 | 2.48454e+17 | exponential |

### Numeric features

<details>
<summary>Show the table (187 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| num_0 | 1.13563e+06 | 0.0303976 | 0.767728 | -0.681594 | 1.85875 |
| num_1 | 1.13563e+06 | 0.00250591 | 0.98981 | -3.10233 | 3.03537 |
| num_2 | 1.13563e+06 | -0.00289956 | 0.999397 | -5.19934 | 5.19934 |
| num_3 | 1.13563e+06 | -0.0671039 | 0.99515 | -5.19934 | 2.16969 |
| num_4 | 1.13563e+06 | 8.70671e-05 | 0.995379 | -5.05911 | 3.31144 |
| num_5 | 1.13563e+06 | 0.000363561 | 0.99715 | -5.01834 | 5.19934 |
| num_6 | 1.13563e+06 | -0.00306878 | 0.998557 | -5.19934 | 4.99249 |
| num_7 | 1.13563e+06 | -0.00123984 | 0.998522 | -5.19934 | 4.95717 |
| num_8 | 1.13563e+06 | -0.00454839 | 0.999919 | -5.19934 | 5.19934 |
| num_9 | 1.13563e+06 | 0.00127148 | 0.995396 | -5.19934 | 4.36426 |
| num_10 | 1.13563e+06 | -0.00201234 | 0.994601 | -5.19934 | 5.19934 |
| num_11 | 1.13563e+06 | -0.000886584 | 0.997029 | -5.19934 | 4.03349 |
| num_12 | 1.13563e+06 | -0.00101652 | 0.994681 | -3.25066 | 5.19934 |
| num_13 | 1.13563e+06 | -0.00123883 | 0.998129 | -3.91358 | 3.54721 |
| num_14 | 1.13563e+06 | -0.00387788 | 0.998997 | -4.64369 | 5.19934 |
| num_15 | 1.13563e+06 | -0.00235041 | 1.00356 | -5.19934 | 5.19934 |
| num_16 | 1.13563e+06 | -0.00134925 | 1.00126 | -5.19934 | 5.19934 |
| num_17 | 1.13563e+06 | 0.000832546 | 0.998489 | -5.19934 | 5.19934 |
| num_18 | 1.13563e+06 | -0.000434756 | 0.99954 | -5.19934 | 4.58546 |
| num_19 | 1.13563e+06 | -0.000776263 | 1.00021 | -5.19934 | 5.19934 |
| num_20 | 1.13563e+06 | 0.00167773 | 1.00122 | -5.19934 | 5.03541 |
| num_21 | 1.13563e+06 | 0.00280797 | 0.997106 | -5.19934 | 5.19934 |
| num_22 | 1.13563e+06 | 0.00105843 | 0.999265 | -4.79822 | 4.64161 |
| num_23 | 1.13563e+06 | 0.002044 | 1.0008 | -5.19934 | 5.19934 |
| num_24 | 1.13563e+06 | -0.00301153 | 1.00099 | -5.19934 | 4.68927 |
| num_25 | 1.13563e+06 | 0.000820607 | 0.997593 | -5.19934 | 4.776 |
| num_26 | 1.13563e+06 | -0.0378174 | 0.975542 | -5.19934 | 4.73919 |
| num_27 | 1.13563e+06 | 0.0412401 | 1.00738 | -5.19934 | 5.19934 |
| num_28 | 1.13563e+06 | -0.00578988 | 1.01094 | -4.9645 | 5.19934 |
| num_29 | 1.13563e+06 | -0.000820665 | 1.00957 | -5.19934 | 4.83803 |
| num_30 | 1.13563e+06 | -0.0171763 | 1.00351 | -5.19934 | 5.19934 |
| num_31 | 1.13563e+06 | -0.0076476 | 0.99818 | -2.2085 | 5.19934 |
| num_32 | 1.13563e+06 | -0.00862057 | 0.999535 | -2.20076 | 5.19934 |
| num_33 | 1.13563e+06 | -0.00796315 | 0.998424 | -5.19934 | 5.19934 |
| num_34 | 1.13563e+06 | -0.00867282 | 0.997971 | -5.19934 | 5.19934 |
| num_35 | 1.13563e+06 | -0.0102287 | 0.998068 | -2.20698 | 5.19934 |
| num_36 | 1.13563e+06 | -0.00760907 | 0.998885 | -2.21064 | 5.19934 |
| num_37 | 1.13563e+06 | -0.0347679 | 0.934174 | -2.15665 | 1.19977 |
| num_38 | 1.13563e+06 | -0.0108085 | 0.99845 | -2.20788 | 5.19934 |
| num_39 | 1.13563e+06 | -0.00867797 | 0.997035 | -2.20983 | 5.19934 |
| num_40 | 1.13561e+06 | -0.00871482 | 0.999488 | -5.19934 | 4.04336 |
| num_41 | 1.13563e+06 | -0.0104577 | 0.9982 | -2.21184 | 5.19934 |
| num_42 | 1.13563e+06 | -0.0101166 | 0.997065 | -2.20511 | 5.19934 |
| num_43 | 1.13563e+06 | -0.0100138 | 0.99792 | -2.21241 | 5.19934 |
| num_44 | 1.13563e+06 | -0.0694527 | 0.832266 | -2.20402 | 0.601439 |
| num_45 | 1.13563e+06 | -0.0107772 | 0.997717 | -2.20847 | 5.19934 |
| num_46 | 1.13563e+06 | -0.00886837 | 0.999772 | -2.2117 | 4.05587 |
| num_47 | 1.13563e+06 | -0.00894145 | 0.998111 | -5.19934 | 5.19934 |
| num_48 | 1.13563e+06 | -0.0111757 | 0.998547 | -5.19934 | 5.19934 |
| num_49 | 1.13563e+06 | -0.0116677 | 0.998945 | -2.21123 | 5.19934 |
| num_50 | 1.13563e+06 | -0.00985241 | 0.997256 | -2.21003 | 5.19934 |
| num_51 | 1.13563e+06 | -0.0154062 | 0.964929 | -2.07868 | 1.58435 |
| num_52 | 1.13563e+06 | -0.00953082 | 0.998715 | -2.21006 | 5.19934 |
| num_53 | 1.13563e+06 | -0.00793779 | 0.999371 | -2.2125 | 5.19934 |
| num_54 | 1.13562e+06 | -0.0114165 | 0.999428 | -5.19934 | 5.19934 |
| num_55 | 1.13563e+06 | -0.00889336 | 0.998783 | -5.19934 | 5.19934 |
| num_56 | 1.13563e+06 | -0.0101772 | 0.998297 | -5.19934 | 5.19934 |
| num_57 | 1.13563e+06 | -0.0100595 | 0.997934 | -2.20947 | 5.19934 |
| num_58 | 1.13563e+06 | 0.00648205 | 0.962906 | -1.48962 | 5.19934 |
| num_59 | 1.13563e+06 | -0.0107337 | 0.997415 | -2.20822 | 5.19934 |

(127 more rows not shown)

</details>

### Categorical features

<details>
<summary>Show the table (39 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| bin_0 | 1 | 0.0 | 605143 | 53.29 |
| bin_0 | 2 | 1.0 | 530487 | 46.71 |
| bin_1 | 1 | 1.0 | 747477 | 65.82 |
| bin_1 | 2 | 0.0 | 388153 | 34.18 |
| bin_2 | 1 | 1.0 | 843557 | 74.28 |
| bin_2 | 2 | 0.0 | 292073 | 25.72 |
| cat_0 | 1 | 251 | 1573 | 0.14 |
| cat_0 | 2 | 889 | 1416 | 0.12 |
| cat_0 | 3 | 94 | 1407 | 0.12 |
| cat_0 | 4 | 1327 | 1402 | 0.12 |
| cat_0 | 5 | 1544 | 1158 | 0.1 |
| cat_1 | 1 | 1 | 247459 | 21.79 |
| cat_1 | 2 | 7 | 80685 | 7.1 |
| cat_1 | 3 | 2 | 68162 | 6 |
| cat_1 | 4 | 34 | 50442 | 4.44 |
| cat_1 | 5 | 6 | 27670 | 2.44 |
| cat_2 | 1 | 120 | 3357 | 0.3 |
| cat_2 | 2 | 172 | 2617 | 0.23 |
| cat_2 | 3 | 381 | 2426 | 0.21 |
| cat_2 | 4 | 361 | 2354 | 0.21 |
| cat_2 | 5 | 196 | 2301 | 0.2 |
| cat_3 | 1 | 827 | 1159 | 0.1 |
| cat_3 | 2 | 121 | 937 | 0.08 |
| cat_3 | 3 | 916 | 845 | 0.07 |
| cat_3 | 4 | 86 | 807 | 0.07 |
| cat_3 | 5 | 1085 | 796 | 0.07 |
| cat_4 | 1 | 1 | 749787 | 66.02 |
| cat_4 | 2 | 2 | 385219 | 33.92 |
| cat_4 | 3 | 3 | 624 | 0.05 |
| cat_5 | 1 | 2 | 1048970 | 92.37 |
| cat_5 | 2 | 27 | 7945 | 0.7 |
| cat_5 | 3 | 568 | 150 | 0.01 |
| cat_5 | 4 | 293 | 136 | 0.01 |
| cat_5 | 5 | 218 | 120 | 0.01 |
| timestamp | 1 | 2023-11-22 16:01:37 | 8 | 0 |
| timestamp | 2 | 2023-12-24 13:16:13 | 7 | 0 |
| timestamp | 3 | 2023-12-01 12:34:33 | 7 | 0 |
| timestamp | 4 | 2023-12-16 10:51:25 | 7 | 0 |
| timestamp | 5 | 2023-12-24 11:18:42 | 7 | 0 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a217f6-0aa0-71e6-8604-d6bdd00e741c |
| checksum | v2:b77b0506fcb7f4191e23b99f05b654254f0527f961e51b57762e8129a0e7ac3a |
| built_at | 2026-11-26T13:09:22+00:00 |
| path | cooking_time_1m/01a217f6-0aa0-71e6-8604-d6bdd00e741c |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
