---
unique_name: aids_clinical_trials_group_175
name: AIDS Clinical Trials Group Study 175 (ACTG 175)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Outdated
tags:
- AI-Filled (Verify)
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/890/aids+clinical+trials+group+study+175
- http://arxiv.org/abs/2604.01841
- https://doi.org/10.24432/C5ZG8F
- https://classic.clinicaltrials.gov/ct2/show/NCT00000625
- '# generated enlargement (files of 5,000, 15,000 and 50,000 rows made from the 2,139; SEL-16), not this data'
- https://www.kaggle.com/datasets/aadarshvelu/aids-virus-infection-prediction
- https://cran.r-project.org/package=speff2trial
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the real ACTG 175 trial (2,139 HIV patients enrolled 1991-1992, NEJM 1996), documented and open, but a trial built to compare 1990s nucleoside regimens, with a censored endpoint as the label; no one predicts with it today.
- Source: Hammer et al. 1996, "A trial comparing nucleoside monotherapy with combination therapy in HIV-infected adults with CD4 cell counts from 200 to 500 per cubic millimeter", N Engl J Med (NIAID AIDS Clinical Trials Group, NCT00000625). The patient rows were public in the CRAN package speff2trial (`ACTG175`, 2,139 x 27; first version 2009-07-02) long before UCI linked them (dataset 890, doi 10.24432/C5ZG8F, "Linked on 9/25/2023"; UCI gives 1996 as the creation year). As published on UCI (API read 2026-10-31): 2,139 rows, the id `pidnum`, the target `cid` ("censoring indicator (1 = failure, 0 = censoring)") and 22 features: `time` ("time to failure or censoring"), `trt` (four arms), `treat` ("0=ZDV only, 1=others"), age, weight, hemophilia, homosexual activity, IV drug use, Karnofsky score, antiretroviral history (`oprior`, `z30`, `zprior`, `preanti`, `str2`, `strat`), race, gender, `symptom`, `offtrt` ("off-trt before 96+/-5 weeks"), CD4 and CD8 at baseline (`cd40`, `cd80`) and at 20 weeks (`cd420`, `cd820`). The event, per speff2trial: the first of "a decline in CD4 T cell count of at least 50" (the trial's 50% decline), "progression to AIDS, or death".
- Use case: the source's purpose is a treatment comparison ("To examine the performance of two different types of AIDS treatments", UCI); no actor predicts with it. A prognosis use (an HIV clinician at enrolment estimating the risk of progression under a regimen) is ours to state, and out of date: zidovudine, didanosine and zalcitabine regimens gave way to combination ART with viral-load monitoring, hence `Outdated`; fit approximate. Regime IID: one row per patient of one trial, no site or date column.
- Siblings and duplicates: no other ACTG or HIV-trial record (`grep` for ACTG, AIDS clinical, HIV, CD4 finds only unrelated records such as `nci_aids_antiviral_screen`). The Kaggle upload `aadarshvelu/aids-virus-infection-prediction` in source_links holds files of 5,000, 15,000 and 50,000 rows (`AIDS_Classification_50000.csv`) made from these 2,139, and relabels `cid` as "infected": generated (SEL-16), never a copy to build from. External collections: UCI 890; the R packages speff2trial and mets (`ACTG175`); the AWARE paper (arXiv 2604.01841), which per the run's note uses the 50,000-row Kaggle file (not confirmed from its abstract).
- Better data: from the curator's Zotero collection (item 289, the AWARE paper); no further search this round.
- Papers and pages: Hammer et al. 1996 (the trial); speff2trial (Juraska, Gilbert, Lu, Zhang, Davidian, Tsiatis: covariate-adjusted treatment-effect estimation on these rows); UCI 890; clinicaltrials.gov NCT00000625.
- Metric: none found (the UCI page and API name the tasks "Classification, Regression" and no metric; the trial compares arms by time to event; speff2trial estimates treatment effects), so the fallback `roc_auc` on `cid`; inputs none.
- Risks for /add-dataset: `time`, `cd420`, `cd820` and `offtrt` are measured after baseline and `time` ends at the event: drop them (USE-3, LEAK); `cid` marks an event over follow-up that differs per patient, so a negative can be a patient followed briefly: a fixed horizon built from `time`, with patients censored before it dropped, is the repair to weigh (USE-5); `treat` is a coarsening of `trt`; the treatment arm is a feature, so the task predicts outcome under an assigned 1990s regimen.
- Priority: gap 0 (medical & healthcare and binary classification are not thin), use case 0 (the source names no prediction or decision), source +, shape + (2,139 patients, about 17 baseline features of mixed type), risk - (post-baseline columns and the censored target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 289: "Retrieval-aligned Tabular Foundation Models Enable Robust Clinical Risk Prediction in ...".
- as published: patients, 2,139 rows x 23 features (+ID), randomized trial enrolled 1991-1992; target: cid: failure (CD4 drop >= 50%, AIDS-defining event or death) vs censored; access: open.
- Why: Real randomized-trial data, open (UCI, CC BY 4.0), with documented provenance and mixed clinical, history and lab features. The AWARE paper uses a 50,000-row Kaggle enlargement of it, which is generated (SEL-16); this is the real original.
- Adds: Not recorded. Caveats: time, cd420, cd820 and offtrt are measured after baseline and must be dropped (time leaks the target); the 1990s ZDV/ddI/ddC regimens are obsolete, so the data is dated and small.
