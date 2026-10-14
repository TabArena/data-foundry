---
unique_name: digicow_farmer_training_adoption_challenge
name: DigiCow Farmer Training Adoption Challenge
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
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
v2_path: datasets/_dev/tabarena-v0pt2/digicow_farmer_training_adoption_challenge/dataset.py
source_row: 731
type_adapter_id: curation-record-v1
---

## Comments

"You are allowed to access and, use and share challenge data for the competition. for any commercial, non-commercial, research or education purposes, by open source."

Domain: agriculture

Discussion on possibly leaking features:
https://zindi.africa/competitions/digicow-farmer-training-adoption-challenge/discussions/30808

three classification tasks for 7, 90, and 120-day adoption windows. Competition used weighted average of logloss (25%) and ROC-AUC (75%)

**Assessment (AI, 2026-10-07):** Recommend `No` with `Too Small` and `Data Quality Issue`. The label shows adoption only where and when DigiCow recorded it. Of the 120-day adopters, 1 of the 1,021 trained in Aug-Oct 2024 adopted within 7 days, against 45%, 64% and 95% for Nov 2024, Dec 2024 and Feb 2025. One date, 2024-12-12, lies inside the adoption window of 1,028 of 2,389 adopters. TRA_gertumxc's farmers adopted at 5-13% in late 2024 and never in 2025. The temporal windows hold 9, 5, 19 and 103 adopters, from 1, 1, 2 and 7 trainers. The stored dates have day and month swapped. The challenge scored log loss 75% and ROC AUC 25% (reversed above).
