---
unique_name: fda_drug_shortages
name: Drug Shortages
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
problem_type: Multiclass Classification
source_links:
- https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/drug-shortages
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and a preview of the published files, nothing built. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: FDA's drug shortage list (1,615 presentations); the availability is the current status FDA posts from the firm's information, a snapshot that changes after extraction, and the features are mostly identifiers.
- Source: the FDA Drug Shortages database (CDER, www.fda.gov/drugs/drug-safety-and-availability/drug-shortages), released on openFDA on 2025-03-25 (open.fda.gov/about/updates), 1,615 presentations (API meta, updated 2026-10-30) with `status` (Current 1,153, To Be Discontinued 443, Resolved), `shortage_reason`, `related_info` and `update_date`. As in STRABLE: 1,180 rows x 10 columns, initial postings 2012-2025, target `availability` Available 763 / Unavailable 267 / Limited Availability 150. STRABLE's text says "The task is to predict the duration of the shortage" (App. C.2, item 33), its config `availability`.
- Use case: a hospital pharmacist, when a shortage is posted, anticipates whether a given presentation stays available; but the label is the status at the extraction date, shared by all rows rather than a fixed time after each posting (SEL-6: a look back), and the API's counts already differ from STRABLE's (749 Available today); fit approximate at best; regime temporal by `initial_posting_date` if a dated target is built.
- Siblings and duplicates: `drug_directory` (TabSTAR, the FDA NDC listing, `TBD -> 2nd Tier`, "not a real predictive task") is the precedent for FDA listings; `fda_drugs_at_fda` and `fda_drug_enforcement_recalls` are other tasks (PROV-7). External collections: STRABLE.
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the FDA drug shortages page; open.fda.gov/apis/drug/drugshortages and its field reference (open.fda.gov/fields/drugshortages.yaml); STRABLE, Blayer et al. 2026 (arXiv 2605.12292).
- Metric: none found (the FDA and openFDA pages; STRABLE's AUROC, App. D.1, is benchmark-wide), so the fallback `log_loss` (MET-1, MET-5).
- Risks for /add-dataset: the paper's target (the duration) needs resolved shortages with dates, the config's (availability) is a snapshot (USE-5, SEL-6); `presentation` and `package_ndc` are unique per row; `related_info`, `status` and `update_date` are written with the availability (LEAK-10).
- Priority: gap + (multiclass thin), use case 0, source +, shape 0 (1,180 rows, mostly identifiers and text), risk - (a snapshot label).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,180 rows x 10 columns incl. target (STRABLE parquet); target: availability.
- Why: Predict the availability status of a drug in the FDA shortage list
- Notes: openFDA drug shortages endpoint. Paper says 'duration of the shortage'; config target is availability (multiclass).
