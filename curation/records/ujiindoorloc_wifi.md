---
unique_name: ujiindoorloc_wifi
name: 'UJIIndoorLoc: a multi-building and multi-floor database for WLAN fingerprint-based indoor localization'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the task's table is 21,048 fingerprints (19,937 training, 1,111 validation taken three months later) x 520 WAP RSSI columns, of which 273 are heard in more than 1% of the fingerprints and 113 in more than 5%. The call stands at priority 2. A competition metric exists for the joint position (EvAAL-ETRI 2015, off-site track), and it needs four predicted outputs.
- As published: UCI 310 (https://archive.ics.uci.edu/dataset/310/ujiindoorloc), `ujiindoorloc.zip` 1,463,759 bytes with `UJIndoorLoc/trainingData.csv` (42,725,381 bytes, 19,937 rows) and `validationData.csv` (2,381,949 bytes, 1,111 rows), 529 columns each: WAP001 to WAP520 ("Positive value 100 used if WAP001 was not detected"), LONGITUDE, LATITUDE, FLOOR, BUILDINGID, SPACEID, RELATIVEPOSITION, USERID, PHONEID and TIMESTAMP (UCI variable information). Counted: training from 2013-05-30 to 2013-06-20, validation from 2013-09-19 to 2013-10-08 (the paper says 4 months later); 13 building-floor classes of 995 to 2,749 rows, all 13 in the validation file (24 rows or more each); 933 distinct coordinates in training, the paper's 933 reference points. The training file has 18 users and 16 phones; the validation file has user 0 and 11 phones, 2 of which appear in training (397 of the 1,111 rows), and SPACEID and RELATIVEPOSITION are 0 there.
- The task's table: both files stacked, 21,048 rows x 520 RSSI inputs (counted), TIMESTAMP as the split key. Every WAP is heard somewhere; 55 never in the training file and 153 never in the validation file; 381 in more than 0.1% of the fingerprints, 273 in more than 1%, 113 in more than 5%. A fingerprint hears 17 WAPs at the median, and 76 hear none. 637 training rows copy another row in every column. SPACEID, RELATIVEPOSITION and USERID leave (parts of the label and collection metadata, empty in the validation file); PHONEID is known at prediction time, but 9 of the 11 validation phones are unseen in training.
- Access: open, no login, a 1.5 MB zip. UCI's API returned no licence field on 2026-11-08; the screening read CC BY 4.0 on the page.
- Changes the call: the metric. The IPIN 2015 EvAAL-ETRI off-site competition on this database scored "Method accuracy = average (SampleError(Ri, Ei))" with "SampleError(Ri, Ei) = Distance(Ri, Ei) + (penalty1 * buildingfail) + (penalty2 * floorfail)", "penalty1 is set to 50" and "penalty2 is set to 4" ("floorfail is the absolute difference between actual floor and the predicted one"; the distance is Euclidean on the projected longitude and latitude, in metres), on a "large private final test set that has not been published" (https://evaal.isti.cnr.it/2015/competitors/technical-annex-off-site). It is a competition's metric (MET-4) for the joint position, so it needs longitude, latitude, floor and building predicted together. A single-target task (a building-floor class, or one coordinate) cannot use it, so the fallback for the chosen target stays (MET-5), and the joint form is a question for /add-dataset. The priority stays 2 (gap 0, use case 0, source +, shape +, risk -). The validation file is the only later data, so a temporal split has one test fold of 1,111 rows from other users, other points and mostly other phones. Sibling: `uji_long_term_wifi_fingerprinting` (see its assessment): the same lab and task on other data, not a version (PROV-6 does not apply); the curator may take one of the two.
- Not checked: the IPIN 2014 paper's own counts of WAPs heard; the OpenML copies; the journal paper on the 2015 competition (Torres-Sospedra et al., JAISE 9:263, 2017; the open copies answered 403).
