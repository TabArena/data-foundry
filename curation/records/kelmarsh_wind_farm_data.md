---
unique_name: kelmarsh_wind_farm_data
name: Kelmarsh wind farm data
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/competitions/predict-the-wind-speed-at-a-wind-turbine
- https://zenodo.org/records/5841834
- (muchn newer data on Zenodo)
source_row: 622
type_adapter_id: curation-record-v1
---

# Kelmarsh wind farm data

## Comments

Unclear if the task is reasonable, need to take a closer look

Kaggle: Predicting from one turbine to another (so more or less grouped but also temporal, as we predict in the future?)
"The data is split between train and test datasets by weeks: 2-weeks are assigned to the training dataset, which includes the target_feature, then 1-week is assigned to the test dataset, which excludes it, and this is repeated for the full dataset."
Kaggle task is from same person that uploaded the Kaggle competition, so it seems reasonable to do? Unclear how real of a task it is....
