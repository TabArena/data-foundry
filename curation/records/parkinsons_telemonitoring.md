---
unique_name: parkinsons_telemonitoring
name: Parkinsons_Telemonitoring
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
original_source: UCI
year: '2009'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5ZS3N
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

UCI Parkinsons telemonitoring data consisting of voice/dysphonia measurements from 42 patients used to predict UPDRS scores. Multiple curators (TabArena verdict, Lennart, Andrej) classified it as audio-derived data. As a voice/audio-signal dataset (with grouping by patient) it is not representative tabular ML and falls under wrong source modality. Suggest No; consistent with prior verdicts, though the features are engineered acoustic measures a human could re-examine.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Audio.

voice measurements from 42 people

Lennart: Audio data

Andrej: Audio
