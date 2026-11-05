# IID, grouped and temporal splits

Part 4 of the curation rules, under P4 (Honest evaluation) in [principles.md](principles.md). The rules of earlier
parts win over this file's rules in a conflict; within this file a rule wins over the rules below it of the same
strength. How to weigh, exceptions and amendments: [principles.md](principles.md).

Whether a dataset is IID or non-IID is decided by the appropriate train-test split: the split that most closely
mirrors the real-world application ([use_case.md](use_case.md)). This file covers the three regimes, the split of a
temporal task that is not forecasting (the line between them is SEL-10 and SEL-11 in [selection.md](selection.md)),
temporal windows, grouped splits and hidden groups in an IID task. Background from the TabArena paper (Section 2,
Appendix B.3), extended by the curators' decisions.

## Rules

### The split and the regimes

**SPLIT-1 (Must).** The split is the one that most closely mirrors the real-world application, and it decides whether
a dataset is IID or non-IID. The split depends on the application, and the curator picks the one the dataset's
application needs (USE-1, [use_case.md](use_case.md)). Why: on the same data, a split that does not mirror the
application overrates or underrates models (the two applications under Patterns).

**SPLIT-2 (Must).** A split follows one of three regimes.

* IID: the test rows follow no particular structure; a random hold-out is right.
* Temporal: a time index exists, and the test rows come strictly after the training rows (predicting the future).
* Grouped: a group index exists, and all rows of a group stay on one side, so the model is tested on unseen entities.
  The label is either one per group (is this customer fraudulent, from their transactions) or one per row (the
  outcome of each visit of a patient unseen in training).

**SPLIT-3 (Must).** In practice a non-IID task is grouped or temporal (Lennart, 2026-10-12); we have met no third
kind. A task is one or the other, never both, and the use case (P3, [use_case.md](use_case.md)) decides which. A
temporal split does not remove group structure, and a grouped split does not make a task time-invariant, but the
split decides which dependency the test measures. An order inside groups (the latest statement of each customer) is
part of the grouping.

**SPLIT-4 (Must).** The split follows what the task does in reality, not the size of the gap. If the deployed model
predicts for an entity new data would not contain (a material nobody has measured, a new respondent), the test
entities must be new, even when a random split costs little. If new rows keep having the value, the column is a
feature and the split stays. Why: holding out the values of any useful feature opens a gap, so the gap never decides;
a manager, a soil type or a fund category is known for every new row. Cases: superconductivity.

**SPLIT-5 (Must).** The split a paper or a dataset page prescribes is a claim to check against the task design, not a
fact. Authors often pick a random split on data that is really temporal. Check a claim about a split against the data
as well. A benchmark's non-IID label can also be wrong for our framing, in either direction. Cases:
appliances_energy_prediction, kick.

### Forecasting and a missing time axis

**SPLIT-6 (Must; applies SEL-11).** A fixed predictive task that only needs a temporal split (a delivery time, a
default, a sale price) gets a temporal split. Forecasting itself is out (SEL-10, [selection.md](selection.md)), and a
panel that looks like forecasting is tested with TP-10 ([task_probes.md](task_probes.md)). Cases:
combined_cycle_power_plant, appliances_energy_prediction.

**SPLIT-7 (Must).** A missing or hidden timestamp does not make a task IID. The time index is often absent: dropped
by an uploader, never shipped, or only implied by how the data was collected (readings logged over months, every
feature and the target contemporaneous). When the setup is values unfolding over time from a stream of signals, it is
temporal or forecasting whether or not a date column survived. Cases: combined_cycle_power_plant.

**SPLIT-8 (Must; narrows SPLIT-7, SPLIT-14 and USE-10).** When a task is temporal in nature or by its use case but
the release cannot give the windows SPLIT-14 asks for, it ships in the closest regime that keeps the rows, tagged as
forced from temporal, with the cost measured against the valid windows where the data has any. This covers a release
with no dates at all (one extract, the status at that moment standing in for a forecast), a release with one stock
month of the base or a few cohort months of one customer base (a split by those months tests a change of cohort, not
of time), and a release with too few periods for three windows. The closest regime is IID (tag
`ForcedIIDFromTemporal`), or grouped by the entity when the periods are stacked and the entities recur across them
(tag `ForcedGroupedFromTemporal`). Say what the timestamp or a dated window would change and that it should be
recovered if a later release has it. A forced split, grouped or IID, ships only when a leak test across the
split finds none (no row shares its outcome, its unit's outcome or its period's outcome with the other side, no
hidden group, no order dependence); where it finds one, as hours of one storm on both sides in
how_much_did_it_rain, the dataset is `No`. (Lennart, 2026-10-12; amended 2026-10-21, Lennart: one stock month, from
mobile_churn and the churn snapshots; too few periods, from nba_players_2016_2019,
open_university_learning_analytics_dataset and distribution_transformers_at_cauca_department; amended 2026-11-02,
Andrej: which forced splits ship, from the insurance tables of the zero-inflated batch.) Cases:
account_debt_south_africa, mobile_churn, open_university_learning_analytics_dataset (nba_players_2016_2019 was
retired on 2026-10-26 on its use case, not its split), the seven insurance tables of 2026-11-02 (Cases table).

### Temporal tasks

Every feature has to have existed at the prediction time of its row: LEAK-10 in [leak_checks.md](leak_checks.md).

**SPLIT-9 (Must; amended 2026-11-05, Lennart, on lt_vehicle_loan_default_prediction).** A training row whose label tells
a test row's outcome and was not yet known at the prediction point must not be in train: a row that is in train because
its outcome came early (hotel_booking_demand: bookings arriving after the prediction date, kept because they were
already cancelled), or a label of the test row's own entity set after its prediction point (alfa_battle_2_0_task_2: a
client's earlier product flagged as defaulted after the later one was issued). Why: the model learns such outcomes as a
shortcut. The shortcut is measured and removed, whatever it costs SPLIT-14's floor. The rest of the unmatured training
labels is not a shortcut and falls under SPLIT-10: labels that reach a test row only through codes shared by many
entities (the recent default rate of a dealer or a branch), with no link to the row's own entity and an effect that does
not grow toward the release end; the notes give its measured size. Check that the filter removes the shortcut: for
hotel_booking_demand, filtering on the status date does not, filtering on the arrival date does. Cases:
hotel_booking_demand, alfa_battle_2_0_task_2, lt_vehicle_loan_default_prediction.

**SPLIT-10 (Should; applies SPLIT-9; amended 2026-11-04 and 2026-11-05, Lennart, on
lt_vehicle_loan_default_prediction).** When a label is known only some time after its row (a delivery time, a permit's
processing time, an outcome after a follow-up), a model refit at a window's start knows only the rows whose label had
arrived. Simulate that: train on the rows whose outcome is known by the window's start, with a gap of about the label's
delay between train and test. The gap is part of the task and is stated with it. A planning gap the use case has (a
forecast made a day ahead) is a gap too. Why: without the gap the newest training rows are the fast ones, and a model
that sees the time as a number is biased. Cases: brazilian_ecommerce, sf_permit_time.
Amended 2026-11-04 and reworded 2026-11-05 (Lennart, on lt_vehicle_loan_default_prediction: "we argue from measurement
and context that we dont see this pattern in the data as a problem, the gap is already accounted for by collection or
other means"): the measurements decide, also where the source or the context documents late labels. A gap is set where a
measurement shows a shortcut through recent labels (SPLIT-9) or a selection by the outcome at the release end, and where
late labels are documented and the collection does not cover them. No gap is needed where the collection covers what the
gap guards against and the measurements show neither: the time column's smallest step is longer than the delay (sales
dated by month), the newest period is as complete as a later read of it, or a fixed outcome horizon (one due date for
every row, every label final at release) removes the selection by the outcome, since the unmatured rows are then not the
fast ones. A fixed horizon does not remove the delay itself: the newest training labels were still unknown at a window's
start, so the notes give what they add at equal training size. Where the gap a case needs breaks SPLIT-14's floor, the
departure is an exception (principles.md, Tensions). Cases: ames_housing, perth_house_prices, melbourne_housing_market,
lt_vehicle_loan_default_prediction.

**SPLIT-11 (Should).** Train on everything before the window (an expanding train side). The first split is the newest
window, with the most training data and the most representative; the others walk back in time.

**SPLIT-12 (Should).** The horizon is a human judgment from the source: how far ahead the actor predicts ("managers
predict sales up to six weeks in advance"), the competition's own test window, the refit cadence. Choose the test
windows to match it and write the reasoning down.

**SPLIT-13 (Should).** Look for grouped structure inside a temporal task: repeated observations of one entity over
time (transactions of one customer). An entity that recurs across the cutoff is part of the task when the model
predicts for known entities, and a question when the use case is a new entity (USE-10, [use_case.md](use_case.md)).

### How many windows

**SPLIT-14 (Must).** A temporal task has at least 3 windows, and no window's train side holds less than 50% of the
data. Why: a smaller train side is too unlike the real application. A task that cannot meet it ships under SPLIT-8
(Lennart, 2026-10-21). Windows that share one train side count as one window: a new test window means a refit, so
each window trains on what is known before it (Andrej, 2026-11-02).

**SPLIT-15 (Should).** Roll the windows back from the newest data: as many windows as an IID or grouped task of that
size would get folds. Then check that the windows are still meaningful (SPLIT-16 to SPLIT-18).

**SPLIT-16 (Must).** Do not fall back to an IID split for a non-stationary sequence whose windows hold too few
positives. Counting the positives per window and the `Too Small` verdict are TP-9 ([task_probes.md](task_probes.md)).
Marker: `Too Small`. Cases: seismic_bumps.

**SPLIT-17 (Should).** Widen windows that get too small: below about 50 test rows per window, use wider windows and
fewer splits. Why: finer windows add no test rows (the 50% floor of SPLIT-14 fixes the test pool); they cut it into
smaller, noisier pieces. Cases: coffee_rating_prediction.

**SPLIT-18 (Should).** Short-lived quantities need short windows: weather test windows of one to two weeks at most.
Cases: climate_model_weather_forecasting.

### The training history

**SPLIT-19 (Should).** When the source defines the split (a competition's or a paper's official periods), follow it.
A prescribed split is still a claim to check (SPLIT-5).

**SPLIT-20 (Should).** Otherwise decide what the train side holds from the use case: the history a model refit at each
window would train on. Read what the source's authors trained on, check the history for breaks (COVID-19, a change of
rules or of the data collection), keep a recent stretch with at least one full season before the newest window, and
say why. Check whether the newest windows fall in an atypical season and widen them so most do not. Cases: aeolus.

**SPLIT-21 (Must).** Decide neither the training history nor the windows from a comparison over a few test windows.
Why: such a comparison changes with the kind of window, so it measures the windows, not the design. Cases: aeolus
(Lennart, 2026-10-12).

### Row order as time

**SPLIT-22 (Should).** The raw file order can be the time order without a timestamp; keep it. A deduplication, merge
or lookup can reorder rows: rebuild a row-order time index after such steps and check it against the date. Cases:
seismic_bumps, california.

### Grouped tasks

**SPLIT-23 (Must).** The source's use case, cited, decides what one prediction is (a row, or a whole group: replicates
averaged, any instance positive, the latest row, the best of several candidates) and what is known about a new group
when predicting; the label structure alone does not.

Cold start or warm start is decided from the use case before grouping: USE-10 and USE-11 in
[use_case.md](use_case.md).

**SPLIT-24 (Must).** Group on a true group id, or on one constructed exactly from the data: identical profile text or
a poster-specific masked contact, consecutive blocks of identical person-level answers in the raw file order,
identical values in the columns that define the entity. Never on a similarity-threshold cluster, and never on a hash
of the feature vector standing in for an unknown entity. Cases: emscad, in_vehicle_coupon_recommendation,
concrete_compressive_strength, airfoil_self_noise, maternal_health_risk.

**SPLIT-25 (Must).** When the real groups matter and cannot be recovered, retire the dataset rather than group on a
guess, and note that the authors could be asked for the group labels. Cases: maternal_health_risk,
hazelnut_spread_contaminant_detection.

**SPLIT-26 (Should).** Take the group key from the source's own data, at the resolution the features see. Keep the
source's rows: deduplicating with averaged targets is a different dataset. Cases: superconductivity.

**SPLIT-27 (Should).** Before calling a small grouped task unlearnable, judge it with several model families scored per
group, against the class-share baseline, with a permutation test across groups. One untuned gradient-boosting run is
not enough: on unseen groups its probabilities are overconfident. Cases: mice_protein.

**SPLIT-28 (Must).** A regression task whose models all score below the mean on unseen groups has no signal across
groups; then the use case has to allow known groups, or the dataset goes. Before recasting it as warm start, compare a
model with the group's known value carried forward. Cases: telemonitoring_parkinsons.

### Hidden groups in an IID task

**SPLIT-29 (Must).** An IID split is wrong when many rows share an entity that new data would not have and the entity
carries the label. Why: a random split then rewards recognising the entity.

**SPLIT-30 (Must; applies EV-3).** A hidden-group probe hit is a question (EV-3, [evidence.md](evidence.md); Lennart,
2026-10-06). Re-split only when the context says the rows share an entity new data would not have (the source calls
the column an id, or the use case predicts for new entities), or when the evidence is very strong. The size of the
gap never decides (SPLIT-4).

**SPLIT-31 (Should).** Over related entities, IID can match how a task is framed even when it is optimistic: such a
task is a candidate for a grouped or temporal variant, not a fix. Cases: amazon_employee_access, bank_marketing.
Molecules are the exception (amended 2026-10-26, Lennart, on qsar_bioconcentration: "in other cases, we also moved
towards a scaffold split as is often correct for chemicals"): a molecule dataset whose rows carry exact structures
groups on the Bemis-Murcko scaffold, as a new chemical under assessment often comes from a series not yet measured. A
molecule without a ring is a group of its own, and so is each molecule of a scaffold that holds more than a tenth of
the molecules, which is no series and would leave folds of very unequal size (`scaffold_groups` in
`data_foundry.v2.chemistry`). Cases: drug_induced_autoimmunity_prediction, qsar_bioconcentration, qsar_oral_toxicity,
qsar_tid_11.

The hidden-group cases and the probe's calibration are in [task_probes.md](task_probes.md), "Hidden groups".

## Weighed factors

* **Only a few groups** (− for a grouped split): with only a few groups, a grouped split is a domain-shift test
  between them rather than prediction for unseen entities; that is its own decision (covertype: 3 wilderness areas,
  IID instead; heart_disease: 3 hospitals kept grouped, as the source's own transfer design).

## Patterns

Quick ways to apply the rules; a pattern never overrides a rule, and the dataset at hand wins over the pattern.

* **The same data, two applications (SPLIT-1).** Alice predicts whether past transactions were fraudulent, for
  follow-up investigations: a random (IID) split fits. Bob predicts whether new transactions are fraudulent, to stop
  fraud as it happens: a temporal split fits, because it simulates unseen future transactions. With a random split Bob
  would overrate models that exploit temporal leakage; with a temporal split Alice would underrate them.
* **Composite keys (SPLIT-4, SPLIT-24).** Rows identical in every column but one are one entity at another age, dose,
  time or frequency (concrete_compressive_strength). When that key is what one row's entity is, group on it; when new
  rows keep the key, it is a feature.
* **Few groups per class (TP-5).** With few groups, real signal is not enough: count the groups of each class in total
  and per test fold ([task_probes.md](task_probes.md)).

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.

| Rule | Dataset | Decision (date, curator) | Kind |
|---|---|---|---|
| SPLIT-1 | airfoil_self_noise | grouped by setup, not by run: under the run split 91.5% of the test runs had their chord and angle in training at another speed, and a new angle or size is the query a tunnel cannot answer with one more run; treated like concrete_compressive_strength's mix (2026-10-20, Lennart) | applied |
| SPLIT-4 | superconductivity | grouped by composition: a model is used for compositions nobody has measured, though a random split costs at most 0.009 R^2 (2026-10-06) | applied |
| SPLIT-5, SPLIT-6 (SEL-10) | appliances_energy_prediction | 10-minute readings over 4.5 months, evaluated with a random split by its authors; it is forecasting, `No` | applied |
| SPLIT-5 | kick | a comment called the Kaggle split grouped by auction location, yet 78.9% of its test rows are at a location also in train | applied |
| SPLIT-6, SPLIT-7 (SEL-10) | combined_cycle_power_plant | no timestamp, looks like IID sensor regression, but it is a six-year hourly stream predicting the plant's output: forecasting, `No` | applied |
| SPLIT-8 | account_debt_south_africa | ships as IID, tagged forced IID from temporal; held out by file block, ROC AUC falls from 0.877 to 0.843 and 0.786 (2026-10-12, Lennart) | applied |
| SPLIT-8 | mobile_churn, churn_telco_south_asia, bank_customer_churn, tour_travels_churn | one stock month (mobile_churn: June's base plus the July and August joiners) or one undated snapshot: IID, `ForcedIIDFromTemporal`; on mobile_churn's 1,533 later joiners, training on June gives ROC AUC 0.661 against 0.690 IID, the others cannot measure it (2026-10-21, Lennart) | applied |
| SPLIT-8 | nba_players_2016_2019, open_university_learning_analytics_dataset | too few periods (3 seasons; 4 start dates): stacked and grouped by player or by module-presentation, `ForcedGroupedFromTemporal`; on the one valid window R^2 0.745 against 0.744 grouped (nba), log loss 1.185 against 1.205 grouped (open_university) (2026-10-21, Lennart); nba retired on 2026-10-26 on its use case (USE-1, USE-5), not on the split | applied |
| SPLIT-8 | distribution_transformers_at_cauca_department | two label years, one window: one year IID, `ForcedIIDFromTemporal`, not stacked, as the two files hold the same units with identical attributes; ROC AUC 0.648 trained on 2019 and tested on 2020 against 0.639 on the random folds (2026-10-21, Lennart) | applied |
| SPLIT-8 | bemtpl97 | one policy year (1997), undated, the raw order sorted by postcode: IID, `ForcedIIDFromTemporal`; the cost cannot be measured (2026-11-04, Lennart: beMTPL97 and freMTPL2 treated alike) | applied |
| SPLIT-8 | fremtpl2 | no policy dates; the blocks read as stacked periods with linked IDpols, but both the periods and the links are inferred, not the source's key (SPLIT-24), unlike nba and open_university, which group by a recorded entity: IID, `ForcedIIDFromTemporal`; grouping by the inferred chains costs +0.00049 Poisson deviance and leaves the ranking unchanged (2026-11-04, Lennart) | applied |
| SPLIT-8 | frempl_french_motor_personal_line, rand_health_insurance_experiment_doctor_visits, spanish_motor_insurance_coverage_level_2022_2024, pricing_game_2017_french_mtpl, allstate_claim_prediction_challenge_1m; australian_vehicle_insurance_2004_2005, liberty_mutual_fire_peril_loss_cost; how_much_did_it_rain | the amendment: a forced split, grouped or IID, ships only when the leak test across the split finds none (how_much_did_it_rain's `No` of 2026-10-30 named a measured leak, hours of one storm on both sides). The forced grouped tables were tested the same way on 2026-11-02 (shared rows and units, the training side's outcome of the test rows' period, features built from other rows' outcomes): frempl, rand, spanish 2022-2024, pricing_game_2017 and allstate_1m show none and ship; wisconsin_local_government_property_insurance_fund leaks its years' claim level across the split (removing the test year's training rows costs ROC AUC 0.010 on 8 of 9 splits), open as its issue 1; australian (no row shares its outcome across the split, no hidden group, no order dependence) and liberty (a risk's training loss ranks its test terms at AUC 0.50-0.52, and removing a test risk's terms from training costs no more than removing as many random rows) ship as forced IID ("Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship.", 2026-11-02, Andrej; "I want you to also do leakage checks for forced grouped", same day) | applied |
| SPLIT-9 | hotel_booking_demand | train kept bookings arriving after the prediction date that were already cancelled (100% positive), so the model learned "future arrival means cancelled"; filtering on the status date kept the shortcut, filtering on the arrival date removed it | applied |
| SPLIT-9 | alfa_battle_2_0_task_2 | the training products of clients with a product in the test window are dropped (32,861-39,221 rows; 60-83% of each training side kept), standing in for the as-of filter on label dates the data lacks: a later product defaults at 95.1% after a defaulted earlier one (2.3% otherwise), flat over lags of 1-10 months, while 45.5% of later defaults had one, so the earlier flag was set after the later issue; without the filter the window's ROC AUC rises by 0.002-0.009. Differs from ieee_fraud_detection (LEAK-34, 2026-10-01), whose carried labels follow the host's labelling rule and are read as known history (2026-10-26, Lennart) | applied |
| SPLIT-9 | lt_vehicle_loan_default_prediction | not a shortcut, gap 0 kept: the last 30 days' default rates of the supplier, branch, employee and postcode codes add +0.0026 ROC AUC at equal pool size (0.0005-0.0051, 9 of 9 windows; up to +0.0057 in other encodings), the size of alfa_battle_2_0_task_2's removed effect; set apart by the mechanism: each code is shared by many borrowers and no borrower recurs (rebuilt borrowers score 0.517-0.543), so no test row is linked to its own client's earlier label (alfa: 95.1% default after an earlier default against 2.3%), and the effect does not grow at the release end (0.0025 in the newest window against 0.0028); the notes give its size (2026-11-05, Lennart) | applied |
| SPLIT-10 | brazilian_ecommerce | a gap of one month; R^2 0.353 with the gap, -0.054 without (2026-10-15, Lennart) | applied |
| SPLIT-10 | sf_permit_time | a gap of 6 months, since a 1-month gap still censored the slow permits | applied |
| SPLIT-10 | alfa_battle_2_0_task_2 | no label dates, a default flagged up to a year after issue: a 12-month gap leaves 13-27% of the rows for training, a 6-month gap 35-53%; SPLIT-9 met by dropping the products of the test window's clients. Serves SPLIT-14 (2026-10-21, Lennart); gap 0 (2026-10-26, Lennart) | exception |
| SPLIT-10 | lending_club | outcomes known up to 36 months after issue, no outcome dates: a 36-month gap leaves 5-9% of the rows for training, a 12-month gap 33-46%. Serves SPLIT-14 (2026-10-21, Lennart) | exception |
| SPLIT-10 | ames_housing | no gap: the extract's last month is short (June 2010, 78% of a usual June) but its normal sales show no price selection (mean residual -0.001), and sales are dated by month, so the smallest gap (a month) is longer than the delay. Serves P4: the windows train on every recorded sale before them, as a model refit each month would (2026-10-26, Lennart) (an application since the amendment of 2026-11-04) | applied |
| SPLIT-10 | perth_house_prices | no gap: sales are dated by month, so the smallest gap (a month) is longer than the delay, and the newest month present early (December 2020, 0.71 of November) shows no price selection (mean residual +0.017 against +0.003 to +0.025); the second exception of this reason (2026-10-26, Lennart) (an application since the amendment of 2026-11-04) | applied |
| SPLIT-10 | house_sales | a one-week gap: from the deed date to the recording date the delay has a median of 6 days, and 91% of sales are recorded within 14 days (review of 2026-10-20) | applied |
| SPLIT-10 | zillow_prize | a one-month gap: training is every sale before the preceding month, since Zillow receives sales with a delay (review of 2026-10-20) | applied |
| SPLIT-10 | melbourne_housing_market | no gap, measured: every weekly sheet from August 2017 holds as many sales as the companion file read up to October 2018 (558 of 558 on 17 March 2018), and the newest window's mean residual is +0.009 against -0.013 to +0.022 (2026-10-21, Lennart: a gap only if the newest months show selection) | applied |
| SPLIT-10 | lt_vehicle_loan_default_prediction | no gap, an application of the amendment as reworded on 2026-11-05: one due date per loan (the first instalment, inferred at least about a month after disbursement; the release gives none) and every label final at release, so the unmatured rows are not selected by their outcome, and the release end shows drift, not censoring; the newest training labels add 0.0018-0.0051 ROC AUC at equal training size across four learners (no gap scores 0.007-0.017 above a 30-day gap), +0.0026 of it through recent default rates of shared codes (SPLIT-9 row); a 30-day gap would keep the 50% floor only with three two-day windows instead of nine (SPLIT-15) (2026-11-04, Lennart: the amendment; 2026-11-05, Lennart: an application, not an exception) | applied |
| SPLIT-9, SPLIT-10 | nyc_taxi_trip_duration_1m, pkdd_15_taxi_trip_time_prediction_ii_1m, cooking_time_1m, maps_router_eta_1m, delivery_eta_1m | trip and order times in weekly or monthly windows: the training rows whose trip or order ends after the window start are counted per window, and a one-day gap is set where any are (nyc 77-127 per window, pkdd 8-48, cooking_time 108-172, maps_router_eta 578-656; 0 after); delivery_eta_1m has none, its orders stop overnight (2026-10-21, Lennart) | applied |
| SPLIT-10 | pricing_game_2016_french_fleet | no gap: no report dates, and rows are cut at 31 December, so even a 1-day gap before the January window leaves 50.2% of the rows and a month 48.7%; the bound is simulated in the notes. Serves SPLIT-14 (2026-11-02, Andrej) | exception |
| SPLIT-10 | noaa_afsc_bottom_trawl_survey_cpue | no gap: the source states no delay between a survey and its use (only the surveys it used, 1982-2019, TM-459 p. 3), catches are counted at sea, and FOSS held the 2026 summer's hauls by 30 October, before the next season, so the delay is shorter than the windows' step (yearly seasons). Serves P4: each two-year window trains on every survey before it, as a model refit after each season would; the third case resting on a delay shorter than the time column's step, after ames_housing and perth_house_prices (2026-11-02, Andrej: "Unless the original paper says so, we should go with no planning gap") | exception |
| SPLIT-10 | ames_housing, perth_house_prices | proposed amendment, due at the third exception of this reason (principles.md, "Exceptions and amendments"): "No gap is needed when the label's delay is shorter than the resolution of the time column (sales dated by month) and the newest period shows no selection by the outcome (its mean residual within the other windows' range)." Both exceptions rest on these two facts; alfa_battle_2_0_task_2 and lending_club depart for another reason (SPLIT-14's floor) and do not count (proposed 2026-10-26 from the consistency check on ames_housing; open for Lennart) (settled by the amendment of 2026-11-04, Lennart) | applied |
| SPLIT-12 | house_sales, perth_house_prices, ames_housing, zillow_prize, melbourne_housing_market | no window length for the whole family: each keeps the horizon of its own source or refit cadence (three weeks; one month, spaced; two months; one month after a one-month gap; three weekly sheets), since "different task might forecast differently long" and "we dont need to force the same split" (2026-10-21, Lennart) | applied |
| SPLIT-12, SPLIT-19 | medical_facility_operational_data | the source's horizon followed: Crowley et al. (2020) train on six months and test on "a further consecutive two weeks", so nine 14-day windows replace nine equal-count windows of 42-53 days, each from the first whole day at or after the start of one of the old ones: the same number of folds, 12,408 test visits instead of 40,995, training sides still expanding (50.1% to 94.6%). The longer windows had cost nothing measurable (14.40 against 14.42 MAE on the same weeks), and the exception to SPLIT-19 proposed for them was dropped; the day key is built in `_clean`, as the time column is the arrival rank (2026-11-05, Lennart, issue 8) | applied |
| SPLIT-14 | california_house_prices_2020 | `min_train_fraction=0.25` let the oldest window train on 25% of the rows; its windows now train on 50%, 67% and 83% (2026-10-21) | applied |
| SPLIT-14 (amended 2026-11-02, Andrej), SPLIT-11 | pricing_game_2016_french_fleet | three four-month windows of 2013 that all trained on 2011-2012 do not count as three windows; each window now trains on the periods closed before it starts (64%, 71%, 78% of the rows) (2026-11-02, Andrej) | applied |
| SPLIT-14, SPLIT-10 | wisconsin_local_government_property_insurance_fund | three expanding yearly windows (test 2008, 2009, 2010) in place of the member folds, whose leak test found the year's claim level shared across the split: the 2008 window trains on 2006-2007, 41% of the rows, below the floor, on the curator's call ("We found that grouped splits leak, so I would recommend to use three splits, one for each year of 2008, 2009, 2010"); unlike california_house_prices_2020, where a window below the floor was dropped, five policy years give no third window above it. No gap, an exception to SPLIT-10 that serves SPLIT-14, as pricing_game_2016_french_fleet (2026-11-02, Andrej) | exception |
| SPLIT-16 (TP-9) | seismic_bumps | 49 positives in the newest half, 0-5 per window: `Too Small`, no fallback to an IID split | applied |
| SPLIT-17 | coffee_rating_prediction | 26 monthly windows of 2-72 reviews doubled the confidence interval of a model comparison; 13 two-month windows hold 54-115 | applied |
| SPLIT-18 | climate_model_weather_forecasting | weather test windows of one to two weeks at most | applied |
| SPLIT-20, SPLIT-21 | aeolus | flights from 2023 on rather than all of 2016-2024, two-week windows with one of three in the holiday peak (2026-10-12, Lennart) | applied |
| SPLIT-20 | perth_house_prices | one-month windows every third month back from December 2020 (`step=3`) instead of nine contiguous months in 2020, so most windows fall outside the COVID months and the stale-record period; chosen from counts, not scores (2026-10-26, Lennart) | applied |
| SPLIT-20 | airqo_low_cost_air_quality_monitor_calibration_challenge | five monthly windows from October 2020 (`n_windows=5`) instead of the three dry-season months December 2020 to February 2021, so the test covers both seasons and October and November score all three sites (smallest train side 57.3%); the fact proposed for an exception, that only the newest season has all three sites, was false; Nakawa enters October with 63 hours of history, noted under USE-10; chosen from season and site coverage, not scores (2026-11-05, Lennart, issue 1) | applied |
| SPLIT-22 | seismic_bumps | the raw file order is the order of the mining shifts; kept as time | applied |
| SPLIT-23 | sat11_hand_algo_runtime | `context="all_rows"`: algorithm selection predicts the runtime of all 10 candidate algorithms on a new instance and runs the fastest, so a model sees all of an instance's rows | applied |
| SPLIT-23 | protein_model_quality_rf_pcp | `context="all_rows"`: CASP releases a target's server models at once and the researcher ranks them together; a context model scores 0.483 against 0.322 for a row-only one (2026-11-05, Lennart); huesken_sirna_efficacy reopened to follow | applied |
| SPLIT-23 | huesken_sirna_efficacy | `context="all_rows"`: a researcher designs and ranks a gene's candidate guides together; per-gene context adds nothing measurable here (LightGBM 0.6708 against 0.6699, paired SE 0.0025), unlike protein (+0.161), and the context follows the use case, not the gain (2026-11-05, Lennart) | applied |
| SPLIT-22 | california | the Kaggle id is the sale order; an index lookup sorted the rows by address, so the row-order time index is rebuilt after it | applied |
| SPLIT-24 | emscad | grouped on identical profile text or a poster-specific masked contact (4,441 groups); the first suggestion, a TF-IDF cosine cluster at 0.95 or more, was barred | applied |
| SPLIT-24 | in_vehicle_coupon_recommendation | consecutive blocks of identical person-level answers in the raw file order: 587 respondents | applied |
| SPLIT-24 | concrete_compressive_strength | a mix is its seven ingredient amounts, tested at several ages: 428 mixes behind 1,030 tests (2026-10-14) | applied |
| SPLIT-24 | airfoil_self_noise | a setup is one chord and one angle with all its speeds, one figure of the report (2026-10-20; before, a run of chord, angle and velocity, 2026-10-06) | applied |
| SPLIT-24, SPLIT-25 | maternal_health_risk | the first suggestion, a hash of the feature vector standing in for the unknown entity, was barred; the six collection sites are not in the file: retired | applied |
| SPLIT-25 | hazelnut_spread_contaminant_detection | re-scans of about ten set-ups, not recoverable: retired | applied |
| SPLIT-26 | superconductivity | key: element shares from `unique_m.csv`, which the features are computed from; a formula string would split one composition written two ways | applied |
| SPLIT-27 | mice_protein | LightGBM log loss 2.53 against a baseline of 2.07, while a random forest reached 1.12 | applied |
| SPLIT-28 | telemonitoring_parkinsons | R^2 -0.17 to -0.31 grouped against 0.75 IID; as warm start 6.33 against 6.48 for the carried-forward value; retired (2026-10-02) | applied |
| SPLIT-29, SPLIT-31 | sarcoma | IID by patient kept over a split by tissue source site: the site is weakly visible from the features (one site against the rest ROC AUC 0.70-0.75, 0.69-0.73 within dedifferentiated liposarcoma) and holding sites out raises a random forest's log loss (0.64 to 0.77 before the merge of MFS and UPS, 0.46 to 0.58 after), but a lab types the tumours of new patients and one site holds 101 of the 201 rows; the optimism is stated in `splits_comment`. The reason is the use case, not a null gap: in glioma_grading (retired 2026-10-26 on USE-1) the features did not predict the site and a split by site scored like a random one (2026-10-22, Lennart) | applied |
| Few groups (factor) | covertype | 3 wilderness areas: IID instead of grouped | applied |
| Few groups (factor) | heart_disease | 3 hospitals, leave one out kept: the source built its model in Cleveland and applied it at the other hospitals, no class drops out (51 or more of each per test fold), and 7 of 15 pairs of model families separate (4 to 5 under a random 10 x 3 split); SPLIT-1, SPLIT-4 and SPLIT-23 outweigh the factor (2026-10-27, Lennart) | applied |
| Few groups (factor) | huesken_sirna_efficacy | 30 genes, grouped by target gene kept (10 test genes, 648-942 test rows per fold): a new gene is the unit predicted for, and LightGBM beats the training mean on every split (0.1618 against 0.2024); not a general license for few groups, the signal across groups is measured (2026-11-04, Lennart) | applied |
| SPLIT-31 | amazon_employee_access, bank_marketing | IID kept: optimistic, but it matches how the task is framed; candidates for a grouped or temporal variant | applied |
| SPLIT-31 | infrared_thermography_temperature | IID kept over a measured year-to-year shift (a first-year calibration over-predicts the second year by 0.06-0.09 °C): the calibration is a function of the inputs that should not depend on the day, so no real signal across time; temporal is a candidate variant (2026-10-21, Lennart) | applied |
| SPLIT-31 | qsar_oral_toxicity | IID kept over related chemicals (random forest 0.882 IID, 0.842 by Butina clusters, 0.843 by reconstructed Murcko scaffolds, ranking unchanged); the scaffold-grouped variant on structures linked by row order stays a listed candidate, not built (2026-10-21, Lennart); superseded 2026-10-26 by the amendment below | applied |
| SPLIT-31 | drug_induced_autoimmunity_prediction | grouped on the Bemis-Murcko scaffold, ring-less drugs alone, the bare benzene ring one group (7% of the drugs): new candidates come from series not yet tested, as in the TDC ADMET benchmarks (2026-10-19, Lennart) | applied |
| SPLIT-31 | qsar_bioconcentration | the amendment: scaffold groups in place of IID, ring-less chemicals and the bare benzene ring (34%) alone; close training analogs of the test chemicals fall from 12.6% to 6.4% (2026-10-26, Lennart) | applied |
| SPLIT-31 | qsar_oral_toxicity | reopened under the amendment: every row has its own QSAR-ready structure since 2026-10-21, so the scaffold is exact; ring-less chemicals (23%) and the bare benzene ring (18%) alone; close training analogs fall from 24.7% to 16.3%, against 11.0% for the untested chemicals, so the fit stays approximate (2026-10-26, Lennart) | applied |
| SPLIT-31 | qsar_tid_11 | scaffold groups in place of IID: the file carries ChEMBL compound ids, and ChEMBL 17 (the release the data was drawn from) gives every one its structure; 21 ring-less compounds alone, the bare benzene ring 2%; close training analogs fall from 79.7% to 59.2%, untuned LightGBM RMSE 0.794 to 0.920; the features stay the source's fingerprint (2026-11-01, Lennart) | applied |

## In Data Foundry

The declarations (`Grouping`, `Temporal`, `TemporalSplits`, the gap and horizon fields), the default 3-fold protocol,
the row budget and the `_1m` versions: [definitions.md](../../knowledge-data-foundry/references/definitions.md),
"Splits". The probes that test grouping and hidden groups:
[checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md).
