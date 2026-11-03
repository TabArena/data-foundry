---
unique_name: nacc_uds_dementia_conversion
name: NACC Uniform Data Set (UDS)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1097/WAD.0b013e318142774e
- https://naccdata.org/requesting-data/nacc-data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the NACC Uniform Data Set, the large multi-centre US Alzheimer's cohort with standard visit forms since 2005 and a clinician's diagnosis at every visit; the conversion target has to be built from consecutive visits, and access is by request.
- Source: Beekly, Ramos, Lee, Deitrich, Jacka et al., "The National Alzheimer's Coordinating Center (NACC) Database: The Uniform Data Set", Alzheimer Dis Assoc Disord 2007 (https://doi.org/10.1097/WAD.0b013e318142774e): "NACC implemented the UDS (September 2005) by developing data collection forms for initial and follow-up visits", collected "longitudinally, to better characterize ADC participants with mild Alzheimer disease and mild cognitive impairment in comparison with nondemented controls" (abstract). As published now (naccdata.org, "Requesting data"): "56,000+" participants and "217,000+" visits, 3.7 per participant on average; health history, CDR, GDS, NPI-Q, FAS, a neuropsychological battery and the clinical diagnosis, with MRI, amyloid PET, CSF, APOE and neuropathology for subsets; "Available free to researchers worldwide" through a request and a data use agreement that keeps the data "solely by the individuals identified in the data request". The year is the snapshot we pin (PROV-9).
- Use case: a memory-clinic clinician at a visit judges whether a cognitively normal or MCI patient will progress by the next visit, to set follow-up, refer to a trial or weigh treatment (our reading: the UDS is a research database and names no decision); fit approximate (ADRC participants are volunteers and referrals, a `Selection Bias` to weigh; visit intervals vary, so the horizon must be fixed). Regime grouped by participant (several visits each) or by ADRC centre, or temporal by visit date; one to pick (SPLIT-3).
- Siblings and duplicates: `nacc_mci_progression` (this run; NACC UDS, stable against progressive MCI at 3 years) is a cut of this dataset and proposed as its `Duplicate` (PROV-4, PROV-6); its framing is kept here: stable against progressive MCI on the MCI participants is the binary alternative to the three-class diagnosis at the next visit (problem_type is a choice), and it came from the curator's Zotero collection (item 133, the AutoML-Multiverse paper below). `tadpole` (`TBD -> 2nd Tier`; ADNI) is another cohort, no duplicate (PROV-4); so are `dementia_prediction` (`Yes (Disagreement)`, OASIS longitudinal) and `oasis3_dementia_status` (this run). The ADNI link that sat in this record's source links (https://adni.loni.usc.edu/data-samples/adni-data/) is TADPOLE's source, moved here (PROV-12). External collections: none among the records.
- Better data: found as better data for `tadpole` (about 56,000 participants against TADPOLE's ADNI extract of about 1,700); no further search this run.
- Papers and pages: Beekly et al. 2007 (abstract read); naccdata.org; Kohli et al., "AutoML-Multiverse: An Instability-Aware Framework for Quantifying Analytic Variability in Alzheimer's Disease Machine-Learning Studies", medRxiv 2026 (https://doi.org/10.64898/2026.03.13.26347938), which uses NACC (N ≤ 1,057 per task) next to ADNI (abstract).
- Metric: none for the database. The AutoML-Multiverse abstract reports accuracy ("stable versus progressive mild cognitive impairment (MCI) classification accuracy was 0.68±0.06 (ADNI) and 0.63±0.08 (NACC)") without a threshold or costs (full text not read); TADPOLE's diagnosis ranking is on ADNI, another source. So the fallback, `log_loss` for three classes or `roc_auc` for the binary framing (MET-5, MET-6, MET-8); inputs none.
- Risks for /add-dataset: the target is built (the diagnosis at a later visit) with a fixed horizon (USE-5, SPLIT-12); the UDS forms changed across versions and must be harmonised (`Needs extensive data wrangling`); fields of the current visit that encode the current diagnosis (CDR global, the clinician's etiology) are known at the visit, but anything filled after the next visit (neuropathology, later diagnoses) goes (USE-3); biomarkers exist for subsets, missing by centre (LEAK-13 to check); access by request with a DUA (EV-4, noted only).
- Priority: gap + (multiclass is thin), use case 0 (no decision named by the source), source + (NACC, a paper and the forms), shape + (tens of thousands of participants, mixed clinical features, grouped and temporal structure), risk - (a target to build and forms to harmonise): 3.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `tadpole`.
- as published: 56,000+ participants, 217,000+ visits (1-20 per participant, mean 3.7) from US ADRCs; health history, CDR, GDS, NPI-Q, FAS, neuropsychological battery, cognitive and etiological diagnosis; subsets ...; target: clinical diagnosis (normal / MCI / dementia) at the next visit, i.e. conversion; access: request.
- Why: TADPOLE's diagnosis target, predicted from the same kinds of visit features (demographics, cognitive scores, clinical ratings, biomarkers where present). TADPOLE is an ADNI extract (about 1,700 participants), which is also maintained through ADNI4 on LONI IDA (application and DUA): that is a version of TADPOLE's source
- Adds: About 30x the participants and many more visits, ongoing. The cognitive and clinical features cover everyone, while imaging and CSF exist for subsets only. Access is by request with a DUA that limits use to named researchers, so redistribution is barred, like ADNI
