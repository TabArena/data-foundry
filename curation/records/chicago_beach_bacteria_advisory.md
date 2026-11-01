---
unique_name: chicago_beach_bacteria_advisory
name: Chicago Park District Beach Lab Data (E. coli culture and Enterococci qPCR tests at Lake Michigan beaches)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
year: '2016'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://data.cityofchicago.org/d/2ivx-z93u
- https://data.cityofchicago.org/d/xvsz-3xcj
- https://data.cityofchicago.org/d/qmqz-2xku
- https://data.cityofchicago.org/d/k7hf-8y75
- https://github.com/Chicago/clear-water
- https://doi.org/10.5281/zenodo.1053023
- https://doi.org/10.1016/j.wroa.2018.100016
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Chicago's beach-day bacteria tests of 2006-2026 with the City's own published nowcast task (does a beach exceed the swim-advisory level today, from same-day tests at other beaches); the task table has to be assembled by date.
- Source: Chicago Park District with the UIC School of Public Health laboratory, "Beach Lab Data" on the City of Chicago Data Portal (2ivx-z93u, created 2016-05-04, updated 2026-10-08), with portal tables of water sensors (qmqz-2xku), beach weather stations (k7hf-8y75) and the City's published predictions (xvsz-3xcj). As published: 34,967 rows (SODA count, 2026-10-31), one per beach and sample, with two replicate readings and their mean for culture E. coli (17,963 rows, to 2016-09) and qPCR Enterococci DNA (17,594 rows, 2015 to 2026-09); 31 beach names. Of the culture means 2,497 exceed 235 CFU (13.9%), of the DNA means 1,227 exceed 1,000 CCE (7.0%).
- Use case: the Park District decides each morning which beaches get a swim advisory; the portal: "When DNA bacteria levels exceed 1000 CCE, a yellow swim advisory flag is implemented", and the culture test "requires 18-24 hours of processing". Lucius et al. predict exceedance at untested beaches from same-day tests at a few beaches, a model that "can be used to inform management decisions on when to warn residents or close beaches". Fit direct. Regime temporal by season: the paper tunes by "leave-one-year-out cross validation" and holds out 2016 (Sec. 2.7); a nowcast from same-day readings at other sites, not a forecast of the series (SEL-10, SEL-11).
- Siblings and duplicates: `water_quality` (`No`, AHDS: "imaginary data") is the record it was found next to, a different task; no earlier record of Chicago's beach data (grep over curation/records for beach and E. coli). External collections: none known.
- Better data: found as a real task next to `water_quality`; no further search this round.
- Papers and pages: Lucius, Rose, Osborn, Sweeney, Chesak, Beslow, Schenk, "Predicting E. coli concentrations using limited qPCR deployments at Chicago beaches", Water Research X (online 2018-12-27, doi 10.1016/j.wroa.2018.100016, PMC6549907); code github.com/Chicago/clear-water (Zenodo 10.5281/zenodo.1053023, v1.2.0, MIT; Master.R trains on 2006-2015, tests on 2016, threshold 235 CFU).
- Metric: the paper fixes the operating point from the decision: "By constraining the model to only have a 1.8 percent false-positive rate, the true positive rate is forecasted to be 22 percent" (Sec. 2.7), 1.8% being the historical false-positive rate of the prior-day model, and reports sensitivity and precision at that point (abstract: sensitivity "from 3.4 percent to 11.2 percent"). A deliberate operating point (MET-5, MET-7): sensitivity at a 1.8% false-positive rate needs a custom metric (MET-13); otherwise `roc_auc`, the fallback, which the paper also plots. Inputs none.
- Risks for /add-dataset: build the task table by pivoting other beaches' same-day readings into features (joins by date, missing tests, which beaches are the tested ones); the method changes in 2015-2016 (culture E. coli at 235 CFU, then qPCR Enterococci at 1,000 CCE), so one era or the other (USE-5); each beach's own replicate readings are the target's inputs and go (LEAK checks); a few dates carry the years 0016 and 0023 (typos to repair); the City's predictions table is a model's output, never a feature.
- Priority: gap 0 (environment, binary and temporal are not thin), use case + (named by the source), source + (City portal and a peer-reviewed paper), shape + (about 18,000 beach-days per method, 20 seasons), risk - (task table to assemble, method change).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `water_quality`.
- as published: 34,967 beach-day sample rows (SODA count, 2026-10-30): about 17,000 culture E. coli rows 2006-2016 (1,450-1,730 a season) and about 17,600 qPCR Enterococci DNA rows 2015-2026 (1,700-2,000 a season, ...; target: whether a beach's bacteria level exceeds the swim-advisory threshold (qPCR Enterococci above 1,000 CCE, the yellow-flag level; or culture E. coli above the ...; access: open.
- Why: A real, open water-safety classification with a decision behind it; water_quality has no real counterpart (its is_safe is set from limits on the same 20 imaginary concentrations)
- Adds: Real measurements, 20 seasons, a named publisher and a documented decision. Caveats: microbial recreational water, not drinking-water chemistry; features must be assembled (other beaches' same-day tests, weather and water sensors); lagged-value designs would turn it into forecasting, the cross-beach nowcast does not
