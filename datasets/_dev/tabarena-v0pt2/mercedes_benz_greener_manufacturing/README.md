---
report_format: data-foundry-report-v2
unique_name: mercedes_benz_greener_manufacturing
container_format: 2
checksum: v2:b8629e3d00921aba00d5e2c984318cbea4a19a968f5956ac364f4bbc3d67d244
build:
  uuid: 01a21800-41be-73a4-9ad1-3eab14ef72b3
  checksum: v2:b8629e3d00921aba00d5e2c984318cbea4a19a968f5956ac364f4bbc3d67d244
  built_at: '2026-11-26T13:16:42+00:00'
  path: mercedes_benz_greener_manufacturing/01a21800-41be-73a4-9ad1-3eab14ef72b3
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
  n_rows: 4204
  n_features: 374
  dtypes:
    category: 373
    float64: 1
    int64: 1
  n_test_dataset_rows: null
task:
  target: y
  problem_type: regression
  metric: r2
  metric_origin: source
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: time_index
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 9
  n_folds: 1
  random_state: 4267
  time_horizon: 233
  time_horizon_unit: steps
  time_gap: null
  time_gap_unit: null
  reason: 'The car ID is the only order: the competition ships no dates, does not
    confirm that the IDs follow the order of testing, and held out its own test cars
    at random. Each test window is a run of 233 consecutive cars in ID order, trained
    on every earlier car (Andrej, 2026-11-19). No source gives a length (the 320 cars
    used until then were the arithmetic of the first curation''s scikit-learn TimeSeriesSplit):
    half the cars come before ID 4,230, so nine windows, the count an IID task of
    this size gets (3 x 3), all train on half the cars or more only at 233 cars each,
    which fill the newest half (2,097 test cars). The windows walk back from the newest;
    with no dates there is no season or period to choose between. No gap is needed:
    a car''s testing time is known when it leaves the bench, and no row carries a
    date to measure a longer delay.

    How the data arrives (Andrej, 2026-11-06): the bench time is known when the car
    leaves the bench, minutes after its configuration is fixed, so a model refit at
    a window''s start knows every earlier car. The ID is taken as the testing order;
    the dropped code X5 forms 29 levels in 31 contiguous runs of IDs, about 200 cars
    each in this file, likely production periods. A window''s first cars share their
    block with the newest training cars, but the block explains about 1% of the variance
    of the bench time (block means 96.1 to 102.6 s). A configuration tested again
    (15% to 27% of a window''s test cars, with the six coded categories kept) is the
    car''s known history, not a leak.'
  n_train:
    min: 2107
    max: 3971
  n_test:
    min: 233
    max: 233
bundle_checks:
  ok: true
  errors: []
  warnings:
  - dataset_constant_column
  - dataset_duplicate_columns
  infos: []
  accepted: {}
decisions: []
---

# mercedes_benz_greener_manufacturing

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `y`, scored with `r2` on temporal splits by `time_index`. 4,204 rows and 374 features. Source: Kaggle (2017).

Built as `01a21800-41be-73a4-9ad1-3eab14ef72b3` on 2026-11-26. See [Build](#build).

## In brief

**Question.** How long will a car with a given set of options take to pass the test bench?

**Use case.** For example, Mercedes-Benz plans its test bench by predicting how long each car configuration will take to pass testing; the competition aimed to cut the time cars spend on the bench.

**One row.** One Mercedes-Benz car that passed the test bench, ordered by its ID (4,204 cars; dates not stated).

**Predicted.** The time the car took to pass testing, in seconds (72 to 170, mean about 101).

**Known at prediction time.** The car's options, anonymized, as six coded categories and several hundred yes/no options (the source's examples are four-wheel drive or a head-up display).

**What the test data stands for.** The newest 2,097 cars form 9 test windows of 233 cars in ID order, each trained on all earlier cars: the newest on 3,971 cars (94%), the oldest on 2,107 (50%).

**Our changes to the source.** We order the cars by ID and test on later ones; we drop the coded category that marks time groups, a near-constant coded category with its 4 unusual rows, and one outlier testing time.

> **Use case fit: approximate (a stand-in with a known gap).** The car ID stands in for the order of testing, which the source does not confirm, and without dates the time a test window spans is unknown.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/mercedes_benz_greener_manufacturing.md`](../../../../curation/records/mercedes_benz_greener_manufacturing.md)
- The original source: <https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/mercedes_benz_greener_manufacturing/`. To get them:

```text
We use the train.csv from the Kaggle competition.

kaggle competitions download -c mercedes-benz-greener-manufacturing -f train.csv.zip && unzip train.csv.zip &&  rm train.csv.zip
mkdir -p local-data-warehouse/mercedes_benz_greener_manufacturing && mv train.csv local-data-warehouse/mercedes_benz_greener_manufacturing/
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/mercedes_benz_greener_manufacturing   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/mercedes_benz_greener_manufacturing   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing |
| year | 2017 |
| domain | industry & manufacturing |
| license | Kaggle Competition Rules |
| data_tags | Non-IID, Temporal, Anonymized |
| reference | Novy2017MercedesBenzGreenerManufacturing |
| rows x columns | 4,204 x 375 |
| task.target | y |
| task.problem_type | regression |
| task.metric | r2 |
| task.split_regime | temporal_non_iid |
| task.time_on | time_index |

**Metric**

| field | value |
|---|---|
| name | `r2` (standard; takes value; higher is better) |
| origin | source: the source's metric |
| original | R^2 score (coefficient of determination) |
| reference | https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing/overview/evaluation |
| definition | Coefficient of determination of the test time y |

<details>
<summary>Feature types: 373 categorical, 0 string, 0 datetime</summary>

- categorical (373): `X0`, `X1`, `X2`, `X3`, `X6`, `X8`, `X10`, `X12`, `X13`, `X14`, `X15`, `X16`, `X17`, `X18`, `X19`, `X20`, `X21`, `X22`, `X23`, `X24`, `X26`, `X27`, `X28`, `X29`, `X30`, `X31`, `X32`, `X33`, `X34`, `X35`, `X36`, `X37`, `X38`, `X39`, `X40`, `X41`, `X42`, `X43`, `X44`, `X45`, `X46`, `X47`, `X48`, `X49`, `X50`, `X51`, `X52`, `X53`, `X54`, `X55`, `X56`, `X57`, `X58`, `X59`, `X60`, `X61`, `X62`, `X63`, `X64`, `X65`, `X66`, `X67`, `X68`, `X69`, `X70`, `X71`, `X73`, `X74`, `X75`, `X76`, `X77`, `X78`, `X79`, `X80`, `X81`, `X82`, `X83`, `X84`, `X85`, `X86`, `X87`, `X88`, `X89`, `X90`, `X91`, `X92`, `X93`, `X94`, `X95`, `X96`, `X97`, `X98`, `X99`, `X100`, `X101`, `X102`, `X103`, `X104`, `X105`, `X106`, `X107`, `X108`, `X109`, `X110`, `X111`, `X112`, `X113`, `X114`, `X115`, `X116`, `X117`, `X118`, `X119`, `X120`, `X122`, `X123`, `X124`, `X125`, `X126`, `X127`, `X128`, `X129`, `X130`, `X131`, `X132`, `X133`, `X134`, `X135`, `X136`, `X137`, `X138`, `X139`, `X140`, `X141`, `X142`, `X143`, `X144`, `X145`, `X146`, `X147`, `X148`, `X150`, `X151`, `X152`, `X153`, `X154`, `X155`, `X156`, `X157`, `X158`, `X159`, `X160`, `X161`, `X162`, `X163`, `X164`, `X165`, `X166`, `X167`, `X168`, `X169`, `X170`, `X171`, `X172`, `X173`, `X174`, `X175`, `X176`, `X177`, `X178`, `X179`, `X180`, `X181`, `X182`, `X183`, `X184`, `X185`, `X186`, `X187`, `X189`, `X190`, `X191`, `X192`, `X194`, `X195`, `X196`, `X197`, `X198`, `X199`, `X200`, `X201`, `X202`, `X203`, `X204`, `X205`, `X206`, `X207`, `X208`, `X209`, `X210`, `X211`, `X212`, `X213`, `X214`, `X215`, `X216`, `X217`, `X218`, `X219`, `X220`, `X221`, `X222`, `X223`, `X224`, `X225`, `X226`, `X227`, `X228`, `X229`, `X230`, `X231`, `X232`, `X233`, `X234`, `X235`, `X236`, `X237`, `X238`, `X239`, `X240`, `X241`, `X242`, `X243`, `X244`, `X245`, `X246`, `X247`, `X248`, `X249`, `X250`, `X251`, `X252`, `X253`, `X254`, `X255`, `X256`, `X257`, `X258`, `X259`, `X260`, `X261`, `X262`, `X263`, `X264`, `X265`, `X266`, `X267`, `X268`, `X269`, `X270`, `X271`, `X272`, `X273`, `X274`, `X275`, `X276`, `X277`, `X278`, `X279`, `X280`, `X281`, `X282`, `X283`, `X284`, `X285`, `X286`, `X287`, `X288`, `X289`, `X290`, `X291`, `X292`, `X293`, `X294`, `X295`, `X296`, `X297`, `X298`, `X299`, `X300`, `X301`, `X302`, `X304`, `X305`, `X306`, `X307`, `X308`, `X309`, `X310`, `X311`, `X312`, `X313`, `X314`, `X315`, `X316`, `X317`, `X318`, `X319`, `X320`, `X321`, `X322`, `X323`, `X324`, `X325`, `X326`, `X327`, `X328`, `X329`, `X330`, `X331`, `X332`, `X333`, `X334`, `X335`, `X336`, `X337`, `X338`, `X339`, `X340`, `X341`, `X342`, `X343`, `X344`, `X345`, `X346`, `X347`, `X348`, `X349`, `X350`, `X351`, `X352`, `X353`, `X354`, `X355`, `X356`, `X357`, `X358`, `X359`, `X360`, `X361`, `X362`, `X363`, `X364`, `X365`, `X366`, `X367`, `X368`, `X369`, `X370`, `X371`, `X372`, `X373`, `X374`, `X375`, `X376`, `X377`, `X378`, `X379`, `X380`, `X382`, `X383`, `X384`, `X385`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{Novy2017MercedesBenzGreenerManufacturing,
  author = {Alexander Novy and CH1Mercedes and Christian Drescher and Christian Pfaundler and KOESIM and Will Cukierski},
  title  = {Mercedes-Benz Greener Manufacturing},
  year   = {2017},
  howpublished = {\url{https://kaggle.com/competitions/mercedes-benz-greener-manufacturing}},
  note   = {Kaggle competition}
}
```

</details>

## Sample rows

The first 5 of 4,204 rows of the final frame (the oldest rows: the frame is sorted by `time_index`); 12 of 375 columns, the target first. Cells are cut at 40 characters.

| y | time_index | X0 | X1 | X2 | X3 | X6 | X8 | X10 | X12 | X13 | X14 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 130.81 | 0 | k | v | at | a | j | o | 0 | 0 | 1 | 0 |
| 88.53 | 6 | k | t | av | e | l | o | 0 | 0 | 0 | 0 |
| 76.26 | 7 | az | w | n | c | j | x | 0 | 0 | 0 | 0 |
| 80.62 | 9 | az | t | n | f | l | e | 0 | 0 | 0 | 0 |
| 78.02 | 13 | az | v | n | f | d | n | 0 | 0 | 0 | 0 |

## Curation notes

We start with the train.csv from Kaggle.

- The data has been anonymized, so feature meanings are unknown.
- There is generally weird behavior related to the ID and potentially a time column (see X5 here https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing/discussion/34949). However, it is hard to parse the exact details due to anonymization. We generally take from this that the data is sorted sequentially by ID and that there may be time dependencies. Also checkout https://www.kaggle.com/code/sudalairajkumar/simple-exploration-notebook-mercedes which shows relation between index and y, showing that y goes up with higher index and it shows that X5 (the time group feature), has the highest importance. Plus, it has one outlier.
- We remove the one outlier from y.
  Why it may leave (CLEAN-11, amended 2026-10-21): it is a single extreme target in the training period only. The car took 265.3 s against a next highest of 169.9 s (mean 100.7 s, sd 12.7 s), and it is car 883 of 4,209 in ID order, among the oldest cars that every test window trains on (the oldest window trains on the first 2,107 cars of the cleaned data). The competition host does not name the row; it leaves as the field's expert default for a single extreme testing time (CLEAN-11 allows the source's words or the experts' default, case by case; Lennart, 2026-10-21).
- We drop X5 as it leaks time group information in temporal splits (besides having a full categorical-value distribution shift with a temporal split).
- We tread the ID as a time_index.
- There are exactly 4 rows that have value that is not equal to "d" in column "X4". This indicates some kind of sub-group or data different. Given the lack of semantics and anonymity, we cannot parse the meaning of "X4". Thus, to avoid this being an indicator of data leakage, we remove these rows and subsequently drop "X4" as well.
- Of the coded categories (X0-X8) we keep X0, X1, X2, X3, X6 and X8 and drop only X5 (time marker) and X4 (near constant). X3, X6 and X8 were once dropped "to be safe"; a check on the competition's file (2026-11-06) found no time pattern in them: their link to the ID decile (Cramér's V, shuffled IDs in brackets) is X3 0.176 (0.047), X6 0.055 (0.050), X8 0.086 (0.076), close to the kept X0 to X2 (0.108 to 0.138 against 0.078 to 0.106), against X5 0.928 (0.080); no level of the three is confined to a part of the ID range, and each X8 level spans the IDs from the first to the last hundred. Adding them changed the R² of untuned LightGBM by +0.0015 (standard error 0.0039) over the 9 windows of 320 cars then shipped, so they stay as columns of the car's configuration (columns leave for what they are, not for being unexplained; Andrej, 2026-11-11). The 0/1 options from X10 on stay, except X11, which is constant (11 other constant options, such as X93, stay).

## Splits

Expanding-window temporal splits: 9 test window(s) of 233 rows, walking back from the newest data, newest first; train is all earlier data. The test windows by `time_index`, as listed: 7973 to 8417 (233 test, 3,971 train rows); 7499 to 7972 (233 test, 3,738 train rows); 7005 to 7498 (233 test, 3,505 train rows); 6539 to 7004 (233 test, 3,272 train rows); 6111 to 6538 (233 test, 3,039 train rows); 5630 to 6103 (233 test, 2,806 train rows); 5163 to 5627 (233 test, 2,573 train rows); 4701 to 5162 (233 test, 2,340 train rows); 4230 to 4699 (233 test, 2,107 train rows).

The car ID is the only order: the competition ships no dates, does not confirm that the IDs follow the order of testing, and held out its own test cars at random. Each test window is a run of 233 consecutive cars in ID order, trained on every earlier car (Andrej, 2026-11-19). No source gives a length (the 320 cars used until then were the arithmetic of the first curation's scikit-learn TimeSeriesSplit): half the cars come before ID 4,230, so nine windows, the count an IID task of this size gets (3 x 3), all train on half the cars or more only at 233 cars each, which fill the newest half (2,097 test cars). The windows walk back from the newest; with no dates there is no season or period to choose between. No gap is needed: a car's testing time is known when it leaves the bench, and no row carries a date to measure a longer delay.
How the data arrives (Andrej, 2026-11-06): the bench time is known when the car leaves the bench, minutes after its configuration is fixed, so a model refit at a window's start knows every earlier car. The ID is taken as the testing order; the dropped code X5 forms 29 levels in 31 contiguous runs of IDs, about 200 cars each in this file, likely production periods. A window's first cars share their block with the newest training cars, but the block explains about 1% of the variance of the bench time (block means 96.1 to 102.6 s). A configuration tested again (15% to 27% of a window's test cars, with the six coded categories kept) is the car's known history, not a leak.

9 repeat(s) x 1 fold(s) with seed 4267; train 2,107 to 3,971 rows, test 233 rows. Prediction horizon: 233 steps.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 3971 | 233 | 0 | 7972 | 7973 | 8417 |
| 1 | 0 | 3738 | 233 | 0 | 7498 | 7499 | 7972 |
| 2 | 0 | 3505 | 233 | 0 | 7004 | 7005 | 7498 |
| 3 | 0 | 3272 | 233 | 0 | 6538 | 6539 | 7004 |
| 4 | 0 | 3039 | 233 | 0 | 6103 | 6111 | 6538 |
| 5 | 0 | 2806 | 233 | 0 | 5627 | 5630 | 6103 |
| 6 | 0 | 2573 | 233 | 0 | 5162 | 5163 | 5627 |
| 7 | 0 | 2340 | 233 | 0 | 4699 | 4701 | 5162 |
| 8 | 0 | 2107 | 233 | 0 | 4229 | 4230 | 4699 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows mercedes_benz_greener_manufacturing`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | 7973 - 8417 | 233 | 0.945 | mean 98.87, median 97.99, p10 86.4, p90 112.1 | mean 100.7, median 99.16, p10 88.14, p90 115.4 | 0.573 | X2 (0.57), X38 (0.53), X0 (0.39) | 0.0086 |
| 1 | 7499 - 7972 | 233 | 0.889 | mean 99.09, median 98.61, p10 86.98, p90 113.8 | mean 100.8, median 99.19, p10 88.21, p90 115.6 | 0.403 | X38 (0.40), X3 (0.40), X0 (0.30) | 0.0043 |
| 2 | 7005 - 7498 | 233 | 0.834 | mean 99.52, median 98.1, p10 88.4, p90 114.1 | mean 100.9, median 99.26, p10 88.2, p90 115.7 | 0.436 | X3 (0.44), X38 (0.31), X0 (0.26) | 0 |
| 3 | 6539 - 7004 | 233 | 0.778 | mean 99.01, median 97.63, p10 87.44, p90 112.7 | mean 101, median 99.46, p10 88.24, p90 115.9 | 0.444 | X3 (0.44), X2 (0.34), X0 (0.30) | 0.0129 |
| 4 | 6111 - 6538 | 233 | 0.723 | mean 100.5, median 98.45, p10 88.1, p90 114.4 | mean 101.1, median 99.49, p10 88.26, p90 116 | 0.722 | X3 (0.72), X2 (0.30), X1 (0.22) | 0.0086 |
| 5 | 5630 - 6103 | 233 | 0.667 | mean 101, median 99.01, p10 88.37, p90 116.4 | mean 101.1, median 99.53, p10 88.25, p90 116 | 0.55 | X3 (0.55), X0 (0.30), X2 (0.22) | 0 |
| 6 | 5163 - 5627 | 233 | 0.612 | mean 101.5, median 100.2, p10 88.44, p90 117.1 | mean 101.1, median 99.51, p10 88.25, p90 115.8 | 0.527 | X3 (0.53), X2 (0.30), X0 (0.26) | 0.0043 |
| 7 | 4701 - 5162 | 233 | 0.557 | mean 102.6, median 100.2, p10 87.98, p90 119.6 | mean 100.9, median 99.41, p10 88.29, p90 115.5 | 0.505 | X0 (0.51), X2 (0.30), X1 (0.26) | 0.0043 |
| 8 | 4230 - 4699 | 233 | 0.501 | mean 99.86, median 98.12, p10 87.84, p90 114 | mean 101, median 99.52, p10 88.35, p90 115.7 | 0.505 | X3 (0.51), X2 (0.29), X0 (0.24) | 0.0172 |

## Bundle checks

0 error(s), 2 warning(s), 0 info (28 checks run, plus the dataset's own checks).

- **warning** `dataset_constant_column`: 11 constant column(s) (1 distinct non-null value): ['X93', 'X107', 'X233', 'X235', 'X268']. (hint: Drop them unless the constant is meaningful for the task.)
- **warning** `dataset_duplicate_columns`: 45 duplicated column pair(s): [('X31', 'X35'), ('X31', 'X37'), ('X33', 'X39'), ('X54', 'X76'), ('X71', 'X84')]. (hint: Keep one column of each pair.)

## Data checks

### Feature summary

<details>
<summary>Show the table (375 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| X0 | category | 0 | 0 | 47 | z, ak, y, ay, t, x, o, f, n, w |
| X1 | category | 0 | 0 | 27 | aa, s, b, l, v, r, i, a, c, o |
| X2 | category | 0 | 0 | 44 | as, ae, ai, m, ak, r, n, s, f, e |
| X3 | category | 0 | 0 | 7 | c, f, a, d, g, e, b |
| X6 | category | 0 | 0 | 12 | g, j, d, i, l, a, h, k, c, b |
| X8 | category | 0 | 0 | 25 | j, s, f, n, i, e, r, a, w, v |
| X10 | category | 0 | 0 | 2 | 0, 1 |
| X12 | category | 0 | 0 | 2 | 0, 1 |
| X13 | category | 0 | 0 | 2 | 0, 1 |
| X14 | category | 0 | 0 | 2 | 0, 1 |
| X15 | category | 0 | 0 | 2 | 0, 1 |
| X16 | category | 0 | 0 | 2 | 0, 1 |
| X17 | category | 0 | 0 | 2 | 0, 1 |
| X18 | category | 0 | 0 | 2 | 0, 1 |
| X19 | category | 0 | 0 | 2 | 0, 1 |
| X20 | category | 0 | 0 | 2 | 0, 1 |
| X21 | category | 0 | 0 | 2 | 0, 1 |
| X22 | category | 0 | 0 | 2 | 0, 1 |
| X23 | category | 0 | 0 | 2 | 0, 1 |
| X24 | category | 0 | 0 | 2 | 0, 1 |
| X26 | category | 0 | 0 | 2 | 0, 1 |
| X27 | category | 0 | 0 | 2 | 1, 0 |
| X28 | category | 0 | 0 | 2 | 0, 1 |
| X29 | category | 0 | 0 | 2 | 0, 1 |
| X30 | category | 0 | 0 | 2 | 0, 1 |
| X31 | category | 0 | 0 | 2 | 0, 1 |
| X32 | category | 0 | 0 | 2 | 0, 1 |
| X33 | category | 0 | 0 | 2 | 0, 1 |
| X34 | category | 0 | 0 | 2 | 0, 1 |
| X35 | category | 0 | 0 | 2 | 0, 1 |
| X36 | category | 0 | 0 | 2 | 0, 1 |
| X37 | category | 0 | 0 | 2 | 0, 1 |
| X38 | category | 0 | 0 | 2 | 0, 1 |
| X39 | category | 0 | 0 | 2 | 0, 1 |
| X40 | category | 0 | 0 | 2 | 0, 1 |
| X41 | category | 0 | 0 | 2 | 0, 1 |
| X42 | category | 0 | 0 | 2 | 0, 1 |
| X43 | category | 0 | 0 | 2 | 0, 1 |
| X44 | category | 0 | 0 | 2 | 0, 1 |
| X45 | category | 0 | 0 | 2 | 0, 1 |
| X46 | category | 0 | 0 | 2 | 1, 0 |
| X47 | category | 0 | 0 | 2 | 0, 1 |
| X48 | category | 0 | 0 | 2 | 0, 1 |
| X49 | category | 0 | 0 | 2 | 0, 1 |
| X50 | category | 0 | 0 | 2 | 0, 1 |
| X51 | category | 0 | 0 | 2 | 1, 0 |
| X52 | category | 0 | 0 | 2 | 0, 1 |
| X53 | category | 0 | 0 | 2 | 0, 1 |
| X54 | category | 0 | 0 | 2 | 0, 1 |
| X55 | category | 0 | 0 | 2 | 0, 1 |
| X56 | category | 0 | 0 | 2 | 0, 1 |
| X57 | category | 0 | 0 | 2 | 0, 1 |
| X58 | category | 0 | 0 | 2 | 1, 0 |
| X59 | category | 0 | 0 | 2 | 0, 1 |
| X60 | category | 0 | 0 | 2 | 0, 1 |
| X61 | category | 0 | 0 | 2 | 1, 0 |
| X62 | category | 0 | 0 | 2 | 0, 1 |
| X63 | category | 0 | 0 | 2 | 0, 1 |
| X64 | category | 0 | 0 | 2 | 0, 1 |
| X65 | category | 0 | 0 | 2 | 0, 1 |

(315 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0.738 | 0.278 | 154.196 | 0.015 | log | 57845.6 | 60798.8 | exponential |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| time_index | 4204 | 4208.08 | 2438.25 | 0 | 8417 |
| y | 4204 | 100.619 | 12.4176 | 72.11 | 169.91 |

### Categorical features

<details>
<summary>Show the table (753 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| X0 | 1 | z | 359 | 8.54 |
| X0 | 2 | ak | 348 | 8.28 |
| X0 | 3 | y | 323 | 7.68 |
| X0 | 4 | ay | 313 | 7.45 |
| X0 | 5 | t | 306 | 7.28 |
| X1 | 1 | aa | 833 | 19.81 |
| X1 | 2 | s | 598 | 14.22 |
| X1 | 3 | b | 592 | 14.08 |
| X1 | 4 | l | 589 | 14.01 |
| X1 | 5 | v | 408 | 9.71 |
| X10 | 1 | 0 | 4148 | 98.67 |
| X10 | 2 | 1 | 56 | 1.33 |
| X100 | 1 | 1 | 2903 | 69.05 |
| X100 | 2 | 0 | 1301 | 30.95 |
| X101 | 1 | 1 | 3934 | 93.58 |
| X101 | 2 | 0 | 270 | 6.42 |
| X102 | 1 | 0 | 4175 | 99.31 |
| X102 | 2 | 1 | 29 | 0.69 |
| X103 | 1 | 1 | 3299 | 78.47 |
| X103 | 2 | 0 | 905 | 21.53 |
| X104 | 1 | 0 | 4196 | 99.81 |
| X104 | 2 | 1 | 8 | 0.19 |
| X105 | 1 | 0 | 4194 | 99.76 |
| X105 | 2 | 1 | 10 | 0.24 |
| X106 | 1 | 0 | 4149 | 98.69 |
| X106 | 2 | 1 | 55 | 1.31 |
| X107 | 1 | 0 | 4204 | 100 |
| X108 | 1 | 0 | 4142 | 98.53 |
| X108 | 2 | 1 | 62 | 1.47 |
| X109 | 1 | 0 | 4034 | 95.96 |
| X109 | 2 | 1 | 170 | 4.04 |
| X110 | 1 | 0 | 4200 | 99.9 |
| X110 | 2 | 1 | 4 | 0.1 |
| X111 | 1 | 1 | 4099 | 97.5 |
| X111 | 2 | 0 | 105 | 2.5 |
| X112 | 1 | 0 | 4192 | 99.71 |
| X112 | 2 | 1 | 12 | 0.29 |
| X113 | 1 | 0 | 4111 | 97.79 |
| X113 | 2 | 1 | 93 | 2.21 |
| X114 | 1 | 0 | 3590 | 85.39 |
| X114 | 2 | 1 | 614 | 14.61 |
| X115 | 1 | 0 | 3004 | 71.46 |
| X115 | 2 | 1 | 1200 | 28.54 |
| X116 | 1 | 0 | 3377 | 80.33 |
| X116 | 2 | 1 | 827 | 19.67 |
| X117 | 1 | 0 | 3997 | 95.08 |
| X117 | 2 | 1 | 207 | 4.92 |
| X118 | 1 | 1 | 2616 | 62.23 |
| X118 | 2 | 0 | 1588 | 37.77 |
| X119 | 1 | 1 | 2616 | 62.23 |
| X119 | 2 | 0 | 1588 | 37.77 |
| X12 | 1 | 0 | 3888 | 92.48 |
| X12 | 2 | 1 | 316 | 7.52 |
| X120 | 1 | 1 | 4027 | 95.79 |
| X120 | 2 | 0 | 177 | 4.21 |
| X122 | 1 | 0 | 4174 | 99.29 |
| X122 | 2 | 1 | 30 | 0.71 |
| X123 | 1 | 0 | 4193 | 99.74 |
| X123 | 2 | 1 | 11 | 0.26 |
| X124 | 1 | 0 | 4202 | 99.95 |

(693 more rows not shown)

</details>

## Build

| field | value |
|---|---|
| uuid | 01a21800-41be-73a4-9ad1-3eab14ef72b3 |
| checksum | v2:b8629e3d00921aba00d5e2c984318cbea4a19a968f5956ac364f4bbc3d67d244 |
| built_at | 2026-11-26T13:16:42+00:00 |
| path | mercedes_benz_greener_manufacturing/01a21800-41be-73a4-9ad1-3eab14ef72b3 |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
