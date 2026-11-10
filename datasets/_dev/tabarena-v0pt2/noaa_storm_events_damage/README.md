---
report_format: data-foundry-report-v2
unique_name: noaa_storm_events_damage
container_format: 2
checksum: v2:e51184b0799a7d88bdaba23f8a389da212c7acdb8483e1266df56cf760c3d618
build: null
build_stale: false
data:
  n_rows: 843144
  n_features: 13
  dtypes:
    category: 8
    datetime64[ns]: 1
    float64: 7
  n_test_dataset_rows: null
task:
  target: property_damage_usd
  problem_type: regression
  metric: mean_tweedie_deviance
  metric_origin: context
  scoring_columns:
  - cell_weight
  unit_weight:
    column: cell_weight
    unit: cell
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: begin_time
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
  time_gap: 3
  time_gap_unit: months
  n_train:
    min: 702587
    max: 793017
  n_test:
    min: 44056
    max: 45870
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  - dataset_conflicting_duplicate_rows
  accepted:
    task_target_value_dominant: 'Zero-inflated: 68% of the entries are $0, kept as
      entered; part of the zeros are unestimated damage (13 of 121 EF4 and EF5 tornado
      segments at $0; kept under LEAK-25 as amended, Andrej, 2026-11-02).'
decisions:
- Entries without a damage figure are dropped; $0 stays
- A $0 depends on the office
---

# noaa_storm_events_damage

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `property_damage_usd`, scored with `mean_tweedie_deviance` on temporal splits by `begin_time`. 843,144 rows and 13 features. Source: GOV Website (2026).

Not built yet. The current definition gives checksum `v2:e51184b0799a7d88bdaba23f8a389da212c7acdb8483e1266df56cf760c3d618`.

## In brief

**Question.** How much property damage, in dollars, did a storm event reported by the US National Weather Service cause in one county or forecast zone?

**Use case.** For example, a state hazard-mitigation planner totals the property damage of the storm events already reported, per county or zone and hazard, from what the first reports say about each event before its damage is assessed (its type, place, season, size and cause), to see where disaster resources and mitigation go, as Diaz and Joseph (2019) do for tornadoes "for science-informed tornado disaster planning".

**One row.** One event of the NWS Storm Data archive in one US county or forecast zone, 2007-2025 (thunderstorm wind, hail, flood, tornado, winter storm and 29 other types), among the events with a damage entry (an office leaves 0% to 98% of its events blank); the hazards whose entries almost never carry property damage (marine zones, drought, heat, cold, fog and a few more) are left out.

**Predicted.** The property damage the NWS office entered for the event, in nominal dollars; 68% of the entries are $0 and the smallest damage entered is $10.

**Known at prediction time.** The event type, the place (state, county or zone, forecast office, where county events began), when it began and, unless damage alone timed it, how long it lasted, a measured wind speed or the hail size, whether a wind report was measured or a damage report, and a flood's cause. The first report says whether damage was seen; some types are entered only with damage (4.5-5.0% of test rows).

**Known only when scoring.** How many entries the test year holds for the entry's county or zone and event type: each entry weighs 1 over that number, so each county or zone, event type and year counts once. The count is known only once the year is over, so it is read with the test labels and never when predicting.

**What the test data stands for.** The test data is a later calendar year (2023, 2024 or 2025), with every event published by the refit at the start of that year (all but the last three months) for training.

**Our changes to the source.** We drop entries without a damage figure, 918 double entries, narratives, tornado rating and path, end point, casualties, crop damage, reporter and hurricane category, and blank the wind speeds estimated from the damage and the durations it sets (tornado, strong wind, heavy rain, seiche, wind reported as damage or thunderstorm wind under 50 kt): all written from, with or after the damage. Wind speed and hail size become two columns.

> **Use case fit: approximate (a stand-in with a known gap).** The planner acts on a county's or zone's total per hazard: the score counts each county or zone, hazard and year once but averages its entries' errors, not their sum. The inputs are Storm Data entries made weeks later. The label is a rough estimate, and a $0 means no damage or no estimate made, by a convention that differs by office and drifts. No exposure is given.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`REVIEW.md`](REVIEW.md) | The open questions for the curator, removed once they are settled. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/noaa_storm_events_damage.md`](../../../../curation/records/noaa_storm_events_damage.md)
- The original source: <https://www.ncei.noaa.gov/access/storm-events-database/>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/noaa_storm_events_damage/`. To get them:

```text
# The yearly details files of the Storm Events Database (NOAA NCEI bulk CSV), as downloaded on 2026-10-30.
# NCEI rewrites a year's file when it changes (the c-date in the name); _load_raw takes the one file per year.
mkdir -p local-data-warehouse/noaa_storm_events_damage && cd local-data-warehouse/noaa_storm_events_damage
for f in d2007_c20260323 d2008_c20260323 d2009_c20260323 d2010_c20260323 d2011_c20260323 \
         d2012_c20261026 d2013_c20260323 d2014_c20260323 d2015_c20260323 d2016_c20260323 \
         d2017_c20260519 d2018_c20260323 d2019_c20260323 d2020_c20260323 d2021_c20260323 \
         d2022_c20260625 d2023_c20260323 d2024_c20260728 d2025_c20260819; do
    wget https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_${f}.csv.gz
done
# Column documentation: Storm-Data-Bulk-csv-Format.pdf in the same directory; the preparation rules:
# NWS Instruction 10-1605 (https://www.weather.gov/media/directives/010_pdfs/pd01016005curr.pdf).
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/noaa_storm_events_damage   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/noaa_storm_events_damage   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | GOV Website: https://www.ncei.noaa.gov/access/storm-events-database/ |
| year | 2026 |
| domain | environmental science & climate |
| license | Public Domain |
| data_tags | Non-IID, Temporal, Spatial |
| reference | ncei_storm_events_database |
| rows x columns | 843,144 x 16 |
| task.target | property_damage_usd |
| task.problem_type | regression |
| task.metric | mean_tweedie_deviance |
| task.unit_weight | {'column': 'cell_weight', 'unit': 'cell'} |
| task.split_regime | temporal_non_iid |
| task.time_on | begin_time |

**Metric**

| field | value |
|---|---|
| name | `mean_tweedie_deviance` (standard; takes value; lower is better) |
| origin | context: obvious from the task: the source defines no metric |
| definition | sum(w * 2 * (y^(2-q) / ((1-q)(2-q)) - y p^(1-q) / (1-q) + p^(2-q) / (2-q))) / sum(w) at power q (1 Poisson; 1 < q < 2 a compound Poisson-gamma cost, y >= 0; q >= 2 needs y > 0), w the optional weight input (1 without it); p below min_prediction counts as it |
| reason | NCEI and NWSI 10-1605 define no task or metric, and no competition was found. Diaz and Joseph (2019, Weather and Climate Extremes 25:100216, https://doi.org/10.1016/j.wace.2019.100216) model tornado damage from this database with several metrics (accuracy and AUROC for any damage, MSE on the log of the positive amounts), on tornadoes only and a random split: no source metric for this task (MET-5). The planner sums the expected damage of events per county or zone and hazard, so the metric scores each event's expected dollars: the mean Tweedie deviance at power 1.5, a compound Poisson-gamma loss minimised by the mean, for an amount that is $0 for 68% of the entries and heavy-tailed above it. Each county or zone, event type and year counts once, the unit the planner decides on (Andrej, 2026-11-09, review issue 12): an entry weighs 1 over its cell's entries (`cell_weight`), where unweighted a cell counted once per entry (11,765 to 12,676 cells per test year, 3.5 to 3.7 entries each, 88% of the test entries sharing a cell). The entries' errors are averaged within a cell, not summed, so they do not offset as in the planner's total, and the score's best prediction is the cell-weighted mean (training mean $863,406 weighted against $453,533 for the 2025 window). RMSLE, declared until 2026-11-08 (Andrej, 2026-11-03, for the earlier triage actor), scores the order of magnitude and is minimised by a geometric mean (the RMSLE-optimal constant for 2024 is $16 against a mean of $355,555), so its predictions summed over events understate the loss the planner plans for; trained each for its own metric, the two pick different models in 3 of 3 windows (2026-11-06). The deviance damps the tail far more than a squared error (on the dollars the largest 0.1% of the entries hold 99.94% of the squared deviation) and less than a log, so large events weigh more than under RMSLE, while the label is coarse (44% of the positive figures have one significant digit). A prediction below $10 counts as $10, the smallest damage the source records (Andrej, 2026-11-09, review issue 14; none of the 268,670 entries with damage lies between $0 and $10), so a finer prediction is no planning difference; it replaces the $1 of the collection's rule for a deviance floor (MET-13), two orders below the $909 training mean of Dense Smoke, the cheapest event type. At the floor (2026-11-09): no prediction of LightGBM or CatBoost fitted with the Tweedie loss, of a Tweedie GLM or of the means, 2% of a LightGBM fitted by squared error, and in the task probe 0% of the random forest's and 44% of the linear model's and LightGBM's, fitted by squared error. Chosen over RMSLE by the curator (Lennart, 2026-11-08, review issue 8). |
| params | {'power': 1.5, 'min_prediction': 10.0} |
| inputs | weight: `cell_weight` |

**Scoring columns**

Kept in the frame for the metric; do not use them as features. Drop them from the inputs (`feature_columns(container)`), then pass the test rows' values to the scorer (`data_foundry.v2.metrics.scorer(container)(y_test, y_pred, test_idx)`).

| column | role | how the metric uses it | model input |
|---|---|---|---|
| `cell_weight` | weight | mean_tweedie_deviance: 1 over the number of entries of the row's county or zone, event type and year (`cell`), so that each cell counts once in the deviance; known only once the year is over, for scoring only, never a feature or a training weight | unit weight: weight a validation loss by it; never a feature |

The test-row values of `cell_weight` are for the scorer only: never read them when predicting a test row.

**Unit weight**

The score counts each `cell` once: `cell_weight` is 1 over the unit's number of rows, so the weights of a unit sum to 1. It is for scoring only, never a training weight or a feature. A model that picks its settings on a validation split weights the validation loss by `cell_weight` too (`validation_weight(container)` from `data_foundry.curation_container`) and keeps a unit's rows on one side of that split; `cell` is metadata, never a feature.

<details>
<summary>Feature types: 8 categorical, 0 string, 1 datetime</summary>

- categorical (8): `event_type`, `state`, `cz_type`, `county_zone`, `wfo`, `magnitude_type`, `flood_cause`, `cell`
- string (0): none
- datetime (1): `begin_time`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{ncei_storm_events_database,
  author = {{NOAA National Centers for Environmental Information}},
  title = {Storm Events Database},
  year = {2026},
  howpublished = {\url{https://www.ncei.noaa.gov/access/storm-events-database/}},
  note = {Bulk CSV files (details), 2007-2025, downloaded 2026-10-30 from https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/}
}
```

</details>

## Sample rows

The first 5 of 843,144 rows of the final frame (the oldest rows: the frame is sorted by `begin_time`); 12 of 16 columns, the target first. Cells are cut at 40 characters.

| property_damage_usd | state | event_type | cz_type | wfo | magnitude_type | flood_cause | begin_lat | begin_lon | begin_time | duration_hours | county_zone |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3000 | NEW YORK | Winter Weather | Z | BTV | nan | nan | nan | nan | 2007-01-01 00:00:00 | 6 | 36Z035 |
| 0 | WISCONSIN | Winter Storm | Z | DLH | nan | nan | nan | nan | 2007-01-01 00:00:00 | 5 | 55Z003 |
| 0 | INDIANA | Flood | C | PAH | nan | Heavy Rain | 38.48 | -87.53 | 2007-01-01 00:00:00 | 662 | 18C051 |
| 10000 | INDIANA | Flood | C | IND | nan | Heavy Rain | 39.47 | -87.4 | 2007-01-01 00:00:00 | 659.667 | 18C167 |
| 2000 | NEW YORK | Winter Weather | Z | BTV | nan | nan | nan | nan | 2007-01-01 00:00:00 | 6 | 36Z030 |

## Curation notes

We start with the yearly details files 2007-2025 of NOAA NCEI's Storm Events Database (bulk CSV, one row per Storm Data event in one county, forecast zone or marine zone), the archive of the National Weather Service's Storm Data publication. The source defines no prediction task.

- Prediction point: a storm has passed, the event has ended and is logged from the first reports (type, place, begin and end time, a measured wind speed or the hail size, whether damage was seen), before any damage survey, claim or damage estimate. Every column is checked against it. Strong Wind, Lightning and Thunderstorm Wind below 50 kt enter Storm Data only when they result in "a fatality, injury, or damage" (NWSI 10-1605, Sec. 29, 45 and 46), and so, mostly, do hail under 3/4 inch (Sec. 19: entered when its accumulations "cause property and/or crop damage") and dust devils (Sec. 10): 4.5-5.0% of the test rows, 95-96% of them with damage. They stay, since the first report says whether damage was seen (LEAK-37). The numbers below are untuned LightGBM (400 trees) on the shipped features, trained on 2007 to September 2023 and tested on 2024, RMSE on log1p of the dollars (RMSLE, the metric until 2026-11-08): 2.626 as shipped (scratch, 2026-11-01).
- Target: `DAMAGE_PROPERTY`, coded as a number and a magnitude letter ("10.00K" = $10,000), parsed to dollars and shipped in dollars (`property_damage_usd`): a target scored by a deviance ships untransformed, since the deviance scores the mean on the dollars, which a fit on the log scale misses (CLEAN-16). Until 2026-11-08 it shipped as log1p (`log1p_property_damage_usd`) for RMSLE (review issue 8). Nominal dollars as entered, not adjusted for inflation.
- Metric floor: a prediction below $10 counts as $10 (`min_prediction`; Andrej, 2026-11-09, review issue 14), the smallest damage the source records: of the 843,144 entries 268,670 carry damage, none between $0 and $10, 423 at exactly $10, 457 (0.17%) below $100 and 6.1% below $1,000, and offices enter round values (44% of the positive figures have one significant digit). A planner reads an expected $1 and an expected $10 as the same nothing, so a prediction finer than any entry makes no planning difference. It replaces the $1 of 2026-11-08 (Lennart, review issue 8), set by the collection's rule for a deviance floor (MET-13 as amended on 2026-11-06): two orders below the smallest plausible mean, the $909 training mean of Dense Smoke, the cheapest of the 33 event types with a positive training mean, rounded down to a power of ten; $10 is the source's own resolution, about two orders below that mean too. Volcanic Ashfall, $0 in all its training entries, has no positive mean: a model should predict near $0 there, and the floor binds by design. At the floor (2026-11-09, on the cell-vote score): no prediction of LightGBM or CatBoost fitted with the Tweedie loss, of a Tweedie GLM on event type and month or of the training means, and 1.7% to 2.3% of a LightGBM fitted by squared error, whose score the floor moves (12,103 at $10 against 22,656 at $1 in 2023); the Tweedie-fitted models score the same at $1 and $10. In the task probe 0% of the random forest's predictions and 43.8% of the linear model's and LightGBM's, fitted by squared error, which predict below $10 there.
- Score unit (Andrej, 2026-11-09, review issue 12): each county or zone, event type and calendar year (`cell`) counts once. A mitigation planner decides per jurisdiction and hazard on the loss expected in a year (44 CFR 201.6(c)(2); FEMA's Local Mitigation Planning Policy Guide, B1-d and B2-b; the National Risk Index's expected annual loss per county or tract and hazard). An entry weighs 1 over its cell's entries (`cell_weight`), a scoring column the metric reads, never a feature or a training weight, and the task declares it as its `unit_weight` (MET-17, extended from repeats of one decision to entries whose dollars add). The cells: 258,067 over 2007-2025, 3.3 entries each; in the test years 11,765, 12,676 and 12,636 cells of 3.5 to 3.7 entries, 88% of the test entries sharing a cell, 40% to 44% of the cells forecast zones. Unweighted, a cell counted once per entry, so a county with many hail or wind reports of one hazard weighed more than one with a single large event. The errors of a cell's entries are averaged, not summed, so they do not offset as in the planner's total; scoring the cell sums would need a `sum` aggregation the scorer does not have. On 8 models of issues 8 and 10 (2026-11-09, floor $1) one vote per cell ordered them as the cell sums did (Kendall tau 1.00, 0.86 and 1.00 in 2023, 2024 and 2025) and against the per-entry score at tau 0.86, 0.79 and 1.00, with another top model in 2024 (the GLM on event type and month in place of tuned LightGBM). The weight moves the best prediction from the mean to the cell-weighted mean, as cells of one entry hold larger damage (training mean of the 2025 window $863,406 weighted against $453,533; the ratio by event type 0.67 to 2.06), yet tuned LightGBM trained with the weight scored worse than without it in every window (13,201 against 10,148, 3,125 against 2,999, 1,287 against 1,160). A cell's count is known only once its year is over (`known_at_scoring`); every test window is a calendar year, so every test cell is whole.
- Signal under the declared metric (2026-11-08; untuned LightGBM fitted with the Tweedie loss on the shipped splits, and the task probe): fitted with the Tweedie loss, LightGBM of 100 trees scores 4,108 to 5,327, 2,048 to 2,453 and 788 to 838 in 2023, 2024 and 2025 (5 fits each), against 4,453, 4,216 and 2,929 for the training mean and 2,660, 2,301 and 1,740 for the training mean per event type; at 400 trees 6,153 to 24,115, 3,400 to 6,442 and 994 to 1,447, and at 1,500 trees 12,344 to 51,125, 7,694 to 22,318 and 2,003 to 2,972. So a model fitted for the metric beats a constant in 2024 and 2025 (in 2 of 5 fits in 2023) and the mean per event type clearly only in 2025, and more capacity scores worse: the deviance is decided by the few largest events, as the panel read its picks (review issue 8). The task probe's families, fitted by squared error on the dollars, all lose to the training mean (mean deviance 3,866 over the 3 windows; random forest 5,796, linear 115,411, LightGBM 190,920; on the cell-vote score with the $10 floor of 2026-11-09 5,615 against 7,555, 48,331 and 95,058), so it flags `no_signal`, `drift_baseline` and `unstable` (TP-1, TP-2, TP-5). Read against tuned models (review issue 10; Lennart, 2026-11-08: the deviance stays as shipped): LightGBM with the Tweedie loss, tuned per window over 24 configurations (learning rate, leaves, rows per leaf, feature fraction) with early stopping on the last 12 months of the training side, refit on the whole side, 3 seeds, scores 3,463, 2,044 and 962 in 2023, 2024 and 2025 (seeds 2,997 to 4,270, 1,968 to 2,101 and 926 to 1,005). Against the mean per event type that is +802 in 2023, within noise (bootstrap SE 1,580 over test rows, 1,617 over test days), -257 in 2024 (SE 129 and 314) and -777 in 2025 (SE 30 and 44); against the training mean -990, -2,172 and -1,966. A Tweedie GLM on event type and month scores 2,553, 2,130 and 1,598, below the per-type mean in every window. So the task keeps a real signal over the per-type mean in 2024 and 2025, and in 2023 a few large events leave the difference unreadable. Note: with each entry's damage capped at $10M (the cap binds on 1,761 entries and removes 87% of the dollars) the tuned model beats the per-type mean by 18% to 32% in every window and seed; the cap is not shipped, since the planner's sum includes the catastrophes and fremtpl2 and houses declined capped targets. Under RMSLE untuned LightGBM gained about 1.3 over a constant in every window. On the score of 2026-11-09 (each cell one vote, floor $10; review issues 12, 14 and 15; tuned models validated with the cell weight, 3 seeds): the GLM on event type and month scores 3,218, 2,778 and 2,024 (2023, 2024, 2025), the mean per event type 3,367, 2,986 and 2,200, CatBoost with the Tweedie loss 3,908, 2,535 and 2,047, tuned Tweedie LightGBM 10,148, 2,999 and 1,160 (seeds 9,300 to 11,090, 2,935 to 3,081, 1,128 to 1,194) and squared-error LightGBM 12,103, 54,579 and 7,977, against 7,816, 5,602 and 3,428 for the training mean. The top method differs in every window (GLM, CatBoost, tuned LightGBM) and stays on top in 57%, 59% and 78% of 2,000 bootstrap resamples of test days; Kendall's W of the five methods' ranks across the windows is 0.62; tuned LightGBM minus the per-type mean is +6,781 (SE 7,458), +13 (SE 753) and -1,040 (SE 120). With each entry capped at $10M (fitted and scored on the capped target, not shipped): W 0.91, the top kept in 81%, 92% and 95% of the resamples, tuned LightGBM below the per-type mean in every window (-247, SE 70; -137, SE 90; -255, SE 30). The damage stays uncapped (Andrej, 2026-11-10, review issue 15): on the shipped, uncapped score the methods are ordered at Kendall's W 0.62 across the windows and separate from a mean per event type only in 2025, the measured noise of a task decided by a few large events; the planner's expected annual loss includes them, and a $10M cap would score 13% of the dollars.
- Rows without a damage figure (blank `DAMAGE_PROPERTY`, 18% of the 1,225,290 events 2007-2025) have no target and are dropped. We read the blank as the "no information available" box ("either check the 'no information available' box, or make an estimate. The lone exception is for flood events", NWSI 10-1605, Sec. 2.7, p. 11): an inference, since the export of the box is not documented; Flood and Flash Flood have 26 blanks, all in 2007, and none from 2008 on. A $0 entry stays a 0. The curator's call (Andrej, 2026-10-30, zero-inflated review): "We don't care. We want to add any relevant predictive task, independent if it is zero inflated or not"; reading it as making $0 against blank a cleaning choice is the AI's.
- Dropped as hazards whose entries almost never carry property damage (USE-1; Andrej, 2026-11-03, review issue 2, the domain practitioner's list): every marine type and drought, heat, excessive heat, cold/wind chill, extreme cold/wind chill, dense fog, freezing fog, rip current, funnel cloud, waterspout and high surf: 156,767 entries with a damage figure (15.7%), 99.1% of them $0, with 0.5% of the dollars, so they hold almost none of the property damage the planner plans for. The event type alone predicts their zeros, so they made the task look easier. On the rows left untuned LightGBM scores RMSLE 2.67, 2.93 and 2.94 (2025, 2024, 2023) against 4.05, 4.28 and 4.20 for a constant.
- No storm-level input (review issue 4): the number of a storm's entries and counties (`EPISODE_ID`) changes untuned LightGBM's RMSLE by -0.010 to +0.001 counted over all its entries, and by -0.012 to +0.017 counted over the types entered whatever the damage (strong wind, lightning and thunderstorm wind under 50 kt enter Storm Data only with damage, 3.3% of the entries), so it adds no measurable signal and would carry part of the label.
- Exposure (MET-14, MET-15; 2026-11-06): none. The target is the damage of one event as entered, not a count or an amount accrued over an amount at risk, so it ships without a rate, a weight or an offset. The source gives no population, building or insured value, and the one proxy tested, the county's population (Census estimate for 2020, county rows of 2016-2025), does not scale with the damage (Spearman -0.14 to +0.05 with the log damage among the positive entries of five types; exposure study of 2026-11-05). `duration_hours` is a span the outcome partly sets, not an exposure (below). The storms whose positive entries all carry one figure (2,063 of the 16,080 with two or more, 2016-2025) hold round office values (one of eight round amounts from $1,000 to $100,000 in 73.5% of them; one or two significant digits in every one with three or more entries), not a storm total split over its zones.
- Anomaly: a $0 mixes "no damage" with "no estimate made" (13 of 121 EF4 and EF5 tornado segments, and 17.3% of EF2 and above, are at $0), and the mix is office practice: among Thunderstorm Wind entries the share at $0 runs from 7% to 91% between the 10th and 90th percentile of the 107 offices with 100 or more entries (decision table). It drifts: an office's 2024 share predicts its 2025 share at r 0.958 and its 2007-2016 share at r 0.575, and 30.5% of 82 offices moved by more than 0.2 from 2007-2021 to 2023-2025. The line between $0 and blank moves inside an office too: from 2007-2010 to 2022-2025, 70% of the rise in an office's Thunderstorm Wind blanks came out of its $0 entries (98 offices). The office (`wfo`) is a feature, so a model can learn the practice; it is not repaired. Kept under LEAK-25 as amended for this case (Andrej, 2026-11-02): a mix whose recording follows a reporting unit shipped as a feature stays, with the unit's spread and drift in the notes and fit approximate, as the task keeps a measured signal beyond the office, the period and the place; the blanks, the source's own 'not recorded' box, are dropped.
- History: from 2007 on. In the files of 2000-2005, 70% to 72% of the events have no damage figure, 61% in 2006 (the year the files move from the PDS to the CSV entry format; in 2006 the PDS rows are 71.3% blank, floods 63.3%, the CSV rows 0.1%), then 7.3% in 2007, rising to 22-24% in 2022-2025, so the kept rows change composition; the positive damage drifts down within the kept years too (median of Thunderstorm Wind $5,000 in 2007-2017, $2,000 in 2025).
- Dropped, written from the damage or recorded with it (LEAK-10): the narratives (the episode narrative is not read, the event narrative only finds double entries), `TOR_F_SCALE` (the Enhanced Fujita rating "describes the strength of the tornado based on the amount and type of damage", format document p. 4), `TOR_LENGTH`, `TOR_WIDTH` and the `TOR_OTHER_*` continuation fields (the path from the damage survey), the end point `END_LAT`, `END_LON`, `END_RANGE`, `END_AZIMUTH`, `END_LOCATION` (for a tornado the end of the surveyed path, for a wind swath "within the county where the wind damage swath exists", NWSI 10-1605, Sec. 46.1, p. A-68), the injuries and deaths, and the crop damage. Measured: with the rating, the path and the end point the RMSE falls from 2.626 to 2.596 (tornado rows 4.796 to 4.107); with the casualties and the crop damage to 2.561; two flags read off the event narrative (a dollar amount, a damage word such as "roof" or "downed") give 2.559.
- Dropped (LEAK-10): `CATEGORY`, which the format document calls unknown. It is filled for the Hurricane (Typhoon) events only, 1 to 5, and set per zone: 23 of the 95 episodes with a category carry more than one value, and Hurricane Michael's Category 5 zone (2018) is the reanalysis of April 2019, after the event; NWSI 10-1605 (Sec. 25.3) pairs each category with the types of damage. 482 rows, none in 2025.
- Dropped (LEAK-10): `SOURCE`, the reporter of the event. One of its values, "NWS Storm Survey" (about 23,700 entries, 72% with damage), is a damage survey the office makes after the event, and the column has no missing values, so blanking that value would leave the same marker; merged into "Unknown" (about 1,400 entries) it would hold it too (RMSE 2.559 merged and as published). The other reporters (a 911 call center, a utility, a trained spotter) are known at the first report, so the drop costs real signal: RMSE 2.626 without the column. The drop follows kick and expresso_churn_prediction.
- Blanked (LEAK-10): the wind speeds the office estimated from the damage, `magnitude_type` "EG" (252,451 entries) and "ES" (the same for sustained wind, 1,151); the type stays. NWSI 10-1605, Sec. 46.3, p. A-69: the preparer "exercises professional judgment to determine the estimated maximum wind value based on observed structural or tree damage". Matched to the real-time Local Storm Reports of 2024 (same office, within 15 minutes and 10 km), 94.4% of 12,498 EG Thunderstorm Wind events had a first report "TSTM WND DMG" without a speed, while measured gusts kept their speed in 92.7% of cases and hail sizes in 97.9%. Whether a wind report was a damage report or a measured gust is in the first report, so `magnitude_type` stays and the blank follows it (no marker). Among entries with damage the estimate tracks the dollars (Spearman 0.46); on the EG and ES test rows the RMSE is 2.760 with it and 2.860 blank. The 24 impossible speeds (22 Thunderstorm Wind entries of 1-10 kt, 2 Strong Wind entries of 0 kt) are all estimates and go with them.
- Blanked (LEAK-10): `duration_hours` where the outcome alone sets the span or its start, by event type, and on the wind entries whose span only the damage can have timed, by event type, speed type and measured speed; never by reporter, so a blank is no survey marker. Tornado: a tornado begins and ends with the vortex's ground contact, which the damage survey sets (NWSI 10-1605, Sec. 47; 68% of the tornado rows come from "NWS Storm Survey"), and the duration tracks the dropped path length (Spearman 0.83 with `TOR_LENGTH`); on the tornado test rows the RMSE is 4.537 with it and 4.796 blank. Strong Wind and Heavy Rain (CC 2026-11-06, Lennart; 18,243 and 20,836 rows, 4.6%): App. A times them by the damage, Strong Wind from "When the wind started to cause a fatality, injury, or significant damage" to "When the wind no longer caused a fatality, injury, or significant damage" (Sec. 45), Heavy Rain from "When the heavy rain that led to damage began" until it "no longer posed a threat to life or property" (Sec. 21). Their blank costs nothing measurable: on their test rows RMSLE changes by -0.009, -0.018 and -0.046 (2023, 2024, 2025; untuned LightGBM on the shipped splits, mean of 4 bagging seeds, SD 0.03 to 0.06). Seiche (51 rows; blanked after the re-review of 2026-11-06, which read App. A again for every type and found it missing from D13's reading): it begins "When water levels rose to initiate shoreline flooding, resulting in a fatality, injury or damage" (Sec. 41), so the damage draws its start; too few rows to measure. The Thunderstorm Wind and High Wind entries the first report gives as damage (CC 2026-11-08, Lennart; review issue 7): the entries whose speed the office estimated from the damage (`magnitude_type` EG or ES, 241,088 rows) and the Thunderstorm Wind entries measured under 50 kt (MG or MS, 435 rows), 241,523 rows, 75.8% of the 318,813 rows of the five types D13 kept with a note. App. A times Thunderstorm Wind from "When damage first occurred or winds 50 knots (58 mph) or greater were first reported" to "When damage ended or winds of 50 knots (58 mph) were last reported" (Sec. 46), and High Wind likewise with its wind criteria (Sec. 24); on these entries no wind of the criterion was reported, so only the damage can have timed the span, as for Strong Wind. An EG or ES speed is the preparer's estimate from the damage (Sec. 46.3, above), and 94.4% of the EG Thunderstorm Wind entries of 2024 had a first report of damage without a speed (the other 5.6% had a speed in the first report, so the blank locates these spans closely, not exactly); a Thunderstorm Wind entry measured under 50 kt met no wind criterion and enters Storm Data only with damage (92% of the 435 have property damage). The blank follows `event_type`, `magnitude_type` and `wind_speed_kt`, so a missing duration tells a model nothing those features do not (leak probe, 2026-11-08: the missing indicator alone scores R^2 0.192, `event_type` alone 0.185; all features 0.352, 0.348 without the column). Its cost on these rows' test rows under RMSLE, the metric before review issue 8 (2026-11-08, the shipped splits, mean of 4 bagging seeds per window): +0.023 to +0.036 RMSLE under a LightGBM of 1,500 trees and 127 leaves (12 of 12 seeds positive) and +0.008 to +0.032 under untuned LightGBM of 400 trees; on all rows +0.009 to +0.026 and -0.003 to +0.027.
- Potential leak, kept on purpose (CC 2026-11-06 and 2026-11-08, Lennart): `duration_hours` of the Thunderstorm Wind and High Wind entries with a measured speed (of 50 kt or more for Thunderstorm Wind; 31,985 and 41,432 rows), of Coastal Flood, Lakeshore Flood and Storm Surge/Tide (3,873 rows) and, by the same reading (re-review of 2026-11-06), of Dust Storm and Volcanic Ashfall (1,553 rows): 78,843 rows (9.4%), whose span App. A times by the damage or by a criterion without it. Thunderstorm Wind runs from "When damage first occurred or winds 50 knots (58 mph) or greater were first reported" to "When damage ended or winds of 50 knots (58 mph) were last reported" (Sec. 46), High Wind likewise with the high-wind criteria (Sec. 24), the three floods from "When the water level began to cause damage or flooding" to "When the water level dropped to a point where damage or flooding ended" (Sec. 4, 27, 44), Dust Storm from when blowing dust "first reduced visibility to locally/regionally established values or began to cause a major impact" (Sec. 11), and Volcanic Ashfall from "When volcanic ash began to cause disruption to transportation, commerce, fatality, injury, or damage" (Sec. 51). On these entries the first report holds a measured wind, a water level, blowing dust or ash, so the criterion can have set the span, and Storm Data does not record which of the two did; the wind entries on which only the damage can have timed it are blank (above). Measured on 2026-11-08 on the declared metric (the column blanked on these rows against the shipped definition; LightGBM fitted with the Tweedie loss, 15 set-ups of 100, 400 and 1,500 trees on the 3 shipped splits): no consistent sign, from -41% to +99% of the mean deviance on these rows' test rows over the re-review's 15 set-up and window pairs (6 positive, median -5%) and 24 positive of all 45 fits (median +2%); -27% to +67% on all rows. By type: the measured Thunderstorm Wind spans gain in 35 of 45 fits (median +11% of the deviance on their rows; +7%, +22% and +19% in 2023, 2024 and 2025 under the 100-tree model, the best fitted for this metric), while High Wind (23 of 45 positive), Coastal Flood (26 of 45) and Dust Storm (16 of 45) show no consistent sign; Lakeshore Flood, Storm Surge/Tide and Volcanic Ashfall have 0 to 60 test rows per window, too few to read. Under RMSLE, the metric before review issue 8, the same blank measured -0.02 to +0.12 RMSLE on these rows (15 fits, 11 positive, median about +0.04; -0.01 to +0.09 on all rows), the measured Thunderstorm Wind spans +0.03 to +0.18 in 30 of 30 fits, more than the blanked spans carried. The +0.012 to +0.021 RMSLE of the CC line of 2026-11-06 and the -0.01 to +0.08 of the re-review were measured on all five types, before the blank. Kept by the LEAK-10 / LEAK-37 Cases row of 2026-11-06 (a span drawn by the outcome or by a criterion without it stays, with its worth noted); revisit if Storm Data records which criterion timed an event. Flood is timed by a threat to life or property, from "When flood waters began to threaten life or property" to when there was "no longer any threat to life or property" (Sec. 15; its definition, "inundation by water which causes damage", is the entry criterion, not the clock), and Hurricane (Typhoon) and Tropical Storm from when "the direct effects" of the storm were first experienced (Sec. 25, 49; the "damage or" wording is that of their marine types, Sec. 34 and 39, which are dropped): judged outcome-free and kept. On the declared metric the Flood duration is worth +43%, +0% and +9% of the deviance on its test rows (2023, 2024, 2025; LightGBM of 100 trees with the Tweedie loss, mean of 5 set-ups, 13 of 15 positive) and +5% to +7% on all rows; under RMSLE the Flood and Flash Flood durations together had no consistent sign (-0.09 to +0.09 over the 15 fits).
- Potential leak, kept on purpose (CC 2026-11-08, Lennart; review issue 11): `duration_hours` of Flash Flood (74,914 rows). NWSI 10-1605 Sec. 14 times it by a threat, from "When flood waters became an immediate threat to life or property" to when they "receded to a point where there was no longer an immediate threat to life or property", but one of its four listed onsets is "The point at which any amount of water comes in contact, flowing into, or causes damage to an above ground residence or public building", so the damage can set some starts. Storm Data records no onset type (`flood_cause` gives the cause, heavy rain for 95% of the entries), so no feature locates them. In the event narratives (read only to find double entries, then dropped), 6.8% of the 74,987 Flash Flood entries with a damage figure name water at or in a building or damage to one (mean damage $6.5M against $0.8M for the rest), 36% a road closed or water over a road and 10% a rescue or evacuation; among positive entries the duration tracks the dollars at Spearman 0.44 where the narrative names a building and 0.31 where it does not. Its worth on the declared metric: blanking it raises the deviance on the Flash Flood test rows by +102%, +93% and +31% (2023, 2024, 2025; LightGBM of 100 trees with the Tweedie loss, mean of 5 set-ups, 15 of 15 positive) and on all rows by +9%, +27% and +16%, much of a model's skill. Where the worth comes from (narratives used only to split the test rows, never as a feature or to blank; 2026-11-08): on the 82% of Flash Flood test rows whose narratives name no damage-like onset the duration cuts the deviance by 40% to 48% (100-tree and tuned Tweedie LightGBM, 24 of 24 fits positive), so a longer flood predicts larger damage there too (the share of entries with damage stays flat across duration terciles, the median positive damage rises from $5k to $15k); the 5% that name a building carry 68% to 81% of the total cut (55% to 97% of their deviance), and their spans are longer, not shorter (median 2.75 h against 2.0 h), which points to bigger events rather than starts set later by the damage, without proving it. Kept under LEAK-10's third clause (2026-11-08): the outcome can draw a minority of the starts and the span keeps its worth where it did not; revisit if Storm Data records the onset type. Coastal Flood's duration keeps its worth where the narratives name no damage (+17% to +19% of the deviance); Storm Surge/Tide and Dust Storm show no worth either way.
- Dropped as identifiers or copies: `EVENT_ID`, `EPISODE_ID`, `DATA_SOURCE` (constant from 2007); `YEAR`, `MONTH_NAME`, the begin and end date and time columns and `CZ_TIMEZONE` (in `begin_time` and `duration_hours`); `STATE_FIPS`, `CZ_FIPS`, `CZ_NAME` (in `county_zone`); `BEGIN_RANGE`, `BEGIN_AZIMUTH`, `BEGIN_LOCATION` (a place name and the offset from it, which `begin_lat` and `begin_lon` give); `MAGNITUDE` (in `wind_speed_kt` and `hail_size_in`).
- Built: `begin_time` from `BEGIN_YEARMONTH`, `BEGIN_DAY` and `BEGIN_TIME` (local standard time, as published); `duration_hours` from the end columns the same way (end minus begin; none is negative, the longest are the 31-day entries of a month, such as Flood and Wildfire; blank where the outcome alone sets the span or its start, and on the wind entries whose span only the damage can have timed, above); `county_zone`, the state FIPS code, the zone type and the county or zone number (one code per county, forecast zone or marine zone); `hail_size_in` and `wind_speed_kt` from `MAGNITUDE`, which holds inches for Hail and Marine Hail and knots for the wind types (format document p. 4), one unit per column (a lossless split).
- Dropped as double entries (LEAK-19): 918 rows equal to another row in every column but the event and episode ids, event narrative included, in every year and type (248 Thunderstorm Wind, 228 Hail).
- Note: duplicate rows are kept otherwise: 0.6% of the rows (5,402) are copies of another row in every feature and the target, mostly forecast-zone entries of one storm in one zone at the same time (Heavy Snow, Winter Storm), which the source entered as separate events with their own narratives; with the same begin time they never fall on both sides of a window.
- Note: zone events (30.1% of the rows) have no begin latitude and longitude (all but 4), nor do 153 county events (30.1% of all rows lack them); their place is `county_zone` (7,697 codes).
- Note: the same storm system appears as several events (one per county or zone, `EPISODE_ID` groups them, each storm entered by one office); no episode spans two months (0 of 140,270), so none crosses a window boundary.
- Note: a year's file is rewritten when NCEI updates it. The 2024 files of 17 March 2025 and of 28 July 2026 agree on the damage of 99.83% of the 69,545 events in both (107 blanks filled, 14 values changed; 907 events, 1.3%, were added or removed), and 0 of the 64,921 damage values of January-October 2025 differ between the files of 16 January and 19 August 2026, so the newest year, 2025 (file of 19 August 2026), is settled (leak probe 13).
- Licence: US Government work; NCEI's metadata (C00510) asks to "Cite dataset when used as a source" and warns that reports "may be unverified by the NWS".
- Note: held for training rows only, not shipped (cross-dataset item of 2026-11-09, Andrej): the columns dropped or blanked above as written from, with or after the damage, counted on the task's rows: the tornado rating, path length and width and the `TOR_OTHER_*` fields (23,615 tornado entries), the end point `END_*` (589,452 entries), the injuries and deaths (11,343 entries with one), the crop damage (16,725 entries above $0), the hurricane `CATEGORY` (482), `SOURCE` with its value "NWS Storm Survey" (23,621 entries), the wind speeds estimated from the damage (EG and ES, 253,602), the durations the outcome sets or times (304,268 blanked) and the event narrative (664,164 entries; the episode narrative is not read). The planner holds them for the events of past years when a model is fit, but not for an event logged from its first reports. They would need a training-only role, which the format does not have yet (MET-14, LEAK-41, MET-16), so they stay out for now.
- CC (2026-11-06, Lennart): decision D13 of the exposure study (#51; review issue 6): `duration_hours` is blank for Strong Wind and Heavy Rain, whose span NWSI 10-1605 App. A draws by the damage (Sec. 45, 21), and kept with a note for Thunderstorm Wind, High Wind, Coastal Flood, Lakeshore Flood and Storm Surge/Tide, which it times by the damage or a wind or flooding criterion (Sec. 46, 24, 4, 27, 44), under the new LEAK-10 / LEAK-37 Cases row on spans the outcome sets. Supersedes the definition Andrej shipped on 2026-11-03, which blanked only the tornado durations, as the column audit of 2026-11-01 had read the begin and end of Thunderstorm Wind alone and judged the other spans first-report facts: the study of 2026-11-05 read App. A for every type and measured the column's worth on the seven damage-timed types (+0.02 to +0.04 RMSLE, trained from 2016). On the shipped splits it is +0.013 to +0.021 on those rows, all of it on the five kept types (+0.012 to +0.021) and none on Strong Wind and Heavy Rain.
- CC (2026-11-08, Lennart): review issue 7, B ("Blank these rows"): `duration_hours` is blank also on the Thunderstorm Wind and High Wind entries whose speed the office estimated from the damage (EG, ES) and on the Thunderstorm Wind entries measured under 50 kt, 241,523 rows on which only the damage can have timed the span, as for Strong Wind; the note keeps the measured-wind, dust, ash and flood spans, with their worth measured again (above). Supersedes in part Lennart's D13 of 2026-11-06 (the line above), which kept the duration of every Thunderstorm Wind and High Wind entry with a note.
- CC (2026-11-08, Lennart): review issue 8, B: the target ships in dollars and is scored by the mean Tweedie deviance at power 1.5 (floor $1, above), since the planner sums expected dollars, which RMSLE does not score; the right metric for the task comes first, and earlier calls that do not match the task give way. Supersedes Andrej's RMSLE: issue 3, A, of 2026-11-03, kept for the earlier triage actor, and "the declared metric, RMSLE from context, checked" (Andrej, 2026-11-03) when issue 5 made the planner the actor.
- CC (2026-11-08, Lennart): review issue 10, A (as implemented): the mean Tweedie deviance on the dollars stays as shipped, with the signal stated in the notes (above): tuned Tweedie LightGBM beats the mean per event type in 2024 and 2025, and in 2023 the difference is within noise; the capped target is a note, not shipped.
- CC (2026-11-08, Lennart): review issue 11, B ("Flash Flood kept with a note"): the Flash Flood duration is no longer read as outcome-free but kept with a `Potential leak, kept on purpose:` note giving its worth on the declared metric, since one of its onsets in NWSI 10-1605 Sec. 14 is damage to a building; Flood, Hurricane (Typhoon) and Tropical Storm stay read as outcome-free. Supersedes, for Flash Flood, the reading recorded at the re-review of 2026-11-06.
- CC (2026-11-09, Andrej): review issue 13, A (as implemented): `SOURCE` stays dropped for every entry. The column as published carries the post-event "NWS Storm Survey" marker on the surveyed entries (23,621 on the task's rows), and keeping the reporter would need the surveyed entries re-sourced from an outside archive (the Iowa Environmental Mesonet's Local Storm Reports) by an approximate match in time and place, which in 2024 finds another source for 81% to 91% of the surveyed county entries and leaves the rest marked by a blank.
- CC (2026-11-09, Andrej): review issue 12, c ("Reply (c): Each cell one vote"): the score counts each county or zone, event type and year once: an entry weighs 1 over its cell's entries (`cell_weight`, the task's `unit_weight` with `cell` as its unit), a scoring column, never a feature or a training weight; the use case is reworded to a planner who totals the damage of events already reported, the moment the inputs allow. Supersedes the per-entry unit of issue 8's score (Lennart, 2026-11-08); the metric stays.
- CC (2026-11-09, Andrej): review issue 14, B ("Option B: $10."): the metric's floor is $10, the smallest damage the source records, in place of the $1 of 2026-11-08 (Lennart, review issue 8) from the collection's rule of two orders below the cheapest mean.
- CC (2026-11-10, Andrej): review issue 15, a ("Reply (a): Uncapped"): the damage stays uncapped in training and scoring. The planner's expected annual loss includes the large events (FEMA's National Risk Index builds it from the recorded losses uncapped), and a $10M cap removes 87% of the dollars; the ranking's instability (Kendall's W 0.62 across the windows; tuned LightGBM separates from the mean per event type only in 2025) is a fact of a noisy task, stated in the notes, not a reason to change the target. Supersedes the AI's recommendation of the cap of 2026-11-09.

## Splits

A model refit at the start of each year estimates the damage of that year's events; the yearly cadence is ours (NCEI releases monthly). The test windows are the calendar years 2025, 2024 and 2023 (newest first), each a full cycle of the storm seasons (tornadoes in spring, hurricanes in autumn, winter storms), since storm damage is strongly seasonal and a shorter window would test one season. Each window trains on every earlier event from 2007 on except the last three months before it: a Storm Data month is certified "no later than 60 days after the end of the month" (NWSI 10-1605, Sec. 3), and NCEI's public files are "updated monthly with up to a 120 day delay possible" (C00510). In archived releases a month first appears complete 75-80 days after its end (the 2025 file of 16 January 2026 holds all of October 2025 and no November), so at a refit on 1 January the public files hold the events through September. Offices and counties recur across the years (SPLIT-13): the model estimates the damage of new events in known places.

3 repeat(s) x 1 fold(s) with seed 4267; train 702,587 to 793,017 rows, test 44,056 to 45,870 rows. Prediction horizon: 1 years. Gap between train and test: 3 months.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 793017 | 45870 | 2007-01-01 00:00:00 | 2024-09-30 22:30:00 | 2025-01-01 00:00:00 | 2025-12-31 23:40:00 |
| 1 | 0 | 749875 | 44255 | 2007-01-01 00:00:00 | 2023-09-30 21:35:00 | 2024-01-01 00:00:00 | 2024-12-31 23:20:00 |
| 2 | 0 | 702587 | 44056 | 2007-01-01 00:00:00 | 2022-09-30 20:47:00 | 2023-01-01 00:00:00 | 2023-12-30 23:00:00 |

## Decisions

### 1. Entries without a damage figure are dropped; $0 stays

A blank damage field leaves the row without a target. We read it as the 'no information available' box of NWSI 10-1605, Sec. 2.7 (an inference: floods, which must get an amount, have no blank from 2008 on). A $0 is kept as entered; it mixes no damage with no estimate made, and an office can move between $0 and blank for the same kind of event over the years (notes).

| event type | events | blank (dropped) | $0 among entries | median of the positive ($) |
|---|---|---|---|---|
| Thunderstorm Wind | 320270 | 0.183 | 0.439 | 5000 |
| Hail | 202110 | 0.258 | 0.903 | 10000 |
| Flash Flood | 74995 | 0 | 0.639 | 12000 |
| Winter Weather | 70969 | 0.229 | 0.958 | 10000 |
| High Wind | 65130 | 0.178 | 0.823 | 15000 |
| Drought | 63979 | 0.283 | 0.993 | 50000 |
| Winter Storm | 57818 | 0.193 | 0.907 | 22500 |
| Flood | 48531 | 0 | 0.713 | 12000 |
| Heavy Snow | 43874 | 0.183 | 0.963 | 20000 |
| Marine Thunderstorm Wind | 36703 | 0.265 | 0.997 | 5000 |
| Tornado | 27658 | 0.146 | 0.412 | 50000 |
| Heat | 23772 | 0.239 | 0.999 | 400000 |

### 2. A $0 depends on the office

Offices differ widely in how often they enter $0 for the same event type, and the practice drifts over the years; the office is a feature, so a model can learn the practice, and the target is not repaired (kept under LEAK-25 as amended, Andrej, 2026-11-02).

| index | value |
|---|---|
| offices with 100 or more Thunderstorm Wind entries | 107 |
| share at $0, 10th percentile of the offices | 0.073 |
| share at $0, 25th percentile of the offices | 0.199 |
| share at $0, 50th percentile of the offices | 0.546 |
| share at $0, 75th percentile of the offices | 0.823 |
| share at $0, 90th percentile of the offices | 0.913 |

## Bundle checks

0 error(s), 0 warning(s), 2 info (27 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 5,402 exact duplicate row(s) (0.6% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)
- **info** `dataset_conflicting_duplicate_rows`: 621 row(s) (0.1%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)

Accepted on purpose:

- `task_target_value_dominant`: Zero-inflated: 68% of the entries are $0, kept as entered; part of the zeros are unestimated damage (13 of 121 EF4 and EF5 tornado segments at $0; kept under LEAK-25 as amended, Andrej, 2026-11-02).

## Data checks

### Feature summary

<details>
<summary>Show the table (16 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| flood_cause | category | 718019 | 85.16 | 7 | Heavy Rain, Heavy Rain / Snow Melt, Heavy Rain / Tropical System, Heavy Rain / … |
| magnitude_type | category | 509961 | 60.48 | 4 | EG, MG, MS, ES |
| state | category | 0 | 0 | 55 | TEXAS, IOWA, ILLINOIS, MISSOURI, VIRGINIA, KANSAS, PENNSYLVANIA, KENTUCKY, NEW … |
| event_type | category | 0 | 0 | 34 | Thunderstorm Wind, Hail, Flash Flood, Winter Weather, High Wind, Flood, Winter … |
| cz_type | category | 0 | 0 | 2 | C, Z |
| wfo | category | 0 | 0 | 123 | PAH, PHI, DMX, LWX, JAN, SGF, FWD, RNK, OUN, SHV |
| county_zone | category | 0 | 0 | 7697 | 17C031, 04C013, 08C041, 42C003, 56Z110, 48C439, 19C153, 29C077, 01C077, 40C143 |
| cell | category | 0 | 0 | 258067 | 56Z110\|High Wind\|2017, 01C077\|Thunderstorm Wind\|2025, 56Z110\|High Wind\|2016, 56… |
| begin_time | datetime64\[ns\] | 0 | 0 | 508378 | 2011-02-01 00:00:00, 2011-05-01 00:00:00, 2015-02-01 00:00:00, 2019-06-01 00:00… |
| wind_speed_kt | float64 | 763563 | 90.56 | 119 | 50.0, 52.0, 51.0, 56.0, 53.0, 54.0, 55.0, 35.0, 57.0, 58.0 |
| hail_size_in | float64 | 693507 | 82.25 | 123 | 1.0, 0.75, 0.88, 1.75, 1.25, 1.5, 2.0, 2.75, 2.5, 3.0 |
| duration_hours | float64 | 304268 | 36.09 | 7195 | 0.0, 2.0, 1.0, 0.0833, 0.0167, 3.0, 6.0, 12.0, 0.0333, 8.0 |
| begin_lat | float64 | 253692 | 30.09 | 122108 | 37.27, 41.02, 41.13, 41.23, 37.18, 37.17, 37.12, 41.03, 41.6, 36.87 |
| begin_lon | float64 | 253692 | 30.09 | 168134 | -93.8, -93.2, -94.35, -93.29, -92.4, -92.45, -92.66, -92.92, -97.15, -93.22 |
| property_damage_usd | float64 | 0 | 0 | 1867 | 0.0, 1000.0, 5000.0, 10000.0, 2000.0, 3000.0, 50000.0, 25000.0, 20000.0, 15000.0 |
| cell_weight | float64 | 0 | 0 | 123 | 1.0, 0.5, 0.3333, 0.25, 0.2, 0.1667, 0.1429, 0.125, 0.1111, 0.1 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 68.13 | 252.181 | 1.038 | 1.28786e+15 | 19.078 | log1p | 8.12822e+06 | 6.00805e+06 | lognormal |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| begin_lat | 589452 | 37.8213 | 4.98192 | -14.4 | 70.5029 |
| begin_lon | 589452 | -90.5268 | 11.5554 | -171.033 | 171.366 |
| property_damage_usd | 843144 | 435007 | 3.58868e+07 | 0 | 1.7e+10 |
| duration_hours | 538876 | 14.9923 | 57.7054 | 0 | 743.983 |
| cell_weight | 843144 | 0.306077 | 0.309374 | 0.00323625 | 1 |
| hail_size_in | 149637 | 1.17508 | 0.4935 | 0.13 | 7.75 |
| wind_speed_kt | 79581 | 53.8418 | 9.32148 | 17 | 149 |

### Categorical features

<details>
<summary>Show the table (42 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| begin_time | 1 | 2011-02-01 00:00:00 | 301 | 0.04 |
| begin_time | 2 | 2011-05-01 00:00:00 | 266 | 0.03 |
| begin_time | 3 | 2015-02-01 00:00:00 | 259 | 0.03 |
| begin_time | 4 | 2019-06-01 00:00:00 | 249 | 0.03 |
| begin_time | 5 | 2019-05-01 00:00:00 | 229 | 0.03 |
| cell | 1 | 56Z110\|High Wind\|2017 | 309 | 0.04 |
| cell | 2 | 01C077\|Thunderstorm Wind\|2025 | 262 | 0.03 |
| cell | 3 | 56Z110\|High Wind\|2016 | 201 | 0.02 |
| cell | 4 | 56Z110\|High Wind\|2014 | 194 | 0.02 |
| cell | 5 | 56Z110\|High Wind\|2013 | 180 | 0.02 |
| county_zone | 1 | 17C031 | 1832 | 0.22 |
| county_zone | 2 | 04C013 | 1818 | 0.22 |
| county_zone | 3 | 08C041 | 1623 | 0.19 |
| county_zone | 4 | 42C003 | 1565 | 0.19 |
| county_zone | 5 | 56Z110 | 1559 | 0.18 |
| cz_type | 1 | C | 589601 | 69.93 |
| cz_type | 2 | Z | 253543 | 30.07 |
| event_type | 1 | Thunderstorm Wind | 261454 | 31.01 |
| event_type | 2 | Hail | 149637 | 17.75 |
| event_type | 3 | Flash Flood | 74914 | 8.89 |
| event_type | 4 | Winter Weather | 54685 | 6.49 |
| event_type | 5 | High Wind | 53486 | 6.34 |
| flood_cause | 1 | &lt;NA> | 718019 | 85.16 |
| flood_cause | 2 | Heavy Rain | 113459 | 13.46 |
| flood_cause | 3 | Heavy Rain / Snow Melt | 5848 | 0.69 |
| flood_cause | 4 | Heavy Rain / Tropical System | 3255 | 0.39 |
| flood_cause | 5 | Heavy Rain / Burn Area | 1281 | 0.15 |
| magnitude_type | 1 | &lt;NA> | 509961 | 60.48 |
| magnitude_type | 2 | EG | 252451 | 29.94 |
| magnitude_type | 3 | MG | 73180 | 8.68 |
| magnitude_type | 4 | MS | 6401 | 0.76 |
| magnitude_type | 5 | ES | 1151 | 0.14 |
| state | 1 | TEXAS | 60683 | 7.2 |
| state | 2 | IOWA | 33479 | 3.97 |
| state | 3 | ILLINOIS | 32727 | 3.88 |
| state | 4 | MISSOURI | 32010 | 3.8 |
| state | 5 | VIRGINIA | 29362 | 3.48 |
| wfo | 1 | PAH | 21300 | 2.53 |
| wfo | 2 | PHI | 20797 | 2.47 |
| wfo | 3 | DMX | 18432 | 2.19 |
| wfo | 4 | LWX | 17916 | 2.12 |
| wfo | 5 | JAN | 16827 | 2 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
