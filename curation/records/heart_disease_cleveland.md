---
unique_name: heart_disease_cleveland
name: heart_disease_cleveland
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
notebook_path: datasets/beyond_iid/new_iid/heart_disease_cleveland/heart_disease_cleveland.ipynb
source_row: 756
type_adapter_id: curation-record-v1
---

## Comments

Consists of 4 datasets with similar features and low value counts depending on how it is used. Need to figure out how to use it. Otherwise, nothing speaks against using them in the benchmark

We take all datasets from this repo as they all represent real tasks. We use the binary classification version of the datasets and the processed files.

CC (2026-10-06, Lennart): Kept after the task-probe review (flag `no_spread`). A real, classic task with clear signal (best ROC AUC 0.913 on BeyondArena) and little room between methods: they spread from 0.913 to about 0.89, 15 of 29 are tied with the best, and the ranks vary across folds more than on any other BeyondArena dataset (Kendall's W 0.15). With 303 patients this is the noise of a small task, not a reason to act.

**Assessment (AI, 2026-10-14):** No leak in `ca` or `thal`: `ca` counts major coronary arteries with calcium on cardiac cinefluoroscopy and `thal` is an exercise thallium scan, noninvasive tests done before the angiography that sets the label (Detrano et al. 1986, Circulation 73:970, PMID 3698241; Detrano et al. 1986, Am J Cardiol 57:1041, PMID 3706156). The data reproduces their sensitivity and specificity (`ca` >= 1: 66.7% / 80.7%).

CC (2026-10-20, Andrej): I disagree with keeping it as a separate task; suggest merging the four hospitals of the study into one dataset (`heart_disease`).
- **One study, three tasks:** Cleveland, Hungary and VA Long Beach (and Switzerland, not shipped) come from one study (Detrano et al. 1989) with the same 13 features and label (angiography, an X-ray of the coronary arteries, shows >50% narrowing). A model trained only on the other three hospitals gets AUC 0.886 here, against 0.913 trained on Cleveland, and adding them to training changes nothing (+0.002). Kept apart, the benchmark counts one task three times.
- **Little room between methods:** an untrained count of 6 textbook findings gets AUC 0.907, LR 0.907, TabPFN 3.5 0.913 (+0.006, wins 49/60 folds); on BeyondArena 15 of 29 configurations tie with the best. Not trivial, the methods do spread, but alone this task barely ranks them.
- **Statlog Heart is an exact subset** (270 rows, same labels). No problem for this record, but `heart_statlog` must stay out.
- **Merged version** (920 patients, hospital column, random split stratified by hospital and label): TabPFN 0.913 vs LR 0.906 (wins 56/60). The hospital alone gives AUC 0.72 through its disease rate (36-94%); with the column every model gets it equally.
- **Reference:** Detrano R, Janosi A, Steinbrunn W, Pfisterer M, Schmid JJ, Sandhu S, Guppy KH, Lee S, Froelicher V. International application of a new probability algorithm for the diagnosis of coronary artery disease. Am J Cardiol. 1989;64(5):304-310. doi:10.1016/0002-9149(89)90524-9

CC (2026-10-21, Andrej): Retired as a duplicate of `heart_disease`, which holds this hospital's patients together with the other two of the Detrano study (Switzerland left out) and splits by hospital, as the source applied its model at other hospitals. The folder is removed from the v2 working copy; BeyondArena keeps the dataset as shipped.

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
