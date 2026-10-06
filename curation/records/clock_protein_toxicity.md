---
unique_name: clock_protein_toxicity
name: Toxicity
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
- Many features
- Tiny Data
collections:
- FS Benchmark
original_source: UCI
year: '2021'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C59313
- https://www.openml.org/d/46855
notebook_path: datasets/beyond_iid/new_iid/clock_protein_toxicity/clock_protein_toxicity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/clock_protein_toxicity/dataset.py
source_row: 1031
type_adapter_id: curation-record-v1
---

## Comments

Same source as clock_protein_period

The original paper even comes with feature selection. Have to use data.csv file.

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid task after the task-probe review. The probe flagged `no_signal` (untuned LightGBM ROC AUC 0.51; the linear model and random forest below the dummy), but tuned methods find a small, consistent signal: on BeyondArena, LightGBM (default) beats AUC 0.5 on 44 of the 60 folds (mean AUC 0.539), tuned XGBoost on 46; 9 of 29 methods are tied with the best. The probe's best single feature (`MDEC-23`, skill +0.28) was a selection effect: picked on the first split, whose training rows are later splits' test rows; picked on each split's own training side, the best single feature gives AUC 0.51. 56 toxic and 115 non-toxic molecules with 1,117 descriptors: a hard, high-dimensional task, as the FS Benchmark listing intends. A small signal is not a reason to retire.

## Reference

@article{gul2021structure,
  title={Structure-based design and classifications of small molecules regulating the circadian rhythm period},
  author={Gul, Seref and Rahim, Fatih and Isin, Safak and Yilmaz, Fatma and Ozturk, Nuri and Turkay, Metin and Kavakli, Ibrahim Halil},
  journal={Scientific reports},
  volume={11},
  number={1},
  pages={18510},
  year={2021},
  publisher={Nature Publishing Group UK London}
}
