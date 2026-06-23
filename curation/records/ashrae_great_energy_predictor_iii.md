---
unique_name: ashrae_great_energy_predictor_iii
name: ASHRAE - Great Energy Predictor III
checked_by:
- Lennart
data_foundry_status: Suspended
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- New - IST
original_source: Kaggle
year: '2019'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
- Temporal (NON-IID)
problem_type: Regression
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/ashrae-energy-prediction/leaderboard
source_row: 701
type_adapter_id: curation-record-v1
---

# ASHRAE - Great Energy Predictor III

## Comments

Solutions used IID version of the data, unclear if this is still the case but this is a forecasting-as-tabular task 

But alll solutions also used additonal data that had a leak. Leak should not be a problem for our benchmarking efforts

I think we can make this a nice split / use it for our setting

a lot of notes on this data....see data foundry. Split must be temporal/grouped. But also we only have 1 year but data was used to forecast 2 years....

## Reference

Addison Howard, Chris Balbach, Clayton Miller, Jeff Haberl, Krishnan Gowri, and Sohier Dane. ASHRAE - Great Energy Predictor III. https://kaggle.com/competitions/ashrae-energy-prediction, 2019. Kaggle.
