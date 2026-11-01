---
unique_name: nhanes_iron_deficiency_ferritin
name: NHANES ferritin + complete blood count (iron deficiency without anaemia)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/FERTIN_J.htm
- http://arxiv.org/abs/2609.22154
- https://doi.org/10.1136/bmjopen-2024-097016
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/CBC_J.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_FERTIN.htm
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: serum ferritin measured for NHANES participants aged 1-5 and 12+ (6,589 values in 2017-2018, 10,557 in the 2017-March 2020 file) with the complete blood count; the screen for iron deficiency without anaemia that Efros et al. 2025 define on private EHR data (ferritin < 30 ng/mL at normal haemoglobin, AUC 0.814) can be built on public data.
- Source: CDC/NCHS NHANES laboratory files: Ferritin FERTIN_J (2017-2018, first published April 2020; "Examined participants 1-5 years old and 12 years and older were eligible"; 7,332 records, 6,589 with LBXFER; Roche Cobas e601) and P_FERTIN (2017-March 2020 pre-pandemic, first published July 2021; the same eligibility; 10,557 values; it pools the 2017-2018 participants with 2019-March 2020). FERTIN_I (2015-2016) and FERTIN_L (2021-2023) cover only children 1-5 and females 12-49. Joined by SEQN to the complete blood count (CBC_J or P_CBC), demographics and optionally the biochemistry profile.
- Use case: Efros, Soffer, Mudrik, Robinson, Kenet, Nadkarni and Klang, "Predictive machine-learning model for screening iron deficiency without anaemia: a retrospective cohort study", BMJ Open 2025 (doi 10.1136/bmjopen-2024-097016): a clinician with a routine blood count of a non-anaemic adult decides whether to test ferritin or treat; target "low ferritin levels (<30 ng/mL)" in adults with haemoglobin >= 130 g/L (men) or >= 120 g/L (women); fit approximate here (a population survey, not patients sent for a ferritin test); regime IID by participant (cross-sectional), temporal by wave only if cycles are pooled.
- Siblings and duplicates: `dhs_childhood_anemia` (`TBD -> Yes`; anaemia by haemoglobin in children, another target); the other NHANES records of this run (`nhanes_ckd_screening`, `nhanes_liver_elastography_fibrosis`, `nhanes_dxa_body_fat` and more) are other tasks of the same survey (PROV-7). No iron-deficiency record (grep: ferritin, iron deficiency). External collections: none known.
- Better data: from the curator's Zotero collection (item 284, Lotfian Delouee et al., arXiv 2609.22154, which names iron-deficiency screening as one of two case studies and no dataset in its abstract); no further search this round.
- Papers and pages: the FERTIN_J, P_FERTIN, FERTIN_I and FERTIN_L codebooks (read); the Efros et al. abstract (Europe PMC, read; 211,486 Mount Sinai adults, 19.56% low ferritin; their data is not public).
- Metric: Efros et al. report AUC (0.814, against 0.741 for a blood-count-only model) with specificity, PPV and NPV at a 70% sensitivity of their choosing, the AUC as the headline but not a declared criterion (MET-5); the fallback `roc_auc` is the same; inputs none.
- Risks for /add-dataset: the label is the task paper's cut-off (ferritin < 30 ng/mL) on non-anaemic participants by its haemoglobin thresholds (USE-5); the iron panel (serum iron, TIBC, transferrin saturation), the transferrin receptor and ferritin itself must be left out (LEAK-10); children 1-5 need other thresholds, so restrict to adults as Efros did; menstruating women carry most positives; joins on SEQN across 3-4 files; survey weights not used.
- Priority: gap 0 (medical & healthcare, binary and IID are not thin), use case 0 (the decision is named by Efros for an EHR population; on survey data the fit is approximate), source + (NCHS codebooks and lab methods), shape + (about 10,000 ferritin values in 2017-March 2020, blood count and demographics), risk 0 (the cut-off is fixed by the task paper; the leaking columns are known).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 284: "A Comparative Framework for Evaluating Foundation Models on Tabular Data: A Case Study ...".
- as published: participants, 6,589 with ferritin in 2017-2018 (ages 1-5 and 12+), joined on SEQN to CBC and demographics; more rows if earlier cycles are pooled; target: low serum ferritin (iron deficiency; threshold e.g. < 30 ng/mL), restricted to participants without anaemia; access: open.
- Why: A lead for the task the paper frames, not a dataset the paper uses: the public counterpart of the private Mount Sinai cohort (Efros 2025). Measured lab target, features known when the CBC is drawn, open data.
- Adds: No iron-deficiency record exists. Caveat: the label is a ferritin threshold the curator must fix; iron-panel columns (TSAT, serum iron) would leak and must be excluded.
