---
unique_name: ljubljana_primary_tumor
name: Ljubljana Primary Tumor
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
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5WK5Q
notebook_path: datasets/beyond_iid/new_iid/ljubljana_primary_tumor/ljubljana_primary_tumor.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/ljubljana_primary_tumor/dataset.py
source_row: 770
type_adapter_id: curation-record-v1
---

## Comments

Need to resolve ordinal encoding, otherwise looks good!

Has a lot of classes, need to see there are enough labels per class or if I need to group some cases / remove some samples

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Prostate has 10 rows (3-4 per test fold), colon and thyroid 14 each (4-5). Together they are 13% of the test rows and 22% of a random forest's log loss (1.43 against 2.20 for the class shares). The definition already drops the classes with fewer than 10 rows. Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The 1986-1987 papers report accuracy only; we drop the classes with fewer than 10 rows (MET-2). Original rejected: accuracy. log_loss is the multiclass fallback.

**Assessment (AI, 2026-10-27):** evidence for the Selection Bias marker of PR #16, checked on primary-tumor.data: all 20 head and neck patients have neck nodes and 21 of the 24 breast patients have armpit nodes (8% and 4% of the other patients). The rows are patients whose primary was found, with the spread typical of it, not the patients with metastases of unknown origin the use case is about. The definition's fit_reason does not name this yet.

CC (2026-10-27, Lennart): fit approximate (was direct): patients with metastases of unknown origin do not show the selection of these rows, so it is a known gap (USE-8, amended on the review of PR #16); the Selection Bias marker stays.

## Reference

UCI
