---
unique_name: data_wave_competition_lab
name: data-wave-competition-lab
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
- https://zindi.africa/competitions/data-wave-competition-lab/data
source_row: 951
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`; PROV-4, PROV-6): a one-day rerun of Ghana's Indigenous Intel Challenge on the same Smart Indigenous Weather App data and task, recorded as `ghanas_indigenous_intel` (No (Retired), Andrej; Too Small, Data Quality Issue).
- Source: Zindi hackathon "Data Wave - Competition Lab" (2025-11-29, 08:00 to 14:45 UTC, secret code required, 500 Zindi points; read through the Zindi API, https://zindi.africa/competitions/data-wave-competition-lab). Its data files include `ghana-indigenous-intel-challenge20250815-4756-1bz0qx9.zip`, the archive of the parent challenge (https://zindi.africa/competitions/ghana-indigenous-intel-challenge, started 2025-08-14), next to `train.csv`, `test.csv`, `SampleSubmission.csv` and `Indigenous_Weather_Forecasting-Starter_Notebook.ipynb`.
- Same data and task: "The data for this challenge was collected using the Smart Indigenous Weather App ... Data was collected from local farmers in the Pra River Basin of Ghana"; "Your task is to build a classification model that predicts the type of rainfall—heavy, moderate, or small—expected in the next 12 to 24 hours, based solely on indigenous ecological indicators submitted by trained farmers" (Description and Data Description pages), hosted by RAIL at KNUST: the parent challenge's description, data and target.
- Metric: F1 Score (Evaluation page). The page says the variables "were and continue to be collected", so the rerun may carry more rows; added rows of the same collection and task are a version, not a distinct task (PROV-6). If it does carry many more farmer-days, that bears on the sibling's `Too Small`, not on a second record.
- Siblings: `ghanas_indigenous_intel` (CC 2026-10-01, Lennart: retired for Too Small and a likely censoring bias in the rain-gauge label; "Revisit if a cleaner or larger release appears"). A later rerun exists too (`ghana-indigenous-intel-challenge-cameroon-community-hack`, 2026-10-26).
- Reject check (AI, 2026-10-22): stands. PROV-4/PROV-6 (Must), source confirmed (PROV-5). The Zindi API names ghana-indigenous-intel-challenge as this hackathon's parent, and every data file is byte-identical in size to the parent's (train.csv 870,530; test.csv 202,185; SampleSubmission.csv 60,111; the parent's zip ghana-indigenous-intel-challenge20250815-4756-1bz0qx9.zip 186,984), with the same description, data description and F1 metric (https://api.zindi.world/v1/competitions/data-wave-competition-lab vs .../ghana-indigenous-intel-challenge). Same data, same task: a duplicate of ghanas_indigenous_intel (No (Retired)). The screener's open question about added rows is settled: there are none.

Zindi 'data-wave-competition-lab' with no description, comments, or metadata in the record, so the task type, target, domain, size, and modality are all unknown. Per the instructions, too little information is not by itself grounds for rejection. The only signal is that it is a Zindi competition (often genuine African real-world tabular tasks, but also sometimes image/forecasting). A human must open the competition page to determine the task, target, data modality, size, and split before any verdict.
