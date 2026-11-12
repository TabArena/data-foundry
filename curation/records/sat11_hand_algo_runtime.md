---
unique_name: sat11_hand_algo_runtime
name: SAT11-HAND-ALGO runtime-regression from aslib_data
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Grouped)
- Multi-target
collections:
- TabArena Reject
- TabSTAR
original_source: ASlib
year: '2011'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.cs.ubc.ca/labs/algorithms/Projects/SATzilla/
- https://www.openml.org/d/41980
- https://github.com/coseal/aslib_data/tree/master/SAT11-HAND-ALGO
notebook_path: datasets/beyond_iid/grouped/sat11_hand_algo_runtime/sat11_hand_algo_runtime.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sat11_hand_algo_runtime/dataset.py
source_row: 694
type_adapter_id: curation-record-v1
---

## Comments

CC: "Some code runtime prediction challenge; see https://arxiv.org/pdf/1506.02465 and https://arxiv.org/pdf/1111.2249  and https://github.com/coseal/aslib_data/tree/master/SAT11-HAND; on openml the instance ID is missing, so in its current state this would create a leak (we have information about the to-be-solved SAT instance). Leak without instance ID, could get real data from other sources but this would then require grouped splits as normally done in AS literature"  

Good to have some datasets from this kind of literature as well, maybe checkout if any newer cases exist we can add to the benchmark

For 41980, we can parse the row ID to get a grouped algorithm selection task. This would be great to cover as well! Otherwise use https://github.com/coseal/aslib_data/tree/master/SAT11-HAND


I would focus on including such datasets for SAT solving, as this seems a "realer" use case than for ML algorithm selection which is usually Pareto, dominated by other methods. 

We use the task that aims to go from (Instance_features, algorithm_features) -> runtime; which is more or less an alternative to multi-target modelling aiming to generalize across algorithms.

CC (2026-10-06, Lennart): The split holds out instances, not instance families, on purpose. The instances come in 48 families (74% of an instance's nearest neighbours are in its own family), but a selector in use has other members of a new instance's family in its data, so holding out single instances, as ASlib does, is the realistic setting.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: edge_sa, edge_sl.

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: edge_sa and edge_sl (edge counts of the solver's code graph) stay numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source par_k {"cutoff": 5000, "k": 10, "target_transform": "log", "timeout_rel_tol": 0.0001} — PAR10 (penalized average runtime, factor 10) of the selected algorithm; also reported as the fraction of the single-best to virtual-best gap closed (Bischl et al. 2016, ASlib: A benchmark library for algorithm selection, Artificial Intelligence 237:41-58; Pulatov et al. 2022 (PMLR v188)); inputs {"group": "instance_id"}.

**Assessment (AI, 2026-10-21):** the log transform of the runtime moved from par_k's `target_transform` param to the spec-level `target_transform="log"` (the param is removed, so no double inverse is possible); the score is unchanged. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `sat03_16_indu_algo_runtime` (TBD -> Yes, priority 4), `sat18_exp_algo_runtime` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: real SAT-competition runs scored by the source's PAR10 of the predicted-fastest solver; only the spread under PAR10 is unmeasured. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-06, Andrej): ship (review page issue 1); a timed-out run stays at the recorded 5,000 s in the log target (issue 3), since it is the value ASlib records and how to treat a censored run is part of what a model has to work out; counting it at the 50,000 s PAR10 charge made every model pick 17-19% better but would replace the recorded value. Metric (PAR10) and split checked and kept.

CC (2026-11-11, Andrej): PAR10 alone picks the solver (review page issue 4, B): the grouping declares `prediction_unit="row"` and no aggregation instead of `select_min`, so a tie at an instance's lowest prediction counts as the mean of the tied solvers' costs, as PAR10 defines it, not as the solver first in the file; the same form as asp_potassco_classification. Trained models never tie on the 60 splits and score the same (LightGBM 8,970 s, random forest 8,323 s, linear 11,350 s); a constant prediction moves from 19,140 s to 18,539 s. `dataset check` 0 errors.

CC (2026-11-12, Lennart): the split count in scored units (the review's issue 2, rule SPLIT-33) moves out of this
PR into its own, to be decided with the other grouped datasets and reopened there; it is removed from this record
for now. Until then the protocol counts the 1,840 rows: 10 x 3 splits.

## Review

**Outcome:** added. ASlib's SAT11-HAND scenario (Xu, Hutter, Hoos and Leyton-Brown 2012; Bischl et al. 2016): the
runtimes of 10 SAT solvers on 184 handcrafted instances of the 2011 SAT competition, one row per run (1,840 rows),
from instance features and features of the solver's code; whole instances are held out, and the score is ASlib's
PAR10 of the solver predicted fastest per instance. The AI recommends shipping it as defined. Reviewed without a panel,
from the gathered evidence: the record, the curator's decisions of 2026-10-01 and 2026-10-06, and a model run
on the shipped data. Validity: real competition runs, features known before any solver runs, the solver's name
dropped, and `runstatus` (the timeout flag) dropped; the 112 instances on which every solver times out are dropped,
which changes no selection. Value: a model run used BeyondArena's version (all 296 instances, RMSE on the log
runtime), where the benchmark methods range from 1.89 (best) and 2.00 (TabPFN-3.5) over a median of 2.09 to 3.83
(untuned
linear regression), and two forests for instance difficulty and solver offsets rank 3 of 41: one difficulty
factor carries 87% of the variance. How well v0.2's PAR10 on 61 test instances per fold separates methods is not
measured. Quality: three constant columns (`POSNEG_RATIO_CLAUSE_max`, `UNARY`, `clustering_max`, constant in the raw
file too) can go without a decision. Weighed: a documented algorithm-selection benchmark scored by its source's metric
(+), few instances per fold and an untested spread under PAR10 (-).

**Main points:** Ship: timeouts at the recorded 5,000 s, PAR10 (issues 1, 3 and 4 resolved); PAR10 alone picks the
solver, a tie counted as PAR10 defines it (issue 4). The split count (2) is deferred to its own PR.

**Record judgment:** valid. The task is the one the curator chose (one model for all solvers, from instance and
solver features, as in Pulatov et al. 2022), and the split by instance rather than by instance family is his decision
of 2026-10-06: a selector in use has other members of a new instance's family in its data. The censoring of runtimes at
5,000 s is handled for PAR10 (timeouts kept at the limit, all-timeout instances dropped). The data-scouting run of
2026-10-31 found better data for the same task, `sat03_16_indu_algo_runtime` (priority 4) and `sat18_exp_algo_runtime`
(priority 3), screened in their own records and not added yet; whether SAT11-HAND stays next to them is for when they
are added. The `Multi-target` tag stays (one runtime per solver, stacked as rows).

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: real competition runs, features known before any solver runs, the source's metric
       (PAR10 of the solver predicted fastest), and the curator's split by instance with its reason recorded.
     - What is not measured is how well PAR10 on 61 test instances per fold separates methods; on BeyondArena's
       version (RMSE, all 296 instances) the benchmark methods spread from 1.89 to 3.83, with a median of 2.09.
     - Ship as defined, or retire?
   * **Background:** one difficulty factor of the instance carries 87% of the variance of the instance-by-solver
     table, and a model of instance difficulty plus solver offsets ranks 3 of 41 there, so the solvers differ mostly
     by an offset and a few solver-specific families. Newer ASlib scenarios of the same kind
     (`sat03_16_indu_algo_runtime`, priority 4; `sat18_exp_algo_runtime`, priority 3) are screened and not added.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 184 instances x 10 solvers, grouped by instance, PAR10 | the source's task and metric; no defect found | PAR10 spread unmeasured; few instances per fold |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | leaves the place to a larger SAT scenario once added | no defect of the data found; the newer scenarios are not added yet |

   * **Recommendation:** A: no reason in the task itself to retire it, and methods spread on the version measured[^1a].
     **Decision:** A or B?

   [^1a]: **TP-2** (Should): retire, fix or keep a task for a concrete reason found in the task itself; until one is
     found, the task stays.

   **Andrej (2026-11-06, discuss):** We made changes to asp potassco - is this dataset affected by it too?

   **Answer (AI, 2026-11-06):**

   * **Yes, in two places; a third is open:**
     - The split count (decided, asp_potassco_classification issue 2, B): splits now follow the units the metric
       scores (SPLIT-33). PAR10 scores per instance, and 184 instances leave a training side of 122, so this dataset
       gets 20 x 3 splits instead of 10 x 3. `dataset check` confirms it; the shipped container keeps 10 x 3 until
       its next build.
     - The target scale (decided, asp issue 4): the log scale stays, here as there.
     - The timeouts (open, asp issue 3): this dataset is where the evidence differs. Here every model picks 17% to 19%
       better when a timed-out run counts as the PAR10 charge (50,000 s) instead of the recorded 5,000 s, which meets
       your bar for adapting the target; on asp it does not. The choice is made there (options A, B, C), and applies
       here.
   * **Not affected:** asp's reframing as runtime regression (asp issue 1) took this dataset as its model; the
     metric (PAR10, from ASlib) and the rows (instances no solver finished dropped, as asp now does too) stay.
   * **Recommendation:** ship as defined, with the 20 x 3 splits, and take the timeout target from asp issue 3.

   **Andrej (2026-11-06, discuss):** If you suggest to change anything for this dataset, there should ne a decision
   item, this is not clear right now.

   **Answer (AI, 2026-11-06):**

   * **Each change now has its own item:** issue 2, the split count (20 x 3 under the rule decided on
     asp_potassco_classification, already in the definition's checks); issue 3, how a timed-out run is counted in
     the target (open, recommended: the PAR10 charge). This issue asks only whether to ship once those are settled.
   * **Recommendation:** ship (A), with issues 2 and 3 as you decide them.

   **Resolved (2026-11-06, Andrej):** ship (A), with issues 2 and 3 as decided below; metric and split checked.

   **Deferred (2026-11-12):** issue 2, the split count, moved to its own PR (Lennart); this dataset ships with the
   protocol's count of its 1,840 rows, 10 x 3 splits, until that PR decides.

2. **Split count: 20 x 3 splits, counted in instances, instead of 10 x 3 counted in runs?**

   **Deferred (2026-11-12):** Lennart moved the split count in scored units (rule SPLIT-33) out of this PR into
   its own, to be decided with the other grouped datasets; this issue is reopened there. Until then the protocol
   counts the 1,840 rows: 10 x 3 splits.

3. **Count a timed-out run as the recorded 5,000 s, or as the 50,000 s PAR10 charges for it?**

   * **Problem:**
     - Counted as the PAR10 charge (10 times the 5,000 s limit) instead of the 5,000 s ASlib records, a timed-out run
       makes every model pick better: LightGBM, the forest, the linear models and TabPFN by 17% to 19%, on 47 to 57 of the
       60 splits, which meets the bar you set on asp_potassco_classification issue 3 (adapt the target only when a change
       clearly benefits all models equally).
     - The shipped target is the recorded value: ASlib stores all 2,695 timed-out runs at exactly 5,000 s (finished
       runs end at 4,995.8 s at most). The scoring stays PAR10, ASlib's measure, either way.
     - Keep the recorded 5,000 s, or count a timeout as 50,000 s in the target?
   * **Background:** a timed-out run is right-censored (only "more than 5,000 s" is known). The log target with the
     recorded limit keeps the order within an instance but charges a timeout as a run just past the slowest finish;
     PAR10 charges it ten times the limit. On asp_potassco_classification the same change does not clear the bar (mixed
     results within about two standard errors), so the two datasets may end up with different targets.
   * **Experiments** (PAR10 of the pick, mean seconds over the 60 splits, instances held out):

     | Model | Recorded 5,000 s | 50,000 s | Censored model | Timeouts left out of training |
     |---|---|---|---|---|
     | LightGBM | 8,970 | 7,420 (-1,549) | 7,523 (-1,447) | 14,532 (+5,562) |
     | Random forest | 8,323 | 6,783 (-1,540) | 7,148 (-1,176) | 15,222 (+6,899) |
     | Linear (one per solver) | 11,350 | 9,255 (-2,095) | 8,699 (-2,651) | 19,788 (+8,438) |
     | TabPFN 3.5 | 7,820 | 6,464 (-1,356) | not run | 21,208 (+13,387) |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Recorded 5,000 s (implemented) | the target as ASlib stores it | the source's values; the same form as asp_potassco_classification | leaves a gain every model shows unused |
     | B | The PAR10 charge, 50,000 s | a timed-out run's target is 10 times the limit, on the log scale | every model picks 17-19% better; training charges what the score charges | a value the source did not record; differs from asp_potassco_classification if that keeps its 600 s |

   * **Recommendation:** B: the gain holds for every model, so it meets your bar. **Decision:** A or B?

   **Notes for the AI:** on B, in `_clean` set the runtime of runs with `runstatus != "ok"` to 50,000 before the log, a
   curation note with the table above, `dataset check`, record CC line, CHANGELOG. Evidence of the asp_potassco review
   (timeouts) covers this dataset.

   **Andrej (2026-11-06, ok):** We go with A since this is the real recorded value and changing it is already part of
   the solution models are supposed to find. Document this decision.

   **Resolved (2026-11-06, Andrej):** the recorded 5,000 s stays (A): it is the value ASlib records, and how to treat a
   censored run is part of what a model has to work out; the curation notes and the record say so, with the measured
   gain of the PAR10 charge (17-19%) for reference. The scoring stays PAR10.

4. **Let PAR10 alone choose the solver, so a tie is scored as PAR10 defines it?**

   * **Problem:**
     - The definition chooses the solver predicted fastest twice: the grouping's `select_min`, which the scorer applies
       first and which breaks a tie by the order of the rows, and PAR10 (`par_k`), which counts solvers tied at the
       lowest prediction as the mean of their costs.
     - With `select_min` a tie scores the solver that comes first in the file; asp_potassco_classification declares no
       aggregation, so there PAR10 alone chooses.
     - Keep `select_min`, or let PAR10 choose alone?
   * **Effect on the task:** none on the trained models measured: LightGBM, the random forest and the linear models
     (one per solver) tie at an instance's lowest prediction in 0 of 3,680 test instances over the 60 splits and score
     the same either way. A constant prediction ties everywhere: 19,140 s with `select_min` (always the first solver in
     the file) against 18,539 s under PAR10's rule (the mean over the solvers), up to 5,107 s apart on one split.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `select_min` (implemented) | `prediction_unit="group"`, `aggregation="select_min"`; PAR10 sees one row per instance | the definition as built; states one decision per instance | a tie scores the solver first in the file; a different form from asp_potassco_classification |
     | B | PAR10 chooses alone | `prediction_unit="row"`, no aggregation; PAR10 keeps the instance as its group | a tie scored as PAR10 defines it, whatever the row order; one form for both ASlib datasets | changes a definition otherwise settled, for an effect only tied predictions show |

   * **Recommendation:** B: a score should not depend on the order of the rows, and both ASlib datasets then declare
     the same form[^4a]. **Decision:** A or B?

   [^4a]: definitions.md ("Grouped"): when the metric chooses per instance by itself (`par_k`), the grouping declares
     `prediction_unit="row"` and no aggregation.

   **Andrej (2026-11-11, discuss):** Is it a standardization for the two related tasks that does not change the
   functionality?

   **Answer (AI, 2026-11-11):** Yes, for any model that does not tie; a score changes only where predictions tie.
   - What B changes: only who picks the solver. With `select_min` the scorer keeps the row with the lowest prediction
     per instance and hands PAR10 that one row; with B PAR10 gets all rows and picks the same lowest row itself. The
     target, features, splits, the instance as the metric's group and PAR10's charge for a timeout stay as they are.
   - Where it differs: a tie at an instance's lowest prediction. `select_min` scores the solver first in the file,
     PAR10 the mean of the tied solvers' costs.
   - Measured on the 60 shipped splits (3,680 test instances), PAR10 in seconds:

     | Model | Instances tied | `select_min` (A) | PAR10 alone (B) | Largest split difference |
     |---|---|---|---|---|
     | LightGBM | 0 | 8,970 | 8,970 | 0 |
     | Random forest | 0 | 8,323 | 8,323 | 0 |
     | Linear, one per solver | 0 | 11,350 | 11,350 | 0 |
     | Constant prediction | 3,680 | 19,140 | 18,539 | 5,107 |

   - Also changed: the README's split line loses "one prediction per group (select_min)", and the container's
     grouping reads `prediction_unit: row` with no aggregation, as asp_potassco_classification's does.
   - A model that predicts ties (rounded or capped predictions, a constant fallback) is scored by row order under A
     and by PAR10's own rule under B. The recommendation stays B. **Decision:** A or B?

   **Notes for the AI:** on B, in `grouping` set `prediction_unit="row"` and remove `aggregation` (`context="all_rows"`
   stays), the grouping's `definition` unchanged, `dataset check`, a CC line in the record, CHANGELOG, and the
   "still declares `select_min`" line in definitions.md goes. On A, that line says it is kept and why. Tie counts: a
   re-fit of issue 3's LightGBM, random forest and linear models on the shipped target.

   **Andrej (2026-11-11, change):** Option B: PAR10 chooses alone.

   **Resolved (2026-11-11, Andrej):** B: the grouping declares `prediction_unit="row"` and no aggregation, so PAR10
   picks the solver predicted fastest per instance and counts a tie as the mean of the tied solvers' costs; the same
   form as asp_potassco_classification. `dataset check` 0 errors (the known constant-column warning); README
   regenerated. The trained models score the same as before; the shipped container keeps `select_min` until its next
   build.

## Reference

@inproceedings{xu-sat12a,
  author    = {L. Xu and F. Hutter and H. Hoos and K. Leyton-Brown},
  title     = {Evaluating Component Solver Contributions to Portfolio-Based Algorithm Selectors},
  pages     = {228-241},
  crossref  = {sat12}
}

@Proceedings{sat12,
  editor =         {A. Cimatti and R. Sebastiani},
  title =         {Proceedings of the Fifteenth International Conference on Theory and Applications of Satisfiability Testing (SAT'12)},
  booktitle = {Proceedings of the Fifteenth International Conference on Theory and Applications of Satisfiability Testing (SAT'12)},
  publisher =         springer,
  series =         lncs,
  volume =         7317,
  year =         2012
}
@article{bischl_aslib_2016,
	title = {{ASlib}: {A} {Benchmark} {Library} for {Algorithm} {Selection}},
	number = {237},
	journal = {Artificial Intelligence Journal (AIJ)},
	author = {Bischl, Bernd and Kerschke, Pascal and Kotthoff, Lars and Lindauer, Marius and Malitsky, Yuri and Fréchette, Alexandre and Hoos, Holger H. and Hutter, Frank and Leyton-Brown, Kevin and Tierney, Kevin and Vanschoren, Joaquin},
	year = {2016},
	pages = {41--58}
}
