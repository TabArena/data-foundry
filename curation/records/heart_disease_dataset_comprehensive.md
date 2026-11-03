---
unique_name: heart_disease_dataset_comprehensive
name: Heart-Disease-Dataset-(Comprehensive)
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/d/43672
source_row: 377
type_adapter_id: curation-record-v1
---

## Comments

CC: "Duplicate containing many of the other heart disease datasets (cleveland, hungarian, ....) "

**Assessment (AI, 2026-10-27):** a duplicate of `heart_disease`, which since PR #20 holds the Cleveland, Budapest and Long Beach files of the Detrano study in one dataset (the single-hospital datasets are retired into it).
