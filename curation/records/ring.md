---
unique_name: ring
name: ring
suggestion: 'No'
decision_markers:
- Duplicate
original_source: Github
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/ring/metadata.yaml
type_adapter_id: curation-record-v1
---

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: None-Source.

missing source information, not found any detaisl,extrem imbalance, look syntethic from the data distributions (maybe generated via sklearn)

Lennart: missing source information

Andrej: Missing source information

CC (2026-10-31, Lennart): ring is a duplicate of `ringnorm` (Breiman's ringnorm, DELVE): all 7,400 feature rows of the PMLB file match OpenML 1496 exactly, the labels recoded from 1/2 to 0/1 with the same class counts (3,736 / 3,664). The classes are balanced, so the earlier "extreme imbalance" note does not hold; the source is ringnorm's, so `Missing source information` gives way to `Duplicate`. Found by the better-data scouting run of 2026-10-30 and checked by row comparison.
