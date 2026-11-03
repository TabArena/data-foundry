---
unique_name: hifld_prison_boundaries
name: Prison Boundaries
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::prison-boundaries/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/prison-boundaries
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a federal inventory of 3,755 US correctional facilities whose capacity STRABLE made the target; the layer serves homeland-security and emergency planning, and no decision predicts a prison's capacity from its name, type, security level and footprint.
- Source: HIFLD Open layer "Prison Boundaries" (DHS Homeland Infrastructure Foundation-Level Data: facility polygons with name, address, type, status, security level, population and capacity; source and validation dates 2007-2024 in STRABLE's cut). HIFLD Open went offline in August-September 2025; the Data Rescue Project archived its 415 layers in DataLumos (https://www.datarescueproject.org/hifld-data-saved/), and HIFLD Next re-hosts them. As used by STRABLE (HF parquet, previewed): 3,755 rows x 23 columns, target `CAPACITY` shipped as a cube root (1.0 to 21.5, about 1 to 10,000 beds), `POPULATION` dropped, no -999 "not available" capacities left.
- Use case: none in the source; filling a missing capacity for evacuation or emergency planning would be the curation's own (USE-1). Fit none to approximate; regime IID (one inventory snapshot, no outcome time).
- Siblings and duplicates: no duplicate (grep for prison, HIFLD, the layer link); the other HIFLD layers of STRABLE screened in this run: `hifld_public_schools`, `hifld_transmission_lines`, `hifld_transmission_towers`, `hifld_hospitals`, `hifld_colleges_and_universities` and more `hifld_*` records. External collections: STRABLE (Table C.4 row 89: "Geospatial boundaries and capacities of US correctional facilities. The task is to predict population.", while its `config.json` sets `CAPACITY`).
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19), Sec. 3 (tables "paired with a target variable", a "snapshot strategy", a skewness-minimizing target transform); no paper that predicts from this layer found.
- Metric: none found (HIFLD publishes no task; STRABLE scores R² for every regression task, App. D.1 "Evaluation metrics", a benchmark-wide choice, MET-5), so the fallback `rmse` on the bed capacity (STRABLE's cube root is a modelling scale, MET-3); inputs none.
- Risks for /add-dataset: no task (`No Good Target (yet)`; SEL-3, USE-2); `POPULATION` would be a near-copy of the target if restored (LEAK-10); 41% of `SECURELVL` is "NOT AVAILABLE"; the source is offline, so a build reads the DataLumos archive, not STRABLE's transformed cut (PROV-13).
- Priority: gap 0, use case 0, source + (HIFLD layer metadata, a government inventory), shape + (3,755 facilities, categorical, string and numeric columns), risk - (no task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 3,755 rows x 23 columns incl. target (STRABLE parquet); target: CAPACITY.
- Why: Predict the capacity of a US correctional facility
- Notes: HIFLD layer. Paper says 'population'; config target is CAPACITY.
