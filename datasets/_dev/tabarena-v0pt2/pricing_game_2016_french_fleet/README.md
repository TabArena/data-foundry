---
report_format: data-foundry-report-v2
unique_name: pricing_game_2016_french_fleet
container_format: 2
checksum: v2:57be91f15844b84f5d9064c9fdd86e9f1242e26a62f713e4a00300181f72aa7e
build: null
build_stale: false
data:
  n_rows: 87228
  n_features: 16
  dtypes:
    category: 13
    datetime64[ns]: 1
    float64: 3
    int64: 1
  n_test_dataset_rows: null
task:
  target: claim_charge_per_vehicle_year
  problem_type: regression
  metric: normalized_weighted_gini
  metric_origin: stand_in
  scoring_columns:
  - exposure
  sample_weight: exposure
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: period_start
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
  n_train:
    min: 56178
    max: 56178
  n_test:
    min: 5312
    max: 19229
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos: []
  accepted:
    dataset_duplicate_rows: 'Vehicles of one fleet in the same period share every
      contract class and the start, so the length to the year''s end, and differ only
      by their own two classes: natural repeats (LEAK-18). With `period_start` a feature
      no copy crosses the split.'
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
- Every window trains on the periods of 2011-2012
- A net recovery counts as no cost
---

# pricing_game_2016_french_fleet

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `claim_charge_per_vehicle_year`, scored with `normalized_weighted_gini` on temporal splits by `period_start`. 87,228 rows and 16 features. Source: Other (2016).

Not built yet. The current definition gives checksum `v2:57be91f15844b84f5d9064c9fdd86e9f1242e26a62f713e4a00300181f72aa7e`.

## In brief

**Question.** What will a vehicle of a French company's fleet cost in material-damage claims per vehicle-year of cover, from the contract's and the vehicle's rating classes and the length of cover to the year's end, known when its period of cover starts?

**Use case.** A fleet insurer setting its tariff: it fits the pure premium, the expected claim cost per vehicle-year, on the closed years and charges it for the time each vehicle stays in the fleet. The 2016 actuarial pricing game posed this pricing task on this portfolio.

**One row.** One vehicle of a fleet contract over one period with unchanged contract terms, cut at each change and at the year's end: 87,228 periods of 68,485 vehicles in 18,037 contracts of an unnamed French insurer, 2011 to 2013.

**Predicted.** The period's claim charges summed, per vehicle-year of the period (0 for 95.7% of the periods), net of the flat amounts recovered under the IDA convention between insurers, where the insurer pays its client and recovers a flat amount from the other insurer; a net recovery counts as 0. Each period counts by its vehicle-years in training and scoring. The charges are scaled by one constant of the release.

**Known at prediction time.** The contract's age, the client's activity, zone, fleet size and management, a new-company flag, the distribution channel, payment frequency, formula, deductible and insured value classes; the vehicle's age and power-value classes; the period's start date and the length of cover to the year's end. Most periods end earlier, at a cut not known at the start (a quarter on a month's end), so their vehicle-years are no input.

**What the test data stands for.** Tested on the periods starting in 2013 in three four-month windows, each trained on the periods of 2011-2012, all closed by then, as the year's tariff fit on the closed years; most fleets of 2013 were insured before.

**Our changes to the source.** We summed each period's claim charges, set the 537 net negative totals to 0 and divided by the period's vehicle-years, which weight the period; added the length of cover to the year's end; dropped the identifiers, the year and the period's end date, made the unknown insured value missing, and gave two codes their labels.

> **Use case fit: direct (the rows, features and split mirror the use case).** The rows are the periods an insurer prices, the features the rating classes and the length of cover it knows then, and each test window follows its training side. The target is the claim cost per vehicle-year a fleet tariff charges, weighted by the vehicle-years over which it is earned; the signal is in the claim frequency.

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
| data_tags | Non-IID, Temporal, Anonymized, Spatial |
| reference | Charpentier2016PricingGame |
| rows x columns | 87,228 x 18 |
| task.target | claim_charge_per_vehicle_year |
| task.problem_type | regression |
| task.metric | normalized_weighted_gini |
| task.sample_weight | exposure |
| task.split_regime | temporal_non_iid |
| task.time_on | period_start |

**Metric**

| field | value |
|---|---|
| name | `normalized_weighted_gini` (custom; takes value; higher is better) |
| origin | stand_in: a stand-in for the source's metric, which cannot be computed |
| original | each player's result in the 2014 market the organisers ran as a price aggregator: each insured going to a company drawn at random among the cheapest premiums, every player's premiums scaled by one uniform factor to a total of 2.5 million euros (rules, Sec. 4 'Règles du Jeu') |
| reference | http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf |
| definition | WG(y, p) / WG(y, y), WG = sum L_i R_(i-1) - sum L_(i-1) R_i over rows sorted by descending p, R the cumulative weight share, L the cumulative share of weight * y (tied p form one step, the mean over their orderings) |
| reason | The market needs the other players' premiums and the claims of 2014, neither published. The uniform scaling ('un facteur d'inflation appliqué uniformément') took away each player's price level, so the market rewarded the relative prices; the Gini scores their order, not their spread (a weighted Tweedie GLM and the same GLM with its relativities doubled on the log scale both score 0.173). The normalized Gini is the metric of the insurers' Kaggle competitions (Allstate 2011, Liberty Mutual 2014), here in Liberty Mutual's weighted form: the periods are ranked by the predicted charge per vehicle-year and each counts by its vehicle-years, so the score rewards the rate a fleet tariff charges, not a guess of how long a vehicle stays (MET-15). pricing_game_2017_french_mtpl, whose game kept the price level and ruined a player at 170% losses, scores a Tweedie deviance instead. The game's page (actinfo.hypotheses.org/69) and CASdatasets' pricingame.Rd name no other metric. On the shipped windows (newest first, 5 seeds) a regularised Tweedie LightGBM fitted with the weight scores 0.114, 0.158 and 0.190, a weighted Tweedie GLM 0.159, 0.171 and 0.200, the length to 31 December and the start alone -0.016 on average, the weighted constant 0; a model of the charge over the realized period, the target until 2026-11-06, ranks the rate at 0.136 on average against 0.154. The closeness to the market, measured on the shipped windows by the game's rule (8 tariffs, among them the GLM and the LightGBM with their relativities flattened or steepened, each rescaled to the window's claim total; each period goes to the cheaper premium; every two-player market, 84 pairs): the Gini picks the market's winner in 44 pairs and ties on 21, as it cannot see a change of spread, while the exposure-weighted Tweedie deviance (power 1.5) after the same uniform rescaling picks it in 76; among the fitted tariffs alone (two LightGBMs, the GLM, the constant; 18 pairs) the two are close, 15 for the Gini and 16. Whether the Gini stays the stand-in with this shortfall is open for the curator (REVIEW.md issue 8). |
| inputs | weight: `exposure` |

**Scoring columns**

Kept in the frame for the metric; do not use them as features. Drop them from the inputs (`feature_columns(container)`), then pass the test rows' values to the scorer (`data_foundry.v2.metrics.scorer(container)(y_test, y_pred, test_idx)`).

| column | role | how the metric uses it | model input |
|---|---|---|---|
| `exposure` | weight | normalized_weighted_gini: the period's vehicle-years (the source's Exposition_au_risque, 0.08 to 1), realized: 57.4% of the periods end before 31 December at a cut not known at the start (a quarter of them on a month's end), known only when it comes. The rate's denominator; each row's weight in the metric and in training; never a feature | training weight; never a feature |

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

The first 5 of 87,228 rows of the final frame (the oldest rows: the frame is sorted by `period_start`); 12 of 18 columns, the target first. Cells are cut at 40 characters.

| claim_charge_per_vehicle_year | period_start | contract_age_class | new_company | fleet_management | zone | fleet_size_class | payment_frequency | exposure | vehicle_age_class | deductible_class | n_vehicles |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2011-01-01 00:00:00 | 1 - 2 ans | Yes | P | 2 | 2 | quarterly | 1 | &lt;= 5 ans | 4. 301 - 400 | 1 |
| 0 | 2011-01-01 00:00:00 | 2 - 3 ans | Yes | P | 4 | 1 | annual | 1 | &lt;= 5 ans | 3. 201 - 300 | 1 |
| 0 | 2011-01-01 00:00:00 | 1 - 2 ans | No | P | 1 | 2 | semi-annual | 0.25 | > 5 ans | 2. 1 - 200 | 1 |
| 2204.39 | 2011-01-01 00:00:00 | 4 - 5 ans | No | N | 1 | 2 | annual | 0.16 | &lt;= 5 ans | 2. 1 - 200 | 1 |
| 0 | 2011-01-01 00:00:00 | 1 - 2 ans | Yes | P | 3 | 1 | quarterly | 1 | > 5 ans | 2. 1 - 200 | 1 |

## Curation notes

We start with train_contrats.csv and train_sinistres.csv, the files the organisers of the second actuarial pricing game (2016) gave its players.

- Prediction point: the start of a vehicle's period of cover, when the insurer prices it with the year's tariff, fit on the closed years. The game asked for "une prime pure" (a pure premium) for each of the 32,772 periods of 2014 in test_contrats.csv (rules, Sec. 2, which write 37,772), with the periods of 2011 to 2013 to learn from; the claim charge per vehicle-year is the pure premium's rate, which times a period's vehicle-years gives the period's pure premium. Known then: the contract's and the vehicle's rating classes, the period's start and its length of cover to the year's end. Not known: the period's claims, and when a period cut short will end.
- Source and year: the game's page (actinfo.hypotheses.org/69, 17 July 2016) dates the first stage "entre le 15 juillet et le 15 septembre", and the files carry a Last-Modified date of 13 July 2016. The rules (pricing-game-2016-FR.pdf, Sec. 1) describe every column; CASdatasets' copy holds the same values, its levels renamed one to one, except its DirectComp, which is 0 for 1,064 of the 1,190 claims the organisers flag IDA (a problem of that copy, not used here).
- The portfolio is commercial fleets with a material-damage cover, not the "private motor insurance" of CASdatasets' documentation: the rules describe "Mode de gestion de la flotte", "Taille de la flotte" and "Classe de franchise de la garantie DTA" (DTA is the usual French abbreviation of an all-accident damage cover), and 1,190 of the 4,568 claims fall under the IDA convention between insurers. The row names of the training file and the 2014 file together run exactly from 1 to 120,000, so the files are likely a sample of the portfolio: counts per contract (at most 12 vehicles of a contract at once) and a vehicle's last period describe the file, not the fleets.
- Target `claim_charge_per_vehicle_year`: the charges (CHARGE_SINISTRE) of the period's claims summed, 0 without a claim, divided by the period's vehicle-years `exposure` (MET-14); the summed charge leaves the frame as a part of the target, and `_clean` checks that the target times `exposure` gives it back. Each of the 4,568 claims joins one period on the contract, the registration, the year and the period's dates, and the claim count equals the joined claims on every period (checked in `_load_raw`). 4,250 periods have a claim (286 two or more, at most 7); 3,711 have a positive total (median 1,339, at most 13,992), so 95.7% of the targets are 0; per vehicle-year the positive values run up to 75,929, a large charge on a period of a month or two. The curator first chose the claim indicator (2026-10-30, record), switched to the charge per period on 2026-11-02 after a measurement (the charge is what the insurer prices and what the game asked for), and to the charge per vehicle-year on 2026-11-06 (CC below).
- 537 periods net below 0 set to 0 (down to -1,863), as pricing_game_2017_french_mtpl and frempl_french_motor_personal_line do (the family call of 2026-10-30: "a net recovery is no claim cost of the year"). They are claims under the IDA convention ("1 si sinistre Indemnisation Direct de l'Assuré", rules Sec. 1), where the insurer pays its client and recovers a flat amount, not the cost, from the other insurer; every claim with a charge of 0 or less is IDA, and 126 of the 1,190 IDA claims are at 50% responsibility. Tweedie and Poisson losses need a non-negative target. The total is clipped, not each claim (65 periods mix signs, 16 of them net below 0); the clip raises the total claim cost by 4.3%.
- Only the frequency carries signal. Among the periods with a positive charge, the log charge is not predictable from the classes (R^2 -0.06 for LightGBM, -0.02 for ridge, measured on 2011-2012 to 2013), and a weighted Poisson model of the claims per vehicle-year ranks the charges per vehicle-year at 0.164, 0.167 and 0.210 on the windows (newest first), against 0.114, 0.158 and 0.190 for the weighted Tweedie model of the charge (normalized weighted Gini, regularised LightGBM, 5 seeds). The task is the frequency task with severity noise on top. Raw rate, not log1p (CLEAN-16 as amended: a rate scored by a Gini keeps the scale the curator chose): the Gini ranks by the expected charge per vehicle-year, which a log1p fit transformed back orders by its geometric mean instead. A fit weighted by the vehicle-years on this scale estimates E[charge | x] / E[vehicle-years | x], the charge per vehicle-year that breaks even.
- Exposure (LEAK-41, MET-14, MET-15; issue 5, resolved 2026-11-06): `exposure` is the source's Exposition_au_risque, "Véhicules année (exposition au risque)": the period's vehicle-years, (end - start + 1) / 365 (/ 366 in the leap year 2012) times the period's vehicles (2 on two periods), rounded to 0.01, which `_clean` checks on every period. It is realized: of the 87,228 periods of 68,485 vehicles (2011 to 2013), 57.4% end before 31 December at a cut not known at the start (a quarter of them on a month's end) and 0.8% at a contract anniversary, so their length is known only at their end. The task divides the period's charge by it and weights each period by it in training and scoring (the weight scoring column and the `sample_weight`), never as a feature. The part known at the start ships as the feature `exposure_to_year_end`, the same formula to 31 December (LEAK-7, LEAK-37). The shipped features were leak-free since the fix of 2026-11-02 (next bullet), but the target summed over the realized period still rewarded predicting how long a vehicle stays: about 0.03 of the row Gini (the direct model of the total 0.210 against 0.182 for its rate times the length to 31 December; a rough attribution of the exposure study of 2026-11-05). A fit that ignores the weight loses 0.010 of the declared metric on the shipped windows (SD 0.009, lower on 4 of 5 seeds; 0.006 in the study; 0.005, lower on 2 of 3 seeds, in the review panel's run of 2026-11-06): within seed noise, little since no period is shorter than 30 days.
- Why the rate (CC below): a fleet's premium is regularised per vehicle as vehicles come in and go out (a French fleet-insurance guide, echangesassurances.org: "La prime est régularisée en fin d'année sur la base du parc réel (pro-rata temporis)"; AXA Belgium's fleet terms set a regularisable premium apart from a non-regularisable one, so not every fleet contract is), so a fleet tariff charges a rate per vehicle-year, earned over the time the vehicle stays. A realized time on risk is also a valid weight when the outcome cuts it short: when a period's end is a stopping time of its claim history, the weighted fit estimates E[charge | x] / E[vehicle-years | x], the rate that breaks even per vehicle-year (the exposure study's stopping-time argument, checked there by simulation; a stopping rule driven by unobserved risk was not simulated). The game's 2014 file gave its players each period's realized end and length (58.2% end before 31 December 2014); that is no ground here, since a host's test file is a holdout of the same snapshot, not deployment data (LEAK-38).
- The realized length as a feature (fixed on 2026-11-02): until then `exposure` was a feature holding the realized length, and with `period_start` a feature it gave back the dropped end. On the three windows it added ROC AUC on the claim indicator +0.040, +0.055 and +0.052 over the length known at the start (regularised LightGBM on the rating classes and the start's day of the year, 3 seeds), and the early ends go with claims: a rate ratio of 1.22 [1.12, 1.33] given the rating classes (Poisson GLM with the length as offset, 2011-2012). Confirmed by the curator (Andrej, 2026-11-02) and recorded as the LEAK-10 case for time on risk cut short by the outcome: the cut is fixed where the data locates it. With the rate, the realized length is the weight alone. Probe 22 (LEAK-41: both arms, the decision on the worse): the features predict the realized vehicle-years at R^2 0.38, mostly through `fleet_management` and `exposure_to_year_end`, both known at the start, so they stay (USE-6). The L2 arm has no power here: the weight itself, as a feature, gains -0.001 there (SD 0.052). In the weighted Tweedie arm the weight as a feature gains +0.007 (SD 0.028; +0.012, SD 0.007, in the review panel's 3-seed run of 2026-11-06), and no feature's gain goes through the weight by more than one SD (`exposure_to_year_end` +0.017, SD 0.029; `distribution_channel` +0.011, SD 0.036; `client_activity` +0.008; `fleet_size_class` +0.005; `fleet_management` -0.004). 1/vehicle-years alone scores 0.029, the ceiling a proxy would reach. On the shipped windows (5 seeds) the time features (`exposure_to_year_end`, `period_start`) add 0.007 to the weighted Tweedie fit (SD 0.009; 0.003 in the review panel's run), within seed noise, and 0.001 to the weighted L2 fit; the realized vehicle-years as a feature would add 0.013 to the Tweedie fit (on 5 of 5 seeds).
- The covariates carry the signal: on the three windows (newest first) a regularised Tweedie LightGBM fitted with the weight scores a normalized weighted Gini of 0.114, 0.158 and 0.190 (bootstrap standard errors 0.068, 0.054 and 0.023), an untuned one 0.105, 0.098 and 0.183, a weighted Tweedie GLM 0.159, 0.171 and 0.200, the length to 31 December and the start's day of the year alone 0.005, -0.027 and -0.027, and the weighted constant 0 (5 seeds; the start enters as its day of the year). The models beat the constant on every window, so the task is not trivial (TP-4), on the newest window (103 positive charges) by about 1.7 standard errors. A weighted Tweedie deviance (power 1.5) orders them otherwise. Raw, it also scores the level, and puts the GLM below the weighted constant on every window (89.9 against 91.2 on average) and the LightGBM above it on the two newest (94.9); rescaled uniformly to each window's claim total, as the game scaled every player's premiums, it scores the relative prices: the GLM 89.6, the constant 90.8 and the LightGBM 91.3 (window means), the LightGBM, whose relativities run too steep, behind the flat tariff (the metric is open, REVIEW.md issue 8). The charge per vehicle-year trends up: 167 on the training side, 180 to 205 in the 2013 windows, a level a tariff loads apart and that neither the Gini nor the game's uniform scaling scores. The task probes flag `no_signal` and `drift_baseline` (TP-1, TP-2): they score R^2, which follows a few large rates (best family linear, R^2 0.001); under the declared metric the linear family scores 0.168, the random forest 0.121 and the probes' untuned L2 LightGBM 0.003, against 0 for the weighted dummy, as for pricing_game_2017_french_mtpl. The leak probes find nothing: every feature alone at R^2 0.001 or below; 9.8% of the test rows have a copy of their features in training once the start date is left out, none with it.
- Not added, measured on all of 2013 on the claim indicator (the same LightGBM, trained on 2011-2012): the contract's and the vehicle's claims and exposure of the previous year (ROC AUC 0.667 with them, 0.668 without; a known entity's history is legitimate, USE-10, but it carries nothing here), and the contract's vehicles in force at the period's start (0.667).
- Dropped: `contract_id` (apparently numbered in the order of subscription: median 14,885 for contracts of at most a year, 2,027 for those over 5 years, which the contract's age class carries) and `vehicle_id` (the anonymised registration), `year` (the year of the period's start on every row), `period_end` (unknown at the start for the periods that end early; the realized length it sets ships as the weight `exposure`), `vehicle_category` (one value) and the files' unnamed row index.
- `insured_value_class` "ND" (not available) made missing: 87,093 periods (99.8%); the 135 others hold five value classes.
- Labels restored: `payment_frequency` A, S, T as annual, semi-annual, quarterly (the French "annuel", "semestriel", "trimestriel"); `new_company` 2 as Yes and 1 as No ("à 2 si création", rules Sec. 1). The other classes keep the organisers' codes: French labels for the ages and the deductible, anonymised numbers for the zone, activity, channel, formula, fleet size and power-value class.
- Dtypes: the four bands of a quantity are ordered categories, lowest first, the open end a level of its own (CLEAN-14): the contract's age ("<= 1 ans" to "> 5 ans"), the vehicle's age ("<= 5 ans", "> 5 ans"), the deductible ("1. 0" to "6. > 600") and the insured value ("<= 7.6K" to "137K - 380K"). `payment_frequency` is an ordered category by the number of payments a year, fewest first: annual < semi-annual < quarterly (1, 2 or 4), the same order as in spanish_motor_insurance_coverage_level_2022_2024 and pricing_game_2017_french_mtpl (Lennart, 2026-11-08, issue 8 of the first's REVIEW.md). The other class columns are unordered categories; the power-value class (11 levels, a combined power and value grid) has no documented order. `exposure_to_year_end` and `n_vehicles` numeric (`n_vehicles` is 1 on every period but 2, which hold 2; kept as the source ships it); `period_start` a date. `exposure` is the weight scoring column, never a feature.
- 11,807 periods (13.5%) repeat the features of another, 10,828 of them with the same target and 979 with another: vehicles of one fleet in the same period share every contract class and the start, so the length to the year's end, and differ only by their own two classes. Natural, kept (LEAK-18).
- The source's floor of 30 days (LEAK-41, last clause, as amended for this case on 2026-11-08, Lennart, REVIEW.md issue 7: a selection the source made before release, the same in train and test, that cannot be undone, defines the task's population and is sized in the notes): the organisers left out every period shorter than 30 days before release, in the training file and the 2014 pricing file alike, so every row passed a selection by its realized length. The lengths stop at an edge, not a taper (no period of 29 days, 909 of 30, about 700 a day at 32 to 40 days); a vehicle's consecutive periods leave 1,558 gaps of 1 to 29 days where the dropped periods would sit; no period starts after 2 December. By weight the cut is small, about 1.5% of the vehicle-years (the density at 30 to 59 days extrapolated down to one day; some 15% of the rows), and uneven across the windows, roughly 11%, 3% and 1.6% of their vehicle-years, newest first (a rougher extrapolation that assumes a flat density). Short periods claim more per vehicle-year (early ends of 30 to 59 days 0.143 to 0.160, against 0.124 for those of 180 days or more), so the dropped ones likely did too. The cut periods and their claims are not published, so the selection cannot be undone; it is the same on the training and test sides, so under the amended rule it defines the task's population: the periods of cover of a month or more.
- Anomaly: the categorical levels are anonymised and the charges scaled by one constant (the record's generated-data tests of 2026-11-01: disclosure control, not generation); the charges are kept as published (the constant, 1.077841, changes no ranking).
- The newest periods lose no claims: claims per vehicle-year are 0.117, 0.119 and 0.119 in 2011 to 2013, and 0.115, 0.114 and 0.117 for the periods ending in the fourth quarter (LEAK-24 not triggered).
- Note: claims of the periods that close late in 2012 may have been reported only after the year's tariff is fit. The files hold the counts as of their extract (claims closed up to 2014, 41 still open) and no report date, so the delay can only be simulated: hiding the training charges of the claims that fall in the last 30 or 90 days of 2012 (each claim placed uniformly in its period; 134 and 377 periods, 5 seeds) moves the January window from 0.190 to 0.192 and 0.187 (regularised Tweedie LightGBM fitted with the weight); at the May and September windows' start those claims are four and eight months old. Applied to every window, as if the year's tariff were fit once on 1 January 2013, it moves the window mean from 0.154 to 0.151 and 0.119: the September window falls to 0.101 and 0.015, as the training periods that start late in 2012 lose most of their claims and the model learns that late starts claim little. 41 claims were still open at the extract, so their charges may still move. A simulation, not a measurement. No gap separates the January window from its training side: an exception to SPLIT-10 that serves SPLIT-14's floor (Andrej, 2026-11-02). With every training label fixed at 31 December 2012, a gap inside 2012 would admit the 2012 periods by their realized end (LEAK-41), and a whole year leaves 2011 alone, 30.4% of the rows. The May and September windows start four and eight months after the training side ends.
- CC (2026-11-06, Lennart): the target is the claim charge per vehicle-year over the realized period, `exposure` (the source's Exposition_au_risque, restored) its denominator, the weight scoring column and the `sample_weight`, never a feature (MET-14, MET-15, LEAK-41; issue 5, D11 of the exposure review); the length to 31 December stays a feature as `exposure_to_year_end` (LEAK-7, LEAK-37); the metric is the normalized weighted Gini of the rate, still a stand-in for the game's market; the scale stays the identity (CLEAN-16 as amended). Supersedes Andrej's call of 2026-11-02 on the target (the claim charge per period, issue 4): the exposure study measured later that the total over the realized period rewards predicting how long a vehicle stays (about 0.03 of the row Gini) and that the rate model ranks the rate better under the weighted Gini (0.153 against 0.138 for the model of the total; 0.154 against 0.136 on the shipped windows).
- CC (2026-11-06, Lennart): every window trains on the periods that started before 2013 (56,178 periods of 2011-2012, 24,674 vehicle-years), all closed by 31 December 2012, so no training row is admitted by its realized end (LEAK-41; issue 5, D11 of the exposure review). Supersedes Andrej's expanding training sides of 2026-11-02 (issue 2 (d)): the exposure study's red team measured later that the 2013 periods they admitted, those that ended early, claim more (0.127 and 0.131 claims per vehicle-year against 0.115 and 0.116 for the 2013 periods they left out; 10.8% and 4.0% of the training vehicle-years of the September and May windows), and LEAK-41 (2026-11-06) bars training on rows selected by their realized end.

## Splits

Three test windows, the periods starting in 2013 by thirds of the year (September to December, May to August,
January to April, newest first): 5,312, 6,509 and 19,229 periods, 987, 2,218 and 10,659 vehicle-years. Every
window trains on the periods that started before 2013, the 56,178 periods of 2011-2012 (64.4% of the rows,
24,674 of the 38,538 vehicle-years); rows are cut at 31 December, so each of them closed by 31 December 2012
and its label is known at every window's start. The use case is a tariff: the game priced every period of 2014
from 2011-2013, and the claims of 2014 were never published, so 2013 is the test year (suggested on 2026-10-30
and accepted with the curator's Yes). Until 2026-11-06 each window trained on every period closed before it
starts (67,886, 61,797 and 56,178 periods; Andrej, 2026-11-02). From 2013 on that admitted only the periods
that ended early, which claim more: 0.127 and 0.131 claims per vehicle-year against 0.115 and 0.116 for the 2013
periods still running, 10.8% and 4.0% of the training vehicle-years of the September and May windows. No
training row is now admitted by its realized end (LEAK-41; the curator's call of 2026-11-06). The claims carry
no dates, so a period still running cannot enter with its claims to date, and between two year ends a training
side can grow only by the periods that ended early: the three windows share one training side, one model
scored on three cohorts. SPLIT-14 as amended on 2026-11-02 counts windows that share a training side as one
window; whether to amend it for this case or ship the task forced (SPLIT-8) is open for the curator. On the old
training sides the same model scored 0.137, 0.160 and 0.190 (newest first), on the shared one 0.114, 0.158 and
0.190 (regularised Tweedie LightGBM fitted with the weight, 5 seeds). Three windows, not the nine of the
convention (SPLIT-15): finer windows only cut the same test rows into noisier pieces. A period's start caps its
length, so each window holds one cohort of lengths: the commonest start is 1 January (12,028 periods in 2013),
the claims per vehicle-year are 0.129, 0.122 and 0.117 (newest first), and the share of periods with a claim
follows the length (2.3%, 3.9%, 6.0%). A window's score ranks the periods within its cohort, and the mean over
the windows runs below a score pooled over 2013 (0.154 against 0.171, the same model). The newest window is the
smallest and the noisiest (123 periods with a claim, 103 with a positive charge; bootstrap standard error
0.068). No gap separates the January window from the training side (SPLIT-10; the notes give the reason and
the simulated bound); the May and September windows start four and eight months after it ends. Fleets and
vehicles recur across the cutoff, as a tariff prices the insurer's known fleets (SPLIT-13): 76-81% of the test
periods belong to a contract in training, 23-26% to a vehicle in training.

3 repeat(s) x 1 fold(s) with seed 4267; train 56,178 rows, test 5,312 to 19,229 rows. Prediction horizon: 4 months.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 56178 | 5312 | 2011-01-01 00:00:00 | 2012-12-02 00:00:00 | 2013-09-01 00:00:00 | 2013-12-02 00:00:00 |
| 1 | 0 | 56178 | 6509 | 2011-01-01 00:00:00 | 2012-12-02 00:00:00 | 2013-05-01 00:00:00 | 2013-08-31 00:00:00 |
| 2 | 0 | 56178 | 19229 | 2011-01-01 00:00:00 | 2012-12-02 00:00:00 | 2013-01-01 00:00:00 | 2013-04-30 00:00:00 |

## Decisions

### 1. The charge per realized vehicle-year, weighted by the vehicle-years

The source's length is realized: a period that ends before 31 December is known only at its end, and 57.4% of the periods end at a cut not known at the start, a quarter of them on a month's end. Those ends go with claims: in 2011-2012 a vehicle's last period in the file that ends early has more claims per vehicle-year than a period that runs to the year's end (a rate ratio of 1.22 given the rating classes). The target is therefore the charge per vehicle-year, each period weighted by its vehicle-years and never given them as a feature; the length to 31 December, known at the start, is the feature `exposure_to_year_end` (curation_comments).

| the period ends | periods | vehicle-years (realized) | claims | claims per vehicle-year |
|---|---|---|---|---|
| 31 December | 23611 | 14646 | 1627 | 0.111 |
| earlier, the vehicle goes on | 10845 | 3024 | 334 | 0.11 |
| earlier, the vehicle's last period in the file | 21722 | 7005 | 959 | 0.137 |

### 2. Every window trains on the periods of 2011-2012

Rows are cut at 31 December, so every period that started before 2013 closed by 31 December 2012. Training on the periods closed before each window starts admitted from 2013 on only the periods that ended early, which claim more than the 2013 periods still running then; claims carry no dates, so those could not join with their claims to date.

| test window | test periods | test vehicle-years | training periods | training vehicle-years | 2013 periods closed before (admitted until 2026-11-06) | their claims per vehicle-year | 2013 periods still running (left out) | claims per vehicle-year of those |
|---|---|---|---|---|---|---|---|---|
| 2013-09-01 to 2014-01-01 | 5312 | 987 | 56178 | 24674 | 11708 | 0.127 | 14030 | 0.115 |
| 2013-05-01 to 2013-09-01 | 6509 | 2218 | 56178 | 24674 | 5619 | 0.131 | 13610 | 0.116 |
| 2013-01-01 to 2013-05-01 | 19229 | 10659 | 56178 | 24674 | 0 | nan | 0 | nan |

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

- `dataset_duplicate_rows`: Vehicles of one fleet in the same period share every contract class and the start, so the length to the year's end, and differ only by their own two classes: natural repeats (LEAK-18). With `period_start` a feature no copy crosses the split.
- `dataset_conflicting_duplicate_rows`: The same repeats as dataset_duplicate_rows: vehicles of one fleet with the same classes in the same period, with different claim charges per vehicle-year (another charge, or the same charge over another realized length). Natural (LEAK-18); the outcome of one vehicle is not the other's.
- `task_target_value_dominant`: Zero-inflated by nature: the claim charge per vehicle-year is 0 for 95.7% of the periods, those with no claim (95.1%) or whose claims net to 0 or less after IDA recoveries (0.6%, negative totals set to 0); not a cap or a placeholder.
- `meta_license_unknown`: The organisers state no licence for the game's files; CASdatasets, which redistributes the same tables, is GPL (>= 2).

## Data checks

### Feature summary

<details>
<summary>Show the table (18 rows)</summary>

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
| claim_charge_per_vehicle_year | float64 | 0 | 0 | 3672 | 0.0, 140.1193, 128.5433, 2371.2501, 161.6761, 280.2386, 424.604, 799.8766, 5265… |
| n_vehicles | int64 | 0 | 0 | 2 | 1, 2 |

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
