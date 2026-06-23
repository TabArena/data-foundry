---
unique_name: stackoverflow_salary_data
name: stackoverflow_salary_data
checked_by:
- Lennart
- Mustafa
- Alex
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Free Text (Sentences)
- Larger IID Data
collections:
- TexTabBench Extra
original_source: Company
year: '2024'
domain: business & marketing
required_split:
- Random (IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/berkayalan/stack-overflow-annual-developer-survey-2024
- https://survey.stackoverflow.co/
source_row: 21
type_adapter_id: curation-record-v1
---

# stackoverflow_salary_data

## Comments

stackoverflow survey

Survey data would need work to make it a predictive task

Perfect example of a scientific discovery task. There is no relation in the collected data that we would want to predict in a real-world system. All of this is just to gather insights, not to learn something for new users. Moreover, there is no data task that could be forced to make sense somehow. There are simply no meaningful predictive relationships in the data

AP: all seem (multi-)categorical, but if there are so many categories we might consider going free text maybe?; 

LP: some of the features could be treated as free text most likely after adding some extra preprocessing

## Reference

Kaggle
