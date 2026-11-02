---
unique_name: international_stroke_trial_outcome
name: 'The International Stroke Trial (IST) database: six-month outcome'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2011'
domain: medical & healthcare
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1186/1745-6215-12-101
- https://doi.org/10.7488/ds/104
- https://datashare.ed.ac.uk/handle/10283/128
- https://doi.org/10.1186/1745-6215-13-24
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the International Stroke Trial database (19,435 acute-stroke patients randomised 1991-1996, an open data paper) with the six-month outcome in four classes and the variables at randomisation; the four classes are another framing of the trial's primary outcome that `international_stroke_trial` records as a binary target from the same file, and the care is dated.
- Source: Sandercock, Niewada, Członkowska and the IST Collaborative Group, "The International Stroke Trial database", Trials 12:101 (2011, https://doi.org/10.1186/1745-6215-12-101; full text read via Europe PMC, PMC3104487), correction in Trials 13:24 (2012, https://doi.org/10.1186/1745-6215-13-24); data on Edinburgh DataShare (https://doi.org/10.7488/ds/104; the DataShare page answered 403 on 2026-10-31). As published: "19 435 patients with acute stroke, with 99% complete follow-up"; one row per patient with the randomisation variables (HOSPNUM, RDELAY, RCONSC, SEX, AGE, RSLEEP, RATRIAL, RCT, RVISINF, blood pressure, deficits, stroke subtype, the allocated treatments), the 14-day or discharge data, the six-month data, COUNTRY and CNTRYNUM, and three predicted probabilities (EXPDD, EXPD6, EXPD14); target OCCODE "Six month outcome (1-dead/2-dependent/3-not recovered/4-recovered/0 or 9 - missing status".
- Use case: a stroke physician estimates the six-month prognosis at admission to inform the family, plan rehabilitation or select patients for a trial; the data paper offers the data for "planning further trials, for sample size calculations and for novel secondary analyses", no decision; fit approximate ("none of the patients received thrombolytic therapy"); regime grouped by hospital or country (467 hospitals in 36 countries per the run's Assessment), since a model serves new hospitals (SPLIT-3, to decide).
- Siblings and duplicates: `international_stroke_trial` (unscreened, screen_64, from the curator's Zotero collection): the same file with death or dependency at six months (OCCODE 1-2 against 3-4) as target, a framing of the same signal (PROV-6, CLEAN-18), so the curator keeps one record and picks two or four classes; `stroke_prediction` (`No`, SEL-7) and the other stroke records are other data. External collections: none found.
- Better data: no new search; found through the gap scout for multiclass tasks.
- Papers and pages: Sandercock et al. 2011 (Table 2, the variable list); the trial report (IST Collaborative Group, Lancet 1997); the 2012 correction.
- Metric: none found for prognosis (the data paper names uses, not a metric; the trial compared the share dead or dependent between arms), so the fallback `log_loss` for four classes, `roc_auc` for the binary framing (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: keep only the randomisation variables; the 14-day, discharge, compliance, cause-of-death and follow-up columns are post-outcome and go (LEAK); EXPDD, EXPD6 and EXPD14 are model predictions of the outcome whose fit the variable list does not describe, so they go (LEAK-27 if kept); the allocated treatments are known at randomisation and stay; OCCODE 0 or 9 rows go; take the corrected file (Trials 13:24); the dated care belongs in the fit reason.
- Priority: gap + (multiclass is thin), use case 0 (no source names a decision), source + (a Trials data paper with the variable list), shape + (19,435 patients, mixed types, hospital and country groups), risk - (another framing of the file `international_stroke_trial` records; prediction columns to drop).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for multiclass tasks.
- as published: 19,435 acute stroke patients from 467 hospitals in 36 countries, randomised 1991-1996, 99% follow-up; about 110 variables at randomisation (age, sex, consciousness, deficits, stroke subtype, atrial ...; target: OCCODE, six-month outcome: dead, dependent, not recovered, recovered (0/9 missing); access: open.
- Why: A large trial database published for secondary analyses (CC BY), with a clinical four-class ordinal outcome; drop the 14-day outcome columns and the shipped predicted probabilities of death/dependence (EXPDD, EXPD6, EXPD14), a model output. Dated care (no thrombolysis): name it in the fit
- Adds: A medical multiclass prognosis task with a grouped structure (hospital, country) and mixed categorical and numeric features

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same IST file, a 4-class and a binary framing of one outcome (`international_stroke_trial`; PROV-6). The curator keeps one, or both as distinct tasks.

CC (2026-11-02, Lennart): raised from `nci_aids_antiviral_screen`'s review as the collection's other open
multiclass-against-binary framing (flagged 2026-10-31), now that the NCI screen ships the binary target: "it is fine
and does not matter too much, either priority is fine". No change; the framing stays as the record has it.
