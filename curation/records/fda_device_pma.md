---
unique_name: fda_device_pma
name: Device PMA
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
source_links:
- https://open.fda.gov/apis/device/pma/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/device-pma
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and a preview of the published files, nothing built. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: FDA's PMA database (57,373 applications and supplements since 1976); STRABLE's binary target separates approvals from accepted 30-day notices, which is the type of submission the applicant chose, so the task needs a new target (the review time, for example).
- Source: the FDA CDRH premarket approval database on openFDA (open.fda.gov/apis/device/pma; "1976 to null", monthly), 57,373 records (API meta, updated 2026-10-19). As in STRABLE: 54,636 rows x 20 columns, target `decision_code` APPR 27,898 / OK30 26,738; STRABLE dropped `supplement_number`, `supplement_type`, `supplement_reason` and `ao_statement`. The field reference (open.fda.gov/fields/devicepma.yaml) defines the 30-day code as "30 day notice acceptance (decision made in ≤30 days)", and for a 30-day notice "The applicant may distribute the device 30 days after the date on which FDA receives the notice".
- Use case: as framed by STRABLE, none: the code follows from the kind of submission, known when the applicant files it. A re-target fits a real decision: a manufacturer planning a device change or a launch predicts the review time of an original PMA or a 180-day supplement (`decision_date` minus `date_received`), or whether an original PMA is approved, withdrawn or denied; fit approximate until that is defined; regime temporal (`date_received`), grouped inside by `pma_number`, the supplements of one device (SPLIT-13).
- Siblings and duplicates: `fda_device_classification` shares the product codes, another task (PROV-7). External collections: STRABLE (App. C.2, item 27: "The task is to predict the final decision status").
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the openFDA page and field reference; STRABLE, Blayer et al. 2026 (arXiv 2605.12292). No prediction paper found.
- Metric: none found (the openFDA page and field reference; STRABLE's AUROC, App. D.1, is benchmark-wide), so the fallback for whichever target is chosen (MET-1, MET-5).
- Risks for /add-dataset: `decision_date` gives STRABLE's label away (in STRABLE's file OK30 decisions come a median 28 days after receipt, APPR 103) (LEAK-10); the target must be redefined (USE-5); `date_received` holds placeholder dates (1900-01-01); `openfda` packs registration numbers.
- Priority: gap 0 (binary), use case 0, source +, shape + (54,636 records, dates, mixed fields), risk - (the target is the submission type; a decision-date leak).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 54,636 rows x 20 columns incl. target (STRABLE parquet); target: decision_code.
- Why: Predict the decision code of a premarket approval (PMA) application or supplement
- Notes: openFDA API extract.
