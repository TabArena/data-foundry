---
unique_name: allstate_claims_severity
name: Allstate_Claims_Severity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Anonymized
tags:
- Larger IID Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2016'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/allstate-claims-severity
- https://www.openml.org/search?type=data&id=42571
notebook_path: datasets/beyond_iid/new_iid/allstate_claims_severity/allstate_claims_severity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/allstate_claims_severity/dataset.py
source_row: 645
type_adapter_id: curation-record-v1
---

## Comments

CC: "Predict amount of insurance claims. Data anonymized. Unclear whether date is given or temporal split is required. Kaggle challenge; data does not allow us to remove/avoid temporal split or detect it from meta-data"

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source mae — Mean Absolute Error (https://www.kaggle.com/competitions/allstate-claims-severity (Kaggle API evaluationMetric)).

**Assessment (AI, 2026-10-21):** the loss ships on a log scale again (`np.log`, as before today's change) and is scored by the competition's MAE on the loss as published, after the inverse (`Metric.source("mae", target_transform="log")`, MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: the host's claim-cost task and MAE are kept, methods spread (RMSE 0.531 to 0.565 on the log scale, mean 0.814), no copy or leak found. Priority 3: gap 1, use case 0, source 0, shape 1, risk -0.

CC (2026-11-10, Andrej): review page marks: ship as defined (issue 1, decided 2026-11-04); the split stays random over claims, natural in effect, with the twins (7,654 claims sharing all 14 numbers, a link 56% to 75% real, residual correlation 0.07, grouping costs 0.0002 RMSE) noted in `curation_comments` (issue 2, option a: "We go with Random, tagged forced from temporal."); time basis forced from temporal (issue 3, option B): `ForcedIIDFromTemporal` added to `data_tags` with its `Time basis:` bullet (claims over an unstated period, the id a random draw).

## Review

**Outcome:** added. Allstate's Kaggle competition of 2016, "How severe is an insurance claim?": 188,317 claims with
116 categorical and 14 numeric attributes whose names and meanings are hidden, the target the claim's cost (`loss`),
shipped on a log scale and scored by the competition's mean absolute error on the cost as published, on random claims
(the file has no claim dates). The AI recommends shipping it as defined. Reviewed without a review panel, from the
gathered evidence: the record, the BeyondArena results on the shipped data and checks on the shipped data; there is no
model run for it. Validity: the definition keeps the competition's task (the cost of a filed claim) and its
metric; the attributes are anonymised (`Anonymized`), so when each is recorded cannot be checked; the shipped data has
no exact copy of a feature row across the split (one copy is dropped). Value: on the one BeyondArena fold the methods
spread from RMSE 0.531 (TabPFN-3.5) to 0.565 (linear model) on the log scale, against 0.814 for the mean; the best
single raw column (`cat80`) reaches 0.713. Quality: nothing open. Weighed: the insurer's own claims and the
competition's metric +, anonymised attributes and no claim dates -.

**Main points:** All settled (2026-11-10): ship as defined (issue 1), the random split with the twins noted (issue 2,
a), tagged forced from temporal (issue 3, B).

**Record judgment:** valid, and the record's fields match the definition. The use case is the host's ("predicting the
cost, and hence severity, of claims", to improve its claims service); fit `approximate`, as the definition says, since
the attributes' timing cannot be checked and random claims of one undated period stand in for the claims to come. Like
the other undated snapshots of the benchmark, the split is plain IID and not tagged as forced from temporal (a note
across datasets, not an issue here). The metric review page keeps the competition's MAE.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing is open: the definition keeps the competition's task and metric, and no check found a leak, a copy
       across the split or a spread problem.
   * **Background:** what was checked, on the shipped BeyondArena data (the v0.2 definition has the same rows and
     columns): no exact copy of a feature row (one was dropped before), so no test row has a copy in training; the
     hidden-group probe sweep of 2026-10-14 over all definitions found no hidden group here; the attributes are masked
     by the host, a known risk the `Anonymized` marker covers[^1a].
   * **Experiments:** BeyondArena, one fold, RMSE on the log of the cost: TabPFN-3.5 0.531, tuned RealMLP 0.532,
     tuned CatBoost 0.534, tuned LightGBM 0.536, random forest 0.557 to 0.561, linear model 0.565, the mean 0.814; the
     best single raw column 0.713. The methods spread, so the dataset stays on value[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | nothing changes | the host's own claims, task and metric; methods spread | attributes anonymised; one undated period |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | less weight on anonymised Kaggle data | no defect found; the host's own claims and metric leave |

   * **Recommendation:** A, nothing found that changes the task. **Decision:** ship (A), or retire (B)?

   [^1a]: **LEAK-32** (Should): masked or anonymised features that may hide a transform are a known risk of anonymised
     data, covered by its tag and the `Anonymized` marker: no action.
   [^1b]: **TP-3** (Must): if tuned methods spread, keep the dataset.

   **Resolved (2026-11-04, Andrej):** ship as defined (A); the split question is open in issue 2.

2. **Keep the random split over claims, tagged as forced from temporal?**

   * **Problem:**
     - The claim id is a random draw, not a time order or a group: Kaggle's training and test claims interleave at
       random over one id range, and neither the cost nor the attributes change along the ids.
     - About 4% of claims share all 14 numeric attributes with another claim (perhaps the same policy or car), and
       the state-like column `cat112` holds a region, but holding either out together changes the score little or
       not at all for the twins.
     - By its use case the task is temporal (price claims filed tomorrow from past ones), but the release has no
       dates, so the rules ship it IID with the tag forced from temporal, which the definition lacks[^2a].
   * **Background:** the 313,864 ids (188,318 training, 125,546 Kaggle test) are drawn from 1 to 587,634, with 47%
     of that range unused. `cat112` has 51 levels, as many as US states plus DC (median 1,331 claims, 30 to 25,148).
     The claims that share all 14 numbers always share 19 categorical columns too (among them `cat104` to `cat116`)
     and differ in a median of 14 other categorical columns, against 28 for random pairs; their ids lie as far apart
     as random ids.
   * **Experiments:** all on Kaggle's train.csv (re-downloaded 2026-11-04), LightGBM on the 130 shipped features
     with the log of the cost, RMSE on the log scale (lower is better) and MAE on the cost:

     | Check | Result |
     |---|---|
     | Share of training ids per id decile | 59.6% to 60.4% in every decile; runs of train and test ids as long as coin flips give (151,334 against 150,656) |
     | Cost over 20 id bins | mean log cost 7.670 to 7.696, no trend (Kruskal p = 0.87); rank correlation with the id 0.00001 |
     | Neighbouring ids | cost of id and id + 1 (60,400 pairs) correlates 0.004; with the mean of the 10 ids around it 0.003 |
     | Attributes over the id | largest rank correlation 0.005 |
     | Model telling low from high ids (adversarial) | ROC AUC 0.501 (5 folds); training against Kaggle's test rows 0.499 |
     | Train on the first 80% of ids, test on the last 20% | 0.535 (MAE 1,136), against 0.538 to 0.541 (MAE 1,148 to 1,166) for random 80/20 splits |
     | The id and its gaps to the neighbouring ids added as features | 0.5385 against 0.5380 without them: no id leak |
     | 5 folds: random / twins held out together / by `cat112` / by `cat116` (326 levels) / by the block `cont1` to `cont13` | 0.5380 / 0.5382 / 0.5510 / 0.5409 / 0.5385 (MAE 1,145 / 1,146 / 1,166 / 1,150 / 1,146) |
     | Same 130 features on two rows | 1 pair in training (dropped), 4 Kaggle test rows match a training row |
     | Twins (same 14 numbers; 7,654 claims, 4.1%) | the twin's cost predicts a claim's a little (correlation 0.19, against -0.02 with shuffled costs), but it is already in the features: held out together, the twins score 0.551 against 0.550 |

   * **Effect on the task:** none on rows, splits or scores under B; the regime metadata and a note change.
   * **Consistency:** porto_seguro (another insurer's anonymised Kaggle table, its issue 2 of today) found the same
     shuffled id and proposes the same tag; australian_vehicle_insurance_2004_2005, an undated insurance table,
     ships IID tagged forced from temporal after the same leak test (2026-11-02, Andrej).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no tag (implemented) | nothing changes | none found | departs from the forced-split rule and the insurance precedent; the score's temporal meaning is not stated |
     | B | Random, tagged forced from temporal | `data_tags` gain `ForcedIIDFromTemporal`; a note says what a dated release would change | follows the rule and australian_vehicle_insurance; the leak test passes (no shared rows, no order effect, twins and regions do not leak) | none found |
     | C | Grouped by `cat112` (state) | folds hold out whole states | tests a new market | new claims come from the same states, so it tests a case the insurer does not have; scores worse (0.551 against 0.538) for that reason only |
     | D | Temporal by id | train on low ids, test on high ids | none found | the id is a random draw, not time: a random split under another name (0.535) |

   * **Recommendation:** B: the data allows no temporal split and needs no grouped one, and the tag says what the IID
     score stands for. **Decision:** random as now (A), random tagged forced from temporal (B), or grouped by state
     (C)?

   [^2a]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime that keeps the rows, tagged as forced from temporal; it ships only when a leak test across
     the split finds none (no shared outcome, no hidden group, no order dependence). **SPLIT-29** (Must): an IID split
     is wrong when many rows share an entity new data would not have and the entity carries the label.
     **SPLIT-22** (Should): the raw file order can be the time order; here it is not.

   **Andrej (2026-11-04, discuss):** Are you sure that the data should not actually be a temporal or grouped split?

   **Answer (AI, 2026-11-04):**

   * You asked whether the split should be temporal or grouped.
   * Temporal: yes by its use case, no in the data. The id is a random draw: train and test ids interleave like
     coin flips, a model cannot tell low from high ids (ROC AUC 0.501), and the cost does not drift or cluster along
     the ids (neighbour correlation 0.004). Training on the first 80% of ids scores like a random split (0.535
     against 0.538 to 0.541). So no time order can be recovered, and the id leaks nothing (adding it changes 0.5380
     to 0.5385).
   * Grouped: no. No claim repeats (1 duplicate pair of 188,318). 4.1% of claims share their 14 numbers with
     another, perhaps the same policy; holding these out together changes nothing (0.5382 against 0.5380). The
     state-like `cat112` costs 0.013 when whole states are held out, but new claims come from the same states.
   * That is the forced-from-temporal case: ship IID with the tag (B). **Decision:** A, B or C?

   **Answer (AI, 2026-11-06):** the time framing, from today's review of how each dataset's data arrives.

   * The tag and its `Time basis:` line are now issue 3, so this issue decides the split only: random claims (A and
     B are the same folds) or grouped by state (C).
   * How the data arrives supports the random split: claims are filed one by one over a period Allstate never
     states, the cost follows after a settlement time that differs by claim, and the release keeps no time (the id is
     a random draw), so no window by filing date can be built and random is the closest regime that keeps the
     rows[^2b].
   * Grouping by state answers another use case (pricing a market the insurer does not serve yet), not the lost time:
     new claims come from the same states.

   **Notes for the AI:** on B, add `ForcedIIDFromTemporal` to `data_tags` next to `Anonymized`, as
   australian_vehicle_insurance_2004_2005 declares it; a split note in `curation_comments` in that definition's form
   (the use case, no dates, the id is a random draw, the leak test numbers above, recover dates if a later release
   has them); one sentence in `fit_reason`; `dataset check`. Then the record's CC line covers issue 1 (A), the split
   (B) and the metric (MAE on the cost, checked and kept), with `Andrej` in `checked_by`. Kaggle's bundle zip
   holds an older inner `train.csv.zip` (2018) whose `train.csv` has 12,550 malformed lines appended after row
   188,318; pandas cannot parse it; the top-level `train.csv` is clean, and the shipped 188,317 rows (after the one
   duplicate) match it.

   [^2b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows (dates lost)
     ships in the closest regime that keeps the rows, tagged as forced from temporal, after a leak test across the
     split. **SPLIT-32** (Should): when samples, features and the target arrive is information for the split.

   **Answer (AI, 2026-11-06):**

   * **Problem:**
     - Under the new entity-leakage rules the twins (7,654 claims equal in all 14 numbers and in 19 categoricals)
       are not look-alikes: most links are real, and their costs agree a little beyond what every column predicts,
       so they are not natural[^2e1].
     - The release has no policy id or date, so the only key is the twins' own values, built by us.
     - Keep the random split as natural in effect (a), or hold each twin group out whole (b)?
   * **Experiments:** Kaggle's train.csv; LightGBM on the log cost, folds that keep twins together:
     - Link mostly real: cont1 to cont13 are a coarse profile (15,997 profiles) and cont14 a fine number (18,740
       values) unrelated to it. Shuffling cont14 over all claims leaves 1,884 claims with a twin, against 7,654.
       Within a profile, 4,049 pairs share a cont14 value, against 1,630 to 1,790 one to three values apart. So
       56% to 75% of the links are real.
     - The cost travels a little: after a model of all 130 columns, twin residuals correlate 0.07 (95% interval
       0.04 to 0.11), against -0.01 for near twins (same profile, nearest other cont14) and 0.01 for shuffled twins.
       After the 33 shared columns alone the twins correlate 0.13.
     - Worth nothing measurable: even a perfect lookup of the twin's residual moves the RMSE on twin rows from 0.552
       to 0.551, and on all rows by less than 0.0001. Holding twins out together costs 0.0002 (0.5382 against
       0.5380, the table above).
     - No order: the id is a random draw (ROC AUC 0.501). Twin ids lie as far apart as random ones (median gap
       167,200 against 171,144), none within 10.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random, natural in effect (implemented) | the issue's A or B; a note gives the twins, the 2.7% to 2.8% of test rows with a twin in training and the 0.07 | like liberty_mutual_fire_peril_loss_cost, a real link whose label moves no score | a model that reads training rows when predicting can use a twin's cost; departs from the rule once the cost travels |
     | b | Grouped by twin | the 3,756 twin groups (2 to 5 claims) held out whole, every other claim alone; issue 3's tag becomes `ForcedGroupedFromTemporal` | no twin across the split; costs 0.0002 RMSE; keeps every row | a key built by us on anonymised columns, 25% to 44% of its links chance[^2e2] |

   * **Recommendation:** b: the cost travels with a link that is mostly real and exact on 33 columns, and holding
     it out costs nothing. a if the key seems too uncertain; then the twins stay as a note. Grouping by state (C)
     stays not recommended. **Decision:** a or b?

   **Notes for the AI:** on b, in `_clean` after the duplicate drop, `twin` = the factorized 14 `cont` values (a
   claim without a twin forms its own group), `Grouping(on="twin", labels="per_sample", prediction_unit="row",
   context="none", definition=...)`, the column out of the features; a curation bullet with the three tests above;
   record `required_split` Grouped; rebuild and check that no test row has a twin in training.

   [^2e1]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one verdict: natural
     (distinct look-alikes, random split), entity fix (units recovered from the source or rebuilt from the features;
     several observations of one unit, each with its own label, grouped), temporal fix, or not recoverable (the
     identifiable copies dropped). A key rebuilt from the features is the curator's call. **LEAK-42** (Should; draft
     PR #62): three tests set the verdict: a link above a chance rate that keeps the data's structure, a label that
     travels with the link beyond what the shared features predict, and an order. A real link that carries no label
     is no leak.
   [^2e2]: **SPLIT-24** (Must): group on a true id, or on one constructed from the data, either exactly (identical
     values in the columns that define the entity) or by a calibrated link whose chance rate shows that most of its
     links are real. Never on a hash of the feature vector standing in for an unknown entity. **SPLIT-25** (Must):
     when the real groups matter and cannot be recovered, never group on a guess.

   **Andrej (2026-11-06, discuss):** Are you sure about your recommendation? After all it is unclear if your links are
   really about the same entity and the RMSE barely changes

   **Answer (AI, 2026-11-09):** no: with that uncertainty, a is the better recommendation. The key is our own guess, and
   nothing measurable rides on it.

   * **The key is too uncertain:** the chance test puts 56% to 75% of the twin links on one claim recorded twice; the
     rest are coincidences of a coarse profile and a common `cont14` value. Grouping on the key would tie a quarter to
     almost half of the twin groups on a coincidence, and the rules keep a key rebuilt from the features case by case,
     by how certain it is that the key works[^2f1].
   * **Nothing measurable rides on it:** the cost travels a little (twin residuals correlate 0.07), but a perfect lookup
     of the twin moves the RMSE on twin rows from 0.552 to 0.551, and grouping costs 0.0002 overall.
   * **Recommendation:** a: the random split stays, natural in effect, with a note on the twins (7,654 claims, 2.7% to
     2.8% of test rows with a twin in training, a residual correlation of 0.07, a link 56% to 75% real), as for
     liberty_mutual_fire_peril_loss_cost. **Decision:** a or b?

   **Notes for the AI:** on a, a curation bullet with the numbers above; issue 3 (the time basis) is unaffected; the
   cross-dataset item on entity leakage now lists allstate as a.

   [^2f1]: **LEAK-41** and **SPLIT-24** (draft PR #62): a key rebuilt from the features is decided case by case, by how
   certain it is that the key works; a link calibrated against chance may group rows.

   **Andrej (2026-11-10, discuss):** We go with Random, tagged forced from temporal.

   **Resolved (2026-11-10, Andrej):** a: the random split over claims stays, natural in effect; a curation bullet gives
   the twins (7,654 claims, 2.7% to 2.8% of test rows with a twin in training, residual correlation 0.07, a link 56% to
   75% real, grouping costs 0.0002 RMSE) and why the split does not group on the rebuilt key. The tag is issue 3.

3. **Time basis: name the random split forced from temporal (`ForcedIIDFromTemporal`)?**

   * **Problem:**
     - Claims are filed one by one over a period Allstate never states, the cost follows after a settlement time that
       differs by claim, and the release keeps no time: the id is a random draw (a model tells low from high ids at
       ROC AUC 0.501).
     - The record's collection facts fit what was found (`Samples: Over Time`, `Time: Lost`, `Target: Varying
       Delay`), but the definition names no time basis, so nothing says what the random score stands for.
     - The use case prices claims filed after the data and a claim's cost can move with time, so of the time bases
       only the forced tag fits: name it, or another one?
   * **Background:** the questions that tell the time bases apart[^3a]:
     - Can time affect the target? Yes: a claim's cost follows the repair, medical and legal costs of its year and
       the mix of claims.
     - Does the use case predict for a time after its data? Yes: Allstate estimates the cost when a claim is filed,
       from claims already settled.
     - One shared prediction moment? No: each claim is predicted at its own filing date.
     - Does arrival over time move the target? Argued from the source, as nothing dated can measure it: costs inflate
       and the claim mix shifts; with the time lost that is the forced case[^3b].
     - `Snapshot` does not fit, as the use case does not fill in claims of a period already covered;
       `StationaryRelation` does not fit, as a cost is not a present state and no dated data shows the relation flat.
   * **Experiments:** the leak test across a forced split is issue 2's table: no order effect along the id (first 80%
     of ids to the last 20%, RMSE 0.535 against 0.538 to 0.541 on random splits), no shared outcome through the twins
     with the same 14 numbers (held out together 0.5382 against 0.5380), no copy of a feature row across the split.
     Whether claims of one period share their outcome cannot be tested without dates.
   * **Unknown:** whether `loss` is the settled cost or a figure developed up to the extract; if the latter, the
     newest claims carry partial costs, which only a dated release could show.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | `data_tags = ("Anonymized",)`; `dataset check` notes a split that is not temporal and does not say why | nothing changes | the score's meaning in time is not stated |
     | B | Forced from temporal | the tag `ForcedIIDFromTemporal` and a `Time basis:` line naming the unstated period, the random id and what a dated release would change | says what the random score stands for; issue 2's leak test passes; follows australian_vehicle_insurance_2004_2005 | none found |
     | C | Stationary relation | the tag `StationaryRelation` and a line arguing that a claim's cost follows its attributes whenever it is filed | none found | claim costs move with prices and the claim mix; no dated data to measure it on |

   * **Recommendation:** B: a forward use case whose time is lost is what the forced tag names; it holds for both
     random options of issue 2. **Decision:** no time basis (A), forced (B) or stationary relation (C)?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("ForcedIIDFromTemporal", "Anonymized")` and the
   curation bullet "- Time basis: ForcedIIDFromTemporal: claims filed one by one over a period Allstate does not
   state, each cost known after a settlement time that differs by claim; the release keeps no claim date and the id
   is a random draw (a model tells low from high ids at ROC AUC 0.501; training on the first 80% of ids scores RMSE
   0.535 against 0.538 to 0.541 on random splits), so random claims stand in for the claims to come. A dated release
   would allow a split by filing date and show whether `loss` is final."; no `splits_comment` (default split); the
   record's facts stay. If issue 2 ends on C (grouped by state), the tag is `ForcedGroupedFromTemporal` instead, as a
   grouped definition refuses the IID one. On C here: `StationaryRelation` with a line giving the argument.

   [^3a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     the record keeps the source's collection facts, and a definition can name the use-case prototype it follows
     (`Timeless`, `Snapshot`, `DelayedTarget`, `StationaryRelation`) with a `Time basis:` line stating the fact behind
     it; a forward task whose time is lost or too short is forced.
   [^3b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal (`ForcedIIDFromTemporal`, or
     `ForcedGroupedFromTemporal` for a grouped split), after a leak test across the split: a row's, its unit's or its
     period's outcome shared with the other side, a hidden group, an order dependence.

   **Resolved (2026-11-10, Andrej):** B: `data_tags = ("ForcedIIDFromTemporal", "Anonymized")` and the drafted `Time
   basis: ForcedIIDFromTemporal:` bullet in `curation_comments` (claims over an unstated period, the id a random draw,
   the 80/20 id test, what a dated release would change). Rows and split unchanged; record facts unchanged.

## Reference

https://www.kaggle.com/competitions/allstate-claims-severity
