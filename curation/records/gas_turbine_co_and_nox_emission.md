---
unique_name: gas_turbine_co_and_nox_emission
name: gas_turbine_CO_and_NOx_emission
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
year: '2015'
source_links:
- https://doi.org/10.24432/C5WC95
source_row: 52
type_adapter_id: curation-record-v1
---

# gas_turbine_CO_and_NOx_emission

## Comments

CC: "Related to 10.24432/C5002N 36733; instances of 11 sensor measures aggregated over one hour, from a gas turbine located in Turkey for the purpose of studying flue gas emissions, namely CO and NOx"

Version of the yield forecasting data with timestamp, they did learn with the next paper! haha

Multivariate forecasting task. Not tabular, as tabular model could also just read off the sensor at timepoint t
