---
report_format: data-foundry-report-v2
unique_name: nhanes_dxa_body_fat
container_format: 2
checksum: v2:41aaa5545238feee0cf7f2eb85bd0e7a54dd997c7a4723f8526e300e994f60b5
build: null
build_stale: false
raw_files:
  DXX.xpt: 9567c94c4a2efd3bb67817f051bec4e778c648c9a2dd222a894fe0ca78598d37
  DXX_B.xpt: 6eeb2dabff1fc4a33df2dfe2b46e86eb6f0986319f238f1cb8066e7d695852f6
  DXX_C.xpt: 8840fcaa518d7ee0c3c64e826dfb512cf0ac9be5cd00b1895a9782cb885c91df
  DXX_D.xpt: f5122f3660a0a90601e3f6d865a82091a80db099dd8db4efb861c6cb5310710b
  DXX_G.xpt: df4a9741ef55866ca039b0a01f55ab4d3dd55f83f4ee845ca03e8bfca9a65099
  DXX_H.xpt: 792ebf3791156367832a01be0c96286ef8da1f540a1d674077f5af12951e99e5
  DXX_I.xpt: 56623a1b1c790e43d2c3d9792d30418de8553db53b55ef5e38ab2d00a8e983e8
  DXX_J.xpt: de16420ff3f978f72dbcc6a83c64de041440f29ad1f516f5e1cc5476af994ff1
  BMX.xpt: 6b9bc4d998c0004fc42b213cc7f5bf347df937707f46d6d25fab926723a60500
  BMX_B.xpt: 55715d4387960f88e48a2adf44da0b270a83290b1edf7c8e4ecc0eb2c29c59cf
  BMX_C.xpt: b3d3e431b5964ea8b5807035044322fcf32f3878d814d4a844204e51c793f090
  BMX_D.xpt: a52909be94cf825ba8a65477a9528603576fd5fbf3abadd72549a3f15c88566e
  BMX_G.xpt: 4814bfc3047ed400b9d43d285f8c3ea7c940ac6489404a9b699579715d158ec3
  BMX_H.xpt: fd5e9fc6e6aab0a4aee6e699f51497bbc9b62101f7f43aee924c473e38fd9442
  BMX_I.xpt: d31da84e14212b4e58e8340598a5b8e2144fac83333563e966eb1b332e4141d6
  BMX_J.xpt: 8d675e42d8826ac98714b2c3dd4c5138a5e353fb4424f7eff5e6db4a01ce838a
  DEMO.xpt: a17bd1ebfd6007b8dc93f16259cb090678eb6c467a39363b7e932bba15febf89
  DEMO_B.xpt: 6458dc2307cee244ab6ba26f70ec78c7b842ffc68e668bc43f0ab6b9737937d9
  DEMO_C.xpt: 2a2fdb88263337bfa06f0516bfb419631595f0a0ee88fb96069bed13d1857c6f
  DEMO_D.xpt: bf9cc79cce501b2fbe5aa8d5b403b618548d02d4aefeb528335cdd9f4c40a3af
  DEMO_G.xpt: eaf0525d1952626885af3e935415a1f66ad62c18698080e7354789c125af252d
  DEMO_H.xpt: f8f0cbb3085a323d4cde22349b164878fea1e64dbc404e65b5815c7816b547d7
  DEMO_I.xpt: c9297c6c37ae8f78f29be9568fa2a03cf3b112616a39afee04030fc775a66a0d
  DEMO_J.xpt: c0b46e0345ea19404928656277c8b0d10b0cca348a9b2fe4fc3c67e8b7ee73ec
data:
  n_rows: 39601
  n_features: 11
  dtypes:
    category: 2
    float64: 9
    int64: 1
  n_test_dataset_rows: null
task:
  target: percent_body_fat
  problem_type: regression
  metric: rmse
  metric_origin: fallback
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: survey_cycle
  time_unit: years
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 4
  n_folds: 1
  random_state: 4267
  time_horizon: 2
  time_horizon_unit: years
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 21768
    max: 35943
  n_test:
    min: 3658
    max: 5056
bundle_checks:
  ok: true
  errors: []
  warnings:
  - task_time_on_few_unique
  infos:
  - dataset_conflicting_duplicate_rows
  - meta_time_horizon_unit
  accepted:
    splits_below_target: 'Four of the nine windows an IID split of 39,601 people would
      get (SPLIT-33): the release holds eight cycles, and a fifth window, 2005-2006,
      would train on 42.7% of the people, below the half-the-data floor (splits comment).'
decisions: []
---

# nhanes_dxa_body_fat

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `percent_body_fat`, scored with `rmse` on temporal splits by `survey_cycle` (one step is a year). 39,601 rows and 11 features. Source: GOV Website (2008).

Not built yet. The current definition gives checksum `v2:41aaa5545238feee0cf7f2eb85bd0e7a54dd997c7a4723f8526e300e994f60b5`.

## In brief

**Question.** What is a person's whole-body fat percentage, as a DXA scan measures it, judging from sex, age, ethnicity and a tape and a scale?

**Use case.** A clinician, a screening programme or a gym estimates body fat, and so body-fat obesity, from weight, height and a few tape measures instead of a DXA scan, as the relative fat mass equation built on these files does (Woolcott and Bergman 2018). The tested population is aged 8-59: no one older was scanned after 2010.

**One row.** One person aged 8 or over examined by the US National Health and Nutrition Examination Survey in one of the eight two-year cycles with whole-body DXA (1999-2006, 2011-2018), whose whole-body percent fat CDC measured, not imputed.

**Predicted.** The whole-body fat percentage of the DXA scan taken at the same examination.

**Known at prediction time.** The survey cycle, sex, age, race and ethnicity, weight, height, body-mass index, waist and upper-arm circumference, and upper-leg and upper-arm length.

**What the test data stands for.** Each of the four newest cycles (2011-2012, 2013-2014, 2015-2016, 2017-2018) is the test data once, with every earlier cycle for training, so the test people stand for people met after the equation was fitted.

**Our changes to the source.** We keep only measured scans, not CDC's imputed ones, and only the measures taken in every cycle (skinfolds, thigh, calf, sagittal diameter and hip were each taken in some cycles only); from 2011 non-Hispanic Asians get their own ethnicity level.

> **Use case fit: direct (the rows, features and split mirror the use case).** The features are what a tape, a scale and a short interview give, and the label is the scan they replace. The scanner and its software changed between 1999-2006 and 2011-2018, and many of the heaviest people have no usable scan, so the sample thins the top of the range.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/nhanes_dxa_body_fat.md`](../../../../curation/records/nhanes_dxa_body_fat.md)
- The original source: <https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx>
- A part of the data (NHANES Body Measures (BMX), the same eight cycles): <https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/BMX_J.htm>
- A part of the data (NHANES Demographics (DEMO), the same eight cycles): <https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DEMO_J.htm>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/nhanes_dxa_body_fat/`. To get them:

```text
We download three files per survey cycle from CDC: the whole-body DXA file, the body measures and the
demographics (8 cycles, 24 SAS transport files, 180 MB).

mkdir -p local-data-warehouse/nhanes_dxa_body_fat && cd local-data-warehouse/nhanes_dxa_body_fat
for ys in 1999: 2001:_B 2003:_C 2005:_D 2011:_G 2013:_H 2015:_I 2017:_J; do
  y=${ys%%:*}; s=${ys#*:}
  for f in DXX DEMO BMX; do
    wget "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/$y/DataFiles/$f$s.xpt"
  done
done
```

<details>
<summary>The 24 raw files the sources name</summary>

| file | source | bytes | rows | sha256 (start) |
|---|---|---|---|---|
| `DXX.xpt` | GOV Website publication | 24,737,440 |  | `9567c94c4a2efd3b` |
| `DXX_B.xpt` | GOV Website publication | 32,695,200 |  | `6eeb2dabff1fc4a3` |
| `DXX_C.xpt` | GOV Website publication | 30,371,680 |  | `8840fcaa518d7ee0` |
| `DXX_D.xpt` | GOV Website publication | 29,517,840 |  | `f5122f3660a0a906` |
| `DXX_G.xpt` | GOV Website publication | 4,248,640 |  | `df4a9741ef55866c` |
| `DXX_H.xpt` | GOV Website publication | 4,502,320 |  | `792ebf3791156367` |
| `DXX_I.xpt` | GOV Website publication | 4,314,080 |  | `56623a1b1c790e43` |
| `DXX_J.xpt` | GOV Website publication | 3,818,640 |  | `de16420ff3f978f7` |
| `BMX.xpt` | NHANES Body Measures (BMX), the same eight cycles | 2,827,840 |  | `6b9bc4d998c0004f` |
| `BMX_B.xpt` | NHANES Body Measures (BMX), the same eight cycles | 2,183,680 |  | `55715d4387960f88` |
| `BMX_C.xpt` | NHANES Body Measures (BMX), the same eight cycles | 2,551,120 |  | `b3d3e431b5964ea8` |
| `BMX_D.xpt` | NHANES Body Measures (BMX), the same eight cycles | 2,153,760 |  | `a52909be94cf825b` |
| `BMX_G.xpt` | NHANES Body Measures (BMX), the same eight cycles | 1,946,720 |  | `4814bfc3047ed400` |
| `BMX_H.xpt` | NHANES Body Measures (BMX), the same eight cycles | 2,045,520 |  | `fd5e9fc6e6aab0a4` |
| `BMX_I.xpt` | NHANES Body Measures (BMX), the same eight cycles | 1,989,600 |  | `d31da84e14212b4e` |
| `BMX_J.xpt` | NHANES Body Measures (BMX), the same eight cycles | 1,466,000 |  | `8d675e42d8826ac9` |
| `DEMO.xpt` | NHANES Demographics (DEMO), the same eight cycles | 11,500,560 |  | `a17bd1ebfd6007b8` |
| `DEMO_B.xpt` | NHANES Demographics (DEMO), the same eight cycles | 3,273,520 |  | `6458dc2307cee244` |
| `DEMO_C.xpt` | NHANES Demographics (DEMO), the same eight cycles | 3,569,840 |  | `2a2fdb88263337bf` |
| `DEMO_D.xpt` | NHANES Demographics (DEMO), the same eight cycles | 3,566,560 |  | `bf9cc79cce501b2f` |
| `DEMO_G.xpt` | NHANES Demographics (DEMO), the same eight cycles | 3,753,760 |  | `eaf0525d19526268` |
| `DEMO_H.xpt` | NHANES Demographics (DEMO), the same eight cycles | 3,833,200 |  | `f8f0cbb3085a323d` |
| `DEMO_I.xpt` | NHANES Demographics (DEMO), the same eight cycles | 3,756,480 |  | `c9297c6c37ae8f78` |
| `DEMO_J.xpt` | NHANES Demographics (DEMO), the same eight cycles | 3,412,720 |  | `c0b46e0345ea1940` |

</details>

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/nhanes_dxa_body_fat   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/nhanes_dxa_body_fat   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | GOV Website: https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx |
| year | 2008 |
| domain | medical & healthcare |
| license | Public domain (US federal government data); the NCHS data user agreement applies |
| data_tags | Non-IID, Temporal |
| reference | nchs2008nhanesdxa |
| part: NHANES Body Measures (BMX), the same eight cycles | GOV Website: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/BMX_J.htm; license: Public domain (US federal government data); the NCHS data user agreement applies |
| part: NHANES Demographics (DEMO), the same eight cycles | GOV Website: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DEMO_J.htm; license: Public domain (US federal government data); the NCHS data user agreement applies |
| rows x columns | 39,601 x 12 |
| task.target | percent_body_fat |
| task.problem_type | regression |
| task.metric | rmse |
| task.split_regime | temporal_non_iid |
| task.time_on | survey_cycle |
| task.time_unit | years |

**Metric**

| field | value |
|---|---|
| name | `rmse` (standard; takes value; lower is better) |
| origin | fallback: the default for the problem type: the source defines no metric the task would use in practice |
| definition | sqrt(mean((y - p)^2)) |
| reason | NHANES defines no prediction task. The relative fat mass paper on these files (Woolcott and Bergman 2018, Sci Rep 8:10980) chose its equation by several criteria together (R^2, RMSE, AIC, bias, accuracy, precision and simplicity) and Lee et al. 2017 (Br J Nutr 118:858) report R^2 and the standard error of estimate, so no source fixes one metric; RMSE in percent-fat points, which both report, is the regression fallback. The paper's RMSE was survey-weighted and pooled over the five imputations; ours is unweighted on measured scans, because a clinician scores the patient in front of them, not the US population. |

<details>
<summary>Feature types: 2 categorical, 0 string, 0 datetime</summary>

- categorical (2): `sex`, `race_ethnicity`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{nchs2008nhanesdxa,
  author       = {{Centers for Disease Control and Prevention, National Center for Health Statistics}},
  title        = {{National Health and Nutrition Examination Survey: Dual-Energy X-ray Absorptiometry,
                  Whole Body (DXX), 1999-2006 and 2011-2018}},
  year         = {2008},
  howpublished = {\url{https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx}},
  note         = {First published January 2008 (1999-2000 file); cycles 2011-2018 published March 2020}
}
```

</details>

## Sample rows

The first 5 of 39,601 rows of the final frame (the oldest rows: the frame is sorted by `survey_cycle`). Cells are cut at 40 characters.

| percent_body_fat | survey_cycle | sex | age_years | race_ethnicity | weight_kg | standing_height_cm | bmi | upper_leg_length_cm | upper_arm_length_cm | arm_circumference_cm | waist_circumference_cm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 27 | 1999 | Male | 54 | Non-Hispanic White | 80.9 | 170.1 | 27.96 | 40.7 | 37.6 | 33.4 | 98.6 |
| 21.2 | 1999 | Male | 8 | Non-Hispanic Black | 29.8 | 133 | 16.85 | 31.4 | 27.8 | 21.1 | 56.1 |
| 32.4 | 1999 | Female | 18 | Mexican American | 52.5 | 158.9 | 20.79 | 36.4 | 34 | 26 | 69.5 |
| 15.1 | 1999 | Male | 26 | Non-Hispanic White | 64.8 | 182.4 | 19.48 | 42.4 | 36.5 | 30 | 75.4 |
| 25.7 | 1999 | Male | 51 | Mexican American | 66.8 | 166.7 | 24.04 | 40.9 | 35.5 | 30.6 | 85.7 |

## Curation notes

We start with the NHANES whole-body DXA files (DXX), joined on the participant number `SEQN` to the body
measures (BMX) and demographics (DEMO) of the same cycle, for the eight cycles with DXA (1999-2006, 2011-2018).

- Prediction point: the examination, once weight, height and the tape measures are taken and before (or
  instead of) a DXA scan. Every feature is recorded at that examination; the scan is taken the same day.
- Target: `DXDTOPF`, whole-body percent fat, renamed `percent_body_fat`. Every other DXA column (regional fat,
  lean and bone mass, total fat mass) is an outcome of the same scan and is never read.
- Measured whole-body values only, by the rule each era's release allows. 1999-2006: CDC filled missing and
  invalid scans by multiple imputation (five records per person, `_MULT_`): "Imputed values should not be
  treated as measured variables" (DXX_D). We keep the first record of people whose whole-body flag (`DXITOT`,
  `DXITOTST` in 2005-2006) is 0 and whose percent fat is the same in all five records, as DXX_D says a fully
  measured person's records are. The second test drops 90 people whose flag reads 0 but whose percent fat
  varies across the records: 80 in 2003-2004 (by up to 4.6 points) and 10 in 2005-2006, where the bone flag
  marks an imputation (by 0.1 point). 2011-2018 has no imputation: we keep completed scans (`DXAEXSTS` 1) with
  a percent fat. CDC publishes the whole-body value there also when one region of the scan is invalid ("If any
  region was coded as invalid all bone and soft tissue measurements for that region were set to missing",
  DXX_J), so 893 kept scans of 2011-2018 have an invalid region, a kind of scan the 1999-2006 rule drops
  (Selection Bias below). This keeps 39,601 people: 21,768 in 1999-2006 (5,491 dropped as imputed) and 17,833
  in 2011-2018 (4,671, 6,425, 5,797, 4,875, 4,521, 5,056, 4,598 and 3,658 per cycle). `SEQN` is unique.
- Selection Bias: pregnant women were not scanned, nor people over the table limit (300 lb in 1999-2006, 450 lb
  and 6 ft 5 in later). The heaviest people often have no usable scan, and the two eras do not drop the same
  scans:
  - 1999-2006: every scan with an invalid region was imputed, and imputed scans are dropped here; the heaviest
    people had most of them (76% of people with BMI 40 or more have an imputed scan, 13% below BMI 25).
  - 2011-2018: scans with an invalid region keep a whole-body value and stay: 893 rows (140, 148, 241 and 364
    per cycle, 10% of the 2017-2018 cycle), median BMI 33.6 against 24.9 for fully valid scans; 149 of the
    2017-2018 ones have the trunk coded "excessive x-ray noise due to morbid obesity".
  - 2011-2018: completed scans without a whole-body value grow from 4.8% of 2011-2012 to 15.6% of 2017-2018,
    and these people are heavier (median BMI 29.9 against 25.7). In 2017-2018 only 50% of examined adults aged
    20-59 with BMI 40 or more have a usable scan, against 75% of those below BMI 30.
  CDC warns that "use of only the measured variables could lead to biased results" for population estimates;
  for an equation it means fewer very heavy people than a clinic meets.
- Features: the measures taken in every cycle (weight, height, BMI, upper-leg and upper-arm length, upper-arm and
  waist circumference), sex, age in years, race and ethnicity and the cycle's first year. BMI is weight over
  height squared as CDC computes it, kept as released. Dropped because they were taken in some cycles only:
  thigh and calf circumference and the triceps and subscapular skinfolds (1999-2006), the sagittal abdominal
  diameter (2011-2016) and hip circumference (2017-2018); the skinfolds and the sagittal diameter need
  calipers, not a tape. The exam's six-month period (`RIDEXMON`) is not a measurement of the person; the
  survey weights describe the sample design and are not read.
- Race and ethnicity: `RIDRETH1`, the coding of every cycle, plus a "Non-Hispanic Asian" level from `RIDRETH3`
  for 2011-2018, when NHANES began to oversample Asian Americans. `RIDRETH1` counts them in "Other race", which
  holds 3-5% of the 1999-2006 rows and 16-23% of the 2011-2018 rows, two thirds or more of them Asian. Asians
  of 1999-2006 stay in "Other race": those cycles do not code them apart. Asians carry more fat at a given
  BMI; with the level, the mean error for Asian people in the 2017-2018 test window falls from +0.98 to +0.58
  points (measured, LightGBM).
- Missing measures stay missing and the rows stay (0.3% to 0.9% per measure), as at an examination where one
  measure could not be taken.
- Duplicates: no row repeats; a few rows share every feature with another person and differ in percent fat,
  natural for different people with the same rounded measures.
- Note: the 5% shift of lean to fat mass is in both eras (DXX_D for the QDR-4500A data; DXX_G: "The NHANES BCA
  option was enabled ... this option adds 5% of lean mass to the fat mass"), so it is no break between them.
  The break is the scanner and software: a Hologic QDR-4500A in 1999-2006 (software 8.26, then Discovery 12.4
  from 2005), Hologic Discovery A with Apex in 2011-2018.
- Ages: DXA was offered at 8-85 in 1999-2004, 8-69 in 2005-2006 and 8-59 in 2011-2018 (the documentation of each
  cycle), so the test cycles hold ages 8-59 and the older people are in training only. Children and
  adolescents are kept: the paediatric relative fat mass was built on these files (Woolcott and Bergman 2019).
- Note: this task replaces body_density_prediction's (252 men of 1985, body density by underwater weighing) with
  another reference method for the same use case; the two scores are not comparable.
- Metric: RMSE in percent-fat points, unweighted (fallback; the metric's reason says where we looked and why
  the survey weights are not used).

## Splits

Leaf L-ORDER.windows: a body-fat equation is fitted on the people examined so far and used on people met later
(the relative fat mass was developed on NHANES 1999-2004 and validated on 2005-2006, Woolcott and Bergman 2018),
and the survey cycle orders the people. Each test window is one two-year cycle; the windows are the four newest
cycles, newest first: 2017-2018 (3,658 people), 2015-2016 (4,598), 2013-2014 (5,056) and 2011-2012 (4,521),
training on every earlier cycle: 35,943, 31,345, 26,289 and 21,768 people (90.8%, 79.2%, 66.4% and 55.0%).
Every window tests on the Discovery A scanner of 2011-2018. The first three train on both eras; the 2011-2012
window trains on the old scanner's cycles alone and so tests across the change of scanner and of sampling (the
largest feature drift of the candidate windows, by the window statistics), a change in data collection that a
deployed equation meets; there the "Non-Hispanic Asian" level (13.7% of the test people) has no training row,
since 1999-2006 do not code it. Four windows against the nine a random split of 39,601 people would get: only
eight cycles exist, and a fifth window, 2005-2006, would train on 42.7% of the people, below the floor of half
the data. No gap: the scan and the measures are taken at the same examination, so a person's label exists when
they are examined. The 2011-2018 values as released are CDC's re-analysis with the Apex software (every
2011-2018 DXX file: "First Published: March 2020"); the gap rests on the same-day scan, not on release dates.
The test cycles hold ages 8-59 only (DXA eligibility from 2011); the 60-85-year-olds of 1999-2006 train only.

4 repeat(s) x 1 fold(s) with seed 4267; train 21,768 to 35,943 rows, test 3,658 to 5,056 rows. Prediction horizon: 2 years.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 35943 | 3658 | 1999 | 2015 | 2017 | 2017 |
| 1 | 0 | 31345 | 4598 | 1999 | 2013 | 2015 | 2015 |
| 2 | 0 | 26289 | 5056 | 1999 | 2011 | 2013 | 2013 |
| 3 | 0 | 21768 | 4521 | 1999 | 2005 | 2011 | 2011 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows nhanes_dxa_body_fat`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | 2017 - 2017 (years) | 3658 | 0.908 | mean 32.32, median 32.1, p10 20.3, p90 43.7 | mean 31.44, median 31.1, p10 19.4, p90 43.5 | 0.785 | age_years (0.79), race_ethnicity (0.19), bmi (0.03) | 0 |
| 1 | 2015 - 2015 (years) | 4598 | 0.792 | mean 31.85, median 31.6, p10 20.1, p90 43.4 | mean 31.42, median 31.1, p10 19.4, p90 43.7 | 0.784 | age_years (0.78), race_ethnicity (0.19), upper_leg_length_cm (0.08) | 0 |
| 2 | 2013 - 2013 (years) | 5056 | 0.664 | mean 32.07, median 31.8, p10 20.8, p90 43.6 | mean 31.26, median 30.9, p10 19.2, p90 43.5 | 0.766 | age_years (0.77), race_ethnicity (0.21), upper_leg_length_cm (0.04) | 0 |
| 3 | 2011 - 2011 (years) | 4521 | 0.55 | mean 31.26, median 30.8, p10 19.6, p90 43.2 | mean 31.29, median 30.9, p10 19.1, p90 43.6 | 1.159 | race_ethnicity (1.16), age_years (0.83), upper_leg_length_cm (0.10) | 0.1369 |

## Bundle checks

0 error(s), 1 warning(s), 2 info (28 checks run, plus the dataset's own checks).

- **warning** `task_time_on_few_unique`: `time_on='survey_cycle'` has only 8 distinct time points. (hint: Consumers derive inner validation folds by cutting the time axis into intervals; too few time points makes that degenerate.)
- **info** `dataset_conflicting_duplicate_rows`: 3 row(s) (0.0%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)
- **info** `meta_time_horizon_unit`: `time_horizon_unit='years'` implies calendar time, but `time_on='survey_cycle'` has dtype int64, so the horizon cannot be cross-checked. (hint: Fine when the numeric values themselves are calendar units (e.g. a year column); otherwise use `time_horizon_unit='steps'` for a plain numeric time index.)

Accepted on purpose:

- `splits_below_target`: Four of the nine windows an IID split of 39,601 people would get (SPLIT-33): the release holds eight cycles, and a fifth window, 2005-2006, would train on 42.7% of the people, below the half-the-data floor (splits comment).

## Data checks

### Feature summary

<details>
<summary>Show the table (12 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| sex | category | 0 | 0 | 2 | Male, Female |
| race_ethnicity | category | 0 | 0 | 6 | Non-Hispanic White, Non-Hispanic Black, Mexican American, Other Hispanic, Non-H… |
| upper_leg_length_cm | float64 | 340 | 0.86 | 281 | 40.0, 39.0, 38.0, 41.0, 42.0, 37.0, 39.5, 40.5, 41.5, 43.0 |
| waist_circumference_cm | float64 | 322 | 0.81 | 1025 | 74.0, 97.0, 92.0, 94.0, 86.0, 91.0, 77.0, 76.0, 81.0, 78.0 |
| arm_circumference_cm | float64 | 202 | 0.51 | 379 | 32.0, 31.0, 30.0, 33.0, 29.0, 28.0, 34.0, 29.5, 26.0, 27.0 |
| upper_arm_length_cm | float64 | 198 | 0.5 | 238 | 36.0, 38.0, 37.0, 35.0, 39.0, 34.0, 36.5, 40.0, 35.5, 37.5 |
| bmi | float64 | 182 | 0.46 | 3142 | 22.6, 24.5, 21.1, 23.7, 21.5, 24.6, 21.3, 23.8, 22.0, 26.2 |
| standing_height_cm | float64 | 161 | 0.41 | 781 | 163.0, 163.6, 165.3, 161.4, 161.7, 162.8, 163.3, 162.0, 166.9, 166.5 |
| weight_kg | float64 | 115 | 0.29 | 1491 | 62.8, 69.4, 71.4, 65.3, 61.3, 63.1, 63.8, 67.3, 63.5, 71.6 |
| age_years | float64 | 0 | 0 | 78 | 12.0, 16.0, 13.0, 14.0, 18.0, 15.0, 8.0, 9.0, 19.0, 17.0 |
| percent_body_fat | float64 | 0 | 0 | 434 | 27.3, 27.9, 29.1, 28.3, 30.9, 30.8, 31.3, 30.3, 26.1, 32.1 |
| survey_cycle | int64 | 0 | 0 | 8 | 2001, 2003, 2013, 2005, 1999, 2015, 2011, 2017 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0.046 | -0.539 | 78.064 | 0.091 | log | 362088 | 2.57374e+08 | exponential |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| survey_cycle | 39601 | 2007.33 | 6.26176 | 1999 | 2017 |
| age_years | 39601 | 31.5166 | 19.4421 | 8 | 85 |
| weight_kg | 39486 | 70.0752 | 22.2338 | 16.9 | 188.5 |
| standing_height_cm | 39440 | 163.505 | 13.2001 | 105.5 | 195.1 |
| bmi | 39419 | 25.7506 | 6.48177 | 12.04 | 69 |
| upper_leg_length_cm | 39261 | 39.2396 | 4.21799 | 23.6 | 55 |
| upper_arm_length_cm | 39403 | 35.9581 | 3.57967 | 21 | 47.5 |
| arm_circumference_cm | 39399 | 30.3948 | 5.76607 | 13.8 | 57 |
| waist_circumference_cm | 39279 | 88.2062 | 17.4526 | 32 | 176 |
| percent_body_fat | 39601 | 31.5448 | 8.83539 | 11.5 | 56.2 |

### Categorical features

| column | rank | value | count | pct |
|---|---|---|---|---|
| race_ethnicity | 1 | Non-Hispanic White | 14296 | 36.1 |
| race_ethnicity | 2 | Non-Hispanic Black | 9247 | 23.35 |
| race_ethnicity | 3 | Mexican American | 9164 | 23.14 |
| race_ethnicity | 4 | Other Hispanic | 2781 | 7.02 |
| race_ethnicity | 5 | Non-Hispanic Asian | 2335 | 5.9 |
| sex | 1 | Male | 20775 | 52.46 |
| sex | 2 | Female | 18826 | 47.54 |

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
