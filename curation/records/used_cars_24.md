---
unique_name: used_cars_24
name: Used cars 24
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Missing source information
tags:
- New IID
- Free Text (Short)
- AI-Filled (Verify)
collections:
- CARTE/TARTE
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/avikasliwal/used-cars-price-prediction
- (unsure) https://www.cars24.com/
source_row: 866
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A used-cars price-prediction dataset (Kaggle, possibly from cars24.com) — a standard tabular regression task with several string columns benefiting from preprocessing. The CC comment flags that the source is unclear and the data may be synthetic, which is the main risk; if real it would be a reasonable IID regression dataset. A human must verify the data provenance (genuine scraped listings vs synthetic), size, and whether it duplicates other used-car datasets before promoting it, so a provisional 2nd-tier hold is appropriate.

---

used cars data; many columns that could benefit from string preprocessing; likely synthetic data given the missing source and data state
