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
year: '2022'
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

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the 11 descriptors that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: the 11 descriptors holding only 0 and 1 (E-state and atom counts such as nsBr, khs.dS, LipinskiFailures) stay numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Gul et al. 2021 compare classifiers by 10-fold CV accuracy only (Table 2), without a threshold or costs, on 171 molecules (33% toxic). Original rejected: accuracy (MET-6, coarse on 171 rows). roc_auc is the binary fallback.

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
