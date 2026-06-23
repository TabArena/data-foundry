---
unique_name: analyzing_customer_spending_habits
name: Analyzing Customer Spending Habits
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Website
year: '2017'
domain: business & marketing
required_split:
- Temporal (NON-IID)
- '?'
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/thedevastator/analyzing-customer-spending-habits-to-improve-sa
source_row: 537
type_adapter_id: curation-record-v1
---

# Analyzing Customer Spending Habits

## Comments

Looks good albeit some information are missing, scrapped from somewhere. The data comes with 3 target columns (more or less) about the revenue of the customer

Looking closer at the data, the distribution seems fake, the date seem fine but all other columns might be weird (also check the gender ration)

We cannot re-identify customers as they are not detectable from just the given features. so there might be one customer purchasing multiple things. The task would be to go from age, country, gender to what the value of the customer purchases

## Reference

https://data.world/vineet/salesdata
