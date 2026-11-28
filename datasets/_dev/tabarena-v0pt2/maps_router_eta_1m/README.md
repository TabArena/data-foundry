---
report_format: data-foundry-report-v2
unique_name: maps_router_eta_1m
container_format: 2
checksum: v2:8c716f7f7c75013e47df0651a6ceb90da506065abb09e74c80d1c4bb13c7214e
build:
  uuid: 01a217f9-ef72-765d-af6c-5c08d1ed6255
  checksum: v2:8c716f7f7c75013e47df0651a6ceb90da506065abb09e74c80d1c4bb13c7214e
  built_at: '2026-11-26T13:41:04+00:00'
  path: maps_router_eta_1m/01a217f9-ef72-765d-af6c-5c08d1ed6255
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
  n_rows: 11463937
  n_features: 988
  dtypes:
    category: 2
    datetime64[ns]: 1
    float32: 985
    float64: 1
  n_test_dataset_rows: null
task:
  target: target_log_spkm
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
    TabReD trains on 1-20 November 2023, validates on 20-27 November and tests on
    27 November to 4 December (https://arxiv.org/abs/2406.19380). TabReD states no
    refit cadence, so the length says how long one fitted model serves. A week holds
    every weekday once, and travel times are lower on weekends. The routes run over
    40 days, 1 November to 10 December 2023, so every possible window is a late-autumn
    week: none can test another year, another season or the year-end holidays. The
    test windows are the three newest weeks (CC 2026-11-11), newest first: 4-10 December,
    27 November to 3 December and 20-26 November, the last two TabReD''s own test
    and validation weeks. The oldest window, 20-26 November, trains on less than half
    the routes (44.8%), the two newest on more; it stays as the curator''s exception,
    as three whole weeks above half do not fit in the 40 days without overlap (Andrej,
    2026-11-20). The windows walk back from the newest because the 40 days leave no
    other choice: a fourth whole week, 13-19 November, would train on about a quarter
    (27.2%). The gap of one day is part of the task: a travel time is known only when
    the drive ends (up to 16.6 hours after the request, from the target and track_length
    in metres), so at a window''s start the last routes before it have no label yet;
    without the gap 656, 654 and 578 train routes per window (request time + seconds
    per km x km) would end after the window start, with it none. The gap removes 292k,
    313k and 299k of the 11.2M, 8.8M and 6.4M earlier routes (2.6 to 4.7%). TabReD
    documents only the target (log seconds per km), not the unit of track_length;
    we read it as metres because no value is below 1,000.0 (TabReD''s 1 km floor,
    we assume) and the implied drive is then 0.03 to 16.6 hours (median 12 minutes),
    against a median of 194 hours if read as km. The data have few implausible rows:
    31 of 13.6M (12 above 150 km/h, 5 below 2 km/h, 14 longer than 12 hours), none
    among the late routes, so the gap is set by ordinary short drives requested in
    the last hours before a window start.'
  n_train:
    min: 6108934
    max: 10902438
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
    splits_train_under_half: 'The curator''s exception for this dataset (Andrej, 2026-11-20;
      first signed off by Lennart, 2026-11-11): the oldest week trains on 44.8% of
      all routes, beside 79.9% and 62.3%; a third whole week above half does not fit
      in the 40 days without overlap, and the week is TabReD''s own validation week.'
decisions: []
---

# maps_router_eta_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `target_log_spkm`, scored with `rmse` on temporal splits by `timestamp`. 11,463,937 rows and 988 features. Source: Kaggle (2024).

Built as `01a217f9-ef72-765d-af6c-5c08d1ed6255` on 2026-11-26. See [Build](#build).

## In brief

**Question.** How long will a car take per kilometre on a requested route, given the current road conditions?

**Use case.** A car navigation service, when a driver requests a route, predicts the travel time from the current road conditions (TabReD's description).

**One row.** One car route of a navigation service from 1 November to 10 December 2023, from TabReD's 2.5% random sample of the log; service and region not stated.

**Predicted.** The travel time per kilometre, as the log of seconds per kilometre.

**Known at prediction time.** Anonymous numeric, categorical and yes/no features that summarise the route's road graph, its current traffic and road details such as speed limits, plus the time of the request.

**What the test data stands for.** Each test window is one of the three newest weeks (20 November to 10 December 2023), up to 500,000 routes each; a week is TabReD's own validation and test length. Training is every route requested at least a day before the window, of which a benchmark fits on a random million; the oldest window trains on 45% of the routes.

> **Use case fit: direct (the rows, features and split mirror the use case).** The features describe the route and the road conditions at the request, and later weeks are tested. They are anonymous, so their timing cannot be checked one by one.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/maps_router_eta.md`](../../../../curation/records/maps_router_eta.md)
- The original source: <https://www.kaggle.com/datasets/pcovkrd84mejm/maps-routing>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/maps_router_eta/`. To get them:

```text
We get the TabRed data from Kaggle.

kaggle datasets download -d pcovkrd84mejm/maps-routing -f maps_routing.parquet && unzip maps_routing.parquet.zip && rm maps_routing.parquet.zip && mkdir -p local-data-warehouse/maps_router_eta && mv maps_routing.parquet local-data-warehouse/maps_router_eta/
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/maps_router_eta_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/maps_router_eta_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/datasets/pcovkrd84mejm/maps-routing |
| year | 2024 |
| domain | industry & manufacturing |
| license | CC-BY-NC-SA-4.0 |
| data_tags | Non-IID, Temporal, Anonymized |
| reference | rubachev2025tabred |
| rows x columns | 11,463,937 x 989 |
| task.target | target_log_spkm |
| task.problem_type | regression |
| task.metric | rmse |
| task.split_regime | temporal_non_iid |
| task.time_on | timestamp |

**Metric**

| field | value |
|---|---|
| name | `rmse` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | RMSE (TabReD's regression metric) |
| reference | Rubachev et al., TabReD, ICLR 2025 (https://arxiv.org/abs/2406.19380) |
| definition | Root mean squared error of the log seconds-per-km target, as TabReD scores its regression tasks |

<details>
<summary>Feature types: 2 categorical, 0 string, 1 datetime</summary>

- categorical (2): `cat_0`, `cat_1`
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

The first 5 of 11,463,937 rows of the final frame (the oldest rows: the frame is sorted by `timestamp`); 12 of 989 columns, the target first. Cells are cut at 40 characters.

| target_log_spkm | num_0 | num_1 | num_2 | num_3 | num_4 | num_5 | num_6 | num_7 | num_8 | num_9 | num_10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4.99357 | 0.689529 | 0.678433 | 0.426459 | 0.393967 | 0.294161 | -0.0414126 | -1.16444 | -0.47381 | 0.206696 | -0.0716214 | -0.0378767 |
| 3.96892 | 0.292676 | 0.287442 | -0.199347 | 2.34355 | -1.43644 | 1.40791 | 0.282216 | -1.03009 | 0.783473 | 1.68491 | -0.979039 |
| 4.59788 | -0.490721 | -0.502074 | -1.25396 | -0.748138 | 0.0815958 | -0.0414126 | 0.282216 | -0.47381 | 0.398997 | 0.605554 | -0.93644 |
| 4.37939 | 0.292676 | 0.287442 | 1.28191 | 1.45218 | -0.0526489 | 0.703922 | 0.282216 | 0.221344 | 0.266668 | 0.933027 | -0.162066 |
| 4.07423 | 0.968089 | 0.287442 | 1.15977 | 0.548366 | -1.7426 | 1.40791 | 0.282216 | -1.03009 | 1.73222 | 2.02775 | -0.974379 |

## Curation notes

We start with data from TabRed, which already comes preprocessed.
We perform no additional preprocessing steps.

- Potential leak, kept on purpose: TabReD releases the 984 numeric features only after a quantile transform to a normal distribution (all within ±5.1993, the clip of scikit-learn's QuantileTransformer; 624 reach it); which rows it was fit on is not documented, and the raw features are not published. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if the TabReD authors say the fit used all rows.
- The row budget: each test window keeps at most 500k of its rows, drawn at random within the window, and each train side holds every earlier row (minus the one-day gap); the frame keeps every row a split uses. The 1M train budget is recorded, not applied: a benchmark sub-samples each train side to 1M rows before a fit with `subsample_train`, by default a random 1M of the newest year before the window. The data span 1 November to 10 December 2023, so that is a random 1M of all earlier routes, as in TabReD: random sub-sampling instead of a time-based one keeps data from the whole period and the distribution shift across it.

## Splits

Expanding-window temporal splits: 3 test window(s) of 7 days, walking back from the newest data, newest first; train is all earlier data up to a gap of 1 days. The test windows by `timestamp`, as listed: 2023-12-04 to 2023-12-10 (500,000 test, 10,902,438 train rows); 2023-11-27 to 2023-12-03 (500,000 test, 8,496,883 train rows); 2023-11-20 to 2023-11-26 (500,000 test, 6,108,934 train rows). Each test window keeps at most 500k of its rows, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows (by default rows drawn at random from the newest year before each window, extended back in time until it holds that many rows, `subsample_train`).

Each test window is one week, TabReD's own validation and test length: TabReD trains on 1-20 November 2023, validates on 20-27 November and tests on 27 November to 4 December (https://arxiv.org/abs/2406.19380). TabReD states no refit cadence, so the length says how long one fitted model serves. A week holds every weekday once, and travel times are lower on weekends. The routes run over 40 days, 1 November to 10 December 2023, so every possible window is a late-autumn week: none can test another year, another season or the year-end holidays. The test windows are the three newest weeks (CC 2026-11-11), newest first: 4-10 December, 27 November to 3 December and 20-26 November, the last two TabReD's own test and validation weeks. The oldest window, 20-26 November, trains on less than half the routes (44.8%), the two newest on more; it stays as the curator's exception, as three whole weeks above half do not fit in the 40 days without overlap (Andrej, 2026-11-20). The windows walk back from the newest because the 40 days leave no other choice: a fourth whole week, 13-19 November, would train on about a quarter (27.2%). The gap of one day is part of the task: a travel time is known only when the drive ends (up to 16.6 hours after the request, from the target and track_length in metres), so at a window's start the last routes before it have no label yet; without the gap 656, 654 and 578 train routes per window (request time + seconds per km x km) would end after the window start, with it none. The gap removes 292k, 313k and 299k of the 11.2M, 8.8M and 6.4M earlier routes (2.6 to 4.7%). TabReD documents only the target (log seconds per km), not the unit of track_length; we read it as metres because no value is below 1,000.0 (TabReD's 1 km floor, we assume) and the implied drive is then 0.03 to 16.6 hours (median 12 minutes), against a median of 194 hours if read as km. The data have few implausible rows: 31 of 13.6M (12 above 150 km/h, 5 below 2 km/h, 14 longer than 12 hours), none among the late routes, so the gap is set by ordinary short drives requested in the last hours before a window start.

3 repeat(s) x 1 fold(s) with seed 4267; train 6,108,934 to 10,902,438 rows, test 500,000 rows. Prediction horizon: 7 days. Gap between train and test: 1 days. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as rows.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 10902438 | 500000 | 2023-11-01 00:00:13 | 2023-12-02 23:59:58 | 2023-12-04 00:00:29 | 2023-12-10 23:59:52 |
| 1 | 0 | 8496883 | 500000 | 2023-11-01 00:00:13 | 2023-11-25 23:59:55 | 2023-11-27 00:00:53 | 2023-12-03 23:59:53 |
| 2 | 0 | 6108934 | 500000 | 2023-11-01 00:00:13 | 2023-11-18 23:59:57 | 2023-11-20 00:00:37 | 2023-11-26 23:59:49 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows maps_router_eta_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Dec 2023 | 500000 | 0.951 | mean 4.893, median 4.91, p10 4.412, p90 5.34 | mean 4.858, median 4.874, p10 4.371, p90 5.311 | 0.039 | num_87 (0.04), num_81 (0.04), num_84 (0.04) | 0 |
| 1 | Nov 2023 - Dec 2023 | 500000 | 0.741 | mean 4.887, median 4.899, p10 4.407, p90 5.339 | mean 4.844, median 4.861, p10 4.35, p90 5.307 | 0.025 | num_427 (0.03), num_537 (0.02), num_428 (0.02) | 0 |
| 2 | Nov 2023 | 500000 | 0.533 | mean 4.88, median 4.892, p10 4.396, p90 5.337 | mean 4.843, median 4.861, p10 4.351, p90 5.301 | 0.059 | num_427 (0.06), num_428 (0.06), num_100 (0.06) | 0 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicates_skipped`: Skipped duplicate-column/row checks: 11,337,833,693 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to run them; nothing else checks duplicate rows and columns.)

Accepted on purpose:

- `splits_train_under_half`: The curator's exception for this dataset (Andrej, 2026-11-20; first signed off by Lennart, 2026-11-11): the oldest week trains on 44.8% of all routes, beside 79.9% and 62.3%; a third whole week above half does not fit in the 40 days without overlap, and the week is TabReD's own validation week.

## Data checks

### Feature summary

<details>
<summary>Show the table (989 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| cat_0 | category | 0 | 0 | 93 | 1, 2, 7, 4, 10, 6, 5, 3, 18, 8 |
| cat_1 | category | 0 | 0 | 94 | 1, 2, 7, 4, 10, 6, 5, 3, 18, 8 |
| timestamp | datetime64\[ns\] | 0 | 0 | 2.81291e+06 | 2023-11-03 09:41:11, 2023-11-23 08:17:07, 2023-12-02 16:24:54, 2023-11-25 14:13… |
| num_457 | float32 | 1.11461e+07 | 97.23 | 69276 | -0.7152, -0.0464, 0.7647, -1.6897, 0.3481, 1.1449, -1.2075, 1.4216, 1.7387, 2.0… |
| num_348 | float32 | 1.11197e+07 | 97 | 75454 | -0.6257, 0.0364, -1.567, 0.832, 0.4197, 1.1972, -1.1024, 1.4642, 1.3526, 1.78 |
| num_566 | float32 | 1.10984e+07 | 96.81 | 73418 | -0.5336, 0.1144, -1.5215, 0.8717, 0.4766, -1.0188, 1.2394, 1.4942, 1.805, 2.0854 |
| num_675 | float32 | 1.09104e+07 | 95.17 | 90825 | -0.1068, -1.1305, 0.5221, 1.1769, 0.8427, -0.5496, 1.498, 1.7502, 0.2953, 2.0533 |
| num_239 | float32 | 1.08683e+07 | 94.8 | 105796 | -1.0575, -0.0703, 0.5511, 0.879, 1.2259, -0.478, 1.5377, 1.7862, 1.6845, 0.3106 |
| num_784 | float32 | 1.01327e+07 | 88.39 | 155403 | -0.7039, 0.5035, 1.1744, 0.0854, 1.439, 1.7275, 0.9694, 1.995, 2.2318, 2.144 |
| num_130 | float32 | 5.7531e+06 | 50.18 | 555934 | -0.3535, 1.2669, 0.8662, 2.0137, 2.2258, 2.4569, 1.7619, -3.0899, 2.6563, 2.5839 |
| num_893 | float32 | 2.83222e+06 | 24.71 | 687536 | -0.3111, 1.4753, 1.0379, 2.3995, -3.1014, 2.0799, 2.6517, 2.8778, 2.5118, 3.0937 |
| num_972 | float32 | 2.47233e+06 | 21.57 | 5.47009e+06 | 3.092, 3.09, 3.0937, 3.0923, 3.0907, 3.0907, 3.0907, -0.5381, 0.3071, -0.7133 |
| num_973 | float32 | 2.47233e+06 | 21.57 | 5.50869e+06 | 3.0903, 3.0904, 3.0906, 3.0971, -0.1349, -0.2755, -0.552, 3.0914, 3.0903, 3.0926 |
| num_974 | float32 | 2.47233e+06 | 21.57 | 5.43922e+06 | -0.4968, 3.0912, 0.0087, -0.5555, 3.0903, 3.0902, -0.4147, -0.5016, 0.6507, 3.0… |
| num_883 | float32 | 2.22937e+06 | 19.45 | 3.91788e+06 | -0.5885, 3.0908, 3.0903, 3.0899, -5.1993, 3.0902, 3.0906, 3.0904, 3.0901, -0.13… |
| num_915 | float32 | 1.95529e+06 | 17.06 | 3 | -0.3844, 0.8553, 1.6793 |
| num_916 | float32 | 1.95529e+06 | 17.06 | 4.09214e+06 | -1.2448, 0.1842, 1.6793, -0.1794, -0.4581, -0.486, 1.0532, 0.6317, -0.6526, 0.4… |
| num_917 | float32 | 1.95529e+06 | 17.06 | 3 | 0.8127, -0.2575, -1.2448 |
| num_918 | float32 | 1.9554e+06 | 17.06 | 3 | -0.3857, 0.8517, 1.6742 |
| num_919 | float32 | 1.9554e+06 | 17.06 | 4.08804e+06 | -1.2421, 0.1817, 1.6742, -0.1799, -0.4562, -0.4837, 1.0504, 0.4107, -0.7759, 0.… |
| num_920 | float32 | 1.9554e+06 | 17.06 | 3 | 0.8144, -0.2549, -1.2421 |
| num_921 | float32 | 1.95557e+06 | 17.06 | 3 | -0.3871, 0.8499, 1.6742 |
| num_922 | float32 | 1.95557e+06 | 17.06 | 4.0875e+06 | -1.2448, 0.1791, 1.6742, -0.1825, -0.4571, -0.4847, 1.048, 0.4081, 0.6263, -0.7… |
| num_923 | float32 | 1.95557e+06 | 17.06 | 3 | 0.8127, -0.2575, -1.2448 |
| num_906 | float32 | 1.94568e+06 | 16.97 | 4188 | -1.331, -0.7614, -0.5264, -0.3669, -0.2471, -0.1448, -0.0603, 0.0151, 0.0804, 0… |
| num_907 | float32 | 1.94568e+06 | 16.97 | 7.26092e+06 | -2.9886, -2.4655, -2.1929, -2.0074, -1.8605, -1.7387, -1.6347, -1.5402, -1.4551… |
| num_908 | float32 | 1.94568e+06 | 16.97 | 10458 | -1.5713, -1.63, -1.425, -1.2697, -1.4716, -1.5186, -1.3814, -1.2313, -1.1694, -… |
| num_909 | float32 | 1.94568e+06 | 16.97 | 3745 | -1.331, -0.758, -0.5235, -0.3669, -0.2445, -0.1448, -0.0577, 0.0151, 0.0829, 0.… |
| num_910 | float32 | 1.94568e+06 | 16.97 | 7.26192e+06 | -2.9886, -2.4655, -2.2009, -2.0137, -1.8659, -1.7453, -1.6379, -1.5445, -1.4597… |
| num_911 | float32 | 1.94568e+06 | 16.97 | 10565 | -1.2641, -1.63, -1.5713, -1.5175, -1.3022, -1.3402, -1.425, -1.4716, -1.3814, -… |
| num_912 | float32 | 1.94568e+06 | 16.97 | 2936 | -1.331, -0.758, -0.525, -0.3669, -0.2445, -0.146, -0.0603, 0.0151, 0.0804, 0.13… |
| num_913 | float32 | 1.94568e+06 | 16.97 | 7.2616e+06 | -2.9886, -2.4655, -2.1969, -2.0113, -1.867, -1.743, -1.6376, -1.5458, -1.4605, … |
| num_914 | float32 | 1.94568e+06 | 16.97 | 10692 | -1.5742, -1.63, -1.5215, -1.3846, -1.425, -1.3433, -1.2367, -1.2697, -1.6949, -… |
| num_924 | float32 | 1.94568e+06 | 16.97 | 252 | -1.4193, -0.8144, -0.5083, -0.2705, -0.0758, 0.0879, 0.2252, 0.3402, 0.4381, 0.… |
| num_925 | float32 | 1.94568e+06 | 16.97 | 7.40651e+06 | -3.1048, -2.4569, -2.0966, -1.8517, -1.6446, -1.3402, -1.0932, -1.4828, -1.2101… |
| num_926 | float32 | 1.94568e+06 | 16.97 | 311 | -0.146, -0.0439, 0.0389, -0.0842, -0.2085, -0.1043, 0.1005, -0.294, -0.1245, -0… |
| num_927 | float32 | 1.94568e+06 | 16.97 | 238 | -1.4195, -0.8149, -0.5092, -0.2718, -0.0766, 0.0867, 0.2248, 0.3406, 0.439, 0.5… |
| num_928 | float32 | 1.94568e+06 | 16.97 | 7.40676e+06 | -3.1024, -2.4569, -2.0966, -1.8516, -1.649, -1.4828, -1.0905, -1.3348, -1.2101,… |
| num_929 | float32 | 1.94568e+06 | 16.97 | 319 | -0.0414, -0.0615, -0.2085, 0.0, -0.2291, -0.0829, 0.0201, -0.1245, -0.2497, 0.1… |
| num_930 | float32 | 1.94568e+06 | 16.97 | 252 | -1.4202, -0.8144, -0.5092, -0.2731, -0.0783, 0.0854, 0.2226, 0.3375, 0.4353, 0.… |
| num_931 | float32 | 1.94568e+06 | 16.97 | 7.40799e+06 | -3.1103, -2.4569, -2.0965, -1.8469, -1.6444, -1.4783, -1.3341, -1.0887, -1.2049… |
| num_932 | float32 | 1.94568e+06 | 16.97 | 314 | -0.0439, -0.1271, -0.0854, -0.1068, -0.0025, 0.0188, -0.2111, 0.0791, 0.0389, -… |
| num_933 | float32 | 1.94568e+06 | 16.97 | 489 | -0.6364, -0.3415, -0.5322, -0.5672, -0.4992, -0.5999, -0.7816, -0.7088, -0.4335… |
| num_934 | float32 | 1.94568e+06 | 16.97 | 6.44118e+06 | 0.054, 0.1575, 0.3362, 0.1829, 0.5308, 0.2342, 0.3602, 0.434, 0.4093, 0.4584 |
| num_935 | float32 | 1.94568e+06 | 16.97 | 564 | -0.0364, -0.2124, -0.1018, -0.1245, -0.146, -0.0804, -0.059, -0.1906, -0.2562, … |
| num_936 | float32 | 1.94568e+06 | 16.97 | 485 | -0.5969, -0.5293, -0.3388, -0.5613, -0.6303, -0.4006, -0.4626, -0.7023, -0.3682… |
| num_937 | float32 | 1.94568e+06 | 16.97 | 6.44166e+06 | 0.3583, 0.0531, 0.5293, 0.4328, 0.1563, 0.5052, 0.4082, 0.1818, 0.1304, 0.2833 |
| num_938 | float32 | 1.94568e+06 | 16.97 | 571 | -0.1296, -0.1524, -0.1081, -0.2394, 0.0213, -0.0439, -0.1957, -0.0867, -0.0213,… |
| num_939 | float32 | 1.94568e+06 | 16.97 | 483 | -0.5969, -0.6674, -0.5643, -0.464, -0.2783, -0.3388, -0.6333, -0.5293, -0.4006,… |
| num_940 | float32 | 1.94568e+06 | 16.97 | 6.44293e+06 | 0.1829, 0.3335, 0.3576, 0.054, 0.2336, 0.4078, 0.5286, 0.5047, 0.4559, 0.4319 |
| num_941 | float32 | 1.94568e+06 | 16.97 | 572 | -0.1727, -0.1068, -0.1283, -0.1499, -0.0842, -0.0402, -0.2809, -0.0615, 0.0025,… |
| num_942 | float32 | 1.94568e+06 | 16.97 | 352 | -0.4197, -0.5307, -0.3655, -0.588, -0.4738, -0.6472, -0.3124, -0.2627, -0.2124,… |
| num_943 | float32 | 1.94568e+06 | 16.97 | 6.75673e+06 | 0.3007, -0.2992, 0.0431, -0.2653, 0.1093, -0.0582, 0.5677, 0.2059, 0.331, 0.0093 |
| num_944 | float32 | 1.94568e+06 | 16.97 | 398 | -0.1829, -0.1575, -0.1321, -0.0565, -0.0816, -0.005, -0.0314, -0.2072, 0.0452, … |
| num_945 | float32 | 1.94568e+06 | 16.97 | 355 | -0.4197, -0.588, -0.4738, -0.5307, -0.6487, -0.3655, -0.3137, -0.2627, -0.2136,… |
| num_946 | float32 | 1.94568e+06 | 16.97 | 6.75494e+06 | 0.3019, 0.11, 0.5705, -0.6518, -0.2969, 0.2394, -0.3678, 0.0771, -0.0892, 0.4538 |
| num_947 | float32 | 1.94568e+06 | 16.97 | 407 | -0.0565, -0.0816, -0.1575, -0.0314, 0.0176, -0.0075, -0.1829, -0.2098, -0.2588,… |
| num_948 | float32 | 1.94568e+06 | 16.97 | 351 | -0.417, -0.5279, -0.585, -0.4724, -0.3629, -0.3111, -0.6456, -0.2601, -0.2111, … |
| num_949 | float32 | 1.94568e+06 | 16.97 | 6.75412e+06 | 0.3015, -0.4752, 0.3317, 0.1084, 0.0088, 0.4226, -0.0917, -0.4041, -0.3693, 0.1… |
| num_950 | float32 | 1.94568e+06 | 16.97 | 397 | -0.1587, -0.2098, -0.0088, -0.1842, -0.0829, -0.1334, -0.0577, 0.0163, -0.2355,… |

(929 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | -0.17 | -0.442 | 0.142 | 0.006 | log | 7.77812e+06 | 1.54966e+20 | exponential |

### Numeric features

<details>
<summary>Show the table (986 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| num_0 | 1.14639e+06 | 0.0128664 | 0.969493 | -1.66337 | 5.19934 |
| num_1 | 1.14639e+06 | 0.0133812 | 0.971079 | -1.69359 | 5.19934 |
| num_2 | 1.14639e+06 | -0.000287927 | 1.00055 | -5.19934 | 4.55473 |
| num_3 | 1.14639e+06 | 0.0485897 | 0.864966 | -0.748138 | 5.19934 |
| num_4 | 1.14639e+06 | 0.0129246 | 0.997871 | -5.19934 | 3.87485 |
| num_5 | 1.14639e+06 | -0.000112111 | 0.938031 | -2.81896 | 5.19934 |
| num_6 | 1.14639e+06 | -0.0545168 | 0.683268 | -5.19934 | 3.15253 |
| num_7 | 1.14639e+06 | 0.0150427 | 0.936356 | -1.68967 | 3.29025 |
| num_8 | 1.1333e+06 | -0.0120099 | 0.995268 | -5.19934 | 3.56433 |
| num_9 | 1.1333e+06 | -0.0675138 | 1.00162 | -5.19934 | 4.072 |
| num_10 | 1.13299e+06 | -0.0116493 | 0.994715 | -5.19934 | 3.82032 |
| num_11 | 1.14639e+06 | 0.0745044 | 0.992969 | -5.19934 | 5.19934 |
| num_12 | 1.14639e+06 | -0.012092 | 0.995825 | -5.19934 | 3.74109 |
| num_13 | 1.14639e+06 | -0.0124153 | 0.997874 | -5.19934 | 3.825 |
| num_14 | 1.14639e+06 | -0.000370988 | 0.0183615 | -0.000479446 | 3.24716 |
| num_15 | 1.14639e+06 | -0.0136386 | 0.993441 | -5.19934 | 3.73962 |
| num_16 | 1.14639e+06 | -0.000431669 | 1.00043 | -5.1488 | 4.83803 |
| num_17 | 1.14639e+06 | -0.050117 | 0.994171 | -5.19934 | 3.49398 |
| num_18 | 1.14639e+06 | -0.0598072 | 0.999771 | -5.19934 | 5.19934 |
| num_19 | 1.14639e+06 | 0.0462416 | 0.876317 | -0.80492 | 5.19934 |
| num_20 | 1.14639e+06 | -0.0143337 | 0.995851 | -5.19934 | 3.77579 |
| num_21 | 994900 | 0.0627325 | 0.813802 | -3.16013 | 5.19934 |
| num_22 | 1.14639e+06 | 0.0219663 | 0.961893 | -1.5036 | 2.5383 |
| num_23 | 1.14639e+06 | 0.0794006 | 0.737001 | -0.328619 | 5.19934 |
| num_24 | 1.14639e+06 | 0.0100124 | 0.997353 | -3.84279 | 5.19934 |
| num_25 | 1.14639e+06 | 0.00190179 | 0.996102 | -5.19934 | 3.96257 |
| num_26 | 1.14639e+06 | 0.0639997 | 0.997011 | -5.19934 | 5.19934 |
| num_27 | 1.14639e+06 | -0.00891125 | 0.994904 | -5.19934 | 3.68033 |
| num_28 | 1.14639e+06 | -0.0126756 | 0.996034 | -3.64996 | 4.03247 |
| num_29 | 1.14639e+06 | 0.0466912 | 0.801672 | -3.40266 | 3.08994 |
| num_30 | 1.14639e+06 | 0.0172804 | 0.797324 | -1.88035 | 5.19934 |
| num_31 | 1.14639e+06 | 0.00791007 | 0.940377 | -2.21209 | 5.19934 |
| num_32 | 1.14639e+06 | 0.0166747 | 0.970591 | -1.63396 | 5.19934 |
| num_33 | 1.14639e+06 | 0.0588112 | 0.579548 | -0.13171 | 4.08484 |
| num_34 | 1.1321e+06 | 0.0670497 | 0.860296 | -0.726606 | 5.19934 |
| num_35 | 1.1321e+06 | -0.00766542 | 0.99751 | -5.19934 | 3.63038 |
| num_36 | 1.1321e+06 | -0.0129185 | 0.990035 | -5.19934 | 5.19934 |
| num_37 | 1.1321e+06 | 0.0658912 | 0.860355 | -0.726606 | 5.19934 |
| num_38 | 1.1321e+06 | -0.00807393 | 0.997423 | -5.19934 | 5.19934 |
| num_39 | 1.1321e+06 | -0.0124593 | 0.989464 | -5.19934 | 5.19934 |
| num_40 | 1.1321e+06 | 0.0656752 | 0.85959 | -0.724973 | 5.19934 |
| num_41 | 1.1321e+06 | -0.00643643 | 0.996706 | -5.19934 | 5.19934 |
| num_42 | 1.1321e+06 | -0.0109631 | 0.989781 | -5.19934 | 5.19934 |
| num_43 | 1.13195e+06 | 0.0667335 | 0.603278 | -0.163824 | 2.19689 |
| num_44 | 1.13195e+06 | -0.0016844 | 0.981303 | -1.87305 | 2.19689 |
| num_45 | 1.13195e+06 | -0.0645623 | 0.737289 | -1.86585 | 0.451469 |
| num_46 | 1.13194e+06 | 0.0663185 | 0.602719 | -0.163824 | 2.19689 |
| num_47 | 1.13194e+06 | -7.69844e-05 | 0.980229 | -1.86585 | 2.19689 |
| num_48 | 1.13194e+06 | -0.0648495 | 0.737639 | -1.86585 | 0.451469 |
| num_49 | 1.13194e+06 | 0.0668118 | 0.605713 | -0.165095 | 2.21113 |
| num_50 | 1.13194e+06 | -0.00163046 | 0.98094 | -1.87305 | 2.19689 |
| num_51 | 1.13194e+06 | -0.0646489 | 0.736883 | -1.86585 | 0.45008 |
| num_52 | 1.1321e+06 | 0.0262476 | 0.918726 | -1.08872 | 5.19934 |
| num_53 | 1.1321e+06 | -0.0284555 | 1.0015 | -5.19934 | 5.19934 |
| num_54 | 1.1321e+06 | -0.0363352 | 0.994641 | -5.19934 | 3.63256 |
| num_55 | 1.1321e+06 | 0.0280801 | 0.917038 | -1.0857 | 5.19934 |
| num_56 | 1.1321e+06 | -0.0304802 | 1.00075 | -5.19934 | 5.19934 |
| num_57 | 1.1321e+06 | -0.0388321 | 0.996081 | -5.19934 | 3.60014 |
| num_58 | 1.1321e+06 | 0.0269001 | 0.918396 | -1.08721 | 5.19934 |
| num_59 | 1.1321e+06 | -0.0290595 | 1.0009 | -5.19934 | 5.19934 |

(926 more rows not shown)

</details>

### Categorical features

<details>
<summary>Show the table (15 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| cat_0 | 1 | 1 | 887151 | 77.39 |
| cat_0 | 2 | 2 | 79202 | 6.91 |
| cat_0 | 3 | 7 | 46502 | 4.06 |
| cat_0 | 4 | 4 | 42922 | 3.74 |
| cat_0 | 5 | 10 | 31341 | 2.73 |
| cat_1 | 1 | 1 | 887153 | 77.39 |
| cat_1 | 2 | 2 | 79202 | 6.91 |
| cat_1 | 3 | 7 | 46500 | 4.06 |
| cat_1 | 4 | 4 | 42922 | 3.74 |
| cat_1 | 5 | 10 | 31341 | 2.73 |
| timestamp | 1 | 2023-11-03 09:41:11 | 7 | 0 |
| timestamp | 2 | 2023-11-23 08:17:07 | 7 | 0 |
| timestamp | 3 | 2023-12-02 16:24:54 | 7 | 0 |
| timestamp | 4 | 2023-11-25 14:13:03 | 7 | 0 |
| timestamp | 5 | 2023-11-12 13:30:10 | 7 | 0 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a217f9-ef72-765d-af6c-5c08d1ed6255 |
| checksum | v2:8c716f7f7c75013e47df0651a6ceb90da506065abb09e74c80d1c4bb13c7214e |
| built_at | 2026-11-26T13:41:04+00:00 |
| path | maps_router_eta_1m/01a217f9-ef72-765d-af6c-5c08d1ed6255 |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
