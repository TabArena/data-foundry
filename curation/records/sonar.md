---
unique_name: sonar
name: sonar
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- Outdated
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Time-series (Classification)
tags:
- Tiny Data
collections:
- TabArena Reject
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/sonar/metadata.yaml
- 10.24432/C5T01Q
source_row: 71
type_adapter_id: curation-record-v1
---

# sonar

## Comments

The data comes from an old experiment where the feature describes a sound and the label describes the origin of the sound. This is clearly outdated and would be solved with time-series models today. Give this, I vote to exclude it and hope for real, new small data that is not from time-series data

The data is also basically a simulation/handcrafted set for this toy example and not something one would deploy in reality (also likely more for scientific discovery)
