---
unique_name: sivep_gripe_sari_outcome
name: SIVEP-Gripe SRAG (severe acute respiratory illness) notifications, Brazil
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Many features
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://opendatasus.saude.gov.br/
- https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026
- '# data dictionary 2019-2025'
- https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/dicionario-de-dados-2019-a-2025.pdf
v2_path: datasets/_dev/tabarena-v0pt2/sivep_gripe_sari_outcome/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 2: Brazil's national notifications of hospitalised severe acute respiratory illness (SIVEP-Gripe, Ministry of Health), 4,060,608 rows for 2020-2024 with 194 columns and the outcome cure or death; death predicted at notification from symptoms, comorbidities, vaccination and place is a well-studied task, but 80 columns are filled later and the COVID years dominate.
- Source: Ministério da Saúde, "Banco de dados da Síndrome Respiratória Aguda Grave (SRAG) - 2019 a 2026" on the Portal de Dados Abertos do SUS (dadosabertos.saude.gov.br, the former OpenDataSUS; page read: SARI surveillance through Sivep-Gripe since 2009, widened to COVID-19 in 2020; licence "Creative Commons Atribuição"), yearly files as CSV, JSON and Parquet (INFLUD19 to INFLUD26), the data dictionary of 2019-2025 (dated 25/05/2023, "Casos de síndrome respiratória aguda grave hospitalizados") and the notification form; 2009-2018 in two older datasets. Rows from the Parquet footers (read by range request): 2020 1,206,920; 2021 1,745,672; 2022 560,577; 2023 279,453; 2024 267,986; 194 columns in each: notification, onset, admission, ICU and outcome dates, residence and notifying unit, sex, age, race, education, pregnancy, symptoms (`FEBRE` to `PERD_PALA`, `SATURACAO`), comorbidities, influenza and COVID vaccination, antivirals, `UTI`, `SUPORT_VEN`, imaging, PCR, antigen and serology results, `CLASSI_FIN`, `CRITERIO`, `EVOLUCAO` (1 cure, 2 death, 3 death from other causes, 9 unknown), genomic surveillance fields.
- The task's table: one row per hospitalised SARI notification with a known outcome (cure or death; death from other causes and unknown need a rule), at most 4,060,608 rows for 2020-2024 before that filter x about 110 columns filled at notification (demographics, residence, symptoms, saturation, comorbidities, vaccination, onset and admission dates, the admitting unit); the other 80 are filled later. Access: open, Parquet files of 21-127 MB a year, no login.
- Use case: a hospital team, when a SARI patient is admitted and notified, estimates the risk of death to decide on monitoring, ICU referral and beds. Baqui et al. (Scientific Reports 2021, doi 10.1038/s41598-021-95004-8, read through a summary of PMC8329284) model death against recovery in hospital on SIVEP-Gripe for Brazilian authorities (ranking risk factors, hospital management), so the per-patient triage framing is ours. Fit direct at notification once the later columns go. Regime temporal by notification date (waves, variants and vaccination change the risk); states are a possible grouping.
- Siblings and duplicates: `sinan_dengue_case_screening` (`Yes`, Lennart, 2026-11-08) comes from the same portal and ministry with another disease and task (PROV-7); `curial_covid_ed_triage` (`TBD -> Yes`, priority 3) and `sirio_libanes_covid_icu` (`TBD -> Yes`, priority 2) are COVID triage tasks of single hospitals with laboratory inputs, other sources. No other SIVEP record (grep: srag, sivep). External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the portal page and the dictionary (outcome and criteria fields read); Baqui et al. 2021: 231,112 PCR-positive patients of February-September 2020, XGBoost ROC AUC 0.813 on a random 80/20 split; many other mortality models on this data (not read).
- Metric: Baqui et al. rank models by ROC AUC (average precision and sensitivity at 80% specificity also reported), so `roc_auc`, which is also the fallback (MET-5, MET-8). Inputs: none.
- Risks for /add-dataset: ICU admission and dates, ventilation, imaging, every laboratory result, `CLASSI_FIN`, `CRITERIO`, the closing and typing dates and the genomic fields are filled after notification (LEAK-10, drop, as for the dengue sibling); antiviral and COVID-treatment fields need their dates checked against the notification (USE-3); `DT_EVOLUCA` and `DT_ENCERRA` time the outcome; the newest files hold open cases (LEAK-24); codes and closing criteria changed over the years (clinical closing criteria dropped for COVID on 2022-10-31, dictionary); free-text fields (`OUTRO_DES`, `MORB_DESC`, the unit's name) and ids; the 2020-2021 waves hold most rows.
- Priority: gap 0 (medical, binary and temporal covered), use case 0 (the triage framing is ours), source + (the ministry's release with a dictionary), shape + (millions of rows, about 110 mixed inputs, years and states), risk - (80 later columns, changing codes, open outcomes in the newest years).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the forms notified on or after the outcome dropped, 14.4% of the rows, LEAK-10/LEAK-6; in-stay free-text cells blanked and 3 dead-on-arrival rows dropped; the survivor-marking covid_vaccine blank and the post-admission influenza dose set to No; vaccine day counts in 30-day bins, LEAK-17; the intensive-care-on-admission group and hospital-acquired SARI named, USE-3; censoring, metric, units, licence and potential-leak notes; hospital as name [municipality code], schooling under 7 and impossible values missing, one name per municipality code, CLEAN-11/12/14); disputed: LEAK-10 (the late forms), USE-3/USE-8 (an intensive-care flag), SEL-1 (race or colour, with rais), MET-8/MET-11 (roc_auc or log_loss); for the curator: issues 1-4. Priority 3: gap 0, use case 0, source +, shape +, risk 0 (use case: bed planning and monitoring, but the per-patient framing is ours and the fit approximate, form only; shape: 790,430 admissions, mixed inputs, temporal; risk: the leaks found are fixed, one Must call to confirm).
