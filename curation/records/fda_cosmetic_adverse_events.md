---
unique_name: fda_cosmetic_adverse_events
name: Cosmetic Event
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- STRABLE
original_source: GOV Website
year: '2025'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
source_links:
- https://open.fda.gov/apis/cosmetic/event/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/cosmetic-event
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and a preview of the published files, nothing built. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: 85,511 cosmetic adverse-event reports from FDA (openFDA, 2025); the target is the outcome the reporter states in the same report, reduced by STRABLE to 3 of 7 values, and 92% of STRABLE's rows are talc or powder reports.
- Source: FDA's "Cosmetic Adverse Events" dataset, released on openFDA on 2025-09-13 (open.fda.gov/about/updates), 85,511 reports (API meta, updated 2025-08-31), coverage "2001 to null"; a responsible person "is required to report serious adverse events associated with the use of cosmetic products" (open.fda.gov/apis/cosmetic/event), within 15 business days. Older reports carry CAERS ids in `legacy_report_id` (`2021-CFS-011967`). As in STRABLE: 75,000 rows x 13 columns (a stratified cap at 75,000, App. C.3), target `outcomes` Other Serious 37,245 / Death 25,781 / Hospitalization 11,974. In the API `outcomes` is a list over 7 values (Other Serious 65,580, Death 26,542, Hospitalization 16,388, Disability 492, Required Intervention 394, Life Threatening 372, Congenital Anomaly 56); how STRABLE made one class of it is not stated.
- Use case: FDA's cosmetics safety staff, when a report arrives, rank it by severity for follow-up; but the reporter states the outcome in the report itself, so nobody predicts it at that point (compare SEL-7); fit approximate at best; regime temporal (`initial_received_date` ships).
- Siblings and duplicates: `fda_food_adverse_events` is CAERS, which openFDA says covers "foods, dietary supplements, and cosmetics", so the older cosmetic reports may sit in both (17 of STRABLE's legacy ids match food-event report numbers in STRABLE's cut): one PROV-6 overlap to remove at the add stage. The other STRABLE FDA records are other tasks (PROV-7). External collections: STRABLE (App. C.2, item 23: "The task is to predict the severity of the reported reaction").
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: open.fda.gov/apis/cosmetic/event and its field reference (open.fda.gov/fields/cosmeticevent.yaml); STRABLE, Blayer et al. 2026 (arXiv 2605.12292). No prediction paper found.
- Metric: none found (the openFDA page and field reference; STRABLE's AUROC, App. D.1, is benchmark-wide), so the fallback `log_loss`; inputs none (MET-1, MET-5).
- Risks for /add-dataset: the target needs a definition from the outcome list (the most severe outcome, for example) (USE-5); in STRABLE's file 92% of rows name a talc or powder product and every Death row does, with ovarian cancer the top reaction (28,575 mentions), which points to litigation-sourced reports: a Selection Bias question for the curator; `report_type` (Expedited 15-Day, Pre-MoCRA, Direct) and `report_version` follow the reporting route; reactions and products are free-text lists.
- Priority: gap + (multiclass thin), use case 0, source +, shape + (85,511 reports, mixed fields), risk - (an unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 75,000 rows x 13 columns incl. target (STRABLE parquet); capped at 75,000 by STRABLE; target: outcomes.
- Why: Predict the outcome category of a reported cosmetic adverse event
- Notes: openFDA API extract. Subsampled by STRABLE to 75,000 rows (stratified).
