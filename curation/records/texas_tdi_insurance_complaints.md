---
unique_name: texas_tdi_insurance_complaints
name: 'Insurance complaints: All data (Texas Department of Insurance)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: insurance
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://data.texas.gov/d/ubdr-4uff
- https://data.texas.gov/d/jjc8-mxkg
- https://www.tdi.texas.gov/tips/ways-we-can-help.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: every complaint the Texas Department of Insurance closed since mid-2012 (293,168 complaints; 309,247 complaint-respondent rows), with TDI's finding whether the licensee was in error (19% confirmed); an outcome known only after the review, predictable at intake as in `consumer_complaints`, in the thin insurance domain.
- Source: Texas Department of Insurance on the Texas Open Data Portal: "Insurance complaints: All data" (ubdr-4uff: "a row for each person and organization named in a complaint") and "Insurance complaints: One record / complaint" (jjc8-mxkg, without the respondent), created 2021, refreshed 2026-10. As published (Socrata API, 2026-10-31): received 2011-04-28 (13 rows in 2011) to 2026-10-23, 11,000 to 27,000 complaints a year; 17 documented columns: complaint number, respondent name, id, role and type, complainant role and type, reason, `complaint_confirmed_code` ("A 'Yes' answer means TDI confirmed the licensed person or organization was in error"; Yes 58,038, No 251,209 rows), disposition, received and closed dates, complaint type, coverage type and level, involved party type, keyword.
- Use case: TDI's complaint staff estimate at intake whether a complaint will be confirmed against the company, agent or adjuster, to prioritise the review (a consumer or advocate could use the same estimate); the source describes the complaint process (tdi.texas.gov, "How to get help with an insurance issue or file a complaint") but names no prediction; fit approximate. Regime temporal by received date, as `consumer_complaints`; respondents recur, a grouped question inside the temporal split (SPLIT-3).
- Siblings and duplicates: `insurance_complaints` (`TBD -> 2nd Tier`, `No Good Target (yet)`; Connecticut Insurance Department, no outcome column) is the record it was found for, another regulator, not a duplicate. `consumer_complaints` (`Yes`, shipped; CFPB complaints) is the precedent for predicting a complaint's outcome at receipt. External collections: none found.
- Better data: found as better data for `insurance_complaints`.
- Papers and pages: the two portal datasets; TDI's help page; no paper or competition found.
- Metric: none found (the portal descriptions and TDI's page define no task), so the fallback `roc_auc`; inputs none.
- Risks for /add-dataset: disposition and closed date are outcomes (drop, LEAK-10); keywords may be added during handling (check, LEAK); only closed complaints are published (no row lacks a closed date), so the latest months hold only the quickly closed ones (right-censoring as in `consumer_complaints`: mature the test window, SPLIT-9); a complaint against several respondents has several rows (take the one-record view or define the unit, USE-4); respondent name and id are high-cardinality.
- Priority: gap + (insurance is thin), use case 0 (the curation's), source + (a state regulator with column definitions), shape + (293k complaints over 14 years, categorical mix, dates), risk - (outcome columns, censoring of open complaints).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `insurance_complaints`.
- as published: 309,136 rows (one per complaint x named respondent) = 293,062 complaints (the one-record-per-complaint view jjc8-mxkg), received 2011-04-28 to 2026-10-23; 17 columns: complaint number, respondent ...; target: complaint_confirmed_code: TDI confirmed that the licensed company, agent or adjuster was in error (binary, about 19% Yes); access: open.
- Why: The same task as the CT record (consumer complaints against insurers at a state insurance regulator, with the outcome of the regulator's review), with a clear, binary outcome column the CT file lacks (its 'No Good Target (yet)'); features of the same kind (company, coverage, reason, dates)
- Adds: 3.4x the complaints of the CT file (90,081 rows, 2015-2026), 15 years for a temporal split, and a target someone acts on. Leaks to drop: disposition and closed date are outcomes; check whether keywords are assigned during handling. Group by respondent or split by received date.
