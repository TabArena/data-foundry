---
unique_name: framingham_heart_study_fhs
name: Framingham Heart Study (FHS)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
tags:
- New IID
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2013'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/christofel04/cardiovascular-study-dataset-predict-heart-disea/data
- https://www.kaggle.com/datasets/aasheesh200/framingham-heart-study-dataset
- https://www.framinghamheartstudy.org/fhs-for-researchers/data-available-overview/
- https://www.nhlbi.nih.gov/science/framingham-heart-study-fhs
- https://www.framinghamheartstudy.org/fhs-risk-functions/hard-coronary-heart-disease-10-year-risk/
v2_path: datasets/_dev/tabarena-v0pt2/framingham_heart_study_fhs/dataset.py
source_row: 667
type_adapter_id: curation-record-v1
---

## Comments

Likely use data from Kaggle

A bit hard to parse what the origin is and where the Kaggle data was downloaded from, but we can use it

**Assessment (AI, 2026-10-07):** All three Kaggle uploads are `framingham.csv` from MIT's 15.071 The Analytics Edge (OCW Spring 2017; aasheesh200 is byte-identical). Its 4,240 rows are the baseline exam (period 1, PREVCHD = 0) of the NHLBI BioLINCC Framingham teaching dataset; all 15 features match row for row. MIT's `TenYearCHD` equals TIMECHD < 10 years in all 4,240 rows, but TIMECHD is the censor date for participants without an event (documentation, p. 4). So 265 of its 644 positives had no CHD: 249 died of other causes and 16 were lost to follow-up. The v2 definition reads the teaching data (CRAN riskCommunicator) and rebuilds the label: 4,224 participants, 379 with CHD. BioLINCC calls teaching data "completely unsuitable for publication purposes".

## Reference

https://www.nhlbi.nih.gov/sites/default/files/media/docs/risk-assessment.pdf
