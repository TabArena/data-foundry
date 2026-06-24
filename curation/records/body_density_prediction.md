---
unique_name: body_density_prediction
name: bodyfat
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Disagreement
decision_markers:
- Outdated
- Not Representative
- Too Small
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: Other
year: '1985'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/560
- https://www.kaggle.com/datasets/fedesoriano/body-fat-prediction-dataset
source_row: 750
type_adapter_id: curation-record-v1
---

# bodyfat

## Comments

Looking good, might be trivial or easy

original source is UCI, now gone. Found on OpenML and on Kaggle

Data looks good but is a bit old. There should be more/newer data with the same task as this is still done by models in machines in gyms.

Note, the task is not about bodyfat prediction as this is determined by a deterministic formula. Instead, the task is to estimate the density (which can be used to get the body fat via the deterministic formula). However, density requires a test. So we aim to predict from data the density such that we can skip this test.

Discussion: In general a valid task, but if someone would actually want to build a serious predictive model for that it would be possible to collect a lot more data.

Also, I think that the use from this is limited unless we actually embed the density prediction into the body fat formula and evaluate on that. Better alternatives for this task (ChatGPT):
1) NHANES https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.htm
2) UK Biobank (restricted access): https://www.ukbiobank.ac.uk/about-our-data/types-of-data/physical-measurements/

## Reference

@article{penrose1985generalized,
  title={Generalized body composition prediction equation for men using simple measurement techniques},
  author={Penrose, Keith W and Nelson, Arnold G and Fisher, Arnold Garth},
  journal={Medicine \& Science in Sports \& Exercise},
  volume={17},
  number={2},
  pages={189},
  year={1985},
  publisher={Ovid Technologies (Wolters Kluwer Health)}
}
