---
unique_name: yprop_4_1
name: yprop_4_1
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Data Quality Issue
- Missing source information
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/d/416
source_row: 414
type_adapter_id: curation-record-v1
---

## Comments

CC: "one of 41 drug design datasets. Little information on features given, likely chemical properties. Maybe use only one of those datasets. Most models perform similarly/differences seem random. OpenML version seems not to match paper version and therefore CTR23 excluded these datasets, strange version on OpenML, see CTR23. Might include issues found by previous studies (i.e. leaks, inappropriate data versions) as exclusion criterion"

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `nci_yeast_anticancer_drug_screen` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.
