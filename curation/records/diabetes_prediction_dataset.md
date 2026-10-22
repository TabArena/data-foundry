---
unique_name: diabetes_prediction_dataset
name: Diabetes Prediction Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Missing source information
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset
source_row: 825
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Missing source information`, PROV-1): an anonymous Kaggle upload whose only provenance is a generic paragraph about EHRs; no provider, institution, paper or first upload upstream is named, and the curator's CC below already calls the source missing and the data likely fake.
- Source: Kaggle "Diabetes prediction dataset" by user iammustafatz (https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset, dataset id 3102947, year of first version not checked), licence "copyright-authors"; as published: one table with gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level and the binary `diabetes`.
- What the uploader says about the source (Kaggle metadata "sources"): "EHRs were collected from multiple healthcare providers and aggregated into a single dataset. The data was then cleaned and preprocessed" — no provider, country, period or ethics approval, and no reply naming one.
- PROV-2 does not keep it: there is no source to point to beyond the uploader, and the CC line reports a Kaggle discussion (588830) arguing the data is wrong or fake; if the data is generated it is also a PROV-3 case (`AHDS`), not measured here.
- Previous markers `Ethical Issue`, `Data Quality Issue` and `AHDS` are not decided by the source's words: proposed to drop `Ethical Issue` (no objection by subjects or creators is stated, SEL-1); `AHDS` and `Data Quality Issue` stay only if the reject-checker or a measurement backs them (PROV-3 tests not run).
- Siblings: many diabetes records (`cdc_diabetes_health_indicators`, `pima_indians_diabetes_database`, `early_stage_diabetes_risk_prediction`, `nhanes_undiagnosed_diabetes`, ...) have named sources; none is this table's upstream as far as checked by name.
- Reject check (AI, 2026-10-22): stands. PROV-1 (no upstream beyond the anonymous uploader) and PROV-2 cannot rescue it, because the data fails PROV-3 when measured (checker download, 100,000 rows): HbA1c_level takes only 18 values and blood_glucose_level only 18, each level near-uniform (~7,500 rows), and the label is tied to the levels: every row with HbA1c >= 6.8 or glucose >= 200 is diabetic, and every diabetic row has HbA1c >= 5.7 and glucose >= 126 (label-linked marks, PROV-3 tests 5/7); corr(HbA1c, glucose) only 0.17. Add `AHDS` back with the measurement; drop `Ethical Issue`. https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset

Popular Kaggle 'Diabetes Prediction Dataset' (iammustafatz) with no documented source; the curator and a linked Kaggle discussion indicate the data is likely fake/fabricated, and it is flagged for ethical and data-quality issues. This fails criterion 1 (unique real source), criterion 4B (artificial data), and likely criterion 5 (ethical). Confidence in rejection is high. A human need only confirm the fabricated-data discussion thread before finalizing the reject.

---

CC: ""Very simplistic dataset, missing source information and the way it is shared is questionable

Likely, the data is wrong / fake: see https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset/discussion/588830""
