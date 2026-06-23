---
unique_name: htru2_2
name: HTRU2
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Data Quality Issue
- Wrong Domain / Source Modality
tags:
- Non-IID (Temporal)
- '?'
- New IID
collections:
- TabArena Reject
original_source: UCI
year: '2016'
domain: physics & astronomy
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5DK6R
source_row: 630
type_adapter_id: curation-record-v1
---

# HTRU2

## Comments

CC: "Sounds like a cool application TBH, predict characteristics of a star

Features excluded from time-series. Might be a valid task. Could argue that if we benchmark this dataset, we should also compare against time-series approaches"

Data has no timestamp

Data stream task... (because they dont see the value of refitting in the paper, or cannot refit fast enough)

Paper used random splits. It seems all features are time invariant as well, if not averages over time points of the observed element (?). Unclear what kind of shift they mean in the paper as it does not seem like a shifting task. Could be used as IID

## Reference

@article{lyon2016fifty,
  title={Fifty years of pulsar candidate selection: from simple filters to a new principled real-time classification approach},
  author={Lyon, Robert J and Stappers, Ben W and Cooper, Sally and Brooke, John Martin and Knowles, Joshua D},
  journal={Monthly Notices of the Royal Astronomical Society},
  volume={459},
  number={1},
  pages={1104--1123},
  year={2016},
  publisher={Oxford University Press}
}
