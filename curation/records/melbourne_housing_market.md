---
unique_name: melbourne_housing_market
name: Melbourne Housing Market
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
collections:
- New (BeyondArena)
original_source: Kaggle
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/anthonypino/melbourne-housing-market
- https://www.kaggle.com/datasets/dansbecker/melbourne-housing-snapshot
v2_path: datasets/_dev/tabarena-v0pt2/melbourne_housing_market/dataset.py
source_row: 726
type_adapter_id: curation-record-v1
---

## Comments

Similar to GOV data, no predictive task connected so far.

Unclear which version to use, scraped data in many cases.

Otherwise okay and another price prediction task for some cases.

**Assessment (AI, 2026-10-07):** Valid as a sale-price regression over Domain.com.au's weekly auction sheets, split by time. Version: Melbourne_housing_FULL.csv (Jan 2016 to Mar 2018): its realestate.com.au attributes lower RMSE in log price from 0.211 (the LESS file's columns) to 0.183. These were looked up after the sale, but close to it from late 2016 on: `Bedroom2` matches the sheet's bedroom count in 98.9-100% of each test window, against 85.2% for the Apr-Sep 2016 sales looked up in April 2017. Only S/SP/SA prices are sales; PI and VB prices are bids (4.3% and 6.6% below a sale-price model), dropped. dansbecker/melbourne-housing-snapshot (record melbourne_housing_snapshot) is a September 2017 subset of the full file. The Airbnb links belong to record melbourne_airbnb_open_data.

Related work, not a source: Melbourne Airbnb listings (https://www.kaggle.com/datasets/tylerx/melbourne-airbnb-open-data, from Inside Airbnb, https://insideairbnb.com/).
