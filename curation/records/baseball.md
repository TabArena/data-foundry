---
unique_name: baseball
name: baseball
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Missing source information
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/d/185
source_row: 590
type_adapter_id: curation-record-v1
---

## Comments

CC: "Baseball player statistics with hall of fame as nominal target, very imbalanced! Also potential omitted variable bias as date information could also be relevant, also task might be trivial or better modeled by deterministic rules; unclear source data"

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `lahman_hall_of_fame` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.
