---
unique_name: 5g_energy_consumption
name: aiml-for-5g-energy-consumption-modelling
checked_by:
- Andrej
data_foundry_status: 'Yes'
suggestion: TBD -> Yes
decision_markers:
- Data Quality Issue
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Zindi
problem_type: Regression
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/aiml-for-5g-energy-consumption-modelling
- https://huggingface.co/datasets/netop/5G-Network-Energy-Consumption
- https://challenge.aiforgood.itu.int/match/matchitem/83
- https://github.com/ITU-AI-ML-in-5G-Challenge/5G-Energy-Consumption-Modelling-Solution-Team-Farzi-Data-Scientists/tree/main
source_row: 890
type_adapter_id: curation-record-v1
---

# aiml-for-5g-energy-consumption-modelling

## Comments

Would require grouped-temporal split, but not possible due to data size

We could do a grouped split as a validation study, but this would not exactly correspond to the actual task
