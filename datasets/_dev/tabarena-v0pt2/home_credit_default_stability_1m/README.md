---
report_format: data-foundry-report-v2
unique_name: home_credit_default_stability_1m
container_format: 2
checksum: v2:9f065a85f70a1ef378fa5e27d3137ae19db629634ea8e9dd8ab99bbd979b2c10
build:
  uuid: 01a217fa-29fa-7f2b-a908-f1cc4d7dd86e
  checksum: v2:9f065a85f70a1ef378fa5e27d3137ae19db629634ea8e9dd8ab99bbd979b2c10
  built_at: '2026-11-26T13:10:44+00:00'
  path: home_credit_default_stability_1m/01a217fa-29fa-7f2b-a908-f1cc4d7dd86e
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
  n_rows: 1526659
  n_features: 710
  dtypes:
    category: 114
    datetime64[ns]: 1
    float32: 536
    float64: 38
    int32: 1
    int8: 1
    uint32: 20
  n_test_dataset_rows: null
task:
  target: target
  problem_type: binary_classification
  metric: roc_auc
  metric_origin: stand_in
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: target
  time_on: date_decision
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
  reason: 'The length is how long one fitted scorecard keeps scoring (the curator''s
    pick, 2026-11-11): a scorecard is fit

    on applications whose default is known and then scores every new application until
    the next refit, and Home

    Credit''s competition fit one model and scored it on each week after its training
    data ("When a model runs in

    production, it can only see past performance and predictions"). No source gives
    Home Credit''s refit cadence,

    so the window is the longest whose three windows all train on at least half the
    applications: four months

    (five would leave the oldest on 35.1%). The two months used until 2026-11-11 came
    from cutting TabReD''s

    4.5-month test period into three, not from a refit cadence.

    The windows tile the months from 1 November 2019, the oldest start that keeps
    half the applications for

    training, to the release end, so at four months they leave no choice; they test
    the months after, across and

    before the drop of late March 2020, when applications fell from 60,748 in March
    (4.6% defaults) to 8,289 in

    April (2.2%) and the default rate stayed at 1.8-2.8% a week afterwards. A scorecard
    that should stay stable

    over time has to hold through that change, which no refit sees coming (the curator''s
    pick of 2026-11-11).

    Applications tested (defaults), then the train side and its share of the 1,526,659:
    July to

    5 October 2020 150,240 (3,175, 2.1%), 1,376,419 (90.2%); March to June 2020 143,724
    (4,714, 3.3%), 1,232,695

    (80.7%); November 2019 to February 2020 403,789 (15,541, 3.8%), 828,906 (54.3%).
    No window trains on less than

    half.

    No gap: the weekly default rate stays at 1.8% to 2.8% to the end of the release,
    so the labels look final, as

    for lt_vehicle_loan_default_prediction.

    The year before July 2020

    holds 937,675 rows, so that window trains on the newest 1M (from 11 June 2019);
    the year before March 2020

    holds 1,094,102, of which a random 1M; the November 2019 window trains on all
    828,906 (January to October

    2019).'
  n_train:
    min: 828906
    max: 1376419
  n_test:
    min: 143724
    max: 403789
  row_budget:
    train: 1000000
    test: 500000
  train_sampling:
    default: newest_year
    unit: rows
    stratify_on: target
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicates_skipped
  - dataset_pure_feature_value_skipped
  accepted:
    dataset_missing_value_sentinel: '-1 is a real value: the avgdbd* columns are ''average
      days past or before due of payment'' (Kaggle feature_definitions.csv), negative
      means paid early; -1 is the mode of a smooth distribution (-1 4.8%, -2 4.7%,
      -3 4.2%, 0 3.8%, down to -1220), missing values are NaN, and the default rate
      rises from 2.1% (< -1) over 3.3% (-1) and 4.5% (0) to 8.6% (late).'
    splits_feature_missing_in_test: 'Decided (Lennart, 2026-11-11): 12 columns stop
      in September-October 2019 and 15 start in April-June 2020, as the bank recorded
      them (curation_comments).'
decisions: []
---

# home_credit_default_stability_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Binary classification of `target`, scored with `roc_auc` on temporal splits by `date_decision`. 1,526,659 rows and 710 features. Source: Kaggle (2024).

Built as `01a217fa-29fa-7f2b-a908-f1cc4d7dd86e` on 2026-11-26. See [Build](#build).

## In brief

**Question.** Will a client default on the loan Home Credit is deciding on?

**Use case.** When a loan application arrives, Home Credit, a consumer lender for people with little or no credit history, scores the client's default risk to decide on the loan; its scorecard is refit regularly and should stay stable over time.

**One row.** One loan application decided between January 2019 and early October 2020 (1,526,659 of them).

**Predicted.** Whether the client defaulted (3.1% did); the time span in which a default counts is not stated.

**Known at prediction time.** The application, the client's personal data, earlier applications to Home Credit, credit-bureau and tax-registry records, deposits and debit cards, summarised over the client's history, and the decision date; some categories (district, employer, education, contract status and the like) are masked codes.

**What the test data stands for.** Three four-month test windows, newest first: July to early October 2020, March to June 2020 and November 2019 to February 2020, after, across and before the drop in applications and defaults of late March 2020, as for a scorecard that serves four months between refits; training is all earlier applications, which a benchmark sub-samples to at most a million from the newest 10 to 13 months.

**Our changes to the source.** We test three four-month windows from November 2019 to early October 2020 in place of TabReD's single test period (May to early October 2020), and keep columns TabReD dropped (the decision month and week, categories with many values).

> **Use case fit: approximate (a stand-in with a known gap).** The default has no stated time span, and the applications decided just before a window train with their outcomes, which a lender refitting then would not yet know.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/home_credit_default_stability.md`](../../../../curation/records/home_credit_default_stability.md)
- The original source: <https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/home_credit_default_stability/`. To get them:

```text
We get the data from the Kaggle competition.

kaggle competitions download -c home-credit-credit-risk-model-stability
mkdir -p local-data-warehouse/home_credit_default_stability && mv home-credit-credit-risk-model-stability.zip local-data-warehouse/home_credit_default_stability/ && cd local-data-warehouse/home_credit_default_stability/ && unzip home-credit-credit-risk-model-stability.zip && rm home-credit-credit-risk-model-stability.zip && rm -rf csv_files && rm -rf parquet_files/test && rm sample_submission.csv feature_definitions.csv
```

On first use, `_prepare_raw_files` writes `merged_input_data.parquet` into the same folder.

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/home_credit_default_stability_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/home_credit_default_stability_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability |
| year | 2024 |
| domain | finance |
| license | Kaggle Competition Rules |
| data_tags | Non-IID, Temporal |
| reference | Herman2024HomeCreditCreditRiskModelStability |
| rows x columns | 1,526,659 x 711 |
| task.target | target |
| task.problem_type | binary_classification |
| task.metric | roc_auc |
| task.split_regime | temporal_non_iid |
| task.stratify_on | target |
| task.time_on | date_decision |

**Metric**

| field | value |
|---|---|
| name | `roc_auc` (standard; takes proba; higher is better) |
| origin | stand_in: a stand-in for the source's metric, which cannot be computed |
| original | Home Credit 2023 - Gini Stability: mean weekly Gini + 88 * min(0, slope) - 0.5 * std(residuals) |
| reference | https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/overview/evaluation |
| definition | Per test week (WEEK_NUM) gini_w = 2*AUC_w - 1; fit gini_w = a*week + b by least squares; score = mean(gini_w) + 88*min(0, a) - 0.5*std(residuals). |
| reason | Our four-month test windows hold 14, 19 and 18 weeks of WEEK_NUM (weeks 78 and 60 split between two windows); the weekly Gini has SE about 0.02 to 0.04 (Hanley-McNeil at an AUC of 0.8), so the 88 x slope term has SE about 0.23 / 0.17 / 0.08, about 20 times the SE of the mean weekly Gini and larger than the Gini differences between methods: per window the score is mostly noise (MET-2). The windows of 2026-10-21 held 5 to 10 weeks, where it was larger still (1.2 / 0.5 / 0.43). ROC AUC per window is the per-week building block. |

<details>
<summary>Feature types: 113 categorical, 1 ordinal, 0 string, 1 datetime</summary>

- categorical (113): `target`, `cardtype_51L`, `credtype_322L`, `disbursementtype_67L`, `equalitydataagreement_891L`, `inittransactioncode_186L`, `lastapprcommoditycat_1041M`, `lastapprcommoditytypec_5251766M`, `lastcancelreason_561M`, `lastrejectcommoditycat_161M`, `lastrejectcommodtypec_5251769M`, `lastrejectreason_759M`, `lastrejectreasonclient_4145040M`, `lastst_736L`, `opencred_647L`, `previouscontdistrict_112M`, `twobodfilling_608L`, `description_5085714M`, `education_1103M`, `education_88M`, `maritalst_385M`, `maritalst_893M`, `requesttype_4525192L`, `max_isbidproduct_390L`, `max_isdebitcard_527L`, `min_isdebitcard_527L`, `last_cancelreason_3545846M`, `first_cancelreason_3545846M`, `last_credacc_status_367L`, `last_credtype_587L`, `first_credtype_587L`, `last_district_544M`, `first_district_544M`, `last_education_1138M`, `first_education_1138M`, `last_familystate_726L`, `first_familystate_726L`, `last_inittransactioncode_279L`, `first_inittransactioncode_279L`, `last_postype_4733339M`, `first_postype_4733339M`, `last_profession_152M`, `first_profession_152M`, `last_rejectreason_755M`, `first_rejectreason_755M`, `last_rejectreasonclient_4145042M`, `first_rejectreasonclient_4145042M`, `last_status_219L`, `first_status_219L`, `last_classificationofcontr_13M`, `first_classificationofcontr_13M`, `last_classificationofcontr_400M`, `first_classificationofcontr_400M`, `last_contractst_545M`, `first_contractst_545M`, `last_contractst_964M`, `first_contractst_964M`, `last_description_351M`, `first_description_351M`, `last_financialinstitution_382M`, `first_financialinstitution_382M`, `last_financialinstitution_591M`, `first_financialinstitution_591M`, `last_purposeofcred_426M`, `first_purposeofcred_426M`, `last_purposeofcred_874M`, `first_purposeofcred_874M`, `first_subjectrole_182M`, `first_subjectrole_93M`, `max_contaddr_smempladdr_334L`, `max_safeguarantyflag_411L`, `last_contaddr_district_15M`, `first_contaddr_district_15M`, `last_contaddr_zipcode_807M`, `first_contaddr_zipcode_807M`, `last_education_927M`, `first_education_927M`, `first_empl_industry_691L`, `last_empladdr_district_926M`, `first_empladdr_district_926M`, `last_empladdr_zipcode_114M`, `first_empladdr_zipcode_114M`, `first_familystate_447L`, `first_housetype_905L`, `last_incometype_1044T`, `first_incometype_1044T`, `last_language1_981M`, `first_language1_981M`, `last_registaddr_district_1083M`, `first_registaddr_district_1083M`, `last_registaddr_zipcode_184M`, `first_registaddr_zipcode_184M`, `last_relationshiptoclient_415T`, `last_relationshiptoclient_642T`, `last_role_1084L`, `first_role_1084L`, `last_sex_738L`, `first_sex_738L`, `last_type_25L`, `first_type_25L`, `last_collater_typofvalofguarant_298M`, `first_collater_typofvalofguarant_298M`, `last_collater_typofvalofguarant_407M`, `first_collater_typofvalofguarant_407M`, `last_collaterals_typeofguarante_359M`, `first_collaterals_typeofguarante_359M`, `last_collaterals_typeofguarante_669M`, `first_collaterals_typeofguarante_669M`, `last_subjectroles_name_541M`, `first_subjectroles_name_541M`, `first_subjectroles_name_838M`, `isbidproduct_1095L`, `max_persontype_1072L`
- ordinal (1): `first_empl_employedtotal_800L (LESS_ONE < MORE_ONE < MORE_FIVE)`
- string (0): none
- datetime (1): `date_decision (%Y-%m-%d)`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{Herman2024HomeCreditCreditRiskModelStability,
  author = {Daniel Herman and Tomas Jelinek and Walter Reade and Maggie Demkin and Addison Howard},
  title  = {Home Credit - Credit Risk Model Stability},
  year   = {2024},
  howpublished = {\url{https://kaggle.com/competitions/home-credit-credit-risk-model-stability}},
  note   = {Kaggle competition}
}
```

</details>

## Sample rows

The first 5 of 1,526,659 rows of the final frame (the oldest rows: the frame is sorted by `date_decision`); 12 of 711 columns, the target first. Cells are cut at 40 characters.

| target | date_decision | MONTH | WEEK_NUM | actualdpdtolerance_344P | amtinstpaidbefduel24m_4187115A | annuity_780A | annuitynextmonth_57A | applicationcnt_361L | applications30d_658L | applicationscnt_1086L | applicationscnt_464L |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Yes | 2019-01-01 00:00:00 | 201901 | 0 | 0 | nan | 1576.6 | 0 | 0 | 0 | 0 | 0 |
| No | 2019-01-01 00:00:00 | 201901 | 0 | 0 | nan | 5400 | 0 | 0 | 0 | 0 | 0 |
| No | 2019-01-01 00:00:00 | 201901 | 0 | 0 | nan | 1545.2 | 0 | 0 | 1 | 0 | 1 |
| No | 2019-01-01 00:00:00 | 201901 | 0 | nan | nan | 2773.2 | 0 | 0 | 0 | 0 | 0 |
| No | 2019-01-01 00:00:00 | 201901 | 0 | 0 | nan | 3019.8 | 0 | 0 | 0 | 0 | 0 |

## Curation notes

We start with the data from Kaggle and follow the preprocessing from TabRed (https://github.com/yandex-research/tabred/tree/main/preprocessing#homecredit-default-stability-homecredit-20), which in turn follows two Kaggle solutions (https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/507946, https://www.kaggle.com/code/yuuniekiri/fork-of-home-credit-catboost-inference).

- We follow TabRed and use temporal splits for the task. The Kaggle experts used various strategies and most commonly StratifiedGroupKFold to align offline CV with the temporal-split data on the leaderboard. That is, the split used for training can be StratifiedGroupKFold, but not for testing.
- Metric: ROC AUC stands in for the competition's Gini Stability, whose slope term is noise on our test windows (Lennart, 2026-10-21, then on windows of 5-10 weeks; it stays noise on the 14-19 weeks of the four-month windows of 2026-11-11, as the metric's reason gives).
- Test windows (Lennart, 2026-11-11): four months ("Reply (c): Four months"), the longest length whose three windows all train on at least half the applications, as a scorecard serves for months between refits; the proposed windows at that length ("Agree."): July to 5 October 2020, March to June 2020 and November 2019 to February 2020, which tile the months from the oldest start that keeps half the applications for training to the release end (splits comment).
- Note, the original competition was heavily influenced by metric hacking, which is not relevant for our offline benchmark tasks. Thus, results are not directly comparable ot transferable.
- We change the preprocessing from Kaggle and TabRed in specific steps: (A) we depart from the TabRed and Kaggle solutions in that we do not drop high-cardinality string columns, (B) we do not drop month and week, as it was only dropped due to the metric leak in the competition, (C) we only drop constant columns if they are constant w.r.t. NaN and non-NaN values, (D) we do not perform ordinal encoding and drop minor categories, (E) we keep every row: the 1M train budget of this _1m version is applied by a benchmark, which sub-samples each train side before a fit (see the splits comment), (F) we keep the date column without transformations for the pipelines to handle, and (G) the code from TabRed is outdated and does not function the same anymore when it comes to down-casting string and categorical data of the data from Kaggle, we fix this by treating categorical data as categorical following the original Kaggle scripts, moreover, we had to remove getting the std() of a date column, which is not supported anymore.
- We drop case_id as it is already collapsed and thus does not contain extra information.
- We cast all object and string columns to be categorical. Note that they are anonymized and string preprocessing likely does not add a lot of value as a result.
- We drop name-related columns as they do not hold relevant information. These were otherwise dropped as high-cardinality string columns in TabRed or on Kaggle.
- Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
  categories in the order of the source's codebook (`ORDINAL_LEVELS`).
- The target (2026-11-01, CLEAN-25): `target` ships its classes as words (1 is the event). Binary: "Yes" is the
  event, the class that sorts second, so it is the metrics' positive class.
- The row budget: each test window keeps at most 500k of its rows (all of them here), and each train side holds every earlier row, so the frame keeps all 1,526,659 applications. The 1M train budget is recorded, not applied: a benchmark sub-samples each train side to 1M rows before a fit with `subsample_train`. Its default is the newest year before the window, extended back in time until it holds 1M rows, and a random 1M of those (splits comment), in place of TabReD's random sub-sampling of all earlier rows: a study of the sub-sampling found the newest year best for dated data.
- Columns recorded on one side of a window only (Lennart, 2026-11-11): 12 columns stop being recorded in September and October 2019 (`responsedate_1012D`, `birthdate_574D`, `pmtscount_423L`, `pmtssum_45A`, the four `*_pmtamount_36A`, `n_unique_employername_160M` and the three `*_processingdate_168D`), so the November 2019 window tests without them; 15 start between April and June 2020 (`contractssum_5085716L`, the four `*_contractsum_5085717L`, the four `*_amount_4917619A`, the three `*_deductiondate_4917603D`, `n_unique_name_4917606M`, `first_housetype_905L` and `responsedate_4917613D`), so the March and July 2020 windows train almost without them. Kept: the data as the bank recorded it, which a model refit then met too.

## Splits

Expanding-window temporal splits: 3 test window(s) of 4 months, starting at 2020-07-01, 2020-03-01, 2019-11-01, newest first; train is all earlier data. The test windows by `date_decision`, as listed: 2020-07-01 to 2020-10-05 (150,240 test, 1,376,419 train rows); 2020-03-01 to 2020-06-30 (143,724 test, 1,232,695 train rows); 2019-11-01 to 2020-02-29 (403,789 test, 828,906 train rows). Each test window keeps at most 500k of its rows, drawn at random; each train side holds every earlier row, and a benchmark sub-samples it to 1M rows (by default rows drawn at random from the newest year before each window, extended back in time until it holds that many rows, `subsample_train`).

The length is how long one fitted scorecard keeps scoring (the curator's pick, 2026-11-11): a scorecard is fit
on applications whose default is known and then scores every new application until the next refit, and Home
Credit's competition fit one model and scored it on each week after its training data ("When a model runs in
production, it can only see past performance and predictions"). No source gives Home Credit's refit cadence,
so the window is the longest whose three windows all train on at least half the applications: four months
(five would leave the oldest on 35.1%). The two months used until 2026-11-11 came from cutting TabReD's
4.5-month test period into three, not from a refit cadence.
The windows tile the months from 1 November 2019, the oldest start that keeps half the applications for
training, to the release end, so at four months they leave no choice; they test the months after, across and
before the drop of late March 2020, when applications fell from 60,748 in March (4.6% defaults) to 8,289 in
April (2.2%) and the default rate stayed at 1.8-2.8% a week afterwards. A scorecard that should stay stable
over time has to hold through that change, which no refit sees coming (the curator's pick of 2026-11-11).
Applications tested (defaults), then the train side and its share of the 1,526,659: July to
5 October 2020 150,240 (3,175, 2.1%), 1,376,419 (90.2%); March to June 2020 143,724 (4,714, 3.3%), 1,232,695
(80.7%); November 2019 to February 2020 403,789 (15,541, 3.8%), 828,906 (54.3%). No window trains on less than
half.
No gap: the weekly default rate stays at 1.8% to 2.8% to the end of the release, so the labels look final, as
for lt_vehicle_loan_default_prediction.
The year before July 2020
holds 937,675 rows, so that window trains on the newest 1M (from 11 June 2019); the year before March 2020
holds 1,094,102, of which a random 1M; the November 2019 window trains on all 828,906 (January to October
2019).

3 repeat(s) x 1 fold(s) with seed 4267; train 828,906 to 1,376,419 rows, test 143,724 to 403,789 rows. Prediction horizon: 4 months. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as rows.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 1376419 | 150240 | 2019-01-01 00:00:00 | 2020-06-30 00:00:00 | 2020-07-01 00:00:00 | 2020-10-05 00:00:00 |
| 1 | 0 | 1232695 | 143724 | 2019-01-01 00:00:00 | 2020-02-29 00:00:00 | 2020-03-01 00:00:00 | 2020-06-30 00:00:00 |
| 2 | 0 | 828906 | 403789 | 2019-01-01 00:00:00 | 2019-10-31 00:00:00 | 2019-11-01 00:00:00 | 2020-02-29 00:00:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows home_credit_default_stability_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Jul 2020 - Oct 2020 | 150240 | 0.902 | Yes 2.1% (about 3,102) | Yes 3.3% (about 45,353) | 8.235 | MONTH (8.24), WEEK_NUM (8.22), mean_refreshdate_3813885D (7.70) | 0.1542 |
| 1 | Mar 2020 - Jun 2020 | 143724 | 0.807 | Yes 3.3% (about 4,750) | Yes 3.4% (about 41,357) | 8.301 | max_pmts_year_1139T (8.30), WEEK_NUM (8.01), MONTH (7.81) | 0.2761 |
| 2 | Nov 2019 - Feb 2020 | 403789 | 0.543 | Yes 4.0% (about 16,212) | Yes 2.8% (about 23,209) | 9.341 | responsedate_1012D (9.34), MONTH (7.94), WEEK_NUM (7.93) | 0.5194 |

## Bundle checks

0 error(s), 0 warning(s), 2 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicates_skipped`: Skipped duplicate-column/row checks: 1,085,454,549 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to run them; nothing else checks duplicate rows and columns.)
- **info** `dataset_pure_feature_value_skipped`: Skipped the pure-feature-value check: 1,085,454,549 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to force it.)

Accepted on purpose:

- `dataset_missing_value_sentinel`: -1 is a real value: the avgdbd* columns are 'average days past or before due of payment' (Kaggle feature_definitions.csv), negative means paid early; -1 is the mode of a smooth distribution (-1 4.8%, -2 4.7%, -3 4.2%, 0 3.8%, down to -1220), missing values are NaN, and the default rate rises from 2.1% (< -1) over 3.3% (-1) and 4.5% (0) to 8.6% (late).
- `splits_feature_missing_in_test`: Decided (Lennart, 2026-11-11): 12 columns stop in September-October 2019 and 15 start in April-June 2020, as the bank recorded them (curation_comments).

## Data checks

### Feature summary

<details>
<summary>Show the table (711 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| last_credacc_status_367L | category | 1.45006e+06 | 94.98 | 6 | AC, CL, CA, PCL, PO, CR |
| equalitydataagreement_891L | category | 1.44863e+06 | 94.89 | 2 | True, False |
| first_housetype_905L | category | 1.42584e+06 | 93.4 | 6 | OWNED, PARENTAL, FLAT, COMPANY_FLAT, COOP_FLAT, STATE_FLAT |
| last_relationshiptoclient_415T | category | 1.36297e+06 | 89.28 | 10 | CHILD, SPOUSE, OTHER_RELATIVE, SIBLING, FRIEND, OTHER, PARENT, COLLEAGUE, NEIGH… |
| cardtype_51L | category | 1.33497e+06 | 87.44 | 2 | INSTANT, PERSONALIZED |
| max_isdebitcard_527L | category | 1.18297e+06 | 77.49 | 2 | False, True |
| min_isdebitcard_527L | category | 1.18297e+06 | 77.49 | 2 | False, True |
| first_familystate_726L | category | 1.02687e+06 | 67.26 | 5 | MARRIED, SINGLE, WIDOWED, DIVORCED, LIVING_WITH_PARTNER |
| first_empl_industry_691L | category | 1.00442e+06 | 65.79 | 24 | OTHER, GOVERNMENT, EDUCATION, TRADE, HEALTH, MANUFACTURING, AGRICULTURE, TRANSP… |
| first_empl_employedtotal_800L | category | 998344 | 65.39 | 3 | MORE_FIVE, MORE_ONE, LESS_ONE |
| last_relationshiptoclient_642T | category | 935626 | 61.29 | 10 | SIBLING, SPOUSE, CHILD, OTHER_RELATIVE, FRIEND, PARENT, COLLEAGUE, OTHER, NEIGH… |
| requesttype_4525192L | category | 853395 | 55.9 | 3 | DEDUCTION_6, PENSION_6, SOCIAL_6 |
| first_familystate_447L | category | 798046 | 52.27 | 5 | MARRIED, SINGLE, WIDOWED, DIVORCED, LIVING_WITH_PARTNER |
| last_incometype_1044T | category | 757320 | 49.61 | 8 | PRIVATE_SECTOR_EMPLOYEE, SALARIED_GOVT, RETIRED_PENSIONER, EMPLOYED, SELFEMPLOY… |
| last_sex_738L | category | 757320 | 49.61 | 2 | F, M |
| last_familystate_726L | category | 408731 | 26.77 | 5 | MARRIED, SINGLE, WIDOWED, DIVORCED, LIVING_WITH_PARTNER |
| first_credtype_587L | category | 333576 | 21.85 | 3 | COL, CAL, REL |
| first_inittransactioncode_279L | category | 333576 | 21.85 | 3 | POS, CASH, NDF |
| last_credtype_587L | category | 311529 | 20.41 | 3 | COL, CAL, REL |
| last_inittransactioncode_279L | category | 311529 | 20.41 | 3 | POS, CASH, NDF |
| lastst_736L | category | 305137 | 19.99 | 11 | D, A, K, T, N, S, Q, L, H, P |
| opencred_647L | category | 305137 | 19.99 | 2 | False, True |
| max_isbidproduct_390L | category | 305137 | 19.99 | 2 | False, True |
| last_cancelreason_3545846M | category | 305137 | 19.99 | 66 | a55475b1, P94_109_143, P85_114_140, P73_130_169, P198_89_166, P180_60_137, P24_… |
| first_cancelreason_3545846M | category | 305137 | 19.99 | 74 | a55475b1, P94_109_143, P85_114_140, P30_86_84, P198_89_166, P180_60_137, P73_13… |
| last_district_544M | category | 305137 | 19.99 | 404 | a55475b1, P131_33_167, P197_47_166, P123_6_84, P98_137_111, P204_99_158, P147_2… |
| first_district_544M | category | 305137 | 19.99 | 969 | a55475b1, P131_33_167, P197_47_166, P123_6_84, P98_137_111, P204_99_158, P159_1… |
| last_education_1138M | category | 305137 | 19.99 | 6 | P97_36_170, P33_146_175, a55475b1, P106_81_188, P17_36_170, P157_18_172 |
| first_education_1138M | category | 305137 | 19.99 | 6 | a55475b1, P97_36_170, P33_146_175, P106_81_188, P17_36_170, P157_18_172 |
| last_postype_4733339M | category | 305137 | 19.99 | 9 | a55475b1, P177_117_192, P60_146_156, P149_40_170, P46_145_78, P217_110_186, P67… |
| first_postype_4733339M | category | 305137 | 19.99 | 9 | a55475b1, P177_117_192, P46_145_78, P149_40_170, P67_102_161, P60_146_156, P217… |
| last_profession_152M | category | 305137 | 19.99 | 3575 | a55475b1, P104_137_180, P46_72_80, P95_143_148, P203_66_70, P21_76_53, P167_22_… |
| first_profession_152M | category | 305137 | 19.99 | 1999 | a55475b1, P46_72_80, P104_137_180, P21_76_53, P116_59_165, P139_125_64, P121_11… |
| last_rejectreason_755M | category | 305137 | 19.99 | 17 | a55475b1, P99_56_166, P45_84_106, P198_131_9, P94_109_143, P196_88_176, P121_60… |
| first_rejectreason_755M | category | 305137 | 19.99 | 18 | a55475b1, P99_56_166, P94_109_143, P45_84_106, P198_131_9, P48_22_32, P30_86_84… |
| last_rejectreasonclient_4145042M | category | 305137 | 19.99 | 11 | a55475b1, P94_109_143, P5_143_178, P19_25_34, P30_86_84, P53_10_15, P69_72_116,… |
| first_rejectreasonclient_4145042M | category | 305137 | 19.99 | 14 | a55475b1, P94_109_143, P30_86_84, P52_67_90, P69_72_116, P129_162_80, P84_14_61… |
| last_status_219L | category | 305203 | 19.99 | 10 | K, D, A, T, Q, N, H, L, S, P |
| first_status_219L | category | 305137 | 19.99 | 11 | D, A, K, T, N, S, Q, L, H, P |
| last_collater_typofvalofguarant_298M | category | 141371 | 9.26 | 3 | a55475b1, 8fd95e4b, 9a0c095e |
| first_collater_typofvalofguarant_298M | category | 141371 | 9.26 | 5 | 9a0c095e, 8fd95e4b, a55475b1, 06fb9ba8, 26cf31be |
| last_collater_typofvalofguarant_407M | category | 141371 | 9.26 | 3 | a55475b1, 8fd95e4b, 9a0c095e |
| first_collater_typofvalofguarant_407M | category | 141371 | 9.26 | 7 | 9a0c095e, a55475b1, 8fd95e4b, 06fb9ba8, 3cbe86ba, 9276e4bb, c7a5ad39 |
| last_collaterals_typeofguarante_359M | category | 141371 | 9.26 | 8 | a55475b1, c7a5ad39, 9276e4bb, 0e63c0f0, 7b62420e, 3cbe86ba, 168ad9f3, f4d8a027 |
| first_collaterals_typeofguarante_359M | category | 141371 | 9.26 | 15 | c7a5ad39, a55475b1, 3cbe86ba, 9276e4bb, 168ad9f3, 940efad7, 5224034a, 0e63c0f0,… |
| last_collaterals_typeofguarante_669M | category | 141371 | 9.26 | 6 | a55475b1, 0e63c0f0, 168ad9f3, 3cbe86ba, 9276e4bb, f4d8a027 |
| first_collaterals_typeofguarante_669M | category | 141371 | 9.26 | 15 | c7a5ad39, a55475b1, 9276e4bb, 7b62420e, 0e63c0f0, 940efad7, 2fd21cf1, 3cbe86ba,… |
| last_subjectroles_name_541M | category | 141371 | 9.26 | 2 | a55475b1, ab3c25cf |
| first_subjectroles_name_541M | category | 141371 | 9.26 | 9 | ab3c25cf, a55475b1, 15f04f45, daf49a8a, be4fd70b, 0c42a10e, 1d94eac1, 71ddaa88,… |
| first_subjectroles_name_838M | category | 141371 | 9.26 | 9 | ab3c25cf, a55475b1, be4fd70b, daf49a8a, 15f04f45, P28_48_88, 0c42a10e, 71ddaa88… |
| last_classificationofcontr_13M | category | 140386 | 9.2 | 3 | a55475b1, 01f63ac8, ea6782cc |
| first_classificationofcontr_13M | category | 140386 | 9.2 | 11 | ea6782cc, a55475b1, 01f63ac8, 00135d9c, 4408ff0f, 1cf4e481, be7b251d, 2c070815,… |
| last_classificationofcontr_400M | category | 140386 | 9.2 | 25 | a55475b1, ea6782cc, 01f63ac8, 00135d9c, 4408ff0f, 1cf4e481, e2453741, f0a30139,… |
| first_classificationofcontr_400M | category | 140386 | 9.2 | 301 | ea6782cc, a55475b1, 01f63ac8, 42a42e75, e2453741, 9158339f, 00135d9c, d7416962,… |
| last_contractst_545M | category | 140386 | 9.2 | 3 | a55475b1, 7241344e, 8f3a197f |
| first_contractst_545M | category | 140386 | 9.2 | 47 | 7241344e, a55475b1, 8f3a197f, 0dc85f9d, b919198c, a52d5641, dd67cff0, 885ce291,… |
| last_contractst_964M | category | 140386 | 9.2 | 60 | a55475b1, 7241344e, 89c856d6, 41694615, dc23998c, b6834721, b2f1bf5c, 181f7276,… |
| first_contractst_964M | category | 140386 | 9.2 | 198 | 7241344e, a55475b1, 8f3a197f, d7416962, 8260bab9, b83056f9, 4476359f, 89721976,… |
| last_description_351M | category | 140386 | 9.2 | 10 | a55475b1, f8e51f8d, 0349102c, 6da7c7ed, 53179c19, 95decc86, 18e98e64, 0cb4d552,… |
| first_description_351M | category | 140386 | 9.2 | 11 | a55475b1, 95decc86, 53179c19, 6da7c7ed, f8e51f8d, 1d89fa48, 0cb4d552, 18e98e64,… |

(651 more rows not shown)

</details>

### Target distribution

| target | count | pct |
|---|---|---|
| No | 1478665 | 96.86 |
| Yes | 47994 | 3.14 |

### Numeric features

<details>
<summary>Show the table (596 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| MONTH | 152666 | 201936 | 44.6509 | 201901 | 202010 |
| WEEK_NUM | 152666 | 40.7677 | 23.76 | 0 | 91 |
| actualdpdtolerance_344P | 110932 | 0.048372 | 6.08112 | 0 | 1943 |
| amtinstpaidbefduel24m_4187115A | 96815 | 55927.6 | 71521.5 | 0 | 1.05116e+06 |
| annuity_780A | 152666 | 4034.31 | 2992.75 | 145.8 | 56021.8 |
| annuitynextmonth_57A | 152666 | 1433.86 | 2813.39 | 0 | 61800 |
| applicationcnt_361L | 152666 | 0 | 0 | 0 | 0 |
| applications30d_658L | 152666 | 0.135512 | 0.471731 | 0 | 15 |
| applicationscnt_1086L | 152666 | 0.417283 | 3.06051 | 0 | 564 |
| applicationscnt_464L | 152666 | 1.04573 | 9.47559 | 0 | 245 |
| applicationscnt_629L | 152666 | 0.262337 | 2.43151 | 0 | 85 |
| applicationscnt_867L | 152666 | 2.8862 | 4.38081 | 0 | 287 |
| avgdbddpdlast24m_3658932P | 91431 | 29.92 | 315.707 | -665 | 4680 |
| avgdbddpdlast3m_4187120P | 58052 | 29.5238 | 367.871 | -531 | 4680 |
| avgdbdtollast24m_4525197P | 55571 | 30.4637 | 321.252 | -653 | 4680 |
| avgdpdtolclosure24_3658938P | 106055 | 45.0822 | 315.498 | 0 | 4680 |
| avginstallast24m_3658937A | 90266 | 5397.43 | 6371.74 | 0 | 261870 |
| avglnamtstart24m_4525187A | 16324 | 44552.9 | 44527.5 | 0 | 400000 |
| avgmaxdpdlast9m_3716943P | 77132 | 0.730294 | 4.5321 | 0 | 231 |
| avgoutstandbalancel6m_4187114A | 68809 | 46062.8 | 64060.1 | -510000 | 1.12872e+06 |
| avgpmtlast12m_4525200A | 50184 | 6372.43 | 8618.18 | 0 | 261870 |
| clientscnt12m_3712952L | 152666 | 0.0387316 | 0.865326 | 0 | 198 |
| clientscnt3m_3712950L | 152666 | 0.0193691 | 0.620862 | 0 | 105 |
| clientscnt6m_3712949L | 152666 | 0.0274652 | 0.79139 | 0 | 154 |
| clientscnt_100L | 152666 | 0.0509347 | 0.479235 | 0 | 106 |
| clientscnt_1022L | 152666 | 0.11009 | 1.37218 | 0 | 266 |
| clientscnt_1071L | 152666 | 0.0342774 | 0.190352 | 0 | 11 |
| clientscnt_1130L | 152666 | 0.0309237 | 0.210132 | 0 | 24 |
| clientscnt_157L | 152666 | 0.078806 | 0.842898 | 0 | 241 |
| clientscnt_257L | 152666 | 0.00314412 | 0.0683156 | 0 | 12 |
| clientscnt_304L | 152666 | 0.0770375 | 1.31625 | 0 | 423 |
| clientscnt_360L | 152666 | 0.00322272 | 0.0597166 | 0 | 3 |
| clientscnt_493L | 152666 | 0.015642 | 1.00607 | 0 | 354 |
| clientscnt_533L | 152666 | 0.0759174 | 0.284239 | 0 | 6 |
| clientscnt_887L | 152666 | 2.34458 | 38.6052 | 0 | 1237 |
| clientscnt_946L | 152666 | 0.0328429 | 0.343081 | 0 | 72 |
| cntincpaycont9m_3716944L | 107327 | 6.17368 | 6.25143 | 0 | 392 |
| cntpmts24_3658933L | 106762 | 10.614 | 7.87838 | 0 | 25 |
| credamount_770A | 152666 | 49893.6 | 44295 | 2000 | 432659 |
| currdebt_22A | 152666 | 19763.6 | 51407.1 | 0 | 1.09239e+06 |
| currdebtcredtyperange_828A | 152666 | 11093 | 37330.7 | 0 | 1.02939e+06 |
| datefirstoffer_1144D | 69111 | -2462.03 | 1616.2 | -4883 | 13 |
| datelastinstal40dpd_247D | 13400 | -1972.72 | 1555.65 | -5174 | -26 |
| datelastunpaid_3546854D | 63825 | -958.899 | 1246.18 | -5140 | 13 |
| daysoverduetolerancedd_3976961L | 107602 | 96.5504 | 482.263 | 0 | 5244 |
| disbursedcredamount_1113A | 152666 | 46099.8 | 42659.6 | 0 | 400000 |
| downpmt_116A | 152666 | 567.522 | 4256.49 | 0 | 461867 |
| dtlastpmtallstes_4499206D | 55000 | -413.342 | 845.578 | -5233 | 13 |
| eir_270L | 133498 | 0.277416 | 0.197525 | 0 | 0.45 |
| firstclxcampaign_1125D | 66574 | -990.635 | 465.966 | -1709 | 14 |
| firstdatedue_489D | 104584 | -1834.16 | 1453.94 | -5318 | 45 |
| homephncnt_628L | 152666 | 0.637411 | 0.851553 | 0 | 8 |
| inittransactionamount_650A | 19311 | 32436.1 | 33280.1 | 0 | 200000 |
| lastactivateddate_801D | 107490 | -629.309 | 905.943 | -5318 | 14 |
| lastapplicationdate_877D | 122344 | -468.571 | 748.067 | -5242 | 14 |
| lastapprcredamount_781A | 108646 | 36912.8 | 37034.4 | 0 | 400000 |
| lastapprdate_640D | 108646 | -609.128 | 889.847 | -5321 | 14 |
| lastdelinqdate_224D | 54882 | -539.273 | 645.565 | -4859 | 13 |
| lastrejectcredamount_222A | 75863 | 51141.8 | 53356 | 0 | 1e+06 |
| lastrejectdate_50D | 75863 | -835.042 | 1006.34 | -5265 | 14 |

(536 more rows not shown)

</details>

### Categorical features

<details>
<summary>Show the table (516 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| cardtype_51L | 1 | &lt;NA> | 133411 | 87.39 |
| cardtype_51L | 2 | INSTANT | 19031 | 12.47 |
| cardtype_51L | 3 | PERSONALIZED | 224 | 0.15 |
| credtype_322L | 1 | COL | 98847 | 64.75 |
| credtype_322L | 2 | CAL | 34508 | 22.6 |
| credtype_322L | 3 | REL | 19311 | 12.65 |
| date_decision | 1 | 2019-11-29 00:00:00 | 917 | 0.6 |
| date_decision | 2 | 2019-11-30 00:00:00 | 884 | 0.58 |
| date_decision | 3 | 2019-12-28 00:00:00 | 716 | 0.47 |
| date_decision | 4 | 2019-12-30 00:00:00 | 638 | 0.42 |
| date_decision | 5 | 2019-11-16 00:00:00 | 631 | 0.41 |
| description_5085714M | 1 | a55475b1 | 131712 | 86.27 |
| description_5085714M | 2 | 2fc785b2 | 18355 | 12.02 |
| description_5085714M | 3 | &lt;NA> | 2599 | 1.7 |
| disbursementtype_67L | 1 | SBA | 113919 | 74.62 |
| disbursementtype_67L | 2 | GBA | 34504 | 22.6 |
| disbursementtype_67L | 3 | DD | 4154 | 2.72 |
| disbursementtype_67L | 4 | &lt;NA> | 89 | 0.06 |
| education_1103M | 1 | a55475b1 | 86209 | 56.47 |
| education_1103M | 2 | 6b2ae0fa | 45190 | 29.6 |
| education_1103M | 3 | 717ddd49 | 13495 | 8.84 |
| education_1103M | 4 | 39a0853f | 4615 | 3.02 |
| education_1103M | 5 | &lt;NA> | 2599 | 1.7 |
| education_88M | 1 | a55475b1 | 148536 | 97.29 |
| education_88M | 2 | &lt;NA> | 2599 | 1.7 |
| education_88M | 3 | 6b2ae0fa | 1132 | 0.74 |
| education_88M | 4 | 717ddd49 | 340 | 0.22 |
| education_88M | 5 | a34a13c8 | 41 | 0.03 |
| equalitydataagreement_891L | 1 | &lt;NA> | 144931 | 94.93 |
| equalitydataagreement_891L | 2 | True | 7227 | 4.73 |
| equalitydataagreement_891L | 3 | False | 508 | 0.33 |
| first_cancelreason_3545846M | 1 | a55475b1 | 76779 | 50.29 |
| first_cancelreason_3545846M | 2 | &lt;NA> | 30322 | 19.86 |
| first_cancelreason_3545846M | 3 | P94_109_143 | 30085 | 19.71 |
| first_cancelreason_3545846M | 4 | P85_114_140 | 2268 | 1.49 |
| first_cancelreason_3545846M | 5 | P30_86_84 | 2226 | 1.46 |
| first_classificationofcontr_13M | 1 | ea6782cc | 115757 | 75.82 |
| first_classificationofcontr_13M | 2 | &lt;NA> | 13999 | 9.17 |
| first_classificationofcontr_13M | 3 | a55475b1 | 12315 | 8.07 |
| first_classificationofcontr_13M | 4 | 01f63ac8 | 6276 | 4.11 |
| first_classificationofcontr_13M | 5 | 00135d9c | 2435 | 1.59 |
| first_classificationofcontr_400M | 1 | ea6782cc | 52177 | 34.18 |
| first_classificationofcontr_400M | 2 | a55475b1 | 37389 | 24.49 |
| first_classificationofcontr_400M | 3 | &lt;NA> | 13999 | 9.17 |
| first_classificationofcontr_400M | 4 | 01f63ac8 | 6893 | 4.52 |
| first_classificationofcontr_400M | 5 | 42a42e75 | 5670 | 3.71 |
| first_collater_typofvalofguarant_298M | 1 | 9a0c095e | 98339 | 64.41 |
| first_collater_typofvalofguarant_298M | 2 | 8fd95e4b | 27915 | 18.29 |
| first_collater_typofvalofguarant_298M | 3 | &lt;NA> | 14101 | 9.24 |
| first_collater_typofvalofguarant_298M | 4 | a55475b1 | 12268 | 8.04 |
| first_collater_typofvalofguarant_298M | 5 | 06fb9ba8 | 43 | 0.03 |
| first_collater_typofvalofguarant_407M | 1 | 9a0c095e | 68080 | 44.59 |
| first_collater_typofvalofguarant_407M | 2 | a55475b1 | 37847 | 24.79 |
| first_collater_typofvalofguarant_407M | 3 | 8fd95e4b | 32348 | 21.19 |
| first_collater_typofvalofguarant_407M | 4 | &lt;NA> | 14101 | 9.24 |
| first_collater_typofvalofguarant_407M | 5 | 06fb9ba8 | 264 | 0.17 |
| first_collaterals_typeofguarante_359M | 1 | c7a5ad39 | 69741 | 45.68 |
| first_collaterals_typeofguarante_359M | 2 | a55475b1 | 37847 | 24.79 |
| first_collaterals_typeofguarante_359M | 3 | 3cbe86ba | 21240 | 13.91 |
| first_collaterals_typeofguarante_359M | 4 | &lt;NA> | 14101 | 9.24 |

(456 more rows not shown)

</details>

## Build

| field | value |
|---|---|
| uuid | 01a217fa-29fa-7f2b-a908-f1cc4d7dd86e |
| checksum | v2:9f065a85f70a1ef378fa5e27d3137ae19db629634ea8e9dd8ab99bbd979b2c10 |
| built_at | 2026-11-26T13:10:44+00:00 |
| path | home_credit_default_stability_1m/01a217fa-29fa-7f2b-a908-f1cc4d7dd86e |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
