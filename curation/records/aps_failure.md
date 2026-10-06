---
unique_name: aps_failure
name: APSFailure
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2016'
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=41138
- https://doi.org/10.24432/C5V60Q
notebook_path: datasets/beyond_iid/old_iid/aps_failure/aps_failure.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/aps_failure/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Comes with a cost matrix. Originally comes with custom train/test split. Last 16k are test. Strongly imbalanced task. Might originally be time-series. Error very close to zero on TabRepo - might indicate a leak; data from daily usage indicates temporal relationship as well and potentailly future failures per seasons; data contains histograms; missing values must be nan-ed

Update: Error is close to zero because it is trivial to classify the negative cases due to the high class imbalance. However meaningful learning is possible. One paper about challenge: https://link.springer.com/chapter/10.1007/978-3-319-46349-0_33. D

Potential issue: maybe temporal, heavily preprocssed

Lennart: verify split

Andrej: need to verify that original provided split was also random

CC (2026-10-06, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `one_feature`: `ck_000` alone +0.944 skill against +0.982 for LightGBM). Not trivial: the best single feature chosen on each split's training side (`ci_000` or `aa_000`) ranks the test rows at ROC AUC 0.970, below all 20 BeyondArena configurations (TabPFN-3 0.994 to a default linear model 0.988) on every fold; the methods cut the remaining error (1 - AUC) from 0.031 to 0.006. The flag comes from AUC near its ceiling, where the methods differ in the third decimal; the original challenge scored a cost (500 per missed failure, 10 per false alarm). Still open from the earlier triage: the source ships a train/test split (the last 16,000 readings) that may be temporal; there are no timestamps to check it, so the random folds stay.

## Reference

10.24432/C5V60Q
