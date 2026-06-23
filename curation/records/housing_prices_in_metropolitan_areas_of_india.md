---
unique_name: housing_prices_in_metropolitan_areas_of_india
name: Housing Prices in Metropolitan Areas of India
checked_by:
- Lennart
data_foundry_status: Suspended
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
- Data Quality Issue
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
- Scientific Discovery
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ruchi798/housing-prices-in-metropolitan-areas-of-india
source_row: 671
type_adapter_id: curation-record-v1
---

# Housing Prices in Metropolitan Areas of India

## Comments

Looks good to use. Scraped from the internet, not temporal information, but likely still a valid task given the features

Contains several groups of data, so we could merge it to one task and try to learn to predict, but likely one model per task is okay. Notebook from creator did create one dataset by merging all of them. I think we can do the same and it is still a good task (even if sub-splitting might give better perofrmance)

Bangalore.csv
Chennai.csv
Delhi.csv
Hyderabad.csv
Kolkata.csv
Mumbai.csv

Because we are missing temporal information, this could be seen as a scientifc discovery task. I see it as a gap-filling task (predict prices of houses sold for which we dont know the price for the sake of using it)

But it really should not be seen as such. The data contains duplicates (likely prices from the same house, almost 50% of the data). So it really needs the missing temporal information to be a valid task. Thus this cannot be used.

## Reference

Kaggle
