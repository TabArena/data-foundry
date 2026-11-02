---
unique_name: fda_animal_veterinary_adverse_events
name: Animal and Veterinary Event
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- STRABLE
original_source: GOV Website
year: '2019'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://open.fda.gov/apis/animalandveterinary/event/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/animalandveterinary-event
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and a preview of the published files, nothing built. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: FDA CVM's animal drug adverse-event reports (1.38M on openFDA); the seriousness flag is a regulatory label coded from the outcome by a published rule, so a report-triage task at best, and STRABLE's 1,345-row slice is not a random draw.
- Source: FDA Center for Veterinary Medicine adverse-event reports, first released on openFDA as "Animal Drug Adverse Event Reports" on 2019-04-03 (open.fda.gov/about/updates); the endpoint holds 1,378,854 reports (API meta, updated 2026-10-05) as nested JSON (animal, drug and reaction lists, outcome, health assessment). As in STRABLE: 1,345 rows x 20 columns, 776 of them received in 2024-2025, target `serious_ae` 670 true / 675 false against 349,659 true / 556,070 false in the API; STRABLE does not say how the slice was taken.
- Use case: a pharmacovigilance case processor (the manufacturer's or CVM's), when a report comes in, flags it as serious for expedited reporting and review; the source names no such use, so the use case is ours; fit approximate (reactions and seriousness are coded by the same processor in the same report); regime temporal, reports arrive over time (`original_receive_date` ships).
- Siblings and duplicates: the other openFDA records from STRABLE (`fda_cosmetic_adverse_events`, `fda_food_adverse_events`, `fda_tobacco_problem_reports` and the device, drug and recall records) are other reporting systems or tasks (PROV-7); no other record holds CVM data. External collections: STRABLE (App. C.2, item 3: "The task is to predict the severity of clinical signs"; config target `serious_ae`).
- Better data: a candidate of the benchmark STRABLE; no further search this round. The source itself holds about 1,000 times STRABLE's rows.
- Papers and pages: open.fda.gov/apis/animalandveterinary/event and its field reference (open.fda.gov/fields/animalandveterinaryevent.yaml); STRABLE, Blayer et al. 2026 (arXiv 2605.12292). No paper predicting seriousness from these reports found.
- Metric: none found (the openFDA page and field reference define no task; STRABLE scores AUROC on every classification table, App. D.1, a benchmark-wide choice, not the source's), so the fallback `roc_auc`; inputs none (MET-1, MET-5).
- Risks for /add-dataset: the field reference defines the label by a rule, "The adverse event is fatal or life-threatening, or requires professional intervention, or causes an abortion, or stillbirth, or infertility, ..." (SEL-5): its inputs (`outcome.medical_status` Died or Euthanized, dropped by STRABLE; reaction terms for death or abortion, kept) must go, and whether the rest is still a task is open; rebuild from the API rather than STRABLE's slice (nested lists to flatten); `type_of_information` includes product-defect reports without an adverse event.
- Priority: gap 0 (binary, medical & healthcare not thin), use case 0 (ours), source +, shape + (1.38M reports, mixed fields), risk - (a label set by a published rule from the outcome, SEL-5; an unexplained slice).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,345 rows x 20 columns incl. target (STRABLE parquet); target: serious_ae.
- Why: Predict whether an animal adverse-event report (drug exposure) is serious
- Notes: openFDA API extract; only 1,345 rows of a much larger API (STRABLE's slice). Paper text says 'severity of clinical signs'; the config target is serious_ae (binary).
