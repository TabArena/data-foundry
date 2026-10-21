---
report_format: data-foundry-report-v2
unique_name: african_credit_scoring_challenge
container_format: 2
checksum: v2:ce2bf2e2e4d01e49c2cc2a9920af6c019b6250daf0591bbeb2426d01254317f2
build: null
build_stale: false
data:
  n_rows: 58953
  n_features: 10
  dtypes:
    category: 5
    datetime64[ns]: 2
    float64: 3
    int64: 1
  n_test_dataset_rows: null
task:
  target: default
  problem_type: binary_classification
  metric: f1
  split_regime: temporal_non_iid
  stratify_on: default
  time_on: disbursement_date
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 9
  n_folds: 1
  random_state: 4267
  time_horizon: 30
  time_horizon_unit: days
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 29819
    max: 57573
  n_test:
    min: 500
    max: 2206
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  - dataset_conflicting_duplicate_rows
  accepted:
    dataset_pure_feature_value: The hits are 11 disbursement dates of 13-30 July 2022,
      the due dates of those 7-day loans (9 dates from 21 July to 5 August) and the
      due date 2022-09-19 (608 rows, 3 defaults). July 2022 was the first month of
      the Type_1 product, and its Type_1 rows default at 0.37% against 0.88-1.49%
      in August-November (1.99% overall). Default-size repay charges are as rare there
      (0.42%), so the low rate belongs to the period, which a model sees at disbursement,
      and does not hide defaults. None of these rows is a test row, and all but 4
      (60- and 90-day Type_4 loans of 27-28 July) are on every training side.
    splits_rows_unused: '6 loans of 60-365 days, disbursed on 2023-09-19 and from
      2024-06-11 to 2024-06-15, settle from 2024-09-09 (the first day of the newest
      window) to 2024-10-18: no window may train on them, and they were disbursed
      before the oldest 2024 window starts (2024-07-11).'
decisions:
- 'Total_Amount_to_Repay and Lender_portion_to_be_repaid are dropped: recorded after
  the outcome'
- 'Rows whose lender funds less than one unit are dropped: labelled 0 whatever the
  customer did'
- A label counts as settled 30 days after the due date
- 'Test windows: the end of the Type_1 lending and the newest 90 days, none longer
  than 30 days'
---

# african_credit_scoring_challenge

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Binary classification of `default`, scored with `f1` on temporal splits by `disbursement_date`. 58,953 rows and 10 features. Source: Zindi (2024).

Not built yet. The current definition gives checksum `v2:ce2bf2e2e4d01e49c2cc2a9920af6c019b6250daf0591bbeb2426d01254317f2`.

## In brief

**Question.** Will a borrower in Kenya default on a loan that has just been paid out?

**Use case.** When a loan is disbursed, a lender scores the customer's risk of default from the loan's terms and the customer's settled earlier loans, and refits the model at least once a month on the loans whose outcome it knows.

**One row.** One lender's part of one loan in Kenya, October 2021 to October 2024 (a loan with two lenders gives two rows); 54,163 of the 58,953 rows are from July to November 2022, mostly 7-day loans of one product.

**Predicted.** The loan's default, recorded on each lender row as it stood when the data was pulled (about 2% of rows; the two rows of a loan share the label in 2,132 of 2,134 loans). A label counts as settled 30 days after the due date; the source states no other horizon.

**Known at prediction time.** The customer (as an id, so the same customer's settled earlier loans can be in training), new or repeat customer, the lender, the loan product, amount and duration, the disbursement and due dates, the lender's funded amount and share.

**What the test data stands for.** Nine test windows of at most 30 days: six at the end of the 2022 lending of the main product and three at the end of the data in 2024. Each trains on the loans whose label had settled before the window starts.

**Our changes to the source.** We drop the amounts to repay, which grow after a default, the rows of lenders funding less than one unit (labelled no default whatever happened) and the loans not settled at the data pull, and we split by disbursement date where the competition split rows at random.

> **Use case fit: approximate (a stand-in with a known gap).** The customer's history is known only through labels settled before each window, while a lender learns of a repayment the day it is made. How the loans were sampled is not stated.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`explore.ipynb`](explore.ipynb) | The workbench for looking at the data (`ds = workbench()`), committed without outputs. Not needed to rebuild. |
| [`REVIEW.md`](REVIEW.md) | The open questions for the curator, removed once they are settled. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/african_credit_scoring_challenge.md`](../../../../curation/records/african_credit_scoring_challenge.md)
- The original source: <https://zindi.africa/competitions/african-credit-scoring-challenge>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/african_credit_scoring_challenge/`. To get them:

```text
The Zindi data page needs a login. We download a Kaggle copy of the competition files that a participant
(Kaggle user thelastsmilodon, 32nd place) uploaded on 2025-01-14, two days after submissions closed, with the
licence "other" and no description. Its Train.csv, Test.csv, economic_indicators.csv and
VariableDefinitions.txt have the byte sizes the Zindi data page lists (8,785,708, 2,379,732, 7,930 and 1,539).
The upload has no version, so we record the SHA-256 of our files (first 16 hex digits): Train.csv
20d437430408084a, Test.csv 8d31edd85335c681, economic_indicators.csv bc49ee02a535465a, VariableDefinitions.txt
0cc43fb6c53d6503.

mkdir -p local-data-warehouse/african_credit_scoring_challenge
uvx --from kaggle==2.2.2 kaggle datasets download thelastsmilodon/african-credit-scoring-challenge-data -p local-data-warehouse/african_credit_scoring_challenge
unzip local-data-warehouse/african_credit_scoring_challenge/african-credit-scoring-challenge-data.zip -d local-data-warehouse/african_credit_scoring_challenge/
rm local-data-warehouse/african_credit_scoring_challenge/african-credit-scoring-challenge-data.zip
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/african_credit_scoring_challenge   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/african_credit_scoring_challenge   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Zindi: https://zindi.africa/competitions/african-credit-scoring-challenge |
| year | 2024 |
| domain | finance |
| license | Zindi Competition Rules |
| data_tags | Non-IID, Temporal |
| reference | Zindi2024AfricanCreditScoringChallenge |
| rows x columns | 58,953 x 11 |
| task.target | default |
| task.problem_type | binary_classification |
| task.metric | f1 |
| task.split_regime | temporal_non_iid |
| task.stratify_on | default |
| task.time_on | disbursement_date |

<details>
<summary>Feature types: 5 categorical, 0 string, 2 datetime</summary>

- categorical (5): `customer_id`, `lender_id`, `loan_type`, `New_versus_Repeat`, `default`
- string (0): none
- datetime (2): `disbursement_date (%Y-%m-%d)`, `due_date (%Y-%m-%d)`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{Zindi2024AfricanCreditScoringChallenge,
  author = {{Zindi}},
  title = {African Credit Scoring Challenge},
  year = {2024},
  howpublished = {\url{https://zindi.africa/competitions/african-credit-scoring-challenge}},
  note = {Zindi competition, 2024-11-29 to 2025-01-12}
}
```

</details>

## Sample rows

The first 5 of 58,953 rows of the final frame (the oldest rows: the frame is sorted by `disbursement_date`). Cells are cut at 40 characters.

| default | customer_id | lender_id | loan_type | Total_Amount | disbursement_date | due_date | duration | New_versus_Repeat | Amount_Funded_By_Lender | Lender_portion_Funded |
|---|---|---|---|---|---|---|---|---|---|---|
| No | 245749 | 245684 | Type_12 | 10000 | 2021-10-04 00:00:00 | 2021-11-03 00:00:00 | 30 | New Loan | 10000 | 1 |
| No | 245655 | 245684 | Type_12 | 10000 | 2021-10-13 00:00:00 | 2021-10-27 00:00:00 | 14 | New Loan | 10000 | 1 |
| No | 245959 | 245684 | Type_12 | 15600 | 2021-10-14 00:00:00 | 2021-10-21 00:00:00 | 7 | Repeat Loan | 15600 | 1 |
| No | 134790 | 245684 | Type_11 | 1105 | 2021-11-16 00:00:00 | 2021-12-16 00:00:00 | 30 | Repeat Loan | 1105 | 1 |
| No | 245959 | 245684 | Type_12 | 15600 | 2021-11-18 00:00:00 | 2021-11-25 00:00:00 | 7 | Repeat Loan | 15600 | 1 |

## Curation notes

We start with Train.csv of the Zindi African Credit Scoring Challenge, from a Kaggle copy of the competition files.

- Prediction point: when a loan is disbursed, with the customer's settled earlier loans known.
- We rename target to default. The competition scored F1, which we declare (TP-6).
- We add no count of a loan's other lender rows: built from the rows present at the data pull, which buy-outs can change, it cannot be dated to disbursement. Test.csv (no labels) is read only for decision table 2.
- We drop ID and tbl_loan_id (identifiers) and country_id (Kenya in every row).
- We drop Total_Amount_to_Repay and Lender_portion_to_be_repaid: recorded at the data pull, they grow with a defaulted loan's days past due (decision table).
- We drop the 8,899 rows whose lender funds less than one unit (Amount_Funded_By_Lender below 0.5): none is labelled 1, where about 105 would be expected at the rate of their months, and for the same customers and months 1.04% of them carry a default-size repay charge against 0.40% of the customers' other loans. They are labelled 0 whatever the customer did and hide about 90-130 defaults (decision table).
- Unsettled labels: recent defaults include late payments paid later (decision table, counted per loan). A label counts as settled 30 days after the due date, a conservative cut rather than a measured end of settlement, and we drop the 802 rows due less than 30 days before the data pull.
- Temporal split on disbursement_date: 9 test windows of at most 30 days, each training on the loans settled before it starts (splits comment).
- customer_id stays as a categorical: an entity's own history is legitimate under a temporal split (ieee_fraud_detection's uid). A default usually ends a customer's history, which made "the customer's last loan" a winning rule in the competition's random split; here a training side holds only settled loans.
- lender_id, loan_type and New_versus_Repeat are categoricals. New_versus_Repeat differs between a loan's two rows in 133 of the 2,134 two-row loans, so we read it per lender.
- disbursement_date and due_date are datetimes; we keep due_date, disbursement_date plus duration, as a source column.
- We do not join economic_indicators.csv: for Kenya alone it is a function of the year, with no values for 2024.
- Duplicates: the 275 extra copies of identical rows have their own tbl_loan_id and share a date; we keep them as separate loans.
- Anomaly: 54,163 of the 58,953 rows are from July to November 2022 (1.16% defaults), mostly Type_1 7-day loans. The source does not say how the loans were sampled.
- One row funds 2,627.1 of a loan of 2,249 (share 1.168): we set its Amount_Funded_By_Lender and Lender_portion_Funded to missing.
- Potential leak, kept on purpose: Amount_Funded_By_Lender and Lender_portion_Funded are values at the data pull, and lenders can buy each other out (host). Within a loan product they show no link to the outcome (ROC AUC 0.46 and 0.49 alone on the Type_1 rows); the link over all rows is the mix of products. Kept like kick's unverified host fields; revisit if the host documents when shares are recorded.
- Note: the task probes flag no_spread, drift_baseline and unstable; we keep the task under task_probes.md rules 1-3 and 9 (weak separation on windows of 20-56 default rows; the drift is in log loss; LightGBM falls just below the class shares on the oldest 2024 window only, skill -0.03, and beats them on the other 4 probed windows). Re-check against tuned runs.
- Licence: the Zindi rules call the data "private property of the client"; the Kaggle copy is a participant's upload.

## Splits

A lender scores each loan when it is disbursed and refits on the loans whose outcome it knows, at least once a month: no test window is longer than 30 days, the declared horizon. A loan's label counts as known 30 days after its due date, so each training side holds the loans whose due date lies more than 30 days before the window starts; loans disbursed in the weeks before a window, and longer loans still running, are not in that window's training side. The windows cover the two periods with enough loans for such windows, newest first: three 30-day windows at the end of the data (2024-07-11 to 2024-10-08, all but 9 rows Type_7 loans; 500-677 rows, 296-394 loans and 32-56 default rows each) and six windows of about equal numbers of rows at the end of the Type_1 lending, from 2022-10-20 (the first day by which half of all rows have a settled label) to 2022-12-01 (the last Type_1 loan; 5-10 days, 1,812-2,206 rows and 20-31 default rows each). A row is one lender's part of a loan, so a two-lender loan counts twice. The 1,901 rows between (2022-12-02 to 2024-07-10, about 100 a month of changing products) are too few for 30-day test windows and are training data only, apart from 6 long loans that settle on or after the first day of the newest window and so are in no split. The 2024 windows test a new product: Type_7 loans, first lent on 2023-07-27, with 98-688 Type_7 rows on their training sides and 12-44% of their test rows from a customer seen in training. Their labels are 30-119 days past due at the data pull; counted per loan, 2024 loans 31-45 days past due default at 7.2% (15 of 209) against 5.8-9.8% in each later bucket and 11.8-20.4% before 30 days (decision table 3), so the 30-day cut is conservative at this edge, not a measured end of settlement. The 2022 windows leave out the 8-18% of the rows of their dates whose lender funds less than one unit (curation comments). Nine windows of equal numbers of rows from 2022-10-20 (the v1 notebook's equal buckets) would test 2022-12-16 to 2024-07-10 as one window: one model for 573 days, with 28% of the window's rows in products that have no training row. Windows of equal numbers of distinct dates, as in kick, would put all 9 windows between March 2023 and October 2024 (112 to 872 rows and 9 to 72 default rows each) and leave 95% of the rows for training only.

9 repeat(s) x 1 fold(s) with seed 4267; train 29,819 to 57,573 rows, test 500 to 2,206 rows. Prediction horizon: 30 days.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 57573 | 677 | 2021-10-04 00:00:00 | 2024-08-02 00:00:00 | 2024-09-09 00:00:00 | 2024-10-08 00:00:00 |
| 1 | 0 | 57076 | 593 | 2021-10-04 00:00:00 | 2024-07-03 00:00:00 | 2024-08-10 00:00:00 | 2024-09-08 00:00:00 |
| 2 | 0 | 56938 | 500 | 2021-10-04 00:00:00 | 2024-05-13 00:00:00 | 2024-07-11 00:00:00 | 2024-08-09 00:00:00 |
| 3 | 0 | 41843 | 2131 | 2021-10-04 00:00:00 | 2022-10-15 00:00:00 | 2022-11-22 00:00:00 | 2022-12-01 00:00:00 |
| 4 | 0 | 39566 | 2071 | 2021-10-04 00:00:00 | 2022-10-08 00:00:00 | 2022-11-15 00:00:00 | 2022-11-21 00:00:00 |
| 5 | 0 | 36968 | 1931 | 2021-10-04 00:00:00 | 2022-10-01 00:00:00 | 2022-11-08 00:00:00 | 2022-11-14 00:00:00 |
| 6 | 0 | 34009 | 2206 | 2021-10-04 00:00:00 | 2022-09-29 00:00:00 | 2022-10-31 00:00:00 | 2022-11-07 00:00:00 |
| 7 | 0 | 31845 | 1969 | 2021-10-04 00:00:00 | 2022-09-17 00:00:00 | 2022-10-25 00:00:00 | 2022-10-29 00:00:00 |
| 8 | 0 | 29819 | 1812 | 2021-10-04 00:00:00 | 2022-09-12 00:00:00 | 2022-10-20 00:00:00 | 2022-10-24 00:00:00 |

## Decisions

### 1. Total_Amount_to_Repay and Lender_portion_to_be_repaid are dropped: recorded after the outcome

A repaid Type_7 row owes a median 3.5% over Total_Amount at 1-240 days past due at the data pull (2.0% for the 69 rows of 2023); a defaulted one owes more the longer it has been overdue (penalties). Lender_portion_to_be_repaid is the lender's part of that amount.

| days past due at the pull | defaulted: rows | repaid: rows | defaulted: median charge | repaid: median charge |
|---|---|---|---|---|
| 1-30 | 89 | 529 | 0.0461 | 0.0351 |
| 31-60 | 44 | 598 | 0.0766 | 0.0351 |
| 61-120 | 89 | 1003 | 0.0931 | 0.0351 |
| 121-240 | 10 | 201 | 0.2447 | 0.0352 |
| 241-480 | 3 | 69 | 0.3388 | 0.02 |

### 2. Rows whose lender funds less than one unit are dropped: labelled 0 whatever the customer did

None of the 8,899 rows whose lender funds less than one unit (8,520 with no share) is labelled 1. For the customers with Type_1 loans of both kinds in the same months, 1.04% of these rows carry a default-size repay charge (over 20%), against 0.40% of the customers' other loans, where such a charge means label 1 in 89% of cases; after a charged loan of either kind the customer almost never borrowed again. The rows hide about 90 defaults of these customers (about 130 in all) under the label 0.

| lender amount | repay charge | loans | labelled 1 | customer borrowed again after the due date |
|---|---|---|---|---|
| 0.5 or more | over 20% | 114 | 101 | 0 |
| 0.5 or more | up to 20% | 28480 | 26 | 0.879 |
| below 0.5 (dropped) | over 20% | 90 | 0 | 0.011 |
| below 0.5 (dropped) | up to 20% | 8577 | 0 | 0.869 |

### 3. A label counts as settled 30 days after the due date

Of the 2024 loans, counted once per loan, 20.4% of those 1-7 days overdue at the pull are labelled 1 and 11.8-14.9% of those 8-30 days overdue, against 5.8-9.8% from 31 days on (7.2% at 31-45 days), so recent defaults include late payments that are paid later. 30 days is a conservative cut, not a measured end of settlement. Loans due less than 30 days before the pull are dropped, and each training side holds only loans settled before its window starts.

| days past due at the pull | loans | defaults | default_rate |
|---|---|---|---|
| 1-7 | 93 | 19 | 0.204 |
| 8-14 | 74 | 11 | 0.149 |
| 15-30 | 203 | 24 | 0.118 |
| 31-45 | 209 | 15 | 0.072 |
| 46-60 | 173 | 10 | 0.058 |
| 61-90 | 367 | 33 | 0.09 |
| 91-120 | 302 | 25 | 0.083 |
| 121-180 | 172 | 13 | 0.076 |
| 181-365 | 92 | 9 | 0.098 |

### 4. Test windows: the end of the Type_1 lending and the newest 90 days, none longer than 30 days

Three 30-day windows end on 2024-10-08; six windows of about equal numbers of rows run from 2022-10-20, the first day by which half of all rows have a settled label, to the last Type_1 loan (2022-12-01). A row is one lender's part of a loan. The rows between are training data only.

| window | first day | last day | test rows | test loans | default rows | defaulted loans | default rate | training rows | test rows of a customer in training | rows dropped for the lender amount |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2024-09-09 | 2024-10-08 | 677 | 394 | 51 | 28 | 0.075 | 57573 | 0.44 | 0 |
| 1 | 2024-08-10 | 2024-09-08 | 593 | 359 | 56 | 34 | 0.094 | 57076 | 0.25 | 0 |
| 2 | 2024-07-11 | 2024-08-09 | 500 | 296 | 32 | 21 | 0.064 | 56938 | 0.12 | 0 |
| 3 | 2022-11-22 | 2022-12-01 | 2131 | 2086 | 29 | 24 | 0.014 | 41843 | 0.96 | 0.152 |
| 4 | 2022-11-15 | 2022-11-21 | 2071 | 2040 | 28 | 26 | 0.014 | 39566 | 0.94 | 0.153 |
| 5 | 2022-11-08 | 2022-11-14 | 1931 | 1903 | 20 | 20 | 0.01 | 36968 | 0.93 | 0.179 |
| 6 | 2022-10-31 | 2022-11-07 | 2206 | 2181 | 31 | 30 | 0.014 | 34009 | 0.89 | 0.174 |
| 7 | 2022-10-25 | 2022-10-29 | 1969 | 1945 | 21 | 20 | 0.011 | 31845 | 0.85 | 0.082 |
| 8 | 2022-10-20 | 2022-10-24 | 1812 | 1795 | 21 | 20 | 0.012 | 29819 | 0.85 | 0.107 |

## Bundle checks

0 error(s), 0 warning(s), 2 info (26 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 275 exact duplicate row(s) (0.5% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)
- **info** `dataset_conflicting_duplicate_rows`: 1 row(s) (0.0%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)

Accepted on purpose:

- `dataset_pure_feature_value`: The hits are 11 disbursement dates of 13-30 July 2022, the due dates of those 7-day loans (9 dates from 21 July to 5 August) and the due date 2022-09-19 (608 rows, 3 defaults). July 2022 was the first month of the Type_1 product, and its Type_1 rows default at 0.37% against 0.88-1.49% in August-November (1.99% overall). Default-size repay charges are as rare there (0.42%), so the low rate belongs to the period, which a model sees at disbursement, and does not hide defaults. None of these rows is a test row, and all but 4 (60- and 90-day Type_4 loans of 27-28 July) are on every training side.
- `splits_rows_unused`: 6 loans of 60-365 days, disbursed on 2023-09-19 and from 2024-06-11 to 2024-06-15, settle from 2024-09-09 (the first day of the newest window) to 2024-10-18: no window may train on them, and they were disbursed before the oldest 2024 window starts (2024-07-11).

## Data checks

### Feature summary

<details>
<summary>Show the table (11 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| customer_id | category | 0 | 0 | 6363 | 247613, 250874, 259757, 260083, 255356, 262000, 249457, 246888, 254014, 263235 |
| lender_id | category | 0 | 0 | 4 | 267278, 251804, 267277, 245684 |
| loan_type | category | 0 | 0 | 19 | Type_1, Type_7, Type_5, Type_4, Type_10, Type_6, Type_9, Type_14, Type_2, Type_… |
| New_versus_Repeat | category | 0 | 0 | 2 | Repeat Loan, New Loan |
| default | category | 0 | 0 | 2 | No, Yes |
| disbursement_date | datetime64\[ns\] | 0 | 0 | 732 | 2022-07-16 00:00:00, 2022-07-25 00:00:00, 2022-08-01 00:00:00, 2022-07-23 00:00… |
| due_date | datetime64\[ns\] | 0 | 0 | 847 | 2022-07-23 00:00:00, 2022-08-01 00:00:00, 2022-08-08 00:00:00, 2022-07-30 00:00… |
| Total_Amount | float64 | 0 | 0 | 17497 | 1500.0, 5000.0, 10000.0, 2199.0, 4699.0, 2000.0, 4989.0, 6499.0, 2250.0, 15000.0 |
| Amount_Funded_By_Lender | float64 | 1 | 0 | 23152 | 450.0, 1000.0, 600.0, 659.7, 1496.7, 1200.0, 1949.7, 1409.7, 10000.0, 675.0 |
| Lender_portion_Funded | float64 | 1 | 0 | 12270 | 0.3, 0.2, 0.16, 0.5, 0.1333, 0.25, 1.0, 0.2375, 0.1333, 0.375 |
| duration | int64 | 0 | 0 | 61 | 7, 14, 30, 90, 60, 45, 31, 29, 25, 92 |

</details>

### Target distribution

| default | count | pct |
|---|---|---|
| No | 57779 | 98.01 |
| Yes | 1174 | 1.99 |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| Total_Amount | 58953 | 15566.1 | 152185 | 2 | 2.3e+07 |
| duration | 58953 | 8.71094 | 11.752 | 1 | 548 |
| Amount_Funded_By_Lender | 58952 | 2919.89 | 12732.1 | 0.5 | 1.6e+06 |
| Lender_portion_Funded | 58952 | 0.252118 | 0.10598 | 7.92984e-06 | 1 |

### Categorical features

<details>
<summary>Show the table (28 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| New_versus_Repeat | 1 | Repeat Loan | 58429 | 99.11 |
| New_versus_Repeat | 2 | New Loan | 524 | 0.89 |
| customer_id | 1 | 247613 | 192 | 0.33 |
| customer_id | 2 | 250874 | 159 | 0.27 |
| customer_id | 3 | 259757 | 127 | 0.22 |
| customer_id | 4 | 260083 | 115 | 0.2 |
| customer_id | 5 | 255356 | 105 | 0.18 |
| default | 1 | No | 57779 | 98.01 |
| default | 2 | Yes | 1174 | 1.99 |
| disbursement_date | 1 | 2022-07-16 00:00:00 | 938 | 1.59 |
| disbursement_date | 2 | 2022-07-25 00:00:00 | 887 | 1.5 |
| disbursement_date | 3 | 2022-08-01 00:00:00 | 884 | 1.5 |
| disbursement_date | 4 | 2022-07-23 00:00:00 | 872 | 1.48 |
| disbursement_date | 5 | 2022-07-30 00:00:00 | 853 | 1.45 |
| due_date | 1 | 2022-07-23 00:00:00 | 940 | 1.59 |
| due_date | 2 | 2022-08-01 00:00:00 | 887 | 1.5 |
| due_date | 3 | 2022-08-08 00:00:00 | 885 | 1.5 |
| due_date | 4 | 2022-07-30 00:00:00 | 871 | 1.48 |
| due_date | 5 | 2022-08-06 00:00:00 | 865 | 1.47 |
| lender_id | 1 | 267278 | 55373 | 93.93 |
| lender_id | 2 | 251804 | 3149 | 5.34 |
| lender_id | 3 | 267277 | 243 | 0.41 |
| lender_id | 4 | 245684 | 188 | 0.32 |
| loan_type | 1 | Type_1 | 52826 | 89.61 |
| loan_type | 2 | Type_7 | 2053 | 3.48 |
| loan_type | 3 | Type_5 | 1521 | 2.58 |
| loan_type | 4 | Type_4 | 1235 | 2.09 |
| loan_type | 5 | Type_10 | 464 | 0.79 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
