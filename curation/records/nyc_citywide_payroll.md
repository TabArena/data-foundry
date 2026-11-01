---
unique_name: nyc_citywide_payroll
name: Citywide Payroll Data (Fiscal Year), City of New York
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Ethical Issue
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2015'
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.cityofnewyork.us/City-Government/Citywide-Payroll-Data-Fiscal-Year-/k397-673e
- https://data.cityofnewyork.us/api/views/k397-673e.json
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: New York City's payroll of every city employee by fiscal year, 509,525 to 613,008 rows a year for FY2014-FY2026 with names, published for budget transparency; the target (base salary or overtime pay) has no task in the source and the rows name people, the two concerns the curator marked on `employee_salaries` and the Vancouver remuneration record, carried here as the same markers.
- Source: NYC Office of Payroll Administration (OPA), "Citywide Payroll Data (Fiscal Year)" on NYC Open Data (k397-673e, made public 2015-10-31, rows updated 2026-10-29): "Data is collected because of public interest in how the City's budget is being spent on salary and overtime pay for all municipal employees." 17 columns: fiscal year, payroll number, agency, last, first and middle name, agency start date, work-location borough, title, leave status at 30 June, base salary, pay basis, regular hours, regular gross paid, OT hours, total OT paid, total other pay; 561,580 rows for FY2026 (Socrata counts, 2026-10-31). NYPD and District Attorney names are redacted because disclosure "could endanger the life and safety of the public servants listed thereon"; OT hours follow a new method from FY2023.
- Use case: none named by the source: "This data can be used to analyze how the City's financial resources are allocated and how much of the City's budget is being devoted to overtime." The scout's actor (an HR or budget analyst estimating the pay or overtime of a position) is written by the curation and does not count (USE-1). Base salary follows title and pay step, close to a lookup; overtime pay per employee is the more open target. Regime temporal by fiscal year, the same people across years.
- Siblings and duplicates: `employee_salaries` (Montgomery County 2016; Lennart: `TBD -> 2nd Tier`, `No Good Target (yet)`, `Ethical Issue`, "Again contains PII"; CARTE/TARTE, MulTaBench) and `employee_remuneration_and_expenses_earning_over_75000` (Vancouver; the same verdict and markers, "Contains PII", "No target or features for a target at all"). Other publishers, so no duplicates (PROV-4); the curator decides whether dropping the names settles the PII concern for all three. External collections: none found for this file.
- Better data: found as better data for `employee_salaries` and `employee_remuneration_and_expenses_earning_over_75000`; no further search this round.
- Papers and pages: the Open Data page and its column descriptions.
- Metric: none found, so the fallback `rmse` (MET-1, MET-8).
- Risks for /add-dataset: names go, and agency, title and start date together may still single people out (SEL-1 as the siblings carry it); regular gross paid, regular hours and pay basis restate base salary, and OT hours restate OT pay (LEAK-10); the same person recurs across years without a person id, only names (SPLIT-24); employees who left during the year have partial pay; about 0.55 million rows a year are over the 500k cap.
- Priority: gap 0, use case 0 (transparency, no decision), source + (a city agency with column descriptions), shape + (half a million rows a year, 13 years), risk - (no target with a decision; names in the rows).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `employee_remuneration_and_expenses_earning_over_75000`, `employee_salaries`.
- as published: One row per employee and payroll per fiscal year: about 7.34M rows in total (509,525 for FY2014 up to 561,580 for FY2026, counted through the Socrata API). 17 columns: fiscal year, payroll number, ...; target: base salary, or regular gross or total OT paid in the year (all published); access: open.
- Why: The target matches employee_salaries (Montgomery County 2016: annual salary from department, division, assignment category, position title, date first hired, gender), and its features are of the same kind: agency, title, start date and borough. The Vancouver record (name, department, title, remuneration) gives the ...
- Adds: About 0.5M employees a year against 9,228 (Montgomery, 2016 only) and about 2-5k a year (Vancouver, over-75k earners only), 13 fiscal years for a temporal split, and overtime as a second target. The publisher of the old record was checked too: Montgomery County's 'Employee Salaries' releases for 2019-2025 (about 10k ...
