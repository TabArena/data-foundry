---
unique_name: haberman_survival
name: haberman
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'No'
decision_markers:
- Trivial
- Outdated
- Not Representative
tags:
- Tiny Data
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: UCI
year: '1970'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/haberman/metadata.yaml
- https://doi.org/10.24432/C5XK51
source_row: 120
type_adapter_id: curation-record-v1
---

## Comments

Might be a trivial dataset, only really 2 features and a temporal component

But otherwise seems valid enough, we could add it and later remove if needed

CC (2026-07-27, Lennart): Kept **No** / removed. Beyond the tiny size (~306 rows), it no longer
represents a real-world problem and the setup is very simplistic and weird (essentially two features
plus a temporal component) — hence `Trivial` / `Outdated` / `Not Representative`. The "could add it and
later remove" note above is superseded.

## Reference

UCI
