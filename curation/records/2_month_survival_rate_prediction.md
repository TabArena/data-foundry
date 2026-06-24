---
unique_name: 2_month_survival_rate_prediction
name: 2 Month survival rate prediction
checked_by:
- Lennart
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- New IID
- Multi-target
collections:
- New (BeyondArena)
original_source: Other
year: '1994'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/880/support2
- https://doi.org/10.3886/ICPSR02957.v2
- https://hbiostat.org/data/
- https://hbiostat.org/data/repo/supportdesc
source_row: 687
type_adapter_id: curation-record-v1
---

## Comments

Multi-target task?

Need to filter predictions from features, need to determine best target (binary or regression), need to filter dnr

## Reference

@article{knaus1995support,
  title={The SUPPORT prognostic model: Objective estimates of survival for seriously ill hospitalized adults},
  author={Knaus, William A and Harrell, Frank E and Lynn, Joanne and Goldman, Lee and Phillips, Russell S and Connors, Alfred F and Dawson, Neal V and Fulkerson, William J and Califf, Robert M and Desbiens, Norman and others},
  journal={Annals of internal medicine},
  volume={122},
  number={3},
  pages={191--203},
  year={1995},
  publisher={American College of Physicians}
}
