---
unique_name: agile_bridge_beginners
name: agile-bridge-beginners
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
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/agile-bridge-beginners/data
source_row: 969
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a private one-day re-hosting of Zindi's "Financial Inclusion in Africa" (2019) for Agile Bridge users, with the parent's data and metric.
- Source: Zindi hackathon `agile-bridge-beginners`, titled "Financial Inclusion in Africa", 2023-02-03, "a private hackathon only open to Agile Bridge users"; the Zindi API names its parent `indabax-togo-2022`; first publication of the data: Zindi "Financial Inclusion in Africa" (https://zindi.africa/competitions/financial-inclusion-in-africa, opened 2019-07-29, 10,679 participants). As published: Train.csv, Test.csv, VariableDefinitions.csv; "approximately 33,600 individuals" from the FinScope and FinAccess surveys of Kenya 2018, Rwanda 2016, Tanzania 2017 and Uganda 2018; target `bank_account` (Yes = 1, No = 0).
- Use case: the parent's (predict who has or uses a bank account); nothing new here.
- Siblings and duplicates: `financial_inclusion_in_africa_for_botswana` (`TBD -> Yes`, `Duplicate`) carries the same data and lists eight more re-hostings; no record holds the 2019 parent itself under its own slug. The Data Description and Evaluation text of this page match the 2019 parent word for word.
- Metric: Mean Absolute Error on the 0/1 label (Zindi Evaluation page), as in the parent.
- Recommend: add https://zindi.africa/competitions/agile-bridge-beginners to the canonical Financial Inclusion record's `source_links` and settle which record is canonical.
- Reject check (AI, 2026-10-22): stands. PROV-4/PROV-5. The Zindi API names the parent indabax-togo-2022, titled "Financial Inclusion in Africa". The Data Description is 94% identical to the 2019 original (https://zindi.africa/competitions/financial-inclusion-in-africa): "approximately 33,600 individuals ... Finscope surveys ranging from 2016 to 2018". Same files and the same MAE metric. The original is kept: its link is in financial_inclusion_in_africa_for_botswana (TBD -> Yes). https://zindi.africa/competitions/agile-bridge-beginners

A Zindi 'agile-bridge-beginners' competition with no comments, description, target, or domain in the record. There is essentially no information to assess scope, modality, or task type, and the 'beginners' framing suggests it may be a tutorial/toy dataset. Per the guidelines, insufficient info alone should not force a hard reject. A human must open the competition page to determine the actual target, modality, size, and whether the data is real or synthetic before any decision.
