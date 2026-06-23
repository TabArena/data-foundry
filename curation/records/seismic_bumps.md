---
unique_name: seismic_bumps
name: seismic-bumps
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- Non-IID (Temporal)
collections:
- New
year: '2013'
source_links:
- 10.24432/C5W902
source_row: 48
type_adapter_id: curation-record-v1
---

# seismic-bumps

## Comments

Already in TabArena



CC: ""forecasting seismic bumps in a coal mine from longwalls in a Polish mine; used for clusterting. 

Description highlights practical importance of the taskl. each row contains a summary statement about seismic activity in the rock mass within one shift (8 hours). If decision 
attribute has the value 1, then in the next shift any seismic bump with an energy higher than 10^4 J was 
registered. Hence, the task might be time-invariant.unsure whether the features are extracted from time-series. even if yes, they are extracted from 8h windows and I think this is rather a tabular task. BUT: Temporal correlations need to be investigated. unsure whether the extracted features are time-invariant ""

Temporal features are missing, could this still be used as IID by removing all the time-based features? Or could we find the original time by reverse engineering these features?

Also bascially averages/sums of time series that are the acutal features

8 hours gaps between rows be enough to avoid leakage from temporal components?

I forgot that we had the same discussion and same conclusion last time already, as this is already part of Tabrena haha
Read the paper for details https://www.researchgate.net/publication/281395657_Application_of_rule_induction_algorithms_for_analysis_of_data_collected_by_seismic_hazard_monitoring_systems_in_coal_mines

## Reference

See some of the papers on UCI
