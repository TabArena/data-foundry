---
unique_name: insurance_complaints
name: insurance_complaints
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- Free Text (Short)
- Non-IID (Temporal)
collections:
- TexTabBench Extra
- STRABLE
source_links:
- https://www.kaggle.com/datasets/adelanseur/insurance-company-complaints
- https://data.ct.gov/Business/Insurance-Company-Complaints-Resolutions-Status-an/t64r-mt64
source_row: 503
type_adapter_id: curation-record-v1
---

## Comments

Insurance claims data from website, mostly just reports without clear target and ground truth. Needs some thought if it could be made a real task

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `texas_tdi_insurance_complaints` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.
