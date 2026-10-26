---
unique_name: inegi_gcim_vegetation_mapping_challenge
name: inegi-gcim-vegetation-mapping-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Data Quality Issue
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
domain: environmental science & climate
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/inegi-gcim-vegetation-mapping-challenge/data
- https://zindi.africa/competitions/inegi-gcim-vegetation-mapping-challenge
source_row: 885
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a real land-cover classification from INEGI with tabular per-point inputs, but the inputs are largely remote-sensing reflectance (SEL-13 boundary) and the labels are noisy by design.
- Source: Zindi / ITU "INEGI UN-GGIM Vegetation Mapping Challenge", 2 to 28 September 2024, data by INEGI, Mexico's national statistics and mapping agency (https://zindi.africa/competitions/inegi-gcim-vegetation-mapping-challenge); as published: Train.csv (about 1.1 MB) and Test.csv, per-record "values of remote sensing reflectance (year and dry season composites from Harmonized Landsat Sentinel imagery) as well as bioclimate data for precipitation and temperature, relief (elevation, slope, aspect, topographical position), canopy height", plus "a second set with the original noisy vegetation labels, and a third set with revised labels" (so several label sets, not a plain one table); 9 classes; one tile of about 150 x 150 km near Puerto Vallarta.
- Use case: INEGI cleans training labels for its deep-learning vegetation map, to replace "manual – visual interpretation"; the benchmark task would be per-point vegetation class from the covariates, an approximate fit to the stated label-cleaning goal; regime spatial (grouped) because points in one tile are spatially autocorrelated, the Zindi split is not described.
- Siblings and duplicates: `crowdsourced_mapping` (land cover from satellite time series) and `covertype` (cartographic covariates) are related tasks, not duplicates; no other INEGI record. External collections: none found.
- Papers and pages: competition page only; no paper or published solution found.
- Metric: multiclass log loss, Zindi Evaluation page ("The evaluation metric for this challenge is the Log Loss", submission Class_1 ... Class_9); a deliberate leaderboard choice (MET-4); inputs none; which label set the test is scored against (noisy or revised) is not stated (MET-1).
- Risks for /add-dataset: the reflectance bands are remote-sensing spectra, which SEL-13 counts as image-derived, mixed with many non-visual covariates (bioclimate, relief, canopy height) that may keep it tabular (SEL-15 vs SEL-13, a curator call); the target is noisy and the revised labels are "NOT exhaustively checked" (unclear target); coordinates and a spatial split need checking (SPLIT); row count unknown (Train.csv 1.1 MB suggests a few thousand rows).
- Priority: gap + (spatial grouped regime is thin), use case 0 (label cleaning, not the decision itself), source 0 (institutional but documented only on the competition page), shape 0 (size unknown), risk - (noisy target, SEL-13 doubt) -> 1 + 1 = 2.

The stated task is a label-cleaning / weak-supervision meta-task: build a model to identify outliers (wrong/suspicious labels) and suggest more plausible labels for vegetation mapping, rather than a clean predictive classification with a fixed target. That framing (data cleaning / label correction) does not map to a standard IID predictive task and risks a leaky/ill-defined target, and vegetation mapping can carry geospatial/remote-sensing characteristics. It could be repurposed into a straightforward land-cover classification if a trustworthy label column exists. A human must verify whether a clean categorical target and tabular features (not raster/remote-sensing) are available before considering it.

---

propose and develop a robust and accurate machine learning model that can help to clean and improve training data, either identifying outliers (wrong or suspicious labels), or even suggesting a more plausible label in the given test data
