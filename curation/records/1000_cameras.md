---
unique_name: 1000_cameras
name: 1000-cameras
checked_by:
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- Non-IID (Temporal)
- 2nd Tier / Scientific Discovery
collections:
- TabArena Reject
source_links:
- https://www.openml.org/d/43714
- https://perso.telecom-paristech.fr/eagan/class/igr204/datasets and https://www.kaggle.com/datasets/crawford/1000-cameras-dataset
source_row: 551
type_adapter_id: curation-record-v1
---

## Comments

CC: "Probably not a predictive task, but if yes, then with temporal split"

Does not seem like a good task. No proper target can be found that would be usable in the real world. Price prediction on past trends would not help that much; also the price is not corrected for time — most likely it could be a year task of predicting the next year's prices. But it is also a bit boring then.

TBD... could be seen as good enough

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `dpreview_camera_specifications_price` (TBD -> 2nd Tier, priority 1). Each is screened in its own record; this record's verdict stays the curator's.
