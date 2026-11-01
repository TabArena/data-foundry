---
unique_name: hifld_pol_terminals
name: POL Terminal
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
domain: industry & manufacturing
problem_type: Regression
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::petroleum-terminals/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/pol-terminal
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: an ORNL/ANL inventory of US bulk petroleum terminals with shell storage capacity as STRABLE's target; it could serve to estimate terminals without a reported capacity, but no source names that use.
- Source: the HIFLD Open layer "POL Terminals" (ORNL, ANL and the NGA HSIP team): "Data contains locational and other attribute information for operable bulk petroleum product terminals with a total bulk shell storage capacity of 50,000 barrels or more, and/or ability to receive volumes from tanker, barge, or pipeline ... for a total of 2,302 terminals" (copy HSEMA_PPD, ArcGIS item 6e4d363ba51b4408a7bc046f44e9db83); SOURCE values include AirNav, tankterminals.com and Google Maps; the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE: 2,091 terminals x 52 columns; target CAPACITY, transformed by a cube root (barrels by the layer's description; median about 251,000, 14 zeros, 158 under 50,000 on the preview) (preprocess_HIFLD-POL-terminal.py). STRABLE Appendix C.2: "Petroleum, Oil, and Lubricant storage terminals. The task is to predict storage capacity."
- Use case: an energy-security or emergency planner estimating the storage of a terminal whose capacity is not reported, from its type, commodities, transport modes and operator; not named by a source; fit approximate; regime IID (one row per terminal). Precedent: registry tables with a target picked by a benchmark went to `TBD -> 2nd Tier` with `No Good Target (yet)` (museums, journal_score_sjr, ai_jobs_net_salaries; Lennart).
- Siblings and duplicates: none among the records. External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-POL-terminal.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD and its sources define no task); STRABLE scores every table with "R² for regression; AUROC for classification" (Appendix D.1), a benchmark-wide default rather than a choice for this task (MET-5), so the fallback rmse in barrels (STRABLE's cube root is no spec transform; log1p fits, given the zeros); inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: whether a capacity of 0 means unknown (CLEAN); the 50,000-barrel threshold of the layer cuts the low end; POPULATION is filled for 18 rows; EXSTARS_I looks like the IRS terminal control number (an identifier); OWNER and OPERATOR are names of high cardinality; the HIFLD file is offline, so it needs a surviving copy (PROV-13).
- Priority: gap -, use case -, source + (ORNL and ANL, documented), shape + (2,091 terminals, 51 mixed columns), no known risk beyond the zeros.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 2,091 rows x 52 columns incl. target (STRABLE parquet); target: CAPACITY.
- Why: Predict the storage capacity of a petroleum, oil and lubricant terminal
- Notes: HIFLD layer.
