---
unique_name: michelin
name: Michelin
checked_by:
- Lennart
- Mustafa
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Free Text (Sentences)
- New IID
collections:
- CARTE/TARTE
- TabSTAR
year: '2026'
source_links:
- https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021
- https://guide.michelin.com/en/restaurants https://raw.githubusercontent.com/ngshiheng/michelin-my-maps/main/data/michelin_my_maps.csv
source_row: 22
type_adapter_id: curation-record-v1
---

# Michelin

## Comments

Scraped and curated Michelin restaurants data

still gets updated!

Any predictive task related to the starts is super random as the process of getting starts is quite complicated with and has a lot of edge cases not related to features

Has spatial information, but likely not leakage (but requires preprocessing)

Could try to get more data from websites etc

There is no way we can construct a task from this data that does make any sense

## Reference

https://doi.org/10.34740/kaggle/dsv/14367500 / Kaggle
