---
report_format: data-foundry-report-v2
unique_name: consumer_complaints_1m
container_format: 2
checksum: v2:56836ef7f8abe260378a4a10fe3e2c974383d315e689f9c2b5c09341f0c704d9
build:
  uuid: 01a217f6-76b0-7b60-b916-08d61cf191cc
  checksum: v2:56836ef7f8abe260378a4a10fe3e2c974383d315e689f9c2b5c09341f0c704d9
  built_at: '2026-11-26T13:07:21+00:00'
  path: consumer_complaints_1m/01a217f6-76b0-7b60-b916-08d61cf191cc
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
  n_rows: 3361291
  n_features: 12
  dtypes:
    category: 9
    datetime64[ns]: 1
    string: 3
  n_test_dataset_rows: null
task:
  target: Company response to consumer
  problem_type: multiclass_classification
  metric: log_loss
  metric_origin: fallback
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: Company response to consumer
  time_on: Date received
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 3
  n_folds: 1
  random_state: 4267
  time_horizon: 3
  time_horizon_unit: months
  time_gap: 1
  time_gap_unit: months
  reason: 'We try to create splits that simulate a model deployed to solve the task.


    - The official data is updated daily. The CFPB publishes no model and no refit
    cadence, so we simulate a model that is refit every three months and then deployed.
    The quarter is our assumption: it is longer than the 15 to 60 days a closure takes
    (a company "provides a response within 15 calendar days" and has "up to 60 calendar
    days to provide a final response", https://www.consumerfinance.gov/compliance/consumer-complaint-program/company-process/;
    the 180 days we wrote before are the deadline of the optional public response),
    and a quarter holds 200k to 350k complaints.

    - This introduces the unrealistic downside of data shift within a quarter that
    a model refit more often would not meet.

    - A one-month gap (Andrej, 2026-11-19): the train side ends a month before each
    quarter, as a refit at the start of the quarter would not yet hold most of the
    last month''s closures (at the download of 2026-01-23, 70% of December, 14% of
    November and 7% of October 2025 were still in progress). Measured (2026-11-18,
    equal training size, 3 seeds): leaving out the 30 days before each quarter worsens
    log loss by 0.004 to 0.017, broadly rather than through company waves, so recent
    closures carry a shortcut a deployed model would not have. A 60-day gap would
    put July-September 2024 under half the complaints (49.6%).


    The newest quarter is always tested. The other two are spread evenly over the
    six quarters from July 2024 on, the oldest whose train side holds half the complaints,
    so they test other seasons and another year (the curator''s choice of 2026-11-10)
    and hold the two changes a deployed model met in that time: July-September 2024
    falls before the closure mix moved ("Closed with explanation" was 51% to 57% of
    each quarter of 2024 and 57% to 67% of 2025), and January-March 2025 holds the
    wave of January 2025 (165,305 complaints that month; 12.9% of the quarter about
    money transfers, mostly Block, Inc. (Cash App) and Early Warning Services (Zelle)).'
  n_train:
    min: 1772438
    max: 3158152
  n_test:
    min: 203139
    max: 350790
  row_budget:
    train: 1000000
    test: 500000
  train_sampling:
    default: newest_year
    unit: rows
    stratify_on: Company response to consumer
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos: []
  accepted:
    dataset_pure_feature_value: 'Block, Inc. (Cash App) closes 99.8% of its complaints
      with an explanation throughout 2019-2025: a company response policy, and the
      company is known when the complaint is filed.'
    time_newest_period_short: 'Decided (Lennart, 2026-11-11): December 2025 holds
      54,655 complaints against 73,058 to 77,970 a month from September to November,
      as complaints still in progress when the archive was taken are left out (curation_comments,
      the closures in progress).'
decisions: []
---

# consumer_complaints_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Multiclass classification of `Company response to consumer`, scored with `log_loss` on temporal splits by `Date received`. 3,361,291 rows and 12 features. Source: GOV Website (2026).

Built as `01a217f6-76b0-7b60-b916-08d61cf191cc` on 2026-11-26. See [Build](#build).

## In brief

**Question.** Will a company close a consumer's complaint with an explanation only, or with non-monetary or monetary relief?

**Use case.** For example, when a complaint about a financial product reaches the US Consumer Financial Protection Bureau (CFPB), the bureau or the company estimates how it will be closed, to spot complaints likely to end in relief.

**One row.** One complaint to the CFPB from a US state, received from 24 April 2017 to 31 December 2025, whose consumer agreed to publish the written account.

**Predicted.** How the company closed it (a company responds within 15 days and gives its final response within up to 60): with an explanation (64.89%), with non-monetary relief (33.08%) or with monetary relief (2.03%).

**Known at prediction time.** The date received, the product and issue with their sub-categories, the company, the state and ZIP code (masked for small places), whether the consumer is an older American or a servicemember, and the consumer's written complaint.

**What the test data stands for.** Each test window is one quarter, as for a model we assume is refit every three months: October-December 2025, January-March 2025 and July-September 2024, three seasons in two years. Training is every earlier complaint from April 2017 on, of which a benchmark fits on a million: by default the newest year, extended back in time until it holds a million, and a random million of those.

**Our changes to the source.** We drop the company's public response, which leaks the outcome, keep complaints with a published text from after consumer disputes ended (April 2017), and build from the CFPB's archive, in which every 2025 label is settled.

> **Use case fit: direct (the rows, features and split mirror the use case).** Everything the model sees is in the complaint when it is filed, every label is settled, and later quarters are tested. Only complaints whose consumer agreed to publish the text are included, a narrower group than all complaints.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/consumer_complaints.md`](../../../../curation/records/consumer_complaints.md)
- The original source: <https://www.consumerfinance.gov/data-research/consumer-complaints/>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/consumer_complaints/`. To get them:

```text
The CFPB removed the complaint narratives from the live database download on 2026-09-14 and archived every
previously published complaint in its FOIA reading room as CCDB exports (one zip per period, exported
2026-09-14, with the narratives and the company responses as of that date):
https://www.consumerfinance.gov/foia-requests/foia-electronic-reading-room/cfpb-consumer-complaint-database-narratives-archive/
We use the exports up to December 2025 (downloaded 2026-10-01) and keep the zips as they are:

mkdir -p local-data-warehouse/consumer_complaints/foia_archive && cd local-data-warehouse/consumer_complaints/foia_archive
for f in 1_December_2011_through_April_2018             2_May_2018_through_April_2021             3_May_2021_through_October_2022             4_November_2022_through_August_2023             5_September_2023_through_March_2024             6_April_2024_through_July_2024             7_August_2024_through_October_2024             8_November_2024_through_December_2024             9_January_2025_through_February_2025             10_March_2025_through_April_2025             11_May_2025_through_June_2025             12_July_2025_through_August_2025             13_September_2025_through_October_2025             14_November_2025_through_December_2025; do
    wget https://files.consumerfinance.gov/f/documents/CCDB_Export_${f}.zip
done
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/consumer_complaints_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/consumer_complaints_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | GOV Website: https://www.consumerfinance.gov/data-research/consumer-complaints/ |
| year | 2026 |
| domain | finance |
| license | U.S. Government Works |
| data_tags | Non-IID, Temporal, Spatial |
| reference | cfpb2025ConsumerComplaintDatabase |
| rows x columns | 3,361,291 x 13 |
| task.target | Company response to consumer |
| task.problem_type | multiclass_classification |
| task.metric | log_loss |
| task.split_regime | temporal_non_iid |
| task.stratify_on | Company response to consumer |
| task.time_on | Date received |

**Metric**

| field | value |
|---|---|
| name | `log_loss` (standard; takes proba; lower is better) |
| origin | fallback: the default for the problem type: the source defines no metric the task would use in practice |
| definition | mean of -log p(true class) |
| reason | The CFPB database is a public register with no prediction task; the task is our adaptation following a benchmark paper, not an original task with a defined metric. |

<details>
<summary>Feature types: 9 categorical, 3 string, 1 datetime</summary>

- categorical (9): `Product`, `Sub-product`, `Issue`, `Sub-issue`, `State`, `Low population area`, `Tag: Older American`, `Tag: Servicemember`, `Company response to consumer`
- string (3): `Company`, `Consumer complaint narrative`, `ZIP code`
- datetime (1): `Date received`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{cfpb2025ConsumerComplaintDatabase,
  author       = {{Consumer Financial Protection Bureau}},
  title        = {Consumer Complaint Database},
  year         = {2025},
  howpublished = {\url{https://www.consumerfinance.gov/data-research/consumer-complaints/}},
  note         = {Narratives archive (FOIA reading room), exported 2026-09-14. Accessed: 2026-10-01},
}
```

</details>

## Sample rows

The first 5 of 3,361,291 rows of the final frame (the oldest rows: the frame is sorted by `Date received`); 12 of 13 columns, the target first. Cells are cut at 40 characters.

| Company response to consumer | Date received | Product | Sub-product | Issue | Sub-issue | Consumer complaint narrative | Company | State | ZIP code | Low population area | Tag: Older American |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Closed with explanation | 2017-04-24 00:00:00 | Credit reporting, credit repair service… | Credit reporting | Improper use of your report | Report provided to employer without you… | XXXX I am NOT XXXX customer. I am not X… | Experian Information Solutions Inc. | VA | 222XX | True | nan |
| Closed with explanation | 2017-04-24 00:00:00 | Mortgage | FHA mortgage | Problem with a credit reporting company… | Investigation took more than 30 days | Loancare took over my mortgage in XXXX … | LoanCare, LLC | NJ | 08844 | False | nan |
| Closed with explanation | 2017-04-24 00:00:00 | Payday loan, title loan, or personal lo… | Personal line of credit | Charged fees or interest you didn't exp… | nan | I obtained a loan and was not told they… | CURO Intermediate Holdings | TN | 379XX | True | nan |
| Closed with explanation | 2017-04-24 00:00:00 | Credit reporting, credit repair service… | Credit reporting | Incorrect information on your report | Public record information inaccurate | There is a Tax Lien that was filed with… | EQUIFAX, INC. | GA | 30157 | False | nan |
| Closed with explanation | 2017-04-24 00:00:00 | Credit reporting, credit repair service… | Credit reporting | Incorrect information on your report | Public record information inaccurate | XXXX XXXX XXXX Has been reporting since… | EQUIFAX, INC. | FL | 32114 | False | False |

## Curation notes

The dataset on Kaggle (https://www.kaggle.com/datasets/selener/consumer-complaint-database) has data from up until 2019. We use the government data up to the end of 2025.

- Source history: the CFPB stopped publishing complaint narratives on 2026-08-14 and removed them from the live download on 2026-09-14; the live file no longer has the narrative or the consent column. We therefore build from the FOIA narratives archive (exported 2026-09-14). Its labels are settled: an earlier build from the 2026-01-23 download filtered out complaints still "In progress" (7% of Oct, 14% of Nov and 70% of Dec 2025), which biased the test months towards quickly closed complaints.
- Compared with the 2026-01-23 download, the archive has the same labels for all 3.49M shared complaints, 64,743 more closed complaints (mostly Nov-Dec 2025), Windows line endings in 2017-2020 narratives (normalised) and fewer fully masked ZIP codes ("XXXXX": 1.8% instead of 4.8%).
- We stop at 2025-12-31. Complaints received in 2026 rarely have a published narrative (3.5% in March, 1.5% in July, none in August 2026, against 16% in November 2025), so they are a small and differently selected sample.

- Context and descriptions of the features can be found here: https://cfpb.github.io/api/ccdb/fields.html
- "Company public response" is not free text but selected "from a set list of options".
- Following TexTabBench, we focus on predicting the type of closure a complaint got, that is the "Company response to consumer" column. We want to predict if a complaint will be closed with just an explanation, with non-monetary relief, or with monetary relief.
- We filter the data to only include entries after consumer disputations were discontinued as this represent a shift in protocol. This filters all data before April 24th 2017.
- We keep only complaints whose "Company response to consumer" is one of the three closure types, dropping those still "In progress", marked "Untimely response" or without a response (0.2% of the complaints with a published narrative).
- We filter all rows without a published complaint narrative (only complaints whose consumer consented to sharing it have one; the archive has no consent column). This ensures the data contains text sentences.
- We drop "Company public response" and "Timely response?": both are recorded when the company responds, at the same time as the closure type we predict.
- We only allow complaints from US states (no territories or international complaints) and remove cases with missing states.
- The data has unresolved spatial information in the ZIP code. Some ZIPs are censored (ending in "XXX" or full removed "XXXXXX").
- We add a feature for "Low population area", which determines that the ZIP is censored.
- The tags filed contains only three non-nan labels, of which one is a duplicate of the others. We created two categorical features from it instead.
- We drop duplicates (2% of the data) as the data should not contain naturally occurring duplicates and this likely results from some overlap in data collection or data entry or faulty re-submissions. We investigated some of the duplicates and they appear to be identical complaints. There exist duplicates with different target labels, we also drop these as we have no way to determine what the correct label is (all copies are dropped).
- We drop constant columns, the complaint ID, and when the complaint was send to the company (as it does not related to the target task)
- The class shares shift over time (from the v1 exploration, counted 2026-10-22 on the cleaned data): "Closed with explanation" is 85% of 2017, 54% of 2024 and 63% of 2025, "Closed with non-monetary relief" 10%, 44% and 35%, and "Closed with monetary relief" 4.5%, 1.7% and 1.3%. In the three test quarters (July-September 2024, January-March 2025 and October-December 2025) explanation is 55%, 66% and 67%, monetary relief 1.5%, 1.1% and 1.8%.
- The row budget: We test October-December 2025, January-March 2025 and July-September 2024. Each quarter keeps at most 500k of its rows (v2 split protocol; all of them here, 204k to 351k), and each train side holds every earlier complaint, so the container holds every complaint. The container records the 1M train budget, and a benchmark sub-samples each train side to 1M rows before a fit (`subsample_train`; by default the newest year before the quarter, extended back in time until it holds 1M rows, and a random 1M of those). Over eight years of history, a sample of all of it would dilute the recent complaints, and the class shares have shifted over time (above).

## Splits

Expanding-window temporal splits: 3 test window(s) of 3 months, starting at 2025-10-01, 2025-01-01, 2024-07-01, newest first; train is all earlier data up to a gap of 1 months. The test windows by `Date received`, as listed: 2025-10-01 to 2025-12-31 (203,139 test, 3,158,152 train rows); 2025-01-01 to 2025-03-31 (350,790 test, 2,198,684 train rows); 2024-07-01 to 2024-09-30 (213,655 test, 1,772,438 train rows). Each test window keeps at most 500k of its rows, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows (by default rows drawn at random from the newest year before each window, extended back in time until it holds that many rows, `subsample_train`).

We try to create splits that simulate a model deployed to solve the task.

- The official data is updated daily. The CFPB publishes no model and no refit cadence, so we simulate a model that is refit every three months and then deployed. The quarter is our assumption: it is longer than the 15 to 60 days a closure takes (a company "provides a response within 15 calendar days" and has "up to 60 calendar days to provide a final response", https://www.consumerfinance.gov/compliance/consumer-complaint-program/company-process/; the 180 days we wrote before are the deadline of the optional public response), and a quarter holds 200k to 350k complaints.
- This introduces the unrealistic downside of data shift within a quarter that a model refit more often would not meet.
- A one-month gap (Andrej, 2026-11-19): the train side ends a month before each quarter, as a refit at the start of the quarter would not yet hold most of the last month's closures (at the download of 2026-01-23, 70% of December, 14% of November and 7% of October 2025 were still in progress). Measured (2026-11-18, equal training size, 3 seeds): leaving out the 30 days before each quarter worsens log loss by 0.004 to 0.017, broadly rather than through company waves, so recent closures carry a shortcut a deployed model would not have. A 60-day gap would put July-September 2024 under half the complaints (49.6%).

The newest quarter is always tested. The other two are spread evenly over the six quarters from July 2024 on, the oldest whose train side holds half the complaints, so they test other seasons and another year (the curator's choice of 2026-11-10) and hold the two changes a deployed model met in that time: July-September 2024 falls before the closure mix moved ("Closed with explanation" was 51% to 57% of each quarter of 2024 and 57% to 67% of 2025), and January-March 2025 holds the wave of January 2025 (165,305 complaints that month; 12.9% of the quarter about money transfers, mostly Block, Inc. (Cash App) and Early Warning Services (Zelle)).

3 repeat(s) x 1 fold(s) with seed 4267; train 1,772,438 to 3,158,152 rows, test 203,139 to 350,790 rows. Prediction horizon: 3 months. Gap between train and test: 1 months. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as rows.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 3158152 | 203139 | 2017-04-24 00:00:00 | 2025-08-31 00:00:00 | 2025-10-01 00:00:00 | 2025-12-31 00:00:00 |
| 1 | 0 | 2198684 | 350790 | 2017-04-24 00:00:00 | 2024-11-30 00:00:00 | 2025-01-01 00:00:00 | 2025-03-31 00:00:00 |
| 2 | 0 | 1772438 | 213655 | 2017-04-24 00:00:00 | 2024-05-31 00:00:00 | 2024-07-01 00:00:00 | 2024-09-30 00:00:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows consumer_complaints_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Oct 2025 - Dec 2025 | 203139 | 0.94 | Closed with explanation 66.9%, Closed with monetary relief 2.0%, Closed with no… | Closed with explanation 65.2%, Closed with monetary relief 2.5%, Closed with no… | 2.31 | Product (2.31), Issue (0.59), Sub-issue (0.12) | 0 |
| 1 | Jan 2025 - Mar 2025 | 350790 | 0.654 | Closed with explanation 66.4%, Closed with monetary relief 1.0%, Closed with no… | Closed with explanation 67.0%, Closed with monetary relief 2.8%, Closed with no… | 3.946 | Product (3.95), Issue (1.44), Sub-product (0.49) | 0 |
| 2 | Jul 2024 - Sep 2024 | 213655 | 0.527 | Closed with explanation 54.7%, Closed with monetary relief 1.5%, Closed with no… | Closed with explanation 70.5%, Closed with monetary relief 3.2%, Closed with no… | 5.122 | Product (5.12), Issue (1.35), Sub-issue (0.29) | 0 |

## Bundle checks

0 error(s), 0 warning(s), 0 info (28 checks run, plus the dataset's own checks).


Accepted on purpose:

- `dataset_pure_feature_value`: Block, Inc. (Cash App) closes 99.8% of its complaints with an explanation throughout 2019-2025: a company response policy, and the company is known when the complaint is filed.
- `time_newest_period_short`: Decided (Lennart, 2026-11-11): December 2025 holds 54,655 complaints against 73,058 to 77,970 a month from September to November, as complaints still in progress when the archive was taken are left out (curation_comments, the closures in progress).

## Data checks

### Feature summary

<details>
<summary>Show the table (13 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| Tag: Older American | category | 3.04981e+06 | 90.73 | 2 | False, True |
| Tag: Servicemember | category | 3.04981e+06 | 90.73 | 2 | True, False |
| Sub-issue | category | 227808 | 6.78 | 212 | Information belongs to someone else, Reporting company used your report imprope… |
| Low population area | category | 48608 | 1.45 | 2 | False, True |
| Product | category | 0 | 0 | 14 | Credit reporting or other personal consumer reports, Credit reporting, credit r… |
| Sub-product | category | 36 | 0 | 58 | Credit reporting, General-purpose credit card or charge card, Checking account,… |
| Issue | category | 0 | 0 | 93 | Incorrect information on your report, Improper use of your report, Problem with… |
| State | category | 0 | 0 | 50 | TX, FL, CA, GA, NY, IL, PA, NC, NJ, MD |
| Company response to consumer | category | 0 | 0 | 3 | Closed with explanation, Closed with non-monetary relief, Closed with monetary … |
| Date received | datetime64\[ns\] | 0 | 0 | 3139 | 2025-01-17 00:00:00, 2025-01-18 00:00:00, 2025-01-16 00:00:00, 2025-01-15 00:00… |
| Consumer complaint narrative | string | 0 | 0 | 2.24838e+06 | In accordance with the Fair Credit Reporting act. The List of accounts below ha… |
| Company | string | 0 | 0 | 5628 | EQUIFAX, INC., TRANSUNION INTERMEDIATE HOLDINGS, INC., Experian Information Sol… |
| ZIP code | string | 0 | 0 | 6845 | XXXXX, 604XX, 770XX, 331XX, 30349, 631XX, 303XX, 752XX, 070XX, 190XX |

</details>

### Target distribution

| Company response to consumer | count | pct |
|---|---|---|
| Closed with explanation | 2211821 | 65.8 |
| Closed with non-monetary relief | 1072286 | 31.9 |
| Closed with monetary relief | 77184 | 2.3 |

### Numeric features

No numeric features to summarize.

### Categorical features

<details>
<summary>Show the table (57 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| Company | 1 | EQUIFAX, INC. | 74499 | 22.16 |
| Company | 2 | TRANSUNION INTERMEDIATE HOLDINGS, INC. | 70753 | 21.05 |
| Company | 3 | Experian Information Solutions Inc. | 68751 | 20.45 |
| Company | 4 | CAPITAL ONE FINANCIAL CORPORATION | 6046 | 1.8 |
| Company | 5 | JPMORGAN CHASE & CO. | 5221 | 1.55 |
| Company response to consumer | 1 | Closed with explanation | 220904 | 65.72 |
| Company response to consumer | 2 | Closed with non-monetary relief | 107459 | 31.97 |
| Company response to consumer | 3 | Closed with monetary relief | 7766 | 2.31 |
| Consumer complaint narrative | 1 | In accordance with the Fair Credit Reporting act. The List of ac... | 2424 | 0.72 |
| Consumer complaint narrative | 2 | My credit reports are inaccurate. These inaccuracies are causing... | 2262 | 0.67 |
| Consumer complaint narrative | 3 | You have reported inaccurate and unauthorized accounts on my cre... | 1530 | 0.46 |
| Consumer complaint narrative | 4 | Upon reviewing my credit report, I have identified inaccurate ac... | 1282 | 0.38 |
| Consumer complaint narrative | 5 | I am writing to have the following information removed from my c... | 1119 | 0.33 |
| Date received | 1 | 2025-01-17 00:00:00 | 1877 | 0.56 |
| Date received | 2 | 2025-01-18 00:00:00 | 1241 | 0.37 |
| Date received | 3 | 2025-01-16 00:00:00 | 977 | 0.29 |
| Date received | 4 | 2025-01-15 00:00:00 | 949 | 0.28 |
| Date received | 5 | 2025-01-20 00:00:00 | 845 | 0.25 |
| Issue | 1 | Incorrect information on your report | 112482 | 33.46 |
| Issue | 2 | Improper use of your report | 61623 | 18.33 |
| Issue | 3 | Problem with a company's investigation into an existing problem | 32332 | 9.62 |
| Issue | 4 | Problem with a credit reporting company's investigation into an ... | 24525 | 7.3 |
| Issue | 5 | Attempts to collect debt not owed | 16339 | 4.86 |
| Low population area | 1 | False | 262620 | 78.13 |
| Low population area | 2 | True | 68579 | 20.4 |
| Low population area | 3 | &lt;NA> | 4930 | 1.47 |
| Product | 1 | Credit reporting or other personal consumer reports | 153389 | 45.63 |
| Product | 2 | Credit reporting, credit repair services, or other personal cons... | 78731 | 23.42 |
| Product | 3 | Debt collection | 34547 | 10.28 |
| Product | 4 | Checking or savings account | 16161 | 4.81 |
| Product | 5 | Credit card or prepaid card | 10753 | 3.2 |
| State | 1 | TX | 42820 | 12.74 |
| State | 2 | FL | 40959 | 12.19 |
| State | 3 | CA | 35961 | 10.7 |
| State | 4 | GA | 25939 | 7.72 |
| State | 5 | NY | 19581 | 5.83 |
| Sub-issue | 1 | Information belongs to someone else | 65309 | 19.43 |
| Sub-issue | 2 | Reporting company used your report improperly | 47069 | 14 |
| Sub-issue | 3 | Their investigation did not fix an error on your report | 35861 | 10.67 |
| Sub-issue | 4 | &lt;NA> | 22844 | 6.8 |
| Sub-issue | 5 | Account status incorrect | 17468 | 5.2 |
| Sub-product | 1 | Credit reporting | 230038 | 68.44 |
| Sub-product | 2 | General-purpose credit card or charge card | 15534 | 4.62 |
| Sub-product | 3 | Checking account | 13284 | 3.95 |
| Sub-product | 4 | I do not know | 10713 | 3.19 |
| Sub-product | 5 | Other debt | 7501 | 2.23 |
| Tag: Older American | 1 | &lt;NA> | 305193 | 90.8 |
| Tag: Older American | 2 | False | 20892 | 6.22 |
| Tag: Older American | 3 | True | 10044 | 2.99 |
| Tag: Servicemember | 1 | &lt;NA> | 305193 | 90.8 |
| Tag: Servicemember | 2 | True | 23370 | 6.95 |
| Tag: Servicemember | 3 | False | 7566 | 2.25 |
| ZIP code | 1 | XXXXX | 4930 | 1.47 |
| ZIP code | 2 | 604XX | 1073 | 0.32 |
| ZIP code | 3 | 770XX | 995 | 0.3 |
| ZIP code | 4 | 331XX | 694 | 0.21 |
| ZIP code | 5 | 30349 | 685 | 0.2 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a217f6-76b0-7b60-b916-08d61cf191cc |
| checksum | v2:56836ef7f8abe260378a4a10fe3e2c974383d315e689f9c2b5c09341f0c704d9 |
| built_at | 2026-11-26T13:07:21+00:00 |
| path | consumer_complaints_1m/01a217f6-76b0-7b60-b916-08d61cf191cc |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
