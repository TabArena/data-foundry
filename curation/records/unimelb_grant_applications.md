---
unique_name: unimelb_grant_applications
name: 'University of Melbourne grant applications (Kaggle 2011): will the grant be awarded'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2010'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/unimelb
- https://vincentarelbundock.github.io/Rdatasets/doc/modeldata/grants_other.html
- https://doi.org/10.1007/978-1-4614-6849-3
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the University of Melbourne's grant applications of 2005-2008 (Kaggle "Predict Grant Applications", 2010-2011, scored by AUC): whether an application succeeds, from its sponsor, category, value band, research codes and up to 15 investigators' records; a real institutional decision with a leaderboard metric and a textbook case study, in a wide per-investigator layout to reshape.
- Source: Kaggle competition `unimelb`, "Predict Grant Applications" (https://www.kaggle.com/competitions/unimelb; Kaggle API on 2026-10-31: opened 2010-12-13, deadline 2011-02-20, 5,000 USD, 203 teams, "This task requires participants to predict the outcome of grant applications for the University of Melbourne"); files unimelb_training.csv (3,577,489 bytes, labelled), unimelb_test.csv (919,446 bytes, labels hidden), unimelb_example.csv. Kuhn and Johnson, Applied Predictive Modeling (Springer 2013, https://doi.org/10.1007/978-1-4614-6849-3) use it as a case study; the modeldata R package ships their processed version (Rdatasets `grants_other` and `grants_test`: "These data are from a 2011 Kaggle competition sponsored by the University of Melbourne", grants of 2005-2008, 6,633 before 2008 for training, 1,557 of 2008 for validation and 518 of 2008 for test; predictors aggregated by investigator role, among them country of birth, language, PhD, department, faculty, prior successful and unsuccessful grants, A*, A, B and C publications, years in the university, RFCD codes, contract value band, sponsor and grant category). About 8,708 labelled applications (6,633 + 2,075), to confirm on the Kaggle file.
- Use case: the university's research office, when an application is lodged, estimates its chance of success to decide where to put support and review effort (the Rdatasets page: the university wanted to triage applications and learn which factors predicted success); fit direct; regime temporal by grant start date (Kuhn and Johnson train before 2008 and test on 2008; whether the Kaggle test file is a later period was not checked) (SPLIT-6).
- Siblings and duplicates: no record holds it (grep by unimelb, grant appl, grants_other); the modeldata and Rdatasets copies are processed derivatives of the Kaggle file, so build from the Kaggle raw (PROV-8, PROV-15). External collections: Rdatasets (modeldata).
- Better data: from the curator's Zotero collection (item 131, the Rdatasets index); no further search this round.
- Papers and pages: the Kaggle competition (API metadata; the data page needs JavaScript and was not read); Kuhn and Johnson 2013 (not read here); the Rdatasets documentation of `grants`.
- Metric: the leaderboard metric is "Area Under Receiver Operating Characteristic Curve" (Kaggle API, evaluation_metric), so `roc_auc` (MET-4); inputs none.
- Risks for /add-dataset: up to 15 investigators per row in repeated column blocks (aggregate per role, as the book does; CLEAN); sponsor code, person ids, department and faculty numbers are codes, with the column meanings documented (ids and category codes: no `Anonymized` marker by the pattern, to confirm); the prior successful and unsuccessful grant counts must be counted before the application date (LEAK: check against the same person's later applications); missing investigator fields may be recorded differently for successful grants (LEAK-13 probe); only the training file has labels; the download needs the competition's rules accepted (EV-4).
- Priority: gap 0 (research administration; education, the nearest domain, is thin with 3, for the curator to place), use case + (the sponsor's own decision), source + (a Kaggle competition and a textbook case study), shape + (about 8,700 applications, categorical, numeric and date fields, a time order), no known risk counted (the leak checks above are probes, not findings).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 131: "vincentarelbundock.github.io/Rdatasets/datasets.html".
- as published: Grant applications 2005-2008. Kaggle files: unimelb_training.csv 3.6 MB and unimelb_test.csv 0.9 MB (test labels hidden). Each row is one application, wide, with sponsor code, grant category, ...; target: Grant.Status (application successful); access: registration.
- Why: Real institutional records with a decision-maker named by the source, a known competition, and a textbook case study.
- Adds: A research-administration domain. Caveats: repeated per-investigator columns need reshaping; sponsor and codes are anonymized; only the training file has labels; dated 2005-2008.
