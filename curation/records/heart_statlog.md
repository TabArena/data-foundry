---
unique_name: heart_statlog
name: heart_statlog
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Duplicate
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
type_adapter_id: curation-record-v1
---

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

Lennart: Sample size

Andrej: Sample size

CC (2026-10-21, Andrej): Duplicate of the Cleveland data: all 270 rows are rows of UCI's `processed.cleveland.data` (270 of its 297 complete rows), each with the same label (Statlog codes 1 = absent, 2 = present). The Cleveland patients are in `heart_disease` (the Detrano study's three hospitals, split by hospital), which retired `heart_disease_cleveland` on 2026-10-21.
