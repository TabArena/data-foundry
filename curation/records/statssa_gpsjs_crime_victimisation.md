---
unique_name: statssa_gpsjs_crime_victimisation
name: Governance, Public Safety and Justice Survey (GPSJS), successor of the Victims of Crime Survey
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: social science
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/1091
- https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/980
- https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/948
- https://www.statssa.gov.za
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: Statistics South Africa's crime-victimisation survey (GPSJS, which absorbed the Victims of Crime Survey), household and individual files per wave on DataFirst under CC BY; documented and in a thin domain, but the survey defines no prediction task and the victimisation label comes from the same interview as the features (SEL-7), as on the Zindi record it was found for.
- Source: Statistics South Africa, Governance, Public Safety and Justice Survey, distributed by DataFirst (University of Cape Town): 2022-2023 (catalog 948, fieldwork April 2022 to March 2023), 2023-2024 (catalog 980), 2024-2025 (catalog 1091, "Round 4", doi 10.25828/56HE-TF09), each "Public access data for use under a Creative Commons CC-BY (Attribution-only) License". As published (study pages): "a household file and an individual file"; a design of "an expected sample of approximately 33 000 dwelling units" from 3,324 primary sampling units; household crimes answered by a proxy, usually the head, individual crimes by a selected member aged 16 or older; the 5-year question "In the past 5 years have you or any member of the household experienced any of the following crimes?" kept unchanged for trends, and a 12-month series. The series began in April 2018 and absorbed the Victims of Crime Survey (catalog 948). Case and variable counts are not on the study pages; the run's counts (about 19,000 to 21,000 individuals a wave, five waves from 2018/19) were not verified, and the record links three waves.
- Use case: none in the source (national statistics on crime and on views of police and courts). The Zindi task the record was found for asks for "a woman's level of risk of being victimized by a crime given basic information about her and her life", without an actor or a decision; a programme that targets people at risk would be ours; fit approximate at best. Regime IID within a wave (households and sampling units as groups), or temporal across waves.
- Siblings and duplicates: `womens_mentorship_hackathon` (AI `TBD -> 2nd Tier`, priority 2: Zindi's women's-safety table, about 7,700 labelled women, crime in the last five years, DataFirst and Stats SA named as partners). Its survey wave is not confirmed; the Victims of Crime Survey is the likely origin (DataFirst also holds VOCS 2011-2018). If confirmed, these waves are newer releases of its source (PROV-6) and the curator decides which one enters. External collections: none found.
- Better data: found as better data for `womens_mentorship_hackathon`; no further search this round.
- Papers and pages: the DataFirst study pages (DDI metadata, questionnaires and reports, not opened); Stats SA's GPSJS statistical releases.
- Metric: none for the survey; the Zindi precursor scored ROC AUC (MET-4 there), so `roc_auc` for a binary victimisation target, which is also the fallback (MET-1, MET-8); inputs none; the survey weights are never a feature.
- Risks for /add-dataset: SEL-7: the respondent knows the label, asked in the same interview as the features, so keep only what is fixed before the reference period (age, sex, household, place) and drop answers that can follow a crime (feeling unsafe, avoidance, reporting, trust in the police; LEAK-10); household crimes come from a proxy; the target (which crime, 12 months or 5 years, the person or the household) is ours to define (USE-5); questionnaire changes between waves (PROV-13); weights and sampling units.
- Priority: gap + (social science has 1 accepted dataset), use case 0 (no decision in the source), source + (Stats SA with DDI documentation), shape + (about 33,000 dwelling units a wave by design, several waves), risk - (SEL-7 and answers that follow a crime).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `womens_mentorship_hackathon`.
- as published: individual files (one person aged 16+ per household, CAPI): 18,970 (2018/19, 494 vars), 19,655 (2019/20), 20,543 (2022/23), 21,050 (2023/24), 20,703 (2024/25, 294 vars); household files of the same ...; target: whether the respondent was a victim of a given crime (individual crimes in the past 12 months; the 5-year question is kept unchanged from VOCS); access: open.
- Why: the record's Zindi table (~11,000 women, crime in the last 5 years, DataFirst and Stats SA named as partners) is suspected to come from Stats SA's Victims of Crime Survey; GPSJS is that series' continuation with the same victimisation questions, so the same target and the same kind of respondent features
- Adds: named, documented first publication with a codebook (the record's wave is unknown), five full yearly waves for a temporal split, 2-3x the women per wave, newest wave 2024/25; CC-BY on DataFirst (DataFirst also holds VOCS 2011-2018). Same SEL-7 risk: the label and the features come from one interview
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
