---
unique_name: telemonitoring_parkinsons_biomedical_voice_measurements
name: Parkinsons
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: TBD -> Yes
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
tags:
- Tiny Data
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: UCI
year: '2009'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C59C74
source_row: 638
type_adapter_id: curation-record-v1
---

# Parkinsons

## Comments

Same source as Parkinsons and saved in the same repo under telemonitoring/, but here we only have data from cases that already have Parkinson's. The task is to predict the progression of a patient at the next time interval (so non-iid grouped), that is we have a different target per time point per patient. 

It was used to monitor the progression. 

Moreover, it was technically a correlation analysis / for scientific discovery. We keep it as we can clearly frame this as a task for predicting future UPDRS scores

AT: It seems as if repeated observations per time stamp are present. We might need to groupby and summarize them, because the target is unique. That way we would end up with just 124 samples -> real problem but solve in the future?

## Reference

If you use this dataset, please cite the following paper:
A Tsanas, MA Little, PE McSharry, LO Ramig (2009)
'Accurate telemonitoring of Parkinson.s disease progression by non-invasive 
speech tests',
IEEE Transactions on Biomedical Engineering (to appear).
