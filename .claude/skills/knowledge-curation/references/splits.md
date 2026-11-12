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
**SPLIT-33 (Should).** An IID or grouped task gets repeated 3-fold cross-validation, with 20, 10, 3 or 1 repeats as its
train side holds fewer than 500, 2,500 or 250,000 units, or more, at any size of the frame. The unit is what the
metric scores: the group when the metric scores per group and the split holds each such group out whole (a PAR10 per
instance over one row per instance and solver, the instances held out or inside held-out classes), else the group
when each group has one label, else the row. A metric group the split cuts across folds (a survey year over held-out
stations, any group under an IID split) is scored on part of its rows in every fold, so the rows count. Why: the noise
of a score follows the number of units scored, so a task gets the same splits whatever the layout of its table.
Cases: sat11_hand_algo_runtime, protein_model_quality_rf_pcp, wadden_sea_sibes_macoma_abundance.

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
recovered if a later release has it. A forced split, grouped or IID, gets a leak test across the split and the
leak probes: does a row share its outcome, its unit's outcome or its period's outcome with the other side, is there
a hidden group, an order dependence. A leak found is weighed case by case like any other: removed where it can be,
otherwise the task may still ship as an approximate fit with the leak measured in the notes. Being forced alone never
makes a dataset `No`, and a dataset stays tagged as forced whatever the test finds, since its source's regime was
another. (Lennart, 2026-10-12; amended 2026-10-21, Lennart: one stock month, from
mobile_churn and the churn snapshots; too few periods, from nba_players_2016_2019,
open_university_learning_analytics_dataset and distribution_transformers_at_cauca_department; amended 2026-11-02,
Andrej, on the insurance tables of the zero-inflated batch: a leak test across a forced split; reworded 2026-11-05,
Lennart: the test informs a case-by-case call and the forced tag stays.) Cases:
account_debt_south_africa, mobile_churn, open_university_learning_analytics_dataset (nba_players_2016_2019 was
retired on 2026-10-26 on its use case, not its split).

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
windows to match it and write the reasoning down. The curator signs off on the horizon and the test windows of every
new temporal dataset, as on its metric (Lennart, 2026-11-10: "I am not even sure there is a good reason for some of
the forecast horizons here").

**SPLIT-13 (Should).** Look for grouped structure inside a temporal task: repeated observations of one entity over
time (transactions of one customer). An entity that recurs across the cutoff is part of the task when the model
predicts for known entities, and a question when the use case is a new entity (USE-10, [use_case.md](use_case.md)).

### How many windows

**SPLIT-14 (Must; amended 2026-11-08 and 2026-11-11, Lennart).** A temporal task has at least 3 windows. The newest
window and at least one other train on at least 50% of the data; further windows may train on less, down to 30% of the
data, and at most as many windows train on less than 50% as on 50% or more. A window under 30% needs a reason the
curator accepts for that dataset. Every window under 50% needs the curator's sign-off: the review raises it as an issue,
`dataset check` warns (`splits_train_under_half`, and `splits_train_under_floor` under 30%; a broken core is the error
`splits_floor_core`), and the definition accepts the warning only once the record carries the curator's CC line, never
on the AI's word (Lennart, 2026-11-11). The splits comment names every window under 50% and its train share; no model
score is required for it. Why: a much smaller train side is too unlike the real application, but in every floor case of
the reviews of 2026-11-10 and 2026-11-11 at least two windows already trained on 50% or more, and the windows below them
added years, seasons, events or test rows the newest windows lack (Lennart, 2026-11-11: "we very much noticed that the
floor can be below 50% to get better/more test windows quite frequently ... In some cases we can also go lower"). A flat
lower floor would not do: at 40% mercedes_benz_greener_manufacturing (31.5%) and ieee_fraud_detection (38.9%) would
still lose windows the curator kept. A task that cannot meet it ships under SPLIT-8 (Lennart, 2026-10-21). Each window
has its own train side: windows that share one train side test one model on several test periods, which is one
evaluation, not several. As time moves on, a refit sees the data that arrived since, so each window trains on what is
known before it starts (Andrej, 2026-11-02; reframed 2026-11-05, Lennart). The amendment of 2026-11-08 (one older window
at 40% when most test entities recur; Lennart: "the task is too good to remove because of the 50% floor") is replaced by
the two tiers since 2026-11-11: its condition of recurring entities and its duty to report a model's score lapse.

**SPLIT-15 (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and Andrej).** The newest
window is always a test window: it is the deployment period. The other windows are the curator's choice, per dataset,
argued from the use case: which periods a deployed model must handle (other years, seasons, holidays, events, a
change of rules or of the data collection). The evidence is statistics of the data, never a model's score: the
candidate windows of the declared length and gap with their months and weekdays, their rows and train share, the
target's distribution, and how far the features drift from the train side (`dataset windows <name>`,
[definitions.md](../../knowledge-data-foundry/references/definitions.md), "Choosing the test windows"). Prefer windows
in other years, then other seasons, then other months, weeks or days, over the windows just before the newest
(Andrej, 2026-11-10). Walking back from the newest is one choice among others and needs its reason too, such as a
history too short for others, or a use case that only cares about the weeks after a refit. Every choice stays above
SPLIT-14's floor; the length and the gap come from SPLIT-12; as many windows as an IID or grouped task of that size
would get folds, then check that they are still meaningful (SPLIT-16 to SPLIT-18). The splits comment names the
windows, the reasons and the numbers they rest on. Why: on aeolus, climate_model and delivery_eta the newest three
windows ranked a model pair the other way round than the whole eligible history did, and three windows spread over it
cut that error 5 to 15 times, while three windows drawn at random did worse than three spread evenly (closed PR #69).

**SPLIT-16 (Must).** Do not fall back to an IID split for a non-stationary sequence whose windows hold too few
positives. Counting the positives per window and the `Too Small` verdict are TP-9 ([task_probes.md](task_probes.md)).
Marker: `Too Small`. Cases: seismic_bumps.

**SPLIT-17 (Should).** Widen windows that get too small: below about 50 test rows per window, use wider windows and
fewer splits. Why: finer windows add no test rows (SPLIT-14's floor fixes the test pool); they cut it into
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
concrete_compressive_strength, airfoil_self_noise, maternal_health_risk, frempl_french_motor_personal_line.

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

**SPLIT-31 (Should).** Over related entities, IID can match how a task is framed even when it is optimistic: such a task
is a candidate for a grouped or temporal variant, not a fix. Cases: amazon_employee_access (bank_marketing until
2026-11-08, when it was split by time). Molecules are the exception (amended 2026-10-26, Lennart, on
qsar_bioconcentration: "in other cases, we also moved towards a scaffold split as is often correct for chemicals"): a
molecule dataset whose rows carry exact structures groups on the Bemis-Murcko scaffold, as a new chemical under
assessment often comes from a series not yet measured. A molecule without a ring is a group of its own, and so is each
molecule of a scaffold that holds more than a tenth of the molecules, which is no series and would leave folds of very
unequal size (`scaffold_groups` in `data_foundry.v2.chemistry`). Cases: drug_induced_autoimmunity_prediction,
qsar_bioconcentration, qsar_oral_toxicity, qsar_tid_11.

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
| SPLIT-8 | fremtpl2 | no policy dates; the blocks read as stacked periods with linked IDpols, but both the periods and the links are inferred, not the source's key (SPLIT-24), unlike nba and open_university, which group by a recorded entity: IID, `ForcedIIDFromTemporal`, because prior work uses a random hold-out or a split grouped on identical rating factors and none links records across years (2026-11-04 and 2026-11-05, Lennart; the size of a gap decides nothing, SPLIT-4, SPLIT-30). On 2026-11-08 (Lennart, its issue 11) the random split stays with a note rather than folds grouped on identical rating factors: one 19-row rating profile with 72 claims in 3.63 years makes the whole IID-against-grouped gap (94-102% of 0.0007 to 0.0017), 19 rows of 677,991 are not many (SPLIT-29), and LightGBM ranks ahead of a Poisson GLM under every split | applied |
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
| SPLIT-10 | ames_housing, perth_house_prices | proposed amendment, due at the third exception of this reason (principles.md, "Exceptions and amendments"): "No gap is needed when the label's delay is shorter than the resolution of the time column (sales dated by month) and the newest period shows no selection by the outcome (its mean residual within the other windows' range)." Both exceptions rest on these two facts; alfa_battle_2_0_task_2 and lending_club depart for another reason (SPLIT-14's floor) and do not count (proposed 2026-10-26 from the consistency check on ames_housing; open for Lennart) (settled by the amendment of 2026-11-04, Lennart) | applied |
| SPLIT-10 | spanish_homeowners_motor_insurance_2010_2014 | no gap for late-reported claims: the panel is yearly and a one-year gap leaves the 2012 window 33% of the rows, below SPLIT-14's floor; hiding 30 or 90 days of the newest year's claims moves the mean Gini from 0.219 to 0.226 and 0.203, within noise. Serves SPLIT-14 (2026-11-02, Andrej; row added 2026-11-06) | exception |
| SPLIT-10 | wisconsin_local_government_property_insurance_fund | exception (2026-11-08, Lennart): no gap; every policy year ships with its final claim amounts, so no label is selected by the release end, and a one-year gap would put two of the three windows below the floor; serves SPLIT-14 as amended on this fund | exception |
| SPLIT-12 | house_sales, perth_house_prices, ames_housing, zillow_prize, melbourne_housing_market | no window length for the whole family: each keeps the horizon of its own source or refit cadence (three weeks; one month, spaced; two months; one month after a one-month gap; three weekly sheets), since "different task might forecast differently long" and "we dont need to force the same split" (2026-10-21, Lennart) | applied |
| SPLIT-12, SPLIT-19 | medical_facility_operational_data | the source's horizon followed: Crowley et al. (2020) train on six months and test on "a further consecutive two weeks", so nine 14-day windows replace nine equal-count windows of 42-53 days, each from the first whole day at or after the start of one of the old ones: the same number of folds, 12,408 test visits instead of 40,995, training sides still expanding (50.1% to 94.6%). The longer windows had cost nothing measurable (14.40 against 14.42 MAE on the same weeks), and the exception to SPLIT-19 proposed for them was dropped; the day key is built in `_clean`, as the time column is the arrival rank (2026-11-05, Lennart, issue 8) | applied |
| SPLIT-14 | california_house_prices_2020 | `min_train_fraction=0.25` let the oldest window train on 25% of the rows; its windows now train on 50%, 67% and 83% (2026-10-21) | applied |
| SPLIT-14 (amended 2026-11-08, Lennart) | wisconsin_local_government_property_insurance_fund | three yearly windows, test 2008, 2009 and 2010 on 40.6%, 60.6% and 80.3% of the rows: two windows above the floor, 97.6% to 98.8% of each test year's members in earlier years, and member folds leaked the year's claim level (pooled ROC AUC +0.010 to +0.012; within a year +0.031 to +0.036 Gini for a GLM); the 2008 window changes the order of the two simplest predictors (coverage alone 0.368 against a GLM's 0.312 on the valid windows, 0.251 against 0.291 with 2008), stated in the notes | applied |
| SPLIT-14 (amended 2026-11-08, Lennart) | ashrae_great_energy_predictor_iii_1m | three four-month windows tile 2017 (2026-11-10, Lennart, issue 1, A), test September-December, May-August and January-April 2017 on 83.0%, 66.0% and 49.47% of the rows: two windows above the floor, every test meter's building in training, and folds by entity would test unseen buildings; LightGBM's RMSLE is 1.277 on the valid windows and 1.256 on all three (1.208 and 1.221 without the absolute date features), so the oldest window, which scores like the newest, moves the mean by about 0.02, stated in the notes | applied |
| SPLIT-14 (amended 2026-11-11, Lennart) | anes_voting_2026 | nine one-election windows 1996-2024 (2026-11-11, Lennart, issue 1, A): five train on 51.4% to 89.8%, the four oldest on 49.2%, 46.4%, 43.2% and 40.0%; nine is the count a random split of this size gets | applied |
| SPLIT-14 (amended 2026-11-11, Lennart) | ieee_fraud_detection | three one-month windows after the competition's one-month gap (2026-11-11, Lennart, issue 1, A): May and April on 70.7% and 53.5%, March on 38.9%; a February window would train on December only (23.3%) | applied |
| SPLIT-14 (amended 2026-11-11, Lennart) | maps_router_eta_1m | the three newest weeks of a 40-day release (2026-11-11, Lennart, issue 1, A, after the consistency check of 2026-11-10): 79.9% and 62.3%, the oldest on 44.8% of all routes; anonymous routes, so the condition of recurring entities of 2026-11-08 would not have held | applied |
| SPLIT-14 (amended 2026-11-11, Lennart) | mercedes_benz_greener_manufacturing | nine windows of 320 cars in ID order (2026-11-11, Lennart, issue 1, A): six train on 54.3% to 92.4%, three on 46.7%, 39.1% and 31.5%; 2,880 test cars against 2,097 at 233 cars | applied |
| SPLIT-14 (amended 2026-11-02, Andrej), SPLIT-8 | pricing_game_2016_french_fleet | forced grouped by contract (`fleet_group`: the contract, the three that share a registration joined on 2026-11-08, issue 9; 3 x 3 folds over 2011-2013, `ForcedGroupedFromTemporal`) in place of the windows (2026-11-08, Lennart, issue 6 (b): "Forced by contract"), superseding Andrej's expanding four-month windows (2026-11-02) and D11's three windows of 2013 on one training side (2026-11-06): rows are cut at 31 December and the claims carry no dates, so the windows are whole years and 2013 on 2011-2012 is the one valid window (2012 on 2011 trains on 30.4%); windows inside 2013 either share one training side, one evaluation, or admit the 2013 periods by their realized end (LEAK-41); the leak test across the contract folds passes (the test year's own training periods gain -0.33 and -0.43 on the declared metric, -0.009 and -0.001 Gini, against wisconsin's +0.113), and on the 2013 periods the forced split scores no better than the valid window (+0.16, SD 0.45; a new fleet's cold start 1.13); the exception to SPLIT-10 lapsed with the windows | applied |
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
| SPLIT-24 | frempl_french_motor_personal_line | no policy id: a policy component joins records where one may continue another (starting the day the other ends, ages advanced), within a file and across the five sample files (Andrej, 2026-11-03), widened to a successor with one profile column changed and no counter lower (Lennart, 2026-11-08): 61,091 components; the chance links (about 1% across files, about two thirds of the one-column links) only join two policies, the stricter side | applied |
| SPLIT-24 | pricing_game_2016_french_fleet | the group is the contract with the contracts that share a vehicle's registration joined (connected components of the source's contract and registration ids, an exact key): registration 32348 has one period under each of contracts 6168, 6169 and 6170, the only registration under more than one contract, so 18,035 groups of 18,037 contracts; a client guessed from neighbouring contract numbers and equal fleet classes was not used, a guess with no shared claim or outcome behind it (Lennart, 2026-11-08, issue 9 (B)) | applied |
| SPLIT-24, SPLIT-25 | maternal_health_risk | the first suggestion, a hash of the feature vector standing in for the unknown entity, was barred; the six collection sites are not in the file: retired | applied |
| SPLIT-25 | hazelnut_spread_contaminant_detection | re-scans of about ten set-ups, not recoverable: retired | applied |
| SPLIT-26 | superconductivity | key: element shares from `unique_m.csv`, which the features are computed from; a formula string would split one composition written two ways | applied |
| SPLIT-27 | mice_protein | LightGBM log loss 2.53 against a baseline of 2.07, while a random forest reached 1.12 | applied |
| SPLIT-28 | telemonitoring_parkinsons | R^2 -0.17 to -0.31 grouped against 0.75 IID; as warm start 6.33 against 6.48 for the carried-forward value; retired (2026-10-02) | applied |
| SPLIT-29, SPLIT-31 | sarcoma | IID by patient kept over a split by tissue source site: the site is weakly visible from the features (one site against the rest ROC AUC 0.70-0.75, 0.69-0.73 within dedifferentiated liposarcoma) and holding sites out raises a random forest's log loss (0.64 to 0.77 before the merge of MFS and UPS, 0.46 to 0.58 after), but a lab types the tumours of new patients and one site holds 101 of the 201 rows; the optimism is stated in `splits_comment`. The reason is the use case, not a null gap: in glioma_grading (retired 2026-10-26 on USE-1) the features did not predict the site and a split by site scored like a random one (2026-10-22, Lennart) | applied |
| Few groups (factor) | covertype | 3 wilderness areas: IID instead of grouped | applied |
| Few groups (factor) | heart_disease | 3 hospitals, leave one out kept: the source built its model in Cleveland and applied it at the other hospitals, no class drops out (51 or more of each per test fold), and 7 of 15 pairs of model families separate (4 to 5 under a random 10 x 3 split); SPLIT-1, SPLIT-4 and SPLIT-23 outweigh the factor (2026-10-27, Lennart) | applied |
| Few groups (factor) | huesken_sirna_efficacy | 30 genes, grouped by target gene kept (10 test genes, 648-942 test rows per fold): a new gene is the unit predicted for, and LightGBM beats the training mean on every split (0.1618 against 0.2024); not a general license for few groups, the signal across groups is measured (2026-11-04, Lennart) | applied |
| SPLIT-31 | amazon_employee_access | IID kept: optimistic, but it matches how the task is framed; a candidate for a grouped or temporal variant (bank_marketing left this row on 2026-11-08: the row below) | applied |
| SPLIT-1, SPLIT-19, SPLIT-22, LEAK-17 | bank_marketing | split by time in place of SPLIT-31's IID keep: five expanding windows of 4,521 records on the file's date order (UCI: "ordered by date"; the year rebuilt where the month wraps, the dates checked against the order, the file position the time key), training on 50% to 90%. What sets it apart from amazon_employee_access: the source scores on time-ordered windows, the date order is recoverable, a client's later record gave an earlier one's label away across the random split (+0.020 ROC AUC to a lookup) and the subscription rate moves tenfold (5.1% in 2008, 51.6% in 2010). The windows score ROC AUC 0.586 on average (LightGBM; 0.614 logistic regression) against 0.76 at random, and a weak score under the right split keeps no wrong one (forest_fires) (2026-11-08, Lennart, issue 1) | applied |
| SPLIT-31 | infrared_thermography_temperature | IID kept over a measured year-to-year shift (a first-year calibration over-predicts the second year by 0.06-0.09 °C): the calibration is a function of the inputs that should not depend on the day, so no real signal across time; temporal is a candidate variant (2026-10-21, Lennart) | applied |
| SPLIT-31 | qsar_oral_toxicity | IID kept over related chemicals (random forest 0.882 IID, 0.842 by Butina clusters, 0.843 by reconstructed Murcko scaffolds, ranking unchanged); the scaffold-grouped variant on structures linked by row order stays a listed candidate, not built (2026-10-21, Lennart); superseded 2026-10-26 by the amendment below | applied |
| SPLIT-31 | drug_induced_autoimmunity_prediction | grouped on the Bemis-Murcko scaffold, ring-less drugs alone, the bare benzene ring one group (7% of the drugs): new candidates come from series not yet tested, as in the TDC ADMET benchmarks (2026-10-19, Lennart) | applied |
| SPLIT-31 | qsar_bioconcentration | the amendment: scaffold groups in place of IID, ring-less chemicals and the bare benzene ring (34%) alone; close training analogs of the test chemicals fall from 12.6% to 6.4% (2026-10-26, Lennart) | applied |
| SPLIT-31 | qsar_oral_toxicity | reopened under the amendment: every row has its own QSAR-ready structure since 2026-10-21, so the scaffold is exact; ring-less chemicals (23%) and the bare benzene ring (18%) alone; close training analogs fall from 24.7% to 16.3%, against 11.0% for the untested chemicals, so the fit stays approximate (2026-10-26, Lennart) | applied |
| SPLIT-31 | qsar_tid_11 | scaffold groups in place of IID: the file carries ChEMBL compound ids, and ChEMBL 17 (the release the data was drawn from) gives every one its structure; 21 ring-less compounds alone, the bare benzene ring 2%; close training analogs fall from 79.7% to 59.2%, untuned LightGBM RMSE 0.794 to 0.920; the features stay the source's fingerprint (2026-11-01, Lennart) | applied |
| SPLIT-24, SPLIT-26, SPLIT-4 | boreal_postfire_lichen_biomass | one group per Saskatchewan plot kept (the names carry no burn key), with the measured effect in the notes, over a burn key joined from an outside source (Canada's NFDB and NBAC fire polygons, point in polygon on the plot's fire year): tried on 2026-11-09 and taken back on 2026-11-10 (Andrej: "Back to A, with the note"). 94 of 190 SK plots lay inside a mapped burn of their year (none of the 66 dated before 1945); burn-mates in training flattered the SK RMSE by about 5 kg/ha against a fold-draw SE of about 40, and no model changed rank; the join cost 2 GB of maps, a shapefile reader and a build tied to NFDB's current version only | applied |
| SPLIT-33 | sat11_hand_algo_runtime | one row per instance and solver, scored by PAR10 per instance, the instances held out: the repeats follow the 184 instances (20 x 3), not the 1,840 runs (10 x 3) | proposed |
| SPLIT-33 | protein_model_quality_rf_pcp, huesken_sirna_efficacy, sepsis_prediction_1m | scored per protein, per gene and per patient, each held out whole: 445 proteins and 30 genes give 20 x 3 (the rows 3 x 3 and 10 x 3), 40,336 patients 3 x 3 (the 1.55M rows 1 x 3) | proposed |
| SPLIT-33 | wadden_sea_sibes_macoma_abundance | scored per survey year (15) over a split by station: every test fold holds part of every year, about 1,300 stations a year, so the years do not set the repeats; the rows do (59,044: 3 x 3, not 20 x 3) | proposed |

## In Data Foundry

The declarations (`Grouping`, `Temporal`, `TemporalSplits`, the gap and horizon fields), the default 3-fold protocol,
the row budget and the `_1m` versions: [definitions.md](../../knowledge-data-foundry/references/definitions.md),
"Splits". The probes that test grouping and hidden groups:
[checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md).
