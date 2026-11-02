---
unique_name: bsnip1_psychosis_eye_movement
name: 'Bipolar & Schizophrenia Consortium for Parsing Intermediate Phenotypes (B-SNIP 1), NDA Collection #2274'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Selection Bias
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
source_links:
- https://doi.org/10.15154/tnzs-a323
- https://nda.nih.gov/edit_collection.html?id=2274
- https://doi.org/10.1176/appi.ajp.2013.12101339
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3934403
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5682604/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the B-SNIP 1 consortium's phenotyping of 2,440 people (psychosis probands, relatives, controls) on the NIMH Data Archive, eye tracking for 1,499; a diagnosis label for established, treated cases fits no clinical decision, the eye-movement measures must be derived from per-subject experiment files, and access goes through an NDA data use request.
- Source: Bipolar & Schizophrenia Consortium for Parsing Intermediate Phenotypes (B-SNIP 1), NDA Collection #2274 (PI Carol Tamminga; doi 10.15154/tnzs-a323; collection created 2014-12-09, initial shares mostly 2017); cohort paper Tamminga et al., Am J Psychiatry 2013 (doi 10.1176/appi.ajp.2013.12101339; 933 probands, 1,055 relatives, 459 controls per the run's Assessment, not re-read). As published (collection page, read 2026-10-31): 2,440 subjects shared; clinical assessments (demographics, medications, PANSS-based interview, Montgomery-Åsberg and Young Mania scales, Barratt, Social Functioning Scale), cognition (BACS, WMS-III, WRAT4), EEG subject files (1,532), "eye tracking subject-experiment data" (1,499; pro-saccade, antisaccade, ramp-mask-ramp pursuit, gaze contingency), imaging (1,098). Whether eye-tracking summary measures ship is not stated.
- Use case: none clear. The consortium: "The founding goal of establishing disease biomarkers for current psychotic diagnoses has been poorly met, because the cognitive, electrophysiologic, eye movement, and brain imaging biomarkers did not regularly discriminate individuals with different DSM psychosis diagnoses" (Tamminga et al., Schizophr Bull 2014, doi 10.1093/schbul/sbt179, Abstract). A psychiatrist diagnoses by interview, and the cases here are established and medicated; fit approximate at best (a biomarker aid to diagnosis). Regime grouped by family (relatives of probands), with five sites.
- Siblings and duplicates: `schizo` (`TBD -> 2nd Tier`; Rubin & Wu 1997, 43 + 43 subjects), the record this was found for; `gse147221_schizophrenia_methylation` (`TBD -> 2nd Tier`, priority 1: "no clinical decision fits established cases"), the closest precedent. External collections: not searched (web search budget used up).
- Better data: found as better data for `schizo` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: Tamminga et al. 2013 (AJP) and 2014 (Schizophr Bull); the B-SNIP GWAS of smooth pursuit and antisaccade, Transl Psychiatry 2017 (doi 10.1038/tp.2017.210: eye-movement measures of 849 participants, schizophrenia 230, schizoaffective 155, psychotic bipolar 206, controls 258, Abstract); the B-SNIP biotypes are clusters (SEL-4), not a target.
- Metric: none found (the papers compare groups and run association studies; no classifier is scored), so the fallback `roc_auc` for a binary diagnosis (MET-1, MET-8); inputs: family and site for the split, never features.
- Risks for /add-dataset: access needs an NDA account and an institutional data use certification (no criterion, EV-4, but nothing can be redistributed); the eye-movement measures are to be derived from per-subject experiment files (`Needs extensive data wrangling`); antipsychotics and illness duration act on eye movements and cognition (a confound of established cases); probands recruited from clinics and controls from the community (`Selection Bias`); relatives share families with probands (LEAK-17, SPLIT-26); which contrast to ship (schizophrenia against controls, or among the psychoses) is open (USE-5).
- Priority: gap 0 (medical & healthcare and binary not thin), use case 0 (no decision fits established cases), source + (the NDA collection and its cohort papers), shape 0 (the tabular measures do not exist as published), risk − (derivation, medication confound, request access).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `schizo`.
- as published: 2,440 subjects shared on NDA (AJP 2013: 933 probands with schizophrenia, schizoaffective or psychotic bipolar I disorder, 1,055 first-degree relatives, 459 healthy controls); eye-tracking experiment ...; target: DSM-IV diagnosis: schizophrenia (or schizoaffective / psychotic bipolar) vs healthy control; access: request.
- Why: same target (schizophrenia vs healthy) and same kind of features (smooth-pursuit gain and saccade measures from a standard eye-tracking protocol, Eyelink II at 500 Hz, the same protocol at all sites) as the Rubin and Wu 1997 data behind schizo
- Adds: about 1,500 people with eye tracking against the 43 + 43 subjects of Rubin and Wu, five sites, the 2000s instead of the 1990s, several psychosis groups and relatives. Caveats: the eye-tracking data are shared as per-subject experiment files, so the summary measures must be derived (extensive wrangling); NDA's data ...
