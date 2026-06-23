---
unique_name: particulate_matter_ukair_2017
name: particulate-matter-ukair-2017
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
year: '2017'
source_links:
- openml 41267
- UK AIR homepage
- https://uk-air.defra.gov.uk/data/
source_row: 53
type_adapter_id: curation-record-v1
---

# particulate-matter-ukair-2017

## Comments

CC: "Benchmark excludes latitude and longitude. Has datetime features and two alternative targets. requires temporal split"

From what I can gather from the website, this is close to a multivariate forecasting task (forecasting the PM value per site); all "features" are just site/location information and the target is the PM value
