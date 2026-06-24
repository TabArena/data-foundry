---
unique_name: faulty_air_quality_sensor_challenge
name: Faulty Air Quality Sensor Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: industry & manufacturing
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/umojahack-africa-2022-beginner-challenge/data
source_row: 1009
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi UmojaHack 2022 beginner challenge: classify whether an air-quality sensor/device is faulty from its output data. This is a plausible real-world binary classification task in the industry/IoT domain. The key risk is that the sensor outputs are time-stamped readings, which could make this a per-device grouped or temporal problem (or even a time-series classification) rather than IID, and beginner-track data may be small. A human must inspect the data to confirm the feature structure, target balance, dataset size, and whether a grouped/temporal split is required.

---

Classify if a device is faulty based on its output data
