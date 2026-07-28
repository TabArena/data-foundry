---
unique_name: molecularproperties
name: molecularproperties
checked_by:
- Lennart
data_foundry_status:
- WIP (Triage)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
- Wrong Domain / Source Modality
tags:
- Non-IID (Grouped)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/competitions/champs-scalar-coupling/data?select=train.csv
source_row: 534
type_adapter_id: curation-record-v1
---

## Comments

CC: "Can pre-filter data according to existing molecules, requires expert feature engineering to even find predictive signal from molecular structures but has some un-engineered data we could use/join; target is made up of combination of targets"


Solutions were very custom NN models, not tabular. Might be solvable by tabular, but requires custom preprocessing and is unclear
