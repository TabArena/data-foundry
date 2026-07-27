---
unique_name: yeast
name: yeast
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Data Quality Issue
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/search?type=data&id=181
- https://doi.org/10.24432/C5KG68
source_row: 347
type_adapter_id: curation-record-v1
---

## Comments

CC: "Data already preprocessed (discriminant analysis). This likely introduced data leaks"

CC (2026-07-27, Lennart): **Confirmed leak — stays No.** One feature is *"Score of discriminant analysis
of the amino acid content of vacuolar and extracellular proteins"* — a supervised discriminant analysis
fit on the whole dataset and baked into every row. That transform needs a train/test split to be
leak-free, but the data was already processed once and cannot be recomputed per split, so it
irreversibly leaks the test distribution (`Data Quality Issue`, crit. 4D).
