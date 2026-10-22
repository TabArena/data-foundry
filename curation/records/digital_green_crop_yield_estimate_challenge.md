---
unique_name: digital_green_crop_yield_estimate_challenge
name: digital-green-crop-yield-estimate-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
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

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a real survey of Indian smallholder farms with a yield target, but the survey records the season after harvest, so the use case is a look back unless the post-harvest columns go; the curator's note below calls it predictive discovery.
- Source: Zindi "Digital Green Crop Yield Estimate Challenge", 4 September 2023, data collected by Digital Green, supported by GIZ's FAIR Forward (https://zindi.africa/competitions/digital-green-crop-yield-estimate-challenge); as published: "more than 5000 data points, each having more than 40 features", "collected through a survey conducted across multiple districts in India", Train.csv (1.6 MB, about 75%), Test.csv, VariableDescription.csv; target `Yield` per acre ("rice or wheat" in the description, rice in the data description).
- Use case: the page says yield predictions "empower smallholder farmers to make informed planting and resource allocation decisions"; that needs only what is known at planting, while the survey (from memory of the files, to verify) holds harvest and threshing dates, harvest method and residue columns: fit approximate; regime grouped by district or block would mirror a new area, else IID; temporal if the sowing dates span several seasons.
- Siblings and duplicates: none found in `curation/records/` (no other Digital Green record). External collections: none found.
- Papers and pages: no paper; competition page and variable description only; top solutions not read (the forum reports extreme yield outliers, unverified).
- Metric: RMSE, Zindi Evaluation page ("The evaluation metric for this competition is Root Mean Squared Error"); a leaderboard choice (MET-4); inputs none.
- Risks for /add-dataset: post-harvest columns (LEAK: drop to a planting-time task, USE-1); outliers or unit errors in `Yield` and `Acre` (CLEAN); SEL-3 doubt raised by the curator's note.
- Priority: gap 0 (environmental science & climate, regression, IID not thin), use case 0 (approximate), source + (Digital Green named, a codebook ships), shape + (about 5,000 farms, 40+ mixed columns), risk - (post-harvest columns, outliers): 2.

Zindi 'Digital Green Crop Yield Estimate Challenge' to predict per-acre rice/wheat yield in India from farm survey data, a continuous regression target. It is a plausible real-world tabular regression, but the curator frames it as survey-based 'predictive discovery' and yield prediction can blur into agronomic estimation; a grouped split (by farm/region) may be needed. It maps to the criteria reasonably but with caveats about target quality and representativeness. A human must verify the data is one tabular file (not satellite imagery), the size, the exact yield target, and the appropriate split; 2nd Tier for now.

---

predict the crop yield per acre of rice or wheat crops in India

Survey data, I'd say it should rather be a predictive discovery task
