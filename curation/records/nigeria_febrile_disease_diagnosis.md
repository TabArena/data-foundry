---
unique_name: nigeria_febrile_disease_diagnosis
name: NFRF Project Patient Dataset with Febrile Diseases (southern Nigeria)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2024'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.5281/zenodo.13756418
- https://doi.org/10.1186/s12879-026-13434-z
- https://doi.org/10.20944/preprints202501.1310.v1
- https://doi.org/10.4258/hir.2025.31.2.125
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 4,868 febrile patients from four southern Nigerian states (May-December 2021) with rated symptoms, risk factors and diagnoses confirmed after blood film, serology and blood counts; a symptom-based malaria or typhoid diagnosis task with a named decision, on a restricted Zenodo deposit with severity-coded labels.
- Source: "NFRF Project Patient Dataset with Febrile Diseases", Zenodo 10.5281/zenodo.13756418 (2024-09-13, CC BY 4.0, access restricted: files on request; creators University of Uyo Teaching Hospital and Mount Royal University; NFRF grant NFRFE-2019-01365): "symptoms, risk factors, suspected diagnosis, further investigation, and confirmed diagnoses". Sabi et al., BMC Infectious Diseases 2026 (doi 10.1186/s12879-026-13434-z, abstract): "data collected between May 2021 and December 2021 from four states in southern Nigeria. A total of 4,868 valid responses" (Cross River 1,531, Rivers 1,232, Akwa Ibom 1,223, Imo 882; 40% under 19). Attai et al., Healthc Inform Res 31(2):125 (2025), Sec. II.2 (read): 4,870 records; "Symptom severity was rated using a 5-point scale"; "The severity of both suspected and confirmed diagnoses was rated on a linguistic scale" of six levels, binarised as absent against levels 2-6; "Further investigations, such as blood film examination, serology, full blood counts, etc., were conducted" before the confirmed diagnoses; 3,914 records after dropping missing symptoms, children under 5 and three rare diseases (32 symptoms, 6 diagnoses).
- Use case: a health worker in a resource-limited clinic decides at first contact, from symptoms and risk factors, whether to treat or test for malaria, typhoid or another febrile illness (the HIR paper builds a mobile diagnostic tool for this); fit direct; regime IID by patient, or grouped by state to test transfer.
- Siblings and duplicates: `dengue_hematology_bangladesh` and `ed_uti_urine_culture_prediction` (other infections, other sources), `tanzania_waterborne_disease_cases` (district counts, another task); no duplicate (grep: febrile, malaria, Uzoka, Uyo). External collections: none known.
- Better data: from the curator's Zotero collection (item 56, a malaria-diagnosis ensemble paper; this table holds its task with about 7.6 times the rows); no further search this round.
- Papers and pages: the three papers above (abstracts via Europe PMC; the HIR methods in PMC12086442); Amannah, Attai and Uzoka, Preprints 202501.1310 (2025; 3,914 records; random forest, XGBoost and MLP).
- Metric: precision, recall and F1 per disease (HIR, Sec. III), several side by side and no threshold fixed (MET-5, MET-6), so the fallback `roc_auc` for one binary diagnosis; inputs none.
- Risks for /add-dataset: access on request only (noted, EV-4; the data must be obtained first); the labels are severity ratings of several diagnoses (choose malaria, the task of item 56, or one dataset per disease; `Multi-target` if shipped together); the suspected-diagnosis and investigation columns must go (LEAK-10; the HIR paper removed the suspected diagnoses); whether the symptom ratings were recorded before or after the confirmation is not stated (LEAK-13, `Class-dependent Recording` to check); the column list is not public.
- Priority: gap 0 (medical, binary and IID are not thin), use case + (the source names point-of-care diagnosis in low-resource settings), source + (an institutional deposit and three papers), shape + (4,868 patients, about 30 rated symptoms plus risk factors, four states), risk - (request-only access, a severity-coded multi-label target, unknown recording time of the symptoms).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 56: "Ensemble Machine Learning for Malaria Diagnosis in Resource-Limited Settings Using ...".
- as published: patients; 4,868 records from 4 southern Nigerian states (3,914 used in the 2025 diagnosis preprint); columns: symptoms, risk factors, suspected diagnosis, investigations, confirmed diagnoses; exact ...; target: confirmed diagnosis of malaria (also typhoid, HIV/AIDS, TB, respiratory and urinary tract infections; multi-label); access: request.
- Why: same task as item 56 (symptom-based malaria diagnosis) on 7.6x the rows from several states and hospitals
- Adds: larger febrile-illness differential-diagnosis table; check that the confirmed label comes from lab tests (SEL-7) and drop the suspected-diagnosis and investigation columns (leak)
