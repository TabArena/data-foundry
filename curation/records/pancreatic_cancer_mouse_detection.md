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

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the 73 mice gave 1 to 6 serum samples each (median 2, 29 one), the label is the mouse's, and the use case reads each sample of an unseen mouse as a new patient's test, so a mouse bled six times counts as six patients. Weighting each sample by 1 over its mouse's samples ranks 8 untuned models at Kendall tau 0.66 per split (lowest -0.07, on 24 test mice) and 0.86 for the ranking by the mean over 30 of the shipped splits, the same best model on 23 of 30, the largest shift of the scan. Open for Lennart as issue 1 of the folder's REVIEW.md; recommended: each mouse counts once (B), unless the use case is a person tested again and again; ROC AUC would first need an optional weight input.

CC (2026-11-08, Lennart): issue 1, B: each mouse counts once, as one patient. The ROC AUC weights a serum sample by 1 over its mouse's number of samples (`mouse_weight`, a scoring column for the metric only); each sample is still read on its own. The weight is for scoring only, never a `sample_weight`, also though it does not follow from the inputs (Lennart's rule of 2026-11-08, MET-15 amended, MET-17); the bundle warning accepted with that reason.

**Assessment (AI, 2026-11-08):** training with the weight does not help: it changes a regularised logistic regression's weighted ROC AUC by -0.015 (SE 0.006, lower on 39 of 60 grouped random splits). New checksum v2:bcf94742... (not built); `dataset check` 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (roc_auc, weighted by mouse_weight) is checked.

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
