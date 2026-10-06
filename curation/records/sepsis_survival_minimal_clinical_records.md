---
unique_name: sepsis_survival_minimal_clinical_records
name: Sepsis Survival Minimal Clinical Records
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
- Tiny Data
collections:
- New (BeyondArena)
original_source: UCI
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/827/sepsis+survival+minimal+clinical+records
- https://doi.org/10.24432/C53C8N
notebook_path: datasets/beyond_iid/new_iid/sepsis_survival_minimal_clinical_records/sepsis_survival_minimal_clinical_records.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sepsis_survival_minimal_clinical_records/dataset.py
source_row: 662
type_adapter_id: curation-record-v1
---

## Comments

CC: "It has three features, which sound hard to be fully meaningful. But it is a real task"

3 Features, unsure how trivial the dataset is

The dataset is full of "real" duplicates and is technically just a small or tiny dataset. We keep it as is to see how methods can handle it, but this is not really large data...

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid task by design after the task-probe review (flag `one_feature`). The 110,204 admissions hold only 975 distinct feature rows (age, sex, episode number; 7.4% died): the duplicates are real patients, and predicting survival from these three fields alone is the source paper's question. Age carries most of the signal but not all of it: age alone, chosen on each split's training side, gives ROC AUC 0.704, above only 6 of 28 BeyondArena configurations and below the best on all 9 folds; the best methods (TabPFN-3, tuned LightGBM, RealMLP) reach 0.707, a default random forest 0.689, and a lookup of each cell's death rate on the training side 0.689. So `Trivial` does not hold: sex and episode number add a small, consistent gain, and the methods gain by smoothing over age.

## Reference

@article{chicco2020survival,
  title={Survival prediction of patients with sepsis from age, sex, and septic episode number alone},
  author={Chicco, Davide and Jurman, Giuseppe},
  journal={Scientific reports},
  volume={10},
  number={1},
  pages={17156},
  year={2020},
  publisher={Nature Publishing Group UK London}
}
