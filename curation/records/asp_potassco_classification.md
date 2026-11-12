---
unique_name: asp_potassco_classification
name: ASP-POTASSCO-classification from aslib_data
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: ASlib
year: '2014'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
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

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the 96 problem classes hold 1 to 134 instances (median 5), and the largest 10% of them hold 51% of the instances, so a few large classes decide about half of the log loss; the selector acts per instance, and the split holds out whole classes. Weighting each instance by 1 over its class's instances ranks 8 untuned models at Kendall tau 0.86 per split (lowest 0.64) and 0.86 for the ranking by the mean over the 30 shipped splits, the same best model on 17 of 30. Open for Lennart as issue 5 of the record's Review (numbered after issues 1 to 4 of the PAR10 branch); recommended: per instance, with a note that names the imbalance (B).

CC (2026-11-08, Lennart): issue 5, B: scored per instance, with a note. Each instance is a decision of the selector (MET-17); the notes say that the largest 10% of the 96 problem classes hold 51% of the instances and that counting each class once ranks 8 untuned models at Kendall tau 0.86 per split.

CC (2026-11-08, Lennart): the declared metric (log_loss) is checked.

## Review

**Outcome:** added. In the working copy since the migration; a scan of 2026-11-08 for units with unequal numbers of
rows (raised on boreal_postfire_lichen_biomass's issue 7) found that the problem classes the split holds out hold 1 to
134 instances each, so a few large classes decide about half of the log loss. Resolved on 2026-11-08: scored per
instance, with a note on the large classes (issue 5).

**Main points:** Open: none. Resolved on 2026-11-08: scored per instance, each instance a decision of the selector,
with a note that the largest 10% of the problem classes hold 51% of the instances (issue 5).

**Issues for Lennart:**

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
