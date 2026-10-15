---
unique_name: clock_protein_toxicity
name: Toxicity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
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

CC (2026-10-15, Andrej): I disagree with keeping it. The signal is no bigger than what shuffled labels give.

- **Shuffled labels score as well.** On 10 of the task's 60 splits, untuned models (linear, random forest, LightGBM) score AUC 0.48-0.52. With shuffled labels (20 shuffles, same splits) they average 0.50, ranging 0.40-0.60 (5th-95th percentile), and about half the shuffles beat the true labels. Best model family: p = 0.71.
- **Beating 0.5 on most folds is chance.** On the same splits, shuffled labels beat 0.5 on up to 90% of them (95th percentile), more than the 44 of 60 folds quoted above.
- **Picking the best method inflates the score.** On shuffled labels, the best of only 4 untuned models reaches AUC 0.545 or more on 25% of the shuffles (40 shuffles). The 0.539 above is the best of 29 methods.
- **The authors' feature selection does not carry over.** Their 13-feature subset (`Toxicity-13F.csv`) gives a decision tree 72.9% CV accuracy. The same selection (RFE with a decision tree) redone inside each fold gives 58.8%, below the 67.3% of always predicting non-toxic.

Suggest retiring for no signal. 

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
