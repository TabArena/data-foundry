---
unique_name: forensic_glass_identification
name: glass2
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1987'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/glass2/metadata.yaml
- https://doi.org/10.24432/C5WW2P
notebook_path: datasets/beyond_iid/new_iid/forensic_glass_identification/forensic_glass_identification.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/forensic_glass_identification/dataset.py
source_row: 755
type_adapter_id: curation-record-v1
---

## Comments

PMLB version has less samples and less classes, so likely filtered (?)

Generally a valid potential task, might be outdated but still valid for the task?

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Tableware (class 6) has 9 rows, 3 in every test fold, and class 5 has 13 (4-5). Together they are 10% of the test rows and 14% of a random forest's log loss (0.70 against 1.51 for the class shares). Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — the source defines no metric for the 6-class task; its only result (Spiehler's comparison) counts errors on a different, binary target.

## Reference

UCI
