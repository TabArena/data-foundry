---
unique_name: homesite_quote_conversion
name: Homesite_Quote_Conversion
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2016'
domain: insurance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/homesite-quote-conversion/data?select=train.csv.zip
source_row: 651
type_adapter_id: curation-record-v1
---

# Homesite_Quote_Conversion

## Comments

CC: "Split seems to be random per QuoteNumber sample; feature engineered geographic information as it seems"

This data was used as non-IID by TabRed! It was non-iid by https://arxiv.org/abs/2407.02112

LP: I vote for IID based on the Kaggle discussions on how to do cross-validation, my understanding of the prediction task, and that the test data contains timestamps from the same period as the train. At the same time, the date seems to be a real-world factor that we could introduce for splits and use in such a way. Likely we want to treat it as non-IID

We keep it as IID but add a warning to its usage.

## Reference

Darrel, Stephen D Stayton, and Will Cukierski. Homesite Quote Conversion. https://kaggle.com/competitions/homesite-quote-conversion, 2015. Kaggle.
