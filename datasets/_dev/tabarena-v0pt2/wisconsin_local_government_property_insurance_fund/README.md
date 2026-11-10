---
report_format: data-foundry-report-v2
unique_name: wisconsin_local_government_property_insurance_fund
container_format: 2
checksum: v2:efc2f81142f88ea6137ac4a6ddb29d663f9dce402e1e1e7e49a31785abd2e577
build: null
build_stale: false
data:
  n_rows: 5639
  n_features: 9
  dtypes:
    category: 5
    float64: 4
    int64: 2
  n_test_dataset_rows: null
task:
  target: bc_claims
  problem_type: regression
  metric: ordered_lorenz_gini
  metric_origin: source
  scoring_columns:
  - Premium
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: Year
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 3
  n_folds: 1
  random_state: 4267
  time_horizon: 1
  time_horizon_unit: years
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 2292
    max: 4529
  n_test:
    min: 1110
    max: 1125
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - meta_time_horizon_unit
  accepted:
    task_time_on_few_unique: 'Five policy years, 2006-2010, the whole time axis of
      the file: the yearly windows train on two to four earlier years, and the file
      has no finer time.'
    meta_license_unknown: 'The first edition''s repository, which holds the shipped
      file, has no licence file (GitHub API, 2026-11-01), and its book pages state
      none. The second edition named in the download description (OpenActTexts/LDAVer2,
      WiscPropFund.csv: the same rows with fewer columns) has a CC0-1.0 LICENSE in
      its repository (committed 2024-10-03), and its book pages state CC BY 4.0; the
      rows can be taken from it if the release needs a stated licence.'
    task_target_value_dominant: '70.2% zeros: member-years without a building and
      contents claim (`Freq` 0), real no-claim years and not a cap or a placeholder;
      the batch''s other zero-inflated targets are accepted on the same ground (Andrej,
      2026-11-03).'
decisions:
- The fund's premium is the metric's base, never an input
- The yearly claims agree with the claim-level file
- Three yearly windows, the oldest below half the rows
---

# wisconsin_local_government_property_insurance_fund

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `bc_claims`, scored with `ordered_lorenz_gini` on temporal splits by `Year`. 5,639 rows and 9 features. Source: GitHub (2017).

Not built yet. The current definition gives checksum `v2:efc2f81142f88ea6137ac4a6ddb29d663f9dce402e1e1e7e49a31785abd2e577`.

## In brief

**Question.** What will a Wisconsin local government member's building and contents claims cost the state's property fund in the coming year, from the rating variables the fund holds when it sets the year's premium?

**Use case.** The actuaries of Wisconsin's Local Government Property Insurance Fund set each county, city, town, village, school district or other member's premium relativity for the coming year. A new rating is adopted when it moves premium toward the members whose claims outrun what they pay now; the source built such a rating engine for the fund and scored it against the fund's premium.

**One row.** One member's building and contents cover in one year, 2006 to 2010 (5,639 member-years of 1,227 members; 1,038 members are in all five years).

**Predicted.** The year's total building and contents claims, in dollars: 0 for 70% of the member-years, up to $12.9 million. A prediction is scored by how it reorders the members against the fund's premium for the year.

**Known at prediction time.** The member itself, its type, the year's coverage amount and the deductible it chose, whether its fire protection class is below 5, its alarm credit, whether it had a claim in the two years before (unknown where the file does not hold both years), its claim count of the year before (unknown where the file does not hold that year), and the year.

**What the test data stands for.** Each of the policy years 2008, 2009 and 2010 is held out in turn, and the model trains on every earlier year, as the fund rates the members it knows for the next year. The 2008 window trains on 2006-2007 alone, 41% of the rows.

**Our changes to the source.** We drop the claim count and the other restatements of the year's claims, keep the fund's premium out of the inputs as the yardstick of the score, mark the no-claim credit unknown where the file lacks the member's two earlier years, and add the member's claim count of the year before.

> **Use case fit: approximate (a stand-in with a known gap).** The inputs are the rating variables the fund holds at renewal, the label is the year's claims and the test is the next year, but the training years carry final claim amounts the fund knew only in part when it rated, and the public file lacks inputs the fund rates on: the endorsements, the member's county and the full fire class.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`REVIEW.md`](REVIEW.md) | The open questions for the curator, removed once they are settled. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/wisconsin_local_government_property_insurance_fund.md`](../../../../curation/records/wisconsin_local_government_property_insurance_fund.md)
- The original source: <https://github.com/OpenActTexts/Loss-Data-Analytics/blob/38859ed741b21d41a26b5abb668e1172c088a216/Data/PropertyFundInsample.csv>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/wisconsin_local_government_property_insurance_fund/`. To get them:

```text
The open textbook Loss Data Analytics (Open Actuarial Textbooks project, E.W. Frees and co-authors) ships the
data of its Wisconsin Property Fund case study (Ch. 1) in its GitHub repository. We pin the repository's first
commit (2017-06-27), whose two files are still the ones on master (commit 32310ad, 2026-11-01).
PropertyFundInsample.csv holds one row per member and year, 2006-2010; Insample.csv in the same folder is a
byte-identical copy, and WiscPropFund.csv of the second edition (OpenActTexts/LDAVer2) holds the same rows
with fewer columns. CLAIMLEVEL.csv holds the individual claims, used only to check the yearly totals.

mkdir -p local-data-warehouse/wisconsin_local_government_property_insurance_fund && cd local-data-warehouse/wisconsin_local_government_property_insurance_fund
for f in PropertyFundInsample.csv CLAIMLEVEL.csv; do wget https://raw.githubusercontent.com/OpenActTexts/Loss-Data-Analytics/38859ed741b21d41a26b5abb668e1172c088a216/Data/$f; done
sha256sum PropertyFundInsample.csv CLAIMLEVEL.csv
# 436cc782e87b401e34d00c4d5e7cf801c683f7063c5018fc2d067c104e0b1c96  PropertyFundInsample.csv
# e338a1bd130cb07ffdb2e6a82af8b5eef393cfc703e9a2cf90758c12c5246c95  CLAIMLEVEL.csv
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/wisconsin_local_government_property_insurance_fund   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/wisconsin_local_government_property_insurance_fund   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | GitHub: https://github.com/OpenActTexts/Loss-Data-Analytics/blob/38859ed741b21d41a26b5abb668e1172c088a216/Data/PropertyFundInsample.csv |
| year | 2017 |
| domain | insurance |
| license |  |
| data_tags | Non-IID, Temporal |
| reference | OpenActTexts2017LossDataAnalytics |
| rows x columns | 5,639 x 11 |
| task.target | bc_claims |
| task.problem_type | regression |
| task.metric | ordered_lorenz_gini |
| task.split_regime | temporal_non_iid |
| task.time_on | Year |

**Metric**

| field | value |
|---|---|
| name | `ordered_lorenz_gini` (custom; takes value; higher is better) |
| origin | source: the source's metric |
| original | Gini index of the ordered Lorenz curve with the fund's premium as base: members sorted by the relativity score / premium, cumulative premium share against cumulative claims share (Frees, Meyers and Cummings 2011, JASA 106:1085-1098), computed with the premium the fund collected as the denominator |
| reference | https://doi.org/10.3390/risks4010004 |
| definition | twice the area between the ordered Lorenz curve and the diagonal: rows sorted by the relativity p / B (B the base premium, the weight), x the cumulative share of B, y the cumulative share of the losses y; 0 when p adds nothing to B (tied relativities form one step); per_unit: y and p are per unit of B, rows sorted by p and x the cumulative share of B (the unnormalised weighted Gini of a rate) |
| inputs | weight: `Premium` |

**Scoring columns**

Kept in the frame for the metric; do not use them as features. Drop them from the inputs (`feature_columns(container)`), then pass the test rows' values to the scorer (`data_foundry.v2.metrics.scorer(container)(y_test, y_pred, test_idx)`).

| column | role | how the metric uses it | model input |
|---|---|---|---|
| `Premium` | weight | ordered_lorenz_gini: the fund's building and contents premium for the member-year, the base of the source's Gini: members are sorted by prediction / Premium and the cumulative share of the claims is set against the cumulative share of the premium. Never a feature: it is the output of the rating the task replaces. | never a feature |

The test-row values of `Premium` are for the scorer only: never read them when predicting a test row.

<details>
<summary>Feature types: 5 categorical, 0 string, 0 datetime</summary>

- categorical (5): `PolicyNum`, `EntityType`, `AlarmCredit`, `Fire5`, `NoClaimCredit`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{OpenActTexts2017LossDataAnalytics,
  title = {Loss Data Analytics},
  author = {{Open Actuarial Textbooks Project}},
  year = {2017},
  howpublished = {\url{https://github.com/OpenActTexts/Loss-Data-Analytics}},
  note = {Ch. 1, Case Study: Wisconsin Property Fund; data file PropertyFundInsample.csv, first committed on 27 June 2017. The task and its metric: E.W. Frees, G. Lee and L. Yang, Multivariate Frequency-Severity Regression Models in Insurance, Risks 4(1):4, 2016, doi:10.3390/risks4010004}
}
```

</details>

## Sample rows

The first 5 of 5,639 rows of the final frame (the oldest rows: the frame is sorted by `Year`). Cells are cut at 40 characters.

| bc_claims | PolicyNum | Year | LnCoverage | Premium | lnDeduct | Fire5 | NoClaimCredit | EntityType | AlarmCredit | prev_year_claims |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 120027 | 2006 | 3.07427 | 13196 | 8.51719 | 0 | nan | County | 0 | nan |
| 0 | 160817 | 2006 | 0.569525 | 1838 | 6.21461 | 0 | nan | Village | 0 | nan |
| 0 | 133542 | 2006 | 2.25794 | 3920 | 8.51719 | 1 | nan | School | 5 | nan |
| 48060.8 | 120008 | 2006 | 3.82976 | 21644 | 6.21461 | 1 | nan | County | 15 | nan |
| 812 | 160030 | 2006 | 1.58076 | 3790 | 6.21461 | 1 | nan | Village | 0 | nan |

## Curation notes

We start with PropertyFundInsample.csv of the open textbook Loss Data Analytics (OpenActTexts on GitHub), the building and contents (BC) cover of Wisconsin's Local Government Property Insurance Fund, 2006-2010: a close extract of the sample Frees, Lee and Yang (2016, Risks 4:4, Sec. 5) model (5,639 member-years with 1,679 claimants, against their 5,660 and 1,684).

- Prediction point: the start of a policy year, when the fund rates the member for the year. The member's type, the year's coverage and deductible, its fire class, its alarm credit and the no-claim credit are known then; the year's claims are not. The fund's rating project wanted "a more accurate and cost efficient rating engine" (Lee 2017, UW-Madison dissertation advised by Frees, Ch. 1).
- Year: the rows were first published in the textbook's repository on 2017-06-27 (its first commit); Frees, Lee and Yang (2016) analyse them but publish no data, and the fund's project site offers none.
- `Freq`, `lny` and `yAvg` dropped: the year's claim count (0 exactly where the claims are 0), the log of the claims and the average claim restate the target.
- `BCcov` and `Deduct` dropped: `LnCoverage` is the log of the coverage in millions (within 5e-10) and `lnDeduct` the log of the deductible, the forms the source models them in (Lee 2017, Table 5.8).
- `Premium` (the fund's premium for the year) is the base of the metric, a scoring column and never an input. The source's models take the rating variables only (Lee 2017, Table 5.8) and are scored against the premium (Frees, Lee and Yang 2016, Sec. 6.2: "The Gini index is calculated using relativities computed with the actual premium collected by the LGPIF in 2011 as the denominator, with the scores predicted by each model as numerator. This means we are looking for improvements over the original premium scores used by the LGPIF"). The premium is the output of the rating the task replaces: a linear fit on the rating variables explains 98.1-98.5% of the variance of its log within each year (decision 1). As in 2_month_survival_rate_prediction, a comparator of the source is no input (USE-6). The premium is an outside agency's price: "a Premium variable that was generated by an external agency (based on a very expensive process)" (Frees and Lee 2016, Rating Endorsements Using Generalized Linear Models, Variance 10(1), Sec. 5), which the project's engine was built to reproduce and replace (Lee 2017, Ch. 1 and Table 7.9, "Rating Agency Premium"). As an input it is no leak and gains nothing (REVIEW.md issue 4, 2026-11-09): what the rating variables leave of it follows a claim in the year before (+0.008 in log premium, SE 0.004) and not one in its own year (+0.000, SE 0.004); with it as a feature the Tweedie GLM of the notes scores a mean Gini of 0.283 against 0.285 without, each window within its bootstrap SE, and LightGBM within noise or lower.
- The six entity-type flags become `EntityType` and the four alarm-credit flags `AlarmCredit` (0, 5, 10 or 15% credit): exactly one flag of each block is set in every row, so the merge is lossless (CLEAN-13).
- `PolicyNum`, the member, is an input: the fund rates the members it has insured before (USE-10), and 97.6-98.8% of each test year's members are in its training years. Its first two digits are the entity type. An untuned LightGBM Tweedie scores 0.146, 0.254 and 0.327 with it (test 2008, 2009, 2010) and 0.146, 0.221 and 0.081 without; the gap is in 2010 alone, and there it is where a model ranks one member: the Milwaukee school of the $12.9M claim (35% of the year's claims), whose training years held small claims ($0, $53k, $11k, $0). Without that row the model without `PolicyNum` scores higher (0.342 against 0.257; LightGBM Tweedie bagged over 5 seeds, REVIEW.md issue 6), so the 2010 gap is no measure of what the member id is worth.
- `NoClaimCredit` is 1 exactly when the member had no claim in the two years before, wherever both years are in the file (1,852 rows against 0, and 0 against 1,375): history known at rating time. It looks computed from the file's own claims rather than read from the fund's rating (0 on every 2006-2007 row, where the file lacks the two years; REVIEW.md issue 5), so it shows what the fund could know, not that the fund rated on it. Where the file lacks one of the two years it is 0 (all 2,292 rows of 2006-2007 and 119 of the 120 later ones; one member with a gap year has 1), which says only that the history is not in the file, and a linear model would read it as "had a claim". These 2,412 rows are set missing (CLEAN-10, as house_sales). The 2008 window trains on 2006-2007 alone, so its training side holds no known credit and the column informs only the 2009 and 2010 windows.
- Added: `prev_year_claims`, the member's claim count of the year before (`Freq` of the same `PolicyNum` and `Year` - 1), missing where the file does not hold that year: every 2006 row and 1.3% to 2.7% of the later rows (members new to the file or back after a gap). History the fund holds when it rates (USE-10, LEAK-34; Andrej, 2026-11-09, REVIEW.md issue 5 (b)). Of the 4,408 member-years with the year before in the file, 54.7% have a claim after a claim in the year before against 21.1% after none (53.4% against 15.7%, 50.2% against 18.0% and 60.5% against 27.4% in the test years 2008, 2009 and 2010), and it is known for 1,110, 1,082 and 1,094 of their 1,125, 1,112 and 1,110 test member-years. Measured on a scratch copy of the shipped frame (2026-11-09; the shipped windows, the declared Gini; mean over 2008, 2009, 2010): the Tweedie GLM of the notes scores 0.260 with it against 0.285 without (by window -0.054, +0.019 and -0.038, paired bootstrap SE 0.041 to 0.056), the untuned LightGBM Tweedie 0.221 against 0.242, a bagged LightGBM (3 seeds) 0.206 against 0.205 (seed SD 0.015 and 0.031): every difference within noise. The task probe's untuned families, re-run with it (2026-11-09), move the other way: linear 0.202 against 0.119, random forest 0.202 against 0.142, LightGBM 0.073 against 0.020 (means over the 3 windows, SD across windows 0.075 to 0.152), the count the best single feature in every window (0.086 against 0.032 for `EntityType`): no direction holds across model families, so the count is added for fidelity, not for a measured gain. The member id already lets a model learn each member's level from its training years (without `PolicyNum` the count lifts the LightGBM from 0.149 to 0.178), and the premium, the Gini's base, rises after a claim the year before. The count is close to final at rating time; the year before's amount stays out, since the file holds final amounts of claims that may have been open at renewal and cannot mark them (LEAK-10). In the 2008 window the count is known only on the 2007 training rows.
- `Fire5` is 1 when the fire protection class (0 to 10) is below 5. The claim-level file, which covers claimants only, shows the unknown class -99 coded as 1 for 48 claimant members (66 member-years). It stays as published: the unknowns can be found only among members with a claim, so blanking them would tell the outcome (LEAK-10 before CLEAN-10). `Fire5` and `NoClaimCredit` hold only 0 and 1 (and missing): categorical.
- The coverage of a year is set before its claims: the change of log coverage from the year before is +0.059 with a claim in the year and +0.061 without (+0.052 with a claim in the top 10%). It grew about 5% a year in 2007-2009; in 2010 it fell for 67.7% of the members (median -2.6%).
- Exposure: `Premium` is the rating's output and the base of the Lorenz curve, not an amount at risk. The target is a total and the premium is set at the start of the year (not realized), so MET-15 asks for no training weight, and none is declared; an unweighted fit of the total estimates E[y|x], which the Lorenz curve then divides by the premium. The premium is a scoring column only, never an input (MET-2, the note above). The coverage (`LnCoverage`, the log of the building and contents sum insured, set for the year at renewal) stays a feature, not an offset: the source estimates its coefficient rather than fixing it at 1, as its general definition of an exposure offset would (Frees, Lee and Yang 2016, Sec. 2.2, p. 5; Table 11, p. 19: 0.853 in the negative binomial frequency part and 0.136 in the GB2 severity part, an implied elasticity of the expected claims of about 0.99 before the zero-one inflation); GLMs on this file with coverage, deductible, entity type, no-claim credit, `Fire5`, alarm credit and year give it 1.14 for the claim count (Poisson) and 0.67 for a Tweedie fit of the total (coverage alone: 1.01 and 0.77-0.82); and a feature lets a model learn any elasticity. Rows are member-years with no time at risk. Whether a member joined or left during a year cannot be located row by row; the exit years show no claim shortfall (observed/expected 0.93, z -0.46; permanent exits 0.86, z -0.85), the entry years no excess beyond chance (1.22, z 1.07), and the premium is not prorated in either. 48 members appear in one year only (54 in two, 55 in three, 32 in four, 1,038 in all five).
- Target `bc_claims`, `y`, the year's total BC claims in dollars; 70.2% of the member-years are 0, none is negative. Dollars rather than the log scale CLEAN-16 defaults to: the metric divides each prediction by the premium, so a prediction's size counts, not only its order; the source models dollars (Tweedie and GB2 models), and the fund prices from expected dollars (MET-3, USE-5). On the three yearly windows (test 2008, 2009, 2010) an untuned LightGBM fit on dollars with a Tweedie loss scores 0.146, 0.254 and 0.327, the same model fit on log1p with squared error -0.049, 0.248 and 0.016, an untuned Tweedie GLM on dollars 0.254, 0.251 and 0.350.
- Note: the task probes flag no_signal, scored by R^2 on dollars, which follows a few large claims (random forest 0.234, SD 0.28 across the windows; linear 0.032): even the true claim indicator times the training claimants' mean reaches R^2 0.007 to 0.038 on the windows. Both parts carry signal (untuned LightGBM, test 2008, 2009, 2010): a claim is ranked at ROC AUC 0.791, 0.774 and 0.760 (log coverage alone 0.745, 0.738, 0.736), the log claims of the claimants at R^2 0.054, 0.095 and 0.221. The leak probes find nothing: every feature alone at R^2 0.027 or below (`prev_year_claims`; 0.014 before it was added, 2026-11-09), no test row with an exact copy of its inputs in training. Since the count was added the task probes also flag `unstable`: the random forest's R^2 skill beats the dummy in 2 of the 3 windows.
- The totals match the claim-level file: CLAIMLEVEL.csv (6,258 BC claims) sums to the year's claims within $1 for 5,633 of the 5,639 member-years (decision 2); 4 of the 6 others hold claim lines that look duplicated in the claim-level file (82,532.36 = 2 x 41,266.18). `y` is kept as published; how mature it is, below.
- CLAIMLEVEL.csv also names each claimant's county, but only for the 759 members with a claim, so it is not joined: its missingness would tell the outcome.
- Note: how mature the labels are (cross-dataset item of 2026-11-09, Andrej): `y` sums closed claims only: the book keeps "only claims that are closed, with obligations fully met" (Ch. 1) and CLAIMLEVEL.csv marks all 6,258 claim lines `Closed`; a claim open when the file was made is missing from its year (LEAK-24). With no extraction or closure date, the share open on 1 January of a test year cannot be counted; the training years carry final amounts where the fund rated with part of them (splits_comment). Both sides come from one extract, and 2010, the newest year, has the highest claim share (36.3%, 26.8% to 31.4% before): no shortfall shows.
- Note: held for training rows only, not shipped (cross-dataset item of 2026-11-09, Andrej): `Freq`, the year's claim count behind `y` (6,255 claims on 1,679 member-years), and the claim lines of CLAIMLEVEL.csv (6,258 BC claims), each with its amount, its peril in `Description` and its `CoverageCode`. The fund holds them for the years it has closed when it fits, but not for the year it rates. They would need a training-only role, which the format does not have yet (MET-14, LEAK-41, MET-16), so they stay out for now.
- Metric: the source's Gini of the ordered Lorenz curve with the fund's premium as the base (`ordered_lorenz_gini`; Frees, Meyers and Cummings 2011; Frees, Lee and Yang 2016, Sec. 6.2), not normalized, as the source reports it: a prediction that adds nothing to the premium (the premium itself) scores 0.000 in every window, while a constant prediction, which orders the members by the inverse of their premium, is a different baseline: -0.004, -0.124 and 0.061 (test 2008, 2009, 2010). The source argues for it (it measures "the satisfaction of the fund manager with each score", and with "large masses at zero ... traditional metrics are less helpful", Sec. 3), and Lee (2017) concludes by it; the Spearman correlation reported beside it (Sec. 6.1, Table 18) ignores the premium (MET-5). Sorting by coverage alone is the level a model must beat, and a high one. On the three yearly windows (test 2008, 2009, 2010) coverage in dollars scores 0.019, 0.195 and 0.540 (mean 0.251), an untuned Tweedie GLM 0.254, 0.251 and 0.350 (mean 0.285), an untuned LightGBM Tweedie 0.146, 0.254 and 0.327 (mean 0.242); coverage leads only in 2010, the storm year. The best monotone fit of one feature chosen on the training side (log coverage in every window) scores 0.094, 0.141 and 0.461 and beats the GLM only in 2010, so the task is not `Trivial` (TP-4). Before the split changed, models tuned on the training side reached 0.324 (2009) and 0.350 (2010) without `PolicyNum`. These models stand in for the benchmark's tuned methods, which have no results here yet (TP-1). Each window's score turns on its largest claim: without that one row (left out only to measure the swing; leaving a row out by its outcome is no remedy) LightGBM Tweedie bagged over 5 seeds moves from 0.133 to 0.147 (2008), from 0.253 to 0.110 (2009, a $2.16M claim, 20% of the year's) and from 0.250 to 0.257 (2010; without `PolicyNum` from 0.108 to 0.342), and the constant in 2010 from 0.061 to -0.218. The losses stay uncapped in scoring, as the source scores them and as frempl_french_motor_personal_line keeps its largest claim (CC 2026-11-10). The first tuned benchmark run decides: the table stays if tuned methods spread beyond that swing of about 0.1 to 0.3 per window (TP-3), and is retired for that reason otherwise (TP-2).
- Anomaly: 2010 was a year of severe weather (Lee 2017, Ch. 1): $36.7M of claims against $11.0M-20.5M in 2006-2009, and one water damage claim at a Milwaukee school, $12.9M, is 35% of the year's claims. Kept as recorded; it is in the 2010 window, and that window's score moves with where it is ranked.
- CC (2026-11-09, Andrej): the fund's premium stays a scoring column only, the Gini's base and no input (REVIEW.md issue 4 (a), "Scoring column only"): it is the outside agency's price the project's engine replaces, and as an input it is no leak and gains nothing.
- CC (2026-11-09, Andrej): `prev_year_claims`, the member's claim count of the year before, is added (REVIEW.md issue 5 (b), "The previous year's claim count"); the year before's amount stays out.
- CC (2026-11-10, Andrej): the losses stay uncapped in scoring, with each window's one-row swing in the notes, and the first tuned benchmark run decides whether the table tells methods apart (REVIEW.md issue 6 (A), "Uncapped, with notes and a gate").

## Splits

Three expanding yearly windows, newest first: test 2010 trained on 2006-2009 (4,529 rows, 80.3%; 1,110 test
member-years, 403 with a claim), test 2009 on 2006-2008 (3,417 rows, 60.6%; 1,112, 301) and test 2008 on
2006-2007 (2,292 rows, 40.6%; 1,125, 309). The fund rates the members it knows once a year for the next year,
and the source tested on the next year, 2011, which is not public. The 2008 window trains on 40.6%, below half
the rows, as SPLIT-14 allows since its amendment of 2026-11-08 (Lennart, on this fund, REVIEW.md issue 3: two
windows above the floor, 97.6% to 98.8% of each test year's members in earlier years, and member folds leaked
the year's claim level): the curator's call of 2026-11-02 (Andrej), after the leak test found the year's claim
level shared across the member folds the definition shipped before ("We found that grouped splits leak, so I
would recommend to use three splits, one for each year of 2008, 2009, 2010"), kept ("We think the task is too
good to remove because of the 50% floor", Lennart, 2026-11-06). The short window changes the order of the two
simplest predictors: on the two windows above the floor coverage alone (0.368) beats a Tweedie GLM (0.312), with
the 2008 window the GLM comes first (0.291 against 0.251). In that window the no-claim credit is unknown on
every training row (the file starts in 2006), so it informs only the two later windows. No test year has a row
on its training side, and no gap separates the sides. Exception to SPLIT-10 (2026-11-08, Lennart): every policy
year ships with its final claim amounts, so no label is selected by the release end, and a one-year gap would
leave the 2009 window 2006-2007 and the 2008 window one year, below the floor in two of the three windows; it
serves SPLIT-14. The training years carry final claim amounts, which the fund knew only in part when it rated
(fit approximate). Members recur across the cutoff, as the fund re-rates them (SPLIT-13, USE-10): 98.8%, 97.6%
and 98.6% of the 2008, 2009 and 2010 members are in their training years, and `PolicyNum` is an input. The
windows differ: the claims were $12.1M, $11.0M and $36.7M, and in 2010, a year of severe weather, coverage fell
for 67.7% of the members and one claim is 35% of the year's claims, so that window's score moves with where that
one member is ranked.

3 repeat(s) x 1 fold(s) with seed 4267; train 2,292 to 4,529 rows, test 1,110 to 1,125 rows. Prediction horizon: 1 years.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 4529 | 1110 | 2006 | 2009 | 2010 | 2010 |
| 1 | 0 | 3417 | 1112 | 2006 | 2008 | 2009 | 2009 |
| 2 | 0 | 2292 | 1125 | 2006 | 2007 | 2008 | 2008 |

## Decisions

### 1. The fund's premium is the metric's base, never an input

The source scores a new rating against the fund's premium (Frees, Lee and Yang 2016, Sec. 6.2), and its models take the rating variables only. The premium is close to a function of the shipped rating variables, and ranks the year's claims about as well as the coverage alone.

| Year | member-years | R^2 of log premium on the rating variables | Spearman, premium and claims | Spearman, coverage and claims |
|---|---|---|---|---|
| 2006 | 1154 | 0.981 | 0.437 | 0.42 |
| 2007 | 1138 | 0.982 | 0.416 | 0.398 |
| 2008 | 1125 | 0.985 | 0.417 | 0.402 |
| 2009 | 1112 | 0.983 | 0.4 | 0.389 |
| 2010 | 1110 | 0.985 | 0.464 | 0.446 |

### 2. The yearly claims agree with the claim-level file

CLAIMLEVEL.csv lists every BC claim; its sum per member and year is compared with `y`.

| Year | member-years | member-years matching within $1 | claims, PropertyFundInsample ($) | claims, CLAIMLEVEL ($) |
|---|---|---|---|---|
| 2006 | 1154 | 1153 | 20458945 | 20459145 |
| 2007 | 1138 | 1137 | 17250071 | 17252427 |
| 2008 | 1125 | 1124 | 12068478 | 12109744 |
| 2009 | 1112 | 1110 | 11046302 | 11052577 |
| 2010 | 1110 | 1109 | 36659306 | 36659309 |

### 3. Three yearly windows, the oldest below half the rows

The test years are 2008, 2009 and 2010, each trained on every earlier year. The 2008 window trains on 2006-2007, under half of the rows (SPLIT-14), on the curator's call of 2026-11-02. 2010, a year of severe weather, holds the largest claims. The no-claim credit is missing where the file lacks the member's two earlier years, the claim count of the year before where it lacks that year.

| Year | member-years | share with a claim | claims ($M) | largest claim share | train share of a window starting here | members seen in earlier years | no two earlier years in the file (NoClaimCredit missing) | no year before in the file (prev_year_claims missing) |
|---|---|---|---|---|---|---|---|---|
| 2006 | 1154 | 0.268 | 20.5 | 0.323 | 0 | 0 | 1154 | 1154 |
| 2007 | 1138 | 0.314 | 17.3 | 0.108 | 0.205 | 0.986 | 1138 | 16 |
| 2008 | 1125 | 0.275 | 12.1 | 0.13 | 0.406 | 0.988 | 29 | 15 |
| 2009 | 1112 | 0.271 | 11 | 0.196 | 0.606 | 0.976 | 45 | 30 |
| 2010 | 1110 | 0.363 | 36.7 | 0.352 | 0.803 | 0.986 | 46 | 16 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (27 checks run, plus the dataset's own checks).

- **info** `meta_time_horizon_unit`: `time_horizon_unit='years'` implies calendar time, but `time_on='Year'` has dtype int64, so the horizon cannot be cross-checked. (hint: Fine when the numeric values themselves are calendar units (e.g. a year column); otherwise use `time_horizon_unit='steps'` for a plain numeric time index.)

Accepted on purpose:

- `task_time_on_few_unique`: Five policy years, 2006-2010, the whole time axis of the file: the yearly windows train on two to four earlier years, and the file has no finer time.
- `meta_license_unknown`: The first edition's repository, which holds the shipped file, has no licence file (GitHub API, 2026-11-01), and its book pages state none. The second edition named in the download description (OpenActTexts/LDAVer2, WiscPropFund.csv: the same rows with fewer columns) has a CC0-1.0 LICENSE in its repository (committed 2024-10-03), and its book pages state CC BY 4.0; the rows can be taken from it if the release needs a stated licence.
- `task_target_value_dominant`: 70.2% zeros: member-years without a building and contents claim (`Freq` 0), real no-claim years and not a cap or a placeholder; the batch's other zero-inflated targets are accepted on the same ground (Andrej, 2026-11-03).

## Data checks

### Feature summary

<details>
<summary>Show the table (11 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| NoClaimCredit | category | 2412 | 42.77 | 2 | 1.0, 0.0 |
| PolicyNum | category | 0 | 0 | 1227 | 180733, 180736, 180737, 180738, 180739, 180740, 180741, 180718, 180724, 180725 |
| Fire5 | category | 0 | 0 | 2 | 1, 0 |
| EntityType | category | 0 | 0 | 6 | School, Village, Town, City, Misc, County |
| AlarmCredit | category | 0 | 0 | 4 | 0, 15, 10, 5 |
| prev_year_claims | float64 | 1231 | 21.83 | 36 | 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0 |
| LnCoverage | float64 | 0 | 0 | 5611 | -1.6094, -1.4642, -1.204, -2.3914, 4.7288, 2.8937, 4.3668, -1.8971, 2.3043, -0.… |
| lnDeduct | float64 | 0 | 0 | 10 | 6.2146, 6.9078, 8.5172, 7.824, 9.2103, 10.1266, 9.6158, 10.8198, 11.5129, 11.22… |
| bc_claims | float64 | 0 | 0 | 1637 | 0.0, 1000.0, 1500.0, 3000.0, 1950.0, 2500.0, 7500.0, 900.0, 6000.0, 2720.0 |
| Year | int64 | 0 | 0 | 5 | 2006, 2007, 2008, 2009, 2010 |
| Premium | int64 | 0 | 0 | 4750 | 100, 276, 186, 486, 292, 9, 415, 637, 253, 279 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 70.23 | 39.804 | 1.014 | 5.3113e+10 | 18.588 | log1p | 40194.7 | 37275.4 | lognormal |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| Year | 5639 | 2007.98 | 1.41595 | 2006 | 2010 |
| LnCoverage | 5639 | 2.13288 | 1.97718 | -4.71756 | 7.80172 |
| Premium | 5639 | 14796 | 25520.7 | 9 | 412328 |
| lnDeduct | 5639 | 7.15724 | 1.17434 | 6.21461 | 11.5129 |
| prev_year_claims | 4408 | 1.09755 | 8.75945 | 0 | 263 |
| bc_claims | 5639 | 17287.3 | 230463 | 0 | 1.29222e+07 |

### Categorical features

<details>
<summary>Show the table (19 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| AlarmCredit | 1 | 0 | 2611 | 46.3 |
| AlarmCredit | 2 | 15 | 2462 | 43.66 |
| AlarmCredit | 3 | 10 | 327 | 5.8 |
| AlarmCredit | 4 | 5 | 239 | 4.24 |
| EntityType | 1 | School | 1597 | 28.32 |
| EntityType | 2 | Village | 1341 | 23.78 |
| EntityType | 3 | Town | 971 | 17.22 |
| EntityType | 4 | City | 793 | 14.06 |
| EntityType | 5 | Misc | 609 | 10.8 |
| Fire5 | 1 | 1 | 3131 | 55.52 |
| Fire5 | 2 | 0 | 2508 | 44.48 |
| NoClaimCredit | 1 | &lt;NA> | 2412 | 42.77 |
| NoClaimCredit | 2 | 1.0 | 1852 | 32.84 |
| NoClaimCredit | 3 | 0.0 | 1375 | 24.38 |
| PolicyNum | 1 | 180733 | 5 | 0.09 |
| PolicyNum | 2 | 180736 | 5 | 0.09 |
| PolicyNum | 3 | 180737 | 5 | 0.09 |
| PolicyNum | 4 | 180738 | 5 | 0.09 |
| PolicyNum | 5 | 180739 | 5 | 0.09 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
