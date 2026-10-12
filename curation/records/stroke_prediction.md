---
unique_name: stroke_prediction
name: Stroke Prediction
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
decision_markers:
- Missing source information
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Other
year: '2021'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset
v2_path: datasets/_dev/tabarena-v0pt2/stroke_prediction/dataset.py
source_row: 669
type_adapter_id: curation-record-v1
---

## Comments

Unclear if data is fake (https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset/discussion/218525)

When asked for the dataset source, the uploader repeatedly says that it is confidential, without commenting whether it's real or not. Also, he says "you should only use this dataset for educational purposes, not for research or economical purposes."

The data looks reasonable to use, is used a lot, and might be real. We can use it for now and filter later if needed

**Assessment (AI, 2026-10-07):** Source traced: the Kaggle file is a cut of the training file of the McKinsey Analytics Online Hackathon (Analytics Vidhya DataHack, 2018-04-14; 43,400 patients, 783 strokes; byte-identical on Mendeley Data, doi:10.17632/x8ygrw87jw.1). The file is partly generated or altered: Residence_type, ever_married and work_type carry nothing beyond age (likelihood-ratio p 0.39-0.88; BRFSS 2015 data of the same size shows clear dependence). Women and men aged 25-29 are married alike (45.0% each; BRFSS 53.8% / 40.3%), Residence_type is a coin flip independent of every column, and glucose is flat from 55 to 65 mg/dL with nothing lower. The clinical columns look real. A missing BMI follows the stroke (adjusted odds ratio 3.7). Suggest No + AHDS / Data Quality Issue.

## Reference

Kaggle
