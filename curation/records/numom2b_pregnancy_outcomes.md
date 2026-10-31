---
unique_name: numom2b_pregnancy_outcomes
name: 'nuMoM2b: Nulliparous Pregnancy Outcomes Study: Monitoring Mothers-to-be'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Random (IID)
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://dash.nichd.nih.gov/
- https://doi.org/10.1016/j.ajog.2015.01.019
- https://doi.org/10.64898/2025.12.16.25342440
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: an NICHD prospective cohort of 10,037 nulliparous women seen at three pregnancy visits and at delivery (recruited 2010-2013), designed "to determine maternal characteristics ... that predict adverse pregnancy outcomes", with preterm birth as the primary outcome and preeclampsia and fetal growth restriction as key ones; a strong source, but access by request, many tables, and the target to choose.
- Source: Haas et al., "A description of the methods of the Nulliparous Pregnancy Outcomes Study: monitoring mothers-to-be (nuMoM2b)", AJOG 2015, doi 10.1016/j.ajog.2015.01.019 (PMC4387083; abstract read): "Nulliparous women in the first trimester of pregnancy were recruited into an observational cohort study. Participants were seen at 3 study visits during pregnancy and again at delivery"; "The primary outcome of the study was defined as pregnancy ending at <37+0 weeks' gestation. Key study hypotheses involve adverse pregnancy outcomes of spontaneous preterm birth, preeclampsia, and fetal growth restriction"; "We recruited 10,037 women". Data in NICHD DASH (dash.nichd.nih.gov) on request with a data use agreement; the codebook size (11,617 variables in 79 tables) and the DASH release year are from the Assessment, not checked.
- Use case: at the first-trimester visit an obstetrician decides on closer surveillance or prophylaxis (low-dose aspirin for preeclampsia risk) in a first pregnancy, from history, the visit's measurements and labs (written by the curation; the study names the prediction aim, not a decision); fit direct for nulliparous women; regime IID by woman (one pregnancy each), with the eight centres as an optional grouped variant.
- Siblings and duplicates: `nvss_natality_pregnancy_outcomes` (`TBD -> Yes`, priority 2; US birth certificates, another source with under-reported checkbox outcomes), `maternal_health_risk` (`No (Retired)`): same field, not duplicates (PROV-4). External collections: none known.
- Better data: from the curator's Zotero collection (item 119, the postpartum-readmission preprint); no further search this round.
- Papers and pages: Crabtree, Wakefield, Gheorghe and Frasch, medRxiv doi 10.64898/2025.12.16.25342440 (v2, March 2026, read; v1 "contained data leakage that inflated discrimination metrics"): 14-day postpartum readmission, 154 of 8,774 (1.8%), best ROC-AUC 0.569 from 10 sociodemographic predictors; nuMoM2b prediction papers on preeclampsia or preterm birth were not looked up (the run's web search budget was used up).
- Metric: for readmission the preprint reports ROC-AUC and PR-AUC side by side with sensitivity and specificity, no primary (MET-5); for the study's own outcomes none was looked up, so the fallback `roc_auc`; inputs none.
- Risks for /add-dataset: access by a DASH request (noted only, EV-4); the target is ours to pick among the prespecified outcomes (preterm birth < 37 weeks, the study's primary outcome, or preeclampsia; the readmission target is barely learnable); the prediction point must be one visit (the first-trimester visit), with later visits, delivery and postpartum tables left out (USE-3, LEAK-10); joins across many tables (`Needs extensive data wrangling`); biospecimen and genetic data may need separate approval.
- Priority: gap 0 (medical, binary and IID are not thin), use case 0 (written by the curation), source + (an NICHD study with a design paper and a codebook), shape + (about 10,000 pregnancies, many mixed variables per visit), risk - (request access, many tables, the target to choose).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 119: "Traditional Machine Learning Outperforms Automated Machine Learning for Postpartum ...".
- as published: 10,038 nulliparous women with singleton pregnancies, one row per pregnancy; codebook of 11,617 variables in 79 tables (visits per trimester, delivery, postpartum); readmission data for 8,774; target: As used: 14-day postpartum rehospitalisation (1.8%). Stronger options in the cohort: preeclampsia/hypertensive disorders, preterm birth or gestational ...; access: request.
- Why: Large prospective cohort with prespecified, adjudicated outcomes and a codebook that dates each variable relative to the outcome.
- Adds: Obstetric outcomes; only the small maternal_health_risk covers maternal health. Risks: access by DASH request and data-use agreement; heavy joins across 79 tables; the readmission target is barely learnable (AUC 0.57), so pick a better outcome.
