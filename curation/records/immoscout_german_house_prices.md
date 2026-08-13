---
unique_name: immoscout_german_house_prices
name: ImmoScout24 German-House-Prices
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
- Free Text (Short)
collections:
- TabSTAR
original_source: Kaggle
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=43342&sort=runs&status=active
- https://www.kaggle.com/code/shritech1404/german-housing-price-prediction
- Original source is a deleted dataset from Kaggle
notebook_path: datasets/beyond_iid/new_iid/immoscout_german_house_prices/immoscout_german_house_prices.ipynb
source_row: 684
type_adapter_id: curation-record-v1
---

## Comments

Missing date column, but as it represents a snapshot of data at a certain time point (when scraped) it represents live data and could be used to fit a model for other houses at the same time

Moreover, this is not sold prices (as immoscout shows only prices you can ask to buy it for and how much it was sold for AFAIK), so the snapshot here represents a task where someone would want to predict the price I should offer for my house given other houses that are currently offered. Thus, it seems like a real task where someone would want to build a model to know how much they should offer the houses at in the current market (with the limitation that past trends are ignored)

## Reference

Kaggle / OpenML
