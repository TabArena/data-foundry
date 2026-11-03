---
unique_name: oasis3_dementia_status
name: 'OASIS-3: Longitudinal Neuroimaging, Clinical, and Cognitive Dataset for Normal Aging and Alzheimer Disease'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2019'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1101/2019.12.13.19014902
- https://sites.wustl.edu/oasisbrains/home/oasis-3/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: OASIS-3 (LaMontagne et al. 2019), 1,378 Knight ADRC participants aged 42 to 95 with 2,842 MR sessions, UDS clinical forms and a FreeSurfer volumes spreadsheet; the newer, larger release of the project behind the accepted `dementia_prediction` (OASIS-2), so the curator picks one OASIS release (PROV-6). Access by request.
- Source: Washington University Knight ADRC, OASIS project page (https://sites.wustl.edu/oasisbrains/home/oasis-3/): a "retrospective compilation of data for 1378 participants" (the page also says 1379), 755 cognitively normal and 622 at stages of cognitive decline, about 30 years of data, 2,842 MR, 2,157 PET and 1,472 CT sessions; UDS forms A1-D2, psychometrics, FreeSurfer and PUP output spreadsheets, amyloid Centiloids. Paper: LaMontagne et al., medRxiv 2019, doi:10.1101/2019.12.13.19014902 (not read here). Access: a request on the project page, then NITRC-IR registration.
- Use case: none stated by the release (a data-sharing project). A candidate, as for OASIS-2: a memory clinic judges dementia status from an MRI's volume measures with age, sex and education; written by the curation, fit approximate (research volunteers, a clinical rating as the label). Regime grouped by participant (repeated visits and scans).
- Siblings and duplicates: `dementia_prediction` (OASIS-2, 150 subjects and 373 visits; `Yes (Disagreement)`, shipped in BeyondArena, markers `Wrong Domain / Source Modality`, `Time-series (Classification)`, `Selection Bias`; AT: "we need to quickly talk about how we proceed with medical image data"); `oasis1_dementia_mri` (OASIS-1, 416 subjects; `TBD -> 2nd Tier`, priority 1); `nacc_uds_dementia_conversion` (NACC UDS, to which Knight ADRC also reports, so participants may overlap; not checked). External collections: none found for OASIS-3.
- Better data: found as better data for `dementia_prediction`; no further search this round.
- Papers and pages: the OASIS-3 page; the medRxiv paper (not read). Papers that classify dementia on OASIS-3 were not searched: the session's web search budget ran out.
- Metric: none found (the release defines no task; the OASIS-2 sibling declared the fallback), so the fallback `log_loss` for a three-class status, `roc_auc` if binary (MET-1, MET-8).
- Risks for /add-dataset: build the target per MR session from the nearest clinical visit (CDR or the clinician's diagnosis) within a stated window (USE-5); CDR, MMSE and the diagnosis forms of that visit restate the label (LEAK-10); FreeSurfer regional volumes come from an image pipeline, the SEL-13 and SEL-15 question the curators left open on `dementia_prediction`; joins of the clinical, MR-session and FreeSurfer tables by participant and days since entry (`Needs extensive data wrangling`); research volunteers rather than clinic patients (the `Selection Bias` of the sibling, to check); the data use terms are noted, not weighed (EV-4).
- Priority: gap + (multiclass is thin), use case 0 (written by the curation), source + (the institution's page and a paper), shape + (1,378 participants, thousands of sessions, grouped), risk - (image-derived volumes, a target built across tables, a version of an accepted release).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `dementia_prediction`.
- as published: 1,378 participants (755 cognitively normal, 622 at stages of cognitive decline), ages 42-95, about 30 years of Knight ADRC data, 2,842 MR sessions; UDS clinical forms, psychometrics and a FreeSurfer ...; target: Clinical dementia status per visit (CDR / clinician diagnosis), as the OASIS-2 Group (nondemented, demented, converted) is derived; access: registration.
- Why: Same source family and same task as dementia_prediction (OASIS-2 with 150 subjects and 373 visits): dementia status from MRI-derived volumes (and demographics), with the same kind of features and the participant id for a grouped split
- Adds: About 9x the participants and 7x the MR sessions, regional FreeSurfer volumes instead of three global measures (eTIV, nWBV, ASF), a longer follow-up for converters; NACC's Uniform Data Set (tens of thousands of participants, by request) is a still larger alternative not checked here
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: two releases of the OASIS project behind the accepted `dementia_prediction`; pick one release (`oasis1_dementia_mri`; PROV-6). The curator keeps one, or both as distinct tasks.
