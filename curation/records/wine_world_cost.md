---
unique_name: wine_world_cost
name: wine_cost
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
- Free Text (Sentences)
collections:
- TexTabBench
original_source: Other
year: '2023'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/elvinrustam/wine-dataset
notebook_path: datasets/beyond_iid/new_iid/wine_world_cost/wine_world_cost.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/wine_world_cost/dataset.py
source_row: 682
type_adapter_id: curation-record-v1
---

## Comments

Need to check description for leakage; need to preprocess price; need to preprocess capacity; make secondary grape a description?; fix/normalize by unit; think about multi-cat column like characteristics; filter to per bottle price, make percentage a percentage, handle double year and parse to be number/date

Scraped from the web

**Assessment (AI, 2026-10-14):** the description check asked above is done. No description states the wine's own price (one quotes a stale price of the same wine, 17 compare with other wines). R² over the 9 splits: all text and tabular columns 0.724; with every sentence holding price or value words removed 0.721; everything except the description 0.700. The shop is most likely Majestic Wine (UK): 78 descriptions and 18 titles name it.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — scraped Kaggle dataset with no competition, paper or stated metric.
