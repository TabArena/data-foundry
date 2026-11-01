---
unique_name: county_health_rankings_premature_mortality
name: County Health Rankings & Roadmaps national data (analytic and trends files)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Website
year: '2010'
domain: medical & healthcare
problem_type: Regression
source_links:
- https://www.countyhealthrankings.org/health-data/methodology-and-sources/data-documentation
- https://www.countyhealthrankings.org/sites/default/files/2010%20Analytic%20Documentation.pdf
- https://www.countyhealthrankings.org/sites/default/files/media/document/Trends%20documentation%202025.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a county-level table, 2010-2025, of a ranking program's outcome (premature death, YPLL-75) and its determinants. Mortality and the determinants are counted over the same years, so no decision is made with a prediction.
- Source: County Health Rankings & Roadmaps (University of Wisconsin Population Health Institute). National data runs from 2010 (the 2010 Analytic Documentation) to the 2025 release and a March 2026 supplement (data documentation page, read 2026-10-31). Each release has analytic data (CSV, SAS), trends data for 15 measures (CSV, SAS) and documentation. The trends file layout (2025 Trends documentation): year span, measure name, state and county FIPS, numerator, denominator, raw value, confidence interval, measure id, release year and flags. Premature death is "Years of potential life lost before age 75 per 100,000 population (age-adjusted)", from the NCHS mortality files over three-year spans (1997-1999 to 2020-2022), and carries a data weight of 50% in the Rankings. The county count and the analytic file's columns were not checked.
- Use case: none for a prediction. The program ranks counties on measured outcomes and factors; the curated framing (estimate a county's premature mortality from its determinants) would be ours. Fit approximate at best. Regime grouped by county across releases, or temporal with a lag (the factors of release t, the mortality of a later span).
- Siblings and duplicates: `pollution` (`TBD -> 2nd Tier`, priority 1: McDonald & Schwing 1973, 60 SMSAs, the same explanatory regression). No CHR record existed before this run. External collections: none found.
- Better data: found as better data for `pollution` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the data documentation and the trends documentation; papers on the CHR model were not searched (web search budget used up).
- Metric: none found (a ranking program, no prediction task), so the fallback `rmse` (MET-1, MET-8). Inputs none.
- Risks for /add-dataset: mortality and the determinants are counted over the same window for all counties, a look back (SEL-6); a lag would fix it, and the curator decides. Several measures are outcomes or modelled small-area estimates close to the target, such as life expectancy, child and infant mortality, or poor health days (LEAK: keep determinants only). Overlapping three-year spans across releases repeat the same deaths (group by county, SPLIT). Small counties have suppressed values. The yearly files change measures and definitions, with trend breaks flagged. The terms of use were not read.
- Priority: gap 0 (medical not thin), use case 0 (none), source + (documented program), shape + (about 3,100 counties x 16 releases, grouped), risk - (no decision, same-window look back).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `pollution`.
- as published: one row per US county (about 3,100, count to verify) per annual release, 2010-2025, dozens of measures (ranked and additional) with numerators, denominators and CIs; target: premature age-adjusted mortality (deaths under 75 per 100,000, NCHS mortality files) or premature death (YPLL-75 per 100,000, age-adjusted): the same quantity ...; access: open (download without registration; terms of use not read).
- Why: same task as pollution: area mortality from air pollution, demography, education, income and housing of the area; features of the same kind (measured PM2.5 from the CDC Environmental Public Health Tracking Network instead of relative pollution potentials)
- Adds: about 3,100 counties against 60 metropolitan areas, 2010s data against 1959-1961, yearly releases (group by county). Risks: several measures are health outcomes or modelled small-area estimates close to the target (keep determinants only, LEAK), no climate columns, terms of use not read
