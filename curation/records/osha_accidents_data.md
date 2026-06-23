---
unique_name: osha_accidents_data
name: OSHA_accidents_data
checked_by:
- Lennart
- Mustafa
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- Free Text (Sentences)
- Non-IID (Temporal)
collections:
- TexTabBench
original_source: GOV Website
year: '2017'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ruqaiyaship/osha-accident-and-injury-data-1517
- https://www.osha.gov/data
source_row: 479
type_adapter_id: curation-record-v1
---

# OSHA_accidents_data

## Comments

Workplace Accidents 2015-2017; could get newer version of data;  unclear what might be a good traget given the domain

sometimes contains very specific info that might be deemed PII; has many multi-categorical columns for event data; text seems to follow a standard formatting that we could also engineer to be more free text

## Reference

Kaggle
