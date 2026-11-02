---
report_format: data-foundry-report-v2
unique_name: allstate_claim_prediction_challenge_1m
container_format: 2
checksum: v2:3d40dd1d79838a3330ee56d59821cf4566a4de512087be674fc0dcf5f1b02958
build: null
build_stale: false
data:
  n_rows: 1500000
  n_features: 28
  dtypes:
    category: 14
    float64: 13
    int64: 3
  n_test_dataset_rows: null
task:
  target: log1p_claim_amount
  problem_type: regression
  metric: normalized_gini
  metric_origin: source
  scoring_columns: null
  split_regime: grouped_non_iid
  stratify_on: null
  time_on: null
  group_on: Household_ID
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 609658
    test_groups_per_fold:
      min: 203143
      max: 203219
splits:
  n_repeats: 1
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 999818
    max: 1000000
  n_test:
    min: 499760
    max: 500000
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  - dataset_conflicting_duplicate_rows
  - groups_not_clustered
  accepted:
    splits_rows_never_tested: The v2 protocol caps each test fold at 500k rows; the
      folds by household overshoot by whole households, so 240 of the 1.5M rows are
      trimmed from a test fold (2026-11-01).
    groups_labels_constant: The label is one per vehicle-year and claims are rare
      (0.72%), so 97.8% of the households with two or more rows have a single label;
      9,475 of 429,370 have several (2026-11-01).
    task_target_value_dominant: 'A zero-inflated target, not a cap or a placeholder:
      0 is a vehicle-year without a bodily-injury claim, 99.28% of the shipped rows
      (see the curation notes; 2026-11-01).'
decisions:
- Grouped by household, not by year
- The 2007 rows are dropped
- Missing values stay
---

# allstate_claim_prediction_challenge_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `log1p_claim_amount`, scored with `normalized_gini` on grouped splits by `Household_ID`. 1,500,000 rows and 28 features. Source: Kaggle (2011).

Not built yet. The current definition gives checksum `v2:3d40dd1d79838a3330ee56d59821cf4566a4de512087be674fc0dcf5f1b02958`.

## In brief

**Question.** How much will an insured vehicle cost Allstate in bodily-injury liability claims over a calendar year, on the scale Allstate adjusted the amounts to, from the vehicle's characteristics?

**Use case.** For example, Allstate rating a vehicle for bodily-injury liability cover when a policy year starts: the vehicle's expected claim cost ranks its risk and sets the vehicle part of the premium. The competition names the target and the features, not the decision.

**One row.** One vehicle insured by Allstate in one calendar year, 2005 or 2006 (8.5 million vehicle-years of 3.4 million households in the competition's labelled file once 2007 is dropped, of which whole households holding 1.5 million vehicle-years are sampled).

**Predicted.** The vehicle's bodily-injury liability claim payments in that year, adjusted by Allstate to remove known non-vehicle effects by a rule it did not disclose, so in no currency: 0 for 99.27% of the vehicle-years. Shipped as log1p, scored on the amount.

**Known at prediction time.** The calendar year, the vehicle's model year and blinded make, model and submodel, 18 anonymised vehicle characteristics, and 5 anonymised characteristics of the policy.

**What the test data stands for.** All vehicle-years of a household stay on one side, so the test data stands for households not seen in training, from the same two years; the competition scored 2008 and 2009, whose claims were never published.

**Our changes to the source.** We dropped the 2007 rows, whose large claims look unsettled, and one exact copy of a row; sampled whole households down to the row budget; dropped the row number, the vehicle's number within the household and three vehicle columns that behave like random draws (Cat10 to Cat12); and coded the source's missing values as missing.

> **Use case fit: approximate (a stand-in with a known gap).** Vehicle and policy attributes known at pricing, and the vehicle's own claims. But the amounts' adjustment is undisclosed and no exposure is published. Held-out households of the same years stand in for next year's book, so known households (53% in the competition's test file), their claim history and unseen vehicle series go untested; 73% of the rows have a missing value, which the application never has.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`REVIEW.md`](REVIEW.md) | The open questions for the curator, removed once they are settled. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/allstate_claim_prediction_challenge.md`](../../../../curation/records/allstate_claim_prediction_challenge.md)
- The original source: <https://www.kaggle.com/competitions/ClaimPredictionChallenge>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/allstate_claim_prediction_challenge/`. To get them:

```text
We use train_set.csv of the Kaggle competition (2005-2007); the test rows of 2008 and 2009 were never labelled publicly.

kaggle competitions download -c ClaimPredictionChallenge -f train_set.zip && unzip train_set.zip && rm train_set.zip
sha256sum train_set.csv  # e8809676c72e976c659687bc35c0f132c651e77e691b50b9baf7128112019679
mkdir -p local-data-warehouse/allstate_claim_prediction_challenge && mv train_set.csv local-data-warehouse/allstate_claim_prediction_challenge/
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/allstate_claim_prediction_challenge_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/allstate_claim_prediction_challenge_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Kaggle: https://www.kaggle.com/competitions/ClaimPredictionChallenge |
| year | 2011 |
| domain | insurance |
| license | Kaggle Competition Rules |
| data_tags | Non-IID, Grouped, ForcedGroupedFromTemporal, Anonymized |
| reference | Allstate2011ClaimPredictionChallenge |
| version of | allstate_claim_prediction_challenge |
| rows x columns | 1,500,000 x 30 |
| task.target | log1p_claim_amount |
| task.problem_type | regression |
| task.metric | normalized_gini |
| task.split_regime | grouped_non_iid |
| task.group_on | Household_ID |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `normalized_gini` (custom; takes value; higher is better) |
| origin | source: the source's metric |
| original | Normalized Gini coefficient (the public leaderboard on 2008 and the final ranking on 2009) |
| reference | https://www.kaggle.com/competitions/ClaimPredictionChallenge/overview/evaluation |
| definition | G(y, p) / G(y, y), G = (sum of the cumulative share of the losses sorted by descending p - (n + 1) / 2) / n (tied p averaged over their orderings, so a constant p scores 0; the Kaggle code takes row order) |
| target scale | ships on the `log1p` scale for modelling; scored on the original scale after the inverse of `log1p` |

<details>
<summary>Feature types: 14 categorical, 0 string, 0 datetime</summary>

- categorical (14): `Blind_Make`, `Blind_Model`, `Blind_Submodel`, `Cat1`, `Cat2`, `Cat3`, `Cat4`, `Cat5`, `Cat6`, `Cat7`, `Cat8`, `Cat9`, `OrdCat`, `NVCat`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{Allstate2011ClaimPredictionChallenge,
  author = {{Allstate Insurance Company}},
  title = {Allstate Claim Prediction Challenge},
  year = {2011},
  howpublished = {\url{https://www.kaggle.com/competitions/ClaimPredictionChallenge}},
  note = {Kaggle competition}
}
```

</details>

## Sample rows

The first 5 of 1,500,000 rows of the final frame (random rows: the frame is shuffled); 12 of 30 columns, the target first. Cells are cut at 40 characters.

| log1p_claim_amount | Household_ID | Calendar_Year | Model_Year | Blind_Make | Blind_Model | Blind_Submodel | Cat1 | Cat2 | Cat3 | Cat4 | Cat5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 3136123 | 2005 | 1995 | K | K.52 | K.52.4 | G | nan | A | A | C |
| 0 | 3134760 | 2005 | 2005 | BO | BO.52 | BO.52.1 | D | A | A | nan | nan |
| 0 | 5946957 | 2005 | 1999 | P | P.34 | P.34.0 | J | C | B | nan | nan |
| 0 | 2132181 | 2006 | 1995 | N | N.25 | N.25.0 | A | nan | A | A | A |
| 0 | 6687083 | 2005 | 1988 | AJ | AJ.52 | AJ.52.0 | D | nan | C | nan | nan |

## Curation notes

We start with train_set.csv of the Kaggle competition (13,184,290 vehicle-years of 2005 to 2007; the 4,314,865 test rows of 2008 and 2009 were never labelled publicly) and keep 2005 and 2006: 8,473,402 vehicle-years of 3,445,943 households, 61,838 claims.

- Prediction point: when a vehicle's year of bodily-injury liability cover is rated. The vehicle and the policy's characteristics are known then; the year's claims are not. The features are anonymised vehicle and policy characteristics (data page); their timing cannot be checked further (LEAK-38).
- Target `log1p_claim_amount`, log1p of `Claim_Amount`: the vehicle's claim payments of the year, "adjusted to control for known non-vehicle effects" (data page) by an undisclosed rule, so "it isn't actually in units of any major currency" (Allstate, forum thread 928; USE-5). Scored on the amount (`target_transform="log1p"`, MET-3), as in frempl_french_motor_personal_line. Trained on the amount instead, untuned LightGBM scores a normalized Gini of 0.001 to 0.035 on the shipped folds, against 0.022 to 0.054 on the log1p scale; the review panel's own sample of the same definition found no winner (0.038 to 0.068 against 0.050 to 0.089).
- 99.27% of the rows are 0 (none negative; Huangfu 2015, Sec. 2.0, p. 6: "only 95,605 non-zero values (about 0.73%) among the 13,184,290 records"; 0.72% claims in the shipped 1.5M rows). Only the claim part carries signal, and little of it: on the shipped folds untuned LightGBM reaches a normalized Gini of 0.053 / 0.054 / 0.022 (bootstrap standard error 0.022 to 0.029; random predictions average -0.002 to 0.004 with a standard deviation of 0.019 to 0.025) at R^2 -0.004 to -0.003 on the log1p scale, and ranks claims at ROC AUC 0.56. A regularised LightGBM classifier of whether a claim occurs scores 0.065 / 0.060 / 0.039.
- The 2007 rows are dropped (LEAK-24, MET-2; decision 2): at the same claim rate and median claim as 2005 and 2006, their large claims are missing. Claims above 2,000 are 0.43% of the 2007 claims against 1.31% and 1.26%, in every band of vehicle age and each of the three largest makes, and the shortfall grows toward the tail (2007 against 2005: 1.01 at the median, 0.65 at the 99th and 0.59 at the 99.9th percentile). Large bodily-injury claims are paid over years and the release gives no valuation date, so the 2007 payments are probably incomplete. Pooled test folds over the three years also rewarded learning each year's claim level from other households: a predictor that knew only the year scored 0.055 to 0.058. On the two kept years the year column is a feature; the model's pooled score exceeds its score within each year by -0.000 to +0.001, and a year-only predictor scores 0.001 to 0.026.
- Missing values: the source's "?" becomes missing. 73.0% of the shipped rows have one; Cat2 is missing by model year (decision 3). The source removed such records from its test file and asked that models not use missingness, as "when the model is applied, all of the features will be collected" (forum thread 826), so the benchmark tests rows the application never sees (USE-8). Missingness carries no outcome beyond the vehicle type (a leave-one-out test by the review panel). Random draws in place of the missing values score 0.047 / 0.052 / 0.008 against 0.053 / 0.054 / 0.022, complete and incomplete test rows show no consistent gap (0.039 / 0.079 / -0.034 against 0.059 / 0.049 / 0.044), and training on complete rows only scores worse (0.045 / -0.029 / -0.020), so the rows stay; complete rows only would keep 27% of them and few vehicles built before 2000 (47.9% of the 2005-2006 rows, 13.8% of their complete rows, 8.6% of the competition's test file).
- No exposure is published: a row is a vehicle in a calendar year, and some are part years (vehicles whose model year is the next calendar year can only have been insured for part of it; they claim at 0.20% against 0.73% overall). The target is the year's payments, not a rate per year insured.
- One exact copy dropped (household 6365215's vehicle 4 in 2006, twice); three vehicle-years that appear twice with differing values are kept. Once the vehicle number and Cat10 to Cat12 are gone, 10,946 shipped rows (0.7%) repeat another row of the same household in every column, such as two vehicles of one type on one policy; a household is on one side of every fold, so they never straddle a split.
- `Row_ID` (the file's row number) and `Vehicle` dropped: the vehicle's number within its household "may not apply to the same vehicle from year to year" (data page), and its values run over every vehicle the household insured at any time in the year, including cars added after the rating, among them replacements after the row's own crash (LEAK-10). The household's count of vehicles in the year, which an earlier draft built in its place, was dropped for the same reason: vehicles added since the previous year claim at 1.17% when the count rose and at 0.72% otherwise, and the column added 0.015 to 0.020 Gini on the earlier folds.
- Cat10, Cat11 and Cat12 dropped (PROV-3, CLEAN-22): the same vehicle keeps its value from one year to the next only as often as a random redraw would, and their Cramér's V with every other column and with the claim is at most 0.0024, so they are not the vehicle characteristics the data page names.
- `Household_ID` is the group column, never a feature.
- Dtypes: the blinded make, model and submodel (74, 1,237 and 2,569 levels in 2005-2006), Cat1 to Cat9, OrdCat and NVCat categorical; the rest numeric. OrdCat, the "ordered categorical vehicle variable" (data page), is categorical as the ordinals of liberty_mutual_fire_peril_loss_cost and pricing_game_2017_french_mtpl (CLEAN-14): its claim rates over the levels 1 to 7 (0.32%, 0.82%, 0.60%, 0.72%, 0.64%, 0.60%, 0.11%) show no risk order.
- Note: NVCat and NVVar1 to NVVar4 are the policy's non-vehicle characteristics, for which the host expected no "main effects" but "interactions with the vehicle variables" (data page). Kept.
- Potential leak, kept on purpose (LEAK-30, weak): Var1 to Var8 and NVVar1 to NVVar4 are "mean 0 stdev 1" (data dictionary), yet over the labelled file their means are -0.065 to +0.019 and their standard deviations 0.97 to 1.04, so the host scaled them over a population we do not know, which may have taken in the test years. The yearly means of Var1 to Var8 rise from 2005 to 2007 (Var2 from -0.154 to +0.013) as the fleet's model-year mix changes; NVVar1 to NVVar4 do not rise. One shift and one scale per column; the unscaled values were never published.
- Note: 87% of the shipped rows share every feature with a row of another household (one vehicle type and policy profile): natural repeats, kept (LEAK-18).
- Note: the competition rules say "Participants will not use the data for purposes unrelated to the competition"; a 2022 forum question about the licence (thread 309810) has no answer.

Version of `allstate_claim_prediction_challenge`: We sub-sample the frame to 1.5M rows by whole households and use grouped 3-fold cross-validation, so every fold trains on about 1M and tests on about 500k rows (v2 split protocol). The households are drawn at random, not stratified (a regression target), so the claim rate stays that of 2005-2006.

## Splits

Default splits, grouped by household (Household_ID): 3 folds over 1.5M rows of whole households drawn at random from the 8.5M of 2005-2006 (claim rate 0.72%, as in those years), each training on about 1M and testing on about 500k rows with 3,490 to 3,653 claims. The task is temporal by its use case: the competition gave 2005-2007 for training and scored 2008 (public leaderboard) and 2009 (final ranking), whose claims were never published. Once 2007 is dropped (see the curation notes), no yearly window keeps half the rows for training (the 2006 window trains on 2005 alone, 47.5% of the rows), below the floor of SPLIT-14, so the task ships under SPLIT-8, stacked and grouped by household (ForcedGroupedFromTemporal): households recur across the years (72.6% of the 2006 vehicle-years belong to a household of 2005), and random rows would put a household's other year on both sides. The forced split shows no cost that this noise can measure. On the full release, before 2007 was dropped, untuned LightGBM trained on 2005-2006 scored 0.084 on all 4.7M rows of 2007, against 0.059 to 0.115 on the 2007 rows of the folds by household then shipped. On the shipped rows, trained on 2005 and scored on 2006 it reaches 0.064 (0.042 to 0.101 over random thirds of the test rows), against 0.019 to 0.030 on the shipped folds' 2006 rows and 0.022 to 0.054 on all their rows (bootstrap standard error 0.022 to 0.029). Folds of random rows score -0.008 to 0.082 on the same rows. What the folds do not test: a renewal book where most households are known (53% of the competition's test households were in its training file) and their claim history counts (in the full release, vehicles of households with an earlier claim claim at 1.44%, others at 0.77%); no history feature ships, so nothing leaks either. Nor do they test vehicle series not seen in training: only 0.02% of the test rows have a model or submodel unseen in training. A release with dates beyond 2007 should get a temporal split. A leak test across the folds (2026-11-02) finds none: 84% of the test rows repeat the features of a training row of another household, but a lookup of those rows' mean target scores -0.008 / -0.008 / -0.002, no test claim repeats a training row's features and amount, and no household recurs under another id; taking the test year's rows out of training costs no more than taking out as many random rows (6 of 6 fold-years). Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine").

1 repeat(s) x 3 fold(s) with seed 4267; train 999,818 to 1,000,000 rows, test 499,760 to 500,000 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 999818 | 500000 |
| 0 | 1 | 999942 | 500000 |
| 0 | 2 | 1000000 | 499760 |

## Group structure

One group is a household, "a household identification number that allows year-to-year tracking of each household" (data page): its rows are its insured vehicles in each year it is in the file (3,445,943 households in 2005-2006, 1 to 27 rows, 2.5 on average). The competition trained on 2005-2007 and scored 2008 and 2009, where 53% of the test households were also in the training file (forum thread 708). Two labelled years cannot give the windows of a temporal split (see the splits), so whole households are held out instead: a test household is new, and neither of its years is in training. Each vehicle-year is one prediction from its own row. The label is one per vehicle-year, so it can differ within a household; 97.8% of the households with two or more shipped rows have no claim or claims of one amount, because claims are rare.

| field | value |
|---|---|
| group column | `Household_ID` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 609,658 |
| rows per group (min / median / max) | 1 / 2.0 / 23 |
| largest group | 0.0% of the rows |
| test groups per fold | 203,143 to 203,219 |
| groups of two or more rows with a single label | 97.8% |
| nearest neighbour in the same group | 0.0% of the rows (chance: 0.0%) |
| label variance explained by the group | 0.39 (shuffled groups: 0.40) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. Grouped by household, not by year

Two labelled years give no window whose train side holds half of the rows (SPLIT-14), so the years are stacked and whole households are held out (SPLIT-8); households recur across the years, so random rows would put a household's other year on both sides.

| Calendar_Year | vehicle-years | share of vehicle-years (%) | households | share of vehicle-years whose household is in an earlier year |
|---|---|---|---|---|
| 2005 | 4025672 | 47.5 | 2562088 | 0 |
| 2006 | 4447730 | 52.5 | 2844270 | 0.726 |

### 2. The 2007 rows are dropped

The claim rate and the median claim are stable over the years, the upper tail of 2007 is not: large bodily-injury claims are paid over years, and the release gives no date at which the amounts were read, so the 2007 payments are probably incomplete (LEAK-24). Pooled test folds also rewarded learning each year's claim level (MET-2).

| Calendar_Year | claim rate (%) | claims | median claim | 90th percentile | 99th percentile | 99.9th percentile | claims above 2,000 (%) | mean claim |
|---|---|---|---|---|---|---|---|---|
| 2005 | 0.749 | 30148 | 47.2 | 527.9 | 2276.2 | 4918.1 | 1.31 | 201.1 |
| 2006 | 0.712 | 31690 | 46.6 | 522.1 | 2210.4 | 4967.7 | 1.26 | 200.8 |
| 2007 | 0.717 | 33767 | 47.7 | 451.3 | 1486.8 | 2931.5 | 0.43 | 163.2 |

### 3. Missing values stay

The source removed the records with a missing value from its test file and asked that models not use missingness. Cat2 is missing by model year; missingness carries no outcome beyond the vehicle type, and keeping only complete rows would drop most older vehicles.

| Model_Year (5-year bins) | vehicle-years | complete rows | Cat2 missing (%) | Cat4 missing (%) | Cat7 missing (%) | any missing (%) | claim rate, complete rows (%) | claim rate, rows with a missing value (%) |
|---|---|---|---|---|---|---|---|---|
| 1980 | 93373 | 2 | 100 | 62.9 | 75 | 100 | 0 | 0.334 |
| 1985 | 414770 | 301 | 99.9 | 51.1 | 68.2 | 99.9 | 0.664 | 0.476 |
| 1990 | 1104625 | 4424 | 97.7 | 36.1 | 51.3 | 99.6 | 0.565 | 0.685 |
| 1995 | 2448653 | 310235 | 72.3 | 37.6 | 51 | 87.3 | 0.854 | 0.803 |
| 2000 | 3389382 | 1484071 | 0 | 45.2 | 56.1 | 56.2 | 0.789 | 0.769 |
| 2005 | 1022599 | 482113 | 0 | 45.3 | 52.8 | 52.9 | 0.596 | 0.543 |

## Bundle checks

0 error(s), 0 warning(s), 3 info (26 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 10,946 exact duplicate row(s) (0.7% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)
- **info** `dataset_conflicting_duplicate_rows`: 143 row(s) (0.0%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)
- **info** `groups_not_clustered`: Rows are no closer to their own group than chance (0.0% of nearest neighbours vs 0.0%), and the group explains no more of the label than shuffled groups (0.39 vs 0.40). (hint: The grouping may not be needed: compare IID and grouped scores with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.)

Accepted on purpose:

- `splits_rows_never_tested`: The v2 protocol caps each test fold at 500k rows; the folds by household overshoot by whole households, so 240 of the 1.5M rows are trimmed from a test fold (2026-11-01).
- `groups_labels_constant`: The label is one per vehicle-year and claims are rare (0.72%), so 97.8% of the households with two or more rows have a single label; 9,475 of 429,370 have several (2026-11-01).
- `task_target_value_dominant`: A zero-inflated target, not a cap or a placeholder: 0 is a vehicle-year without a bodily-injury claim, 99.28% of the shipped rows (see the curation notes; 2026-11-01).

## Data checks

### Feature summary

<details>
<summary>Show the table (30 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| Cat7 | category | 815197 | 54.35 | 4 | C, A, B, D |
| Cat5 | category | 634684 | 42.31 | 3 | A, C, B |
| Cat4 | category | 633965 | 42.26 | 3 | A, C, B |
| Cat2 | category | 593064 | 39.54 | 3 | C, A, B |
| Cat1 | category | 3038 | 0.2 | 10 | B, I, D, F, G, A, C, E, J, H |
| Cat6 | category | 3038 | 0.2 | 5 | B, C, D, E, F |
| Blind_Make | category | 979 | 0.07 | 71 | K, AJ, BW, AU, Y, X, BO, W, L, AO |
| Blind_Model | category | 979 | 0.07 | 1173 | K.7, X.45, AU.14, W.16, AU.11, BO.38, AJ.58, AO.7, AJ.52, AJ.129 |
| Blind_Submodel | category | 979 | 0.07 | 2411 | K.7.3, AU.58.0, AU.14.0, AU.11.3, W.16.3, K.7.0, AU.14.1, BW.3.0, BW.95.0, BW.1… |
| OrdCat | category | 828 | 0.06 | 7 | 4, 2, 5, 3, 1, 6, 7 |
| Cat3 | category | 443 | 0.03 | 6 | A, B, C, E, F, D |
| Cat8 | category | 420 | 0.03 | 3 | A, B, C |
| Cat9 | category | 0 | 0 | 2 | B, A |
| NVCat | category | 0 | 0 | 15 | M, O, N, L, J, E, F, B, H, K |
| Var1 | float64 | 0 | 0 | 339 | -0.7141, -0.7704, -0.6338, -0.1195, -0.3927, -0.2802, 0.5876, -0.2963, -0.4007,… |
| Var2 | float64 | 0 | 0 | 293 | 0.0484, 0.2213, -0.6432, -0.2974, -0.9891, -0.8162, -0.1245, -1.2484, -0.7297, … |
| Var3 | float64 | 0 | 0 | 192 | -1.2399, -1.2862, -0.4532, -0.9622, 0.2179, -0.6151, 1.0972, -1.078, -0.3837, -… |
| Var4 | float64 | 0 | 0 | 294 | 0.1472, -0.5293, 0.3164, -0.6985, -0.0219, 0.4855, -0.3602, -1.2904, 0.2318, -1… |
| Var5 | float64 | 0 | 0 | 640 | 0.5272, -0.1567, -0.1984, -0.1151, -0.0437, 0.5034, 0.6997, 0.3785, 0.5807, -0.… |
| Var6 | float64 | 0 | 0 | 2475 | -0.6794, -0.5858, -1.1964, -1.1344, -0.6853, -0.6888, -1.0654, -0.6268, -0.2887… |
| Var7 | float64 | 0 | 0 | 347 | -0.9353, -0.5913, -0.8616, -0.837, -0.8125, -0.9845, -1.0582, -1.0091, -0.8985,… |
| Var8 | float64 | 0 | 0 | 5619 | -0.2536, -0.218, -0.3315, -0.3495, -0.2979, -0.2249, -0.3843, -0.3085, -0.3515,… |
| NVVar1 | float64 | 0 | 0 | 20 | -0.2315, 3.1978, 6.6271, 2.0547, 1.4831, 1.1402, 2.5119, 0.9116, 4.3409, 0.7483 |
| NVVar2 | float64 | 0 | 0 | 23 | -0.2661, 2.7836, 4.3085, 2.0212, 1.5637, 8.8831, 3.3936, 5.8333, 1.2587, 5.2234 |
| NVVar3 | float64 | 0 | 0 | 24 | -0.2723, 2.7155, 1.9685, 4.2094, 1.5204, 8.6911, 3.3131, 5.7033, 1.2216, 5.1058 |
| NVVar4 | float64 | 0 | 0 | 22 | -0.2514, 3.0687, 6.3888, 1.962, 1.4086, 1.0766, 0.8553, 2.4047, 4.1754, 0.6972 |
| log1p_claim_amount | float64 | 0 | 0 | 10760 | 0.0, 3.8063, 0.9846, 5.9848, 4.2045, 1.9469, 2.3227, 2.5164, 3.8714, 4.577 |
| Household_ID | int64 | 0 | 0 | 609658 | 6674438, 6853096, 198043, 6390913, 2101395, 7257690, 6673513, 7080015, 2541967,… |
| Calendar_Year | int64 | 0 | 0 | 2 | 2006, 2005 |
| Model_Year | int64 | 0 | 0 | 27 | 2002, 2004, 2000, 2001, 2003, 2005, 1999, 1998, 1997, 1995 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 99.29 | 14.49 | 12.756 | 0.127 | 0.017 | log1p | 5012.4 | 1.92261e+06 | exponential |

### Numeric features

<details>
<summary>Show the table (16 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| Household_ID | 150000 | 4.35694e+06 | 2.27862e+06 | 11 | 7.5421e+06 |
| Calendar_Year | 150000 | 2005.52 | 0.499391 | 2005 | 2006 |
| Model_Year | 150000 | 1998.88 | 5.11799 | 1981 | 2007 |
| Var1 | 150000 | -0.0282943 | 0.97731 | -2.57822 | 5.14339 |
| Var2 | 150000 | -0.11159 | 0.948449 | -2.49339 | 7.43172 |
| Var3 | 150000 | -0.0519099 | 1.02056 | -2.74405 | 5.56333 |
| Var4 | 150000 | -0.10038 | 0.948233 | -2.50822 | 7.20025 |
| Var5 | 150000 | -0.0124762 | 0.989698 | -3.35034 | 4.00627 |
| Var6 | 150000 | -0.0698237 | 0.97112 | -2.37666 | 4.58429 |
| Var7 | 150000 | -0.0464221 | 1.00537 | -2.36071 | 3.90597 |
| Var8 | 150000 | -0.092216 | 0.99924 | -2.16304 | 47.3234 |
| NVVar1 | 150000 | 0.0149355 | 1.0233 | -0.23153 | 6.62711 |
| NVVar2 | 150000 | 0.0186202 | 1.0357 | -0.266117 | 8.88308 |
| NVVar3 | 150000 | 0.0102548 | 1.01153 | -0.272337 | 8.69114 |
| NVVar4 | 150000 | 0.0298493 | 1.05281 | -0.251419 | 6.3888 |
| log1p_claim_amount | 150000 | 0.0273812 | 0.35593 | 0 | 8.36345 |

</details>

### Categorical features

<details>
<summary>Show the table (63 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| Blind_Make | 1 | K | 18266 | 12.18 |
| Blind_Make | 2 | AJ | 17632 | 11.75 |
| Blind_Make | 3 | BW | 14368 | 9.58 |
| Blind_Make | 4 | AU | 12079 | 8.05 |
| Blind_Make | 5 | Y | 9694 | 6.46 |
| Blind_Model | 1 | K.7 | 6822 | 4.55 |
| Blind_Model | 2 | X.45 | 3451 | 2.3 |
| Blind_Model | 3 | AU.14 | 3316 | 2.21 |
| Blind_Model | 4 | W.16 | 2668 | 1.78 |
| Blind_Model | 5 | AU.11 | 2446 | 1.63 |
| Blind_Submodel | 1 | K.7.3 | 1879 | 1.25 |
| Blind_Submodel | 2 | AU.58.0 | 1663 | 1.11 |
| Blind_Submodel | 3 | AU.14.0 | 1622 | 1.08 |
| Blind_Submodel | 4 | AU.11.3 | 1594 | 1.06 |
| Blind_Submodel | 5 | W.16.3 | 1525 | 1.02 |
| Cat1 | 1 | B | 46029 | 30.69 |
| Cat1 | 2 | I | 29578 | 19.72 |
| Cat1 | 3 | D | 28070 | 18.71 |
| Cat1 | 4 | F | 15518 | 10.35 |
| Cat1 | 5 | G | 9049 | 6.03 |
| Cat2 | 1 | C | 63767 | 42.51 |
| Cat2 | 2 | &lt;NA> | 58992 | 39.33 |
| Cat2 | 3 | A | 24689 | 16.46 |
| Cat2 | 4 | B | 2552 | 1.7 |
| Cat3 | 1 | A | 86503 | 57.67 |
| Cat3 | 2 | B | 22896 | 15.26 |
| Cat3 | 3 | C | 15432 | 10.29 |
| Cat3 | 4 | E | 10593 | 7.06 |
| Cat3 | 5 | F | 9291 | 6.19 |
| Cat4 | 1 | A | 65422 | 43.61 |
| Cat4 | 2 | &lt;NA> | 63141 | 42.09 |
| Cat4 | 3 | C | 16888 | 11.26 |
| Cat4 | 4 | B | 4549 | 3.03 |
| Cat5 | 1 | A | 76850 | 51.23 |
| Cat5 | 2 | &lt;NA> | 63220 | 42.15 |
| Cat5 | 3 | C | 8999 | 6 |
| Cat5 | 4 | B | 931 | 0.62 |
| Cat6 | 1 | B | 48249 | 32.17 |
| Cat6 | 2 | C | 42504 | 28.34 |
| Cat6 | 3 | D | 40519 | 27.01 |
| Cat6 | 4 | E | 13140 | 8.76 |
| Cat6 | 5 | F | 5264 | 3.51 |
| Cat7 | 1 | &lt;NA> | 81093 | 54.06 |
| Cat7 | 2 | C | 52693 | 35.13 |
| Cat7 | 3 | A | 12116 | 8.08 |
| Cat7 | 4 | B | 2632 | 1.75 |
| Cat7 | 5 | D | 1466 | 0.98 |
| Cat8 | 1 | A | 99719 | 66.48 |
| Cat8 | 2 | B | 40581 | 27.05 |
| Cat8 | 3 | C | 9672 | 6.45 |
| Cat8 | 4 | &lt;NA> | 28 | 0.02 |
| Cat9 | 1 | B | 126976 | 84.65 |
| Cat9 | 2 | A | 23024 | 15.35 |
| NVCat | 1 | M | 65780 | 43.85 |
| NVCat | 2 | O | 38251 | 25.5 |
| NVCat | 3 | N | 15225 | 10.15 |
| NVCat | 4 | L | 8857 | 5.9 |
| NVCat | 5 | J | 6313 | 4.21 |
| OrdCat | 1 | 4 | 67519 | 45.01 |
| OrdCat | 2 | 2 | 47849 | 31.9 |

(3 more rows not shown)

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
