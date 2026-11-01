---
unique_name: uji_long_term_wifi_fingerprinting
name: Long-Term Wi-Fi fingerprinting dataset and supporting material (UJI library)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2017'
domain: technology & internet
required_split:
- Temporal (NON-IID)
source_links:
- https://doi.org/10.5281/zenodo.1066041
- https://doi.org/10.5281/zenodo.3748719 (v2.2, 2020, 25 months)
- https://doi.org/10.3390/data3010003 (Mendoza-Silva et al., Data 2018, 3(1):3)
- 'https://doi.org/10.24432/C5MS59 (UJIIndoorLoc, UCI 310: ~21k WiFi fingerprints, 3 buildings, 2013; no record either, not checked here)'
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 103,584 WiFi fingerprints from 25 monthly campaigns on two floors of one library, at fixed reference points with separate test sets each month; a documented study of positioning under signal drift, narrow in its collection (one person, mostly one phone) and with a position as target.
- Source: Universitat Jaume I with Tampere University of Technology: Mendoza-Silva, Richter, Torres-Sospedra, Lohan and Huerta, "Long-Term WiFi Fingerprinting Dataset for Research on Robust Indoor Positioning", Data 3(1):3, 2018 (doi 10.3390/data3010003); Zenodo v1 (doi 10.5281/zenodo.1066041, 2017-11-24: "collected by one person using one Android smartphone during 15 months at two floor of the library building", 63,504 fingerprints) and v2.2 (doi 10.5281/zenodo.3748719, 2020-04-11: 25 months, 103,584 fingerprints, a Samsung Galaxy A5 used only in the last campaign; MIT on the Zenodo page, while the zip's Readme says "The data is licensed under CC Attribution 4.0"). As published (file listing and a preview of the v2.2 zip): `db/<month>/` with four files per campaign, `trnNNrss.csv` (620 access-point columns, 100 = not detected), `trnNNcrd.csv` (x, y, floor), `trnNNtms.csv` (time), `trnNNids.csv`; one training set and five test sets per month (15 training sets in month 1, 2 training and 10 test sets in month 25); a training set holds 576 fingerprints at about 48 positions, 12 per position; floors 3 and 5.
- Use case: an indoor positioning service places a phone from the access points it hears and must keep working as the radio map ages; the source states research on robust positioning and names no actor; fit approximate (one collector, fixed points, one building); regime temporal: train on early months and test on later ones, the source's long-term design.
- Siblings and duplicates: `ujiindoorloc_wifi` (screened in the same batch: the same lab's 2013 multi-building database, other data, the same task); `ble_rssi_dataset_for_indoor_localization` (`TBD -> Yes`, priority 1: BLE beacons, 1,420 rows); `3d_estimation_using_rssi_of_wlan_dataset_complete_1_target` (`No`, Missing source information); `ujiindoorloc_mag` (`No`, Lennart: magnetic-field series). No duplicate (PROV-4); the curator may want only one WiFi fingerprinting task of the two UJI sets. External collections: none found.
- Better data: found as better data for `ble_rssi_dataset_for_indoor_localization` (the run's Assessment); no further search this round.
- Papers and pages: the data paper (148 citations; not read: MDPI answered 403; abstract via Semantic Scholar: one training and five test dataset types per month, at the same positions and directions each time); the Zenodo pages and the zip's Readme.
- Metric: none found as one deliberate choice (the Zenodo pages and the Readme name none; the paper's evaluation not read; the field reports the mean positioning error and the floor hit rate side by side), so the fallback for the target chosen (MET-1, MET-5).
- Risks for /add-dataset: the target is a position (x, y, floor), so a single-target task needs a choice: the floor (two classes, likely easy), one coordinate, or the reference point on the training routes (CLEAN-18, USE-5); 12 repeats per point are near copies, so a random split is wrong (SPLIT); 620 sparse RSSI columns, mostly the placeholder 100 (CLEAN: encode as missing); one collector and mostly one phone; the campaign files must be stacked with a month column.
- Not checked: the data paper's text and its evaluation; the total row count against 103,584.
- Priority: gap 0 (technology & internet has 4 accepted, temporal not thin), use case 0 (a research dataset, no actor), source + (data paper, Zenodo, Readme), shape + (103,584 rows, 620 features, 25 dated campaigns), risk - (no single target, near-copy repeats).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ble_rssi_dataset_for_indoor_localization`.
- as published: 103,584 WiFi fingerprints (v2.2), 25 months of collection campaigns on two floors of the university library, one person, mainly one Android phone, at fixed reference points; RSSI per access point; ...; target: location of the fingerprint (reference point coordinates and floor); access: open.
- Why: Same task as ble_rssi (fingerprint localisation from the RSSI of fixed transmitters), WiFi access points instead of BLE beacons
- Adds: 73x the labelled rows (103,584 against 1,420), repeated campaigns over 25 months, so the temporal split the curators chose is built in and measures signal drift; fewer locations per row is not a problem (Too Small risk of the record gone)
