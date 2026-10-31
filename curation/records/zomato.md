---
unique_name: zomato
name: Zomato
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- No Good Target / Scientific Discovery
tags:
- Free Text (Short)
collections:
- CARTE/TARTE
- TexTabBench
source_links:
- https://www.kaggle.com/datasets/anas123siddiqui/zomato-database?select=restaurant.csv
source_row: 494
type_adapter_id: curation-record-v1
---

## Comments

"Data has been taken from different sources from databases, websites, and credential data was generated itself"
Some of the data is fake, the other data could be used for predictions?

Food delivery rating

Orders and important information about sales etc are dummy-generated and not real data! Likewise, for some values of the users.

Some of the data could be used for a tabular task, unclear how much we can use it for text-based tasks without major additional effort on our side

**Assessment (AI, 2026-10-31):** the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) carries a related version, "Zomato Restaurants", not this record's data, so no collection tag: Text-tabular; raw user review text and vote count are features (posted alongside the rating). The record zomato is tagged CARTE/TexTabBench but links a different Kaggle dataset (anas123siddiqui/zomato-database, partly generated); MulTaBench's source is the Bangalore scrape, so the record's link may be wrong.
