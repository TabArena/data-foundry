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
notebook_path: datasets/beyond_iid/new_iid/homesite_quote_conversion/homesite_quote_conversion.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/homesite_quote_conversion/dataset.py
source_row: 651
type_adapter_id: curation-record-v1
---

## Comments

CC: "Split seems to be random per QuoteNumber sample; feature engineered geographic information as it seems"

This data was used as non-IID by TabRed! It was non-iid by https://arxiv.org/abs/2407.02112

LP: I vote for IID based on the Kaggle discussions on how to do cross-validation, my understanding of the prediction task, and that the test data contains timestamps from the same period as the train. At the same time, the date seems to be a real-world factor that we could introduce for splits and use in such a way. Likely we want to treat it as non-IID

We keep it as IID but add a warning to its usage.

CC (2026-10-01, Lennart): Leak audit: possible leak, kept for now on purpose; revisit if the fields are ever documented. `PropertyField37` x `PersonalField12` looks like a status code filled after the quote: (Y, 1-4) holds 20,008 quotes, 99.3% converted (40.6% of all conversions); (Y, 5) holds 54,769 quotes, 0.14% converted. Dropping both lowers LightGBM AUC from 0.965 to 0.915. Kept because the fields are anonymised (the meaning cannot be checked), Homesite set the competition up with them (the official test data has the same fields), and removing a possibly valid signal on a guess would change the host's task. The Kaggle discussions (about 80 threads read via the kaggle CLI, incl. the winners' and best-single-model threads) never mention either field; top private scores were AUC 0.969-0.97, so all strong solutions used the signal. Cost to keep in mind: the dataset sits near its ceiling, which compresses differences between strong models.

## Reference

Darrel, Stephen D Stayton, and Will Cukierski. Homesite Quote Conversion. https://kaggle.com/competitions/homesite-quote-conversion, 2015. Kaggle.
