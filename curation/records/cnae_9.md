---
unique_name: cnae_9
name: cnae-9
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- NLP (Text)
- Wrong Domain / Source Modality
- Outdated
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/d/1468
- https://doi.org/10.24432/C51G7P
source_row: 357
type_adapter_id: curation-record-v1
---

# cnae-9

## Comments

CC: "1080 documents of free text business descriptions of Brazilian companies categorized into a subset of 9 categories; which got one-hot encoded?"

Could be a valid text-as-tabular task. But the preprocessing is outdated and not changeable anymore. Moreover, in the end we go just from text to prediction, so it is pure NLP!
