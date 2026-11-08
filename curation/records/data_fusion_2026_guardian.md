---
unique_name: data_fusion_2026_guardian
name: Bank Fraud (Bank Fraud Datafusion)
checked_by:
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- tabular-dl-more-data
original_source: Other
year: '2026'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://ods.ai/competitions/data-fusion2026-guardian
- https://arxiv.org/abs/2610.26794
- https://ods.ai/competitions/data-fusion2026-guardian/dataset
- '# a participant''s re-upload of the competition files (Kaggle, licence ''other''), with the column dictionary'
- https://www.kaggle.com/datasets/d1ffic00lt/data-fusion-2026-case-1
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a recent, very large bank anti-fraud task (operations held for security reasons that the client did not confirm), scored by the organiser with PR-AUC; the per-operation features have to be built from each client's history, and the same competition has a second record.
- Source: Data Fusion Contest 2026, Task 1 "Страж" (Guardian), on ODS.ai, 2026-02-09 to 2026-03-30 (1,741 participants, 9,507 submissions; the task page does not name the bank). Task page: "Необходимо решить задачу классификации для операций, которые по различным причинам, связанных с безопасностью, были не подтверждены клиентами банка" (classify the operations that, for security reasons, the bank's clients did not confirm). As published: operations of 100,000 clients over about 1.5 years, more than 200M operations; pretrain 2023-10-01 to 2024-09-30 (unlabelled), train 2024-10-01 to 2025-05-31 (labelled: about 51k red and 36k yellow operations), pre-test and test 2025-06-01 to 2025-08-09 (633,683 operations to score, labels hidden). Files (listed on a participant's Kaggle re-upload, read 2026-10-31): pretrain_part_1..3, train_part_1..3, pretest and test (parquet) and train_labels.parquet; 23 columns per operation (customer_id, event_id, event_dttm, event type, coded event description, channel and subchannel, amount in roubles, currency, MCC group, coded POS condition, accept and browser language, timezone, session_id, coded OS, battery, OS version, screen size, developer-tools flag, VoIP call during the operation, remote-desktop flag, root access). Target: red (held, not confirmed by the client) = 1; yellow (suspicious, confirmed by the client) and every operation without feedback = 0 ("Все остальные операции без обратной связи клиента стоит считать подтвержденными").
- Use case: the bank's anti-fraud system scores each operation as it happens and holds the risky ones for the client's confirmation; fit direct for the operations the bank sees; regime temporal: the source splits by period and the same 100,000 clients appear in every period, so known clients are scored on later operations (USE-10).
- Siblings and duplicates: `data_fusion_2026_guardian_fraud` is the same competition (created the same day from the curator's Zotero collection; screen batch 61): one of the two should become `No` + `Duplicate` (PROV-4), the kept one carrying `tabular-dl-more-data` in its collections (the main session's call). Closest precedents: `alfa_battle_2_0_task_1` and `alfa_battle_2_0_task_2` (Alfa-Bank transaction-history contests, task 2 `Yes`) for features built from a client's history, `ieee_fraud_detection` (`Yes`) for the fraud task. External collections: tabular-dl-more-data (Rubachev, Lazarev, Babenko 2026, arXiv 2610.26794, "Bank Fraud": 10.97M train / 591K validation / 590K test, 119 features built from the logs "following public solutions", negatives sampled at 15% for training, the last two two-week periods of the labelled train period as validation and test, average precision).
- Better data: a candidate of the benchmark tabular-dl-more-data; no further search this round.
- Papers and pages: the task page (https://ods.ai/competitions/data-fusion2026-guardian; the data tab is open to registered participants only); Rubachev et al. 2026; a public solution (github.com/alex-dudin/data-fusion-2026-guardian: a sequence model over the client's history with optional "session/future/label-history" signals and heads for red, suspicious and red-vs-yellow).
- Metric: PR-AUC over operations, computed with sklearn's `average_precision_score` (the task page); the competition's metric, deliberate (MET-4); inputs none.
- Risks for /add-dataset: per-operation features must be built from each client's earlier operations, the unlabelled pretrain included (`Needs extensive data wrangling`); signals from a client's later operations (the "future" features of a public solution) are leaks at the prediction point, while the client's own past is legitimate (LEAK-10, LEAK-34); label-history features need the date the client's feedback arrived (LEAK-12, SPLIT-10); the test labels are hidden, so the benchmark uses the labelled period 2024-10 to 2025-05 with its own windows (SPLIT-5); labels exist only for operations the bank's system held, and fraud it missed counts as negative (no `Selection Bias` marker: the selection is how the label comes to exist); the size forces a subsample, and sampled negatives must not change the class balance of the test folds, or PR-AUC changes meaning (MET-2); event description, POS code and OS are described columns with coded values, so no `Anonymized` marker; yellow is a third outcome, and red against the rest is the source's framing. Data terms: the page links the contest rules; the re-upload's licence is "other" (no criterion, EV-4).
- Priority: gap 0 (finance, binary and temporal not thin), use case + (the bank's hold-and-confirm decision, named by the source), source + (the organiser's task page with periods, labels and metric; the column dictionary on the re-upload), shape + (100,000 clients, more than 200M operations, mixed types, temporal), risk - (history features to build with leak traps; a second record of the same competition).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark tabular-dl-more-data (https://arxiv.org/abs/2610.26794).
- as published: 10.97M train / 591K val / 590K test, 119 features; temporal split: train 2024-10-01..2025-05-04, validation 2025-05-04..05-18, test 2025-05-18..06-01; training negatives sampled at 15%; about 0.5% ...; target: operation not confirmed by the client ('red' class; client-confirmed suspicious 'yellow' operations and all others are negatives).
- Why: Flag bank client operations that the client did not confirm (fraud) for an anti-fraud system (Data Fusion Contest 2026, task 1 'Guardian', ODS.AI, 2026-02-09..03-30)
- Notes: The release is operation logs of 100,000 clients over about 1.5 years (over 200M operations; about 51K red and 36K yellow labelled operations in train), with unlabelled pre-train and pre-test periods, split into train_part_1..3 parquet files and train_labels.parquet; the authors build per-operation features (event ...

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).
