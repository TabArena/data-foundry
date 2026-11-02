---
unique_name: pro_act_als_progression
name: 'PRO-ACT: Pooled Resource Open-Access ALS Clinical Trials database'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
domain: medical & healthcare
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://ncri1.partners.org/ProACT
- https://doi.org/10.1212/WNL.0000000000000951
- https://doi.org/10.1038/nbt.3051
- https://hbiostat.org/data/
- https://www.re3data.org/repository/r3d100012215
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the largest pooled ALS clinical-trial database (13,717 patients from 44 phase II/III trials), behind two DREAM Prize4Life challenges that predicted the ALSFRS slope of months 3 to 12 (and survival) from the first three months of records; the per-patient table has to be built from long tables.
- Source: Pooled Resource Open-Access ALS Clinical Trials database (PRO-ACT; Prize4Life with the Neurological Clinical Research Institute at Massachusetts General Hospital), www.ALSdatabase.org and ncri1.partners.org/ProACT; first described by Atassi et al., "The PRO-ACT database: design, initial analyses, and predictive features", Neurology 2014;83(19):1719-1725 (doi 10.1212/WNL.0000000000000951; abstract via Europe PMC): "Over 8 million de-identified longitudinally collected data points from over 8,600 individuals with ALS" pooled from "16 completed phase II/III ALS clinical trials and one observational study". Today (site, read 2026-10-31): 13,717 subject records, 44 trials, more than 18 million data points: demographics, lab tests, medical and family history, clinical outcomes (ALSFRS(-R), vital capacity, survival, treatment arm). Baseline is trial entry: "survival was calculated from the time of trial entry" (Atassi, Methods). Access by registration and the site's terms (not read).
- Use case: the challenges': predict a patient's progression from the first three months of trial records; Kueffner et al. 2015 "estimate that using both winning algorithms in future trial designs could reduce the required number of patients by at least 20%" (abstract). A trial sponsor or ALS clinician at month 3 stratifies or adjusts for the expected decline. Fit direct for the slope; regime IID over patients, with the trial of origin as a group if an identifier ships (check: Atassi says "new randomized subject numbers were created").
- Siblings and duplicates: no ALS or neurodegeneration record (grep: PRO-ACT, ALSFRS, amyotrophic). External collections: the DREAM-Phil Bowen ALS Prediction Prize4Life (2012; 1,822 patients) and the DREAM Prize4Life ALS Stratification Challenge (2015; PRO-ACT plus 1,479 patients from community-based registers). Frank Harrell's data page (hbiostat.org/data, in source_links) was read only in part; an ALS entry there is unverified.
- Better data: from the curator's Zotero collection (items 79, 127, 136); no further search this round.
- Papers and pages: Atassi et al. 2014 (PMC4239834); Kueffner et al., "Crowdsourced analysis of clinical trial data to predict amyotrophic lateral sclerosis progression", Nat Biotechnol 2015 (doi 10.1038/nbt.3051; full text not reachable, read through its abstract); Kueffner et al., "Stratification of amyotrophic lateral sclerosis patients: a crowdsourcing approach", Sci Rep 2019 (PMC6345935).
- Metric: the 2012 challenge scored RMSD and Pearson correlation ("used and described in the previous ALS prediction challenge"), and the 2015 one a sum of z-scores over the teams, "zslope = zCI + zPCC − zRMSD", with the concordance index alone for survival (Kueffner 2019, Methods, "Predictions assessment and scoring scheme"). A sum of z-scores across teams cannot score one model, and which of RMSD and PCC ranked in 2012 was not read, so `rmse` (the challenges' RMSD) as a stand-in, or the fallback, is to settle at /add-dataset (MET-4, MET-10, MET-11); inputs none.
- Risks for /add-dataset: per-patient features built from the long tables over the first three months, as the challenges did (joins and time windows, USE-3); the slope needs ALSFRS visits after month 3, and the ALSFRS and ALSFRS-R scales mix across trials (USE-5); the treatment arms of 44 trials; the trial of origin as a group (SPLIT-3); the terms of use to read (no criterion, EV-4).
- Priority: gap 0 (medical & healthcare, regression and IID are not thin), use case + (the challenges' trial-design use with a month-3 prediction point), source + (Neurology and Nature Biotechnology papers, a maintained database), shape + (thousands of patients, many clinical and lab features), risk - (a feature build from long tables).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 127: "Datasets"; the curator's Zotero collection, item 136: "Datasets"; the curator's Zotero collection, item 79: "Datasets".
- as published: 13,717 ALS patients from 44 phase II/III trials: demographics, labs, history, vitals, and longitudinal ALSFRS and survival (18+ million data points). Per-patient features must be built from the ...; target: ALSFRS(-R) slope over months 3-12, or survival (the DREAM ALS Prediction Prize challenges); access: registration.
- Why: Large pooled real trial data with an established prediction task and a crowdsourced benchmark (Kueffner et al. 2015). | Large pooled trial database with a published prediction challenge and a defined prediction point | The largest pooled ALS trial database with a published prediction challenge (Kueffner et al. 2015, ...
- Adds: Neurodegenerative disease progression, absent from the records. Caveats: registration and terms; the longitudinal tables need a feature build. | A neurodegenerative-disease progression task, not in the records. Sizes now confirmed. The table must be built from longitudinal records as the DREAM challenge did; the ...
