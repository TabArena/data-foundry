---
report_format: data-foundry-report-v2
unique_name: ashrae_great_energy_predictor_iii_1m
container_format: 2
checksum: v2:906fb334403c1228bf8885a726a057a06832b83c17ccb985180e3fa81e769742
build:
  uuid: 01a217f7-4633-7434-88dd-e6f961ffc4b5
  checksum: v2:906fb334403c1228bf8885a726a057a06832b83c17ccb985180e3fa81e769742
  built_at: '2026-11-26T13:08:43+00:00'
  path: ashrae_great_energy_predictor_iii_1m/01a217f7-4633-7434-88dd-e6f961ffc4b5
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
  n_rows: 32926795
  n_features: 15
  dtypes:
    category: 4
    datetime64[ns]: 1
    float64: 10
    int64: 1
  n_test_dataset_rows: null
task:
  target: log1p_meter_reading
  problem_type: regression
  metric: rmsle
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
  time_horizon: 4
  time_horizon_unit: months
  time_gap: null
  time_gap_unit: null
  reason: 'Three test windows of 4 months tile 2017, the competition''s first test
    year: September-December, May-August and January-April 2017, newest first; train
    is all earlier hours. The newest window always stays, and at 4 months January-April
    and May-August are the only two windows that overlap neither it nor each other,
    so the three windows test each season once (kept by the curator on 2026-11-10).

    A window is the horizon: a savings baseline is fit once on the year before a retrofit
    and predicts the year or two after it without a refit (the competition trained
    on 2016 to predict 2017 and 2018, GEPIII overview, Miller et al. 2020, Sec. 2.2;
    CalTRACK, Sec. 3.1.3 and 3.6.1.1; LBNL''s NMEC guidance v2.0, p. 10), so the window
    is the longest that gives three windows inside 2017: four months. Windows of 3
    or 2 months would fit (9 and 10 candidates above the floor) but score a model
    refit more often, an easier task than the use case.

    The oldest window trains on 2016 alone: 50.07% of the hours (8,784 of 17,544)
    but 49.47% of the rows (19,325,311 of 39,062,170), as 2016 has more gaps and drops
    (site 0''s recording gap). We keep it under the floor''s amendment of 2026-11-08:
    the two newer windows train on 66.0% and 83.0% of the rows, and an older window
    may train on 40% or more when most test entities recur; here every test meter''s
    building is in training, and folds by entity would test unseen buildings. LightGBM
    (one seed, default parameters with 1,000 trees and early stopping on the last
    10% of each train sample in time order, fit on the default 1M sample of the newest
    year before each window, the date in the recommended encoding) scores RMSLE 1.212,
    1.342 and 1.213, newest first: 1.277 on the two valid windows and 1.256 on all
    three. The oldest window scores like the newest and moves the mean by about 0.02;
    the direction comes from May-August, which the absolute date features (year, total
    seconds) make harder: without them the scores are 1.240, 1.176 and 1.247 (1.208
    on the two valid windows, 1.221 on all three).'
  n_train:
    min: 19325311
    max: 32426795
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
    splits_train_under_half: 'Signed off (Lennart, 2026-11-10): January-April 2017
      trains on 49.47% of the readings, beside 66.0% and 83.0%; kept as the curator''s
      exception to SPLIT-14''s half-data floor (Andrej, 2026-11-19).'
decisions:
- Weather shifted from UTC to the sites' local time
- Readings taken in kWh from BDG2
- Hours a meter did not record dropped
- Zeros of the thermal meters outside their season kept
---

# ashrae_great_energy_predictor_iii_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `log1p_meter_reading`, scored with `rmsle` on temporal splits by `timestamp`. 32,926,795 rows and 15 features. Source: Kaggle (2019).

Built as `01a217f7-4633-7434-88dd-e6f961ffc4b5` on 2026-11-26. See [Build](#build).

## In brief

**Question.** How much energy would a building's meter have used in a given hour, given the building, the time and the weather?

**Use case.** After an energy-efficiency retrofit, an engineer or investor estimates what the building would have used without it, from a model fit on the readings before, and credits the difference as savings (the competition's purpose).

**One row.** One hourly reading of one meter (electricity, chilled water, steam or hot water) of one building of the competition, 2016-2017; of the 39.1M readings, the splits use every one before September 2017 and 500,000 of September-December 2017.

**Predicted.** The meter's reading in that hour in kWh (the heating and cooling meters converted to kWh by the competition's organisers), scored on a logarithmic scale as in the competition.

**Known at prediction time.** The building (site, primary use, floor area, year built, floors), the meter type, the local date and hour, and the site's weather in that hour (temperature, dew point, cloud, rain, pressure, wind); no reading after the cutoff.

**What the test data stands for.** Three four-month windows tile 2017, newest first, each trained on all earlier readings, of which a benchmark fits on a random million of the newest year. A savings baseline is fit once and used for a year or more without a refit, so the window is the longest that gives three windows inside 2017; the oldest trains on 2016 alone, just under half the readings.

**Our changes to the source.** We add the competition's 2017 readings, which its organisers released later with every meter in kWh, to split by time and to put all meters in one unit. Hours when a meter was not recording are dropped, as the top teams did: electricity at 0, a heating or cooling plant at 0 for two days in its season, a reading stuck for a week, and one steam meter's unit error.

> **Use case fit: direct (the rows, features and split mirror the use case).** As in measuring retrofit savings, the model sees only the building, the time and the observed weather of each hour, never a later reading, and is fit on earlier readings. Hours when a meter did not record are dropped, as the savings would be measured on recorded hours only; the noise of real meters stays.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/ashrae_great_energy_predictor_iii.md`](../../../../curation/records/ashrae_great_energy_predictor_iii.md)
- The original source: <https://www.kaggle.com/competitions/ashrae-energy-prediction>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/ashrae_great_energy_predictor_iii/`. To get them:

```text
We download four files of the Kaggle competition (train.csv holds 2016) and, from the Building Data Genome
Project 2 (BDG2) repository of the competition's technical team, the competition's 2017 readings
(kaggle.csv, sha256 67e6d3e82cc737d28389845fc5e526711705fc264fd178a7a0b6f8f3d8d3c82e), the raw meter files
with every reading in kWh (one per meter type) and the building metadata that maps BDG2's building names to
the competition's building_id. The files are Git LFS objects, pinned to the commit that added kaggle.csv. The
competition's 2018 readings (its private test year) are not public.

mkdir -p local-data-warehouse/ashrae_great_energy_predictor_iii && cd local-data-warehouse/ashrae_great_energy_predictor_iii
for f in train.csv weather_train.csv weather_test.csv building_metadata.csv; do kaggle competitions download -c ashrae-energy-prediction -f $f -p .; done
unzip train.csv.zip && unzip weather_train.csv.zip && unzip weather_test.csv.zip && rm train.csv.zip weather_train.csv.zip weather_test.csv.zip
BDG2=https://media.githubusercontent.com/media/buds-lab/building-data-genome-project-2/9581aafed95b28e3d5ac39929c15fbc0ba36af5b/data
mkdir -p bdg2/raw && wget -O bdg2/kaggle.csv $BDG2/meters/kaggle/kaggle.csv && wget -O bdg2/metadata.csv $BDG2/metadata/metadata.csv
for m in electricity chilledwater steam hotwater; do wget -O bdg2/raw/$m.csv $BDG2/meters/raw/$m.csv; done
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/ashrae_great_energy_predictor_iii_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/ashrae_great_energy_predictor_iii_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/competitions/ashrae-energy-prediction |
| year | 2019 |
| domain | environmental science & climate |
| license | Kaggle Competition Rules (7A: use for any purpose, commercial or non-commercial; 7B: no redistribution to anyone not participating in the competition); the 2017 readings and the readings in kWh from BDG2: MIT License at the pinned commit (2020), CC BY 4.0 on its Zenodo release v1.0 (doi 10.5281/zenodo.3887306), and a LICENSE headed 'Attribution-ShareAlike 4.0 Unported' in the repository since 2023-10-14 |
| data_tags | Non-IID, Temporal |
| reference | Howard2019ASHRAEGreatEnergyPredictorIII,Miller2020GEPIII,Miller2020BDG2 |
| rows x columns | 32,926,795 x 16 |
| task.target | log1p_meter_reading |
| task.problem_type | regression |
| task.metric | rmsle |
| task.split_regime | temporal_non_iid |
| task.time_on | timestamp |

**Metric**

| field | value |
|---|---|
| name | `rmsle` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | RMSLE (Root Mean Squared Logarithmic Error) |
| reference | https://www.kaggle.com/competitions/ashrae-energy-prediction/overview/evaluation |
| definition | sqrt(mean((log1p(pred) - log1p(actual))^2)) of kWh over all meter-hours, computed after the inverse of our log1p_meter_reading target. |
| target scale | ships on the `log1p` scale for modelling; scored on the original scale after the inverse of `log1p` |

<details>
<summary>Feature types: 4 categorical, 0 string, 1 datetime</summary>

- categorical (4): `building_id`, `meter`, `site_id`, `primary_use`
- string (0): none
- datetime (1): `timestamp`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{Howard2019ASHRAEGreatEnergyPredictorIII,
  author = {Addison Howard and Chris Balbach and Clayton Miller and Jeff Haberl and Krishnan Gowri and Sohier Dane},
  title = {ASHRAE - Great Energy Predictor III},
  year = {2019},
  howpublished = {\url{https://kaggle.com/competitions/ashrae-energy-prediction}},
  note = {Kaggle competition}
}
@article{Miller2020GEPIII,
  author = {Clayton Miller and Pandarasamy Arjunan and Anjukan Kathirgamanathan and Chun Fu and Jonathan Roth and June Young Park and Chris Balbach and Krishnan Gowri and Zoltan Nagy and Anthony D. Fontanini and Jeff Haberl},
  title = {The {ASHRAE} Great Energy Predictor {III} competition: Overview and results},
  journal = {Science and Technology for the Built Environment},
  volume = {26},
  number = {10},
  pages = {1427--1447},
  year = {2020},
  doi = {10.1080/23744731.2020.1795514}
}
@article{Miller2020BDG2,
  author = {Clayton Miller and Anjukan Kathirgamanathan and Bianca Picchetti and Pandarasamy Arjunan and June Young Park and Zoltan Nagy and Paul Raftery and Brodie W. Hobson and Zixiao Shi and Forrest Meggers},
  title = {The Building Data Genome Project 2, energy meter data from the {ASHRAE} Great Energy Predictor {III} competition},
  journal = {Scientific Data},
  volume = {7},
  pages = {368},
  year = {2020},
  doi = {10.1038/s41597-020-00712-x}
}
```

</details>

## Sample rows

The first 5 of 32,926,795 rows of the final frame (the oldest rows: the frame is sorted by `timestamp`); 12 of 16 columns, the target first. Cells are cut at 40 characters.

| log1p_meter_reading | building_id | meter | timestamp | site_id | primary_use | square_feet | year_built | floor_count | air_temperature | cloud_coverage | dew_temperature |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7.52426 | 1203 | steam | 2016-01-01 00:00:00 | 13 | Lodging/residential | 138602 | nan | nan | -7.2 | 8 | -10.6 |
| 3.10785 | 1195 | electricity | 2016-01-01 00:00:00 | 13 | Office | 16472 | nan | nan | -7.2 | 8 | -10.6 |
| 6.14349 | 260 | chilledwater | 2016-01-01 00:00:00 | 2 | Education | 126985 | 1979 | nan | 7.2 | 0 | -5.6 |
| 2.35613 | 629 | electricity | 2016-01-01 00:00:00 | 4 | Education | 40835 | 1931 | 6 | 4.4 | 0 | -2.2 |
| 5.20056 | 1358 | steam | 2016-01-01 00:00:00 | 15 | Lodging/residential | 61439 | 1903 | nan | nan | nan | nan |

## Curation notes

We start with the Kaggle competition's train.csv (2016), building_metadata.csv and weather files and, from the BDG2 repository of its technical team, the 2017 readings (kaggle.csv), the raw meter files in kWh and their building metadata.

- Prediction point: after a cutoff, the model gives each known meter's reading for a later hour from the building's metadata, the meter type, the local time and the site's weather, as in the competition; no later reading is an input. The top five teams fit boosted trees and neural networks on these inputs, with no lagged readings (GEPIII overview, Table 2).
- Not a naive forecast: each meter's hour-of-week profile from the same month a year earlier scores RMSE 1.393 / 1.273 / 1.372 on the three windows, LightGBM with 1,000 trees on a random 1M of all earlier rows per window 1.261 / 1.176 / 1.223. One model per site does no better than one large model (1.238 / 1.178 / 1.222), so meter types and sites stay one task.
- We stack 2016 and 2017, the competition's public test year ("matches seamlessly with the training data", BDG2 paper, p. 8), keeping the hours with a reading; 2018 is not public.
- Units: the competition kept each site's own unit (ton-hours, pounds of steam, mmBTU, kBTU; BDG2 paper, Table 4). We take the readings in kWh from BDG2's raw files, converted and corrected by the same team (p. 8); per meter they differ from Kaggle's by one constant factor in 99.9% of the hours (decision table).
- The weather is in UTC and the readings in local time (p. 8): we shift it by the 1st place solution's offsets and join it on site and hour. Daylight saving time at 8 sites changed RMSE by -0.007 to +0.005 per window, so we keep standard time.
- Recording errors, removed as all top five teams did: site 0's electricity before 2016-05-21, electricity at 0, chilled water at 0 for 48 hours or more in May-October and steam or hot water in November-April, readings stuck for a week or more (site 5's electricity, March-November 2017), and building 1099's steam unit error (above 10 times its median, January-June 2016). 1.70M hours (4.2%, decision table).
- 94.5% of the 2016 hours we drop are on the 1st place team's hand-made list of bad readings, and they cover 64% of that list. Zeros of heating and cooling meters outside their season stay: a plant switched off, which a model can learn.
- The target is log1p of kWh, in one unit for all meters; the metric is the competition's RMSLE on kWh, computed after the inverse (`target_transform="log1p"`).
- building_id and site_id are categories: the test hours belong to meters seen in train, as in the competition.
- precip_depth_1_hr = -1 stays: it codes a trace of rain in NOAA's ISD-Lite data (format note, field 11).
- `cloud_coverage` is in oktas (0-8), and 9 means the sky is obscured (fog or precipitation), so the cloud
  amount cannot be estimated (ISD's code table): 9,905 rows, missing (CLEAN-10; the curator's marks of
  2026-10-31, as in rain_in_australia).
- The row budget: The cleaned frame has 39.1M hourly readings, so the dataset ships only as this `_1m` version. Each test window keeps at most 500k of its rows, drawn at random within the window (v2 split protocol), and each train side holds every earlier reading, so the container holds every reading before September 2017 and 500k of September-December 2017. The container records the 1M train budget, and a benchmark sub-samples each train side to 1M rows before a fit (`subsample_train`; by default a random 1M of the newest year before the window). A year covers every season, so the default sample keeps all seasons.

## Splits

Expanding-window temporal splits: 3 test window(s) of 4 months, starting at 2017-09-01, 2017-05-01, 2017-01-01, newest first; train is all earlier data. The test windows by `timestamp`, as listed: 2017-09-01 to 2017-12-31 (500,000 test, 32,426,795 train rows); 2017-05-01 to 2017-08-31 (500,000 test, 25,798,439 train rows); 2017-01-01 to 2017-04-30 (500,000 test, 19,325,311 train rows). Each test window keeps at most 500k of its rows, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows (by default rows drawn at random from the newest year before each window, extended back in time until it holds that many rows, `subsample_train`).

Three test windows of 4 months tile 2017, the competition's first test year: September-December, May-August and January-April 2017, newest first; train is all earlier hours. The newest window always stays, and at 4 months January-April and May-August are the only two windows that overlap neither it nor each other, so the three windows test each season once (kept by the curator on 2026-11-10).
A window is the horizon: a savings baseline is fit once on the year before a retrofit and predicts the year or two after it without a refit (the competition trained on 2016 to predict 2017 and 2018, GEPIII overview, Miller et al. 2020, Sec. 2.2; CalTRACK, Sec. 3.1.3 and 3.6.1.1; LBNL's NMEC guidance v2.0, p. 10), so the window is the longest that gives three windows inside 2017: four months. Windows of 3 or 2 months would fit (9 and 10 candidates above the floor) but score a model refit more often, an easier task than the use case.
The oldest window trains on 2016 alone: 50.07% of the hours (8,784 of 17,544) but 49.47% of the rows (19,325,311 of 39,062,170), as 2016 has more gaps and drops (site 0's recording gap). We keep it under the floor's amendment of 2026-11-08: the two newer windows train on 66.0% and 83.0% of the rows, and an older window may train on 40% or more when most test entities recur; here every test meter's building is in training, and folds by entity would test unseen buildings. LightGBM (one seed, default parameters with 1,000 trees and early stopping on the last 10% of each train sample in time order, fit on the default 1M sample of the newest year before each window, the date in the recommended encoding) scores RMSLE 1.212, 1.342 and 1.213, newest first: 1.277 on the two valid windows and 1.256 on all three. The oldest window scores like the newest and moves the mean by about 0.02; the direction comes from May-August, which the absolute date features (year, total seconds) make harder: without them the scores are 1.240, 1.176 and 1.247 (1.208 on the two valid windows, 1.221 on all three).

3 repeat(s) x 1 fold(s) with seed 4267; train 19,325,311 to 32,426,795 rows, test 500,000 rows. Prediction horizon: 4 months. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as rows.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 32426795 | 500000 | 2016-01-01 00:00:00 | 2017-08-31 23:00:00 | 2017-09-01 00:00:00 | 2017-12-31 23:00:00 |
| 1 | 0 | 25798439 | 500000 | 2016-01-01 00:00:00 | 2017-04-30 23:00:00 | 2017-05-01 00:00:00 | 2017-08-31 23:00:00 |
| 2 | 0 | 19325311 | 500000 | 2016-01-01 00:00:00 | 2016-12-31 23:00:00 | 2017-01-01 00:00:00 | 2017-04-30 23:00:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows ashrae_great_energy_predictor_iii_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Sep 2017 - Dec 2017 | 500000 | 0.985 | mean 4.572, median 4.443, p10 1.308, p90 7.399 | mean 4.623, median 4.49, p10 1.333, p90 7.486 | 0.065 | air_temperature (0.06), sea_level_pressure (0.05), dew_temperature (0.04) | 0 |
| 1 | May 2017 - Aug 2017 | 500000 | 0.784 | mean 4.706, median 4.487, p10 1.345, p90 7.822 | mean 4.598, median 4.466, p10 1.335, p90 7.441 | 1.427 | air_temperature (1.43), dew_temperature (0.89), sea_level_pressure (0.48) | 0 |
| 2 | Jan 2017 - Apr 2017 | 500000 | 0.587 | mean 4.629, median 4.524, p10 1.365, p90 7.361 | mean 4.594, median 4.467, p10 1.276, p90 7.445 | 0.476 | dew_temperature (0.48), air_temperature (0.33), sea_level_pressure (0.08) | 0 |

## Decisions

### 1. Weather shifted from UTC to the sites' local time

The weather files are in UTC and the meter readings in local time (BDG2 paper, p. 8). With the 1st place solution's offsets the mean day peaks at 14:00-16:00 local time at every site.

| site_id | utc_offset_hours | warmest_hour_utc | warmest_hour_local | coldest_hour_local |
|---|---|---|---|---|
| 0 | -5 | 19 | 14 | 6 |
| 1 | 0 | 14 | 14 | 5 |
| 2 | -7 | 23 | 16 | 6 |
| 3 | -5 | 20 | 15 | 5 |
| 4 | -8 | 22 | 14 | 5 |
| 5 | 0 | 14 | 14 | 5 |
| 6 | -5 | 20 | 15 | 6 |
| 7 | -5 | 20 | 15 | 5 |
| 8 | -5 | 19 | 14 | 6 |
| 9 | -6 | 21 | 15 | 6 |
| 10 | -7 | 22 | 15 | 6 |
| 11 | -5 | 20 | 15 | 5 |
| 12 | 0 | 14 | 14 | 4 |
| 13 | -6 | 21 | 15 | 5 |
| 14 | -5 | 20 | 15 | 5 |
| 15 | -5 | 20 | 15 | 5 |

### 2. Readings taken in kWh from BDG2

The competition kept each site's own unit; BDG2's raw files hold the same readings converted to kWh (paper, Tables 4 and 5). Meters per meter type by the factor between the two, named by the unit it implies; the ratio is the same within 0.1% for 99.9% of a meter's hours.

| unit in the competition data | electricity | chilledwater | steam | hotwater |
|---|---|---|---|---|
| kBTU | 105 | 32 | 0 | 11 |
| kWh | 1296 | 4 | 12 | 20 |
| lb of steam | 0 | 0 | 312 | 0 |
| mmBTU | 0 | 86 | 0 | 112 |
| other: kWh x 3 | 0 | 1 | 0 | 0 |
| other: kWh x 3,600 | 12 | 15 | 0 | 0 |
| ton-hours | 0 | 360 | 0 | 2 |

### 3. Hours a meter did not record dropped

Hours with a reading per meter type and the hours each rule flags (a row can match several rules): site 0's 2016 gap, electricity at 0, a cooling or heating plant at 0 for 48 hours or more in its operating months, a reading repeated for a week or more, and building 1099's steam unit error.

| meter | hours_with_a_reading | site_0_gap | electricity_zero | plant_zero_in_season | stuck_for_a_week | unit_error | dropped |
|---|---|---|---|---|---|---|---|
| electricity | 24237933 | 348560 | 691763 | 0 | 525863 | 0 | 1221609 |
| chilledwater | 8494182 | 0 | 0 | 169893 | 34637 | 0 | 204530 |
| steam | 5505619 | 0 | 0 | 78420 | 24314 | 3332 | 106066 |
| hotwater | 2525586 | 0 | 0 | 135093 | 33852 | 0 | 168945 |

### 4. Zeros of the thermal meters outside their season kept

Chilled-water zeros peak in winter and steam and hot-water zeros in summer: a plant switched off for the season, which a model can learn. Share of shipped rows with a reading of 0, by month and meter type.

| month | chilledwater | electricity | hotwater | steam |
|---|---|---|---|---|
| 1 | 0.269 | 0 | 0.071 | 0.032 |
| 2 | 0.252 | 0 | 0.092 | 0.039 |
| 3 | 0.228 | 0 | 0.11 | 0.05 |
| 4 | 0.171 | 0 | 0.137 | 0.067 |
| 5 | 0.055 | 0 | 0.329 | 0.136 |
| 6 | 0.035 | 0 | 0.391 | 0.18 |
| 7 | 0.036 | 0 | 0.409 | 0.197 |
| 8 | 0.03 | 0 | 0.413 | 0.179 |
| 9 | 0.037 | 0 | 0.387 | 0.162 |
| 10 | 0.068 | 0 | 0.374 | 0.165 |
| 11 | 0.193 | 0 | 0.121 | 0.055 |
| 12 | 0.252 | 0 | 0.087 | 0.031 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicates_skipped`: Skipped duplicate-column/row checks: 526,828,720 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to run them; nothing else checks duplicate rows and columns.)

Accepted on purpose:

- `splits_train_under_half`: Signed off (Lennart, 2026-11-10): January-April 2017 trains on 49.47% of the readings, beside 66.0% and 83.0%; kept as the curator's exception to SPLIT-14's half-data floor (Andrej, 2026-11-19).

## Data checks

### Feature summary

<details>
<summary>Show the table (16 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| building_id | category | 0 | 0 | 1449 | 1298, 1259, 1301, 1295, 1297, 1294, 1249, 1296, 1241, 1293 |
| meter | category | 0 | 0 | 4 | electricity, chilledwater, steam, hotwater |
| site_id | category | 0 | 0 | 16 | 13, 9, 2, 14, 3, 15, 0, 4, 6, 5 |
| primary_use | category | 0 | 0 | 16 | Education, Office, Entertainment/public assembly, Lodging/residential, Public s… |
| timestamp | datetime64\[ns\] | 0 | 0 | 17544 | 2017-01-02 03:00:00, 2016-11-06 10:00:00, 2016-06-13 08:00:00, 2017-08-17 01:00… |
| floor_count | float64 | 2.75426e+07 | 83.65 | 18 | 1.0, 2.0, 4.0, 3.0, 6.0, 5.0, 8.0, 7.0, 9.0, 11.0 |
| year_built | float64 | 1.99284e+07 | 60.52 | 116 | 1976.0, 1964.0, 2006.0, 1966.0, 1975.0, 1967.0, 1968.0, 2007.0, 1970.0, 1960.0 |
| cloud_coverage | float64 | 1.48092e+07 | 44.98 | 9 | 0.0, 2.0, 4.0, 6.0, 8.0, 7.0, 1.0, 3.0, 5.0 |
| precip_depth_1_hr | float64 | 5.89173e+06 | 17.89 | 167 | 0.0, -1.0, 3.0, 5.0, 8.0, 10.0, 13.0, 15.0, 2.0, 18.0 |
| wind_direction | float64 | 2.42068e+06 | 7.35 | 59 | 0.0, 300.0, 170.0, 290.0, 180.0, 310.0, 270.0, 160.0, 280.0, 190.0 |
| sea_level_pressure | float64 | 1.74634e+06 | 5.3 | 756 | 1015.9, 1015.2, 1015.6, 1016.2, 1016.4, 1016.0, 1016.3, 1015.5, 1014.9, 1015.8 |
| wind_speed | float64 | 231991 | 0.7 | 73 | 0.0, 2.1, 2.6, 1.5, 3.1, 3.6, 4.1, 4.6, 5.1, 5.7 |
| dew_temperature | float64 | 167814 | 0.51 | 553 | 13.3, 13.9, 10.0, 15.0, 12.8, 17.8, 15.6, 14.4, 18.3, 22.2 |
| air_temperature | float64 | 152097 | 0.46 | 646 | 22.8, 23.3, 24.4, 25.0, 23.9, 25.6, 20.0, 21.7, 22.2, 15.0 |
| log1p_meter_reading | float64 | 0 | 0 | 4.51906e+06 | 0.0, 2.4984, 3.0445, 6.7568, 2.1332, 2.4188, 3.434, 3.2581, 7.4494, 2.2377 |
| square_feet | int64 | 0 | 0 | 1397 | 150695, 387638, 64583, 200933, 42755, 72958, 65000, 171084, 71088, 62242 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 5.92 | 0.767 | -1.229 | 6.949 | 0.338 | log1p | 1.60505e+07 | 5.64343e+07 | exponential |

### Numeric features

<details>
<summary>Show the table (11 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| square_feet | 3.29268e+06 | 108740 | 117576 | 283 | 875000 |
| year_built | 1.29922e+06 | 1967.66 | 30.5003 | 1900 | 2017 |
| floor_count | 538252 | 4.28306 | 4.03004 | 1 | 26 |
| air_temperature | 3.27755e+06 | 16.2616 | 11.0487 | -28.9 | 48.3 |
| cloud_coverage | 1.81135e+06 | 1.92629 | 2.36658 | 0 | 8 |
| dew_temperature | 3.27603e+06 | 7.92625 | 10.2582 | -35 | 26.7 |
| precip_depth_1_hr | 2.70323e+06 | 0.850614 | 7.91817 | -1 | 597 |
| sea_level_pressure | 3.1179e+06 | 1015.62 | 7.29363 | 968.2 | 1050.1 |
| wind_direction | 3.05071e+06 | 174.362 | 113.062 | 0 | 360 |
| wind_speed | 3.2696e+06 | 3.42438 | 2.2665 | 0 | 24.2 |
| log1p_meter_reading | 3.29268e+06 | 4.61667 | 2.63613 | 0 | 16.2398 |

</details>

### Categorical features

<details>
<summary>Show the table (24 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| building_id | 1 | 1298 | 5956 | 0.18 |
| building_id | 2 | 1259 | 5923 | 0.18 |
| building_id | 3 | 1301 | 5888 | 0.18 |
| building_id | 4 | 1295 | 5792 | 0.18 |
| building_id | 5 | 1297 | 5790 | 0.18 |
| meter | 1 | electricity | 1938077 | 58.86 |
| meter | 2 | chilledwater | 698778 | 21.22 |
| meter | 3 | steam | 455594 | 13.84 |
| meter | 4 | hotwater | 200231 | 6.08 |
| primary_use | 1 | Education | 1320330 | 40.1 |
| primary_use | 2 | Office | 719680 | 21.86 |
| primary_use | 3 | Entertainment/public assembly | 368941 | 11.2 |
| primary_use | 4 | Lodging/residential | 351392 | 10.67 |
| primary_use | 5 | Public services | 276591 | 8.4 |
| site_id | 1 | 13 | 449630 | 13.66 |
| site_id | 2 | 9 | 445383 | 13.53 |
| site_id | 3 | 2 | 410619 | 12.47 |
| site_id | 4 | 14 | 407036 | 12.36 |
| site_id | 5 | 3 | 397544 | 12.07 |
| timestamp | 1 | 2017-01-02 03:00:00 | 292 | 0.01 |
| timestamp | 2 | 2016-11-06 10:00:00 | 286 | 0.01 |
| timestamp | 3 | 2016-06-13 08:00:00 | 280 | 0.01 |
| timestamp | 4 | 2017-08-17 01:00:00 | 279 | 0.01 |
| timestamp | 5 | 2017-02-26 13:00:00 | 277 | 0.01 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a217f7-4633-7434-88dd-e6f961ffc4b5 |
| checksum | v2:906fb334403c1228bf8885a726a057a06832b83c17ccb985180e3fa81e769742 |
| built_at | 2026-11-26T13:08:43+00:00 |
| path | ashrae_great_energy_predictor_iii_1m/01a217f7-4633-7434-88dd-e6f961ffc4b5 |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
