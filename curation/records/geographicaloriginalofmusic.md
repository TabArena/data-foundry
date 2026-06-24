---
unique_name: geographicaloriginalofmusic
name: GeographicalOriginalofMusic
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
original_source: UCI
domain: Multimedia (from non-tabular modalities)
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/315/geographical+original+of+music
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

UCI 'Geographical Original of Music' dataset consisting of audio features extracted from 1059 wave files, with the goal of predicting geographic origin (lat/long). Prior TabArena curation and both reviewers (Lennart, Andrej) flagged it as Audio. It is a non-tabular (audio) modality recast as engineered features, where audio models would dominate, so it is not representative tabular ML. Confidently No on the audio-modality exclusion.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Audio.

audio features extracted from 1059 wave files

Lennart: Audio

Andrej: Audio
