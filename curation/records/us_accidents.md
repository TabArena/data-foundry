---
unique_name: us_accidents
name: US Accidents
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- Free Text (Short)
collections:
- CARTE/TARTE
- TabSTAR
source_links:
- https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
- https://arxiv.org/abs/1906.05409 https://arxiv.org/abs/1909.09638
source_row: 493
type_adapter_id: curation-record-v1
---

# US Accidents

## Comments

nformation of accidents in US cities between 2016 and 2023. From this dataset, two tasks are conducted: (1) the range of accident counts for the US cities (2) the severity of the reported accidents

Just survey data for insights, not predictive task or features that would be collected like in a predictive task

Kaggle-spotted-problems: timestamps are wrong, a few other problems

Might need to filter by source of accident, has spatial components"Description

Descriptions are short blurbs containing mostly geolocation and no other meaning, so it is closer to a string than a real-world sentence. It is also a very clear format for the text, which could be solved via FE.
