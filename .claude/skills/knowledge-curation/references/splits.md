# IID, grouped and temporal splits

Whether a dataset is IID or non-IID is decided by the appropriate train-test split: the split that most closely
mirrors the real-world application ([use_case.md](use_case.md)). Background from the TabArena paper (Section 2,
Appendix B.3), extended by the curators' decisions.

## The same data, two applications

Alice predicts whether past transactions were fraudulent, for follow-up investigations: a random (IID) split fits.
Bob predicts whether new transactions are fraudulent, to stop fraud as it happens: a temporal split fits, because it
simulates unseen future transactions. With a random split Bob would overrate models that exploit temporal leakage;
with a temporal split Alice would underrate them. The split depends on the application, and the curator picks the one
the dataset's application needs.

## The regimes

* IID: the test rows follow no particular structure; a random hold-out is right.
* Temporal: a time index exists, and the test rows come strictly after the training rows (predicting the future).
* Grouped: a group index exists, and all rows of a group stay on one side, so the model is tested on unseen entities.
  The label is either one per group (is this customer fraudulent, from their transactions) or one per row (the
  outcome of each visit of a patient unseen in training). The source's use case, cited, also decides what one
  prediction is (a row, or a whole group: replicates averaged, any instance positive, the latest row, the best of
  several candidates) and what is known about a new group when predicting; the label structure alone does not.

In practice a non-IID task is grouped or temporal (Lennart, 2026-10-12); we have met no third kind. A task is one or
the other, never both: a temporal split does not remove group structure, and a grouped split does not make a task
time-invariant, but the split decides which dependency the test measures. An order inside groups (the latest
statement of each customer) is part of the grouping.

With only a few groups, a grouped split is a domain-shift test between them rather than prediction for unseen
entities; that is its own decision (covertype: 3 wilderness areas, IID instead).

## Forecasting is out, temporal tasks are in

Time-series forecasting (future values of a series: demand, sales or a price over a horizon) needs other assumptions
and another protocol and has its own community, so it is excluded. A fixed predictive task that only needs a temporal
split (a delivery time, a default, a sale price) is in scope.

A missing or hidden timestamp does not make a task IID. The time index is often absent: dropped by an uploader, never
shipped, or only implied by how the data was collected (readings logged over months, every feature and the target
contemporaneous). When the setup is values unfolding over time from a stream of signals, it is temporal or
forecasting whether or not a date column survived. `combined_cycle_power_plant` has no timestamp and looks like IID
sensor regression, but it is a six-year hourly stream predicting the plant's output: forecasting, `No`.

When a task is temporal in nature but the release has no dates at all (one extract, the status at that moment
standing in for a forecast), it ships as IID, tagged as forced IID from temporal, with the cost of the missing time
axis measured where the data allows (account_debt_south_africa: held out by file block, ROC AUC falls from 0.877 to
0.843 and 0.786; Lennart, 2026-10-12). Say what the timestamp would change and that it should be recovered if a
later release has it.

The split a paper or a dataset page prescribes is a claim to check against the task design, not a fact. Authors often
pick a random split on data that is really temporal (`appliances_energy_prediction`: 10-minute readings over 4.5
months, evaluated with a random split; it is forecasting, `No`). Check a claim about a split against the data as well:
kick's comment called the Kaggle split grouped by auction location, yet 78.9% of its test rows are at a location also
in train. A benchmark's non-IID label can also be wrong for our framing, in either direction.

## Temporal tasks

* The horizon is a human judgment from the source: how far ahead the actor predicts ("managers predict sales up to six
  weeks in advance"), the competition's own test window, the refit cadence. Choose the test windows to match it and
  write the reasoning down.
* Check that every feature existed at the prediction time of its row ([leak_checks.md](leak_checks.md)).
* Look for grouped structure inside the temporal task: repeated observations of one entity over time (transactions of
  one customer). An entity that recurs across the cutoff is part of the task when the model predicts for known
  entities, and a question when the use case is a new entity ([use_case.md](use_case.md)).
* Train on everything before the window (an expanding train side). The first split is the newest window, with the
  most training data and the most representative; the others walk back in time.

### How many windows

Roll the windows back from the newest data: as many windows as an IID or grouped task of that size would get folds,
never fewer than 3, and never a window whose train side holds less than 50% of the data, which would be too unlike the
real application. Then check that the windows are still meaningful:

* Count the minority-class rows (or the target's spread) per window. If the windows hold a handful of positives or
  none, the scores are noise and the dataset is too small for a temporal task (`seismic_bumps`: 49 positives in the
  newest half, 0-5 per window). Do not fall back to an IID split for a non-stationary sequence; it is `Too Small`.
* Widen windows that get too small. Finer windows add no test rows (the 50% floor fixes the test pool); they cut it
  into smaller, noisier pieces. Below about 50 test rows per window, use wider windows and fewer splits
  (`coffee_rating_prediction`: 26 monthly windows of 2-72 reviews doubled the confidence interval of a model
  comparison; 13 two-month windows hold 54-115).
* Short-lived quantities need short windows: weather test windows of one to two weeks at most
  (climate_model_weather_forecasting).

### Labels that arrive late, and the gap

When a label is known only some time after its row (a delivery time, a permit's processing time, an outcome after a
follow-up), a model refit at a window's start knows only the rows whose label had arrived. Simulate that: train on the
rows whose outcome is known by the window's start, with a gap of about the label's delay between train and test
(brazilian_ecommerce: one month; sf_permit_time: 6 months, since a 1-month gap still censored the slow permits).
Without the gap the newest training rows are the fast ones, and a model that sees the time as a number is biased
(brazilian_ecommerce: R^2 0.353 with the gap, -0.054 without; Lennart, 2026-10-15). The gap is part of the task and is
stated with it. A planning gap the use case has (a forecast made a day ahead) is a gap too.

A training row whose label is not yet known at the prediction point must not be in train. hotel_booking_demand kept
bookings arriving after the prediction date that were already cancelled (100% positive), so the model learned "future
arrival means cancelled"; filtering on the status date does not remove the shortcut, filtering on the arrival date
does.

### The training history

When the source defines the split (a competition's or a paper's official periods), follow it. Otherwise decide what
the train side holds from the use case: the history a model refit at each window would train on. Read what the
source's authors trained on, check the history for breaks (COVID-19, a change of rules or of the data collection),
keep a recent stretch with at least one full season before the newest window, and say why. Check whether the newest
windows fall in an atypical season and widen them so most do not. Decide neither from a comparison over a few test
windows: such a comparison changes with the kind of window, so it measures the windows, not the design (aeolus: flights
from 2023 on rather than all of 2016-2024, two-week windows with one of three in the holiday peak; Lennart, 2026-10-12).

### Row order as time

The raw file order can be the time order without a timestamp (seismic_bumps' mining shifts; california's Kaggle id is
the sale order). Keep it. A deduplication, merge or lookup can reorder rows (an index lookup sorted california by
address): rebuild a row-order time index after such steps and check it against the date.

## Grouped tasks

* Group on a true group id, or on one constructed exactly from the data: identical profile text or a poster-specific
  masked contact (emscad, 4,441 groups), consecutive blocks of identical person-level answers in the raw file order
  (in_vehicle_coupon_recommendation, 587 respondents), identical values in the columns that define the entity
  (concrete_compressive_strength: a mix is its seven ingredient amounts, tested at several ages; airfoil_self_noise: a
  run is one chord, angle and velocity). Never a similarity-threshold cluster (the first emscad suggestion, TF-IDF
  cosine at least 0.95) and never a hash of the feature vector standing in for an unknown entity (the first
  maternal_health_risk suggestion).
* When the real groups matter and cannot be recovered, retire the dataset rather than group on a guess, and note that
  the authors could be asked for the group labels (maternal_health_risk: six collection sites not in the file;
  hazelnut_spread_contaminant_detection: re-scans of about ten set-ups).
* Decide cold start or warm start from the use case before grouping ([use_case.md](use_case.md)).
* Before calling a small grouped task unlearnable, judge it with several model families scored per group, against the
  class-share baseline, with a permutation test across groups. One untuned gradient-boosting run is not enough: on
  unseen groups its probabilities are overconfident (mice_protein: LightGBM log loss 2.53 against a baseline of 2.07,
  while a random forest reached 1.12). A regression task whose models all score below the mean on unseen groups has no
  signal across groups (telemonitoring_parkinsons: R^2 -0.17 to -0.31 grouped against 0.75 IID); then the use case has
  to allow known groups, or the dataset goes. Before recasting it as warm start, compare a model with the group's
  known value carried forward (telemonitoring: 6.33 against 6.48 for that baseline; retired 2026-10-02).
* With few groups, real signal is not enough: count the groups of each class in total and per test fold
  ([task_probes.md](task_probes.md), rule 5).

## Hidden groups in an IID task

An IID split is wrong when many rows share an entity that new data would not have and the entity carries the label: a
random split then rewards recognising the entity.

* A probe hit is a question (Lennart, 2026-10-06). Re-split only when the context says the rows share an entity new
  data would not have (the source calls the column an id, or the use case predicts for new entities), or when the
  evidence is very strong. Holding out the values of any useful feature opens a gap, so the gap never decides: a
  manager, a soil type or a fund category is known for every new row.
* The split follows what the task does in reality, not the size of the gap. If the deployed model predicts for an
  entity new data would not contain (a material nobody has measured, a new respondent), the test entities must be
  new, even when a random split costs little (superconductivity: at most 0.009 R^2, grouped by composition). If new
  rows keep having the value, the column is a feature and the split stays.
* Take the group key from the source's own data, at the resolution the features see (superconductivity: element
  shares from `unique_m.csv`, which the features are computed from; a formula string would split one composition
  written two ways). Keep the source's rows: deduplicating with averaged targets is a different dataset.
* Rows identical in every column but one are one entity at another age, dose, time or frequency (concrete: 428 mixes
  behind 1,030 tests). When that key is what one row's entity is, group on it; when new rows keep the key, it is a
  feature.
* Over related entities, IID can match how a task is framed even when optimistic (amazon_employee_access,
  bank_marketing): candidates for a grouped or temporal variant, not fixes.

The cases and the probe's calibration are in [task_probes.md](task_probes.md), "Hidden groups".

## In Data Foundry

The declarations (`Grouping`, `Temporal`, `TemporalSplits`, the gap and horizon fields), the default 3-fold protocol,
the row budget and the `_1m` versions: [definitions.md](../../knowledge-data-foundry/references/definitions.md),
"Splits". The probes that test grouping and hidden groups:
[checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md).
