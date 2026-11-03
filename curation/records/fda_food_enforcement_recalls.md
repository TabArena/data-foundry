---
unique_name: fda_food_enforcement_recalls
name: Food Enforcement
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Free Text (Sentences)
collections:
- STRABLE
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://open.fda.gov/apis/food/enforcement/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/food-enforcement
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and a preview of the published files, nothing built. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the hazard class (I, II or III) FDA assigns to a food recall after it is reported, 29,512 recalled products in the Enforcement Report; the triage task of `fda_drug_enforcement_recalls` on food hazards (pathogens, allergens), carried mostly by free text.
- Source: the FDA Enforcement Report (food products) on openFDA (open.fda.gov/apis/food/enforcement), 29,512 records (API meta, updated 2026-10-21: Class II 14,763, Class I 12,985, Class III 1,763, Not Yet Classified 1), one row per recalled product. As in STRABLE: 7,654 rows x 22 columns, report dates 2012-06 to 2025-12, target `classification` II 3,909 / I 3,088 / III 657: about a quarter of the endpoint, selection not stated.
- Use case: the class is "assigned by FDA to a particular product recall that indicates the relative degree of health hazard" (Class I examples: "food found to contain botulinum toxin, food with undeclared allergens"), and a Pending recall is one "determined to be recalls, but that remain in the process of being classified" (open.fda.gov/fields/foodenforcement.yaml); when the recall is reported, FDA's recall staff or the firm anticipate the class. Fit direct once the fields set at or after classification go; regime temporal (`recall_initiation_date`), with the products of one recall (`event_id`) mostly sharing the class (171 of 7,473 events in STRABLE's file have more than one class) (SPLIT-13).
- Siblings and duplicates: `fda_drug_enforcement_recalls` is the drug cut of the same Enforcement Report with the same task (PROV-6, the same call as there; the device cut has no record). The other STRABLE FDA records are other tasks (PROV-7). External collections: STRABLE (App. C.2, item 43: "The task is to predict the reason for the recall"; the config's target is `classification`).
- Better data: a candidate of the benchmark STRABLE; no further search this round. The endpoint holds about four times STRABLE's rows.
- Papers and pages: the openFDA page and field reference; STRABLE, Blayer et al. 2026 (arXiv 2605.12292); RecallRisk-BERT, Atalay and Yigit-Sert 2026 (arXiv 2606.27174), the same task on device recalls.
- Metric: none from the source (openFDA defines no task); RecallRisk-BERT reports its metrics side by side and STRABLE's AUROC (App. D.1) is benchmark-wide, so the fallback `log_loss`; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: drop `status`, `termination_date`, `center_classification_date` and `report_date` (LEAK-10, USE-3); STRABLE's text and config disagree on the target (the reason vs the class; the class is the decision, USE-5); `reason_for_recall` and `product_description` carry the hazard as free text (SEL-12, check); the API adds `more_code_info` and `openfda`.
- Priority: gap + (multiclass thin), use case + (the source names the decision and its Pending stage), source +, shape + (29,512 records; text, categorical, dates), risk - (text-dominant; a PROV-6 cut shared with the drug records).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 7,654 rows x 22 columns incl. target (STRABLE parquet); target: classification.
- Why: Predict the recall classification (Class I/II/III) of a food enforcement report
- Notes: openFDA API extract. Paper says 'reason for the recall'; config target is classification.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: two cuts of the FDA Enforcement Report (`fda_drug_enforcement_recalls`; PROV-6). The curator keeps one, or both as distinct tasks.
