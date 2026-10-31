---
unique_name: radcure_head_neck_survival
name: Computed Tomography Images from Large Head and Neck Cohort (RADCURE), clinical data table
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.7937/J47W-NM11
- https://www.cancerimagingarchive.net/collection/radcure/
- https://doi.org/10.1002/mp.16972 (Welch et al. 2024, Medical Physics, data descriptor)
- 'https://doi.org/10.1158/2767-9764.crc-22-0152 (Kazmierski et al. 2023, Cancer Research Communications: crowdsourced overall-survival challenge on 2,552 RADCURE patients, external validation on 873)'
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10309070/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the clinical table of 3,346 head and neck cancer patients treated with definitive radiotherapy at Princess Margaret (UHN, Toronto) in 2005-2017, published on TCIA with a data descriptor; an institutional challenge defined 2-year overall survival, ranked by AUROC, with a split by date of diagnosis.
- Source: Welch et al., "Computed Tomography Images from Large Head and Neck Cohort (RADCURE)", The Cancer Imaging Archive, V1 2023-06-14, now V4 (2024-12-19), doi 10.7937/J47W-NM11; data descriptor Welch et al., Medical Physics 2024 (doi 10.1002/mp.16972). As published: one clinical XLSX (463 KB, CC BY 4.0) of 3,346 patients, columns grouped as demographic, diagnosis, exposure, follow-up, treatment and other, TNM 7th edition; oropharynx about 50%, larynx 25%, nasopharynx 12%, hypopharynx 5%; median age 63, 80% male; median follow-up 5 years, 60% alive at last follow-up; ages of 90 and over set to 90 and dates offset (TCIA page). The CT images and contours are under NIH controlled access and are not needed. V2 removed a column (RT_Tech) and V4 renamed the clinical columns.
- Use case: at the start of radiotherapy the oncologist estimates the patient's prognosis, which bears on treatment intensity and follow-up; the challenge paper's primary objective was "to predict 2-year overall survival (OS)" from pre-treatment data, while the actor and decision are the curation's reading (fit approximate until the paper's motivation is quoted). Regime temporal: the challenge "split into training (n = 1,802) and test (n = 750) subsets according to the date of diagnosis" (Kazmierski et al. 2023, Methods; the Results section describes a 70/30 split at 2013-12-22, a discrepancy to settle).
- Siblings and duplicates: `pharynx` (`No`, `AHDS`: the BNG-generated version of 195 RTOG trial patients), for which this was found; `raman_head_neck_cancer` (`TBD -> 2nd Tier`, Raman spectra, another task); no record of the TCIA OPC-Radiomics collection, a subset of RADCURE (TCIA page), and none of HN1 or HECKTOR. External collections: none found.
- Better data: found as better data for `pharynx`; no further search this round.
- Papers and pages: the TCIA page and the Medical Physics descriptor; Kazmierski et al., "Multi-institutional Prognostic Modeling in Head and Neck Cancer: Evaluating Impact and Generalizability of Deep Learning and Radiomics", Cancer Research Communications 3(6):1140 (2023), PMC10309070, the challenge on 2,552 RADCURE patients with external validation on HN1 (137), MDACC (627) and a private cohort (298); its preprint arXiv 2101.11935 (2021).
- Metric: `roc_auc` from the source: "The primary evaluation metric for the binary endpoint, which was used to rank the models, was the AUROC", average precision only to break ties, the C-index for the optional lifetime-risk task (Kazmierski et al. 2023, Methods); a deliberate challenge choice (MET-4, MET-5); inputs none.
- Risks for /add-dataset: the 2-year label needs the patients censored before 2 years dropped (USE-5; few, with a 5-year median follow-up); whether the year or date of diagnosis survives TCIA's date offset decides the temporal split (SPLIT-7); follow-up, recurrence and cause-of-death columns are outcomes and go (LEAK-10); the challenge's inputs were age, sex, T, N, stage, disease site, performance status, HPV status, radiation dose and systemic therapy, and dose and chemotherapy are the treatment decided at the same point (USE-4 to settle); the column set changed between versions (V2, V4), so pin the version.
- Priority: gap 0 (medical, binary, temporal are not thin), use case 0 (the challenge's task is quoted, the decision is ours), source + (TCIA, a descriptor and a challenge paper), shape + (3,346 patients, mixed clinical features, a date split).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `pharynx`.
- as published: 3,346 head and neck cancer patients treated with definitive radiotherapy 2005-2017 (about 50% oropharynx, 25% larynx, 12% nasopharynx, 5% hypopharynx); one clinical CSV/XLSX with demographic, ...; target: overall survival after radiotherapy (death status and time; the challenge predicted it as a risk score and a fixed-horizon event); access: open (clinical table CC BY 4.0 through the TCIA Data Retriever; the CT images are under NIH controlled access, not needed).
- Why: Same task as the real data behind pharynx (195 RTOG oropharynx-carcinoma trial patients, survival after radiotherapy from site, T, N, condition, grade, age, sex and treatment): the same target with the same kind of pre-treatment clinical features (site, T, N, ECOG performance status, age, sex, treatment modality), ...
- Adds: Real patients instead of Bayesian-network-generated rows; 17x the patients of the original 195; 2005-2017 instead of a 1970s trial; HPV status and smoking, which drive oropharynx prognosis today. Risks: censored follow-up (a fixed-horizon target must drop patients censored before it), ages capped at 90 and dates ...
