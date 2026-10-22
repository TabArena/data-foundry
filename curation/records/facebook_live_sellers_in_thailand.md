---
unique_name: facebook_live_sellers_in_thailand
name: Facebook Live Sellers in Thailand
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2019'
domain: social science
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5R60S
source_row: 809
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` (CC line, `TabArena Reject`) stands: the source publishes the data for describing engagement patterns, with no predictive target.
- Source: UCI dataset 488, donated 2019-04-21, 7,051 posts x 11 columns from the Facebook pages of 10 Thai fashion and cosmetics retailers (status type, publish time, counts of reactions, comments, shares, likes, loves, wows, hahas, sads, angrys); introduced by N. Dehouche, "Dataset on usage and engagement patterns for Facebook Live sellers in Thailand", Data in Brief, 2020. UCI lists the associated task as "Clustering" and names no target.
- Use case: none in the source; the CC line's only conceivable task (status type and date to an engagement count) would be engagement prediction, close to SEL-9 and outside what the data was published for (SEL-3, SEL-8). Regime would be temporal (`status_published`).
- Siblings and duplicates: `facebook_comment_volume` is a different dataset (comment-volume regression on other pages). External collections: none checked beyond UCI.
- Metric: none (no task in the source).
- Markers: `No Good Target  / Scientific Discovery` fits UCI's "Clustering"; `Out-of-scope Task (CTR/RecSys/Ranking)` rests on a hypothetical framing, not on the source, and could be dropped; the curator has the call.

UCI dataset of Facebook Live-seller posts (video/photo/status/link) with reaction/engagement counts, published for scientific discovery of engagement patterns rather than a defined predictive task. As the comment notes, the only conceivable target would be mapping status type and date to engagement features, which is essentially an engagement/CTR-style descriptive problem, not a clean tabular classification/regression. It is already a TabArena Reject. Excluded on no-good-target / out-of-scope grounds; a human need only confirm no usable predictive target exists.

---

CC: "Posts of facebook pages (video, photos, statuses, or links); status published is temporal; used for scientific discovery and not predictive task (only real task would be to map for status type and date to any of the reaction features)"

## Reference

Dataset on usage and engagement patterns for Facebook Live sellers in Thailand
By N. Dehouche. 2020

Published in Data in Brief
