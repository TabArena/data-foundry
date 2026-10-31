---
unique_name: gallstone_disease
name: Gallstone
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: UCI
year: '2025'
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

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Esen et al. 2024 report accuracy, precision, recall, F-measure and AUC side by side, none named as the criterion (MET-5).

CC (2026-10-27, Lennart): keep it as Andrej marked it: the Selection Bias marker and fit direct (USE-8, amended on the review of PR #16); how the patients were chosen is not stated.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `Hepatic Fat Accumulation (HFA)`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3); Comorbidity's three undocumented 2 and 3 (each with one listed disease) recoded to 1, the rows kept (CLEAN-11); the fat-accumulation grade an ordered category.

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
