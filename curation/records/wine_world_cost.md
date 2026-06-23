---
unique_name: wine_world_cost
name: wine_cost
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- New IID
- Free Text (Sentences)
collections:
- TexTabBench
original_source: Other
year: '2023'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/elvinrustam/wine-dataset
source_row: 682
type_adapter_id: curation-record-v1
---

# wine_cost

## Comments

Need to check description for leakage; need to preprocess price; need to preprocess capacity; make secondary grape a description?; fix/normalzie by unit; think about multi-cat column like characteristics; filter to per bottle price, make percentage a percentage, handle double year and parce to be number/date

Scraped from the web
