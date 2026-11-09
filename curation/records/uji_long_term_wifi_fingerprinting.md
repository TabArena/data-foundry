---
unique_name: uji_long_term_wifi_fingerprinting
name: Long-Term Wi-Fi fingerprinting dataset and supporting material (UJI library)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the task's table is 104,160 fingerprints (counted in v2.2; the Zenodo page states 103,584) x 620 access-point RSSI columns. Every AP is heard at least once, but only 110 in more than 1% of the fingerprints, so the real width is closer to 100. The call stands at priority 2. `ujiindoorloc_wifi` is a sibling with the same task on other data, not a version.
- As published: Zenodo concept 10.5281/zenodo.1066040 with four versions: V1 (2017-11-24, `UJI_LIB_DB.zip` 3,294,914 bytes, 15 months, 63,504 fingerprints), 2.0 (2018-08-17), 2.1 (2018-11-06) and 2.2 (2020-04-11, `UJI_LIB_DB_v2.2.zip` 6,466,389 bytes, 264 MB unpacked). The zip's changelog: 2.0 added "10 months of additional measurements (September 2017 - June 2018)" with the Samsung Galaxy S3 and "1 month of additional measurements (June 2018)" with a Samsung Galaxy A5 (2017), and filled the new APs' columns of the old months with +100; 2.1 identified 16 APs of the 4 nearest wireless devices (`nearAPs.csv`); 2.2 changed the ids to 10 digits. `db/01` to `db/25` hold four headerless CSVs per set: `rss` (620 columns, 100 = not detected), `crd` (x, y, floor), `tms` (time to the millisecond) and `ids`. Counted: month 1 has 15 training and 5 test sets (11,760 rows), months 2 to 24 one training and 5 test sets each (3,696 rows), month 25 two training and 10 test sets (7,392 rows, the S3 and the A5); 104,160 rows in all, 23,040 training and 81,120 test, from 2016-06-02 to 2018-07-13; floors 3 and 5 with 52,080 rows each. V1's 63,504 equals months 1-15 exactly; v2.2's stated 103,584 is one set (576 rows) short of the count, and no two files are identical.
- The task's table: all sets stacked with a month column, 104,160 rows x 620 RSSI inputs (counted). A training set has 576 fingerprints at 48 positions, 12 per position. Test sets 1 and 5 repeat the 48 training positions; test sets 2 and 3 take 48 other positions each and test set 4 68 others, 212 positions in all. All 620 APs are heard at least once; 245 in more than 0.1% of the fingerprints, 110 in more than 1%, 83 in more than 5%. A fingerprint hears 19 APs at the median (max 54), so 3.2% of the cells are readings. 401 APs are heard in some training set, 448 in months 1-15 and 422 in months 16-25. 101 RSS vectors repeat exactly. The target is x or y (metres, local coordinates) or the floor (two balanced classes); the phone varies only in month 25.
- Access: open, no login, a 6.5 MB zip. Licence: the Zenodo page says MIT; the zip's Readme says "The data is licensed under CC Attribution 4.0 International (CC BY 4.0). The script files are provided under MIT license".
- Changes the call: none that moves the priority (2: gap 0, use case 0, source +, shape +, risk -). On width: about 110 of the 620 columns carry a reading in more than 1% of the rows. Under a temporal split, the APs installed later are blank in the training months (the 100 placeholder becomes missing, CLEAN). Siblings (PROV-4, PROV-6, PROV-7): `ujiindoorloc_wifi` is another collection by the same lab (three buildings with 4 or more floors, 2013, 18 users and 16 phones in its training file, 520 APs), so the two share no rows and neither is a version or a cut of the other; both carry the same task. If the curator takes one, the trade is this set's 5x rows and 25-month time axis, from one collector with two phones on two floors at 212 positions, against UJIIndoorLoc's many users and phones, 13 building-floor classes and a competition metric.
- Not checked: the data paper's text and its evaluation (MDPI answered 403 again); why the stated count is 576 lower than the files; which month-25 sets come from the A5.

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).
