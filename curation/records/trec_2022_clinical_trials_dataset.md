---
unique_name: trec_2022_clinical_trials_dataset
name: TREC 2022 Clinical Trials Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
- NLP (Text)
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2022'
domain: medical & healthcare
problem_type: Other
original_data_state: Other
source_links:
- https://catalog.data.gov/dataset/trec-2022-clinical-trials-dataset
source_row: 837
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9; `NLP (Text)`, SEL-12): the TREC 2022 Clinical Trials track, a retrieval task that ranks trials for free-text patient cases.
- Source: NIST, TREC 2022 Clinical Trials track (data.gov entry; trec-cds.org/2022.html): "given a free text summary of a patient health record, find suitable clinical trials for that patient". As published: 50 topics, each "a lengthy (5-10 sentence) patient case description", "synthetic patient cases created by individuals with medical training"; the corpus is an April 2021 snapshot of ClinicalTrials.gov in XML; qrels from physicians who judge each pooled trial eligible, excluded or not relevant.
- Use case: trial matching for a patient, solved as retrieval: systems return a ranked list of up to 1,000 trial IDs per topic. No tabular table and no per-row target (the qrels label topic-trial pairs from pooled runs).
- Siblings and duplicates: `clinical_trials` and `covid_trials` are other trial-registry records (different data); no duplicate.
- Metric: NDCG over the ranked list ("the performance of the retrieval submissions will be measured using normalized discounted cumulative gain").
- Reject check (AI, 2026-10-22): stands. SEL-9 (Must): trec-cds.org/2022.html: "Participants of the track will be challenged with retrieving clinical trials from ClinicalTrials.gov", runs are "a ranked list of up to one thousand IDs", "measured using normalized discounted cumulative gain (NDCG)"; topics are free-text synthetic admission notes (SEL-12). An IR ranking task on text with no row-level target.

The TREC 2022 Clinical Trials track is an information-retrieval / ranking task: given a patient case description (free text), rank/match eligible clinical trials. This is a text-based IR/ranking problem, not an IID/temporal/grouped tabular predictive classification or regression task. It falls under out-of-scope (ranking/IR) and NLP. No clear tabular target exists, so this should be rejected.
