---
report_format: data-foundry-report-v2
unique_name: craigslist_used_vehicles_f150
container_format: 2
checksum: v2:5eb4bdf13ac6ca89d4dd3b6205f22f5e7ba05ba29b800869cecc7ec3a256df32
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
  n_rows: 97291
  n_features: 18
  dtypes:
    category: 10
    datetime64[ns]: 1
    float64: 6
    string: 2
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
    min: 50573
    max: 85283
  n_test:
    min: 5814
    max: 12008
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
      41.1%).'
decisions: []
---

# craigslist_used_vehicles_f150

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `price`, scored with `rmsle` on temporal splits by `scrape_date`. 97,291 rows and 18 features. Source: Kaggle (2018).

Not built yet. The current definition gives checksum `v2:5eb4bdf13ac6ca89d4dd3b6205f22f5e7ba05ba29b800869cecc7ec3a256df32`.

## In brief

**Question.** At what price is a used Ford F-150 listed on Craigslist?

**Use case.** The source names none; ours: a price guide refit once per scrape on every earlier scrape prices the next scrape's F-150 listings, for a seller or dealer setting an asking price or a buyer or marketplace judging one.

**One row.** One F-150 listing in one of nine nationwide scrapes of Craigslist's US car adverts (2018 to May 2021), one row per truck within a scrape; a truck seen again in a later test scrape keeps only its latest copy.

**Predicted.** The asking price in US dollars, from 1,000 to 150,000.

**Known at prediction time.** What the advert states: its title (numbers that could be a price removed), model year, mileage, the model string with trim and cab, condition, cylinders, fuel, title status, transmission, drive, size, body type, colour, whether an owner or a dealer sells it, the Craigslist site and its coordinates, and the scrape's date.

**What the test data stands for.** Each test set is one later scrape, with all earlier scrapes for training: the next market the price guide meets after its refit.

**Our changes to the source.** We keep the Ford F-150 of a scraped table of all makes, one row per truck within a scrape, drop a relisted truck's earlier copies (no test truck in training), placeholder prices and the 2026 scrape, set values impossible for an F-150 missing, drop the posting text and take the seller type and the title, without its numbers, from the url.

> **Use case fit: approximate (a stand-in with a known gap).** The fields are what an advert shows and the test scrapes are later markets, but the target is the asking price (a gap for a buyer who wants the sale price) and the poster types the fields in. A relisted truck's earlier copies are removed, so its dealer's knowledge of the earlier price is not part of the task.

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
| rows x columns | 97,291 x 19 |
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
<summary>Feature types: 8 categorical, 2 ordinal, 2 string, 0 datetime</summary>

- categorical (8): `seller`, `fuel`, `title_status`, `transmission`, `drive`, `type`, `paint_color`, `region`
- ordinal (2): `condition (salvage < fair < good < excellent < like new < new)`, `size (mid-size < full-size)`
- string (2): `model`, `advert_title`
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

The first 5 of 97,291 rows of the final frame (the oldest rows: the frame is sorted by `scrape_date`); 12 of 19 columns, the target first. Cells are cut at 40 characters.

| price | year | condition | cylinders | fuel | odometer | title_status | transmission | drive | size | type | paint_color |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 9.79785 | 2013 | like new | nan | gas | 113198 | clean | automatic | 4wd | full-size | truck | white |
| 8.51719 | 2008 | nan | nan | gas | 181500 | clean | automatic | nan | nan | nan | nan |
| 8.16052 | 1991 | good | 8 | gas | 74797 | clean | manual | 4wd | full-size | pickup | white |
| 9.51044 | 2008 | excellent | 8 | gas | 124500 | clean | automatic | 4wd | full-size | truck | white |
| 10.0856 | 2015 | nan | nan | gas | nan | clean | automatic | nan | nan | nan | nan |

## Curation notes

We start with the eleven Kaggle versions of austinreese/craigslist-carstrucks-data (one CSV each, every US car listing on Craigslist at the scrape) and keep the Ford F-150.

- Prediction point: when the advert is written, so every field the advert shows is known; the price arrives with it, so the split needs no gap.
- Versions and dates: each version is one scrape, dated by its upload, not by its postings: a scrape holds about five weeks of postings, which end at the upload in versions 8 and 10 (their `posting_date`) and, by listing id, 5 to 10 weeks before it in versions 2 to 6. Version 1 (uploaded 2019-10-08) is an older scrape: Craigslist issues listing ids in posting order (they follow the posting date of versions 8, 10 and 11 with a correlation of 0.99998), and all of version 1's ids lie about 277 million ids, over a year of postings, before version 2's, so it is dated 2018-10-10, the dataset's first upload: its order is measured, its date inferred (`Time: Inferred` for that period; it is training data only, and the split uses only the order). Versions 9 and 10 (2021-04-20 and 2021-05-06) share 26-27% of their listing ids and form one period (dated 2021-05-06; a listing in both kept once, from version 10); no other pair of versions shares more than 27 ids. Version 11 (2026-11-05) is left out: five years after the others, with columns of its own.
- US sites only: version 1 also holds Canadian and Mexican Craigslist sites (437 F-150 rows on craigslist.ca, prices in Canadian dollars, and 46 on craigslist.com.mx), which are dropped.
- The F-150: manufacturer `ford` and a model string starting with "f150" or "f-150" (versions 1-3 hold the model in `make`). The model string ships as text: 491 to 950 spellings a scrape (3,309 in all) that hold the trim, cab, bed and drive; a price typed into it (13 rows, such as "$21995") is removed.
- One row per truck within a scrape period: one row per VIN, then one row per model year, mileage, price and Craigslist site, and, where the mileage is no multiple of 1,000, one row per model year, mileage and price on any site: dealers post one truck on several sites, and among such groups that carry VINs, 99.8% of 11,280 carry one VIN. The cross-site step drops 3,481 rows (3.2%; 1.5% to 3.5% of each scrape, 9.5% of May 2021); the price's 10th, 50th and 90th percentiles move from 3,500, 14,995 and 33,995 to 3,500, 14,950 and 33,919 dollars. Round mileages also match by VIN (98.5% of 741 groups) but are left, 2,713 rows more. These copies never leave their scrape, so they put no test truck in training; the step keeps a test window from scoring one truck several times (up to 56).
- No test truck in training: a truck relisted in a later scrape is linked by its VIN or by its title, model year and mileage (which agree with the VIN in 93% to 99.7% of the pairs where both carry one, and find about a third more relistings; only 44% of the rows carry a VIN), and when it appears in a test scrape, its copies in earlier scrapes are dropped: 7,843 rows (7.5%), 4,415 of them from the training-only scrapes (1.0% of Oct 2018 to 16.4% of Jan 2020) and 2,258, 192, 591 and 387 from the Mar 2020 to Dec 2020 windows (their trucks are tested again later); May 2021 stays whole. Before the drop 12.6%, 18.0%, 2.2%, 5.4% and 3.2% of the Mar 2020 to May 2021 test rows had their VIN in training; after it none has an earlier copy by either link. Left: a truck whose title or mileage changed and that carries no VIN (1.5% to 2.3% of a window's test rows share model year and odd mileage with a training row, a link that agrees with the VIN in only 61% to 96%). The price's 10th, 50th and 90th percentiles move from 3,500, 14,950 and 33,919 to 3,495, 14,499 and 33,950 dollars; untuned LightGBM's RMSLE rises by 0.3% to 6.3% per window (0.314 to 0.321 on average), the part the relistings made easy.
- Title: `advert_title` is the advert's title from the url's slug (`/d/<slug>/<id>.html`, 99.9% of rows; never the posting text): from its first model-year token on (a city prefix comes before it), hyphens as spaces, every "<n>k" and every token holding a number of 1,000 or more that is no model year (1975 to the scrape's year + 1) removed, so no title states a price, a down payment or a mileage; `_clean` asserts it. It names the trim and cab that 59% of the model strings, a bare "f-150", leave out. On the shipped rows: 0 titles with 7 or more digits in a row, 42 whose model year equals the price (a 2000 truck at 2,000 dollars); 38,868 spellings; 133 missing. Untuned LightGBM with the title's words lowers RMSLE by 5.0% to 6.6% per window (0.321 to 0.302 on average; 0.314 before both changes).
- Price: listings under 1,000 or over 150,000 dollars are dropped (0 and 1 mean "call for price"; 4-13% of a scrape's F-150 rows are under 1,000), and so are placeholder prices (one digit five times or more, such as 99999, or a sequence, 1234, 12345 or 123456; 52 rows) and down payments posted as the price (under 5,000 for a truck of 2015 or newer; 124 rows). Charm prices such as 9,999 (435 rows) or 8,888 are real asking prices and stay.
- Impossible values are set missing, the row kept, one rule each: a mileage over 500,000; a model year before 1975 (the F-150's first) or after the scrape's year; front-wheel drive (no F-150 has it; 2,456 rows); cylinders other than 6 or 8 (218); size compact or sub-compact (191); fuel electric before model year 2022 (11); coordinates outside the US (53). A mileage under 100 on a truck at least two model years old is a placeholder (0, 1) and set missing too (483 rows). `cylinders` becomes a number ("other" missing); `condition` and `size` are ordered scales.
- Seller: `seller` is owner or dealer, the Craigslist section the poster picked (`/cto/` or `/ctd/` in the url): 36,982 owners and 60,309 dealers. Dealers list comparable trucks (2013-2015, 60,000 to 120,000 miles) 95 to 2,195 dollars higher in every scrape (by the median).
- Dropped: the posting text, its title column and image links (never read: 70-80% of the F-150 texts hold a phone number), the url, listing id and VIN (identifiers, used for the steps above; the url's slug ships as the title), `manufacturer` (constant), `county` (empty), `state` (absent in versions 1-3; the site and the coordinates carry it) and the site's name (spelled differently in versions 1-3): the site's subdomain in the url replaces it as `region`.
- The target ships as the log of the price; the metric is RMSLE on the price in dollars.
- Anomaly: the fields are typed in by the poster: `condition`, `cylinders`, `drive`, `size`, `type` and `paint_color` are 26-62% missing. The mileage is 32% missing in 2018 and 17-27% up to Dec 2020, then 1.7% in May 2021: Craigslist made it a required field around 30 November 2020 (version 8's weekly postings go from 14-16% missing to 4.5% that week), a change a model in use meets too.

## Splits

Five test windows, each one scrape, each trained on every earlier scrape: May 2021 (versions 9 and 10, 12,008 trucks, 87.7% of the rows in training), Dec 2020 (8,244; 79.2%), Sep 2020 (5,814; 73.2%), Jun 2020 (9,823; 63.1%) and Mar 2020 (10,829; 52.0%), with no test truck in training (a relisted truck's earlier copies are dropped). The horizon is one scrape (uploads 5 to 21 weeks apart; the scraper ran "every few months"): a pricing model refit on the listings so far meets the next market. No gap for the label: the price arrives with the advert. The scrape schedule leaves postings unseen before each window, by listing id about 7, 3, 16, 7.5 and 15 weeks before the Mar 2020 to May 2021 windows.
Every scrape whose training side keeps half the rows is a window; the older scrapes (Oct 2018, Oct 2019, Dec 2019, Jan 2020) train on 0% to 41.1% and stay training data. The Mar 2020 window clears the 50% floor only with version 1 in training (42.4% without it); version 1's order is measured from listing ids, only its date is inferred. Five windows against the nine an IID split of 97,291 trucks would get (SPLIT-15): the 50% floor stops more. The windows are named by upload; their postings are, by listing id, about Jan to mid-Feb 2020 (Mar 2020, before COVID-19), Mar to Apr 2020 (Jun 2020, the pandemic's start), Aug to early Sep 2020, 28 Oct to 3 Dec 2020 and mid-Mar to 5 May 2021, when used-truck asking prices rose (the median of comparable trucks, 2013-2015 with 60,000 to 120,000 miles, from about 21,000 dollars in Jun 2020 to about 26,000).
The 2026 scrape (version 11) is not a window: five years after the others, with trucks of model years the training data never shows.
Not declared: a seller who also knows the rest of the scrape being priced. Training on the earlier scrapes plus four fifths of the test scrape (5 random folds) scores lower than this split, by 3.2%, 2.5%, 12.3%, 2.7% and 6.6% in the Mar 2020 to May 2021 windows (untuned LightGBM, RMSLE 0.296 against 0.314 on average, measured 2026-11-25 before the relisting drop and the title), mostly the market's move within one scrape; it puts training rows beside test rows of the same period and no longer tests a model meeting a later market.

5 repeat(s) x 1 fold(s) with seed 4267; train 50,573 to 85,283 rows, test 5,814 to 12,008 rows. Prediction horizon: 1 steps.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 85283 | 12008 | 2018-10-10 00:00:00 | 2020-12-03 00:00:00 | 2021-05-06 00:00:00 | 2021-05-06 00:00:00 |
| 1 | 0 | 77039 | 8244 | 2018-10-10 00:00:00 | 2020-09-16 00:00:00 | 2020-12-03 00:00:00 | 2020-12-03 00:00:00 |
| 2 | 0 | 71225 | 5814 | 2018-10-10 00:00:00 | 2020-06-17 00:00:00 | 2020-09-16 00:00:00 | 2020-09-16 00:00:00 |
| 3 | 0 | 61402 | 9823 | 2018-10-10 00:00:00 | 2020-03-22 00:00:00 | 2020-06-17 00:00:00 | 2020-06-17 00:00:00 |
| 4 | 0 | 50573 | 10829 | 2018-10-10 00:00:00 | 2020-01-07 00:00:00 | 2020-03-22 00:00:00 | 2020-03-22 00:00:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows craigslist_used_vehicles_f150`.

| window | period | weekdays | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|---|
| 0 | May 2021 | Thu | 12008 | 0.877 | mean 9.683, median 9.852, p10 8.516, p90 10.6 | mean 9.379, median 9.546, p10 8.102, p90 10.4 | 0.707 | odometer (0.71), year (0.09), region (0.06) | 0 |
| 1 | Dec 2020 | Thu | 8244 | 0.792 | mean 9.64, median 9.852, p10 8.412, p90 10.57 | mean 9.346, median 9.51, p10 8.039, p90 10.37 | 0.165 | year (0.16), odometer (0.06), seller (0.04) | 0 |
| 2 | Sep 2020 | Wed | 5814 | 0.732 | mean 9.586, median 9.741, p10 8.294, p90 10.57 | mean 9.327, median 9.473, p10 8.006, p90 10.34 | 0.158 | year (0.16), region (0.12), seller (0.04) | 0 |
| 3 | Jun 2020 | Wed | 9823 | 0.631 | mean 9.445, median 9.607, p10 8.343, p90 10.31 | mean 9.303, median 9.469, p10 8.003, p90 10.35 | 0.086 | year (0.09), seller (0.05), region (0.04) | 0 |
| 4 | Mar 2020 | Sun | 10829 | 0.52 | mean 9.349, median 9.473, p10 8.161, p90 10.31 | mean 9.291, median 9.461, p10 7.937, p90 10.36 | 0.03 | year (0.03), seller (0.02), region (0.02) | 0.0003 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 1 exact duplicate row(s) (0.0% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)

Accepted on purpose:

- `dataset_missing_value_label`: `title_status` 'missing' is Craigslist's own option, a truck without a title document: a real state, not a missing value.
- `dataset_conflicting_duplicate_rows`: 93.6% of 1,708 same-year, same-mileage, different-price groups share a VIN: one truck at two prices within one scrape. A scrape is never cut by the split, so they stay together.
- `task_time_on_few_unique`: Nine scrape periods, one date each, by design: the scrape is the time step.
- `splits_below_target`: Five windows against nine: every scrape whose training side keeps half the rows is a window; the 50% floor stops more (Jan 2020 trains on 41.1%).

## Data checks

### Feature summary

<details>
<summary>Show the table (19 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| size | category | 59955 | 61.62 | 2 | full-size, mid-size |
| condition | category | 41951 | 43.12 | 6 | excellent, good, like new, fair, new, salvage |
| paint_color | category | 30314 | 31.16 | 12 | white, black, red, blue, silver, grey, green, brown, custom, yellow |
| type | category | 29436 | 30.26 | 13 | pickup, truck, other, offroad, sedan, SUV, van, coupe, mini-van, bus |
| drive | category | 25748 | 26.46 | 2 | 4wd, rwd |
| fuel | category | 840 | 0.86 | 4 | gas, other, diesel, hybrid |
| title_status | category | 348 | 0.36 | 6 | clean, rebuilt, lien, salvage, missing, parts only |
| transmission | category | 314 | 0.32 | 3 | automatic, manual, other |
| region | category | 0 | 0 | 413 | kansascity, boise, sanantonio, minneapolis, houston, grandrapids, dallas, tulsa… |
| seller | category | 0 | 0 | 2 | dealer, owner |
| scrape_date | datetime64\[ns\] | 0 | 0 | 9 | 2018-10-10 00:00:00, 2019-10-14 00:00:00, 2021-05-06 00:00:00, 2019-12-02 00:00… |
| cylinders | float64 | 34986 | 35.96 | 2 | 8.0, 6.0 |
| odometer | float64 | 21810 | 22.42 | 41180 | 150000.0, 200000.0, 180000.0, 160000.0, 170000.0, 130000.0, 190000.0, 140000.0,… |
| lat | float64 | 695 | 0.71 | 33059 | 29.8135, 38.9847, 42.8511, 46.2348, 33.7792, 43.1824, 33.7865, 42.8511, 35.199,… |
| long | float64 | 695 | 0.71 | 34031 | -82.472, -88.1704, -83.4512, -119.128, -84.4118, -84.1122, -84.4454, -83.4512, … |
| year | float64 | 284 | 0.29 | 48 | 2013.0, 2014.0, 2016.0, 2010.0, 2015.0, 2018.0, 2011.0, 2012.0, 2017.0, 2008.0 |
| price | float64 | 0 | 0 | 9409 | 7.824, 8.1605, 8.4118, 8.7796, 8.6125, 8.0064, 7.3132, 7.6009, 8.9227, 8.5172 |
| advert_title | string | 133 | 0.14 | 38868 | 2016 ford 150 xlt, 2018 ford 150 xlt, 2017 ford 150 xlt, 2015 ford 150 xlt, 201… |
| model | string | 0 | 0 | 3309 | f-150, f150, f-150 xlt, f150 xlt, f150 4x4, f-150 lariat, f150 supercrew cab, f… |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | -0.589 | -0.788 | 0.793 | 0.01 | log | 910084 | 8.84173e+17 | exponential |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| price | 97291 | 9.41099 | 0.890454 | 6.90776 | 11.8492 |
| year | 97007 | 2009.44 | 7.29083 | 1975 | 2022 |
| cylinders | 62305 | 7.28706 | 0.957922 | 6 | 8 |
| odometer | 75481 | 113483 | 63527.5 | 0 | 480000 |
| lat | 96596 | 38.4794 | 6.10116 | 17.2656 | 65.8122 |
| long | 96596 | -94.4928 | 16.1682 | -159.59 | -67.0074 |

### Categorical features

<details>
<summary>Show the table (57 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| advert_title | 1 | 2016 ford 150 xlt | 643 | 0.66 |
| advert_title | 2 | 2018 ford 150 xlt | 612 | 0.63 |
| advert_title | 3 | 2017 ford 150 xlt | 431 | 0.44 |
| advert_title | 4 | 2015 ford 150 xlt | 379 | 0.39 |
| advert_title | 5 | 2013 ford 150 xlt | 361 | 0.37 |
| condition | 1 | &lt;NA> | 41951 | 43.12 |
| condition | 2 | excellent | 25124 | 25.82 |
| condition | 3 | good | 20856 | 21.44 |
| condition | 4 | like new | 5715 | 5.87 |
| condition | 5 | fair | 3235 | 3.33 |
| drive | 1 | 4wd | 55564 | 57.11 |
| drive | 2 | &lt;NA> | 25748 | 26.46 |
| drive | 3 | rwd | 15979 | 16.42 |
| fuel | 1 | gas | 92377 | 94.95 |
| fuel | 2 | other | 3776 | 3.88 |
| fuel | 3 | &lt;NA> | 840 | 0.86 |
| fuel | 4 | diesel | 263 | 0.27 |
| fuel | 5 | hybrid | 35 | 0.04 |
| model | 1 | f-150 | 47705 | 49.03 |
| model | 2 | f150 | 12269 | 12.61 |
| model | 3 | f-150 xlt | 3170 | 3.26 |
| model | 4 | f150 xlt | 2838 | 2.92 |
| model | 5 | f150 4x4 | 2762 | 2.84 |
| paint_color | 1 | &lt;NA> | 30314 | 31.16 |
| paint_color | 2 | white | 20096 | 20.66 |
| paint_color | 3 | black | 12919 | 13.28 |
| paint_color | 4 | red | 9120 | 9.37 |
| paint_color | 5 | blue | 6699 | 6.89 |
| region | 1 | kansascity | 951 | 0.98 |
| region | 2 | boise | 943 | 0.97 |
| region | 3 | sanantonio | 875 | 0.9 |
| region | 4 | minneapolis | 858 | 0.88 |
| region | 5 | houston | 842 | 0.87 |
| scrape_date | 1 | 2018-10-10 00:00:00 | 16209 | 16.66 |
| scrape_date | 2 | 2019-10-14 00:00:00 | 12237 | 12.58 |
| scrape_date | 3 | 2021-05-06 00:00:00 | 12008 | 12.34 |
| scrape_date | 4 | 2019-12-02 00:00:00 | 11577 | 11.9 |
| scrape_date | 5 | 2020-03-22 00:00:00 | 10829 | 11.13 |
| seller | 1 | dealer | 60309 | 61.99 |
| seller | 2 | owner | 36982 | 38.01 |
| size | 1 | &lt;NA> | 59955 | 61.62 |
| size | 2 | full-size | 35680 | 36.67 |
| size | 3 | mid-size | 1656 | 1.7 |
| title_status | 1 | clean | 92744 | 95.33 |
| title_status | 2 | rebuilt | 1605 | 1.65 |
| title_status | 3 | lien | 1438 | 1.48 |
| title_status | 4 | salvage | 1026 | 1.05 |
| title_status | 5 | &lt;NA> | 348 | 0.36 |
| transmission | 1 | automatic | 92270 | 94.84 |
| transmission | 2 | manual | 3100 | 3.19 |
| transmission | 3 | other | 1607 | 1.65 |
| transmission | 4 | &lt;NA> | 314 | 0.32 |
| type | 1 | pickup | 34099 | 35.05 |
| type | 2 | truck | 32707 | 33.62 |
| type | 3 | &lt;NA> | 29436 | 30.26 |
| type | 4 | other | 606 | 0.62 |
| type | 5 | offroad | 122 | 0.13 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
