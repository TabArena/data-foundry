---
unique_name: ofsted_school_inspection_outcomes
name: 'Ofsted state-funded school inspections and outcomes: management information (England)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2015'
domain: education
original_data_state: One Table
source_links:
- https://www.gov.uk/government/statistical-data-sets/monthly-management-information-ofsteds-school-inspections-outcomes
- https://assets.publishing.service.gov.uk/media/5f6b4b76d3bf7f72337b6ef7/Management_information_-_state-funded_schools_1_September_2015_to_31_August_2019.csv
- https://assets.publishing.service.gov.uk/media/5a757ca240f0b6397f35ece5/Management_information_-_schools_-_1_Sept_2005_to_31_August_2015.xlsx
- https://www.bi.team/publications/using-data-science-in-policy/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: Ofsted's official inspection records of state-funded schools in England (files for 2005-2015 and 2015-2019, monthly releases since) with the overall-effectiveness grade, school characteristics and the previous inspection's grades; BIT modelled which schools would be rated requires improvement or inadequate to target inspections; the same inspection's sub-judgements must go, and graded overall effectiveness ends in 2024.
- Source: Ofsted, "State-funded school inspections and outcomes: management information" (https://www.gov.uk/government/statistical-data-sets/monthly-management-information-ofsteds-school-inspections-outcomes, first published 2015-06-30, last updated 2026-10-16): "Management information aggregated and published monthly, and publications of inspections and outcomes from 2005 to 2015 and 2015 to 2019"; the 2005-2015 file is "a one-off publication of inspection outcomes" of section 5 inspections. As published (the header of the 2015-2019 CSV, previewed, 14.7 MB): 57 columns, one row per inspection (section 5 and section 8 visits): URN, phase, type of education, admissions policy, sixth form, religious character, region, local authority, IDACI quintile, number of pupils, warning notices in the year, inspection type and dates, overall effectiveness, category of concern, four sub-judgements, safeguarding, and the previous inspection's dates and grades; overall effectiveness 1 outstanding to 4 inadequate, 9 for visits without a grade.
- Use case: the inspectorate decides which schools to inspect first by the risk of a poor grade; BIT's school-inspection model (https://www.bi.team/publications/using-data-science-in-policy/) flagged schools likely to be rated "requires improvement" or "inadequate" and caught 65% of them in the top 10% by risk, 87% in the top 20%; fit direct for the binary framing; regime temporal by inspection date, with the school as a group across inspections (SPLIT-3: one regime, the temporal one).
- Siblings and duplicates: none (grep: ofsted, school inspection); the accepted education datasets (`student_portuguese_performance`, `open_university_learning_analytics_dataset`, `early_learning_predictors`) are student-level, another unit. External collections: none found.
- Better data: no new search; found through the gap scout for education.
- Papers and pages: the gov.uk data page (read); BIT, "Using data science in policy" (2017; the page read gives the target and the capture rates, not the data or the model).
- Metric: BIT reports the share of low-rated schools caught in the top 10% and the top 20%, two values of k, so no single fixed k (MET-7); the fallback `roc_auc` for the binary framing or `log_loss` for four grades (MET-1, MET-5, MET-8). Inputs: none.
- Risks for /add-dataset: category of concern, the sub-judgements, safeguarding and the section 8 outcome belong to the same inspection and go (LEAK); "Number of warning notices issued in academic year" may postdate the inspection (to check); Ofsted's own risk assessment picks the schools that get a graded inspection, the selection that creates the label (no marker, Patterns "Selection bias"); single-word overall-effectiveness grades were dropped for inspections from September 2024 (from memory, to verify in the release notes), so the target ends there; the four-grade or binary framing to pick; richer features need a join to DfE performance and census data by URN.
- Priority: gap + (education is thin), use case + (BIT names the targeting decision), source + (Ofsted official statistics), shape + (tens of thousands of dated inspections, mixed types), risk - (same-inspection columns; joins for richer features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for education.
- as published: one row per inspection: 57 columns in the 2015-2019 file (about 20,000 inspections, estimated from its 14.7 MB): school phase, type, admissions policy, sixth form, faith, region, local authority, ...; target: overall effectiveness of a graded inspection (1 outstanding to 4 inadequate), or the binary 'requires improvement or inadequate'; access: open (Open Government Licence).
- Why: an official, open, documented table with a real decision on the prediction; time order by inspection date and groups by school
- Adds: a school-level (not student-level) education task with mixed categorical and numeric features and a temporal split; can be joined to DfE performance and census data by URN for more features
