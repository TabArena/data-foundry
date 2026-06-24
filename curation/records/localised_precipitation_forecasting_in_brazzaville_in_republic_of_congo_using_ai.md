---
unique_name: localised_precipitation_forecasting_in_brazzaville_in_republic_of_congo_using_ai
name: localised-precipitation-forecasting-in-brazzaville-in-republic-of-congo-using-ai
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/localised-precipitation-forecasting-in-brazzaville-in-republic-of-congo-using-ai
source_row: 948
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Zindi competition whose name explicitly states localised precipitation forecasting for Brazzaville. Forecasting future precipitation values over a horizon is time-series forecasting, which is explicitly excluded from the benchmark scope. The name alone strongly signals a forecasting task rather than a fixed predictive task that merely needs a temporal split. A human could double-check whether it is framed as nowcasting from concurrent features (which might change the verdict), but on the name and typical framing this is a No.
