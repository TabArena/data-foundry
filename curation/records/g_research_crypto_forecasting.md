---
unique_name: g_research_crypto_forecasting
name: G-Research Crypto Forecasting
checked_by:
- Lennart
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2021'
domain: finance
required_split:
- Temporal (NON-IID)
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/g-research-crypto-forecasting/data?select=train.csv
source_row: 707
type_adapter_id: curation-record-v1
---

# G-Research Crypto Forecasting

## Comments

CC: "Stock data could be used, requires very specific splits and a lot of preprocessing, given its raw form, could try as is but will likely mostly be noise "

Forecasting-as-tabular task. Unsure if timestamps exist to create real splits. Would need some thought how to subsample

Solved with LGBM twice, training data seems to have enough data for creating our own splits for the future: https://www.kaggle.com/code/sugghi/training-3rd-place-solution

CV was temporal

## Reference

Alessandro Ticchi, Andrew Scherer, Carla McIntyre, Carlos Stein N Brito, Derek Snow, Develra, dstern, James Colless, Kieran Garvey, Maggie, Maria Perez Ortiz, Ryan Lynch, and Sohier Dane. G-Research Crypto Forecasting . https://kaggle.com/competitions/g-research-crypto-forecasting, 2021. Kaggle.
