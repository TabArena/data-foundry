---
report_format: data-foundry-report-v2
unique_name: allstate_claim_prediction_challenge_1m
container_format: 2
checksum: v2:9a7d721139b9e67d54130eae07e57a289caf6647dee29261d812998293ad30ac
build: null
build_stale: false
data:
  n_rows: 1500000
  n_features: 31
  dtypes:
    category: 14
    float64: 16
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
    n_groups: 1057582
    test_groups_per_fold:
      min: 352490
      max: 352527
splits:
  n_repeats: 1
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 1000000
    max: 1000000
  n_test:
    min: 499915
    max: 500000
  row_budget:
    train: 1000000
    test: 500000
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  - dataset_conflicting_duplicate_rows
  - groups_not_clustered
  accepted:
    groups_labels_constant: The label is one per vehicle-year and claims are rare
      (0.82%), so 98.2% of the households with two or more rows of the 2006 renewal
      book have a single label (2026-11-03; restated 2026-11-08).
    task_target_value_dominant: 'A zero-inflated target, not a cap or a placeholder:
      0 is a vehicle-year without a bodily-injury claim, 99.18% of the rows of the
      2006 renewal book (see the curation notes; 2026-11-03; restated 2026-11-08).'
decisions:
- The 2006 renewal book, with 2005 as its history
- The 2007 rows are dropped
- Missing values stay
---

# allstate_claim_prediction_challenge_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `log1p_claim_amount`, scored with `normalized_gini` on grouped splits by `Household_ID`. 1,500,000 rows and 31 features. Source: Kaggle (2011).

Not built yet. The current definition gives checksum `v2:9a7d721139b9e67d54130eae07e57a289caf6647dee29261d812998293ad30ac`.

## In brief

**Question.** How much will a vehicle renewed for 2006 cost Allstate in bodily-injury liability claims that year, on the scale Allstate adjusted the amounts to, from the vehicle's characteristics and the household's record of 2005?

**Use case.** For example, Allstate rating a vehicle for bodily-injury liability cover at the 2006 renewal: the vehicle's expected claim cost ranks its risk and sets the vehicle part of the premium, with the household's record of the year before, as an insurer prices a renewal. The competition names the target and the features, not the decision.

**One row.** One vehicle on an Allstate policy at the start of 2006, insured in 2005 too: the renewal book, 2.75 million of the 4.4 million vehicle-years of 2006 in the competition's labelled file, of which whole households holding 1.5 million are sampled. The cars that joined during 2006 are left out, and the rows of 2005 give only the history.

**Predicted.** The vehicle's bodily-injury liability claim payments in 2006, adjusted by Allstate to remove known non-vehicle effects by a rule it did not disclose, so in no currency: 0 for 99.18% of the vehicle-years. Shipped as log1p, scored on the amount.

**Known at prediction time.** The vehicle's model year and blinded make, model and submodel, 18 anonymised vehicle characteristics, 5 anonymised characteristics of the policy, and from 2005: the household's vehicles and claims, how many of its cars are on the policy at the renewal, and this car's claims.

**What the test data stands for.** All vehicles of a household stay on one side, so the test data stands for renewing households not seen in training, from the same year; the competition scored 2008 and 2009, whose claims were never published.

**Our changes to the source.** We kept the 2006 cars insured in 2005 (the renewal book) with their 2005 record as counts, without the cars that joined in 2006; dropped 2007, whose large claims look unsettled, and one exact copy; sampled whole households to the row budget; dropped the row number, the vehicle's number in the household, the year and Cat10 to Cat12, which behave like random draws; and coded missing values as missing.

> **Use case fit: approximate (a stand-in with a known gap).** Vehicle and policy attributes and the household's record of the year before, for the renewed cars. But the amounts' adjustment is undisclosed, no exposure is published, new business and unseen vehicle series go untested, and 73% of rows have a missing value the application never has. Kaggle's winners reached 0.20 Gini on 2009 against our 0.06 to 0.11 per fold, as this Gini turns on a few large claims.

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
| rows x columns | 1,500,000 x 33 |
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

The first 5 of 1,500,000 rows of the final frame (random rows: the frame is shuffled); 12 of 33 columns, the target first. Cells are cut at 40 characters.

| log1p_claim_amount | Household_ID | Model_Year | Blind_Make | Blind_Model | Blind_Submodel | Cat1 | Cat2 | Cat3 | Cat4 | Cat5 | Cat6 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 4844660 | 2005 | AJ | AJ.35 | AJ.35.2 | I | C | A | nan | nan | D |
| 0 | 2603436 | 2001 | AR | AR.41 | AR.41.5 | B | A | B | A | A | C |
| 0 | 6813927 | 2006 | AI | AI.16 | AI.16.0 | A | C | B | A | A | D |
| 0 | 6728741 | 1997 | Y | Y.10 | Y.10.0 | B | nan | A | A | A | C |
| 0 | 222974 | 2002 | X | X.38 | X.38.5 | C | C | A | C | A | B |

## Curation notes

We start with train_set.csv of the Kaggle competition (13,184,290 vehicle-years of 2005 to 2007; the 4,314,865 test rows of 2008 and 2009 were never labelled publicly) and keep the renewal book of 2006: the 2,754,936 cars insured in 2005 too, 61.9% of the 4,447,729 vehicle-years of 2006 (1,942,447 households, 22,632 claims), with 2005 as their history (decision 1; Andrej, 2026-11-03: "2006 renewal book with the 2005 history (counts)"; Lennart, 2026-11-08: "Option B: The renewal book.").

- Prediction point: when a vehicle on the policy at the start of 2006 is rated for its year of bodily-injury liability cover at the 2006 renewal. The vehicle and the policy's characteristics and the household's record of 2005 are known then; the year's claims are not. The features are anonymised vehicle and policy characteristics (data page); their timing cannot be checked further (LEAK-38).
- The renewal book (MET-14, LEAK-41; Lennart, 2026-11-08, review issue 6: B): the cars that joined during 2006, 38.1% of its vehicle-years (a new household's car, 27.4%, or a car added by a household of 2005, 10.7%), are left out, as their start is not released and they were on risk for part of the year. Followed into 2007, they claim per row in 2006 at 0.46 and 0.54 times their own 2007 rate (0.45 to 0.59 in every band of model-year age, 0.31 to 0.35 for model year 2007, the latest of them), while the cars carried from 2005 claim at 0.98 times theirs (0.91 to 1.11 by band), and 2007 repeats the shares and rates (review panel, 2026-11-08; decision 1). A target per row would price a part year for them, and no rate per year insured can be built without an exposure. The filter reads a fact of 2005, known at the renewal, never whether a car is seen in 2007. Before it, the flag `vehicle_insured_2005` alone scored a normalized Gini of 0.046 to 0.052, half or more of untuned LightGBM's 0.058 to 0.102 on all rows; the flag is now constant and gone. A car added in 2006 with the model year and submodel of a car of 2005 cannot be told apart from it: 38,728 rows of the book (1.41%) share a key that has more rows in 2006 than in 2005 (claiming at 0.69% against 0.82%), and they stay, as dropping them would select on the cars added later in the year. New business is not tested.
- The 2005 history (LEAK-10, LEAK-34): `household_vehicles_2005` and `household_claims_2005` (the household's vehicle-years and the ones with a claim), `vehicle_claims_2005` (this car's vehicle-years with a claim; the car is matched on household, model year and submodel, as `Vehicle` is no stable id) and `household_vehicles_carried` (the household's cars on the policy at the 2006 renewal, those insured in 2005 too; in the book, its number of rows). None is missing in the book. In 2006 a car whose household claimed in 2005 claims at 1.56%, one whose household did not at 0.81%; a car that claimed in 2005 at 1.89%. The rating date within the year is not published, so a 2005 claim reported after an early 2006 renewal counts as known; the share cannot be measured (as in spanish_homeowners_motor_insurance_2010_2014). On the shipped folds the history lifts untuned LightGBM from 0.097 / 0.079 / 0.056 to 0.106 / 0.091 / 0.061 on the amount, and by 0.001 to 0.003 on claim yes/no, each within one standard deviation of random predictions; `household_vehicles_carried` adds 0.001 to 0.009 of that on 3 of 3 folds (on all rows it had lowered the score by 0.004 to 0.009). On all rows the history had lifted the Gini on claim yes/no from 0.112-0.117 to 0.126-0.137; most of that lift was the shorter term of the cars that joined during 2006.
- The 2005 claim amounts are not a feature: the file gives them as read years after the renewal, and bodily-injury amounts keep growing for years (the 2007 claims above 2,000 are a third as frequent as in 2005, decision 2), so they hold more than the insurer saw at the renewal. spanish_homeowners_motor_insurance_2010_2014 keeps its previous-year home claim cost, a short-tail cover. Their gain on all rows of 2006 was within the noise (+0.001 to +0.014).
- Target `log1p_claim_amount`, log1p of `Claim_Amount`: the vehicle's claim payments of the year, "adjusted to control for known non-vehicle effects" (data page) by an undisclosed rule, so "it isn't actually in units of any major currency" (Allstate, forum thread 928; USE-5). Scored on the amount (`target_transform="log1p"`, MET-3), as in frempl_french_motor_personal_line; the competition's normalized Gini on the amount (Andrej, 2026-11-03, issue 4: A).
- 99.18% of the book's rows are 0 (none negative; Huangfu 2015, Sec. 2.0, p. 6: "only 95,605 non-zero values (about 0.73%) among the 13,184,290 records"). Little signal, decided by a few large claims (median claim 41.8, 99th percentile 2,161): untuned LightGBM scores a normalized Gini of 0.106 / 0.091 / 0.061 on the shipped folds, where a constant scores 0 and random predictions have a standard deviation of 0.023 to 0.025, and 0.022 to 0.106 over nine folds of three random household splits (mean 0.069, standard deviation 0.024). The task probe, on sides capped at 200,000 rows, finds LightGBM above the dummy on 3 of 3 splits (+0.037, SE 0.004) and its linear model and random forest at chance.
- Kaggle's leaderboard (0.2016 for the winner on 2009) is far above these folds. Most of the gap is the claims' tail: scored on claim yes/no instead of the amount, the same predictions reach about twice the Gini, and the tail of Kaggle's test years cannot be measured, as their amounts were never published. Tuning, ensembles and twice the training rows are the rest (review, issue 4).
- The 2007 rows are dropped (LEAK-24, MET-2; decision 2; confirmed by Andrej on 2026-11-03; 2007 can come back with settled amounts): at the same claim rate and median claim as 2005 and 2006, their large claims are missing. Claims above 2,000 are 0.43% of the 2007 claims against 1.31% and 1.26%, in every band of vehicle age and each of the three largest makes, and the shortfall grows toward the tail (2007 against 2005: 1.01 at the median, 0.65 at the 99th and 0.59 at the 99.9th percentile). Large bodily-injury claims are paid over years and the release gives no valuation date, so the 2007 payments are probably incomplete.
- Missing values: the source's "?" becomes missing. 73.0% of the book's rows have one; Cat2 (39.6% missing) is missing by model year (decision 3). The source removed such records from its test file and asked that models not use missingness, as "when the model is applied, all of the features will be collected" (forum thread 826), so the benchmark tests rows the application never sees (USE-8). On the 2005-2006 build, missingness carried no outcome beyond the vehicle type (a leave-one-out test by the review panel), random draws in place of the missing values scored no better, and training on complete rows only scored worse, so the rows stay; complete rows only would drop most vehicles built before 2000.
- One exact copy dropped (household 6365215's vehicle 4 in 2006, twice). Once the vehicle number and Cat10 to Cat12 are gone, 22,720 rows of the book (0.82%) repeat another row of the same household in every column, such as two vehicles of one type on one policy; a household is on one side of every fold, so they never straddle a split.
- `Row_ID` (the file's row number) and `Vehicle` dropped: the vehicle's number within its household "may not apply to the same vehicle from year to year" (data page), and its values run over every vehicle the household insured at any time in the year, including cars added after the rating, among them replacements after the row's own crash (LEAK-10). The household's count of vehicles in the year was dropped for the same reason (vehicles already insured the year before claim at 1.05% when the count rose, 0.77% otherwise); the 2005 counts take its place. `Calendar_Year` has one value and goes.
- Cat10, Cat11 and Cat12 dropped (PROV-3, CLEAN-22): the same vehicle keeps its value from one year to the next only as often as a random redraw would, and their Cramér's V with every other column and with the claim is at most 0.0024, so they are not the vehicle characteristics the data page names.
- `Household_ID` is the group column, never a feature.
- Dtypes: the blinded make, model and submodel (73, 1,167 and 2,379 levels in the book), Cat1 to Cat9, OrdCat and NVCat categorical (CLEAN-14); the rest numeric. OrdCat, the "ordered categorical vehicle variable" (data page), is categorical as the ordinals of liberty_mutual_fire_peril_loss_cost and pricing_game_2017_french_mtpl: its claim rates in the book over the levels 1 to 7 (0.14%, 0.91%, 0.71%, 0.81%, 0.74%, 0.66%, 0.24%) show no risk order.
- Note: NVCat and NVVar1 to NVVar4 are the policy's non-vehicle characteristics, for which the host expected no "main effects" but "interactions with the vehicle variables" (data page). Kept.
- Potential leak, kept on purpose (LEAK-30, weak): Var1 to Var8 and NVVar1 to NVVar4 are "mean 0 stdev 1" (data dictionary), yet over the labelled file their means are -0.065 to +0.019 and their standard deviations 0.97 to 1.04, so the host scaled them over a population we do not know, which may have taken in the test years. The yearly means of Var1 to Var8 rise from 2005 to 2007 (Var2 from -0.154 to +0.013) as the fleet's model-year mix changes; NVVar1 to NVVar4 do not rise. One shift and one scale per column; the unscaled values were never published.
- Note: 81.8% of the book's rows share every feature with a row of another household (one vehicle type, policy profile and history): natural repeats, kept (LEAK-18).
- Note: the competition rules say "Participants will not use the data for purposes unrelated to the competition"; a 2022 forum question about the licence (thread 309810) has no answer.
- Exposure (LEAK-41, MET-14; 2026-11-06, measured 2026-11-08): the release publishes no exposure; the rows are vehicle-years of the cars on the policy at the start of 2006 (the cars that joined during the year are left out, above), some cut short by a claim. The book's cars gone by 2007 had claimed at 0.98% in 2006, against 0.72% for the cars still insured; among the cars of households that continued into 2007, at 1.39% against 0.72%, as a claim ends the cover (a write-off or a replacement), while the cars whose whole household left claimed at 0.81%. Without dates a cut cannot be told from a non-renewal, so the share cut short is only bounded: at most 39.3% of the book's cars are not seen in 2007 (28.0% with their whole household), and 15.8% of the cars of households that continued are gone (11.4% of the book); without an exposure, the most a price per year would differ cannot be bounded. For these cuts the target stays per contract, the insurer's cost of the cover it wrote (Lennart, 2026-11-08, review issue 7: confirmed): a rate per year would raise the cut rows further, and none can be built. No feature carries the cut: the in-year vehicle count, which the outcome cuts, is already dropped, and `household_vehicles_carried` counts the cars on the policy from 2005 whatever their claims. The Kaggle metric is an unweighted Gini, so no weight is declared. If a later release adds an exposure, it is a realized time on risk: the rate's denominator and weight, never a feature.

Version of `allstate_claim_prediction_challenge`: We sub-sample the 2006 renewal book (2.75M rows) to 1.5M by whole households and use grouped 3-fold cross-validation, so every fold trains on about 1M and tests on about 500k rows (v2 split protocol). The households are drawn at random, not stratified (a regression target), so the claim rate stays that of the book. The 2005 history is built on the full file before the filter and the sampling.

## Splits

Default splits, grouped by household (Household_ID): 3 folds over 1.5M rows of whole households drawn at random from the 2.75M of the 2006 renewal book (claim rate 0.82%, as in the book), each training on about 1M and testing on about 500k rows with 4,006 to 4,210 claims. The task is temporal by its use case: the competition gave 2005-2007 for training and scored 2008 (public leaderboard) and 2009 (final ranking), whose claims were never published. With 2007 dropped (its large claims look unsettled) and 2005 used as the history of 2006, one labelled target year is left, so no window of a temporal split exists and the task ships under SPLIT-8 (ForcedGroupedFromTemporal): the folds hold out whole households, whose vehicles share the household's record, so random rows would put a household's other cars on both sides. Before the history was built, trained on 2005 and scored on 2006 all rows reached 0.064, inside the range of the folds by household (0.022 to 0.054 then; 0.022 to 0.106 now over nine folds of the renewal book), so the forced split shows no cost this noise can measure. What the folds do not test: new business (the cars that joined during 2006 are left out), vehicle series not seen in training (0.02% of test rows on the earlier folds), and a rating at a known date within the year. A release with dates beyond 2007 should get a temporal split. Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine"; 2026-11-03: the 2006 renewal book; Lennart, 2026-11-08: only the cars on the policy at the start of 2006).

1 repeat(s) x 3 fold(s) with seed 4267; train 1,000,000 rows, test 499,915 to 500,000 rows. Row budget: at most 1M train / 500k test rows per split.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 1000000 | 500000 |
| 0 | 1 | 1000000 | 499915 |
| 0 | 2 | 1000000 | 500000 |

## Group structure

One group is a household, "a household identification number that allows year-to-year tracking of each household" (data page): its rows are its vehicles of the 2006 renewal book (1,942,447 households, 1 to 11 rows, 1.42 on average), which share the household's 2005 record. The competition trained on 2005-2007 and scored 2008 and 2009. One target year cannot give the windows of a temporal split (see the splits), so whole households are held out: a test household is new to the model, and its history comes from 2005, as for every row. Each vehicle-year is one prediction from its own row. The label is one per vehicle-year, so it can differ within a household; 98.2% of the households with two or more rows of the book have no claim or claims of one amount, because claims are rare.

| field | value |
|---|---|
| group column | `Household_ID` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 1,057,582 |
| rows per group (min / median / max) | 1 / 1.0 / 11 |
| largest group | 0.0% of the rows |
| test groups per fold | 352,490 to 352,527 |
| groups of two or more rows with a single label | 98.2% |
| nearest neighbour in the same group | 0.1% of the rows (chance: 0.0%) |
| label variance explained by the group | 0.71 (shuffled groups: 0.70) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. The 2006 renewal book, with 2005 as its history

An insurer rates a renewal on the household's record of the year before; with 2007 dropped, 2006 is the one year that has one, and 2005 gives the counts of vehicles and claims (LEAK-10: counts only, the 2005 amounts were read years later). Only the cars insured in 2005 too stay, the cars on the policy at the start of 2006 (Lennart, 2026-11-08): the cars that joined during 2006 claim per row at about half the rate the same cars show in 2007, so they were on risk for part of the year, a term the release does not give (MET-14). The filter reads a fact of 2005, never whether a car is seen in 2007 (LEAK-41). One target year has no window for a temporal split, so whole households are held out (SPLIT-8).

| 2005 record | vehicle-years | share of the 2006 rows (%) | claim rate 2006 (%) | cars followed into 2007 | their 2006 rate / their 2007 rate |
|---|---|---|---|---|---|
| car insured in 2005 (kept) | 2754936 | 61.94 | 0.822 | 1634780 | 0.98 |
| car added by a household of 2005 (dropped) | 475645 | 10.69 | 0.622 | 334037 | 0.54 |
| car of a new household (dropped) | 1217148 | 27.37 | 0.501 | 972970 | 0.46 |
| kept: household claimed in 2005 | 38473 | 0.87 | 1.562 | 19919 | 1.03 |
| kept: household without a claim in 2005 | 2716463 | 61.08 | 0.811 | 1614861 | 0.98 |
| kept: car claimed in 2005 | 17284 | 0.39 | 1.886 | 8819 | 1 |
| kept: car without a claim in 2005 | 2737652 | 61.55 | 0.815 | 1625961 | 0.98 |

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
| 1980 | 28801 | 1 | 100 | 63.7 | 75.6 | 100 | 0 | 0.351 |
| 1985 | 127455 | 95 | 99.9 | 52.2 | 68.6 | 99.9 | 2.105 | 0.451 |
| 1990 | 351010 | 1388 | 97.8 | 37.1 | 51.5 | 99.6 | 0.36 | 0.704 |
| 1995 | 823043 | 106643 | 71.8 | 38 | 50.9 | 87 | 0.935 | 0.851 |
| 2000 | 1164546 | 515206 | 0 | 45 | 55.6 | 55.8 | 0.887 | 0.856 |
| 2005 | 260081 | 120583 | 0 | 46 | 53.6 | 53.6 | 0.906 | 0.837 |

## Bundle checks

0 error(s), 0 warning(s), 3 info (27 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 12,366 exact duplicate row(s) (0.8% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)
- **info** `dataset_conflicting_duplicate_rows`: 146 row(s) (0.0%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)
- **info** `groups_not_clustered`: Rows are no closer to their own group than chance (0.1% of nearest neighbours vs 0.0%), and the group explains no more of the label than shuffled groups (0.71 vs 0.70). (hint: The grouping may not be needed: compare IID and grouped scores with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.)

Accepted on purpose:

- `groups_labels_constant`: The label is one per vehicle-year and claims are rare (0.82%), so 98.2% of the households with two or more rows of the 2006 renewal book have a single label (2026-11-03; restated 2026-11-08).
- `task_target_value_dominant`: A zero-inflated target, not a cap or a placeholder: 0 is a vehicle-year without a bodily-injury claim, 99.18% of the rows of the 2006 renewal book (see the curation notes; 2026-11-03; restated 2026-11-08).

## Data checks

### Feature summary

<details>
<summary>Show the table (33 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| Cat7 | category | 813931 | 54.26 | 4 | C, A, B, D |
| Cat5 | category | 638453 | 42.56 | 3 | A, C, B |
| Cat4 | category | 637784 | 42.52 | 3 | A, C, B |
| Cat2 | category | 593627 | 39.58 | 3 | C, A, B |
| Cat1 | category | 3068 | 0.2 | 10 | B, I, D, F, G, A, C, E, H, J |
| Cat6 | category | 3068 | 0.2 | 5 | B, C, D, E, F |
| Blind_Make | category | 945 | 0.06 | 72 | K, AJ, BW, AU, Y, X, BO, W, L, AO |
| Blind_Model | category | 945 | 0.06 | 1142 | K.7, X.45, AU.14, W.16, AU.11, BO.38, AJ.58, AJ.52, AO.7, AJ.129 |
| Blind_Submodel | category | 945 | 0.06 | 2323 | K.7.3, AU.58.0, AU.14.0, AU.11.3, W.16.3, K.7.0, AU.14.1, K.7.1, BW.3.0, BW.115… |
| OrdCat | category | 736 | 0.05 | 7 | 4, 2, 5, 3, 1, 6, 7 |
| Cat3 | category | 485 | 0.03 | 6 | A, B, C, E, F, D |
| Cat8 | category | 394 | 0.03 | 3 | A, B, C |
| Cat9 | category | 0 | 0 | 2 | B, A |
| NVCat | category | 0 | 0 | 15 | M, O, N, L, J, E, F, B, H, K |
| Var1 | float64 | 0 | 0 | 331 | -0.7141, -0.7704, -0.6338, -0.3927, -0.1195, 0.5876, -0.2802, -0.2963, -0.4891,… |
| Var2 | float64 | 0 | 0 | 286 | 0.0484, 0.2213, -0.6432, -0.2974, -0.9891, -0.8162, -0.1245, -1.2484, -0.5568, … |
| Var3 | float64 | 0 | 0 | 191 | -1.2399, -1.2862, -0.4532, -0.9622, 0.2179, -0.6151, 1.0972, -1.078, -0.3837, -… |
| Var4 | float64 | 0 | 0 | 283 | 0.1472, 0.3164, -0.5293, -0.6985, -0.0219, 0.4855, -0.3602, -1.2904, 0.2318, -1… |
| Var5 | float64 | 0 | 0 | 636 | 0.5272, -0.1567, -0.1984, -0.1151, 0.6997, 0.5034, -0.0437, 0.3785, 0.5807, -0.… |
| Var6 | float64 | 0 | 0 | 2445 | -0.6794, -0.5858, -1.1964, -0.6888, -0.5461, -1.1344, -1.0654, -0.2887, -0.6268… |
| Var7 | float64 | 0 | 0 | 348 | -0.9353, -0.5913, -0.8616, -0.837, -0.9845, -0.8125, -1.0582, -0.8985, -1.0091,… |
| Var8 | float64 | 0 | 0 | 5490 | -0.2536, -0.218, -0.3315, -0.2979, -0.3843, -0.2249, -0.3495, -0.3515, -0.3085,… |
| NVVar1 | float64 | 0 | 0 | 22 | -0.2315, 3.1978, 2.0547, 1.4831, 6.6271, 1.1402, 2.5119, 0.9116, 4.3409, 0.7483 |
| NVVar2 | float64 | 0 | 0 | 23 | -0.2661, 2.7836, 2.0212, 4.3085, 1.5637, 3.3936, 8.8831, 5.8333, 1.2587, 5.2234 |
| NVVar3 | float64 | 0 | 0 | 25 | -0.2723, 2.7155, 1.9685, 4.2094, 1.5204, 3.3131, 8.6911, 5.7033, 1.2216, 5.1058 |
| NVVar4 | float64 | 0 | 0 | 23 | -0.2514, 3.0687, 1.962, 1.4086, 6.3888, 1.0766, 2.4047, 0.8553, 4.1754, 0.6972 |
| household_vehicles_2005 | float64 | 0 | 0 | 12 | 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 |
| household_claims_2005 | float64 | 0 | 0 | 3 | 0.0, 1.0, 2.0 |
| vehicle_claims_2005 | float64 | 0 | 0 | 3 | 0.0, 1.0 |
| log1p_claim_amount | float64 | 0 | 0 | 12258 | 0.0, 1.806, 3.75, 0.9188, 3.134, 1.0294, 2.6623, 4.4651, 5.9314, 2.4548 |
| Household_ID | int64 | 0 | 0 | 1.05758e+06 | 2628554, 2559242, 6231746, 6560893, 2777633, 2155351, 227307, 6278868, 2446870,… |
| Model_Year | int64 | 0 | 0 | 26 | 2004, 2002, 2001, 2000, 2003, 2005, 1999, 1998, 1997, 1995 |
| household_vehicles_carried | int64 | 0 | 0 | 11 | 1, 2, 3, 4, 5, 6, 7, 8, 11, 9 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 99.19 | 13.665 | 11.99 | 0.133 | 0.019 | log1p | 5614.8 | 1.50217e+06 | exponential |

### Numeric features

<details>
<summary>Show the table (19 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| Household_ID | 150000 | 4.42064e+06 | 2.21533e+06 | 6 | 7.51905e+06 |
| Model_Year | 150000 | 1998.79 | 4.96008 | 1981 | 2006 |
| Var1 | 150000 | -0.0187882 | 0.980763 | -2.57822 | 5.14339 |
| Var2 | 150000 | -0.113193 | 0.937554 | -2.45881 | 7.20694 |
| Var3 | 150000 | -0.0470443 | 1.02411 | -2.74405 | 5.56333 |
| Var4 | 150000 | -0.101097 | 0.937682 | -2.45748 | 6.98037 |
| Var5 | 150000 | -0.000562013 | 0.989035 | -3.35034 | 3.86354 |
| Var6 | 150000 | -0.0653475 | 0.968373 | -2.33455 | 4.58429 |
| Var7 | 150000 | -0.0390669 | 1.00806 | -2.77849 | 3.90597 |
| Var8 | 150000 | -0.0920556 | 0.983703 | -2.16304 | 34.6775 |
| NVVar1 | 150000 | -0.0142889 | 0.934439 | -0.23153 | 6.62711 |
| NVVar2 | 150000 | -0.000790603 | 0.955985 | -0.266117 | 8.88308 |
| NVVar3 | 150000 | -0.0141102 | 0.922447 | -0.272337 | 8.69114 |
| NVVar4 | 150000 | -0.00749821 | 0.954868 | -0.251419 | 6.3888 |
| household_vehicles_2005 | 150000 | 1.94079 | 1.04443 | 1 | 12 |
| household_claims_2005 | 150000 | 0.0139733 | 0.119072 | 0 | 2 |
| vehicle_claims_2005 | 150000 | 0.00605333 | 0.0775676 | 0 | 1 |
| household_vehicles_carried | 150000 | 1.738 | 0.869169 | 1 | 11 |
| log1p_claim_amount | 150000 | 0.0298532 | 0.364621 | 0 | 8.27794 |

</details>

### Categorical features

<details>
<summary>Show the table (63 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| Blind_Make | 1 | K | 18965 | 12.64 |
| Blind_Make | 2 | AJ | 17985 | 11.99 |
| Blind_Make | 3 | BW | 14388 | 9.59 |
| Blind_Make | 4 | AU | 12186 | 8.12 |
| Blind_Make | 5 | Y | 9564 | 6.38 |
| Blind_Model | 1 | K.7 | 7039 | 4.69 |
| Blind_Model | 2 | X.45 | 3421 | 2.28 |
| Blind_Model | 3 | AU.14 | 3378 | 2.25 |
| Blind_Model | 4 | W.16 | 2643 | 1.76 |
| Blind_Model | 5 | AU.11 | 2382 | 1.59 |
| Blind_Submodel | 1 | K.7.3 | 2044 | 1.36 |
| Blind_Submodel | 2 | AU.58.0 | 1733 | 1.16 |
| Blind_Submodel | 3 | AU.14.0 | 1731 | 1.15 |
| Blind_Submodel | 4 | AU.11.3 | 1662 | 1.11 |
| Blind_Submodel | 5 | W.16.3 | 1564 | 1.04 |
| Cat1 | 1 | B | 45558 | 30.37 |
| Cat1 | 2 | I | 29358 | 19.57 |
| Cat1 | 3 | D | 28858 | 19.24 |
| Cat1 | 4 | F | 15437 | 10.29 |
| Cat1 | 5 | G | 9164 | 6.11 |
| Cat2 | 1 | C | 62710 | 41.81 |
| Cat2 | 2 | &lt;NA> | 59310 | 39.54 |
| Cat2 | 3 | A | 25445 | 16.96 |
| Cat2 | 4 | B | 2535 | 1.69 |
| Cat3 | 1 | A | 88108 | 58.74 |
| Cat3 | 2 | B | 21700 | 14.47 |
| Cat3 | 3 | C | 15300 | 10.2 |
| Cat3 | 4 | E | 10844 | 7.23 |
| Cat3 | 5 | F | 9170 | 6.11 |
| Cat4 | 1 | A | 64878 | 43.25 |
| Cat4 | 2 | &lt;NA> | 63815 | 42.54 |
| Cat4 | 3 | C | 16934 | 11.29 |
| Cat4 | 4 | B | 4373 | 2.92 |
| Cat5 | 1 | A | 76052 | 50.7 |
| Cat5 | 2 | &lt;NA> | 63878 | 42.59 |
| Cat5 | 3 | C | 9122 | 6.08 |
| Cat5 | 4 | B | 948 | 0.63 |
| Cat6 | 1 | B | 47806 | 31.87 |
| Cat6 | 2 | C | 42360 | 28.24 |
| Cat6 | 3 | D | 41029 | 27.35 |
| Cat6 | 4 | E | 13445 | 8.96 |
| Cat6 | 5 | F | 5061 | 3.37 |
| Cat7 | 1 | &lt;NA> | 81545 | 54.36 |
| Cat7 | 2 | C | 52194 | 34.8 |
| Cat7 | 3 | A | 12116 | 8.08 |
| Cat7 | 4 | B | 2725 | 1.82 |
| Cat7 | 5 | D | 1420 | 0.95 |
| Cat8 | 1 | A | 99711 | 66.47 |
| Cat8 | 2 | B | 40309 | 26.87 |
| Cat8 | 3 | C | 9943 | 6.63 |
| Cat8 | 4 | &lt;NA> | 37 | 0.02 |
| Cat9 | 1 | B | 128138 | 85.43 |
| Cat9 | 2 | A | 21862 | 14.57 |
| NVCat | 1 | M | 67436 | 44.96 |
| NVCat | 2 | O | 36592 | 24.39 |
| NVCat | 3 | N | 15820 | 10.55 |
| NVCat | 4 | L | 8817 | 5.88 |
| NVCat | 5 | J | 6870 | 4.58 |
| OrdCat | 1 | 4 | 67593 | 45.06 |
| OrdCat | 2 | 2 | 47475 | 31.65 |

(3 more rows not shown)

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
