---
unique_name: international_womens_day_challenge
name: international-womens-day-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: social science
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/international-womens-day-challenge/data
source_row: 881
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

The target is the percentage of households per ward that are female-headed and earn below R19,600, i.e. an aggregate areal/census regression at ward level rather than individual-record prediction. Aggregated census-ward targets are small in row count and lean toward a descriptive/scientific-discovery framing, which weakens the representative-tabular case. It is a real regression task and not obviously out of scope, so 2nd Tier is appropriate pending checks. A human must verify the number of wards (rows), feature richness, and whether the target/features cause aggregation leakage.

---

predict percentage of households per ward that are both female-headed and earn an annual income that is below R19,600
