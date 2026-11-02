---
unique_name: ai_national_summit_2024_competition
name: ai-national-summit-2024-competition
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/ai-national-summit-2024-competition/data
- https://zindi.africa/competitions/indabax-rwanda-2024-hacktathon
source_row: 965
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a re-hosting of the cryptojacking detection data of "UmojaHack Africa 2023: Cryptojacking Detection Challenge (INTERMEDIATE)", recorded as `umojahack_africa_2023_intermediate_challenge`.
- Source: Zindi hackathon "AI National Summit 2024 Competition", 2024-06-08, Tunisia (IEEE INSAT), 47 participants; parent `umojahack-africa-2023-intermediate-challenge` (2023-03-18, 435 participants) per the Zindi API; the second link, "IndabaX Rwanda 2024 Hackathon" (2024-06-21), has the same parent and text. As published: "~4 000 recordings in test and ~9 000 readings in train", network- and host-based features of website activity, label cryptojacking or not; the data "was originally collected by researchers from Instituto Politecnico Nacional" (the first publication is that group's paper, a question for the parent record).
- Siblings and duplicates: `umojahack_africa_2023_intermediate_challenge` (`TBD -> 2nd Tier`) holds the parent; all three pages share the Data Description word for word.
- Metric: F1 on hard labels (Zindi Evaluation page), as in the parent.
- Recommend: move both links to the parent's `source_links`.
- Reject check (AI, 2026-10-22): stands. PROV-4. Both linked pages (AI National Summit 2024, IndabaX Rwanda 2024) have API parent umojahack-africa-2023-intermediate-challenge. Data Description and Evaluation are identical to the parent (ratio 1.0): "~4 000 recordings in test and ~9 000 readings in train". Same files, F1. The parent record umojahack_africa_2023_intermediate_challenge is kept (TBD -> 2nd Tier). https://zindi.africa/competitions/ai-national-summit-2024-competition

A 2024 Zindi summit/hackathon competition (also linked to an IndabaX Rwanda hackathon) with no comments or metadata describing the task. There is no information on the target, modality, domain, or size, and summit hackathons are commonly toy/educational. The guidelines advise against rejecting purely for lack of info. A human must open the source pages to establish the predictive task, modality, size, and provenance, and check whether the two linked competitions are duplicates.
