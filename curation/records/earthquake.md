---
unique_name: earthquake
name: earthquake
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Time-series (Forecasting)
- Duplicate
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '2023'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/alessandrolobello/the-ultimate-earthquake-dataset-from-1990-2023
- http://www.stern.nyu.edu/SOR/SmoothMeth
source_row: 803
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Kaggle compilation of global earthquakes 1990-2023 (date, location, depth, magnitude). It has no well-defined supervised target: magnitude/occurrence prediction is a temporal forecasting / scientific-discovery problem rather than a fixed IID tabular task, and it is already tagged TabArena Reject / 2nd Tier. The record also notes it relates to OpenML d/550, suggesting overlap with existing data. Excluded as a forecasting / no-good-target scientific catalogue; a human need only confirm there is no extractable fixed classification/regression target before final rejection.

---

Unsure if a real task, or how it could be used. However, we can still take a look at it

Related/based on openml.org/d/550
