---
unique_name: valuation
name: Valuation
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
- Needs extensive data wrangling
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: finance
required_split:
- Custom
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://catalog.data.gov/dataset/property-valuation-and-assessment-data-db7c2
source_row: 830
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

NYC property valuation and assessment data (data.gov) — essentially a government SQL dump with geospatial and text fields and no clean predictive task out of the box. The CC comment notes that assessed value may follow a fixed formula or come from a third party, and that extensive expert feature engineering plus multi-year collection would be needed to build a sound dataset. It is potentially salvageable into a property-value regression task but requires substantial wrangling and leakage checks, so a provisional 2nd-tier hold is appropriate pending human inspection of the target and feature provenance.

---

CC: "GOV data without a real predictive task; full evaluation either depends on a clear formula from the GOV or is given by some third party. Has geospatial data; temporal impact on price; requires a lot of expert feature engineering to make it work; basically just a SQL dump but not a real dataset yet; maybe not a lot of temporal leakage as it is just one year; could collect data from prior years as well and filter it to a good dataset etc"

Also includes text otherwise
