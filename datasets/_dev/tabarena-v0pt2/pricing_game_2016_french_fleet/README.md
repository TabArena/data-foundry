---
report_format: data-foundry-report-v2
unique_name: pricing_game_2016_french_fleet
container_format: 2
checksum: v2:49ac634b942694668ae0306cd04daede95b576c8305a4d5eb4cb8d3b89698d66
build: null
build_stale: false
data:
  n_rows: 87228
  n_features: 16
  dtypes:
    category: 13
    datetime64[ns]: 1
    float64: 3
    int64: 2
  n_test_dataset_rows: null
task:
  target: claim_charge_per_vehicle_year
  problem_type: regression
  metric: rescaled_mean_tweedie_deviance
  metric_origin: stand_in
  scoring_columns:
  - exposure
  sample_weight: exposure
  split_regime: grouped_non_iid
  stratify_on: null
  time_on: null
  group_on: contract_id
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 18037
    test_groups_per_fold:
      min: 6012
      max: 6013
splits:
  n_repeats: 3
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 57460
    max: 58572
  n_test:
    min: 28656
    max: 29768
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos: []
  accepted:
    dataset_duplicate_rows: 'Vehicles of one fleet in the same period share every
      contract class and the start, so the length to the year''s end, and differ only
      by their own two classes: natural repeats (LEAK-18). The split by contract keeps
      them on one side; 4.3% of the test periods have a copy with the same start from
      another fleet.'
    dataset_conflicting_duplicate_rows: 'The same repeats as dataset_duplicate_rows:
      vehicles of one fleet with the same classes in the same period, with different
      claim charges per vehicle-year (another charge, or the same charge over another
      realized length). Natural (LEAK-18); the outcome of one vehicle is not the other''s.'
    task_target_value_dominant: 'Zero-inflated by nature: the claim charge per vehicle-year
      is 0 for 95.7% of the periods, those with no claim (95.1%) or whose claims net
      to 0 or less after IDA recoveries (0.6%, negative totals set to 0); not a cap
      or a placeholder.'
    meta_license_unknown: The organisers state no licence for the game's files; CASdatasets,
      which redistributes the same tables, is GPL (>= 2).
decisions:
- The charge per realized vehicle-year, weighted by the vehicle-years
- Whole contracts held out, forced from temporal
- A net recovery counts as no cost
---

# pricing_game_2016_french_fleet

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `claim_charge_per_vehicle_year`, scored with `rescaled_mean_tweedie_deviance` on grouped splits by `contract_id`. 87,228 rows and 16 features. Source: Other (2016).

Not built yet. The current definition gives checksum `v2:49ac634b942694668ae0306cd04daede95b576c8305a4d5eb4cb8d3b89698d66`.

## In brief

**Question.** What will a vehicle of a French company's fleet cost in material-damage claims per vehicle-year of cover, from the contract's and the vehicle's rating classes and the length of cover to the year's end, known when its period of cover starts?

**Use case.** A fleet insurer setting its tariff: it fits the pure premium, the expected claim cost per vehicle-year, on the closed years and charges it for the time each vehicle stays in the fleet. The 2016 actuarial pricing game posed this pricing task on this portfolio.

**One row.** One vehicle of a fleet contract over one period with unchanged contract terms, cut at each change and at the year's end: 87,228 periods of 68,485 vehicles in 18,037 contracts of an unnamed French insurer, 2011 to 2013.

**Predicted.** The period's claim charges summed, per vehicle-year of the period (0 for 95.7% of the periods), net of the flat amounts recovered under the IDA convention between insurers, where the insurer pays its client and recovers a flat amount from the other insurer; a net recovery counts as 0. Each period counts by its vehicle-years in training and scoring. The charges are scaled by one constant of the release.

**Known at prediction time.** The contract's age, the client's activity, zone, fleet size and management, a new-company flag, the distribution channel, payment frequency, formula, deductible and insured value classes; the vehicle's age and power-value classes; the period's start date and the length of cover to the year's end. Most periods end earlier, at a cut not known at the start (a quarter on a month's end), so their vehicle-years are no input.

**What the test data stands for.** Whole fleet contracts are held out with all their periods of 2011 to 2013, in three folds by contract repeated three times, so the test data stands for fleets the model has seen in no year, the years mixed. A tariff is fit on the closed years and applied to the next, but three years cut at 31 December give one valid yearly window where three are needed.

**Our changes to the source.** We summed each period's claim charges, set the 537 net negative totals to 0 and divided by the period's vehicle-years, which weight the period; added the length of cover to the year's end; kept the contract as the group of the split; dropped the registration, the year and the period's end date, made the unknown insured value missing, and gave two codes their labels.

> **Use case fit: approximate (a stand-in with a known gap).** Real periods with the rating classes and the length of cover the insurer knows at pricing, and the claim cost per vehicle-year a fleet tariff charges. Held-out fleets of the same years stand in for next year's book, where about 80% of the periods belong to fleets insured before; on the 2013 periods the forced split scores as the valid yearly window does.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`REVIEW.md`](REVIEW.md) | The open questions for the curator, removed once they are settled. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/pricing_game_2016_french_fleet.md`](../../../../curation/records/pricing_game_2016_french_fleet.md)
- The original source: <https://actinfo.hypotheses.org/69>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/pricing_game_2016_french_fleet/`. To get them:

```text
The second actuarial pricing game (Arthur Charpentier, Romuald Elie and Jérémie Jakubowicz, for the 100% Data
Science day of the Institut des Actuaires on 8 November 2016; announced on https://actinfo.hypotheses.org/69,
DOI 10.58079/al7p) gave its players three CSV files, still on the organiser's site (Last-Modified 13 July
2016) and archived by the Wayback Machine on 12 September 2025 with the same bytes. The rules describe the
columns: http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf.
We use the two training files; test_contrats.csv (the 32,772 periods of 2014 to price) has no claims.
The R package CASdatasets holds the same tables, renamed and recoded, as pg16trainpol, pg16trainclaim and
pg16test (man/pricingame.Rd); its DirectComp column disagrees with the organisers' IDA flag on 1,064 claims.

mkdir -p local-data-warehouse/pricing_game_2016_french_fleet && cd local-data-warehouse/pricing_game_2016_french_fleet
for f in train_contrats train_sinistres; do wget http://freakonometrics.free.fr/pricinggame/$f.csv; done
# or: wget -O $f.csv http://web.archive.org/web/20250912080148id_/http://freakonometrics.free.fr/pricinggame/$f.csv
sha256sum train_contrats.csv train_sinistres.csv
# d0f9caeb8146a03bdfe8ef67be2a5df576f35ae31a34d91f4c10946885c4f14a  train_contrats.csv
# d41f7b18afea4767c50d750909be669c272696fd9d75587ca83a00d1ce6e45fe  train_sinistres.csv
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/pricing_game_2016_french_fleet   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://actinfo.hypotheses.org/69 |
| year | 2016 |
| domain | insurance |
| license | nan |
| data_tags | Non-IID, Grouped, Anonymized, Spatial, ForcedGroupedFromTemporal |
| reference | Charpentier2016PricingGame |
| rows x columns | 87,228 x 19 |
| task.target | claim_charge_per_vehicle_year |
| task.problem_type | regression |
| task.metric | rescaled_mean_tweedie_deviance |
| task.sample_weight | exposure |
| task.split_regime | grouped_non_iid |
| task.group_on | contract_id |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `rescaled_mean_tweedie_deviance` (custom; takes value; lower is better) |
| origin | stand_in: a stand-in for the source's metric, which cannot be computed |
| original | each player's result in the 2014 market the organisers ran as a price aggregator: each insured going to a company drawn at random among the cheapest premiums, every player's premiums scaled by one uniform factor to a total of 2.5 million euros (rules, Sec. 4 'Règles du Jeu') |
| reference | http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf |
| definition | p' = max(p, min_prediction); c = sum(w * y) / sum(w * p') over the scored rows; then sum(w * d(y, c * p')) / sum(w), d the Tweedie unit deviance at power q, 2 * (y^(2-q) / ((1-q)(2-q)) - y m^(1-q) / (1-q) + m^(2-q) / (2-q)) for the mean m (q = 1 Poisson); invariant to a common scale of p above the floor; NaN when sum(w * y) = 0 |
| reason | The market needs the other players' premiums and the claims of 2014, neither published. The game scaled every player's premiums by one uniform factor to the same total ('un facteur d'inflation appliqué uniformément') before each insured went to the cheapest, so it rewarded the relative prices, their order and their spread, and not their level. This score does the same: each scored set's predictions are multiplied by sum(w y) / sum(w p), which brings their weighted total to the set's claims as the game set every total, then scored by the Tweedie deviance at power 1.5, the compound Poisson-gamma loss of a pure premium, each period weighted by its vehicle-years, so the score rewards the rate a fleet tariff charges, not a guess of how long a vehicle stays (MET-15). The closeness to the market, measured by the game's rule on the three windows of 2013 shipped until 2026-11-08 (8 tariffs, among them a Tweedie GLM and a LightGBM with their relativities flattened or steepened, each rescaled to the window's claim total; each period to the cheaper premium; every two-player market): this score picks the market's winner in 76 of 84 pairs, the normalized weighted Gini, the stand-in until 2026-11-08, in 44, tying on 21 as it cannot see a change of spread (the GLM and the same GLM with its relativities doubled on the log scale both scored 0.173); on the shipped contract folds 225 of 252 against 128, tying on 63, and among the fitted tariffs alone (two LightGBMs, the GLM, the constant) 52 of 54 against 43. australian_vehicle_insurance_2004_2005 and spanish_motor_insurance_coverage_level_2022_2024 keep the Gini, with no market of uniformly rescaled premiums behind them; pricing_game_2017_french_mtpl, whose game kept the price level and ruined a player at 170% losses, scores the plain Tweedie deviance. The game's page (actinfo.hypotheses.org/69) and CASdatasets' pricingame.Rd name no other metric. The floor of 0.1 per vehicle-year is two orders below the cheapest cells' mean, rounded down (MET-13; the notes). |
| params | {'power': 1.5, 'min_prediction': 0.1} |
| inputs | weight: `exposure` |

**Scoring columns**

Kept in the frame for the metric; do not use them as features. Drop them from the inputs (`feature_columns(container)`), then pass the test rows' values to the scorer (`data_foundry.v2.metrics.scorer(container)(y_test, y_pred, test_idx)`).

| column | role | how the metric uses it | model input |
|---|---|---|---|
| `exposure` | weight | rescaled_mean_tweedie_deviance: the period's vehicle-years (the source's Exposition_au_risque, 0.08 to 1), realized: 57.4% of the periods end before 31 December at a cut not known at the start (a quarter of them on a month's end), known only when it comes. The rate's denominator; each row's weight in the metric and in training; never a feature | training weight; never a feature |

The test-row values of `exposure` are for the scorer only: never read them when predicting a test row.

**Training weight**

Fit every model with `exposure` as each row's sample weight (`sample_weight(container)` from `data_foundry.curation_container`), and never use it as a feature. The metric weights the test rows by the same column, so a model fitted without it targets another quantity.

<details>
<summary>Feature types: 8 categorical, 5 ordinal, 0 string, 1 datetime</summary>

- categorical (8): `distribution_channel`, `new_company`, `fleet_management`, `client_activity`, `zone`, `fleet_size_class`, `power_value_class`, `formula`
- ordinal (5): `contract_age_class (<= 1 ans < 1 - 2 ans < 2 - 3 ans < 3 - 4 ans < 4 - 5 ans < > 5 ans)`, `vehicle_age_class (<= 5 ans < > 5 ans)`, `deductible_class (1. 0 < 2. 1 - 200 < 3. 201 - 300 < 4. 301 - 400 < 5. 401 - 600 < 6. > 600)`, `insured_value_class (<= 7.6K < 7.6K - 38K < 38K - 76K < 76K - 137K < 137K - 380K)`, `payment_frequency (annual < semi-annual < quarterly)`
- string (0): none
- datetime (1): `period_start`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{Charpentier2016PricingGame,
  author = {Charpentier, Arthur and Elie, Romuald and Jakubowicz, J{\'e}r{\'e}mie},
  title = {Pricing Game 100\% Data Science},
  year = {2016},
  howpublished = {\url{https://actinfo.hypotheses.org/69}},
  note = {Second actuarial pricing game, Institut des Actuaires, 100\% Data Science day of 8 November 2016;
    data files train\_contrats.csv and train\_sinistres.csv at http://freakonometrics.free.fr/pricinggame/;
    DOI 10.58079/al7p; distributed as pg16trainpol and pg16trainclaim in the R package CASdatasets (Dutang
    and Charpentier)}
}
```

</details>

## Sample rows

The first 5 of 87,228 rows of the final frame (random rows: the frame is shuffled); 12 of 19 columns, the target first. Cells are cut at 40 characters.

| claim_charge_per_vehicle_year | period_start | contract_age_class | new_company | fleet_management | zone | fleet_size_class | payment_frequency | exposure | vehicle_age_class | deductible_class | n_vehicles |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2012-03-27 00:00:00 | > 5 ans | No | N | 1 | 1 | annual | 0.16 | > 5 ans | 2. 1 - 200 | 1 |
| 0 | 2011-01-04 00:00:00 | 3 - 4 ans | No | N | 3 | 2 | annual | 0.16 | &lt;= 5 ans | 2. 1 - 200 | 1 |
| 0 | 2012-02-07 00:00:00 | &lt;= 1 ans | No | P | 3 | 2 | annual | 0.9 | > 5 ans | 2. 1 - 200 | 1 |
| 0 | 2013-04-10 00:00:00 | > 5 ans | No | N | 3 | 1 | annual | 0.39 | > 5 ans | 2. 1 - 200 | 1 |
| 0 | 2012-02-24 00:00:00 | 3 - 4 ans | No | N | 1 | 1 | annual | 0.5 | &lt;= 5 ans | 2. 1 - 200 | 1 |

## Curation notes

We start with train_contrats.csv and train_sinistres.csv, the files the organisers of the second actuarial pricing game (2016) gave its players.

- Prediction point: the start of a vehicle's period of cover, when the insurer prices it with the year's tariff, fit on the closed years. The game asked for "une prime pure" (a pure premium) for each of the 32,772 periods of 2014 in test_contrats.csv (rules, Sec. 2, which write 37,772), with the periods of 2011 to 2013 to learn from; the claim charge per vehicle-year is the pure premium's rate, which times a period's vehicle-years gives the period's pure premium. Known then: the contract's and the vehicle's rating classes, the period's start and its length of cover to the year's end. Not known: the period's claims, and when a period cut short will end.
- Source and year: the game's page (actinfo.hypotheses.org/69, 17 July 2016) dates the first stage "entre le 15 juillet et le 15 septembre", and the files carry a Last-Modified date of 13 July 2016. The rules (pricing-game-2016-FR.pdf, Sec. 1) describe every column; CASdatasets' copy holds the same values, its levels renamed one to one, except its DirectComp, which is 0 for 1,064 of the 1,190 claims the organisers flag IDA (a problem of that copy, not used here).
- The portfolio is commercial fleets with a material-damage cover, not the "private motor insurance" of CASdatasets' documentation: the rules describe "Mode de gestion de la flotte", "Taille de la flotte" and "Classe de franchise de la garantie DTA" (DTA is the usual French abbreviation of an all-accident damage cover), and 1,190 of the 4,568 claims fall under the IDA convention between insurers. The row names of the training file and the 2014 file together run exactly from 1 to 120,000, so the files are likely a sample of the portfolio: counts per contract (at most 12 vehicles of a contract at once) and a vehicle's last period describe the file, not the fleets.
- Target `claim_charge_per_vehicle_year`: the charges (CHARGE_SINISTRE) of the period's claims summed, 0 without a claim, divided by the period's vehicle-years `exposure` (MET-14); the summed charge leaves the frame as a part of the target, and `_clean` checks that the target times `exposure` gives it back. Each of the 4,568 claims joins one period on the contract, the registration, the year and the period's dates, and the claim count equals the joined claims on every period (checked in `_load_raw`). 4,250 periods have a claim (286 two or more, at most 7); 3,711 have a positive total (median 1,339, at most 13,992), so 95.7% of the targets are 0; per vehicle-year the positive values run up to 75,929, a large charge on a period of a month or two. The curator first chose the claim indicator (2026-10-30, record), switched to the charge per period on 2026-11-02 after a measurement (the charge is what the insurer prices and what the game asked for), and to the charge per vehicle-year on 2026-11-06 (CC below).
- 537 periods net below 0 set to 0 (down to -1,863), as pricing_game_2017_french_mtpl and frempl_french_motor_personal_line do (the family call of 2026-10-30: "a net recovery is no claim cost of the year"). They are claims under the IDA convention ("1 si sinistre Indemnisation Direct de l'Assuré", rules Sec. 1), where the insurer pays its client and recovers a flat amount, not the cost, from the other insurer; every claim with a charge of 0 or less is IDA, and 126 of the 1,190 IDA claims are at 50% responsibility. Tweedie and Poisson losses need a non-negative target. The total is clipped, not each claim (65 periods mix signs, 16 of them net below 0); the clip raises the total claim cost by 4.3%.
- Only the frequency carries signal. Among the periods with a positive charge, the log charge is not predictable from the classes (R^2 -0.06 for LightGBM, -0.02 for ridge, measured on 2011-2012 to 2013). On the shipped contract folds a weighted Poisson LightGBM of the claims per vehicle-year, times the training side's mean charge per claim, scores 81.04 on the declared metric and a normalized weighted Gini of 0.204, against 82.04 and 0.185 for the weighted Tweedie LightGBM of the charge (9 folds, predictions averaged over 3 seeds; the frequency model better by 1.00 on the declared metric, contract-bootstrap standard error 0.34, on every fold). The task is the frequency task with severity noise on top. Raw rate, not log1p: a deviance scores the mean on the scale the target ships (CLEAN-16), and a log1p fit sent back predicts about the geometric mean instead. A fit weighted by the vehicle-years on this scale estimates E[charge | x] / E[vehicle-years | x], the charge per vehicle-year that breaks even.
- Exposure (LEAK-41, MET-14, MET-15; issue 5, resolved 2026-11-06): `exposure` is the source's Exposition_au_risque, "Véhicules année (exposition au risque)": the period's vehicle-years, (end - start + 1) / 365 (/ 366 in the leap year 2012) times the period's vehicles (2 on two periods), rounded to 0.01, which `_clean` checks on every period. It is realized: of the 87,228 periods of 68,485 vehicles (2011 to 2013), 57.4% end before 31 December at a cut not known at the start (a quarter of them on a month's end) and 0.8% at a contract anniversary, so their length is known only at their end. The task divides the period's charge by it and weights each period by it in training and scoring (the weight scoring column and the `sample_weight`), never as a feature. The part known at the start ships as the feature `exposure_to_year_end`, the same formula to 31 December (LEAK-7, LEAK-37). The shipped features were leak-free since the fix of 2026-11-02 (next bullet), but the target summed over the realized period still rewarded predicting how long a vehicle stays: about 0.03 of the row Gini (the direct model of the total 0.210 against 0.182 for its rate times the length to 31 December; a rough attribution of the exposure study of 2026-11-05). A fit that ignores the weight scores 0.64 worse on the declared metric on the shipped contract folds (82.68 against 82.04, SD 0.44 over the folds, worse on 8 of 9) and 0.011 lower on the Gini (lower on 8 of 9); on the windows of 2013 shipped until 2026-11-08 it lost 0.010 of the Gini (SD 0.009), within seed noise there, little since no period is shorter than 30 days.
- Why the rate (CC below): a fleet's premium is regularised per vehicle as vehicles come in and go out (a French fleet-insurance guide, echangesassurances.org: "La prime est régularisée en fin d'année sur la base du parc réel (pro-rata temporis)"; AXA Belgium's fleet terms set a regularisable premium apart from a non-regularisable one, so not every fleet contract is), so a fleet tariff charges a rate per vehicle-year, earned over the time the vehicle stays. A realized time on risk is also a valid weight when the outcome cuts it short: when a period's end is a stopping time of its claim history, the weighted fit estimates E[charge | x] / E[vehicle-years | x], the rate that breaks even per vehicle-year (the exposure study's stopping-time argument, checked there by simulation; a stopping rule driven by unobserved risk was not simulated). The game's 2014 file gave its players each period's realized end and length (58.2% end before 31 December 2014); that is no ground here, since a host's test file is a holdout of the same snapshot, not deployment data (LEAK-38).
- The realized length as a feature (fixed on 2026-11-02): until then `exposure` was a feature holding the realized length, and with `period_start` a feature it gave back the dropped end. On the three windows of 2013 of that day it added ROC AUC on the claim indicator +0.040, +0.055 and +0.052 over the length known at the start (regularised LightGBM on the rating classes and the start's day of the year, 3 seeds), and the early ends go with claims: a rate ratio of 1.22 [1.12, 1.33] given the rating classes (Poisson GLM with the length as offset, 2011-2012). Confirmed by the curator (Andrej, 2026-11-02) and recorded as the LEAK-10 case for time on risk cut short by the outcome: the cut is fixed where the data locates it. With the rate, the realized length is the weight alone. Probe 22 (LEAK-41: both arms, the decision on the worse), run again on the contract folds under the declared metric (2026-11-08; 3 splits x 3 seeds, each side capped at 50,000 rows): the features predict the realized vehicle-years at R^2 0.45, mostly through `fleet_management` (49% of the gain) and `exposure_to_year_end` (37%), both known at the start, so they stay (USE-6). In the weighted Tweedie arm the weight as a feature improves the declared metric by 0.37 (SD 0.49, the honest fit at 85.60), and no feature's gain goes through the weight above noise (the largest, `fleet_management`, -0.51, SD 0.41). The L2 arm fits this metric poorly (101.6, SD 7.8), the weight as a feature makes it worse (by 11.7, SD 6.6), and no feature's gain goes through the weight above noise either. On the windows of 2013 under the Gini (2026-11-06) the Tweedie arm gave the weight +0.007 (SD 0.028) and 1/vehicle-years alone 0.029, the ceiling a proxy would reach; the time features (`exposure_to_year_end`, `period_start`) added 0.007 to the weighted Tweedie fit (SD 0.009), within seed noise, and the realized vehicle-years as a feature would have added 0.013 (on 5 of 5 seeds).
- The covariates carry the signal (TP-4), on the shipped contract folds (9 folds, predictions averaged over 3 seeds; the declared metric, lower is better, then the normalized weighted Gini): a weighted Tweedie GLM on the classes and the length to 31 December 81.24 and 0.200, a regularised Tweedie LightGBM fitted with the weight 82.04 and 0.185, the weighted constant 82.63 and 0, the length to 31 December and the start's day of the year alone 83.64 and -0.009; an untuned Tweedie LightGBM 86.84 and 0.145, a deeper one (63 leaves) 86.51 and 0.159. Bootstrap by contract (1,000 resamples of each fold's test contracts) of the declared metric's differences: the GLM beats the constant by 1.39 (standard error 0.46; on all 9 folds, by more than 2 standard errors on 8), the LightGBM beats it by 0.59 (0.58; on 7 of 9, beyond 2 standard errors on 2), and the GLM beats the LightGBM by 0.80 (0.43; on all 9, beyond 2 standard errors on 4); under the Gini each model beats the constant by about 9 standard errors and the GLM the LightGBM by 0.016 (0.013). The declared metric separates a GLM from a flat tariff on every fold, so the task is not trivial, but the signal is weak (the GLM 1.7% below the constant), and the metric punishes relativities that run too steep, as the game's market did: the untuned and the deeper LightGBM score worse than the constant on every fold, and the regularised LightGBM's predictions flattened (raised to the power 0.5 around their mean) score 81.30 against its 82.04 (on the windows of 2013 its actual over expected ran from 1.4 to 2.0 in the cheapest predicted fifth down to 0.5 to 0.9 in the dearest). A tree model needs regularising here to beat a flat tariff. The charge per vehicle-year trends up, 160, 174 and 184 in 2011 to 2013; a fold mixes the years, so a model reads that level from the start date, where a tariff for the next year would have to extrapolate it (splits_comment). The task probes on the declared metric (5 of 9 folds) flag `no_signal` (TP-1, TP-2): their untuned families, fitted by squared error with the weight, all score worse than the weighted dummy (82.83): linear 85.14, random forest 96.11, LightGBM 106.66, the best single feature (`power_value_class`) 82.35; under the Gini on the windows of 2013 their linear family had scored 0.168 against 0. They read squared-error fits of a few large rates, whose relativities this metric punishes, while the actuarial fits above beat the constant (EV-3). The group probes find no gap between IID and grouped folds (weighted R^2 -0.008 in both). The leak probes on the contract folds find nothing: all features at weighted R^2 -0.012, every feature alone at 0.002 or below; copies across the split are LEAK-18's repeats (below).
- Metric (MET-11, MET-13; REVIEW.md issue 8, Lennart, 2026-11-08): `rescaled_mean_tweedie_deviance`, the exposure-weighted Tweedie deviance at power 1.5 of the charge per vehicle-year after each scored set's predictions are multiplied by sum(w y) / sum(w p), as the game scaled every player's premiums to one total; a stand-in for the game's market, closer to it than the normalized weighted Gini it replaces (the metric's reason). The factor reads the labels of the rows being scored, as the deviance does, and the model never sees it: on a validation fold it works the same way, each fold rescaled to its own claim total, and a learner that stops early on it needs it as a custom evaluation function. The floor `min_prediction` is 0.1 per vehicle-year, the collection's rule (MET-13): two orders below the smallest plausible mean, about 26 to 31 for the cheapest cells of two or three rating classes with at least 500 periods (vehicles over 5 years in contracts aged 4 to 5 years in zone 2: 844 periods, 25.7; fleet management N and power-value class 2: 689 periods, 30.7; the portfolio 173), so about 0.3, rounded down to a power of ten, in the release's units (the charges scaled by one constant); as for the 0.1 EUR of pricing_game_2017_french_mtpl, a convention that can change with the rule. No fitted model's prediction falls below it on the shipped folds. The floor applies before the rescaling, so the score ignores a common scale of the predictions only above it: a model predicts on the target's scale.
- Not added, measured on all of 2013 on the claim indicator (the same LightGBM, trained on 2011-2012): the contract's and the vehicle's claims and exposure of the previous year (ROC AUC 0.667 with them, 0.668 without; a known entity's history is legitimate, USE-10, but it carries nothing here), and the contract's vehicles in force at the period's start (0.667).
- Dropped: `vehicle_id` (the anonymised registration), `year` (the year of the period's start on every row), `period_end` (unknown at the start for the periods that end early; the realized length it sets ships as the weight `exposure`), `vehicle_category` (one value) and the files' unnamed row index. `contract_id`, the organisers' contract number, stays as the group column of the split, never a feature (it is apparently numbered in the order of subscription: median 14,885 for contracts of at most a year, 2,027 for those over 5 years, which the contract's age class carries).
- `insured_value_class` "ND" (not available) made missing: 87,093 periods (99.8%); the 135 others hold five value classes.
- Labels restored: `payment_frequency` A, S, T as annual, semi-annual, quarterly (the French "annuel", "semestriel", "trimestriel"); `new_company` 2 as Yes and 1 as No ("à 2 si création", rules Sec. 1). The other classes keep the organisers' codes: French labels for the ages and the deductible, anonymised numbers for the zone, activity, channel, formula, fleet size and power-value class.
- Dtypes: the four bands of a quantity are ordered categories, lowest first, the open end a level of its own (CLEAN-14): the contract's age ("<= 1 ans" to "> 5 ans"), the vehicle's age ("<= 5 ans", "> 5 ans"), the deductible ("1. 0" to "6. > 600") and the insured value ("<= 7.6K" to "137K - 380K"). `payment_frequency` is an ordered category by the number of payments a year, fewest first: annual < semi-annual < quarterly (1, 2 or 4), the same order as in spanish_motor_insurance_coverage_level_2022_2024 and pricing_game_2017_french_mtpl (Lennart, 2026-11-08, issue 8 of the first's REVIEW.md). The other class columns are unordered categories; the power-value class (11 levels, a combined power and value grid) has no documented order. `exposure_to_year_end` and `n_vehicles` numeric (`n_vehicles` is 1 on every period but 2, which hold 2; kept as the source ships it); `period_start` a date. `exposure` is the weight scoring column, never a feature.
- 11,807 periods (13.5%) repeat the features of another, 10,828 of them with the same target and 979 with another: vehicles of one fleet in the same period share every contract class and the start, so the length to the year's end, and differ only by their own two classes. Natural, kept (LEAK-18). The split by contract keeps a fleet's vehicles on one side; across it, 4.3% of the test periods have a copy of their features and start in training, from another fleet (3.7% with the same target only, mostly no claim; 8.6% without the start).
- The source's floor of 30 days (LEAK-41, last clause, as amended for this case on 2026-11-08, Lennart, REVIEW.md issue 7: a selection the source made before release, the same in train and test, that cannot be undone, defines the task's population and is sized in the notes): the organisers left out every period shorter than 30 days before release, in the training file and the 2014 pricing file alike, so every row passed a selection by its realized length. The lengths stop at an edge, not a taper (no period of 29 days, 909 of 30, about 700 a day at 32 to 40 days); a vehicle's consecutive periods leave 1,558 gaps of 1 to 29 days where the dropped periods would sit; no period starts after 2 December. By weight the cut is small, about 1.5% of the vehicle-years (the density at 30 to 59 days extrapolated down to one day; some 15% of the rows), and the same in every contract fold, which mixes the start cohorts (on the four-month windows of 2013 shipped until 2026-11-08 it was uneven, roughly 11%, 3% and 1.6% of their vehicle-years, newest first, by a rougher extrapolation that assumes a flat density). Short periods claim more per vehicle-year (early ends of 30 to 59 days 0.143 to 0.160, against 0.124 for those of 180 days or more), so the dropped ones likely did too. The cut periods and their claims are not published, so the selection cannot be undone; it is the same on the training and test sides, so under the amended rule it defines the task's population: the periods of cover of a month or more.
- Anomaly: the categorical levels are anonymised and the charges scaled by one constant (the record's generated-data tests of 2026-11-01: disclosure control, not generation); the charges are kept as published (the constant, 1.077841, changes no ranking).
- The newest periods lose no claims: claims per vehicle-year are 0.117, 0.119 and 0.119 in 2011 to 2013, and 0.115, 0.114 and 0.117 for the periods ending in the fourth quarter (LEAK-24 not triggered).
- Late-reported claims (SPLIT-9, SPLIT-10): a claim enters the files only once reported, and they hold the claims as of their extract (claims closed up to 2014, 41 still open, so their charges may still move) with no report date. Under the split by contract every period, in training or test, carries its claims as of that one extract, so no training label is more complete than a test label. The exception to SPLIT-10 for no gap before the January window of 2013 (Andrej, 2026-11-02; its ground restated on 2026-11-06) lapsed with the windows on 2026-11-08 (REVIEW.md issue 6). What a dated split would add, a tariff fit on 1 January that has not yet seen the late claims of 2012, can only be simulated: hiding the training charges of the claims that fall in the last 30 or 90 days of 2012 (each claim placed uniformly in its period; 134 and 377 periods) moved the January window of 2013 from 0.190 to 0.192 and 0.187 (normalized weighted Gini, regularised Tweedie LightGBM fitted with the weight, 5 seeds), within noise.
- CC (2026-11-06, Lennart): the target is the claim charge per vehicle-year over the realized period, `exposure` (the source's Exposition_au_risque, restored) its denominator, the weight scoring column and the `sample_weight`, never a feature (MET-14, MET-15, LEAK-41; issue 5, D11 of the exposure review); the length to 31 December stays a feature as `exposure_to_year_end` (LEAK-7, LEAK-37); the metric is the normalized weighted Gini of the rate, still a stand-in for the game's market; the scale stays the identity (CLEAN-16 as amended). Supersedes Andrej's call of 2026-11-02 on the target (the claim charge per period, issue 4): the exposure study measured later that the total over the realized period rewards predicting how long a vehicle stays (about 0.03 of the row Gini) and that the rate model ranks the rate better under the weighted Gini (0.153 against 0.138 for the model of the total; 0.154 against 0.136 on the shipped windows).
- CC (2026-11-06, Lennart): every window trains on the periods that started before 2013 (56,178 periods of 2011-2012, 24,674 vehicle-years), all closed by 31 December 2012, so no training row is admitted by its realized end (LEAK-41; issue 5, D11 of the exposure review). Supersedes Andrej's expanding training sides of 2026-11-02 (issue 2 (d)): the exposure study's red team measured later that the 2013 periods they admitted, those that ended early, claim more (0.127 and 0.131 claims per vehicle-year against 0.115 and 0.116 for the 2013 periods they left out; 10.8% and 4.0% of the training vehicle-years of the September and May windows), and LEAK-41 (2026-11-06) bars training on rows selected by their realized end.
- CC (2026-11-08, Lennart): the periods are split by contract, forced from temporal (REVIEW.md issue 6, reply (b), "Forced by contract"): `contract_id` is the group column of the default 3 x 3 grouped splits, never a feature, tagged ForcedGroupedFromTemporal (SPLIT-8); the windows and the exception to SPLIT-10 for no gap go. Supersedes the three four-month windows of 2013 on one training side (D11, the CC of 2026-11-06 above), which SPLIT-14 as amended on 2026-11-02 counts as one evaluation, and Andrej's expanding windows of 2026-11-02 (issue 2 (d)), already replaced by D11, which train on the 2013 periods chosen by their realized end (LEAK-41). The leak test across the contract folds passes, and on the 2013 periods the forced split scores as the valid window does (splits_comment).
- CC (2026-11-08, Lennart): the metric is `rescaled_mean_tweedie_deviance` (power 1.5, `min_prediction` 0.1 per vehicle-year, weighted by `exposure`), the stand-in for the game's market in place of the normalized weighted Gini (REVIEW.md issue 8 (B): "Agree. GO with the change in metric and use it going forward"). What sets this table apart from australian_vehicle_insurance_2004_2005 and spanish_motor_insurance_coverage_level_2022_2024, which keep the Gini: its original is a market that rescaled every tariff uniformly, and the closeness to it is measured (76 of 84 two-player markets against 44 for the Gini on the windows of 2013; 225 of 252 against 128 on the contract folds). It is the stand-in for a pricing game whose market rescales uniformly, for later datasets of that kind (MET-11).

## Splits

Grouped 3-fold splits by contract (`contract_id`), repeated three times, forced from temporal (SPLIT-8,
ForcedGroupedFromTemporal; Lennart, 2026-11-08, REVIEW.md issue 6): every period of a fleet's contract, in every
year, stays on one side; a test fold holds 6,012 or 6,013 contracts and 28,656 to 29,768 periods. The use case is
a tariff fit on the closed years and applied to the next (the game priced 2014 from 2011-2013, and the claims of
2014 were never published), but rows are cut at 31 December and the claims carry no dates, so the windows of a
temporal split are whole years: 2013 trained on 2011-2012 (64.4% of the rows) is the one valid window, and 2012
trained on 2011 holds 30.4%, below SPLIT-14's floor. Windows inside 2013 either share that training side, one
model scored on three cohorts of period lengths, which SPLIT-14 as amended on 2026-11-02 counts as one window
(shipped from 2026-11-06 to 2026-11-08), or train on the 2013 periods that ended before the window starts,
chosen by their realized end, which LEAK-41 bars (Andrej's expanding windows of 2026-11-02). What the dates
would change, on the folds' 2013 periods (regularised Tweedie LightGBM fitted with the weight, 3 seeds, 9
folds): the forced model scores 84.32 on the declared metric against 84.27 for the valid window's model,
trained on every period of 2011-2012 (+0.06, SD 0.52 over the folds), and 0.172 against 0.178 on the
normalized weighted Gini (-0.005, SD 0.012), so the forced split is no more optimistic on 2013 than the valid
window. The valid window's model without the test fleets' periods, a new fleet's cold start on about two thirds
of the training periods, loses 1.10 on the declared metric (SD 0.86) and 0.015 of the Gini (SD 0.021; 0.004,
SD 0.013, on the review panel's folds of 2026-11-06). In the valid window 79% to 81% of the folds' 2013 periods
belong to a contract insured in 2011-2012, where the forced split tests fleets never seen. A fold also mixes the
years: the charge per vehicle-year rises from 160 in 2011 to 184 in 2013, a level a model can read from the
start date where a tariff for the next year would have to extrapolate it, and a tariff fit on 1 January would
miss the late-reported claims of 2012 (the notes). The leak test across the split, as for
wisconsin_local_government_property_insurance_fund (each test year scored by a model trained without that
year's training periods, against one trained without as many random training periods; 9 folds), finds no
year-level leak: on the declared metric the year's own training periods gain -0.12 pooled (SD 0.60, a gain on
3 of 9 folds) with the start as its day of the year and -0.18 (SD 0.61, 4 of 9) with the start as a date; on
the Gini -0.007 (SD 0.016) and +0.008 (SD 0.012, 7 of 9), +0.005 within a year, against wisconsin's +0.113
pooled; the claims per vehicle-year are flat across the years (0.117, 0.119, 0.119). The leak probes on the
folds find nothing, and IID and grouped folds score alike (the notes). A vehicle keeps its contract (one of
68,485 has two), so a test fleet's vehicles are new too.

3 repeat(s) x 3 fold(s) with seed 4267; train 57,460 to 58,572 rows, test 28,656 to 29,768 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 58572 | 28656 |
| 0 | 1 | 58424 | 28804 |
| 0 | 2 | 57460 | 29768 |
| 1 | 0 | 57979 | 29249 |
| 1 | 1 | 58515 | 28713 |
| 1 | 2 | 57962 | 29266 |
| 2 | 0 | 58128 | 29100 |
| 2 | 1 | 58109 | 29119 |
| 2 | 2 | 58219 | 29009 |

## Group structure

One group is a fleet contract: `contract_id`, the organisers' "Numéro d'affaire" (rules, Sec. 1), with every period of cover of every vehicle of the fleet over 2011 to 2013: 18,037 contracts, 7,280 present in one year, 6,064 in two and 4,693 in all three; the largest holds 81 periods (0.05% of the vehicle-years), and a vehicle keeps its contract (one of 68,485 has two). The use case prices a fleet's periods with the year's tariff, fit on the closed years, but three years cut at 31 December give one valid temporal window (2013 trained on 2011-2012) where SPLIT-14 asks for three, so the periods are split by contract instead (SPLIT-8, ForcedGroupedFromTemporal): a test fleet is one the model has seen in no year, where 79.5% of the 2013 periods belong to a contract insured in an earlier year. Each period is one prediction, made from its own row.

| field | value |
|---|---|
| group column | `contract_id` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 18,037 |
| rows per group (min / median / max) | 1 / 3.0 / 81 |
| largest group | 0.1% of the rows |
| test groups per fold | 6,012 to 6,013 |
| groups of two or more rows with a single label | 79.5% |
| nearest neighbour in the same group | 3.5% of the rows (chance: 0.0%) |
| label variance explained by the group | 0.18 (shuffled groups: 0.20) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. The charge per realized vehicle-year, weighted by the vehicle-years

The source's length is realized: a period that ends before 31 December is known only at its end, and 57.4% of the periods end at a cut not known at the start, a quarter of them on a month's end. Those ends go with claims: in 2011-2012 a vehicle's last period in the file that ends early has more claims per vehicle-year than a period that runs to the year's end (a rate ratio of 1.22 given the rating classes). The target is therefore the charge per vehicle-year, each period weighted by its vehicle-years and never given them as a feature; the length to 31 December, known at the start, is the feature `exposure_to_year_end` (curation_comments).

| the period ends | periods | vehicle-years (realized) | claims | claims per vehicle-year |
|---|---|---|---|---|
| 31 December | 23611 | 14646 | 1627 | 0.111 |
| earlier, the vehicle goes on | 10845 | 3024 | 334 | 0.11 |
| earlier, the vehicle's last period in the file | 21722 | 7005 | 959 | 0.137 |

### 2. Whole contracts held out, forced from temporal

A tariff is fit on the closed years and applied to the next, but rows are cut at 31 December and the claims carry no dates, so the windows are whole years: 2013 trained on 2011-2012 is the one valid window, and 2012 trained on 2011 holds 30.4% of the rows, below the floor of 50%. Windows inside 2013 either share that one training side, one evaluation, or admit the 2013 periods that ended early, chosen by their realized end. The contracts recur across the years, so the periods are split by contract (SPLIT-8, ForcedGroupedFromTemporal); the claims per vehicle-year are flat across the years, and the leak test across the contract folds passes (splits_comment).

| year of the period's start | periods | vehicle-years (realized) | contracts | claims | rows of the earlier years (a yearly window's training side) | periods whose contract has an earlier year | periods ending before 31 December | claims per vehicle-year |
|---|---|---|---|---|---|---|---|---|
| 2011 | 26530 | 11588 | 10234 | 1357 | 0 | 0 | 0.578 | 0.117 |
| 2012 | 29648 | 13086 | 11305 | 1563 | 0.304 | 0.672 | 0.581 | 0.119 |
| 2013 | 31050 | 13864 | 11948 | 1648 | 0.644 | 0.795 | 0.586 | 0.119 |

### 3. A net recovery counts as no cost

The target is the period's claim charges summed, per vehicle-year. Claims under the IDA convention, where the insurer pays its client and recovers a flat amount from the other insurer, can net below 0; such a total is set to 0, as in pricing_game_2017_french_mtpl and frempl_french_motor_personal_line.

| index | periods |
|---|---|
| periods with a claim | 4250 |
| with two or more claims | 286 |
| with an IDA claim | 1156 |
| with no claim of positive charge | 523 |
| with a net total below 0 (set to 0) | 537 |

## Bundle checks

0 error(s), 0 warning(s), 0 info (27 checks run, plus the dataset's own checks).


Accepted on purpose:

- `dataset_duplicate_rows`: Vehicles of one fleet in the same period share every contract class and the start, so the length to the year's end, and differ only by their own two classes: natural repeats (LEAK-18). The split by contract keeps them on one side; 4.3% of the test periods have a copy with the same start from another fleet.
- `dataset_conflicting_duplicate_rows`: The same repeats as dataset_duplicate_rows: vehicles of one fleet with the same classes in the same period, with different claim charges per vehicle-year (another charge, or the same charge over another realized length). Natural (LEAK-18); the outcome of one vehicle is not the other's.
- `task_target_value_dominant`: Zero-inflated by nature: the claim charge per vehicle-year is 0 for 95.7% of the periods, those with no claim (95.1%) or whose claims net to 0 or less after IDA recoveries (0.6%, negative totals set to 0); not a cap or a placeholder.
- `meta_license_unknown`: The organisers state no licence for the game's files; CASdatasets, which redistributes the same tables, is GPL (>= 2).

## Data checks

### Feature summary

<details>
<summary>Show the table (19 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| insured_value_class | category | 87093 | 99.85 | 5 | 7.6K - 38K, 38K - 76K, 76K - 137K, 137K - 380K, &lt;= 7.6K |
| contract_age_class | category | 0 | 0 | 6 | > 5 ans, &lt;= 1 ans, 1 - 2 ans, 2 - 3 ans, 4 - 5 ans, 3 - 4 ans |
| new_company | category | 0 | 0 | 2 | No, Yes |
| fleet_management | category | 0 | 0 | 2 | N, P |
| zone | category | 0 | 0 | 6 | 3, 1, 2, 5, 4, 6 |
| fleet_size_class | category | 0 | 0 | 2 | 1, 2 |
| payment_frequency | category | 0 | 0 | 3 | quarterly, annual, semi-annual |
| vehicle_age_class | category | 0 | 0 | 2 | &lt;= 5 ans, > 5 ans |
| deductible_class | category | 0 | 0 | 6 | 2. 1 - 200, 3. 201 - 300, 4. 301 - 400, 5. 401 - 600, 6. > 600, 1. 0 |
| formula | category | 0 | 0 | 4 | 3, 5, 4, 2 |
| client_activity | category | 0 | 0 | 8 | 1, 7, 3, 6, 8, 4, 2, 5 |
| distribution_channel | category | 0 | 0 | 3 | 1, 2, 3 |
| power_value_class | category | 0 | 0 | 11 | 7, 4, 8, 9, 5, 6, 3, 2, 1, 10 |
| period_start | datetime64\[ns\] | 0 | 0 | 1003 | 2013-01-01 00:00:00, 2012-01-01 00:00:00, 2011-01-01 00:00:00, 2013-04-01 00:00… |
| exposure | float64 | 0 | 0 | 93 | 1.0, 0.25, 0.5, 0.08, 0.75, 0.1, 0.16, 0.09, 0.13, 0.12 |
| exposure_to_year_end | float64 | 0 | 0 | 95 | 1.0, 0.75, 0.5, 0.25, 0.84, 0.92, 0.67, 0.33, 0.42, 0.17 |
| claim_charge_per_vehicle_year | float64 | 0 | 0 | 3672 | 0.0, 140.1193, 128.5433, 2371.2501, 161.6761, 280.2386, 424.604, 233.7151, 207.… |
| n_vehicles | int64 | 0 | 0 | 2 | 1, 2 |
| contract_id | int64 | 0 | 0 | 18037 | 9744, 5569, 2281, 4202, 3251, 3067, 12940, 9443, 337, 8684 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 95.75 | 18.665 | 4.732 | 2.87013e+06 | 2.471 | log1p | 69871.8 | 69524.7 | lognormal |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| exposure | 87228 | 0.441811 | 0.316183 | 0.08 | 1 |
| n_vehicles | 87228 | 1.00002 | 0.00478834 | 1 | 2 |
| contract_id | 87228 | 8241.83 | 5193.01 | 1 | 20994 |
| exposure_to_year_end | 87228 | 0.717125 | 0.303319 | 0.08 | 1.82 |
| claim_charge_per_vehicle_year | 87228 | 191.839 | 1694.15 | 0 | 75929 |

### Categorical features

<details>
<summary>Show the table (53 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| client_activity | 1 | 1 | 20633 | 23.65 |
| client_activity | 2 | 7 | 16954 | 19.44 |
| client_activity | 3 | 3 | 16277 | 18.66 |
| client_activity | 4 | 6 | 10747 | 12.32 |
| client_activity | 5 | 8 | 9578 | 10.98 |
| contract_age_class | 1 | > 5 ans | 20330 | 23.31 |
| contract_age_class | 2 | &lt;= 1 ans | 18687 | 21.42 |
| contract_age_class | 3 | 1 - 2 ans | 12687 | 14.54 |
| contract_age_class | 4 | 2 - 3 ans | 12365 | 14.18 |
| contract_age_class | 5 | 4 - 5 ans | 11744 | 13.46 |
| deductible_class | 1 | 2. 1 - 200 | 39300 | 45.05 |
| deductible_class | 2 | 3. 201 - 300 | 27306 | 31.3 |
| deductible_class | 3 | 4. 301 - 400 | 13229 | 15.17 |
| deductible_class | 4 | 5. 401 - 600 | 3419 | 3.92 |
| deductible_class | 5 | 6. > 600 | 2015 | 2.31 |
| distribution_channel | 1 | 1 | 61935 | 71 |
| distribution_channel | 2 | 2 | 18622 | 21.35 |
| distribution_channel | 3 | 3 | 6671 | 7.65 |
| fleet_management | 1 | N | 57051 | 65.4 |
| fleet_management | 2 | P | 30177 | 34.6 |
| fleet_size_class | 1 | 1 | 44230 | 50.71 |
| fleet_size_class | 2 | 2 | 42998 | 49.29 |
| formula | 1 | 3 | 68235 | 78.23 |
| formula | 2 | 5 | 12247 | 14.04 |
| formula | 3 | 4 | 6713 | 7.7 |
| formula | 4 | 2 | 33 | 0.04 |
| insured_value_class | 1 | &lt;NA> | 87093 | 99.85 |
| insured_value_class | 2 | 7.6K - 38K | 56 | 0.06 |
| insured_value_class | 3 | 38K - 76K | 31 | 0.04 |
| insured_value_class | 4 | 76K - 137K | 30 | 0.03 |
| insured_value_class | 5 | 137K - 380K | 15 | 0.02 |
| new_company | 1 | No | 76412 | 87.6 |
| new_company | 2 | Yes | 10816 | 12.4 |
| payment_frequency | 1 | quarterly | 37472 | 42.96 |
| payment_frequency | 2 | annual | 28650 | 32.84 |
| payment_frequency | 3 | semi-annual | 21106 | 24.2 |
| period_start | 1 | 2013-01-01 00:00:00 | 12028 | 13.79 |
| period_start | 2 | 2012-01-01 00:00:00 | 11190 | 12.83 |
| period_start | 3 | 2011-01-01 00:00:00 | 9533 | 10.93 |
| period_start | 4 | 2013-04-01 00:00:00 | 1030 | 1.18 |
| period_start | 5 | 2012-04-01 00:00:00 | 1028 | 1.18 |
| power_value_class | 1 | 7 | 19906 | 22.82 |
| power_value_class | 2 | 4 | 19211 | 22.02 |
| power_value_class | 3 | 8 | 12842 | 14.72 |
| power_value_class | 4 | 9 | 12599 | 14.44 |
| power_value_class | 5 | 5 | 12419 | 14.24 |
| vehicle_age_class | 1 | &lt;= 5 ans | 58468 | 67.03 |
| vehicle_age_class | 2 | > 5 ans | 28760 | 32.97 |
| zone | 1 | 3 | 32071 | 36.77 |
| zone | 2 | 1 | 21324 | 24.45 |
| zone | 3 | 2 | 16365 | 18.76 |
| zone | 4 | 5 | 8701 | 9.98 |
| zone | 5 | 4 | 7875 | 9.03 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
