---
report_format: data-foundry-report-v2
unique_name: numerai_v5_2_1m
container_format: 2
checksum: v2:1672385d846098a33013cb30c7b54a877f1e955d524c8a4fcf66a8baa47c364f
build:
  uuid: 01a218ca-2052-7ea4-b72c-31e63d9ade2b
  checksum: v2:1672385d846098a33013cb30c7b54a877f1e955d524c8a4fcf66a8baa47c364f
  built_at: '2026-11-26T17:10:34+00:00'
  path: numerai_v5_2_1m/01a218ca-2052-7ea4-b72c-31e63d9ade2b
  data_foundry_version: 0.0.5
  git_sha: 0d939f6d218cce0b083c3474f78e93095b5804d0-dirty
  libraries:
    python: 3.12.3
    pandas: 2.3.3
    numpy: 2.1.3
    pyarrow: 20.0.0
    scikit-learn: 1.7.2
    polars: 1.41.1
build_stale: false
data:
  n_rows: 6881281
  n_features: 2377
  dtypes:
    float32: 1199
    int32: 1
    int8: 1178
  n_test_dataset_rows: null
task:
  target: target_ender_20
  problem_type: regression
  metric: mean_group_pearsonr
  metric_origin: source
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: era
  time_unit: weeks
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 3
  n_folds: 1
  random_state: 4267
  time_horizon: 52
  time_horizon_unit: weeks
  time_gap: 4
  time_gap_unit: weeks
  reason: 'An era''s 20-market-day target resolves about 5 weeks later: the download
    of 2026-10-06 has targets up to era 1235 and none for 1236-1240, so at era T the
    newest known target is that of era T - 5. Numerai''s v5.2 notebook says to "embargo
    the first 4 eras following our last train era", but its code skips only 3 eras,
    so our gap is one era stricter. One year per window: Numerai ranks a model by
    its one-year average score ("Your model''s reputation is just its 1 year average
    score", which "directly determines the rank of models on the model leaderboard",
    https://docs.numer.ai/numerai-tournament/scoring) and advises retraining at major
    data releases ("it''s usually best to re-train your models when major versions
    are released", https://docs.numer.ai/numerai-tournament/data), so a model fit
    before the window predicts 52 weekly eras; participants refit anywhere from weekly
    to once per release (https://forum.numer.ai/t/how-often-do-you-re-train-your-model/8164).
    A year also holds every season. The newest window always stays, and the two before
    it walk back from it because the 2,376 features are v5.0''s set of July 2024 (about
    era 1125) and Numerai builds its features with the targets of the eras it has,
    so an older window would test on eras that shaped the features: the three newest
    years lie as close to that date as three one-year windows allow, though not after
    it (45 of the 52 eras of the oldest window, 1080-1131, come before it). Windows
    that keep at least half the rows for training reach back to era 716 (51.4%); the
    curator kept the three newest years on 2026-11-10, 3 of the 30 splits an IID split
    of this size would get (SPLIT-33). Inner validation (tuning, early stopping) must
    be era-blocked with a 4-era gap as well: a stock''s 20-day targets overlap for
    3 eras, so on the newest train side a random hold-out gives LightGBM a per-era
    correlation of 0.040 (t 16.8), against 0.004 (t 1.1) on the last 52 train eras
    after a 4-era gap.'
  n_train:
    min: 5834640
    max: 6492875
  n_test:
    min: 327025
    max: 361712
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
  - task_metric_input_is_model_input
  accepted:
    splits_dimensions_off_protocol: 'Three windows against the 30 an IID split of
      1,235 eras would get (SPLIT-33): older one-year windows would test eras whose
      targets built the v5.0 features of July 2024, so the curator kept the three
      newest years on 2026-11-10. The splits comment names the target, the count reached
      and what stops more (SPLIT-15; Lennart, 2026-11-26).'
    task_feature_looks_like_exposure: 'A false positive of the name heuristic: `feature_swept_irrespirable_grillade`
      is one of Numerai''s 2,376 anonymised features, whose names are random words;
      no feature is an amount at risk (Lennart, 2026-11-26).'
    task_target_value_dominant: The target is Numerai's within-era rank of a return,
      binned into five ordered levels; the middle level 0.5 holds half the rows by
      construction, and the task is scored by per-era correlation (Lennart, 2026-11-26).
    task_target_low_cardinality: The target is a continuous return that Numerai ranks
      within each era and bins into 5 ordered levels (0 to 1); Numerai treats it as
      regression (its example models are regressors scored by correlation), and so
      do we.
decisions:
- Feature-eras filled with the middle bin are set to missing
---

# numerai_v5_2_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `target_ender_20`, scored with `mean_group_pearsonr` on temporal splits by `era` (one step is a week). 6,881,281 rows and 2,377 features. Source: Other (2025).

Built as `01a218ca-2052-7ea4-b72c-31e63d9ade2b` on 2026-11-26. See [Build](#build).

## In brief

**Question.** How will a stock's return over the next 20 market days rank against the other stocks of the same week?

**Use case.** Every Friday after the market close, a participant of the Numerai tournament scores each stock from its features as of that day and submits the scores, which Numerai combines for its trading.

**One row.** One stock in one weekly era of Numerai's v5.2 tournament data; dates and stock names are hidden.

**Predicted.** The stock's own return over the next 20 market days, ranked within the week and binned into five levels from 0 to 1; it is known about five weeks later.

**Known at prediction time.** 2,376 disguised features of the stock as of that Friday (Numerai's full set without its Faith family), each binned into five levels within the week.

**What the test data stands for.** Three test years of 52 weekly eras, the newest three, newest first: Numerai ranks a model by its one-year average score and advises retraining at major data releases. Training is all earlier eras but the last four before the test year, whose targets are not yet known; a benchmark fits on the newest 1M of their rows.

**Our changes to the source.** We set the values Numerai fills in for a feature without data in a week to missing, and use all features but the 372 that Numerai chose with the targets of our test years.

> **Use case fit: approximate (a stand-in with a known gap).** Numerai's features are designed to predict the target, and the set we use dates from July 2024, within the oldest test year. The score is Numerai's own: the per-week correlation, averaged over the weeks of the test window. Everything else is known on the Friday.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/numerai_v5_2.md`](../../../../curation/records/numerai_v5_2.md)
- The original source: <https://numer.ai/data/v5.2>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/numerai_v5_2/`. To get them:

```text
We download Numerai's v5.2 ("Faith2") tournament files with the numerapi client on 2026-10-06:

mkdir -p local-data-warehouse/numerai_v5_2 && cd local-data-warehouse/numerai_v5_2
uvx --from numerapi==3.1.1 python -c "from numerapi import NumerAPI; api = NumerAPI(); [api.download_dataset(f'v5.2/{f}', f) for f in ('features.json', 'train.parquet', 'validation.parquet')]"

Retired at the source: on 2026-10-16 Numerai released Classic v6.0 and retired the public v5.0-v5.3 training and validation downloads (docs; forum thread 8367: "The v5.x data is no longer available"), so the command above no longer serves train.parquet or validation.parquet. We keep v5.2 as a frozen release: our local files, pinned by the SHA-256 below, are the only exact copy. No community mirror matches them: the Hugging Face upload Mcdonald82/numerai-v5.2 (2026-02-23) holds the same train.parquet re-saved (same rows, schema and column statistics) but validation only to era 1206; Kaggle uploads are older snapshots or v5.3. Numerai's terms of service (4.2) forbid passing the data on, so no mirror is a sanctioned download route.

The API serves only the current weekly snapshot of each file, with no versioned URL. Ours came from the S3 folder 20261005: features.json (323,414 bytes), train.parquet (2,597,791,287 bytes, eras 1-574) and validation.parquet (4,417,740,944 bytes, eras 575-1240). Numerai adds new eras to validation.parquet as their targets resolve, so the definition keeps eras 1-1235; a later download gives the same rows as long as Numerai does not revise past eras. SHA-256 of our files:

64cd254cba63c0966eeeb71c7c83c99cacb81d4acd8b36524195d20c92dd5c35  features.json
73b41e084c91e50618227aca3759be46f59367a4506d0f3f43a5112fb83bbeca  train.parquet
04f74ad99dd1afcee046a12c52d1a98b51dab4bf978fa042aa3f5fbaeb4601c0  validation.parquet
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://numer.ai/data/v5.2 |
| year | 2025 |
| domain | finance |
| license | Numerai Terms of Service (updated 2026-08-31), section 4.2: use solely to participate in Numerai tournaments; no commercial use outside its services, no redistribution, keep the data confidential |
| data_tags | Non-IID, Temporal, Anonymized |
| reference | numerai2025v52 |
| rows x columns | 6,881,281 x 2,378 |
| task.target | target_ender_20 |
| task.problem_type | regression |
| task.metric | mean_group_pearsonr |
| task.split_regime | temporal_non_iid |
| task.time_on | era |
| task.time_unit | weeks |

**Metric**

| field | value |
|---|---|
| name | `mean_group_pearsonr` (custom; takes value; higher is better) |
| origin | source: the source's metric |
| original | CORR (numerai_corr), the per-era correlation averaged over eras |
| reference | https://docs.numer.ai/numerai-tournament/scoring/correlation-corr |
| definition | per era: rank-gaussianize the predictions, signed power 1.5; centre the target, signed power 1.5; Pearson correlation; mean over eras (numerai_tools numerai_corr) |
| params | {'method': 'numerai_corr'} |
| inputs | group: `era` |

<details>
<summary>Feature types: 0 categorical, 0 string, 0 datetime</summary>

- categorical (0): none
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{numerai2025v52,
  author = {{Numerai}},
  title = {Numerai Tournament Dataset v5.2 (Faith2)},
  year = {2025},
  howpublished = {\url{https://numer.ai/data/v5.2}},
  note = {Obfuscated global equity data, downloaded with numerapi; documentation at \url{https://docs.numer.ai/numerai-tournament/data}}
}
```

</details>

## Sample rows

The first 5 of 6,881,281 rows of the final frame (the oldest rows: the frame is sorted by `era`); 12 of 2,378 columns, the target first. Cells are cut at 40 characters.

| target_ender_20 | era | feature_abessive_philistine_camisado | feature_able_deprived_nona | feature_ablest_inflexional_egeria | feature_abrasive_forcipate_crewel | feature_absonant_wintry_hiring | feature_absorbable_hyperalgesic_mode | feature_absorbing_pluviometrical_techno… | feature_accadian_pledged_bore | feature_accepted_unviable_fruitage | feature_acclamatory_draconian_view |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 1 | 4 | 4 | nan | nan | 3 | 1 | nan | nan | 0 | 4 |
| 0.25 | 1 | 0 | 1 | nan | nan | 3 | 4 | nan | nan | 1 | 0 |
| 0.5 | 1 | 2 | 4 | nan | nan | 1 | 2 | nan | nan | 3 | 3 |
| 0.75 | 1 | 0 | 2 | nan | nan | 2 | 0 | nan | nan | 2 | 1 |
| 0.25 | 1 | 1 | 3 | nan | nan | 2 | 1 | nan | nan | 2 | 0 |

## Curation notes

We start with train.parquet and validation.parquet of the Numerai tournament data v5.2 ("Faith2"), with all features of features.json except the Faith family.

- Prediction point: every Friday after the market close (one era), a model scores each stock from its features as of that day; the target is the stock's return over the next 20 market days, known about 5 weeks later (at era T the newest resolved target is that of era T - 5).
- Scope: a ranking of the stocks within each week, not forecasting of a series. `id` is unique across all 6.88M rows, so the data holds no series per stock, and a stock's newest known target (matched by its nearest neighbour on the 780 `medium` features five eras back) correlates 0.01, -0.00 and -0.01 with its target at three test eras. Whether some disguised features are trailing returns cannot be tested.
- Target: `target_ender_20`, equal to the main target `target` of v5.2: a stock-specific return, ranked within each era and binned into 0, 0.25, 0.5, 0.75 and 1, so every era has a mean of 0.5. The other 40 target columns are future returns and are not read.
- Features: the 2,376 features of Numerai's `all` set without its 372 `faith` features (exactly v5.0's `all`, unchanged since July 2024), each an integer bin 0-4 within its era with an obfuscated name (CC 2026-10-26: "yes ship all"; CLEAN-22, no task reason leaves the other features out). With Numerai's own example and deep LightGBM settings, `medium` and `all` cannot be told apart on the test windows (the sign of the difference follows the training sample; on the full history they tie), and training on more rows helps more than either set.
- Rows: we keep data_type `train` and `validation` up to era 1235 and drop data_type `test` (eras 1236-1240), whose targets had not resolved on 2026-10-06.
- `era` (one per week; Numerai publishes no dates) becomes an integer and the time column. `id` is unique per stock per era (docs), so it identifies no stock and is not read.
- Missing values: Numerai sets every value of a feature-era without data to 2 (hello_numerai.ipynb of v5.2); we set such feature-eras to missing (decision table). Elsewhere each bin holds 20% of an era's stocks, so no single stock is filled with 2. No duplicate rows.
- Anomaly: the universe grows from 2,314 stocks in era 1 to 6,057-7,231 per era since era 1100.
- Note: the task probes flag no_signal, drift_baseline and unstable. We keep the task (task_probes.md, rule 2, TP-2): on the shipped splits, with the 2,376 features, Numerai's example LightGBM (2,000 trees, learning rate 0.01, depth 5, column sample 0.1) correlates with the target at 0.0094 ± 0.0021, 0.0127 and 0.0127 per era, newest window first, and its deep benchmark settings at 0.0108 and 0.0173 (newest and oldest windows); the probes score R², under which no model beats the mean (2026-10-26). With the 780 `medium` features, before, a 600-tree LightGBM gave 0.0071, 0.0142 and 0.0154. The newest window is fragile: one of five other random 1M train samples gives ridge a t of 0.8 there. Tuned results are pending; if tuned methods do not beat the constant 0.5 window by window under the metric that scores, the dataset goes to `TBD -> 2nd Tier` (as zillow_prize).
- Metric: Numerai's CORR, computed per era and averaged over the 52 eras of a test window (the spec). Pooled `pearsonr`, declared before, tracked it within 0.0002 per model because every era's target mean is 0.5. RMSE, declared before that, ranks the scale of the predictions, not the ranking of the stocks within each era: its model ranking agreed with per-era CORR at Kendall tau -0.11, 0.11 and 0.39 in the three windows, and a copy of one LightGBM's predictions scaled by 3 lost to the constant 0.5 in every window.
- We drop the 372 `faith` features (LEAK-31, CC 2026-10-26): Numerai engineers features "to be predictive of the target" and released the Faith family at era 1192 (Faith I) and about era 1198 (Faith II) because they predicted the target over past eras, our test eras 1080-1191 among them. Every value may be point-in-time, but the choice of features was made with our test labels. On the shipped splits, ridge with the 75 Faith features of `medium` gained +0.0043 ± 0.0006 per-era correlation in 1080-1131 (about 28% of the signal there), +0.0013 ± 0.0007 in 1132-1183, +0.0056 ± 0.0018 in 1184-1191 and +0.0010 ± 0.0006 after the release. The `midnight` features (244 in `all`, released about era 1098) stay: the 122 of them in `medium` showed no gain before their release (-0.0005 ± 0.0011 in 1080-1097). Note: Numerai's v5.0 rebuild (July 2024, about era 1125) also falls within the oldest test window; not measured.
- History: each train side holds all earlier eras but the 4-era gap, and a benchmark sub-samples it to 1M rows with the default rule (`subsample_train`): the newest year, 52 weekly eras (`time_unit="weeks"`), extended back in time until it holds 1M rows. The newest 52 eras hold 326k to 332k rows, so a benchmark fits on the newest 151 to 159 eras, about three years. Numerai's example models train on all eras; the container keeps them, for a method that samples by its own rule.
- Note: feature neutralization post-processes predictions per era, so it belongs to a model or a scorer and is not applied.
- Note: numerai28_6 (OpenML 23517), an older sample of this data, is not added separately.
- The row budget: each test window keeps at most 500k of its rows (all of them here: 327,025 to 361,712), and each train side holds every earlier era but the 4-era gap, so the frame keeps all 6,881,281 rows (eras 1-1235). The 1M train budget is recorded, not applied: a benchmark sub-samples each train side to 1M rows before a fit with `subsample_train`, whose default takes the newest year (52 eras, as `era` counts weeks) extended back in time until it holds 1M rows: eras 1021-1179 for the newest window, 973-1127 and 925-1075 for the older ones.

## Splits

Expanding-window temporal splits: 3 test window(s) of 52 time values, walking back from the newest data, newest first; train is all earlier data up to a gap of 4 time values. The test windows by `era`, as listed: 1184 to 1235 (361,712 test, 6,492,875 train rows); 1132 to 1183 (333,081 test, 6,161,238 train rows); 1080 to 1131 (327,025 test, 5,834,640 train rows). Each test window keeps at most 500k of its rows, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows (by default rows drawn at random from the newest year before each window, extended back in time until it holds that many rows, `subsample_train`).

An era's 20-market-day target resolves about 5 weeks later: the download of 2026-10-06 has targets up to era 1235 and none for 1236-1240, so at era T the newest known target is that of era T - 5. Numerai's v5.2 notebook says to "embargo the first 4 eras following our last train era", but its code skips only 3 eras, so our gap is one era stricter. One year per window: Numerai ranks a model by its one-year average score ("Your model's reputation is just its 1 year average score", which "directly determines the rank of models on the model leaderboard", https://docs.numer.ai/numerai-tournament/scoring) and advises retraining at major data releases ("it's usually best to re-train your models when major versions are released", https://docs.numer.ai/numerai-tournament/data), so a model fit before the window predicts 52 weekly eras; participants refit anywhere from weekly to once per release (https://forum.numer.ai/t/how-often-do-you-re-train-your-model/8164). A year also holds every season. The newest window always stays, and the two before it walk back from it because the 2,376 features are v5.0's set of July 2024 (about era 1125) and Numerai builds its features with the targets of the eras it has, so an older window would test on eras that shaped the features: the three newest years lie as close to that date as three one-year windows allow, though not after it (45 of the 52 eras of the oldest window, 1080-1131, come before it). Windows that keep at least half the rows for training reach back to era 716 (51.4%); the curator kept the three newest years on 2026-11-10, 3 of the 30 splits an IID split of this size would get (SPLIT-33). Inner validation (tuning, early stopping) must be era-blocked with a 4-era gap as well: a stock's 20-day targets overlap for 3 eras, so on the newest train side a random hold-out gives LightGBM a per-era correlation of 0.040 (t 16.8), against 0.004 (t 1.1) on the last 52 train eras after a 4-era gap.

3 repeat(s) x 1 fold(s) with seed 4267; train 5,834,640 to 6,492,875 rows, test 327,025 to 361,712 rows. Prediction horizon: 52 weeks. Gap between train and test: 4 weeks. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as rows.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 6492875 | 361712 | 1 | 1179 | 1184 | 1235 |
| 1 | 0 | 6161238 | 333081 | 1 | 1127 | 1132 | 1183 |
| 2 | 0 | 5834640 | 327025 | 1 | 1075 | 1080 | 1131 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows numerai_v5_2_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | 1184 - 1235 (weeks) | 361712 | 0.944 | mean 0.4998, median 0.5, p10 0.25, p90 0.75 | mean 0.5033, median 0.5, p10 0.25, p90 0.75 | 1.278 | feature_seismologic_scant_hairpin (1.28), feature_laboring_cliquish_sensualist … | nan |
| 1 | 1132 - 1183 (weeks) | 333081 | 0.895 | mean 0.5006, median 0.5, p10 0.25, p90 0.75 | mean 0.5001, median 0.5, p10 0.25, p90 0.75 | 1.426 | feature_seismologic_scant_hairpin (1.43), feature_converse_unflinching_firm (1.… | nan |
| 2 | 1080 - 1131 (weeks) | 327025 | 0.848 | mean 0.4996, median 0.5, p10 0.25, p90 0.75 | mean 0.4996, median 0.5, p10 0.25, p90 0.75 | 1.482 | feature_seismologic_scant_hairpin (1.48), feature_transitive_cylindrical_astilb… | nan |

## Decisions

### 1. Feature-eras filled with the middle bin are set to missing

Numerai sets every stock of a feature-era without data to 2; an era in which a feature takes only that value is missing data, not a middle rank. It occurs only in the older eras (shares of the rows in this frame).

| eras | rows | share of feature values missing | features with a missing era |
|---|---|---|---|
| 1-574 | 2746268 | 0.0725824 | 1198 |
| 575-894 | 1894207 | 5.3939e-05 | 30 |
| 895-1235 | 2240806 | 0 | 0 |

## Bundle checks

0 error(s), 0 warning(s), 2 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicates_skipped`: Skipped duplicate-column/row checks: 16,363,686,218 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to run them; nothing else checks duplicate rows and columns.)
- **info** `task_metric_input_is_model_input`: The metric reads the task's group or time column(s) ['era'] where they are; they are not scoring columns.

Accepted on purpose:

- `splits_dimensions_off_protocol`: Three windows against the 30 an IID split of 1,235 eras would get (SPLIT-33): older one-year windows would test eras whose targets built the v5.0 features of July 2024, so the curator kept the three newest years on 2026-11-10. The splits comment names the target, the count reached and what stops more (SPLIT-15; Lennart, 2026-11-26).
- `task_feature_looks_like_exposure`: A false positive of the name heuristic: `feature_swept_irrespirable_grillade` is one of Numerai's 2,376 anonymised features, whose names are random words; no feature is an amount at risk (Lennart, 2026-11-26).
- `task_target_value_dominant`: The target is Numerai's within-era rank of a return, binned into five ordered levels; the middle level 0.5 holds half the rows by construction, and the task is scored by per-era correlation (Lennart, 2026-11-26).
- `task_target_low_cardinality`: The target is a continuous return that Numerai ranks within each era and bins into 5 ordered levels (0 to 1); Numerai treats it as regression (its example models are regressors scored by correlation), and so do we.

## Data checks

### Feature summary

<details>
<summary>Show the table (2,378 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| feature_seismologic_scant_hairpin | float32 | 1.1026e+06 | 16.02 | 5 | 1.0, 4.0, 0.0, 2.0, 3.0 |
| feature_abrasive_forcipate_crewel | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 4.0, 0.0, 3.0, 2.0 |
| feature_airtight_persuadable_ekaterinburg | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 0.0, 4.0, 3.0, 2.0 |
| feature_antimalarial_maungy_jinni | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 3.0, 4.0, 2.0, 0.0 |
| feature_apprentice_motivating_familiarity | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 0.0, 3.0, 1.0, 2.0 |
| feature_assentive_judgmental_tondo | float32 | 1.09629e+06 | 15.93 | 5 | 0.0, 4.0, 3.0, 2.0, 1.0 |
| feature_atherosclerotic_laming_walton | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 0.0, 4.0, 3.0, 2.0 |
| feature_augmentable_circulatory_telautography | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 3.0, 4.0, 2.0, 0.0 |
| feature_avocado_gassier_recurrence | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 0.0, 4.0, 1.0, 2.0 |
| feature_avocado_unsympathising_byrnie | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 1.0, 0.0, 2.0, 4.0 |
| feature_bared_seismological_ravine | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 2.0, 0.0, 4.0, 1.0 |
| feature_bicameral_showery_wallaba | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 2.0, 0.0, 1.0, 3.0 |
| feature_biodegradable_unreadable_infernal | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 1.0, 2.0, 4.0, 0.0 |
| feature_blessed_inevitable_rhein | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 3.0, 4.0, 0.0, 2.0 |
| feature_bulbed_dozenth_troglodytism | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 2.0, 4.0, 1.0, 0.0 |
| feature_butyric_laconical_hagiarchy | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 0.0, 3.0, 1.0, 2.0 |
| feature_called_extra_devilment | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 0.0, 1.0, 3.0, 2.0 |
| feature_celluloid_oozy_eartha | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 3.0, 4.0, 0.0, 2.0 |
| feature_chartered_urethroscopic_araby | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 3.0, 4.0, 0.0, 2.0 |
| feature_colloidal_duskier_regulator | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 3.0, 1.0, 0.0, 2.0 |
| feature_combatable_imperial_spinthariscope | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 4.0, 2.0, 0.0, 1.0 |
| feature_commiserative_psychometric_crook | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 1.0, 0.0, 2.0, 3.0 |
| feature_converse_unflinching_firm | float32 | 1.09629e+06 | 15.93 | 5 | 0.0, 4.0, 2.0, 3.0, 1.0 |
| feature_crablike_yugoslavic_buckra | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 1.0, 2.0, 0.0, 4.0 |
| feature_credal_efflorescent_confab | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 4.0, 3.0, 0.0, 2.0 |
| feature_decent_intelligible_narcoleptic | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 0.0, 2.0, 4.0, 3.0 |
| feature_defiant_jural_homochromy | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 4.0, 2.0, 1.0, 0.0 |
| feature_delineative_despairing_questioning | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 0.0, 4.0, 3.0, 2.0 |
| feature_deputy_extenuating_thiamin | float32 | 1.09629e+06 | 15.93 | 5 | 0.0, 1.0, 2.0, 4.0, 3.0 |
| feature_derived_noisemaker_treponema | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 4.0, 0.0, 2.0, 3.0 |
| feature_destroyable_paleolithic_cellulase | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 4.0, 0.0, 2.0, 3.0 |
| feature_detainable_unreprovable_ark | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 4.0, 2.0, 1.0, 0.0 |
| feature_determinate_metaleptic_corundum | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 0.0, 1.0, 2.0, 4.0 |
| feature_diapedetic_accusing_nymphet | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 0.0, 2.0, 4.0, 3.0 |
| feature_different_wilier_burweed | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 0.0, 1.0, 4.0, 2.0 |
| feature_dioptric_monarchal_beadswoman | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 0.0, 3.0, 2.0, 1.0 |
| feature_doggiest_ledgiest_gingelly | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 3.0, 0.0, 4.0, 2.0 |
| feature_driven_retrogressive_vibration | float32 | 1.09629e+06 | 15.93 | 5 | 0.0, 3.0, 4.0, 1.0, 2.0 |
| feature_easy_bentham_origanum | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 2.0, 4.0, 0.0, 1.0 |
| feature_ectomorphic_plump_indisposition | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 0.0, 1.0, 2.0, 3.0 |
| feature_elaborative_autarkic_phrygian | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 0.0, 1.0, 4.0, 2.0 |
| feature_emulative_bacilliform_arezzo | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 3.0, 2.0, 0.0, 4.0 |
| feature_etruscan_unborne_garibaldi | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 3.0, 2.0, 1.0, 0.0 |
| feature_exhausting_cunning_bier | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 4.0, 0.0, 1.0, 2.0 |
| feature_explorative_pronephric_hitchcock | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 0.0, 1.0, 2.0, 4.0 |
| feature_farther_sightable_camerlengo | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 4.0, 2.0, 0.0, 1.0 |
| feature_fitchy_stricken_detoxicant | float32 | 1.09629e+06 | 15.93 | 5 | 0.0, 4.0, 2.0, 3.0, 1.0 |
| feature_fitful_willyard_kaon | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 3.0, 1.0, 2.0, 0.0 |
| feature_gaited_metagrabolized_thiamine | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 3.0, 0.0, 4.0, 2.0 |
| feature_gamiest_free_harmonica | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 3.0, 2.0, 1.0, 0.0 |
| feature_grenada_steadying_pycnidium | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 0.0, 4.0, 2.0, 3.0 |
| feature_gristlier_aperient_notability | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 4.0, 2.0, 3.0, 0.0 |
| feature_hardy_upsetting_luncheonette | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 0.0, 3.0, 2.0, 1.0 |
| feature_heraclidan_counterbalancing_highlighting | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 1.0, 2.0, 4.0, 0.0 |
| feature_hithermost_flinty_antagonist | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 3.0, 0.0, 1.0, 2.0 |
| feature_immiscible_sloshiest_rosenberg | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 1.0, 2.0, 3.0, 0.0 |
| feature_imported_piscicultural_northward | float32 | 1.09629e+06 | 15.93 | 5 | 1.0, 3.0, 4.0, 0.0, 2.0 |
| feature_joking_uncongenial_globule | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 4.0, 1.0, 2.0, 0.0 |
| feature_laboring_cliquish_sensualist | float32 | 1.09629e+06 | 15.93 | 5 | 3.0, 0.0, 2.0, 4.0, 1.0 |
| feature_largish_unqualifying_incompatibility | float32 | 1.09629e+06 | 15.93 | 5 | 4.0, 1.0, 0.0, 3.0, 2.0 |

(2,318 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 5.02 | -0.002 | -0.499 | 0.05 | 0.024 | log1p | 808521 | 3.97975e+06 | exponential |

### Numeric features

<details>
<summary>Show the table (2,378 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| era | 688128 | 670.657 | 348.412 | 1 | 1235 |
| target_ender_20 | 688128 | 0.499881 | 0.223656 | 0 | 1 |
| feature_abessive_philistine_camisado | 688128 | 1.99777 | 1.41465 | 0 | 4 |
| feature_able_deprived_nona | 688128 | 1.99794 | 1.41342 | 0 | 4 |
| feature_ablest_inflexional_egeria | 672495 | 1.99981 | 1.41505 | 0 | 4 |
| feature_abrasive_forcipate_crewel | 578858 | 1.99946 | 1.41449 | 0 | 4 |
| feature_absonant_wintry_hiring | 688128 | 2.0024 | 1.41447 | 0 | 4 |
| feature_absorbable_hyperalgesic_mode | 688128 | 2.00003 | 1.41564 | 0 | 4 |
| feature_absorbing_pluviometrical_technocrat | 653072 | 1.99788 | 1.41452 | 0 | 4 |
| feature_accadian_pledged_bore | 608172 | 2.00272 | 1.41488 | 0 | 4 |
| feature_accepted_unviable_fruitage | 688128 | 2.0002 | 1.41361 | 0 | 4 |
| feature_acclamatory_draconian_view | 688128 | 1.99946 | 1.41455 | 0 | 4 |
| feature_according_tied_bedlam | 629033 | 2.00028 | 1.41548 | 0 | 4 |
| feature_accostable_ambulatory_overcompensation | 688128 | 1.99884 | 1.41461 | 0 | 4 |
| feature_accosted_strengthened_displeasure | 688128 | 2.00253 | 1.41526 | 0 | 4 |
| feature_accountable_uninhabitable_reunion | 667237 | 2.00033 | 1.41492 | 0 | 4 |
| feature_accoutered_revolute_vexillology | 688128 | 2.00293 | 1.41281 | 0 | 4 |
| feature_accrued_groutier_lodestar | 676915 | 2.00155 | 1.41571 | 0 | 4 |
| feature_acetabular_citatory_bumper | 688128 | 2.00278 | 1.41521 | 0 | 4 |
| feature_acetose_crackerjack_needlecraft | 688128 | 1.9997 | 1.41501 | 0 | 4 |
| feature_acetose_permeated_irregular | 681758 | 2.00183 | 1.41467 | 0 | 4 |
| feature_acheulian_conserving_output | 600352 | 2.00135 | 1.41455 | 0 | 4 |
| feature_acheulian_constrainable_ahriman | 672857 | 2.0012 | 1.41518 | 0 | 4 |
| feature_acknowledged_anteorbital_bilker | 608172 | 2.0017 | 1.41439 | 0 | 4 |
| feature_acronychal_bilobate_stevenage | 688128 | 1.99939 | 1.41423 | 0 | 4 |
| feature_acrylic_gallic_wine | 650972 | 1.99969 | 1.41424 | 0 | 4 |
| feature_acrylic_pacifying_purification | 688128 | 2.00384 | 1.41545 | 0 | 4 |
| feature_active_yclept_hydrometallurgy | 688128 | 1.99932 | 1.4161 | 0 | 4 |
| feature_adaptative_nasal_monastery | 681758 | 2.00092 | 1.41405 | 0 | 4 |
| feature_adjudicative_unkissed_exotic | 669807 | 2.0016 | 1.41455 | 0 | 4 |
| feature_adminicular_shod_levant | 688128 | 2.00135 | 1.4143 | 0 | 4 |
| feature_admonished_municipal_bletting | 683463 | 2.00229 | 1.41439 | 0 | 4 |
| feature_adorable_infernal_cartesianism | 688128 | 1.99905 | 1.41411 | 0 | 4 |
| feature_adorable_unsuitable_cholecystectomy | 688128 | 2.00062 | 1.41412 | 0 | 4 |
| feature_adsorbed_rebuttable_imitator | 688128 | 1.99913 | 1.41524 | 0 | 4 |
| feature_adsorbent_rebel_atony | 600352 | 2.0011 | 1.41446 | 0 | 4 |
| feature_adunc_cosmogonical_radiobiology | 653072 | 2.00172 | 1.4147 | 0 | 4 |
| feature_advertent_deferent_kaif | 688128 | 1.99946 | 1.41533 | 0 | 4 |
| feature_advised_subdural_toadflax | 688128 | 1.99978 | 1.41408 | 0 | 4 |
| feature_advocatory_unfathered_utricle | 650303 | 1.99737 | 1.41418 | 0 | 4 |
| feature_aeneolithic_nineteenth_whipper | 688128 | 1.99798 | 1.4138 | 0 | 4 |
| feature_aerobic_contrapuntal_memento | 653072 | 1.99708 | 1.41357 | 0 | 4 |
| feature_aerobiological_occultist_flophouse | 629033 | 2.00066 | 1.41363 | 0 | 4 |
| feature_aerological_untested_granulator | 672495 | 1.99948 | 1.41453 | 0 | 4 |
| feature_aery_restrainable_thai | 688128 | 1.99976 | 1.41453 | 0 | 4 |
| feature_afferent_splenic_rosaniline | 688128 | 2.00372 | 1.41331 | 0 | 4 |
| feature_affettuoso_revealing_miscellanist | 688128 | 1.99947 | 1.41408 | 0 | 4 |
| feature_affinitive_tinier_southernism | 653072 | 1.99915 | 1.41372 | 0 | 4 |
| feature_afoul_drainable_cateran | 688128 | 1.99909 | 1.41438 | 0 | 4 |
| feature_agamid_yuletide_physiology | 688128 | 1.99994 | 1.41375 | 0 | 4 |
| feature_aged_steely_eve | 688128 | 2.00368 | 1.41496 | 0 | 4 |
| feature_agentive_argyle_kail | 672857 | 2.00279 | 1.41486 | 0 | 4 |
| feature_aggregate_biliteral_enceinte | 688128 | 1.99925 | 1.41528 | 0 | 4 |
| feature_agronomical_gamic_fremantle | 688128 | 2.00245 | 1.41501 | 0 | 4 |
| feature_ailurophobic_boggy_trocar | 688128 | 2.0023 | 1.41529 | 0 | 4 |
| feature_aired_temptable_murmansk | 650972 | 2.00057 | 1.41526 | 0 | 4 |
| feature_airtight_persuadable_ekaterinburg | 578858 | 1.99835 | 1.41434 | 0 | 4 |
| feature_airworthy_sweetish_interpolater | 688128 | 1.99993 | 1.4145 | 0 | 4 |
| feature_airy_fecund_disgrace | 653072 | 1.99908 | 1.41391 | 0 | 4 |
| feature_akkadian_beerier_pentameter | 653072 | 1.99848 | 1.41434 | 0 | 4 |

(2,318 more rows not shown)

</details>

### Categorical features

No categorical/object features to summarize.

## Build

| field | value |
|---|---|
| uuid | 01a218ca-2052-7ea4-b72c-31e63d9ade2b |
| checksum | v2:1672385d846098a33013cb30c7b54a877f1e955d524c8a4fcf66a8baa47c364f |
| built_at | 2026-11-26T17:10:34+00:00 |
| path | numerai_v5_2_1m/01a218ca-2052-7ea4-b72c-31e63d9ade2b |
| data_foundry_version | 0.0.5 |
| git_sha | 0d939f6d218cce0b083c3474f78e93095b5804d0-dirty |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
