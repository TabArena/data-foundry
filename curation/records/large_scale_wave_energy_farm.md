---
unique_name: large_scale_wave_energy_farm
name: Large-scale Wave Energy Farm
checked_by:
- Andrej
suggestion: TBD -> Yes
tags:
- Larger IID Data
collections:
- TabArena Reject
original_source: UCI
year: '2023'
domain: Other
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5GG7Q
source_row: 598
type_adapter_id: curation-record-v1
---

# Large-scale Wave Energy Farm

## Comments

CC: "The dataset includes 4 CSV files for 49 and 100 wave energy converters based on Perth and Sydney wave scenarios. The main goal is predicting the total power output of the wave farm based on the coordination of WECs (X1, Y1, X2, Y2,..., Xn, Yn). Unclear whether this is a tabular task or time-series and whether it is better to use all data together or as single tasks; used for optimization and not a predictive task for any kind of model (if shall be usable as surrogate)"
It seems as if the samples are configurations, not time stamps. This would make it a tabular task, but it might be tricky to design a good data split, since random splits could lead to less diverse configurations than what would actually be relevant at test time.
Could require domain-specific split or something group-based.

## Reference

Neshat, Mehdi, et al. "Optimisation of large wave farms using a multi-strategy evolutionary framework." Proceedings of the 2020 genetic and evolutionary computation conference. 2020.
