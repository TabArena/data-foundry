---
unique_name: expresso_churn_prediction
name: expresso-churn-prediction
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Review Prio 1 (Atlas)
- New IID
- Larger IID Data
collections:
- New
original_source: Zindi
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/expresso-churn-prediction/data
- https://zindi.africa/competitions/dsn-pre-bootcamp-hackathon-expresso-churn-prediction-challenge
- https://zindi.africa/competitions/customer-churn-prediction-learning-experience/data
- https://zindi.africa/competitions/expresso-churn-prediction-challenge
- https://zindi.africa/competitions/microsoft-x-dsn-free-ai-classes-in-every-city-hackathon-expresso-churn-prediction/data
v2_path: datasets/_dev/tabarena-v0pt2/expresso_churn_prediction_1m/dataset.py
source_row: 912
type_adapter_id: curation-record-v1
---

## Comments

Expresso (telecom operator in Senegal & Mauritania) customer churn prediction (Zindi). One row per customer (~2.5M) with usage/tenure features aggregated over a 90-day window; target is binary churn. No explicit per-row time index, so a random split is plausible; verify there is no hidden temporal leakage from the aggregation window. Real telco data with a clear task → likely usable for the benchmark, pending verification of size after cleaning and of the split regime.

Lennart: solved with IID in the competition, and all features are set up to be IID. Need to check train-test region drift or similar, otherwise likely a valid task in this setting with all features being well-defined

**Assessment (AI, 2026-10-07):** There is no train-test drift. user_id is the SHA-1 hash of the extract's row number, and Zindi's Test.csv is a uniform random 15% of the extract. A model separating the two files scores ROC AUC 0.500, so the IID split stands.

REGION is dropped. Among churners it is missing for 92-95% at every level of activity (1 to 62 active days), while among stayers the share falls from 67% to 7%. The field looks filled after the observation window. Without it, ROC AUC falls from 0.93 to 0.90.

The Azubian (1,077,024 rows) and DSN (400,000 rows) cuts are rows of this Train.csv. On Zindi, indabax_eswatini_2022 lists the Azubian file and has this competition as its parent.

## Reference

Zindi
