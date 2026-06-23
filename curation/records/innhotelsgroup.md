---
unique_name: innhotelsgroup
name: INNHotelsGroup
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Missing source information
- Duplicate
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: Kaggle
year: '2024'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/mariyamalshatta/inn-hotels-group
source_row: 50
type_adapter_id: curation-record-v1
---

# INNHotelsGroup

## Comments

CC: "Predict whether a booking will be canceled. Nice dataset; maybe temporal data due to arrival year?"

We don't know the source. This is problematic as we don't know the period of time used for registering cancelations

After some digging, found an earlier reference: https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset/discussion/383267

This then pointed to a paper where a more extensive dataset can be downloaded, therefore I mark this a duplicate

## Reference

Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. Data in brief, 22, 41-49.
