---
unique_name: dol_lca_h1b_offered_wages
name: OFLC LCA Programs (H-1B, H-1B1, E-3) disclosure data, US Department of Labor
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://www.dol.gov/agencies/eta/foreign-labor/performance
- https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY2025_Q4.xlsx
- https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Record_Layout_FY2025_Q4.pdf
- https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/FY26Q3/LCA_Record_Layout_FY2026_Q3.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: employer-filed wage offers for H-1B, H-1B1 and E-3 jobs over 18 fiscal years from the US Department of Labor, a strong and dated source, but a look-up of pay for a role, like the salary records the curator left in the 2nd tier, on a population of sponsored jobs.
- Source: US Department of Labor, ETA, Office of Foreign Labor Certification, "LCA Programs (H-1B, H-1B1, E-3)" disclosure data (dol.gov/agencies/eta/foreign-labor/performance): one annual xlsx per fiscal year FY2008-FY2019, cumulative quarterly files FY2020-FY2025, FY2026 through Q3 (determinations to 2026-06-30), each "containing unique records identified by the applicable OFLC case number". As published (FY2026 Q3 layout): case status and dates, visa class, `JOB_TITLE`, `SOC_CODE`, full-time and employment-type flags, employer name, address, FEIN and `NAICS_CODE`, worksite city, county, state and postal code, `WAGE_RATE_OF_PAY_FROM/TO` ("Wage paid to nonimmigrant workers at the First Worksite Location") with `WAGE_UNIT_OF_PAY`, `PREVAILING_WAGE` with its unit, `PW_WAGE_LEVEL` (I-IV) and source, H-1B-dependent and wilful-violator flags; row counts not checked.
- Use case: an employer, recruiter or candidate estimates the pay for a role, employer and place before an offer (ours; DOL publishes the files for disclosure and notes they "are not employer responses to the Bureau of Labor Statistics' Occupational Employment Statistics (BLS-OES) survey"); fit approximate. Regime temporal by `DECISION_DATE` (18 fiscal years).
- Siblings and duplicates: `ai_jobs_net_salaries` and `it_salary` (both `TBD -> 2nd Tier` with `No Good Target (yet)`; the curator on the first: "Unclear if this would be used for predictions or just insights") are the records this was found for; `data_scientist_salary`, `employee_salaries` (`TBD -> 2nd Tier`) and `stackoverflow_salary_data` (`No`) are other salary tasks. No other record of the LCA files (grep: H-1B, OFLC, labor condition, prevailing wage). External collections: none found.
- Better data: found as better data for `ai_jobs_net_salaries` and `it_salary`; no further search this round.
- Papers and pages: the OFLC performance page and the record layouts; no paper read.
- Metric: none found (DOL pages; disclosure data, no task); fallback `rmse` (MET-1, MET-8), likely on a log wage scored in dollars (MET-3); inputs none.
- Risks for /add-dataset: the offered wage may not fall below the prevailing wage, so `PREVAILING_WAGE` and `PW_WAGE_LEVEL` are a floor set before filing: known at the prediction point but close to the target (USE-6, a weighing call); `STATUTORY_BASIS` = "Wage" means an annual wage of $60,000 or more and goes (LEAK); the wage is a range with a unit to annualise (CLEAN); a certified LCA attests a wage before a petition and is not a hire; point-of-contact, attorney and preparer names and e-mails are personal data and go; the layout changed in FY2020 (align columns across years).
- Priority: gap 0 (business, regression, temporal not thin), use case 0 (ours), source + (government files with record layouts), shape + (hundreds of thousands of cases a year by the run's estimate, mixed columns, dates), risk - (a pay look-up as in the 2nd-tier salary records; target tied to the prevailing-wage floor): 2.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ai_jobs_net_salaries`, `it_salary`.
- as published: One Labor Condition Application case per row ('Each record is a unique case identified by its OFLC case number'); annual files FY2008-FY2019, quarterly files FY2020-FY2025, FY2026 through Q3 ...; target: Offered wage (wage rate of pay, annualised by its unit) for the position; restricted to data and AI SOC codes (e.g. 15-2051 Data Scientists, 15-1252 Software ...; access: open.
- Why: The same quantity as the record (annual pay of a tech job from title, seniority proxy, employer and location), measured from a legal filing by the employer instead of an anonymous self-report, from a government source with dated cases. | The same quantity as it_salary (annual pay of an IT job from position, ...
- Adds: A strong, traceable source; far more rows; 18 fiscal years for a temporal split. Caveats: only US jobs sponsored for H-1B/E-3 workers (a selected population); the prevailing wage and wage level are set from the SOC, area and level and sit close to the target (drop or justify, LEAK); employer names may need care. ...
