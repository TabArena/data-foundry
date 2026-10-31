---
unique_name: fsa_cohort_default_rate
name: Cohort Default Rate
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: education
original_data_state: One Table
source_links:
- https://nsldsfap.ed.gov/cdr-searchable-database
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/cohort-default-rate
- https://arxiv.org/abs/2605.12292
- https://fsapartners.ed.gov/knowledge-center/topics/default-management/official-cohort-default-rates-schools
- '# field definitions of the 300, 304 and 305 reports'
- https://fsapartners.ed.gov/sites/default/files/2022-09/DMInstructionsforSchoolDataFiles.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the STRABLE release and a preview of its files; a human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: FSA's official three-year cohort default rates per school; STRABLE's binary target "Average or Greater than 30" is not a default threshold (the run's note) but a flag for which formula FSA used, set by whether fewer than 30 borrowers entered repayment, and the file's default rates (cohorts FY2019-2021) sit near 0% because of the payment pause. Close to `No` (SEL-3) unless the curator wants a re-target.
- Source: U.S. Department of Education, Federal Student Aid, official cohort default rates for schools, published each September (https://fsapartners.ed.gov/knowledge-center/topics/default-management/official-cohort-default-rates-schools; search https://nsldsfap.ed.gov/cdr-searchable-database); fields in "Data File Instructions and Definitions" (https://fsapartners.ed.gov/sites/default/files/2022-09/DMInstructionsforSchoolDataFiles.pdf). As published (the 300 report): one row per school with OPE ID, name, address, program length, school type, and for each of three cohort years Num (borrowers in default), Denom (borrowers in repayment), DRate and Rate Sub-Type, plus Ethnic Code, Cong Dis, Region and "Average or Greater than 30". STRABLE read PEPS300ReportFY21Official.xlsx ("Eligible Schools File") and dropped Num, Denom and DRate as leakage: 4,700 schools x 14 columns, target "Average or Greater than 30" (17.5% ones).
- The target in the source's words (Table 1, p. 2): "Schools with fewer than 30 borrowers entering repayment during the cohort period use an average formula. 0–Non-average formula 1–Average formula." It follows from the dropped Denom columns (SEL-5) and is no outcome (SEL-3). STRABLE's paper names another task, "to predict the default rate percentage" (App. C.2).
- Use case: for DRate, none named: FSA computes each rate from loan records and sanctions a school at 30% or more for three years or above 40% for one ("Definitions", p. 3); predicting a school's rate from its name, location and type has no named actor; fit none for the shipped target, approximate at best after a re-target. Regime: IID over schools, temporal across annual files.
- Siblings and duplicates: `fsa_gainful_employment` and `fsa_foreign_gifts_and_contracts` (other FSA files, other tasks); `college_scorecard` (`Yes`, ED's institution files, completion rate). No other default-rate record (searched cohort default). External collections: STRABLE ("Cohort Default Rate").
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Papers and pages: FSA's instructions above and its Cohort Default Rate Guide; STRABLE (arXiv 2605.12292, App. C.2 and D.1). The FY2021 national rate was 0.0% (released September 2024, during the payment pause), per school disclosures citing FSA's briefing (e.g. Tulane's FY2021 CDR letter); FSA's briefing itself not read.
- Metric: none found (FSA sets sanction thresholds, not a prediction task), so the fallback `roc_auc` for a binary target or `rmse` for a rate; STRABLE scores AUROC (App. D.1) (MET-1).
- Risks for /add-dataset: the shipped label is a formula flag (re-target or `No`); a rate target needs a file from before the pause (FY2018 or earlier); rates are not shown when Denom is 10 or fewer; Rate Sub-Type repeats the flag's mechanism.
- Priority: gap + (education), use case 0, source + (FSA's field definitions), shape + (4,700 schools, mixed columns), risk - (the label is a formula flag), risk - (rates near 0% in this file).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 4,700 rows x 14 columns incl. target (STRABLE parquet); target: Average or Greater than 30.
- Why: Predict whether a US postsecondary institution's student-loan cohort default rate is at or above a threshold
- Notes: Raw file PEPS300ReportFY21Official.xlsx (FSA, FY2021 official rates). Binary target 'Average or Greater than 30' is a STRABLE-derived threshold label; the paper says 'default rate percentage'.
