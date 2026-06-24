---
unique_name: musk
name: musk
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Disagreement
tags:
- Tiny Data
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: UCI
year: '1994'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/75/musk+version+2
- https://www.openml.org/search?type=data&sort=runs&id=1116&status=active
- https://doi.org/10.24432/C51608
- https://doi.org/10.24432/C5ZK5B
source_row: 5
type_adapter_id: curation-record-v1
---

# musk

## Comments

CC: "multiple instance problem - multiple instances of the same molecule are in the data. The classifier should classify as 1 if any of the instances is 1 (0 if none). Leak if used with random splits. Classic Physics/Chemistry application, definitely worth including. Not in TabRepo, but likely due to leak; Could be used after preprocessing to reduce to the original (very small) dataset of 102 molecules. When done, the dataset is however too small for our selection size"

We use musk version 2 as a starting point and treat it as a grouped prediction task

AT: No disagreement, but we should discuss how to treat the multi-instance problem

## Reference

10.24432/C51608
