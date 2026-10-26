# Is the task worth benchmarking

Part 6 of the curation rules, under P6 (worth benchmarking: not trivial, not too small, every fold scorable) in
[principles.md](principles.md). The rules of earlier parts win over this file's rules in a conflict; within this file a
rule wins over the rules below it of the same strength. How to weigh, exceptions and amendments:
[principles.md](principles.md).

Whether a curated task is empty, trivial, too small, or worth benchmarking, and how to answer the flags of the task
probes (dummy baselines against untuned model families on the task's own splits). The rules come from the review of
the datasets the probes flagged in the TabArena v0.2 build (from 2026-10-05; the evidence is in each record's dated
comment) and from the reviews since. The markers they set (`Trivial`, `Too Small`) are listed in
[selection.md](selection.md), "Decision markers".

Rule N is TP-N; definitions cite them as task_probes.md rule N, so keep the numbers. An ID is a name and the position
sets the precedence: TP-9 stands under TP-5, the rule it applies to temporal tasks. After each decision on a flagged
dataset, add a row to the Cases table (and a rule when the case changes how a flag is read), so the next decision
starts from the precedent.

## Rules

**TP-1 (Must).** A flag is a question, not a verdict ([evidence.md](evidence.md), EV-3). The probes fit untuned
models, so check every flag against the benchmark's tuned methods before acting on it (Methods, "How to check a
flag"). Cases: clock_protein_toxicity, asp_potassco_classification, consumer_complaints_1m.

**TP-2 (Should).** A small but real signal is no reason to retire, and neither is a cutoff on the best skill. Retire,
fix or keep a task for a concrete reason found in the task itself; until one is found, the task stays. Cases:
forest_fires (R² 0.013, but TabPFN-3.5 beats the mean on 26 of 32 folds) is a valid task.

**TP-3 (Must).** If tuned methods spread, keep the dataset. No further discussion is needed (a rule of an earlier
part still wins). Cases: gallstone_disease, electric_motor_temperature_prediction, hr_analytics.

**TP-4 (Must).** `Trivial` needs proof. Read what the dominant feature means first: the natural core of a task (a
listed price for a sale price, age for survival) is expected to dominate. Then test it: the raw feature, chosen on
each split's training side, has to match or beat the methods fold by fold. Marker: `Trivial`. Cases: fitness_club
(yes, retired); sepsis_survival, california (no, kept).

**TP-5 (Must).** `Too Small` means a handful of units of a class, per test fold and in total, counted in the unit the
task is scored on (parkinsons: 8 healthy people, 2-3 per fold; retired). A small dataset as such is a tiny-data task
like the others (musk: 102 molecules, 13 musk per fold; kept). In a temporal task a test fold is a window: TP-9.
Marker: `Too Small`.

**TP-9 (Must; narrows TP-5).** Count the minority-class rows (or the target's spread) per test window of a temporal
task. When the windows hold a handful of positives or none, the scores are noise and the dataset is `Too Small` for
a temporal task. Do not fall back to an IID split for a non-stationary sequence (SPLIT-16); wider windows are the
alternative to try (SPLIT-17; [splits.md](splits.md), "How many windows"). Marker: `Too Small`. Cases: seismic_bumps (49
positives in the newest half, 0-5 per window; Lennart, 2026-09-30).

**TP-6 (Must; amended 2026-10-21, Lennart).** Keep two questions apart: is the task valid, and is it the best
version? A valid task stays. A better version the source itself defines (a stage it describes) replaces the current
one: eryhemato before the biopsy (features from a later stage: USE-4 in [use_case.md](use_case.md)). A fix of our own
invention (dropping near-ties, a label merge made from names) is not a better version. Which metric scores the task,
and how the data is matched to it, is [metrics.md](metrics.md) (MET).

**TP-7 (Must).** When the definition builds the target itself (merged or dropped classes), use an established
convention, test each candidate (classes per test fold after dropping duplicates, signal, how rule-like the label
is), and run the leak probes on the source's labels too (LEAK-4, [leak_checks.md](leak_checks.md)). Cases:
audiology_diagnosis.

**TP-8 (Must; narrows TP-5).** A short class in a multiclass task is a question about that class, not about the
task. `Too Small` applies when the short classes carry a large share of the score (alvin: the 8 rows of the rarest
classes give 51-54% of a window's log loss) or a test fold holds only a handful of units in all (parkinsons). A rare
class of the source's own labels whose rows carry about their share of the loss stays (mic: 0.7% of the test rows,
4.8% of a random forest's log loss). A class that a grouped split leaves out of a fold because few groups hold it is
not a small class (force_2020: Halite, 14,711 rows in 4 wells). Marker: `Too Small`.

**TP-10 (Must; amended 2026-10-22, Lennart, on g_research_crypto_forecasting, and 2026-10-26, on rain_in_australia).** A panel with one series per entity
(a meter, a store, a station, a coin) can look like time-series forecasting, which is out of scope (SEL-10,
[selection.md](selection.md)). It is a tabular task when both legs hold: (1) a model on the features clearly beats each
entity's naive forecast on the shipped windows, measured by the task's declared metric (a correlation metric where the
source scores one); (2) the source's top solutions are tabular models on point-in-time features, and no feature is a
lag of the target column itself, apart from its last observation when it is known at the prediction point and the
actor reads it (trailing returns or other summaries of the series up to the prediction point are allowed). Amended
2026-10-26 (Lennart, on rain_in_australia's 9 am rain reading, the label of the day before): "we are allowed to keep
this if we can compute it and it makes sense to know the last observation". Leg 1 then carries the test: the model
must clearly beat the forecasts built from the series itself. Such "tabular forecasting" tasks exist where people want to generalise across entities. How to test it:
Methods, "A forecasting-like task". Cases: ashrae_great_energy_predictor_iii (2026-10-15),
g_research_crypto_forecasting (2026-10-22), rain_in_australia (2026-10-26). stock and appliances_energy_prediction stay retired: their context and
data show forecasting tasks (Lennart, 2026-10-22).

## Methods

How to check a flag, how to test a forecasting-like panel, what each flag computes, and the hidden-group and
generated-data probes with their calibrations.

### How to check a flag

* **Tuned results** (TP-1). The benchmark's per-fold results of tuned methods on the dataset: per method
  configuration the mean score, its skill against a dummy on the same splits, the folds on which it beats the dummy,
  and whether it is tied with the best (paired per fold; repeated folds overlap, so read the ties as a lower bound).
  Kendall's W says how well the method ranks agree across folds; it is low on small folds even when the mean ranking
  is stable. Add the raw-feature test of TP-4. Say so when the results ran on another version of the data (another
  split, other columns, other scoring). In Data Foundry: `tuned_results.py`
  ([checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md)).
* **A dominant feature** falls in one of three cases: a leak or a definition (recorded after the outcome, or the label
  is derived from it; run the leak probes), the natural core of the task (TP-4), or a shortcut with no domain reason
  (a generated or edited dataset: PROV-3 in [provenance.md](provenance.md), "Is the data generated?"). Look at the raw
  feature without a model too: `Listed Price` used as the prediction scored R² 0.64 until the 39 listings at $0 were set
  aside, then 0.89-0.91.
* **A zero-inflated regression target** (forest_fires: 48% zeros). Check the oracle bound (the true zero / non-zero
  indicator with the positives' train mean: R² 0.58) and a hurdle model, P(y > 0) × E[y | y > 0], with its two stages
  reported apart (AUC of y > 0: 0.51-0.58; R² on the positive rows: below 0). Neither stage was learnable, so the
  zeros explain the variance but give no signal.
* **A grouped task** (TP-5): count the groups of each class in the whole dataset and per test fold. Repeats reshuffle
  the same groups, so more repeats add no evidence. Scored per group, one fold's metric rests on that fold's test
  groups (parkinsons: 10-11 patients, 16-24 patient pairs per AUC).
* **Lab measurements from a source with known processing artefacts**: run the subgroup test
  ([leak_checks.md](leak_checks.md), probe 7) on any marker in the file names or metadata, and bound what the marker
  can explain (pancreatic: a `t` suffix separates some control spectra at AUC 0.67, but its class shares could explain
  at most AUC 0.56 of the label, which reaches 0.63-0.66; kept, the question noted in the record).
* **A `solved` task** (TP-6, USE-4): look for a stage the source describes and test the task there (eryhemato: "first
  evaluated clinically with 12 features. Afterwards, skin samples were taken"; macro AUC 0.999 after the biopsy, 0.98
  before).
* **Robustness over splits**: the share of splits on which the models beat the dummy and the standard error of the
  mean skill, not the spread of one split's score (coffee: 13 of 13 windows, standard error 0.03).

### A forecasting-like task

How to test TP-10: compare the best naive forecast (each entity's profile from the same season a year earlier, or
its last value) with a default and a stronger gradient-boosting model, and check whether models split by entity type
do better than one model. Read what the source's top solutions used. The worked case is
ashrae_great_energy_predictor_iii in the Cases table.

### The flags

| Flag | Rule | What the script computes | First check |
|---|---|---|---|
| `no_signal` | TP-1, TP-2 | The best family's mean skill is not above twice its standard error (or 0.02). | Tuned results: do the strongest regularised methods beat the dummy fold by fold? Untuned models overfit noise (forest_fires, clock_protein_toxicity, asp_potassco: all kept). |
| `solved` | TP-6, TP-4 | ROC AUC, macro ROC AUC or R² of at least 0.995. | A leak or a lookup (leak probes, shallow tree); then a stage of the source where the task is not solved. |
| `no_spread` | TP-3 | The best and worst family differ by less than twice the standard error of their per-split difference (or 0.01). | Tuned results: if methods spread, keep (TP-3). On a large, low-noise dataset strong methods converge (amex); on a small one it is noise. |
| `one_feature` | TP-4 | The best single feature, chosen on each split's training side, reaches 95% of the best family's skill and leaves at most 1.25 times its remaining error (1 − skill). | TP-4: what the feature means, then the raw feature against the methods fold by fold (`tuned_results.py --feature auto`). |
| `drift_baseline` | TP-1, TP-2 | Temporal tasks: a constant from the newest train rows has a loss within 2% of the best family's (log loss, or squared error). | The task may be mostly drift: compare the windows' class shares or means over time. |
| `unstable` | TP-1, TP-5 | The best family beats the dummy on fewer than 80% of the splits, or the standard error of its mean skill is above 0.05; for a temporal task the standard error counts only when the best family loses to the dummy on a window (since 2026-10-15: a level drifting between windows moves the skill with the dummy's error; every earlier temporal case that beat the dummy on all windows was kept). | How many units a test fold holds; whether tuned methods are robust over all splits. |
| `few_minority` | TP-5, TP-8 (TP-7, TP-9) | A probed test fold holds fewer than 5 rows (groups, for a task scored per group) of a class, binary or multiclass. The report names each class that falls short with its smallest count in a test fold (`few_minority_classes` in the JSON). | TP-5 and TP-8: count the units of each named class in total and the share of the log loss its rows carry; wider windows or merged classes (TP-7), or `Too Small`. |

The script probes every shipped split (up to 30) for a dataset of at most 5,000 scored units (rows, or groups for a
task scored per group) and the first 5 otherwise, encodes text columns (TF-IDF + SVD), and reports each family's
skill, the single feature chosen per split and the smallest class per test fold. Flags from sweeps before 2026-10-06
used weaker rules (one feature chosen once on the first split, an unpaired spread test, the standard deviation for
`unstable`, text left out) and are not comparable. Before 2026-10-12, `few_minority` checked binary tasks only. Before
2026-10-15 the linear family read categories as integer codes (breast_cancer_prediction's linear probe: ROC AUC 0.80
with codes, 0.92 one-hot), and `unstable` counted the standard error on temporal tasks that beat the dummy on every
window.

### Hidden groups (`hidden_groups.py`)

The rule for a hit (a question, decided by the context and the use case, never by the gap alone) is SPLIT-30, with
SPLIT-29 and SPLIT-31, in [splits.md](splits.md), "Hidden groups in an IID task". The probe ranks columns with repeated
values (categorical, text and numeric; since 2026-10-21 floats too, not only whole numbers, so a value computed once per
entity, such as a wind-tunnel run's boundary-layer thickness, is a candidate) by how much a row's label follows from the
other rows with that value, beyond what the value says about unseen values. Among those that look like an entity
(attributes that stay fixed within a value, or a label the value nearly fixes) it measures untuned LightGBM on a random
split against a split by the column. It tests the same way keys of all columns but one (composite keys), clusters of
rows that agree on almost every column (near copies) and an exact key on each normalised text column (text keys). Its
docstring has the thresholds.

**Near copies cover a group that no single column holds, in a wide table.** Each row becomes a set of tokens (a
quantile bin or a value per column, without the values most rows have), and two rows are near copies when their
token Jaccard is at least 0.85 (92% of the columns agree; on fingerprint bits it is the Tanimoto coefficient) and they
share at least 10 tokens. Clusters of more than 100 rows are common profiles (empty records) or chains of neighbours,
and their rows are left single. The output gives the clusters at 0.9, 0.85, 0.8 and 0.7 and the gap at 0.85, against
the same random folds with each cluster moved into one fold. Read a near-copy hit as a pointer: find in the source
what the rows of a cluster share (the salt forms of one parent structure, one company inspected again, one client's
invoices) and take the group key from there, never from the clusters (SPLIT-24 in [splits.md](splits.md) bars
similarity clusters).
When no row has 10 informative columns the check does not run, and the output says `not run` (before 2026-10-21 it
read 0.0%): no evidence either way, as on huntprohibited_1m (9 features), where exact keys on the description later
found a copy in train for 1.4-4.9% of the test ads. A text column is one token, so an edited copy of a text never
counts here; the text keys cover it.

**Text keys cover a text posted again.** For each string column whose values have a median of at least 3 words, the
probe normalises the text (NFKC, lower case, every run of characters other than letters and digits as one space) and
groups the rows with the same text: an exact key from the data, which SPLIT-24 allows. Texts held by more than 100 rows
(boilerplate) are left single. The output (`(text: <column>)`) gives the keys, the rows that share one, `s_id` and, for
an IID task, the gap against the random folds with each key moved into one fold (the gap models read no text, so the
gap comes from the other columns of the repeated rows); for a temporal task, the test rows whose text is on the training
side. A text key catches a copy with other capitals, punctuation or spacing, not one with a word changed. A string
column that is a candidate of its own (a title, a company profile) is left to the column check.

Sweep of 2026-10-21 (173 built containers, the grouped ones as if IID), before and after floats became candidates (a
candidate now also needs 20 values held by two rows or more, so a sparse spectrum bin with one repeated 0 is none) and
the text keys came in. New hits: airfoil_self_noise `suction-side-displacement-thickness` (105 values for 106 runs;
gap 0.123, next to its known `run`), drug_induced_autoimmunity_prediction `SMR_VSA10` and `SMR_VSA7` (IID, 587
molecules; gaps 0.172 and 0.112 of a random-split skill of 0.657), and in grouped datasets early_learning_predictors
`pri_fees_amount_pv`, force_2020 `FORMATION` and `Y_LOC` (a well's location) and sepsis_prediction_1m `Age` and
`HospAdmTime` (constant per patient). lgd stays without a candidate: its loan-to-value ratio has 1.3 rows per value. No
text key is a hit: emscad's `description`, `requirements` and `benefits` keys hold 17-29% of the rows with gaps of
0.019-0.032 (its known group already holds them out), huntprohibited_1m's `description` 3.3% (gap 0.001),
mercari_price_suggestion's `name` 28% (gap 0.000); consumer_complaints_1m's narrative is a column candidate. The
near-copy check does not run on 32 of the 173 datasets (airfoil_self_noise, lgd, huntprohibited_1m, mercari among them).

**Composite keys cover an entity measured more than once.** Rows identical in every column but one are one entity at
another age, dose, time or frequency. concrete_compressive_strength's 1,030 tests are 428 mixes (the seven ingredient
amounts), 182 of them tested at several ages; no single column holds a mix, and 8 columns give no near copies, so the
probe missed it until 2026-10-14. It now hashes, exactly, the key of all columns but one for each column (two when
none counts and rows times keys stay within 200M). A key counts when the rows that share it with a differing row are
at least 10% of the rows and four times the share with every column permuted on its own, when it holds a column of
at least 20 values, and keys of more than 100 rows are left out. These rules keep out repeats by chance: the all-"No"
symptom profile of early_stage_diabetes_risk_prediction (binary columns only), tour_travels_churn and website_phishing
(a few categories), blood_transfusion (common pairs of counts, one column an exact copy of another) and the empty
customers of expresso_churn_prediction_1m (keys of 16,000 rows). A key's gap may instead raise the error left by a
quarter: concrete's `(all but Age)` gives R^2 0.923 random against 0.857 grouped, 7% of the skill but nearly twice
the error. Take a key hit to the source: when the key is what one row's entity is (a mix, a wind-tunnel run), group on
it (SPLIT-24 in [splits.md](splits.md), "Grouped tasks"); when new rows keep the key, it is a feature (SPLIT-4). A group
by no column at all (the target protein of a CASP decoy) still does not show up; read what one row is in the source.

Calibration of the composite keys on 2026-10-14 (all 177 definitions, the grouped ones as if IID): three hits,
concrete `(all but Age)`, airfoil_self_noise `(all but frequency)` (its wind-tunnel runs) and
amazon_employee_access `(all but RESOURCE)` (the requester's manager and role columns, next to its `MGR_ID` hit).
Keys count without a hit in 19 IID or grouped datasets, with gaps of at most 0.035 (coil_2000); the next is fiat_500
(30% of the rows: one dealer's cars of one model, age and price at other mileages; gap 0.023). In 7 temporal tasks a
key recurs across the cutoff (rossmann_store_sales `(all but Date)`: 100% of the test rows). The search takes 0.2 s on a
median dataset and 228 s at most (2.5M rows and 988 columns, 80 of the keys); the sweep with 12 jobs of 2 threads took
12.5 minutes.

**Temporal tasks get no hit.** The shipped split already keeps the future out, and an entity that recurs across the
cutoff is part of the task. For the top candidates (the entity-like ones first) and the near copies, the probe
reports the share of test rows whose value occurs on the training side of each shipped split (`test_rows_seen`):
`building_id` 100% (ashrae_great_energy_predictor_iii_1m), `customer_id` 69% (african_credit_scoring_challenge),
`USER_ID` 64% (alvin_smart_money_management_classification_challenge). Read it against the use case (grouped
structure inside a temporal task, SPLIT-13 in [splits.md](splits.md)): a high share is right when the model predicts for
known entities, and a question when the use case is a new entity.

Calibration on 2026-10-06 (the 15 grouped datasets run as if IID): the probe finds the known group or an equivalent
key in 11 (respondent, poster group, patient, subject, customer, molecule, mouse, motor profile, instance, facility
attributes, ASP instance); the 4 it misses have small gaps (0.03-0.05: cardiotocography, micro_mass,
5g_energy_consumption, video_transcoding_time_prediction), where a random split would gain little.

Calibration of the near copies on 2026-10-12 (all 184 definitions, the grouped ones as if IID with their group column
left out of the tokens): no IID dataset is a near-copy hit. The closest are coil_2000 (85% of the rows in clusters
of customers who share their zip area's socio-demographic columns, which the source derives from the zip code; gap
0.036, 7.9% of the random-split skill), labour_inspection_compliance (52%, a company inspected again; gap 0.019, 5.9%)
and qsar_tid_11 (35%, analog series; gap 0.035, 4.7%). qsar_oral_toxicity has small families: 366 clusters of 2-25
compounds hold 11% of the rows at 0.85 (3.7% at 0.9, 24% at 0.8), and the gap is 0.006 (skill 0.750 against 0.744),
the analog effect its record describes, not series to memorise. Among the grouped datasets early_learning_predictors
is a hit (facilities; gap 0.041, 10.9%) and fraud_detection_in_electricity_and_gas_consumption_1m comes close (one
client's invoices; 24% of the rows, gap 0.041, 8.5%). The similarity is 0.85 because at 0.8 qsar_tid_11's analog
series reach a gap of 0.061-0.071 (8-9% of the skill over three fold seeds), next to the hit line; the 10-token
minimum keeps out tables of a few columns, where rows agree on all but one by design (amazon_employee_access, an
employee's role columns and manager: gap 0.14 at 0.8 without it). The clusters take 0.1 s on a median dataset and at
most 58 s (2.5M rows); a sweep of all 184 definitions with 10 jobs of 2 threads took 13 minutes.

| Dataset | Hit | Decision | Evidence |
|---|---|---|---|
| amazon_employee_access | `MGR_ID` (4,243 values) | no action (2026-10-06) | a request's manager is known when it is made, and managers recur: a feature, not an entity new data lacks. `(all but RESOURCE)` (2026-10-14) is the requester's manager and role columns, the same question |
| covertype | `Soil_Type` (40 values) | no action (2026-10-06) | every location has a known soil type; its two "attributes" are zones derived from it |
| mutual_funds_india | `sub_category` (38 values) | no action (2026-10-06) | a new fund has a known sub-category |
| superconductivity | `range_atomic_radius` (repeated compositions) | grouped by composition (2026-10-06) | the features come from the composition alone and a model is used for compositions without a measured temperature; a random split gave 35% of the test rows an identical row in train. Key: element shares from `unique_m.csv` (15,164 compositions; joins `Dy1Ir2Rh2B4`/`Dy1Rh2Ir2B4` and `V2Zr1`/`V66.6Zr33.3`). Gap on Tc at most 0.009 R², ranking unchanged: the use case decided, not the gap. Not by element set (a new family is a different task) |
| airfoil_self_noise | none until 2026-10-14; then `(all but frequency)`, the same groups. The single-column check missed the run because it only takes floats that are whole numbers: the thickness column alone separates 104 of the 106 runs (review panel, 2026-10-19); since 2026-10-21 floats are candidates and the thickness is a hit (gap 0.123) | grouped by wind-tunnel run (2026-10-06), then by setup, one chord at one angle with all its speeds (2026-10-20) | 106 runs (chord x angle x velocity), each a measured spectrum of 8-19 bands stored as one block; a random 3-fold split puts two thirds of a run's other bands in train (62.5% is the share of rows whose nearest neighbour is in the same run). R² random / by run with the angle numeric: extra trees 0.946 / 0.850, LightGBM 0.937 / 0.840 (as shipped, angle categorical, by run: 0.819 / 0.813). Found by reading the source, not by the probe |
| concrete_compressive_strength | `(all but Age)` (428 mixes; 2026-10-14) | grouped by mix (2026-10-14) | a mix is its seven ingredient amounts and 182 mixes are tested at several ages; a random split gave 73% of the test rows their mix in train at another age. R² random / by mix: LightGBM 0.925 / 0.874, MLP 0.916 / 0.838, ridge 0.816 / 0.804, the ranking changes. The use case designs a new mix. Missed by the column and near-copy checks |
| account_debt_south_africa | none (the eight municipalities have no column; they show as blocks of the file) | IID kept, tagged `ForcedIIDFromTemporal` (2026-10-12) | a municipality scores its own accounts, so its level is known; held out by file position, LightGBM ROC AUC falls from 0.877 to 0.843 (blocks of 2,500 rows) and 0.786 (thirds of the file), recorded in a bullet. One extract without dates: the status at the extract stands in for a forecast |

### Generated data (`generated_probes.py`)

Simulated data is out of scope (SEL-16 in [selection.md](selection.md), marker `AHDS`), and a generator leaves marks a
model can learn completely: the best possible score is then known, and strong methods reach it, so their ranking is
noise. The tests that decide whether a table was generated are PROV-3's, in [provenance.md](provenance.md), "Is the
data generated?". The probe looks for four marks; its docstring has the thresholds.

* `formula` (regression): a median regression on the numeric features, their squares, one-hot categoricals and the
  products of each binary column with each numeric feature fits many rows exactly (within the target's rounding),
  far more than it fits a shuffled target. Rows at a mass point of the target (a cap, a timeout) do not count:
  sat11_hand_algo_runtime has 36% of its rows at the timeout. The target is also tried after `exp`, since a
  definition may have logged it.
* `rule_leaves` (classification): leaves of a depth-5 tree, fit on one half and read on the other, whose held-out
  rows all belong to a minority class cover at least a fifth of that class.
* `independent_columns` (any task): on 1,000 rows, the features and the target together, at most 10% of the column
  pairs depend on each other at the 5% level (independent columns give about 5%), and at least half of the numeric
  columns with 20 or more values (at least 5 of them) are uniform over their range by a KS test. The JSON lists the
  uniform columns (`uniform_names`).
* `uniform_within_class` (classes, or a regression target of at most 20 values): the same two thresholds on the
  features within each class of at least 50 rows, pooled over the classes. It catches a generator that draws each
  feature uniformly between its class's minimum and maximum: the whole table then looks dependent, because the
  ranges differ by class.

**Reading a flag.** A flag is a question ([evidence.md](evidence.md), EV-3). A target that is legitimately computed
from the features (a score, a label defined by thresholds) or a leak gives the first two marks; inputs set by a design
(a uniform grid, a Latin hypercube) can give the last two. Before proposing a retirement, find what the source says
("simulated", "artificial", "generated", a textbook example) and look for marks the probe does not test, with the
tests of PROV-3 in [provenance.md](provenance.md): dependence that the world would show but the data does not (churn's
area codes spread over all states alike), several columns with one distribution, every row of a group following a rule.
When you can, write the generator down: that settles it. For the independence marks, name the dependence the domain must
show (AST and ALT in liver patients, size and equity in banks) and check it directly. Either statistic alone is common
in real data: santander_customer_transaction_prediction has 5.4% of its pairs dependent but no uniform column,
homesite_quote_conversion 13 of 42 uniform columns (each `...B` field codes its `...A` field in 25 equal-frequency bins)
but 45% of its pairs dependent, and bank_customer_churn has one uniform column, `estimated_salary`.

Calibration on 2026-10-06 (all 128 datasets of the working copy): the probe flags the two datasets known to be
generated and no other. The nearest regression is student_portuguese_performance (2.6% exact against 0.0%), the
nearest classifications are eryhemato_squamous_disease (17.7% of the minority in rule leaves: clinical diagnoses),
website_phishing (16.1%: its features are rule outputs) and homesite_quote_conversion (13.9%).

Calibration of the two independence flags on 2026-10-12 (all 184 definitions: the 125 built ones from their
containers, the other 59 rebuilt; plus the six retired generated datasets): neither flag fires on any of them, and both
fire on the two generated tables found in the 7 October run, which have no definition (UCI 503 and OpenML 46372, run
through `check_frame`).

* `independent_columns`: UCI 503 has 5.7% of 406 pairs dependent and 11 of 17 columns uniform (the 17-feature
  definition drafted in that run: 6.5% and 7 of 7). Lowest pair shares in the working copy: santander (5.4%),
  audiology_diagnosis (7.2%) and biogeographical_ancestry_prediction (7.9%), none with a uniform column; then
  qsar_tid_11 (14.2%). Highest uniform share with at least 5 columns tested: homesite_quote_conversion (0.31).
* `uniform_within_class`: OpenML 46372 has 4.0% of 150 within-class pairs dependent and 60 of 60 cells uniform
  (UCI 503: 5.0% and 50 of 68). Lowest in the working copy: santander (4.9%, 0 of 200 uniform),
  biogeographical_ancestry_prediction (5.6%, nothing tested), bank_customer_churn (11.1%, 2 of 8). Highest uniform
  share: pancreatic_cancer_mouse_detection (0.41, every pair dependent). The book's 197 rows that OpenML 46372 was
  made from (corporate_credit_rating_cat_data_set_ratings_raitings) have no class of 50 rows; with classes down to
  10 rows they give 17.1% of 105 pairs dependent and 10 of 24 cells uniform, no flag. Classes need 50 rows because
  the KS test loses its power on small classes: with classes of 10-49 rows, lung_cancer reaches 0.495 uniform.

| Dataset | Flag | Decision | Evidence |
|---|---|---|---|
| healthcare_insurance_expenses | `formula` (72% exact, 2% shuffled) | retired, `AHDS` (2026-10-06) | Lantz's textbook data, "simulated on the basis of demographic statistics from the US Census Bureau"; 1,220 of 1,338 charges equal 1072 + 3.363 age² + 1.39 bmi + 589 children − 489 [male] + region + [smoker](1500 + 489 bmi + 15000 [bmi > 30]), the rest add a random extra cost; the best BeyondArena methods reach the best possible score |
| churn | `rule_leaves` (26%) | retired, `AHDS` (2026-10-06) | MLC++: "artificial based on claims similar to real world"; area codes independent of the state, one distribution for all call counts, charges = minutes × fixed rates, international-plan rules with 79/79 and 89/89 churners |

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.
The rows come from the v0.2 review of the flagged datasets (from 2026-10-05) and the reviews since; Flags are the
task-probe flags the decision answers. The decisions on metrics (2026-10-21) are in [metrics.md](metrics.md), Cases.

| Rule | Dataset | Flags | Decision | Decisive evidence | Kind |
|---|---|---|---|---|---|
| TP-4 | fitness_club | one_feature | retired, `Trivial` (2026-10-05) | `months_as_member` alone, chosen on all 30 training sides, AUC 0.822, above all 37 configurations; `days_before` = 2 × weekday in 1,251 of 1,500 rows (generated) | applied |
| TP-5 | parkinsons_biomedical_voice_measurements | no_spread, one_feature, unstable | retired, `Too Small` (2026-10-05) | 8 healthy people, 2-3 per test fold; ranks less stable than on 98% of BeyondArena | applied |
| TP-7 | audiology_diagnosis | no_spread, unstable | target re-defined, rebuilt (2026-10-06) | our own 3-class merge replaced by hearing loss with or without a conductive part; duplicates and non-hearing-loss diagnoses dropped; no flags since | applied |
| TP-6 | eryhemato_squamous_disease | solved | clinical features only, rebuilt (2026-10-06) | macro AUC 0.999 with the biopsy features, 0.98 and 87% accuracy before the biopsy | applied |
| TP-2 | forest_fires | no_signal | kept (2026-10-06) | TabPFN-3.5 beats the mean on 26 of 32 folds (R² 0.013); a hurdle model adds nothing | applied |
| TP-1 | clock_protein_toxicity | no_signal | kept (2026-10-06) | LightGBM above AUC 0.5 on 44 of 60 folds (0.539); the probe's single feature was a selection effect | applied |
| TP-1 | asp_potassco_classification | no_signal | kept (2026-10-06) | TabICLv2 beats the class shares on 30 of 30 folds; label noisy (62% of runner-ups within 1 s) | applied |
| TP-4 | sepsis_survival_minimal_clinical_records | one_feature | kept (2026-10-06) | age alone AUC 0.704, below the best (0.707) on every fold; 975 distinct cases by design | applied |
| TP-4 | california_house_prices_2020 | one_feature | kept (2026-10-06) | the listed price is the natural core; sold = listed R² 0.89-0.91, methods 0.93-0.945 | applied |
| TP-4 | aps_failure | one_feature | kept (2026-10-06) | the per-split single feature (AUC 0.970) stays below all 20 configurations; AUC near its ceiling | applied |
| TP-5 | musk | no_spread, unstable | kept (2026-10-06) | 13 musk and 21 non-musk molecules per fold: a tiny-data task | applied |
| TP-1 | pancreatic_cancer_mouse_detection | unstable | kept (2026-10-06) | foundation models above AUC 0.5 on all their folds; the `t` file suffix is an open question in the record | applied |
| TP-2 | amex_non_iid_1m | no_spread | kept (2026-10-06) | strong methods converge at AUC 0.95 on 1.5M rows | applied |
| TP-2 | acquire_valued_shoppers_challenge | no_spread | kept (2026-10-06) | a real task with a low ceiling (best AUC 0.654, 12 of 21 tied) | applied |
| TP-3 | coil_2000, marketing_campaign, naticusdroid_android_permissions_dataset | no_spread | kept (2026-10-06) | tuned methods separate: at most 2 of 29 tied with the best | applied |
| TP-3 | gallstone_disease, indian_liver_patient_dataset, mercedes_benz_greener_manufacturing | no_spread | kept (2026-10-06) | tuned methods spread | applied |
| TP-1 | mercari_price_suggestion | no_spread | kept (2026-10-06) | the probe left its text out: R² 0.06 without, 0.67 with it | applied |
| TP-1 | coffee_rating_prediction, garments_worker_productivity | unstable | kept (2026-10-06) | tree models beat the mean in 13 of 13 and 28-29 of 30 windows | applied |
| TP-2 | heart_disease_cleveland | no_spread | kept (2026-10-06) | a real task with clear signal (AUC 0.91); little room between methods is the noise of a small task | applied |
| TP-1 | consumer_complaints_1m | unstable | kept (2026-10-06, rebuild sweep) | best probe model above the dummy in 3 of 3 windows (AUC 0.90); the standard error of 0.060 over 3 windows is drift, not a missing signal; all 21 BeyondArena configurations beat the dummy | applied |
| TP-3 | electric_motor_temperature_prediction | no_spread | kept (2026-10-06, rebuild sweep) | R^2 0.94-0.97 for every probe model, a gap 3 folds cannot test; tuned RMSE 1.77-3.52 on BeyondArena | applied |
| TP-4 | expresso_churn_prediction_1m | one_feature | kept (2026-10-07) | active days (REGULARITY, AUC 0.890) are the natural core of a churn task; on the full 1M/500k folds untuned LightGBM beats it on 3 of 3 (0.903 against 0.890) | applied |
| TP-4 | thyroid_discordant | none (the marker came from a curation comment and was never tested) | `Trivial` removed (2026-10-22, Lennart) | `FTI`, the best single feature on all 30 training sides, ROC AUC 0.822 against 0.974 for a random forest, lower on 30 of 30 splits | applied |
| TP-2 | mortgage | drift_baseline (one_feature before the macro-lag fix) | kept (2026-10-07) | the previous quarter's class shares (log loss 0.134) match untuned models on 50k sampled rows; on the full training side LightGBM beats them in 3 of 3 quarters (0.120/0.132/0.136 against 0.125/0.137/0.139) and ranks loans within a quarter (AUC 0.56-0.72) | applied |
| TP-2 | rosbank1 | no_spread | kept (2026-10-07) | 3 monthly windows of 63-123 clients cannot test a LightGBM - linear gap of 0.045 AUC (paired SE 0.036); all models beat the dummy in 3 of 3; no longer history in the release (as electric_motor_temperature_prediction) | applied |
| TP-2 | apistox | unstable (no_spread before the SMILES encoding) | kept (2026-10-07; 2026-10-12 with RDKit descriptors; 2026-10-14 without the SMILES) | above the dummy in 4 of 4 windows; the standard error (0.117 for the linear model on SMILES TF-IDF, 0.065 for LightGBM with the RDKit descriptors, 0.066 without the SMILES) is window-to-window variation of a small temporal task (as consumer_complaints_1m) | applied |
| TP-2 | bias_correction_r_bias_correction_r_2 | no_spread; unstable (2026-10-15, after the days without an LDAPS run were dropped) | kept (2026-10-07, 2026-10-15) | a window is 6-7 weather days and the day carries 82.5% of the target's variance, so strong methods separate little (paired SE 0.03-0.04 RMSE); their mean beats a per-station MOS in 7 of 9 windows; re-check with tuned results. `unstable`: LightGBM falls just below the training mean in the oldest window only (2017-06-30 to 07-06, skill -0.07, dummy RMSE 1.11) and beats it on the other 8 (0.61-0.96) | applied |
| TP-1, TP-2, TP-3 | african_credit_scoring_challenge | no_spread, drift_baseline (unstable on 5 windows) | kept (2026-10-07) | windows of 20-56 defaults; the linear model beats the class shares in 9 of 9 (AUC 0.649); the drift flag is about log loss (the default rate moves from 1-1.4% to 6.4-9.4%), which ROC AUC, the metric, ignores; re-check with tuned results | applied |
| TP-2 | sf_permit_time | no_spread (after the 6-month label gap) | kept (2026-10-12) | random forest, LightGBM and linear within 0.032 skill (paired SE 0.019) on 5 of 8 windows; in 2021-H2 LightGBM carries the slow COVID level forward, as a real refit in July 2021 would; no tuned results in the cache, re-check with the first tuned runs | applied |
| TP-8 | alvin_smart_money_management_classification_challenge | few_minority | retired, `Too Small` (2026-10-12) | only Train.csv has labels: 3 windows of 27-41 test purchases from 5-12 users; Shopping has 2 test rows over all windows; the 8 rows of the rarest classes carry 51-54% of window 1's log loss | applied |
| TP-8 | forensic_glass_identification, ljubljana_primary_tumor, mic, sarcoma | few_minority | kept (2026-10-12) | rare classes of 9-14 rows, 3-5 per test fold: 0.7-13% of the test rows, 4.8-22% of a random forest's log loss | applied |
| TP-8 | micro_mass, asp_potassco_classification | few_minority | kept (2026-10-12) | the grouped split makes fold sizes uneven (B. thuringiensis 2-6 spectra from 8 strains, h3-n1 1-17 runs from 9 instance groups): 18% and 1.7% of the test rows, 25% and 3.9% of a random forest's log loss | applied |
| TP-8, TP-1 | force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition | few_minority, no_spread | kept (2026-10-12) | Anhydrite (1,807 rows, 10 wells) and Halite (14,711 rows, 4 wells) each miss one of 3 well-grouped test folds, accepted as `splits_test_class_missing`; no_spread comes from untuned LightGBM diverging (log loss 2.77), while random forest (0.744) and linear (0.989) spread against the class shares (1.284) | applied |
| TP-3 | hr_analytics | no_spread | kept (2026-10-14) | rebuilt from the hackathon's own train file (Kaggle's copy added 2,623 test rows labelled 1 and gave 0.80); the real labels give ROC AUC 0.62-0.63 for every family (LightGBM +0.012 over random forest, paired SE 0.006): a real signal with a low ceiling | applied |
| TP-3 | open_university_learning_analytics_dataset | no_spread | kept pending tuned results (2026-10-22, Lennart) | after the weight-0 TMA change, default models on all 9 grouped splits reach log-loss skill 0.173 (random forest), 0.170 (LightGBM), 0.162 (logistic regression); random forest leads by 0.011 (paired SE 0.009); every family beats the class shares on every split | re-check with the first tuned run |
| TP-10 | ashrae_great_energy_predictor_iii | none (a forecasting-like panel) | in scope as one task (2026-10-15) | RMSE on log kWh per window: the best naive forecast 1.393 / 1.273 / 1.372; default LightGBM (100 trees) loses to it, 1.444 / 1.403 / 1.448; LightGBM with 1,000 trees wins, 1.261 / 1.176 / 1.223; models per site do about the same as one model; the top five teams used no lagged readings | applied |
| TP-10 | g_research_crypto_forecasting | none (a forecasting-like panel) | in scope as one task (2026-10-22, Lennart; the rule amended) | weighted Pearson per window +0.040 / +0.052 / +0.045, every 95% day-block interval above the coin's mean (-0.002 / +0.007 / +0.008); the top three solutions were LightGBM on the coins' trailing 60-900-minute returns against the market, no lag of the target column; no top solution used a sequence model (LSTM) or ARIMA | applied |
| TP-10 | rain_in_australia | none (a forecasting-like panel) | in scope as one task, the 9 am rain reading kept (2026-10-26, Lennart; leg 2 amended) | ROC AUC on the 9 windows then shipped: all features 0.849; the best forecast from the location's own rain series 0.752 (a regression of the amount with a > 1 mm rule), its classifier 0.754, persistence 0.661; the full model ahead in 9 of 9 windows; without Rainfall and RainToday 0.847 | applied |
| TP-10 | stock, appliances_energy_prediction | none (not probed again) | stay retired, `Time-series (Forecasting)` (2026-10-22, Lennart) | the amendment (leg 1 by the declared metric, trailing summaries allowed) reopens neither: "we know from the context and data state that these are indeed forecasting tasks" | applied |
| TP-9 | seismic_bumps | none (temporal windows) | retired, `Too Small` (2026-09-30, Lennart) | the honest split is temporal; the test windows come from the newest half, which holds 49 of the 170 positives: 30 windows of 43 shifts have 0-5 positives each (6 have none), and 3 or 2 windows (14-26 positives each) still give ROC AUC intervals of about ±0.1 to ±0.14 per window | applied |

## In Data Foundry

How to run the task, group, hidden-group and generated-data probes and the tuned-results check on a definition, and
where their output goes: [checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md). The
probe methods themselves are in this skill's [scripts/](../scripts/).
