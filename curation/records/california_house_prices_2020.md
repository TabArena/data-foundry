---
unique_name: california_house_prices_2020
name: CALIFORNIA_PRICES_2020
checked_by:
- Lennart
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Missing source information
tags:
- Non-IID (Temporal)
- Free Text (Sentences)
collections:
- AutoML_MM
- TabSTAR
original_source: Other
year: '2021'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46669
- https://www.kaggle.com/c/california-house-prices
source_row: 734
type_adapter_id: curation-record-v1
---

## Comments

California Houses 2020 Prices (Duplicate with calif_houses below).

Timestamp is missing! ....

Unclear if summary has an impact on predictions. A lot of spatial features, likely require spatial splits.

Very likely scraped from https://www.redfin.com/CA/Los-Altos/540-Pine-Ln-94022/home/1137626 / https://www.redfin.com/news/data-center/

Only data from redfin looks like this: https://www.kaggle.com/datasets/thuynyle/redfin-housing-market-data?select=neighborhood_market_tracker.tsv000
One could buy a scraped version: https://crawlfeeds.com/datasets/redfin-usa-properties-dataset

Summary contains free text that might not be super useful but still very much contains a lot to extract

---

Sold Price is target from the kaggle competition, the TextTabBench Paper considers Total interior livable area and Listed Price instead, data might be spatial and temporal. How do we deal with multi-categorical columns like Heating/Cooling/Parking? Also the Bedroom column is sometimes integer sometimes Text (multi-categorical), I feel like it could take a lot of preprocessing depending on what we do with columns like Heating/Cooling/Parking and similar

Unclear source of data, likely copied from somewhere with modifications. Used for teaching maybe? Data looks scraped

We need to find the original source... something from D2L website

MT: summary column feels like it makes more sense to be preprocessed into multiple columns, if it was to be converted to an embedding I can see the LM doing the conversion being confused by some fancy wording that may not mean a better apartment (like italian style of apartment) and leading to misleading results, so it makes sense just to be preprocessed in a real life scenario
Also in a real life scenario images would be used as well for such task

## Reference

Kaggle
