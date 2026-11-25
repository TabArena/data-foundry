---
report_format: data-foundry-report-v2
unique_name: craigslist_used_vehicles_f150
container_format: 2
checksum: v2:d4e097689948af9fe9fea8921ba1e779f664e3c06fed8c86a7f2573f7bdaa3b8
build: null
build_stale: false
raw_files:
  v1/craigslist-carstrucks-data.zip: 35d5490a6dd9d25fedc9f860d6983385a8bfb45a423cef029c847952f2f63231
  v10/craigslist-carstrucks-data.zip: eb2ad6c7dedd3c73ffed4bf47929ab66e55d7da186ed240230caa1fad85d2e8f
  v11/craigslist-carstrucks-data.zip: 729dc4d4d87013d6ec0645b79041b04b98f42f06794a94acfbb3dabffb613151
  v2/craigslist-carstrucks-data.zip: 7c4b775c58ec4318248b27f6e68a34077ecabe9b3aa68aec55070161881f85a1
  v3/craigslist-carstrucks-data.zip: 33a022c6b6457c7ac0308f8adaa7c83fd6010a5fd234116cc30d6a16569f35ef
  v4/craigslist-carstrucks-data.zip: 2b7ded7f1040b08ba626d61d95e4648aeba2716828db47a8b24d7497e25ad10f
  v5/craigslist-carstrucks-data.zip: 0fb834aee406546cd2730bf65a4aa8e2073042e106c9b7acedd88990a5d87325
  v6/craigslist-carstrucks-data.zip: 26772c279637608186d8519a4b9db8aef772c501d49823af8e0d5b339529d5cf
  v7/craigslist-carstrucks-data.zip: 7c1daf9330bc4834128acb01bc942dba5d1a3beb7e1bcc589ec4832677466321
  v8/craigslist-carstrucks-data.zip: 0e221d0bf3294eac04a3afa16df8649d3fb1ee64e2b39d9478821a1190966bdc
  v9/craigslist-carstrucks-data.zip: 37a4bfa379201ff846d7008a2c27a246dc97383577536c64dd4b1125df7baae4
data:
  n_rows: 105134
  n_features: 17
  dtypes:
    category: 10
    datetime64[ns]: 1
    float64: 6
    string: 1
  n_test_dataset_rows: null
task:
  target: price
  problem_type: regression
  metric: rmsle
  metric_origin: context
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: scrape_date
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 5
  n_folds: 1
  random_state: 4267
  time_horizon: 1
  time_horizon_unit: steps
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 54988
    max: 93126
  n_test:
    min: 6405
    max: 13087
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  accepted:
    dataset_missing_value_label: '`title_status` ''missing'' is Craigslist''s own
      option, a truck without a title document: a real state, not a missing value.'
    dataset_conflicting_duplicate_rows: '93.6% of 1,708 same-year, same-mileage, different-price
      groups share a VIN: one truck at two prices within one scrape. A scrape is never
      cut by the split, so they stay together.'
    task_time_on_few_unique: 'Nine scrape periods, one date each, by design: the scrape
      is the time step.'
    splits_below_target: 'Five windows against nine: every scrape whose training side
      keeps half the rows is a window; the 50% floor stops more (Jan 2020 trains on
      40.3%).'
decisions: []
---

# craigslist_used_vehicles_f150

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `price`, scored with `rmsle` on temporal splits by `scrape_date`. 105,134 rows and 17 features. Source: Kaggle (2018).

Not built yet. The current definition gives checksum `v2:d4e097689948af9fe9fea8921ba1e779f664e3c06fed8c86a7f2573f7bdaa3b8`.

## In brief

**Question.** At what price is a used Ford F-150 listed on Craigslist?

**Use case.** For example, a seller or dealer sets the asking price of a used F-150, or a buyer or a marketplace judges a listing, with a model trained on the listings of earlier months.

**One row.** One F-150 listing in one of nine nationwide scrapes of Craigslist's US car adverts (2018 to May 2021), one row per truck and scrape.

**Predicted.** The asking price in US dollars, from 1,000 to 150,000.

**Known at prediction time.** What the advert states: model year, mileage, the model string with trim and cab, condition, cylinders, fuel, title status, transmission, drive, size, body type, colour, whether an owner or a dealer sells it, the Craigslist site and its coordinates, and the scrape's date.

**What the test data stands for.** Each test set is one later scrape, with all earlier scrapes for training: the next market a model meets.

**Our changes to the source.** We keep the Ford F-150 of a scraped table of all makes, one row per truck within a scrape (also across sites), drop placeholder prices (0, 1, 12345, 99999, down payments) and the 2026 scrape, set values impossible for an F-150 missing, drop the posting text and keep the seller type from the url.

> **Use case fit: approximate (a stand-in with a known gap).** The fields are what an advert shows and the test scrapes are later markets, but the target is the asking price (a gap for a buyer who wants the sale price), the poster types the fields in, and the title is not shipped. Kept on purpose, not a gap: a relisted truck trains with its earlier price, as its dealer knows.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/craigslist_used_vehicles_f150.md`](../../../../curation/records/craigslist_used_vehicles_f150.md)
- The original source: <https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/craigslist_used_vehicles_f150/`. To get them:

```text
One folder per Kaggle version (each version is one scrape; the zips stay zipped):

for N in 1 2 3 4 5 6 7 8 9 10 11; do kaggle datasets download austinreese/craigslist-carstrucks-data/$N -p local-data-warehouse/craigslist_used_vehicles_f150/v$N; done

The definition reads the zips once and writes their Ford rows, without the posting text, to ford_listings.parquet.
```

<details>
<summary>The 11 raw files the sources name</summary>

| file | source | bytes | rows | sha256 (start) |
|---|---|---|---|---|
| `v1/craigslist-carstrucks-data.zip` | Kaggle publication | 40,786,848 |  | `35d5490a6dd9d25f` |
| `v10/craigslist-carstrucks-data.zip` | Kaggle publication | 275,237,598 |  | `eb2ad6c7dedd3c73` |
| `v11/craigslist-carstrucks-data.zip` | Kaggle publication | 260,443,332 |  | `729dc4d4d87013d6` |
| `v2/craigslist-carstrucks-data.zip` | Kaggle publication | 310,693,598 |  | `7c4b775c58ec4318` |
| `v3/craigslist-carstrucks-data.zip` | Kaggle publication | 309,098,399 |  | `33a022c6b6457c7a` |
| `v4/craigslist-carstrucks-data.zip` | Kaggle publication | 301,787,839 |  | `2b7ded7f1040b08b` |
| `v5/craigslist-carstrucks-data.zip` | Kaggle publication | 360,298,489 |  | `0fb834aee406546c` |
| `v6/craigslist-carstrucks-data.zip` | Kaggle publication | 300,777,993 |  | `26772c2796376081` |
| `v7/craigslist-carstrucks-data.zip` | Kaggle publication | 246,059,937 |  | `7c1daf9330bc4834` |
| `v8/craigslist-carstrucks-data.zip` | Kaggle publication | 280,225,112 |  | `0e221d0bf3294eac` |
| `v9/craigslist-carstrucks-data.zip` | Kaggle publication | 280,201,864 |  | `37a4bfa379201ff8` |

</details>

On first use, `_prepare_raw_files` writes `ford_listings.parquet` into the same folder.

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/craigslist_used_vehicles_f150   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/craigslist_used_vehicles_f150   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data |
| year | 2018 |
| domain | business & marketing |
| license | CC0: Public Domain |
| data_tags | Non-IID, Temporal, Spatial |
| reference | reese2018craigslist |
| rows x columns | 105,134 x 18 |
| task.target | price |
| task.problem_type | regression |
| task.metric | rmsle |
| task.split_regime | temporal_non_iid |
| task.time_on | scrape_date |

**Metric**

| field | value |
|---|---|
| name | `rmsle` (standard; takes value; lower is better) |
| origin | context: obvious from the task: the source defines no metric |
| definition | sqrt(mean((log1p(y) - log1p(max(p, 0)))^2)); y >= 0, a prediction below 0 counts as 0 |
| reason | A scraped Kaggle dataset without a task, leaderboard or paper: the data card, the scraper's GitHub README and a web search name no metric. For an asking price the error that matters is relative to the price, so RMSLE on the price in dollars. |
| target scale | ships on the `log` scale for modelling; scored on the original scale after the inverse of `log` |

<details>
<summary>Feature types: 8 categorical, 2 ordinal, 1 string, 0 datetime</summary>

- categorical (8): `seller`, `fuel`, `title_status`, `transmission`, `drive`, `type`, `paint_color`, `region`
- ordinal (2): `condition (salvage < fair < good < excellent < like new < new)`, `size (mid-size < full-size)`
- string (1): `model`
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{reese2018craigslist,
  author       = {Austin Reese},
  title        = {Used Cars Dataset (Craigslist Cars+Trucks Data)},
  year         = {2018},
  howpublished = {\url{https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data}},
  note         = {Kaggle dataset, versions 1 to 11},
}
```

</details>

## Sample rows

The first 5 of 105,134 rows of the final frame (the oldest rows: the frame is sorted by `scrape_date`); 12 of 18 columns, the target first. Cells are cut at 40 characters.

| price | year | condition | cylinders | fuel | odometer | title_status | transmission | drive | size | type | paint_color |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10.434 | 2015 | good | 6 | gas | nan | clean | automatic | 4wd | full-size | truck | black |
| 8.00637 | 2001 | fair | nan | gas | nan | clean | automatic | nan | nan | nan | nan |
| 8.92266 | 2003 | nan | nan | gas | nan | clean | automatic | nan | nan | nan | nan |
| 7.09008 | 1994 | nan | nan | gas | nan | clean | automatic | nan | nan | nan | nan |
| 10.4341 | 2016 | nan | nan | gas | nan | clean | automatic | nan | nan | nan | nan |

## Curation notes

We start with the eleven Kaggle versions of austinreese/craigslist-carstrucks-data (one CSV each, every US car listing on Craigslist at the scrape) and keep the Ford F-150.

- Prediction point: when the advert is written, so every field the advert shows is known; the price arrives with it, so the split needs no gap.
- Versions and dates: each version is one scrape, dated by its upload, not by its postings: a scrape holds about five weeks of postings, which end at the upload in versions 8 and 10 (their `posting_date`) and, by listing id, 5 to 10 weeks before it in versions 2 to 6. Version 1 (uploaded 2019-10-08) is an older scrape: Craigslist issues listing ids in posting order (they follow the posting date of versions 8, 10 and 11 with a correlation of 0.99998), and all of version 1's ids lie about 277 million ids, over a year of postings, before version 2's, so it is dated 2018-10-10, the dataset's first upload: its order is measured, its date inferred (`Time: Inferred` for that period; it is training data only, and the split uses only the order). Versions 9 and 10 (2021-04-20 and 2021-05-06) share 26-27% of their listing ids and form one period (dated 2021-05-06; a listing in both kept once, from version 10); no other pair of versions shares more than 27 ids. Version 11 (2026-11-05) is left out: five years after the others, with columns of its own.
- US sites only: version 1 also holds Canadian and Mexican Craigslist sites (437 F-150 rows on craigslist.ca, prices in Canadian dollars, and 46 on craigslist.com.mx), which are dropped.
- The F-150: manufacturer `ford` and a model string starting with "f150" or "f-150" (versions 1-3 hold the model in `make`). The model string ships as text: 600 to 1,000 spellings a scrape (3,343 in all) that hold the trim, cab, bed and drive; a price typed into it (13 rows, such as "$21995") is removed.
- One row per truck within a scrape period: one row per VIN, then one row per model year, mileage, price and Craigslist site, and, where the mileage is no multiple of 1,000, one row per model year, mileage and price on any site: dealers post one truck on several sites, and among such groups that carry VINs, 99.8% of 11,280 carry one VIN. The cross-site step drops 3,481 rows (3.2%; 1.5% to 3.5% of each scrape, 9.5% of May 2021); the price's 10th, 50th and 90th percentiles move from 3,500, 14,995 and 33,995 to 3,500, 14,950 and 33,919 dollars. Round mileages also match by VIN (98.5% of 741 groups) but are left, 2,713 rows more.
- Price: listings under 1,000 or over 150,000 dollars are dropped (0 and 1 mean "call for price"; 4-13% of a scrape's F-150 rows are under 1,000), and so are placeholder prices (one digit five times or more, such as 99999, or a sequence, 1234, 12345 or 123456; 52 rows) and down payments posted as the price (under 5,000 for a truck of 2015 or newer; 124 rows). Charm prices such as 9,999 (435 rows) or 8,888 are real asking prices and stay.
- Impossible values are set missing, the row kept, one rule each: a mileage over 500,000; a model year before 1975 (the F-150's first) or after the scrape's year; front-wheel drive (no F-150 has it; 2,456 rows); cylinders other than 6 or 8 (218); size compact or sub-compact (191); fuel electric before model year 2022 (11); coordinates outside the US (53). A mileage under 100 on a truck at least two model years old is a placeholder (0, 1) and set missing too (483 rows). `cylinders` becomes a number ("other" missing); `condition` and `size` are ordered scales.
- Seller: `seller` is owner or dealer, the Craigslist section the poster picked (`/cto/` or `/ctd/` in the url): 37,839 owners and 67,295 dealers. Dealers list comparable trucks 500 to 2,200 dollars higher in every scrape.
- Dropped: the posting text, title and image links (never read: 70-80% of the F-150 texts hold a phone number), the url, listing id and VIN (identifiers, used for the steps above; the advert's title, which the url carries as a slug, is not shipped), `manufacturer` (constant), `county` (empty), `state` (absent in versions 1-3; the site and the coordinates carry it) and the site's name (spelled differently in versions 1-3): the site's subdomain in the url replaces it as `region`.
- The target ships as the log of the price; the metric is RMSLE on the price in dollars.
- Potential leak, kept on purpose: a truck relisted in a later scrape (its VIN seen before; 8,634 rows, 8.2%) is in training with its earlier price when it is tested: 12.6%, 18.0%, 2.2%, 5.4% and 3.2% of the Mar 2020 to May 2021 windows, at the same price in 4.0%, 7.6%, 0.8%, 1.9% and 1.1%. No listing id appears in two periods, so each is a new advert (at a new price in 61.6% of cases), a repost the use case meets: a dealer knows the earlier price of a truck it posts again. Dropping the linked ones moves the RMSE by -1.6% to +1.9%; only 46.5% of the rows carry a VIN, so the rest cannot be linked.
- Anomaly: the fields are typed in by the poster: `condition`, `cylinders`, `drive`, `size`, `type` and `paint_color` are 23-66% missing. The mileage is 32% missing in 2018 and 17-23% up to Dec 2020, then 1.7% in May 2021: Craigslist made it a required field around 30 November 2020 (version 8's weekly postings go from 14-16% missing to 4.5% that week), a change a model in use meets too.

## Splits

Five test windows, each one scrape, each trained on every earlier scrape: May 2021 (versions 9 and 10, 12,008 trucks, 88.6% of the rows in training), Dec 2020 (8,631; 80.4%), Sep 2020 (6,405; 74.3%), Jun 2020 (10,015; 64.8%) and Mar 2020 (13,087; 52.3%). The horizon is one scrape (uploads 5 to 21 weeks apart; the scraper ran "every few months"): a pricing model refit on the listings so far meets the next market. No gap for the label: the price arrives with the advert. The scrape schedule leaves postings unseen before each window, by listing id about 7, 3, 16, 7.5 and 15 weeks before the Mar 2020 to May 2021 windows.
Every scrape whose training side keeps half the rows is a window; the older scrapes (Oct 2018, Oct 2019, Dec 2019, Jan 2020) train on 0% to 40.3% and stay training data. The Mar 2020 window clears the 50% floor only with version 1 in training (43.5% without it); version 1's order is measured from listing ids, only its date is inferred. Five windows against the nine an IID split of 105,134 trucks would get (SPLIT-15): the 50% floor stops more. The windows are named by upload; their postings are, by listing id, about Jan to mid-Feb 2020 (Mar 2020, before COVID-19), Mar to Apr 2020 (Jun 2020, the pandemic's start), Aug to early Sep 2020, 28 Oct to 3 Dec 2020 and mid-Mar to 5 May 2021, when used-truck asking prices rose (the median of comparable trucks, 2013-2015 with 60,000 to 120,000 miles, from about 21,000 dollars in Jun 2020 to about 26,000).
The 2026 scrape (version 11) is not a window: five years after the others, with trucks of model years the training data never shows.

5 repeat(s) x 1 fold(s) with seed 4267; train 54,988 to 93,126 rows, test 6,405 to 13,087 rows. Prediction horizon: 1 steps.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 93126 | 12008 | 2018-10-10 00:00:00 | 2020-12-03 00:00:00 | 2021-05-06 00:00:00 | 2021-05-06 00:00:00 |
| 1 | 0 | 84495 | 8631 | 2018-10-10 00:00:00 | 2020-09-16 00:00:00 | 2020-12-03 00:00:00 | 2020-12-03 00:00:00 |
| 2 | 0 | 78090 | 6405 | 2018-10-10 00:00:00 | 2020-06-17 00:00:00 | 2020-09-16 00:00:00 | 2020-09-16 00:00:00 |
| 3 | 0 | 68075 | 10015 | 2018-10-10 00:00:00 | 2020-03-22 00:00:00 | 2020-06-17 00:00:00 | 2020-06-17 00:00:00 |
| 4 | 0 | 54988 | 13087 | 2018-10-10 00:00:00 | 2020-01-07 00:00:00 | 2020-03-22 00:00:00 | 2020-03-22 00:00:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows craigslist_used_vehicles_f150`.

| window | period | weekdays | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|---|
| 0 | May 2021 | Thu | 12008 | 0.886 | mean 9.683, median 9.852, p10 8.516, p90 10.6 | mean 9.396, median 9.547, p10 8.132, p90 10.4 | 0.63 | odometer (0.63), year (0.08), region (0.07) | 0 |
| 1 | Dec 2020 | Thu | 8631 | 0.804 | mean 9.656, median 9.852, p10 8.412, p90 10.57 | mean 9.37, median 9.546, p10 8.086, p90 10.37 | 0.159 | year (0.16), odometer (0.04), seller (0.04) | 0 |
| 2 | Sep 2020 | Wed | 6405 | 0.743 | mean 9.627, median 9.798, p10 8.304, p90 10.59 | mean 9.348, median 9.532, p10 8.006, p90 10.34 | 0.185 | year (0.18), region (0.12), odometer (0.04) | 0 |
| 3 | Jun 2020 | Wed | 10015 | 0.648 | mean 9.444, median 9.607, p10 8.343, p90 10.31 | mean 9.339, median 9.51, p10 8.006, p90 10.35 | 0.06 | year (0.06), region (0.04), seller (0.03) | 0 |
| 4 | Mar 2020 | Sun | 13087 | 0.523 | mean 9.404, median 9.546, p10 8.243, p90 10.31 | mean 9.322, median 9.473, p10 8.005, p90 10.36 | 0.043 | seller (0.04), year (0.04), region (0.02) | 0.0002 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 1 exact duplicate row(s) (0.0% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)

Accepted on purpose:

- `dataset_missing_value_label`: `title_status` 'missing' is Craigslist's own option, a truck without a title document: a real state, not a missing value.
- `dataset_conflicting_duplicate_rows`: 93.6% of 1,708 same-year, same-mileage, different-price groups share a VIN: one truck at two prices within one scrape. A scrape is never cut by the split, so they stay together.
- `task_time_on_few_unique`: Nine scrape periods, one date each, by design: the scrape is the time step.
- `splits_below_target`: Five windows against nine: every scrape whose training side keeps half the rows is a window; the 50% floor stops more (Jan 2020 trains on 40.3%).

## Data checks

### Feature summary

<details>
<summary>Show the table (18 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| size | category | 65045 | 61.87 | 2 | full-size, mid-size |
| condition | category | 45515 | 43.29 | 6 | excellent, good, like new, fair, new, salvage |
| paint_color | category | 32212 | 30.64 | 12 | white, black, red, blue, silver, grey, green, brown, custom, yellow |
| type | category | 31147 | 29.63 | 13 | pickup, truck, other, offroad, SUV, sedan, van, coupe, mini-van, bus |
| drive | category | 27186 | 25.86 | 2 | 4wd, rwd |
| fuel | category | 961 | 0.91 | 4 | gas, other, diesel, hybrid |
| title_status | category | 382 | 0.36 | 6 | clean, rebuilt, lien, salvage, missing, parts only |
| transmission | category | 343 | 0.33 | 3 | automatic, manual, other |
| region | category | 0 | 0 | 413 | boise, kansascity, grandrapids, anchorage, sanantonio, minneapolis, houston, tu… |
| seller | category | 0 | 0 | 2 | dealer, owner |
| scrape_date | datetime64\[ns\] | 0 | 0 | 9 | 2018-10-10 00:00:00, 2020-03-22 00:00:00, 2019-10-14 00:00:00, 2019-12-02 00:00… |
| cylinders | float64 | 37688 | 35.85 | 2 | 8.0, 6.0 |
| odometer | float64 | 21972 | 20.9 | 41604 | 150000.0, 200000.0, 180000.0, 160000.0, 130000.0, 170000.0, 190000.0, 140000.0,… |
| lat | float64 | 760 | 0.72 | 33575 | 29.8135, 38.9847, 42.8511, 33.7792, 43.1824, 46.2348, 42.8511, 36.1149, 33.7865… |
| long | float64 | 760 | 0.72 | 34556 | -82.472, -88.1704, -83.4512, -84.4118, -84.1122, -119.128, -83.4512, -84.4454, … |
| year | float64 | 284 | 0.27 | 48 | 2013.0, 2014.0, 2016.0, 2010.0, 2015.0, 2011.0, 2018.0, 2012.0, 2017.0, 2008.0 |
| price | float64 | 0 | 0 | 9771 | 7.824, 8.1605, 8.4118, 8.7796, 8.6125, 8.0064, 7.6009, 8.9227, 7.3132, 8.5172 |
| model | string | 0 | 0 | 3343 | f-150, f150, f-150 xlt, f150 xlt, f150 4x4, f-150 lariat, f150 supercrew cab, f… |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | -0.625 | -0.825 | 0.774 | 0.009 | log | 980211 | 4.46114e+18 | exponential |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| price | 105134 | 9.43315 | 0.879763 | 6.90776 | 11.8492 |
| year | 104850 | 2009.62 | 7.18467 | 1975 | 2022 |
| cylinders | 67446 | 7.27827 | 0.960511 | 6 | 8 |
| odometer | 83162 | 112717 | 63072.9 | 0 | 480000 |
| lat | 104374 | 38.5993 | 6.12514 | 17.2656 | 65.8122 |
| long | 104374 | -94.6514 | 16.3153 | -159.59 | -67.0074 |

### Categorical features

<details>
<summary>Show the table (52 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| condition | 1 | &lt;NA> | 45515 | 43.29 |
| condition | 2 | excellent | 27450 | 26.11 |
| condition | 3 | good | 22212 | 21.13 |
| condition | 4 | like new | 6230 | 5.93 |
| condition | 5 | fair | 3299 | 3.14 |
| drive | 1 | 4wd | 60869 | 57.9 |
| drive | 2 | &lt;NA> | 27186 | 25.86 |
| drive | 3 | rwd | 17079 | 16.24 |
| fuel | 1 | gas | 99674 | 94.81 |
| fuel | 2 | other | 4189 | 3.98 |
| fuel | 3 | &lt;NA> | 961 | 0.91 |
| fuel | 4 | diesel | 273 | 0.26 |
| fuel | 5 | hybrid | 37 | 0.04 |
| model | 1 | f-150 | 51780 | 49.25 |
| model | 2 | f150 | 13022 | 12.39 |
| model | 3 | f-150 xlt | 3363 | 3.2 |
| model | 4 | f150 xlt | 3011 | 2.86 |
| model | 5 | f150 4x4 | 2879 | 2.74 |
| paint_color | 1 | &lt;NA> | 32212 | 30.64 |
| paint_color | 2 | white | 22037 | 20.96 |
| paint_color | 3 | black | 14122 | 13.43 |
| paint_color | 4 | red | 9885 | 9.4 |
| paint_color | 5 | blue | 7265 | 6.91 |
| region | 1 | boise | 1038 | 0.99 |
| region | 2 | kansascity | 1012 | 0.96 |
| region | 3 | grandrapids | 918 | 0.87 |
| region | 4 | anchorage | 918 | 0.87 |
| region | 5 | sanantonio | 910 | 0.87 |
| scrape_date | 1 | 2018-10-10 00:00:00 | 16369 | 15.57 |
| scrape_date | 2 | 2020-03-22 00:00:00 | 13087 | 12.45 |
| scrape_date | 3 | 2019-10-14 00:00:00 | 13044 | 12.41 |
| scrape_date | 4 | 2019-12-02 00:00:00 | 12959 | 12.33 |
| scrape_date | 5 | 2020-01-07 00:00:00 | 12616 | 12 |
| seller | 1 | dealer | 67295 | 64.01 |
| seller | 2 | owner | 37839 | 35.99 |
| size | 1 | &lt;NA> | 65045 | 61.87 |
| size | 2 | full-size | 38324 | 36.45 |
| size | 3 | mid-size | 1765 | 1.68 |
| title_status | 1 | clean | 100356 | 95.46 |
| title_status | 2 | rebuilt | 1705 | 1.62 |
| title_status | 3 | lien | 1484 | 1.41 |
| title_status | 4 | salvage | 1077 | 1.02 |
| title_status | 5 | &lt;NA> | 382 | 0.36 |
| transmission | 1 | automatic | 99824 | 94.95 |
| transmission | 2 | manual | 3183 | 3.03 |
| transmission | 3 | other | 1784 | 1.7 |
| transmission | 4 | &lt;NA> | 343 | 0.33 |
| type | 1 | pickup | 37470 | 35.64 |
| type | 2 | truck | 35413 | 33.68 |
| type | 3 | &lt;NA> | 31147 | 29.63 |
| type | 4 | other | 642 | 0.61 |
| type | 5 | offroad | 126 | 0.12 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
