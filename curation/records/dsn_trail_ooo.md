---
unique_name: dsn_trail_ooo
name: dsn-trail-ooo
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
- https://zindi.africa/competitions/dsn-trail-ooo/data
source_row: 958
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): "TRAIL OOU X DSN DATA SCIENCE TRAINING" (Zindi, 2 Apr - 3 May 2024, https://zindi.africa/competitions/dsn-trail-ooo, 44 participants, run by Olabisi Onabanjo University's TRAIL initiative with Data Science Nigeria) re-uses the data of the "DSN AI Bootcamp Qualification Hackathon" (Zindi, 9 Sep - 3 Oct 2020, https://zindi.africa/competitions/dsn-ai-bootcamp-qualification-hackathon), recorded as `dsn_ai_bootcamp_qualification_hackathon_by_data_science_nigeria` (`TBD -> Yes`).
- Source: Zindi's competition API names the 2020 hackathon as this competition's `parent`; both pages carry the same Kowope Mart / DSBank description and the same Data Description ("The data sample has been split into train and test with a volume of 56,000 and 24,000", `form_field1` ... `form_field50`, target `default_status`), and the same files: Train.csv 18,065,184 bytes, Test.csv 7,668,359, SampleSubmission.csv 378,110 in both.
- Metric: both score Area Under the Curve ("The error metric is Area Under the Curve", Evaluation tab).
- The task stays in the benchmark through the 2020 record; nothing here adds a distinct task (PROV-6).
- Reject check (AI, 2026-10-22): stands. Zindi API: parent = dsn-ai-bootcamp-qualification-hackathon (2020). The files are byte-identical in size: Train 18,065,184 / Test 7,668,359 / SampleSubmission 378,110. The task is kept in dsn_ai_bootcamp_qualification_hackathon_by_data_science_nigeria (PROV-4).

Zindi 'dsn-trail-ooo' competition with an empty record (only the link is present). The name is opaque and there is no description of the task, target, or data. Data Science Nigeria / Zindi competitions are usually legitimate tabular predictive tasks, so it should not be rejected solely for missing detail. A human must inspect the competition page and data to establish whether it is a real tabular classification/regression task, its size, target, and split regime.
