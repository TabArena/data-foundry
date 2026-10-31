---
unique_name: curial_covid_ed_triage
name: 'CURIAL: COVID-19 triage from routine ED bloods and vitals (OUH, PUH, UHB)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: Other
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://oxfordbrc.nihr.ac.uk/research-themes/modernising-medical-microbiology-and-big-infection-diagnostics/iord-about/
- https://arxiv.org/abs/2603.09356
- https://doi.org/10.1016/S2589-7500(20)30274-0
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: COVID-19 triage in the emergency department from blood tests, blood gas and vital signs of the first hour, about 115,000 Oxford patients in the first paper and three NHS trusts later, with a clear rule-out decision; the controls come from the pre-pandemic period and the data are available by application only.
- Source: Soltan, Kouchaki, Zhu, Kiyasseh, Taylor, Hussain, Peto, Brent, Eyre, Clifton, "Rapid triage for COVID-19 using routine clinical data for patients attending hospital: development and prospective validation of an artificial intelligence screening test", Lancet Digit Health 3(2):e78-e87 (2021; PMID 33509388, PMC7831998; abstract read through Europe PMC): electronic health records of four Oxfordshire teaching hospitals (OUH); PCR-confirmed COVID-19 patients presenting December 2019 to April 2020 against pre-pandemic controls; about 115,000 patients; models tuned to 70%, 80% and 90% sensitivity; the ED model reached AUROC 0.939 (77.4% sensitivity, 95.7% specificity) and 0.881 in a two-week prospective test on 3,326 ED patients. Data: OUH through an application to the Infections in Oxfordshire Research Database (IORD), the other trusts (PUH, UHB) on request; no public file. The cohort sizes OUH 161,955, PUH 38,717 and UHB 95,236 are from the run's first pass of arXiv 2603.09356 (its abstract names no datasets; not re-read).
- Use case: the ED team, within the first hour of a patient's arrival, rules COVID-19 out or in to choose the ward stream and isolation before the PCR result returns (the paper's screening test that rules out COVID-19 with high confidence from data available within an hour, abstract); fit approximate: pre-pandemic controls are not the negatives the triage meets during a pandemic (`Selection Bias`, cases and controls from different periods); regime temporal or grouped by trust (the papers validate prospectively and across trusts; SPLIT-5).
- Siblings and duplicates: `mimic_iv_ed_triage`, `nhamcs_ed_hospitalization`, `ed_uti_urine_culture_prediction` (other ED tasks), `sirio_libanes_covid_icu` (COVID-19 ICU admission, another source). No other record of CURIAL (grep: curial, IORD). External collections: none found.
- Better data: from the curator's Zotero collection (item 124); no further search this round.
- Papers and pages: Soltan et al. 2021; the IORD page (oxfordbrc.nihr.ac.uk); Thakur et al., "Democratising Clinical AI through Dataset Condensation for Classical Clinical Models", arXiv 2603.09356 (2026; the Zotero item). Later CURIAL papers on external trusts were not read.
- Metric: the paper reports AUROC, sensitivity, specificity and NPV at three operating points (sensitivity 70%, 80%, 90%), so it fixes no single threshold: `roc_auc` (MET-6, MET-7, MET-8); a metric at a fixed sensitivity would be custom (MET-13). Inputs none.
- Risks for /add-dataset: whether a benchmark can obtain the data at all (an IORD application for approved research; a note, EV-4); cases and controls from different periods, so changes in assays, analysers or recording between periods can give the label away (LEAK-13 to LEAK-15; probe `Class-dependent Recording`); the task is tied to the 2020 pandemic waves; blood gas exists only for some patients (missingness tied to severity).
- Priority: gap 0 (medical, binary not thin), use case + (the paper names the ED rule-out and the first-hour prediction point), source + (a peer-reviewed development and prospective validation), shape + (about 115,000 patients, mixed labs and vitals), risk - (period-separated controls, a likely recording leak).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 124: "Democratising Clinical AI through Dataset Condensation for Classical Clinical Models".
- as published: Emergency department presentations: OUH 161,955; PUH 38,717; UHB 95,236 (as used in arXiv 2603.09356). Features: demographics, routine blood tests and vital signs; about 2017-2021 including ...; target: SARS-CoV-2 PCR-confirmed COVID-19 status; access: request.
- Why: Large real multi-site EHR task with a clear actor and moment; a site-grouped split is possible.
- Adds: A large ED infection triage task across three hospitals. Risks: OUH by IORD application only and the other trusts on request; negatives partly from the pre-pandemic period (cases and controls from different periods, selection bias); tied to the pandemic period.
