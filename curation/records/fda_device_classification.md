---
unique_name: fda_device_classification
name: Device Classification
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Free Text (Sentences)
collections:
- STRABLE
original_source: GOV Website
domain: medical & healthcare
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://open.fda.gov/apis/device/classification/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/device-classification
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and a preview of the published files, nothing built. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: FDA's registry of 7,097 device product codes with their regulatory class; closer to a lookup of the classification regulation than to a prediction (the `drug_directory` precedent), and several flags follow from the class.
- Source: the FDA CDRH product classification database on openFDA (open.fda.gov/apis/device/classification), 7,097 product codes (API meta, updated 2026-10-19), one row each with `device_class`, `regulation_number`, `submission_type_id`, `review_code`, `review_panel`, flags, `device_name` and `definition`. As in STRABLE: 6,522 rows x 10 columns (classes 1, 2 and 3 only), target `device_class` 2: 3,594 / 1: 2,399 / 3: 529; STRABLE dropped `regulation_number`, `submission_type_id` and `review_code`.
- Use case: a manufacturer or regulatory consultant with a new device type estimates its class, and so the 510(k), De Novo or PMA route, before contacting FDA; the source names no such use, and FDA sets the class by matching the device type to a classification regulation, so the fit is approximate; regime likely IID over product codes (the endpoint ships no date).
- Siblings and duplicates: `drug_directory` (TabSTAR, the FDA NDC listing; Lennart: "Just a list of drug listings, not a real predictive task", `TBD -> 2nd Tier`) is the closest precedent; `fda_device_pma` shares the product codes but is another task (PROV-7). External collections: STRABLE (App. C.2, item 25: "The task is to predict the specific device class").
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: open.fda.gov/apis/device/classification (the field reference YAML returned 403); STRABLE, Blayer et al. 2026 (arXiv 2605.12292). No prediction paper found.
- Metric: none found (the openFDA page; STRABLE's AUROC, App. D.1, is benchmark-wide), so the fallback `log_loss`; inputs none (MET-1, MET-5).
- Risks for /add-dataset: flags decided with or after the class carry the label (in STRABLE's file `gmp_exempt_flag` Y on 532 class-1 codes, 6 class-2, no class-3; `third_party_flag` Y never on class 3; `life_sustain_support_flag` Y never on class 1) (LEAK-10); `regulation_number`, `submission_type_id` and `review_code` stay out; `device_name` and `definition` are short free text (SEL-12, check).
- Priority: gap + (multiclass thin), use case 0, source +, shape + (6,522 codes; flags, panel, text), risk - (flags set by the class).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 6,522 rows x 10 columns incl. target (STRABLE parquet); target: device_class.
- Why: Predict the FDA regulatory class (I/II/III) of a medical device type
- Notes: openFDA API extract.
