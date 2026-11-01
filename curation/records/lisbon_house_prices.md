---
unique_name: lisbon_house_prices
name: Lisbon House Prices
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Missing source information
tags:
- Tiny Data
- New IID
collections:
- TabSTAR
source_links:
- https://www.kaggle.com/datasets/cgrodrigues/lisbon-house-prices
- https://www.openml.org/search?type=data&id=43660&sort=runs&status=active
source_row: 637
type_adapter_id: curation-record-v1
---

## Comments

We are missing where it is coming from, but the data looks reasonably real. Is an IID task where we try to figure out prices from the same year (ignoring leakage)

Unsure if we want to include, also since we have more than enough other price datasets. But likely still better than most 2nd tier datasets

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `portugal_real_estate_listings` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.
