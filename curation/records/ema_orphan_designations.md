---
unique_name: ema_orphan_designations
name: EMA Orphan Designations
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.ema.europa.eu/en/medicines/download-medicine-data
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/orphan-designations
- https://arxiv.org/abs/2605.12292
- https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-01):** `TBD -> 2nd Tier`, priority 2: the EMA's register of orphan designations, where STRABLE predicts "Positive" against everything else. Apart from 36 refusals, "Non-Positive" is a designation withdrawn or expired by the download date, a status that grows with the designation's age, so no decision fits it as published (the `ema_medicines` precedent).
- Source: European Medicines Agency, "Download medicine data" (https://www.ema.europa.eu/en/medicines/download-medicine-data), orphan designations table (https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx, "Output automatically generated from content on www.ema.europa.eu", read 2026-11-01): 3,310 designations from 2000 to 2025 with medicine name, related EMA product number, active substance, date of designation or refusal, intended use, EU designation number, status, first published and last updated dates, URL; `Status` Positive 2,201, Withdrawn 985, Expired 88, Negative 36. As used by STRABLE (HF parquet, previewed): 3,083 rows x 10 columns, `Status` binarised to Positive 2,155 against Non-Positive 928.
- Use case: a sponsor or investor could want to know at designation whether a product keeps its designation through to authorisation, but the label is the status on the download day: in STRABLE's cut, designations of 2000-2004 are 72% Non-Positive and those of 2020-2024 9%, since withdrawal and expiry take years (SEL-6). The 36 refusals are the only outcome of the assessment itself, too few for a task (TP-5). Fit none as published, approximate after a re-target with a fixed horizon from the designation date (withdrawn within n years); regime temporal by designation date.
- Siblings and duplicates: `ema_medicines` (`TBD -> 2nd Tier`, priority 2; this table was its second link until 2026-11-01) and `ema_paediatric_investigation_plans` (`TBD -> 2nd Tier`, priority 2): the same EMA page, other tables and tasks (PROV-7). No duplicate (grep for orphan). External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C, "Orphan Designations": "Medicines designated for rare diseases by the EMA. The task is to predict therapeutic area."; its config predicts `Status`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the EMA download page and table; STRABLE (`preprocess_euro-med-agency_orphan_designations.py`, named in the `ema_medicines` block, not read); papers using the table not searched.
- Metric: none found (the EMA publishes tables, no task; STRABLE's AUROC is benchmark-wide, MET-5), so the fallback `roc_auc`; inputs none.
- Risks for /add-dataset: re-target first (USE-5, SEL-6); `Medicine name` and `Related EMA product number` exist only for designations that reached an authorised medicine (271 rows, 260 Positive) and `Last updated date` is missing for 676 rows, 660 of them Positive (LEAK-10, LEAK-13); the EU designation number encodes the year; `Active substance` and `Intended use` are free text; the paper's therapeutic-area task has no column in the table.
- Priority: gap 0 (binary; medical & healthcare not thin), use case 0 (none named), source + (the EMA's official register), shape + (3,310 designations over 25 years; text and dates), risk - (a download-date status; outcome-linked columns).

**Assessment (AI, 2026-11-01):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292) as "Orphan Designations"; split out on 2026-11-01 from `ema_medicines`, which held this table as a second link.
- as published: 3,083 rows x 10 columns incl. target (STRABLE parquet); target: Status.
- Why: Predict whether an EMA orphan designation has a positive status
- Notes: EMA download (orphan_designations.csv). Paper says 'therapeutic area'; config target is Status (binary).
