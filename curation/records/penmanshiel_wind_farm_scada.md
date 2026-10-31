---
unique_name: penmanshiel_wind_farm_scada
name: Penmanshiel wind farm data
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2022'
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zenodo.org/records/16807304
- https://zenodo.org/records/5946808
- https://doi.org/10.5281/zenodo.5946807
- https://arxiv.org/abs/2608.26613
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: nine years of 10-minute SCADA data from 14 turbines of the Penmanshiel wind farm, from the publisher and in the format of the Kelmarsh release; no task is published for it, and the one borrowed from Kelmarsh (a turbine's wind speed from its neighbours) is the curator's open question there.
- Source: Cubico Sustainable Investments (Charlie Plumley, Roberta Takeuchi), "Penmanshiel wind farm data", Zenodo v3, 2025-08-13, doi 10.5281/zenodo.16807304 (concept record 10.5281/zenodo.5946807, first version 2022), CC BY 4.0 (read 2026-10-31): 10-minute SCADA and event data from 14 Senvion MM82 turbines grouped by year from 2016 to the end of 2024, WT03 absent, not all signals for the full period, static data (coordinates, rated power, rotor diameter, hub height), the signal mapping, PMU and grid-meter data; 26 files, 7.5 GB. The release names no task; it asks users to say where, how and why they use the data.
- Use case: a wind-farm operator reconstructs or checks one turbine's wind speed or power from its neighbours when a sensor fails (the framing of the Kelmarsh community competition, carried over by the scout); fit approximate; regime temporal (10-minute rows), with turbines as groups.
- Siblings and duplicates: `kelmarsh_wind_farm_data` (Lennart `TBD -> Yes`, `Needs extensive data wrangling`: "Unclear if the task is reasonable") and `kelmarsh_wind_farm_2016_2024` (AI `TBD -> Yes`, priority 2, the newer Kelmarsh release) are another farm of the same publisher: not a duplicate or a version (PROV-4), but the curator would ship one farm or treat the farms as groups. `wind_turbine_scada_dataset` (`No`) is another source. External collections: none found.
- Better data: found as better data for `kelmarsh_wind_farm_data` (and in the curator's Zotero collection, item 257); no further search this round.
- Papers and pages: Masoumi et al., "Technical Comparative Benchmarking Study: Advanced AI Hybrid Methods for Renewable Energy Farm Optimization and Forecasting" (arXiv 2608.26613, 2026; abstract read) uses the Penmanshiel SCADA data for power forecasting (MAE in kW), a forecasting task and out of scope (SEL-10); the 2026 Kelmarsh provenance audit (Zenodo 23196733) replicates its checks on Penmanshiel v3 and reports no defect for it on the record page.
- Metric: none for this farm; the Kelmarsh community competition scored MAE (MET-4 for that framing, only a stand-in here), otherwise the fallback `rmse`.
- Risks for /add-dataset: the task (SEL-3; gap filling at the same timestamp, or forecasting under SEL-10 and SEL-11); hundreds of signals per turbine and signals that start late; 7.5 GB to cut to a window; the target turbine's own signals stay out of its features (LEAK-10).
- Priority: gap 0, use case 0 (a borrowed framing), source + (operator release with signal mapping and static data), shape + (14 turbines, 2016-2024, 10-minute rows), risk - (unsettled task, heavy wrangling).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `kelmarsh_wind_farm_data`; the curator's Zotero collection, item 257: "Technical Comparative Benchmarking Study: Advanced AI Hybrid Methods for Renewable ...".
- as published: 14 Senvion MM82 turbines (no WT03), 10-minute SCADA and events data grouped by year, 2016 to end of 2024 (2023 files by quarter), plus static, PMU and grid-meter data; files of 200-750 MB per year ...; target: the 10-minute wind speed or power at one turbine from the other turbines of the farm (same signals as Kelmarsh); access: open.
- Why: The same task, publisher, export system (Greenbyte) and signal mapping as Kelmarsh, at a second farm. | same publisher, format and turbine family as the Kelmarsh data behind kelmarsh_wind_farm_data, with 14 turbines instead of 6 and nine years; real operational data under an open licence
- Adds: More than twice the turbines (14 against 6, 28.7 MW against 12.3 MW), so more neighbours per target turbine and more turbine groups, over the same 2016-2024 span. The audit of Zenodo 23196733 replicated its Kelmarsh checks on Penmanshiel v3; read it for export defects before building. | more turbines (more groups for ...
