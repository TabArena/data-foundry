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

**Assessment (AI, 2026-10-22):** the workbook's `No` (Lennart and Andrej: Audio) holds under SEL-12 and SEL-13; recommend adding `Duplicate` as well: this is the same UCI dataset as `geographical_origin_of_music` (Lennart, `No`), here under its PMLB name. The curator has the call.
- Source: UCI 315 "Geographical Original of Music", donated 2014-10-17, DOI 10.24432/C5VK5D; as published: 1,059 tracks of traditional and world music from 33 countries or areas, 68 MARSYAS timbre features (a second file adds chroma features), targets latitude and longitude of the capital of the country of origin. UCI: "The program MARSYAS was used to extract audio features from the wave files" and "All features were transformed to have a mean of 0, and a standard deviation of 1".
- Use case: none named; the source states the task ("predict the geographical origin of music") as a music-information-retrieval question, with no actor or decision; regime IID if it were kept.
- Siblings and duplicates: `geographical_origin_of_music` (OpenML 44965 and the same UCI DOI; Lennart: `No`, `Wrong Domain / Source Modality`, `Time-series (Classification)`), whose comment points to PMLB `4544_GeographicalOriginalofMusic`, the name of this record. External collections: PMLB; TabSTAR (on the sibling).
- Metric: not looked up (the verdict is `No`).
- Risks for /add-dataset: none to pass on; features computed from audio describe the recording's content (SEL-12, SEL-13), and they were scaled over all rows (LEAK-30).
- Priority: none (verdict `No`).

UCI 'Geographical Original of Music' dataset consisting of audio features extracted from 1059 wave files, with the goal of predicting geographic origin (lat/long). Prior TabArena curation and both reviewers (Lennart, Andrej) flagged it as Audio. It is a non-tabular (audio) modality recast as engineered features, where audio models would dominate, so it is not representative tabular ML. Confidently No on the audio-modality exclusion.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Audio.

audio features extracted from 1059 wave files

Lennart: Audio

Andrej: Audio
