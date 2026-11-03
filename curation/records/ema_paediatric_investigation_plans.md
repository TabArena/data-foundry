---
unique_name: ema_paediatric_investigation_plans
name: Paediatric Investigation Plan
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
original_data_state: One Table
source_links:
- https://www.ema.europa.eu/en/medicines/download-medicine-data
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/paediatric-investigation-plan
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: EMA decisions on paediatric investigation plans. Three of STRABLE's four classes name the procedure the sponsor applied for, which the sponsor already knows; only "refusal" is an outcome (72 of 3,056).
- Source: European Medicines Agency, "Download medicine data" (https://www.ema.europa.eu/en/medicines/download-medicine-data), table "Paediatric investigation plans: decisions following evaluation by the Paediatric Committee (PDCO)". As published in STRABLE (paediatric_investigation_plans.csv; parquet previewed 2026-10-31): 3,056 rows x 16 columns, one EMA decision per row, 2007-2024; target `Decision type`: "W: decision granting a waiver in all age groups for all conditions or indications" 1,246; "PM: decision on the application for modification of an agreed PIP" 977; "P: decision agreeing on a investigation plan, with or without partial waiver(s) and or deferral(s)" 761; "R: decision refers to a refusal" 72.
- Use case: the sponsor knows whether it asked for a full waiver, a plan or a modification, so W, P and PM are no prediction (USE-2, as SEL-7 for a label the subject already knows); a sponsor estimating whether the PDCO will refuse its application is a decision (binary, 72 refusals, 2.4%). Fit none as published, approximate after that re-target; regime temporal by decision date.
- Measured on the preview: 941 of the 977 PM rows carry a "-M<n>" suffix in `PIP number` (a modification), against 28 of the 1,246 W rows, so the id gives the class away.
- Siblings and duplicates: `ema_medicines` (the same EMA page, another table and task); `fda_device_pma` (FDA decision codes, STRABLE) is the closest analogue. External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "Paediatric Investigation Plan": "Research plans for the use of medicines in children. The task is to predict investigation status."
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the EMA download page; STRABLE's processed folder `paediatric-investigation-plan` (no preprocessing script found in github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the EMA publishes tables, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `log_loss` for the four classes or `roc_auc` for the refusal framing (MET-8); inputs none.
- Risks for /add-dataset: the target (USE-5, USE-2) as above; `PIP number` and `Decision number` encode the procedure and the date (LEAK); `Compliance opinion date` and `Compliance procedure number` (89% missing) exist only after a plan is agreed and checked (LEAK-10); 72 refusals give about 14 per test fold in five folds (TP-5, TP-8); `Contact for public enquiries` holds phone numbers and e-mail addresses (no feature).
- Priority: gap 0 (the multiclass framing is the application type; the task that could ship is the binary refusal, not thin), use case 0, source + (the EMA's official table), shape + (3,056 decisions over 17 years, mixed), risk - (the label is mostly the application type).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 3,056 rows x 16 columns incl. target (STRABLE parquet); target: Decision type.
- Why: Predict the EMA decision type on a paediatric investigation plan
- Notes: EMA download (paediatric_investigation_plans.csv).
