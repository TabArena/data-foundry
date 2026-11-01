---
unique_name: hifld_mobile_home_parks
name: Mobile Home Parks
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::mobile-home-parks/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/mobile-home-parks
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the source says why park sizes matter (emergency preparedness), but STRABLE's size class is a bin of the kept UNITS where UNITS is known and has no unit count behind it for the other 83% of rows, most of them found on imagery.
- Source: the HIFLD Open layer "Mobile Home Parks" (ORNL and DHS GMO): "An inventory of mobile home park locations and the number of mobile homes within those parks is, therefore, essential for emergency preparedness, response, and evacuation" (copy in FEMA's "Mobile Home Parks RAPT", ArcGIS item 2ba2e5e2007f4a159d4dfab8534beed3, downloaded 2025-07-22). Rows come from state registries (California HCD, Florida Health, New York, Indiana, Wisconsin), from 2010 Census blocks "to contain 10 or more mobile homes/trailers" (8,678 rows) and from imagery (SOURCE "IMAGERY", 35,239 rows) (preview); the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE: 56,094 parks x 26 columns; target SIZE in three classes, SMALL (<50) 39,899, MEDIUM (51-100) 9,086, LARGE (>100) 7,109; UNITS kept as a feature (preprocess_HIFLD-Mobile-home-parks.py). STRABLE Appendix C.2: "Geographic locations and capacities of mobile home parks. The task is to predict the number of lots."
- Use case: an emergency manager planning an evacuation needs the number of homes in a park no registry counts (the source's words above); a size estimate from location, type and name serves that; fit approximate (most labels are estimates themselves); regime IID (one row per park).
- Siblings and duplicates: none among the records. External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-Mobile-home-parks.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD defines no task); STRABLE scores classification by AUROC (Appendix D.1), a benchmark-wide default (MET-5), so the fallback log_loss for the three classes, or rmse if re-targeted to UNITS; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: SIZE is the bin of UNITS where UNITS is known (9,766 rows; the bin rule matches 95.5% of them on the preview), so UNITS goes (SEL-5); the other 46,328 rows have no unit count and VAL_METHOD "IMAGERY ONLY" or "IMAGERY/OTHER", so their class may be an analyst's reading of aerial imagery (to confirm from HIFLD's metadata; then the label is an image reading, SEL-13, USE-5); a re-target to UNITS on the registry rows (regression, about 9,800 parks) may be the cleaner task; STRABLE's paper and config disagree on the target; MHPID and x/y are identifiers and projected coordinates.
- Priority: gap + (multiclass is thin), use case - (a need the source names, not a prediction with a direct fit), source + (ORNL, a SOURCE per row), shape + (56,094 parks), risk - (the label is a bin of a kept feature or an imagery estimate).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 56,094 rows x 26 columns incl. target (STRABLE parquet); target: SIZE.
- Why: Predict the size class of a mobile home park
- Notes: HIFLD layer. Paper says 'number of lots'; config target is SIZE (multiclass).
