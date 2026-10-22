---
unique_name: ble_rssi_dataset_for_indoor_localization
name: BLE_RSSI_dataset_for_Indoor_localization
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 1
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: UCI
year: '2018'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5B62T
- https://archive.ics.uci.edu/dataset/435/ble+rssi+dataset+for+indoor+localization+and+navigation
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 1: a real BLE fingerprinting table with the workbook's temporal call, but only 1,420 labelled readings spread over a grid of locations.
- Source: UCI dataset 435, donated 2018-01-24 by Mehdi Mohammadi and Ala Al-Fuqaha (Western Michigan University), CC BY 4.0; as published: `iBeacon_RSSI_Labeled.csv` with 1,420 rows and `iBeacon_RSSI_Unlabeled.csv` with 5,191 rows, columns `location`, `date` and 13 RSSI columns `b3001`-`b3013` (-200 for out of range); target `location`, a grid cell such as `A01` (10 x 10 ft cells), on the first floor of Waldo Library, read with an iPhone 6S. The record's `year` 2019 was AI-filled; UCI gives 2018 (citation 2017), corrected to 2018.
- Use case: a navigation app places a phone in a building from the beacons it hears; the source names "indoor localization and navigation" but no actor or decision; fit approximate; regime temporal, as the workbook reviewers (Lennart, Andrej) decided, because readings carry timestamps and were taken in sessions (neighbouring readings in time are near copies).
- Siblings and duplicates: `ujiindoorloc_mag` (`No` by Lennart, a magnetic-field time series with its own split, a different task); `mobile_c36_oversampling` mentions indoor localisation, not this data. No duplicate found. External collections: none found.
- Papers and pages: https://archive.ics.uci.edu/dataset/435; Mohammadi et al., "Semi-supervised Deep Reinforcement Learning in Support of IoT and Smart City Services" (arXiv 1810.04118, IEEE IoT Journal 2018), the creators' paper; later uses re-label into four zones (arXiv 2402.11433).
- Metric: none found as a single ranked criterion (UCI page states none; the creators' paper reports localisation accuracy and distance error among several, not read in full), so the fallback (log_loss or roc_auc for multiclass) (MET-1, MET-5).
- Risks for /add-dataset: the number of grid cells against 1,420 rows (likely `Too Small` per class, TP-5; a zone re-labelling would be our own target, USE-5); the unlabeled file is unusable; `date` order must drive the split (SPLIT-6).
- Priority: gap - (technology, temporal not thin), use case - (no actor named), source + (UCI with the creators' paper), shape - (1,420 rows, 13 features, many classes), risk - (Too Small).

UCI BLE RSSI indoor-localization dataset: predict location from Bluetooth Low Energy RSSI fingerprints at fixed reference points. It is a genuine real-world tabular task (RSSI values per beacon as features), already given a TabArena curation verdict of 'Temporal Tabular' with multiple reviewers agreeing on a temporal split. Representative of tabular ML and ethically unambiguous. A human must confirm the exact target formulation (discrete location/zone classification vs continuous coordinates), the cleaned size, and that the noted spatial+temporal structure is handled by the temporal split.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Temporal Tabular.

temporal

Potential issue: spatial and temporal data

Lennart: temporal data

Andrej: temporal split
