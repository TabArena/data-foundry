---
unique_name: ev_charging_station_data_california_region
name: EV Charging Station Data- California Region
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Missing source information
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/datasets/datasetengineer/ev-charging-station-data-california-region
source_row: 184
type_adapter_id: curation-record-v1
---

## Comments

The data is described in limited detail and might contain some real features but other features are clearly made up (the weather is perfectly uniformly distributed in California!), thus I judge it as fake data

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `acn_data_ev_charging_sessions` (TBD -> Yes, priority 3), `norway_residential_ev_charging_sessions` (TBD -> 2nd Tier, priority 1). Each is screened in its own record; this record's verdict stays the curator's.
