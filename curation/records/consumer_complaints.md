---
unique_name: consumer_complaints
name: Consumer Complaint Database
checked_by:
- Lennart
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- Free Text (Sentences)
collections:
- TexTabBench
original_source: GOV Website
year: '2019'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/selener/consumer-complaint-database
- https://catalog.data.gov/dataset/consumer-complaint-database
notebook_path: datasets/beyond_iid/temporal/consumer_complaints/consumer_complaints_1m.ipynb
source_row: 735
type_adapter_id: curation-record-v1
---

## Comments

Real world complaints about financial products and services; data might contain sub-cohorts based on reporting category; we might want to filter to only a subset of cohorts; many missing values; data might have temporal drift; contains zip code to get more tabular features; temporal; we could get a new version of the data from the website

Needs a lot of preprocessing / feature engineering to become a usable task

We got the newer version from here: https://www.consumerfinance.gov/data-research/consumer-complaints/

Ref for descriptions https://cfpb.github.io/api/ccdb/fields.html

Only "Consumer complaint narrative" is a sentence field. "Company public response" is from one a predefined list of options

## Reference

Kaggle / Gov
