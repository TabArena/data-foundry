# pancreatic_cancer_mouse_detection

**Outcome:** added. In the working copy since the migration; a scan of 2026-11-08 for units with unequal numbers of
rows (raised on boreal_postfire_lichen_biomass's issue 7) found that the ROC AUC counts a mouse once per serum sample,
1 to 6 times. Resolved on 2026-11-08: each mouse counts once in the ROC AUC (issue 1).

**Main points:** Open: none. Resolved on 2026-11-08: each mouse counts once in the ROC AUC, weighted by 1 over its
number of serum samples (issue 1).

**Issues for Lennart:**

1. **Count each mouse once in the ROC AUC, or each serum sample, as now?**

   * **Problem:**
     - A row is one serum spectrum, and the 73 mice gave 1 to 6 samples each (median 2, 29 mice one), so a mouse bled six times counts six times in the ROC AUC.
     - The label is the mouse's (PanIN or control), and the use case reads each sample of an unseen mouse as "a new patient's test", so one mouse stands for up to six patients.
     - Should each sample weigh 1 over its mouse's number of samples in the score, so that each mouse counts once while each sample is still read on its own?
   * **Background:**
     - 181 spectra: 80 of 35 PanIN mice and 101 of 38 control mice; the largest 10% of the mice hold 25% of the
       spectra. The release gives no bleed dates; the paper says the bleeds were at least 5 days apart.
     - Unlike superconductivity and boreal_postfire_lichen_biomass, the inputs differ between a mouse's samples (each
       bleed has its own spectrum), so a model gives each sample its own score; the weight changes only how much each
       sample counts.
     - Weighted this way, the ROC AUC is the chance that a random sample of a random PanIN mouse scores above a random
       sample of a random control mouse.
     - One prediction per mouse from all its samples would change the use case (a test from one serum sample) and is
       not proposed.
   * **Rules:** the use case decides at which unit the score counts[^pc-unit]. The rules ask for the score weight to be
     the training weight when it is a realized amount at risk, and waive that when it follows from the inputs[^pc-weight];
     this weight is neither, so B accepts the check's warning with a reason the rules do not name yet (a weight that
     gives each unit one vote).
   * **Effect on the task:** per sample, a mouse bled often decides more of the score; per mouse, each animal, the
     study's stand-in for a patient, counts once. With about 24 test mice per fold, a mouse with five or six samples
     moves a fold's AUC more per sample than per mouse.
   * **Experiments:** the scan of 2026-11-08, 8 untuned predictors (two logistic regressions, random forest, extra
     trees, two LightGBM, kNN and the class shares) on 30 of the shipped splits, on the raw spectrum standardized per
     bin (not the recommended encoding).
     - The weighted score ranks the models like the per-sample one at Kendall tau 0.66 per split on average (lowest
       -0.07, on 24 test mice) and 0.86 for the ranking by the mean over the splits; the same best model on 23 of 30
       splits. Kendall tau measures how far two orders of the models agree, 1 when they are the same.
     - In the ranking by the mean, two pairs swap, both near ties: the two LightGBM (ROC AUC 0.582 and 0.579 per
       sample) and kNN against the class shares (0.4999 and 0.5000 per mouse). The logistic regression leads under both
       (0.665 per sample, 0.644 per mouse).
     - The largest shift of the scan (boreal_postfire_lichen_biomass: 0.81 per split, 0.86 for the mean).
   * **Consistency:**
     - boreal_postfire_lichen_biomass counts each plot once since 2026-11-08[^pc-boreal]; there every input belongs to
       the plot, here only the label belongs to the mouse.
     - micro_mass counts each strain once in its score (1 to 6 spectra per strain); musk and
       fraud_detection_in_electricity_and_gas_consumption_1m predict once per group, a different use case.
     - The same scan raised superconductivity (per composition) and dementia_prediction (per person).
   * **Panel:** none; raised by the one-vote-per-unit scan of 2026-11-08 (boreal_postfire_lichen_biomass issue 7).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per sample (implemented) | ROC AUC over all spectra | fits a person tested again and again, each test a decision; nothing changes | a mouse counts by how often it was bled, up to six times |
     | B | Each mouse counts once | ROC AUC weighted by 1 over the mouse's samples, a scoring column for the metric only; ROC AUC first gets an optional weight input | one vote per animal, the unit that stands for a patient; the pattern boreal follows | a framework change; the check's warning accepted with a reason the rules do not name yet; on 24 test mice the per-split ranking stays noisy |

   * **Recommendation:** B, since the use case reads each mouse as a new patient; A if the use case is a person tested
     again and again, each test a decision, and then the use case says so. **Decision:** A or B?

   **Notes for the AI:** on B: (1) `roc_auc` takes no `weight` today; give it an optional row weight in
   `src/data_foundry/v2/metrics.py` (scikit-learn's `sample_weight`, `optional_inputs=("weight",)`,
   `weighted_definition` so the unweighted spec and the built containers' checksums stay unchanged), with a test, as
   `rmse` got for boreal; (2) in `_load_raw`, add `mouse_weight`, 1 over the mouse's number of samples
   (`1.0 / df.groupby("mouse_id")["mouse_id"].transform("size")`), declared as
   `ScoringColumn(column="mouse_weight", role="weight", used_by="roc_auc", ...)`; (3)
   `Metric.fallback(reason=..., inputs={"weight": "mouse_weight"})`, the reason adding that each mouse counts once;
   no `sample_weight`; (4) accept `task_metric_weight_without_sample_weight`: a design weight of the score that gives
   each mouse one vote (SPLIT-23), not an amount at risk (MET-15) nor a survey weight (MET-16); it does not follow
   from the inputs, so the main session adds this reading to MET-15 (or, if the curator prefers, declares it as the
   `sample_weight` too); (5) the grouping's definition and the task summary's `split` keep "each sample read on its
   own" and add the weighting; `dataset check`, the CC line, a CHANGELOG entry, a Cases row in metrics.md. On A:
   reword the use case so that each test sample is one test of a person tested repeatedly, and add a note that a
   mouse counts by its number of samples (tau 0.66 per split against one vote per mouse).

   [^pc-unit]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole
     group). **MET-1** (Must): the declared metric scores the real task, at the unit the actor acts on.
   [^pc-weight]: **MET-15** (Must): a realized denominator is the metric's row weight and the task's sample weight; a
     metric weight that is a function of the features needs no sample weight, and the bundle check
     `task_metric_weight_without_sample_weight` is then accepted with that reason. **MET-16** (Should): a survey or
     design weight is never a feature, and the task is scored unweighted unless the use case is a population estimate
     (boreal's `plot_weight` was read as no such weight: it is ours, not the source's).
   [^pc-boreal]: boreal_postfire_lichen_biomass, issue 7, Lennart, 2026-11-08: "Option B: Each plot counts once."

   **Lennart (2026-11-08, change):** Option B: Each mouse counts once.

   **Resolved (2026-11-08, Lennart):** B, each mouse counts once. `roc_auc` got an optional `weight` input, and the
   ROC AUC is weighted by `mouse_weight`, 1 over the mouse's number of samples, a scoring column for the metric only
   with no training weight (Lennart's rule of 2026-11-08: a one-vote weight is for scoring only, also when it does not
   follow from the inputs; training with it measured -0.015 ROC AUC). Each sample is still read on its own; the use
   case now says each mouse counts once, as one patient.
