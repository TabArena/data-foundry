---
unique_name: heart_disease_va_long_beach
name: heart_disease_va_long_beach
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Outdated
- Duplicate
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/heart_disease_cleveland/metadata.yaml
- https://doi.org/10.24432/C52P4X
notebook_path: datasets/beyond_iid/new_iid/heart_disease_va_long_beach/heart_disease_va_long_beach.ipynb
source_row: 759
type_adapter_id: curation-record-v1
---

## Comments

Consists of 4 datasets with similar features and low value counts depending on how it is used. Need to figure out how to use it. Otherwise, nothing speaks against using them in the benchmark

We take all datasets from this repo as they all represent real tasks. We use the binary classification version of the datasets and the processed files.

CC (2026-10-20, Andrej): I disagree with keeping it as a separate task; suggest merging the four hospitals of the study into one dataset (`heart_disease`).
- **Other hospitals predict it better than its own data:** same study (Detrano et al. 1989), features and label as `heart_disease_cleveland` and `heart_disease_hungary`. Trained on VA, TabPFN 3.5 gets AUC 0.708 (LR 0.666); trained only on the other three hospitals, never seeing a VA patient, 0.741. Kept apart, it repeats the Cleveland task with less data.
- **Part of the model separation is which tests were done:** 53 of 200 patients had no exercise test (64% disease vs 78%), and missing-value flags alone give AUC 0.57. With missing values filled at random, TabPFN falls to 0.679 (48/60 folds) and its lead over LR halves (+0.042 to +0.024). Whether a test was done is known before the angiogram, so no leak, but it rewards reading this hospital's practice.
- **6 patients had the angiogram before the exercise test** (7-15 days, one 369 days). Too few to matter.
- **Reference:** Detrano R, Janosi A, Steinbrunn W, Pfisterer M, Schmid JJ, Sandhu S, Guppy KH, Lee S, Froelicher V. International application of a new probability algorithm for the diagnosis of coronary artery disease. Am J Cardiol. 1989;64(5):304-310. doi:10.1016/0002-9149(89)90524-9

CC (2026-10-21, Andrej): Retired as a duplicate of `heart_disease`, which holds this hospital's patients together with the other two of the Detrano study (Switzerland left out) and splits by hospital, as the source applied its model at other hospitals. The folder is removed from the v2 working copy; BeyondArena keeps the dataset as shipped.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Detrano et al. 1989 score reliability (calibration) and percent correctly classified, no threshold or costs for the hard call; percent correctly classified rejected (MET-6, MET-8).

CC (2026-10-21, Lennart): proposal accepted: roc_auc (fallback) for the heart_disease_* datasets, not log_loss.

## Reference

@article{detrano1989international,
  title={International application of a new probability algorithm for the diagnosis of coronary artery disease},
  author={Detrano, Robert and Janosi, Andras and Steinbrunn, Walter and Pfisterer, Matthias and Schmid, Johann-Jakob and Sandhu, Sarbjit and Guppy, Kern H and Lee, Stella and Froelicher, Victor},
  journal={The American journal of cardiology},
  volume={64},
  number={5},
  pages={304--310},
  year={1989},
  publisher={Elsevier}
}
