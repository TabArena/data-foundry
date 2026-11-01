---
unique_name: hdx_conflict_events
name: Conflict Events
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- STRABLE
source_links:
- https://data.humdata.org/dataset/acled-data
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/conflict-events_wide
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-6): STRABLE sums HDX HAPI's monthly ACLED counts over the 2024 file, so each row is an admin-2 area and event type with its events and fatalities counted over the same calendar year: the target is a count over one window shared by all rows, next to a feature (`events`) from that window, which supports only a look back; the predictive framing of the monthly series, next month's fatalities, is forecasting (SEL-10).
- Source: ACLED (Armed Conflict Location & Event Data Project), served by OCHA's HDX HAPI as "HDX HAPI - Coordination & Context: Conflict Events" (https://data.humdata.org/dataset/hdx-hapi-conflict-event; documentation https://hdx-hapi.readthedocs.io/en/latest/data_usage_guides/coordination_and_context/): "HDX HAPI leverages ACLED's publicly accessible data, aggregated on a monthly basis and to administrative regions"; "events: The number of events with the given event_type"; "fatalities: The number of fatalities due to the given event_type"; "The three event categories are not mutually exclusive". The record's link https://data.humdata.org/dataset/acled-data answers 404; the HAPI page above replaces it.
- STRABLE's cut (scripts/script_preprocess_data/preprocess_ohca_conflict-events_wide.py): hdx_hapi_conflict_event_global_2024.csv, admin level 0 dropped, `data.groupby(groupby_col, as_index=False).agg({'events': 'sum', 'fatalities': 'sum'})` over area, event type and HDX ids, rows with events > 0 kept: 1,520 rows x 13 columns from 7 countries, target fatalities (transformed by STRABLE), features area names and codes, event type, HDX dataset and resource ids, a p-code warning, and events.
- Use case: none: an area's fatalities in a year beside its event count for the same year describe that year; the event categories overlap (civilian targeting is part of political violence), so rows double count.
- Siblings and duplicates: `wfp_food_prices` (another HDX-served STRABLE table); no ACLED record (searched acled, conflict, humdata). External collections: STRABLE ("Conflict Events", App. C.2: "to predict the number of fatalities").
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Metric: none found; STRABLE scores R^2 (App. D.1).
- Reject check (AI, 2026-10-31): stands. STRABLE groups the 2024 file by area, event type and HDX ids, without the month, and sums `events` and `fatalities` (https://github.com/soda-inria/strable/blob/main/scripts/script_preprocess_data/preprocess_ohca_conflict-events_wide.py). The target is therefore counted over one calendar year shared by all rows, next to the same year's event count, which allows only a look back. The monthly series would give next-month fatalities from the target's own lags: forecasting (SEL-10).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,520 rows x 13 columns incl. target (STRABLE parquet); target: fatalities.
- Why: Predict the number of fatalities in an admin-area conflict-event aggregate
- Notes: Raw file hdx_hapi_conflict_event_global_2024.csv (HDX HAPI, ACLED-based counts per admin2 area and event type; 'events' count is a feature). Config source spelled 'OHCA' (OCHA). Rows are area aggregates, not single events.
