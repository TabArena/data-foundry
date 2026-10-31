---
unique_name: 5g_energy_consumption
name: aiml-for-5g-energy-consumption-modelling
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Data Quality Issue
tags:
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: Zindi
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/aiml-for-5g-energy-consumption-modelling
- https://huggingface.co/datasets/netop/5G-Network-Energy-Consumption
- https://challenge.aiforgood.itu.int/match/matchitem/83
- https://github.com/ITU-AI-ML-in-5G-Challenge/5G-Energy-Consumption-Modelling-Solution-Team-Farzi-Data-Scientists/tree/main
notebook_path: datasets/beyond_iid/grouped/5g_energy_consumption/5g_energy_consumption.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/5g_energy_consumption/dataset.py
source_row: 890
type_adapter_id: curation-record-v1
---

## Comments

Would require grouped-temporal split, but not possible due to data size

We could do a grouped split as a validation study, but this would not exactly correspond to the actual task

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays `mape`: the challenge ranked the private leaderboard by weighted MAPE, the weights (higher for new stations or configurations) given in its test file (Zindi evaluation page). Here every test station is new and the weights are not in the released data, so unweighted MAPE is the nearest listed metric. The notes now name WMAPE. Needs a rebuild to reach the container (notes only).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: stand_in mape — stands in for Weighted MAPE (WMAPE), Zindi private leaderboard: false: the per-row WMAPE weights come with the test file and are not published; every test station here is new, so unweighted mape is the closest stand-in (https://zindi.africa/competitions/aiml-for-5g-energy-consumption-modelling).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): codes shipped as numbers, left for the curator's review: `weekday_number`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): weekday_number a category.
