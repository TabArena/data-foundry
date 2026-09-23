---
unique_name: cdc_diabetes_health_indicators
name: CDC Diabetes Health Indicators (BRFSS 2015)
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
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset
- https://www.kaggle.com/code/alexteboul/diabetes-health-indicators-dataset-notebook
- https://doi.org/10.24432/C53919
- https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
- https://www.openml.org/search?type=data&id=46598&sort=runs&status=active
- https://www.cdc.gov/brfss/annual_data/2015/pdf/codebook15_llcp.pdf
- (https://www.kaggle.com/datasets/tarekmuhammed/patients-data-for-medical-field/ is a duplicate / cleaned version)
source_row: 657
type_adapter_id: curation-record-v1
---

## Comments

Dataset is preprocessed version already https://www.kaggle.com/code/alexteboul/diabetes-health-indicators-dataset-notebook
The selection looks very reasonable and well motivated, I would keep it.
Biggest problem: it drops rows with na...

It makes sense to filter to only cases that answer the questions truthfully and fully for a less-biased predictive model in the medical domain. Moreover, given the large amount of data, this seems okay to do it. I would use it the way it is for now and only fix / add new version of it if we get a domain expert to make the decisions.

Goes from 441,456 records and 330 -> 253,680, 21

Need to decide which version to take for the label:
0 = no diabetes 1 = prediabetes 2 = diabetes
0 = no diabetes 1 = prediabetes &  diabetes

Use first case as it is more native to the real world problem and less biased.


(Rel https://www.cdc.gov/pcd/issues/2019/19_0109.htm)

CC (2026-09-23, Lennart): This record curates Teboul's "Diabetes Health Indicators" cut of BRFSS 2015 (253,680 x 21, diabetes target), which is what the notes above describe; UCI 891 (DOI 10.24432/C53919) and OpenML 46598 mirror it. It used to be named after its first link, kamilpytlak's "Personal Key Indicators of Heart Disease" (https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease), which is a different BRFSS cut (2020 wave, heart-disease target) and is not covered by this record; if wanted it needs its own record, and by our duplicate rule (same BRFSS data with another target) it would likely be `No` + `Duplicate`. TableShift's BRFSS Diabetes task (`diabetes_2`, waves 2015-2021, race shift) is marked Duplicate of this record.

## Reference

Kaggle
