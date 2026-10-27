---
unique_name: heart_disease_switzerland
name: heart_disease_switzerland
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'No'
decision_markers:
- Outdated
- Too Small
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
notebook_path: datasets/_dev/feature_selection/heart_disease_switzerland/heart_disease_switzerland.ipynb
source_row: 758
type_adapter_id: curation-record-v1
---

## Comments

Consists of 4 datasets with similar features and low value counts depending on how it is used. Need to figure out how to use it. Otherwise, nothing speaks against using them in the benchmark

We take all datasets from this repo as they all represent real tasks. We use the binary classification version of the datasets and the processed files.

Too few samples, is few-shot

**Assessment (AI, 2026-10-27):** `Trivial` removed and the year set to 1988, the year of the UCI donation its siblings carry, on Lennart's ask to resolve the side findings of PR #20. TP-4 test on the 123 patients of `processed.switzerland.data` (115 diseased, 8 without; 3 folds x 20 repeats, stratified): the best single feature chosen on each split's training side (chest-pain type in 45 of 60 folds) reaches ROC AUC 0.677 against 0.705 for logistic regression and 0.708 for a random forest, and matches both on 22 of 60 folds, so no feature or rule solves the task. With 2 or 3 patients without disease per test fold the file stays `Too Small` (TP-5); the verdict `No` is unchanged. Its patients are left out of `heart_disease` (the release kept 8 of the paper's 23 without disease).

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
