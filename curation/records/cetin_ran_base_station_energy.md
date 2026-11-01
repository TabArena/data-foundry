---
unique_name: cetin_ran_base_station_energy
name: Performance Management Counters from Live 5G, 4G and 2G Radio Access Network
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2026'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5281/zenodo.17815388
- https://doi.org/10.1038/s41597-026-07723-0
- https://europepmc.org/article/PMC/PMC13696700
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: measured energy use of 352 live base stations of a Slovak operator next to their load counters at 15 minutes, the task of the accepted `5g_energy_consumption` on a documented, peer-reviewed source; energy is reported per radio unit and sector, so cell rows must be aggregated.
- Source: Lehoczký, Turcsány, Krajčovičová, Zatroch, Kajan, Galinski (Slovak University of Technology; Ericsson Slovakia), "Performance Management Counters from Live 5G, 4G and 2G Radio Access Network", Scientific Data 13:1480 (online 2026-07-03, doi 10.1038/s41597-026-07723-0, PMC13696700); data on Zenodo (doi 10.5281/zenodo.17815388, 2026-05-06, CC BY 4.0); "The raw input data were provided by CETIN Networks". As published (descriptor Table 2): Dataset_01, LTE 2100 and NR 1800, 35 days, 25 base stations, 302,052 records; Dataset_02, LTE 1800 and NR 2100, 64 days, 63 stations, 3,601,840 records; Dataset_03, GSM 900, LTE 700/800/1800 and NR 2100/3500, 84 days, 264 stations, 30,213,561 records. One CSV per technology and band per baseband: base station and sector pseudonyms, timestamp, PM counters (RB utilisation, CQI, RRC-connected and active users, UL and DL volume, MIMO rank), and energy "as the total electrical energy consumed during each 15-minute interval, measured in watt-hours (Wh)".
- Use case: an operator estimates a site's energy use from its traffic load and radio configuration, to plan energy saving and compare sites; the descriptor: "network operators face the challenge of maintaining throughput efficiency while minimising energy consumption. This dataset offers a rare and unique opportunity to investigate these relationships on commercial infrastructure and to build predictive models grounded in live network behaviour". Fit approximate: "Energy consumption data is generated at node level ... Therefore, power consumption per cell is not directly observable". Regime grouped by base station (a new site), as for `5g_energy_consumption`; the rows form a series, so the task stays a nowcast from the same interval's counters (SEL-10, SEL-11).
- Siblings and duplicates: `5g_energy_consumption` (`Yes`, the ITU/Zindi 2023 challenge, grouped, `mape` standing in for WMAPE) is the record it was found for, another operator and source (PROV-4). No earlier record of this descriptor. External collections: none known.
- Better data: found as better data for `5g_energy_consumption`; no further search this round.
- Papers and pages: the Scientific Data descriptor (Methods, Technical Validation, Usage Notes) and the Zenodo README.
- Metric: none found (the descriptor and the README define no task). The fallback `rmse`; the same task on `5g_energy_consumption` keeps the challenge's MAPE, a weighing call for the curator (MET-10); inputs none.
- Risks for /add-dataset: cells must be summed to the node the energy belongs to without counting one measurement twice ("careful attention must be paid to avoid duplicating energy consumption values", descriptor); about 17% of records miss at least one KPI; one CSV per band per baseband to join; calendar dates of the periods not checked; 34 million records, so a cut by subset or station.
- Priority: gap 0 (regression, grouped and technology are not thin), use case + (the descriptor names the operator's energy decision), source + (peer-reviewed descriptor), shape + (352 stations, grouped), risk - (aggregation to the energy's level, joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `5g_energy_consumption`.
- as published: Sector x 15-minute interval records from live base stations of a commercial operator in Slovakia, three subsets (descriptor Table 2): Dataset_01 LTE 2100/NR 1800, 35 days, 25 base stations, 302,052 ...; target: Energy consumption per interval, reported at radio-unit and baseband level (README: 'not as direct per-cell energy consumption'); access: open.
- Why: Same task as 5g_energy_consumption: base-station energy from concurrent load and configuration counters, measured on a live network, with stations as the group for a grouped split.
- Adds: A named network provider and a peer-reviewed data descriptor (the ITU/Zindi set has neither in the record), about 350 base stations over 35-84 days instead of a few days, 2G/4G/5G and several bands, CC BY 4.0. Caveats: energy is per radio unit / baseband, so rows need aggregating to that level; the energy-saving mode ...
