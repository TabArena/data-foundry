---
report_format: data-foundry-report-v2
unique_name: chicago_traffic_crashes
container_format: 2
checksum: v2:e54f9570c1debb30e834661f8ca7a7160541103afc3b536ec130ed513dd7cc71
build:
  uuid: 01a217fd-5b06-7d55-841f-8e0d110f9174
  checksum: v2:e54f9570c1debb30e834661f8ca7a7160541103afc3b536ec130ed513dd7cc71
  built_at: '2026-11-26T13:13:40+00:00'
  path: chicago_traffic_crashes/01a217fd-5b06-7d55-841f-8e0d110f9174
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
  n_rows: 998117
  n_features: 15
  dtypes:
    category: 10
    datetime64[ns]: 1
    float64: 5
  n_test_dataset_rows: null
task:
  target: most_severe_injury
  problem_type: multiclass_classification
  metric: log_loss
  metric_origin: fallback
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: most_severe_injury
  time_on: crash_date
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
  time_gap: 1
  time_gap_unit: months
  reason: 'Training starts on 2017-09-01; no side is sampled.

    October 2026 is excluded because the source snapshot ends within that month; the
    newest test month is September 2026.

    The length is the refit cadence, one month (the curator''s pick, 2026-11-11):
    the one documented cycle of the

    analyst''s work is monthly, as CDOT compiles its list of traffic fatalities "after
    monthly reviews of fatal

    traffic crash information" and updates it monthly (Vision Zero Chicago Traffic
    Fatalities, catalog.data.gov);

    the yearly crash report is its other cycle. The quarter used until 2026-11-11
    was a convention of the build that

    no source names. A month holds 6 to 15 fatal crashes against 20 to 30 in a quarter,
    so a window''s score leans

    less on them, which the log loss over all five classes allows. The one-month horizon
    is a refit cadence, not a

    medical outcome window.

    The windows (the curator''s pick of 2026-11-11: nine spread over four years, at
    one month): the newest month

    always stays; the other eight are spread over the 53 monthly windows that keep
    half the crashes for training

    (May 2022 to September 2026), stepping back five and six months in turn, so each
    window falls in another

    calendar month and every season appears at least twice (September, October and
    November; April and May; June

    and July; December and January), and they lie on both sides of the 2023Q4 step
    in "reported, not evident"

    (below). Test crashes (fatal ones), then training crashes after the notification
    filter and their share of the

    998,117: September 2026 9,641 (6), 978,937 (98.1%); April 2026 8,961 (10), 931,711
    (93.3%); October 2025 9,031

    (7), 879,272 (88.1%); May 2025 10,079 (6), 830,229 (83.2%); November 2024 8,924
    (9), 777,987 (77.9%); June 2024

    10,120 (10), 727,880 (72.9%); December 2023 9,095 (12), 675,888 (67.7%); July
    2023 9,499 (8), 627,408 (62.9%);

    January 2023 8,091 (15), 574,344 (57.5%). In all 83,441 test crashes, 83 of them
    fatal; no window trains on

    less than half the crashes.

    Train ends one month before each window (a one-month gap, as zillow_prize): a
    model refit at a month start

    would not yet see the final class of the last month''s crashes, since the SR1050
    manual lets a report be amended

    when a person dies later (printed pages 2-3 and 9) and a traffic death is counted
    within 30 days of the crash.

    The source has no label versions or amendment dates. The portal''s row field :updated_at
    bounds the delay: for

    crashes of June-August 2026 the last update is a median 16.1 days after the crash
    and 99.4% of rows are last

    updated within 30 days; 5 of 32 fatal crashes were updated later (33-102 days);
    injury shares do not shift

    across the update. Limits: :updated_at changes with any field, not only the label;
    the bulk reload of

    2026-05-21 hides earlier history; 1,904 older crashes were rewritten in one batch
    on 2026-11-03.

    lt_vehicle_loan_default_prediction has no gap because there a 30-day gap would
    leave training sides under

    SPLIT-14''s 50% floor and its measured effect was small; here the floor holds
    and the gap costs 0.9-1.6% of a

    training side. The 9,529 crashes of August 2026, the newest window''s gap month,
    fall in no split, as do 9

    crashes of January to July 2026 notified only after 1 September 2026 and the one
    notified before its event.

    Training also requires DATE_POLICE_NOTIFIED strictly before the month start of
    the window (the refit) and not

    before the recorded event; 9 to 37 crashes of a training side''s history are not
    yet notified then and are left

    out. This intermediate timestamp is removed before the model frame is returned.
    The event time is floored to

    whole hours in `_clean`, before the rows are sorted by it, and cohorts are drawn
    on the floored hour (window and

    gap bounds fall on midnight, so no cohort changes); only the check "not notified
    before the recorded event"

    reads the source minute, through a flag removed with the timestamp (2026-11-05,
    LEAK-13).

    Locations can recur across time; this is not unseen-location evaluation.

    Drift (SPLIT-20, USE-5 open): the share of "REPORTED, NOT EVIDENT" steps from
    4.09-4.71% (2022Q1-2023Q3) to

    5.56% in 2023Q4, then 6.07-6.54% (2024Q2-2026Q1) and 6.64-6.74% (2026Q2-Q3, a
    further rise in desk reports),

    while incapacitating plus fatal falls from about 2.0% to 1.4%; the desk-report
    share stays at 50-53%. January

    and July 2023 lie before the step (4.0% and 4.8% of their crashes), December 2023
    in its quarter (5.2%) and the

    six newer windows after it (6.0-6.8%); the step was accepted as drift on 2026-11-05,
    the same task on both

    sides. Its cause (a change in recording practice?) is not known.'
  n_train:
    min: 574344
    max: 978937
  n_test:
    min: 8091
    max: 10120
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  - dataset_conflicting_duplicate_rows
  - splits_rows_unused
  accepted: {}
decisions:
- Keep all five police injury classes
- Filter measurable notification unavailability before each refit
---

# chicago_traffic_crashes

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Multiclass classification of `most_severe_injury`, scored with `log_loss` on temporal splits by `crash_date`. 998,117 rows and 15 features. Source: GOV Website (2026).

Built as `01a217fd-5b06-7d55-841f-8e0d110f9174` on 2026-11-26. See [Build](#build).

## In brief

**Question.** What is the most serious police-recorded injury in this crash?

**Use case.** A city road-safety analyst estimates, for each reported crash, the probability of each police injury level from the recorded crash and road facts, to estimate the expected number of people killed or seriously injured at each site and rank sites for countermeasures.

**One row.** One CPD-recorded Chicago crash before October 2026; from September 2017, when citywide coverage starts.

**Predicted.** The most severe injury among people involved: fatal, incapacitating, nonincapacitating, reported but not evident, or no indication. This is an officer-recorded classification, potentially amended later, not a fixed medical follow-up.

**Known at prediction time.** The finalized report's crash and road facts, without its injury, damage or reporting fields: crash hour and location, posted speed, trafficway type, first collision type, units involved, and sparse work-zone and private-property flags.

**What the test data stands for.** Nine one-month crash cohorts spread from January 2023 to September 2026, each in another calendar month, are tested against all earlier crashes up to one month before the window that were notified before the monthly refit, the cycle of the city's fatal-crash review; labels are from the final snapshot.

**Our changes to the source.** We exclude reporting activity, injury/damage outcomes, investigation judgments, identifiers, the road and condition fields whose recording follows the injury and the door-opening flag; start at September 2017; floor crash time to whole hours.

> **Use case fit: approximate (a stand-in with a known gap).** The police injury level stands in for the serious injuries the analyst counts: trauma-registry linkage finds police reports catch about half of them (Traffic Injury Prevention 2024), and the share of 'reported, not evident' injuries steps up in late 2023. Lane count, alignment, road defects, weather, lighting, surface and traffic control are dropped because injury reports record them more completely, though an analyst could take them from road inventories.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/chicago_traffic_crashes.md`](../../../../curation/records/chicago_traffic_crashes.md)
- The original source: <https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/chicago_traffic_crashes/`. To get them:

```text
Download the official CSV export to local-data-warehouse/chicago_traffic_crashes/crashes.csv:
https://data.cityofchicago.org/api/views/85ca-t3if/rows.csv?accessType=DOWNLOAD
The pinned snapshot is the export downloaded on 2026-11-04 (1,109,972 rows; sha256
4bf63b07d869d992887c08d70bc017a357f731e6bf563dd6098546417b29027b). The 2026-10-29 bytes are no longer kept.
The live portal amends historical records, so downloading again need not reproduce those bytes, and the
export URL stops working on 2026-12-22.
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/chicago_traffic_crashes   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/chicago_traffic_crashes   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | GOV Website: https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if |
| year | 2026 |
| domain | social science |
| license | See Terms of Use (City of Chicago Data Portal) |
| data_tags | Non-IID, Temporal, Spatial |
| reference | chicago_crashes |
| rows x columns | 998,117 x 16 |
| task.target | most_severe_injury |
| task.problem_type | multiclass_classification |
| task.metric | log_loss |
| task.split_regime | temporal_non_iid |
| task.stratify_on | most_severe_injury |
| task.time_on | crash_date |

**Metric**

| field | value |
|---|---|
| name | `log_loss` (standard; takes proba; lower is better) |
| origin | fallback: the default for the problem type: the source defines no metric the task would use in practice |
| definition | mean of -log p(true class) |
| reason | The original City portal, field dictionary and linked SR1050 manual define a crash-report release, not a scored prediction competition or a single defining model-selection metric. Use multiclass log loss for the accepted five-class probability task. On July-September 2026 about 35% of the loss is in the 'reported, not evident' class and about 10% in incapacitating plus fatal; skill over the class prior is 18.0% on all rows against 11.8% on on-scene reports alone (one quick LightGBM on most of the shipped inputs, 2026-11-05). |

<details>
<summary>Feature types: 9 categorical, 1 ordinal, 0 string, 1 datetime</summary>

- categorical (9): `beat_of_occurrence`, `first_crash_type`, `not_right_of_way_i`, `street_direction`, `street_name`, `trafficway_type`, `work_zone_i`, `work_zone_type`, `workers_present_i`
- ordinal (1): `most_severe_injury (NO INDICATION OF INJURY < REPORTED, NOT EVIDENT < NONINCAPACITATING INJURY < INCAPACITATING INJURY < FATAL)`
- string (0): none
- datetime (1): `crash_date`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{chicago_crashes,
  author = {{City of Chicago, Chicago Police Department}},
  title = {Traffic Crashes - Crashes},
  year = {2026},
  howpublished = {\url{https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if}}
}
```

</details>

## Sample rows

The first 5 of 998,117 rows of the final frame (the oldest rows: the frame is sorted by `crash_date`); 12 of 16 columns, the target first. Cells are cut at 40 characters.

| most_severe_injury | crash_date | posted_speed_limit | first_crash_type | trafficway_type | not_right_of_way_i | street_no | street_direction | street_name | beat_of_occurrence | work_zone_i | work_zone_type |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NO INDICATION OF INJURY | 2017-09-01 00:00:00 | 30 | REAR END | NOT DIVIDED | nan | 4750 | N | PULASKI RD | 1722 | nan | nan |
| NO INDICATION OF INJURY | 2017-09-01 00:00:00 | 30 | PARKED MOTOR VEHICLE | ONE-WAY | nan | 1658 | W | JUNEWAY TER | 2422 | nan | nan |
| NO INDICATION OF INJURY | 2017-09-01 00:00:00 | 30 | TURNING | NOT DIVIDED | nan | 3201 | N | CUMBERLAND AVE | 1631 | nan | nan |
| NO INDICATION OF INJURY | 2017-09-01 00:00:00 | 35 | TURNING | DIVIDED - W/MEDIAN (NOT RAISED) | nan | 1130 | W | GRAND AVE | 1214 | nan | nan |
| NO INDICATION OF INJURY | 2017-09-01 00:00:00 | 30 | FIXED OBJECT | DIVIDED - W/MEDIAN (NOT RAISED) | nan | 1422 | N | DAMEN AVE | 1424 | nan | nan |

## Curation notes

We start with the original City's 2026-11-04 bulk CSV export, not a Kaggle re-upload. Figures marked
"(2026-10-29)" were measured on the earlier export, whose bytes are no longer kept.

- Prediction point: a reported crash's finalized crash and road facts, before its injury classification, from which a city road-safety analyst estimates the chance of each injury level to rank sites by expected people killed or seriously injured (2026-11-05; superseded: an approximate scene-based injury assessment for emergency response). On 2026-10-29 Myunghwan accepted closer-to-fact finalized information rather than reconstructing timely initial-call availability (superseded 2026-11-05 for the actor: finalized records are what the analyst works from, so they are no longer the gap). Later administrative/reporting activity, injury consequences and outcome encodings remain excluded; Myunghwan accepted this exact approximate task for shipping on 2026-10-29; build and repository integration are separate steps.
- CC (2026-11-05, Lennart): the use case is a city road-safety analyst who ranks sites by expected people killed or seriously injured (USE-1, USE-9: the blind reviewer named the same actor without our notes). It supersedes the emergency-response framing Myunghwan accepted on 2026-10-29: 50.9% of the rows are desk reports nobody was dispatched to (5.3% injured against 25.5% on scene). Every row stays. The fit stays approximate: police reports catch about half of serious injuries in trauma-registry linkage, the 'reported, not evident' share steps up in 2023Q4, and the road facts recorded more completely for injury crashes are dropped.
- Late labels (SPLIT-10; 2026-11-04, Lennart): a one-month gap between train and test, as zillow_prize. A report can be amended after a later death, and a traffic death counts within 30 days of the crash, so a refit at a month start would see the newest month's crashes in a lower class than the final snapshot gives. The source has no label versions or amendment times; the portal's :updated_at field (any field, not only the label) puts 99.4% of last updates within 30 days of the crash (median 16.1 days, crashes of June-August 2026), with 5 of 32 fatal crashes updated later, at 33-102 days. Labels stay those of the final snapshot. A month is 0.9-1.6% of a training side (1.0-1.4% at the quarterly windows of 2026-11-05), and the strict notification eligibility remains.
- CC (2026-11-05, Lennart): the one-month gap stays (SPLIT-10 as amended 2026-11-04: the gap is about the label's delay). It covers 99.4% of last updates; two months would cover 4 of the 5 late fatal updates and cost about 1% of each training side.
- CC (2026-11-05, Lennart): the step in 'reported, not evident' in 2023Q4 is accepted as drift, with the shares in `splits_comment` (USE-5 fails only when the label is shown to be another quantity, SPLIT-20).
- CC (2026-11-11, Lennart): one-month test windows ("Reply (b): One month": the cycle of the city's monthly fatal-crash review), nine of them spread over four years ("Option B: Nine spread over four years."): September 2026, April 2026, October 2025, May 2025, November 2024, June 2024, December 2023, July 2023 and January 2023, each in another calendar month, with the one-month gap and the notification filter at each month start; every window trains on 57.5% to 98.1% of the crashes. Measurements above on "the three newest windows" or "all 9 splits" were taken on the quarterly windows used until then.
- CRASH_DATE is the event timestamp: its original precision defines source-copy checks, and it is floored to whole hours for every row in `_clean`, before the framework sorts the rows by it (cohorts: original precision until 2026-11-05, now the floored hour, the same windows). Exact-hour recording differed by injury even within report type (on-scene: 8.21% injured versus 13.07% uninjured; desk: 18.86% versus 25.09%). The paired three-quarter diagnostic (2026-10-29, 21-input recipe) removed minute information for 889,076 rows without moving any quarter; mean log loss changed from 0.550174 to 0.550105. This harmonizes minute precision, not event-time accuracy. DATE_POLICE_NOTIFIED is notification time, used only as intermediate training-eligibility metadata and excluded from predictors together with delays. CRASH_DATE_EST_I is a later reporting flag, not a timestamp. The source carries no timezone offset; no UTC conversion is assumed.
- CC (2026-11-05, Lennart): `crash_date` is floored in `_clean`, not in `_make_splits` (LEAK-13, as hepatitis_c_prediction and gallstone_disease). The framework sorts the rows by the time column between the two steps, so the floor in `_make_splits` left each hour in minute order, and a row's rank in its hour lowered log loss by 0.00098 (0.00008 to 0.00202, on all 9 splits). Each hour now keeps the content order, the windows are the same, and the one crash notified before its recorded time stays unused through a flag computed from the source minute.
- Injury counts, CRASH_TYPE and DAMAGE are outcome information; REPORT_TYPE, photo/statement flags, and primary/secondary contributory causes are reporting or investigation information and are excluded. INTERSECTION_RELATED_I is a causal judgment, not an at-intersection indicator. HIT_AND_RUN_I is withheld as post-collision flight/aid behavior rather than an initial physical condition; no injury-caused mechanism is claimed proved for that flag.
- Keep underlying trafficway, posted speed, location and initial-collision facts as approximate candidates. FIRST_CRASH_TYPE follows the manual's first damage/injury event and sequence rules; it is not necessarily a raw caller observation. The bulk header NOT_RIGHT_OF_WAY_I corresponds to API alias private_property_i, meaning contact beginning outside the public right-of-way. Blank Y/N fields remain missing, not inferred N.
- Exclude LANE_CNT, ALIGNMENT and ROAD_DEFECT from the initial recipe: the IDOT March 2011 dictionary, printed elements 80, 81 and 84 (PDF pages 40 and 43), requires them for injury/towing reports but not minor drive-away reports. Their underlying road facts preexist injury, but outcome-dependent collection makes the stored fields unsafe stand-ins without reconstruction. This is a source-based precaution, not a claim that every value is demonstrably leaked.
- POSTED_SPEED_LIMIT has the same historical N/Y requirement (element 50); omission from the earlier sibling sweep was corrected. A zero speed is 0.548% of uninjured against 0.280% of injured crashes in the frame, but 39% of zeros are parking-lot crashes and within parking lots the rates are 3.00% against 2.80%: a zero mostly marks a place without a posted limit, a scene fact, not a field left blank on minor reports. The 66 source values of 99 all fall in 2015, before the frame starts. The check does not validate every nonzero default. Myunghwan accepted keeping posted speed as implemented on 2026-10-29; no source-value replacement or reconstruction was requested.
- WEATHER_CONDITION, LIGHTING_CONDITION, ROADWAY_SURFACE_COND, TRAFFIC_CONTROL_DEVICE and DEVICE_CONDITION are dropped (LEAK-10; Lennart, 2026-11-04), as LANE_CNT, ALIGNMENT and ROAD_DEFECT: on the three newest windows they lower the five-class log loss by 0.0039, and flags saying only whether each was recorded win back 0.0028 of that (72%), so most of their gain is whether the field was filled in. Without them the task still rests on the collision type, the units involved, the hour and the road layout (log loss 0.4960 against the class prior's 0.6140; superseded 2026-11-05: 0.4962 against 0.6130 on the shipped 15 inputs from 2017-09, the same LightGBM, mean of the three newest windows).
- CC (2026-11-05, Lennart): `dooring_i` is dropped (LEAK-10 through LEAK-38's measured clause, as the five fields). Within a crash type, injured crashes have it filled in 4-8 times as often, though the 'N' value alone shows no consistent difference by outcome; the drop costs 0.00011 log loss (0.49609 to 0.49620, three newest windows). If the LEAK-38 amendment opened on 2026-11-05 takes the any-source scope, `dooring_i` falls under it too.
- Training starts on 2017-09-01, when citywide coverage starts (SPLIT-20; Lennart, 2026-11-04): before it, 7.3% of crashes have any injury against 15.3% after, with 4,000-7,000 crashes a month against 9,000-10,000. It leaves the score unchanged (0.49609 against 0.49600 from 2013, on the 16 inputs of 2026-11-04; 0.49620 against 0.49610 on the shipped 15 inputs, 2026-11-05) and costs about 99,100 rows per training side. No training side then exceeds one million rows, so the task ships unsampled, not as a `_1m` version.
- Remove exact source copies using every original field except CRASH_RECORD_ID, IDOT_CONTROL_NO and REPORT_TYPE; keep the first source-order representative. The full export has 63 extra copies on that key (both exports); on the 2026-10-29 export 36 already matched even with the control number included, and the broader key removed 26 additional rows from the labeled pre-October cohort; raw rows remain preserved. Distinct administrative IDs alone do not establish independent events. Do not deduplicate on the reduced or hour-rounded predictor vector: some source-distinct crashes coincide after context is removed, and conflicting reduced profiles can be genuine label ambiguity. The remaining reused control number with different time/location is not collapsed. Missing labels and the unfinished October cohort are excluded; classes are not merged. Partial early coverage does not establish citywide incident rates.
- CRASH_HOUR, CRASH_DAY_OF_WEEK and CRASH_MONTH are redundant components of CRASH_DATE. LOCATION repeats latitude/longitude; report identifiers are not predictors. Coordinate zeros are made missing because they cannot identify a Chicago crash location. Unknown/unreported categorical codes become missing; no outcome-based imputation is used.
- CC (2026-11-05, Lennart): the declared metric (the fallback multiclass log loss over the five police injury classes) is checked and stays as declared.
- Retrospective officer judgments, outcome-dependent reporting completeness and historical label amendments remain limitations. The source permits more complete forms for injury/towing and amendment after later deaths (SR1050 manual, printed pages 2-3 and 9). The approximate fit does not waive feature-specific leakage checks or establish deployment validity.

## Splits

Custom temporal splits (`_make_splits`): 9 test window(s), each with its own train side. The test windows by `crash_date`, as listed: 2026-09-01 to 2026-09-30 (9,641 test, 978,937 train rows); 2026-04-01 to 2026-04-30 (8,961 test, 931,711 train rows); 2025-10-01 to 2025-10-31 (9,031 test, 879,272 train rows); 2025-05-01 to 2025-05-31 (10,079 test, 830,229 train rows); 2024-11-01 to 2024-11-30 (8,924 test, 777,987 train rows); 2024-06-01 to 2024-06-30 (10,120 test, 727,880 train rows); 2023-12-01 to 2023-12-31 (9,095 test, 675,888 train rows); 2023-07-01 to 2023-07-31 (9,499 test, 627,408 train rows); 2023-01-01 to 2023-01-31 (8,091 test, 574,344 train rows).

Training starts on 2017-09-01; no side is sampled.
October 2026 is excluded because the source snapshot ends within that month; the newest test month is September 2026.
The length is the refit cadence, one month (the curator's pick, 2026-11-11): the one documented cycle of the
analyst's work is monthly, as CDOT compiles its list of traffic fatalities "after monthly reviews of fatal
traffic crash information" and updates it monthly (Vision Zero Chicago Traffic Fatalities, catalog.data.gov);
the yearly crash report is its other cycle. The quarter used until 2026-11-11 was a convention of the build that
no source names. A month holds 6 to 15 fatal crashes against 20 to 30 in a quarter, so a window's score leans
less on them, which the log loss over all five classes allows. The one-month horizon is a refit cadence, not a
medical outcome window.
The windows (the curator's pick of 2026-11-11: nine spread over four years, at one month): the newest month
always stays; the other eight are spread over the 53 monthly windows that keep half the crashes for training
(May 2022 to September 2026), stepping back five and six months in turn, so each window falls in another
calendar month and every season appears at least twice (September, October and November; April and May; June
and July; December and January), and they lie on both sides of the 2023Q4 step in "reported, not evident"
(below). Test crashes (fatal ones), then training crashes after the notification filter and their share of the
998,117: September 2026 9,641 (6), 978,937 (98.1%); April 2026 8,961 (10), 931,711 (93.3%); October 2025 9,031
(7), 879,272 (88.1%); May 2025 10,079 (6), 830,229 (83.2%); November 2024 8,924 (9), 777,987 (77.9%); June 2024
10,120 (10), 727,880 (72.9%); December 2023 9,095 (12), 675,888 (67.7%); July 2023 9,499 (8), 627,408 (62.9%);
January 2023 8,091 (15), 574,344 (57.5%). In all 83,441 test crashes, 83 of them fatal; no window trains on
less than half the crashes.
Train ends one month before each window (a one-month gap, as zillow_prize): a model refit at a month start
would not yet see the final class of the last month's crashes, since the SR1050 manual lets a report be amended
when a person dies later (printed pages 2-3 and 9) and a traffic death is counted within 30 days of the crash.
The source has no label versions or amendment dates. The portal's row field :updated_at bounds the delay: for
crashes of June-August 2026 the last update is a median 16.1 days after the crash and 99.4% of rows are last
updated within 30 days; 5 of 32 fatal crashes were updated later (33-102 days); injury shares do not shift
across the update. Limits: :updated_at changes with any field, not only the label; the bulk reload of
2026-05-21 hides earlier history; 1,904 older crashes were rewritten in one batch on 2026-11-03.
lt_vehicle_loan_default_prediction has no gap because there a 30-day gap would leave training sides under
SPLIT-14's 50% floor and its measured effect was small; here the floor holds and the gap costs 0.9-1.6% of a
training side. The 9,529 crashes of August 2026, the newest window's gap month, fall in no split, as do 9
crashes of January to July 2026 notified only after 1 September 2026 and the one notified before its event.
Training also requires DATE_POLICE_NOTIFIED strictly before the month start of the window (the refit) and not
before the recorded event; 9 to 37 crashes of a training side's history are not yet notified then and are left
out. This intermediate timestamp is removed before the model frame is returned. The event time is floored to
whole hours in `_clean`, before the rows are sorted by it, and cohorts are drawn on the floored hour (window and
gap bounds fall on midnight, so no cohort changes); only the check "not notified before the recorded event"
reads the source minute, through a flag removed with the timestamp (2026-11-05, LEAK-13).
Locations can recur across time; this is not unseen-location evaluation.
Drift (SPLIT-20, USE-5 open): the share of "REPORTED, NOT EVIDENT" steps from 4.09-4.71% (2022Q1-2023Q3) to
5.56% in 2023Q4, then 6.07-6.54% (2024Q2-2026Q1) and 6.64-6.74% (2026Q2-Q3, a further rise in desk reports),
while incapacitating plus fatal falls from about 2.0% to 1.4%; the desk-report share stays at 50-53%. January
and July 2023 lie before the step (4.0% and 4.8% of their crashes), December 2023 in its quarter (5.2%) and the
six newer windows after it (6.0-6.8%); the step was accepted as drift on 2026-11-05, the same task on both
sides. Its cause (a change in recording practice?) is not known.

9 repeat(s) x 1 fold(s) with seed 4267; train 574,344 to 978,937 rows, test 8,091 to 10,120 rows. Prediction horizon: 1 months. Gap between train and test: 1 months.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 978937 | 9641 | 2017-09-01 00:00:00 | 2026-07-31 23:00:00 | 2026-09-01 00:00:00 | 2026-09-30 23:00:00 |
| 1 | 0 | 931711 | 8961 | 2017-09-01 00:00:00 | 2026-02-28 23:00:00 | 2026-04-01 00:00:00 | 2026-04-30 23:00:00 |
| 2 | 0 | 879272 | 9031 | 2017-09-01 00:00:00 | 2025-08-31 23:00:00 | 2025-10-01 00:00:00 | 2025-10-31 23:00:00 |
| 3 | 0 | 830229 | 10079 | 2017-09-01 00:00:00 | 2025-03-31 23:00:00 | 2025-05-01 00:00:00 | 2025-05-31 23:00:00 |
| 4 | 0 | 777987 | 8924 | 2017-09-01 00:00:00 | 2024-09-30 23:00:00 | 2024-11-01 00:00:00 | 2024-11-30 23:00:00 |
| 5 | 0 | 727880 | 10120 | 2017-09-01 00:00:00 | 2024-04-30 23:00:00 | 2024-06-01 00:00:00 | 2024-06-30 23:00:00 |
| 6 | 0 | 675888 | 9095 | 2017-09-01 00:00:00 | 2023-10-31 23:00:00 | 2023-12-01 00:00:00 | 2023-12-31 23:00:00 |
| 7 | 0 | 627408 | 9499 | 2017-09-01 00:00:00 | 2023-05-31 23:00:00 | 2023-07-01 00:00:00 | 2023-07-31 23:00:00 |
| 8 | 0 | 574344 | 8091 | 2017-09-01 00:00:00 | 2022-11-30 23:00:00 | 2023-01-01 00:00:00 | 2023-01-31 23:00:00 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows chicago_traffic_crashes`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Sep 2026 | 9641 | 0.981 | FATAL 0.1%, INCAPACITATING INJURY 1.5%, NO INDICATION OF INJURY 81.7%, NONINCAP… | FATAL 0.1%, INCAPACITATING INJURY 1.8%, NO INDICATION OF INJURY 84.8%, NONINCAP… | 0.022 | trafficway_type (0.02), first_crash_type (0.02), beat_of_occurrence (0.01) | 0 |
| 1 | Apr 2026 | 8961 | 0.933 | FATAL 0.1%, INCAPACITATING INJURY 1.2%, NO INDICATION OF INJURY 84.2%, NONINCAP… | FATAL 0.1%, INCAPACITATING INJURY 1.7%, NO INDICATION OF INJURY 84.7%, NONINCAP… | 0.02 | first_crash_type (0.02), trafficway_type (0.02), beat_of_occurrence (0.01) | 0.0008 |
| 2 | Oct 2025 | 9031 | 0.881 | FATAL 0.1%, INCAPACITATING INJURY 1.5%, NO INDICATION OF INJURY 82.6%, NONINCAP… | FATAL 0.1%, INCAPACITATING INJURY 1.8%, NO INDICATION OF INJURY 84.8%, NONINCAP… | 0.029 | trafficway_type (0.03), first_crash_type (0.02), street_name (0.01) | 0.0001 |
| 3 | May 2025 | 10079 | 0.832 | FATAL 0.1%, INCAPACITATING INJURY 1.1%, NO INDICATION OF INJURY 84.2%, NONINCAP… | FATAL 0.1%, INCAPACITATING INJURY 1.7%, NO INDICATION OF INJURY 85.6%, NONINCAP… | 0.03 | trafficway_type (0.03), first_crash_type (0.02), beat_of_occurrence (0.01) | 0.0002 |
| 4 | Nov 2024 | 8924 | 0.779 | FATAL 0.1%, INCAPACITATING INJURY 1.5%, NO INDICATION OF INJURY 84.4%, NONINCAP… | FATAL 0.1%, INCAPACITATING INJURY 1.9%, NO INDICATION OF INJURY 85.4%, NONINCAP… | 0.048 | trafficway_type (0.05), first_crash_type (0.01), beat_of_occurrence (0.01) | 0.0001 |
| 5 | Jun 2024 | 10120 | 0.729 | FATAL 0.1%, INCAPACITATING INJURY 1.6%, NO INDICATION OF INJURY 82.7%, NONINCAP… | FATAL 0.1%, INCAPACITATING INJURY 1.9%, NO INDICATION OF INJURY 85.1%, NONINCAP… | 0.058 | trafficway_type (0.06), first_crash_type (0.02), beat_of_occurrence (0.01) | 0.0001 |
| 6 | Dec 2023 | 9095 | 0.677 | FATAL 0.1%, INCAPACITATING INJURY 1.4%, NO INDICATION OF INJURY 84.7%, NONINCAP… | FATAL 0.1%, INCAPACITATING INJURY 1.9%, NO INDICATION OF INJURY 85.7%, NONINCAP… | 0.082 | trafficway_type (0.08), first_crash_type (0.02), street_name (0.01) | 0.0002 |
| 7 | Jul 2023 | 9499 | 0.629 | FATAL 0.1%, INCAPACITATING INJURY 2.0%, NO INDICATION OF INJURY 83.5%, NONINCAP… | FATAL 0.1%, INCAPACITATING INJURY 1.8%, NO INDICATION OF INJURY 85.2%, NONINCAP… | 0.062 | trafficway_type (0.06), first_crash_type (0.02), street_name (0.01) | 0.0001 |
| 8 | Jan 2023 | 8091 | 0.575 | FATAL 0.2%, INCAPACITATING INJURY 1.6%, NO INDICATION OF INJURY 86.4%, NONINCAP… | FATAL 0.1%, INCAPACITATING INJURY 1.7%, NO INDICATION OF INJURY 85.4%, NONINCAP… | 0.062 | trafficway_type (0.06), first_crash_type (0.03), street_name (0.01) | 0.0006 |

## Decisions

### 1. Keep all five police injury classes

Source classes remain distinct; missing labels are not interpreted as no injury. October 2026 is not a complete cohort.

| most_severe_injury | source | retained |
|---|---|---|
| FATAL | 1150 | 1086 |
| INCAPACITATING INJURY | 17898 | 16906 |
| NO INDICATION OF INJURY | 946094 | 845835 |
| NONINCAPACITATING INJURY | 89588 | 85063 |
| REPORTED, NOT EVIDENT | 52842 | 49227 |
|  | 2400 | 0 |

### 2. Filter measurable notification unavailability before each refit

Notification must precede refit and cannot precede its recorded event. It is eligibility metadata only and does not date the injury label; the one-month gap before each window (its rows counted here) stands in for later amendments.

| month start | gap month rows | prior rows | not yet notified | notification before event | eligible train pool | test rows |
|---|---|---|---|---|---|---|
| 2026-09-01 00:00:00 | 9529 | 978947 | 9 | 1 | 978937 | 9641 |
| 2026-04-01 00:00:00 | 8658 | 931730 | 18 | 1 | 931711 | 8961 |
| 2025-10-01 00:00:00 | 9029 | 879292 | 19 | 1 | 879272 | 9031 |
| 2025-05-01 00:00:00 | 8892 | 830255 | 25 | 1 | 830229 | 10079 |
| 2024-11-01 00:00:00 | 9866 | 778009 | 21 | 1 | 777987 | 8924 |
| 2024-06-01 00:00:00 | 10719 | 727912 | 31 | 1 | 727880 | 10120 |
| 2023-12-01 00:00:00 | 8755 | 675918 | 29 | 1 | 675888 | 9095 |
| 2023-07-01 00:00:00 | 9570 | 627446 | 37 | 1 | 627408 | 9499 |
| 2023-01-01 00:00:00 | 8916 | 574378 | 33 | 1 | 574344 | 8091 |

## Bundle checks

0 error(s), 0 warning(s), 3 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 397 exact duplicate row(s) (0.0% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)
- **info** `dataset_conflicting_duplicate_rows`: 49 row(s) (0.0%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)
- **info** `splits_rows_unused`: 9,539 row(s) (1.0%) appear in no train and no test set. (hint: Expected of a temporal split (the rows of a gap, history no window trains on, rows a filter keeps out of every training side); say why in `splits_comment`.)

## Data checks

### Feature summary

<details>
<summary>Show the table (16 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| workers_present_i | category | 996747 | 99.86 | 2 | Y, N |
| work_zone_type | category | 994851 | 99.67 | 3 | CONSTRUCTION, MAINTENANCE, UTILITY |
| work_zone_i | category | 993043 | 99.49 | 2 | Y, N |
| not_right_of_way_i | category | 953767 | 95.56 | 2 | Y, N |
| trafficway_type | category | 12894 | 1.29 | 18 | NOT DIVIDED, DIVIDED - W/MEDIAN (NOT RAISED), ONE-WAY, FOUR WAY, PARKING LOT, D… |
| first_crash_type | category | 0 | 0 | 18 | PARKED MOTOR VEHICLE, REAR END, SIDESWIPE SAME DIRECTION, TURNING, ANGLE, FIXED… |
| street_direction | category | 1 | 0 | 4 | W, S, N, E |
| street_name | category | 0 | 0 | 1627 | WESTERN AVE, PULASKI RD, CICERO AVE, ASHLAND AVE, HALSTED ST, KEDZIE AVE, MICHI… |
| beat_of_occurrence | category | 0 | 0 | 278 | 1834, 114, 813, 815, 1831, 833, 122, 2512, 834, 2413 |
| most_severe_injury | category | 0 | 0 | 5 | NO INDICATION OF INJURY, NONINCAPACITATING INJURY, REPORTED, NOT EVIDENT, INCAP… |
| crash_date | datetime64\[ns\] | 0 | 0 | 78540 | 2026-01-14 08:00:00, 2025-02-06 08:00:00, 2026-01-14 09:00:00, 2024-11-21 10:00… |
| latitude | float64 | 8215 | 0.82 | 342559 | 41.9762, 41.901, 41.7515, 41.7914, 41.7223, 41.7547, 41.8809, 41.8968, 41.9008,… |
| longitude | float64 | 8215 | 0.82 | 342552 | -87.9053, -87.6199, -87.586, -87.5801, -87.5853, -87.7414, -87.6176, -87.617, -… |
| posted_speed_limit | float64 | 0 | 0 | 46 | 30.0, 25.0, 35.0, 20.0, 15.0, 10.0, 40.0, 45.0, 0.0, 5.0 |
| street_no | float64 | 0 | 0 | 11987 | 1600.0, 800.0, 100.0, 200.0, 2400.0, 4700.0, 1200.0, 7900.0, 300.0, 500.0 |
| num_units | float64 | 0 | 0 | 17 | 2.0, 3.0, 1.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 |

</details>

### Target distribution

| most_severe_injury | count | pct |
|---|---|---|
| NO INDICATION OF INJURY | 845835 | 84.74 |
| NONINCAPACITATING INJURY | 85063 | 8.52 |
| REPORTED, NOT EVIDENT | 49227 | 4.93 |
| INCAPACITATING INJURY | 16906 | 1.69 |
| FATAL | 1086 | 0.11 |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| posted_speed_limit | 998117 | 28.4714 | 5.83206 | 0 | 70 |
| street_no | 998117 | 3699.18 | 2838.16 | 0 | 13799 |
| num_units | 998117 | 2.03779 | 0.45608 | 1 | 18 |
| latitude | 989902 | 41.8583 | 0.0864392 | 41.6446 | 42.0228 |
| longitude | 989902 | -87.6797 | 0.0592767 | -87.9397 | -87.5246 |

### Categorical features

<details>
<summary>Show the table (48 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| beat_of_occurrence | 1 | 1834 | 11616 | 1.16 |
| beat_of_occurrence | 2 | 114 | 9976 | 1 |
| beat_of_occurrence | 3 | 813 | 9959 | 1 |
| beat_of_occurrence | 4 | 815 | 9285 | 0.93 |
| beat_of_occurrence | 5 | 1831 | 8754 | 0.88 |
| crash_date | 1 | 2026-01-14 08:00:00 | 226 | 0.02 |
| crash_date | 2 | 2025-02-06 08:00:00 | 141 | 0.01 |
| crash_date | 3 | 2026-01-14 09:00:00 | 130 | 0.01 |
| crash_date | 4 | 2024-11-21 10:00:00 | 117 | 0.01 |
| crash_date | 5 | 2026-01-14 07:00:00 | 115 | 0.01 |
| first_crash_type | 1 | PARKED MOTOR VEHICLE | 229946 | 23.04 |
| first_crash_type | 2 | REAR END | 210498 | 21.09 |
| first_crash_type | 3 | SIDESWIPE SAME DIRECTION | 154284 | 15.46 |
| first_crash_type | 4 | TURNING | 146424 | 14.67 |
| first_crash_type | 5 | ANGLE | 108781 | 10.9 |
| most_severe_injury | 1 | NO INDICATION OF INJURY | 845835 | 84.74 |
| most_severe_injury | 2 | NONINCAPACITATING INJURY | 85063 | 8.52 |
| most_severe_injury | 3 | REPORTED, NOT EVIDENT | 49227 | 4.93 |
| most_severe_injury | 4 | INCAPACITATING INJURY | 16906 | 1.69 |
| most_severe_injury | 5 | FATAL | 1086 | 0.11 |
| not_right_of_way_i | 1 | &lt;NA> | 953767 | 95.56 |
| not_right_of_way_i | 2 | Y | 40183 | 4.03 |
| not_right_of_way_i | 3 | N | 4167 | 0.42 |
| street_direction | 1 | W | 361305 | 36.2 |
| street_direction | 2 | S | 329453 | 33.01 |
| street_direction | 3 | N | 241412 | 24.19 |
| street_direction | 4 | E | 65946 | 6.61 |
| street_direction | 5 | &lt;NA> | 1 | 0 |
| street_name | 1 | WESTERN AVE | 27451 | 2.75 |
| street_name | 2 | PULASKI RD | 23908 | 2.4 |
| street_name | 3 | CICERO AVE | 22474 | 2.25 |
| street_name | 4 | ASHLAND AVE | 21804 | 2.18 |
| street_name | 5 | HALSTED ST | 19120 | 1.92 |
| trafficway_type | 1 | NOT DIVIDED | 423283 | 42.41 |
| trafficway_type | 2 | DIVIDED - W/MEDIAN (NOT RAISED) | 150185 | 15.05 |
| trafficway_type | 3 | ONE-WAY | 122515 | 12.27 |
| trafficway_type | 4 | FOUR WAY | 86627 | 8.68 |
| trafficway_type | 5 | PARKING LOT | 65473 | 6.56 |
| work_zone_i | 1 | &lt;NA> | 993043 | 99.49 |
| work_zone_i | 2 | Y | 3810 | 0.38 |
| work_zone_i | 3 | N | 1264 | 0.13 |
| work_zone_type | 1 | &lt;NA> | 994851 | 99.67 |
| work_zone_type | 2 | CONSTRUCTION | 2608 | 0.26 |
| work_zone_type | 3 | MAINTENANCE | 414 | 0.04 |
| work_zone_type | 4 | UTILITY | 244 | 0.02 |
| workers_present_i | 1 | &lt;NA> | 996747 | 99.86 |
| workers_present_i | 2 | Y | 1211 | 0.12 |
| workers_present_i | 3 | N | 159 | 0.02 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a217fd-5b06-7d55-841f-8e0d110f9174 |
| checksum | v2:e54f9570c1debb30e834661f8ca7a7160541103afc3b536ec130ed513dd7cc71 |
| built_at | 2026-11-26T13:13:40+00:00 |
| path | chicago_traffic_crashes/01a217fd-5b06-7d55-841f-8e0d110f9174 |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
