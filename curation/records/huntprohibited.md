---
unique_name: huntprohibited
name: huntprohibited
checked_by:
- Lennart
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Free Text (Sentences)
- Non-IID (Temporal)
- Larger IID Data
collections:
- New - IST
original_source: Kaggle
year: '2014'
domain: business & marketing
required_split:
- Temporal (NON-IID)
- '?'
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/avito-prohibited-content/data?select=avito_train.zip
source_row: 642
type_adapter_id: curation-record-v1
---

# huntprohibited

## Comments

CC: "Russian text; text to features script exists; free-text categorical in json format, extra leaking column, that could be used to sub-filter data; close_hours leaking test data; some count features from text; likely some problem with malicous users, who one should detect instead of the ads itself"

needs some basic preprocessing as shown by the hosts; non english language might be a problem for downstream models

## Reference

Kaggle
