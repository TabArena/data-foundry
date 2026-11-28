---
report_format: data-foundry-report-v2
unique_name: airqo_low_cost_air_quality_monitor_calibration_challenge
container_format: 2
checksum: v2:a6df0030463bd95255b326c4b74397d51feed953b9b28c676e30d68da4a29ca2
build:
  uuid: 01a21800-ad9e-73d9-a085-fce439694fdb
  checksum: v2:a6df0030463bd95255b326c4b74397d51feed953b9b28c676e30d68da4a29ca2
  built_at: '2026-11-26T13:17:08+00:00'
  path: airqo_low_cost_air_quality_monitor_calibration_challenge/01a21800-ad9e-73d9-a085-fce439694fdb
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
  n_rows: 10828
  n_features: 16
  dtypes:
    category: 2
    datetime64[ns, UTC+03:00]: 1
    float64: 9
    int64: 5
  n_test_dataset_rows: null
task:
  target: ref_pm2_5
  problem_type: regression
  metric: rmse
  metric_origin: source
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: created_at
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 6
  n_folds: 1
  random_state: 4267
  time_horizon: 1
  time_horizon_unit: months
  time_gap: null
  time_gap_unit: null
  reason: 'Six one-month windows, newest first: February 2021, January 2021, December
    2020, November 2020, October 2020

    and August 2020 (Lennart: October to February on 2026-11-05; August on 2026-11-11).

    August

    2020 trains on less than half the hours (47.7%), beside the five months from October
    on 57.3% to 92.3%. A

    model refit at the start of each month corrects that month''s readings; the monthly
    cadence is the curator''s

    judgment (Lennart, 2026-11-04; checked 2026-11-11), as no source gives one. Adong
    et al. (2022) say it is

    "important to retrain these models periodically" and name "seasonal re-calibration"
    as future work; AirQo''s

    refit practice is not documented. The test covers three seasons: mean reference
    41.4 in August, the end of

    the June-August dry season; 42.3 and 40.5 in October and November, two months
    of the September-November

    rains; and 44.8, 49.5 and 74.2 in the December-February dry season (SPLIT-20).
    September 2020 (53.0%) is left

    out: 63 of its 462 hours (13.6%) are at Nakawa, which has no earlier hour, a new-site
    test in this known-site

    task (USE-10). The three dry-season windows of 2026-11-04 ("ok (a)") are superseded.
    Site coverage differs by

    month: August scores Makerere only, October and November all three sites, December
    has no USEmbassy rows,

    January 45, February no Nakawa. History before the test months: USEmbassy from
    2019-07-25, Makerere from

    2020-07-15 (306 hours, half a month, before August; 2.5 to 6.5 months before the
    later windows), and Nakawa

    from 2020-09-19 with only 63 hours (to 2020-09-23) before the October window,
    then 1.4 to 3.4 months;

    Nakawa''s October hours are close to a new-site test (USE-10). The reference is
    for the same hour and no

    reporting delay is documented, so no gap is needed; no training row has a label
    from after its window start.

    Random folds over the hourly stream gave the model reference labels of neighbouring
    hours and scored a quarter

    better (untuned LightGBM, one seed, mean RMSE 11.23 against 15.34 on the five
    test months of 2026-11-05;

    trained on an equal-size random draw of all other months, future included, 14.53).
    Superseded 2026-11-05:

    12.94 against 18.26 on the three windows (review panel, 2026-11-04). Six of the
    nine windows an IID split of

    this size would get: September 2020 is out (Nakawa''s hours have no history),
    and July 2020 and earlier train

    on under 47.7% of the hours, July scoring Makerere''s first hours (Andrej, 2026-11-19).'
  n_train:
    min: 5166
    max: 9994
  n_test:
    min: 576
    max: 1310
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos: []
  accepted:
    splits_train_under_half: 'Signed off (Lennart, 2026-11-11): August 2020 trains
      on 47.7% of the hours, beside the five months from October 2020 to February
      2021 on 57.3% to 92.3%; kept as the curator''s exception to SPLIT-14''s half-data
      floor (Andrej, 2026-11-19).'
    splits_dimensions_off_protocol: 'Six of the nine windows an IID split of this
      size would get: September 2020 is out (Nakawa''s hours have no history), and
      July 2020 and earlier train on under 47.7% of the hours, July scoring Makerere''s
      first hours (Andrej, 2026-11-19).'
decisions:
- Dead sensor channels set missing
- Single-hour reference errors dropped
- Nakawa reference outage dropped
---

# airqo_low_cost_air_quality_monitor_calibration_challenge

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `ref_pm2_5`, scored with `rmse` on temporal splits by `created_at`. 10,828 rows and 16 features. Source: Zindi (2021).

Built as `01a21800-ad9e-73d9-a085-fce439694fdb` on 2026-11-26. See [Build](#build).

## In brief

**Question.** What reference-monitor PM2.5 value corresponds to this hour's low-cost monitor reading at a site?

**Use case.** AirQo corrects low-cost PM2.5 readings with a model learned from hours in which its devices sat next to a reference monitor. Here a model refit at the start of each month corrects that month's new hourly readings at the three collocated devices.

**One row.** One hourly collocated low-cost/reference observation at one of three Kampala sites, from 2019 to 2021.

**Predicted.** The same-hour reference-monitor PM2.5 mass concentration in micrograms per cubic metre.

**Known at prediction time.** The recorded hour and site, both low-cost sensors' PM2.5 and PM10 readings, the city-wide temperature and humidity, and the site descriptors. No reference value from the month being corrected is known, so reference values from other hours are not predictors.

**What the test data stands for.** Six monthly windows, October 2020 to February 2021 and August 2020, each trained on every earlier hour: a model refit at the start of each month corrects that month's readings. The test covers the end of Kampala's June-August dry season, two months of the September-November rains and the December-February dry season.

**Our changes to the source.** Use only the labeled Train.csv. Drop the opaque row ID; set a dead sensor's two channels missing (sensor 2 in 516 hours, sensor 1 in 18); drop 12 single-hour reference errors and 92 hours of a Nakawa reference outage (10,828 of 10,932 rows stay); parse the recorded UTC+3 timestamp, type the site as categorical and decode the 90m landform class into its catalogue words.

> **Use case fit: approximate (a stand-in with a known gap).** AirQo's main use is correcting network devices that have no reference monitor; with three sites that transfer cannot be tested (leaving one site out, an untuned LightGBM scores RMSE 24.84 against 19.90 for the raw sensor). The task tests the next monthly refit at known collocated sites, a cadence the curator chose; the source paper names seasonal retraining as future work. Reference aggregation and site-metadata dates are unverified.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/airqo_low_cost_air_quality_monitor_calibration_challenge.md`](../../../../curation/records/airqo_low_cost_air_quality_monitor_calibration_challenge.md)
- The original source: <https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/airqo_low_cost_air_quality_monitor_calibration_challenge/`. To get them:

```text
Download Train.csv, Test.csv and optionally SampleSubmission.csv through an authorized account at
https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge/data.
Myunghwan supplied these original-download files on 2026-10-27 with a _LowCost filename suffix.
We archived those bytes and restored the published filenames without editing their contents.
This is user-supplied provenance; no agent-authenticated download or publisher checksum is claimed.
Place Train.csv under the warehouse's airqo_low_cost_air_quality_monitor_calibration_challenge/.
Its SHA-256 must be e856a03d70873f70630a1cb39c30ec9214f3710a8f343b72ca148081b66c5d92.
Test.csv and SampleSubmission.csv are provenance/partition checks, not additional training labels.
Keep competition data private under the published terms.
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/airqo_low_cost_air_quality_monitor_calibration_challenge   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/airqo_low_cost_air_quality_monitor_calibration_challenge   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Zindi: https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge |
| year | 2021 |
| domain | environmental science & climate |
| license | Zindi competition data terms: private participant use; redistribution to nonparticipants prohibited. |
| data_tags | Non-IID, Temporal, Spatial |
| reference | AirQoCalibration2021 |
| rows x columns | 10,828 x 17 |
| task.target | ref_pm2_5 |
| task.problem_type | regression |
| task.metric | rmse |
| task.split_regime | temporal_non_iid |
| task.time_on | created_at |

**Metric**

| field | value |
|---|---|
| name | `rmse` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | Root Mean Squared Error |
| reference | https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge#evaluation |
| definition | Square root of the mean squared error on original reference PM2.5, in micrograms per cubic metre |

<details>
<summary>Feature types: 2 categorical, 0 string, 1 datetime</summary>

- categorical (2): `site`, `landform_90m`
- string (0): none
- datetime (1): `created_at (ISO8601)`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{AirQoCalibration2021,
  author = {{AirQo} and {Zindi}},
  title = {AirQo Low-Cost Air Quality Monitor Calibration Challenge},
  year = {2021},
  howpublished = {https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge},
  note = {Three Kampala collocations; source evaluation uses RMSE}
}
```

</details>

## Sample rows

The first 5 of 10,828 rows of the final frame (the oldest rows: the frame is sorted by `created_at`); 12 of 17 columns, the target first. Cells are cut at 40 characters.

| ref_pm2_5 | created_at | site | pm2_5 | pm10 | s2_pm2_5 | s2_pm10 | humidity | temp | lat | long | altitude |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 89 | 2019-07-25 09:00:00+03:00 | USEmbassy | 76.1204 | 82.675 | 71.9696 | 82.3521 | 0.9735 | 20.575 | 0.299255 | 32.5927 | 1199 |
| 77 | 2019-07-25 15:00:00+03:00 | USEmbassy | 54.225 | 66.3379 | 52.0771 | 65.7181 | 0.603333 | 26.8417 | 0.299255 | 32.5927 | 1199 |
| 91 | 2019-07-25 16:00:00+03:00 | USEmbassy | 53.8402 | 66.529 | 51.7559 | 65.4907 | 0.655833 | 26.1333 | 0.299255 | 32.5927 | 1199 |
| 68 | 2019-07-25 17:00:00+03:00 | USEmbassy | 55.828 | 68.3515 | 52.8033 | 67.0073 | 0.69275 | 25.475 | 0.299255 | 32.5927 | 1199 |
| 67 | 2019-07-25 18:00:00+03:00 | USEmbassy | 60.667 | 71.0945 | 58.0433 | 71.3072 | 0.740833 | 24.4917 | 0.299255 | 32.5927 | 1199 |

## Curation notes

We start with the 10,932 labeled rows of the supplied 2021 competition Train.csv; 10,828 ship.

- Prediction point: the start of each month, when a model refit on every earlier collocated hour corrects
  that month's new hourly readings at the three collocated devices. No reference value from that month is
  known, so lagged or neighbouring reference values are not features (a previous-hour reference lowers an
  untuned LightGBM's mean RMSE from 18.21 to 16.28 on the three windows, all from test-month labels;
  superseded 2026-11-05: 15.34 to 14.09 on the five windows, February 27.12 to 23.23).
  Lennart chose this forward reading on 2026-11-04 with the temporal split; it supersedes the retrospective
  correction of archived hours that Myunghwan approved on 2026-10-27/28.
- Keep ref_pm2_5 on its original micrograms-per-cubic-metre scale, with source RMSE; no target
  transformation, clipping or weighting. Labels run from 0.2 to 459.0. The 92 Nakawa outage hours of
  2020-11-10 to 2020-11-23 were kept on 2026-11-04 (superseded 2026-11-05: they leave, CC below).
- Drop ID: it is an opaque, unique row key. Parse created_at as the supplied UTC+3 time without adding
  another three-hour shift. No target lags, leads, reference-neighbor features or full-data label transforms.
- Treat site and landform_90m as nominal. The source's Google Earth Engine links identify landform_90m as
  discrete ALOS landform classes, decoded into the catalogue's words (21 "Upper slope (warm)", 31 "Lower slope
  (warm)"; CLEAN-12, Lennart 2026-11-04). The ALOS classes cross slope position with a warm/cool aspect, a
  partial order, so they stay unordered (CLEAN-14). landform_270m is continuous mTPI and stays numeric; its
  -11 valley value is valid. Keep the original greenness scale because its rescaling is undocumented.
- Reference spikes (Lennart, 2026-11-04: "mark it well in the dataset notes"): a reference hour above 3 times
  both low-cost PM2.5 channels and above 3 times the same site's reference in both neighbouring hours is a
  single-hour artefact of the reference monitor, set missing and its row dropped (CLEAN-11, CLEAN-15). The
  rule catches 5 hours: Nakawa 2020-10-03 10:00 (444.0), 2020-10-05 09:00 (176.8), 2020-10-17 09:00 (374.5),
  2020-10-30 17:00 (150.6) and Makerere 2021-02-17 20:00 (249.1) (superseded 2026-11-05: 12 hours, CC below).
  The rule reads the target and its neighbouring labels. The four Nakawa hours are on the training side of
  every window (superseded 2026-11-05: under the five windows they are October 2020 test labels); the
  Makerere hour is in the February 2021 test window, where CLEAN-11 lets a single extreme target leave only
  from the training period (settled 2026-11-05: an impossible value, dropped in every window, CC
  below). The rule follows the spike (rate-of-change) screening that hourly reference-monitor feeds such as
  EPA's AirNow run as automated QC (no published QC document is quoted yet). It needs both neighbouring hours
  in the file, so four look-alike hours with a missing neighbour stay (superseded 2026-11-05: the rule takes
  the neighbouring hours present and drops them, CC below), and USEmbassy 2021-02-10 07:00 (459.0, February
  window) misses the threshold by 0.55 (to sensor 1; to sensor 2 by 26.2). Spikes lasting several hours,
  often at two sites at once, stay: they look like real pollution events.
- Keep ordinary missingness: five humidity and 17 temperature values. Exact upstream averaging and
  reference-label construction are unknown; unusual positive values are not proven erroneous.
- Sensor 2's PM2.5 and PM10 both read exactly 0 in 500 labeled hours, all at USEmbassy between
  2019-11-18 and 2019-12-17 in 13 runs of 11 to 117 hours; neither channel is 0 anywhere else, and sensor 1
  never reads below 0.57. In those hours sensor 1 reads a mean PM2.5 of 52 and the reference 59, so the
  zeros are a dead channel, not clean air. Both sensor-2 channels are set missing for those hours and the
  rows stay, with sensor 1 and the reference (CLEAN-11: an impossible value becomes missing; Lennart,
  2026-11-04). The definition raises if the joint zeros no longer number 500. Sixteen more hours of the same
  outage, with sensor 2 near zero (0.0014 to 1.37 in 15 of them), and 18 USEmbassy hours with sensor 1 dead
  (2019-11-13/14, 2020-06-07/08) stay as readings (superseded 2026-11-05: set missing, CC below).
- All 16 predictors remain after ID removal. The eight geographic/site descriptors are constant within
  each site and encode its identity; recurrence is legitimate for this known-site task. Temperature and
  humidity are identical across sites at every shared hour: one city-wide ("prevailing") series, not device
  sensors. No duplicate site-hour or exact predictor copy occurs in the supplied labeled file.
- The supplied Test.csv has 2,733 rows, approximately 20 percent within each site, over overlapping dates.
  It has no reference labels. Training uses only labeled Train.csv; the leaderboard's random split is not
  recreated.
- New-site transfer, AirQo's network use, cannot be tested with three sites whose periods barely overlap
  (see fit_reason). Exact device serials, source reference aggregation and site-metadata snapshot dates
  remain unverified.
- On the five windows of 2026-11-05 (October 2020 to February 2021; not measured again with August 2020),
  untuned models give mean RMSE 36.42 for the training mean, 21.01 for raw sensor 1, 20.71 for a linear
  model, 15.08 for a forest and 15.34 for LightGBM (27.4, 14.7, 12.2, 9.3 and 13.2 per window, February
  first; one seed). February, the highest-pollution month, dominates the mean. (Superseded 2026-11-05: 41.22,
  25.32, 24.76, 19.21 and 18.26 on the three windows of 2026-11-04; LightGBM 16.69, with January 16.8 and
  November 13.0, before the 7 hours the spike rule adds.)
- Exact feature-copy share is zero on all five windows of 2026-11-05 (not measured again with August 2020).
  The hidden-group probe finds no entity-like column; near-copy clusters hold 6.7% of rows, and 12.1% of test
  rows have one on the training side (superseded 2026-11-05: the quantized profiles' 17.72 percent and
  0.001215 skill gap came from the random folds). Only 4 of 4,624 test rows have a same-site training hour
  within one hour, at the window starts.
- The leak probes run on the five windows of 2026-11-05 (not run again with August 2020; superseded
  2026-11-05: the pinned CLI failed on timezone-aware dates, and a by-hand substitute on the three windows
  found no leak) and find none: all features score skill 0.813, each sensor channel alone 0.61 to 0.66 and
  every other column alone below 0, and no test row copies a training row. Dropping one column moves an
  untuned LightGBM's mean RMSE by at most 0.62, and created_at alone scores a skill of 0.04.
- The split is temporal (Lennart, 2026-11-04), replacing the site-balanced random folds Myunghwan approved on
  2026-10-28; see the splits comment.
- CC (2026-11-05, Lennart): five monthly windows from October 2020 instead of the three dry-season months
  (SPLIT-20, as aeolus and perth_house_prices widened theirs). The test now holds 4,631 hours
  (4,624 after the spike rule) over both seasons, and October and November score all three sites; the smallest
  train side is 57.3% (SPLIT-14). Nakawa enters the October window with 63 hours of history (2020-09-19 to
  2020-09-23), so its October hours are close to a new-site test inside this known-site task (USE-10). It
  supersedes the three windows of 2026-11-04 ("ok (a)"). (Superseded 2026-11-11: six windows, August 2020
  added, CC below.)
- CC (2026-11-05, Lennart): the 92-hour Nakawa reference outage leaves (CLEAN-11 impossible-value
  clause, then CLEAN-15; as qsar_tid_11 and 2024_lusaka_mobility_prediction_hackathon). A Nakawa hour of
  2020-11-10 to 2020-11-23 with the reference below 0.3 times both low-cost PM2.5 channels is a failed
  reference: 92 hours, reference 0.1 to 11.2 against channels of 12 to 190, while Nakawa's monthly median
  ratio of reference to sensor 1 is 1.04 to 1.21 elsewhere. The target is set missing and the rows leave;
  the definition raises unless the count is 92. Without the date bound the same test catches 96 Nakawa hours.
  Under the five windows these are November 2020 test labels; November keeps 599 hours, 260 of them at Nakawa
  (596 and 258 after the spike rule).
- CC (2026-11-05, Lennart): one symmetric dead-channel rule at 0.27 (CLEAN-11; as heart_disease,
  ashrae and protein_model_quality_rf_pcp): a sensor whose PM2.5 is below 0.27 times the other sensor's has
  both its channels set missing, and the row stays. It adds 16 sensor-2 hours of the 2019 outage and 18
  sensor-1 hours (2019-11-13/14, 2020-06-07/08), all at USEmbassy and on every window's training side; the
  definition raises unless the counts are 500, 16 and 18. Dead hours reach a ratio of 0.255, and the lowest
  live one, Makerere 2020-12-05 06:00 at 0.294 (December test window), stays a reading.
- CC (2026-11-05, Lennart): the spike rule becomes an instrument-error rule for every window, test windows
  included ((a) of its consistency check; CLEAN-11 impossible-value clause, then CLEAN-15; as the
  Nakawa outage, qsar_tid_11 and 2024_lusaka_mobility_prediction_hackathon). Collocated instruments sample
  the same air, so a reference hour several times both sensors and the hours around it is a value the
  reference could not have read ("we think the value is wrong"). A reference hour above 3 times both PM2.5
  channels and above 3 times the same site's reference in each neighbouring hour present, with at least one
  present (an outage hour counts as absent), is set missing and the row leaves; the definition raises unless
  the count is 12. It adds the four look-alikes with a missing neighbour, Nakawa 2020-10-29 17:00 (172.1),
  2020-11-02 18:00 (232.1), 2021-01-01 22:00 (147.2) and Makerere 2020-12-08 14:00 (82.9), and three more:
  Nakawa 2020-10-13 05:00 (36.2 against channels of 11.1 and 11.8, the weakest at 3.06 times, before a
  morning rise the sensors show by 07:00), 2020-11-04 13:00 (40.4 against 6.7 and 7.2) and USEmbassy
  2020-11-06 02:00 (155.0 against 30.4 and 31.6). All 12 are test labels (October 6, November 3, December,
  January and February 1 each); 10,828 rows ship. USEmbassy 2021-02-10 07:00 (459.0 against 153.2 and 161.7,
  before 99.0, no 08:00 hour) stays: it is 2.84 times sensor 2, and a channel factor of 2.83 would catch it
  and no other hour. LightGBM's mean RMSE goes from 16.69 to 15.34 (November 13.0 to 9.3, January 16.8 to
  14.7).
- CC (2026-11-05, Lennart): the declared metric (RMSE on the original micrograms-per-cubic-metre scale, the
  source's) is checked and stays as declared. Public data redistribution permission
  is not established by these checks; the source's private-participant restrictions remain in force.
- CC (2026-11-11, Lennart): a sixth test window, August 2020 ("Six months with August
  2020", (c) of the consistency check), the end of the June-August dry season that no other test month holds.
  August's 576 hours are all at Makerere, which has 306 earlier hours (15-31 July 2020); it trains on 47.7%
  of the hours, the one window under half, signed off (SPLIT-14 as amended on 2026-11-11). September 2020
  stays out: 63 of its 462 hours are at Nakawa, which has no earlier hour. The monthly windows without a gap
  are checked (the horizon).

## Splits

Expanding-window temporal splits: 6 test window(s) of 1 month, starting at 2021-02-01, 2021-01-01, 2020-12-01, 2020-11-01, 2020-10-01, 2020-08-01, newest first; train is all earlier data. The test windows by `created_at`, as listed: 2021-02-01 to 2021-02-28 (834 test, 9,994 train rows); 2021-01-01 to 2021-01-31 (1,048 test, 8,946 train rows); 2020-12-01 to 2020-12-31 (836 test, 8,110 train rows); 2020-11-01 to 2020-11-30 (596 test, 7,514 train rows); 2020-10-01 to 2020-10-31 (1,310 test, 6,204 train rows); 2020-08-01 to 2020-08-31 (576 test, 5,166 train rows).

Six one-month windows, newest first: February 2021, January 2021, December 2020, November 2020, October 2020
and August 2020 (Lennart: October to February on 2026-11-05; August on 2026-11-11).
August
2020 trains on less than half the hours (47.7%), beside the five months from October on 57.3% to 92.3%. A
model refit at the start of each month corrects that month's readings; the monthly cadence is the curator's
judgment (Lennart, 2026-11-04; checked 2026-11-11), as no source gives one. Adong et al. (2022) say it is
"important to retrain these models periodically" and name "seasonal re-calibration" as future work; AirQo's
refit practice is not documented. The test covers three seasons: mean reference 41.4 in August, the end of
the June-August dry season; 42.3 and 40.5 in October and November, two months of the September-November
rains; and 44.8, 49.5 and 74.2 in the December-February dry season (SPLIT-20). September 2020 (53.0%) is left
out: 63 of its 462 hours (13.6%) are at Nakawa, which has no earlier hour, a new-site test in this known-site
task (USE-10). The three dry-season windows of 2026-11-04 ("ok (a)") are superseded. Site coverage differs by
month: August scores Makerere only, October and November all three sites, December has no USEmbassy rows,
January 45, February no Nakawa. History before the test months: USEmbassy from 2019-07-25, Makerere from
2020-07-15 (306 hours, half a month, before August; 2.5 to 6.5 months before the later windows), and Nakawa
from 2020-09-19 with only 63 hours (to 2020-09-23) before the October window, then 1.4 to 3.4 months;
Nakawa's October hours are close to a new-site test (USE-10). The reference is for the same hour and no
reporting delay is documented, so no gap is needed; no training row has a label from after its window start.
Random folds over the hourly stream gave the model reference labels of neighbouring hours and scored a quarter
better (untuned LightGBM, one seed, mean RMSE 11.23 against 15.34 on the five test months of 2026-11-05;
trained on an equal-size random draw of all other months, future included, 14.53). Superseded 2026-11-05:
12.94 against 18.26 on the three windows (review panel, 2026-11-04). Six of the nine windows an IID split of
this size would get: September 2020 is out (Nakawa's hours have no history), and July 2020 and earlier train
on under 47.7% of the hours, July scoring Makerere's first hours (Andrej, 2026-11-19).

6 repeat(s) x 1 fold(s) with seed 4267; train 5,166 to 9,994 rows, test 576 to 1,310 rows. Prediction horizon: 1 months.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 9994 | 834 | 2019-07-25 09:00:00+03:00 | 2021-01-31 22:00:00+03:00 | 2021-02-01 00:00:00+03:00 | 2021-02-28 23:00:00+03:00 |
| 1 | 0 | 8946 | 1048 | 2019-07-25 09:00:00+03:00 | 2020-12-31 23:00:00+03:00 | 2021-01-01 00:00:00+03:00 | 2021-01-31 22:00:00+03:00 |
| 2 | 0 | 8110 | 836 | 2019-07-25 09:00:00+03:00 | 2020-11-30 22:00:00+03:00 | 2020-12-01 00:00:00+03:00 | 2020-12-31 23:00:00+03:00 |
| 3 | 0 | 7514 | 596 | 2019-07-25 09:00:00+03:00 | 2020-10-31 23:00:00+03:00 | 2020-11-01 00:00:00+03:00 | 2020-11-30 22:00:00+03:00 |
| 4 | 0 | 6204 | 1310 | 2019-07-25 09:00:00+03:00 | 2020-09-30 23:00:00+03:00 | 2020-10-01 00:00:00+03:00 | 2020-10-31 23:00:00+03:00 |
| 5 | 0 | 5166 | 576 | 2019-07-25 09:00:00+03:00 | 2020-07-31 23:00:00+03:00 | 2020-08-01 00:00:00+03:00 | 2020-08-31 23:00:00+03:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows airqo_low_cost_air_quality_monitor_calibration_challenge`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Feb 2021 | 834 | 0.923 | mean 74.21, median 59.05, p10 23.59, p90 154.7 | mean 51.55, median 43, p10 21, p90 94 | 1.235 | site (1.24), lat (1.24), long (1.24) | 0 |
| 1 | Jan 2021 | 1048 | 0.826 | mean 49.48, median 41.85, p10 15.3, p90 93.73 | mean 51.79, median 43, p10 21.8, p90 94 | 2.157 | lat (2.16), altitude (2.16), greenness (2.16) | 0 |
| 2 | Dec 2020 | 836 | 0.749 | mean 44.81, median 35.55, p10 16.2, p90 84 | mean 52.51, median 44, p10 22.9, p90 95 | 6.837 | site (6.84), lat (6.84), long (6.84) | 0 |
| 3 | Nov 2020 | 596 | 0.694 | mean 40.47, median 34.95, p10 13.3, p90 74.95 | mean 53.47, median 44.5, p10 23.7, p90 97 | 0.945 | site (0.94), altitude (0.94), landform_270m (0.94) | 0 |
| 4 | Oct 2020 | 1310 | 0.573 | mean 42.31, median 36.55, p10 15.89, p90 76.11 | mean 55.82, median 46, p10 25.23, p90 100 | 2.025 | site (2.02), altitude (2.02), landform_270m (2.02) | 0 |
| 5 | Aug 2020 | 576 | 0.477 | mean 41.42, median 35.05, p10 20.3, p90 70.25 | mean 58.75, median 49, p10 27, p90 104 | 11.265 | site (11.27), long (11.27), s2_pm2_5 (1.50) | 0 |

## Decisions

### 1. Dead sensor channels set missing

Both sensor-2 channels read exactly 0 in 500 USEmbassy hours (2019-11-18 to 2019-12-17) while sensor 1 and the reference show ordinary pollution, so the channel was dead (Lennart, 2026-11-04). One symmetric rule takes the rest of the same failure (Lennart, 2026-11-05): a sensor whose PM2.5 is below 0.27 times the other sensor's is dead, 16 more sensor-2 hours of that outage and 18 sensor-1 hours (2019-11-13/14, 2020-06-07/08). Dead hours reach a ratio of 0.255; the lowest live ratio is 0.294 (Makerere 2020-12-05 06:00). The dead sensor's two channels are set missing and the rows stay (CLEAN-11). The missing weather values stay too.

| kind | site | hours | first | last | dead_pm2_5_max | live_pm2_5_mean | reference_mean |
|---|---|---|---|---|---|---|---|
| sensor 2, both channels 0 | USEmbassy | 500 | 2019-11-18 11:00:00+03:00 | 2019-12-17 11:00:00+03:00 | 0 | 52.2 | 59.3 |
| sensor 2, below 0.27 of sensor 1 | USEmbassy | 16 | 2019-11-18 09:00:00+03:00 | 2019-12-14 07:00:00+03:00 | 2.87 | 27.9 | 36.1 |
| sensor 1, below 0.27 of sensor 2 | USEmbassy | 18 | 2019-11-13 02:00:00+03:00 | 2020-06-08 09:00:00+03:00 | 35.51 | 62.7 | 51.1 |

### 2. Single-hour reference errors dropped

Twelve reference hours read above 3 times both low-cost PM2.5 channels and above 3 times the same site's reference in each neighbouring hour in the file, with at least one there (Nakawa 2020-10-03 10:00: 444.0 against channels of 35 and 36 and neighbours of 47.5 and 86.0). Collocated instruments sample the same air, so a single hour that neither the sensors nor the hours around it share is an instrument error of the reference, an impossible value. They become missing and the rows leave, in the test windows too (CLEAN-11, CLEAN-15; Lennart, 2026-11-04 and 2026-11-05), by the rule, not by hand.

| site | created_at | pm2_5 | s2_pm2_5 | ref_pm2_5 | ref_before | ref_after |
|---|---|---|---|---|---|---|
| Nakawa | 2020-10-03 10:00:00+03:00 | 34.9 | 35.7 | 444 | 47.5 | 86 |
| Nakawa | 2020-10-05 09:00:00+03:00 | 20.6 | 22.2 | 176.8 | 25.4 | 26 |
| Nakawa | 2020-10-13 05:00:00+03:00 | 11.1 | 11.8 | 36.2 | 6.2 | nan |
| Nakawa | 2020-10-17 09:00:00+03:00 | 36.8 | 37.7 | 374.5 | 42.8 | 34.7 |
| Nakawa | 2020-10-29 17:00:00+03:00 | 21.9 | 23.4 | 172.1 | nan | 32.9 |
| Nakawa | 2020-10-30 17:00:00+03:00 | 19 | 19.8 | 150.6 | 20 | 28.8 |
| Nakawa | 2020-11-02 18:00:00+03:00 | 30.6 | 30.8 | 232.1 | nan | 49.6 |
| Nakawa | 2020-11-04 13:00:00+03:00 | 6.7 | 7.2 | 40.4 | nan | 12.8 |
| USEmbassy | 2020-11-06 02:00:00+03:00 | 30.4 | 31.6 | 155 | nan | 24 |
| Makerere | 2020-12-08 14:00:00+03:00 | 10.4 | 10.2 | 82.9 | nan | 11.3 |
| Nakawa | 2021-01-01 22:00:00+03:00 | 42.5 | 42.9 | 147.2 | nan | 43 |
| Makerere | 2021-02-17 20:00:00+03:00 | 52 | 49.5 | 249.1 | 21.7 | 43.7 |

### 3. Nakawa reference outage dropped

From 2020-11-10 to 2020-11-23, 92 Nakawa hours have the reference below 0.3 times both low-cost PM2.5 channels (2020-11-21 02:00: 0.1 against 101.2 and 102.0); outside these days Nakawa's monthly median ratio of reference to sensor 1 is 1.04 to 1.21. Collocated instruments sample the same air, so the reference failed: an impossible label, set missing, and the rows leave (CLEAN-11, CLEAN-15; Lennart, 2026-11-05). The rule is bounded to the run's site and days; without the date bound the same test catches 96 Nakawa hours.

| day | hours | reference_median | sensor1_pm2_5_median | sensor2_pm2_5_median |
|---|---|---|---|---|
| 2020-11-10 | 4 | 1.8 | 21.3 | 22.1 |
| 2020-11-11 | 7 | 3.2 | 19.7 | 20.2 |
| 2020-11-12 | 7 | 1.3 | 26.6 | 27.6 |
| 2020-11-13 | 4 | 3.7 | 30.9 | 31.5 |
| 2020-11-14 | 6 | 2.8 | 31.5 | 31.9 |
| 2020-11-15 | 6 | 1.6 | 34.9 | 35.4 |
| 2020-11-16 | 4 | 3 | 32.1 | 32.8 |
| 2020-11-17 | 8 | 2 | 48.6 | 49.9 |
| 2020-11-18 | 7 | 2.7 | 40.6 | 41.6 |
| 2020-11-19 | 7 | 0.7 | 23 | 23.7 |
| 2020-11-20 | 8 | 2 | 51 | 52.6 |
| 2020-11-21 | 9 | 1.8 | 101.2 | 102 |
| 2020-11-22 | 11 | 1.3 | 40.3 | 41.2 |
| 2020-11-23 | 4 | 3 | 37.8 | 38.6 |

## Bundle checks

0 error(s), 0 warning(s), 0 info (28 checks run, plus the dataset's own checks).


Accepted on purpose:

- `splits_train_under_half`: Signed off (Lennart, 2026-11-11): August 2020 trains on 47.7% of the hours, beside the five months from October 2020 to February 2021 on 57.3% to 92.3%; kept as the curator's exception to SPLIT-14's half-data floor (Andrej, 2026-11-19).
- `splits_dimensions_off_protocol`: Six of the nine windows an IID split of this size would get: September 2020 is out (Nakawa's hours have no history), and July 2020 and earlier train on under 47.7% of the hours, July scoring Makerere's first hours (Andrej, 2026-11-19).

## Data checks

### Feature summary

<details>
<summary>Show the table (17 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| site | category | 0 | 0 | 3 | USEmbassy, Makerere, Nakawa |
| landform_90m | category | 0 | 0 | 2 | Upper slope (warm), Lower slope (warm) |
| created_at | datetime64\[ns, UTC+03:00\] | 0 | 0 | 9053 | 2021-01-31 01:00:00+03:00, 2021-01-30 22:00:00+03:00, 2021-01-30 21:00:00+03:00… |
| s2_pm2_5 | float64 | 516 | 4.77 | 10288 | 25.1633, 42.667, 46.53, 34.49, 46.41, 70.47, 54.3, 50.438, 65.96, 41.96 |
| s2_pm10 | float64 | 516 | 4.77 | 10299 | 112.8544, 20.65, 66.9, 52.0767, 69.3238, 15.586, 56.9734, 26.3625, 24.57, 88.50… |
| pm2_5 | float64 | 18 | 0.17 | 10788 | 33.5895, 48.74, 48.222, 36.4314, 47.2929, 31.15, 36.3617, 36.7208, 28.4675, 19.… |
| pm10 | float64 | 18 | 0.17 | 10793 | 94.2267, 57.77, 25.6059, 90.63, 76.87, 62.305, 103.96, 42.4225, 25.1083, 20.78 |
| temp | float64 | 17 | 0.16 | 1577 | 19.2417, 19.025, 20.7917, 19.6083, 20.7333, 19.925, 19.8833, 19.7833, 19.3667, … |
| humidity | float64 | 5 | 0.05 | 4270 | 0.9992, 0.9995, 1.0, 0.9992, 0.9988, 0.9993, 0.9994, 0.9978, 0.9991, 0.999 |
| lat | float64 | 0 | 0 | 3 | 0.2993, 0.3335, 0.3317 |
| long | float64 | 0 | 0 | 3 | 32.5927, 32.5686, 32.6095 |
| ref_pm2_5 | float64 | 0 | 0 | 1199 | 38.0, 36.0, 27.0, 34.0, 39.0, 48.0, 37.0, 31.0, 42.0, 46.0 |
| altitude | int64 | 0 | 0 | 3 | 1199, 1233, 1191 |
| greenness | int64 | 0 | 0 | 3 | 4374, 6340, 5865 |
| landform_270m | int64 | 0 | 0 | 3 | 14, 28, -11 |
| population | int64 | 0 | 0 | 3 | 6834, 8518, 4780 |
| dist_major_road | int64 | 0 | 0 | 3 | 130, 475, 500 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1.961 | -0.26 | 1220.13 | 0.384 | log | 107759 | 103209 | lognormal |

### Numeric features

<details>
<summary>Show the table (14 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| pm2_5 | 10810 | 51.7132 | 34.612 | 0.567273 | 335.433 |
| pm10 | 10810 | 59.9882 | 38.2329 | 0.595909 | 407.714 |
| s2_pm2_5 | 10312 | 50.651 | 33.3751 | 0.590682 | 330.275 |
| s2_pm10 | 10312 | 59.6656 | 37.7118 | 0.78 | 384.627 |
| humidity | 10823 | 0.824704 | 0.135332 | 0.307167 | 1 |
| temp | 10811 | 21.9638 | 2.8067 | 16.175 | 30.7818 |
| lat | 10828 | 0.313923 | 0.0166933 | 0.299255 | 0.333501 |
| long | 10828 | 32.5883 | 0.0137744 | 32.5686 | 32.6095 |
| altitude | 10828 | 1207.56 | 16.3666 | 1191 | 1233 |
| greenness | 10828 | 5160.28 | 906.626 | 4374 | 6340 |
| landform_270m | 10828 | 14.2835 | 12.2235 | -11 | 28 |
| population | 10828 | 7010.35 | 1188.22 | 4780 | 8518 |
| dist_major_road | 10828 | 284.151 | 175.508 | 130 | 500 |
| ref_pm2_5 | 10828 | 53.2955 | 34.9304 | 0.2 | 459 |

</details>

### Categorical features

| column | rank | value | count | pct |
|---|---|---|---|---|
| created_at | 1 | 2021-01-31 01:00:00+03:00 | 3 | 0.03 |
| created_at | 2 | 2021-01-30 22:00:00+03:00 | 3 | 0.03 |
| created_at | 3 | 2021-01-30 21:00:00+03:00 | 3 | 0.03 |
| created_at | 4 | 2020-10-04 17:00:00+03:00 | 3 | 0.03 |
| created_at | 5 | 2021-01-30 20:00:00+03:00 | 3 | 0.03 |
| landform_90m | 1 | Upper slope (warm) | 9212 | 85.08 |
| landform_90m | 2 | Lower slope (warm) | 1616 | 14.92 |
| site | 1 | USEmbassy | 6107 | 56.4 |
| site | 2 | Makerere | 3105 | 28.68 |
| site | 3 | Nakawa | 1616 | 14.92 |

## Build

| field | value |
|---|---|
| uuid | 01a21800-ad9e-73d9-a085-fce439694fdb |
| checksum | v2:a6df0030463bd95255b326c4b74397d51feed953b9b28c676e30d68da4a29ca2 |
| built_at | 2026-11-26T13:17:08+00:00 |
| path | airqo_low_cost_air_quality_monitor_calibration_challenge/01a21800-ad9e-73d9-a085-fce439694fdb |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
