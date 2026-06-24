---
unique_name: ble_rssi_dataset_for_indoor_localization
name: BLE_RSSI_dataset_for_Indoor_localization
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: UCI
year: '2019'
domain: technology & internet
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5B62T
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

UCI BLE RSSI indoor-localization dataset: predict location from Bluetooth Low Energy RSSI fingerprints at fixed reference points. It is a genuine real-world tabular task (RSSI values per beacon as features), already given a TabArena curation verdict of 'Temporal Tabular' with multiple reviewers agreeing on a temporal split. Representative of tabular ML and ethically unambiguous. A human must confirm the exact target formulation (discrete location/zone classification vs continuous coordinates), the cleaned size, and that the noted spatial+temporal structure is handled by the temporal split.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Temporal Tabular.

temporal

Potential issue: spatial and temporal data

Lennart: temporal data

Andrej: temporal split
