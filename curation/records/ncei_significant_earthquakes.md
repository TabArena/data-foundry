---
unique_name: ncei_significant_earthquakes
name: Historical Earthquake Locations
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- STRABLE
original_source: GOV Website
year: '1972'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::historical-earthquake-locations/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/historical-earthquake-locations
- https://arxiv.org/abs/2605.12292
- '# the first source, NOAA NCEI (the HIFLD copy above returns 404 on 2026-10-31)'
- https://doi.org/10.7289/V5TD9V7K
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: NOAA NCEI's catalogue of significant earthquakes since 2150 BC, with the damage category as target; a rapid loss estimate after a quake is a real decision, but the catalogue is selected partly on damage and deaths, ships the other outcomes beside the target, and spans four millennia.
- Source: NOAA NCEI / World Data Service, "NCEI/WDS Global Significant Earthquake Database, 2150 BC to Present" (doi:10.7289/V5TD9V7K; ISO metadata: originator NGDC/WDS, publication date 1972-01-01, "over 5,700 earthquakes"; the HazEL API lists 6,697 events on 2026-10-31). Inclusion: an event that "caused deaths, caused moderate damage (approximately $1 million or more), magnitude 7.5 or greater", a Modified Mercalli Intensity of X or greater, or a tsunami; fields: date, location, focal depth, magnitudes, maximum MMI intensity, deaths, injuries, houses destroyed and damaged, "$ dollar damage estimates if available", each with a description category. STRABLE took the HIFLD copy (Significant_Earthquakes_....csv; the HIFLD page returns 404 on 2026-10-31) and kept the 3,998 events with a damage category (parquet previewed 2026-10-31): 62 columns; target `Damage Description (total)`, 4 classes: Limited (<$1 million) 1,121, Moderate (~$1 to $5 million) 1,307, Severe (~>$5 to $24 million) 1,006, Extreme (~$25 million or more) 564; median year 1961, 68% since 1900, a quarter before 1857.
- Use case: NCEI names "earthquake hazard assessment and mitigation", no actor or decision. In practice USGS PAGER estimates economic losses minutes after a quake from magnitude, location and exposure, to set an alert level for responders; a damage class from magnitude, depth, location and year mirrors that only roughly (no exposed population, dollars of the day, an observed intensity). Fit approximate (a use case of ours). Regime temporal: new events are predicted, and reporting and dollar values change over time (SPLIT-6).
- Siblings and duplicates: `earthquake` (Kaggle copy of the USGS catalogue 1990-2023, `No`, `No Good Target / Scientific Discovery` and `Time-series (Forecasting)`) and `quake` (Simonoff 1996, `No`, "not a predictive task originally"): catalogues without an impact target; this record differs by its target (damage), so their precedent does not carry over by itself; `nepal_earthquake_building_damage` (damage grades of buildings, another unit); `ncei_significant_volcanic_eruptions` (the sister NCEI hazard database). Not a duplicate. External collections: STRABLE (arXiv 2605.12292), "Historical Earthquake Locations": "Global database of significant historical earthquakes. The task is to predict earthquake magnitude", while STRABLE's config targets the damage category (an error of the copy, PROV-15).
- Better data: a candidate of the benchmark STRABLE; no further search this round (the NCEI source itself is larger and current: 6,697 events against STRABLE's 3,998 labelled).
- Papers and pages: NCEI's product page (https://www.ncei.noaa.gov/products/natural-hazards/tsunamis-earthquakes-volcanoes/earthquakes) and ISO metadata; the HazEL tool and API (https://www.ngdc.noaa.gov/hazel/); STRABLE's script `preprocess_HIFLD-historical-earthquake-locations.py` (github.com/soda-inria/strable); PAGER papers not read; papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the NCEI pages, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `log_loss` (MET-8, MET-11); the classes are ordered, so an ordinal treatment is the curator's call. Inputs none.
- Risks for /add-dataset: the other outcomes ship beside the target: deaths, injuries, missing, houses destroyed and damaged, their amount orders and descriptions and their `(total)` versions, and `Comments`, NCEI's narrative of the damage, all to drop (LEAK-10, USE-3); the observed maximum intensity is known only from field reports after the event; selection on the outcome: an event below $1 million enters only through deaths, magnitude, intensity or a tsunami (`Selection Bias`); damage in dollars of the day, with no inflation adjustment, and how NCEI assigns the class when no dollar figure is reported is to check in its documentation (USE-5); `URL`, `ID`, `OBJECTID`, `DRAWING_ORDER`, `x` and `y` are ids, display fields or projections; rebuild from NCEI (PROV-8, PROV-11), not the HIFLD copy.
- Priority: gap + (multiclass thin), use case 0 (the source names no actor), source + (NCEI DOI and metadata), shape + (3,998 events, 61 mixed columns, a time axis), risk - (outcome columns beside the target; selection on the outcome).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 3,998 rows x 62 columns incl. target (STRABLE parquet); target: Damage Description (total).
- Why: Predict the total damage category of a significant earthquake
- Notes: HIFLD copy of the NOAA NCEI Significant Earthquake Database. Paper says 'earthquake magnitude'; config target is 'Damage Description (total)' (multiclass).
