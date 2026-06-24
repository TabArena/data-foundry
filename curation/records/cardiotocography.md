---
unique_name: cardiotocography
name: Cardiotocography
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: UCI
year: '2010'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/193/cardiotocography
- https://doi.org/10.24432/C51S4N
source_row: 693
type_adapter_id: curation-record-v1
---

# Cardiotocography

## Comments

The label is the consensus of three experts (so likely noisy).

Can be either 10 or 3 class problem.
Raw data has dates!


From going through the raw data description, it seems one had one or multiple measurements per patient and split it into multiple rows or segments and then created tabular features. Targets can be different per instance. Need to take raw data to get the group IDs.

## Reference

@misc{cardiotocography_193,
  author       = {Campos, D. and Bernardes, J.},
  title        = {{Cardiotocography}},
  year         = {2000},
  howpublished = {UCI Machine Learning Repository},
  note         = {{DOI}: https://doi.org/10.24432/C51S4N}
}
