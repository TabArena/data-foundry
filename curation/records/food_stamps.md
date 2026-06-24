---
unique_name: food_stamps
name: Food Stamps
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Not Representative
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- TableShift
source_links:
- https://tableshift.org/datasets.html#food-stamps
- https://www.census.gov/programs-surveys/acs
source_row: 609
type_adapter_id: curation-record-v1
---

## Comments

Holdout one region to get grouped data, unclear if real task would not also fit on some data from the same region (given that it is temporal). Consider, why would "a localized study that draws participants or respondents from some geographic areas, but excludes other areas" do for this kind of task?

As a result, the task seems not to be representative for real-world grouped data. Need to consider it when curating.

Moreover, we can create many other tasks from this data (see Unemployment, Income, Public Health Insurance
)
