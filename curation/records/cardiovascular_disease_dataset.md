---
unique_name: cardiovascular_disease_dataset
name: Cardiovascular-Disease-dataset
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Data Quality Issue
- Missing source information
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
- TabSTAR
- TabArena Reject
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset
- https://www.openml.org/search?type=data&id=45547&sort=runs&status=active
source_row: 828
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curators' `No` (CC lines, TabArena Reject) rests on `Missing source information`; the source can be traced, so that reason does not hold, while the data-quality doubts stay open. Counter-argument below; the curator has the call.
- Source: the Kaggle upload (sulianova, file `cardio_train.csv` dated 2019-10-17, licence "unknown") says only "70 000 records of patients data, 11 features + target" and "All of the dataset values were collected at the moment of medical examination". The same columns (age in days, height, weight, gender, ap_hi, ap_lo, cholesterol 1-3, gluc 1-3, smoke, alco, active, cardio) are the data of the Mail.Ru ML Boot Camp championship of 15 June to 15 July 2017, organised "together with Insilico Medicine" (VK/Mail.Ru blog on Habr, habr.com/en/articles/330960): "Датасет сформирован из 100.000 реальных клинических анализов" (built from 100,000 real clinical tests), "Тренировочная выборка состоит из 70 тысяч результатов" (the training set is 70 thousand), and 20 thousand in a hidden test set. The Kaggle file matches the competition's training set in size and columns; OpenML 45547 is a copy of the Kaggle file.
- Use case: screening for cardiovascular disease from a routine check-up ("по результатам классического врачебного осмотра", from a classic doctor's examination, Habr post on the 3rd-place solution, habr.com/post/335188); fit approximate: who examined the patients and how the label was set are not documented. Regime IID.
- Metric: the competition scored log loss ("метрикой является логарифмическая функция потерь", Habr 330960), a leaderboard metric (MET-4).
- Siblings and duplicates: `heart_disease_*`, `framingham_heart_study_fhs` are other cohorts, not duplicates. External collections: TabSTAR, OpenML 45547.
- Data quality: the Kaggle discussion the CC cites lists impossible blood pressures (negative or thousands for ap_hi/ap_lo) and heights; these are entry errors that can be made missing (CLEAN rules), and the organiser's statement of real clinical tests argues against generated data (PROV-3), though the clinic and the label definition stay unknown.
- **Counter-argument (AI):** `Missing source information` (PROV-1) needs a source that cannot be traced; here the first publication is a named competition by Mail.Ru and Insilico Medicine with its size, split and metric stated. What stays open is the data's documentation (which clinic, how `cardio` was diagnosed, PROV-2) and the outlier values. Suggest re-reading the verdict on those grounds (`Data Quality Issue` if the curator judges the damage irreparable, otherwise a `TBD -> 2nd Tier` with the competition as the source); the curator has the call.

Popular Kaggle/OpenML cardiovascular-disease dataset (predict presence of cardiovascular disease from clinical/examination features). Although widely used, the record and curation notes flag that the data source is unknown, the data may be synthetic, and there are documented quality issues (outliers, implausible values), and it is already in the TabArena Reject collection. Missing provenance plus credible suspicion of synthetic/dirty data make it unsuitable. A human could re-check the discussion threads, but the existing markers (Data Quality Issue, Missing source information) support rejection.

---

CC: ""Source of data is missing. Unclear if real data or not

it is used a lot, also in papers

Various concerns about data quality issues: https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset/discussion/451915
Also see TabArena comments on it""
CC: ""Uploaded by Matthias Feurer - not much information; from Kaggle, seems like a real task without much more information

At the same time see the Kaggle discussions no one knows the source and it might be synthetic data due to outliers. Remove due to missing source information""
