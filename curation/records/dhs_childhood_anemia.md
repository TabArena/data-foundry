---
unique_name: dhs_childhood_anemia
name: 'DHS children''s recode: childhood anaemia (hemoglobin-tested children 6-59 months, 16 countries)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://dhsprogram.com/data/
- https://arxiv.org/abs/2605.26589
- https://github.com/yusufbrima/anemiafoundationmodel
- https://api.dhsprogram.com/rest/dhs/data?indicatorIds=CN_ANMC_C_ANY&f=json&perpage=1000
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: anaemia measured by a haemoglobin test in children 6-59 months of 16 national DHS surveys (2008-2024; 68,856 children after the paper's cleaning), predicted from the child, mother and household answers of the same visit; a lab-measured target with a published leave-one-country-out protocol, to be assembled from 16 children's recode files behind a DHS registration.
- Source: the DHS Program (ICF, funded by USAID), the children's recode (KR) file of each national survey, one release per survey; the task as defined by Brima et al., "Few-shot Cross-country Generalization of Tabular Machine Learning and Foundation Models for Childhood Anemia Prediction under Distribution Shift", arXiv 2605.26589 (2026-05-26). As published: one KR file per survey, one row per child under five of an interviewed woman, several hundred recode variables; the anaemia level `hw57` (WHO thresholds adjusted for altitude) exists only for tested children 6-59 months. The paper (Table 1, Fig. 10): 152,230 KR rows, 80,493 without `hw57`, 2,881 out of age, 68,856 analysed (Guatemala 2014-15 9,987, DRC 2021-22 9,002, Mali 2023-24 6,086 ... Armenia 2015-16 1,313; Bolivia 2008 the oldest, Malawi 2024 the newest); predictors (Table 2): child age `hw1`, sex `b4`, height-for-age and weight-for-age z-scores `hw70`/`hw72`, recent illness `h22`/`h11`/`h31`, deworming `h43`, vitamin A `h34`, mother's age, age at first birth, education and smoking, wealth `v190`/`v191`, residence `v025`, water, sanitation, household structure, parity, altitude `v040`; target any anaemia (mild, moderate, severe merged) against none. The DHS API lists the child-anaemia indicator (CN_ANMC_C_ANY) for 177 surveys in 57 countries, 2000-2024, so the pool can grow. Access: free DHS registration with a project description; the terms bar redistribution (a note, EV-4). The GitHub repository (MIT) holds code only (extract, harmonize, LOCO scripts), no data.
- Use case: a nutrition programme or community health worker, at a household or clinic visit, flags children likely to be anaemic for a haemoglobin test, iron supplementation or deworming, from what the visit records (the paper: prediction for countries with little data); fit approximate (a household survey stands in for the visit, and the finger-prick test itself is cheap where a HemoCue is at hand). Regime grouped: by country, as the paper's leave-one-country-out; within a survey, children cluster by mother and sampling cluster (`v001`), so never a plain IID split.
- Siblings and duplicates: `dhs_child_anemia` (this batch) holds the same DHS KR anaemia target for Zambia 2018/2024 and the pooled surveys: a cut of the same source, proposed `Duplicate` (PROV-6) with this record kept. Other DHS records: `indonesia_dhs_2017_contraceptive_method` (another target), `economic_well_being_prediction_challenge` (a wealth target); `nhanes_iron_deficiency_ferritin` (US, another source). External collections: none found (the paper's own benchmark only).
- Better data: from the curator's Zotero collection (item 199); no search for better data in this run.
- Papers and pages: Brima et al. 2026 (arXiv 2605.26589, code github.com/yusufbrima/anemiafoundationmodel); Zulu et al., medRxiv 2025-08-03 (doi 10.1101/2025.08.01.25332670): ZDHS 2018, 7,743 children, 58.5% anaemic, XGBoost AUC 0.673; the DHS recode manual for the variable definitions.
- Metric: `roc_auc`, the paper's declared primary metric (Sec. 2.8: "Our primary metric was the area under the receiver operating characteristic curve (AUC-ROC)"), with accuracy, precision, recall, F1, Brier and ECE as secondary (Table 3 sorts by Brier); a deliberate choice (MET-5); inputs: the country as the group, to ship as a column.
- Risks for /add-dataset: never ship the haemoglobin values (`hw53`, `hw56`) or other anaemia fields as features (LEAK-10); decide whether the mother's anaemia (`v457`, measured in the same visit; the Zambia paper's second predictor) is known at the prediction point (USE-3); harmonize 16 KR files across DHS recode phases (the paper's Table 4: 53% of rows miss a predictor, all of Jordan) (`Needs extensive data wrangling`); the survey weight `v005` is for estimation, never a feature; DHS registration to build (EV-4).
- Priority: gap 0 (medical & healthcare, binary and grouped are not thin), use case 0 (approximate fit), source + (DHS recode documentation and the paper), shape + (68,856 children, mixed child, mother and household features, a country grouping), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 199: "Few-shot Cross-country Generalization of Tabular Machine Learning and Foundation Models ...".
- as published: children aged 6-59 months with measured hemoglobin: 68,856 rows after cleaning (152,230 raw KR rows) from 16 national surveys 2008-2024 (Guatemala 9,987, DRC 9,002, Mali 6,086 ... Armenia 1,313). ...; target: anaemia yes/no: DHS hw57 (hemoglobin < 11 g/dL, adjusted for altitude); hemoglobin itself is not a feature; access: registration.
- Why: Real, nationally representative surveys with a lab-measured outcome and a documented codebook (DHS recode manual). Country gives a natural grouped split (leave-one-country-out), as in the paper.
- Adds: A child global-health and nutrition classification task with a grouped regime; the only DHS-based record today is economic_well_being_prediction_challenge (a wealth target). Caveats: the target threshold uses altitude (v040 is also a feature, fine as it is known); DHS terms bar redistribution (licence note only).
