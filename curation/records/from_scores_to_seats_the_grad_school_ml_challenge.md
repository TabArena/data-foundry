---
unique_name: from_scores_to_seats_the_grad_school_ml_challenge
name: from-scores-to-seats-the-grad-school-ml-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
domain: education
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/from-scores-to-seats-the-grad-school-ml-challenge/data
source_row: 940
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a two-day beginner hackathon on graduate-admission features whose data is most likely the Kaggle "Graduate Admission" set (500 rows, a self-estimated "Chance of Admit") enlarged or relabelled; the data could not be inspected.
- Source: Zindi hackathon "From Scores to Seats: The Grad School ML Challenge" by Hackade (Nigeria, 2025-04-04 to 2025-04-06, access restricted); "predict whether a student will be admitted into a graduate program based on their academic profile, including standardized test scores, university rating, CGPA, and research background"; files train.csv, test.csv, variable_description.csv; target `Admitted` (1 admitted, 0 not). Row count not stated (the sample IDs reach ID_004125, more than the 500 rows of the Kaggle set).
- Use case: an applicant or a university estimates admission from the profile; fit unclear, since the features match Acharya et al.'s Kaggle "Graduate Admission" data (GRE, TOEFL, University Rating, SOP, LOR, CGPA, Research), whose target is a 0-1 "Chance of Admit", not an observed admission decision; regime IID.
- Siblings and duplicates: no graduate-admission record (grep for admission, Acharya, chance of admit); `law_school_admission_bianry` and `turkish_university_admissions` are other admission tasks. If the data is the Kaggle set, the Kaggle upload is the first publication and this would be a `Duplicate` (PROV-4).
- Papers and pages: https://zindi.africa/competitions/from-scores-to-seats-the-grad-school-ml-challenge (Zindi API read 2026-10-22); Acharya, Armaan and Antony 2019, "A comparison of regression models for prediction of graduate admissions" (the Kaggle set); no copy of the Zindi files found on GitHub or the web.
- Metric: F1 on hard 0/1 labels, the Zindi Evaluation page ("The evaluation metric for this challenge is F1 Score"); leaderboard metric (MET-4), threshold left to the participant (MET-6); inputs none.
- Risks for /add-dataset: the provenance (a copy, a synthetic enlargement or a threshold of "Chance of Admit"; PROV-3, PROV-4, SEL-5); the target may not be an observed outcome (SEL-3); size unknown.
- Priority: gap + (education thin), use case 0, source 0 (a two-day hackathon page), shape 0 (size unknown), risk - (provenance and target).

Zindi competition with no comments; the name suggests predicting graduate-school admission/placement ('seats') from applicant scores, an education-domain tabular classification or regression task with a clear target. This would be representative real-world tabular ML if the data is genuine applicant records. Insufficient detail to confirm the exact target, size, and whether the data is synthetic/handmade. A human must inspect the competition data to confirm the target definition, problem type, and that it is not an artificial/generated set.
