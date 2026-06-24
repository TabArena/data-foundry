---
unique_name: cylinder_bands
name: cylinder-bands
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Outdated
- No Good Target (yet)
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1995'
domain: industry & manufacturing
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C50C7B
source_row: 559
type_adapter_id: curation-record-v1
---

## Comments

CC: "Process delay data. Might require time splits or even group splits. Unclear what the exact measurements are and how they relate. Most likely this task is not representative anymore. Trees dominate on TabRepo - indicates that something is off. Maybe group leak, i.e. due to job_number? Or feature types may be defined wrongly; also has temporal connections"

Check for group or temporal split

it also seems this was more a data mining than prediction task? No need to generalize to new data!

## Reference

Evans, B., and Fisher, D. (1994). Overcoming process delays with decision tree induction. IEEE Expert, Vol. 9, No. 1, 60--66.
