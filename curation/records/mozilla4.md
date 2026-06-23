---
unique_name: mozilla4
name: mozilla4
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Outdated
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
year: '2006'
source_links:
- https://www.openml.org/d/1046
source_row: 536
type_adapter_id: curation-record-v1
---

# mozilla4

## Comments

CC: "Might be clustered by id. Might need some special preprocessing. Event might leak the state? TabRepo error pretty low - makes a leak more likely. Task has a temporal component, but it seems as if features were designed to be time-invariant. Nevertheless, for each class future time steps cannot appear before later ones - a good task definition requires a custom split; also multiple ID groups where the class depends on a "trigger" to stay the same (i.e. state tracking)"

Seems to be a software code defect prediction akin to pc1 (etc) datasets.
These are very outdated.

Data is also modeled as a survival task. Moreover, features seem to be repeated entries with some conditional logic for the features based on time passing.

Data use case too special, and wrong task (survival), and too old to use for now

## Reference

PROMISE repository web page http://promisedata.org/repository .

https://ieeexplore.ieee.org/document/4273266

Modeling the Effect of Size on Defect Proneness for Open-Source Software
