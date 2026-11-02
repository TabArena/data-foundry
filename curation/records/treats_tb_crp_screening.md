---
unique_name: treats_tb_crp_screening
name: TREATS community TB screening with point-of-care CRP (Zambia, South Africa, 2019)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2026'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.17037/data.00005150
- https://datacompass.lshtm.ac.uk/id/eprint/5150
- https://doi.org/10.1016/S2214-109X(23)00113-4
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: open data of a community TB screening study with point-of-care CRP, symptoms and a chest X-ray CAD score in Zambia and South Africa (2019); the reference standard exists only for the 1,777 sputum-eligible participants (117 with TB), and the file is likely a nested cut of the TREATS prevalence survey, which has its own record.
- Source: Ruperez Larrea (LSHTM), "Data for: Use of point-of-care C-reactive protein testing for screening of tuberculosis in the community in high-burden settings: a prospective, cross-sectional study in Zambia and South Africa", LSHTM Data Compass (doi 10.17037/DATA.00005150, published 2026-04-15): `CRP_dataset_open.csv` (open, CC BY 4.0), a controlled file (HIV and ART status, exact dates, medical officer comments; data sharing agreement) and a codebook. Codebook: "This is the minimal dataset required to conduct the analysis presented in the published paper", Ruperez et al., Lancet Glob Health 11(5):e704-e714 (2023, doi 10.1016/S2214-109X(23)00113-4), and "Dataset containing results of an investigation to determine the prevalence of tuberculosis (TB) among enrolled participants of the TREATS study between February 19 and August 11, 2019. Participants were aged 15 years and over and located in one of 3 communities in Zambia or 1 community in South Africa." As published (preview of the open CSV): 9,588 participants x 46 columns: five symptoms with their durations, CAD4TB score (9,533 filled), medical officer CXR review, reading and referral, enrolment month, sex, age group, TB history, current TB treatment (48), country (Zambia 7,539, South Africa 2,049), CRP value (1,593 filled) and its cut-offs, sputum eligibility ("Sputum eligible if either symptoms or CADscore>=40": 1,847), Xpert Ultra grades and culture results, and the composite reference `Xpertculture` ("Positive if Xpert Ultra final result ... or culture final results were positive for Mycobacterium tuberculosis"): 117 positive, 1,660 negative, blank for 7,811 not tested; among those with CRP 76 positive and 1,235 negative.
- Use case: the paper's: a community TB screening programme decides who goes on to confirmatory sputum testing, from symptoms, a point-of-care CRP and the chest X-ray CAD score; fit approximate: the outcome exists only for the sputum-eligible (symptoms or CAD4TB of 40 or more), so the task we can ship is triage among screen-positives, not screening of everyone. Regime IID within one survey period of six months (community is not in the open file; country ships).
- Siblings and duplicates: `treats_tb_prevalence_survey` (TREATS prevalence survey 2019-2021, 35,315 participants in the Zimmer analysis, access on request; not screened yet): the codebook places this study among "enrolled participants of the TREATS study" in 2019, so the open file is likely a cut of that survey with CRP added (a PROV-6 question for the curator: one task, which release; not confirmed from the paper); `coda_tb_clinical_triage` (CODA TB DREAM, clinic triage of people with cough; another source, PROV-7). External collections: none found.
- Better data: from the curator's Zotero collection (item 163); no further search this round.
- Papers and pages: Ruperez et al. 2023 (not read; no abstract on Crossref); Zimmer et al., medRxiv doi 10.64898/2026.03.30.26349632 (a model for community TB screening on pooled data that includes TREATS; moved here from the links, PROV-12).
- Metric: not read; a screening test is usually judged by sensitivity and specificity against the WHO target product profile, which would need the paper's threshold or operating point (MET-6, MET-7); so the fallback `roc_auc` until the paper is read. Inputs none.
- Risks for /add-dataset: columns that carry the outcome or the referral after testing, to drop: Xpert grades and results (`s1_gxp_group`, `s2_gxp_group`, `s1s2_gxp_group`, `mwrd_*`, `s1s2_gxp_group_final`), culture fields (`cult_final`, `culture_result`, `culture_eligible`), and the medical officer's referral (`mo_tbreferral`, `mo_referral`, which codes "referred for TB-treatment (bacteriologically)") (LEAK-10); verification bias, the reference only for the sputum-eligible; the CAD4TB score is a chest X-ray model output (SEL-13 against SEL-14: CAD scores are combined with symptoms in screening algorithms; decide); CRP measured on only 1,593 participants, by offer (missing not at random); about 23 positives per test fold in 5-fold CV over the 1,777 labelled; HIV status only in the controlled file.
- Priority: gap 0 (medical, binary and IID are covered), use case + (the paper's screening decision), source + (LSHTM repository, codebook, Lancet Global Health paper), shape 0 (1,777 labelled participants, 117 with TB), risk - (verification bias, leak columns, a likely cut of a recorded survey).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 163: "Development and validation of a machine learning model for community-based tuberculosis ...".
- as published: 9,588 enrolled, 1,588 with CRP results, 76 TB cases among the sputum-eligible (paper); open CSV of about 55 columns (sex, age band, country, TB history, 5 symptoms with durations, CRP, CAD4TB score, ...; target: TB by Xpert Ultra or culture (binary); access: open.
- Why: Real, open data for the community TB screening task of the Zimmer paper, whose pooled data are closed.
- Adds: A public instance of community TB triage; small. Caveats: about 80 positives; verification bias (outcome only for the screen-positive plus a sample); CAD4TB is a chest X-ray model score (SEL-13 question); HIV status only in the controlled file. Access re-confirmed: open CSV (CC BY 4.0) and a controlled file.
