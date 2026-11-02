---
unique_name: fda_drug_enforcement_recalls
name: Drug Enforcement
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
- https://open.fda.gov/apis/drug/enforcement/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/drug-enforcement
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and a preview of the published files, nothing built. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the hazard class (I, II or III) FDA assigns to a drug recall after it is reported, 18,048 recalled products in the Enforcement Report; a triage task with a prediction point the source names, carried mostly by free text.
- Source: the FDA Enforcement Report (drug products) on openFDA (open.fda.gov/apis/drug/enforcement), 18,048 records (API meta, updated 2026-10-21: Class II 14,577, Class I 1,750, Class III 1,719, Not Yet Classified 2), one row per recalled product. As in STRABLE: 4,504 rows x 42 columns (the `openfda` drug fields flattened), report dates 2012-06 to 2025-12, target `classification` II 2,764 / III 1,116 / I 624: a quarter of the endpoint with another class mix, selection not stated.
- Use case: the class is "assigned by FDA to a particular product recall that indicates the relative degree of health hazard", and a recall in status Pending is one "determined to be recalls, but that remain in the process of being classified" (open.fda.gov/fields/drugenforcement.yaml). At that point the reason, product, quantity and distribution are known, and FDA's recall staff (or the recalling firm, planning the recall depth and public warning) anticipate the class; RecallRisk-BERT (arXiv 2606.27174, 2026) frames the same task on device recalls as "post-report recall triage". Fit direct once the fields set at or after classification go; regime temporal (`recall_initiation_date`), with the products of one recall (`event_id`) mostly sharing the class (85 of 4,417 events in STRABLE's file have more than one class) (SPLIT-13).
- Siblings and duplicates: `fda_food_enforcement_recalls` is another cut of the same Enforcement Report with the same task (PROV-6): one combined dataset with the product type as a feature, or one cut, is the curator's call; the device cut (open.fda.gov/apis/device/enforcement, 40,358 records) has no record. The other STRABLE FDA records are other tasks (PROV-7). External collections: STRABLE (App. C.2, item 31: "The task is to predict the recall classification level").
- Better data: a candidate of the benchmark STRABLE; no further search this round. The endpoint holds four times STRABLE's rows.
- Papers and pages: the openFDA page and field reference; STRABLE, Blayer et al. 2026 (arXiv 2605.12292); RecallRisk-BERT, Atalay and Yigit-Sert 2026 (arXiv 2606.27174; device recalls, where LightGBM on text embeddings and structured fields did best on severity).
- Metric: none from the source (openFDA defines no task); RecallRisk-BERT reports accuracy, macro precision, recall, F1 and ROC-AUC side by side, and STRABLE's AUROC (App. D.1) is benchmark-wide, so the fallback `log_loss`; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: drop the fields set at or after classification (`status`, `termination_date`, `center_classification_date`, `report_date`) (LEAK-10, USE-3); `reason_for_recall` and `product_description` are free text that carry most of the signal (SEL-12: text embeddings with a tabular learner did well in RecallRisk-BERT, check); the `openfda` fields (present on about 38% of rows) are joined from current labels at query time; rebuild from the API.
- Priority: gap + (multiclass thin), use case + (the source names the decision and its Pending stage; a paper names the triage), source +, shape + (18,048 records; text, categorical, dates), risk - (text-dominant; a PROV-6 cut shared with the food records).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 4,504 rows x 42 columns incl. target (STRABLE parquet); target: classification.
- Why: Predict the recall classification (Class I/II/III) of a drug enforcement report
- Notes: openFDA API extract.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: two cuts of the FDA Enforcement Report (`fda_food_enforcement_recalls`; PROV-6). The curator keeps one, or both as distinct tasks.
