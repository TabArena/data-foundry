---
unique_name: heart_disease_hungary
name: heart_disease_hungary
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
notebook_path: datasets/beyond_iid/new_iid/heart_disease_hungary/heart_disease_hungary.ipynb
source_row: 757
type_adapter_id: curation-record-v1
---

## Comments

Consists of 4 datasets with similar features and low value counts depending on how it is used. Need to figure out how to use it. Otherwise, nothing speaks against using them in the benchmark

We take all datasets from this repo as they all represent real tasks. We use the binary classification version of the datasets and the processed files.

CC (2026-10-20, Andrej): I disagree with keeping it as a separate task; suggest merging the four hospitals of the study into one dataset (`heart_disease`).
- **One study, three tasks:** same study (Detrano et al. 1989), features and label as `heart_disease_cleveland` and `heart_disease_va_long_beach`. A model trained only on the other three hospitals gets AUC 0.902 here (TabPFN 3.5), against 0.914 trained on Hungary; training on all hospitals adds +0.004. Kept apart, the benchmark counts one task three times.
- **A simple rule comes close:** an untrained count of 4 findings (chest pain without anginal symptoms, chest pain on exercise, ST depression > 0, an exercise-ECG sign of reduced blood flow, and male) gets AUC 0.887; LR 0.908, TabPFN 0.914 (wins 43/59 folds). Not trivial, but little room.
- **Two tests are hardly recorded:** `ca` (calcium seen on fluoroscopy) is 99% missing and `thal` (thallium scan, an image of the heart's blood flow) 90%. Both still add 0.015 AUC. `slope` is missing exactly when there is no ST depression (188 of 190), so its gaps restate a finding rather than how data was collected.
- **Undocumented selection:** the study had 425 Hungarian patients, UCI has 294, and how they were chosen is not stated. The disease rate is similar (36% vs 38%), so not severe.
- **Doc errors (fix in the merged dataset):** the README says "we merge grades", but the file is already 0/1; the raw dates show 1983-87, not "period not stated"; the record's source link points to PMLB's Cleveland page.
- **Reference:** Detrano R, Janosi A, Steinbrunn W, Pfisterer M, Schmid JJ, Sandhu S, Guppy KH, Lee S, Froelicher V. International application of a new probability algorithm for the diagnosis of coronary artery disease. Am J Cardiol. 1989;64(5):304-310. doi:10.1016/0002-9149(89)90524-9

CC (2026-10-21, Andrej): Retired as a duplicate of `heart_disease`, which holds this hospital's patients together with the other two of the Detrano study (Switzerland left out) and splits by hospital, as the source applied its model at other hospitals. The folder is removed from the v2 working copy; BeyondArena keeps the dataset as shipped.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Detrano et al. 1989 score reliability (calibration) and percent correctly classified, no threshold or costs for the hard call; percent correctly classified rejected (MET-6, MET-8).

CC (2026-10-21, Lennart): proposal accepted: roc_auc (fallback) for the heart_disease_* datasets, not log_loss.

CC (2026-10-27, Lennart): retirement confirmed in the review of PR #20: the hospital's patients are part of `heart_disease`, split by hospital.

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
