---
unique_name: ctu_sme_11
name: 'CTU-SME-11: a labeled dataset with real benign and malicious network traffic mimicking a small medium-size enterprise environment'
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Needs extensive data wrangling
original_source: Other
year: '2023'
domain: technology & internet
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://doi.org/10.5281/zenodo.7958259
- https://dspace.cvut.cz/handle/10467/109254
- https://www.stratosphereips.org/datasets-overview
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: real captured traffic of 11 devices over 7 days with expert flow labels, from the CTU-13 lab, but 97.8% of the flows come from one VM (mostly one day of attack traffic) and the labels come from a rule file.
- Source: Bendl, Valeros & Garcia, "CTU-SME-11: a labeled dataset with real benign and malicious network traffic mimicking a small medium-size enterprise environment", Stratosphere Laboratory, CTU Prague, Zenodo 10.5281/zenodo.7958259 (2023-05-25, v1.0.0, CC BY 4.0), "created in 2023 by Štěpán Bendl, as part of his master thesis" (README; thesis at dspace.cvut.cz/handle/10467/109254, page did not load). As published: per device and day, the pcap, Zeek logs with `conn.log.labeled`, and `artifacts/labels.config`, a "netflow labeler rule configuration file" (README); 14 tar.bz2 archives, 96.6 GB listed; a label of "benign, malicious or background" plus a descriptive label, both assigned by experts (Zenodo page). The summary table: 99,993,509 flows, of which 97,830,092 on `Experiment-VM-Linux-Ubuntu2204-1` (95.8M on day 4, almost all malicious); the other 10 devices hold 2,163,417 flows (1,571,169 benign, 527,595 malicious, 64,653 unknown).
- Use case: a network operator flags malicious flows or infected hosts from flow records as they close, the detection task of `ctu_13` (the pages read name no actor); fit approximate. Regime grouped by device (11, an unseen host) or temporal by day (7): one to pick (SPLIT-3).
- Siblings and duplicates: `ctu_13` (`TBD -> Yes`, priority 4; same lab, 2011 botnet captures as Argus flows): another capture, no duplicate (PROV-4). Other network records: `unsw_nb15`, `cic_ids2017` (`No`, generated traffic), `kyoto_2006_plus`, `litnet_2020_network_intrusion`. External collections: none found (Stratosphere's datasets overview lists it).
- Better data: found as better data for `ctu_13`; no further search this round.
- Papers and pages: the Zenodo record, its README and summary table; Bendl's master thesis (CTU 2023, not read).
- Metric: none found (Zenodo page, README; the thesis page did not load); fallback `roc_auc` on benign against malicious (MET-1, MET-8); inputs none.
- Risks for /add-dataset: labels set by rules in `labels.config` likely key on IPs, ports and time ranges, so those columns may encode the label (SEL-5, LEAK): read the config before choosing features; the Ubuntu VM's day-4 burst dominates any pooled sample (subsample per device or drop, CLEAN); background means unknown and goes (USE-7); honeypots (Raspberry Pi, Chromecast, Echo) see mostly attacks, so the device carries the class mix (LEAK-13 to check); 96.6 GB of archives to unpack and concatenate (`Needs extensive data wrangling`).
- Priority: gap 0 (technology & internet, binary, grouped or temporal not thin), use case 0 (no actor named by the source), source + (lab release with README and a thesis), shape + (2.2M flows besides the burst, mixed Zeek fields, devices and days), risk - (rule-based labels, one VM dominates): 2.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ctu_13`.
- as published: 99 million expert-labelled Zeek network flows from 11 devices (IoT, desktop, mobile; bare metal and VMs), captured 7 days, 2023-02-20 to 2023-02-26, Prague; 14 tar.bz2 files, 80 GB compressed / 170 ...; target: flow label: benign / malicious / background (plus a descriptive behaviour label); access: open.
- Why: same lab, same task and label scheme as ctu_13 (real captured traffic, malware run on real hosts, Benign/Malicious/Background), features of the same kind (flow records known when the flow closes); labels put by experts per flow, not by infected-host IP alone
- Adds: 12 years newer (2023 malware and devices vs 2011), 99M labelled flows, Zeek conn logs instead of 2011 Argus NetFlows, a descriptive label per flow, devices as natural groups (11) and 7 days for a temporal split; CC-BY-4.0. Same caveats as ctu_13: Background means unknown, few groups, very large files

CC (2026-11-04, Lennart): `No`, `AHDS (Artifical/Handmade/Deterministic/Simulated)` (SEL-16), with ctu_13: "This should also affect ctu_sme_11 in that case" (PR #33 review).

**Assessment (AI, 2026-11-04):** the same lab's 7-day experiment that "mimics" a small enterprise (https://zenodo.org/records/7958259): experiment VMs infected with malware and then factory reset, participants "forbidden to use personal accounts", and labels from a NetflowLabeler rule file on IPs, ports, protocol, date and duration (`labels.config`, not read). One Ubuntu VM holds 97.8M of the 99.9M flows. The three honeypots receive real Internet attacks, but there the device carries the class (LEAK-13).
