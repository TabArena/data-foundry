---
unique_name: nyc_taxi_green_dec_2016
name: nyc-taxi-green-dec-2016
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- 2nd Tier / Scientfic Discovery
collections:
- TabArena Reject
- TabSTAR
year: '2016'
source_links:
- https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- https://www.openml.org/d/42729
- https://www.kaggle.com/c/nyc-taxi-trip-duration
- https://www.kaggle.com/datasets/wol4aravio/ny-taxi-trip-duration-enriched-by-mathematica
source_row: 631
type_adapter_id: curation-record-v1
---

## Comments

CC: "Various issues: Preprocessing required, time features, specific split, task is also conceptualized in a weird way - there is a Kaggle competition with a different target"

Checkout if there is a relevant task somewhere

Not super sure if this is a good task once we remove all leak or if it just turns out to be forecasting again

Pick one of the NYC green/yellow datasets
