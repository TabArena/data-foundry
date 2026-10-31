---
unique_name: sinan_dengue_case_screening
name: 'SINAN dengue notifications (Brazil, DATASUS): suspected cases with symptoms, comorbidities and final classification'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://dadosabertos.saude.gov.br/dataset/arboviroses-dengue
- https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Dengue/dic_dados_dengue.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Brazil's national notifications of suspected dengue (SINAN, Ministry of Health), millions of rows a year with symptoms, signs and comorbidities filled at notification and a final classification after investigation; screening at first contact is a published task, and the label is clean only where a laboratory decided it.
- Source: Ministério da Saúde (CGARB and CGIAE, SVSA), "Sinan/Dengue" on the Portal de Dados Abertos do SUS (page read): yearly files 2000-2026 and a combined file, updated weekly (page created 22 February 2024, last update 31 October 2026), with a data dictionary of 14 July 2025 (`dic_dados_dengue.pdf`, 22 pages, read). Row counts are not on the page (the run's note: 6,484,890 notifications in 2024). Fields in the dictionary: clinical signs from `febre` to `leucopenia` and `laco` (tourniquet test), comorbidities (`diabetes`, ...), laboratory results and `sorotipo`, `hospitaliz`, `classi_fin` (1 confirmed, 2 discarded, 8 inconclusive), `criterio` (1 laboratory, 2 clinical-epidemiological, 3 clinical), `evolucao`, `dt_sin_pri`. Licence: the portal states CC BY-ND 3.0 (a note only, EV-4).
- Use case: a physician at a health unit, when a suspected case is notified, decides whether to manage and follow it as dengue before or without a laboratory result, from symptoms, signs, age and sex; Bohm et al. 2024 build models "to assist in medical decision-making based only on clinical data". Fit direct for the notifications a laboratory decided. Regime temporal: a model built on past seasons is used in the next (by notification date or epidemiological week); states are a possible grouping.
- Siblings and duplicates: `dengue_hematology_bangladesh` (`TBD -> 2nd Tier`, two Bangladeshi hospital releases with blood counts; another source and feature kind, PROV-4). No other SINAN or DATASUS record (grep: sinan, datasus, dengue). External collections: none found.
- Better data: from the curator's Zotero collection (item 303); no further search this round.
- Papers and pages: Bohm, Borges, Silva, Soares, Ferreira, Belo, Lignon, Bruhn, "Utilization of machine learning for dengue case screening", BMC Public Health 24:1573 (2024), https://doi.org/10.1186/s12889-024-19083-8, PMC11167742 (read): Rio de Janeiro and Minas Gerais, 2016 and 2019; 229,113 confirmed and 135,163 discarded by laboratory criteria among more than 882,612 notifications; laboratory fields dropped; "a random selection of 10,000 confirmed cases and 10,000 discarded cases", a 70/30 split with 10-fold CV; logistic regression with 10 variables. The record's arXiv link (2610.14813, Naimeen and Soberanis 2026) is the Bangladesh study on other data. Both links moved here from source_links as related work (PROV-12); the dictionary PDF was added.
- Metric: Bohm et al. report accuracy, recall, specificity, precision, F1 and AUC side by side (Methods, model evaluation) with no single criterion, so the fallback `roc_auc` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: keep the notifications decided by laboratory (`criterio` = 1) and drop laboratory results, serotype, `criterio`, `evolucao`, hospitalisation and closing dates (LEAK, USE-3); `classi_fin` codes differ by year (the 2025 dictionary has 1, 2, 8; older files are known to use 5 for discarded and 10-12 for the dengue classes; check per year); symptom fields may be empty in early years; the size calls for a cut (recent years, or a 1M cap); `leucopenia` is a blood-count result, known at notification only when a count was done (USE-3).
- Priority: gap 0 (medical, binary and temporal covered), use case + (Bohm et al. name the clinical screening decision), source + (the Ministry's release with a data dictionary), shape + (millions of notifications, mixed types, many years and states), risk - (a clean label only where a laboratory decided, and codes that changed over the years).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 303: "Machine Learning-Based Prediction of Dengue Infection Using Clinical and Hematological ...".
- as published: notified suspected dengue cases, one row per notification. Yearly files 2000-2026, a combined file and a data dictionary (14/07/2025). Row counts are not on the page. 2024 alone had 6,484,890 ...; target: final classification (CLASSI_FIN): confirmed dengue vs discarded, as in Bohm et al. 2024 (laboratory-confirmed vs discarded); alternative: severity class ...; access: open.
- Why: Real, national, open surveillance microdata for the task of item 303 (dengue diagnosis at first presentation), already used for ML dengue screening in the study the paper cites.
- Adds: Better data for dengue diagnosis: far larger, with many years and states (temporal and state-grouped splits). Caveats: the portal licence is CC BY-ND 3.0 (no derivatives; check whether a curated subset is allowed). The lab-result columns define the label and must be dropped. Clinical-epidemiological confirmations are ...
