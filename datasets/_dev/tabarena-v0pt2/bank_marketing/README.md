---
report_format: data-foundry-report-v2
unique_name: bank_marketing
container_format: 2
checksum: v2:0094a67a134188dcc95cc71e82a9e94b1dc6626d7563e9ef590e581de82fcb54
build:
  uuid: 01a21800-849d-76a4-821b-adf2632843b4
  checksum: v2:0094a67a134188dcc95cc71e82a9e94b1dc6626d7563e9ef590e581de82fcb54
  built_at: '2026-11-26T13:16:58+00:00'
  path: bank_marketing/01a21800-849d-76a4-821b-adf2632843b4
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
  n_rows: 45211
  n_features: 12
  dtypes:
    category: 8
    int64: 6
  n_test_dataset_rows: null
task:
  target: SubscribeTermDeposit
  problem_type: binary_classification
  metric: roc_auc
  metric_origin: source
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: SubscribeTermDeposit
  time_on: time_index
  time_of: label
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 10
  n_folds: 1
  random_state: 4267
  time_horizon: 3
  time_horizon_unit: months
  time_gap: null
  time_gap_unit: null
  reason: 'Ten expanding windows on the date of the last contact, rebuilt in `_clean`
    (the year from where the months

    wrap) and not shipped, newest first; each test window runs from its start to the
    next one and trains on every

    earlier record, no gap (Andrej, 2026-11-20):


    | Test window | Kind | Train share | Test records | Subscribers |

    |---|---|---|---|---|

    | 1 Sep-17 Nov 2010 | trickle, quarter | 98.7% | 592 | 272 (45.9%) |

    | 1 Jun-31 Aug 2010 | trickle, quarter | 97.0% | 781 | 407 (52.1%) |

    | 1 Mar-31 May 2010 | trickle, quarter | 95.5% | 667 | 383 (57.4%) |

    | 2 Dec 2009-26 Feb 2010 | trickle, quarter | 93.8% | 781 | 389 (49.8%) |

    | 1 Sep-30 Nov 2009 | trickle, quarter | 91.5% | 1,017 | 454 (44.6%) |

    | 1 Jun-31 Aug 2009 | trickle, quarter | 87.9% | 1,621 | 581 (35.8%) |

    | 4-28 May 2009 | May campaign | 75.6% | 5,575 | 533 (9.6%) |

    | 16-30 Apr 2009 | April campaign | 71.2% | 1,984 | 332 (16.7%) |

    | 28 Jan-15 Apr 2009 | Jan-Feb campaign + trickle | 61.3% | 4,464 | 537 (12.0%)
    |

    | 17 Oct-27 Dec 2008 | November campaign + trickle | 53.2% | 3,691 | 270 (7.3%)
    |


    The windows follow the bank''s calling. The source names "17 campaigns that occurred
    between May 2008 and

    November 2010" (Moro, Laureano, Cortez 2011) without dates, and the file has no
    campaign id, so the campaigns

    are read from the dates: five bursts of mass calling (days of 150 records or more:
    5 May-29 Aug 2008, 17-21 Nov

    2008, 28 Jan-9 Feb 2009, 16-30 Apr 2009, 4-18 May 2009; 5-14% subscribed), and
    from June 2009 a trickle of

    one-by-one calls, at most 115 a day (36-57% subscribed). Each campaign window
    starts at its burst''s first day

    or in the calling gap before it (no record from 30 Aug to 16 Oct 2008, nor from
    28 Dec 2008 to 27 Jan 2009) and

    holds the burst and the trickle after it, so no cut splits a campaign; the trickle
    has no campaign to cut at,

    so it is cut by calendar quarter. The summer 2008 wave is 53.2% of the records,
    so it trains every window and

    is never tested. The subscription rate follows the day''s calling volume (5.8%
    on days with 200 calls or more,

    48.5% on days with 20 or fewer), which the input `calls_that_day` carries; the
    burst windows test mass calling,

    the trickle windows selected calls, and a mean over the windows gives the trickle
    six of ten votes for 12% of

    the records.


    Ten windows against the nine an IID split of 45,211 records would get (SPLIT-15):
    the target is reached, every

    window trains on more than half the records (SPLIT-14), and the smallest holds
    272 subscribers. The source

    scores its model on time-ordered windows too: a random split does "not reflect
    the temporal dimension that a

    real prediction system would have to follow" (Moro et al. 2014, p. 5). The time
    key `time_index` is the

    record''s position in the file, which is in date order; it orders the windows
    and is no model input, and every

    window starts at the first record of its date.

    No gap (SPLIT-10): a record is dated by its last call, which ends the client''s
    calls in that campaign, so its

    outcome is known by the date that orders it. Each test record is predicted from
    the training records and its

    own inputs only; no feature or model step may use other test records (curation
    notes, Protocol).'
  n_train:
    min: 24038
    max: 44619
  n_test:
    min: 592
    max: 5575
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - meta_time_horizon_unit
  accepted:
    dataset_missing_value_sentinel: 'pdays = -1 is the source''s code for ''client
      was not previously contacted'' (UCI codebook), not a missing value: it matches
      previous == 0 row for row (36,954 rows), so it stays as a code with a meaning
      (CLEAN-10).'
decisions: []
---

# bank_marketing

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Binary classification of `SubscribeTermDeposit`, scored with `roc_auc` on temporal splits by `time_index`. 45,211 rows and 12 features. Source: UCI (2012).

Built as `01a21800-849d-76a4-821b-adf2632843b4` on 2026-11-26. See [Build](#build).

## In brief

**Question.** Will a bank client subscribe to a term deposit after the bank's telemarketing calls?

**Use case.** A Portuguese bank's marketing team picks which clients to call in a term-deposit campaign, to spend its calls on the likely buyers (Moro et al. 2014).

**One row.** One client's record in one phone campaign of a Portuguese bank, May 2008 to November 2010; a client can recur across campaigns (45,211 records).

**Predicted.** Whether the client subscribed to a term deposit by the end of the campaign's calls; 11.7% did.

**Known at prediction time.** Before the campaign's first call: age, job, marital status, education, whether the client has defaulted on credit, the account balance, housing and personal loans, the contacts with and outcome of earlier campaigns, and the number of clients the bank calls that day.

**What the test data stands for.** Ten periods of the date of the last contact from October 2008 to November 2010, each trained on every earlier record: the four calling campaigns after the summer 2008 wave, one window each, then six calendar quarters of the one-by-one calls from June 2009, so the test data stands for the clients the bank calls next.

**Our changes to the source.** We drop what the campaign's calls set: the last call's duration, this campaign's number of calls and the day, month and phone type of the last contact. We add the day's calling volume (records on the same date), which the subscription rate follows, and split by time on the rebuilt date instead of at random.

> **Use case fit: approximate (a stand-in with a known gap).** The windows cut at the calling campaigns the dates show, but the file names no campaign, so the calls from June 2009 are cut by calendar quarter; the day's call count, built from the file's own records, approximates the campaign's planned size. Inside a window a client's later record can give an earlier one's label away to a model that reads other test records, which the protocol forbids.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/bank_marketing.md`](../../../../curation/records/bank_marketing.md)
- The original source: <https://archive.ics.uci.edu/dataset/222/bank+marketing>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/bank_marketing/`. To get them:

```text
We download the data from the UCI repository and uzip it to a predefined folder.

mkdir -p local-data-warehouse/bank_marketing/ && wget -P local-data-warehouse/bank_marketing/ https://archive.ics.uci.edu/static/public/222/bank+marketing.zip && unzip -o "local-data-warehouse/bank_marketing/bank+marketing.zip" -d local-data-warehouse/bank_marketing && unzip -o "local-data-warehouse/bank_marketing/bank.zip" -d local-data-warehouse/bank_marketing
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/bank_marketing   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/bank_marketing   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | UCI: https://archive.ics.uci.edu/dataset/222/bank+marketing |
| year | 2012 |
| domain | finance |
| license | CC BY 4.0 |
| data_tags | Non-IID, Temporal |
| reference | moro2014bank-marketing |
| rows x columns | 45,211 x 14 |
| task.target | SubscribeTermDeposit |
| task.problem_type | binary_classification |
| task.metric | roc_auc |
| task.split_regime | temporal_non_iid |
| task.stratify_on | SubscribeTermDeposit |
| task.time_on | time_index |
| task.time_of | label |

**Metric**

| field | value |
|---|---|
| name | `roc_auc` (standard; takes proba; higher is better) |
| origin | source: the source's metric |
| original | AUC (area under the ROC curve), with ALIFT (area under the cumulative lift curve) as second metric |
| reference | Moro, Cortez, Rita 2014, A data-driven approach to predict the success of bank telemarketing, Decision Support Systems 62:22-31 (also Moro, Laureano, Cortez 2011, ESM, on the bank-full data) |
| definition | ROC AUC of term-deposit subscription. |

<details>
<summary>Feature types: 7 categorical, 1 ordinal, 0 string, 0 datetime</summary>

- categorical (7): `job`, `marital`, `default`, `housing`, `loan`, `poutcome`, `SubscribeTermDeposit`
- ordinal (1): `education (primary < secondary < tertiary)`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{moro2014bank-marketing,
  title={A data-driven approach to predict the success of bank telemarketing},
  author={Moro, S{\'e}rgio and Cortez, Paulo and Rita, Paulo},
  journal={Decision Support Systems},
  volume={62},
  pages={22--31},
  year={2014},
  publisher={Elsevier}
}
```

</details>

## Sample rows

The first 5 of 45,211 rows of the final frame (the oldest rows: the frame is sorted by `time_index`); 12 of 14 columns, the target first. Cells are cut at 40 characters.

| SubscribeTermDeposit | age | job | marital | education | default | balance | housing | loan | pdays | previous | poutcome |
|---|---|---|---|---|---|---|---|---|---|---|---|
| no | 58 | management | married | tertiary | no | 2143 | yes | no | -1 | 0 | unknown |
| no | 44 | technician | single | secondary | no | 29 | yes | no | -1 | 0 | unknown |
| no | 33 | entrepreneur | married | secondary | no | 2 | yes | yes | -1 | 0 | unknown |
| no | 47 | blue-collar | married | nan | no | 1506 | yes | no | -1 | 0 | unknown |
| no | 33 | nan | single | nan | no | 1 | no | no | -1 | 0 | unknown |

## Curation notes

- Prediction point (USE-3; CC 2026-11-08, Lennart): before the campaign's first call to the client, when the team picks whom to call. Known then: the client's profile and the earlier campaigns, nothing of this campaign's calls; so `duration`, `campaign`, `day`, `month` and `contact` leave (below).
- We removed the "duration" feature following its original description to obtain a "realistic predictive model".
- The file has the day (`day`, the day of the month) and the month (`month`) of the last contact, but not the year. `_clean` rebuilds the year where the month wraps from December to January (2008: 27,729 records, 2009: 14,862, 2010: 2,620), checks that the dates never fall in the file's order (UCI: "ordered by date"; May 2008 to November 2010, with no record in September 2008), keeps the file position as the time key `time_index` (SPLIT-22), counts the records of each date as `calls_that_day` (below), and drops `day` and `month` (`day_of_week` is a column of the authors' 2014 release only); the rebuilt date sets the test windows (`WINDOW_STARTS`, `splits_comment`) and is not shipped: the campaign's end sets the last contact's date, since the calls stop at a subscription or when the bank stops calling (LEAK-10). The source keeps the month of each call as an input (Moro et al. 2014, Table 2, "month in which the call is made"); this file has only the last call's, and it stays out with the day: every input exists before the first call, and the period is in the time key (Lennart, 2026-11-08).
- Split by time (CC 2026-11-08, Lennart; SPLIT-1, SPLIT-19, SPLIT-22, LEAK-17), in place of the random split shipped until 2026-11-08; `splits_comment` gives the ten windows on the rebuilt date (Andrej, 2026-11-20), which replace five windows of 4,521 records on the file order. Clients recur across campaigns: 995 pairs of records in two different years share the profile and the balance to the euro, the later record has more earlier contacts in 95% of them, and where the earlier record subscribed, the later one's `poutcome` says "success" in 562 of 581 pairs. Under the random split about 3.7% of the test records had the same client's later record in training (a lookup of it: +0.020 ROC AUC to LightGBM, higher on 9 of 9 splits), and models learnt each period's rate (5.1% subscribed in 2008, 17.1% in 2009, 51.6% in 2010) from records of the same months: most of that split's 0.76 ROC AUC came from telling the periods apart. Under the windows a client's earlier records train as its history (LEAK-34), and its later ones never do. On the earlier five windows of 4,521 records (August 2008 to November 2010), newest first, LightGBM scores ROC AUC 0.570, 0.679, 0.605, 0.552 and 0.522 (mean 0.586; 3 seeds, early stopping on the newest tenth of the training side, seed SD 0.029 per window) and logistic regression 0.633, 0.701, 0.640, 0.603 and 0.490 (mean 0.614). The time key is no model input (`time_of="label"`, Andrej, 2026-11-21): it is the record's position in a file ordered by the date of the last contact, and 61.2% of the records (27,667) take more than one call, so that date falls after the prediction point and is set by when the calling stopped - at a subscription or when the bank gave up (the subscription rate falls from 14.6% at one call to 5.8% at six or more). It is the reason the rebuilt date is not shipped either. While it was an input it was worth +0.018 to LightGBM and +0.004 to logistic regression on the earlier five windows; the file position holds no finer information about the outcome than the date does - within a calling day (days with 20 or more calls, 42,187 records) the position does not rank the label (Spearman 0.0013; the subscription rate is 7.4% to 10.0% across the ten within-day deciles). Those five windows are the ones this definition shipped until 2026-11-20, not the ten it ships now; the window scores here and the measurements of `campaign`, `contact`, `pdays` and `balance` below were taken on them (those of `contact` also on the random split and on nine quarterly windows, as its note says) and are kept as measured, not re-run on the ten (Andrej, 2026-11-21).
- Protocol (LEAK-9, an evaluation leak): inside a test window a client's later record can give an earlier test record's label away in its `poutcome`. Linked on the profile, housing and personal loan, the balance to the euro (non-zero), age +0 or +1 and the contacts adding up (a link that finds about 73% of repeat records), 3 to 18 test records per window have a later record of the same client in the same window (99 in all, 0.1% to 2.1% of a window; 5 of 592 in the newest), and in 40 of them it says "success", all of them subscribers (0 to 9 per window). Each test record is predicted from the training records and its own inputs only; no feature or model step may use other test records.
- `campaign` is dropped (LEAK-10; CC 2026-11-08, Lennart, in place of the keep with a note of 2026-11-06): it counts this campaign's contacts including the last (UCI: "number of contacts performed during this campaign and for this client (numeric, includes last contact)"), none of which exists at the prediction point, and the calls stop at a subscription or when the bank stops calling. It is the shape of heart_failure_followup_survival's `time`, a span from the prediction point to the outcome or a criterion without it. Under the random split it was worth 0.0060 ROC AUC to LightGBM (9 splits x 5 seeds, lower without it in 9 of 9) and 0.0079 to logistic regression, 0.0013 and 0.0016 once the year was known; on the earlier five windows it adds +0.0065 to logistic regression (higher in 5 of 5) and -0.014 to LightGBM (higher in 1 of 5).
- `previous` is a count of contacts (UCI: "number of contacts performed before this campaign and for this client"), so it stays numeric. The BeyondArena notebook typed it and `campaign` categorical (41 and 48 levels), which lost the order and left the high counts as rare levels.
- `contact` (cellular, telephone, unknown) is dropped (Andrej, 2026-11-13) with the other fields of the last contact: the codebook lists it with day, month and duration as "related with the last contact of the current campaign". The phone type itself is probably known before the call (where two linked records of a client both record one, it is the same in 3,571 of 3,721) but tells little: in 2009 and 2010, 22.7% of the cellular contacts subscribed and 19.1% of the telephone ones. The column's weight is its "unknown" level, a recording state rather than a phone: it covers all 12,443 rows of May-June 2008 (3.7% subscribed; the authors' 2014 release codes these rows "telephone"), and in later periods its few contacts subscribe far from the cellular ones, above or below (37.8% against 5.8% in September to November 2008; 8.6% and 2.9% against 61.3% and 53.9% in June to August and September to November 2010). Under the random split it was worth 0.021 ROC AUC in both models, nearly all of it the period: replaced by an unknown-or-not flag, it lost 0.0005 (LightGBM, 9 splits x 3 seeds). On the earlier five windows, dropping it lowered LightGBM by 0.006 (lower in 3 of 5) and raised logistic regression by 0.014 (higher in 4 of 5). On nine quarterly windows of the rebuilt date (September 2008 to November 2010, untuned, 2026-11-12) LightGBM scored ROC AUC 0.614 without it and 0.610 with it, logistic regression 0.619 and 0.623: it gained 0.024 to 0.051 on the two windows of June to November 2010, where the unknowns subscribe at 3% to 9%, and lost 0.025 to 0.059 (LightGBM) on the three oldest, carrying 2008's low rate onto later unknowns. None of these was re-run on the ten windows shipped now.
- `pdays` (days since the client was last contacted in an earlier campaign): the data lean to counting to this campaign's start, not its end, but do not settle it. At a fixed date of the last contact it falls by 2.2 days per extra call, and by 1.0 with `previous` and `poutcome` also held fixed, so about half of the slope is who gets called more. It was worth 0.0048 ROC AUC with LightGBM and nothing with logistic regression on the random split (9 splits), and 0.002 with both on the earlier five windows; kept. Its -1 means "client was not previously contacted" (UCI) and matches `previous` == 0 row for row (36,954 rows), so it stays as the source's code (CLEAN-10), and the bundle's sentinel warning is accepted for it.
- Note: `balance` is the "average yearly balance, in euros" (UCI), one value per client: linked without it (profile, age +0/+1, contacts adding up), the same client's records share it to the euro in 17.1% of pairs against 1.2% for different clients, with no excess of slightly changed balances, while age moves. The source does not date it. A reading after the calls could carry a subscription, but on the five windows logistic regression loses 0.002 to 0.003 ROC AUC without it whether or not the client has a later record, so it stays (LEAK-10; as tunisian_fraud_detection_challenge's registry fields). These numbers were measured on the earlier five windows of 4,521 records, which the ten windows of 2026-11-20 replace, and are kept as measured (Andrej, 2026-11-21). Revisit if the source dates it.
- `job`'s "unknown" (288 rows) is missing, as `education`'s (1,857 rows): the authors' 2014 codebook says "There are several missing values in some categorical attributes, all coded with the 'unknown' label" (CLEAN-10; ROC AUC unchanged on 9 of 9 random splits).
- Duplicates (LEAK-16, LEAK-18): on the twelve inputs without the time key, 62 records (0.1%) copy another, label included, and 5 more copy another's inputs with the other label; 92% of the copy rows have a balance of 0, plausible repeats of common profiles called the same day, so they stay. While `contact` was an input (thirteen inputs, until 2026-11-23) the counts were 55 and 1; before `calls_that_day` was an input (twelve inputs, `contact` among them) 811 and 82 (274 and 32 while `campaign` was an input). Since 2026-11-21 the time key is no input, so these are the counts the bundle check sees (it counted none while the key was an input and made every record distinct). In the ten windows two test records have a copy of every input but the time key in training: one in the window from 2 Dec 2009, with the other label, and one in the window from 1 Sep 2009, with the same label; on the twelve inputs before `calls_that_day` it was 0.4% to 1.9% (0.1% to 1.7% with the same label): an earlier record, the client's history when it is one client (LEAK-34). Kept with this note (CC 2026-11-08, Lennart).
- `calls_that_day` (Andrej, 2026-11-20): the number of records in the file with the same rebuilt date of the last contact, counted in `_clean` over the whole file (1 to 825; the definition filters no rows). The subscription rate follows the day's calling volume: 5.8% on the 95 days with 200 calls or more (36,656 records), 12.3% at 101-200, 25.0% at 51-100, 41.0% at 21-50 and 48.5% on days with 20 or fewer (3,224 records), and 44.2% there even for first-time clients (`previous` = 0), so returning clients do not explain it; UCI's second release (`bank-additional-full.csv`, with Banco de Portugal's indicators) shows the same rise, with the bank's monthly calls falling after 2008 and the share subscribing rising. The bank knows how many clients it calls that day when it draws the list, so it is known at the prediction point. Caveat: it is built from the file's own records, dated by each client's last call, so it approximates the campaign's planned size and the day's calls rather than recording them.
- Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
  categories in the order of the source's codebook (`ORDINAL_LEVELS`); codes that mean unknown are missing
  (CLEAN-10).

## Splits

Expanding-window temporal splits: 10 test window(s), each from its start to the next start, the newest to the end of the data (starts: 44619, 43838, 43171, 42390, 41373, 39752, 34177, 32193, 27729, 24038), newest first; train is all earlier data. The test windows by `time_index`, as listed: 44619 to 45210 (592 test, 44,619 train rows); 43838 to 44618 (781 test, 43,838 train rows); 43171 to 43837 (667 test, 43,171 train rows); 42390 to 43170 (781 test, 42,390 train rows); 41373 to 42389 (1,017 test, 41,373 train rows); 39752 to 41372 (1,621 test, 39,752 train rows); 34177 to 39751 (5,575 test, 34,177 train rows); 32193 to 34176 (1,984 test, 32,193 train rows); 27729 to 32192 (4,464 test, 27,729 train rows); 24038 to 27728 (3,691 test, 24,038 train rows).

Ten expanding windows on the date of the last contact, rebuilt in `_clean` (the year from where the months
wrap) and not shipped, newest first; each test window runs from its start to the next one and trains on every
earlier record, no gap (Andrej, 2026-11-20):

| Test window | Kind | Train share | Test records | Subscribers |
|---|---|---|---|---|
| 1 Sep-17 Nov 2010 | trickle, quarter | 98.7% | 592 | 272 (45.9%) |
| 1 Jun-31 Aug 2010 | trickle, quarter | 97.0% | 781 | 407 (52.1%) |
| 1 Mar-31 May 2010 | trickle, quarter | 95.5% | 667 | 383 (57.4%) |
| 2 Dec 2009-26 Feb 2010 | trickle, quarter | 93.8% | 781 | 389 (49.8%) |
| 1 Sep-30 Nov 2009 | trickle, quarter | 91.5% | 1,017 | 454 (44.6%) |
| 1 Jun-31 Aug 2009 | trickle, quarter | 87.9% | 1,621 | 581 (35.8%) |
| 4-28 May 2009 | May campaign | 75.6% | 5,575 | 533 (9.6%) |
| 16-30 Apr 2009 | April campaign | 71.2% | 1,984 | 332 (16.7%) |
| 28 Jan-15 Apr 2009 | Jan-Feb campaign + trickle | 61.3% | 4,464 | 537 (12.0%) |
| 17 Oct-27 Dec 2008 | November campaign + trickle | 53.2% | 3,691 | 270 (7.3%) |

The windows follow the bank's calling. The source names "17 campaigns that occurred between May 2008 and
November 2010" (Moro, Laureano, Cortez 2011) without dates, and the file has no campaign id, so the campaigns
are read from the dates: five bursts of mass calling (days of 150 records or more: 5 May-29 Aug 2008, 17-21 Nov
2008, 28 Jan-9 Feb 2009, 16-30 Apr 2009, 4-18 May 2009; 5-14% subscribed), and from June 2009 a trickle of
one-by-one calls, at most 115 a day (36-57% subscribed). Each campaign window starts at its burst's first day
or in the calling gap before it (no record from 30 Aug to 16 Oct 2008, nor from 28 Dec 2008 to 27 Jan 2009) and
holds the burst and the trickle after it, so no cut splits a campaign; the trickle has no campaign to cut at,
so it is cut by calendar quarter. The summer 2008 wave is 53.2% of the records, so it trains every window and
is never tested. The subscription rate follows the day's calling volume (5.8% on days with 200 calls or more,
48.5% on days with 20 or fewer), which the input `calls_that_day` carries; the burst windows test mass calling,
the trickle windows selected calls, and a mean over the windows gives the trickle six of ten votes for 12% of
the records.

Ten windows against the nine an IID split of 45,211 records would get (SPLIT-15): the target is reached, every
window trains on more than half the records (SPLIT-14), and the smallest holds 272 subscribers. The source
scores its model on time-ordered windows too: a random split does "not reflect the temporal dimension that a
real prediction system would have to follow" (Moro et al. 2014, p. 5). The time key `time_index` is the
record's position in the file, which is in date order; it orders the windows and is no model input, and every
window starts at the first record of its date.
No gap (SPLIT-10): a record is dated by its last call, which ends the client's calls in that campaign, so its
outcome is known by the date that orders it. Each test record is predicted from the training records and its
own inputs only; no feature or model step may use other test records (curation notes, Protocol).

10 repeat(s) x 1 fold(s) with seed 4267; train 24,038 to 44,619 rows, test 592 to 5,575 rows. Prediction horizon: 3 months. The time column `time_index` dates the label, which arrives after the prediction point: it orders and splits the rows, so every training label was known at its window's start, and is no model input (`feature_columns(container)` leaves it out).

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 44619 | 592 | 0 | 44618 | 44619 | 45210 |
| 1 | 0 | 43838 | 781 | 0 | 43837 | 43838 | 44618 |
| 2 | 0 | 43171 | 667 | 0 | 43170 | 43171 | 43837 |
| 3 | 0 | 42390 | 781 | 0 | 42389 | 42390 | 43170 |
| 4 | 0 | 41373 | 1017 | 0 | 41372 | 41373 | 42389 |
| 5 | 0 | 39752 | 1621 | 0 | 39751 | 39752 | 41372 |
| 6 | 0 | 34177 | 5575 | 0 | 34176 | 34177 | 39751 |
| 7 | 0 | 32193 | 1984 | 0 | 32192 | 32193 | 34176 |
| 8 | 0 | 27729 | 4464 | 0 | 27728 | 27729 | 32192 |
| 9 | 0 | 24038 | 3691 | 0 | 24037 | 24038 | 27728 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows bank_marketing`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | 44619 - 45210 | 592 | 0.987 | yes 45.9% (about 272) | yes 11.3% (about 5,053) | 8.347 | calls_that_day (8.35), poutcome (1.17), previous (0.91) | 0 |
| 1 | 43838 - 44618 | 781 | 0.97 | yes 52.1% (about 407) | yes 10.8% (about 4,737) | 8.305 | calls_that_day (8.31), poutcome (1.24), previous (0.88) | 0 |
| 2 | 43171 - 43837 | 667 | 0.955 | yes 57.4% (about 383) | yes 9.8% (about 4,229) | 8.291 | calls_that_day (8.29), poutcome (1.44), previous (0.92) | 0 |
| 3 | 42390 - 43170 | 781 | 0.938 | yes 49.8% (about 389) | yes 9.0% (about 3,819) | 8.31 | calls_that_day (8.31), poutcome (1.40), previous (1.13) | 0 |
| 4 | 41373 - 42389 | 1017 | 0.915 | yes 44.6% (about 454) | yes 8.3% (about 3,426) | 8.319 | calls_that_day (8.32), poutcome (0.81), job (0.73) | 0 |
| 5 | 39752 - 41372 | 1621 | 0.879 | yes 35.8% (about 581) | yes 7.1% (about 2,805) | 8.373 | calls_that_day (8.37), housing (0.59), job (0.50) | 0 |
| 6 | 34177 - 39751 | 5575 | 0.756 | yes 9.6% (about 533) | yes 6.9% (about 2,348) | 3.014 | calls_that_day (3.01), poutcome (0.69), housing (0.51) | 0 |
| 7 | 32193 - 34176 | 1984 | 0.712 | yes 16.7% (about 332) | yes 5.8% (about 1,882) | 3.816 | calls_that_day (3.82), poutcome (0.62), housing (0.17) | 0 |
| 8 | 27729 - 32192 | 4464 | 0.613 | yes 12.0% (about 537) | yes 5.0% (about 1,396) | 5.026 | calls_that_day (5.03), poutcome (0.65), job (0.13) | 0 |
| 9 | 24038 - 27728 | 3691 | 0.532 | yes 7.3% (about 270) | yes 4.8% (about 1,155) | 7.287 | calls_that_day (7.29), poutcome (2.02), balance (0.30) | 0.2493 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `meta_time_horizon_unit`: `time_horizon_unit='months'` implies calendar time, but `time_on='time_index'` has dtype int64, so the horizon cannot be cross-checked. (hint: Declare what one step of the time column counts, `Temporal(..., time_unit=...)`, so the horizon can be cross-checked.)

Accepted on purpose:

- `dataset_missing_value_sentinel`: pdays = -1 is the source's code for 'client was not previously contacted' (UCI codebook), not a missing value: it matches previous == 0 row for row (36,954 rows), so it stays as a code with a meaning (CLEAN-10).

## Data checks

### Feature summary

<details>
<summary>Show the table (14 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| education | category | 1857 | 4.11 | 3 | secondary, tertiary, primary |
| job | category | 288 | 0.64 | 11 | blue-collar, management, technician, admin., services, retired, self-employed, … |
| marital | category | 0 | 0 | 3 | married, single, divorced |
| default | category | 0 | 0 | 2 | no, yes |
| housing | category | 0 | 0 | 2 | yes, no |
| loan | category | 0 | 0 | 2 | no, yes |
| poutcome | category | 0 | 0 | 4 | unknown, failure, other, success |
| SubscribeTermDeposit | category | 0 | 0 | 2 | no, yes |
| age | int64 | 0 | 0 | 77 | 32, 31, 33, 34, 35, 36, 30, 37, 39, 38 |
| balance | int64 | 0 | 0 | 7168 | 0, 1, 2, 4, 3, 5, 6, 8, 23, 7 |
| pdays | int64 | 0 | 0 | 559 | -1, 182, 92, 183, 91, 181, 370, 184, 364, 95 |
| previous | int64 | 0 | 0 | 41 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 |
| time_index | int64 | 0 | 0 | 45211 | 45210, 0, 1, 2, 3, 4, 5, 6, 7, 8 |
| calls_that_day | int64 | 0 | 0 | 154 | 492, 328, 825, 751, 361, 709, 694, 334, 643, 629 |

</details>

### Target distribution

| SubscribeTermDeposit | count | pct |
|---|---|---|
| no | 39922 | 88.3 |
| yes | 5289 | 11.7 |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| age | 45211 | 40.9362 | 10.6188 | 18 | 95 |
| balance | 45211 | 1362.27 | 3044.77 | -8019 | 102127 |
| pdays | 45211 | 40.1978 | 100.129 | -1 | 871 |
| previous | 45211 | 0.580323 | 2.30344 | 0 | 275 |
| time_index | 45211 | 22605 | 13051.4 | 0 | 45210 |
| calls_that_day | 45211 | 357.389 | 198.923 | 1 | 825 |

### Categorical features

<details>
<summary>Show the table (24 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| SubscribeTermDeposit | 1 | no | 39922 | 88.3 |
| SubscribeTermDeposit | 2 | yes | 5289 | 11.7 |
| default | 1 | no | 44396 | 98.2 |
| default | 2 | yes | 815 | 1.8 |
| education | 1 | secondary | 23202 | 51.32 |
| education | 2 | tertiary | 13301 | 29.42 |
| education | 3 | primary | 6851 | 15.15 |
| education | 4 | &lt;NA> | 1857 | 4.11 |
| housing | 1 | yes | 25130 | 55.58 |
| housing | 2 | no | 20081 | 44.42 |
| job | 1 | blue-collar | 9732 | 21.53 |
| job | 2 | management | 9458 | 20.92 |
| job | 3 | technician | 7597 | 16.8 |
| job | 4 | admin. | 5171 | 11.44 |
| job | 5 | services | 4154 | 9.19 |
| loan | 1 | no | 37967 | 83.98 |
| loan | 2 | yes | 7244 | 16.02 |
| marital | 1 | married | 27214 | 60.19 |
| marital | 2 | single | 12790 | 28.29 |
| marital | 3 | divorced | 5207 | 11.52 |
| poutcome | 1 | unknown | 36959 | 81.75 |
| poutcome | 2 | failure | 4901 | 10.84 |
| poutcome | 3 | other | 1840 | 4.07 |
| poutcome | 4 | success | 1511 | 3.34 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a21800-849d-76a4-821b-adf2632843b4 |
| checksum | v2:0094a67a134188dcc95cc71e82a9e94b1dc6626d7563e9ef590e581de82fcb54 |
| built_at | 2026-11-26T13:16:58+00:00 |
| path | bank_marketing/01a21800-849d-76a4-821b-adf2632843b4 |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
