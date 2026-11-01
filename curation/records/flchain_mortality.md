---
unique_name: flchain_mortality
name: Serum free light chains and mortality in Olmsted County (R survival flchain; SurvSet flchain)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2012'
domain: medical & healthcare
original_data_state: One Table
source_links:
- https://doi.org/10.1016/j.mayocp.2012.03.009
- https://github.com/ErikinBC/SurvSet
- https://arxiv.org/abs/2203.03094
- https://cran.r-project.org/package=survival
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 7,874 Olmsted County residents aged 50 or more (a stratified half of the Mayo free-light-chain study) with kappa, lambda, creatinine and MGUS at a blood sample of 1995-2003 and death or last contact through 2009; a real cohort with an observed outcome, but published as a marker study whose authors advise against routine use, with seven inputs.
- Source: Dispenzieri, Katzmann, Kyle et al., "Use of nonclonal serum immunoglobulin free light chains to predict overall survival in the general population", Mayo Clin Proc 87(6):517-523 (2012), https://doi.org/10.1016/j.mayocp.2012.03.009 (read on PMC3538473). The public copy is `flchain` in the R survival package (help page; the study's statistician T. Therneau): a stratified random sample of half the subjects, 7,874 of 15,759 (the paper: 15,859), stratified by age and sex, identifiers and dates removed. As published: one row per person, 11 columns: age, sex, sample.yr, kappa, lambda, flc.grp (the FLC group of the original analysis), creatinine, mgus, futime (days to death or last contact), death, chapter (ICD-9 chapter of the cause of death).
- Use case: none named. The objective is "To determine whether the free light chain (FLC) assay provides prognostic information relevant to the general population" (Abstract), and the Discussion finds the data "not strong enough to support a recommendation of routine FLC measurement". A framing would be ours (a physician estimating a patient's 5-year mortality from a blood panel), fit approximate; the paper leans towards a marker study (SEL-3), not rejected because the target is an observed death. Regime IID, one row per person; sample.yr (1995-2003) allows a temporal check.
- Siblings and duplicates: the SurvSet siblings `rotterdam_breast_cancer` and `smart_vascular_events` are other cohorts; no other record of the Mayo FLC or MGUS cohort. External collections: SurvSet (Drysdale 2022, arXiv 2203.03094); scikit-survival and pycox also ship `flchain` (from memory, not opened).
- Better data: from the curator's Zotero collection (items 96 and 140, SurvSet); no search for better data in this run.
- Papers and pages: Dispenzieri et al. 2012; Kyle et al., NEJM 354:1362-1369 (2006), the MGUS prevalence study the samples come from (not read); the survival package help page.
- Metric: none found. The paper reports Cox risk ratios (4.38 unadjusted, 2.12 adjusted for age, sex and creatinine, Table 2), Kaplan-Meier curves and standardized mortality ratios, and no C-statistic or AUC (PMC3538473); so the fallback `roc_auc` for death within a fixed horizon (MET-1, MET-8). Inputs none.
- Risks for /add-dataset: the target is to be built from futime and death with a horizon every row can reach (follow-up ends June 2009 and samples run to 2003, so about 5.5 years at most); rows censored before the horizon go (SPLIT-9). `chapter` is the cause of death, recorded after the outcome, and goes (LEAK). `flc.grp` groups kappa plus lambda by cut points of the original full sample: redundant, and a weak transductive feature (LEAK-30). Creatinine is missing for part of the rows (to measure). Age will carry most of the signal (a probe for TP-2 rather than `Trivial`).
- Priority: gap 0 (medical and binary are not thin), use case 0 (none named; the authors advise against routine use), source + (Mayo Clinic paper and the documented R package copy), shape + (7,874 people, mixed inputs), risk - (seven inputs and a target to build from censored times).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 140: "SurvSet: An open-source time-to-event dataset repository"; the curator's Zotero collection, item 96: "SurvSet: An open-source time-to-event dataset repository".
- as published: residents aged 50+, 7,874 rows (a stratified half of the study sample), samples 1995-2003, about 8 features (age, sex, sample year, kappa, lambda, FLC group, creatinine, MGUS), time to death; target: death within a fixed horizon (for example 10 years); access: open.
- Why: Real population cohort, larger than most SurvSet sets; weaker: a marker study (leans scientific discovery), few features, flc.grp derived from kappa and lambda, and the cause-of-death column must go | population-based real cohort, mid-size
- Adds: A general-population mortality task; lower priority than the others | lab-marker mortality task; few features. Drop chapter (cause of death, after outcome)
