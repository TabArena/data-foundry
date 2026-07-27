---
unique_name: arsenic_male_lung
name: arsenic-male-lung
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/d/951
source_row: 398
type_adapter_id: curation-record-v1
---

## Comments

CC: "Regression. Could be combined with arsenic-male-bladder for multi-task/or just event"

CC (2026-07-27, Lennart): **Duplicate of `arsenic_male_bladder`** — this is the lung-cancer-outcome
version of the *same* arsenic-exposure data (bladder cancer is the other outcome). Different versions /
cuts of one underlying dataset count as duplicates, so the `Duplicate` marker is correct (not an orphan)
and it stays **No**. Neither variant is kept — the bladder record is itself `No` (missing source information).
