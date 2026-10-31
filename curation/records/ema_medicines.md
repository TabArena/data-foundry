---
unique_name: ema_medicines
name: EMA Medicines
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
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/medicines
- https://arxiv.org/abs/2605.12292
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/orphan-designations
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the EMA's public medicines table, with STRABLE's target "authorised now or not". That status mixes refused applications with products withdrawn years after approval, and several inputs are set at or after authorisation. This record also carries STRABLE's orphan-designations table.
- Source: European Medicines Agency, "Download medicine data" (https://www.ema.europa.eu/en/medicines/download-medicine-data): xlsx tables the site "automatically updates ... overnight"; the Medicines table holds "approved medicines, withdrawn applications for new marketing authorisations, and status of opinions", the Orphan designations table the "status of orphan designations following assessment" by the COMP. As published in STRABLE (parquets previewed 2026-10-31): medicines.csv, 2,559 rows x 26 columns (2,197 human, 362 veterinary); target `Medicine status`, which STRABLE binarised (every status other than "Authorised" merged): Authorised 1,757, Not Authorised 802; columns with "Withdrawal", "date" or "Refusal" in their name dropped as leaks. orphan_designations.csv: 3,083 rows x 10 columns, target `Status`, Positive 2,155 and Non-Positive 928 (the paper says the orphan task is "to predict therapeutic area"; the config predicts the status).
- Use case: a sponsor or analyst estimating at submission whether the EU will authorise a medicine is a decision, but the label is the status at the download date, and inputs such as additional monitoring, conditional approval, ATC code and the EPAR indication text come from the authorisation. Fit none as published, approximate after a re-target; regime temporal by application date (dropped by STRABLE).
- Siblings and duplicates: `ema_paediatric_investigation_plans` (the same EMA page, another table and task); `fda_drugs_at_fda` (FDA marketing status) and `fda_device_pma` (FDA PMA decisions), both STRABLE, are the US analogues. The orphan designations are a second task from the same page (PROV-7) and could have their own record. External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "EMA Medicines": "Information on medicines authorized by the European Medicines Agency. The task is to predict authorization status."; "Orphan Designations": "Medicines designated for rare diseases by the EMA. The task is to predict therapeutic area."
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the EMA download page; STRABLE and `preprocess_euro-med-agency_medicines.py`, `preprocess_euro-med-agency_orphan_designations.py`; papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the EMA publishes tables, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: re-target first (USE-5): for example a negative opinion or withdrawn application against a granted authorisation, from the raw table's status and dates; `Opinion status` (98% missing; its 9 negative opinions are all Not Authorised) and `Additional monitoring` (Yes for 352 authorised against 60 not) follow the outcome (LEAK-10); `Medicine URL` and `EMA product number` are ids; in the orphan table `Last updated date` is missing for 676 rows, 660 of them Positive, a recording that follows the label (LEAK-13); human and veterinary medicines in one table.
- Priority: gap 0 (medical & healthcare, binary not thin), use case 0, source + (the EMA's official tables), shape + (2,559 medicines, 25 inputs, mixed), risk - (a download-date status mixing refusals and later withdrawals; post-authorisation inputs).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 2,559 rows x 26 columns incl. target (STRABLE parquet); target: Medicine status.
- Why: Predict whether a medicine assessed by the EMA is authorised | Predict whether an EMA orphan designation has a positive status
- Notes: EMA medicines download (medicines.csv). | EMA download (orphan_designations.csv). Paper says 'therapeutic area'; config target is Status (binary).

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: STRABLE's orphan-designations table is inside this record and may need its own.
