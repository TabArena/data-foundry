---
unique_name: sinan_dengue_case_screening
name: 'SINAN dengue notifications (Brazil, DATASUS): suspected cases with symptoms, comorbidities and final classification'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
year: '2023'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://dadosabertos.saude.gov.br/dataset/arboviroses-dengue
- https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Dengue/dic_dados_dengue.pdf
v2_path: datasets/_dev/tabarena-v0pt2/sinan_dengue_case_screening_1m/dataset.py
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

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-08):** size check on the data, while adding (`sinan_dengue_case_screening_1m`): the open yearly files of 2014-2015 and 2022-2026 hold probable cases only (no discarded case, `CLASSI_FIN` = 5, in any of them; the portal defines probable cases as every notified case but the discarded ones), so the 6.5M notifications of 2024 cannot be labelled and the task uses 2016-2021, the files that hold discarded cases. Laboratory-decided notifications there: 2,979,887 of 7,030,293 closed as dengue or discarded (42%); 2,623,839 rows after dropping those without the form's clinical section (the signs came into use in the first half of 2016). Temporal, three half-year windows from July 2020 to December 2021 with a two-month gap; train sides over 1M, so the `_1m` version. Classification codes as the screening expected (5 discarded, 10-12 dengue; 1-4 on a few older-form 2016 rows); the place of infection and work-relatedness fields are erased when a case is discarded (LEAK-10). Untuned probes: ROC AUC 0.69-0.70 (Bohm et al.'s 0.985 on a balanced random sample is not reached; corrected 2026-11-09: it cannot be reproduced with their ten variables on these rows, logistic regression ROC AUC 0.578 on their own cohort and sampling).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the notifications made after a dengue sample was taken dropped by the sample dates, 2,253,525 rows left; a one-month gap; the surveillance team as the actor, USE-9 asked; `Selection Bias` with the cohort's numbers; roc_auc kept with its reason corrected; year 2023; the occupation's unknown codes missing and SINAN's own codes decoded; the copies of one patient as a proposed exception to LEAK-19); disputed: SPLIT-15 against SPLIT-20 (the window set); for the curator: issues 1-4 (the window set; the one-patient copies, a LEAK-19 exception to confirm; USE-6, optional activity counts; CLEAN-12, the CBO codes, alike for rais and wioa). Priority 3: gap 0, use case 0 (the source's physician takes no decision on the score; the surveillance team's use is ours and approximate), source + (the Ministry's national release with a data dictionary), shape + (2.25M rows, mixed types, temporal), risk 0 (no open issue raises a leak or an unclear target).
