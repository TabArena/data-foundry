---
unique_name: fda_tobacco_problem_reports
name: Tobacco Problem
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- STRABLE
source_links:
- https://open.fda.gov/apis/tobacco/problem/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/tobacco-problem
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-7): STRABLE's target `number_health_problems` is openFDA's "System-calculated number of Health Problems (i.e., MedDRA terms selected from a standardized list of symptoms, signs, diagnoses and outcomes) reported", a count of what the reporter ticked in the same report whose other fields are the features; FDA has it on receipt, so nobody predicts it.
- Source: FDA Center for Tobacco Products, tobacco problem reports from the Safety Reporting Portal, served by openFDA (https://open.fda.gov/apis/tobacco/problem/; fields https://open.fda.gov/fields/tobaccoproblem.yaml), 2017 on, updated quarterly, 1,383 reports (API meta, last updated 2026-07-31). "Consumers, manufacturers, and health professionals submit reports" on products that are damaged, defective or contaminated or that cause undesirable health effects; FDA posts them unedited and has not determined causality. As published: report_id, date_submitted, number_tobacco_products, tobacco_products, number_health_problems, reported_health_problems, number_product_problems, reported_product_problems, nonuser_affected. STRABLE dropped reported_health_problems: 1,314 rows x 8 columns, target number_health_problems (0: 251, 1: 621, 2: 442).
- Use case: none. SEL-7: "A label the respondent already knows, asked in the same interview as the features ... is predicted by nobody"; the count and the features are fields of one submitted form. STRABLE's paper names "the health problem type" (App. C.2), also a field of the same report.
- Siblings and duplicates: the other openFDA records of the run (`fda_food_adverse_events`, `fda_cosmetic_adverse_events`, `fda_animal_veterinary_adverse_events` and others) share the source kind, not this data. External collections: STRABLE ("Tobacco Problem").
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Papers and pages: the openFDA endpoint and field list; STRABLE (arXiv 2605.12292, App. C.2 and D.1).
- Metric: none found (openFDA defines no task); STRABLE scores AUROC (App. D.1).
- Also: 1,383 reports and 7 features would be small even with a real target.
- Reject check (AI, 2026-10-31): stands. openFDA: number_health_problems is the 'System-calculated number of Health Problems (i.e., MedDRA terms selected from a standardized list of symptoms, signs, diagnoses and outcomes) reported' (https://open.fda.gov/fields/tobaccoproblem.yaml): a count of the reporter's own selections on the same form as every feature, known to FDA on receipt. Every other field is from that same form, so no re-target gives a prediction point.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,314 rows x 8 columns incl. target (STRABLE parquet); target: number_health_problems.
- Why: Predict the number-of-health-problems class of a tobacco product problem report
- Notes: openFDA API extract. Paper says 'health problem type'; config target is number_health_problems (multiclass). Only 8 columns.
