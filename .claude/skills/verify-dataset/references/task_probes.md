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
   the biopsy, asp_potassco scored by PAR10. A fix of our own invention (dropping near-ties, a label merge made from
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
| asp_potassco_classification | no_signal | kept; a PAR10 selection version to replace it (6 Oct) | TabICLv2 beats the class shares on 30 of 30 folds; label noisy (62% of runner-ups within 1 s) |
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
