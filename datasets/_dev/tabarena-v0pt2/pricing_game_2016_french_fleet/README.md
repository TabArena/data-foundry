---
report_format: data-foundry-report-v2
unique_name: pricing_game_2016_french_fleet
container_format: 2
checksum: v2:e9cb550ccd04bef571a1bad1ad290dea3b4459924074dcb1151a074ace03e609
build: null
build_stale: false
data:
  n_rows: 87228
  n_features: 16
  dtypes:
    category: 13
    datetime64[ns]: 1
    float64: 2
    int64: 1
  n_test_dataset_rows: null
task:
  target: claim_charge
  problem_type: regression
  metric: normalized_gini
  metric_origin: stand_in
  scoring_columns: null
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
    max: 67886
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
      contract class and the start, so the length, and differ only by their own two
      classes: natural repeats (LEAK-18). With `period_start` a feature no copy crosses
      the split.'
    dataset_conflicting_duplicate_rows: 'The same repeats as dataset_duplicate_rows:
      vehicles of one fleet with the same classes in the same period, with different
      claim charges. Natural (LEAK-18); the outcome of one vehicle is not the other''s.'
    task_target_value_dominant: 'Zero-inflated by nature: the claim charge is 0 for
      95.7% of the periods, those with no claim (95.1%) or whose claims net to 0 or
      less after IDA recoveries (0.6%, negative totals set to 0); not a cap or a placeholder.'
    meta_license_unknown: The organisers state no licence for the game's files; CASdatasets,
      which redistributes the same tables, is GPL (>= 2).
decisions:
- The period's length is the one known at its start
- A net recovery counts as no cost
---

# pricing_game_2016_french_fleet

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `claim_charge`, scored with `normalized_gini` on temporal splits by `period_start`. 87,228 rows and 16 features. Source: Other (2016).

Not built yet. The current definition gives checksum `v2:e9cb550ccd04bef571a1bad1ad290dea3b4459924074dcb1151a074ace03e609`.

## In brief

**Question.** What will a vehicle of a French company's fleet cost in material-damage claims over a period of cover, from the contract's and the vehicle's rating classes and the length of cover to the year's end, known at the start?

**Use case.** A fleet insurer setting its tariff: it fits the pure premium, the expected claim cost per vehicle and period, on the periods closed so far and prices each fleet vehicle's cover with it. The 2016 actuarial pricing game posed this pricing task on this portfolio.

**One row.** One vehicle of a fleet contract over one period with unchanged contract terms, cut at each change and at the year's end: 87,228 periods of 68,485 vehicles in 18,037 contracts of an unnamed French insurer, 2011 to 2013.

**Predicted.** The period's claim charges summed (0 for 95.7% of the periods), net of the flat amounts recovered under the IDA convention between insurers, where the insurer pays its client and recovers a flat amount from the other insurer; a net recovery counts as 0. The charges are scaled by one constant of the release.

**Known at prediction time.** The contract's age, the client's activity, zone, fleet size and management, a new-company flag, the distribution channel, payment frequency, formula, deductible and insured value classes; the vehicle's age and power-value classes; the period's start date and the length of cover to the year's end, known at the start. Most periods end earlier, at a cut nobody scheduled, which is not known then.

**What the test data stands for.** Tested on the periods starting in 2013 in three four-month windows, each trained on every period closed before the window starts, as a tariff refit every four months; most fleets of 2013 were insured before.

**Our changes to the source.** We summed each period's claim charges and set the 537 net negative totals to 0, replaced the period's realised length by its length to the year's end, dropped the identifiers, the year and the period's end date, made the unknown insured value missing, and gave two codes their labels.

> **Use case fit: direct (the rows, features and split mirror the use case).** The rows are the periods an insurer prices, the features the rating classes and the length of cover it knows then, and each test window follows its training side. The target sums the claims over the cover the vehicle kept, so it also holds how long the vehicle stays, which the insurer can only expect at pricing; the signal is in the claim frequency.

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
| license |  |
| data_tags | Non-IID, Temporal, Anonymized, Spatial |
| reference | Charpentier2016PricingGame |
| rows x columns | 87,228 x 17 |
| task.target | claim_charge |
| task.problem_type | regression |
| task.metric | normalized_gini |
| task.split_regime | temporal_non_iid |
| task.time_on | period_start |

**Metric**

| field | value |
|---|---|
| name | `normalized_gini` (custom; takes value; higher is better) |
| origin | stand_in: a stand-in for the source's metric, which cannot be computed |
| original | each player's result in the 2014 market the organisers ran as a price aggregator: each insured going to a company drawn at random among the cheapest premiums, every player's premiums scaled by one uniform factor to a total of 2.5 million euros (rules, Sec. 4 'Règles du Jeu') |
| reference | http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf |
| definition | G(y, p) / G(y, y), G = (sum of the cumulative share of the losses sorted by descending p - (n + 1) / 2) / n (tied p averaged over their orderings, so a constant p scores 0; the Kaggle code takes row order) |
| reason | The market needs the other players' premiums and the claims of 2014, neither published. The uniform scaling ('un facteur d'inflation appliqué uniformément') took away each player's price level, so the market rewarded the ranking of the risks; the normalized Gini scores that ranking of the claim cost, the metric of the insurers' Kaggle competitions (Allstate 2011, Liberty Mutual 2014); pricing_game_2017_french_mtpl, whose game kept the price level and ruined a player at 170% losses, scores a Tweedie deviance instead. The game's page (actinfo.hypotheses.org/69) and CASdatasets' pricingame.Rd name no other metric. The period's length carries part of the score: the length to the year's end alone ranks the charges at 0.101, 0.150 and 0.066 on the three windows, a regularised Tweedie LightGBM on all features at 0.155, 0.245 and 0.276. Tweedie deviance does not separate the models on these windows. |

<details>
<summary>Feature types: 13 categorical, 0 string, 1 datetime</summary>

- categorical (13): `contract_age_class`, `distribution_channel`, `new_company`, `fleet_management`, `client_activity`, `zone`, `fleet_size_class`, `payment_frequency`, `vehicle_age_class`, `power_value_class`, `deductible_class`, `insured_value_class`, `formula`
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

The first 5 of 87,228 rows of the final frame (the oldest rows: the frame is sorted by `period_start`); 12 of 17 columns, the target first. Cells are cut at 40 characters.

| claim_charge | period_start | contract_age_class | new_company | fleet_management | zone | fleet_size_class | payment_frequency | exposure | vehicle_age_class | deductible_class | n_vehicles |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2011-01-01 00:00:00 | 3 - 4 ans | No | P | 5 | 2 | semi-annual | 1 | &lt;= 5 ans | 2. 1 - 200 | 1 |
| 0 | 2011-01-01 00:00:00 | 3 - 4 ans | No | P | 5 | 2 | semi-annual | 1 | &lt;= 5 ans | 2. 1 - 200 | 1 |
| 0 | 2011-01-01 00:00:00 | 3 - 4 ans | No | P | 5 | 2 | semi-annual | 1 | &lt;= 5 ans | 2. 1 - 200 | 1 |
| 0 | 2011-01-01 00:00:00 | 4 - 5 ans | No | N | 3 | 2 | annual | 1 | &lt;= 5 ans | 4. 301 - 400 | 1 |
| 0 | 2011-01-01 00:00:00 | 4 - 5 ans | No | N | 3 | 2 | annual | 1 | &lt;= 5 ans | 4. 301 - 400 | 1 |

## Curation notes

We start with train_contrats.csv and train_sinistres.csv, the files the organisers of the second actuarial pricing game (2016) gave its players.

- Prediction point: the start of a vehicle's period of cover, when the insurer prices it with the year's tariff, fit on the closed years. The game asked for "une prime pure" (a pure premium) for each of the 32,772 periods of 2014 in test_contrats.csv (rules, Sec. 2, which write 37,772), with the periods of 2011 to 2013 to learn from; the period's claim charge is what a pure premium predicts. Known then: the contract's and the vehicle's rating classes, the period's start and its length of cover to the year's end. Not known: the period's claims, and when a period cut short will end.
- Source and year: the game's page (actinfo.hypotheses.org/69, 17 July 2016) dates the first stage "entre le 15 juillet et le 15 septembre", and the files carry a Last-Modified date of 13 July 2016. The rules (pricing-game-2016-FR.pdf, Sec. 1) describe every column; CASdatasets' copy holds the same values, its levels renamed one to one, except its DirectComp, which is 0 for 1,064 of the 1,190 claims the organisers flag IDA (a problem of that copy, not used here).
- The portfolio is commercial fleets with a material-damage cover, not the "private motor insurance" of CASdatasets' documentation: the rules describe "Mode de gestion de la flotte", "Taille de la flotte" and "Classe de franchise de la garantie DTA" (DTA is the usual French abbreviation of an all-accident damage cover), and 1,190 of the 4,568 claims fall under the IDA convention between insurers. The row names of the training file and the 2014 file together run exactly from 1 to 120,000, so the files are likely a sample of the portfolio: counts per contract (at most 12 vehicles of a contract at once) and a vehicle's last period describe the file, not the fleets.
- Target `claim_charge`: the charges (CHARGE_SINISTRE) of the period's claims summed, 0 without a claim. Each of the 4,568 claims joins one period on the contract, the registration, the year and the period's dates, and the claim count equals the joined claims on every period (checked in `_load_raw`). 4,250 periods have a claim (286 two or more, at most 7); 3,711 have a positive total (median 1,339, at most 13,992), so 95.7% of the targets are 0. The curator first chose the claim indicator (2026-10-30, record) and switched to the charge on 2026-11-02, after a measurement: the charge is what the insurer prices and what the game asked for, and the family's amount targets (fremtpl2, frempl, pricing_game_2017_french_mtpl) keep it.
- 537 periods net below 0 set to 0 (down to -1,863), as pricing_game_2017_french_mtpl and frempl_french_motor_personal_line do (the family call of 2026-10-30: "a net recovery is no claim cost of the year"). They are claims under the IDA convention ("1 si sinistre Indemnisation Direct de l'Assuré", rules Sec. 1), where the insurer pays its client and recovers a flat amount, not the cost, from the other insurer; every claim with a charge of 0 or less is IDA, and 126 of the 1,190 IDA claims are at 50% responsibility. Tweedie and Poisson losses need a non-negative target. The total is clipped, not each claim (65 periods mix signs, 16 of them net below 0); the clip raises the total claim cost by 4.3%.
- Only the frequency carries signal. Among the periods with a positive charge, the log charge is not predictable from the classes (R^2 -0.06 for LightGBM, -0.02 for ridge, measured on 2011-2012 to 2013), and a Poisson model of the claim count ranks the charges as well as models of the charge do (normalized Gini 0.202, 0.271, 0.279 on the windows, against 0.155, 0.245, 0.276 for a Tweedie LightGBM). The task is the frequency task with severity noise on top. Raw charge, not log1p: the normalized Gini ranks by the expected cost, which a log1p fit transformed back orders by its geometric mean instead.
- `exposure` is the length of cover known at the period's start, in vehicle-years ("Véhicules année (exposition au risque)"): (31 December - start + 1) / 365, / 366 in the leap year 2012, times the period's vehicles (2 on two periods), rounded to 0.01 (LEAK-10, LEAK-7). The source's value is the realised length, the same formula to the period's end (it matches on every period). 57.4% of the periods (57.9% in 2013) end before 31 December at a cut nobody scheduled, 0.8% at a contract anniversary, so their length is known only at their end, and with `period_start` a feature it gave back the dropped end. On the three windows the realised length added ROC AUC on the claim indicator +0.040, +0.055 and +0.052 over the length known at the start (regularised LightGBM on the rating classes and the start's day of the year, 3 seeds), and the early ends go with claims: a rate ratio of 1.22 [1.12, 1.33] given the rating classes (Poisson GLM with the length as offset, 2011-2012). The new length follows from the start date and stays as the time at risk a frequency model takes as given. Confirmed by the curator (Andrej, 2026-11-02) and recorded as the LEAK-10 case for time on risk cut short by the outcome: the cut is fixed where the data locates it.
- The covariates add to the length: on the three windows (newest first) the length alone ranks the charges at normalized Gini 0.101, 0.150 and 0.066, a Tweedie GLM on all features at 0.167, 0.270 and 0.268, a regularised Tweedie LightGBM (3 seeds) at 0.155, 0.245 and 0.276 (bootstrap standard errors 0.071, 0.043 and 0.023). The models beat the time at risk on every window, so the task is not trivial (TP-4), though on the newest window (103 positive charges) only by about one standard error. An untuned squared-error LightGBM scores 0.006, 0.226 and 0.253: on the newest window it does not beat the length. On the claim indicator the same split gives ROC AUC 0.550, 0.568 and 0.529 for the length against 0.597, 0.622 and 0.652. The task probes flag `no_signal` and `drift_baseline` (TP-1, TP-2): they score R^2, which follows a few large charges (best family linear, R^2 0.001); under the declared Gini the models beat the length on every window, as for pricing_game_2017_french_mtpl. The leak probes find nothing (every feature alone at R^2 -0.001 or below, 2.9% of the test rows with a feature copy in training).
- Not added, measured on all of 2013 on the claim indicator (the same LightGBM, trained on 2011-2012): the contract's and the vehicle's claims and exposure of the previous year (ROC AUC 0.667 with them, 0.668 without; a known entity's history is legitimate, USE-10, but it carries nothing here), and the contract's vehicles in force at the period's start (0.667).
- Dropped: `contract_id` (apparently numbered in the order of subscription: median 14,885 for contracts of at most a year, 2,027 for those over 5 years, which the contract's age class carries) and `vehicle_id` (the anonymised registration), `year` (the year of the period's start on every row), `period_end` (unknown at the start for the periods that end early; it only sets each window's training side), `vehicle_category` (one value) and the files' unnamed row index.
- `insured_value_class` "ND" (not available) made missing: 87,093 periods (99.8%); the 135 others hold five value classes.
- Labels restored: `payment_frequency` A, S, T as annual, semi-annual, quarterly (the French "annuel", "semestriel", "trimestriel"); `new_company` 2 as Yes and 1 as No ("à 2 si création", rules Sec. 1). The other classes keep the organisers' codes: French labels for the ages and the deductible, anonymised numbers for the zone, activity, channel, formula, fleet size and power-value class.
- Dtypes: every class column categorical; the power-value class (11 levels, a combined power and value grid) has no documented order. `exposure` and `n_vehicles` numeric (`n_vehicles` is 1 on every period but 2, which hold 2; kept as the source ships it); `period_start` a date.
- 11,807 periods (13.5%) repeat the features of another, 10,828 of them with the same target and 979 with another: vehicles of one fleet in the same period share every contract class and the start, so the length, and differ only by their own two classes. Natural, kept (LEAK-18).
- Anomaly: no period is shorter than 30 days, in the training file and the 2014 pricing file alike, and no period of a year starts after 2 December: the organisers seem to have left the shortest periods out, so the task covers periods of a month or more.
- Anomaly: the categorical levels are anonymised and the charges scaled by one constant (the record's generated-data tests of 2026-11-01: disclosure control, not generation); the charges are kept as published (the constant, 1.077841, changes no ranking).
- The newest periods lose no claims: claims per vehicle-year are 0.117, 0.119 and 0.119 in 2011 to 2013, and 0.115, 0.114 and 0.117 for the periods ending in the fourth quarter (LEAK-24 not triggered).
- Note: claims of the periods that close just before a window starts may have been reported only after the refit. The files hold the counts as of their extract (claims closed up to 2014, 41 still open) and no report date, so the delay can only be simulated: hiding the training charges whose claim falls in the last 30 or 90 days before each window's start (each claim placed uniformly in its period; 100 and 318 positive periods for the January window, at most 70 for the others) leaves the mean normalized Gini over the windows at 0.225 and 0.226 against 0.225 (regularised Tweedie LightGBM, 3 seeds). 41 claims were still open at the extract, so their charges may still move. A simulation, not a measurement. No gap separates the sides: an exception to SPLIT-10 that serves SPLIT-14 (Andrej, 2026-11-02), since rows are cut at 31 December and even a 1-day gap before the January window leaves 50.2% of the rows in training, a month 48.7%.

## Splits

Three test windows, the periods starting in 2013 by thirds of the year (September to December, May to August,
January to April, newest first). Each window trains on every period closed before it starts: 67,886, 61,797
and 56,178 periods (78%, 71% and 64% of the rows), so the January window trains on 2011-2012 and the later ones
add the 2013 periods already closed. A period still open at a window's start is in neither side (SPLIT-9). The
use case is a tariff: the game priced every period of 2014 from 2011-2013, and the claims of 2014 were never
published, so 2013 is the test year (suggested on 2026-10-30 and accepted with the curator's Yes). The game's
tariff was fit once for the year; three windows that share that one training side would be one evaluation, so
each window is a refit four months apart, which keeps three windows on distinct training sides (SPLIT-14 as
amended and SPLIT-11, Andrej, 2026-11-02). The 2013 periods closed before a window are the ones cut short (3.2%
and 2.4% with a claim, against 4.9% overall), as a refit on that day would see them; against the training side
held at 2011-2012 the regularised LightGBM's ROC AUC on the claim indicator moves by at most 0.002, the untuned one loses 0.014 on the newest
window (0.580 to 0.566, within its standard error). Three windows, not the nine of the convention (SPLIT-15):
finer windows only cut the same test rows into noisier pieces. Rows are cut at 31 December, so a period's start
caps its length and each window holds one cohort of lengths: most periods start on 1 January (12,028), and the
claims per vehicle-year are flat across the windows (0.117, 0.122, 0.129), but the share of periods with a
claim falls with the length (6.0%, 3.9%, 2.3%). A window's score ranks the periods within its cohort, and the
mean over the windows runs below a score pooled over 2013 (ROC AUC on the claim indicator 0.626 against 0.669, an untuned LightGBM on the
training side held at 2011-2012). The newest window is the smallest and the noisiest (5,312 periods, 123 with a
claim, 103 with a positive charge). No gap separates the sides (SPLIT-10; the notes give the reason and the simulated bound). Fleets and
vehicles recur across the cutoff, as a tariff prices the insurer's known fleets (SPLIT-13): 81-84% of the test
periods belong to a contract in training, 26-30% to a vehicle in training.

3 repeat(s) x 1 fold(s) with seed 4267; train 56,178 to 67,886 rows, test 5,312 to 19,229 rows. Prediction horizon: 4 months.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 67886 | 5312 | 2011-01-01 00:00:00 | 2013-08-02 00:00:00 | 2013-09-01 00:00:00 | 2013-12-02 00:00:00 |
| 1 | 0 | 61797 | 6509 | 2011-01-01 00:00:00 | 2013-04-01 00:00:00 | 2013-05-01 00:00:00 | 2013-08-31 00:00:00 |
| 2 | 0 | 56178 | 19229 | 2011-01-01 00:00:00 | 2012-12-02 00:00:00 | 2013-01-01 00:00:00 | 2013-04-30 00:00:00 |

## Decisions

### 1. The period's length is the one known at its start

The source's length is realised: a period that ends before 31 December is known only at its end, and 57.4% of the periods end at a cut nobody scheduled. Those ends go with claims: in 2011-2012 a vehicle's last period in the file that ends early has more claims per vehicle-year than a period that runs to the year's end (a rate ratio of 1.22 given the rating classes). `exposure` is therefore the length to 31 December for every period (curation_comments).

| the period ends | periods | vehicle-years (realised) | claims | claims per vehicle-year |
|---|---|---|---|---|
| 31 December | 23611 | 14646 | 1627 | 0.111 |
| earlier, the vehicle goes on | 10845 | 3024 | 334 | 0.11 |
| earlier, the vehicle's last period in the file | 21722 | 7005 | 959 | 0.137 |

### 2. A net recovery counts as no cost

The target is the period's claim charges summed. Claims under the IDA convention, where the insurer pays its client and recovers a flat amount from the other insurer, can net below 0; such a total is set to 0, as in pricing_game_2017_french_mtpl and frempl_french_motor_personal_line.

| index | periods |
|---|---|
| periods with a claim | 4250 |
| with two or more claims | 286 |
| with an IDA claim | 1156 |
| with no claim of positive charge | 523 |
| with a net total below 0 (set to 0) | 537 |

## Bundle checks

0 error(s), 0 warning(s), 0 info (26 checks run, plus the dataset's own checks).


Accepted on purpose:

- `dataset_duplicate_rows`: Vehicles of one fleet in the same period share every contract class and the start, so the length, and differ only by their own two classes: natural repeats (LEAK-18). With `period_start` a feature no copy crosses the split.
- `dataset_conflicting_duplicate_rows`: The same repeats as dataset_duplicate_rows: vehicles of one fleet with the same classes in the same period, with different claim charges. Natural (LEAK-18); the outcome of one vehicle is not the other's.
- `task_target_value_dominant`: Zero-inflated by nature: the claim charge is 0 for 95.7% of the periods, those with no claim (95.1%) or whose claims net to 0 or less after IDA recoveries (0.6%, negative totals set to 0); not a cap or a placeholder.
- `meta_license_unknown`: The organisers state no licence for the game's files; CASdatasets, which redistributes the same tables, is GPL (>= 2).

## Data checks

### Feature summary

<details>
<summary>Show the table (17 rows)</summary>

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
| exposure | float64 | 0 | 0 | 95 | 1.0, 0.75, 0.5, 0.25, 0.84, 0.92, 0.67, 0.33, 0.42, 0.17 |
| claim_charge | float64 | 0 | 0 | 3581 | 0.0, 140.1193, 161.6761, 128.5433, 2371.2501, 108.5386, 1077.841, 100.5518, 112… |
| n_vehicles | int64 | 0 | 0 | 2 | 1, 2 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 95.75 | 9.082 | 4.694 | 241319 | 2.071 | log1p | 63051.6 | 64823 | exponential |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| exposure | 87228 | 0.717125 | 0.303319 | 0.08 | 1.82 |
| n_vehicles | 87228 | 1.00002 | 0.00478834 | 1 | 2 |
| claim_charge | 87228 | 76.5342 | 491.242 | 0 | 13992.4 |

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
