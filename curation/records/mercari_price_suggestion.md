---
unique_name: mercari_price_suggestion
name: mercari_price
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
- Free Text (Sentences)
collections:
- TexTabBench
- TabSTAR
original_source: Kaggle
year: '2017'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/elizabethsam/mercari-price-suggestion-challenge https://www.kaggle.com/competitions/mercari-price-suggestion-challenge/overview
notebook_path: datasets/beyond_iid/new_iid/mercari_price_suggestion/mercari_price_suggestion_1m.ipynb
source_row: 658
type_adapter_id: curation-record-v1
---

## Comments

Mercari (Japanese shopping app); a lot of signal from text preprocessing (plus be aware of censoring), maybe create a version after text embeddings to use for benchmarking; likely temporal but all features are IID, so we can use as is; likely many categoricals.

Not sure how useful the name is given the existence of the description, also not sure about category — it could be split into categorical columns but would maybe have way too many.
