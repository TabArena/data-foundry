---
unique_name: gallstone_disease
name: Gallstone
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: UCI
year: '2024'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/1150/gallstone-1
- https://doi.org/10.1097/md.0000000000037258
notebook_path: datasets/beyond_iid/new_iid/gallstone_disease/gallstone_disease.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/gallstone_disease/dataset.py
source_row: 768
type_adapter_id: curation-record-v1
---

## Comments

looks good

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag does not hold. The three untuned families differ by 0.036 in skill (+0.683 to +0.719), which the probe compared, unpaired, with twice their typical standard error over 5 splits (0.054). Tuned methods spread clearly: on BeyondArena TabPFN-3.5 reaches ROC AUC 0.911 and the median method 0.883, with 8 of 29 methods tied with the best.

## Reference

@article{esen2024early,
  title={Early prediction of gallstone disease with a machine learning-based method from bioimpedance and laboratory data},
  author={Esen, {\.I}rfan and Arslan, Hilal and Esen, Selin Akt{\"u}rk and G{\"u}l{\c{s}}en, Mervenur and K{\"u}ltekin, Nimet and {\"O}zdemir, O{\u{g}}uzhan},
  journal={Medicine},
  volume={103},
  number={8},
  pages={e37258},
  year={2024},
  publisher={LWW}
}
