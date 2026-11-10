---
report_format: data-foundry-report-v2
unique_name: spanish_motor_insurance_coverage_level_2022_2024
container_format: 2
checksum: v2:0d0b0429c2c6273e42d2f0fcefeeaa128336b1db1a0fe8450d61c032fab3ef58
build: null
build_stale: false
data:
  n_rows: 354091
  n_features: 23
  dtypes:
    category: 8
    float64: 14
    int64: 4
  n_test_dataset_rows: null
task:
  target: log1p_incurred_per_exposure_year
  problem_type: regression
  metric: normalized_weighted_gini
  metric_origin: context
  scoring_columns:
  - actual_exposure
  sample_weight: actual_exposure
  split_regime: grouped_non_iid
  stratify_on: null
  time_on: null
  group_on: insured_id
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 185677
    test_groups_per_fold:
      min: 61892
      max: 61893
splits:
  n_repeats: 3
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 235823
    max: 236294
  n_test:
    min: 117797
    max: 118268
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - groups_not_clustered
  accepted:
    task_target_value_dominant: '88.1% zeros: policy-years without a claim cost (Andrej,
      2026-11-03: zero-inflated targets are natural for these tasks and a core challenge).'
decisions:
- The policy's status at year end is dropped
- '`vehicle_age` holds the years since licensing'
- The time on risk is the weight, never a feature
- Every earned premium is annualised, to the cent
---

# spanish_motor_insurance_coverage_level_2022_2024

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `log1p_incurred_per_exposure_year`, scored with `normalized_weighted_gini` on grouped splits by `insured_id`. 354,091 rows and 23 features. Source: Other (2026).

Not built yet. The current definition gives checksum `v2:0d0b0429c2c6273e42d2f0fcefeeaa128336b1db1a0fe8450d61c032fab3ef58`.

## In brief

**Question.** What will a Spanish car insurance policy cost the insurer in claims per year on risk in one calendar year, from its covers and annual premiums, the driver and the vehicle?

**Use case.** A Spanish motor insurer pricing a policy: when a policy is written or renewed, it estimates the claim cost of the year from the rating factors, to rank the risk and set the premium. The data article names actuarial pricing as the reuse it supports.

**One row.** One car insurance policy in one calendar year, 2022 to 2024, at an unnamed Spanish insurer (354,091 policy-years of 185,677 policies, as the year's last record of the policy); 69% are flagged new business.

**Predicted.** The year's claim cost over all seven covers, paid plus reserved, in euros per year on risk (the recorded time on risk): 0 for 88.1% of the policy-years. Shipped as log1p, scored on the cost per year by a Gini; each policy-year counts in proportion to its time on risk, in training and scoring.

**Known at prediction time.** The type of cover and the annual premium of each cover, how the premium is paid, new or renewed business, the claim-history class, the driver's age and age when licensed, the vehicle (value, seats, weight per horsepower, brand, fuel), the area and the year.

**Known only when scoring.** The policy-year's recorded time on risk. A cancellation can cut it short, so it is no input: it is the rate's denominator and each policy-year's weight in training and scoring.

**What the test data stands for.** Whole policies are held out with all their years, so the test data stands for policies the model has not seen (52.4% of the policy-years are a policy's first year in the file, while a real next year's book is mostly renewals); three calendar years cannot give the three yearly test windows a pricing model refit each year would need.

**Our changes to the source.** We divide the year's claim cost by the time on risk, which weights each policy-year and is no input; we annualise each earned premium, to the cent; we drop the policy's status at year end, the target's parts (claim counts, per-cover costs) and 49 policy-years with no time on risk, and rename the column the source calls the vehicle's age: it holds the years since licensing.

> **Use case fit: approximate (a stand-in with a known gap).** Real policy-years with the insurer's rating factors and premiums, but held-out policies of the same years stand in for next year's book. Kept, with no measured gain: the year's last record (a change after a claim can show) and an active year's premium blending in the renewal price, which a year cancelled before its anniversary lacks.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`REVIEW.md`](REVIEW.md) | The open questions for the curator, removed once they are settled. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/spanish_motor_insurance_coverage_level_2022_2024.md`](../../../../curation/records/spanish_motor_insurance_coverage_level_2022_2024.md)
- The original source: <https://doi.org/10.17632/sw4jmdb2sm.1>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/spanish_motor_insurance_coverage_level_2022_2024/`. To get them:

```text
Version 1 of the Mendeley Data record (DOI 10.17632/sw4jmdb2sm.1, published 2026-02-16, CC BY 4.0) holds two
files: the portfolio (semicolon-separated CSV, 354,140 rows x 47 columns) and the variable descriptions. The
file links below come from the record's API
(https://data.mendeley.com/public-api/datasets/sw4jmdb2sm/files?folder_id=root&version=1), which also gives
the SHA-256 of each file (checked against these links on 2026-11-01, after they had failed for a few minutes);
"Download All" on https://data.mendeley.com/datasets/sw4jmdb2sm/1 gives the same files.

mkdir -p local-data-warehouse/spanish_motor_insurance_coverage_level_2022_2024 && cd local-data-warehouse/spanish_motor_insurance_coverage_level_2022_2024
wget -O "Dataset of motor insurance portfolio.csv" https://data.mendeley.com/public-files/datasets/sw4jmdb2sm/files/3dc64675-b6bd-4e8e-bfba-b64e585c6599/file_downloaded
wget -O "Descriptive of variables.xlsx" https://data.mendeley.com/public-files/datasets/sw4jmdb2sm/files/b34f32d4-cbe8-4a4e-bd09-9b59796e7fa3/file_downloaded
sha256sum "Dataset of motor insurance portfolio.csv" "Descriptive of variables.xlsx"
# 6a47d19d5278a049ea0aeaf39c955cc26068639bdc58cb4523b201e740f0faf4  Dataset of motor insurance portfolio.csv
# cde44e797a7fd34de29199c78c9301d6f00ed94fd725b4fe8e67e6c2c4cc2e41  Descriptive of variables.xlsx
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/spanish_motor_insurance_coverage_level_2022_2024   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/spanish_motor_insurance_coverage_level_2022_2024   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://doi.org/10.17632/sw4jmdb2sm.1 |
| year | 2026 |
| domain | insurance |
| license | CC BY 4.0 |
| data_tags | Non-IID, Grouped, ForcedGroupedFromTemporal |
| reference | espinosa2026motor |
| rows x columns | 354,091 x 26 |
| task.target | log1p_incurred_per_exposure_year |
| task.problem_type | regression |
| task.metric | normalized_weighted_gini |
| task.sample_weight | actual_exposure |
| task.split_regime | grouped_non_iid |
| task.group_on | insured_id |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `normalized_weighted_gini` (custom; takes value; higher is better) |
| origin | context: obvious from the task: the source defines no metric |
| definition | WG(y, p) / WG(y, y), WG = sum L_i R_(i-1) - sum L_(i-1) R_i over rows sorted by descending p, R the cumulative weight share, L the cumulative share of weight * y (tied p form one step, the mean over their orderings) |
| reason | The data article reports no model and no evaluation (Data in Brief 66:112883, read in full on PMC, PMC13234478), and the Mendeley record defines no task. Pricing actuaries compare tariffs by a Gini of the loss cost per exposure: CAS Monograph 5 (Goldburd, Khare and Tevet, Sec. 7.2.4) sorts the policies by predicted loss cost per exposure and accumulates exposure on the x-axis, while Frees, Meyers and Cummings (2011, JASA 106:1085-1098) order by the relativity to the premium and accumulate premium. The weighted Gini is that CAS form, normalised by the Gini of the perfect order as in Liberty Mutual's Kaggle competition of 2014, whose weight `var11` was a size of the risk; here the weight is the time on risk, chosen by the curator for this table (Andrej, 2026-11-02: "Use exposure-weighted Gini on annualised claim costs"): 49% of the rows are part-years, and the row Gini on the cost of the year rewarded reading the time on risk, which alone scored 0.177 to 0.221 against 0.393 to 0.445 for untuned LightGBM; weighted, the corrected time on risk (a feature until 2026-11-06) scored -0.035 to 0.010. Here policy-years are sorted by the predicted cost per year and the observed cost per year is weighted by the recorded time on risk (`actual_exposure`, a scoring column), so a policy-year counts with its time on risk, and every model trains with that weight (`sample_weight`, MET-15). On the 9 shipped splits 1/time on risk alone, the ceiling of a proxy of the weight, scores 0.075, the annual total premium alone 0.298 and untuned LightGBM 0.317 (both weighted fits). RMSE on the amount follows a few large claims (the 50 largest of 354,091 policy-years hold 75% of the year costs' sum of squares). The Gini sees neither the level nor the spread of the predicted costs; pricing sets the level separately. |
| inputs | weight: `actual_exposure` |
| target scale | ships on the `log1p` scale for modelling; scored on the original scale after the inverse of `log1p` |

**Scoring columns**

Kept in the frame for the metric; do not use them as features. Drop them from the inputs (`feature_columns(container)`), then pass the test rows' values to the scorer (`data_foundry.v2.metrics.scorer(container)(y_test, y_pred, test_idx)`).

| column | role | how the metric uses it | model input |
|---|---|---|---|
| `actual_exposure` | weight | normalized_weighted_gini: the policy-year's time on risk as recorded (`total_exposure` of the release: days in force over 365, in years), realized: shorter when the policy starts or is cancelled during the year. The cost per year's denominator; each row's weight in the metric and in training (`sample_weight`); never a feature, since for a cancelled year it gives the cancellation away (LEAK-41) | training weight; never a feature |

The test-row values of `actual_exposure` are for the scorer only: never read them when predicting a test row.

**Training weight**

Fit every model with `actual_exposure` as each row's sample weight (`sample_weight(container)` from `data_foundry.curation_container`), and never use it as a feature. The metric weights the test rows by the same column, so a model fitted without it targets another quantity.

<details>
<summary>Feature types: 6 categorical, 2 ordinal, 0 string, 0 datetime</summary>

- categorical (6): `policy_type`, `business_type`, `fuel_type`, `municipality_type`, `circulation_area`, `vehicle_brand`
- ordinal (2): `bonus_score (bad < neutral < good)`, `payment_frequency (annual < semiannual < quarterly)`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{espinosa2026motor,
  title = {A detailed dataset of motor insurance policies with coverage-specific financial information},
  author = {Espinosa, Priscila and Lled{\'o}, Josep and Atance, David},
  journal = {Data in Brief},
  volume = {66},
  pages = {112883},
  year = {2026},
  doi = {10.1016/j.dib.2026.112883},
  note = {Data: Mendeley Data, version 1, doi:10.17632/sw4jmdb2sm.1}
}
```

</details>

## Sample rows

The first 5 of 354,091 rows of the final frame (random rows: the frame is shuffled); 12 of 26 columns, the target first. Cells are cut at 40 characters.

| log1p_incurred_per_exposure_year | insured_id | year | policy_type | business_type | payment_frequency | bonus_score | driver_age | years_licensed | age_at_licence | fuel_type | vehicle_value |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 27020 | 2023 | CC | portfolio | annual | good | 64 | 41 | 23 | diesel | 18529.1 |
| 0 | 19059 | 2024 | TPG | portfolio | annual | good | 37 | 6 | 31 | diesel | 22446.6 |
| 0 | 44609 | 2023 | TP | portfolio | annual | good | 41 | 20 | 21 | diesel | 32711.2 |
| 0 | 76746 | 2023 | COMP_E | new business | semiannual | good | 66 | 41 | 25 | gasoline | 11869.7 |
| 0 | 26410 | 2023 | COMP_N | portfolio | annual | good | 34 | 9 | 25 | diesel | 19685.5 |

## Curation notes

We start with "Dataset of motor insurance portfolio.csv" of Mendeley Data sw4jmdb2sm, version 1 (Espinosa, Lledó and Atance 2026, Data in Brief 66:112883).

- Prediction point: when a policy is written or renewed for the year and the insurer prices it. The covers, the premiums, the driver, the vehicle and the claim-history class are known then; the year's claims are not. Data Description: "Each observation corresponds to an insured individual for a given year" (1 January 2022 to 31 December 2024).
- What the authors did (Experimental Design): of 653,943 raw rows, "only the last available record for each insured and year was retained. After this process, the number of observations was reduced to 354,140", the size of the release, so the later checks removed no row. On negative costs: "In the Spanish insurance market, negative incurred values may occasionally arise due to claim reversals or overprovisioning adjustments during the claims-handling process, a practice that is not standard in all international datasets. To maintain comparability and ensure a consistent actuarial interpretation, observations presenting negative incurred values were therefore excluded from the aggregation of total_incurred." Every incurred column has a minimum of 0, so the target is the sum of the covers' non-negative costs; nothing is set here (the AI's suggested call of 2026-10-30). The raw rows are "available from the authors upon reasonable request".
- Target `log1p_incurred_per_exposure_year`: the year's claim cost per year on risk, `total_incurred` ("the total cost incurred by the insurer as a result of claims, including both paid amounts and outstanding reserves", the sum of the seven covers' costs on every row) over the time on risk as recorded, on the log1p scale; the metric is computed on the cost per year (`target_transform="log1p"`, MET-3). The curator's call (Andrej, 2026-11-02, REVIEW.md issue 3): "Use exposure-weighted Gini on annualised claim costs for this dataset [...] Ensure predictions and observed costs are compared on the same annualised scale", so the models predict a cost per year and are scored against the observed cost per year. The recorded time on risk ships as the scoring column `actual_exposure`: the annualising base, the metric's weight and the training weight (`sample_weight`, MET-15), never a feature (LEAK-41). 88.1% of the policy-years cost 0, among them 8,543 (2.4%) with a claim recorded at zero cost. Some of these may be negative cover amounts left out of the sum (maybe: a zero cost sits on 35.8% of the third-party property claims, at most 1.5% on the other covers). Short years give large rates (5.5% of the rows have less than 0.1 years on risk; the largest rate is 3.7 million per year, from 571,128 over 0.153 years), but they hold 0.8% of the cost the weighted Gini counts.
- Why log1p and not the raw amount (MET-3, CLEAN-16; frempl_french_motor_personal_line shipped log1p until 2026-11-08 and the identity scale since (its issue 7 (b): with its length to 31 December a feature), as australian_vehicle_insurance_2004_2005 and pricing_game_2016_french_fleet do): the benchmark's models fit squared error by default, and on the raw amounts that fit chases the largest claims (the largest is 571,128, 0.8% of all claim cost; the 50 largest hold 75% of the sum of squares). The curator kept the log1p scale with the rate (Lennart, 2026-11-06). A fit weighted by the time on risk on this scale estimates the exposure-weighted mean of log1p(cost per year), not the cost per year: among active policy-years it rises from 0.117 below 0.1 years on risk to 1.074 for a full year while the cost per year stays at 221 to 336, so it ranks well only while the time on risk is no input (given it as a feature, the weighted L2 fit loses 0.035 on the declared metric, 0 of 9 splits). On the shipped features both weighted fits score alike: 0.3166 for L2 on log1p and 0.3165 for Tweedie on the cost per year, the actuarial loss (untuned LightGBM, 9 shipped splits x 3 seeds). Before 2026-11-02, on the year's cost and the row Gini, untuned LightGBM ranked at 0.426 / 0.412 / 0.397 on log1p, 0.353 / 0.365 / 0.363 on the raw amounts and 0.411 / 0.406 / 0.392 with a Tweedie loss (first three shipped splits). The Gini is computed on the cost per year either way.
- Only the claim part carries much signal (the hurdle check of task_probes.md, same splits): a claim is ranked at ROC AUC 0.70 to 0.71, while a severity model on the claimants reaches R^2 0.023 to 0.025 on log costs and below 0 on the costs, and the true claim indicator times the claimants' mean explains 5% to 9% of the variance of the amount. A hurdle model (claim probability times severity) ranks at a Gini of 0.359 to 0.367, below the direct log1p model.
- Dropped as parts of the target: the ten claim counts and the incurred cost of each cover (`liability_incurred` and its two parts, `property_incurred`, `theft_incurred`, `fire_incurred`, `glass_incurred`, `legal_protection_incurred`, `occupants_incurred`).
- `policy_status` dropped: "whether the policy was active (A) or cancelled (C) at calendar year" end (Table 1; "at the time of analysis" in the variable sheet), set after the prediction point (LEAK-10). No cancelled policy-year has a later year in the file, and cancelled policy-years claim more in less time (13.9% with a claim at a mean exposure of 0.53, against 11.7% at 0.73). Added back to the shipped features as a flag it raises the declared metric by 0.019 (weighted Tweedie) and 0.011 (weighted L2 on log1p), 9 of 9 splits (untuned LightGBM, 3 seeds; before 2026-11-02 the row Gini by 0.007 to 0.027).
- `liability_exposure` dropped: equal to `total_exposure` on every row.
- 49 policy-years with `total_exposure` 0 dropped: no time on risk and a premium of 0, all cancelled; they are no year a policy is priced for (USE-7). One of them has a claim of 180.11.
- `vehicle_age` renamed `years_licensed`, `age_driving_licence` renamed `age_at_licence`. Table 2 calls the first the "Age of the insured vehicle" and the second the "Year in which the insured obtained the driving licence" (the text: "the number of years since"), but `driver_age` = `vehicle_age` + `age_driving_licence` (to within a year) on 99.92% of the rows; within a policy the first moves from one year to the next as the driver's age does (+1 for 68% of the policies, 0 for 32%) while the second stays the same for 88%; and the second sits at 18 to 28 for most drivers: the first is the years since licensing and the second the age at licensing. The vehicle's own age is not in the release.
- `power_to_weight_ratio` renamed `weight_to_power_ratio`: Table 2 calls it the "Weight-to-power ratio of the vehicle (kg per horsepower)", and the values agree (about 2.5 for supercars, 64.8 for microcars).
- Impossible values made missing (CLEAN-11): an age at licence below 15 (34 rows; Spain's youngest licence, for mopeds, is at 15) with its years licensed, a weight per horsepower of 0 (3 rows; the authors required it "strictly positive"), and a liability premium of 0 (23 rows of policies with other covers: the cover is compulsory, and the premiums were "verified to ensure strictly positive numeric values").
- The codes of `business_type`, `payment_frequency`, `bonus_score`, `fuel_type`, `municipality_type` and `circulation_area` get the labels of Tables 1 and 2. `bonus_score` is an ordered category, bad < neutral < good (CLEAN-14, as bemtpl97's `coverage`; 2026-11-06): the variable sheet gives a word for every level ("a favourable claims history", "a neutral profile", "a poor claims history"). `payment_frequency` is an ordered category by the number of payments a year, fewest first: annual < semiannual < quarterly (1, 2 or 4), the same order as in pricing_game_2016_french_fleet and pricing_game_2017_french_mtpl (Lennart, 2026-11-08, REVIEW.md issue 8). `policy_type` (TP, TPG, CC, COMP_E, COMP_N), `vehicle_brand` (68 brands) and the other four coded columns are unordered categories. The ages, the year, `seats`, the vehicle value, the weight per horsepower and the eight annual premiums stay numbers; the 513 missing vehicle values and 1,287 missing fuel types stay missing.
- Exposure (LEAK-41, MET-14, MET-15; REVIEW.md issue 6, resolved 2026-11-06): `total_exposure`, "the time during each calendar year in which the corresponding policy is exposed to risk", is realized: the days in force over 365 (on a 1/365 grid in all three years), shorter when a policy starts during the year or is cancelled. A start is known when the policy is priced, a cancellation is not, and cancelled policy-years claim almost twice as often per exposure-year (0.50 for the located cancellations below and 0.55 for the first-year ones, against 0.30 for full years and 0.27 for late starts). A portfolio policy, and any policy with a row the year before, is in force from 1 January: exposure 1 on 89,817 of 89,882 active portfolio years and on 47,403 of 47,411 active new-business years that follow a row of the same policy (the new-business flag stays on into a policy's second calendar year). So there a time on risk below a year gives the cancellation away (32,626 located cancellations: 18,784 of the 18,849 portfolio years and 13,842 of the 13,850 of those new-business years below a year are cancelled), while in a new-business policy's first year in the file a cut cannot be told from a late start (5,653 cancelled years), since the release has no start date. The task: the recorded time on risk is the cost per year's denominator, the metric's row weight and the training weight (`actual_exposure`, `sample_weight`), never a feature. The corrected copy the models had until 2026-11-06 (a full year for the located cancellations, the cut left on the 5,653) is dropped too: a length corrected on some rows and realized on others is no input (LEAK-41). Measured on the shipped features (untuned LightGBM weighted by the time on risk, Tweedie on the cost per year and L2 on log1p, 9 shipped splits x 3 seeds): the recorded time on risk as a free feature gains 0.0325 under Tweedie (9 of 9; it misleads the L2 fit, -0.035), and 1/time on risk alone scores 0.075, the ceiling of a proxy; the corrected copy gained 0.0176 under Tweedie (9 of 9) and lost 0.0216 under L2. None of that gain is measured on the 5,653 cuts (replacing them by an estimate of the uncut time from the policy number, which follows first appearance, for this check only: -0.0002, SE 0.0006, 3 of 9; -0.0012 net of a control on random active first-year rows): it is the planned time on risk of policies that start during the year, which the release cannot separate from a cut. So a policy that starts during the year has no planned time on risk among its inputs (moved here from `fit_reason` on 2026-11-06): no gap in the fit, since a tariff prices the year insured, a pricing actuary does not rate on the planned length, and the time on risk sits in the weight (USE-8). Revisit if a release gives the start date or the contracted term: the time from the start to 31 December would ship as its own column (LEAK-7).
- Premiums annualised (LEAK-41): the release's premiums are earned premiums, the annual premium times the time on risk, cancelled years included. The earned total premium follows the time on risk (Spearman 0.83 among active part-years, 0.74 among the first-year cancellations, 0.78 among the located cancellations) and its ratio to it does not (0.034, 0.024, -0.053); the median ratio is 340 to 355 in every band of the time on risk for active policy-years, and flat within each payment frequency too, so a cancelled quarter is not charged in full. Each premium is divided by the recorded time on risk and rounded to the cent: the price of a year on risk. The located cancellations had the division before 2026-11-06; the other policy-years now get it, so no premium carries the time on risk in its level. The rounding (Lennart, 2026-11-08, REVIEW.md issue 7) takes it out of the decimals, found by the re-review of 2026-11-06: the annual tariffs sit on a 5-decimal grid, and the division puts a part-year's premium back on that grid while a full year, a blend of two prices, keeps 11 to 15 decimals. Unrounded, `total_premium` had at most 5 decimals on 39.5% of the located cancellations against 1.0% of the active full years in force from 1 January (on the late starts 0.5% before the division, 44% after); among the policy-years in force from 1 January the eight premiums' decimal counts and cent-grid flags ranked the located cancellations at ROC AUC 0.965 (folds grouped by policy), and the decimal counts as features gained +0.0035 under weighted Tweedie (SE 0.0017, ahead on 8 of 9 splits, 2 seeds) and -0.0052 under weighted L2. LEAK-41 takes out a value whose precision marks the cut whatever it scores. Re-run on the rounded frame (2026-11-08): the same check gives 0.565, no grid from 1 EUR to 1e-5 separates the located cancellations (AUC at most 0.501), and the decimal counts gain +0.0001 under Tweedie (SE 0.0017, 5 of 9) and -0.0012 under L2 (SE 0.0013, 3 of 9); probe 22 finds no feature whose gain goes through the time on risk under either fit. Against the unrounded premiums the score changes by -0.0005 under Tweedie and +0.0005 under L2 (SE 0.0006, 9 splits x 10 seeds). A premium of 0 means the cover is absent.
- Note: the premiums are kept (USE-6: the insurer's own price, known when the policy is written, which a model refines; TP-4: the core of the task, not a lookup). On the declared metric the annual total premium alone scores 0.2975 (0.277 to 0.316 over the 9 shipped splits); untuned LightGBM on all features scores 0.3166 fit by L2 on log1p (ahead of the premium on 9 of 9 splits) and 0.3165 by Tweedie (8 of 9), both weighted by the time on risk, and the eight premiums add 0.043 to 0.052 to it. Before 2026-11-06, with earned premiums, the corrected time on risk as a feature and no training weight, an untuned L2 fit scored below the premium on each of the first three splits (0.310 / 0.287 / 0.267 against 0.314 / 0.288 / 0.290; REVIEW.md issue 5).
- Potential leak, kept on purpose: an active calendar year's annual premium blends the price before the anniversary with the renewal price set at it, which can move with the year's claims, while a year cancelled before its anniversary shows one price. The two covers priced at a few flat amounts a year carry it: in 2023 the occupants premium of 51% of the located cancellations equals one of the 20 commonest amounts of that year's first years, against 7.7% of active full years (30% against 0.3% in 2024). So the premiums still mark a located cancellation among the policy-years in force from 1 January: ROC AUC 0.795 from the shipped features, the premiums rounded to the cent (0.81 unrounded, 0.62 without the premiums; first shipped repeat, 2026-11-08), and on the unrounded premiums 0.79 rounded to 3 significant digits, 0.72 in 10% bands, 0.68 with those two covers as presence flags, 0.67 with the year before's premiums in renewal years. It does not pay on the declared metric (LEAK-41's test, both weighted fits, 9 splits x 3 seeds): against the year before's premiums, known on 1 January, this year's premiums gain -0.0006 (Tweedie) and -0.0010 (L2) through the located cancellation and 0.0000 and +0.0009 through the time on risk; the two flat covers' gain over presence flags (0.0097 and 0.0117) goes through neither (-0.0016 and -0.0023 through the located cancellation, -0.0023 and +0.0006 through the time on risk). Through any cancellation, located or not, this year's premiums as shipped, rounded to the cent, gain +0.0013 under Tweedie (SE 0.0008, 5 of 9) and -0.0002 under L2 (SE 0.0011), and unrounded +0.0010 (SE 0.0006, 7 of 9) and +0.0005 (9 splits x 10 seeds; 3 seeds gave +0.0020). Both stay below two SEs, within one run's seed SD (0.007), at 3% to 4% of the free time on risk's gain. The premiums keep their values (Andrej, 2026-11-02: "do not round the premiums"): the cent rounding of the bullet above (Lennart, 2026-11-08) takes out the decimals' mark and keeps every price to the cent, and rounding to 3 significant digits leaves this mark and changes no score. Revisit if records from the actual prediction point become available: the first record of each year, in the raw rows the authors hold, would remove it.
- Potential leak, kept on purpose: each row is the year's last record of the policy, so an attribute changed during the year can show its state after a claim. Between consecutive years of a policy without a claim in the first, the policy type changes for 2.6% of those with a claim in the second year and 1.7% of those without, the brand for 2.2% and 1.6%, the vehicle value for 3.1% and 2.1%, the bonus class worsens for 0.28% and 0.03%, and the premium per exposure-year moves by +1.4% against +0.4% on average (the median is 0 in both). No consistent score gain detected in the tested comparisons, which is no proof that nothing leaks: setting the attributes of the 11,875 renewal years with a change (type, brand, bonus class, vehicle, payment, area; 6.1% of renewal years without a claim, 8.5% with one) back to the year before's values changes the declared metric by +0.0001 (weighted L2) and -0.0006 (weighted Tweedie, SE 0.0009; the last record ahead on 6 of 9 splits), as in house_sales; before 2026-11-02 the row Gini moved by -0.001 (type, brand or bonus class) and +0.002 (vehicle cells). A renewal year's annual premium is worth 0.012 more than the year before's under both fits, none of it through the cancellation or the time on risk; how much of it is a renewal price reacting to the year's own claims cannot be told without the anniversary date. Kept on the curator's call (Andrej, 2026-11-02). `business_type` is read from the year's last record too: in a policy's second calendar year it turns from new business to portfolio during the year, at a date tied to the start, so a year cancelled early stays new business more often (cancelled second years are new business 3 to 10 points more often within each band of the start, 0.51 against 0.43 overall). Probe 22 (re-run on 2026-11-08, the premiums rounded to the cent) fits the time on risk from the features at R^2 0.340, 42% of that fit's gain from `business_type`, whose gain through the time on risk is +0.0014 under weighted Tweedie (SD 0.0084) and -0.0135 under weighted L2 (SD 0.0071), no gain above noise (1/time on risk alone 0.070 there, 0.075 over the 9 splits). Against its value on 1 January (the year before's last record, on the rows that follow a row of the policy; 76,597 differ), the year's last value gains +0.0002 under Tweedie (SE 0.0004, ahead on 5 of 9 splits) and -0.0014 under L2 (SE 0.0007, 3 of 9), and through any cancellation -0.0002 and -0.0010 (9 splits x 10 seeds, 2026-11-06): no gain, so it stays with this note under the same call (LEAK-10's second clause, LEAK-41's report). Revisit if records from the actual prediction point become available: the first record of each year, which would remove it, is in the raw rows the authors hold.
- Note: in a new-business policy's first year in the file a cancellation (5,653 years) cuts the time on risk, now only the weight (the proportional part, LEAK-7, MET-14), and the earned premiums, which annualising undoes (Spearman 0.024 with the time on risk). The features still rank such a cancellation at ROC AUC 0.77 without the premiums (0.80 with them), mostly from the payment frequency (14.8% of quarterly payers' first years are cancelled, 2.1% of annual payers') and the year (5.8% in 2022, where a policy's first year in the file can be its second calendar year, against 1.6% and 1.5%), both known when the policy is priced (USE-6). Their gain does not go through the cancellation: leaving out the payment frequency, the year or the vehicle value costs the same with the cancellation flag among the features as without (differences +0.0008, -0.0020 and -0.0003 under weighted Tweedie, within 0.0007 under L2), though the flag itself would add 0.014 (0.010 under L2).
- Note: 26 policy-years repeat every feature of another policy's row of the same year (a fleet of identical cars, or two policies of one holder, under two ids); kept as distinct policies (LEAK-18).
- Anomaly: the CICOS agreement settles some claims at "pre-agreed amounts between participating insurers regardless of actual damage" (Limitations): 7,576 of the 42,263 positive costs (17.9%) are exactly 882 (all in 2022), 1,012 (2023) or 1,114 (2024), one flat amount per year, and a few are twice that. Kept as recorded; the year stays a feature.
- Anomaly: nearly every other claim amount sits on a grid of 0.0115 EUR, a cent times 1.15: all the amounts of bodily injury and of the six other covers and 91.7% of the rest of third-party property damage, against 4% to 22% on a cent grid for most covers; 2023's flat 1,012 is 880 x 1.15 and sits on it too. The amounts may carry a factor of 1.15 from the anonymisation that the flat amounts of 2022 and 2024 did not get (maybe; the article does not say). The Gini ignores a common factor. The ten claim costs below 1 EUR (1 to 46 cents, each with a recorded claim) are recorded amounts on this grid and stay; an eleventh, 6.5e-14, is float residue and changes no score.
- Potential leak, kept on purpose (LEAK-9, an evaluation leak): the folds keep every year of a policy together, so in each fold 47.6% of the test rows have their year before in the test fold and 47.6% their year after. `insured_id`, the group column, links them; without it the car (brand, value, seats, weight per horsepower, fuel), the driver's birth year, the age at licence and the area link 82.9% of the test rows that have a next year to that row, uniquely within the fold (0.3% false links). The next year's premium over this year's, its claim-history class and whether it exists give this year's claims away: untuned LightGBM weighted by the time on risk gains +0.121 (SE 0.005, weighted L2 on log1p) and +0.129 (SE 0.006, weighted Tweedie) on the declared metric, 0.44 against 0.31 (9 of 9 splits, 3 seeds; +0.10 and +0.11 with the links from the features alone; +0.027, SE 0.002, for a weighted Tweedie GLM), nearly all of it from the premium; this year's premium over the year before's gains +0.012 (L2) and +0.022 (Tweedie). Each test policy-year is predicted from the training rows and its own features only; no feature or model step may use other test rows, and a method that reads a test policy's other years is called out and not benchmarked (LEAK-9 as amended 2026-11-05, as for frempl_french_motor_personal_line). For the same reason the renewals carry no claims of the year before (REVIEW.md issue 9): under the split by policy each test row's claims would sit in its next year's row, where a model that reads them scores 0.70 to 0.74 against 0.31. A model that reads one row already gets about half of that history from this year's premiums: the year before's claims as features gain +0.004 to +0.007 on renewals with the premiums among the inputs and +0.012 to +0.013 without them (9 of 9 splits), and the claim-history class alone ranks the year before's claim at ROC AUC 0.51 (97% of the renewals are "good").
- Note: `insured_id` is the authors' recoded policy number, "constant across the analysed years"; it is the group column, never a feature.
- Note: how mature the labels are (cross-dataset item of 2026-11-09, Andrej): `total_incurred` is "paid amounts and outstanding reserves" (variable sheet) as of an undated extract. No claim date, closure date or status is published (`policy_status` is the policy's), so the share still open at a refit cannot be counted. The folds mix the three years of one extract, so both sides carry the same maturity; 2024, the least developed year, shows no shortfall (0.312 claims and 302 of cost per exposure-year, against 0.302 and 293 in 2022, 0.305 and 285 in 2023).
- Note: held for training rows only, not shipped (cross-dataset item of 2026-11-09, Andrej): the ten claim counts (77,098 claims on 50,806 policy-years) and the incurred cost of each cover (liability 64% of the claim cost, its property and injury parts 32% and 33%, property damage 25%, glass 6%), dropped above as parts of the target, and `policy_status`, the cancellation at the year's end (38,279 policy-years cancelled). The insurer holds them for the policy-years it has closed when it fits, but not for a policy it prices. They would need a training-only role, which the format does not have yet (MET-14, LEAK-41, MET-16), so they stay out for now.
- CC (2026-11-06, Lennart): REVIEW.md issue 6 resolved by decision D10 of the exposure study of 2026-11-05: `actual_exposure` is the training weight (`sample_weight`, MET-15) as well as the Gini's weight, every premium is annualised and `total_exposure` leaves the features (LEAK-41); the log1p target and the weighted Gini stay. Applied after the weighted re-measure of the same day found no remaining column whose cancellation signal pays on the declared metric (the premium mark, the year's last record, first-year cancellation from the features; the numbers are in the definition's notes and REVIEW.md issue 6). Supersedes Andrej's calls of 2026-11-02: keep the corrected `total_exposure` as the model feature with the 5,653 first-year cuts an approved limitation (REVIEW.md issues 2 and 3), since LEAK-41's partial-correction clause, adopted after that call, takes a length corrected on some rows and realized on others out of the features whatever it scores (the exposure study's +0.0032 for the cuts under weighted Tweedie, 7 of 9 of its own folds, did not hold on the shipped splits: -0.0012 net, SE 0.0006, 3 of 9); keep the premiums as published ("Keep both with explicit potential-leak notes; do not round the premiums", issue 4), since an earned premium carries the cut and annualising removes it (Spearman 0.024 with the time on risk among the first-year cancellations), while the premiums stay unrounded and the year's last record stays with its note; keep the task without a training weight (issue 5), since the training-weight API now exists (`sample_weight`), and with it and the annual premiums both weighted fits beat the premium alone (0.317 against 0.298).
- CC (2026-11-08, Lennart): the annualised premiums are rounded to the cent (REVIEW.md issue 7, "Round to the cent"): unrounded, their decimals marked a part-year (ROC AUC 0.965 for the located cancellations, 0.565 rounded; the decimal counts as features +0.0035 under weighted Tweedie before, +0.0001 after), and the rounding changes the score by -0.0005 under Tweedie and +0.0005 under L2 (SE 0.0006). This corrects the CC of 2026-11-06 above (D10): every premium is annualised and rounded to the cent, not left unrounded ("while the premiums stay unrounded"), and its "no remaining column whose cancellation signal pays" held for the premiums' values, not for their decimals. It changes the wording of Andrej's call of 2026-11-02 ("do not round the premiums", REVIEW.md issue 4) on a fact found after it, the decimals' mark; the prices he kept stay, to the cent.
- CC (2026-11-09, Andrej): the metric stays the normalized Gini of the cost per year weighted by the time on risk (REVIEW.md issue 11, A, as implemented), not the Gini against the premium charged (Frees, Meyers and Cummings' form, `ordered_lorenz_gini` with the earned premium as the base); the call of 2026-11-02 (issue 3) stands.
- CC (2026-11-09, Andrej): the renewals get no claims or cost of the year before, and the notes carry the LEAK-9 protocol line against reading other test rows (REVIEW.md issue 9 (a), "No history, a protocol line").
- CC (2026-11-09, Andrej): the forced split by policy stays, with that protocol line; the one 2024 window is not adopted (REVIEW.md issue 10 (a), "Split by policy"). The release has no date finer than the year.

## Splits

Grouped 3-fold splits by policy (`insured_id`), forced from temporal (SPLIT-8): every year of a policy stays on
one side. A pricing model is refit each year and applied to the next year's policies, but the release holds
three calendar years and no finer date, so a split by year gives one window that keeps half the rows for
training (2024, 47.5% of the rows, against 2022-2023), where SPLIT-14 asks for three; no finer date exists
(the days in force date some starts, but no claim is dated). What the window would change: the test rows'
year before would be training data, so a renewal could carry its last-year claims as a feature (+0.004 to
+0.007 on renewal rows, 9 splits), and the score would be the 2024 window's. Under this split the same
feature would put each test row's claims into its next year's row, also a test row, so the renewals carry no
claims of the year before (REVIEW.md issue 9). Protocol (LEAK-9): all years of a test policy are in its test
fold, and its next year's premium gives this year's claims away (+0.12 on the declared metric for LightGBM
that reads it); each test policy-year is predicted from the training rows and its own features only, and no
feature or model step may use other test rows.
Measured on the shipped definition (2026-11-06; untuned LightGBM weighted by the time on risk, fit by L2 on
log1p and by Tweedie on the cost per year): the 2024 window scores 0.300 to 0.307 (L2) and 0.305 to 0.316
(Tweedie) over 3 seeds, bootstrap SE 0.011 to 0.012, against 0.274 to 0.333 and 0.292 to 0.332 (means 0.309
and 0.311) on the 2024 rows of the 9 splits' folds, so the forced split is no more optimistic for the newest
year than the valid window. The pooled score (0.28 to 0.34 over the 9 splits) mixes years: within the same
folds 2023 rows rank more easily than 2024 rows (0.326 against 0.309 under L2) and 2022 rows a little
(0.317), which comes from the years, not from shared policies. Random policy-years score about the same as
the grouped folds (0.318 against 0.315 under L2, 0.314 against 0.317 under Tweedie), so the grouping follows
the use case, not a measured gap (SPLIT-4). This is not the forced IID split rejected for
how_much_did_it_rain: whole policies are held out, so no test row shares a policy's outcomes with training,
and the cost of the window is measured. The leak test across the split, in the form used for
wisconsin_local_government_property_insurance_fund (each test year scored by a model trained without that
year's training rows, against one trained without as many random rows; 9 splits), finds a small shared
period: the test year's own training rows add +0.010 under L2 (SE 0.002, 9 of 9) and +0.0045 under Tweedie
(SE 0.003, 6 of 9) pooled, at most +0.029 in one year (2022 under L2, SE 0.010, 7 of 9), and +0.006 and
+0.008 with the year out of the features. It sits within each year (the cost per exposure-year is flat at 285
to 302 a year): the year's own mapping from prices and factors to cost, not a year's claim level as there
(+0.113). No column carries it; at most 3% of the score and within the window's SE, it is the forced split's
optimism over a model that cannot see its year. Before 2026-11-02 (row Gini, first three splits): 30 exact
feature copies across the split shared no outcome (the leak probe of 2026-11-06 finds copies for 0.0% of the
test rows), the outcomes of training rows with the same car and driver under another id added +0.0011 (a
shifted-key control +0.0010), and the training side's mean outcome of the row's year added 0.0000 and of year
x area +0.0009; no feature is built from another row's outcome. The year stays a feature (the flat claim
amount of the CICOS agreement changes each year). A release with more
years or dates should get a temporal split. Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine"; kept on 2026-11-09, REVIEW.md issue 10 (a)).

3 repeat(s) x 3 fold(s) with seed 4267; train 235,823 to 236,294 rows, test 117,797 to 118,268 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 235823 | 118268 |
| 0 | 1 | 236099 | 117992 |
| 0 | 2 | 236260 | 117831 |
| 1 | 0 | 235973 | 118118 |
| 1 | 1 | 236294 | 117797 |
| 1 | 2 | 235915 | 118176 |
| 2 | 0 | 236027 | 118064 |
| 2 | 1 | 236104 | 117987 |
| 2 | 2 | 236051 | 118040 |

## Group structure

One group is a policy: `insured_id`, the authors' recoded policy number, "constant across the analysed years" (Data Description), with one row for each calendar year it was in force (67,751 policies with one year, 67,438 with two, 50,488 with three). The use case prices a policy for the year. 52.4% of the policy-years are a policy's first year in the file; the new-business flag (69% of the rows) stays on into a policy's second calendar year, and 62.7% of the 2024 rows had a row the year before. A tariff is fit on past years and applied to the next, but three calendar years give one valid temporal window (2024, trained on 2022-2023) where SPLIT-14 asks for three, so the policy-years are split by policy instead (SPLIT-8, ForcedGroupedFromTemporal): a test policy is one the model has seen in no year. Each policy-year is one prediction, made from its own row. A holder with several policies (several cars) has several ids, which the release cannot join.

| field | value |
|---|---|
| group column | `insured_id` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 185,677 |
| rows per group (min / median / max) | 1 / 2.0 / 3 |
| largest group | 0.0% of the rows |
| test groups per fold | 61,892 to 61,893 |
| groups of two or more rows with a single label | 73.3% |
| nearest neighbour in the same group | 1.1% of the rows (chance: 0.0%) |
| label variance explained by the group | 0.53 (shuffled groups: 0.52) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. The policy's status at year end is dropped

`policy_status` is set when the year ends: no cancelled policy-year has a later year, and cancelled policy-years claim more in less time.

| policy_status | policy_years | share_with_a_later_year | share_with_a_claim | mean_exposure |
|---|---|---|---|---|
| active (A) | 315812 | 0.533 | 0.117 | 0.729 |
| cancelled (C) | 38279 | 0 | 0.139 | 0.527 |

### 2. `vehicle_age` holds the years since licensing

The driver's age is the sum of `vehicle_age` and `age_driving_licence` (to within a year) on 99.92% of the rows; within a policy the first moves from one year to the next as the driver's age does, while the second mostly stays the same, so the first is renamed `years_licensed` and the second `age_at_licence`.

| change from one year to the next (share of policies) | vehicle_age | age_driving_licence | driver_age |
|---|---|---|---|
| -1 or less | 0.001 | 0.116 | 0 |
| 0 | 0.324 | 0.878 | 0.324 |
| 1 | 0.675 | 0.005 | 0.676 |
| 2 or more | 0 | 0 | 0 |

### 3. The time on risk is the weight, never a feature

A portfolio policy, and any policy in a later year in the file, is in force from 1 January, so its time on risk falls below a year only when it is cancelled, and cancelled years claim almost twice as often per exposure-year; in a new-business policy's first year in the file a cut cannot be told from a late start. So the recorded time on risk is the cost per year's denominator and each policy-year's weight in the metric and in training, and no column carries it as a feature (LEAK-41, curation notes).

| business type | policy's year in the file | status at year end | policy_years | share_below_a_year | claims_per_exposure_year |
|---|---|---|---|---|---|
| new business | first | active | 178519 | 0.943 | 0.277 |
| new business | first | cancelled | 5653 | 1 | 0.548 |
| new business | later | active | 47411 | 0 | 0.285 |
| new business | later | cancelled | 13842 | 1 | 0.478 |
| portfolio | first | active | 1266 | 0.051 | 0.285 |
| portfolio | first | cancelled | 239 | 1 | 0.45 |
| portfolio | later | active | 88616 | 0 | 0.307 |
| portfolio | later | cancelled | 18545 | 1 | 0.516 |

### 4. Every earned premium is annualised, to the cent

The premiums are earned pro rata: the earned total premium follows the time on risk, while the premium per year on risk (the earned premium over the time on risk) stays level across its bands, for active and cancelled policy-years alike. Each premium is divided by the time on risk, so no premium carries it in its level (LEAK-41), and rounded to the cent, so none carries it in its decimals: unrounded, a part-year's annual premium falls back on the tariff's 5-decimal grid while a full year keeps 11 to 15 decimals, and the decimals ranked the located cancellations at ROC AUC 0.965; rounded, 0.565 (REVIEW.md issue 7).

| status at year end | time on risk (years) | policy_years | median_earned_total_premium | median_annual_total_premium |
|---|---|---|---|---|
| active | below 0.1 | 16726 | 17.4 | 341 |
| active | 0.1 to 0.25 | 24770 | 59.5 | 340.6 |
| active | 0.25 to 0.5 | 45626 | 133.2 | 339.8 |
| active | 0.5 to 0.75 | 44724 | 213.5 | 345.5 |
| active | 0.75 to 1 | 36484 | 308.3 | 355.3 |
| active | a full year | 147482 | 351.4 | 351.4 |
| cancelled in a new-business first year | below 0.1 | 265 | 21.3 | 409.5 |
| cancelled in a new-business first year | 0.1 to 0.25 | 789 | 76 | 418.9 |
| cancelled in a new-business first year | 0.25 to 0.5 | 1464 | 155.1 | 414.1 |
| cancelled in a new-business first year | 0.5 to 0.75 | 1191 | 246.5 | 429.1 |
| cancelled in a new-business first year | 0.75 to 1 | 1943 | 384.8 | 433.4 |
| cancelled in a new-business first year | a full year | 1 | 596.9 | 596.9 |
| cancelled, in force from 1 January | below 0.1 | 2552 | 20.2 | 417.1 |
| cancelled, in force from 1 January | 0.1 to 0.25 | 4684 | 69.2 | 407.7 |
| cancelled, in force from 1 January | 0.25 to 0.5 | 8106 | 153.9 | 407.6 |
| cancelled, in force from 1 January | 0.5 to 0.75 | 8039 | 240.8 | 394.7 |
| cancelled, in force from 1 January | 0.75 to 1 | 9245 | 337.9 | 385.3 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (27 checks run, plus the dataset's own checks).

- **info** `groups_not_clustered`: Rows are no closer to their own group than chance (1.1% of nearest neighbours vs 0.0%), and the group explains no more of the label than shuffled groups (0.53 vs 0.52). (hint: The grouping may not be needed: compare IID and grouped scores with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.)

Accepted on purpose:

- `task_target_value_dominant`: 88.1% zeros: policy-years without a claim cost (Andrej, 2026-11-03: zero-inflated targets are natural for these tasks and a core challenge).

## Data checks

### Feature summary

<details>
<summary>Show the table (26 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| fuel_type | category | 1287 | 0.36 | 2 | diesel, gasoline |
| policy_type | category | 0 | 0 | 5 | CC, COMP_E, TPG, COMP_N, TP |
| business_type | category | 0 | 0 | 2 | new business, portfolio |
| payment_frequency | category | 0 | 0 | 3 | annual, semiannual, quarterly |
| bonus_score | category | 0 | 0 | 3 | good, neutral, bad |
| vehicle_brand | category | 0 | 0 | 68 | RENAULT, CITROEN, PEUGEOT, VOLKSWAGEN, FORD, OPEL, SEAT, AUDI, MERCEDES, TOYOTA |
| municipality_type | category | 0 | 0 | 3 | inland, coastal, islands |
| circulation_area | category | 0 | 0 | 2 | urban, rural |
| vehicle_value | float64 | 513 | 0.14 | 13494 | 30429.0, 32361.0, 28617.75, 22157.625, 27591.375, 31395.0, 23063.25, 24959.025,… |
| years_licensed | float64 | 36 | 0.01 | 68 | 21.0, 22.0, 18.0, 19.0, 20.0, 25.0, 24.0, 23.0, 17.0, 26.0 |
| age_at_licence | float64 | 36 | 0.01 | 60 | 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0 |
| liability_premium | float64 | 23 | 0.01 | 53252 | 434.98, 496.72, 192.56, 254.98, 191.97, 204.55, 195.63, 211.57, 204.86, 208.28 |
| weight_to_power_ratio | float64 | 3 | 0 | 1623 | 12.0, 11.0, 13.33, 11.9, 13.0, 10.0, 14.44, 14.33, 14.0, 15.0 |
| total_premium | float64 | 0 | 0 | 76368 | 240.44, 242.83, 244.43, 405.27, 243.35, 216.02, 240.43, 218.41, 242.82, 220.01 |
| property_damage_premium | float64 | 0 | 0 | 45502 | 0.0, 1504.02, 1717.47, 881.62, 1081.7, 194.73, 232.11, 1260.67, 228.93, 283.14 |
| theft_premium | float64 | 0 | 0 | 12435 | 0.0, 5.05, 4.35, 5.86, 6.67, 5.46, 3.98, 5.68, 4.37, 5.43 |
| fire_premium | float64 | 0 | 0 | 2654 | 0.0, 1.49, 1.03, 1.7, 1.01, 1.34, 1.21, 1.25, 0.51, 1.06 |
| glass_premium | float64 | 0 | 0 | 10894 | 0.0, 46.1, 16.02, 15.91, 20.18, 19.06, 14.43, 16.51, 16.39, 16.21 |
| legal_protection_premium | float64 | 0 | 0 | 3419 | 10.82, 12.26, 9.74, 11.14, 10.04, 11.89, 9.01, 10.55, 10.23, 10.01 |
| occupants_premium | float64 | 0 | 0 | 794 | 2.59, 2.52, 4.84, 4.69, 2.6, 2.98, 2.65, 2.61, 3.11, 2.58 |
| actual_exposure | float64 | 0 | 0 | 776 | 1.0, 1.0, 0.4795, 0.3945, 0.0603, 0.2274, 0.5616, 0.4822, 0.3973, 0.7288 |
| log1p_incurred_per_exposure_year | float64 | 0 | 0 | 33264 | 0.0, 7.0166, 6.9207, 4.504, 7.0166, 6.7833, 6.9207, 5.7664, 7.7093, 5.8027 |
| insured_id | int64 | 0 | 0 | 185677 | 13306, 49962, 67249, 4407, 3580, 29197, 42053, 17780, 32634, 28730 |
| year | int64 | 0 | 0 | 3 | 2024, 2023, 2022 |
| driver_age | int64 | 0 | 0 | 73 | 40, 38, 39, 41, 37, 42, 36, 44, 45, 43 |
| seats | int64 | 0 | 0 | 8 | 5, 7, 4, 2, 3, 8, 6, 9 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 88.06 | 2.527 | 2.386 | 5.203 | 0.446 | log1p | 247679 | 3.9949e+16 | exponential |

### Numeric features

<details>
<summary>Show the table (18 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| insured_id | 354091 | 76047.7 | 51272.1 | 1 | 185678 |
| year | 354091 | 2023.28 | 0.763658 | 2022 | 2024 |
| driver_age | 354091 | 49.0054 | 12.0687 | 18 | 90 |
| years_licensed | 354055 | 25.9203 | 11.6169 | 0 | 68 |
| age_at_licence | 354055 | 22.9918 | 6.3582 | 15 | 80 |
| vehicle_value | 353578 | 26977.5 | 12326.2 | 1630.12 | 374034 |
| seats | 354091 | 5.08403 | 0.757008 | 2 | 9 |
| weight_to_power_ratio | 354088 | 12.334 | 2.48206 | 2.47 | 64.81 |
| total_premium | 354091 | 420.01 | 239.757 | 14.26 | 6632.39 |
| liability_premium | 354068 | 260.024 | 146.627 | 6 | 3036.13 |
| property_damage_premium | 354091 | 100.412 | 189.039 | 0 | 4632.24 |
| theft_premium | 354091 | 15.7765 | 23.545 | 0 | 1332.31 |
| fire_premium | 354091 | 2.12192 | 2.80771 | 0 | 72.61 |
| glass_premium | 354091 | 27.3041 | 18.3415 | 0 | 511.89 |
| legal_protection_premium | 354091 | 11.6295 | 5.81221 | 0 | 210.88 |
| occupants_premium | 354091 | 2.76044 | 1.19006 | 0 | 68.65 |
| actual_exposure | 354091 | 0.706954 | 0.326162 | 0.00273973 | 1 |
| log1p_incurred_per_exposure_year | 354091 | 0.822458 | 2.28095 | 0 | 15.1299 |

</details>

### Categorical features

<details>
<summary>Show the table (26 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| bonus_score | 1 | good | 341511 | 96.45 |
| bonus_score | 2 | neutral | 7850 | 2.22 |
| bonus_score | 3 | bad | 4730 | 1.34 |
| business_type | 1 | new business | 245425 | 69.31 |
| business_type | 2 | portfolio | 108666 | 30.69 |
| circulation_area | 1 | urban | 190484 | 53.8 |
| circulation_area | 2 | rural | 163607 | 46.2 |
| fuel_type | 1 | diesel | 226367 | 63.93 |
| fuel_type | 2 | gasoline | 126437 | 35.71 |
| fuel_type | 3 | &lt;NA> | 1287 | 0.36 |
| municipality_type | 1 | inland | 228580 | 64.55 |
| municipality_type | 2 | coastal | 101374 | 28.63 |
| municipality_type | 3 | islands | 24137 | 6.82 |
| payment_frequency | 1 | annual | 287859 | 81.3 |
| payment_frequency | 2 | semiannual | 50837 | 14.36 |
| payment_frequency | 3 | quarterly | 15395 | 4.35 |
| policy_type | 1 | CC | 204609 | 57.78 |
| policy_type | 2 | COMP_E | 91186 | 25.75 |
| policy_type | 3 | TPG | 36358 | 10.27 |
| policy_type | 4 | COMP_N | 16181 | 4.57 |
| policy_type | 5 | TP | 5757 | 1.63 |
| vehicle_brand | 1 | RENAULT | 34348 | 9.7 |
| vehicle_brand | 2 | CITROEN | 32486 | 9.17 |
| vehicle_brand | 3 | PEUGEOT | 29569 | 8.35 |
| vehicle_brand | 4 | VOLKSWAGEN | 28785 | 8.13 |
| vehicle_brand | 5 | FORD | 28294 | 7.99 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
