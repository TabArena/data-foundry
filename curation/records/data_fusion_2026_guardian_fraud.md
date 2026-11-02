---
unique_name: data_fusion_2026_guardian_fraud
name: 'Data Fusion Contest 2026, Task 1 ''Guardian'': bank operations the client did not confirm (anti-fraud)'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://ods.ai/competitions/data-fusion2026-guardian
- https://ods.ai/competitions/data-fusion2026-guardian/data
- https://www.kaggle.com/datasets/d1ffic00lt/data-fusion-2026-case-1
- https://github.com/alex-dudin/data-fusion-2026-guardian
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the same competition as `data_fusion_2026_guardian` (Data Fusion Contest 2026, Task 1 "Страж", ODS.ai), which was screened from the benchmark tabular-dl-more-data and keeps the task.
- Source: both records end at the organiser's task page https://ods.ai/competitions/data-fusion2026-guardian ("Data Fusion Contest 2026 - Задача 1 "Страж"", 2026-02-09 to 2026-03-30, 1,741 participants, PR-AUC with scikit-learn's `average_precision_score`; read 2026-10-31) and list the same participant re-upload (kaggle.com/datasets/d1ffic00lt/data-fusion-2026-case-1). This record adds the data tab (`/data`) and a public solution (github.com/alex-dudin/data-fusion-2026-guardian), which `data_fusion_2026_guardian` already names in its block.
- Siblings and duplicates: `data_fusion_2026_guardian` (`TBD -> Yes`, priority 3, AI unverified) carries the full screening, the `tabular-dl-more-data` collection and the paper link (arXiv 2610.26794), and its block names this record as the second record of the same competition (PROV-4). Created in this run, this record may instead be renamed `data_fusion_2026_guardian_duplicate` (records.md, "Duplicates and retirements"); the main session's call.
- Better data: from the curator's Zotero collection (item 306); no further search this round.
- Reject check (AI, 2026-10-31): stands. Both records end at the organiser's task page (https://ods.ai/competitions/data-fusion2026-guardian, Task 1 'Страж', 2026-02-09 to 2026-03-30) and list the same Kaggle re-upload. The kept record names this one as its second record. The extra links here (the /data tab, the alex-dudin solution) are a data tab and a solution, not sources. Move them to the kept record.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 306: "Data Fusion Contest 2026 - Задача 1 "Страж" — Open Data Science".
- as published: Operations of 100,000 bank clients from Oct 2023 to Aug 2025, more than 200M in total. Pretrain (Oct 2023 - Sep 2024) is unlabelled. Train (Oct 2024 - May 2025) has 51k 'red' (unconfirmed) and 36k ...; target: red: the bank held an operation for security reasons and the client did not confirm it (binary; PR-AUC); access: registration.
- Why: Real, recent bank operations with client feedback labels, very large, and a scored competition with 1,739 participants and public solutions.
- Adds: An event-level fraud task with device and session telemetry from 2023-2025; our fraud records are mostly card-transaction snapshots. Caveats: per-operation features must be built from the history (Needs extensive data wrangling). Test labels are hidden, so the benchmark would use the train period with its own ...
