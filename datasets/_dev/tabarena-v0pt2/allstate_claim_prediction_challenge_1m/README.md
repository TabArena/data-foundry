---
report_format: data-foundry-report-v2
unique_name: allstate_claim_prediction_challenge_1m
container_format: 2
checksum: v2:f93e12db969df6e975aee588ba3239b9e75ad34fcc6e0b8b3079a3f2a6a4055e
build: null
build_stale: false
data:
  n_rows: 1500000
  n_features: 32
  dtypes:
    category: 15
    float64: 16
    int64: 2
    int8: 1
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
    n_groups: 959436
    test_groups_per_fold:
      min: 319477
      max: 319812
splits:
  n_repeats: 1
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 999477
    max: 1000000
  n_test:
    min: 499656
    max: 500000
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicates_skipped
  - groups_not_clustered
  accepted:
    splits_rows_never_tested: The v2 protocol caps each test fold at 500k rows; the
      folds by household overshoot by whole households, so 240 of the 1.5M rows are
      trimmed from a test fold (2026-11-01).
    groups_labels_constant: The label is one per vehicle-year and claims are rare
      (0.71%), so 98.2% of the households with two or more rows of 2006 have a single
      label (2026-11-03).
    task_target_value_dominant: 'A zero-inflated target, not a cap or a placeholder:
      0 is a vehicle-year without a bodily-injury claim, 99.29% of the 2006 rows (see
      the curation notes; 2026-11-03).'
decisions:
- 2006 rows, with 2005 as their history
- The 2007 rows are dropped
- Missing values stay
---

# allstate_claim_prediction_challenge_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `log1p_claim_amount`, scored with `normalized_gini` on grouped splits by `Household_ID`. 1,500,000 rows and 32 features. Source: Kaggle (2011).

Not built yet. The current definition gives checksum `v2:f93e12db969df6e975aee588ba3239b9e75ad34fcc6e0b8b3079a3f2a6a4055e`.

## In brief

**Question.** How much will an insured vehicle cost Allstate in bodily-injury liability claims in 2006, on the scale Allstate adjusted the amounts to, from the vehicle's characteristics and the household's record of 2005?

**Use case.** For example, Allstate rating a vehicle for bodily-injury liability cover at the 2006 renewal: the vehicle's expected claim cost ranks its risk and sets the vehicle part of the premium, with the household's record of the year before, as an insurer prices a renewal. The competition names the target and the features, not the decision.

**One row.** One vehicle insured by Allstate in 2006 (4.4 million vehicle-years of 2.8 million households in the competition's labelled file, of which whole households holding 1.5 million vehicle-years are sampled); the rows of 2005 give only the history.

**Predicted.** The vehicle's bodily-injury liability claim payments in 2006, adjusted by Allstate to remove known non-vehicle effects by a rule it did not disclose, so in no currency: 0 for 99.29% of the vehicle-years. Shipped as log1p, scored on the amount.

**Known at prediction time.** The vehicle's model year and blinded make, model and submodel, 18 anonymised vehicle characteristics, 5 anonymised characteristics of the policy, and from 2005: the household's vehicles and claims, how many of its cars were already insured, and this car's claims (missing for a new household).

**What the test data stands for.** All vehicles of a household stay on one side, so the test data stands for households not seen in training, from the same year; the competition scored 2008 and 2009, whose claims were never published.

**Our changes to the source.** We kept the 2006 rows with the household's and the car's 2005 record as counts; dropped 2007, whose large claims look unsettled, and one exact copy; sampled whole households to the row budget; dropped the row number, the vehicle's number in the household, the year and Cat10 to Cat12, which behave like random draws; and coded the source's missing values as missing.

> **Use case fit: approximate (a stand-in with a known gap).** Vehicle and policy attributes and the household's record of the year before, as at the renewal. But the amounts' adjustment is undisclosed, no exposure is published, unseen vehicle series go untested, and 72% of the rows have a missing value the application never has. Kaggle's winners reached a Gini of 0.20 on 2009 against our 0.02 to 0.10 per fold, mostly because this Gini turns on a few large claims.

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
| rows x columns | 1,500,000 x 34 |
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
<summary>Feature types: 15 categorical, 0 string, 0 datetime</summary>

- categorical (15): `Blind_Make`, `Blind_Model`, `Blind_Submodel`, `Cat1`, `Cat2`, `Cat3`, `Cat4`, `Cat5`, `Cat6`, `Cat7`, `Cat8`, `Cat9`, `OrdCat`, `NVCat`, `vehicle_insured_2005`
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

The first 5 of 1,500,000 rows of the final frame (random rows: the frame is shuffled); 12 of 34 columns, the target first. Cells are cut at 40 characters.

| log1p_claim_amount | Household_ID | Model_Year | Blind_Make | Blind_Model | Blind_Submodel | Cat1 | Cat2 | Cat3 | Cat4 | Cat5 | Cat6 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 3844716 | 2001 | AJ | AJ.129 | AJ.129.3 | G | C | A | A | C | E |
| 0 | 4769228 | 2006 | K | K.40 | K.40.3 | E | C | A | A | A | C |
| 0 | 4714582 | 2003 | BO | BO.47 | BO.47.1 | D | A | A | nan | nan | D |
| 0 | 6716825 | 2000 | Y | Y.29 | Y.29.0 | B | C | B | A | A | D |
| 0 | 6191911 | 1995 | I | I.15 | I.15.4 | E | nan | B | A | A | B |

## Curation notes

We start with train_set.csv of the Kaggle competition (13,184,290 vehicle-years of 2005 to 2007; the 4,314,865 test rows of 2008 and 2009 were never labelled publicly) and keep the 4,447,729 vehicle-years of 2006 (2,844,270 households, 31,690 claims), with 2005 as their history (decision 1; Andrej, 2026-11-03: "2006 renewal book with the 2005 history (counts)").

- Prediction point: when a vehicle's year of bodily-injury liability cover is rated at the 2006 renewal. The vehicle and the policy's characteristics and the household's record of 2005 are known then; the year's claims are not. The features are anonymised vehicle and policy characteristics (data page); their timing cannot be checked further (LEAK-38).
- The 2005 history (LEAK-10, LEAK-34): `household_vehicles_2005` and `household_claims_2005` (the household's vehicle-years and the ones with a claim; missing for the 27.4% of rows whose household is new), `vehicle_insured_2005` (the car was insured in 2005: same household, model year and submodel, as `Vehicle` is no stable id), `vehicle_claims_2005` (that car's vehicle-years with a claim; missing when it was not insured) and `household_vehicles_carried` (the household's cars of 2006 insured in 2005, all on the policy at the renewal). In 2006 a household that claimed in 2005 claims at 1.50%, a known household without a claim at 0.78%, a new household at 0.50%; a car that claimed in 2005 at 1.89%. The rating date within the year is not published, so a 2005 claim reported after an early 2006 renewal counts as known; the share cannot be measured (as in spanish_homeowners_motor_insurance_2010_2014). On 1.5M rows of 2006 sampled as shipped, the history lifts untuned LightGBM's ranking of claims from 0.112-0.117 to 0.126-0.137 (normalized Gini on claim yes/no); on the amount the change stays within the noise (0.025-0.104 either way).
- The 2005 claim amounts are not a feature: the file gives them as read years after the renewal, and bodily-injury amounts keep growing for years (the 2007 claims above 2,000 are a third as frequent as in 2005, decision 2), so they hold more than the insurer saw at the renewal. spanish_homeowners_motor_insurance_2010_2014 keeps its previous-year home claim cost, a short-tail cover. Their gain here was within the noise (+0.001 to +0.014).
- Target `log1p_claim_amount`, log1p of `Claim_Amount`: the vehicle's claim payments of the year, "adjusted to control for known non-vehicle effects" (data page) by an undisclosed rule, so "it isn't actually in units of any major currency" (Allstate, forum thread 928; USE-5). Scored on the amount (`target_transform="log1p"`, MET-3), as in frempl_french_motor_personal_line; the competition's normalized Gini on the amount (Andrej, 2026-11-03, issue 4: A).
- 99.29% of the 2006 rows are 0 (none negative; Huangfu 2015, Sec. 2.0, p. 6: "only 95,605 non-zero values (about 0.73%) among the 13,184,290 records"). Little signal, decided by a few large claims (median claim 46.6, 99th percentile 2,210): on 1.5M rows of 2006 sampled as shipped, untuned LightGBM with the history scores a normalized Gini of 0.046 to 0.103 over nine folds of three random household splits (mean 0.070, standard deviation 0.019); random predictions have a standard deviation of 0.019 to 0.032 per fold.
- Kaggle's leaderboard (0.2016 for the winner on 2009) is far above these folds. Most of the gap is the claims' tail: scored on claim yes/no instead of the amount, the same predictions reach about twice the Gini, and the tail of Kaggle's test years cannot be measured, as their amounts were never published. Tuning, ensembles and twice the training rows are the rest (review, issue 4).
- The 2007 rows are dropped (LEAK-24, MET-2; decision 2; confirmed by Andrej on 2026-11-03; 2007 can come back with settled amounts): at the same claim rate and median claim as 2005 and 2006, their large claims are missing. Claims above 2,000 are 0.43% of the 2007 claims against 1.31% and 1.26%, in every band of vehicle age and each of the three largest makes, and the shortfall grows toward the tail (2007 against 2005: 1.01 at the median, 0.65 at the 99th and 0.59 at the 99.9th percentile). Large bodily-injury claims are paid over years and the release gives no valuation date, so the 2007 payments are probably incomplete.
- Missing values: the source's "?" becomes missing. 71.6% of the 2006 rows have one; Cat2 (36.9% missing) is missing by model year (decision 3). The source removed such records from its test file and asked that models not use missingness, as "when the model is applied, all of the features will be collected" (forum thread 826), so the benchmark tests rows the application never sees (USE-8). On the 2005-2006 build, missingness carried no outcome beyond the vehicle type (a leave-one-out test by the review panel), random draws in place of the missing values scored no better, and training on complete rows only scored worse, so the rows stay; complete rows only would drop most vehicles built before 2000.
- No exposure is published: a row is a vehicle in a calendar year, and some are part years (vehicles of model year 2007 can only have been insured for part of 2006; 1.4% of the rows, claiming at 0.25% against 0.71% overall). The target is the year's payments, not a rate per year insured.
- One exact copy dropped (household 6365215's vehicle 4 in 2006, twice). Once the vehicle number and Cat10 to Cat12 are gone, 32,324 rows of 2006 (0.73%) repeat another row of the same household in every column, such as two vehicles of one type on one policy; a household is on one side of every fold, so they never straddle a split.
- `Row_ID` (the file's row number) and `Vehicle` dropped: the vehicle's number within its household "may not apply to the same vehicle from year to year" (data page), and its values run over every vehicle the household insured at any time in the year, including cars added after the rating, among them replacements after the row's own crash (LEAK-10). The household's count of vehicles in the year was dropped for the same reason (vehicles already insured the year before claim at 1.05% when the count rose, 0.77% otherwise); the 2005 counts take its place. `Calendar_Year` has one value and goes.
- Cat10, Cat11 and Cat12 dropped (PROV-3, CLEAN-22): the same vehicle keeps its value from one year to the next only as often as a random redraw would, and their Cramér's V with every other column and with the claim is at most 0.0024, so they are not the vehicle characteristics the data page names.
- `Household_ID` is the group column, never a feature.
- Dtypes: the blinded make, model and submodel (74, 1,230 and 2,550 levels in 2006), Cat1 to Cat9, OrdCat, NVCat and the flag `vehicle_insured_2005` categorical (CLEAN-14); the rest numeric. OrdCat, the "ordered categorical vehicle variable" (data page), is categorical as the ordinals of liberty_mutual_fire_peril_loss_cost and pricing_game_2017_french_mtpl: its claim rates over the levels 1 to 7 (0.21%, 0.80%, 0.57%, 0.70%, 0.63%, 0.57%, 0.14%) show no risk order.
- Note: NVCat and NVVar1 to NVVar4 are the policy's non-vehicle characteristics, for which the host expected no "main effects" but "interactions with the vehicle variables" (data page). Kept.
- Potential leak, kept on purpose (LEAK-30, weak): Var1 to Var8 and NVVar1 to NVVar4 are "mean 0 stdev 1" (data dictionary), yet over the labelled file their means are -0.065 to +0.019 and their standard deviations 0.97 to 1.04, so the host scaled them over a population we do not know, which may have taken in the test years. The yearly means of Var1 to Var8 rise from 2005 to 2007 (Var2 from -0.154 to +0.013) as the fleet's model-year mix changes; NVVar1 to NVVar4 do not rise. One shift and one scale per column; the unscaled values were never published.
- Note: 82.9% of the 2006 rows share every feature with a row of another household (one vehicle type, policy profile and history): natural repeats, kept (LEAK-18).
- Note: the competition rules say "Participants will not use the data for purposes unrelated to the competition"; a 2022 forum question about the licence (thread 309810) has no answer.

Version of `allstate_claim_prediction_challenge`: We sub-sample the 2006 rows to 1.5M by whole households and use grouped 3-fold cross-validation, so every fold trains on about 1M and tests on about 500k rows (v2 split protocol). The households are drawn at random, not stratified (a regression target), so the claim rate stays that of 2006. The 2005 history is built on the full file before the sampling.

## Splits

Default splits, grouped by household (Household_ID): 3 folds over 1.5M rows of whole households drawn at random from the 4.4M of 2006 (claim rate 0.71%, as in that year), each training on about 1M and testing on about 500k rows with about 3,500 claims. The task is temporal by its use case: the competition gave 2005-2007 for training and scored 2008 (public leaderboard) and 2009 (final ranking), whose claims were never published. With 2007 dropped (its large claims look unsettled) and 2005 used as the history of 2006, one labelled target year is left, so no window of a temporal split exists and the task ships under SPLIT-8 (ForcedGroupedFromTemporal): the folds hold out whole households, whose vehicles share the household's record, so random rows would put a household's other cars on both sides. Before the history was built, trained on 2005 and scored on 2006 the rows reached 0.064, inside the range of the folds by household (0.022 to 0.054 then, 0.046 to 0.103 now with the history), so the forced split shows no cost this noise can measure. What the folds do not test: vehicle series not seen in training (0.02% of test rows on the earlier folds), and a rating at a known date within the year. A release with dates beyond 2007 should get a temporal split. Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine"; 2026-11-03: the 2006 renewal book).

1 repeat(s) x 3 fold(s) with seed 4267; train 999,477 to 1,000,000 rows, test 499,656 to 500,000 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 999477 | 500000 |
| 0 | 1 | 1000000 | 499656 |
| 0 | 2 | 1000000 | 499821 |

## Group structure

One group is a household, "a household identification number that allows year-to-year tracking of each household" (data page): its rows are its insured vehicles of 2006 (2,844,270 households, 1 to 18 rows, 1.56 on average), which share the household's 2005 record. The competition trained on 2005-2007 and scored 2008 and 2009. One target year cannot give the windows of a temporal split (see the splits), so whole households are held out: a test household is new to the model, and its history comes from 2005, as for every row. Each vehicle-year is one prediction from its own row. The label is one per vehicle-year, so it can differ within a household; 98.2% of the households with two or more rows have no claim or claims of one amount, because claims are rare.

| field | value |
|---|---|
| group column | `Household_ID` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 959,436 |
| rows per group (min / median / max) | 1 / 1.0 / 14 |
| largest group | 0.0% of the rows |
| test groups per fold | 319,477 to 319,812 |
| groups of two or more rows with a single label | 98.3% |
| nearest neighbour in the same group | 0.1% of the rows (chance: 0.0%) |
| label variance explained by the group | 0.61 (shuffled groups: 0.64) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. 2006 rows, with 2005 as their history

An insurer rates a renewal on the household's record of the year before; with 2007 dropped, 2006 is the one year that has one, so its rows are the task and 2005 gives the counts of vehicles and claims (LEAK-10: counts only, the 2005 amounts were read years later). One target year has no window for a temporal split, so whole households are held out (SPLIT-8).

| 2005 record | vehicle-years | share of rows (%) | claim rate 2006 (%) |
|---|---|---|---|
| household claimed in 2005 | 15414 | 1.03 | 1.46 |
| household known, no claim in 2005 | 1073469 | 71.56 | 0.78 |
| new household | 411117 | 27.41 | 0.503 |
| car claimed in 2005 | 5835 | 0.39 | 1.799 |
| car insured in 2005, no claim | 922958 | 61.53 | 0.815 |
| car not insured in 2005 | 571207 | 38.08 | 0.532 |

### 2. The 2007 rows are dropped

The claim rate and the median claim are stable over the years, the upper tail of 2007 is not: large bodily-injury claims are paid over years, and the release gives no date at which the amounts were read, so the 2007 payments are probably incomplete (LEAK-24).

| Calendar_Year | claim rate (%) | claims | median claim | 90th percentile | 99th percentile | 99.9th percentile | claims above 2,000 (%) | mean claim |
|---|---|---|---|---|---|---|---|---|
| 2005 | 0.749 | 30148 | 47.2 | 527.9 | 2276.2 | 4918.1 | 1.31 | 201.1 |
| 2006 | 0.712 | 31690 | 46.6 | 522.1 | 2210.4 | 4967.7 | 1.26 | 200.8 |
| 2007 | 0.717 | 33767 | 47.7 | 451.3 | 1486.8 | 2931.5 | 0.43 | 163.2 |

### 3. Missing values stay

The source removed the records with a missing value from its test file and asked that models not use missingness. Cat2 is missing by model year; missingness carries no outcome beyond the vehicle type, and keeping only complete rows would drop most older vehicles.

| Model_Year (5-year bins) | vehicle-years | complete rows | Cat2 missing (%) | Cat4 missing (%) | Cat7 missing (%) | any missing (%) | claim rate, complete rows (%) | claim rate, rows with a missing value (%) |
|---|---|---|---|---|---|---|---|---|
| 1980 | 44172 | 1 | 100 | 63.7 | 75.8 | 100 | 0 | 0.34 |
| 1985 | 193817 | 155 | 99.9 | 52.5 | 69.3 | 99.9 | 1.29 | 0.435 |
| 1990 | 532029 | 2118 | 97.7 | 37 | 51.9 | 99.6 | 0.425 | 0.661 |
| 1995 | 1228990 | 157522 | 72 | 37.9 | 51.2 | 87.2 | 0.834 | 0.779 |
| 2000 | 1741297 | 766113 | 0 | 45.1 | 55.8 | 56 | 0.787 | 0.741 |
| 2005 | 707425 | 335788 | 0 | 45.1 | 52.5 | 52.5 | 0.631 | 0.578 |

## Bundle checks

0 error(s), 0 warning(s), 2 info (26 checks run, plus the dataset's own checks).

- **info** `dataset_duplicates_skipped`: Skipped duplicate-column/row checks: 51,000,000 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to force them, or rely on `dataset_checks.run_all_checks`.)
- **info** `groups_not_clustered`: Rows are no closer to their own group than chance (0.1% of nearest neighbours vs 0.0%), and the group explains no more of the label than shuffled groups (0.61 vs 0.64). (hint: The grouping may not be needed: compare IID and grouped scores with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.)

Accepted on purpose:

- `splits_rows_never_tested`: The v2 protocol caps each test fold at 500k rows; the folds by household overshoot by whole households, so 240 of the 1.5M rows are trimmed from a test fold (2026-11-01).
- `groups_labels_constant`: The label is one per vehicle-year and claims are rare (0.71%), so 98.2% of the households with two or more rows of 2006 have a single label (2026-11-03).
- `task_target_value_dominant`: A zero-inflated target, not a cap or a placeholder: 0 is a vehicle-year without a bodily-injury claim, 99.29% of the 2006 rows (see the curation notes; 2026-11-03).

## Data checks

### Feature summary

<details>
<summary>Show the table (34 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| Cat7 | category | 814817 | 54.32 | 4 | C, A, B, D |
| Cat5 | category | 640846 | 42.72 | 3 | A, C, B |
| Cat4 | category | 640243 | 42.68 | 3 | A, C, B |
| Cat2 | category | 554597 | 36.97 | 3 | C, A, B |
| Cat1 | category | 2960 | 0.2 | 10 | B, I, D, F, G, A, C, E, J, H |
| Cat6 | category | 2960 | 0.2 | 5 | B, C, D, E, F |
| Blind_Make | category | 963 | 0.06 | 73 | K, AJ, BW, AU, Y, X, BO, W, AO, L |
| Blind_Model | category | 963 | 0.06 | 1189 | K.7, AU.14, X.45, W.16, AU.11, BO.38, AO.7, AJ.58, AJ.52, AJ.129 |
| Blind_Submodel | category | 963 | 0.06 | 2441 | K.7.3, AU.58.0, AU.14.1, AU.14.0, W.16.3, AU.11.3, K.7.0, BW.115.0, BW.3.0, K.7… |
| OrdCat | category | 851 | 0.06 | 7 | 4, 2, 5, 3, 1, 6, 7 |
| Cat3 | category | 421 | 0.03 | 6 | A, B, C, F, E, D |
| Cat8 | category | 391 | 0.03 | 3 | A, B, C |
| Cat9 | category | 0 | 0 | 2 | B, A |
| NVCat | category | 0 | 0 | 15 | M, O, N, L, J, E, F, B, H, K |
| vehicle_insured_2005 | category | 0 | 0 | 2 | 1, 0 |
| vehicle_claims_2005 | float64 | 571207 | 38.08 | 3 | 0.0, 1.0 |
| household_vehicles_2005 | float64 | 411117 | 27.41 | 13 | 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 |
| household_claims_2005 | float64 | 411117 | 27.41 | 3 | 0.0, 1.0, 2.0 |
| Var1 | float64 | 0 | 0 | 341 | -0.7141, -0.3927, -0.1195, -0.7704, 0.5876, -0.6338, -0.2802, -0.2963, -0.457, … |
| Var2 | float64 | 0 | 0 | 296 | 0.2213, 0.0484, -0.6432, -0.2974, -0.9891, -0.8162, -0.1245, -0.5568, -1.2484, … |
| Var3 | float64 | 0 | 0 | 192 | -1.2399, -0.4532, -1.2862, -0.9622, 0.2179, -0.6151, -0.1292, -0.3837, 1.0972, … |
| Var4 | float64 | 0 | 0 | 297 | 0.1472, 0.3164, -0.5293, -0.6985, -0.0219, 0.4855, -0.3602, -1.2904, 0.2318, -1… |
| Var5 | float64 | 0 | 0 | 646 | 0.5272, -0.1567, -0.1151, -0.1984, -0.0437, 0.6997, -0.2103, -0.9655, 0.5034, 0… |
| Var6 | float64 | 0 | 0 | 2495 | -0.6853, -0.5858, -0.6794, -1.1964, -0.5601, -0.2887, -0.6888, -1.0654, -0.5461… |
| Var7 | float64 | 0 | 0 | 352 | -0.9353, -0.5913, -0.8616, -0.837, -0.8125, -0.9845, -1.0582, -0.8985, 0.7603, … |
| Var8 | float64 | 0 | 0 | 5700 | -0.2536, -0.218, -0.3843, -0.2979, -0.3315, -0.2249, -0.3495, -0.3515, -0.3085,… |
| NVVar1 | float64 | 0 | 0 | 21 | -0.2315, 3.1978, 6.6271, 2.0547, 1.4831, 1.1402, 2.5119, 0.9116, 4.3409, 0.7483 |
| NVVar2 | float64 | 0 | 0 | 21 | -0.2661, 2.7836, 4.3085, 2.0212, 1.5637, 8.8831, 3.3936, 5.8333, 1.2587, 5.2234 |
| NVVar3 | float64 | 0 | 0 | 23 | -0.2723, 2.7155, 1.9685, 4.2094, 1.5204, 8.6911, 3.3131, 5.7033, 1.2216, 5.1058 |
| NVVar4 | float64 | 0 | 0 | 19 | -0.2514, 3.0687, 6.3888, 1.962, 1.4086, 1.0766, 2.4047, 0.8553, 4.1754, 0.6972 |
| log1p_claim_amount | float64 | 0 | 0 | 10662 | 0.0, 2.5422, 4.4684, 1.3335, 2.7124, 3.3793, 5.4364, 1.4268, 3.2815, 5.1176 |
| Household_ID | int64 | 0 | 0 | 959436 | 6048097, 6616483, 4826078, 6898153, 2383660, 6234757, 4239680, 6272474, 7437341… |
| Model_Year | int64 | 0 | 0 | 27 | 2004, 2002, 2005, 2003, 2000, 2001, 1999, 2006, 1998, 1997 |
| household_vehicles_carried | int8 | 0 | 0 | 11 | 1, 0, 2, 3, 4, 5, 6, 7, 8, 9 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 99.3 | 14.664 | 12.93 | 0.129 | 0.017 | log1p | 4972.7 | 5.96175e+07 | exponential |

### Numeric features

<details>
<summary>Show the table (19 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| Household_ID | 150000 | 4.07433e+06 | 2.25828e+06 | 6 | 7.526e+06 |
| Model_Year | 150000 | 1999.29 | 5.15722 | 1981 | 2007 |
| Var1 | 150000 | -0.00828215 | 0.976726 | -2.57822 | 4.54077 |
| Var2 | 150000 | -0.0677365 | 0.963456 | -2.49339 | 7.20694 |
| Var3 | 150000 | -0.0232847 | 1.01967 | -2.79034 | 5.56333 |
| Var4 | 150000 | -0.0574676 | 0.963131 | -2.50822 | 6.98037 |
| Var5 | 150000 | 0.00772883 | 0.987811 | -3.35034 | 4.00627 |
| Var6 | 150000 | -0.0385199 | 0.977279 | -2.37666 | 4.58429 |
| Var7 | 150000 | -0.0226454 | 1.0054 | -2.77849 | 3.90597 |
| Var8 | 150000 | -0.0592684 | 0.984145 | -1.95815 | 33.0366 |
| NVVar1 | 150000 | 0.00980011 | 1.01928 | -0.23153 | 6.62711 |
| NVVar2 | 150000 | 0.0197203 | 1.04377 | -0.266117 | 8.88308 |
| NVVar3 | 150000 | 0.0147238 | 1.03141 | -0.272337 | 8.69114 |
| NVVar4 | 150000 | 0.0206672 | 1.04032 | -0.251419 | 6.3888 |
| household_vehicles_2005 | 108922 | 1.92269 | 1.04283 | 1 | 12 |
| household_claims_2005 | 108922 | 0.0140651 | 0.119001 | 0 | 2 |
| vehicle_claims_2005 | 92735 | 0.00608185 | 0.0777491 | 0 | 1 |
| household_vehicles_carried | 150000 | 1.23913 | 1.06332 | 0 | 9 |
| log1p_claim_amount | 150000 | 0.0272533 | 0.358771 | 0 | 8.926 |

</details>

### Categorical features

<details>
<summary>Show the table (65 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| Blind_Make | 1 | K | 19002 | 12.67 |
| Blind_Make | 2 | AJ | 17701 | 11.8 |
| Blind_Make | 3 | BW | 14514 | 9.68 |
| Blind_Make | 4 | AU | 12222 | 8.15 |
| Blind_Make | 5 | Y | 9606 | 6.4 |
| Blind_Model | 1 | K.7 | 6916 | 4.61 |
| Blind_Model | 2 | AU.14 | 3500 | 2.33 |
| Blind_Model | 3 | X.45 | 3348 | 2.23 |
| Blind_Model | 4 | W.16 | 2576 | 1.72 |
| Blind_Model | 5 | AU.11 | 2352 | 1.57 |
| Blind_Submodel | 1 | K.7.3 | 1959 | 1.31 |
| Blind_Submodel | 2 | AU.58.0 | 1657 | 1.1 |
| Blind_Submodel | 3 | AU.14.1 | 1629 | 1.09 |
| Blind_Submodel | 4 | AU.14.0 | 1592 | 1.06 |
| Blind_Submodel | 5 | W.16.3 | 1537 | 1.02 |
| Cat1 | 1 | B | 45688 | 30.46 |
| Cat1 | 2 | I | 30175 | 20.12 |
| Cat1 | 3 | D | 28339 | 18.89 |
| Cat1 | 4 | F | 14761 | 9.84 |
| Cat1 | 5 | G | 9075 | 6.05 |
| Cat2 | 1 | C | 66772 | 44.51 |
| Cat2 | 2 | &lt;NA> | 55518 | 37.01 |
| Cat2 | 3 | A | 25084 | 16.72 |
| Cat2 | 4 | B | 2626 | 1.75 |
| Cat3 | 1 | A | 85663 | 57.11 |
| Cat3 | 2 | B | 24897 | 16.6 |
| Cat3 | 3 | C | 14408 | 9.61 |
| Cat3 | 4 | F | 10270 | 6.85 |
| Cat3 | 5 | E | 10195 | 6.8 |
| Cat4 | 1 | A | 65211 | 43.47 |
| Cat4 | 2 | &lt;NA> | 64042 | 42.69 |
| Cat4 | 3 | C | 16511 | 11.01 |
| Cat4 | 4 | B | 4236 | 2.82 |
| Cat5 | 1 | A | 75972 | 50.65 |
| Cat5 | 2 | &lt;NA> | 64095 | 42.73 |
| Cat5 | 3 | C | 9034 | 6.02 |
| Cat5 | 4 | B | 899 | 0.6 |
| Cat6 | 1 | B | 48704 | 32.47 |
| Cat6 | 2 | C | 41536 | 27.69 |
| Cat6 | 3 | D | 40955 | 27.3 |
| Cat6 | 4 | E | 13625 | 9.08 |
| Cat6 | 5 | F | 4872 | 3.25 |
| Cat7 | 1 | &lt;NA> | 81492 | 54.33 |
| Cat7 | 2 | C | 52508 | 35.01 |
| Cat7 | 3 | A | 12041 | 8.03 |
| Cat7 | 4 | B | 2707 | 1.8 |
| Cat7 | 5 | D | 1252 | 0.83 |
| Cat8 | 1 | A | 98079 | 65.39 |
| Cat8 | 2 | B | 41817 | 27.88 |
| Cat8 | 3 | C | 10067 | 6.71 |
| Cat8 | 4 | &lt;NA> | 37 | 0.02 |
| Cat9 | 1 | B | 123938 | 82.63 |
| Cat9 | 2 | A | 26062 | 17.37 |
| NVCat | 1 | M | 65686 | 43.79 |
| NVCat | 2 | O | 38782 | 25.85 |
| NVCat | 3 | N | 15206 | 10.14 |
| NVCat | 4 | L | 9061 | 6.04 |
| NVCat | 5 | J | 6285 | 4.19 |
| OrdCat | 1 | 4 | 67487 | 44.99 |
| OrdCat | 2 | 2 | 47097 | 31.4 |

(5 more rows not shown)

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
