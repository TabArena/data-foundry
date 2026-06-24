---
unique_name: hayes_roth
name: hayes_roth
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Outdated
- Trivial
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- Tiny Data
collections:
- TabArena Reject
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/hayes_roth/metadata.yaml
- https://doi.org/10.24432/C5501T
source_row: 97
type_adapter_id: curation-record-v1
---

## Comments

Seems to have a lot of details regarding the data state and how it was created and how categories were assigned

Deterministic rules for the class:

     -- only attributes C-E are diagnostic; values for A and B are ignored
     -- Class Neither: if a 4 occurs for any attribute C-E
     -- Class 1: Otherwise, if (# of 1's)>(# of 2's) for attributes C-E
     -- Class 2: Otherwise, if (# of 2's)>(# of 1's) for attributes C-E
     -- Either 1 or 2: Otherwise, if (# of 2's)=(# of 1's) for attributes C-E
