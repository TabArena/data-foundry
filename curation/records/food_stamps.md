---
unique_name: food_stamps
name: Food Stamps
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Not Representative
- Duplicate
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

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `acs_food_stamps_2014_2024` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-08, Lennart): `No` with `Duplicate` of acs_food_stamps_2014_2024: TableShift's 2018 file of the same ACS item (FS) and population filter lies inside that record's 2014-2024, and its only extra, the held-out East South Central division, is `Not Representative` (PROV-6; consistency check of 2026-11-08).

**Assessment (AI, 2026-11-09):** the CC of 2026-11-08 says TableShift's file has the "same ACS item (FS) and population filter" as acs_food_stamps_2014_2024; its build (folder acs_food_stamps_2014_2024_1m) no longer matches the second part. It keeps one row per occupied household with no filter on the person, where TableShift keeps one row per adult aged 18 to 61 with a personal income up to $30,000. The item FS and the survey are the same, so the `Duplicate` verdict holds (PROV-6: a newer, longer release of the same source and item); the curator's wording is left as written.
