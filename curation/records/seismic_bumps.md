---
unique_name: seismic_bumps
name: seismic-bumps
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
original_source: UCI
year: '2013'
required_split:
- Temporal (NON-IID)
source_links:
- https://doi.org/10.24432/C5W902
type_adapter_id: curation-record-v1
---

# seismic-bumps

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Temporal Tabular.

forecasting seismic bumps in a coal mine from longwalls in a Polish mine; used for clusterting. 

Description highlights practical importance of the taskl. each row contains a summary statement about seismic activity in the rock mass within one shift (8 hours). If decision 
attribute has the value 1, then in the next shift any seismic bump with an energy higher than 10^4 J was 
registered. Hence, the task might be time-invariant.

Potential issue: Temporal

Lennart: temporal data

Andrej: unsure whether the features are extracted from time-series. even if yes, they are extracted from 8h windows and I think this is rather a tabular task. BUT: Temporal correlations need to be investigated. unsure whether the extracted features are time-invariant

## Reference

See some of the papers on UCI
