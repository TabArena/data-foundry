---
unique_name: coda_tb_clinical_triage
name: CODA TB DREAM Challenge dataset, clinical and demographic table (TB triage)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://www.synapse.org/#!Synapse:syn31472953
- https://doi.org/10.1101/2024.03.27.24304980
- https://arxiv.org/abs/2508.02741
- https://doi.org/10.1093/ofid/ofaf572
- http://arxiv.org/abs/2610.03256
- https://doi.org/10.1038/s41597-024-03972-z
- https://doi.org/10.7303/syn31472953
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the clinical and demographic table of the CODA TB DREAM Challenge, adults with two or more weeks of cough at outpatient clinics in seven countries, the target microbiologically confirmed TB; a triage task with a WHO target, but only the 1,105 training participants are released, not all 2,143.
- Source: Huddart, Yadav, Sieberts et al., "A dataset of Solicited Cough Sound for Tuberculosis Triage Testing", Sci Data 11:1149 (online 2024-10-18, doi 10.1038/s41597-024-03972-z, PMC11489852; medRxiv 2024-03-28, doi 10.1101/2024.03.27.24304980), data on Synapse (doi 10.7303/syn31472953, www.synapse.org/TBcough); the challenge: Jaganath, Sieberts, Raberahona et al., "Accelerating Cough-Based Algorithms for Pulmonary Tuberculosis Screening: Results From the CODA TB DREAM Challenge", Open Forum Infect Dis 12(10):ofaf572 (2025, PMC12502651). As published: 2,143 participants and more than 700,000 cough sounds (Sci Data abstract), but "A total of 1,105 participants' data are made available for access and download as a training dataset" and "The validation set is withheld" (Sci Data, Data Records); models can be scored against the hidden test set on Synapse. Clinical variables of the training data (Usage Notes): sex, age, height, weight, reported cough duration, prior TB diagnosis and type, hemoptysis, heart rate, temperature, weight loss, smoking in the last week, fever, night sweats. Countries and TB positives over all 2,143 (Table 3): India 241 (25), Madagascar 234 (103), Philippines 388 (40), South Africa 275 (52), Tanzania 197 (36), Uganda 487 (174), Vietnam 321 (122); 552 positive. Reference standard (Methods): positive on liquid culture, sputum or urine Xpert, or two trace-positive Xpert Ultra results; negative needs no positive Xpert and negative cultures; indeterminate is its own category. Access: certified and validated Synapse users who submit an Intended Data Use Statement and accept the challenge's Terms of Use (a term, EV-4).
- Use case: a clinic worker triages adults with cough to decide who goes on to confirmatory molecular testing; the WHO target for a triage test is "at least 90% sensitive and 70% specific" (Sci Data, Background), and the challenge's clinical inputs leave out HIV status because its testing or results may not be available at the time of the cough assessment (OFID, Methods); fit direct for a clinical-only triage score, which the OFID authors fit after the challenge (a random forest on the clinical variables, AUROC 0.817). Regime IID: the challenge split was randomised at the individual level, not stratified by country (OFID); a grouped split by country (7 groups) is the cross-cohort variant (arXiv 2610.03256); one regime, from the use case (SPLIT-3, SPLIT-5).
- Siblings and duplicates: no record holds CODA TB (grep by CODA, the Synapse id, cough); the TB screening records of the run, `treats_tb_prevalence_survey` and `treats_tb_crp_screening`, are community screening in Zambia and South Africa from other sources: distinct (PROV-7). External collections: none found on the pages read.
- Better data: from the curator's Zotero collection (items 295 and 59); the run names it better data for the CAGE-TB task of arXiv 2610.03256 (Uganda and South Africa; release of that data not stated), which has no record; no further search this round.
- Papers and pages: Sci Data 2024 (the data); OFID 2025 (the challenge); Lu et al., "DeepGB-TB" (arXiv 2508.02741, AAAI 2026: 1,105 patients from seven countries, cough audio and demographics, AUROC 0.903 and F1 0.851); Jansen van Vüren et al., "Cross-cohort TB classification using clinical data gathered in Uganda and South Africa" (arXiv 2610.03256, CAGE-TB: logistic regression AUROC 0.80 and 0.84 on the held-out cohorts).
- Metric: the challenge ranked by AUROC and by "2-way pAUROC within the thresholds of 80% sensitivity and 60% specificity" (OFID, Methods), with total AUROC as the fallback when no curve reached the region; leaderboard metrics (MET-4), so `roc_auc`, with the partial AUROC, bounded by the source's own sensitivity and specificity, a custom metric for the add stage to weigh (MET-10); inputs none.
- Risks for /add-dataset: drop the audio (a non-tabular modality, SEL-12) and ship the clinical table; drop the indeterminate cases (USE-7); keep HIV status and test results out if the table ships them (not known at triage, USE-3); country as a feature or as the group (decide with the regime); prevalence differs by country (10% to 44%); BMI and the log of cough duration are the source's derived inputs (cheap to add).
- Priority: gap 0 (medical, binary and IID are covered), use case + (WHO triage, the source's decision), source + (Sci Data paper, challenge paper), shape + (1,105 participants, 14 mixed clinical variables, 7 countries), no known risk (the withheld test half is a size note, not a risk factor).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 295: "Cross-cohort TB classification using clinical data gathered in Uganda and South Africa"; the curator's Zotero collection, item 59: "DeepGB-TB: A Risk-Balanced Cross-Attention Gradient-Boosted Convolutional Network for ...".
- as published: participants; 2,143 adults with cough of 2+ weeks at outpatient clinics in 7 countries (India, Philippines, South Africa, Uganda, Vietnam, Tanzania, Madagascar); the 1,105-participant training ...; target: tb_status: microbiological reference standard (sputum Xpert MTB/RIF (Ultra) or culture), positive vs negative; access: request.
- Why: label from an independent lab reference, not from the features; a multi-country prospective cohort; clinical-only models are the challenge baseline, and the audio part can be dropped | Same task as CAGE-TB in arXiv 2610.03256, whose data is not released, with more patients and countries and the same reference ...
- Adds: TB triage from symptoms and vitals across 7 countries (a grouped split by country is possible); real use in low-resource screening | Better data for the CAGE-TB task: larger (2,143 vs 721 patients), 7 countries including South Africa and Uganda, and accessible. zotero_05 (item 59) already proposes it as ...
