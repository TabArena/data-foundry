---
unique_name: dare_to_women_tech_shecures_ai_for_diabetes_prediction
name: dare-to-women-tech-shecures-ai-for-diabetes-prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: medical & healthcare
required_split:
- Random (IID)
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/dare-to-women-tech-shecures-ai-for-diabetes-prediction
source_row: 941
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a 10-day community hackathon whose page says nothing about where the health data comes from; the task (type 2 against gestational diabetes) is unclear as a decision.
- Source: Zindi hackathon "Dare to women Tech - SheCures: AI for Diabetes Prediction" (2025-04-14 to 2025-04-24, secret code required, Data Sharing CC-BY SA 4.0), run by the Dare to be Women Tech community for International Girls in ICT Day. As published: `Train.csv`, `Test.csv`, `VariableDefinitions.csv`; the Data Description page is empty, so rows, columns and the origin of the data are unknown (Zindi needs a login; read through the Zindi API, https://zindi.africa/competitions/dare-to-women-tech-shecures-ai-for-diabetes-prediction).
- Use case: "distinguishing between different types of diabetes (such as Type 2 and Gestational Diabetes) using health data", because "many cases are diagnosed late—or incorrectly" (Description page); no actor or moment named; fit approximate at best (pregnancy status separates gestational diabetes by definition, so the target may be near-trivial); regime IID (one row per patient assumed).
- Siblings and duplicates: no record of this competition (grep: shecures, dare-to-women); the diabetes records (`diabetes_prediction_dataset`, `pima_indians_diabetes_database`, `early_stage_diabetes_risk_prediction`, `diabetes_130_us`, ...) are candidates for the upstream, since community hackathons often re-use a Kaggle table: to check against the variable list (PROV-4). External collections: none found.
- Papers and pages: the competition page only; no paper, no top solutions found.
- Metric: accuracy, "The error metric for this challenge is Accuracy" (Evaluation page), the leaderboard metric (MET-4), hard labels; inputs none.
- Risks for /add-dataset: the origin of the data (PROV-1, PROV-3: a generated or re-uploaded table is likely), the target's meaning (USE-5), a pregnancy column that settles the class (SEL-5, TP-4).
- Priority: gap - (medical, binary, IID), use case - (no actor or decision), source - (no data description), shape - (unknown), risk - (unknown origin, unclear target): floor 1.

Zindi hackathon for diabetes prediction, a plausible real-world medical binary-classification task on tabular clinical/demographic features. The record carries no description, so size, feature set, and whether the data is a re-upload of a known (possibly synthetic) diabetes set are unknown. Many 'diabetes prediction' Kaggle/competition sets turn out to be synthetic or duplicates of the Pima set, so provenance is the key risk. A human must verify the data is real and original, its size, the target, and that there are no ethical/synthetic issues before confirming Yes.
