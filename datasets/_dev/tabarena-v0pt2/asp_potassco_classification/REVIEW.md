# asp_potassco_classification

**Outcome:** added. In the working copy since the migration; a scan of 2026-11-08 for units with unequal numbers of
rows (raised on boreal_postfire_lichen_biomass's issue 7) found that the problem classes the split holds out hold 1 to
134 instances each, so a few large classes decide about half of the log loss. The AI recommends keeping the score per
instance and naming the imbalance in the notes (issue 5).

**Main points:** Open: issue 5, keep each instance's vote with a note, or count each problem class once?

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
