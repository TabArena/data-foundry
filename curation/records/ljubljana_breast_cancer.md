---
unique_name: ljubljana_breast_cancer
name: Ljubljana Breast Cancer \
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Trivial
- Outdated
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/faysalmiah1721758/breast-cancer-data
- https://github.com/jbrownlee/Datasets/blob/master/breast-cancer.names
- https://doi.org/10.24432/C51P4M
- https://www.openml.org/d/13
notebook_path: datasets/beyond_iid/new_iid/ljubljana_breast_cancer/ljubljana_breast_cancer.ipynb
source_row: 769
type_adapter_id: curation-record-v1
---

## Comments

looks good

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Every 1986-1988 paper on the data (Michalski et al., Clark & Niblett, Cestnik et al.) reports accuracy only, without costs or a threshold; 30% recurrence on 286 rows. Original rejected: accuracy. roc_auc is the binary fallback.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `tumor-size`, `inv-nodes`, `deg-malig`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `metabric_breast_cancer_clinical` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 scores are numbers (deg-malig); age, tumour size and nodes are ordered categories of their bands, not the bands' midpoints.

CC (2026-11-10, Andrej): retired (`No (Retired)`, `Trivial`, `Outdated`): an untrained 3-item score does as well as every model, so nothing learnable is left beyond what the field already writes down.
- **The score ties every method:** one point each for malignancy grade 3, more than 2 involved nodes and a tumour through a node's capsule, nothing fitted: ROC AUC 0.710 against 0.717 for TabPFN 3.5 (the score at least as good on 28 of 60 folds), 0.710 for a random forest (29 of 60) and 0.683 for logistic regression (20 x 3 folds, seed 4267).
- **Why the real signal does not keep it:** the outcome is real and well above chance, but the methods learn nothing measurably better than the three standard prognostic factors (grade, nodal status, capsular breach); the 2-node cut-off was set in our review of 2026-10-15 without a recorded source.
- **Outdated:** 1980s clinical bands without the hormone-receptor status prognosis uses today; better data for the task is `metabric_breast_cancer_clinical`.
Markers `Trivial` and `Outdated` added, `v2_path` cleared, folder removed. Evidence: `~/claude_jobs/lbc_review/res.csv`.

## Reference

? UCI
