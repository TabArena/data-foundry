---
unique_name: av_healthcare_analytics_length_of_stay
name: Analytics Vidhya JanataHack Healthcare Analytics II (hospital length of stay)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
year: '2020'
domain: medical & healthcare
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.analyticsvidhya.com/datahack/contest/janatahack-healthcare-analytics-ii
- http://arxiv.org/abs/2604.01841
- https://www.kaggle.com/datasets/nehaprabhavalkar/av-healthcare-analytics-ii
- https://www.kaggle.com/datasets/arashnic/covid19-hospital-treatment
- https://www.openml.org/d/43550
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: Analytics Vidhya's JanataHack Healthcare Analytics II (2020), 318,438 admissions at coded hospitals (32 per the run's note) with an 11-class length of stay and features known at admission; large and multiclass, but where the records come from is not documented.
- Source: Analytics Vidhya, JanataHack: Healthcare Analytics II (datahack.analyticsvidhya.com; the contest page now shows no problem statement or data, 19,844 registered). The statement survives on the Kaggle mirror `nehaprabhavalkar/av-healthcare-analytics-ii` (files dated 2020-08-29: train_data.csv, test_data.csv, train_data_dictionary.csv, sample_sub.csv). As published: the train file, 318,438 rows x 18 columns (OpenML 43550, "COVID-19-Hospitals-Treatment-Plan"): case_id, hospital code, type, city and region, available extra rooms, department, ward type and facility, bed grade, patientid, patient city, type of admission, severity of illness, visitors with patient, age band, admission deposit, and `Stay` in 11 classes ("ranging from 0-10 days to more than 100 days"). The test labels were not released. The statement is a role play ("Suppose you have been hired as Data Scientist of HealthMan – a not for profit organization"), and neither the page nor the mirror says where the records come from.
- Use case: the statement names it: the length of stay "helps hospitals to identify patients of high LOS risk (patients who will stay longer) at the time of admission" and "prior knowledge of LOS can aid in logistics such as room and bed allocation planning"; a hospital's bed manager at admission; fit approximate while the origin is unknown (PROV-2). Regime open: grouped by patient (`patientid` can repeat across cases, to count) or by hospital; the contest's split is a claim (SPLIT-5).
- Siblings and duplicates: `length_of_stay` (Microsoft's synthetic sample, `TBD -> 2nd Tier`, `AHDS`) and `ny_sparcs_inpatient_length_of_stay` (`TBD -> Yes`, 2, New York's real discharge file) are the same kind of task from other sources (PROV-7); `hr_analytics` (`Yes`) is the precedent for an Analytics Vidhya hackathon dataset. The Kaggle upload `arashnic/covid19-hospital-treatment` and OpenML 43550 present these rows as COVID-19 data: copies, not records. External collections: OpenML 43550; the AWARE paper (arXiv 2604.01841, per the run's note).
- Better data: from the curator's Zotero collection (item 289, the AWARE paper); no further search this round.
- Papers and pages: the contest page; the statement on the Kaggle mirror.
- Metric: "The evaluation metric for this hackathon is 100*Accuracy Score" (the statement): the competition's metric (MET-4), `accuracy` on the 11 classes; the classes are ordered, so the curator may weigh the fallback `log_loss` if one class dominates (MET-8, to check); inputs none.
- Risks for /add-dataset: the origin of the records and whether they were generated (PROV-1 to PROV-3: check the data for duplicated profiles and implausible joint distributions); `Visitors with Patient` and `Available Extra Rooms in Hospital` may be counted during the stay rather than at admission (USE-3, LEAK); hospital and city codes are masked values of described columns (no `Anonymized` marker, Patterns, "Anonymized data").
- Priority: gap + (multiclass classification is thin, 24 accepted), use case +, source 0 (a hackathon without a documented origin), shape + (318,438 cases, mixed categoricals, patient and hospital groups), risk - (origin and generation unclear).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 289: "Retrieval-aligned Tabular Foundation Models Enable Robust Clinical Risk Prediction in ...".
- as published: admissions (cases), 318,438 labelled rows x 18 columns, 32 anonymized hospitals, dates not given; target: Stay: length of stay in 11 classes (0-10 days up to more than 100 days); access: open.
- Why: Large, with features known at admission (hospital, department, ward, admission type, severity, age band, deposit) and a clear operational use case. Other AV-sourced data has been accepted (hr_analytics).
- Adds: Not recorded; a real-world-looking LOS task at scale. Caveats: the hospitals and the data's origin are not documented (likely 'Missing source information'). The Kaggle 'COVID-19' title is a relabel, not COVID data, and the AWARE paper miscites it to the Fangcang shelter-hospital study.
