---
unique_name: kelmarsh_wind_farm_2016_2024
name: Kelmarsh wind farm data (latest Zenodo version, SCADA 2016 to end of 2024)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2025'
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zenodo.org/records/16807551
- https://zenodo.org/records/5841834
- https://zenodo.org/records/23171808
- https://zenodo.org/records/23196733
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the current Zenodo version (2025-08-12) of the Kelmarsh SCADA release behind `kelmarsh_wind_farm_data`, 2016 to end of 2024 instead of mid-2021; the same task with the same doubts on it, and a documented export defect in the 2023 and 2024 turbine files.
- Source: Cubico Sustainable Investments (Plumley and Takeuchi), Zenodo 10.5281/zenodo.16807551 (2025-08-12, CC BY 4.0): "10-minute SCADA and events data from the 6 Senvion MM92's at Kelmarsh wind farm, grouped by year from 2016 to end 2024 ... Note not all signals are available for the entire period", with static data, the signal mapping, PMU and grid-meter data; yearly SCADA zips of 98 MB (2016) to 716 MB (2023). The version the parent record links (Zenodo 5841834, v0.0.3, 2022-02-01) covers 2016 to mid-2021.
- Use case: as `kelmarsh_wind_farm_data`: the Kaggle community competition (2024) "Predict the wind speed at a target wind turbine, only using data from neighbouring wind turbines"; an operator would fill in or check a failed anemometer from the neighbours. The release names no task (it asks for "performance analysis/improvement opportunities"). Fit approximate. Regime temporal (the Kaggle split alternates two train weeks and one test week, a claim to check, SPLIT-5).
- Siblings and duplicates: `kelmarsh_wind_farm_data` (TBD -> Yes, `Needs extensive data wrangling`; curator: "Unclear if the task is reasonable", "much newer data on Zenodo"); `penmanshiel_wind_farm_scada` (a candidate of this run: the same publisher's 14-turbine farm in the same format). A newer release of the same source (PROV-6): the curator decides which one enters, not both. External collections: none found.
- Better data: found as better data for `kelmarsh_wind_farm_data`; a newer release of the same source (PROV-6).
- Papers and pages: Zenodo 16807551 and 5841834; a 2026 provenance audit (Park et al., Zenodo 23171808 with reconstructed files and a flag table, 23196733 with the code): "In the v4 release, the twelve 2023 and 2024 Turbine_Data files store each year as 81 cumulative blocks that restart at 1 January. Only the first occurrence of each timestamp holds measured values".
- Metric: Mean Absolute Error on the Kaggle competition the parent names (competition API `evaluationMetric`), a community competition by its uploader (MET-4): `mae`, if that framing is kept.
- Risks for /add-dataset: the 2023 and 2024 duplicate blocks (keep the first occurrence of each timestamp or use the audit's reconstruction; PROV-13); the inputs are the neighbours' signals at the same timestamp, so whether this is a time-series task (`Time-series (Regression)`, SEL-10, SEL-11) or gap filling is the open question carried from the parent; hundreds of signals per turbine, sentinel values and signals that start late (the audit's onset manifest).
- Priority: gap 0, use case 0 (the Kaggle task names no actor), source + (operator release with signal mapping), shape + (six turbines, nine years of 10-minute rows), risk - (export defect and the unsettled task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `kelmarsh_wind_farm_data`.
- as published: 6 Senvion MM92 turbines, 10-minute SCADA and events data grouped by year, 2016 to end of 2024 (v0.0.3: 2016 to mid-2021), plus static data, PMU and grid-meter data; per turbine-year about 52,560 ...; target: as in the record: the 10-minute wind speed (or power) at one turbine from the signals of the other turbines; access: open.
- Why: The same source and task the record names; the curator's own note says 'much newer data on Zenodo'. A newer release of the same source: a version (PROV-6), the curator decides which enters.
- Adds: 3.5 more years (mid-2021 to end of 2024), so a longer temporal split. Risk found: a 2026 provenance audit (Zenodo 23171808, 23196733) reports that the v4 2023 and 2024 turbine files store each year as 81 cumulative blocks restarting at 1 January; only the first occurrence of each timestamp holds measured values, so ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
