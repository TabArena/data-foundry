---
unique_name: mental_health_dataset
name: Mental Health Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Missing source information
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
- TabSTAR
domain: medical & healthcare
required_split:
- '?'
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset/
- https://www.openml.org/search?type=data&id=46721&sort=runs&status=active
source_row: 827
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Missing source information`, PROV-1): an anonymous Kaggle upload whose own description does not describe its file, with no traceable upstream.
- Source: Kaggle bhavikjikadara/mental-health-dataset, one file `Mental Health Dataset.csv` (31 MB, 2024-03-18), CC BY 4.0. Re-served as OpenML 46721 (292,364 rows x 17, default target `Occupation`). The uploader's description hedges and describes other data: "This dataset appears to contain a variety of features related to text analysis, sentiment analysis, and psychological indicators, likely derived from posts or text data. Some features include readability indices such as Automated Readability Index (ARI) ... sentiment compound". The file has none of these. Its 17 columns are survey items (`Timestamp, Gender, Country, Occupation, self_employed, family_history, treatment, Days_Indoors, Growing_Stress, Changes_Habits, Mental_Health_History, Mood_Swings, Coping_Struggles, Work_Interest, Social_Weakness, mental_health_interview, care_options`, OpenML feature list). Several of them match the OSMI 2014 tech survey (`mental_health_tech`, 1,259 respondents), which this table exceeds by more than 200 times. The only provenance is "I collected this dataset from the internet", with a link to the OurWorldInData mental-health page (quoted in the curator note below), which publishes country aggregates, not respondents.
- Use case: none; the curator note calls it a discovery table without a clear target, and the OpenML target `Occupation` is no decision.
- Siblings and duplicates: `mental_health_tech` (OSMI survey, `TBD -> 2nd Tier`, Lennart: "no ground truth or objective target"), `busara_mental_health_prediction_challenge`. External collections: TabSTAR (via OpenML 46721).
- Metric: none.
- Also weighed: the row count far above any survey these items come from suggests generated or expanded rows (PROV-3, not tested here).
- Reject check (AI, 2026-10-22): stands. Fails PROV-3 on the data itself, beyond PROV-1: OpenML 46721 (same file as the Kaggle upload, https://www.openml.org/d/46721) has 292,364 rows on only 580 distinct Timestamps, all 8/27/2014-era OSMI survey times, at least 390 rows per timestamp, and 194,641 rows duplicate another once Timestamp is dropped: an expansion of the OSMI 2014 survey (1,259 respondents), not respondents. The description describes other data (readability and sentiment features) and the curator CC finds no target. Add AHDS (SEL-16) to Missing source information; PROV-2's keep needs data that passes PROV-3, which this does not.

A Kaggle/OpenML mental-health dataset (d/46721) the curator describes as parsed from text for scientific discovery, with no clear predictive target and ambiguous provenance ('collected from the internet', linked to OurWorldInData). The record already carries Missing source information and No Good Target markers. It is not a genuine deployed predictive task and provenance is unclear, both disqualifying. A human could revisit if a concrete, well-sourced target emerges, but as presented this is a No.

---

CC: "This is a dataset for scientific discovery that was generated from parsing text. It is unclear how to select a good target for this dataset.

It is not a real predictive ML task, but might be a good proxy. At the same time, all the features are two-step, and it is unclear how this relates to a real use case.

"I collected this dataset from the internet." -> https://ourworldindata.org/mental-health"
