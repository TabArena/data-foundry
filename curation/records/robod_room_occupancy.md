---
unique_name: robod_room_occupancy
name: ROBOD, Room-level Occupancy and Building Operation Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2022'
source_links:
- https://doi.org/10.1007/s12273-022-0925-9
- https://doi.org/10.6084/m9.figshare.19234530
- https://figshare.com/articles/dataset/ROBOD_Room-level_Occupancy_and_Building_Operation_Dataset/19234530
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: five rooms of a university building in Singapore (two lecture rooms, two offices, a library), 181 room-days at 5-minute resolution with indoor environment, Wi-Fi device counts, end-use energy, HVAC operation, weather and the ground-truth presence and occupant count; a documented, wider version of `occupancy_detection_2`'s task, with the same near-proxy and time-series questions.
- Source: Tekler, Ono, Peng, Zhan, Lasternas, Chong, "ROBOD, room-level occupancy and building operation dataset", Building Simulation 15:2127-2137 (2022, doi 10.1007/s12273-022-0925-9); data on figshare (doi 10.6084/m9.figshare.19234530, version 7, published 2022-07-11, CC BY 4.0), one `SupplementaryData.zip` (4.5 MB). As published (README and a header read by range request): `combined_Room1.csv` to `combined_Room5.csv` (lecture rooms 29 days each, office space 29 and 47 days, library 47 days), 2021-09-07 to 2021-12-23, School of Design and Environment 4 building, National University of Singapore; 27 columns in Room 1's header (the other rooms not read): timestamp, VOC, sound pressure level, indoor relative humidity, air temperature, illuminance, PM2.5, indoor CO2, wifi_connected_devices, ceiling fan, lighting, plug-load, chilled-water and FCU-fan energy, temperature setpoint, FCU fan speed, supply air pressure and temperature, barometric pressure, outdoor dry-bulb temperature, solar radiation, wind direction and speed, outdoor CO2 and humidity, occupant_presence (0/1), occupant_count. About 52,000 rows in total (181 days x 288), not counted.
- Use case: a building management system switches ventilation, cooling and lighting by room from detected presence (demand-controlled operation); the figshare text names the field ("occupancy prediction and occupant behaviour modelling, building simulation and control, energy forecasting") but not the actor's decision, so fit approximate. Regime: temporal within each room (a 5-minute stream, the label constant for long stretches) or grouped by room to generalise to a new room; five rooms are few groups.
- Siblings and duplicates: `occupancy_detection_2` (`TBD -> Yes`, with `Time-series (Classification)` and `Trivial`: one office room, per minute, 2015) and its copy `occupancy_detection` (`No`); `hpdmobile_home_occupancy` (`TBD -> Yes`, six homes, another source). Not a duplicate of any (PROV-4). External collections: none found.
- Better data: found as better data for `occupancy_detection_2`; no further search this round.
- Papers and pages: the Building Simulation paper (not read: the publisher's page needs a login, and Crossref has no abstract), so how the ground truth was collected (cameras, counting or schedules) is open; the figshare record.
- Metric: none found (figshare text and README; the paper not read), so the fallback `roc_auc` for presence or `rmse` for the count (MET-1, MET-8); inputs none.
- Risks for /add-dataset: Wi-Fi device counts, lighting, plug-load and fan energy and the FCU fan speed respond to the occupants themselves, so presence may be read off one column (`Trivial` to measure, TP-4; legitimate inputs for detection at the same instant, LEAK-37); rows 5 minutes apart are near copies, so the split must keep whole days or rooms apart (SPLIT); the `Time-series (Classification)` question of `occupancy_detection_2` applies; presence or count as the target (problem type open); the ground-truth method is to be read from the paper (USE-5).
- Priority: gap 0 (binary and temporal are not thin), use case 0 (the field is named, not the decision), source + (a journal data paper with a public deposit), shape + (about 52,000 readings, 24 inputs, room and time structure), risk - (near-proxy columns and a stream label that changes rarely).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `occupancy_detection_2`.
- as published: 5 rooms in a Singapore university building (2 lecture rooms, an administrative office, a researchers' office, a library), 181 days of data in total at 5-minute resolution; indoor environment, Wi-Fi ...; target: room occupied (presence) or number of occupants; access: open (CC BY 4.0, figshare).
- Why: Same task as occupancy_detection_2 (occupancy of an office room from environmental sensing), with office rooms as in the 2016 data
- Adds: Five rooms of three kinds and 181 days against one room over about two weeks; occupant count as a second target; CC BY 4.0. Caveat: Wi-Fi device counts, plug-load and lighting energy are near-proxies of presence; decide which are known at the prediction point
