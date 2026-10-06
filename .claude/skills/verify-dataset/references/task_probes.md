# Reading the task probes

How to answer the flags of [`scripts/task_probes.py`](../scripts/task_probes.py) (rubric item 13): whether a
dataset is empty, trivial, too small, or worth benchmarking. The rules below come from the review of the 24 datasets
the probes flagged in the TabArena v0.2 build (5-6 October 2026; the evidence is in each record's dated comment and
on <https://claude.ai/artifact/APTR4PUmbUn2d133mcFgXf>).

**After each decision on a flagged dataset, add a row to the cases table** (and a rule when the case changes how a
flag is read), so the next decision starts from the precedent.

## The rules

1. **A flag is a question, not a verdict.** The probes fit untuned models; check every flag against tuned methods
   before acting on it (`scripts/tuned_results.py`, below).
2. **A small but real signal is no reason to retire**, and neither is a cutoff on the best skill. forest_fires
   (R² 0.013, but TabPFN-3.5 beats the mean on 26 of 32 folds) is a valid task. Retire, fix or keep a task for a
   concrete reason found in the task itself; until one is found, the task stays.
3. **If tuned methods spread, keep the dataset.** No further discussion is needed.
4. **`Trivial` needs proof.** Read what the dominant feature means first: the natural core of a task (a listed price
   for a sale price, age for survival) is expected to dominate. Then test it: the raw feature, chosen on each
   split's training side, has to match or beat the methods fold by fold (fitness_club: yes, retired;
   sepsis_survival, california: no, kept).
5. **`Too Small` means a handful of units of a class**, per test fold and in total, counted in the unit the task is
   scored on (parkinsons: 8 healthy people, 2-3 per fold; retired). A small dataset as such is a tiny-data task like
   the others (musk: 102 molecules, 13 musk per fold; kept).
6. **Keep two questions apart: is the task valid, and is it the best version?** A valid task stays. A better version
   the source itself defines (a stage it describes, the scoring it uses) replaces the current one: eryhemato before
   the biopsy. A fix of our own invention (dropping near-ties, a label merge made from
   names) is not a better version.
7. **When the definition builds the target itself** (merged or dropped classes), use an established convention,
   test each candidate (classes per test fold after dropping duplicates, signal, how rule-like the label is), and run
   the leak probes on the source's labels too (audiology_diagnosis).

## How to check a flag

* **Tuned results.** `.venv/bin/python .claude/skills/verify-dataset/scripts/tuned_results.py <unique_name>
  [--feature auto]` reads the per-fold BeyondArena results cached under `~/.cache/tabarena/artifacts/` and the shipped
  container they ran on. Per method configuration: the mean score, its skill against a dummy on the same splits, the
  folds on which it beats the dummy, and whether it is tied with the best (paired per fold; repeated folds overlap, so
  read the ties as a lower bound). Kendall's W says how well the method ranks agree across folds; it is low on small
  folds even when the mean ranking is stable. `--feature auto` adds the raw-feature test of rule 4. The runs used the
  shipped (format-1) containers: say so when the v2 definition changed the split, the columns or the scoring.
* **A dominant feature** falls in one of three cases: a leak or a definition (recorded after the outcome, or the label
  is derived from it; run the leak probes), the natural core of the task (rule 4), or a shortcut with no domain reason
  (a generated or edited dataset: `../../check-candidate/SKILL.md`, "Checking whether the data is generated"). Look
  at the raw feature without a model too: `Listed Price` used as the prediction scored R² 0.64 until the 39 listings
  at $0 were set aside, then 0.89-0.91.
* **A zero-inflated regression target** (forest_fires: 48% zeros). Check the oracle bound (the true zero / non-zero
  indicator with the positives' train mean: R² 0.58) and a hurdle model, P(y > 0) × E[y | y > 0], with its two stages
  reported apart (AUC of y > 0: 0.51-0.58; R² on the positive rows: below 0). Neither stage was learnable, so the
  zeros explain the variance but give no signal.
* **A grouped task**: count the groups of each class in the whole dataset and per test fold. Repeats reshuffle the
  same groups, so more repeats add no evidence. Scored per group, one fold's metric rests on that fold's test groups
  (parkinsons: 10-11 patients, 16-24 patient pairs per AUC).
* **Lab measurements from a source with known processing artefacts**: run the subgroup test
  (`../../check-candidate/references/leak_checks.md`, probe 7) on any marker in the file names or metadata, and bound
  what the marker can explain (pancreatic: a `t` suffix separates some control spectra at AUC 0.67, but its class
  shares could explain at most AUC 0.56 of the label, which reaches 0.63-0.66; kept, the question noted in the record).
* **A `solved` task**: look for a stage the source describes and test the task there (eryhemato: "first evaluated
  clinically with 12 features. Afterwards, skin samples were taken"; macro AUC 0.999 after the biopsy, 0.98 before).
* **Robustness over splits**: the share of splits on which the models beat the dummy and the standard error of the
  mean skill, not the spread of one split's score (coffee: 13 of 13 windows, standard error 0.03).

## The flags

| Flag | What the script computes | First check |
|---|---|---|
| `no_signal` | The best family's mean skill is not above twice its standard error (or 0.02). | Tuned results: do the strongest regularised methods beat the dummy fold by fold? Untuned models overfit noise (forest_fires, clock_protein_toxicity, asp_potassco: all kept). |
| `solved` | ROC AUC, macro ROC AUC or R² of at least 0.995. | A leak or a lookup (leak probes, shallow tree); then a stage of the source where the task is not solved. |
| `no_spread` | The best and worst family differ by less than twice the standard error of their per-split difference (or 0.01). | Tuned results: if methods spread, keep (rule 3). On a large, low-noise dataset strong methods converge (amex); on a small one it is noise. |
| `one_feature` | The best single feature, chosen on each split's training side, reaches 95% of the best family's skill and leaves at most 1.25 times its remaining error (1 − skill). | Rule 4: what the feature means, then the raw feature against the methods fold by fold (`tuned_results.py --feature auto`). |
| `drift_baseline` | Temporal tasks: a constant from the newest train rows has a loss within 2% of the best family's (log loss, or squared error). | The task may be mostly drift: compare the windows' class shares or means over time. |
| `unstable` | The best family beats the dummy on fewer than 80% of the splits, or the standard error of its mean skill is above 0.05. | How many units a test fold holds; whether tuned methods are robust over all splits. |
| `few_minority` | Binary tasks: a test fold holds fewer than 5 rows (groups, for a task scored per group) of a class. | Rule 5: count the units of each class in total; wider windows or merged classes, or `Too Small`. |

The script probes every shipped split (up to 30) for a dataset of at most 5,000 scored units (rows, or groups for a
task scored per group) and the first 5 otherwise, encodes
text columns (TF-IDF + SVD), and reports each family's skill, the single feature chosen per split and the smallest
class per test fold. Flags from sweeps before 6 October 2026 used weaker rules (one feature chosen once on the first
split, an unpaired spread test, the standard deviation for `unstable`, text left out) and are not comparable.

## Cases (the v0.2 review)

| Dataset | Flags | Decision | Decisive evidence |
|---|---|---|---|
| fitness_club | one_feature | retired, `Trivial` (5 Oct) | `months_as_member` alone, chosen on all 30 training sides, AUC 0.822, above all 37 configurations; `days_before` = 2 × weekday in 1,251 of 1,500 rows (generated) |
| parkinsons_biomedical_voice_measurements | no_spread, one_feature, unstable | retired, `Too Small` (5 Oct) | 8 healthy people, 2-3 per test fold; ranks less stable than on 98% of BeyondArena |
| audiology_diagnosis | no_spread, unstable | target re-defined, rebuilt (6 Oct) | our own 3-class merge replaced by hearing loss with or without a conductive part; duplicates and non-hearing-loss diagnoses dropped; no flags since |
| eryhemato_squamous_disease | solved | clinical features only, rebuilt (6 Oct) | macro AUC 0.999 with the biopsy features, 0.98 and 87% accuracy before the biopsy |
| forest_fires | no_signal | kept (6 Oct) | TabPFN-3.5 beats the mean on 26 of 32 folds (R² 0.013); a hurdle model adds nothing |
| clock_protein_toxicity | no_signal | kept (6 Oct) | LightGBM above AUC 0.5 on 44 of 60 folds (0.539); the probe's single feature was a selection effect |
| asp_potassco_classification | no_signal | kept (6 Oct) | TabICLv2 beats the class shares on 30 of 30 folds; label noisy (62% of runner-ups within 1 s) |
| sepsis_survival_minimal_clinical_records | one_feature | kept (6 Oct) | age alone AUC 0.704, below the best (0.707) on every fold; 975 distinct cases by design |
| california_house_prices_2020 | one_feature | kept (6 Oct) | the listed price is the natural core; sold = listed R² 0.89-0.91, methods 0.93-0.945 |
| aps_failure | one_feature | kept (6 Oct) | the per-split single feature (AUC 0.970) stays below all 20 configurations; AUC near its ceiling |
| musk | no_spread, unstable | kept (6 Oct) | 13 musk and 21 non-musk molecules per fold: a tiny-data task |
| pancreatic_cancer_mouse_detection | unstable | kept (6 Oct) | foundation models above AUC 0.5 on all their folds; the `t` file suffix is an open question in the record |
| amex_non_iid_1m | no_spread | kept (6 Oct) | strong methods converge at AUC 0.95 on 1.5M rows |
| acquire_valued_shoppers_challenge | no_spread | kept (6 Oct) | a real task with a low ceiling (best AUC 0.654, 12 of 21 tied) |
| coil_2000, marketing_campaign, naticusdroid_android_permissions_dataset | no_spread | kept (6 Oct) | tuned methods separate: at most 2 of 29 tied with the best |
| gallstone_disease, indian_liver_patient_dataset, mercedes_benz_greener_manufacturing | no_spread | kept (6 Oct) | tuned methods spread (rule 3) |
| mercari_price_suggestion | no_spread | kept (6 Oct) | the probe left its text out: R² 0.06 without, 0.67 with it |
| coffee_rating_prediction, garments_worker_productivity | unstable | kept (6 Oct) | tree models beat the mean in 13 of 13 and 28-29 of 30 windows |
| heart_disease_cleveland | no_spread | kept (6 Oct) | a real task with clear signal (AUC 0.91); little room between methods is the noise of a small task |
| consumer_complaints_1m | unstable | kept (6 Oct, rebuild sweep) | best probe model above the dummy in 3 of 3 windows (AUC 0.90); the standard error of 0.060 over 3 windows is drift, not a missing signal; all 21 BeyondArena configurations beat the dummy |
| electric_motor_temperature_prediction | no_spread | kept (6 Oct, rebuild sweep) | R^2 0.94-0.97 for every probe model, a gap 3 folds cannot test; tuned RMSE 1.77-3.52 on BeyondArena (rule 3) |

## Hidden groups in IID tasks (`hidden_groups.py`)

An IID split is wrong when many rows share an entity that new data would not have and the entity carries the label:
a random split then rewards recognising the entity. The probe ranks columns with repeated values by how much a row's
label follows from the other rows with that value, beyond what the value says about unseen values. Among those that
look like an entity (attributes that stay fixed within a value, or a label the value nearly fixes) it measures
untuned LightGBM on a random split against a split by the column; its docstring has the thresholds.

**The rule (Lennart, 2026-10-06): a hit is a question.** Re-split a dataset only when the context says the rows share
an entity that new data would not have (the source calls the column an id, or the use case predicts for new
entities), or when the evidence is very strong. Holding out the values of any useful feature opens a gap, so the gap
alone never decides: a manager, a soil type or a fund category is known for every new row.

**The split follows what the task does in reality, not the size of the gap** (Lennart, 2026-10-06). Ask what a
deployed model predicts for: if it is an entity that new data would not contain (a material nobody has measured, a
new respondent), the test entities must be new, even when a random split costs only a little (superconductivity:
at most 0.009 R², grouped). If new rows keep having the value (a manager, a soil type), the column is a feature and
the split stays. Report the gap across a few model families, but let the use case decide. Take the group key from
the source's own data, at the resolution the features see (superconductivity: element shares from `unique_m.csv`,
which the features are computed from; a formula string would split one composition written two ways). Keep the
source's rows: deduplicating with averaged targets is a different dataset.

**The probe checks single columns only.** A group defined by several columns (a wind-tunnel run is one chord, angle and velocity) or by no column at all (the target protein of a CASP decoy) does not show up; read what one row is in the source and check the combinations of its settings (`df.groupby(settings).ngroup()`, rows per group, blocks in the raw file order).

Calibration on 2026-10-06 (the 15 grouped datasets run as if IID): the probe finds the known group or an equivalent
key in 11 (respondent, poster group, patient, subject, customer, molecule, mouse, motor profile, instance, facility
attributes, ASP instance); the 4 it misses have small gaps (0.03-0.05: cardiotocography, micro_mass,
5g_energy_consumption, video_transcoding_time_prediction), where a random split would gain little.

| Dataset | Hit | Decision | Evidence |
|---|---|---|---|
| amazon_employee_access | `MGR_ID` (4,243 values) | no action (6 Oct) | a request's manager is known when it is made, and managers recur: a feature, not an entity new data lacks |
| covertype | `Soil_Type` (40 values) | no action (6 Oct) | every location has a known soil type; its two "attributes" are zones derived from it |
| mutual_funds_india | `sub_category` (38 values) | no action (6 Oct) | a new fund has a known sub-category |
| superconductivity | `range_atomic_radius` (repeated compositions) | grouped by composition (6 Oct) | the features come from the composition alone and a model is used for compositions without a measured temperature; a random split gave 35% of the test rows an identical row in train. Key: element shares from `unique_m.csv` (15,164 compositions; joins `Dy1Ir2Rh2B4`/`Dy1Rh2Ir2B4` and `V2Zr1`/`V66.6Zr33.3`). Gap on Tc at most 0.009 R², ranking unchanged: the use case decided, not the gap. Not by element set (a new family is a different task) |
| airfoil_self_noise | none (a run is three columns) | grouped by wind-tunnel run (6 Oct) | 106 runs (chord x angle x velocity), each a measured spectrum of 8-19 bands stored as one block; a random split gave a test row 62% of its run's other bands in train. R² random / by run: extra trees 0.946 / 0.850, LightGBM 0.937 / 0.840. Found by reading the source, not by the probe |

## Generated data (`generated_probes.py`)

Simulated data is out of scope (curation guidelines, criterion 4B, marker `AHDS`), and a generator leaves marks a
model can learn completely: the best possible score is then known, and strong methods reach it, so their ranking is
noise. The probe looks for two marks; its docstring has the thresholds.

* `formula` (regression): a median regression on the numeric features, their squares, one-hot categoricals and the
  products of each binary column with each numeric feature fits many rows exactly (within the target's rounding),
  far more than it fits a shuffled target. Rows at a mass point of the target (a cap, a timeout) do not count:
  sat11_hand_algo_runtime has 36% of its rows at the timeout. The target is also tried after `exp`, since a
  definition may have logged it.
* `rule_leaves` (classification): leaves of a depth-5 tree, fit on one half and read on the other, whose held-out
  rows all belong to a minority class cover at least a fifth of that class.

**A flag is a question.** A target that is legitimately computed from the features (a score, a label defined by
thresholds) or a leak gives the same marks. Before proposing a retirement, find what the source says ("simulated",
"artificial", "generated", a textbook example) and look for marks the probe does not test: dependence that the world
would show but the data does not (churn's area codes spread over all states alike), several columns with one
distribution, every row of a group following a rule. When you can, write the generator down: that settles it.

Calibration on 2026-10-06 (all 128 datasets of the working copy): the probe flags the two datasets known to be
generated and no other. The nearest regression is student_portuguese_performance (2.6% exact against 0.0%), the
nearest classifications are eryhemato_squamous_disease (17.7% of the minority in rule leaves: clinical diagnoses),
website_phishing (16.1%: its features are rule outputs) and homesite_quote_conversion (13.9%).

| Dataset | Flag | Decision | Evidence |
|---|---|---|---|
| healthcare_insurance_expenses | `formula` (72% exact, 2% shuffled) | retired, `AHDS` (6 Oct) | Lantz's textbook data, "simulated on the basis of demographic statistics from the US Census Bureau"; 1,220 of 1,338 charges equal 1072 + 3.363 age² + 1.39 bmi + 589 children − 489 [male] + region + [smoker](1500 + 489 bmi + 15000 [bmi > 30]), the rest add a random extra cost; the best BeyondArena methods reach the best possible score |
| churn | `rule_leaves` (26%) | retired, `AHDS` (6 Oct) | MLC++: "artificial based on claims similar to real world"; area codes independent of the state, one distribution for all call counts, charges = minutes × fixed rates, international-plan rules with 79/79 and 89/89 churners |

