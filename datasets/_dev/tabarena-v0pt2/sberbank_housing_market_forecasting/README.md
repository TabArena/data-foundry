---
report_format: data-foundry-report-v2
unique_name: sberbank_housing_market_forecasting
container_format: 2
checksum: v2:7a7d99420a9b7a80146738e44a08debb9b78439e475db65ac6fc67c6beed7c26
build:
  uuid: 01a21800-0ccc-7c5e-8046-df2c8f33cff1
  checksum: v2:7a7d99420a9b7a80146738e44a08debb9b78439e475db65ac6fc67c6beed7c26
  built_at: '2026-11-26T13:16:31+00:00'
  path: sberbank_housing_market_forecasting/01a21800-0ccc-7c5e-8046-df2c8f33cff1
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
  n_rows: 28321
  n_features: 386
  dtypes:
    category: 23
    datetime64[ns]: 1
    float32: 3
    float64: 207
    int64: 153
  n_test_dataset_rows: null
task:
  target: price_doc
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
  n_repeats: 9
  n_folds: 1
  random_state: 4267
  time_horizon: 1
  time_horizon_unit: months
  time_gap: null
  time_gap_unit: null
  reason: 'Nine test windows of one calendar month (Andrej, 2026-11-19); each trains
    on every earlier

    sale, with no gap. The use case (a lender values a flat at its sale) ties no window
    length and no source gives

    Sberbank''s refit cadence: the sources fix only benchmark test periods for one
    frozen model (TabReD seven

    months, 1 December 2014 to 30 June 2015; the competition the eleven months after
    its training data, July 2015

    to May 2016). So the windows follow the count: half the sales lie before 21 February
    2014, so a window trains

    on half or more only from March 2014, and one calendar month is the simplest length
    that fits nine windows

    above half into March 2014 to June 2015. The windows hold 2015 with 394 to 724

    sales a month, the rush of December 2014 (the month the ruble fell) and the busy
    2014 at 771 to 1,214 a month.

    No gap: a sale''s price is known when it is signed, and the economic statistics
    are already read one period

    back for their release delay.'
  n_train:
    min: 14407
    max: 27927
  n_test:
    min: 394
    max: 1583
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  - dataset_conflicting_duplicate_rows
  accepted:
    splits_feature_missing_in_test: 'Decided (Lennart, 2026-11-11): three one-year
      lags of macro columns the source gives for some years only (curation_comments).'
    time_newest_period_short: 'Decided (Lennart, 2026-11-11): 2015 holds 394 to 724
      sales a month against 1,044 to 1,583 from September to December 2014, the market
      after the December 2014 rush; the data ends where the competition''s training
      file ends, 30 June 2015, not at a download cut.'
decisions: []
---

# sberbank_housing_market_forecasting

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `price_doc`, scored with `rmse` on temporal splits by `timestamp`. 28,321 rows and 386 features. Source: Kaggle (2017).

Built as `01a21800-0ccc-7c5e-8046-df2c8f33cff1` on 2026-11-26. See [Build](#build).

## In brief

**Question.** What will a Moscow flat sell for, per square metre?

**Use case.** Sberbank predicts the price of a flat when it is sold, so that renters, developers and lenders can be more confident when they sign (the Kaggle competition's purpose).

**One row.** One sale of a flat in Moscow, August 2011 to June 2015 (28,321 sales), either an owner-occupier purchase or an investment.

**Predicted.** The sale price per square metre of total area, on a logarithmic scale.

**Known at prediction time.** The flat (areas, floor, number of floors, rooms, build year, material, condition, purchase type), its district's population, schools, facilities, ecology and distances to points of interest, the market prices of the sale date (exchange rates, oil, stock indices) and the monthly, quarterly and yearly economic statistics of one period before it.

**What the test data stands for.** Nine test windows of one calendar month, newest first: June, April and February 2015, December, October, August, June, April and March 2014; each trains on every earlier sale (51% to 99% of the sales).

**Our changes to the source.** Following the TabReD benchmark, the target is the price per square metre, and we drop sales at prices up to 1 million rubles or of exactly 2 or 3 million, and flats of 5 square metres or less. The economic statistics are those of the month, quarter or year before the sale, not of the sale's own period.

> **Use case fit: direct (the rows, features and split mirror the use case).** The flat's and district's figures are known at the sale, and later months stand for the sales to come; the use case ties no window length, so the one-month windows are ours. The economic statistics are lagged one period, as their release dates are not given; a monthly figure may still come out days after a sale. The neighbourhood figures are one read of unknown date, kept.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |
| [`BAD_ADDRESS_FIX.xlsx`](BAD_ADDRESS_FIX.xlsx) | Read by `dataset.py`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/sberbank_housing_market_forecasting.md`](../../../../curation/records/sberbank_housing_market_forecasting.md)
- The original source: <https://www.kaggle.com/competitions/sberbank-russian-housing-market>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/sberbank_housing_market_forecasting/`. To get them:

```text
We use the data from Kaggle:

kaggle competitions download -c sberbank-russian-housing-market
mkdir -p local-data-warehouse/sberbank_housing_market_forecasting && mv sberbank-russian-housing-market.zip local-data-warehouse/sberbank_housing_market_forecasting/ && cd local-data-warehouse/sberbank_housing_market_forecasting/ && unzip sberbank-russian-housing-market.zip && rm test.csv.zip sample_submission.csv.zip data_dictionary.txt sberbank-russian-housing-market.zip
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/sberbank_housing_market_forecasting   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/sberbank_housing_market_forecasting   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/competitions/sberbank-russian-housing-market |
| year | 2017 |
| domain | business & marketing |
| license | Kaggle Competition Rules |
| data_tags | Non-IID, Temporal, Spatial |
| reference | Matveev2017SberbankRussianHousingMarket |
| rows x columns | 28,321 x 387 |
| task.target | price_doc |
| task.problem_type | regression |
| task.metric | rmse |
| task.split_regime | temporal_non_iid |
| task.time_on | timestamp |

**Metric**

| field | value |
|---|---|
| name | `rmse` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | Root Mean Squared Logarithmic Error (RMSLE) on price_doc |
| reference | https://www.kaggle.com/competitions/sberbank-russian-housing-market/overview/evaluation |
| definition | RMSE on log(price_doc / full_sq); since full_sq is known per row, log(price/sq) - log(price_hat/sq) = log(price) - log(price_hat), so this is the competition's RMSLE on the sale price up to log vs log1p (negligible at prices of 10^5 to 10^8 RUB) |

<details>
<summary>Feature types: 22 categorical, 1 ordinal, 0 string, 0 datetime</summary>

- categorical (22): `ID_metro`, `ID_railroad_station_walk`, `ID_railroad_station_avto`, `ID_big_road1`, `ID_big_road2`, `ID_railroad_terminal`, `ID_bus_terminal`, `material`, `sub_area`, `product_type`, `culture_objects_top_25`, `thermal_power_plant_raion`, `incineration_raion`, `oil_chemistry_raion`, `radiation_raion`, `railroad_terminal_raion`, `big_market_raion`, `nuclear_reactor_raion`, `detention_facility_raion`, `water_1line`, `big_road1_1line`, `railroad_1line`
- ordinal (1): `ecology (poor < satisfactory < good < excellent)`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{Matveev2017SberbankRussianHousingMarket,
  author = {Alex Matveev and Anastasia Sidorova and DataCanary},
  title  = {Sberbank Russian Housing Market},
  year   = {2017},
  howpublished = {\url{https://kaggle.com/competitions/sberbank-russian-housing-market}},
  note   = {Kaggle competition}
}
```

</details>

## Sample rows

The first 5 of 28,321 rows of the final frame (the oldest rows: the frame is sorted by `timestamp`); 12 of 387 columns, the target first. Cells are cut at 40 characters.

| price_doc | timestamp | full_sq | life_sq | floor | max_floor | material | build_year | num_room | kitch_sq | state | product_type |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 11.8208 | 2011-08-20 00:00:00 | 43 | 27 | 4 | nan | nan | nan | nan | nan | nan | Investment |
| 12.0809 | 2011-08-23 00:00:00 | 34 | 19 | 3 | nan | nan | nan | nan | nan | nan | Investment |
| 11.7948 | 2011-08-27 00:00:00 | 43 | 29 | 2 | nan | nan | nan | nan | nan | nan | Investment |
| 11.8995 | 2011-09-01 00:00:00 | 89 | 50 | 9 | nan | nan | nan | nan | nan | nan | Investment |
| 12.2648 | 2011-09-05 00:00:00 | 77 | 77 | 4 | nan | nan | nan | nan | nan | nan | Investment |

## Curation notes

We follow the preprocessing from TabRed (https://github.com/yandex-research/tabred/tree/main/preprocessing#sberbank-housing-market-forecasting).

- The target is log(price_doc / full_sq), the log of the sale price per square metre of total area (TabReD,
  after the first-place solution); RMSE on it is the competition's RMSLE on `price_doc` (TP-6).
- Address fix: 603 sales whose address could not be located carry the distances of central Moscow (the
  smallest `kremlin_km`). The hosts posted location features for 550 of them in Kaggle discussion 34364
  (BAD_ADDRESS_FIX.xlsx, taken from the nearest known building); we apply them and drop the other 53.
- As TabReD, we drop sales at 1 million rubles or less or at exactly 2 or 3 million (fake low prices, by the
  first-place report often set to avoid tax), and flats with a total area of 5 m2 or less or of 5326 m2 (a
  typo for 53).
- We join macro.csv on the sale date. Market prices (exchange rates, oil, stock indices) are daily and keep the
  sale date's value. The monthly, quarterly and yearly statistics hold their own period's value from its first
  day (published later; the source gives no release dates), so we read them one period before the sale, as
  mortgage lags its macro series to their release (LEAK-10; Lennart, 2026-10-21): 20 monthly columns one
  month back (`_lag_1m`), 5 quarterly one quarter back (`_lag_1q`) and 64 yearly one year back (`_lag_1y`).
  `gdp_quart` already holds the previous quarter, so the model sees GDP two quarters back; `gdp_annual` and
  `gdp_annual_growth` already hold the previous year (a 2014 sale has Russia's 2013 GDP) and are kept as
  joined.
- We drop two duplicated columns with the same values as other columns: "0_6_all", "7_14_all"
- We drop the ID column as it does not provide information.
- Note, the dataset contains a lot of spatial feature and even more already decoded spatial information (like distances to various points of interest).
- We keep the 1,126 sales whose build_year is later than the year of sale (Lennart, 2026-10-14; until then they were dropped as errors). 1,124 were sold 0 to 4 years before it, which fits flats sold before completion; 2 have a build_year coded from a range (such as 20052009), kept as it is.
- Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
  categories in the order of the source's codebook (`ORDINAL_LEVELS`); codes that mean unknown are missing
  (CLEAN-10).
- Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
  each level is carries the words, a score without them is a number): 1 unordered codes carry their words:
  `material`; 1 scores with no words per level are numbers (`SCORES`): `state`.
- Test windows (Andrej, 2026-11-19): nine windows of one calendar month, every one training
  on more than half the sales, in place of three seven-month windows (Lennart, 2026-11-11) whose oldest,
  October 2013 to April 2014, trained on 35.4%; the use case ties no length, and no source gives Sberbank's
  refit cadence (splits comment).
- Potential leak, kept on purpose (Andrej, 2026-11-11): the district statistics and the neighbourhood features
  (distances, counts of facilities nearby) are one read of a date the source does not give: none of 145
  districts and none of 2,991 buildings sold in more than one year changes in them over 2011-2015, while the
  city opened new metro stations (2014-2015) and other facilities. Older sales may carry facilities that came
  after them. They stay: the read cannot be dated row by row and the data owner released it for its
  competition. Revisit if dated district statistics are found.
- Columns recorded on one side of a window only (Lennart, 2026-11-11): the macro file gives `provision_retail_space_sqm` for 2011 and 2012 only and the two education shares (`modern_education_share`, `old_education_build_share`) from 2013 on, so their one-year lags are recorded in 2012-2013 and from 2014: the newest windows test without the first, and the oldest trains without the other two. Kept: the data as published.

## Splits

Expanding-window temporal splits: 9 test window(s) of 1 month, starting at 2015-06-01, 2015-04-01, 2015-02-01, 2014-12-01, 2014-10-01, 2014-08-01, 2014-06-01, 2014-04-01, 2014-03-01, newest first; train is all earlier data. The test windows by `timestamp`, as listed: 2015-06-01 to 2015-06-30 (394 test, 27,927 train rows); 2015-04-01 to 2015-04-30 (724 test, 26,687 train rows); 2015-02-02 to 2015-02-28 (451 test, 25,651 train rows); 2014-12-01 to 2014-12-31 (1,583 test, 23,674 train rows); 2014-10-01 to 2014-10-31 (1,044 test, 21,466 train rows); 2014-08-01 to 2014-08-30 (771 test, 19,646 train rows); 2014-06-02 to 2014-06-30 (1,179 test, 17,790 train rows); 2014-04-01 to 2014-04-30 (1,214 test, 15,524 train rows); 2014-03-01 to 2014-03-31 (1,117 test, 14,407 train rows).

Nine test windows of one calendar month (Andrej, 2026-11-19); each trains on every earlier
sale, with no gap. The use case (a lender values a flat at its sale) ties no window length and no source gives
Sberbank's refit cadence: the sources fix only benchmark test periods for one frozen model (TabReD seven
months, 1 December 2014 to 30 June 2015; the competition the eleven months after its training data, July 2015
to May 2016). So the windows follow the count: half the sales lie before 21 February 2014, so a window trains
on half or more only from March 2014, and one calendar month is the simplest length that fits nine windows
above half into March 2014 to June 2015. The windows hold 2015 with 394 to 724
sales a month, the rush of December 2014 (the month the ruble fell) and the busy 2014 at 771 to 1,214 a month.
No gap: a sale's price is known when it is signed, and the economic statistics are already read one period
back for their release delay.

9 repeat(s) x 1 fold(s) with seed 4267; train 14,407 to 27,927 rows, test 394 to 1,583 rows. Prediction horizon: 1 months.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 27927 | 394 | 2011-08-20 00:00:00 | 2015-05-30 00:00:00 | 2015-06-01 00:00:00 | 2015-06-30 00:00:00 |
| 1 | 0 | 26687 | 724 | 2011-08-20 00:00:00 | 2015-03-31 00:00:00 | 2015-04-01 00:00:00 | 2015-04-30 00:00:00 |
| 2 | 0 | 25651 | 451 | 2011-08-20 00:00:00 | 2015-01-31 00:00:00 | 2015-02-02 00:00:00 | 2015-02-28 00:00:00 |
| 3 | 0 | 23674 | 1583 | 2011-08-20 00:00:00 | 2014-11-29 00:00:00 | 2014-12-01 00:00:00 | 2014-12-31 00:00:00 |
| 4 | 0 | 21466 | 1044 | 2011-08-20 00:00:00 | 2014-09-30 00:00:00 | 2014-10-01 00:00:00 | 2014-10-31 00:00:00 |
| 5 | 0 | 19646 | 771 | 2011-08-20 00:00:00 | 2014-07-31 00:00:00 | 2014-08-01 00:00:00 | 2014-08-30 00:00:00 |
| 6 | 0 | 17790 | 1179 | 2011-08-20 00:00:00 | 2014-05-31 00:00:00 | 2014-06-02 00:00:00 | 2014-06-30 00:00:00 |
| 7 | 0 | 15524 | 1214 | 2011-08-20 00:00:00 | 2014-03-31 00:00:00 | 2014-04-01 00:00:00 | 2014-04-30 00:00:00 |
| 8 | 0 | 14407 | 1117 | 2011-08-20 00:00:00 | 2014-02-28 00:00:00 | 2014-03-01 00:00:00 | 2014-03-31 00:00:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows sberbank_housing_market_forecasting`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Jun 2015 | 394 | 0.986 | mean 11.8, median 11.83, p10 11.33, p90 12.26 | mean 11.78, median 11.85, p10 11.3, p90 12.19 | 9.938 | sewerage_share_lag_1y (9.94), gdp_quart_growth_lag_1q (9.84), divorce_rate_lag_… | 0 |
| 1 | Apr 2015 | 724 | 0.942 | mean 11.8, median 11.86, p10 11.3, p90 12.25 | mean 11.77, median 11.85, p10 11.29, p90 12.19 | 10.984 | sewerage_share_lag_1y (10.98), divorce_rate_lag_1y (10.88), marriages_per_1000_… | 0 |
| 2 | Feb 2015 | 451 | 0.906 | mean 11.86, median 11.94, p10 11.35, p90 12.27 | mean 11.77, median 11.85, p10 11.3, p90 12.19 | 12.66 | sewerage_share_lag_1y (12.66), divorce_rate_lag_1y (12.55), incidence_populatio… | 0.0022 |
| 3 | Dec 2014 | 1583 | 0.836 | mean 11.86, median 11.92, p10 11.4, p90 12.27 | mean 11.77, median 11.85, p10 11.29, p90 12.18 | 9.095 | oil_urals_lag_1m (9.09), rent_price_1room_eco_lag_1m (9.02), mortgage_growth_la… | 0.0019 |
| 4 | Oct 2014 | 1044 | 0.758 | mean 11.79, median 11.84, p10 11.3, p90 12.22 | mean 11.76, median 11.85, p10 11.28, p90 12.17 | 8.807 | rent_price_1room_eco_lag_1m (8.81), gdp_quart_growth_lag_1q (8.77), deposits_gr… | 0 |
| 5 | Aug 2014 | 771 | 0.694 | mean 11.82, median 11.89, p10 11.27, p90 12.23 | mean 11.76, median 11.84, p10 11.28, p90 12.17 | 10.132 | gdp_quart_growth_lag_1q (10.13), mortgage_rate_lag_1m (8.80), deposits_rate_lag… | 0.0013 |
| 6 | Jun 2014 | 1179 | 0.628 | mean 11.8, median 11.85, p10 11.35, p90 12.19 | mean 11.75, median 11.84, p10 11.28, p90 12.17 | 9.269 | deposits_rate_lag_1m (9.27), rent_price_4+room_bus_lag_1m (9.04), rent_price_1r… | 0 |
| 7 | Apr 2014 | 1214 | 0.548 | mean 11.83, median 11.89, p10 11.37, p90 12.22 | mean 11.74, median 11.83, p10 11.28, p90 12.15 | 9.334 | rent_price_1room_eco_lag_1m (9.33), deposits_rate_lag_1m (8.72), rent_price_2ro… | 0 |
| 8 | Mar 2014 | 1117 | 0.509 | mean 11.79, median 11.85, p10 11.33, p90 12.2 | mean 11.73, median 11.83, p10 11.27, p90 12.15 | 9.667 | modern_education_share_lag_1y (9.67), old_education_build_share_lag_1y (9.67), … | 0.0018 |

## Bundle checks

0 error(s), 0 warning(s), 2 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 9 exact duplicate row(s) (0.0% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)
- **info** `dataset_conflicting_duplicate_rows`: 11 row(s) (0.0%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)

Accepted on purpose:

- `splits_feature_missing_in_test`: Decided (Lennart, 2026-11-11): three one-year lags of macro columns the source gives for some years only (curation_comments).
- `time_newest_period_short`: Decided (Lennart, 2026-11-11): 2015 holds 394 to 724 sales a month against 1,044 to 1,583 from September to December 2014, the market after the December 2014 rush; the data ends where the competition's training file ends, 30 June 2015, not at a download cut.

## Data checks

### Feature summary

<details>
<summary>Show the table (387 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| material | category | 8851 | 31.25 | 6 | panel, brick, breezeblock, mass concrete, mass concrete plus brick, wood |
| ecology | category | 7813 | 27.59 | 4 | poor, good, satisfactory, excellent |
| ID_railroad_station_walk | category | 24 | 0.08 | 132 | 24.0, 47.0, 75.0, 39.0, 42.0, 4.0, 33.0, 2.0, 18.0, 28.0 |
| product_type | category | 0 | 0 | 2 | Investment, OwnerOccupier |
| sub_area | category | 0 | 0 | 145 | Poselenie Sosenskoe, Nekrasovka, Poselenie Vnukovskoe, Poselenie Moskovskij, Po… |
| culture_objects_top_25 | category | 0 | 0 | 2 | no, yes |
| thermal_power_plant_raion | category | 0 | 0 | 2 | no, yes |
| incineration_raion | category | 0 | 0 | 2 | no, yes |
| oil_chemistry_raion | category | 0 | 0 | 2 | no, yes |
| radiation_raion | category | 0 | 0 | 2 | no, yes |
| railroad_terminal_raion | category | 0 | 0 | 2 | no, yes |
| big_market_raion | category | 0 | 0 | 2 | no, yes |
| nuclear_reactor_raion | category | 0 | 0 | 2 | no, yes |
| detention_facility_raion | category | 0 | 0 | 2 | no, yes |
| ID_metro | category | 0 | 0 | 222 | 45, 108, 21, 206, 29, 79, 132, 12, 20, 2 |
| ID_railroad_station_avto | category | 0 | 0 | 132 | 75, 105, 19, 4, 39, 24, 42, 73, 47, 2 |
| water_1line | category | 0 | 0 | 2 | no, yes |
| ID_big_road1 | category | 0 | 0 | 48 | 1, 2, 38, 13, 4, 14, 11, 5, 3, 16 |
| big_road1_1line | category | 0 | 0 | 2 | no, yes |
| ID_big_road2 | category | 0 | 0 | 58 | 1, 4, 27, 38, 55, 13, 39, 7, 10, 17 |
| railroad_1line | category | 0 | 0 | 2 | no, yes |
| ID_railroad_terminal | category | 0 | 0 | 8 | 32, 50, 5, 83, 121, 101, 97, 113 |
| ID_bus_terminal | category | 0 | 0 | 14 | 8, 1, 9, 5, 3, 14, 4, 7, 13, 2 |
| timestamp | datetime64\[ns\] | 0 | 0 | 1158 | 2014-12-16 00:00:00, 2014-12-09 00:00:00, 2014-06-30 00:00:00, 2014-12-18 00:00… |
| modern_education_share_lag_1y | float32 | 12535 | 44.26 | 2 | 90.92, 93.08 |
| old_education_build_share_lag_1y | float32 | 12535 | 44.26 | 2 | 23.14, 25.47 |
| child_on_acc_pre_school_lag_1y | float32 | 4425 | 15.62 | 4 | 3.013, 7.311, 16.765, 45.713 |
| provision_retail_space_sqm_lag_1y | float64 | 16414 | 57.96 | 2 | 794.0, 741.0 |
| hospital_beds_raion | float64 | 13665 | 48.25 | 79 | 540.0, 30.0, 1046.0, 2300.0, 240.0, 1084.0, 750.0, 229.0, 645.0, 1183.0 |
| build_year | float64 | 12853 | 45.38 | 118 | 2014.0, 2015.0, 0.0, 2013.0, 1970.0, 2016.0, 1968.0, 1969.0, 1.0, 1967.0 |
| state | float64 | 12702 | 44.85 | 4 | 3.0, 2.0, 1.0, 4.0 |
| cafe_sum_500_min_price_avg | float64 | 12687 | 44.8 | 634 | 500.0, 1000.0, 300.0, 1500.0, 750.0, 400.0, 650.0, 954.84, 600.0, 666.67 |
| cafe_sum_500_max_price_avg | float64 | 12687 | 44.8 | 434 | 1000.0, 1500.0, 500.0, 2500.0, 1250.0, 750.0, 1166.67, 1750.0, 1564.52, 1333.33 |
| cafe_avg_price_500 | float64 | 12687 | 44.8 | 835 | 750.0, 1250.0, 400.0, 2000.0, 575.0, 1000.0, 825.0, 1259.68, 1375.0, 800.0 |
| max_floor | float64 | 8851 | 31.25 | 48 | 17.0, 9.0, 12.0, 5.0, 14.0, 16.0, 1.0, 25.0, 22.0, 0.0 |
| num_room | float64 | 8851 | 31.25 | 13 | 2.0, 1.0, 3.0, 4.0, 5.0, 0.0, 6.0, 8.0, 10.0, 19.0 |
| kitch_sq | float64 | 8851 | 31.25 | 72 | 1.0, 8.0, 5.0, 10.0, 6.0, 9.0, 0.0, 7.0, 12.0, 11.0 |
| preschool_quota | float64 | 6629 | 23.41 | 121 | 2395.0, 6839.0, 5278.0, 10175.0, 11926.0, 1503.0, 3953.0, 1874.0, 3092.0, 5088.0 |
| school_quota | float64 | 6626 | 23.4 | 125 | 7377.0, 17063.0, 10529.0, 21892.0, 24750.0, 5782.0, 9700.0, 6772.0, 12721.0, 62… |
| cafe_sum_1000_min_price_avg | float64 | 6385 | 22.55 | 1574 | 500.0, 1000.0, 750.0, 600.0, 400.0, 700.0, 300.0, 666.67, 660.0, 914.53 |
| cafe_sum_1000_max_price_avg | float64 | 6385 | 22.55 | 1009 | 1000.0, 1500.0, 1750.0, 1250.0, 1166.67, 750.0, 1100.0, 500.0, 1125.0, 833.33 |
| cafe_avg_price_1000 | float64 | 6385 | 22.55 | 2052 | 750.0, 1375.0, 1250.0, 1000.0, 575.0, 400.0, 800.0, 916.67, 1207.26, 880.0 |
| life_sq | float64 | 6363 | 22.47 | 174 | 19.0, 30.0, 18.0, 20.0, 28.0, 29.0, 44.0, 17.0, 32.0, 27.0 |
| raion_build_count_with_material_info | float64 | 4960 | 17.51 | 112 | 43.0, 1.0, 458.0, 2.0, 372.0, 352.0, 244.0, 314.0, 217.0, 1681.0 |
| build_count_block | float64 | 4960 | 17.51 | 76 | 3.0, 0.0, 9.0, 58.0, 55.0, 52.0, 8.0, 25.0, 14.0, 78.0 |
| build_count_wood | float64 | 4960 | 17.51 | 34 | 0.0, 1.0, 2.0, 51.0, 5.0, 146.0, 4.0, 607.0, 11.0, 352.0 |
| build_count_frame | float64 | 4960 | 17.51 | 21 | 0.0, 1.0, 12.0, 4.0, 11.0, 3.0, 19.0, 79.0, 25.0, 5.0 |
| build_count_brick | float64 | 4960 | 17.51 | 101 | 0.0, 10.0, 4.0, 124.0, 16.0, 28.0, 2.0, 65.0, 105.0, 66.0 |
| build_count_monolith | float64 | 4960 | 17.51 | 33 | 0.0, 2.0, 4.0, 3.0, 9.0, 7.0, 5.0, 8.0, 1.0, 16.0 |
| build_count_panel | float64 | 4960 | 17.51 | 91 | 0.0, 28.0, 201.0, 123.0, 111.0, 60.0, 30.0, 41.0, 124.0, 328.0 |
| build_count_foam | float64 | 4960 | 17.51 | 4 | 0.0, 1.0, 11.0, 2.0 |
| build_count_slag | float64 | 4960 | 17.51 | 21 | 0.0, 1.0, 2.0, 9.0, 4.0, 17.0, 5.0, 84.0, 23.0, 3.0 |
| build_count_mix | float64 | 4960 | 17.51 | 9 | 0.0, 1.0, 2.0, 5.0, 4.0, 9.0, 8.0, 3.0, 6.0 |
| raion_build_count_with_builddate_info | float64 | 4960 | 17.51 | 114 | 41.0, 1.0, 459.0, 2.0, 373.0, 244.0, 352.0, 1680.0, 213.0, 175.0 |
| build_count_before_1920 | float64 | 4960 | 17.51 | 29 | 0.0, 1.0, 2.0, 4.0, 13.0, 47.0, 6.0, 34.0, 23.0, 5.0 |
| build_count_1921-1945 | float64 | 4960 | 17.51 | 47 | 0.0, 1.0, 2.0, 4.0, 20.0, 24.0, 3.0, 5.0, 299.0, 14.0 |
| build_count_1946-1970 | float64 | 4960 | 17.51 | 100 | 7.0, 0.0, 1.0, 14.0, 40.0, 184.0, 2.0, 153.0, 439.0, 246.0 |
| build_count_1971-1995 | float64 | 4960 | 17.51 | 92 | 10.0, 0.0, 131.0, 130.0, 93.0, 58.0, 42.0, 59.0, 176.0, 102.0 |
| build_count_after_1995 | float64 | 4960 | 17.51 | 69 | 23.0, 0.0, 57.0, 13.0, 20.0, 176.0, 22.0, 11.0, 252.0, 33.0 |
| cafe_sum_1500_min_price_avg | float64 | 4126 | 14.57 | 2494 | 1000.0, 500.0, 700.0, 300.0, 600.0, 716.67, 660.0, 750.0, 650.0, 833.33 |

(327 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | -0.944 | -1.175 | 0.155 | 0.001 | log | 248444 | 2.73861e+17 | exponential |

### Numeric features

<details>
<summary>Show the table (363 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| full_sq | 28321 | 54.5183 | 23.4276 | 6 | 729 |
| life_sq | 21958 | 34.9188 | 54.5749 | 0 | 7478 |
| floor | 28170 | 7.74388 | 5.3549 | 0 | 77 |
| max_floor | 19470 | 12.61 | 6.79235 | 0 | 99 |
| build_year | 15468 | 3171.4 | 161214 | 0 | 2.0052e+07 |
| num_room | 19470 | 1.91418 | 0.857557 | 0 | 19 |
| kitch_sq | 19470 | 6.25336 | 25.6483 | 0 | 2014 |
| state | 15619 | 2.08349 | 0.859481 | 1 | 4 |
| area_m | 28321 | 1.86006e+07 | 2.14579e+07 | 2.08163e+06 | 2.06072e+08 |
| raion_popul | 28321 | 81667 | 58953.7 | 2546 | 247469 |
| green_zone_part | 28321 | 0.225532 | 0.17728 | 0.00187937 | 0.852923 |
| indust_part | 28321 | 0.119776 | 0.11789 | 0 | 0.521867 |
| children_preschool | 28321 | 5011.23 | 3875.09 | 175 | 19223 |
| preschool_quota | 21692 | 3286.58 | 2170.01 | 0 | 11926 |
| preschool_education_centers_raion | 28321 | 3.96833 | 3.05384 | 0 | 13 |
| children_school | 28321 | 5178.64 | 4050.26 | 168 | 19083 |
| school_quota | 21695 | 8356.94 | 4293.91 | 1012 | 24750 |
| school_education_centers_raion | 28321 | 4.59479 | 3.50874 | 0 | 14 |
| school_education_centers_top_20_raion | 28321 | 0.08785 | 0.306096 | 0 | 2 |
| hospital_beds_raion | 14656 | 1174.88 | 1056.22 | 0 | 4849 |
| healthcare_centers_raion | 28321 | 1.24205 | 1.48374 | 0 | 6 |
| university_top_20_raion | 28321 | 0.0971364 | 0.355534 | 0 | 3 |
| sport_objects_raion | 28321 | 5.99251 | 5.81124 | 0 | 29 |
| additional_education_raion | 28321 | 2.60888 | 2.72472 | 0 | 16 |
| culture_objects_top_25_raion | 28321 | 0.0892271 | 0.623332 | 0 | 10 |
| shopping_centers_raion | 28321 | 3.7165 | 3.9539 | 0 | 23 |
| office_raion | 28321 | 5.39953 | 14.1225 | 0 | 141 |
| full_all | 28321 | 143610 | 279983 | 2546 | 1.71673e+06 |
| male_f | 28321 | 65991 | 128075 | 1208 | 774585 |
| female_f | 28321 | 77619 | 151957 | 1341 | 942145 |
| young_all | 28321 | 10855 | 8420.08 | 365 | 40692 |
| young_male | 28321 | 5563.33 | 4341.84 | 189 | 20977 |
| young_female | 28321 | 5291.74 | 4085.7 | 177 | 19715 |
| work_all | 28321 | 52271.3 | 38171 | 1633 | 161290 |
| work_male | 28321 | 26553.4 | 19285.2 | 863 | 79622 |
| work_female | 28321 | 25717.9 | 18981.5 | 771 | 81668 |
| ekder_all | 28321 | 18540.8 | 13398.6 | 548 | 57086 |
| ekder_male | 28321 | 5595.8 | 4138 | 156 | 19275 |
| ekder_female | 28321 | 12945.1 | 9301.58 | 393 | 37811 |
| 0_6_male | 28321 | 2567.04 | 2001.99 | 91 | 9987 |
| 0_6_female | 28321 | 2444.34 | 1876.11 | 85 | 9236 |
| 7_14_male | 28321 | 2656.48 | 2085.95 | 87 | 9761 |
| 7_14_female | 28321 | 2522.32 | 1970.27 | 82 | 9322 |
| 0_17_all | 28321 | 12179.3 | 9403.42 | 411 | 45170 |
| 0_17_male | 28321 | 6244.38 | 4845.38 | 214 | 23233 |
| 0_17_female | 28321 | 5935.13 | 4565.66 | 198 | 21937 |
| 16_29_all | 28321 | 30789.4 | 59742.2 | 575 | 367659 |
| 16_29_male | 28321 | 15118.3 | 28998.5 | 308 | 172958 |
| 16_29_female | 28321 | 15671.3 | 30769.2 | 253 | 194701 |
| 0_13_all | 28321 | 9556.57 | 7405.93 | 322 | 36035 |
| 0_13_male | 28321 | 4896.02 | 3818.87 | 166 | 18574 |
| 0_13_female | 28321 | 4660.55 | 3594.26 | 156 | 17461 |
| raion_build_count_with_material_info | 23361 | 319.492 | 277.089 | 1 | 1681 |
| build_count_block | 23361 | 49.2684 | 46.89 | 0 | 223 |
| build_count_wood | 23361 | 41.0973 | 126.944 | 0 | 793 |
| build_count_frame | 23361 | 5.07179 | 15.3519 | 0 | 97 |
| build_count_brick | 23361 | 100.581 | 119.689 | 0 | 664 |
| build_count_monolith | 23361 | 11.7904 | 19.2783 | 0 | 127 |
| build_count_panel | 23361 | 106.505 | 88.525 | 0 | 431 |
| build_count_foam | 23361 | 0.159582 | 1.10325 | 0 | 11 |

(303 more rows not shown)

</details>

### Categorical features

<details>
<summary>Show the table (81 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| ID_big_road1 | 1 | 1 | 4430 | 15.64 |
| ID_big_road1 | 2 | 2 | 3455 | 12.2 |
| ID_big_road1 | 3 | 38 | 2721 | 9.61 |
| ID_big_road1 | 4 | 13 | 2704 | 9.55 |
| ID_big_road1 | 5 | 4 | 2169 | 7.66 |
| ID_big_road2 | 1 | 1 | 4136 | 14.6 |
| ID_big_road2 | 2 | 4 | 2376 | 8.39 |
| ID_big_road2 | 3 | 27 | 2040 | 7.2 |
| ID_big_road2 | 4 | 38 | 1204 | 4.25 |
| ID_big_road2 | 5 | 55 | 1167 | 4.12 |
| ID_bus_terminal | 1 | 8 | 6966 | 24.6 |
| ID_bus_terminal | 2 | 1 | 3787 | 13.37 |
| ID_bus_terminal | 3 | 9 | 3328 | 11.75 |
| ID_bus_terminal | 4 | 5 | 2604 | 9.19 |
| ID_bus_terminal | 5 | 3 | 2085 | 7.36 |
| ID_metro | 1 | 45 | 2722 | 9.61 |
| ID_metro | 2 | 108 | 1702 | 6.01 |
| ID_metro | 3 | 21 | 1653 | 5.84 |
| ID_metro | 4 | 206 | 1607 | 5.67 |
| ID_metro | 5 | 29 | 763 | 2.69 |
| ID_railroad_station_avto | 1 | 75 | 1702 | 6.01 |
| ID_railroad_station_avto | 2 | 105 | 1653 | 5.84 |
| ID_railroad_station_avto | 3 | 19 | 1583 | 5.59 |
| ID_railroad_station_avto | 4 | 4 | 1308 | 4.62 |
| ID_railroad_station_avto | 5 | 39 | 1301 | 4.59 |
| ID_railroad_station_walk | 1 | 24.0 | 2677 | 9.45 |
| ID_railroad_station_walk | 2 | 47.0 | 2196 | 7.75 |
| ID_railroad_station_walk | 3 | 75.0 | 1702 | 6.01 |
| ID_railroad_station_walk | 4 | 39.0 | 1301 | 4.59 |
| ID_railroad_station_walk | 5 | 42.0 | 1221 | 4.31 |
| ID_railroad_terminal | 1 | 32 | 8859 | 31.28 |
| ID_railroad_terminal | 2 | 50 | 5419 | 19.13 |
| ID_railroad_terminal | 3 | 5 | 5077 | 17.93 |
| ID_railroad_terminal | 4 | 83 | 3640 | 12.85 |
| ID_railroad_terminal | 5 | 121 | 1839 | 6.49 |
| big_market_raion | 1 | no | 25547 | 90.21 |
| big_market_raion | 2 | yes | 2774 | 9.79 |
| big_road1_1line | 1 | no | 27602 | 97.46 |
| big_road1_1line | 2 | yes | 719 | 2.54 |
| culture_objects_top_25 | 1 | no | 27097 | 95.68 |
| culture_objects_top_25 | 2 | yes | 1224 | 4.32 |
| detention_facility_raion | 1 | no | 26120 | 92.23 |
| detention_facility_raion | 2 | yes | 2201 | 7.77 |
| ecology | 1 | &lt;NA> | 7813 | 27.59 |
| ecology | 2 | poor | 7274 | 25.68 |
| ecology | 3 | good | 6806 | 24.03 |
| ecology | 4 | satisfactory | 3364 | 11.88 |
| ecology | 5 | excellent | 3064 | 10.82 |
| incineration_raion | 1 | no | 25982 | 91.74 |
| incineration_raion | 2 | yes | 2339 | 8.26 |
| material | 1 | panel | 13291 | 46.93 |
| material | 2 | &lt;NA> | 8851 | 31.25 |
| material | 3 | brick | 2714 | 9.58 |
| material | 4 | breezeblock | 1386 | 4.89 |
| material | 5 | mass concrete | 1305 | 4.61 |
| nuclear_reactor_raion | 1 | no | 27550 | 97.28 |
| nuclear_reactor_raion | 2 | yes | 771 | 2.72 |
| oil_chemistry_raion | 1 | no | 28055 | 99.06 |
| oil_chemistry_raion | 2 | yes | 266 | 0.94 |
| product_type | 1 | Investment | 17379 | 61.36 |

(21 more rows not shown)

</details>

## Build

| field | value |
|---|---|
| uuid | 01a21800-0ccc-7c5e-8046-df2c8f33cff1 |
| checksum | v2:7a7d99420a9b7a80146738e44a08debb9b78439e475db65ac6fc67c6beed7c26 |
| built_at | 2026-11-26T13:16:31+00:00 |
| path | sberbank_housing_market_forecasting/01a21800-0ccc-7c5e-8046-df2c8f33cff1 |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
