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
v2_path: datasets/_dev/tabarena-v0pt2/infrared_thermography_temperature/dataset.py
source_row: 665
type_adapter_id: curation-record-v1
---

## Comments

Two targets. Need to carefully check which features make sense to include in the predictive task. Some might be unreasonable. Some features were extracted from infrared images, but those are not given

Discussion: I think this is grouped, subject ID is not unique but counts up with -1,-2,...

**Assessment (AI, 2026-10-07):** Added as a regression of `aveOralM` (oral temperature, monitor mode, the reference of both papers); `aveOralF`, the same readings in fast mode, is dropped as a second measurement of the target. Data: PhysioNet's FLIR_groups1and2.csv, 1,018 subjects (CC0). SubjectID is yymmdd-n and unique per row, so each subject is one row; holding out whole measurement days changes R² by less than 0.004, so the split stays IID, with temporal and day-grouped splits as alternatives. The 17 subjects without a complete round-1 image keep their later image. Random forest R² 0.707 (RMSE 0.274 against 0.509 for the mean), and an additive model beats the source's one-feature calibration on 28 of 30 splits. Is the modality marker an exception here?

## Reference

Infrared Thermography for Measuring Elevated Body Temperature: Clinical Accuracy, Calibration, and Evaluation
By Quanzeng Wang, Yangling Zhou, Pejman Ghassemi, David McBride, J. Casamento, T. Pfefer. 2021

Published in Italian National Conference on Sensors
