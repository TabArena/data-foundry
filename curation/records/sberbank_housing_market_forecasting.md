---
unique_name: sberbank_housing_market_forecasting
name: Sberbank Housing
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2017'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/sberbank-russian-housing-market
- https://github.com/yandex-research/tabred/tree/main/preprocessing#sberbank-housing-market-forecasting
source_row: 711
type_adapter_id: curation-record-v1
---

# Sberbank Housing

## Comments

Use TabRed preprocessing (verify it)

TabRed uses 5 and 7 months for splits

Data splits used by Kaggle experts were grouped/stratified IID ("CV for Investment type model was almost unusable, but CV for OwnerOccupier"). The predicted mean was then off for test data and they used some magic numbers to correct. Thus it sounds like real temporal splits would be better. https://www.kaggle.com/competitions/sberbank-russian-housing-market/discussion/32717

Moreover, it seems that the data is merged from two groups!

## Reference

Alex Matveev, Anastasia_Sidorova_50806198, and DataCanary. Sberbank Russian Housing Market. https://kaggle.com/competitions/sberbank-russian-housing-market, 2017. Kaggle.
