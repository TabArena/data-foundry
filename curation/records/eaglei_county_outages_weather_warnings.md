---
unique_name: eaglei_county_outages_weather_warnings
name: A spatiotemporally harmonized dataset of utility-reported power outages and NWS VTEC weather warnings for the contiguous United States (2015-2024)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2026'
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1038/s41597-026-08356-z
- https://doi.org/10.5281/zenodo.22651795
- '# the EAGLE-I outage data this archive is built from (Brelsford et al. 2024, Scientific Data)'
- https://doi.org/10.1038/s41597-024-03095-5
- '# another dataset (Mukherjee et al. 2018, major US outage events 2000-2016), a smaller alternative, not this record''s data'
- https://doi.org/10.1016/j.dib.2018.06.067
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a 2026 Data Descriptor that links EAGLE-I county outages with NWS watches and warnings for co-occurrence analysis; the primary file holds only outage hours that overlap a warning, so a target and its negatives have to be built.
- Source: Saki, Sofia, Kar and Anagnostou, "A spatiotemporally harmonized dataset of utility-reported power outages and NWS VTEC weather warnings for the contiguous United States (2015-2024)", Scientific Data, 2026 (doi:10.1038/s41597-026-08356-z, PMC13642956); Zenodo doi:10.5281/zenodo.22651795 (CC BY 4.0, 2026-09-08). As published: `Eagle_I_US_2024_with_VTEC_Updated.csv` (367 MB; county x hour rows with `fips_code`, `Hour`, `max_rolling_avg`, `state`, `county`, `median_sum`, `new_event_no`, `evDur_Hr`, `evDur_day`, `Max_outage`, three completeness columns, `WFO`, `Matched_Events`, `Matched_Count`; header read from a preview; "The county-hour table contains millions of rows", Usage Notes), the warning archive `NWS_WARNINGS_COMBINED_data_Updated.csv` (832 MB), daily county source availability, sensitivity summaries and shapefiles. Abstract: "The primary released file contains hourly indexed, positive processed outage observations that overlap at least one VTEC warning". The outage records come from EAGLE-I (Oak Ridge National Laboratory), first published as Brelsford et al., "A dataset of recorded electricity outages by United States county 2014-2022", Scientific Data 11:271, 2024 (doi:10.1038/s41597-024-03095-5; 15-minute county estimates).
- Use case: a utility or an emergency manager, when a warning is issued for a county, stages crews for the outage it expects (the paper cites such decision-support work, e.g. Watson, Pasqualini and Anagnostou 2024, IEEE Access); fit approximate at best: the source says "The dataset supports reproducible analysis of spatiotemporal co-occurrence" (Abstract) and "Warning-outage matches represent spatiotemporal co-occurrence and should not be interpreted as proof that the matched warning caused the outage" (Usage Notes); regime temporal (hourly records 2015-2024).
- Siblings and duplicates: `smart_grid_stability_and_reliability_dataset` (`No`, a declared synthetic table, the record this was found for); `sinalize_sin_transformer_forced_outages` and `distribution_transformers_at_cauca_department` (equipment failures, other tasks). No record of the EAGLE-I data itself (grep: eagle, outage). External collections: none found.
- Better data: found as better data for `smart_grid_stability_and_reliability_dataset` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the Data Descriptor (Background, Methods, Usage Notes); Brelsford et al. 2024; Lee et al., "Predicting Power Outage During Extreme Weather Events with EAGLE-I and NWS Datasets", IEEE IRI 2023 (doi:10.1109/IRI58017.2023.00042, cited by the descriptor, not read); Mukherjee et al. 2018, Data in Brief (1,534 major US outage events 2000-2016, doi:10.1016/j.dib.2018.06.067), a different and smaller dataset, noted in `source_links`.
- Metric: none found (the descriptor defines no task; its technical validation is sensitivity summaries), so the fallback: `rmse` on an outage size or `roc_auc` on an outage flag; inputs none.
- Risks for /add-dataset: no target as published (`No Good Target (yet)`, SEL-3, USE-2): the event table holds positives only, and "an absent source record cannot be assumed to represent a verified zero-outage condition" (Background), so negatives from the warning archive need the availability file; an hourly county stream is close to forecasting (SEL-10, SEL-11, TP-10: no lagged outage as a feature); event-level aggregation and the warning join (`Needs extensive data wrangling`); outage counts scale with a county's customers (normalise or add the customer count).
- Priority: gap 0 (no thin domain, problem type or regime), use case 0 (the source names analysis, not a decision), source + (Scientific Data descriptor, DOE platform), shape + (ten years, all contiguous US counties), risk - (target and negatives to build, forecasting-like stream).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `smart_grid_stability_and_reliability_dataset`.
- as published: County x hour outage records for the contiguous US, 2015-2024, joined to NWS watches and warnings (VTEC) with a multi-hazard index; primary CSV 367 MB; row count not stated on the Zenodo page (to ...; target: Whether a county has a significant customer outage during a weather warning, or its peak customers out / outage duration; access: open.
- Why: The Kaggle record (declared synthetic) predicts grid stability and failure risk from grid sensors and weather; this is real grid failure under weather at county level, with features known at the warning (hazard type, county, season, history)
- Adds: Real, traceable outage data of ten years across the US instead of a generated table. Needs an event-level target built from hourly records and a temporal split; check it does not turn into hourly forecasting. Smaller, simpler alternative: Mukherjee et al. 2018, Data in Brief (1,534 major US outage events 2000-2016, ...
