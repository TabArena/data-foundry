---
unique_name: norway_residential_ev_charging_sessions
name: Electric vehicle charging dataset with 35,000 charging sessions from 12 residential locations in Norway
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
year: '2024'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1016/j.dib.2024.110883
- https://doi.org/10.5281/zenodo.13896176
- https://doi.org/10.1016/j.segan.2023.101195
- https://doi.org/10.1016/j.dib.2021.107105
- https://doi.org/10.5281/zenodo.12730566
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 35,377 measured residential charging sessions of 267 users at 12 Norwegian apartment sites (2018-2021), from a SINTEF/NTNU data article; real data where the EV records it was found for are generated, but the measured file has only the site, the user and the plug-in time as inputs.
- Source: Sørensen, Sartori, Lindberg and Andresen, "Electric vehicle charging dataset with 35,000 charging sessions from 12 residential locations in Norway", Data in Brief 57 (2024) 110883 (read from the PDF on Zenodo); data on Zenodo under CC BY 4.0 (doi 10.5281/zenodo.13896176, the latest version; the article cites 10.5281/zenodo.12730566); the related research article in Sustainable Energy, Grids and Networks 36 (2023) 101195. "Residential charging reports were collected from charge point operators and companies in Norway" (Current Eco, Zaptec, Kople, Mer, NTE), "available for monitoring and billing purposes". Dataset 1 (measured): location, session_id, user_id, plugin_time, plugout_time, connection_time (h), energy_session (kWh); 35,377 sessions from February 2018 to August 2021, 127 to 9,757 per site. Datasets 2-4 hold the authors' modelled battery capacity, charging power, plug-in state of charge and hourly profiles ("realistic predictions have been integrated").
- Use case: the housing cooperative's charging operator, at plug-in, estimates the energy a car will draw and when it will leave, to schedule smart charging under the building's grid limit; the article names "load forecasting, energy flexibility" and smart charging "in buildings and locations with limited grid capacity" (Value of the Data, Background), without an actor's decision; fit approximate; regime temporal by plug-in time, with users known from their history, as `acn_data_ev_charging_sessions`.
- Siblings and duplicates: `acn_data_ev_charging_sessions` (`TBD -> Yes`, 3: workplace and campus sessions with the driver's own energy and departure requests, richer inputs); `ev_charging_grid_optimization_dataset`, `ev_charging_station_data_california_region` and `microgrid_pv_ev_charging_dataset` (all `No`, AHDS). The 2021 Trondheim release (Data in Brief 36, doi 10.1016/j.dib.2021.107105) is site TRO_R here (6,706 sessions; the article cites it for that site), an earlier part of the same data (PROV-6), not a dataset of its own. External collections: none known (not searched: the run's web search budget was used up).
- Better data: found as better data for `ev_charging_grid_optimization_dataset`, `ev_charging_station_data_california_region` and `microgrid_pv_ev_charging_dataset`; no further search this round.
- Papers and pages: the Data in Brief article; the 2023 method paper (not opened).
- Metric: none found (the data article defines no prediction task), so the fallback `rmse` (MET-8) on energy per session in kWh, or on the connection time; inputs none.
- Risks for /add-dataset: three raw inputs, so the task is mostly each user's own profile: run the naive-profile check (TP-10, SEL-11); Datasets 2-4 are model outputs, and plug-out time and connection time are known only at departure (LEAK-10); the target to choose (energy or duration; USE-5); the sites cover different periods, so a late test window holds only a few of them (BAR_2, KRO and OSL_T run past February 2020).
- Priority: gap 0, use case 0 (uses named, no actor's decision), source + (a data article from SINTEF and NTNU), shape 0 (35,377 sessions but three raw inputs), risk - (a profile task that may fail TP-10).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ev_charging_grid_optimization_dataset`, `ev_charging_station_data_california_region`, `microgrid_pv_ev_charging_dataset`.
- as published: over 35,000 residential charging sessions, 267 user IDs, 12 apartment-building locations in Norway (Zenodo description); Dataset1_charging_reports.csv holds the measured plug-in time, plug-out time ...; target: energy charged per session (kWh), or the plug-in duration; access: open.
- Why: the same EV charging session task as above on measured sessions with a data article; only Dataset1 is measured, the other files hold the authors' predictions and must stay out | same demand-side EV charging task as the fake microgrid record, from a published data article with real charge-point reports
- Adds: 35,000 measured sessions, open CC-BY, two papers describing the data; complements ACN-Data with residential charging (ACN is workplace and campus). The 2021 Trondheim set by the same group (Data in Brief 36, 6,878 sessions) is an earlier, smaller release; check how far the two overlap | real sessions, open CC-BY-4.0, ...
