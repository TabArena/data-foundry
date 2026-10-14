---
unique_name: heart_disease_cleveland
name: heart_disease_cleveland
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
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
v2_path: datasets/_dev/tabarena-v0pt2/heart_disease_cleveland/dataset.py
source_row: 756
type_adapter_id: curation-record-v1
---

## Comments

Consists of 4 datasets with similar features and low value counts depending on how it is used. Need to figure out how to use it. Otherwise, nothing speaks against using them in the benchmark

We take all datasets from this repo as they all represent real tasks. We use the binary classification version of the datasets and the processed files.

CC (2026-10-06, Lennart): Kept after the task-probe review (flag `no_spread`). A real, classic task with clear signal (best ROC AUC 0.913 on BeyondArena) and little room between methods: they spread from 0.913 to about 0.89, 15 of 29 are tied with the best, and the ranks vary across folds more than on any other BeyondArena dataset (Kendall's W 0.15). With 303 patients this is the noise of a small task, not a reason to act.

**Assessment (AI, 2026-10-14):** No leak in `ca` or `thal`: `ca` counts major coronary arteries with calcium on cardiac cinefluoroscopy and `thal` is an exercise thallium scan, noninvasive tests done before the angiography that sets the label (Detrano et al. 1986, Circulation 73:970, PMID 3698241; Detrano et al. 1986, Am J Cardiol 57:1041, PMID 3706156). The data reproduces their sensitivity and specificity (`ca` >= 1: 66.7% / 80.7%).

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
