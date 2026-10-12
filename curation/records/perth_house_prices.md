---
unique_name: perth_house_prices
name: Perth-House-Prices
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabSTAR
original_source: Kaggle
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=43822&sort=runs&status=active
- http://house.speakingsame.com/
- https://www.kaggle.com/datasets/syuzai/perth-house-prices
v2_path: datasets/_dev/tabarena-v0pt2/perth_house_prices/dataset.py
source_row: 729
type_adapter_id: curation-record-v1
---

## Comments

Data looks real, way back machine shows this was once a real website. Should be usable for some sort of house price prediction task

Data looks good to use; again, house prices...
But otherwise great features and setup for one of these tasks

Some scraping and minor issues: https://www.kaggle.com/datasets/syuzai/perth-house-prices/discussion/383033

**Assessment (AI, 2026-10-07):** Provenance traced: the uploader scraped house.speakingsame.com and added G-NAF coordinates and bettereducation ranks; OpenML 43822 is the same table. Each property appears once, with its latest sale before 31 January 2021; each suburb holds only its newest sales. The upload stops at $2,440,000, an undocumented cut (1.5% of 2015-2020 house sales in a 2024 Kaggle scrape cost more): the dearest suburbs keep only cheaper sales. The attributes are the site's record: 563 sales predate the build year (dropped), and 23% of the 2020 sales shared with that scrape list fewer bedrooms or bathrooms than their sold listing (stale; noise, not a leak). Temporal task, 9 monthly windows of 2020; LightGBM R² 0.86, no probe flags.
