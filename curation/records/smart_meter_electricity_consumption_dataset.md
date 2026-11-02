---
unique_name: smart_meter_electricity_consumption_dataset
name: Smart Meter Electricity Consumption Dataset
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Missing source information
- AHDS (Artifical/Handmade/Deterministic/Simulated)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/datasets/ziya07/smart-meter-electricity-consumption-dataset
source_row: 172
type_adapter_id: curation-record-v1
---

## Comments

anomaly detection, could be used; looks very fake based on the distributions plus no source information

Note the user is ziya07 as for other fake datasets

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `lead1_energy_anomaly_detection` (TBD -> Yes, priority 2); a related task: `sgcc_electricity_theft_detection` (TBD -> 2nd Tier, priority 1). Each is screened in its own record; this record's verdict stays the curator's.
