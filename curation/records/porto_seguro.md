---
unique_name: porto_seguro
name: porto-seguro
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 4
decision_markers:
- Anonymized
tags:
- Larger IID Data
- 'Samples: One Moment'
- 'Target: Later'
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2017'
domain: insurance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/porto-seguro-safe-driver-prediction
notebook_path: datasets/beyond_iid/new_iid/porto_seguro/porto_seguro.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/porto_seguro/dataset.py
source_row: 646
type_adapter_id: curation-record-v1
---

## Comments

CC: "Data from Kaggle competition. Some ordinal features, definitely interesting. Top solutions applied some interesting feature engineering. We do not know much about the features given, but from what we know about the task it might be suitable to use random splits as the task likely has been designed time-invariant as the targets are always the ground truth of what happened in the future.; -1 maps to nan, needs preprocessing. While some information are missing, it is more likely than not that a random split is appropriate enough; need to make missing values to nans!"

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric `normalized_gini_coefficient` replaced by the default `roc_auc`: for a binary target the normalized Gini is 2 x ROC AUC - 1, so both rank models the same, and a listed name is scored downstream while an unlisted one falls back to the default. The notes name the Gini. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — the competition's normalized Gini coefficient, 2 x AUC - 1 for a binary target, which ranks models the same as ROC AUC (Kaggle evaluation page).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: the host's next-year claim task with its Gini (as ROC AUC), a narrow but stable spread (0.618 to 0.646, Kendall's W 0.99), no copy or leak found. Priority 4: gap 1, use case 1, source 0, shape 1, risk -0.

CC (2026-11-04, Andrej): ship as defined (issue 1); metric checked and kept. Split: random, tagged as forced from temporal and as a delayed target (issue 2).
- **Forced from temporal:** the insurer prices next year's policies, but the release has no dates and its id is a random shuffle; the leak test passes (no shared rows, no hidden group, region-grouped folds score as random ones, 0.639).
- **Delayed target, which justifies the random split:** the holder's data is taken at the start of the policy year and the claim arrives within it, so a random split tests what pricing does at that point; the tag `Delayed Target` (SPLIT-32, PR #50) holds once the audit shows every column existed at that point.
- To do: `data_tags` and the feature audit once PR #50 is in the working copy.

CC (2026-11-09, Andrej): time basis `DelayedTarget` alone (review page issue 3, B): policy holders priced at one moment, a claim within the following year; the tag enters `data_tags` once PR #50 is in the working copy, and the feature check follows the record's `Target: Later`. The blanks in `ps_car_01_cat`, `ps_ind_04_cat` and `ps_ind_02_cat` stay (issue 4, A): "There is no evidence that this is a leak and not a real pattern. The difference in the target distributions is not too crazy, so this is not sufficient to drop."

## Review

**Outcome:** added. Porto Seguro's Kaggle competition of 2017 ("Safe Driver Prediction"): 595,206 policy holders with
37 anonymised features about the driver, the car and the region (the 20 `calc` features dropped, as the top solutions
did; -1 set to missing, as the data page defines it), the target whether the driver filed a claim in the next year
(3.6%), scored by ROC AUC, which ranks models as the competition's normalised Gini does (Gini = 2 AUC - 1), on random
policy holders. The AI recommends shipping it as defined. Reviewed without a review panel, from the gathered evidence:
the record, the BeyondArena results on the shipped data and checks on the shipped data; there is no model run for
it. Validity: the definition keeps the competition's task and its metric; the features are anonymised (`Anonymized`);
the shipped data has no exact copy of a feature row (6 were dropped). Value: on two BeyondArena folds the methods spread
from ROC AUC 0.618 (random forest) to 0.646 (TabPFN-3.5), the linear model 0.630; one of 21 configurations is tied with
the best and the ranks agree across folds (Kendall's W 0.99); the best single raw feature (`ps_car_13`) reaches 0.578.
Quality: nothing open. Weighed: the insurer's own policies, task and metric, and a clear if narrow ranking +,
anonymised features and one undated period -.

**Main points:** Ship as defined (issue 1, decided); random split decided (issue 2); `DelayedTarget` alone (issue 3,
resolved 2026-11-09); the blanks in three columns stay (issue 4, resolved 2026-11-09).

**Record judgment:** valid, and the record's fields match the definition. The use case is the host's: price a policy
by the probability that the driver files a claim within a year. The policies carry no dates, so random policy holders
of one period stand in for next year's; like the other undated snapshots of the benchmark the split is plain IID and
not tagged as forced from temporal (a note across datasets). Dropping the `calc` block rests on the top solutions'
finding that it carries nothing; the allstate_claim_prediction_challenge_1m precedent dropped columns that behave like
random draws after measuring it, and the notes could say the same once measured on the raw file.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing is open: the definition keeps the competition's task and metric, and no check found a leak, a copy
       across the split or a spread problem.
   * **Background:** what was checked, on the shipped BeyondArena data (the v0.2 definition has the same rows and
     columns): no exact copy of a feature row, so no test row has a copy in training; the hidden-group probe sweep of
     2026-10-14 over all definitions found no hidden group here; the masked features are a known risk the `Anonymized`
     marker covers[^1a].
   * **Experiments:** BeyondArena, two folds, ROC AUC: TabPFN-3.5 0.646, tuned CatBoost 0.643, tuned XGBoost 0.641,
     tuned LightGBM 0.640, linear model 0.630, random forest 0.618 to 0.629; one of 21 configurations is tied with the
     best and the method ranks agree across the folds (Kendall's W 0.99). The spread is small but stable, so the dataset
     stays on value[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | nothing changes | the host's own policies, task and metric; a stable ranking | anonymised features; a narrow spread |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | less weight on anonymised Kaggle data | no defect found; the host's own policies and metric leave |

   * **Recommendation:** A, nothing found that changes the task. **Decision:** ship (A), or retire (B)?

   **Resolved (2026-11-04, Andrej):** ship as defined (A); the split question is open in issue 2.

   [^1a]: **LEAK-32** (Should): masked or anonymised features that may hide a transform are a known risk of anonymised
     data, covered by its tag and the `Anonymized` marker: no action.
   [^1b]: **TP-3** (Must): if tuned methods spread, keep the dataset.

2. **Keep the random split over policy holders, tagged as forced from temporal?**

   * **Problem:**
     - The row id is a random shuffle, not a time order or a group: Kaggle's training and test rows interleave at
       random over one id range, and nothing in the data changes along the ids.
     - No policy holder appears twice, and the region code inside `ps_reg_03`, the one hidden grouping the data
       holds, does not change the score when held out.
     - By its use case the task is temporal (price next year's policies from past ones), but the release has no
       dates, so the rules ship it IID with the tag forced from temporal, which the definition lacks[^2a].
   * **Background:** the ids run from 0 to 1,488,027 without a gap; 595,212 are training rows and 892,816 Kaggle's
     test rows. `ps_reg_03` hides a region code: (40 x `ps_reg_03`)^2 is a whole number on every row that has
     it (5,012 values, median 49 policy holders, at most 664; 18.1% missing).
   * **Experiments:** all on Kaggle's train.csv (re-downloaded 2026-11-04), LightGBM on the 37 shipped features,
     ROC AUC:

     | Check | Result |
     |---|---|
     | Share of training rows per id decile | 39.9% to 40.1% in every decile; runs of train and test ids as long as coin flips give (mean 2.08 against 2.08) |
     | Claim rate over 20 id bins | 3.4% to 3.8%, no trend (chi-squared p = 0.64); lag-1 correlation of the target in id order 0.001 |
     | Features over the id | largest rank correlation 0.004 |
     | Model telling low from high ids (adversarial) | ROC AUC 0.500 (5 folds) |
     | Train on the first 80% of ids, test on the last 20% | 0.636, against 0.631 to 0.646 for random 80/20 splits |
     | 5 folds: random / grouped by region code / grouped by car model (`ps_car_11_cat`, 104 levels) | 0.639 / 0.639 / 0.636 |
     | Same 37 features on two rows | 6 pairs in training (dropped), 16 training rows match a test row; none with the 20 `calc` columns |
     | Same `reg` and `car` blocks / same `ind` and `reg` blocks | 1.1% / 8.7% of rows share them (at most 14 / 69 rows); the claim rate of the other rows predicts a row's claim no better than with shuffled labels (0.511 against 0.495; 0.488 against 0.497) |
     | Same region code | 0.511 against 0.482 with shuffled labels: a small regional claim level, shared by new policies of the same region |

   * **Effect on the task:** none on rows, splits or scores under B; the regime metadata and a note change.
   * **Consistency:** australian_vehicle_insurance_2004_2005, an undated insurance table priced for next year, ships
     IID tagged forced from temporal after the same leak test (2026-11-02, Andrej); blood_transfusion's issue 1
     proposes the same tag for one extract standing in for a forecast.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no tag (implemented) | nothing changes | none found | departs from the forced-split rule and the insurance precedent; the score's temporal meaning is not stated |
     | B | Random, tagged forced from temporal | `data_tags` gain `ForcedIIDFromTemporal`; a note says what a dated release would change | follows the rule and australian_vehicle_insurance; the leak test passes (no shared rows, no hidden group, no order effect) | none found |
     | C | Grouped by region code | folds hold out whole regions decoded from `ps_reg_03` | none found | new policies come from the same regions, so it tests a case the insurer does not have; scores the same (0.639) |
     | D | Temporal by id | train on low ids, test on high ids | none found | the id is a shuffle, not time: the same as a random split under another name |

   * **Recommendation:** B: the data allows no temporal or grouped split, and the tag says what the IID score stands
     for. **Decision:** random as now (A), random tagged forced from temporal (B), or grouped by region (C)?

   **Andrej (2026-11-04, discuss):** Are we sure that this is not actually a temporal or grouped task?

   **Answer (AI, 2026-11-04):**

   * You asked whether the task is really temporal or grouped.
   * Temporal: yes by its use case, no in the data. The insurer prices next year's policies, so a dated release would
     call for a temporal split. This release has no dates, and the id is a random shuffle: train and test ids
     interleave like coin flips, and a model cannot tell low from high ids (ROC AUC 0.500). So no time order can be
     recovered. That is the forced-from-temporal case: ship IID with the tag (B).
   * Grouped: no. No policy holder repeats (6 duplicate pairs of 595,206 rows). The only hidden grouping is the region
     code in `ps_reg_03`, and new policies come from the same regions. Holding out regions scores the same as random
     folds (0.639 both). Rows that share whole feature blocks do not share their claims beyond chance.
   * Recommendation: B. **Decision:** A, B or C?

   **Notes for the AI:** on B, add `ForcedIIDFromTemporal` to `data_tags` next to `Anonymized`, as
   australian_vehicle_insurance_2004_2005 declares it; a split note in `curation_comments` in that definition's form
   (the use case, no dates, the id is a shuffle, the leak test numbers above, recover dates if a later release has
   them); one sentence in `fit_reason`; `dataset check`. Then the record's CC line covers issue 1 (A), the split
   (B) and the metric (ROC AUC, the Gini, checked and kept), with `Andrej` in `checked_by`.

   **Andrej (2026-11-04, discuss):** I go with a random split, but want to work on a new tag. 

   I believe we could introduce a new tag for datasets that are not necessarily fully temporal, but also not static. In this dataset we see that the target arrives delayed from the features. So we have features given at one point where we make the prediction and the target (and potentially other features) arrive later with a delay. The new tag could be used whenever all of our available data is assumed to be available at the same time and the target was collected or arrived at some other time point, possibly varying across samples.  For these tasks it also is quite important to check that features used would also actually be available at prediction time. I want you to help me brainstorm if this tag makes sense to differentiate from forced IID and also to think which other datasets should get this tag.

   **Answer (AI, 2026-11-04):**

   * You decided the random split and asked for a new tag: rows whose features are all known at one prediction
     point, while the target (and maybe other fields) arrives later, after a delay that can differ by row.
   * What settles where it fits: the tag describes the rows, not the split. The split tags we have
     (`ForcedIIDFromTemporal`, `ForcedGroupedFromTemporal`) and the regimes (IID, grouped, temporal) say how test
     rows relate to training rows. Your tag says how a row's features relate to its own target. The two are
     independent: an undated table like this one is random and delayed-target; a dated credit book (issue dates,
     default within 36 months) is temporal and delayed-target; a sensor reading with a same-time label is neither.
   * What the rules already ask, without a tag: every task names its prediction point, and every feature must have
     existed at it[^2b]. Missingness or a fill that differs by outcome is tested[^2c]. A value cut short by the
     outcome is kept only when measured as harmless[^2d]. A temporal split leaves a gap of the label's delay[^2e].
     What is missing: nothing marks which datasets have a delayed target, nothing says the check was done column by
     column, and nothing records the delay.
   * The proposal:
     - Name, three candidates: "Delayed Target" (data tag `DelayedTarget`; your words, recommended), "Snapshot
       (Delayed Target)" (`SnapshotDelayedTarget`; says that the features are one snapshot), "Prediction Point"
       (`PredictionPoint`; names the check, but every task has a prediction point).
     - Meaning, one sentence: every feature of a row is taken at one prediction point, and the target is observed
       later, over a window or after a delay that may differ by row.
     - Where it lives: both. A `data_tags` entry in `dataset.py`, next to `Anonymized`, so it reaches the container.
       It is not a regime tag, so the split stays IID, grouped or temporal as now. A record tag of the same name in
       the vocabulary, so triage can mark it before a definition exists.
     - What it obliges: (1) a `Prediction point:` line in the notes: when the features are taken, when and how the
       target arrives, and the delay or window ("claim within the policy year"; "default within 24 months"); (2) a
       feature-availability audit, one verdict per column or block: known at the prediction point, arrives later
       (dropped, or blanked where the late cells can be found), or cannot be told (anonymised; kept with a
       potential-leak note only when the conditional test shows nothing)[^2b][^2c]; (3) fields that are fixed by
       the outcome window itself (time on risk, a follow-up length) are named and measured[^2d]; (4) with a temporal
       split, the gap covers the delay[^2e]. A framework check could refuse the tag without the `Prediction point:`
       line, as it refuses `ForcedIIDFromTemporal` next to a grouping.
     - Relation to forced from temporal: they answer different questions. `ForcedIIDFromTemporal` says the use case
       wants later rows in the test and the data cannot give them, so the score ignores drift. `DelayedTarget` says
       each row has a prediction point and its features were audited against it. This dataset needs both: new
       policies are priced next year (forced from temporal), and each policy's claim arrives within its year
       (delayed target).
   * The audit on this dataset, as a test of the idea (Kaggle's train.csv, 595,212 rows): the meanings are hidden,
     so no column can be read against the codebook. The one thing that can be tested is missingness by outcome.
     79 policy holders miss both `ps_car_01_cat` and `ps_ind_04_cat`; 33 of them claimed (41.8%, against 3.6%
     overall). `ps_ind_02_cat` missing: 40 of 216 claimed (18.5%). Kaggle's test file has the same pattern (124
     rows miss both), which does not prove the values were known at pricing. Whether this survives the other
     features is not yet tested (it needs a model run). So the tag would add a concrete open question here: are
     these records filled in after a claim?
   * Candidates among today's datasets:

     | Dataset | Fits? | Why |
     |---|---|---|
     | porto_seguro | yes | priced at the start of the policy, claim within the year; anonymised, so the audit rests on the missingness test above |
     | australian_vehicle_insurance_2004_2005 | yes, the model case | claim over the policy year; `exposure` is known only at the end and cut short by some claims, already measured and kept with a note |
     | allstate_claims_severity | yes | claim features at filing, the final cost arrives when the claim closes, a delay that differs by claim; anonymised |
     | give_me_some_credit | yes | credit file at the scoring date, 90 days late within two years; the late counters must be checked to end before that date |
     | heloc | yes | credit report at application, serious delinquency within 24 months |
     | credit_card_clients_default | yes | payment history April to September 2005, default on the October payment; one-month delay |
     | home_credit_default_risk | yes | application and earlier credits, payment difficulties later; the audit checks that every bureau and earlier record ends before the application |
     | liberty_mutual_fire_peril_loss_cost, blood_transfusion, distribution_transformers_at_cauca_department, mobile_churn, expresso_churn_prediction_1m | yes | features at a cut, outcome over a stated window (loss over the term, the next drive, the coming year, the next month, the next 90 days) |
     | bank_customer_churn, tour_travels_churn | unclear | the window for leaving is not stated, so no prediction point can be written |
     | account_debt_south_africa | no | the target is the status at the extract, the same moment as the features |
     | food_delivery_time, emscad, huntprohibited_1m, aps_failure | no | the target is a property of the row at the time (a duration, a label set at posting or review), not a later outcome of a snapshot |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Forced from temporal only (as recommended before) | `ForcedIIDFromTemporal` on this dataset; no new tag | follows the existing rule; no new vocabulary | the delayed target and its audit stay unmarked; the check stays implicit in the general leak rules |
     | B | New tag next to forced from temporal | `DelayedTarget` as a data tag and a record tag, with the prediction-point line and the per-column audit; `ForcedIIDFromTemporal` stays where the use case wants later test rows | the two facts stay separate; works with any split; makes the audit a visible duty | one more tag to apply to about 15 datasets |
     | C | New tag replacing forced from temporal for snapshot tasks | `DelayedTarget` only; `ForcedIIDFromTemporal` kept for tables without a delayed target | fewer tags per dataset | loses the note that a dated release would need a temporal split; mixes up two questions |

   * **Recommendation:** B, named "Delayed Target". Implemented later as one change: the tag in the vocabulary and
     the framework, a rule in the leak checks that points to the existing ones, then this dataset and the
     candidates above. For porto_seguro: random split (your call), `ForcedIIDFromTemporal` and `DelayedTarget`, and
     the missingness test run before it ships. **Decision:** B with the name "Delayed Target", another name, or A
     or C?

   **Notes for the AI:** nothing is implemented yet (no vocabulary, rule, `dataset.py` or record change). On B: add
   `DelayedTarget` to the allowed data tags (not to `REGIME_TAGS`), and "Delayed Target" to `tags` in
   `curation/vocabularies.yaml`; a rule next to the feature-availability rule that defines the tag and lists the
   four duties, citing the existing rules rather than restating them; optionally a check in `dataset.py` that the
   tag comes with a `Prediction point:` line in `curation_comments`. Then porto_seguro: both tags, the prediction
   point line, and the conditional missingness test on `ps_car_01_cat`/`ps_ind_04_cat`/`ps_ind_02_cat` (target on
   the other 37 features with and without the missing flags, as a batch job); the counts above come from Kaggle's
   train.csv and test.csv, `-1` read as missing.

   **Andrej (2026-11-04, in chat):** Yes, we can add this tag and create the PR on top of our current ones.

   **Resolved (2026-11-04, Andrej):** random split kept, tagged forced from temporal and justified by the new tag
   `Delayed Target` (B; SPLIT-32: a snapshot whose features exist at one prediction point and whose target arrives
   later): the tag, its rule (SPLIT-32) and the record tag on 12 records are in PR #50. Still to do here: the
   definition's `data_tags` gain `ForcedIIDFromTemporal` and `DelayedTarget` once PR #50 is in this working copy, with
   a `Prediction point:` line and the feature audit (whether `ps_car_01_cat` and `ps_ind_04_cat` missing together
   still marks claims once the other columns are known).

   [^2a]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime that keeps the rows, tagged as forced from temporal; it ships only when a leak test across
     the split finds none (no shared outcome, no hidden group, no order dependence). **SPLIT-29** (Must): an IID split
     is wrong when many rows share an entity new data would not have and the entity carries the label.
     **SPLIT-22** (Should): the raw file order can be the time order; here it is not.
   [^2b]: **USE-3** (Must): name the prediction point, when the model is used and what is known then. **LEAK-1**
     (Must): write down the prediction point first; every test asks whether a value existed at it. **LEAK-10** (Must):
     a feature holds only what existed at the prediction point and never gives the target away (out: a column
     recorded after the outcome, a value computed from the window that defines the target, missingness that encodes
     the outcome).
   [^2c]: **LEAK-38** (Should): anonymised fields that may be post-outcome, in a company's own competition data, stay
     with a potential-leak note only while their timing cannot be tested; when a conditional test measures the
     mechanism (missingness or fill differs by outcome given the covariates), the field is dropped, even if the
     host's test file carries it the same way.
   [^2d]: **LEAK-11** (Should): a value measured after the outcome that weakens the signal stays, with a note;
     australian_vehicle_insurance_2004_2005's `exposure` is the case of time on risk cut short by the outcome.
   [^2e]: **SPLIT-10** (Should): when a label is known only some time after its row, a temporal split leaves a gap of
     about the label's delay between train and test. **SPLIT-9** (Must): a training row whose label is not yet known
     at the prediction point is not in train.

3. **Time basis: `DelayedTarget` alone, now that a definition takes one basis?**

   * **Problem:**
     - Each row is a policy holder priced for the next year, the claim known after that year; the id is a random shuffle and no date survives, and the record calls the release one moment with a later target (`Samples: One Moment`, `Target: Later`), which the data can neither confirm nor refute.
     - Issue 2 was resolved on 2026-11-04 with both `ForcedIIDFromTemporal` and `DelayedTarget`, but since 2026-11-05 a one-moment release is not forced, and the definitions of PR #50 refuse two time bases[^3a].
     - If the policies were priced at one date and the claims counted over the next year, the basis is `DelayedTarget` alone; if their pricing dates spread over a period, `ForcedIIDFromTemporal` alone.
   * **Background:**
     - The host's framing is one pricing moment: "predict the probability that a driver will initiate an auto
       insurance claim in the next year" (https://www.kaggle.com/c/porto-seguro-safe-driver-prediction).
     - The duties of `DelayedTarget`: the window has closed for every row (a year for every policy, by the host's
       framing), and every feature existed at the moment; the anonymised columns allow only the missingness test,
       which finds three columns whose blanks mark claims (issue 4).
     - Issue 2's leak test stays valid under either tag: no repeated policy holder, no order along the id, and
       holding out the region code inside `ps_reg_03` scores the same (0.639).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | `data_tags` hold only `Anonymized` | nothing to write | the decision of issue 2 not applied; `dataset check` notes a split that is not temporal without a basis |
     | B | `DelayedTarget` alone | the tag and its `Time basis:` line naming the moment and the window | follows the record's facts, the host's framing and the forced rule as reworded on 2026-11-05 | rests on the host's framing, as no date can show one moment |
     | C | `ForcedIIDFromTemporal` alone | the tag and its line | right if the policies were priced over a period | contradicts the record's facts; drops the delayed-target duties issue 2 asked for |
     | D | Both, as resolved | both tags | issue 2's resolution as written | the definition does not load ("one time basis") |

   * **Recommendation:** B: one pricing moment with a claim window is what the record, the host and issue 2's new tag
     describe; the forced tag now belongs to releases whose rows arose over a period. **Decision:** A, B, C or D?

   **Notes for the AI:** once PR #50 is in this working copy, on B: `data_tags = ("Anonymized", "DelayedTarget")`
   and in `curation_comments` the bullet `- Time basis: DelayedTarget: policy holders priced at one moment, the target
   a claim within the following year (the host's framing; record: Samples: One Moment, Target: Later). The id is a
   random shuffle and no date survives, so neither the moment nor a later pricing round can be checked; a later round
   is what the split cannot test. Features: anonymised, so only missingness can be audited (issue 4). Leak test across
   the split: no repeated policy holder, no order along the id, the region code in ps_reg_03 held out scores the same
   (ROC AUC 0.639).`; the `split` sentence names the moment; `dataset check`; the record's CC line for issue 2 names
   the basis taken. On C: `("Anonymized", "ForcedIIDFromTemporal")`, a line in the same form, and issue 4 for the
   audit.

   [^3a]: **SPLIT-8** (Must; reworded 2026-11-05, Lennart): a release that is one moment (one extract, one stock month)
     is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`. **SPLIT-32** (Should): `DelayedTarget` when all
     samples share one prediction moment and the target arrives after it, in a window closed for every sample, every
     feature checked to have existed at the moment.

   **Answer (AI, 2026-11-06):** `DelayedTarget` alone (B) keeps everything your resolution of 2026-11-04 asked for.

   - You accepted "Allow `DelayedTarget` together with a forced tag?" in the form the rule now takes: a definition keeps
     one time basis, and the check of every feature against the prediction point follows the record's `Target:` fact,
     whatever the time basis[^3d].
   - porto_seguro's record carries `Target: Later`, so the delayed-target duties of issue 2 (the claim window closed for
     every policy, every feature checked against the pricing moment, the missingness audit of issue 4) hold under B as
     they would with both tags, and the leak test of issue 2 stays in the line.
   - The decision between A, B, C and D stays yours.

   [^3d]: **SPLIT-32** (Should): a definition names one time basis; whatever it is, a record with a `Target:` fact asks
     that every feature be checked against the prediction point (LEAK-1, LEAK-10).

   **Resolved (2026-11-09, Andrej):** B: `DelayedTarget` alone. The `Time basis: DelayedTarget:` bullet is in
   `curation_comments` and the `split` sentence names the one pricing moment; the tag enters `data_tags` once PR #50 is
   in the working copy. The feature check follows the record's `Target: Later`, so nothing the resolution of 2026-11-04
   asked for is lost.

4. **Blanks in `ps_car_01_cat`, `ps_ind_04_cat` and `ps_ind_02_cat` mark claims beyond the other features: drop those rows?**

   * **Problem:**
     - The 79 policy holders missing both `ps_car_01_cat` and `ps_ind_04_cat` claimed at 41.8%, while a model of the other features that cannot see these blanks expects 23.2% (33 claims against 18.3, p = 0.0001).
     - Policy holders without blanks at the same predicted risk claim as predicted (13.3% against 14.3%), so the excess sits in the blanks: a field left blank more often for drivers who go on to claim, which a price set at the start of the year should not see.
     - Drop the 246 rows with a blank in any of the three columns, drop the columns, or keep them?
   * **Background:** this is the feature audit issue 2 left to do. The names are hidden, so whether a blank is a
     field filled in after a claim cannot be read from a codebook; Kaggle's test file has the same pattern (124 rows
     miss both), which does not clear it, since that file is a holdout of the same snapshot[^4a]. Filling the blanks
     with a level would need a statistic over all rows, which our cleaning does not compute[^4b].
   * **Experiments:** Slurm jobs 1366178 and 1366184, Kaggle's train.csv (595,212 rows, -1 read as missing),
     LightGBM on the 37 shipped features, out-of-fold over 5 folds, 3 seeds averaged; the three columns' blanks
     either visible or replaced by a level, so the model cannot see them:
     - Any of the three blank: 246 rows, 41 claims against 24.7 expected (p = 0.0003); `ps_ind_02_cat` blank: 216
       rows, 18.5% claimed against 10.9% expected.
     - ROC AUC over all rows: 0.6392 with the blanks visible and 0.6392 with them hidden: the 246 rows move no
       score.
   * **Effect on the task:** small in the score; what changes is whether the task holds a field shaped by the
     outcome, which a pricing model does not have.
   * **Consistency:** kick dropped `WheelType` once a conditional test measured its mechanism (2026-10-22), and
     gallstone_disease dropped the rows recorded through a second route that models recognised (2026-10-26/27)[^4a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | the blanks stay missing | the host's rows | a measured outcome-shaped blank stays readable |
     | B | Drop the 246 rows | rows with a blank in any of the three columns go; about 594,960 rows remain | removes the measured mechanism; no invented value; the columns stay for every other row | 41 of 21,694 claims leave; the rows exist in the host's test file too |
     | C | Drop the three columns | the columns go for every row | no blank left to read | loses three columns' signal for 99.96% of the rows |
     | D | Keep with a note | as A, with a `Potential leak, kept on purpose:` note and the numbers | documents it | the rule keeps a field only while no test can measure it, and this one is measured |

   * **Recommendation:** B, the smallest change that removes what the test measured. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, in `_clean` after the `-1` to missing step, drop the rows where `ps_car_01_cat`,
   `ps_ind_04_cat` or `ps_ind_02_cat` is missing; a curation note with the numbers above; `row` and `changes` in the
   task summary; `dataset check`. Scripts of the time review of 2026-11-06: `miss_cond.py`, `miss_calib.py`.

   [^4a]: **LEAK-38** (Should): fields whose timing cannot be tested stay with a note; when a conditional test
     measures the mechanism (missingness given the covariates differs by outcome), LEAK-10 applies and the field is
     dropped, even if the host's test file carries it the same way. **LEAK-10** (Must): missingness that encodes the
     outcome is out. **LEAK-39** (Must): rows of one class recorded through a separate route are dropped when it
     cannot be aligned.
   [^4b]: **LEAK-29** (Must): our cleaning never computes a feature value from statistics over all rows. **LEAK-7**
     (Should): the smallest fix that keeps a valid signal.

   **Resolved (2026-11-09, Andrej):** A, keep: "There is no evidence that this is a leak and not a real pattern. The
   difference in the target distributions is not too crazy, so this is not sufficient to drop." The definition is
   unchanged.

## Reference

Addison Howard, Adriano Moala, and Walter Reade. Porto Seguro’s Safe Driver Prediction. https://kaggle.com/competitions/porto-seguro-safe-driver-prediction, 2017. Kaggle.
