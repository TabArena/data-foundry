---
unique_name: siab_long_term_unemployment
name: 'SIAB Regional File: long-term unemployment risk of job seekers at registration (statistical profiling)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/
- https://arxiv.org/abs/2108.04134
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: German administrative labour-market biographies (IAB's 2% SIAB sample) with a published profiling task, long-term unemployment predicted on the day a job seeker registers, split by year; access is by application to the IAB research data centre, the episode table must be built from spell data, and profiling job seekers is an ethics question for the curator (SEL-1, no fail from the source's words).
- Source: the Research Data Centre (FDZ) of the Federal Employment Agency at the IAB, "Sample of Integrated Labour Market Biographies (SIAB)" (https://fdz.iab.de/en/our-data-products/individual-and-household-data/siab/): a 2% random sample of the Integrated Employment Biographies; versions 7519, 7521 and 7523; the factually anonymous Regional File "can be downloaded by the applying institutions as a Scientific Use File (SUF)", the weakly anonymous version only "during research visits (included remote data access)". The task: Kern, Bach, Mautner, Kreuter, "Fairness in Algorithmic Profiling: A German Case Study" (arXiv 2108.04134, 2021; PDF read): SIAB Regional File 7517 v1 with "1,827,903 individuals documented in a total of 62,340,521 rows"; restricted to 2010-2016, "303,724 unique individuals and 643,690 unemployment episodes", 97,599 (15.2%) of them long-term; 157 predictors (socio-demographics, labour-market history, last job), built from "only information observed at or before entry into unemployment"; gender and nationality are protected attributes, "not used as predictors".
- Use case: the public employment service, when a person registers as unemployed, scores the risk of being "continuously unemployed for more than one year" (Social Code Book III, art. 18) to allocate support programmes (the paper's policies: the top 10%, the top 25% or the middle 50% of risk); fit direct; regime temporal: the paper trains on 2010-2015 and evaluates on "the full data from 2016 (89,710 episodes)" (SPLIT-3), with the person as a group across episodes.
- Siblings and duplicates: none (grep: SIAB, IAB, long-term unemployment); `wioa_employment_after_exit` (unscreened: US workforce programmes, employment after exit) is a related labour task from another source (PROV-4). External collections: none found.
- Better data: no new search; found through the gap scout for social science.
- Papers and pages: Kern et al. 2021 (Sec. 3.1 data, 3.2 prediction setup, 3.2.2 metrics); Antoni et al. 2019 (the SIAB data report, cited there, not read).
- Metric: the paper reports accuracy, precision and recall at k, F1, ROC-AUC and PR-AUC under three policies, and tunes by ROC-AUC ("the hyperparameter setting with the highest average ROC-AUC was chosen for each method"): `roc_auc`, the deliberate criterion and the fallback alike (MET-5; several k, so no `precision_at_k`, MET-7). Inputs: none.
- Risks for /add-dataset: the episode table and its 157 predictors must be built from the spell data (`Needs extensive data wrangling`); access only by application, and redistribution depends on the FDZ contract (a fact, no criterion, EV-4); SEL-1: statistical profiling of job seekers is contested (the paper calls for "rigorous auditing processes before such models are put to practice" and discusses the Austrian AMS case), while the data owner releases the data for research: the curator's call; gender and nationality stay out of the features or ship as scoring columns; episodes need a year of follow-up (the paper stops at 2016 for data to 2017); the Regional File coarsens regions, occupations and industries.
- Priority: gap + (social science is thin; labour is absent), use case + (the paper names the actor, the moment and the decision), source + (IAB data with documentation and a published task definition), shape + (643,690 episodes, mixed types, seven years), risk - (a heavy build from spell data; the ethics question).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for social science.
- as published: 2% random sample of German administrative labour-market biographies; version 7517: 1,827,903 people, 62,340,521 spell rows; the paper's task table: 643,690 unemployment episodes of 303,724 people, ...; target: Long-term unemployment: continuously unemployed for more than one year after the episode starts (the German PES definition); access: request.
- Why: A real labour-market decision with a documented prediction point, a temporal split and a peer-reviewed task definition; administrative data, not survey answers.
- Adds: Labour (no accepted dataset); a large temporal task with socio-demographics, employment history and last-job features (industry, skill level, wage). Risks: SEL-1 (algorithmic profiling of job seekers is contested; the paper leaves gender and nationality out); the episode table must be built from spell data (heavy ...
