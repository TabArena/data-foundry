---
unique_name: folktables_acs_income
name: 'Folktables ACSIncome (Retiring Adult: New Datasets for Fair Machine Learning)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- TableShift
original_source: GOV Website
year: '2021'
domain: social science
source_links:
- https://arxiv.org/abs/2108.04884
- https://github.com/socialfoundations/folktables
- https://www.census.gov/programs-surveys/acs/microdata.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: ACS PUMS person records rebuilt as UCI Adult's income-above-$50,000 task (Ding et al., NeurIPS 2021). The $50,000 label falls with `adult`, but the source holds the continuous income (PINCP) and makes the threshold a parameter, so a target with a use case can be defined from it; whether to do so is the curator's call (Consistency check below).
- Proposed reject (refuted): `No` (`No Good Target / Scientific Discovery`, SEL-3): the ACS rebuild of Adult's $50,000 label, published as a benchmark for fair-ML methods; the curators rejected this task on `adult`, and `census_income` by treat-alike. Reject check (AI, 2026-10-31): refuted. The $50,000 label falls with `adult` ("The threshold of $50,000 was chosen so that this dataset can serve as a replacement to UCI Adult", Sec. 3.1). But folktables builds from ACS PUMS, where PINCP is continuous and the threshold a parameter, so the target can be redefined from the source, unlike `adult` or `census_income`, which ship only the binned label. The curators named "a real gap-filling task" on `adult`, and on `food_stamps`: "we can create many other tasks from this data (see Unemployment, Income, Public Health Insurance".
- Source: Ding, Hardt, Miller and Schmidt, "Retiring Adult: New Datasets for Fair Machine Learning", NeurIPS 2021 (https://arxiv.org/abs/2108.04884), with the folktables package (https://github.com/socialfoundations/folktables, MIT; the data under the Census Bureau's terms), built from the US Census Bureau's ACS PUMS. As published: ACSIncome on the 2018 1-year PUMS of all states, 1,664,500 persons x 10 features (Table 1: constant predictor 63.1%, LogReg 77.1%, GBM 79.7% accuracy): AGEP, COW, SCHL, MAR, OCCP, POBP, RELP, WKHP, SEX, RAC1P; "Target: PINCP (Total person's income): an individual's label is 1 if PINCP > 50000" (App. B.1), after filtering to persons "above the age of 16, who reported usual working hours of at least 1 hour per week in the past year, and an income of at least $100", and "we also offer datasets with other income cutoffs" (Sec. 3.1); one dataset per state and survey year 2014-2018, "255 distinct datasets per task". The README: "Every field defining the prediction task can be modified, and all variables in the ACS PUMS data release are valid to include as features or as the target".
- The source's purpose: "our contribution is not in this direction. We instead use census data for the empirical study of algorithmic fairness" (Sec. 3.2); "The choice of the 50,000 dollar threshold is idiosyncratic" (Sec. 2.2).
- Use case: none in the source; no actor decides on income above $50,000 (SEL-3, USE-2 on that label). A PINCP regression needs one we write (USE-1), for example estimating the income of a person who did not report it, the gap the Census Bureau fills by allocation (flag FPINCP); whether that fit is direct is open (USE-8). Regime: temporal by survey year or grouped by state, to decide.
- Siblings and duplicates: `adult` (`No`, `No Good Target / Scientific Discovery`, `Outdated`; the curators' CC: "label is wrong, higher/lower 50k is not relevant in such settings"; its assessment names ACSIncome as the modern rebuild); `census_income` (`No`, SEL-3 by treat-alike, reject check of 2026-10-22 stood); `income_prediction_challenge_for_azubian` (AI `TBD -> 2nd Tier`, priority 2, a likely renamed copy of the KDD Census-Income data); `food_stamps` (Lennart, `TBD -> Yes`), `acs_food_stamps_2014_2024` (this run, `TBD -> Yes`) and `acs_household_broadband` (this run, `TBD -> 2nd Tier`): other tasks from the same PUMS files, not duplicates (PROV-7). External collections: TableShift, task "Income" ("Income >= 56k for employed adults", the American Community Survey via folktables, held-out region New England).
- Better data: found as better data for `income_prediction_challenge_for_azubian`; no further search this round.
- Papers and pages: the paper (Sec. 2.2, 3.1, 3.2, Table 1, App. B.1, read in the arXiv PDF), the folktables README, the Census Bureau's ACS PUMS page, the TableShift datasets page.
- Metric: accuracy for the $50,000 label (Table 1), a fair-ML benchmark's habit, not a decision's (MET-6); for a PINCP regression none, so the fallback `rmse` on a log-scaled income (MET-3). The person weight PWGTP is no feature.
- Risks for /add-dataset: the target (the $50,000 label stays out; a PINCP regression needs a use case, USE-1); drop persons with allocated (imputed) income, flag FPINCP ("Total person's income allocation flag"), or the model learns the Census Bureau's imputation; whether the fit is direct (USE-8); the survey years (the paper's 2014-2018; whether the package reaches the later years the Assessment names, 2014-2023, not checked) and a temporal or state-grouped split; the weights as no feature; overlap with `acs_food_stamps_2014_2024` (PROV-7); `RAC1P` and `SEX` as features, noted on `adult` (no SEL-1 objection found).
- Priority: gap + (social science thin), use case 0 (none in the source for a target we would keep), source + (a NeurIPS paper on the Census Bureau's documented PUMS), shape + (1.66M persons a year, mixed types, state and year axes), risk - (the published label is the one rejected on `adult`; the target must be redefined). The reject check suggested priority 2; the factors give 3.

**Consistency check (AI, 2026-10-31):** the curators' CC on `adult` ("label is wrong, higher/lower 50k is not relevant in such settings") and Lennart's note on `food_stamps` ("we can create many other tasks from this data (see Unemployment, Income, Public Health Insurance") point different ways for this record. What sets it apart from `adult`? (a) The AI's best guess: the ACS PUMS hold the continuous income, so the task can be a PINCP regression with a use case such as estimating a non-respondent's income, recorded as a target of our own (USE-1, "for example"). (b) Reject it as `adult` (SEL-3), keeping only the $50,000 label as published. (c) Settle in an amendment of SEL-3 or USE-5 whether a re-targeted survey task enters when the source's own label is rejected.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `income_prediction_challenge_for_azubian`.
- as published: one row per person; the paper's 2018 1-year all-states version has about 1.66 million rows (figure from the paper, not re-read here) x 10 features (age, class of worker, education, marital status, ...; target: personal income (PINCP) above $50,000 (threshold adjustable); filters age > 16, hours >= 1, income >= $100; access: open.
- Why: the record is very likely a renamed copy of the UCI Census-Income (KDD) CPS extract, and ACSIncome is the published modern rebuild of exactly that task (same target, same kind of demographic and work features); adult.md and census_income.md both name it and say no record exists
- Adds: about 5x the rows of the Zindi/KDD data, 2014-2023 survey years instead of 1994-95, a traceable federal source with a codebook, state and year axes for grouped or temporal splits
