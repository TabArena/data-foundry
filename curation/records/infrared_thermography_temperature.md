---
unique_name: infrared_thermography_temperature
name: Infrared Thermography Temperature
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: Disagreement
decision_markers:
- Wrong Domain / Source Modality
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Website
year: '2023'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.13026/9ay4-2c37
- https://physionet.org/content/face-oral-temp-data/1.0.0/
source_row: 665
type_adapter_id: curation-record-v1
---

## Comments

Two targets. Need to carefully check which features make sense to include in the predictive task. Some might be unreasonable. Some features were extracted from infrared images, but those are not given

Discussion: I think this is grouped, subject ID is not unique but counts up with -1,-2,...

## Reference

Infrared Thermography for Measuring Elevated Body Temperature: Clinical Accuracy, Calibration, and Evaluation
By Quanzeng Wang, Yangling Zhou, Pejman Ghassemi, David McBride, J. Casamento, T. Pfefer. 2021

Published in Italian National Conference on Sensors
