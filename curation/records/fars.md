---
unique_name: fars
name: fars
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Missing source information
tags:
- 2nd Tier / Scientific Discovery
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/d/40672
- https://github.com/EpistasisLab/pmlb/tree/master/datasets/fars (other link https://data.world/nhtsa/fars-data is dead)
source_row: 460
type_adapter_id: curation-record-v1
---

## Comments

CC: "traffic accident data. Not much information given. Need to validate. likely from here https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars"

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `fars_person_injury_severity` (TBD -> 2nd Tier, priority 3). Each is screened in its own record; this record's verdict stays the curator's.
