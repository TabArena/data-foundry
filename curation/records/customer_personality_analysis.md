---
unique_name: customer_personality_analysis
name: Customer_Personality_Analysis
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
- Missing source information
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2021'
domain: business & marketing
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis/data
source_row: 812
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Well-known Kaggle 'Customer Personality Analysis' marketing dataset (~2240 rows, demographics, spend, campaign-response columns). It was published primarily as a segmentation/clustering exercise rather than a clean supervised task; the only natural target is the binary 'Response' (accepted last campaign), but as the curator notes the collection timing is unclear, raising leakage/temporal concerns. Source provenance is also fuzzy (single Kaggle re-upload, no original company). Maps weakly to criteria 1-2 and questionably to criterion 3. A human should verify whether 'Response' is a leak-free target, the true source, and the post-cleaning size before promoting; tentatively 2nd Tier.

---

CC: "Looks like a nice dataset, but source is not entirely clear to me. Also might be more a clustering task than predictive task? - could make it a predictive task using the following feature as target: Response: 1 if customer accepted the offer in the last campaign, 0 otherwise. However, we don't know enough about the time when the features were collected, so rather not use this task"

## Reference

Kaggle
