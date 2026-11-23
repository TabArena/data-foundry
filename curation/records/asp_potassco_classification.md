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
- Experimental Results
collections:
- TabArena Reject
original_source: ASlib
year: '2014'
collection_period: Unknown
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

**Assessment (AI, 2026-11-04):** reviewed without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship; a valid ASlib algorithm-selection task with a modest real signal, but score the chosen configuration's runtime (the source's PAR10, inputs published) instead of log loss on a near-tie-ridden fastest label. Priority 4: gap 1, use case 0, source 1, shape 1, risk -0.

CC (2026-11-04, Andrej): the task is now runtime regression scored by PAR10 (Review issue 1, option B), as sat11_hand_algo_runtime.
- What the task is: one row per instance and clasp configuration (1,212 instances x 11 = 13,332 runs); the model predicts each run's time (log seconds, a run stopped at the 600 s limit counts as 600); per instance the configuration predicted fastest is picked, and the score is PAR10, the mean time of the picks with a timeout counted as 6,000 s. Problem classes are still held out.
- Why: a selector in use learns from the full table of runs, every configuration on every training instance, timeouts included; the fastest-configuration label hid that table from the models. The user loses time mostly to timeouts (96% of the single best configuration's PAR10 comes from them), and log loss scored a pick 0.05 s slower as wrong as a timeout.
- The bar: always running the configuration most often fastest in training gives 611 s, the best possible pick per instance 21 s (30 splits of the earlier definition); a model has to close part of that gap on problem classes it has not seen.
- ASlib's feature costs are left out (the same whichever configuration is picked). To do: rename the dataset (it is no longer a classification).

**Assessment (AI, 2026-11-04):** implemented B in dataset.py: target `runtime` (log), `algorithm` categorical, anonymised `instance_id` a scoring column (role group) of `par_k` (cutoff 600, k 10, `Metric.source`), Grouping on `task_id`; 1,963 timeouts (15% of runs, on 38% of instances) kept at 600 s. `dataset check`: 0 errors, 1 warning (the two constant columns `Removed_Nogoods-1/-2`, already known); par_k computable on every split. The split protocol now gives 3 x 3 splits (13,332 rows) instead of 10 x 3, 32 problem classes per test fold. On the 9 new splits, PAR10 in seconds: untuned LightGBM 699, always the configuration most often fastest in training 754, single best by training PAR10 1,045, best possible 22; LightGBM beats the most-often-fastest rule on 6 of 9 splits, and splits range from 124 to 1,281 s, set by a few problem classes. Task probes (R^2 per row, 5 of 9 splits): random forest 0.57, LightGBM 0.56, linear -0.44, best single feature 0.17, no flags. Leak probes: no single feature above 0.28; 2.0% of test rows have an exact feature copy in train (the instances with repeated features). Group probes: IID R^2 0.90 against grouped 0.53, so the class split matters.

CC (2026-11-05, Andrej): the task summary now says 32 of the 96 problem classes per test fold (it said 27 to 36, a count from the classification splits).

CC (2026-11-06, Andrej): the target stays on the log scale (Review issue 4), and a timed-out run stays at the recorded 600 s (issue 3): the target is the runtime as ASlib records it and how to treat a censored run is left to the models, unless a change clearly benefits all models equally, which counting timeouts at the 6,000 s PAR10 charge does not here (within noise, mixed across models). The scoring stays ASlib's PAR10. Metric and split checked.

CC (2026-11-12, Lennart): the split count in scored units (the review's issue 2, rule SPLIT-33) moves out of this
PR into its own, to be decided with the other grouped datasets and reopened there; it is removed from this record
for now. Until then the protocol counts the 13,332 rows: 3 x 3 splits.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the 96 problem classes hold 1 to 134 instances (median 5), and the largest 10% of them hold 51% of the instances, so a few large classes decide about half of the log loss; the selector acts per instance, and the split holds out whole classes. Weighting each instance by 1 over its class's instances ranks 8 untuned models at Kendall tau 0.86 per split (lowest 0.64) and 0.86 for the ranking by the mean over the 30 shipped splits, the same best model on 17 of 30. Open for Lennart as issue 5 of the record's Review (numbered after issues 1 to 4 of the PAR10 branch); recommended: per instance, with a note that names the imbalance (B).

CC (2026-11-08, Lennart): issue 5, B: scored per instance, with a note. Each instance is a decision of the selector (MET-17); the notes say that the largest 10% of the 96 problem classes hold 51% of the instances and that counting each class once ranks 8 untuned models at Kendall tau 0.86 per split.

CC (2026-11-08, Lennart): the declared metric (log_loss) is checked.

CC (2026-11-12, Andrej): kept after the value study (Review issues 6 A, 7 A); verdict ship, the split and the metric as declared. Measured on the 10 x 3 problem-class splits of that date, which the problem-family split of 2026-11-18 replaced.
- Kept (issue 6): on those splits tuned selectors beat the rule "always run the configuration most often fastest in training" by 180 to 200 s of PAR10 (880 s against 679 to 698 s, about 4 standard errors), and LightGBM fitted per configuration beats the rule on all 11 split sets tried; tuned methods spread from 679 to 884 s.
- Form kept (issue 7): one row per run stays. Against classification of the fastest configuration the picks are mixed by learner (the random forest picks better on the table, TabPFN as classification), and only the table gives a method the runtimes.
- Notes (issue 8): Andrej chose to replace the Task note's baseline numbers (611 s and 646 s, from the classification definition's splits) with the problem-class splits' numbers (rule 880 s, single best solver 996 s, best pick 22 s); not applied, as those splits were replaced on 2026-11-18. Open until re-measured on the family splits.

CC (2026-11-18, Andrej): time basis `UnseenGroup` in place of `Timeless` (Review issue 9, B): the use case picks a configuration for a kind of problem not seen before, so whole problem classes (`task_id`, 96 classes) are held out and each instance's 11 runs stay together. The split is unchanged (grouped 3-fold CV over `task_id`).

CC (2026-11-18, Andrej): Review issue 10, A, as implemented: Grouped 3-fold CV, over whole problem classes (`task_id`, 96 classes of 1 to 134 instances; 7,634-9,658 train / 3,674-5,698 test runs).

CC (2026-11-18, Andrej): "Do both by family" (blind split walk, cross-dataset item on the two algorithm-selection sets, b): the split holds out whole problem families instead of class folders: `problem_family` replaces `task_id`, the class folder with the folders of one generator merged (the 15 problems of the 2007 competition stored twice, HamiltonClumpy's five folders, RLP-150/200, plain and verbose searchTest): 96 folders, 75 families, 25 per test fold, 10 x 3. Why: grouped on the folders, 19% of the test instances (4-45% per fold) had their generator in training. The `UnseenGroup` tag and the grouped 3-fold CV of review issues 9 and 10 stay, now over families. Not built yet.

CC (2026-11-23, Andrej): Review issue 2, B: 10 x 3 splits, counted in the instances PAR10 scores. The split count in scored units (SPLIT-33) is on main (#95), and the protocol reaches it from the data: one runtime per run, so the families do not count; PAR10 scores per instance; each instance's 11 runs sit inside one family. The 1,212 instances leave 694-878 on the train side, below 2,500, so 10 x 3 (the 13,332 runs would give 3 x 3, the 75 families 20 x 3). Supersedes the row count of the CC of 2026-11-12. Not built yet.

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

**Main points:** Resolved: runtime regression scored by PAR10 (1), timeouts at the recorded 600 s (3), the log
scale (4); scored per instance, with a note on the large problem classes (5, Lennart, 2026-11-08). Splits in scored
units, 10 x 3, counted in instances (2, 2026-11-06; confirmed under SPLIT-33 on 2026-11-23). Kept after the value study, since tuned selectors beat
the "most often fastest" rule on every split set tried (6, 2026-11-12), and the table's form kept (7); the notes'
baseline numbers (8) stay open: the numbers chosen on 2026-11-12 were measured on the problem-class splits and need
re-measuring on the family splits. Tagged `UnseenGroup` (9); the class-grouped split kept over ASlib's instance
folds (10), then grouped by problem family, 75 families, 10 x 3 (2026-11-18, not built). The rename (no longer
`_classification`) is still to do.

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
   `_classification`: a rename is left to do. Re-run
   `dataset check` and the task probes.

   **Andrej (2026-11-04, discuss):** We go with B. Also add an explanation to the record.

   **Resolved (2026-11-04, Andrej):** B, runtime regression as sat11_hand_algo_runtime: one row per instance and
   configuration (13,332 rows), the log runtime as target with a timeout at 600 s, `algorithm` a categorical feature,
   the anonymised `instance_id` a scoring column; PAR10 (`par_k`, cutoff 600, k 10) of the configuration predicted
   fastest per instance, the source's metric; feature costs left out and said so; problem classes still held out. The
   record has a CC line explaining the task and why, `problem_type` Regression. The split protocol now gives 3 x 3
   splits (13,332 rows) instead of 10 x 3. The rename (no longer `_classification`) is left as a To do in the record
   and the curation notes.

   [^1c]: **MET-1** (Must): the declared metric scores the decision of the use case, at the unit the actor acts on.

2. **Keep 3 x 3 splits now that the table has one row per run, or go back to 10 x 3?**

   Deferred on 2026-11-12, when Lennart moved the split count in scored units (rule SPLIT-33) out of #79 into its own
   PR; the rule landed on main with #95, so Andrej's decision of 2026-11-06 (B) applies.

   * **Problem:**
     - The table has one row per instance and configuration (13,332 rows for 1,212 instances), and the protocol on
       main counts rows: 3 x 3 splits. PAR10 scores one value per instance, so the noise of the score follows the
       instances; counted in instances the task gets 10 x 3, the splits it would get with one row per instance.
     - Untuned LightGBM on the 9 splits: PAR10 from 124 to 1,281 s; it beats the configuration most often fastest in
       training on 6 of 9.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 3 x 3 (on main) | the protocol counts the runs | no rule change | 9 noisy splits; the count depends on the table's layout |
     | B | 10 x 3 under SPLIT-33 | the protocol counts the instances PAR10 scores | the same splits in either layout | a rule change that moves four more datasets |

   * **Recommendation:** B, with the rule; Andrej chose it on 2026-11-06, before the count left #79. **Decision:** A
     or B?

   **Andrej (2026-11-06, change):** Reply (B): Count the scored groups everywhere

   **Resolved (2026-11-06, Andrej):** B everywhere: the split protocol counts the units the metric scores (SPLIT-33).
   Deferred with the rule on 2026-11-12 and in effect since SPLIT-33 landed (#95): the 1,212 instances PAR10 scores
   give 10 x 3 splits.

   **Resolved (2026-11-23, Andrej):** B, 10 x 3, counted in instances. SPLIT-33 is on main (#95) and decides it from
   the data: the runtime is per run, so the families do not count; PAR10 scores per instance, and each instance's runs
   sit inside one of the 75 families, so the instances count. 1,212 instances leave 694-878 on the train side, below
   2,500. Not built yet.

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

6. **Keep the dataset: do the models beat a simple rule on problem classes not seen in training?**

   Measured on the 10 x 3 splits over the 96 problem-class folders of 2026-11-12 ("the shipped splits" in issues 6 to
   8); since 2026-11-18 the split holds out the 75 problem families (CC of 2026-11-18), on which these numbers were
   not re-measured.

   * **Problem:**
     - Tuned selectors beat the rule "always run the configuration most often fastest in training" by 180 to 200 s on
       the shipped splits (about 4 standard errors, on 22 to 25 of 30 splits), and a LightGBM per configuration beats
       it on all 11 split sets tried.
     - Issue 1's answer left this open: on the 30 splits of the classification definition no untuned model reliably
       beat that rule (611 s), and whether the dataset stays could come back to you.
     - The rule is a stronger bar than ASlib's usual baseline, the single best solver (the configuration with the
       lowest mean PAR10 in training): 880 against 996 s on the shipped splits.
   * **Background:** both rules run one configuration on every instance and need no features. On a split by problem
     class the single best solver follows the timeouts of a few training classes, which the test classes do not share,
     so it times out more (16% of the test instances against 14%). Under a random split of instances both pick the
     same configuration (534 s, issue 3).
   * **Experiments:** PAR10 in seconds on the 30 shipped splits, lower is better. Each method's hyperparameters are
     picked per split from a small grid by an inner 3-fold split by problem class on the training side; seeded models
     are fitted with 3 seeds. Classification fits one row per instance with the fastest configuration as label;
     regression fits the log runtime with a timeout at 600 s, either on the shipped table (one model, the
     configuration a feature) or with one model per configuration. Difference to the rule paired by split.

     | Method | Perspective | PAR10 | Against the rule (SE) | Splits better than the rule |
     |---|---|---|---|---|
     | Random forest, one per configuration | Regression | 679 | -201 (54) | 24 of 30 |
     | LightGBM, one per configuration | Regression | 688 | -192 (46) | 25 of 30 |
     | LightGBM, weighted by the cost of a wrong pick | Classification | 698 | -182 (53) | 22 of 30 |
     | Random forest, weighted by the cost of a wrong pick | Classification | 699 | -181 (50) | 25 of 30 |
     | Random forest on the shipped table | Regression | 714 | -166 (43) | 24 of 30 |
     | TabPFN 3.5, one per configuration | Regression | 715 | -165 (48) | 24 of 30 |
     | Random forests per pair of configurations, weighted votes (AutoFolio's default) | Classification | 718 | -162 (49) | 21 of 30 |
     | k-nearest neighbours | Classification | 732 | -147 (49) | 20 of 30 |
     | TabPFN 3.5 | Classification | 754 | -126 (39) | 25 of 30 |
     | LightGBM on the shipped table | Regression | 787 | -93 (35) | 21 of 30 |
     | LightGBM | Classification | 790 | -90 (48) | 21 of 30 |
     | TabPFN 3.5 on the shipped table | Regression | 838 | -42 (42) | 20 of 30 |
     | Ridge, one per configuration | Regression | 863 | -17 (56) | 16 of 30 |
     | Logistic regression | Classification | 884 | +5 (47) | 20 of 30 |
     | Rule: the configuration most often fastest in training | none | 880 | | |
     | ASlib's single best solver | none | 996 | +117 (39) | 1 of 30 |
     | Best possible pick per instance | none | 22 | | |

     The same comparison on 10 further 10 x 3 split sets drawn like the shipped one (problem classes held out), with
     fixed hyperparameters and one seed; the rule costs 673 to 788 s on them and 880 s on the shipped set:

     | Method (fixed settings) | Mean difference to the rule over the 11 sets | Sets where it beats the rule |
     |---|---|---|
     | LightGBM, one per configuration | -143 | 11 of 11 |
     | Random forest, one per configuration | -97 | 10 of 11 |
     | k-nearest neighbours, classification | -79 | 11 of 11 |
     | Random forests per pair of configurations | -41 | 7 of 11 |
     | Random forest on the shipped table | -29 | 8 of 11 |
     | Random forest, cost-weighted classification | -27 | 7 of 11 |
     | LightGBM, cost-weighted classification | -9 | 6 of 11 |
     | Random forest, classification | +11 | 5 of 11 |
     | LightGBM on the shipped table | +13 | 6 of 11 |
     | LightGBM, classification | +32 | 3 of 11 |
     | Ridge, one per configuration | +75 | 1 of 11 |

     - The signal is real and not one class: without the two classes that move the comparison most (89 and 57
       instances), the best selectors still beat the rule by 115 to 133 s per test instance.
     - The shipped split set is the hardest of the 11 for the rule. One class of 89 instances is solved fastest by
       one configuration on 85 of them in about 10 s, while most others time out there. When that class is held out,
       the rule loses those 85 wins and switches to a configuration that times out on it: in all 10 such folds of the
       shipped set, in 67 of 100 elsewhere. The shipped splits therefore show a margin over the rule about 100 s
       larger than a typical draw, for every method alike.
     - Computing the features costs 1.4 s per instance on average (ASlib's `feature_costs.arff`), which the rule saves
       and the models spend; it changes none of the comparisons.
   * **Consistency:** the task probes kept the dataset twice on log loss (2026-10-06, 2026-10-12). Tuned methods
     spread from 679 to 884 s here[^6a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | as now | tuned methods spread and the best beat the rule on every split set tried | the margin over the rule depends on the split set; LightGBM on the shipped table only matches it on a typical draw (+13 s, 6 of 11 sets), and TabPFN on the shipped table beats it by 42 s (SE 42) even on the shipped splits (issue 7) |
     | B | Retire as `No Signal` | `No (Retired)` | none found | the rule is beaten by about 4 standard errors on the shipped splits |

   * **Recommendation:** A: the methods spread, and the best of them beat even the stronger rule on every split set.
     **Decision:** keep (A) or retire (B)?

   **Notes for the AI:** none on A.

   [^6a]: **TP-3** (Must): if tuned methods spread, keep the dataset.

   **Resolved (2026-11-12, Andrej):** kept (A): the tuned methods spread, and the best beat the "most often fastest"
   rule on every split set tried. Nothing in the definition changes; the record has a CC line.

7. **With the tuned results, does the table's form (one row per run, issue 1 B) still stand?**

   * **Problem:**
     - Issue 1 chose runtime regression on one row per instance and configuration over classification of the fastest
       configuration, on untuned picks that favoured neither.
     - Tuned, the best selectors are ones a benchmark method does not build by itself on either form: one model per
       configuration, or a classifier weighted by the cost of a wrong pick; a benchmark method fits the shipped table
       as one model with the configuration as a feature.
     - Should the form change?
   * **Experiments:** the tuned runs of issue 6, PAR10 in seconds on the shipped splits. "Shipped table" is what a
     benchmark method fits now; "classification" is what it would fit on issue 1's option C (one row per instance, the
     runtimes in scoring columns that it never sees).

     | Learner | Shipped table (regression, one model) | Classification | One model per configuration | Classification weighted by the cost of a wrong pick |
     |---|---|---|---|---|
     | LightGBM | 787 | 790 | 688 | 698 |
     | Random forest | 714 | 807 | 679 | 699 |
     | Extra trees | 807 | 782 | 765 | 762 |
     | TabPFN 3.5 | 838 | 754 | 715 | not run (no sample weights) |
     | Linear | not run (picks one configuration for every instance) | 884 | 863 | 776 |

     - Between the two forms a benchmark method would fit, the evidence is mixed: the random forest picks better on
       the shipped table (by 93 s), TabPFN as classification (by 84 s), LightGBM and extra trees about the same.
     - Both better selectors need the runtimes: one model per configuration is open to a method on the shipped table
       (the configuration is a column), and a cost weight is open to neither form, since a method on option C never
       sees the runtimes.
     - Per learner, one model per configuration picks better than one model on the shipped table (by 35 to 123 s):
       the shipped form tests whether a method learns that the features act differently per configuration.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One row per run (implemented) | as issue 1 B | a method sees every run, and can fit per configuration | fitted as one model, LightGBM only matches the rule on a typical split set and TabPFN beats it by 42 s (SE 42) on the shipped one (issue 6) |
     | B | Classification, runtimes as scoring columns | issue 1 C | TabPFN picks better than on the shipped table | the random forest picks worse; methods never see a runtime or a timeout; a new metric |

   * **Recommendation:** A: no form is better for every learner, and only the shipped table gives a method what the
     best selectors use. **Decision:** keep the form (A) or go back to classification (B)?

   **Notes for the AI:** none on A.

   **Resolved (2026-11-12, Andrej):** the form stays (A), one row per instance and configuration, scored by PAR10;
   issue 1's decision stands. Nothing in the definition changes; the record has a CC line.

8. **Update the notes' baseline numbers to the shipped splits?**

   * **Problem:**
     - The Task bullet of `curation_comments` gives the numbers of the classification definition's splits: the rule
       at 611 s and untuned LightGBM at 646 s, which read alone say that a model loses to the rule.
     - On the shipped splits the rule costs 880 s, the best tuned selector 679 s and LightGBM fitted on the table as
       shipped 787 s (issue 6).
     - Keep the old sentence, or give the shipped splits' numbers?
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave the sentence (implemented) | as now | none found | numbers of splits the dataset no longer ships, which suggest no model beats the rule |
     | B | Replace it with the shipped-split numbers | the sentence names both rules, the best pick and the range of tuned selectors on the shipped splits, and that the rule's cost varies with the split set | a user gets the bar to beat on the splits they use | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, the Task bullet of `curation_comments` gets the bar to beat on the shipped splits: both
   rules, the best pick per instance and the tuned selectors; `dataset check`.

   **Andrej (2026-11-12, change):** Option B: Replace it with the shipped-split numbers.

   **Note (AI, 2026-11-23):** not applied. The numbers of option B (the rule 880 s, ASlib's single best solver 996 s,
   the best pick 22 s, a tuned random forest per configuration 679 s, tuned LightGBM on the table 787 s) were measured
   on the problem-class splits that the problem-family split of 2026-11-18 replaced (CC of that date), so they are not the
   shipped splits' numbers any more. The Task bullet still gives the classification definition's 611 s and 646 s.
   Open until the baselines are re-measured on the 75-family splits.

9. **Time basis: tag the class-grouped folds `UnseenGroup` instead of `Timeless`?**

   * **Problem:**
     - The tree's leaf for repeated measurements says that where the use case holds out a wider group (a problem class), the split groups on it and is tagged `UnseenGroup`; the definition groups on the problem class `task_id` but is tagged `Timeless`.
     - The use case asks for a configuration 'for a kind of problem not seen before', and the folds hold out whole classes (96 classes of 1 to 134 instances).
     - Only the tag and the opening of the `Time basis:` line differ; the grouping and the folds stay.
   * **Background:** Runs of a designed benchmark, 11 per instance, with no arrival order. The stated use is a kind of problem not seen before, so whole problem classes (task_id) are held out with all their instances and runs. Confidence of the blind walk: high.
   * **Walk:** the questions as answered without the current split[^tree]:
     - Is there an order to how samples arrive in the use case? (use case): no. Evidence: Benchmark runs of 11 clasp configurations on fixed instances; no run dates (dossier collection_period: 'no run dates are given'). Algorithm selection treats each instance as a property-of-item query.
     - Was the experiment repeated, producing several rows for the same measurement? (data): yes. Evidence: Each instance has 11 rows, one per configuration (13,332 = 1,212 x 11; instance_id is a scoring column used by the metric to pick per instance).
     - Does the model meet new items, or further measurements of items it has measured? (use case): new items, and a wider group: a new problem class. Evidence: Use case: 'predicts the runtime of each configuration on a new problem instance ... here for a kind of problem not seen before'. The problem class (task_id, 96 classes from the instance path) is computed from the data, so group on it and tag UnseenGroup; instances nest in classes, so each instance's 11 runs stay together.
   * **What the blind dossier lacked, and what it changes:** none. The definition ships whole problem classes held out (task_id, 96 classes of 1 to 134 instances, 32 per test fold), the same leaf. The definition also notes that only ASP-Comp-2007/-2009/-2011 class paths name a year, so no time split is possible, which confirms the 'no order' answer.
   * **What changes:** `data_tags = ("UnseenGroup",)` in `dataset.py`; the `Time basis:` bullet in `curation_comments` opens with `UnseenGroup` (whole problem classes held out) and keeps that no split by time is possible; a CC line in the record.
   * **Blindness:** what the walker saw of the shipped split before deciding: saw: split_tree.md lists asp_potassco_classification as an example under 'Grouped · Timeless (the measurement)'; ignored as evidence.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Grouped 3-fold CV, 3 repeats, over whole problem classes (`task_id`, about 32 classes per test fold; 7,634-9,658 train / 3,674-5,698 test runs of 13,332), `Timeless` (implemented) | No change. | The tag says the runs have no time dimension: one campaign on one machine, only three class paths name a year. | The tag does not name what the folds test, a problem class not seen in training, which the tree's rule asks the tag to say. |
     | B | The same class-grouped folds, tagged `UnseenGroup` | `data_tags` Timeless becomes UnseenGroup; the `Time basis:` line opens with the held-out classes and keeps that no time split is possible; the folds do not change. | Names the transfer to a new problem class, the use case and the tree's rule for a wider group. | A tag-only change still rebuilds the container, as `data_tags` ship in it. |

   * **Recommendation:** B, because the tree's leaf tags a split on a wider group the use case names (a problem class) `UnseenGroup`.. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: set `data_tags` to `UnseenGroup` in `dataset.py`, change the opening of the `Time basis:` bullet and add a CC line; rebuild. No change to the split declaration.

   [^tree]: **SPLIT-36** (Should): walk the decision tree from the record's collection type, answering each question as if no split had been decided; a split the source prescribes is evidence, not an answer.

   **Andrej (2026-11-18, change):** Option B: The same class-grouped folds, tagged UnseenGroup.

   **Resolved (2026-11-18, Andrej):** B. `data_tags` names `UnseenGroup` in place of `Timeless`, and the `Time basis:` line opens with `UnseenGroup (Andrej, 2026-11-18; Timeless before)`: the use case picks a configuration for a kind of problem not seen before, so whole problem classes (`task_id`, 96 classes) are held out and each instance's 11 runs stay together; it keeps that no split by time is possible. The folds (grouped 3-fold CV over `task_id`) are unchanged.

10. **Split: ASlib's 10-fold CV over random instances (cv.arff) instead of 3-fold CV over whole problem classes?**

   * **Problem:**
     - ASlib's cv.arff draws instances at random into 10 folds (one repetition), keeping an instance's 11 configuration runs together, so 90 of the 96 problem classes have instances on both sides.
     - The use case asks for a kind of problem not seen before, which only folds over whole classes test.
     - The source split can be rebuilt: cv.arff in the same ASlib folder gives each instance's fold (not in our download yet).
   * **Source split:** yes, ASlib scenario ASP-POTASSCO (cv.arff); claspfolio 2 paper (random halves): 10-fold CV over instances, random; all 11 configuration runs of an instance in one fold; 90 of 96 problem classes span several folds (counted on cv.arff) ("cv.arff: instance_id, repetition, fold (10 folds, 1 repetition)") https://github.com/coseal/aslib_data/tree/master/ASP-POTASSCO. Credible: partly, Keeping an instance's runs together follows the selector's use (a new instance); the random draw over instances is a benchmark convention for comparability, with no stated reason to let classes cross folds.. Against the tree's leaf: partly, ASlib's 10-fold CV keeps an instance's 11 runs together (the measurement level of the leaf) but draws instances at random so classes cross folds; the blind leaf holds out whole classes because the use case names a kind of problem not seen before.
   * **Why it counts as chosen, not conventional:** Keeping an instance's runs together follows the selector's use (a new instance); the random draw over instances is a benchmark convention for comparability, with no stated reason to let classes cross folds.
   * **What changes on B:** the definition's split declaration is replaced by the source's own construction (its files, periods or groups), and the `splits_comment` records that the tree's leaf was not followed. The rows, features, target and metric do not change; the folds do, so the container is rebuilt.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Grouped 3-fold CV, 3 repeats, over whole problem classes (`task_id`, 96 classes of 1 to 134 instances; 7,634-9,658 train / 3,674-5,698 test runs) (implemented) | No change; `splits_comment` names ASlib's instance folds as the source's split. | Tests a configuration on a problem class absent from training, the stated use. | Not comparable to ASlib or claspfolio 2 results; fold sizes vary with class size (3,674 to 5,698 test runs). |
     | B | ASlib's split: 10 folds over instances from cv.arff (about 121 instances, 1,333 runs per test fold), one repetition, each instance's 11 runs in one fold | `download_description` adds cv.arff; `grouping` on `instance_id` with ASlib's fold ids replaces the class grouping. | Comparable to ASlib's published results; tests a new instance of a known class. | 90 of 96 classes sit on both sides, so a new kind of problem is not tested; one repetition. |

   * **Recommendation:** A, because the use case is a problem class not seen before, and ASlib's random instance folds let 90 of 96 classes into training.. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: replace the split declaration with the source's construction (name the files or periods it uses) and say in `splits_comment` why the tree's leaf is not followed; on A: name the source's split in `splits_comment` as a departure.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: Grouped 3-fold CV, over whole problem classes (`task_id`, 96 classes of 1 to 134 instances; 7,634-9,658 train / 3,674-5,698 test runs).

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
