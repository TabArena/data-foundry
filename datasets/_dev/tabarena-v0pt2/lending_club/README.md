---
report_format: data-foundry-report-v2
unique_name: lending_club
container_format: 2
checksum: v2:6834bf9264dde5858011572d8b859f0a227bda471005b8f8755ce75826225e4f
build:
  uuid: 01a217fd-07e9-7fc8-b8de-4db9313eff79
  checksum: v2:6834bf9264dde5858011572d8b859f0a227bda471005b8f8755ce75826225e4f
  built_at: '2026-11-26T13:13:32+00:00'
  path: lending_club/01a217fd-07e9-7fc8-b8de-4db9313eff79
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
raw_files:
  LC_loans_granting_model_dataset.csv?download=1: 207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc
  accepted_2007_to_2018Q4.csv.gz: 55c16f75120f897683f02e7aabcf080d0e4a20c4832feb1d592cfa941bd62a2d
data:
  n_rows: 609544
  n_features: 67
  dtypes:
    category: 5
    datetime64[ns]: 2
    float64: 55
    int64: 1
    string: 5
  n_test_dataset_rows: null
task:
  target: Default
  problem_type: binary_classification
  metric: roc_auc
  metric_origin: fallback
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: Default
  time_on: issue_d
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
  time_gap: null
  time_gap_unit: null
  reason: 'We try to create splits that simulate a model deployed to solve the task.


    Each test window is one calendar quarter, a model refit every quarter. LendingClub
    released its loan files by

    calendar quarter ("complete loan data for all loans issued through the previous
    completed calendar quarter"),

    and no source names a refit cadence: Sanz-Guerrero and Arroyo (2025) shuffle the
    loans into 5 folds, so the

    quarter matches the release, not a stated cadence (CC 2026-11-11), and a month
    of loans is a small test set.

    The 3 test windows (CC 2026-11-11), newest first: October to December 2015, the
    newest quarter; April to June 2015; and October to

    December 2014, a quarter of another year. October

    to December 2014 trains on less than half the loans (45.9%), beside 85.5% and
    62.8%. The windows are spread

    over two years instead of walking back from the newest: 46% of the loans were
    issued in 2015, so before 2015

    only 2014 Q4, Q3 and Q2 keep 30% of the loans for training (45.9%, 39.2% and 33.0%),
    and 2014 Q4 adds the

    other year at the smallest cost in training data. July to September and January
    to March 2015 are not

    tested. The default rate barely moves between the windows (14.8%, 15.4% and 14.6%;
    on the train sides 13.8%,

    13.3% and 12.8%). The outcome of a loan issued shortly before a window was only
    known later (by 2018), so the

    train side holds labels a deployed model would not have had yet; a gap of a full
    36-month term would remove

    this but leave too little data.


    Exception to SPLIT-10 (2026-10-21, Lennart): a loan''s outcome is known only when
    it ends, up to 36 months after

    issue, and the data has no outcome dates; a 36-month gap leaves 3.9-8.8% of the
    rows for training in the three

    windows and a 12-month gap 22.5-45.9%, under the floor (even a 6-month gap leaves
    only the newest window at

    half: 62.8%, 45.9% and 33.0%; for the windows of 2026-10-21 the figures were 5-9%,
    33-46% and 46% for the

    oldest). Serves SPLIT-14 (Must). The unmatured labels fall under SPLIT-10 (principles.md,
    Tensions).


    Repeat borrowers (Andrej, 2026-11-11): each training side leaves out the loans
    of borrowers who take a loan in

    the test quarter, as alfa_battle_2_0_task_2 does. The release has no borrower
    id, so the borrower is the exact

    match of the month of the earliest credit line, the 3-digit ZIP code, the state
    and the lower-cased employer

    title (`borrower_key`, built in `_clean`, not a feature). A test loan whose borrower''s
    latest earlier loan

    defaulted defaults at 60%, 78% and 69% (October-December 2015, April-June 2015,
    October-December 2014; 376,

    313 and 109 loans), against 8-9% after a repaid earlier loan and 15% without one;
    a lender does not grant a

    new loan on a charged-off one, so that earlier default was most likely recorded
    after the test loan was

    issued, a label a refit at the quarter''s start could not know. The filter removes
    5,213, 3,216 and 1,288

    training loans (1.0%, 0.8% and 0.5%), where 4,942, 3,122 and 1,269 test loans
    have a match; the training

    sides keep 515,664, 379,872 and 278,279 loans (84.6%, 62.3% and 45.7%). LightGBM
    (400 trees) with the matched

    training loans dropped against as many dropped at random: ROC AUC 0.683 against
    0.684, 0.670 against 0.672

    and 0.663 against 0.662; on the matched test loans 0.682 against 0.698, 0.660
    against 0.692 and 0.676

    against 0.708 (2026-11-23).'
  n_train:
    min: 278279
    max: 515664
  n_test:
    min: 49197
    max: 88667
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - splits_rows_unused
  accepted:
    meta_license_unknown: LendingClub published the loans under its terms of use,
      without a licence; the Zenodo cut is CC BY 4.0 and the Kaggle file CC0, set
      by its uploader.
    splits_train_under_half: 'Signed off (Lennart, 2026-11-11): October to December
      2014 trains on 45.9% of the loans (45.7% after the repeat-borrower filter),
      beside October to December 2015 and April to June 2015 on 85.5% and 62.8%; kept
      as the curator''s exception to the half-data floor (Andrej, 2026-11-20).'
decisions: []
---

# lending_club

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Binary classification of `Default`, scored with `roc_auc` on temporal splits by `issue_d`. 609,544 rows and 67 features. Source: Other (2018).

Built as `01a217fd-07e9-7fc8-b8de-4db9313eff79` on 2026-11-26. See [Build](#build).

## In brief

**Question.** Will a three-year LendingClub loan be repaid?

**Use case.** When a loan application arrives at LendingClub, a model scores the borrower's default risk before the company sets its own grade and interest rate, to decide whether to grant the loan.

**One row.** One 36-month loan issued by LendingClub in the US, April 2008 to December 2015 (609,544 loans).

**Predicted.** Whether the loan defaulted (14%) or was fully paid over its three-year term.

**Known at prediction time.** The borrower's income, debt-to-income ratio, FICO score, job title and years employed, home ownership, state and partial zip code; the loan amount, purpose and free-text description; and the credit-bureau history (accounts, balances, delinquencies, inquiries).

**What the test data stands for.** Three quarters are test windows, each trained on all loans issued before it except those of borrowers who take a loan in the window: the newest, October to December 2015, then April to June 2015 and October to December 2014.

**Our changes to the source.** We keep only the 36-month loans issued up to 2015, whose outcomes are all known; we add credit-bureau fields from LendingClub's full file and leave out the company's grade and interest rate.

> **Use case fit: approximate (a stand-in with a known gap).** The features are known at application, but the training side holds outcomes of loans issued just before each window, which a model refit then would not yet have; a full three-year gap would leave too little data.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/lending_club.md`](../../../../curation/records/lending_club.md)
- The original source: <https://www.lendingclub.com>
- A part of the data (the loan-granting cut of arXiv:2401.16458 on Zenodo, the base table): <https://doi.org/10.5281/zenodo.11295916>
- A part of the data (All Lending Club loan data, joined in by loan id): <https://www.kaggle.com/datasets/wordsforthewise/lending-club>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/lending_club/`. To get them:

```text
It seems the official download portal from https://www.lendingclub.com is gone. So we can only utilize artifacts from the past, which seem to go up to 2018.
Old script and source: https://github.com/nateGeorge/preprocess_lending_club_data

From all the artifacts we found online, this seems to be the newest: https://www.kaggle.com/datasets/wordsforthewise/lending-club/data
And the following paper (https://arxiv.org/abs/2401.16458) curated this dataset https://zenodo.org/records/11295916 for tabular-text learning.

Other artifacts:
- https://www.kaggle.com/datasets/adarshsng/lending-club-loan-data-csv
- https://www.kaggle.com/datasets/imsparsh/lending-club-loan-dataset-2007-2011

wget https://zenodo.org/records/11295916/files/LC_loans_granting_model_dataset.csv?download=1
mkdir -p local-data-warehouse/lending_club && mv LC_loans_granting_model_dataset.csv?download=1 local-data-warehouse/lending_club
kaggle datasets download wordsforthewise/lending-club -f accepted_2007_to_2018Q4.csv.gz && mv accepted_2007_to_2018Q4.csv.gz local-data-warehouse/lending_club/
```

| file | source | bytes | rows | sha256 (start) |
|---|---|---|---|---|
| `LC_loans_granting_model_dataset.csv?download=1` | the loan-granting cut of arXiv:2401.16458 on Zenodo, the base table | 167,468,415 |  | `207d65b2712f775a` |
| `accepted_2007_to_2018Q4.csv.gz` | All Lending Club loan data, joined in by loan id | 392,582,231 |  | `55c16f75120f8976` |

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/lending_club   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/lending_club   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://www.lendingclub.com |
| year | 2018 |
| domain | finance |
| license |  |
| data_tags | Non-IID, Temporal, Spatial |
| reference | sanz2025credit |
| part: the loan-granting cut of arXiv:2401.16458 on Zenodo, the base table | Other (2024): https://doi.org/10.5281/zenodo.11295916; license: CC BY 4.0 |
| part: All Lending Club loan data, joined in by loan id | Kaggle: https://www.kaggle.com/datasets/wordsforthewise/lending-club; license: CC0: Public Domain |
| rows x columns | 609,544 x 68 |
| task.target | Default |
| task.problem_type | binary_classification |
| task.metric | roc_auc |
| task.split_regime | temporal_non_iid |
| task.stratify_on | Default |
| task.time_on | issue_d |

**Metric**

| field | value |
|---|---|
| name | `roc_auc` (standard; takes proba; higher is better) |
| origin | fallback: the default for the problem type: the source defines no metric the task would use in practice |
| definition | area under the ROC curve |
| reason | Sanz-Guerrero & Arroyo 2025 tune by balanced accuracy for its 'more stable behaviour' and test AUC second with DeLong tests; balanced accuracy fixes no decision threshold or costs for approving a loan (MET-6). Original rejected: balanced accuracy. roc_auc is the binary fallback (the paper's tested metric). |

<details>
<summary>Feature types: 4 categorical, 1 ordinal, 5 string, 2 datetime</summary>

- categorical (4): `home_ownership_n`, `application_type`, `Default`, `purpose`
- ordinal (1): `emp_length (< 1 year < 1 year < 2 years < 3 years < 4 years < 5 years < 6 years < 7 years < 8 years < 9 years < 10+ years)`
- string (5): `emp_title`, `addr_state`, `zip_code`, `title`, `desc`
- datetime (2): `issue_d (%b-%Y)`, `earliest_cr_line (%b-%Y)`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{sanz2025credit,
  title={Credit Risk Meets Large Language Models: Building a Risk Indicator from Loan Descriptions in P2P Lending},
  author={Sanz-Guerrero, Mario and Arroyo, Javier},
  journal={Inteligencia Artificial},
  volume={28},
  number={75},
  pages={220--247},
  year={2025}
}
```

</details>

## Sample rows

The first 5 of 609,544 rows of the final frame (the oldest rows: the frame is sorted by `issue_d`); 12 of 68 columns, the target first. Cells are cut at 40 characters.

| Default | issue_d | annual_inc | dti_n | loan_amnt | fico_n | emp_length | purpose | home_ownership_n | addr_state | zip_code | title |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Defaulted | 2008-04-01 00:00:00 | 50000 | 18.01 | 7500 | 672 | 1 year | other | RENT | VA | 232xx | To Promote Global Business Pages |
| Defaulted | 2008-04-01 00:00:00 | 64000 | 13.5 | 25000 | 697 | 1 year | major_purchase | MORTGAGE | CT | 060xx | Persuing my dream |
| Fully Paid | 2008-04-01 00:00:00 | 80004 | 11.46 | 2000 | 762 | &lt; 1 year | other | RENT | CO | 801xx | Income Taxes |
| Defaulted | 2008-04-01 00:00:00 | 47000 | 13.3 | 6600 | 702 | 1 year | home_improvement | MORTGAGE | GA | 315xx | air conditioner |
| Fully Paid | 2008-04-01 00:00:00 | 89018 | 14.59 | 5800 | 677 | 7 years | credit_card | MORTGAGE | NV | 891xx | Debt Consolidation |

## Curation notes

We start with the data from Sanz-Guerrero et al. (2025), which is already preprocessed for this task and used for tabular-text learning. It lacks many variables of the original data that can be added without changing the task or leaking the label, so we merge them in from the original data.

- The description is often empty or a standard phrase, so a model must handle text that is mostly missing or uninformative. This is common in real-world tabular-text data, and we want it in the benchmark.
- We reverse the ordinal encoding of the target.
- We reverse the name change of "revenue" back to "annual_inc".
- We drop rows where "application_type" is missing, as these rows have consistent missing values across features and likely are a data loading artifact.
- We keep only the 36-month loans issued up to 2015, the only loans whose labels are complete, and drop the 60-month loans (about a third of the 2014-2015 volume) and all loans issued from 2016 on. The data of Sanz-Guerrero et al. (2025) holds only the loans that had finished (fully paid or charged off) by the 2018Q4 snapshot, so a loan still being repaid is missing.
- In accepted_2007_to_2018Q4.csv.gz, at least 99.8% of the 36-month loans up to 2015Q4 are finished, but only 57-93% per quarter in 2016, and only 63-97% per quarter of the 60-month loans from 2014 on. The missing loans are mostly good ones, so later or longer loans would skew the labels towards early defaults and early payoffs (default rate among finished loans: 15-16% in 2013, 20% in 2015, 24-26% in 2016).
- `term` is used only for this selection and is not a feature (it is part of the company's own assessment, see the merged features). Until 2026-10 the `lending_club_1m` version tested on 2016 and the v1 `lending_club` notebook on 2016-2018.
- We leave out the joint-applicant fields of the original data (sec_app_*, revol_bal_joint): they are filled only from 2017 on, so they are empty for the loans we keep.
- We leave out 14 credit-report fields LendingClub first reported in December 2015 (Andrej, 2026-11-11):
  `all_util`, `il_util`, `inq_fi`, `inq_last_12m`, `max_bal_bc`, `mths_since_rcnt_il`, `open_acc_6m`,
  `open_il_12m`, `open_il_24m`, `open_act_il`, `open_rv_12m`, `open_rv_24m`, `total_bal_il`, `total_cu_tl`. They
  are empty for every loan issued before December 2015 and filled for 49.2% of December's 36-month loans, so
  no training side holds a value, and in the newest test window they only mark the month (default 15.6% whether
  filled or empty;
  counted on LendingClub's file joined to the loans of Sanz-Guerrero et al.).
- Loans per issue year in the cleaned data (from the v1 exploration, counted 2026-10-22): 836 (2008), 4,716 (2009), 8,466 (2010), 12,747 (2011), 41,953 (2012), 99,018 (2013), 161,028 (2014), 280,780 (2015); 46% of the rows are from 2015, the year of the two newer test windows (the oldest is 2014 Q4).
- Ordinal scales (2026-10-30, the curator's decisions of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
  categories in the order of the source's codebook (`ORDINAL_LEVELS`); codes that mean unknown are missing
  (CLEAN-10).

## Splits

Expanding-window temporal splits: 3 test window(s) of 3 months, starting at 2015-10-01, 2015-04-01, 2014-10-01, newest first; train is all earlier data. Each train side keeps no row of an entity of `borrower_key` that its window tests. The test windows by `issue_d`, as listed: 2015-10-01 to 2015-12-01 (88,667 test, 515,664 train rows); 2015-04-01 to 2015-06-01 (64,222 test, 379,872 train rows); 2014-10-01 to 2014-12-01 (49,197 test, 278,279 train rows).

We try to create splits that simulate a model deployed to solve the task.

Each test window is one calendar quarter, a model refit every quarter. LendingClub released its loan files by
calendar quarter ("complete loan data for all loans issued through the previous completed calendar quarter"),
and no source names a refit cadence: Sanz-Guerrero and Arroyo (2025) shuffle the loans into 5 folds, so the
quarter matches the release, not a stated cadence (CC 2026-11-11), and a month of loans is a small test set.
The 3 test windows (CC 2026-11-11), newest first: October to December 2015, the newest quarter; April to June 2015; and October to
December 2014, a quarter of another year. October
to December 2014 trains on less than half the loans (45.9%), beside 85.5% and 62.8%. The windows are spread
over two years instead of walking back from the newest: 46% of the loans were issued in 2015, so before 2015
only 2014 Q4, Q3 and Q2 keep 30% of the loans for training (45.9%, 39.2% and 33.0%), and 2014 Q4 adds the
other year at the smallest cost in training data. July to September and January to March 2015 are not
tested. The default rate barely moves between the windows (14.8%, 15.4% and 14.6%; on the train sides 13.8%,
13.3% and 12.8%). The outcome of a loan issued shortly before a window was only known later (by 2018), so the
train side holds labels a deployed model would not have had yet; a gap of a full 36-month term would remove
this but leave too little data.

Exception to SPLIT-10 (2026-10-21, Lennart): a loan's outcome is known only when it ends, up to 36 months after
issue, and the data has no outcome dates; a 36-month gap leaves 3.9-8.8% of the rows for training in the three
windows and a 12-month gap 22.5-45.9%, under the floor (even a 6-month gap leaves only the newest window at
half: 62.8%, 45.9% and 33.0%; for the windows of 2026-10-21 the figures were 5-9%, 33-46% and 46% for the
oldest). Serves SPLIT-14 (Must). The unmatured labels fall under SPLIT-10 (principles.md, Tensions).

Repeat borrowers (Andrej, 2026-11-11): each training side leaves out the loans of borrowers who take a loan in
the test quarter, as alfa_battle_2_0_task_2 does. The release has no borrower id, so the borrower is the exact
match of the month of the earliest credit line, the 3-digit ZIP code, the state and the lower-cased employer
title (`borrower_key`, built in `_clean`, not a feature). A test loan whose borrower's latest earlier loan
defaulted defaults at 60%, 78% and 69% (October-December 2015, April-June 2015, October-December 2014; 376,
313 and 109 loans), against 8-9% after a repaid earlier loan and 15% without one; a lender does not grant a
new loan on a charged-off one, so that earlier default was most likely recorded after the test loan was
issued, a label a refit at the quarter's start could not know. The filter removes 5,213, 3,216 and 1,288
training loans (1.0%, 0.8% and 0.5%), where 4,942, 3,122 and 1,269 test loans have a match; the training
sides keep 515,664, 379,872 and 278,279 loans (84.6%, 62.3% and 45.7%). LightGBM (400 trees) with the matched
training loans dropped against as many dropped at random: ROC AUC 0.683 against 0.684, 0.670 against 0.672
and 0.663 against 0.662; on the matched test loans 0.682 against 0.698, 0.660 against 0.692 and 0.676
against 0.708 (2026-11-23).

3 repeat(s) x 1 fold(s) with seed 4267; train 278,279 to 515,664 rows, test 49,197 to 88,667 rows. Prediction horizon: 3 months.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 515664 | 88667 | 2008-04-01 00:00:00 | 2015-09-01 00:00:00 | 2015-10-01 00:00:00 | 2015-12-01 00:00:00 |
| 1 | 0 | 379872 | 64222 | 2008-04-01 00:00:00 | 2015-03-01 00:00:00 | 2015-04-01 00:00:00 | 2015-06-01 00:00:00 |
| 2 | 0 | 278279 | 49197 | 2008-04-01 00:00:00 | 2014-09-01 00:00:00 | 2014-10-01 00:00:00 | 2014-12-01 00:00:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows lending_club`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Oct 2015 - Dec 2015 | 88667 | 0.846 | Fully Paid 85.1% (about 75,496) | Fully Paid 86.5% (about 445,946) | 0.642 | num_bc_tl (0.64), total_rev_hi_lim (0.64), mo_sin_old_rev_tl_op (0.63) | 0.0032 |
| 1 | Apr 2015 - Jun 2015 | 64222 | 0.623 | Fully Paid 84.8% (about 54,447) | Fully Paid 86.5% (about 328,532) | 0.953 | num_tl_op_past_12m (0.95), num_bc_tl (0.95), total_il_high_credit_limit (0.95) | 0 |
| 2 | Oct 2014 - Dec 2014 | 49197 | 0.457 | Fully Paid 85.3% (about 41,968) | Fully Paid 87.6% (about 243,675) | 1.307 | num_tl_op_past_12m (1.31), num_bc_tl (1.30), pct_tl_nvr_dlq (1.30) | 0 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `splits_rows_unused`: 324 row(s) (0.1%) appear in no train and no test set. (hint: Expected of a temporal split (the rows of a gap, history no window trains on, rows a filter keeps out of every training side); say why in `splits_comment`.)

Accepted on purpose:

- `meta_license_unknown`: LendingClub published the loans under its terms of use, without a licence; the Zenodo cut is CC BY 4.0 and the Kaggle file CC0, set by its uploader.
- `splits_train_under_half`: Signed off (Lennart, 2026-11-11): October to December 2014 trains on 45.9% of the loans (45.7% after the repeat-borrower filter), beside October to December 2015 and April to June 2015 on 85.5% and 62.8%; kept as the curator's exception to the half-data floor (Andrej, 2026-11-20).

## Data checks

### Feature summary

<details>
<summary>Show the table (68 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| emp_length | category | 35734 | 5.86 | 11 | 10+ years, 2 years, &lt; 1 year, 3 years, 1 year, 5 years, 4 years, 7 years, 8 yea… |
| purpose | category | 0 | 0 | 14 | debt_consolidation, credit_card, home_improvement, other, major_purchase, small… |
| home_ownership_n | category | 0 | 0 | 4 | MORTGAGE, RENT, OWN, OTHER |
| Default | category | 0 | 0 | 2 | Fully Paid, Defaulted |
| application_type | category | 0 | 0 | 2 | Individual, Joint App |
| issue_d | datetime64\[ns\] | 0 | 0 | 93 | 2015-10-01 00:00:00, 2015-07-01 00:00:00, 2015-12-01 00:00:00, 2014-10-01 00:00… |
| earliest_cr_line | datetime64\[ns\] | 0 | 0 | 689 | 2001-08-01 00:00:00, 2000-08-01 00:00:00, 2001-10-01 00:00:00, 2000-10-01 00:00… |
| mths_since_last_record | float64 | 511699 | 83.95 | 122 | 61.0, 62.0, 65.0, 64.0, 69.0, 66.0, 67.0, 71.0, 68.0, 57.0 |
| mths_since_recent_bc_dlq | float64 | 465154 | 76.31 | 152 | 46.0, 45.0, 48.0, 25.0, 14.0, 44.0, 19.0, 35.0, 21.0, 40.0 |
| mths_since_last_major_derog | float64 | 452893 | 74.3 | 157 | 45.0, 42.0, 40.0, 46.0, 48.0, 38.0, 44.0, 41.0, 37.0, 43.0 |
| mths_since_recent_revol_delinq | float64 | 406907 | 66.76 | 153 | 13.0, 14.0, 9.0, 12.0, 15.0, 8.0, 17.0, 7.0, 11.0, 16.0 |
| mths_since_last_delinq | float64 | 311626 | 51.12 | 150 | 9.0, 13.0, 6.0, 8.0, 12.0, 10.0, 7.0, 14.0, 15.0, 11.0 |
| mths_since_recent_inq | float64 | 93570 | 15.35 | 26 | 1.0, 2.0, 0.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 |
| mo_sin_old_il_acct | float64 | 68900 | 11.3 | 479 | 122.0, 121.0, 124.0, 123.0, 126.0, 125.0, 132.0, 130.0, 133.0, 120.0 |
| num_tl_120dpd_2m | float64 | 68588 | 11.25 | 5 | 0.0, 1.0, 2.0, 3.0, 6.0 |
| pct_tl_nvr_dlq | float64 | 47912 | 7.86 | 550 | 100.0, 95.0, 90.0, 96.0, 92.0, 97.0, 90.9, 91.7, 92.3, 80.0 |
| avg_cur_bal | float64 | 47807 | 7.84 | 60256 | 1971.0, 1843.0, 2112.0, 1762.0, 0.0, 1956.0, 1839.0, 2289.0, 1250.0, 2587.0 |
| mo_sin_old_rev_tl_op | float64 | 47799 | 7.84 | 720 | 131.0, 119.0, 125.0, 138.0, 127.0, 124.0, 120.0, 130.0, 132.0, 156.0 |
| mo_sin_rcnt_rev_tl_op | float64 | 47799 | 7.84 | 241 | 2.0, 3.0, 4.0, 1.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 |
| mo_sin_rcnt_tl | float64 | 47798 | 7.84 | 166 | 2.0, 3.0, 4.0, 1.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 |
| num_accts_ever_120_pd | float64 | 47798 | 7.84 | 35 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 |
| num_actv_bc_tl | float64 | 47798 | 7.84 | 30 | 3.0, 2.0, 4.0, 5.0, 1.0, 6.0, 7.0, 8.0, 0.0, 9.0 |
| num_actv_rev_tl | float64 | 47798 | 7.84 | 45 | 4.0, 5.0, 3.0, 6.0, 7.0, 2.0, 8.0, 9.0, 10.0, 1.0 |
| num_bc_tl | float64 | 47798 | 7.84 | 61 | 6.0, 5.0, 7.0, 4.0, 8.0, 9.0, 3.0, 10.0, 11.0, 12.0 |
| num_il_tl | float64 | 47798 | 7.84 | 101 | 3.0, 4.0, 2.0, 5.0, 6.0, 1.0, 7.0, 8.0, 9.0, 10.0 |
| num_op_rev_tl | float64 | 47798 | 7.84 | 60 | 6.0, 5.0, 7.0, 8.0, 4.0, 9.0, 10.0, 3.0, 11.0, 12.0 |
| num_rev_accts | float64 | 47799 | 7.84 | 91 | 10.0, 11.0, 9.0, 12.0, 13.0, 8.0, 14.0, 7.0, 15.0, 16.0 |
| num_rev_tl_bal_gt_0 | float64 | 47798 | 7.84 | 43 | 4.0, 5.0, 3.0, 6.0, 7.0, 2.0, 8.0, 9.0, 10.0, 1.0 |
| num_tl_30dpd | float64 | 47798 | 7.84 | 5 | 0.0, 1.0, 2.0, 3.0, 4.0 |
| num_tl_90g_dpd_24m | float64 | 47798 | 7.84 | 22 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 |
| num_tl_op_past_12m | float64 | 47798 | 7.84 | 28 | 1.0, 2.0, 0.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 |
| tot_coll_amt | float64 | 47798 | 7.84 | 8917 | 0.0, 50.0, 100.0, 75.0, 150.0, 60.0, 200.0, 70.0, 80.0, 55.0 |
| tot_cur_bal | float64 | 47798 | 7.84 | 257345 | 0.0, 19998.0, 5537.0, 12066.0, 14511.0, 16219.0, 27316.0, 17951.0, 22396.0, 225… |
| tot_hi_cred_lim | float64 | 47798 | 7.84 | 269449 | 17500.0, 12500.0, 15500.0, 16500.0, 12000.0, 13500.0, 13800.0, 12400.0, 10000.0… |
| total_il_high_credit_limit | float64 | 47798 | 7.84 | 119478 | 0.0, 10000.0, 15000.0, 5000.0, 20000.0, 12000.0, 6000.0, 25000.0, 8000.0, 4000.0 |
| total_rev_hi_lim | float64 | 47798 | 7.84 | 16364 | 10000.0, 12000.0, 11000.0, 13500.0, 8500.0, 15000.0, 13000.0, 9000.0, 11500.0, … |
| num_bc_sats | float64 | 38224 | 6.27 | 43 | 3.0, 4.0, 2.0, 5.0, 6.0, 7.0, 1.0, 8.0, 9.0, 10.0 |
| num_sats | float64 | 38224 | 6.27 | 70 | 9.0, 8.0, 10.0, 11.0, 7.0, 12.0, 6.0, 13.0, 14.0, 5.0 |
| bc_util | float64 | 37433 | 6.14 | 1343 | 0.0, 98.0, 96.0, 97.0, 95.0, 99.0, 94.0, 93.0, 98.2, 92.0 |
| percent_bc_gt_75 | float64 | 37402 | 6.14 | 207 | 0.0, 100.0, 50.0, 66.7, 33.3, 25.0, 75.0, 40.0, 20.0, 60.0 |
| bc_open_to_buy | float64 | 37048 | 6.08 | 55162 | 0.0, 2000.0, 500.0, 1000.0, 1500.0, 2500.0, 3000.0, 3500.0, 5000.0, 800.0 |
| mths_since_recent_bc | float64 | 36639 | 6.01 | 439 | 3.0, 2.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 1.0, 10.0 |
| acc_open_past_24mths | float64 | 31273 | 5.13 | 48 | 3.0, 4.0, 2.0, 5.0, 1.0, 6.0, 7.0, 0.0, 8.0, 9.0 |
| mort_acc | float64 | 31273 | 5.13 | 35 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 |
| total_bal_ex_mort | float64 | 31273 | 5.13 | 131732 | 0.0, 19998.0, 19217.0, 12066.0, 16219.0, 22396.0, 9999.0, 12479.0, 16473.0, 264… |
| total_bc_limit | float64 | 31273 | 5.13 | 11542 | 0.0, 5000.0, 6000.0, 4000.0, 3000.0, 7000.0, 8000.0, 7500.0, 4500.0, 3500.0 |
| revol_util | float64 | 338 | 0.06 | 1279 | 0.0, 53.0, 58.0, 62.0, 54.0, 57.0, 59.0, 48.0, 61.0, 55.0 |
| annual_inc | float64 | 0 | 0 | 36735 | 60000.0, 50000.0, 40000.0, 65000.0, 45000.0, 70000.0, 80000.0, 75000.0, 55000.0… |
| dti_n | float64 | 0 | 0 | 4035 | 14.4, 19.2, 16.8, 13.2, 18.0, 15.6, 12.0, 20.4, 21.6, 10.8 |
| fico_n | float64 | 0 | 0 | 38 | 662.0, 672.0, 667.0, 677.0, 682.0, 687.0, 692.0, 697.0, 702.0, 707.0 |
| acc_now_delinq | float64 | 0 | 0 | 8 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 14.0, 6.0 |
| chargeoff_within_12_mths | float64 | 0 | 0 | 10 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 10.0, 9.0 |
| collections_12_mths_ex_med | float64 | 0 | 0 | 11 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 20.0, 16.0, 6.0, 14.0 |
| delinq_2yrs | float64 | 0 | 0 | 26 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 |
| delinq_amnt | float64 | 0 | 0 | 1009 | 0.0, 54.0, 30.0, 25.0, 75.0, 53.0, 65000.0, 50.0, 52.0, 57.0 |
| inq_last_6mths | float64 | 0 | 0 | 9 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0 |
| open_acc | float64 | 0 | 0 | 71 | 9.0, 8.0, 10.0, 7.0, 11.0, 12.0, 6.0, 13.0, 14.0, 5.0 |
| pub_rec | float64 | 0 | 0 | 29 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0 |
| pub_rec_bankruptcies | float64 | 6 | 0 | 10 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 12.0 |
| revol_bal | float64 | 0 | 0 | 63298 | 0.0, 6657.0, 5235.0, 5365.0, 5849.0, 10189.0, 5886.0, 6223.0, 6969.0, 4578.0 |

(8 more rows not shown)

</details>

### Target distribution

| Default | count | pct |
|---|---|---|
| Fully Paid | 524786 | 86.09 |
| Defaulted | 84758 | 13.91 |

### Numeric features

<details>
<summary>Show the table (56 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| annual_inc | 609544 | 72595.9 | 66382.2 | 3000 | 9e+06 |
| dti_n | 609544 | 17.5898 | 8.39026 | 0 | 999 |
| loan_amnt | 609544 | 12500.6 | 7784.14 | 1000 | 35000 |
| fico_n | 609544 | 697.034 | 31.1143 | 662 | 847.5 |
| acc_now_delinq | 609544 | 0.0047839 | 0.0770433 | 0 | 14 |
| acc_open_past_24mths | 578271 | 4.35689 | 2.97409 | 0 | 64 |
| avg_cur_bal | 561737 | 12480.2 | 15903.5 | 0 | 958084 |
| bc_open_to_buy | 572496 | 8965.9 | 14222.4 | 0 | 497445 |
| bc_util | 572111 | 62.7062 | 27.2258 | 0 | 339.6 |
| chargeoff_within_12_mths | 609544 | 0.00896408 | 0.108525 | 0 | 10 |
| collections_12_mths_ex_med | 609544 | 0.0149899 | 0.13845 | 0 | 20 |
| delinq_2yrs | 609544 | 0.316174 | 0.870832 | 0 | 30 |
| delinq_amnt | 609544 | 11.4035 | 674.139 | 0 | 94521 |
| inq_last_6mths | 609544 | 0.683116 | 0.963722 | 0 | 8 |
| mo_sin_old_il_acct | 540644 | 124.811 | 52.5375 | 0 | 724 |
| mo_sin_old_rev_tl_op | 561745 | 181.662 | 94.8367 | 3 | 851 |
| mo_sin_rcnt_rev_tl_op | 561745 | 13.283 | 16.5188 | 0 | 372 |
| mo_sin_rcnt_tl | 561746 | 8.2608 | 9.30859 | 0 | 263 |
| mort_acc | 578271 | 1.62073 | 2.04117 | 0 | 47 |
| mths_since_last_delinq | 297918 | 34.2483 | 21.7948 | 0 | 188 |
| mths_since_last_major_derog | 156651 | 43.0424 | 21.0888 | 0 | 188 |
| mths_since_last_record | 97845 | 70.3354 | 27.4075 | 0 | 121 |
| mths_since_recent_bc | 572905 | 24.5088 | 30.8039 | 0 | 616 |
| mths_since_recent_bc_dlq | 144390 | 40.1975 | 22.561 | 0 | 189 |
| mths_since_recent_inq | 515974 | 6.90992 | 5.92506 | 0 | 25 |
| mths_since_recent_revol_delinq | 202637 | 36.0495 | 22.3101 | 0 | 180 |
| num_accts_ever_120_pd | 561746 | 0.495694 | 1.27254 | 0 | 35 |
| num_actv_bc_tl | 561746 | 3.64377 | 2.17815 | 0 | 30 |
| num_actv_rev_tl | 561746 | 5.66671 | 3.18367 | 0 | 52 |
| num_bc_sats | 571320 | 4.64082 | 2.80894 | 0 | 57 |
| num_bc_tl | 561746 | 8.30814 | 4.83785 | 0 | 65 |
| num_il_tl | 561746 | 8.06294 | 7.1575 | 0 | 150 |
| num_op_rev_tl | 561746 | 8.15442 | 4.35591 | 0 | 67 |
| num_rev_accts | 561745 | 14.7494 | 8.049 | 0 | 105 |
| num_rev_tl_bal_gt_0 | 561746 | 5.62922 | 3.12454 | 0 | 45 |
| num_sats | 571320 | 11.3449 | 5.24912 | 0 | 84 |
| num_tl_120dpd_2m | 540956 | 0.000759766 | 0.0298092 | 0 | 6 |
| num_tl_30dpd | 561746 | 0.00337697 | 0.0625893 | 0 | 4 |
| num_tl_90g_dpd_24m | 561746 | 0.0922196 | 0.503103 | 0 | 30 |
| num_tl_op_past_12m | 561746 | 2.03679 | 1.72613 | 0 | 30 |
| open_acc | 609544 | 11.2649 | 5.23243 | 0 | 84 |
| pct_tl_nvr_dlq | 561632 | 94.0521 | 8.78345 | 7.7 | 100 |
| percent_bc_gt_75 | 572142 | 48.2823 | 35.6556 | 0 | 100 |
| pub_rec | 609544 | 0.206038 | 0.607874 | 0 | 86 |
| pub_rec_bankruptcies | 609538 | 0.125849 | 0.368259 | 0 | 12 |
| revol_bal | 609544 | 15528.3 | 21763.7 | 0 | 2.90484e+06 |
| revol_util | 609206 | 53.7225 | 23.8798 | 0 | 892.3 |
| tax_liens | 609544 | 0.0506772 | 0.413507 | 0 | 85 |
| tot_coll_amt | 561746 | 242.243 | 12364.6 | 0 | 9.15254e+06 |
| tot_cur_bal | 561746 | 128100 | 151733 | 0 | 8.00008e+06 |
| tot_hi_cred_lim | 561746 | 158484 | 172640 | 0 | 1e+07 |
| total_acc | 609544 | 24.5051 | 11.7557 | 2 | 169 |
| total_bal_ex_mort | 578271 | 45523.7 | 45274.2 | 0 | 2.92155e+06 |
| total_bc_limit | 578271 | 20046 | 20654.4 | 0 | 760000 |
| total_il_high_credit_limit | 561746 | 37981.3 | 40896.8 | 0 | 2.10191e+06 |
| total_rev_hi_lim | 561746 | 30440.2 | 39343.8 | 0 | 1e+07 |

</details>

### Categorical features

<details>
<summary>Show the table (53 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| Default | 1 | Fully Paid | 524786 | 86.09 |
| Default | 2 | Defaulted | 84758 | 13.91 |
| addr_state | 1 | CA | 94460 | 15.5 |
| addr_state | 2 | NY | 52089 | 8.55 |
| addr_state | 3 | TX | 49414 | 8.11 |
| addr_state | 4 | FL | 43177 | 7.08 |
| addr_state | 5 | IL | 24709 | 4.05 |
| application_type | 1 | Individual | 609307 | 99.96 |
| application_type | 2 | Joint App | 237 | 0.04 |
| desc | 1 | &lt;NA> | 518130 | 85 |
| desc | 2 | Debt consolidation. | 809 | 0.13 |
| desc | 3 | Debt Consolidation. | 474 | 0.08 |
| desc | 4 | debt consolidation. | 430 | 0.07 |
| desc | 5 | Pay off credit cards. | 186 | 0.03 |
| earliest_cr_line | 1 | 2001-08-01 00:00:00 | 4478 | 0.73 |
| earliest_cr_line | 2 | 2000-08-01 00:00:00 | 4377 | 0.72 |
| earliest_cr_line | 3 | 2001-10-01 00:00:00 | 4324 | 0.71 |
| earliest_cr_line | 4 | 2000-10-01 00:00:00 | 4223 | 0.69 |
| earliest_cr_line | 5 | 2002-08-01 00:00:00 | 4114 | 0.67 |
| emp_length | 1 | 10+ years | 187876 | 30.82 |
| emp_length | 2 | 2 years | 55971 | 9.18 |
| emp_length | 3 | &lt; 1 year | 50504 | 8.29 |
| emp_length | 4 | 3 years | 49730 | 8.16 |
| emp_length | 5 | 1 year | 40988 | 6.72 |
| emp_title | 1 | &lt;NA> | 40787 | 6.69 |
| emp_title | 2 | Teacher | 8953 | 1.47 |
| emp_title | 3 | Manager | 7382 | 1.21 |
| emp_title | 4 | Owner | 3885 | 0.64 |
| emp_title | 5 | Registered Nurse | 3748 | 0.61 |
| home_ownership_n | 1 | MORTGAGE | 283421 | 46.5 |
| home_ownership_n | 2 | RENT | 263950 | 43.3 |
| home_ownership_n | 3 | OWN | 62006 | 10.17 |
| home_ownership_n | 4 | OTHER | 167 | 0.03 |
| issue_d | 1 | 2015-10-01 00:00:00 | 33186 | 5.44 |
| issue_d | 2 | 2015-07-01 00:00:00 | 30864 | 5.06 |
| issue_d | 3 | 2015-12-01 00:00:00 | 30240 | 4.96 |
| issue_d | 4 | 2014-10-01 00:00:00 | 26573 | 4.36 |
| issue_d | 5 | 2015-11-01 00:00:00 | 25241 | 4.14 |
| purpose | 1 | debt_consolidation | 346158 | 56.79 |
| purpose | 2 | credit_card | 147840 | 24.25 |
| purpose | 3 | home_improvement | 35187 | 5.77 |
| purpose | 4 | other | 33025 | 5.42 |
| purpose | 5 | major_purchase | 12720 | 2.09 |
| title | 1 | Debt consolidation | 269465 | 44.21 |
| title | 2 | Credit card refinancing | 115448 | 18.94 |
| title | 3 | Home improvement | 26997 | 4.43 |
| title | 4 | Other | 25078 | 4.11 |
| title | 5 | Debt Consolidation | 11067 | 1.82 |
| zip_code | 1 | 945xx | 7056 | 1.16 |
| zip_code | 2 | 112xx | 6991 | 1.15 |
| zip_code | 3 | 750xx | 6488 | 1.06 |
| zip_code | 4 | 606xx | 6455 | 1.06 |
| zip_code | 5 | 100xx | 5776 | 0.95 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a217fd-07e9-7fc8-b8de-4db9313eff79 |
| checksum | v2:6834bf9264dde5858011572d8b859f0a227bda471005b8f8755ce75826225e4f |
| built_at | 2026-11-26T13:13:32+00:00 |
| path | lending_club/01a217fd-07e9-7fc8-b8de-4db9313eff79 |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
