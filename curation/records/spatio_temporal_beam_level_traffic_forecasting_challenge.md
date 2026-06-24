---
unique_name: spatio_temporal_beam_level_traffic_forecasting_challenge
name: spatio-temporal-beam-level-traffic-forecasting-challenge
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
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/spatio-temporal-beam-level-traffic-forecasting-challenge/data
source_row: 886
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Zindi challenge to forecast spatio-temporal beam-level cellular traffic. The name and the comment ('time-series') make clear this is forecasting future traffic over a horizon, which is explicitly out of scope for the benchmark even though the winning solution used tree models. The forecasting setup (predicting future values per beam/time) is not a fixed predictive task that merely needs a temporal split. Recommend reject; a human could confirm there is no reframable fixed-target variant.

---

time-series, but 1st place solution uses tree-based models
