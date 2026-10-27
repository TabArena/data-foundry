---
unique_name: drug_consumption
name: drug_consumption
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2015'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5TC7S
source_row: 819
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 3: a documented survey with a paper, but the labels are the respondents' own reports of drug use in the same questionnaire as the features (SEL-7 doubt) and the target is a choice among 18 drugs; the CC note below calls it a scientific-discovery task.
- Source: Fehrman, Muhammad, Mirkes, Egan, Gorban, "The Five Factor Model of personality and evaluation of drug consumption risk" (arXiv 1506.06297, 2015; Springer 2017); UCI "Drug Consumption (Quantified)", donated 2016-10-16 (https://doi.org/10.24432/C5TC7S); as published: 1,885 respondents x 12 features (NEO-FFI-R, BIS-11, ImpSS scores, age, gender, education, country, ethnicity, all quantified to reals) and 19 drug labels with seven classes each ("Never Used" to "Used in Last Day"), including the decoy drug Semer.
- Use case: UCI states the purpose as "Evaluation of risk to be drug consumer for each drug"; no actor or decision is named (a clinician screening risk from personality tests is our guess), and every label is self-reported in the same anonymous survey (SEL-7 doubt; cdc_diabetes_health_indicators precedent): fit approximate at best; regime IID (one row per respondent).
- Siblings and duplicates: none in `curation/records/`; collection tag `TabArena Reject` (the TabArena study excluded it); the CC note says the TALENT benchmark's target is unclear.
- Papers and pages: the paper above (user/non-user splits by time window, several classifiers, sensitivity and specificity reported; not re-read here).
- Metric: none verified as one deliberate criterion (the paper reports sensitivity and specificity per drug and classifier; MET-5, MET-6 not checked against the text), so the fallback (`roc_auc` for a binary user/non-user target, `log_loss` for the seven classes).
- Risks for /add-dataset: which drug and which binarisation (USE-5); the quantified categorical columns should be decoded back to categories (CLEAN; the CC note); 1,885 rows with rare classes for some drugs (TP-5).
- `Ethical Issue` removed: no source states that the subjects or creators object to ML use (SEL-1); the survey is anonymous.
- Priority: gap + (social science is thin), use case 0 (no actor), source + (paper and UCI page), shape + (1,885 rows, 12 features), risk - (self-reported label, target choice): 3.

UCI 'Drug Consumption (quantified)' dataset: ~1885 respondents with Big-Five personality scores plus demographics, used to predict use of each of ~18 drugs (multiple binary/ordinal targets). It is genuine real-world tabular data with a defensible predictive target (per-drug usage), but it was framed as a scientific-discovery study of personality-drug links rather than a single benchmark task, and it is already tagged TabArena Reject / 2nd Tier. The choice of target is ambiguous (18 candidates) and drug-use prediction from personality raises mild ethical/representativeness concerns. A human must pick the actual target used, confirm sample size after dropping near-constant drugs, and weigh the ethical framing before promoting it.

---

CC: ""Predict using demographic and psychological data whether a person uses drugs. 18 Different targets available. Unclear which one used in Talent. Scientific discovery task.

Categorical data made to be numeric by default""

## Reference

The Five Factor Model of personality and evaluation of drug consumption risk
By E. Fehrman, A. Muhammad, E. Mirkes, Vincent Egan, A. Gorban. 2015

Published in Data Science
