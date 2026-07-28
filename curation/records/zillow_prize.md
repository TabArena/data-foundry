---
unique_name: zillow_prize
name: Zillow Prize
checked_by:
- Lennart
data_foundry_status:
- 'DF: WIP'
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/competitions/zillow-prize-1
source_row: 727
type_adapter_id: curation-record-v1
---

## Comments

Looks like a good temporal dataset

Multiple targets due to working for multiple time horizons, still looks good to just take one of these that we can reproduce on train data as it computes the score in a special way based on these forecasts

Not a lot of information about solutions. Some I see use extensive feature engineering. See what / how we can give it to the model most raw

Basic: https://www.kaggle.com/code/anokas/simple-xgboost-starter-0-0655
