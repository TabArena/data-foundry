---
unique_name: fda_drugs_at_fda
name: Drug Drugs@FDA
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
source_links:
- https://open.fda.gov/apis/drug/drugsfda/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/drug-drugsfda
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and a preview of the published files, nothing built. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: Drugs@FDA (29,428 approved applications); the target is whether a product is marketed or discontinued at the extraction date, a snapshot label, and missing submission records give it away.
- Source: Drugs@FDA (CDER), on openFDA since 2020-08-26 (open.fda.gov/about/updates; open.fda.gov/apis/drug/drugsfda), 29,428 applications (API meta, updated 2026-10-30), each with nested `products` (marketing status per product: "Prescription", "Discontinued", "None (Tentative Approval)", "Over-the-counter", field reference) and `submissions`. As in STRABLE: 27,075 rows x 8 columns, one per application, OTC and tentative approvals left out, and how a product's status became the application's is not stated; target `marketing_status` Discontinued 14,215 / Prescription 12,860. STRABLE's text says "The task is to predict approval years" (App. C.2, item 30).
- Use case: none named; a status at the extraction date over applications approved across decades is a look back (SEL-6); a discontinuation within a fixed time after approval would be a task, but the endpoint carries no dated status change; fit approximate at best; regime IID over applications.
- Siblings and duplicates: `drug_directory` (TabSTAR, the FDA NDC listing, `TBD -> 2nd Tier`) is the precedent; `fda_drug_shortages` and `fda_drug_enforcement_recalls` are other tasks (PROV-7). External collections: STRABLE.
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the openFDA page and field reference (open.fda.gov/fields/drugsfda.yaml); STRABLE, Blayer et al. 2026 (arXiv 2605.12292).
- Metric: none found (the openFDA page; STRABLE's AUROC, App. D.1, is benchmark-wide), so the fallback `roc_auc` (MET-1, MET-5).
- Risks for /add-dataset: rows without `submissions` are Discontinued in 2,694 of 2,698 cases in STRABLE's file (old records, LEAK-10); `submissions` holds dated actions after approval; the label is a snapshot (SEL-6) and the paper's target (approval years) differs from the config's (USE-5).
- Priority: gap 0 (binary), use case 0, source +, shape + (27,075 applications), risk - (a snapshot label; the missing-record shortcut).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 27,075 rows x 8 columns incl. target (STRABLE parquet); target: marketing_status.
- Why: Predict the marketing status of an FDA-approved drug product
- Notes: openFDA API extract. Paper says 'approval years'; config target is marketing_status (binary).
