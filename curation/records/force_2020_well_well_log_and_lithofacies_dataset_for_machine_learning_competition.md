---
unique_name: force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition
name: FORCE 2020 Well well log and lithofacies dataset for machine learning competition
checked_by:
- Lennart
data_foundry_status:
- 'DF: WIP'
suggestion: 'Yes'
tags:
- Larger IID Data
- Non-IID (Grouped)
- Review Prio 1 (Atlas)
collections:
- TabArena Submission
original_source: Github
year: '2020'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
- '?'
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition/tree/master
- https://zenodo.org/records/4351156
- https://github.com/TabArena/tabarena_dataset_curation/issues/2
- https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition/tree/master/lithology_competition
- https://docs.google.com/document/d/13XAftsBVHIm01ZN0lP56Q4hZ9hgdYR1G_6KeV2DdzOA/edit?tab=t.0
source_row: 660
type_adapter_id: curation-record-v1
---

## Comments

Data based on images or other data is made tabular. But competitions used tabular models?

Need to double-check. Also, once checked, update GitHub issue! "

"We held out 10 wells where we only provided the logs (test dataset) and 10 wells that were not provided at all to the contestants."
"10 random wells from the train data set were used in preparing a validation set. Two validation sets were made from each train set prepared. "

## Reference

Bormann P., Aursand P., Dilib F., Dischington P., Manral S. 2020. FORCE Machine Learning Competition. https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition
