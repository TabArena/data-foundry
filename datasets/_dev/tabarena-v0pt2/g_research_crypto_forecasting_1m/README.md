---
report_format: data-foundry-report-v2
unique_name: g_research_crypto_forecasting_1m
container_format: 2
checksum: v2:2ed9741894f7fd1ec6fdd1716fc62bb3ec0ea922ecbc947c9506a428388bc42d
build:
  uuid: 01a217f5-dcae-71fb-b705-cf84808b184a
  checksum: v2:2ed9741894f7fd1ec6fdd1716fc62bb3ec0ea922ecbc947c9506a428388bc42d
  built_at: '2026-11-26T13:14:35+00:00'
  path: g_research_crypto_forecasting_1m/01a217f5-dcae-71fb-b705-cf84808b184a
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
  n_rows: 24670766
  n_features: 27
  dtypes:
    category: 1
    datetime64[ns]: 1
    float64: 27
  n_test_dataset_rows: null
task:
  target: Target
  problem_type: regression
  metric: weighted_pearsonr
  metric_origin: source
  scoring_columns:
  - Weight
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
  time_horizon: 91
  time_horizon_unit: days
  time_gap: 15
  time_gap_unit: minutes
  reason: 'The competition scored every submitted model, frozen after training, on
    the 3 months of live data after its submission deadline (2 February to 3 May 2022);
    no source gives a production refit cadence, so a window is those 91 days (the
    horizon checked by Lennart on 2026-11-11). We use three windows of 91 days as
    test windows and all earlier data as train data, with a 15-minute gap, the minimum
    and the target''s own horizon: a row''s target needs the Close 16 minutes later,
    so the newest training label is known at the close of the window''s first minute,
    when the first test prediction is made (Lennart, 2026-10-22; against a 1-day gap
    the weighted Pearson moves by -0.0003 on average, inside the seed noise, on the
    windows of train.csv). The windows (Lennart, 2026-11-11) test three markets a
    model that trades every minute has to hold in: the newest, 25 October 2021 to
    23 January 2022, the falling market after Bitcoin''s peak of 10 November 2021
    and the deployment period (it holds the 99 EOS.IO bars of 26-27 October 2021 with
    a Low near 1.09 against a price near 4.8, kept as the release gives them, see
    the notes); the bull run of 22 December 2020 to 22 March 2021 (Bitcoin +138%),
    with the widest target spread; and the quiet market of 28 February to 28 May 2020
    (59 trades a coin-minute at the median against 243 in the bull run), with the
    largest crash in the data, Bitcoin''s -39% on 12 March 2020. The three newest
    windows tested before (from 25 October, 26 July and 26 April 2021) put two in
    the busy market of 2021 and none in a quiet one. The crash window trains on less
    than half the rows (48.25%), signed off by Lennart on 2026-11-11 beside the two
    on 69.2% and 93.0% and kept as the curator''s exception (Andrej, 2026-11-19).
    The windows are 91 days because the competition scored frozen models on three
    months of live data; no length lifts the crash window above half, since a window''s
    train side is everything before its start and half the rows lie after 24 March
    2020, after the crash of 12 March. Each window keeps at most 500k of its rows,
    and each train side holds every earlier row, which a benchmark sub-samples to
    1M before a fit, by default from the newest year before the window (`subsample_train`);
    both draw whole minutes at random (every asset of a drawn minute kept), as the
    target and the features are relative to the 14-asset market at each minute. Rows
    of one asset a few minutes apart share most of their 15-minute target window (per
    asset, targets 5 minutes apart correlate with a median of 0.57, range 0.25-0.66,
    in train.csv), so validation inside a train side has to split by time blocks,
    not rows: LightGBM early-stopped on random rows of the train side stops after
    220-528 rounds and scores test R^2 -0.0049, -0.0043 and -0.0090, against +0.0006,
    +0.0013 and +0.0004 when it stops on the newest 10% (random-row train sides, 1-day
    gap).'
  n_train:
    min: 12545715
    max: 24170779
  n_test:
    min: 499987
    max: 499996
  row_budget:
    train: 1000000
    test: 500000
  train_sampling:
    default: newest_year
    unit: time_values
    stratify_on: null
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicates_skipped
  accepted:
    task_metric_weight_without_sample_weight: The asset's Weight is a function of
      Asset_Name, a feature, so MET-15 needs no sample weight (2026-11-06). Training
      with it moved the weighted Pearson by +0.0026 on average, within the spread
      across the three windows that ended on 20 September 2021 (SD 0.0023, t about
      1.96 on 2 df); only the newest window's interval excludes 0 (+0.0050 [+0.0005,
      +0.0099]).
    splits_train_under_half: 'Signed off (Lennart, 2026-11-11): the window of the
      2020 crash (from 28 February 2020) trains on 48.25% of the rows, beside 93.0%
      and 69.2%; kept as the curator''s exception (Andrej, 2026-11-19).'
decisions:
- Temporal split over the same 14 assets, not grouped by asset
- History features from the 3rd-place solution carry the signal
---

# g_research_crypto_forecasting_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `Target`, scored with `weighted_pearsonr` on temporal splits by `timestamp`. 24,670,766 rows and 27 features. Source: Kaggle (2021).

Built as `01a217f5-dcae-71fb-b705-cf84808b184a` on 2026-11-26. See [Build](#build).

## In brief

**Question.** How will a cryptocurrency's price move over the next 15 minutes, compared with the market?

**Use case.** At the close of each minute, a trading firm forecasts each coin's return over the next 15 minutes relative to the market, to decide its positions (the G-Research competition).

**One row.** One coin at one minute: 14 cryptocurrencies, January 2018 to January 2022.

**Predicted.** The coin's return from one to 16 minutes ahead, minus the part that follows the market's return (a weighted mean of the 14 coins); values sit close to zero.

**Known at prediction time.** The coin and the minute, the minute's trading summary (open, high, low and close prices, volume, average price, number of trades) and the price trends of the past hour, 5 hours and 15 hours, for the coin and for the market.

**What the test data stands for.** Three test windows of 91 days: the newest (25 October 2021 to 23 January 2022), the bull run of early 2021 and the quiet market of 2020 with its crash; training is all earlier history with a 15-minute gap, from which a benchmark draws about a million coin-minute rows as whole minutes (all coins of a minute) from the newest year.

**Our changes to the source.** We add the price-trend features of the third-place solution, as the minute itself carries no signal, and drop the minutes without a target.

> **Use case fit: direct (the rows, features and split mirror the use case).** Everything the model sees is known at the minute and the target covers the next 15 minutes, as in trading. On the earlier windows to 20 September 2021, a 12-seed LightGBM ensemble scored +0.039, +0.033 and +0.021 by the weighted Pearson correlation and led the coin's mean in all three, clearly in two; it is to be measured again on the windows tested now.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/g_research_crypto_forecasting.md`](../../../../curation/records/g_research_crypto_forecasting.md)
- The original source: <https://www.kaggle.com/competitions/g-research-crypto-forecasting>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/g_research_crypto_forecasting/`. To get them:

```text
We download three files of the Kaggle competition (accept its rules on Kaggle first). The files were last updated on 2022-01-26; train.csv has 24,236,806 rows and supplemental_train.csv 2,518,278.

kaggle competitions download -c g-research-crypto-forecasting -f train.csv -p local-data-warehouse/g_research_crypto_forecasting
kaggle competitions download -c g-research-crypto-forecasting -f supplemental_train.csv -p local-data-warehouse/g_research_crypto_forecasting
kaggle competitions download -c g-research-crypto-forecasting -f asset_details.csv -p local-data-warehouse/g_research_crypto_forecasting
cd local-data-warehouse/g_research_crypto_forecasting && unzip train.csv.zip && unzip supplemental_train.csv.zip && rm train.csv.zip supplemental_train.csv.zip
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/g_research_crypto_forecasting_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/g_research_crypto_forecasting_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/competitions/g-research-crypto-forecasting |
| year | 2021 |
| domain | finance |
| license | Kaggle Competition Rules (data access and use: competition use only) |
| data_tags | Non-IID, Temporal |
| reference | GResearchCryptoForecasting2021 |
| rows x columns | 24,670,766 x 29 |
| task.target | Target |
| task.problem_type | regression |
| task.metric | weighted_pearsonr |
| task.split_regime | temporal_non_iid |
| task.time_on | timestamp |

**Metric**

| field | value |
|---|---|
| name | `weighted_pearsonr` (custom; takes value; higher is better) |
| origin | source: the source's metric |
| original | weighted version of the Pearson correlation coefficient |
| reference | https://www.kaggle.com/competitions/g-research-crypto-forecasting/overview/evaluation |
| definition | Pearson correlation of Target and the prediction over all test rows, each row weighted by its asset's Weight |
| inputs | weight: `Weight` |

**Scoring columns**

Kept in the frame for the metric; do not use them as features. Drop them from the inputs (`feature_columns(container)`), then pass the test rows' values to the scorer (`data_foundry.metrics.scorer(container)(y_test, y_pred, test_idx)`).

| column | role | how the metric uses it | model input |
|---|---|---|---|
| `Weight` | weight | weighted_pearsonr: the asset's weight from asset_details.csv (Bitcoin 6.78 ... IOTA and Maker 1.10), mapped from Asset_Name; each row is weighted by it in the Pearson correlation. Asset_Name stays a feature. | never a feature |

The test-row values of `Weight` are for the scorer only: never read them when predicting a test row.

<details>
<summary>Feature types: 1 categorical, 0 string, 1 datetime</summary>

- categorical (1): `Asset_Name`
- string (0): none
- datetime (1): `timestamp`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{GResearchCryptoForecasting2021,
  author = {Alessandro Ticchi and Andrew Scherer and Carla McIntyre and Carlos Stein N Brito and Derek Snow and Develra and dstern and James Colless and Kieran Garvey and Maggie and Maria Perez Ortiz and Ryan Lynch and Sohier Dane},
  title = {G-Research Crypto Forecasting},
  year = {2021},
  howpublished = {\url{https://kaggle.com/competitions/g-research-crypto-forecasting}},
  note = {Kaggle competition}
}
```

</details>

## Sample rows

The first 5 of 24,670,766 rows of the final frame (the oldest rows: the frame is sorted by `timestamp`); 12 of 29 columns, the target first. Cells are cut at 40 characters.

| Target | timestamp | Asset_Name | Count | Open | High | Low | Close | Volume | VWAP | log_close_to_mean_60 | market_log_close_to_mean_60 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| -0.0048086 | 2018-01-01 00:01:00 | Ethereum | 173 | 738.303 | 746 | 732.51 | 738.508 | 335.988 | 738.839 | nan | nan |
| -0.00826351 | 2018-01-01 00:01:00 | Ethereum Classic | 5 | 25.92 | 25.92 | 25.874 | 25.877 | 121.087 | 25.8914 | nan | nan |
| -0.00979142 | 2018-01-01 00:01:00 | Litecoin | 167 | 225.33 | 227.78 | 222.98 | 225.207 | 411.897 | 225.198 | nan | nan |
| -0.0139224 | 2018-01-01 00:01:00 | EOS.IO | 32 | 7.6596 | 7.6596 | 7.6567 | 7.6576 | 6626.71 | 7.65771 | nan | nan |
| -0.0146432 | 2018-01-01 00:01:00 | Bitcoin | 229 | 13835.2 | 14013.8 | 13666.1 | 13850.2 | 31.5501 | 13827.1 | nan | nan |

## Curation notes

We start with train.csv (one row per asset and minute, 14 cryptocurrencies, 2018-01-01 to 2021-09-21), supplemental_train.csv (the same, 2021-09-21 00:01 to 2022-01-24) and asset_details.csv of the Kaggle competition.

- The newer months (Lennart, 2026-11-11): supplemental_train.csv continues train.csv minute by minute from 21 September 2021 00:01 to 24 January 2022 00:00 (2,518,278 rows, the same 14 assets and columns, no (timestamp, asset) pair in both; Bitcoin closes at 43,002.5 on the last minute of train.csv and at 42,947.1 on the first of the file). We append it: these are the release's newest months, the period closest to the competition's own scoring of the frozen models (2 February to 3 May 2022), and the newest test window stands for deployment. Together the files hold 26,755,084 rows. The history features are built on both files at once, so their look-back windows run across the seam. The release's other files are left out: example_test.csv and example_sample_submission.csv show the format of the live API (a few rows, no target), and gresearch_crypto/ is the API's code.
- Prediction point: at the close of minute t we predict an asset's `Target`, its return from minute t+1 to t+16 minus its beta times the weighted mean return of the 14 assets (the organisers' tutorial notebook). Known then: every one-minute bar of the 14 assets up to and including minute t.
- Scope: the target is the asset's own residualised forward return, and its signal is the asset's trailing return relative to the 14-asset mean. The bar alone, the asset's own lags alone and the market means alone carry none (LightGBM on each set, three test windows). The curator keeps it as a forecasting-like panel under the amended TP-10 (Lennart, 2026-10-22). Leg 1, measured by the declared metric: early-stopped LightGBM scores weighted Pearson +0.040, +0.052 and +0.045 in the three windows (95% day-block intervals [+0.023, +0.063], [+0.036, +0.070], [+0.027, +0.063]), and its lead over the asset's mean (the naive forecast: -0.002, +0.007, +0.008) excludes 0 in every window (random-row train sides, 1-day gap; superseded 2026-11-06: on the splits shipped then, train sides of 1M whole minutes from all history and a 15-minute gap, the 12-seed ensemble, which averages the 12 models' predictions and leaves out `timestamp`, scores +0.0388 [+0.0205, +0.0623], +0.0333 [+0.0103, +0.0585] and +0.0206 [-0.0050, +0.0496] (a single model +0.0368, +0.0294 and +0.0199), its lead over the coin's mean +0.0384 [+0.0182, +0.0631], +0.0418 [+0.0138, +0.0699] and +0.0231 [-0.0060, +0.0537], +0.034 pooled over the three windows (SE about 0.008), positive on 75, 75 and 77 of 91 days: the oldest window's lead no longer excludes 0). Leg 1 still holds (CC 2026-11-08, Lennart): the model is ahead of the coin's mean in every window by its point estimate, and the interval is read pooled, as for ashrae_great_energy_predictor_iii and rain_in_australia. These figures come from the windows that ended on 20 September 2021, before the newer months were added (2026-11-11); they are to be measured again (the 12-seed ensemble against the coin's mean, day-block intervals) on the windows chosen on 2026-11-11, from 25 October 2021, 22 December 2020 and 28 February 2020, which has not been run yet. Leg 2: the top three solutions are LightGBM on point-in-time features (G-Research's wrap-up), and no feature is a lag of the `Target` column; the relative returns are built from Close and correlate 0.80-0.83 (median over the 14 assets) with sums of the asset's lagged `Target`.
- History features (`history_features`): a row's own bar carries no signal for the next 15 minutes (a LightGBM prediction from the bar correlates -0.002, 0.005 and 0.010 with the target in the three test windows of train.csv, measured in October 2026), so we add the features of the 3rd-place solution: the public notebook "Training 3rd place solution" (sugghi), which Kaggle's write-up record for the 3rd place lists as sugghi's (sole author, team GABA); it uses Close only and trains from 12 January 2019. For 60, 300 and 900 minutes: the log of Close over its trailing mean and the log return, their mean over the assets (`market_*`) and the asset's difference from it (`*_minus_market`). With them the correlation is 0.026, 0.059 and 0.049.
- The 18 features stay after a comparison with the other top solutions (CLEAN-19; Lennart, 2026-10-22): the 2nd place withholds its features (LightGBM on squared loss) and the 1st place has no write-up; lower places add a 15-minute look-back, volume and volatility, technical indicators, the hour, and other coins' returns. Added to the 18 (LightGBM, mean of 2 seeds, change in weighted Pearson in the three windows; random-row train sides, 1-day gap, 2026-10-22): a 15-minute look-back -0.001, -0.001, -0.002; volume and volatility +0.003, +0.004, -0.005; other coins' 15- and 60-minute returns -0.005, -0.013, -0.007; bar shape and time -0.007, -0.007, -0.004. None helps in all three windows.
- We compute the features on the full minute grid before dropping rows. A missing minute takes the asset's last Close for at most 100 minutes (as in the notebook). A trailing mean reaching into a longer gap or before the asset's first minute is missing; a log return checks only its end point, so 193, 1,804 and 9,370 values (60, 300 and 900 minutes) span a longer gap, as in the notebook (all before the newer months, which add none).
- We drop the 753,261 rows (2.8%) without a target, 750,338 of train.csv and 2,923 of supplemental_train.csv: Close(t+1) or Close(t+16) is missing (37% lack only Close(t+1)), and the competition does not score them. 308 of them have both closes and still no target in the file, 224 of these train.csv's last 16 minutes, whose Close(t+16) lay past its end; we do not recompute the host's target. Their bars still enter the history features.
- We replace `Asset_ID` by the asset's name from asset_details.csv (`Asset_Name`, category); its `Weight` in asset_details.csv, the asset's weight in the metric, ships as a scoring column and is not a feature.
- `VWAP` is a positive price and `Volume` a traded amount: we set the infinite and negative VWAP values (13 rows of the frame, 15 of the raw files, all Maker, June 2020) and the negative Volume values (2 rows of the frame, 3 raw, Maker) to missing; supplemental_train.csv has none of either.
- We convert `timestamp` (Unix seconds) to a datetime.
- Anomaly: 117 bars of the frame (119 raw) have a `Low` below half of their open and close and 3 raw bars a `High` above twice, and 271 targets exceed 0.2 in absolute value (mostly Bitcoin Cash around its November 2018 fork). In train.csv these are 16 bars of the frame (18 raw) and 266 targets, which we keep as unusual but real. The newer months add 101 of the low bars, 99 of them EOS.IO on 26-27 October 2021, where its Low sits near 1.09 against a price near 4.8 and its Close jumps between about 4.8 and 4.0 from minute to minute; EOS.IO holds 85 of the 126 targets above 0.1 in absolute value in the newest window, and these two days 3.7% of that window's weighted target variance. We keep them as the release gives them. No (timestamp, asset) pair repeats.
- Temporal, not grouped by asset: the competition forecasts the same 14 assets on later data; a split by asset would only test a shift between 14 assets (decision table).
- History: each train side is all earlier history back to 2018 (minus the 15-minute gap), and a benchmark sub-samples it to the 1M budget as whole minutes (every asset of a drawn minute kept, `sample_by="time"`), by default at random from the newest year before the window (`subsample_train`); SPLIT-20 reason (Lennart, 2026-10-22): the target and the features are relative to the 14-asset market at each minute, and random rows left about 1.3 assets per minute. Measured at the 1M budget (weighted Pearson, mean of 3 seeds, windows 1, 2, 3; on 2026-10-22, on the test rows then shipped, drawn as random rows, with a 1-day gap): whole minutes over all history .041, .046, .045; random rows over all history .042, .045, .043; the newest 1M rows (50 days) .036, .045, .007; the newest year, now the default, is not among these runs. A recent cut swings by window and collapses in the third; the 2nd place found that longer history kept helping and trained on all of it. On the windows that ended on 20 September 2021, the two older test windows (2020-12-22 to 2021-06-21) fell in the 2021 high-volatility regime (median absolute 900-minute return 0.029-0.036, against 0.013-0.022 in every quarter of 2019-2020). With the newer months the test windows are the newest (25 October 2021 to 23 January 2022), the 2021 bull run (22 December 2020 to 22 March 2021) and the quiet market of 2020 with its crash (28 February to 28 May 2020), chosen by Lennart on 2026-11-11 in place of the three newest, of which the two older ones repeated the busy market of 2021.
- Metric: the competition's weighted Pearson correlation, each row weighted by its asset's `Weight` (Bitcoin 6.78 ... IOTA and Maker 1.10). It replaces the pooled `pearsonr` declared before as its stand-in, which ranked seven predictions per window as the weighted correlation does (Kendall tau 1.0).
- Training weight (MET-15, 2026-11-06): none. `Weight` is a function of `Asset_Name`, which the model sees, so MET-15 needs no sample weight: a weight that is a function of the features leaves the best squared-error prediction of each row unchanged. Fitting with it as the sample weight (and in the validation loss) moved the weighted Pearson by +0.0045, +0.0034 and +0.0001 in the three windows that ended on 20 September 2021 (mean of 12 seeds; better in 25 of 36 window-seed pairs; +0.0010 with a fixed 50 rounds instead of early stopping, every interval including 0), within the spread across windows (mean +0.0026, SD 0.0023, t about 1.96 on 2 df); only the newest window's interval excludes 0 (12-seed ensembles, +0.0050 [+0.0005, +0.0099], 95% day-block interval).
- Note: the task probes flag no_signal, drift_baseline and unstable (untuned models, scored by R^2; by the declared weighted Pearson their LightGBM scores 0.028, the linear model 0.023 and the dummy 0, mean of the 3 splits that ended on 20 September 2021). LightGBM (learning rate 0.05, 31 leaves, at least 200 rows per leaf) early-stopped on the newest 10% of each train side reaches R^2 +0.0008, +0.0008 and -0.0023 on the splits shipped on 2026-11-06 (train sides of 1M whole minutes from all history; mean of 4 seeds; their ensemble +0.0010 [-0.0002, +0.0026], +0.0009 [+0.0001, +0.0017] and -0.0019 [-0.0046, +0.0011], 95% day-block intervals, only the middle window's excluding 0). Under the declared weighted Pearson the same signal is clear in the two newer windows and pooled over the three (Scope bullet); drift_baseline comes from a target centred on zero.
- The row budget: each test window keeps at most 500k of its rows, drawn at random as whole minutes (every asset of a drawn minute kept), and each train side holds every earlier row (minus the 15-minute gap); the frame keeps every row a split uses. The 1M train budget is recorded, not applied: a benchmark sub-samples each train side to 1M rows before a fit with `subsample_train`, by default whole minutes drawn at random from the newest year before the window. The full frame has 26,001,823 rows (14 assets, one row per minute, 2018-01-01 to 2022-01-23 23:44; 23,486,468 of them from train.csv).

## Splits

Expanding-window temporal splits: 3 test window(s) of 91 days, starting at 2021-10-25, 2020-12-22, 2020-02-28, newest first; train is all earlier data up to a gap of 15 minutes. The test windows by `timestamp`, as listed: 2021-10-25 to 2022-01-23 (499,987 test, 24,170,779 train rows); 2020-12-22 to 2021-03-22 (499,990 test, 17,985,995 train rows); 2020-02-28 to 2020-05-28 (499,996 test, 12,545,715 train rows). Each test window keeps at most 500k of its rows, drawn as whole values of `timestamp`; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows (by default whole values of the time column drawn at random from the newest year before each window, extended back in time until it holds that many rows, `subsample_train`).

The competition scored every submitted model, frozen after training, on the 3 months of live data after its submission deadline (2 February to 3 May 2022); no source gives a production refit cadence, so a window is those 91 days (the horizon checked by Lennart on 2026-11-11). We use three windows of 91 days as test windows and all earlier data as train data, with a 15-minute gap, the minimum and the target's own horizon: a row's target needs the Close 16 minutes later, so the newest training label is known at the close of the window's first minute, when the first test prediction is made (Lennart, 2026-10-22; against a 1-day gap the weighted Pearson moves by -0.0003 on average, inside the seed noise, on the windows of train.csv). The windows (Lennart, 2026-11-11) test three markets a model that trades every minute has to hold in: the newest, 25 October 2021 to 23 January 2022, the falling market after Bitcoin's peak of 10 November 2021 and the deployment period (it holds the 99 EOS.IO bars of 26-27 October 2021 with a Low near 1.09 against a price near 4.8, kept as the release gives them, see the notes); the bull run of 22 December 2020 to 22 March 2021 (Bitcoin +138%), with the widest target spread; and the quiet market of 28 February to 28 May 2020 (59 trades a coin-minute at the median against 243 in the bull run), with the largest crash in the data, Bitcoin's -39% on 12 March 2020. The three newest windows tested before (from 25 October, 26 July and 26 April 2021) put two in the busy market of 2021 and none in a quiet one. The crash window trains on less than half the rows (48.25%), signed off by Lennart on 2026-11-11 beside the two on 69.2% and 93.0% and kept as the curator's exception (Andrej, 2026-11-19). The windows are 91 days because the competition scored frozen models on three months of live data; no length lifts the crash window above half, since a window's train side is everything before its start and half the rows lie after 24 March 2020, after the crash of 12 March. Each window keeps at most 500k of its rows, and each train side holds every earlier row, which a benchmark sub-samples to 1M before a fit, by default from the newest year before the window (`subsample_train`); both draw whole minutes at random (every asset of a drawn minute kept), as the target and the features are relative to the 14-asset market at each minute. Rows of one asset a few minutes apart share most of their 15-minute target window (per asset, targets 5 minutes apart correlate with a median of 0.57, range 0.25-0.66, in train.csv), so validation inside a train side has to split by time blocks, not rows: LightGBM early-stopped on random rows of the train side stops after 220-528 rounds and scores test R^2 -0.0049, -0.0043 and -0.0090, against +0.0006, +0.0013 and +0.0004 when it stops on the newest 10% (random-row train sides, 1-day gap).

3 repeat(s) x 1 fold(s) with seed 4267; train 12,545,715 to 24,170,779 rows, test 499,987 to 499,996 rows. Prediction horizon: 91 days. Gap between train and test: 15 minutes. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as whole time values.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 24170779 | 499987 | 2018-01-01 00:01:00 | 2021-10-24 23:44:00 | 2021-10-25 00:02:00 | 2022-01-23 23:44:00 |
| 1 | 0 | 17985995 | 499990 | 2018-01-01 00:01:00 | 2020-12-21 23:44:00 | 2020-12-22 00:01:00 | 2021-03-22 23:58:00 |
| 2 | 0 | 12545715 | 499996 | 2018-01-01 00:01:00 | 2020-02-27 23:44:00 | 2020-02-28 00:02:00 | 2020-05-28 23:57:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows g_research_crypto_forecasting_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Oct 2021 - Jan 2022 | 499987 | 0.98 | mean -2.192e-05, median -5.098e-05, p10 -0.003, p90 0.002822 | mean -7.098e-06, median -4.707e-05, p10 -0.004181, p90 0.004149 | 1.275 | High (1.27), Open (1.27), Close (1.27) | 0 |
| 1 | Dec 2020 - Mar 2021 | 499990 | 0.729 | mean -5.533e-05, median -0.0002074, p10 -0.005497, p90 0.005417 | mean -1.929e-05, median -1.761e-05, p10 -0.003995, p90 0.004047 | 0.997 | Count (1.00), High (0.44), Close (0.44) | 0 |
| 2 | Feb 2020 - May 2020 | 499996 | 0.509 | mean -5.767e-05, median -2.047e-05, p10 -0.003282, p90 0.003254 | mean 2.524e-05, median -3.87e-05, p10 -0.004382, p90 0.00445 | 0.166 | High (0.17), Open (0.16), Close (0.16) | 0 |

## Decisions

### 1. Temporal split over the same 14 assets, not grouped by asset

The competition forecasts the 14 assets on later data. The assets enter the data at different times, and a row has no target when the asset's Close one or 16 minutes later is missing (rows of the two raw files).

| asset | first_minute | rows | share_without_target |
|---|---|---|---|
| Binance Coin | 2018-01-01 00:01:00 | 2122479 | 0.0064 |
| Bitcoin | 2018-01-01 00:01:00 | 2136278 | 0.0001 |
| Bitcoin Cash | 2018-01-01 00:01:00 | 2133518 | 0.0023 |
| Cardano | 2018-04-17 09:11:00 | 1971857 | 0.0095 |
| Dogecoin | 2019-04-12 14:34:00 | 1336832 | 0.1085 |
| EOS.IO | 2018-01-01 00:01:00 | 2135134 | 0.0011 |
| Ethereum | 2018-01-01 00:01:00 | 2136196 | 0.0002 |
| Ethereum Classic | 2018-01-01 00:01:00 | 2131118 | 0.0044 |
| IOTA | 2018-05-09 08:07:00 | 1771920 | 0.1091 |
| Litecoin | 2018-01-01 00:01:00 | 2136025 | 0.0003 |
| Maker | 2018-05-10 15:21:00 | 849379 | 0.0496 |
| Monero | 2018-01-01 00:01:00 | 1881113 | 0.1275 |
| Stellar | 2018-02-16 23:53:00 | 1958741 | 0.0316 |
| TRON | 2018-02-06 21:37:00 | 2054494 | 0.0103 |

### 2. History features from the 3rd-place solution carry the signal

The bar of one minute says little about the next 15 minutes; the asset's recent returns relative to the market do (in ranks most clearly). Correlation of each feature with the target on the shipped frame.

| feature | pearson_r_with_target | spearman_r_with_target |
|---|---|---|
| Count | 0.0052 | -0.0074 |
| Open | -0.0009 | 0.0005 |
| High | -0.0009 | 0.0005 |
| Low | -0.0009 | 0.0005 |
| Close | -0.0009 | 0.0005 |
| Volume | 0.0114 | -0.005 |
| VWAP | -0.0009 | 0.0005 |
| log_close_to_mean_60 | -0.0243 | -0.0393 |
| market_log_close_to_mean_60 | 0.0055 | -0.0093 |
| log_close_to_mean_60_minus_market | -0.0452 | -0.0615 |
| log_return_60 | -0.0226 | -0.0355 |
| market_log_return_60 | 0.0016 | -0.0121 |
| log_return_60_minus_market | -0.0387 | -0.0523 |
| log_close_to_mean_300 | -0.0226 | -0.0349 |
| market_log_close_to_mean_300 | -0.0014 | -0.0128 |
| log_close_to_mean_300_minus_market | -0.0367 | -0.0541 |
| log_return_300 | -0.0138 | -0.0245 |
| market_log_return_300 | -0.0014 | -0.0108 |
| log_return_300_minus_market | -0.0216 | -0.0365 |
| log_close_to_mean_900 | -0.0133 | -0.0251 |
| market_log_close_to_mean_900 | -0.0012 | -0.0116 |
| log_close_to_mean_900_minus_market | -0.0214 | -0.0381 |
| log_return_900 | -0.0051 | -0.0153 |
| market_log_return_900 | -0.0001 | -0.008 |
| log_return_900_minus_market | -0.0086 | -0.0233 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicates_skipped`: Skipped duplicate-column/row checks: 715,452,214 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to run them; nothing else checks duplicate rows and columns.)

Accepted on purpose:

- `task_metric_weight_without_sample_weight`: The asset's Weight is a function of Asset_Name, a feature, so MET-15 needs no sample weight (2026-11-06). Training with it moved the weighted Pearson by +0.0026 on average, within the spread across the three windows that ended on 20 September 2021 (SD 0.0023, t about 1.96 on 2 df); only the newest window's interval excludes 0 (+0.0050 [+0.0005, +0.0099]).
- `splits_train_under_half`: Signed off (Lennart, 2026-11-11): the window of the 2020 crash (from 28 February 2020) trains on 48.25% of the rows, beside 93.0% and 69.2%; kept as the curator's exception (Andrej, 2026-11-19).

## Data checks

### Feature summary

<details>
<summary>Show the table (29 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| Asset_Name | category | 0 | 0 | 14 | Bitcoin, Litecoin, EOS.IO, Ethereum, Bitcoin Cash, Ethereum Classic, Binance Co… |
| timestamp | datetime64\[ns\] | 0 | 0 | 2.0412e+06 | 2020-05-11 20:46:00, 2021-01-15 21:25:00, 2018-10-15 23:12:00, 2021-09-19 09:59… |
| log_close_to_mean_900 | float64 | 22054 | 0.09 | 2.46466e+07 | 0.0276, 0.008, -0.0035, 0.011, 0.0056, 0.0132, -0.0066, -0.0019, 0.0103, -0.0009 |
| log_close_to_mean_900_minus_market | float64 | 22054 | 0.09 | 2.46487e+07 | 0.0007, 0.001, -0.0068, 0.0055, -0.0048, 0.0185, -0.0003, 0.0037, -0.0214, 0.00… |
| log_return_900 | float64 | 12708 | 0.05 | 2.38706e+07 | 0.0, 0.0, 0.022, 0.0241, 0.0194, 0.011, 0.0465, 0.0339, 0.015, 0.0541 |
| log_return_900_minus_market | float64 | 12708 | 0.05 | 2.4658e+07 | -0.0073, -0.0004, -0.0133, 0.001, -0.0173, 0.0041, -0.0362, 0.0685, 0.0079, 0.0… |
| log_close_to_mean_300 | float64 | 7182 | 0.03 | 2.4657e+07 | 0.0025, -0.0017, 0.0047, 0.0001, -0.0051, 0.0045, -0.0082, -0.0066, 0.0007, 0.0… |
| log_close_to_mean_300_minus_market | float64 | 7182 | 0.03 | 2.46636e+07 | 0.0029, 0.0009, -0.0016, 0.0028, -0.0032, 0.0022, 0.0057, 0.0057, 0.0017, 0.0048 |
| market_log_close_to_mean_900 | float64 | 6537 | 0.03 | 2.0403e+06 | -0.0059, 0.004, -0.0078, -0.021, -0.0123, 0.0012, 0.02, 0.0302, 0.0138, -0.0171 |
| market_log_return_900 | float64 | 6545 | 0.03 | 2.0403e+06 | -0.0023, -0.0019, 0.0253, 0.0019, 0.0005, 0.0115, 0.0059, -0.0179, -0.0112, -0.… |
| log_return_300 | float64 | 5404 | 0.02 | 2.3627e+07 | 0.0, 0.0101, 0.0, 0.0, 0.0124, 0.0112, 0.0202, 0.0069, 0.007, 0.009 |
| log_return_300_minus_market | float64 | 5404 | 0.02 | 2.46653e+07 | 0.0099, 0.0017, -0.005, 0.0035, -0.0011, 0.0104, -0.0209, -0.0058, 0.0017, 0.00… |
| log_close_to_mean_60 | float64 | 1477 | 0.01 | 2.46218e+07 | 0.0, 0.0, -0.0008, 0.0, 0.0033, 0.0024, 0.0112, 0.0008, 0.0059, 0.0 |
| log_close_to_mean_60_minus_market | float64 | 1477 | 0.01 | 2.46693e+07 | 0.0, -0.0002, -0.0012, 0.0007, -0.0014, 0.0024, 0.0068, 0.0022, -0.0018, 0.0032 |
| log_return_60 | float64 | 1310 | 0.01 | 2.31852e+07 | 0.0, 0.0, 0.0, 0.01, 0.0071, 0.0, 0.0091, 0.0055, 0.0054, 0.0 |
| log_return_60_minus_market | float64 | 1310 | 0.01 | 2.46692e+07 | 0.0006, 0.0065, -0.0098, -0.0096, 0.0009, 0.0025, -0.0011, -0.0009, 0.0053, -0.… |
| market_log_close_to_mean_300 | float64 | 2178 | 0.01 | 2.0409e+06 | 0.0073, -0.0382, 0.0017, 0.0118, -0.0244, -0.0172, 0.0086, -0.0069, 0.0004, 0.0… |
| market_log_return_300 | float64 | 2185 | 0.01 | 2.0409e+06 | 0.0388, -0.0159, -0.0085, -0.0049, 0.0023, -0.0169, -0.0146, -0.0141, 0.0088, 0… |
| Count | float64 | 0 | 0 | 21882 | 6.0, 5.0, 7.0, 4.0, 8.0, 3.0, 9.0, 10.0, 11.0, 2.0 |
| Open | float64 | 0 | 0 | 1.05938e+07 | 0.2701, 0.271, 0.27, 0.0026, 0.2713, 0.2723, 0.0026, 0.2777, 0.275, 0.2693 |
| High | float64 | 0 | 0 | 2.969e+06 | 0.3, 0.28, 0.275, 0.304, 0.27, 0.278, 0.279, 0.303, 0.29, 0.271 |
| Low | float64 | 0 | 0 | 2.84037e+06 | 9.55, 9.5, 0.27, 9.54, 0.3, 9.56, 9.46, 9.53, 9.51, 0.26 |
| Close | float64 | 0 | 0 | 1.05688e+07 | 0.2708, 0.0026, 0.0026, 0.27, 0.2689, 0.2702, 0.2713, 0.28, 0.278, 0.2532 |
| Volume | float64 | 2 | 0 | 2.32434e+07 | 1.0, 2.0, 3.0, 5.0, 4.0, 10.0, 1000.0, 0.1, 6.0, 0.001 |
| VWAP | float64 | 16 | 0 | 2.42711e+07 | 0.0026, 0.0025, 0.0026, 0.0026, 0.0025, 0.0026, 0.0025, 0.0026, 0.2695, 0.0026 |
| Target | float64 | 0 | 0 | 2.33464e+07 | 0.0, 0.0, 0.0, 0.0, 0.0, 0.0027, 0.0017, 0.0033, 0.0018, 0.0015 |
| market_log_close_to_mean_60 | float64 | 420 | 0 | 2.04114e+06 | 0.0031, 0.0058, -0.0091, -0.0047, -0.0225, -0.0071, 0.0024, 0.0092, -0.0184, 0.… |
| market_log_return_60 | float64 | 428 | 0 | 2.04114e+06 | 0.0032, 0.0119, -0.0077, -0.0016, -0.0294, -0.0103, 0.0036, 0.0178, -0.0297, 0.… |
| Weight | float64 | 0 | 0 | 11 | 2.3979, 2.0794, 1.0986, 6.7799, 1.3863, 5.8944, 4.3041, 1.7918, 4.4067, 1.6094 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 51.04 | 1.536 | 0.501 | 0 | 0 | log1p | -1.15967e+07 | -1.15377e+07 | exponential |

### Numeric features

<details>
<summary>Show the table (27 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| Count | 2.46708e+06 | 303.188 | 890.813 | 1 | 96437 |
| Open | 2.46708e+06 | 1610.57 | 6688.09 | 0.001266 | 68616.9 |
| High | 2.46708e+06 | 1614.4 | 6697.94 | 0.001304 | 68775.1 |
| Low | 2.46708e+06 | 1607.35 | 6678.56 | 0.0002 | 68561 |
| Close | 2.46708e+06 | 1610.57 | 6688.09 | 0.00124175 | 68724 |
| Volume | 2.46708e+06 | 297258 | 2.47573e+06 | 8e-08 | 4.2169e+08 |
| VWAP | 2.46708e+06 | 1610.56 | 6688.05 | 0.00128596 | 68688 |
| Target | 2.46708e+06 | 8.72753e-06 | 0.00561044 | -0.299335 | 0.356739 |
| log_close_to_mean_60 | 2.46693e+06 | -1.41935e-06 | 0.00779614 | -0.46041 | 0.431939 |
| market_log_close_to_mean_60 | 2.46704e+06 | -6.24841e-06 | 0.00601801 | -0.35716 | 0.171852 |
| log_close_to_mean_60_minus_market | 2.46693e+06 | 4.87773e-06 | 0.00494391 | -0.237775 | 0.376484 |
| log_return_60 | 2.46694e+06 | 3.42615e-05 | 0.0134087 | -0.684188 | 0.574466 |
| market_log_return_60 | 2.46704e+06 | 2.45207e-05 | 0.0105041 | -0.425549 | 0.297911 |
| log_return_60_minus_market | 2.46694e+06 | 9.86367e-06 | 0.00832788 | -0.615389 | 0.546626 |
| log_close_to_mean_300 | 2.46636e+06 | 2.26631e-05 | 0.0162462 | -0.582611 | 0.631562 |
| market_log_close_to_mean_300 | 2.46684e+06 | -4.41727e-06 | 0.0131396 | -0.4689 | 0.142717 |
| log_close_to_mean_300_minus_market | 2.46636e+06 | 2.76133e-05 | 0.00955982 | -0.422599 | 0.595014 |
| log_return_300 | 2.46651e+06 | 0.000189631 | 0.0278722 | -0.675502 | 1.14248 |
| market_log_return_300 | 2.46684e+06 | 0.000141018 | 0.0225188 | -0.526041 | 0.401162 |
| log_return_300_minus_market | 2.46651e+06 | 5.02366e-05 | 0.0164109 | -0.650818 | 1.06761 |
| log_close_to_mean_900 | 2.4649e+06 | 8.09575e-05 | 0.027468 | -0.660065 | 1.06872 |
| market_log_close_to_mean_900 | 2.46643e+06 | 1.82397e-05 | 0.0224027 | -0.540372 | 0.169946 |
| log_close_to_mean_900_minus_market | 2.4649e+06 | 6.44709e-05 | 0.0158717 | -0.433791 | 0.987507 |
| log_return_900 | 2.46581e+06 | 0.000527903 | 0.0479009 | -0.784335 | 1.93123 |
| market_log_return_900 | 2.46643e+06 | 0.000433775 | 0.0388975 | -0.645669 | 0.326557 |
| log_return_900_minus_market | 2.46581e+06 | 0.000100492 | 0.027957 | -0.676598 | 1.77474 |
| Weight | 2.46708e+06 | 3.06077 | 1.77138 | 1.09861 | 6.77992 |

</details>

### Categorical features

| column | rank | value | count | pct |
|---|---|---|---|---|
| Asset_Name | 1 | Bitcoin | 204493 | 8.29 |
| Asset_Name | 2 | Litecoin | 204230 | 8.28 |
| Asset_Name | 3 | EOS.IO | 203680 | 8.26 |
| Asset_Name | 4 | Ethereum | 203096 | 8.23 |
| Asset_Name | 5 | Bitcoin Cash | 202977 | 8.23 |
| timestamp | 1 | 2020-05-11 20:46:00 | 8 | 0 |
| timestamp | 2 | 2021-01-15 21:25:00 | 8 | 0 |
| timestamp | 3 | 2018-10-15 23:12:00 | 8 | 0 |
| timestamp | 4 | 2021-09-19 09:59:00 | 8 | 0 |
| timestamp | 5 | 2018-12-21 15:39:00 | 8 | 0 |

## Build

| field | value |
|---|---|
| uuid | 01a217f5-dcae-71fb-b705-cf84808b184a |
| checksum | v2:2ed9741894f7fd1ec6fdd1716fc62bb3ec0ea922ecbc947c9506a428388bc42d |
| built_at | 2026-11-26T13:14:35+00:00 |
| path | g_research_crypto_forecasting_1m/01a217f5-dcae-71fb-b705-cf84808b184a |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
