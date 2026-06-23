---
unique_name: cdc_indicators_of_heart_disease
name: CDC Indicators of Heart Disease
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- Larger IID Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: Kaggle
year: '2015'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease
- https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset
- 'Likley highly related to: 10.24432/C53919'
- (https://www.kaggle.com/datasets/tarekmuhammed/patients-data-for-medical-field/ is a duplicate / cleaned version)
- https://www.openml.org/search?type=data&id=46598&sort=runs&status=active
- https://www.cdc.gov/brfss/annual_data/2015/pdf/codebook15_llcp.pdf
source_row: 657
type_adapter_id: curation-record-v1
---

# CDC Indicators of Heart Disease

## Comments

Dataset is preprocessed version already https://www.kaggle.com/code/alexteboul/diabetes-health-indicators-dataset-notebook
The selection looks very reasonable and well motivated, I would keep it
Biggest problem: it drops rows with na...

It makes sense to filter to only cases that answer the questions truthfully and fully for a less-biased predictive model  in the medical domain. Moreover, given the larget amount of data, this seems okay do it. I would use it the way it is for now and only fix / add new version of it if we get a domain expert to make the decisions. 

Goes from 441,456 records and 330 -> 253,680, 21

Need to decide which version to take for the label: 
0 = no diabetes 1 = prediabetes 2 = diabetes
0 = no diabetes 1 = prediabetes &  diabetes

Use first case as it is more native to the real world problem and less biased.


(Rel https://www.cdc.gov/pcd/issues/2019/19_0109.htm)

## Reference

Kaggle
