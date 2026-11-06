---
unique_name: asp_potassco_classification
name: ASP-POTASSCO-classification from aslib_data
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
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

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Ship; a valid ASlib algorithm-selection task with a modest real signal, but score the chosen configuration's runtime (the source's PAR10, inputs published) instead of log loss on a near-tie-ridden fastest label. Priority 4: gap 1, use case 0, source 1, shape 1, risk -0.

CC (2026-11-04, Andrej): the task is now runtime regression scored by PAR10 (option B of the review page), as sat11_hand_algo_runtime.
- What the task is: one row per instance and clasp configuration (1,212 instances x 11 = 13,332 runs); the model predicts each run's time (log seconds, a run stopped at the 600 s limit counts as 600); per instance the configuration predicted fastest is picked, and the score is PAR10, the mean time of the picks with a timeout counted as 6,000 s. Problem classes are still held out.
- Why: a selector in use learns from the full table of runs, every configuration on every training instance, timeouts included; the fastest-configuration label hid that table from the models. The user loses time mostly to timeouts (96% of the single best configuration's PAR10 comes from them), and log loss scored a pick 0.05 s slower as wrong as a timeout.
- The bar: always running the configuration most often fastest in training gives 611 s, the best possible pick per instance 21 s (30 splits of the earlier definition); a model has to close part of that gap on problem classes it has not seen.
- ASlib's feature costs are left out (the same whichever configuration is picked). To do: rename the dataset (it is no longer a classification) once the review page is done; its marks are stored under this name.

**Assessment (AI, 2026-11-04):** implemented B in dataset.py: target `runtime` (log), `algorithm` categorical, anonymised `instance_id` a scoring column (role group) of `par_k` (cutoff 600, k 10, `Metric.source`), Grouping on `task_id`; 1,963 timeouts (15% of runs, on 38% of instances) kept at 600 s. `dataset check`: 0 errors, 1 warning (the two constant columns `Removed_Nogoods-1/-2`, already known); par_k computable on every split. The split protocol now gives 3 x 3 splits (13,332 rows) instead of 10 x 3, 32 problem classes per test fold. On the 9 new splits, PAR10 in seconds: untuned LightGBM 699, always the configuration most often fastest in training 754, single best by training PAR10 1,045, best possible 22; LightGBM beats the most-often-fastest rule on 6 of 9 splits, and splits range from 124 to 1,281 s, set by a few problem classes. Task probes (R^2 per row, 5 of 9 splits): random forest 0.57, LightGBM 0.56, linear -0.44, best single feature 0.17, no flags. Leak probes: no single feature above 0.28; 2.0% of test rows have an exact feature copy in train (the instances with repeated features). Group probes: IID R^2 0.90 against grouped 0.53, so the class split matters. Evidence: ~/claude_jobs/ba_marks_1104/asp_potassco_classification/.

CC (2026-11-05, Andrej): the splits now count instances, not runs: 10 repeats of 3 folds (30 splits) where the 13,332 runs gave 3 x 3. The score is one PAR10 per instance, so its noise depends on the 1,212 instances, not on the 11 rows each has; counted this way the task gets the splits it would get with one row per instance. The same count moves sat11_hand_algo_runtime from 10 x 3 to 20 x 3, open for confirmation in the folder's REVIEW.md (issue 2). The task summary now says 32 of the 96 problem classes per test fold (it said 27 to 36, a count from the classification splits).

CC (2026-11-06, Andrej): the split count follows the scored units everywhere (review page issue 2, B; new rule SPLIT-33): 1,212 instances give 10 x 3 splits. The same count moves sat11_hand_algo_runtime to 20 x 3. Timeouts and the log scale of the target are open as their own questions on the review page.

CC (2026-11-06, Andrej): the target stays on the log scale (review page issue 4), and a timed-out run stays at the recorded 600 s (issue 3): the target is the runtime as ASlib records it and how to treat a censored run is left to the models, unless a change clearly benefits all models equally, which counting timeouts at the 6,000 s PAR10 charge does not here (within noise, mixed across models). The scoring stays ASlib's PAR10. Metric and split checked.

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
