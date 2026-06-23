---
unique_name: digicow_farmer_training_adoption_challenge
name: DigiCow Farmer Training Adoption Challenge
checked_by:
- Andrej
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2026'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/digicow-farmer-training-adoption-challenge/data
source_row: 731
type_adapter_id: curation-record-v1
---

# DigiCow Farmer Training Adoption Challenge

## Comments

"You are allowed to access and, use and share challenge data for the competition. for any commercial, non-commercial, research or education purposes, by open source."

Domain: agriculture

Discussion on possibly leaking features: 
https://zindi.africa/competitions/digicow-farmer-training-adoption-challenge/discussions/30808

three classification tasks for 7, 90, and 120-day adoption windows. Competition used weighted average of logloss (25%) and ROC-AUC (75%)
