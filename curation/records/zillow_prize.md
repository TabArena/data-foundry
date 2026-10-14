---
unique_name: zillow_prize
name: Zillow Prize
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Kaggle
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.kaggle.com/competitions/zillow-prize-1
v2_path: datasets/_dev/tabarena-v0pt2/zillow_prize/dataset.py
source_row: 727
type_adapter_id: curation-record-v1
---

## Comments

Looks like a good temporal dataset

Multiple targets due to working for multiple time horizons, still looks good to just take one of these that we can reproduce on train data as it computes the score in a special way based on these forecasts

Not a lot of information about solutions. Some I see use extensive feature engineering. See what / how we can give it to the model most raw

Basic: https://www.kaggle.com/code/anokas/simple-xgboost-starter-0-0655

**Assessment (AI, 2026-10-07):** Valid temporal regression. The target is Zillow's own residual, log(Zestimate) - log(SalePrice), which Zillow models to improve the Zestimate (FAQ, discussion 33899). Each sale must take the property file of its year: properties_2017 holds edits made after early-2016 sales (building facts differ for 1.2-2.0% of parcels sold January-May 2016, 0.81% of unsold ones), and Zillow warns about its tax values (discussion 40408). August and September 2017 are incomplete ("a biased sample", same post). Concern: sales with |logerror| > 1 (0.4%, mostly miskeyed prices) hold half of the squared error; the competition scored MAE. The signal is small but real: robust LightGBM fits beat the train mean on 9 of 9 monthly windows. The rules forbid redistribution.
