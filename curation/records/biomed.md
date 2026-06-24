---
unique_name: biomed
name: biomed
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Too Small
- Trivial
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/biomed/metadata.yaml
- https://lib.stat.cmu.edu/datasets/biomed.desc
- https://www.openml.org/search?type=data&status=active&id=481&sort=runs
source_row: 566
type_adapter_id: curation-record-v1
---

## Comments

The data contains only 7 observations (patients), and the rest is grouped per patient. It is a very weird use case as it was used for visualization rather than a predictive task.

This might be usable in some way, but it is super unclear how it should be used. We keep it as TBD for now
