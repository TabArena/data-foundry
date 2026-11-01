---
unique_name: fsa_gainful_employment
name: Gainful Employment
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
year: '2017'
domain: education
problem_type: Regression
original_data_state: One Table
source_links:
- https://studentaid.gov/data-center/school/ge
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/gainful-employment
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the STRABLE release and a preview of its files; a human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the Department of Education's final 2015 debt-to-earnings rates of gainful-employment programs (8,637 programs), a measured program outcome tied to a named regulatory decision; but it is the only release, under a rule rescinded in 2019, and STRABLE keeps pass/zone/fail columns computed from the same debt and earnings.
- Source: U.S. Department of Education, Federal Student Aid, GE Debt Measure Year 2015 final D/E rates (GE-DMYR-2015-Final-Rates.xls), released to institutions on 8 January 2017 and posted on the FSA Data Center (https://studentaid.gov/data-center/school/ge; GE Electronic Announcement #100, https://fsapartners.ed.gov/knowledge-center/library/electronic-announcements/2017-01-06/general-subject-gainful-employment-electronic-announcement-100-upcoming-release-final-gainful-employment-debt-earnings-de-rates). As published: one row per program (OPEID, institution, CIP code, credential level) with the annual earnings rate and the discretionary income rate, their numerators and denominators, SSA mean and median earnings, transitional rates, a pass/zone/fail per rate and the official program result. STRABLE: 8,637 rows x 13 columns (2,616 institutions), target "Debt-to-Earnings Annual Rate" (percent); numerators, denominators, SSA earnings, transitional rates and the official result dropped; the pass/zone/fail of the discretionary income rate and of the two transitional rates kept.
- Use case: under the 2014 GE regulations a program lost Title IV eligibility after failing the D/E rates in two of three consecutive years; a program passed with an annual rate of 8% or less or a discretionary rate of 20% or less (FSA's announcement as summarised by FAME and NASFAA). ED computes the rate from loan records and SSA earnings, so the prediction is approximate: a school or a student estimating a program's rate before it is published, or for a program too small to get one. Regime: grouped by institution (8,637 programs at 2,616 institutions).
- Siblings and duplicates: `fsa_cohort_default_rate` and `fsa_foreign_gifts_and_contracts` (other FSA files); `college_scorecard` (`Yes`, ED's institution files; ED's field-of-study files also hold program-level debt and earnings, related data for the curator). No other GE record (searched gainful). External collections: STRABLE ("Gainful Employment", App. C.2: "to predict if a program passes standards", while its config's target is the annual rate).
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Papers and pages: GE Electronic Announcements #100 (2017-01-06) and #104 (2017-01-30); NASFAA's coverage of the release (more than 800 programs failed); the July 2019 final rule that rescinded the regulations; STRABLE (arXiv 2605.12292, App. C.2 and D.1).
- Metric: none found (the regulations set pass/zone/fail thresholds on the rates, not a metric for predicting them), so the fallback `rmse`; STRABLE scores R^2 (App. D.1) (MET-1).
- Risks for /add-dataset: the discretionary-income and transitional pass/zone/fail columns come from the same debt and earnings as the target and go (LEAK); then only institution, location, type, CIP and credential remain; one release under a rescinded rule (`Outdated` to weigh); asterisked values in the debt columns.
- Priority: gap + (education), use case 0 (approximate, actor unnamed), source + (ED's release and announcements), shape + (8,637 programs, mixed types, grouped by institution), risk - (the kept pass/zone/fail columns leak the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 8,637 rows x 13 columns incl. target (STRABLE parquet); target: Debt-to-Earnings Annual Rate.
- Why: Predict the annual debt-to-earnings rate of a vocational program's graduates
- Notes: Raw file GE-DMYR-2015-Final-Rates.xls (2015 final rates). Paper says 'whether a program passes'; config target is the D/E annual rate (regression).
