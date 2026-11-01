---
unique_name: fda_food_adverse_events
name: Food Event
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
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
source_links:
- https://open.fda.gov/apis/food/event/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/food-event
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and a preview of the published files, nothing built. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: CAERS, 151,589 adverse-event reports on foods, supplements and cosmetics since 2004; the outcome is part of what the reporter submits, and STRABLE kept 3 of 13 outcome values by an unstated rule.
- Source: the FDA CFSAN Adverse Event Reporting System (CAERS) on openFDA (open.fda.gov/apis/food/event; "2004 to null", quarterly), "adverse event and product complaint reports submitted to FDA for foods, dietary supplements, and cosmetics", 151,589 reports (API meta, updated 2026-07-07). `outcomes` is a list over 13 values (Other Serious 85,802, Other Outcome 27,322, Hospitalization 23,699, Visited a Health Care Provider 20,711, Death 17,041, Visited Emergency Room 14,378, ...). As in STRABLE: 23,713 rows x 9 columns, target `outcomes` Health Care Provider 8,992 / Emergency Room 7,759 / Hospitalization 6,962, the other ten values (Death and Other Serious among them) absent; the selection is not stated.
- Use case: FDA's CAERS reviewers rank incoming reports by severity for signal follow-up; but the reporter states the outcome in the report, so nothing is predicted at that point (compare SEL-7), and openFDA warns that "a causal relationship cannot be established between product and reactions listed in a report"; fit approximate at best; regime temporal (`date_created` ships).
- Siblings and duplicates: `fda_cosmetic_adverse_events` overlaps on the cosmetic reports (PROV-6 overlap to remove; 50 rows of STRABLE's cut name a cosmetic product); the other STRABLE FDA records are other tasks (PROV-7). External collections: STRABLE (App. C.2, item 44: "The task is to predict the consumer outcome").
- Better data: a candidate of the benchmark STRABLE; no further search this round. The endpoint holds six times STRABLE's rows.
- Papers and pages: the openFDA page and field reference (open.fda.gov/fields/foodevent.yaml); STRABLE, Blayer et al. 2026 (arXiv 2605.12292); CAERS is used for disproportionality signal detection, and no prediction paper was found.
- Metric: none found (the openFDA page and field reference; STRABLE's AUROC, App. D.1, is benchmark-wide), so the fallback `log_loss`; inputs none (MET-1, MET-5).
- Risks for /add-dataset: define the target from the outcome list (the most severe outcome, ordinal) (USE-5); for dietary supplements firms "must notify the FDA" of serious adverse events (openFDA), so the outcome mix depends on the product type and the reporter: a Selection Bias question; `reactions` may name the outcome (MedDRA terms such as death); product names are free text.
- Priority: gap + (multiclass thin), use case 0, source +, shape + (151,589 reports), risk - (an unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 23,713 rows x 9 columns incl. target (STRABLE parquet); target: outcomes.
- Why: Predict the consumer outcome category of a food/supplement adverse-event report (CAERS)
- Notes: openFDA API extract.
