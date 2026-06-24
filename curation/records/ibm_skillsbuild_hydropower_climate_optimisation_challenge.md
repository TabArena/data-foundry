---
unique_name: ibm_skillsbuild_hydropower_climate_optimisation_challenge
name: ibm-skillsbuild-hydropower-climate-optimisation-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://zindi.africa/competitions/ibm-skillsbuild-hydropower-climate-optimisation-challenge/data
source_row: 871
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi IBM SkillsBuild hydropower/climate challenge, flagged as time-series but with a note that the winning solution was tabular. The framing (predicting/optimizing hydropower output from climate inputs over time) leans toward forecasting, which is out of scope, yet the tabular winning approach suggests it might be reframable as a fixed predictive regression with a temporal split. It likely needs substantial wrangling of climate/operational data. A human must determine whether the target is a genuine static prediction vs. a horizon forecast and assess data size/quality; keep in 2nd tier pending that.

---

time-series, but the 1st place solution is tabular
