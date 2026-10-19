# force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition

**Outcome:** added. The lithology (11 classes, log loss) of each depth sample in 118 North Sea wells, from all
three competition files stacked and split by well. GROUP and FORMATION stay as features, as the competition gave
them; the rows carry no depth-window features. The AI recommends shipping it.

**Main points:** Grouped by well. Open: GROUP and FORMATION as features, depth context. Untuned LightGBM diverges
on this data.

**Record judgment:** valid with concerns: the depth context, the interpreted stratigraphy as features, and the
label noise (the organisers put the reachable accuracy near 80%). Well logs are sensor readings per depth, not a
vectorised image, so SEL-13 (criterion 4A) does not exclude them.

**Issues for Lennart:**

1. **Depth context.** May a model use the other depths of the same well, and should the dataset ship depth-window
   features? Evidence: the whole log of a new well exists before it is interpreted; the starter notebook keeps WELL
   "so the data can be separated per well. This will be necessary for any 'windowed' approaches"; the winners used
   "windowing and gradients" (retrospective p. 3), H3G and DavidP rolling windows. Measured (random forest, 3 grouped
   folds): gradients plus 21-sample means and spreads of 9 logs per well move log loss 0.776 -> 0.764 and macro AUC
   0.911 -> 0.923 (better on 2 of 3 folds). Implemented: raw per-depth rows, `context="all_rows"`, no window features
   (feature engineering is the pipeline's job). Alternatives: `context="none"` (each depth from its own row, as
   electric_motor and sepsis), which is what a row-wise harness does anyway; or add the window features in `_clean`,
   as electric_motor adds the source study's EWMA features (small gain here).

2. **GROUP and FORMATION (NPD lithostratigraphy) as features.** They are an interpretation of the same well that
   names rock units (Zechstein = evaporites). They are the strongest single features (FORMATION macro AUC 0.864,
   GROUP 0.833); without both the forest's log loss rises 0.776 -> 0.836 (macro AUC 0.911 -> 0.894). They are not
   the label interpretation: every top in the Zenodo NPD_Lithostratigraphy_*.xlsx files has Interpreter NPD and a
   whole-metre MD, and the deepest top above each sample reproduces GROUP on 100% and FORMATION on 99.95% of the
   rows; only 10% of the 574 group boundaries fall on a lithology change at the same sample (2.8% of consecutive
   samples), and NPD's BASEMENT in 35/9-2 (139 rows) is labelled Shale. Their strength is that units hold rare
   classes (14,709 of 14,711 Halite rows in the Zechstein group, 14,014 of 14,043 Chalk rows in the Shetland group).
   Implemented: kept, because the source's task lists them as inputs ("provided NPD lithostratigraphy").
   Alternative: a logs-only task without them, if formation tops are judged to come too late in a real workflow.

3. **Untuned LightGBM diverges on this data.** With its default `min_child_weight` of 0.001 (grouped fold 0, 100k
   rows): training accuracy 0.73-0.78, test log loss 14-15, 66-79% of predictions above p = 0.999; with
   `min_child_weight=1` log loss 0.81 and macro AUC 0.91; learning rate 0.05 with `min_child_samples=200`: 0.76.
   Not a data fault and nothing changed in the definition, but worth checking TabArena's LightGBM default on this
   dataset before reading its rank. The verifier reports that learning rate 0.05 with early stopping on held-out
   training wells stops at 43-45 iterations with log loss 0.79-0.81 (its log is empty, so I could not confirm the
   numbers).

4. **Metric.** The competition scored a 12 x 12 penalty matrix on hard labels (starter notebook,
   `penalty_matrix.npy`); none of the top three trained on it (retrospective p. 3-4). Implemented: default log loss.
   Alternative: register a custom expected-penalty metric (11 x 11 after dropping Basement). The forest's penalty
   score is -0.66 on the grouped folds (winner on the 10 blind wells: -0.469).

7. **Record follow-ups.** The record's own comment asks to "update GitHub issue!" once checked
   (TabArena/tabarena_dataset_curation#2 is open, milestone tabarena-v0.2). Domain kept as the record's "chemistry &
   material science"; "environmental science & climate" would be the alternative for subsurface geology.
