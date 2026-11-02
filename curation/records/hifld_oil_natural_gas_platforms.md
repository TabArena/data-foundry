---
unique_name: hifld_oil_natural_gas_platforms
name: Oil and Natural Gas Platforms
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Trivial
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: industry & manufacturing
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::oil-natural-gas-platforms/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/oil-natural-gas-platform
- https://arxiv.org/abs/2605.12292
- '# origin: BOEM Platform Structures, the live register of offshore structures (water depth in feet)'
- https://www.data.boem.gov/Platform/PlatformStructures/Default.aspx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: BOEM's offshore platform register with water depth as STRABLE's target, a surveyed property of the site that the kept lease block nearly fixes; no decision named, and `Trivial` is set as a concern to probe.
- Source: BOEM's Platform Structures register (https://www.data.boem.gov/Platform/PlatformStructures/Default.aspx: 7,091 structures, "Water Depth (feet)", install and removal dates, lease, coordinates; "data last updated: 10-31-2026"), copied by ORNL into the HIFLD Open layer "Oil and Natural Gas Platforms": "Offshore Oil and Gas Platforms in the Gulf of Mexico federal waters and off the US Pacific coast" (copy, ArcGIS item fcc8da5737d14d83b6ecf5c36bccaf7c); SOURCEDATE 2016-05 in every row; the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE: 7,137 platforms x 28 columns (4,597 removed, 2,540 in service); target WATERDEPTH (log); LATITUDE, LONGITUDE, DISTLAND and x/y dropped as leakage, AREANUMBER, BLOCKNO, LEASENO and COMPLEXID kept (preprocess_HIFLD-oil-natural-gas-platform.py). STRABLE Appendix C.2: "Offshore oil and gas platforms in US waters. The task is to predict platform status."
- Use case: none; water depth is surveyed before a platform is designed and BOEM records it for every structure. No decision fits that we can see, which is a reading rather than the source's words, so it stays a 2nd-tier candidate and not a fast reject; regime grouped by lease block if kept. Precedent: registry tables with a target picked by a benchmark went to `TBD -> 2nd Tier` with `No Good Target (yet)` (museums, journal_score_sjr, ai_jobs_net_salaries; Lennart).
- Siblings and duplicates: none among the records. External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data. BOEM's register is the live origin (2026 data against the 2016 HIFLD copy).
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-oil-natural-gas-platform.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD and its sources define no task); STRABLE scores every table with "R² for regression; AUROC for classification" (Appendix D.1), a benchmark-wide default rather than a choice for this task (MET-5), so the fallback rmse on feet, with target_transform log; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: the lease block (AREANUMBER plus BLOCKNO) sets the depth: 7,137 platforms sit in 2,481 blocks, and the variance of log depth within a block is 0.012 against 0.862 overall on the preview (TP-4; probe a split by block); STRABLE's paper names STATUS as the task, its config WATERDEPTH (USE-5); REMOVAL is filled for removed platforms only; the 2016 copy is stale against BOEM's live register (PROV-13).
- Priority: gap -, use case -, source + (BOEM through ORNL), shape + (7,137 platforms, 27 mixed columns), risk - (the location fixes the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 7,137 rows x 28 columns incl. target (STRABLE parquet); target: WATERDEPTH.
- Why: Predict the water depth of an offshore oil and gas platform
- Notes: HIFLD layer (BOEM-based). Paper says 'platform status'; config target is WATERDEPTH (regression).
