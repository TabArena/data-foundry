---
unique_name: ncei_significant_volcanic_eruptions
name: Historical Volcanic Locations
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- STRABLE
original_source: GOV Website
year: '2001'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::historical-volcanic-locations/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/historical-volcanic-locations
- https://arxiv.org/abs/2605.12292
- '# the first source, NOAA NCEI (the HIFLD copy above returns 404 on 2026-10-31)'
- https://doi.org/10.7289/V5JW8BSH
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: NOAA NCEI's catalogue of significant eruptions since 4360 BC, with the death-toll category as target; small (603 labelled eruptions of 210 volcanoes), selected on deaths, and its comments narrate the toll.
- Source: NOAA NCEI / World Data Service, "NCEI/WDS Global Significant Volcanic Eruptions Database, 4360 BC to Present" (doi:10.7289/V5JW8BSH; ISO metadata: publication date 2001-03-23, "a global listing of over 600 eruptions"; the HazEL API lists 903 on 2026-10-31). Inclusion: an eruption that caused deaths, caused moderate damage (about $1 million or more), had a VEI of 6 or more, generated a tsunami, or was associated with a significant earthquake; fields: location, elevation, volcano type, VEI, deaths, injuries, houses destroyed and damaged, damage estimates, references and comments. STRABLE took the HIFLD copy (the HIFLD page returns 404 on 2026-10-31) and kept the 603 eruptions with a deaths category (parquet previewed 2026-10-31): 50 columns; target `DEATHS_TOTAL_DESCRIPTION`, 4 classes: Few (~1 to 50 people) 417, Many (~101 to 1000) 94, Some (~51 to 100) 46, Very Many (~1001 or more) 46; median year 1929.
- Use case: NCEI: "These data are necessary for volcanic hazard assessments and mitigation efforts"; no actor or decision. Evacuations are decided before an eruption from monitoring data the table does not hold; a death-toll class after the fact serves hazard studies. Fit approximate at best. Regime temporal (new eruptions, mostly of known volcanoes, USE-10).
- Siblings and duplicates: `ncei_significant_earthquakes` (the sister NCEI database); `volcanoes` (Magellan radar images of Venus, `No`, `Image`): another task. Not a duplicate. External collections: STRABLE (arXiv 2605.12292), "Historical Volcanic Locations": "Locations and eruption history of significant volcanoes. The task is to predict the eruption type", while STRABLE's config targets the deaths category (an error of the copy, PROV-15).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: NCEI's product page (https://www.ncei.noaa.gov/products/natural-hazards/tsunamis-earthquakes-volcanoes/volcanoes) and ISO metadata; STRABLE's script `preprocess_HIFLD-historical-volcanic-locations.py` (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the NCEI pages, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `log_loss` (MET-8, MET-11); the classes are ordered. Inputs none.
- Risks for /add-dataset: selection on the outcome: deaths are an inclusion criterion and eruptions without deaths have no label in STRABLE's cut, so there is no "none" class (`Selection Bias`); `COMMENTS` narrate the deaths, and the injuries, missing, houses and damage columns are other outcomes (LEAK-10); small classes, 46 eruptions each for Some and Very Many, about 9 per test fold with 5 folds (TP-5, TP-8 to check); 603 rows of 210 volcanoes, so one volcano's eruptions repeat; `VALIDITY`, `STATUS`, `NUM_SLIDES` and the ids are record metadata.
- Priority: gap + (multiclass thin), use case 0 (the source names no actor), source + (NCEI DOI and metadata), shape 0 (603 eruptions), risk - (selection on deaths; outcome columns and comments).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 603 rows x 50 columns incl. target (STRABLE parquet); target: DEATHS_TOTAL_DESCRIPTION.
- Why: Predict the death-toll category of a significant volcanic eruption
- Notes: HIFLD copy of the NOAA NCEI Significant Volcanic Eruptions Database. Paper says 'eruption type'; config target is DEATHS_TOTAL_DESCRIPTION. Small: 603 rows.
