---
unique_name: parkinsons_biomedical_voice_measurements
name: Parkinsons
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
tags:
- Tiny Data
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: UCI
year: '2007'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C59C74
source_row: 791
type_adapter_id: curation-record-v1
---

# Parkinsons

## Comments

Voice recordings turned tabular (unclear if real task otherwise). grouped data / 6 recordings per patient. Only 23 real samples, so tiny grouped data, likely not tabular 

Figure out how to split and use

Data contains two datasets!

## Reference

If you use this dataset, please cite the following paper: 
'Exploiting Nonlinear Recurrence and Fractal Scaling Properties for Voice Disorder Detection', 
Little MA, McSharry PE, Roberts SJ, Costello DAE, Moroz IM. 
BioMedical Engineering OnLine 2007, 6:23 (26 June 2007)
