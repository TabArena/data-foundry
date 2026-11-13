---
unique_name: asp_potassco_classification
name: ASP-POTASSCO-classification from aslib_data
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
- 'Entities: Recur'
collections:
- TabArena Reject
original_source: ASlib
year: '2014'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/41705
- https://github.com/coseal/aslib_data/tree/master/ASP-POTASSCO
notebook_path: datasets/beyond_iid/grouped/asp_potassco_classification/asp_potassco_classification.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/asp_potassco_classification/dataset.py
source_row: 695
type_adapter_id: curation-record-v1
---

## Comments

CC: ""Algorithm selection task. samples are per instance_id - unique algorithms. Task is to predict algorithm - not sure whether this makes sense

After post-hoc analysis: Requires group split. We assumed that it doesn't because the instance IDs were unique, however, they are only unique because they represent directories for repeated evaluations of the same task, i.e.: FolioSuite/ASP-Comp-2011-Lparse/26-Solitaire/1-solitaire-20-0.asp.gz - there are multiple solitaire instances and if we use random splits there is a leak.""

CC (2026-10-01, Lennart): The source splits these instances at random (claspfolio 2: random halves of the Potassco set, 2,589 instances from 105 problem classes; ASlib's cv.arff: 10 random folds). Under the source's use case, new instances of known problem classes, a shared class is not a leak, and the instances of a class are different instances, not repeated runs. Grouping by problem class (the instance path without the file name, 96 classes among the 1,212 instances some configuration solves) is our choice: it asks for a configuration on a problem class never seen in training, as for a user with a new encoding. The choice matters: for 85% of instances the nearest other instance in feature space is from the same class (under 4% by chance), and a class's most common best configuration is the best one for 46% of instances (20% for the overall most common).

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid task after the task-probe review (flag `no_signal`). The fastest-configuration label is how OpenML frames this scenario and a common way to do algorithm selection, and tuned methods learn it on unseen problem classes: TabICLv2 beats the class shares on all 30 grouped folds (log loss 2.17 against 2.35); untuned LightGBM and the linear model are overconfident and lose to them. The label is noisy by construction: the best configuration solves half of the 1,212 instances in under 1 s, and for 62% the second-best is within 1 s of it (40% within 0.1 s, one run each). The choice matters on the hard instances (PAR10 534 s for the single best configuration, 21 s for each instance's best), which a classification score does not weigh: a pick 0.05 s slower counts as wrong as a timeout.

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Configuration h3-n1 is the fastest on 21 runs from 9 instance groups, 1-17 per grouped test fold. It is 1.7% of the test rows and 3.9% of a random forest's log loss. The decision of 2026-10-06 (`no_signal`, kept) stands. Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: Tight, Removed_Nogoods-1, Removed_Nogoods-2.

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: Tight (whether the program is tight). Reverted: Removed_Nogoods-1 and Removed_Nogoods-2 (counts, and constant 0 where present).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: stand_in log_loss — stands in for PAR10 (penalized average runtime, timeouts counted as 10 x cutoff) of the selected algorithm (ASlib): ASlib scores PAR10 of the selected configuration, which needs the 11 runtimes per instance; they are not shipped (only the fastest configuration's label), and instances no configuration solved are dropped. Log loss on the fastest-configuration label is the closest computable score. (Bischl et al. 2016, ASlib: A benchmark library for algorithm selection, Artificial Intelligence 237; https://github.com/coseal/aslib_data/tree/master/ASP-POTASSCO (cutoff 600 s)).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship; a valid ASlib algorithm-selection task with a modest real signal, but score the chosen configuration's runtime (the source's PAR10, inputs published) instead of log loss on a near-tie-ridden fastest label. Priority 4: gap 1, use case 0, source 1, shape 1, risk -0.

CC (2026-11-04, Andrej): the task is now runtime regression scored by PAR10 (option B of the review page), as sat11_hand_algo_runtime.
- What the task is: one row per instance and clasp configuration (1,212 instances x 11 = 13,332 runs); the model predicts each run's time (log seconds, a run stopped at the 600 s limit counts as 600); per instance the configuration predicted fastest is picked, and the score is PAR10, the mean time of the picks with a timeout counted as 6,000 s. Problem classes are still held out.
- Why: a selector in use learns from the full table of runs, every configuration on every training instance, timeouts included; the fastest-configuration label hid that table from the models. The user loses time mostly to timeouts (96% of the single best configuration's PAR10 comes from them), and log loss scored a pick 0.05 s slower as wrong as a timeout.
- The bar: always running the configuration most often fastest in training gives 611 s, the best possible pick per instance 21 s (30 splits of the earlier definition); a model has to close part of that gap on problem classes it has not seen.
- ASlib's feature costs are left out (the same whichever configuration is picked). To do: rename the dataset (it is no longer a classification) once the review page is done; its marks are stored under this name.

**Assessment (AI, 2026-11-04):** implemented B in dataset.py: target `runtime` (log), `algorithm` categorical, anonymised `instance_id` a scoring column (role group) of `par_k` (cutoff 600, k 10, `Metric.source`), Grouping on `task_id`; 1,963 timeouts (15% of runs, on 38% of instances) kept at 600 s. `dataset check`: 0 errors, 1 warning (the two constant columns `Removed_Nogoods-1/-2`, already known); par_k computable on every split. The split protocol now gives 3 x 3 splits (13,332 rows) instead of 10 x 3, 32 problem classes per test fold. On the 9 new splits, PAR10 in seconds: untuned LightGBM 699, always the configuration most often fastest in training 754, single best by training PAR10 1,045, best possible 22; LightGBM beats the most-often-fastest rule on 6 of 9 splits, and splits range from 124 to 1,281 s, set by a few problem classes. Task probes (R^2 per row, 5 of 9 splits): random forest 0.57, LightGBM 0.56, linear -0.44, best single feature 0.17, no flags. Leak probes: no single feature above 0.28; 2.0% of test rows have an exact feature copy in train (the instances with repeated features). Group probes: IID R^2 0.90 against grouped 0.53, so the class split matters.

CC (2026-11-05, Andrej): the task summary now says 32 of the 96 problem classes per test fold (it said 27 to 36, a count from the classification splits).

CC (2026-11-06, Andrej): the target stays on the log scale (review page issue 4), and a timed-out run stays at the recorded 600 s (issue 3): the target is the runtime as ASlib records it and how to treat a censored run is left to the models, unless a change clearly benefits all models equally, which counting timeouts at the 6,000 s PAR10 charge does not here (within noise, mixed across models). The scoring stays ASlib's PAR10. Metric and split checked.

CC (2026-11-12, Lennart): the split count in scored units (the review's issue 2, rule SPLIT-33) moves out of this
PR into its own, to be decided with the other grouped datasets and reopened there; it is removed from this record
for now. Until then the protocol counts the 13,332 rows: 3 x 3 splits.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the 96 problem classes hold 1 to 134 instances (median 5), and the largest 10% of them hold 51% of the instances, so a few large classes decide about half of the log loss; the selector acts per instance, and the split holds out whole classes. Weighting each instance by 1 over its class's instances ranks 8 untuned models at Kendall tau 0.86 per split (lowest 0.64) and 0.86 for the ranking by the mean over the 30 shipped splits, the same best model on 17 of 30. Open for Lennart as issue 5 of the record's Review (numbered after issues 1 to 4 of the PAR10 branch); recommended: per instance, with a note that names the imbalance (B).

CC (2026-11-08, Lennart): issue 5, B: scored per instance, with a note. Each instance is a decision of the selector (MET-17); the notes say that the largest 10% of the 96 problem classes hold 51% of the instances and that counting each class once ranks 8 untuned models at Kendall tau 0.86 per split.

CC (2026-11-08, Lennart): the declared metric (log_loss) is checked.

## Review

**Outcome:** added. ASlib's ASP-POTASSCO scenario (Hoos, Lindauer and Schaub 2014; Bischl et al. 2016): 1,212
logic-programming instances from 96 problem classes, each labelled with the fastest of 11 configurations of the
solver clasp, from statistics of the program and of short probing runs; whole problem classes are held out. The AI
recommends shipping it, and asks whether the score should be the time the chosen configuration takes instead of log
loss on the fastest-configuration label (issue 1). Reviewed without a panel, from the gathered evidence: the record,
the review of 2026-09-22, the curator's task-probe decisions and a model run on the shipped data. Validity:
real solver runs, features computed before solving, no leak found; the class split is stricter than the source's
random split, on purpose. Value: on the shipped grouped folds the benchmark methods range from log loss 2.169 (best) and
2.172 (TabPFN-3.5) over a median of 2.250 to 3.759 (untuned logistic regression), against about 2.35 for the class
shares; a small regularised CatBoost that falls back to the class shares for programs unlike any training program ranks
1 of 41 (2.149), so the task rewards caution on new problem classes. The label is noisy by construction: for 62% of
the instances the second-best configuration is within 1 s of the best, from one run each. Quality: two constant
columns (`Removed_Nogoods-1`, `Removed_Nogoods-2`, 0 or missing) and 5 rows that repeat another row's features with
another label. Weighed: a documented algorithm-selection benchmark and a strict split (+), a modest signal over the
class shares (-), a label that scores a pick 0.05 s slower as wrong as a timeout (-), which issue 1 can fix.

**Main points:** All resolved: runtime regression scored by PAR10 (1), timeouts at the recorded 600 s (3), the log
scale (4); scored per instance, with a note on the large problem classes (5, Lennart, 2026-11-08). The split count
(2) is deferred to its own PR. The rename (no longer `_classification`) waits until the page is done.

**Record judgment:** valid. An algorithm-selection scenario of the ASlib library, built from claspfolio 2's Potassco
set; the runs and features are the library's own files, so the source is strong. The curator kept it twice after the
task probes (`no_signal` 2026-10-06, `few_minority` 2026-10-12) and grouped it by problem class (2026-10-01); those
decisions stand and are not reopened here. The record's earlier `problem_type: Regression` was corrected after the
review of 2026-09-22 and now matches the definition. The metric line of 2026-10-21 is an AI assessment, not a curator
call, and its reason ("the 11 runtimes are not shipped") describes our choice, not the source (issue 1).

**Issues for Andrej and Lennart:**

1. **Score the runtime of the chosen configuration instead of log loss on the fastest label?**

   * **Problem:**
     - The definition reduces the 11 measured runtimes of each instance to the label "fastest configuration" and scores
       log loss on it, as a stand-in for ASlib's PAR10 (the mean runtime of the chosen configuration, a timeout counted
       as 10 times the 600 s limit).
     - The stand-in's reason says the runtimes are not shipped, but the source publishes all of them
       (`algorithm_runs.arff`, which `_load_raw` already reads), so the source's score is computable.
     - Keep the stand-in, or ship the runtimes for scoring only and score the chosen configuration's runtime?
   * **Background:** algorithm selection picks one solver configuration per problem; what the user loses is the time
     of the pick against the best one. A metric needs its inputs as columns that the models never see[^1a]; a
     stand-in is meant for a source metric that cannot be computed on our data[^1b].
   * **Effect on the task:** under log loss a pick 0.05 s slower than the best counts as wrong as a pick that times
     out, and for 62% of the instances the second-best configuration is within 1 s of the best (40% within 0.1 s, one
     run each), so much of the loss is a coin flip between near-equal configurations. The choice matters on the hard
     instances: PAR10 is 534 s for the single best configuration and 21 s for each instance's best (curator's note of
     2026-10-06), which log loss does not weigh.
   * **Experiments:** none new; the numbers above are from the record. The benchmark spread on log loss (2.169 to 2.250
     from best to median) is the only value evidence; no run scored PAR10.
   * **Consistency:** sat11_hand_algo_runtime, from the same library, is scored by PAR10 of the selected solver (one
     row per instance and solver, the runtime as target, the fastest predicted runtime selected per instance).
   * **Unknown:** whether the framework can score per instance while the split holds out whole problem classes (two
     group levels); option C avoids that.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Log loss on the fastest label (implemented) | one row per instance; 11-class label; log loss | no framework work; the curator kept it twice | near-ties count as full errors; the stand-in's reason is wrong as written |
     | B | Runtime regression, as sat11 | one row per instance and configuration (13,332 rows); log runtime as target; PAR10 of the fastest predicted configuration per instance | the source's metric and ASlib's usual framing; the same form as sat11 | needs a split by problem class above a scoring group by instance; loses the benchmark's multiclass form of the task |
     | C | Same label, score the chosen configuration's runtime | rows and label unchanged; the 11 runtimes ship as scoring-only columns; PAR10 of the most probable configuration | the source's metric; same rows, split and training label | a new custom metric with its reference implementation; methods still train on the noisy label |

   * **Recommendation:** C: it scores what the user loses, the source publishes the inputs, and it keeps the rows, the
     split and the multiclass form that sets this dataset apart from sat11. **Decision:** keep log loss (A), reframe as
     runtime regression (B), or score the chosen configuration's runtime (C)?

   **Notes for the AI:** on C, `_clean` keeps the runtimes of the 11 configurations per instance (`runstatus != "ok"`
   becomes the 600 s limit, scored as 6,000 s) as scoring columns; a custom metric (general name, for example
   `chosen_class_cost`) takes the argmax of the predicted probabilities and averages the runtime column of that class,
   with a reference implementation and a test against a hand count (MET-13); the stand-in becomes `Metric.source` with
   PAR10 as the original; `fit_reason` drops the sentence on near-ties. On B, follow sat11's definition, with the
   configuration name as a categorical feature, and check that `Grouping(on="task_id")` can score per `instance_id`.
   Either way, re-run `dataset check` and the task probes; on A, correct the stand-in's reason to "the runtimes are in
   the source; we ship only the fastest configuration's label".

   [^1a]: **MET-2** (Must): match the data, the metric and the real task; every input a metric needs ships as a column
     and is never a feature; when the data falls short, adapt the data first (ship the column), otherwise declare a
     stand-in.
   [^1b]: **MET-11** (Must): a stand-in replaces a unique source metric that cannot be computed on our data (inputs
     not published, a task we changed), names the original and why it cannot be computed.

   **Andrej (2026-11-04, discuss):** It seems clear that we go with B or C. What solves the underlying use case better?

   **Answer (AI, 2026-11-04):**

   * **Your question:** B or C, for a user who picks a clasp configuration for an instance of a problem class not seen
     before and loses the time of that pick?
   * **Found:**
     - B, for what the model learns from. A selector in use is trained on the table of runs, every configuration on
       every training instance. B gives a model that table; C reduces it to the name of the fastest configuration, so
       no model sees a timeout or how much a wrong pick costs. The user's loss is almost all timeouts: 96% of the
       single best configuration's PAR10 comes from its timeouts (6,000 s each), and 38% of the instances have a
       configuration that times out.
     - The measured picks do not decide it. Each model trained both ways on the 30 shipped splits, every pick scored
       by PAR10 (table below): LightGBM picks better as in B (646 against 736 s, on 24 of 30 splits) and the forests
       slightly better; k-nearest neighbours, the linear model and TabPFN pick better as in C (TabPFN 709 against
       672 s, B trained with timeouts at 6,000 s). The differences are small next to the spread between splits (about
       400 s), which a few problem classes set.
     - B works with the framework as it is: a prototype definition holds out problem classes, scores PAR10 per
       instance through the anonymised instance id as a scoring column, and neither id reaches the model. C does not:
       a metric input is one column, and C's metric reads 11 runtime columns, so the metric spec has to change
       first. The table's "no framework work" for C and the two-group-levels con of B were wrong.
     - C's one advantage is form: B is a second dataset in sat11's form, while C would be the collection's only
       classification whose cost of a wrong pick differs from row to row (aps_failure, credit_g and the FORCE 2020
       lithofacies set use one cost matrix for all rows).
   * **What holds for both:** on problem classes not seen in training, no method reliably beats always running the
     configuration most often fastest in training (h1 in 26 of 30 splits), 611 s on average; the best pick per
     instance takes 21 s. The best models beat that rule on 18 or 19 of 30 splits. A few classes decide PAR10: 35 of
     the single best configuration's 101 timeouts fall in one class, 71 in five. The task probes kept the dataset on
     log loss (2026-10-06); under PAR10 this is the baseline that matters, and whether the dataset stays may come
     back to you.
   * **Experiments:** mean PAR10 in seconds over the 30 shipped splits, lower is better; small untuned models, each
     trained as in B and as in C:

     | Model | B, timeout at 600 s (as sat11) | B, timeout at 6,000 s | C | Splits where B (600 s) picks better |
     |---|---|---|---|---|
     | LightGBM | 646 | 633 | 736 | 24 of 30 |
     | Random forest | 680 | 659 | 705 | 18 of 30 |
     | Extra trees | 711 | 701 | 720 | 18 of 30 |
     | k-nearest neighbours | 709 | 699 | 609 | 11 of 30 |
     | Linear (ridge, logistic regression) | 853 | 768 | 795 | 12 of 30 |
     | TabPFN 3.5 | not run (no GPU node came up) | 709 | 672 | 17 of 30 (B at 6,000 s) |
     | Always the configuration most often fastest in training | 611 | 611 | 611 | |
     | Best possible pick per instance | 21 | 21 | 21 | |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | B | Runtime regression, as sat11 | one row per instance and configuration (13,332 rows); the log runtime as target, a timeout at the 600 s limit; per instance the configuration predicted fastest, scored by PAR10; problem classes held out | models learn from every run, timeouts included, as a selector in use does; the source's metric; works with the framework as it is | a second dataset in sat11's form; a model without interactions (linear) picks one configuration for every instance |
     | C | Same label, score the chosen configuration's runtime | rows and label unchanged; the 11 runtimes ship as scoring-only columns; PAR10 of the most probable configuration | the collection's only classification with a cost per row; the same rows and split | models never see a runtime or a timeout; needs a change of the metric spec and a new metric |

   * **Recommendation:** B: the user loses time to timeouts, only B lets a model learn them, and it needs no framework
     change; the measured picks favour neither[^1c]. **Decision:** B or C?

   **Notes for the AI:** on B, follow sat11's definition: `_clean` keeps the 11 runs of the 1,212 instances that some
   configuration solved, a timeout at 600 s, `runtime` on the log scale; `algorithm` as a categorical feature (the
   scenario publishes no configuration features); the anonymised `instance_id` as a `ScoringColumn` (role `group`) of
   `par_k` (cutoff 600, k 10); `Grouping(on="task_id", labels="per_sample", prediction_unit="row", context="none")`.
   ASlib adds feature costs (`feature_costs.arff`) to the selected runtime; they are the same whichever configuration
   is picked, so leave them out and say so in the metric's definition. `metric` becomes `Metric.source`, `fit_reason`
   drops the near-tie sentence, the record's `problem_type` goes back to Regression, and the name ends in
   `_classification`: a rename waits until the review page is done (its marks are stored under the name). Re-run
   `dataset check` and the task probes.

   **Andrej (2026-11-04, discuss):** We go with B. Also add an explanation to the record.

   **Resolved (2026-11-04, Andrej):** B, runtime regression as sat11_hand_algo_runtime: one row per instance and
   configuration (13,332 rows), the log runtime as target with a timeout at 600 s, `algorithm` a categorical feature,
   the anonymised `instance_id` a scoring column; PAR10 (`par_k`, cutoff 600, k 10) of the configuration predicted
   fastest per instance, the source's metric; feature costs left out and said so; problem classes still held out. The
   record has a CC line explaining the task and why, `problem_type` Regression. The split protocol now gives 3 x 3
   splits (13,332 rows) instead of 10 x 3. The rename (no longer `_classification`) waits until the review page is
   done, as a To do in the record and the curation notes.

   [^1c]: **MET-1** (Must): the declared metric scores the decision of the use case, at the unit the actor acts on.

2. **Keep 3 x 3 splits now that the table has one row per run, or go back to 10 x 3?**

   **Deferred (2026-11-12):** Lennart moved the split count in scored units (rule SPLIT-33) out of this PR into
   its own, to be decided with the other grouped datasets; this issue is reopened there. Until then the protocol
   counts the 13,332 rows: 3 x 3 splits.

3. **Count a timed-out run as the 600 s limit in the target, or as the 6,000 s that PAR10 charges for it?**

   * **Problem:**
     - A run stopped at the 600 s limit has no measured runtime, only "more than 600 s", and the target counts it as
       600 s (the value ASlib stores) while the score charges it 6,000 s, so the models learn a timeout as barely slower
       than a run that finished in 599 s, though picking it costs ten times as much.
     - On the shipped splits no other value of a timeout picks better with every model, but on
       sat11_hand_algo_runtime, which counts a timeout as its limit the same way, counting it as 10 times the limit
       picks better with every model, on 47 to 57 of its 60 splits and by 17 to 19%.
     - Keep the limit, count a timeout as the PAR10 charge in both datasets, or treat timeouts apart (a censored
       model, a timeout classifier, or training without them)?
   * **Background:**
     - What a timeout is: ASlib ran every configuration once on every instance and stopped it at 600 s; a stopped run
       is stored with status `timeout` and runtime 600. Its runtime is right-censored: only a lower bound is known, and
       the run might never have finished. Here 1,963 of the 13,332 runs (15%) are timeouts, on 458 of the 1,212
       instances (38%); every finished run took at most 599.7 s.
     - What PAR10 does with it: it charges 10 times the limit, 6,000 s, a penalty for leaving the instance unsolved
       and no estimate of its runtime. The score reads a timeout from the target (any value at or above 600 s) and
       charges 6,000 s, so 600 and 6,000 s in the target score the same, and the choice changes only what the models
       learn.
     - Why 600 s now: the reframe of issue 1 copied sat11, whose notes give the reason: the limit keeps the order
       within an instance (every finished run is faster) and is enough to compute PAR10. It keeps the order but not
       the size of the step: on the log scale a timeout sits 0.002 above a run of 599 s and 2.3 below what the score
       charges.
     - What the source's tools do[^3a]: ASlib's R package, which runs the library's benchmark selectors through
       LLAMA, hands them the limit with a separate success flag
       ([convertPerf.R](https://github.com/coseal/aslib-r/blob/master/aslib/R/convertPerf.R)); AutoFolio, by claspfolio
       2's group, replaces every timeout by 10 times the limit before it trains
       ([aslib_scenario.py](https://github.com/mlindauer/ASlibScenario/blob/master/aslib_scenario/aslib_scenario.py):
       "Replace all runtime data with PAR10 values for non-OK runs"). For runtime models, Hutter et al. 2014
       ([Algorithm runtime prediction](https://arxiv.org/abs/1211.0906), the section on censored data) found that
       counting a stopped run as finished at the limit biases the predictions down, that dropping stopped runs gives
       the worst errors, and that imputing a runtime beyond the limit gives the best.
   * **Effect on the task:** every benchmark method fits the shipped target, so the value of a timeout sets how
     strongly a model learns to avoid a configuration that times out[^3b]. Training without the timeouts keeps only the
     runs that finished, so a configuration that often fails on a kind of instance looks as fast as its few finished
     runs there: the model learns from the survivors and errs on exactly the configurations a user has to avoid. A
     timeout classifier and a censored model are methods, not data: both read the timeout from the target (the value
     at the limit, or at 6,000 s), so either target allows them.
   * **Experiments:** PAR10 of the pick in seconds (lower is better), in brackets the difference to the shipped 600 s;
     the target on the log scale; small untuned models and TabPFN, each trained once per target and split (TabPFN on
     24 of the 30 shipped splits: no GPU node came up for the last 6). The linear model is a ridge regression per
     configuration (one linear model over all configurations picks the same configuration for every instance).

     | Shipped splits (30, problem classes held out) | LightGBM | Random forest | Linear | TabPFN 3.5 |
     |---|---|---|---|---|
     | 600 s, the limit (shipped) | 704 | 744 | 771 | 791 |
     | 6,000 s, the PAR10 charge | 691 (-13) | 748 (+5) | 763 (-8) | 801 (+11) |
     | Censored: a runtime beyond 600 s imputed from the model | 713 (+9) | 731 (-13) | 764 (-7) | 805 (+14) |
     | Left out of training | 728 (+24) | 736 (-8) | 793 (+22) | 814 (+23) |
     | Timeout classifier and a runtime model of the finished runs, pick by expected PAR10 | 815 (+111) | 814 (+71) | 873 (+102) | 804 (+13) |

     | Other splits | Model | The limit | 10 x the limit | Censored | Left out of training |
     |---|---|---|---|---|---|
     | sat11, instances held out (60 splits, limit 5,000 s) | LightGBM | 8,970 | 7,420 (-1,549) | 7,523 (-1,447) | 14,532 (+5,562) |
     | | Random forest | 8,323 | 6,783 (-1,540) | 7,148 (-1,176) | 15,222 (+6,899) |
     | | Linear | 11,350 | 9,255 (-2,095) | 8,699 (-2,651) | 19,788 (+8,438) |
     | | TabPFN 3.5 | 7,820 | 6,464 (-1,356) | not run | 21,208 (+13,387) |
     | This dataset, instances held out at random as in ASlib's folds (30 splits) | LightGBM | 192 | 141 (-51) | 160 (-32) | 363 (+170) |
     | | Random forest | 204 | 164 (-40) | 177 (-28) | 353 (+148) |
     | | Linear | 315 | 273 (-42) | 249 (-65) | 555 (+241) |

     - On the shipped splits the PAR10 charge, the censored model and training without the timeouts differ from the
       limit by -13 to +24 s, within two standard errors of the paired difference (8 to 27 s), and the sign changes
       with the model; with TabPFN each is a little worse than the limit. The timeout classifier picks worse with the
       three small models (on 21 or 22 of the 30 splits). For scale: always running the configuration most often
       fastest in training gives 880 s, the best possible pick 22 s.
     - Where the training side holds instances like the test instances (sat11's split, and this dataset's instances
       split at random), the PAR10 charge picks better with every model run (on sat11 by 17 to 19%, on 47 to 57 of 60
       splits; here by 13 to 27%, on 26 to 29 of 30), the censored model about as well, and training without the
       timeouts picks worse on every split with every model. The timeout classifier picks better than the limit on
       sat11 too (by 973 to 3,340 s).
     - The split decides it[^3c]: on the same table, with only the split changed, the PAR10 charge goes from no effect
       to a gain of five or more standard errors with each of the three small models. A model learns which
       configuration times out from instances like the one at hand; on a problem class not seen in training it
       cannot, so no value of a timeout helps there, and the timeout classifier's misjudged risk, weighted by 6,000 s,
       decides its picks.
   * **Consistency:** sat11_hand_algo_runtime counts a timeout as its limit (5,000 s) on the log scale for the same
     reason, and its notes name a survival task type, which the framework does not have, as the better form; the two
     share the form and the library, so they should make one choice. A guideline for molecule data says a censored
     value is no regression target[^3d] (the NCI screen, where 97% of the values were censored); here 15% of the runs
     are, and the pick needs every configuration's outcome, so they stay rows (both datasets already drop the
     instances on which every run timed out).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The limit, 600 s (implemented) | a timed-out run's target is the stored 600 s, sat11's 5,000 s | the value the source stores; no number the source did not measure; ASlib's R tools train on it | training charges a timeout a tenth of what the score charges; on sat11 every model picks worse than under B (by 17 to 19%) |
     | B | The PAR10 charge, 10 x the limit | a timed-out run's target is 6,000 s here and 50,000 s in sat11, both on the log scale; the score and its parameters stay | training charges a timeout what the score charges; within noise of A on the shipped splits (-13 to +11 s); better with every model on sat11 and on this dataset split at random; AutoFolio's convention; one line in each definition | a penalty in a column that otherwise holds runtimes, which the notes have to say; sat11's target changes |
     | C | Leave timed-out runs out of training | the timeouts stay in the test folds, where the score needs every configuration's outcome, and leave the training folds | none found | the model learns from the survivors and picks configurations that time out (worse on every split of sat11 and of the random split); the framework has no rows that only the test side sees |
     | D | Timeout classifier plus runtime model | a method, not a change to the data: it reads the timeout from the target, so A and B both allow it | weighs the chance of a timeout by its cost, as PAR10 does; better than A on sat11 | worse with the three small models on the shipped splits (by 71 to 111 s); a method's choice, which a dataset cannot impose |
     | E | Survival or censored regression | a task type with a censoring flag and a loss and metric that use it, or, as a method, a runtime imputed beyond the limit | treats a timeout as what it is, more than 600 s; a task type could also use the 82 instances no configuration solved | the framework has no such task type; as a method it does about as well as B, not better |

   * **Recommendation:** B in both datasets: training then charges a timeout what the score charges, which changes
     nothing measurable on the shipped splits (-13 to +11 s, within one standard error) and picks better with every
     model wherever the timeouts can be learned (sat11, this dataset split at random), and it takes one line in each
     definition. **Decision:** keep the limit (A), or count a timeout as the PAR10 charge in both datasets (B)?

   **Notes for the AI:** on B, `_clean` here sets a run with `runstatus != "ok"` to `10 * 600.0` before the log
   (comment: the PAR10 charge, not a runtime); sat11's `_clean` sets its non-ok runs to `10 * 5000.0` before it drops
   `runstatus`. `par_k` and its params stay (a value at or above the cutoff is a timeout and counts `k * cutoff`), and
   both metric definitions stay true. Update the task summaries' `predicted` ("a run stopped at the limit counts as
   6,000 s, the charge PAR10 gives it"), sat11's `fit_reason` (its sentence on the order within an instance) and the
   timeout bullet of both notes, with the numbers above. Re-run `dataset check` and the task probes on both, a
   CHANGELOG entry, a CC line in both records (checked_by Andrej). The censored model is Schmee and Hahn's imputation
   as in Hutter et al. 2014: a normal model of the log runtime around out-of-fold predictions (folds by problem class
   here, by instance on sat11), three rounds (two for TabPFN), capped at 100 x the limit.

   [^3a]: **CLEAN-1** (Should): clean to the state an expert would ship; read what the source's top solutions and the
     data owners did.
   [^3b]: **MET-3** (Must): the declared metric is the one on the scale the task means, and the target may ship on the
     scale a practitioner models it on; the transform is the definition's modelling choice, and the metric follows the
     task.
   [^3c]: **EV-6** (Should): a claim is proven by a test that could have refuted it; here only the split changed
     between the runs.
   [^3d]: The molecule guideline in molecules.md ("Use case, targets and metrics"): "Censored values are no regression
     target. The NCI screen's EC50 was not reached in 38,048 of 39,365 rows."

   **Andrej (2026-11-06, discuss):** Why does a timeout count as 600s and why log scale? I feel like we need to
   discuss the options here separately. Open a new discussion point for that.

   **Andrej (2026-11-06, discuss):** I am not quite sure I get it right. One thing is how the target is presented, the
   other how we score. The target given to a model should not be adapted here, it should be left to the model, unless
   there is clear evidence that a decision benefits all models equally. How we score should be defined by the domain,
   either the source of the dataset or another objective source.

   **Answer (AI, 2026-11-06):**

   * **The two are separate, and the scoring is already the domain's:** both datasets score the configuration a model
     picks by PAR10, ASlib's own measure for algorithm selection (Bischl et al. 2016, the source of both scenarios): the
     runtime of the pick, a timeout charged at 10 times the limit. Nothing in this issue changes that.
   * **The target as the source gives it:** ASlib stores every timed-out run at exactly the limit: 2,865 runs at
     600 s here, 2,695 at 5,000 s in sat11_hand_algo_runtime; finished runs end below it (599.7 s and 4,995.8 s at
     most). The shipped target is that recorded value, on a log scale, so it is not adapted; option B of this issue
     (6,000 s, the PAR10 charge) would be.
   * **Your bar applied, per dataset:**
     - Here it is not met: on the shipped splits the 6,000 s target picks better with LightGBM and the linear models
       and worse with the forest and TabPFN, all within about two standard errors.
     - In sat11 it is: the PAR10 charge (50,000 s) picks 17% to 19% better with all four models (LightGBM 8,970 to
       7,420 s, the forest 8,323 to 6,783 s, the linear models 11,350 to 9,255 s, TabPFN 7,820 to 6,464 s), on 47 to 57
       of its 60 splits.
   * **Choose:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The recorded value in both (implemented) | timeouts at the limit as ASlib stores them, 600 s here and 5,000 s in sat11 | the source's values everywhere; one form for both | leaves sat11's measured gain for all models unused |
     | B | Recorded here, PAR10 charge in sat11 | this dataset unchanged; sat11 counts a timeout as 50,000 s in the target | follows your bar dataset by dataset | the two datasets of one form present timeouts differently |
     | C | PAR10 charge in both | 6,000 s here, 50,000 s in sat11 | one form, and training charges what the score charges | here no clear evidence, so it adapts the target against your bar |

   * **Recommendation:** B, as your bar reads: keep what the source records unless every model gains, which only
     sat11 shows. The scoring stays PAR10 in both either way.

   **Answer (AI, 2026-11-06):**

   * **For this dataset only:** sat11_hand_algo_runtime has its own decision item now (its issue 3), so this issue
     decides asp_potassco_classification alone.
   * **Choose:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Recorded 600 s (implemented) | a timed-out run's target is the 600 s ASlib stores | the source's value; your bar is not met here | none found |
     | B | PAR10 charge, 6,000 s | a timed-out run's target is 10 times the limit | training charges what the score charges | mixed across models within noise, so it adapts the target against your bar |

   * **Recommendation:** A.

   **Andrej (2026-11-06, discuss):** Reply (A): Recorded 600 s. Also document why we decided this.

   **Resolved (2026-11-06, Andrej):** the recorded 600 s stays (A): the target is the runtime as ASlib records it, and
   how to treat a censored run is left to the models unless a change clearly benefits all models equally, which the
   6,000 s PAR10 charge does not here (within noise, mixed across models). The scoring stays ASlib's PAR10. The reason
   is in the curation notes and the record; sat11_hand_algo_runtime decided the same (its issue 3).

4. **Keep the target on the log scale?**

   * **Problem:**
     - The target is the log of the runtime, and the score undoes the log before it picks the lowest prediction per
       instance, so the scale changes only what the models fit, and on the shipped splits only the log of one plus the
       seconds picks a little better with every model (with a timeout at 600 s), while raw seconds and the PAR10 cost
       in seconds pick worse with both tree models.
     - Runtimes span five orders of magnitude (0.007 to 600 s, 39% of the finished runs under 1 s and 13% over 100 s),
       so on raw seconds a squared-error fit is mostly about the timeouts (70% of the target's variance, 85% when a
       timeout counts 6,000 s), while on the log scale an error counts by its ratio (2 s for a 1 s run weighs as much
       as 200 s for a 100 s run).
     - Keep the log, or ship raw seconds, the log of one plus the seconds, the PAR10 cost in seconds, the rank within
       the instance, or the runtime relative to the instance's fastest run?
   * **Background:**
     - The pick needs only the order of an instance's 11 predictions, and an increasing transform keeps that order, so
       a given set of predictions scores the same on any scale; the base of the log does not matter either[^4a].
     - A model fit by squared error predicts the mean of its target. On the PAR10 cost in seconds that mean is the
       expected cost of running a configuration, the quantity the pick should minimise; on the log scale it is the
       mean log runtime, which ranks a configuration that is usually fast but sometimes times out ahead of what it
       costs on average. In return, the log keeps the few hundred timeouts and slow runs from deciding the whole fit.
     - 85% of the variance of the log runtime lies between instances (how hard an instance is), which does not change
       the pick. A target relative to the instance's fastest run (the log of the ratio) removes it; the rank within
       the instance (1 to 11) keeps only the order and drops the size of each gap, as the fastest-configuration label
       of issue 1 did.
     - The rank and the relative runtime need the instance's other runs, and the score reads the runtime from the
       target, so either would ship the runtime as a scoring column and need a metric that reads it there[^4b].
   * **Effect on the task:** the benchmark methods fit the shipped scale, most by squared error, so it decides what
     their fit is about: the ratios between runtimes (log), the timeouts and slow runs (raw seconds), or the gaps
     within an instance (rank, relative runtime).
   * **Experiments:** PAR10 of the pick in seconds, the same models and splits as in issue 3; in brackets the
     difference to the log with the same value of a timeout.

     | Shipped splits (30) | A timeout counts | LightGBM | Random forest | Linear | TabPFN 3.5 |
     |---|---|---|---|---|---|
     | Log (shipped) | 600 s | 704 | 744 | 771 | 791 |
     | Raw seconds | 600 s | 781 (+77) | 779 (+36) | 723 (-48) | 757 (-33) |
     | Log of one plus the seconds | 600 s | 688 (-16) | 733 (-11) | 750 (-21) | 764 (-27) |
     | Log of the ratio to the instance's fastest run | 600 s | 725 (+21) | 692 (-52) | 771 (0) | 775 (-16) |
     | Log | 6,000 s | 691 | 748 | 763 | 801 |
     | Raw seconds: the PAR10 cost | 6,000 s | 842 (+151) | 814 (+66) | 818 (+55) | 773 (-28) |
     | Log of one plus the seconds | 6,000 s | 706 (+15) | 746 (-2) | 755 (-8) | 758 (-44) |
     | Log of the ratio to the instance's fastest run | 6,000 s | 740 (+49) | 762 (+14) | 763 (0) | 745 (-56) |
     | Rank within the instance | either | 717 | 713 | 807 | 755 |

     | sat11 (60 splits), a timeout at 10 x the limit | LightGBM | Random forest | Linear | TabPFN 3.5 |
     |---|---|---|---|---|
     | Log | 7,420 | 6,783 | 9,255 | 6,464 |
     | Raw seconds: the PAR10 cost | 7,361 (-59) | 7,235 (+452) | 9,009 (-246) | 7,002 (+538) |
     | Log of one plus the seconds | 7,789 (+369) | 6,984 (+201) | 9,056 (-199) | 6,441 (-22) |
     | Log of the ratio to the instance's fastest run | 7,514 (+94) | 5,923 (-860) | 9,255 (0) | 5,737 (-726) |
     | Rank within the instance | 7,039 (-381) | 6,530 (-253) | 7,876 (-1,379) | 6,869 (+406) |

     - On the shipped splits the log of one plus the seconds picks a little better than the log with every model when
       a timeout counts 600 s (by 11 to 27 s; only TabPFN's gain, on 21 of 24 splits, exceeds two standard errors) and
       with two of four at 6,000 s. Raw seconds and the PAR10 cost in seconds pick worse with both tree models (by 36
       to 151 s); the rank and the relative runtime help TabPFN and mostly the forest, and hurt LightGBM. TabPFN picks
       better than with the log on every other scale (by 16 to 56 s). The linear model picks the same with the
       relative runtime as with the log by construction: per configuration it subtracts the same fitted number from
       all 11 runs of an instance.
     - On sat11 no scale beats the log with every model either: the rank picks better with the three small models (by
       4 to 15%) and worse with TabPFN (by 6%), the relative runtime helps the forest and TabPFN (by 11 to 13%), raw
       seconds go either way, and the log of one plus the seconds picks worse with both tree models. With a timeout at
       the limit, raw seconds beat the log on sat11 by 17 to 21% with the three small models, about what the PAR10
       charge of issue 3 gives on the log scale: both make the fit weigh the timeouts more, but on the shipped splits
       here raw seconds lose with the tree models.
   * **Consistency:** sat11_hand_algo_runtime logs its target, and runtime models in the literature predict the log
     runtime (Hutter et al. 2014); AutoFolio trains on raw seconds with a timeout at the PAR10 charge. The house rule
     logs a skewed duration case by case[^4c]; its one exception, an insurance table that ships the claim cost in
     euros, has a metric that scores the predicted level, where PAR10 scores only the order within an instance.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Log of the runtime (implemented) | the target is the log of the seconds, scored after the exponential | an error counts by its ratio, so a few slow runs do not decide the fit; the scale of runtime models and of sat11; no other scale picks better with every model on both datasets | the fitted mean is a geometric mean, which understates a configuration's risk of a timeout unless the target charges it more (issue 3) |
     | B | Raw seconds | the target in seconds, no transform | no transform to explain | the timeouts make up 70% of the target's variance; picks worse with both tree models here (by 36 and 77 s) |
     | C | Log of one plus the seconds | the target is the log of one plus the seconds, scored after the inverse | a little better than the log here with every model when a timeout counts 600 s; it squeezes the 39% of runs under 1 s together, whose differences cost almost nothing in seconds | with a timeout at 6,000 s better with two of four models only; worse with both tree models on sat11 (at 10 x the limit) |
     | D | The PAR10 cost in seconds | raw seconds with a timeout at 6,000 s | a squared-error fit predicts the expected cost, what the pick minimises | the timeouts make up 85% of the variance; picks worse with the three small models here (by 55 to 151 s) |
     | E | Rank within the instance | the target is the run's rank (1 to 11) among its instance's runs; the runtime ships as a scoring column | only the order the pick needs; better than the log on sat11 with the three small models | drops the size of each gap, as the fastest-configuration label did; worse with LightGBM and the linear model here and with TabPFN on sat11; a new metric input and a change of the metric |
     | F | Relative to the instance's fastest run | the target is the log of the runtime over the instance's fastest; the runtime ships as a scoring column | removes how hard an instance is (85% of the log variance), which the pick ignores | helps TabPFN here and on sat11 and the forest on sat11, hurts LightGBM on both; a new metric input and a change of the metric |

   * **Recommendation:** A, the log in both datasets: no scale picks better with every model on both datasets, the
     raw scales lose here with the tree models, the rank, which wins on sat11 with three of four models, loses here
     with two and needs a new metric, and the timeouts are better weighed through issue 3 (B) than through raw
     seconds, which give sat11 the same gain but cost the tree models here. If timeouts stay at 600 s (issue 3, A),
     C is the close second: a little better here with every model, mixed or worse on sat11. **Decision:** keep the
     log (A), or another scale (B to F)?

   **Notes for the AI:** on B or D, `_clean` drops `np.log` and `target_transform` becomes `identity` (on D the
   timeouts are 6,000 s as in issue 3's B); on C, `np.log1p` and `target_transform="log1p"`; on E or F, the runtime in
   seconds ships as a `ScoringColumn`, the target becomes the rank or the log ratio, and `par_k` needs a variant that
   reads the cost from that column (a new input role, a reference implementation and a test against a hand count),
   with the spec's `target_transform` back to `identity`. Any change applies to sat11_hand_algo_runtime too.

   [^4a]: **MET-3** (Must): the declared metric is the one on the scale the task means; the target may ship on the
     scale a practitioner models it on, and the metric is computed after the inverse of both the true values and the
     predictions.
   [^4b]: **MET-2** (Must): every input a metric needs ships as a column and is never a feature.
   [^4c]: **CLEAN-16** (Should): log a skewed positive target (prices, durations, counts) when the source has not, case
     by case. Its exception, pricing_game_2017_french_mtpl: the claim cost ships in euros because its metric, the mean
     Tweedie deviance, scores the predicted cost's level, where a Gini scores only the order (2026-11-03, Andrej).

   **Andrej (2026-11-06, discuss):** Why does a timeout count as 600s and why log scale? I feel like we need to
   discuss the options here separately. Open a new discussion point for that.

   **Resolved (2026-11-06, Andrej):** the log scale kept (A), in this dataset and in sat11_hand_algo_runtime; the
   target ships on the log scale and PAR10 scores the pick after the inverse.

5. **Keep the log loss per instance with a note on the large classes, or count each problem class once?**

   * **Problem:**
     - A row is one instance, and the 96 problem classes hold 1 to 134 instances each (median 5), so the largest 10% of the classes hold 51% of the instances and decide about half of the score.
     - The selector acts per instance, as ASlib scores it, but the split holds out whole classes, "as for a user with a new encoding", and that user meets one class.
     - Should the score stay per instance, with a note that names the imbalance, or should each instance weigh 1 over its class's number of instances, so that each class counts once?
   * **Background:**
     - The instances of a class differ in their inputs (each has its own program statistics and probing runs) and
       often in their fastest configuration; a model picks per instance, and a weight changes only how much each
       instance counts.
     - 7 of the 96 classes hold one instance; a test fold holds 27 to 36 classes and 185 to 720 instances on the 30
       splits measured, so whether a large class falls in a fold sets much of its score.
     - claspfolio 2 and ASlib score the mean over instances on random splits, with no weight per class.
     - Pending on another branch (Andrej, 2026-11-06, not merged here): the task recast as runtime regression scored
       by ASlib's PAR10 per instance. The same question then holds for PAR10, which also averages over instances.
   * **Rules:** the use case decides at which unit the score counts[^asp-unit]; here the decision is per instance
     and the held-out unit is the class, so the rules do not settle it, and the call is a weighing.
   * **Effect on the task:** per instance, a model that suits the few large classes wins; per class, the 7 one-instance
     classes count as much as the class of 134, and a test fold's score rests on its 27 to 36 classes.
   * **Experiments:** the scan of 2026-11-08, 8 untuned predictors (two logistic regressions, random forest, extra
     trees, two LightGBM, kNN and the class shares) on the 30 shipped splits. Kendall tau measures how far two
     orders of the models agree, 1 when they are the same.
     - Per class against per instance: tau 0.86 per split on average (lowest 0.64) and 0.86 for the ranking by the
       mean over the splits; the same best model on 17 of 30 splits.
     - In the ranking by the mean, two pairs swap: extra trees and random forest, tied per instance (log loss 2.218
       and 2.219), and LightGBM and the logistic regression, both far behind the class shares (2.33 per instance).
   * **Consistency:**
     - sat11_hand_algo_runtime, from the same library, scores each instance once; its instances come in families
       that the split neither separates nor weights.
     - superconductivity, pancreatic_cancer_mouse_detection and dementia_prediction, raised by the same scan, have
       an actor who acts per unit; here the selector acts per instance.
     - video_transcoding_time_prediction (the same scan) has the same shape: the actor acts per row, the units are
       very unequal; its issue 1 recommends the same note.
   * **Panel:** none; raised by the one-vote-per-unit scan of 2026-11-08 (boreal_postfire_lichen_biomass issue 7).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per instance (implemented) | log loss over all instances, as now | ASlib's unit of decision; nothing changes | the notes do not say that a few classes decide half the score |
     | B | Per instance, with a note | as A; the notes say that the largest 10% of the classes hold 51% of the instances, and what counting each class once would change | each instance is a decision; the reader knows what the score weighs | a few large classes still decide about half the score |
     | C | Each class counts once | log loss weighted by 1 over the class's instances, a scoring column for the metric only; log loss first gets an optional weight input | one vote per problem class, the held-out unit | the selector does not act per class; a framework change; the best model changes on 13 of 30 splits |

   * **Recommendation:** B: the selector picks a configuration per instance, so each instance is one decision, and a
     note tells the reader that the score leans on a few large classes. **Decision:** A, B or C?

   **Notes for the AI:** numbered 5: the file on the branch that recasts the task (`asp-sat11-par10`, commit
   dee72751) holds issues 1 to 4 with the curator's marks, so this issue starts after them; when the branches meet,
   append this issue after 4 and merge the Outcome and Main points. On B: a dated bullet in `curation_comments`:
   "Each instance is scored once. The 96 problem classes hold 1 to 134 instances (median 5) and the largest 10% of
   them hold 51% of the instances, so the score leans on a few large classes; counting each class once ranks 8
   untuned models at Kendall tau 0.86 per split (0.86 for the ranking by the mean) and changes the best model on 13
   of 30 splits (Lennart, 2026-11-08, review issue 5)." If the PAR10 recast lands, the bullet holds for PAR10 as it
   stands. On C: `log_loss` gets an optional `weight` input (shared with dementia_prediction's issue 1), a
   `class_weight` scoring column, 1 over the class's instances, `inputs={"weight": "class_weight"}` on the stand-in,
   no `sample_weight`, the check's warning accepted as for pancreatic_cancer_mouse_detection; after the recast, PAR10
   (`par_k`) would need the weight instead. Then `dataset check`, the CC line and a CHANGELOG entry.

   [^asp-unit]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole
     group). **MET-1** (Must): the declared metric scores the real task, at the unit the actor acts on.

   **Lennart (2026-11-08, change):** Option B: Per instance, with a note.

   **Resolved (2026-11-08, Lennart):** B, per instance with a note. The score is unchanged; a dated bullet in the
   notes says that each instance is a decision of the selector, that the largest 10% of the problem classes hold 51%
   of the instances, and that counting each class once ranks 8 untuned models at Kendall tau 0.86 per split.

## Reference

@article{hoos2014claspfolio,
  title={claspfolio 2: Advances in algorithm selection for answer set programming},
  author={Hoos, Holger and Lindauer, Marius and Schaub, Torsten},
  journal={Theory and Practice of Logic Programming},
  volume={14},
  number={4-5},
  pages={569--585},
  year={2014},
  publisher={Cambridge University Press}
}
