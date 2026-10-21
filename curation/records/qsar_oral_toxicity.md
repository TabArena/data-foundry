---
unique_name: qsar_oral_toxicity
name: QSAR oral toxicity
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- New IID
- Many features
collections:
- New (BeyondArena)
original_source: Other
year: '2019'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/508/qsar+oral+toxicity
- https://doi.org/10.24432/C5PS4J
- http://www.michem.unimib.it/download/data/
notebook_path: datasets/_dev/feature_selection/qsar_oral_toxicity/qsar_oral_toxicity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_oral_toxicity/dataset.py
source_row: 685
type_adapter_id: curation-record-v1
---

## Comments

Rel: https://www.centro3r.it/sites/default/files/Ballabio_et_al-2019-Molecular_Informatics.pdf

Looks like a good QSAR dataset and a valid task

**Assessment (AI, 2026-10-07):** UCI 508 is the very toxic endpoint (LD50 < 50 mg/kg) of the calibration set of the ICCVAM/NICEATM acute oral toxicity project behind CATMoS (NTP trainingset_171130.txt has the same 741 / 8,251 class counts), with Dragon ECFP bits from Ballabio et al. 2019. The file stores the authors' 6,744 training rows, then their 2,248 test rows (Table 1). The bits come from the QSAR-ready parent structure, so salt forms share a vector: the v2 definition drops 477 exact copies and 22 rows of 11 vectors with both classes (8,493 left). IID, as in both source splits; random forest AUC 0.88, no probe flags. Fingerprints are in scope as for qsar_tid_11.

**Assessment (AI, 2026-10-20):** priority 4 for the review of the added dataset: gap -, use case +, source +, shape +, no known risk. Well-documented regulatory toxicity task with 1,024 fingerprint bits; issues closed in verification, only an optional extension stays open.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes, no exclusion and no re-split. Applied: the target reads 50 mg/kg or less, the top hazard category (the 2026-10-07 line's "LD50 < 50" is the same correction; 25% of labels come from category data without a point LD50); nine parents that survived the deduplication twice lose their second row through the order linkage to the project's structure file, so 8,484 chemicals remain; the false reason for IID-only (no structure in the file) is replaced by the use case and the structure-blind source protocols; the duplicate counts, the Dragon 7 citation and the fingerprint variant are corrected; the note carries the cluster cost (random forest 0.882 to 0.842 by Butina clusters, 0.887 to 0.843 by scaffolds, ranking unchanged). Open for the curator: the fit label (the prediction set is farther from training than the test rows, 9.3% against 19.7% close analogs; the panel recommends approximate), a scaffold-grouped variant, and the extension with the evaluation set. Priority 4: gap - (no thin domain, problem type or regime), use case + (CATMoS names the screener and the decision), source + (UCI, two papers, the project's own files), shape + (8,484 rows, 1,024 features), risk none (the open items are a label and a variant, not a leak or an unclear target).

CC (2026-10-21, Lennart): 0/1 presence flags are categorical ("Assuming it is binary, the categorical dtype might be best?"); CLEAN-14 amended. The bits were checked to hold only 0 and 1.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Ballabio et al. 2019 report the non-error rate with sensitivity and specificity, the group's house measure, without costs; 25% very toxic. Original rejected: NER. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): keep the scaffold-grouped variant a listed candidate (SPLIT-31), no re-split; IID stays.

CC (2026-10-21, Lennart): fit `approximate`: "this is a more simulated use case than a direct real case". The fit_reason names the gap: the random test chemicals are closer to training than the untested chemicals a screener faces (19.7% against 9.3% with a close analog at Tanimoto 0.7 or more).

CC (2026-10-21, Lennart): Extend with the package's validation set and use the further feature data, preprocessing the SMILES as for the other SMILES datasets.

**Assessment (AI, 2026-10-21):** Extended and re-featured. The definition now reads the authors' package (vt_data.mat, a copy the curator provided; public route: the group's download form, freeware with the paper cited) instead of the UCI file, which equals its ECFP_1024_02 training and test blocks row by row (8,992 of 8,992, classes too). With the project's evaluation set the source has 11,886 chemicals (984 very toxic); after the same deduplication (732 exact copies, 20 both-class vectors over 52 rows, 9 parents kept twice by InChIKey) 11,105 remain, 931 very toxic (8.4%), up from 8,484 and 708. `_prepare_raw_files` decodes the MATLAB string objects of the package, so the build reproduces from the original file; the decoded rows were checked against the project's public structure files (evaluation set by RowID on all 2,894 rows, calibration by CASRN or InChIKey, 100% class agreement) and the SMILES reproduces its row's InChIKey for 99.8% of rows. Features: the 1,024 bits plus 207 RDKit 2D descriptors of the QSAR-ready SMILES, which decide (default LightGBM over the 9 shipped splits: 0.885 bits only, 0.901 with the descriptors, better on 9 of 9; random forest 0.901 to 0.912); the SMILES is dropped as in every SMILES dataset, `rdkit_Ipc` with it (it overflows float32; open for the curator). Metric unchanged (roc_auc fallback; 8.4% very toxic). Fit stays approximate with re-measured numbers (close analogs 24.5% of test rows against 11.0% of the project's untested prediction set; random forest 0.715 for distant chemicals against 0.945 for close ones), and the scaffold-grouped cost is now 0.900 to 0.852.

CC (2026-10-21, Lennart): `rdkit_Ipc`: fix it by scaling rather than dropping it. Accept the `dataset_pure_feature_value` warning (rdkit_fr_Ar_COO) with its reason. `original_source`: take the definition's value (Other).

**Assessment (AI, 2026-10-21):** Applied. `rdkit_descriptors` (data_foundry.v2.chemistry) now ships Ipc as `rdkit_Ipc_log10` = log10(1 + Ipc) for every SMILES dataset, so the definition keeps it (208 descriptors; maximum 166.8 here instead of 6e166). apistox and qsar_bioconcentration change with it: apistox's Ipc reached 2.6e38, just below the float32 limit, now 38.4; qsar_bioconcentration's 7.7e9, now 9.9. The warning is accepted in `accepted_check_warnings`; `original_source` is Other. dataset check: 0 errors, 0 warnings on all three. Not rebuilt.

## Reference

@article{ballabio2019integrated,
  title={Integrated QSAR models to predict acute oral systemic toxicity},
  author={Ballabio, Davide and Grisoni, Francesca and Consonni, Viviana and Todeschini, Roberto},
  journal={Molecular informatics},
  volume={38},
  number={8-9},
  pages={1800124},
  year={2019},
  publisher={Wiley Online Library}
}
