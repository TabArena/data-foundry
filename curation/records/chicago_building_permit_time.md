---
unique_name: chicago_building_permit_time
name: Chicago Building Permits
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
year: '2011'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu
- https://data.cityofchicago.org/api/views/ydr8-5enu.json
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: Chicago's 851,889 issued building permits of 2006-2026 with the days from the start of review to issue, the task of the accepted `sf_permit_time` in a second city with seven times the rows; issued permits only, so the same censoring cut applies.
- Source: City of Chicago, Department of Buildings, "Building Permits" on the Chicago Data Portal (ydr8-5enu, created 2011-09-30, updated daily): "building permits issued by the City of Chicago from 2006 to the present, excluding permits that have been voided or revoked after issuance". As published: 851,889 rows (SODA count, 2026-10-31; issue dates 2006-01-03 to 2026-10-30), one table: permit type, review type, work type, free-text work description, `application_start_date` ("Date when City began reviewing permit application"), `issue_date`, `processing_time` ("Number of days between APPLICATION_START_DATE and ISSUE_DATE"), reported cost, address and geography, fee columns, up to 15 contacts, and `residential_unit_change` (added 2026-10-27). Review types: express permit program 326,498 (mean 23.7 days), easy permit 167,825, standard plan review 140,527 (mean 52.5 days), sign 55,297, self cert 55,072, and smaller ones.
- Use case: an applicant or contractor, or the department staffing its reviews, estimates at filing how long a permit will take; our framing, as for `sf_permit_time`; the portal names no prediction. Fit direct for filed applications. Regime temporal by application date, like the sibling.
- Siblings and duplicates: `sf_permit_time` (`Yes`, BeyondArena, DataSF permits, temporal, RMSLE) is the record it was found for; another city's permits, so its own record (PROV-4), and the curator decides whether both enter. External collections: none known.
- Better data: found as better data for `sf_permit_time`; no further search this round.
- Papers and pages: the portal's dataset and column descriptions; chicago.gov/permit.
- Metric: none found (the portal's descriptions). Follow `sf_permit_time`'s RMSLE on the days (the fallback on the scale a waiting time is judged, MET-3), or `rmse`; inputs none.
- Risks for /add-dataset: issued permits only, so recent applications miss their slow permits (the right-censoring cut of `sf_permit_time`, CC 2026-10-01); `permit_condition` ("Conditions or comments added by reviewing department(s)"), `permit_status`, `permit_milestone`, the paid, unpaid and waived fees and `issue_date` are recorded at or after issue (LEAK checks); contact names are personal data, drop them; `issue_date` means "ready to issue, subject to payment" for most types but the paid issue for express permits, so the target differs by review type (USE-5); the work description is free text; above the row cap, so a cut (standard plan review alone is 140,527).
- Priority: gap 0 (industry, regression and temporal are not thin), use case 0 (our framing), source + (City portal with column definitions), shape + (851,889 permits, mixed types and text), risk - (post-issue columns, censoring).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sf_permit_time`.
- as published: 851,778 permits issued 2006-01-03 to 2026-10-29 (count on 2026-10-30); 11 permit types (express permit program 326,408, easy permit 207,651, renovation/alteration 168,293, signs 55,296, new ...; target: processing_time: days from the start of the City's review of the application to the issue date (the same quantity as sf_permit_time's days from filing to issue); access: open.
- Why: same target and use case as sf_permit_time (time to permit issue, predicted at filing) with features of the same kind: permit and review type, free-text work description, reported cost, location; like the SF table it holds issued permits only, so the same right-censoring cut applies
- Adds: about 7x the rows of the SF table (851,778 against 116,954 before filtering) and 20 years (2006-2026) against 2015-2025; a review_type column that separates standard plan review from express and easy permits; a second city. Check at screening: fee paid/unpaid columns and permit_condition may be filled after issue ...
