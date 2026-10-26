---
unique_name: scku_datathon
name: scku-datathon
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/scku-datathon/data
source_row: 957
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): the SCKU Datathon (Zindi, 2024-02-25 to 2024-03-08, "a private hackathon only open to SKCU members") re-runs the Ernst & Young Carbon Prediction Competition (2023-02-23 to 2023-05-01), its parent in the Zindi API.
- Source: https://zindi.africa/competitions/scku-datathon; files Train.csv 95,570,638 bytes, Test.csv 36,024,298, SampleSubmission.csv 725,308, EY_Carbon_Prediction_StarterNotebook.ipynb and GetStarted.pdf, the same names and byte sizes as https://zindi.africa/competitions/ey-carbon-prediction-hackathon; the same task text (Sentinel-5P weekly pollutant columns at ~500 South African locations, 2019-01 to 2022-11, target `emission`, IDs `ID_LAT_LON_YEAR_WEEK`).
- Siblings and duplicates: the first publication, the EY hackathon, is in `source_links` of `carbon_dioxide_prediction_challenge` (AI-screened `TBD -> 2nd Tier`, priority 2, 2026-10-22), which keeps the five Zindi pages of this dataset in one record; this record ends at the same source (PROV-4, PROV-8).
- Metric: `rmse`, Zindi Evaluation page.
- Reject check (AI, 2026-10-22): stands. PROV-4/PROV-5 confirmed from the Zindi API: scku-datathon (2024-02-25) has parent 'ey-carbon-prediction-hackathon' (2023-02-23) and identical files and sizes (Train.csv 95,570,638; Test.csv 36,024,298; SampleSubmission.csv 725,308; EY_Carbon_Prediction_StarterNotebook.ipynb 2,679,805; GetStarted.pdf 106,935). The EY page is already in source_links of carbon_dioxide_prediction_challenge.

This Zindi 'SCKU datathon' record has no comments, target description, or metadata beyond the competition link, so the task type, modality, target, and size are all unknown. There is too little information to decide, and datathons can span forecasting, NLP, or image tasks. A human must open the competition page to determine whether it is a genuine tabular predictive classification/regression task with a clear target and adequate size.
