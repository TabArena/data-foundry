---
unique_name: digital_green_crop_yield_estimate_challenge
name: digital-green-crop-yield-estimate-challenge
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
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/digital-green-crop-yield-estimate-challenge/data
source_row: 893
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi 'Digital Green Crop Yield Estimate Challenge' to predict per-acre rice/wheat yield in India from farm survey data, a continuous regression target. It is a plausible real-world tabular regression, but the curator frames it as survey-based 'predictive discovery' and yield prediction can blur into agronomic estimation; a grouped split (by farm/region) may be needed. It maps to the criteria reasonably but with caveats about target quality and representativeness. A human must verify the data is one tabular file (not satellite imagery), the size, the exact yield target, and the appropriate split; 2nd Tier for now.

---

predict the crop yield per acre of rice or wheat crops in India

Survey data, I'd say it should rather be a predictive discovery task
