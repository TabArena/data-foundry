---
unique_name: wine_recognition
name: wine_recognition
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Outdated
- Data Quality Issue
- Trivial
tags:
- Tiny Data
collections:
- TabArena Reject
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/wine_recognition/metadata.yaml
- https://doi.org/10.24432/C5PC7J
source_row: 66
type_adapter_id: curation-record-v1
---

## Comments

No information at all from PMLB. Likely not a real task and thus hard to say if we care about it

Found on UCI. It already has some features missing. It is a wine origin prediction from the 90s. Likely trivial as RF can perfectly solve it according to UCI.

Given all of this, I would veto to skip it, also due to its age
