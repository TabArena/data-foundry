---
unique_name: ntia_internet_use_survey_home_adoption
name: NTIA Internet Use Survey (CPS Computer and Internet Use Supplement) public-use datasets
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: GOV Website
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.ntia.gov/page/download-ntia-internet-use-survey-datasets
- https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-computer.html
- https://www2.census.gov/programs-surveys/cps/techdocs/cpsnov23.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: NTIA's Computer and Internet Use Supplement to the CPS, 17 waves from 1994 to 2023 with documented items, but the target (does anyone in the household use the internet at home) is the household's own answer in the interview and no source defines a prediction task on it, the same open points as `acs_household_broadband`.
- Source: National Telecommunications and Information Administration (NTIA) with the US Census Bureau. NTIA's download page lists public-use files for Nov 1994, Oct 1997, Dec 1998, Aug 2000, Sep 2001, Oct 2003, Oct 2007, Oct 2009, Oct 2010, Jul 2011, Oct 2012, Jul 2013, Jul 2015, Nov 2017, Nov 2019, Nov 2021 and Nov 2023 (posted 2024-08-30), in Stata, R, CSV and fixed format with Census documentation. As published (Census technical documentation for November 2023, cpsnov23.pdf): the month's CPS, "approximately 44,000 interviewed households", supplement questions "asked of persons 3 years old and over"; one record per person with household items. Target HEINHOME, "(Does anyone in this household / do you) use the Internet at home?" (1 yes, 2 no); PEINHOME says who.
- Use case: none named by the source; NTIA publishes the files for its Internet Use Survey reports and Data Explorer. The scout's actor (a state digital-equity office targeting outreach at offline households from administrative data) is written by the curation and does not count (USE-1); fit approximate. Regime temporal by wave; one row per household, or grouped by household if person rows stay.
- Siblings and duplicates: `acs_household_broadband` (ACS PUMS, about 1% of US housing units a year, HISPEED; `TBD -> 2nd Tier`, priority 2, `No Good Target (yet)`) holds the same household target for many more households a year; `internet_usage` and `kdd_internet_usage` (GVU 1997 survey of web users only; `TBD -> 2nd Tier` and `No`); `adult` and `census_income` (CPS extracts; `No`, "no actor decides on whether income exceeds 50K") are the closest precedent for a CPS answer as the target. External collections: none found.
- Better data: found as a related task next to `internet_usage` (not better data for it); no further search this round.
- Papers and pages: NTIA's download page; the Census CPS November 2023 technical documentation. Papers that predict home internet adoption from the supplement were not searched: the session's web search budget ran out.
- Metric: none found (NTIA reports weighted shares), so the fallback `roc_auc` (MET-1, MET-8).
- Risks for /add-dataset: settle the task first (SEL-3, SEL-7, `No Good Target (yet)`); the target is a household item on person rows (USE-5, SPLIT-24); computer, smartphone, mobile-data and internet-at-other-places items of the same interview are near-proxies (LEAK-10); wording and universes change between waves (in 2023 HEINHOME's universe is HETVBOX = 1, 2), so stacking waves needs a harmonised target; CPS weights are design columns.
- Priority: gap 0, use case 0 (written by the curation), source + (NTIA and Census documentation), shape + (about 44,000 households a wave, 17 waves, mixed items), risk - (no task definer and a self-reported target; the ACS sibling holds the same target at a larger scale).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `internet_usage`.
- as published: one row per person in the CPS November supplement (household and person records; the CPS interviews about 50,000 households per month, persons and columns to verify in the techdocs); waves Nov 1994, ...; target: whether the household uses the internet at home (or has a home broadband subscription); variable names to check in the techdocs; access: open.
- Why: The same kind of survey as the GVU 1997 internet-user survey (demographics and internet use) but a national probability sample that includes non-users, so it carries a target someone acts on; the GVU file surveyed only web users and its target (years online) has no use case
- Adds: A government source, about 5x the respondents per wave, 17 waves to 2023 for a temporal split, and a decision-relevant target instead of 'Actual_Time'
