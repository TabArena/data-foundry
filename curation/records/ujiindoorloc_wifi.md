---
unique_name: ujiindoorloc_wifi
name: 'UJIIndoorLoc: a multi-building and multi-floor database for WLAN fingerprint-based indoor localization'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: UCI
year: '2014'
domain: technology & internet
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5MS59
- https://archive.ics.uci.edu/dataset/310/ujiindoorloc
- https://doi.org/10.1109/IPIN.2014.7275492
- https://zenodo.org/records/14780428
- https://zenodo.org/records/5174851 (Tampere TIE1/SAH1 2017, X,Y,Z + floor, 10,633 and 9,291 reference fingerprints, CC BY 4.0)
- https://zenodo.org/records/6928554 (Silva et al. 2022 long-term Wi-Fi fingerprinting, 11,140 site-survey samples)
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the reference WiFi fingerprinting database (UCI 310, IPIN 2014): 21,048 fingerprints in three buildings, collected by more than 20 users with 25 phones, with a validation set taken 4 months later; documented and widely used, with a position in several parts as target.
- Source: Torres-Sospedra, Montoliu, Martínez-Usó, Avariento, Arnau, Benedito-Bordonau and Huerta (Universitat Jaume I), "UJIIndoorLoc: A new multi-building and multi-floor database for WLAN fingerprint-based indoor localization problems", IPIN 2014 (doi 10.1109/IPIN.2014.7275492; preprint on Zenodo 14780428); UCI 310 (doi 10.24432/C5MS59, donated 2014-09-17, CC BY 4.0). As published: `trainingData.csv` (19,937 rows) and `validationData.csv` (1,111), 529 columns: WAP001 to WAP520 RSSI ("The positive value 100 is used to denote when a WAP was not detected"), longitude, latitude, floor, building, space, relative position, user, phone, timestamp. Preprint (Sec. I): "The number of different places (reference points) appearing in the database is 933"; "Dataset independence has been assured by taking Validation (or testing) samples 4 months after Training ones"; the validation records were taken "at arbitrary points", without space, relative position and user (user 0).
- Use case: an indoor navigation service places a phone at a building, floor and coordinates from the access points it hears; the source names localization research and applications, no actor; fit approximate; regime temporal: the source's validation set is later and comes from other users and points.
- Siblings and duplicates: `uji_long_term_wifi_fingerprinting` (screened in the same batch: the same lab's library campaigns of 2016-2018, other data, the same task); `3d_estimation_using_rssi_of_wlan_dataset_complete_1_target` (`No`, Missing source information: an untraced OpenML 3D RSSI table); `ble_rssi_dataset_for_indoor_localization` (`TBD -> Yes`, priority 1); `ujiindoorloc_mag` (`No`, Lennart: the magnetic-field database of the same lab, a time series). No duplicate. External collections: OpenML copies and the IPIN 2015 competition's use (both not checked).
- Better data: found as better data for `3d_estimation_using_rssi_of_wlan_dataset_complete_1_target` (the run's Assessment); no further search this round.
- Papers and pages: the IPIN 2014 paper (577 citations per Semantic Scholar; read in its Zenodo preprint); its 1-NN baseline (Table XI): "Success rate 89.92%" (building and floor right) and "Error in positioning 7.9m" (mean error of the fingerprints placed in the right building and floor).
- Metric: the paper reports the building-and-floor success rate and the mean positioning error side by side (Table XI) and names no single criterion, so the fallback for the target chosen (MET-5).
- Risks for /add-dataset: four targets (building, floor, longitude, latitude): pick or build one, such as a building-floor class (13) or one coordinate (CLEAN-18, Multi-target); about 20 samples per reference point in the training file (near copies: a random split leaks the point); `SPACEID` and `RELATIVEPOSITION` are parts of the location label and `USERID`, `PHONEID` collection metadata (LEAK; absent from the validation file); the source's validation set is small (1,111), so a split taken from it gives one small test fold; the 100 placeholder (CLEAN); data of 2013 (`Outdated` to weigh).
- Not checked: the OpenML copies and the IPIN 2015 competition data and metric (the web search budget ran out).
- Priority: gap 0 (technology & internet has 4 accepted, temporal not thin), use case 0 (no actor named), source + (paper, UCI page), shape + (21,048 rows, 520 RSSI columns, 25 devices, a later validation set), risk - (no single target, near-copy samples).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `3d_estimation_using_rssi_of_wlan_dataset_complete_1_target`.
- as published: 21,048 WLAN fingerprints (19,937 training and 1,111 validation, taken later), 529 columns: 520 WAP RSSI values plus building, floor, longitude, latitude, space, relative position, user, phone, ...; target: the position of the phone: longitude and latitude (regression) with floor and building (the vertical, 3D part); access: open.
- Why: Same task as the ITU 2023 challenge (estimate a receiver's 3D position from WLAN RSSI), but published by its creators with a paper and documented collection, where the OpenML upload has no traceable source.
- Adds: A traceable, documented source with 21k fingerprints against 14.4k untraced rows, real devices and users, and a validation set collected separately, which suits a non-IID split. The Tampere 2017 set (other_links) gives X,Y,Z directly if the 3D target matters more. Caveat: older (2013) than the ITU data.
