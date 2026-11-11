---
unique_name: sepsis_survival_minimal_clinical_records
name: Sepsis Survival Minimal Clinical Records
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Trivial
tags:
- Larger IID Data
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- 'Entities: Recur'
collections:
- New (BeyondArena)
original_source: Other
year: '2017'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/827/sepsis+survival+minimal+clinical+records
- https://doi.org/10.24432/C53C8N
notebook_path: datasets/beyond_iid/new_iid/sepsis_survival_minimal_clinical_records/sepsis_survival_minimal_clinical_records.ipynb
source_row: 662
type_adapter_id: curation-record-v1
---

## Comments

CC: "It has three features, which sound hard to be fully meaningful. But it is a real task"

3 Features, unsure how trivial the dataset is

The dataset is full of "real" duplicates and is technically just a small or tiny dataset. We keep it as is to see how methods can handle it, but this is not really large data...

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid task by design after the task-probe review (flag `one_feature`). The 110,204 admissions hold only 975 distinct feature rows (age, sex, episode number; 7.4% died): the duplicates are real patients, and predicting survival from these three fields alone is the source paper's question. Age carries most of the signal but not all of it: age alone, chosen on each split's training side, gives ROC AUC 0.704, above only 6 of 28 BeyondArena configurations and below the best on all 9 folds; the best methods (TabPFN-3, tuned LightGBM, RealMLP) reach 0.707, a default random forest 0.689, and a lookup of each cell's death rate on the training side 0.689. So `Trivial` does not hold: sex and episode number add a small, consistent gain, and the methods gain by smoothing over age.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Chicco & Jurman 2020 call PR AUC with Alive (92.6%) as positive their 'principal indicator', with ROC AUC, MCC, F1 and others; on our folds PR AUC sits at its floor 0.926 with a best of 0.966, so it resolves models poorly (MET-9). Original rejected: PR AUC on the majority class. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): the roc_auc fallback, as proposed, over average_precision with Alive as positive (the paper's principal indicator): AUPRC on the 92.6% majority class sits between its floor of 0.926 and a best of 0.966 and resolves models poorly, while ROC AUC (about 0.7) separates them.

CC (2026-11-10, Andrej): retired (`No (Retired)`, `Trivial`): a clinician's rule, age plus about five years for men, ranks the patients within 0.001 of ROC AUC of TabPFN 3.5, and nothing learnable from the three columns lies beyond it.
- **The rule matches the best method:** on the 9 shipped splits, age alone reaches ROC AUC 0.7044, age + 5 years for men (not fitted) 0.7059, the best train-only smoother (an age spline per sex with a repeat-episode term by age, regularisation by inner cross-validation) 0.7065, TabPFN 3.5 0.7068; the rule trails TabPFN by 0.0010 ± 0.0002, while the splits' own ROC AUC runs from 0.699 to 0.710. An offset fitted per training side comes out at 3 to 5 years and scores the same (0.7058).
- **Nothing is left beyond the age-and-sex curve:** the best achievable ranking, each cell's true death rate, is estimated at about 0.709 (cell rates measured on all rows reach 0.722, of which 0.013 is the noise the same estimate shows on labels simulated from the smooth curve alone); shrinking each of the 975 cells toward the curve, with the strength chosen by inner cross-validation, takes it all the way to the curve on every split.
- **What TabPFN adds over age:** it keeps age's order on 94% of (died, survived) pairs; its gain (+0.0024) is men counted a few years older (+0.0019 net of large gains and losses) and a repeat episode in younger patients (+0.0005).
- **Why the earlier keep does not hold:** age alone below the best on every fold (Lennart, 2026-10-06) met the single-feature test of the time; the amended test counts a rule within the spread of the folds as a match, which makes the dataset a candidate to drop, not a forced retirement.
- **Curator call on top of the rules:** retired because the task is both almost solved and very simple. Almost solved: TabPFN 3.5 (0.7068) sits within about 0.002 of the best achievable ranking (about 0.709). Very simple: its gain over a naive baseline is +0.0024 ROC AUC over age alone and +0.0010 over the unfitted rule, too small to change any decision in practice; a benchmark task on which every method lands within 0.003 of a clinician's rule ranks nothing but smoothing.
Marker `Trivial` added, `v2_path` cleared, folder removed. Evidence: `~/claude_jobs/sepsis_tabpfn/` (TabPFN 3.5 on an A100, Slurm 1376270 and 1376610; `offset_fit.py`, `optimal.py`, `oracle_null.py`, `train_optimal.py`, `pairs.py`).

CC (2026-11-11, Andrej): review marks. Issue 4, on whether a simpler rule than age exists that a clinician could use: measured on the 9 shipped splits, no simpler rule matches the methods. Age rounded to 5 years 0.7030 and age in decades 0.6993 of ROC AUC against 0.7044 for age as it stands, 0.7059 for age plus five years for men and 0.7068 for TabPFN 3.5; a single cut-off reaches 0.5952 (age >= 85) to 0.6467 (age >= 65), and sex or the episode number alone 0.519 and 0.511. The retirement rests on the simplest rule that matches, so it stands; the question is left open on the review. The review moved from the folder's file into this record.

## Review

**Outcome:** added. Hospital admissions in Norway, 2011-2012, of patients with an infection or sepsis: age, sex and the
episode number predict death in hospital (7.4% died), the question of the source (Knoop et al. 2017,
https://doi.org/10.1371/journal.pone.0187990) and of Chicco and Jurman (2020,
https://doi.org/10.1038/s41598-020-73558-3). The AI recommends shipping it as defined. Reviewed on 2026-11-04 without a
panel, from the gathered evidence (the record, the earlier task-probe review; no model run exists for it); the
2026-10-27 review left one question, still open. Validity: all three features are known at admission and the outcome
follows in hospital, a direct fit. Value: age alone reaches ROC AUC 0.704 against 0.707 for the best methods and is
below the best on all 9 folds, so `Trivial` is not proven (Lennart, 2026-10-06). Quality: the 110,204 admissions hold
975 distinct feature rows; the duplicates are real patients and stay (decided). Weighed: the source's own question with
a direct fit +, a large real registry +, three features and a narrow spread between methods -. The metric review of
2026-11-04 proposes log loss for this dataset on its own page; it is not repeated here.

**Main points:** Retired (2026-11-10) with `Trivial`: age plus five years for men, not fitted, ranks within 0.001
of TabPFN 3.5 (issue 4, resolved; draft PR #77). Issues 1 to 3 are moot.

**Record judgment:** valid and narrow: a real Norwegian registry (2011-2012) with three admission facts; the methods
differ only in how they smooth over age.

**Issues for Andrej:**

1. **Ship in TabArena v0.2 as defined?**

   * **Problem:**
     - Three facts known at admission (age, sex, the number of the patient's sepsis episode) predict death in hospital,
       the source's own question, so the task is narrow by design.
     - The earlier flags are settled: `Trivial` does not hold (Lennart, 2026-10-06) and the metric is the ROC AUC
       fallback over the paper's precision-recall area on the 92.6% survivors (Lennart, 2026-10-21).
     - Ship as defined, or name what is missing?
   * **Background:** the 110,204 admissions are of 84,811 patients and hold 975 distinct feature rows; the copies are
     real patients who share age, sex and episode number, and predicting from these three fields is the source's
     question, so they stay[^1a]. With no patient id, a patient's repeat admissions can fall on both sides of a
     split, but the three features hardly tell patients apart. The Korean cohort (137 patients) and the paper's
     Sepsis-3 study cohort are left out on purpose (`curation_comments`).
   * **Experiments:** from the task-probe review of 2026-10-06 (9 folds): age alone, chosen on each split's training
     side, ROC AUC 0.704, above only 6 of 28 BeyondArena configurations and below the best on every fold; the best
     methods (TabPFN-3, tuned LightGBM, RealMLP) 0.707; a default random forest 0.689; a lookup of each cell's death
     rate on the training side 0.689[^1b]. On the paper's metric, the precision-recall area with survivors as the
     positive class sits between its floor of 0.926 and a best of 0.966.
   * **Effect on the task:** sex and episode number add a small, consistent gain over age, and the methods gain by
     smoothing over age; the benchmark tests how methods use few features on many rows.
   * **Sources:** Chicco D, Jurman G, "Survival prediction of patients with sepsis from age, sex, and septic episode
     number alone", Scientific Reports 2020;10(1):17156, https://doi.org/10.1038/s41598-020-73558-3; the rows are the
     S1 Dataset of Knoop et al., PLoS ONE 2017, https://doi.org/10.1371/journal.pone.0187990.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 110,204 admissions, three features, random split, ROC AUC | the source's own question with a direct fit; `Trivial` refuted fold by fold | little room between methods (0.689 to 0.707) |
     | B | Retire | the folder goes, the record gets `No` | none found | a valid task with a real if small signal leaves[^1c] |

   * **Recommendation:** A, a valid task by design whose flags are settled. **Decision:** ship as defined (A), or
     retire (B)?

   [^1a]: **LEAK-18** (Should): few features and plausible repeats are natural; keep them and say so. This dataset
     is the rule's case. **LEAK-16** (Must): duplicate rows need a decision every time.
   [^1b]: **TP-4** (Must): `Trivial` needs proof: the raw feature, chosen on each split's training side, has to match
     or beat the methods fold by fold. This dataset is the rule's case for "no, kept".
   [^1c]: **TP-2** (Should): a small but real signal is no reason to retire; retire, fix or keep for a concrete reason
     found in the task itself.

   **Resolved (2026-11-10, Andrej):** moot, the dataset is retired with `Trivial` (issue 4).

2. **Time basis and split: keep the random split, tagged as forced from temporal, or group by the patient rebuilt from the row order?**

   * **Problem:**
     - Admissions arose over 2011-2012 and no date survives, but the raw file keeps each patient's admissions in consecutive rows in episode order: 84,811 rows open a run at episode 1, exactly UCI's count of patients.
     - The record's collection facts hold (`Samples: Over Time`, `Time: Lost`, `Target: Varying Delay`), because an order inside each patient does not date the rows[^2a]; the definition splits at random and names no time basis.
     - A later admission exists only if the patient survived the earlier one, so time reaches the target through the patient, and the use case scores later admissions: no prototype fits, and the split is forced, at random or grouped by patient[^2b].
   * **Background:**
     - The rebuild: a row continues the patient of the row above when the sex is the same, the episode one higher and
       the age the same or one more. It links 23,173 of the 25,393 repeat admissions (91%); the rest skip an episode
       or change age by more than a year.
     - Deaths sit at the end of a patient's run: 8,095 of the 8,105 deaths are on a patient's last row, and the
       earlier rows die at 0.04%.
     - Across patients the order may follow the first admission: within every age band the admissions per patient
       fall toward the end of the file (ages 60-75: 1.45 in the first tenth, 1.18 in the last), as they would if the
       patients admitted late had less of the window left. No calendar can be rebuilt from it.
   * **Experiments:** the leak test across the split (Slurm job 1366177; LightGBM on the three features, 5 folds x
     3 repeats, ROC AUC): random folds 0.7038 (sd 0.003), folds grouped by the rebuilt patient 0.7038 (sd 0.004).
     Under random folds 31% of the test rows have another admission of the same patient in training, but the three
     features take only 975 distinct values, so no model can tell which.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | nothing to change | the notes say "there should be no temporal leakage", which the patient runs qualify; the score's relation to time is not stated |
     | B | Random, tagged as forced from temporal | `ForcedIIDFromTemporal` and a `Time basis:` line with the leak test | states that the model is used on later admissions; the test across the split passes (grouping costs 0.000) | a patient's admissions still fall on both sides |
     | C | Grouped by the rebuilt patient, tagged as forced from temporal | `ForcedGroupedFromTemporal`; a patient key built from the raw row order by the rule above | no patient on both sides | a key rebuilt from the order, which 9% of repeat rows break; the same score; the use case scores returning patients too |
     | D | Stationary relation | `StationaryRelation` with its line | no forced tag | death in hospital is an outcome after admission that a later admission depends on, not a present state; the prototype needs dated data to show it |

   * **Recommendation:** B: grouping by patient changes nothing, returning patients are part of the use case, and the
     tag says what the random split stands in for. **Decision:** A, B, C or D?

   **Notes for the AI:** once PR #50 is in this working copy, on B: `data_tags = ("ForcedIIDFromTemporal",)`; in
   `curation_comments` replace the bullet "...there should be no temporal leakage" with `- Time basis:
   ForcedIIDFromTemporal: admissions of 2011-2012 with death at discharge, used on later admissions; no date survives
   (Time: Lost). The raw file keeps each patient's admissions in consecutive rows in episode order (84,811 runs from
   episode 1, UCI's count of patients), and a later admission exists only if the earlier one was survived (8,095 of
   8,105 deaths on a patient's last row). Leak test across the split: folds grouped by the rebuilt patient score as
   random folds (ROC AUC 0.7038 both, LightGBM); the three features take 975 values and cannot tell patients apart.
   Admission dates or patient ids would allow a split by time.`; the `split` sentence stays; `dataset check`. On C:
   number the patients in `_load_raw` by the rule (a new patient when the sex changes, the episode is not one higher,
   or the age falls or rises by more than one), declare the grouping on that key (out of the features), tag
   `ForcedGroupedFromTemporal`, and the same line with "grouped" in place of "random". The record keeps its facts
   either way. Scripts of the time review of 2026-11-06: `chains.py`, `order_test.py`, `sep_split.py`.

   [^2a]: **SPLIT-32** (Should): the record carries the source's collection facts; `Time: Dated` needs a date, an
     order that tracks time or a value that encodes the period, and a time order found only within each entity does
     not count. Time affects the target when a sample's target depends on samples before it (a label propagated along
     an entity).
   [^2b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give windows ships in the closest
     regime, at random or grouped by the entity when the entities recur, tagged as forced from temporal, after a leak
     test across the split; the tag stays whatever the test finds. **SPLIT-24** (Must): group only on a true id or one
     constructed exactly from the data. **SPLIT-29** (Must): an IID split is wrong when many rows share an entity that
     new data would not have and the entity carries the label.

   **Answer (AI, 2026-11-06):**

   * **Verdict under the new entity-leakage rules: entity fix, grouped on the patient rebuilt from the row order
     (C).** The release records no patient, the row order rebuilds one, and each admission keeps its own outcome, so a
     patient's admissions are grouped rather than cut to one[^2c].
   * **Is the link real?** Of the 24,161 adjacent pairs whose episode steps up by one, 95.9% agree on sex and age (the
     same or one more), which gives the 23,173 links. Rows that cannot be the same patient agree far less often:
     - two patients side by side in the file (the lower row opens a patient): 5.3% of 84,810 pairs;
     - a row and the nearest row 2 to 10 rows above it with the episode below: 5.4%;
     - a row and a random row with the episode below: 1.6% (20 draws).
     - At those rates about 60 of the 23,173 links (0.2%) may join two patients.
   * **Does the label travel?** Yes, forward: the 23,173 admissions followed by a linked later admission die at 0.04%,
     against 7.8% that their age, sex and episode predict. A later admission tells that the earlier one was survived,
     the carried-forward label the new rules name[^2d]; under random folds 31% of test rows have another admission of
     their patient in training.
   * **Is there an order?** Only inside a patient (the episode number). No calendar across patients can be rebuilt,
     so a split by time is not possible, and grouping is the split that keeps a patient's later admissions out of
     training for the earlier ones.
   * **The equal scores do not decide it:** the three features take 975 values, so no model finds the patient's
     other row today (0.7038 random and grouped), but the rules set the verdict by the link, not by the size of a
     score gap[^2c].
   * **Recommendation changes from B to C:** grouped by the rebuilt patient, tagged as forced from temporal. It costs
     no score and closes the route.
     - The key is rebuilt from the row order, which is your call.
     - 91% of repeat admissions link; the 2,220 that do not (an episode skipped, the age off by more than a year)
       start patients of their own, so some of those can still fall on both sides.

   [^2c]: **LEAK-41** (Must, draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable; in an entity fix several observations of one unit, each
     with its own label, are grouped, and a key rebuilt from the features is the curator's call. **LEAK-42** (Should,
     draft PR #62): three tests set the verdict, not the size of a score gap: is the link above a chance rate that
     keeps the data's structure, does the label travel with it beyond what the shared features predict, is there an
     order. **SPLIT-24** (Must): a key constructed from the data by a calibrated link whose chance rate shows that
     most links are real.
   [^2d]: **LEAK-43** (Should, draft PR #62): a later record of the same unit that holds the earlier record's label
     (a readmission that tells the earlier stay was survived among the examples) carries it forward; a hit is never
     natural, and the split keeps a unit's later records out of training for its earlier ones, by time or grouped by
     the unit.

   **Answer (AI, 2026-11-09):** a note on the record's facts: Andrej added `Time: Within Entity`
   (electric_motor_temperature_prediction, issue 3, b), an order that runs only inside each entity.

   * Each patient's admissions sit in consecutive rows with an episode counter, so the order runs inside a patient and
     nothing orders patients against each other.
   * The record would then carry `Time: Lost` and `Time: Within Entity`, with `Entities: Recur`. This changes neither
     the split nor issue 2's recommendation.
   * **Decision:** add `Time: Within Entity` to the record (yes), or leave the facts (no)?

   **Resolved (2026-11-10, Andrej):** moot, the dataset is retired with `Trivial` (issue 4).

3. **Rows chosen by their discharge codes: mark `Selection Bias` and set the fit to approximate?**

   * **Problem:**
     - The source chose the admissions by their ICD-10 discharge codes and left out each patient's sixth and later admissions of the window, so whether a row exists is settled at discharge and by the patient's later stays, after the prediction point.
     - A clinician at admission meets every patient with a suspected infection, also those who leave without such a code, while the definition states a direct fit and no selection.
     - Mark the selection and set the fit to approximate, or keep it direct?
   * **Background:** the source: "selected ICD-10 discharge codes"; "In patients with more than five admissions
     during the study period, the >= 6.th admission(s) were excluded from analyses" (Knoop et al. 2017,
     https://doi.org/10.1371/journal.pone.0187990). The labels of the rows kept are true; what the selection changes
     is who is scored. The cap touches at most the 782 patients with five admissions in the file.
   * **Effect on the task:** a patient whose stay ends in death or organ failure is more likely to leave with a
     sepsis code than one whose infection resolved and was coded as something else, so the cohort leans on the
     outcome's side; by how much cannot be measured, since the release has no admission diagnosis.
   * **Consistency:** a selection the deployed setting does not share is marked `Selection Bias` with an approximate
     fit (website_phishing, naticusdroid issue 2)[^3a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | fit direct, no marker | no change | the cohort is settled after the prediction point and the fit does not say so |
     | B | Name the selection | record marker `Selection Bias`; `fit="approximate"`; one `fit_reason` sentence | states who is scored; follows the other selected cohorts | none found |

   * **Recommendation:** B: the rows are chosen at discharge, which the clinician at admission cannot do.
     **Decision:** keep (A) or name the selection (B)?

   **Notes for the AI:** on B, `fit="approximate"` and append to `fit_reason`: "The admissions were chosen by their
   discharge codes (infection, systemic inflammation, sepsis, septic shock), and each patient's sixth and later
   admissions of the window were left out, so the cohort is settled at discharge; patients admitted with a suspected
   infection that was coded otherwise are missing." The marker `Selection Bias` on the record with a `CC (<date>,
   Andrej):` line and `Andrej` in `checked_by`; `dataset check`.

   [^3a]: The `Selection Bias` marker: the rows are not drawn from the population the use case predicts for; the fit is
     approximate when the deployed setting does not share the selection (**USE-8**, Must; Lennart, 2026-10-27).
     **USE-3** (Must): name the prediction point and what is known then.

   **Resolved (2026-11-10, Andrej):** moot, the dataset is retired with `Trivial` (issue 4).

4. **Age alone matches the best methods: keep, or retire with `Trivial`?**

   * **Problem:**
     - Age, read as it stands (older means higher risk, nothing fitted), reaches ROC AUC 0.702 against 0.705 for the
       best method family; Lennart's run of 2026-10-06 found 0.704 against 0.707, with age below the best on all 9
       folds by about 0.003.
     - Since 2026-11-10 a feature or rule that matches the methods makes the dataset a candidate to drop, and the
       curator decides[^4a]; Lennart's keep read the earlier test, where age staying below the best on every fold
       meant `Trivial` was not proven.
     - Keep as a task by design, or retire with `Trivial`?
   * **Background:**
     - Age is the natural core of survival, which the test expects to dominate; the test's case list names this
       dataset as kept for that reason, a row that the decision would change.
     - The other two features (sex, episode number) add 0.003 of ROC AUC. The methods differ only in how they smooth
       over age (issue 1).
     - Your principle of 2026-11-10: if nothing learnable from the data beats a rule not fitted on it, the data cannot
       be used for prediction.
   * **Experiments:** task probe on the shipped data (5 of the 9 splits, untuned families; Slurm array 1375808):

     | Method | ROC AUC | Skill over the dummy |
     |---|---|---|
     | Linear | 0.705 | 0.409 |
     | LightGBM | 0.698 | 0.396 |
     | Random forest | 0.690 | 0.380 |
     | Age alone (chosen on all 5 training sides) | 0.702 | 0.404 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | ships as defined; issue 1 decides the rest | the source's own question; a large real registry | methods are ranked on smoothing one variable |
     | B | Retire with `Trivial` | `No (Retired)`, folder removed | follows your principle: the methods learn 0.003 over age | removes the source's own question |

   * **Recommendation:** B: the methods add 0.003 of ROC AUC over age read as it stands, which is the "match" the
     amended test names. **Decision:** A or B?

   **Notes for the AI:** on B, `suggestion: No (Retired)`, marker `Trivial`, a `CC (<date>, Andrej):` line with the
   table, the folder removed and `v2_path` cleared, the CHANGELOG entry; the TP-4 case list moves sepsis_survival
   from kept to retired; issues 1 to 3 close with it.

   [^4a]: **TP-4** (Must, amended 2026-11-10 in PR #57): a raw feature chosen on each split's training side, or a
     rule not fitted on these data (a published formula, the field's definition, a textbook or clinical score), is
     tested against the methods fold by fold; one that beats them proves `Trivial`, one that matches them makes the
     dataset a candidate to drop, and the curator decides.

   **Andrej (2026-11-10, discuss):** Also add TabPFN3.5

   **Answer (AI, 2026-11-10):** TabPFN 3.5 beats age alone on all 9 shipped splits, by 0.0024 of ROC AUC: keep, or retire anyway?

   * **Problem:**
     - On the shipped 9 splits, TabPFN 3.5 reaches ROC AUC 0.7068 against 0.7044 for age alone, ahead on 9 of 9 splits (+0.0024 ± 0.0004).
     - Logistic regression on the three columns one-hot does not beat age (0.7036, ahead on 3 of 9), so of the methods tried only TabPFN learns anything past age.
     - The gain is consistent but about a fifth of the spread of the splits' own AUC (0.699 to 0.710), so it is a beat in the strict sense and next to nothing in size.
   * **Background:**
     - Read strictly, the amended test makes a method that beats the feature on every fold no candidate; read as "learns nothing measurably better", 0.002 of AUC is a match.
     - Log loss below the class shares: TabPFN 3.5 7.6% (0.2426 against 0.2627), logistic regression 7.3%; age alone gives no probabilities.
   * **Experiments:** the 9 shipped splits (3 x 3), TabPFN 3.5 default on an A100 (Slurm job 1376270), all training rows; `~/claude_jobs/sepsis_tabpfn/results_spot.csv`:

     | Method | ROC AUC | Minus age (± SE) | Splits ahead of age | Log loss |
     |---|---|---|---|---|
     | Age alone, as it stands | 0.7044 | | | |
     | Logistic regression, one-hot | 0.7036 | -0.0008 ± 0.0005 | 3 of 9 | 0.2435 |
     | TabPFN 3.5 | 0.7068 | +0.0024 ± 0.0004 | 9 of 9 | 0.2426 |
     | Class shares | 0.5 | | | 0.2627 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep (implemented) | ships as defined; issues 1 to 3 decide the rest | TabPFN beats the feature on every split, so the strict test is not met | the benchmark ranks methods on a 0.002 gain over one variable |
     | b | Retire with `Trivial` | `No (Retired)`, folder removed, TP-4 case row moves to retired | follows your principle: 0.002 of AUC is nothing learnable worth ranking | sets "beats by a negligible margin" as a match, which the test should then say |

   * **Recommendation:** b, with one clause added to the test that a consistent gain too small to matter (here a fifth of the splits' spread) counts as a match. **Decision:** a or b?

   **Resolved (2026-11-10, Andrej):** retire with `Trivial` (b), in chat after the follow-up runs. A clinician's rule, age plus five years for men, matches the best method within the spread of the folds, and nothing learnable lies beyond the age-and-sex curve. In draft PR #77 (on #75): the record `No (Retired)` with `Trivial`, a CC line and `Andrej` in `checked_by`, `v2_path` cleared, the folder removed, the TP-4 case row and case list, the evidence.md example and the CHANGELOG entry.

   | Method, 9 shipped splits | ROC AUC | Minus TabPFN 3.5 (± SE) | Fitted on the data? |
   |---|---|---|---|
   | Age alone | 0.7044 | -0.0024 ± 0.0004 | no |
   | Age + 5 years for men | 0.7059 | -0.0010 ± 0.0002 | no |
   | Age + offset for men fitted per training side (3 to 5 years) | 0.7058 | -0.0011 ± 0.0002 | yes |
   | Age spline per sex + repeat episode by age (inner-CV regularisation) | 0.7065 | -0.0003 ± 0.0001 | yes |
   | TabPFN 3.5 | 0.7068 | | yes |
   | Best achievable: cell death rates, the noise of small cells removed | about 0.709 | | |

   **Andrej (2026-11-11, discuss):** Isnt there a simpler rule than just using age that a clinician could use?

   **Answer (AI, 2026-11-11):** measured; no rule simpler than age matches the methods, so the
   retirement stands on the rule that decided it. The numbers and what to do with them are issue 5.

5. **Does the `Trivial` retirement stand, now that no simpler clinician rule matches the methods?**

   * **Problem:**
     - A rule simpler than a continuous age score is a cut-off ("over 75") or a coarse band (decades), which is what
       a clinician applies at the bedside.
     - Every such rule loses to age read as it stands, by 0.005 (five-year steps) to 0.11 of ROC AUC (a single
       cut-off), so none of them matches the methods.
     - Sex and the episode number carry almost nothing on their own (0.519 and 0.511).
   * **Background:** ROC AUC scores a ranking, so a yes/no rule reaches only the one point its cut-off gives and
     loses to the same information read as a score; the task declares ROC AUC. The rule that decided the retirement,
     age plus five years for men, is unfitted and as simple as a score can be: read the age off the chart, add five
     for a man.
   * **Experiments:** the 9 shipped splits (3 x 3), no rule fitted on the data, TabPFN 3.5 from the run of
     2026-11-10; mean ROC AUC over the splits, and for a yes/no rule the share of admissions it flags
     (`~/claude_jobs/marks_b7/sepsis_survival_minimal_clinical_records/simple_rules.py`; nothing is fitted, so no
     Slurm job):

     | Rule | ROC AUC | SD over splits | Flagged |
     |---|---|---|---|
     | TabPFN 3.5 (for reference) | 0.7068 | | |
     | Age + 5 years for men | 0.7059 | 0.0046 | |
     | Age, as it stands | 0.7044 | 0.0043 | |
     | Age rounded to 5 years | 0.7030 | 0.0040 | |
     | Age in decades | 0.6993 | 0.0036 | |
     | Age in 20-year bands | 0.6885 | 0.0032 | |
     | Age >= 75, or >= 70 for men | 0.6486 | 0.0051 | 44% |
     | Age >= 65 | 0.6467 | 0.0044 | 58% |
     | Age >= 75 | 0.6434 | 0.0044 | 39% |
     | Age >= 80 | 0.6313 | 0.0025 | 29% |
     | Age >= 85 | 0.5952 | 0.0044 | 17% |
     | Male | 0.5189 | 0.0067 | 53% |
     | Episode number | 0.5105 | 0.0041 | |

   * **Effect on the task:** none: the retirement was decided on the rule that matches the methods, and no simpler
     rule does.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The retirement stands as decided (implemented) | nothing changes | the deciding rule is already the simplest that matches the methods | a cut-off a clinician applies at the bedside is not what decided it |
     | B | A, and the table above stays with the case of the unfitted-rule test[^5a] | the case row points at these numbers | shows what a simpler rule costs, for the next dataset the test meets | one more line to carry |
     | C | Reopen the retirement | the dataset returns, since no bedside rule matches the methods | a yes/no rule loses 0.06 of ROC AUC to the methods | the test compares unfitted rules on the metric the task declares, and age as it stands meets it |

   * **Recommendation:** A, with B: the numbers belong to the case, not to a new decision. **Decision:** A, B or C?

   [^5a]: **TP-4** (Must, amended 2026-11-10): a rule not fitted on these data (a published formula, the field's
     definition, a textbook or clinical score) is tested against the methods fold by fold; one that beats them
     proves `Trivial`, one that matches them makes the dataset a candidate to drop, and the curator decides.

## Reference

@article{chicco2020survival,
  title={Survival prediction of patients with sepsis from age, sex, and septic episode number alone},
  author={Chicco, Davide and Jurman, Giuseppe},
  journal={Scientific reports},
  volume={10},
  number={1},
  pages={17156},
  year={2020},
  publisher={Nature Publishing Group UK London}
}
