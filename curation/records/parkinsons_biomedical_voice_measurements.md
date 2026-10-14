---
unique_name: parkinsons_biomedical_voice_measurements
name: Parkinsons
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
- Too Small
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
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C59C74
notebook_path: datasets/beyond_iid/grouped/parkinsons_biomedical_voice_measurements/parkinsons_biomedical_voice_measurements.ipynb
source_row: 791
type_adapter_id: curation-record-v1
---

## Comments

Voice recordings turned tabular (unclear if real task otherwise). Grouped data / 6 recordings per patient. Only 23 real samples, so tiny grouped data, likely not tabular

Figure out how to split and use

Data contains two datasets!

CC (2026-10-05, Lennart): Retired from TabArena v0.2 as too small (task-probe review). The 195 recordings come from 32 people, 24 with Parkinson's and 8 healthy, so the whole healthy class is 8 voices: every grouped test fold holds 10-11 patients, 2 or 3 of them healthy, and the 60 folds recombine the same 8. Scored per patient as v2 declares (`mean`), one fold's ROC AUC rests on 16-24 patient pairs. On BeyondArena (scored per recording, 35 folds) the best method (RealMLP, tuned + ensemble) reaches AUC 0.874, the median 0.809 and TabPFN-3 0.757; the best method's AUC ranges from 0.58 to 1.0 over the folds, and the method ranks agree across folds less than on 98% of BeyondArena datasets (Kendall's W 0.18). The task is learnable (the best single feature, chosen on each split's training side, reaches AUC 0.785, above only 10 of 37 configurations), but a method's rank depends on how it scores these 8 healthy people.

## Reference

If you use this dataset, please cite the following paper: 
'Exploiting Nonlinear Recurrence and Fractal Scaling Properties for Voice Disorder Detection', 
Little MA, McSharry PE, Roberts SJ, Costello DAE, Moroz IM. 
BioMedical Engineering OnLine 2007, 6:23 (26 June 2007)
