---
unique_name: wioa_employment_after_exit
name: 'WIOA Individual Performance Records (PIRL public use file): employment after exit from workforce programmes'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: social science
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.dol.gov/agencies/eta/performance/results/national
- https://www.dol.gov/sites/dolgov/files/ETA/advisories/TEGL/2016/TEGL_26-15-Attachment-II_Acc.pdf
- https://www.dol.gov/sites/dolgov/files/ETA/Performance/PY23%20Databooks/PY2023Appendix/WIOA%20Performance%20Records%20Public%20Use%20File%20Record%20Layout%20PY2023Q4.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the US Department of Labor's public use file of WIOA participant records (over 20 million records per quarterly file, 286 items), with an administrative outcome, employed in the second quarter after exit, that DOL's own adjustment model explains from participant characteristics; the per-person decision is written by the curation, and leaks, disclosure control and an ethics question need the curator.
- Source: DOL Employment and Training Administration, "WIOA Individual Performance Records (Public Use File)": files "contain detailed information on program completers (i.e., exiters)", each holds "a rolling ten (10) quarters of data" and "over 20 million records" (PY2025 Q1 to Q3 as CSV and Parquet; Q3 5.5 GB unzipped). Record layout by Social Policy Research Associates (PY2023 Q4, January 2025, read): PIRL reporting "began on July 1, 2016"; sections individual information ("gathered at program entry and is not updated subsequently"), program participation, services, outcomes, program-specific and calculated items (242 PIRL and 44 CALC items); "Unique records are defined by three fields: the state, individual ID and the exit date". Target PIRL 1602 Employed in 2nd Quarter After Exit Quarter (1 yes, 0 no, 9 not yet available); median earnings in the 2nd quarter after exit (PIRL 1704) as the regression alternative.
- Use case: DOL negotiates each state's performance levels with a statistical adjustment model of the outcome on participant characteristics and economic conditions (TEGL 26-15 Attachment II, read: "a fixed effects model" on individual records "aggregated to the State level on a quarterly basis"). The source's decision is on state aggregates; a per-person version (a local board or case manager, at entry or at exit, judging who needs more services) is written by the curation. Fit approximate. Regime temporal by exit quarter; grouped by state or local board possible.
- Siblings and duplicates: none among the records (searched WIOA, PIRL, WIASRD, workforce). Closest in kind: `anes_voting_2026` (the one accepted social-science task) and the ACS candidates `acs_household_broadband` and `acs_food_stamps_2014_2024` (survey answers, not a measured later outcome). External collections: none found.
- Better data: found by the gap scout for social science; no further search this round.
- Papers and pages: the DOL national results page, the SPRA record layout, TEGL 26-15 Attachment II. No paper on per-person prediction from the file was searched for (the web search budget ran out in this pass).
- Metric: none found for a per-person prediction (Attachment II scores no metric for its fixed-effects regression on state-quarter aggregates), so the fallback `roc_auc` (MET-1, MET-11); inputs none.
- Risks for /add-dataset: the prediction point (entry or exit) decides the columns: services and dates after entry, and every post-exit item (PIRL 1600 employed in the 1st quarter after exit, credentials, wages, occupation and industry after exit, the CALC performance items) leak the 2nd-quarter outcome (LEAK-10); outcome maturity: code 9, and the layout "Set to blank outcomes when it was too soon to report complete data", so keep exiters with complete outcomes and deduplicate the rolling ten quarters across files (SPLIT-9); disclosure control: exiters of local areas with "50 or fewer exiters in a program year" removed, employment codes "modified to avoid disclosing the data source", wages "randomly altered so that adjusted, rather than actual wages, are displayed" (keep with a note, PROV-3 as on framingham_heart_study_fhs; the earnings target is perturbed, so the binary target is the safer one); race, sex, disability, ex-offender and other barrier items are inputs and profiling job seekers is contested, so SEL-1 for the curator; the population to decide (Title I programs, or Wagner-Peyser and Veterans' programs too); millions of rows per program year call for a sample (`_1m`).
- Priority: gap + (social science has 1 accepted), use case 0 (DOL's model works on state aggregates; the per-person decision is ours), source + (an agency's documented file and record layout), shape + (millions of exiters, 286 items of mixed types, quarters and states), risk - (leaks to remove, perturbed values, the ethics question).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for social science.
- as published: more than 20 million participant records per file (PY2025 Q3: 5.5 GB CSV, also Parquet); about 230 PIRL data elements: demographics, barriers at entry (low income, long-term unemployed, ex-offender, ...; target: Employed in the 2nd quarter after the exit quarter (PIRL 1602, binary); median earnings in the 2nd quarter after exit as a regression alternative; access: open.
- Why: A federal agency's open, individual-level data with the outcome its own predictive model targets; the largest open labour-programme outcome file found.
- Adds: Labour and public services; temporal (program years) and grouped (state, local board) regimes; mixed types. Risks: outcome match-source codes modified for confidentiality and small local areas' exiters dropped; services and dates after entry leak; protected attributes among the columns (SEL-1 check); size calls for a ...
