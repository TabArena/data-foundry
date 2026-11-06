---
unique_name: clock_protein_toxicity
name: Toxicity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- No Signal
tags:
- New IID
- Many features
- Tiny Data
- Timeless
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

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the 11 descriptors that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: the 11 descriptors holding only 0 and 1 (E-state and atom counts such as nsBr, khs.dS, LipinskiFailures) stay numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Gul et al. 2021 compare classifiers by 10-fold CV accuracy only (Table 2), without a threshold or costs, on 171 molecules (33% toxic). Original rejected: accuracy (MET-6, coarse on 171 rows). roc_auc is the binary fallback.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the folder's `REVIEW.md` (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends not to ship it. Priority 1: gap -, use case - (our use case), source + (Gul et al. 2021), shape -, risk - (no signal beyond shuffled labels; recommended not to ship).
**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): nAcid and nBase, both -1 in the same 2 molecules (no count), set to missing (CLEAN-10, CLEAN-11)..

CC (2026-11-01, Lennart): marks on the review board of PR #37: the two molecules the descriptor software failed on are dropped (-1 counts, 62-68 descriptors at 0 that the other molecules have, no structures to recompute them); an exception to CLEAN-11.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ncats_cytotoxicity_profiling` (TBD -> Yes, priority 4). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Retire: none of the 40 benchmark methods beats shuffled labels (best ROC AUC 0.539); a label-free typicality score beats them (0.630, p = 0.003) but was found by a search on the same 169 molecules. Priority 1: gap 0, use case 0, source 1, shape 0, risk -1.

CC (2026-11-05, Andrej): retired (`No (Retired)`, `No Signal`): no benchmark method finds more signal than randomly shuffled labels give. The data: 169 small molecules designed to bind CRY1, a protein of the circadian clock (Gul et al. 2021, UCI), 1,117 descriptors computed from each structure, and whether the molecule kills cells in a viability test (55 toxic).
- **The methods score at the level of random labels:** the 40 benchmark methods reach ROC AUC 0.445 to 0.539 (TabPFN-3.5 0.524). With the toxic and non-toxic tags dealt out at random on the same splits, untuned models reach 0.40 to 0.60 and about half the shuffles beat the true labels (best family, p = 0.71); the best of only four models reaches 0.545 or more on a quarter of the shuffles.
- **The paper's accuracy came from a feature selection on all rows:** its 13 chosen descriptors give a decision tree 72.9% accuracy, but chosen again inside each fold 58.8%, below the 67.3% of always predicting non-toxic.
- **The one weak signal found does not rescue it:** a label-free "typicality" score (molecules near the middle of the descriptor space called toxic) reaches 0.630 on the v0.2 splits (p = 0.003), but it was picked after about 137 screens of the same 169 molecules, and none of the benchmark methods finds it.
- **Why Lennart's keep of 2026-10-06 does not hold:** it rested on tuned methods beating 0.5 on most folds (LightGBM on 44 of 60), which shuffled labels do as well.
Marker `No Signal`, new for tasks whose methods stay within what shuffled labels give on the split the use case needs. Better data for the task, `ncats_cytotoxicity_profiling`, is screened in its own record.

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
