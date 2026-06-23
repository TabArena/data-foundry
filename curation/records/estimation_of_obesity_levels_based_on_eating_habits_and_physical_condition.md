---
unique_name: estimation_of_obesity_levels_based_on_eating_habits_and_physical_condition
name: Estimation of Obesity Levels Based On Eating Habits and Physical Condition
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
decision_markers:
- Data Quality Issue
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2019'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5H31Z
- https://www.openml.org/search?type=data&id=46597&sort=runs&status=active
- https://www.kaggle.com/datasets/fatemehmehrparvar/obesity-levels
source_row: 673
type_adapter_id: curation-record-v1
---

# Estimation of Obesity Levels Based On Eating Habits and Physical Condition

## Comments

"77% of the data was generated synthetically using the Weka tool and the SMOTE filter, 23% of the data was collected directly from users through a web platform."

No problem! We can filter the SMOTE data as they are clearly different (float instead of int) values and later in the file. Filter them and then use, might become trivial

Maybe need to transform labels (bins) back to Mass body index regression value instead?...
Need to recompute the body index, remove weight and height which give the target

TODO: remove height / weight, make regression task, remove SMOTE samples

## Reference

@article{palechor2019dataset,
  title={Dataset for estimation of obesity levels based on eating habits and physical condition in individuals from Colombia, Peru and Mexico},
  author={Palechor, Fabio Mendoza and De la Hoz Manotas, Alexis},
  journal={Data in brief},
  volume={25},
  pages={104344},
  year={2019},
  publisher={Elsevier}
}
