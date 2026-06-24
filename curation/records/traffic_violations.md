---
unique_name: traffic_violations
name: Traffic_violations
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '2015'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.openml.org/d/42345
- https://catalog.data.gov/dataset/traffic-violations
- https://www.kaggle.com/datasets/nikhil1e9/traffic-violations
source_row: 846
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Maryland traffic-violations log (~1.5-2M rows) with spatial and temporal fields, available on OpenML/data.gov/Kaggle. The data is large and genuinely tabular, but the CC comment flags that it may simply have been crawled because it is available and may not correspond to a meaningful predictive task; columns like violation type, race, gender, or fine could each be a target. It carries TabArena Reject and 2nd Tier/Scientific Discovery tags. A human must define a non-arbitrary target, confirm a sensible temporal split, and check for leakage and ethical concerns (race/demographic fields), so a provisional 2nd-tier hold is appropriate.

---

CC: "Large scale, spatial, and temporal. Need to think about split. Also unsure whether this data was simply crawled because it's available but does not correspond to a meaningful task. Not much information is given on OpenML. 1.5M samples originally; now has 2M"
