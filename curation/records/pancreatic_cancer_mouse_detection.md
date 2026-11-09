---
unique_name: pancreatic_cancer_mouse_detection
name: NCI Pancreatic
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Many features
- Non-IID (Grouped)
- Spectral Data
collections:
- FS Benchmark
original_source: Other
year: '2003'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://home.ccr.cancer.gov/ncifdaproteomics/CancerCellPanINDataBinned.zip
- https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp
notebook_path: datasets/beyond_iid/grouped/pancreatic_cancer_mouse_detection/pancreatic_cancer_mouse_detection.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/pancreatic_cancer_mouse_detection/dataset.py
source_row: 1035
type_adapter_id: curation-record-v1
---

## Comments

Original data is multiple serums collected per mouse

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid tiny, high-dimensional task after the task-probe review (flag `unstable`). Grouped by mouse, each test fold holds about 12 PanIN and 13 control mice. The signal is weak but real: on BeyondArena RealTabPFN-2.5 (ROC AUC 0.664), EXAONE (0.654) and TabSwift (0.628) beat 0.5 on all 11 of their folds, while the median of 29 configurations is 0.54 (gradient-boosted trees near chance). Open question, the one that could make this a batch-effect case like prostate_cancer_detection (same NCI-FDA data bank, retired for processing artefacts; Baggerly et al. 2004 found such artefacts in the program's ovarian spectra): the file names' `t` suffix (42% of control spectra, 30% of PanIN spectra; 37 of the 73 mice have spectra with and without it). Within the controls, `t` spectra separate from the others at ROC AUC 0.67 (logistic model, grouped by mouse); within PanIN they do not (0.45). The suffix alone could explain at most about AUC 0.56 of the label, which reaches 0.63-0.66, so the label signal is not only the suffix; what `t` marks needs the authors.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — the paper reports sensitivity and specificity at its classifier's operating point, with no single threshold-free metric.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `debernardi_urinary_pancreatic_cancer` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-02, Lennart): The serum spectrum is declared as a spectrum (`spectra`, CLEAN-26; PR #21, Andrej's proposal): it ships raw as the NCI-FDA page publishes it (6,771 bins of 400 ppm, m/z 800 to 11,993), the container records the bins in m/z order as a feature group, and the benchmark encodes it row by row, by default with MALDIquant's steps (square root, Savitzky-Golay over 21 points, SNIP baseline, total ion current). On the 60 shipped splits the default lifts the tree models by 0.10 to 0.15 ROC AUC, PLS-DA by 0.06 and TabPFN v3.5 by 0.03 (0.659 to 0.690); logistic regression loses 0.02. A reconstruction of PR #21's own chain, which ends in a log, scores higher for TabPFN (0.716) and the linear models; the default stays the published workflow. Full resolution: the width is the benchmark's feature-limit step's job.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the 73 mice gave 1 to 6 serum samples each (median 2, 29 one), the label is the mouse's, and the use case reads each sample of an unseen mouse as a new patient's test, so a mouse bled six times counts as six patients. Weighting each sample by 1 over its mouse's samples ranks 8 untuned models at Kendall tau 0.66 per split (lowest -0.07, on 24 test mice) and 0.86 for the ranking by the mean over 30 of the shipped splits, the same best model on 23 of 30, the largest shift of the scan. Open for Lennart as issue 1 of the record's Review; recommended: each mouse counts once (B), unless the use case is a person tested again and again; ROC AUC would first need an optional weight input.

CC (2026-11-08, Lennart): issue 1, B: each mouse counts once, as one patient. The ROC AUC weights a serum sample by 1 over its mouse's number of samples (`mouse_weight`, a scoring column for the metric only); each sample is still read on its own. The weight is for scoring only, never a `sample_weight`, also though it does not follow from the inputs (Lennart's rule of 2026-11-08, MET-15 amended, MET-17); the bundle warning accepted with that reason.

**Assessment (AI, 2026-11-08):** training with the weight does not help: it changes a regularised logistic regression's weighted ROC AUC by -0.015 (SE 0.006, lower on 39 of 60 grouped random splits). New checksum v2:bcf94742... (not built); `dataset check` 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (roc_auc, weighted by mouse_weight) is checked.

## Review

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

## Reference

@article{hingorani2003preinvasive,
  title={Preinvasive and invasive ductal pancreatic cancer and its early detection in the mouse},
  author={Hingorani, Sunil R and Petricoin, Emanuel F and Maitra, Anirban and Rajapakse, Vinodh and King, Catrina and Jacobetz, Michael A and Ross, Sally and Conrads, Thomas P and Veenstra, Timothy D and Hitt, Ben A and others},
  journal={Cancer cell},
  volume={4},
  number={6},
  pages={437--450},
  year={2003},
  publisher={Elsevier}
}
