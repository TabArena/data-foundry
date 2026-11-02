---
unique_name: tls_os_fingerprinting_masaryk
name: Dataset Using TLS Fingerprints for OS Identification in Encrypted Traffic
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2019'
domain: technology & internet
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.3461771
- '# the NOMS 2020 paper (its PDF also on Zenodo, 10.5281/zenodo.3989382)'
- https://doi.org/10.1109/NOMS47738.2020.9110319
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Masaryk University's five days of real Eduroam flow records (18.7M flows, 45,602 Wi-Fi sessions, July 2019) with TCP/IP and TLS handshake fields and the device's OS from DHCP logs, for passive OS identification; real users' traffic instead of the lab-scripted sessions of the Zindi record.
- Source: Laštovička, Špaček, Velan and Čeleda (Masaryk University), "Using TLS Fingerprints for OS Identification in Encrypted Traffic", NOMS 2020 (10.1109/NOMS47738.2020.9110319); data on Zenodo 10.5281/zenodo.3461771 (2019-09-26, CC BY 4.0, one zip of 700 MB). As published: one CSV of flows from the university's wireless devices, 2019-07-12 to 2019-07-16, "anonymized with cryptographic means using Crypto-PAn"; fields: flow start and end, source and destination IP and port, SYN size, TCP window, SYN TTL, HTTP host and four User-Agent OS fields, TLS SNI and its length, client version, cipher suites, extension types and lengths, elliptic curves, EC point formats, session ID, ground-truth OS. Paper Sect. IV: 18,708,983 flows, 10,734 users, 45,602 sessions, 11,962 MAC addresses; Sect. VI.C: Android 39.93%, Apple iOS and macOS 30.03%, Windows 28.49%, others 1.55%.
- Use case: a network operator identifies the OS of the devices on its network from passively observed traffic for its asset inventory (abstract: "Asset identification plays a vital role in situational awareness building"); fit direct for identification from flows, though the operator acts per device. Regime: the paper trains on the first day and tests on the rest (temporal); devices recur across days and sessions, so a grouping by session or device matters too (SPLIT-3).
- Siblings and duplicates: `operating_system_and_browser_identification_in_tls_traffic` (`TBD -> 2nd Tier`, priority 1; Venari lab sessions, a private Zindi hackathon) is the record it was found for; `cesnet_os_fingerprinting_2024` (`TBD -> Yes`, priority 3; CESNET3 flows of 2024, 20 TCP/IP features, five OS classes) is another source with the same target, its own record (PROV-4), and the curator may want one of the two. The same group's 2023 dataset (https://doi.org/10.5281/zenodo.7635138, "Passive Operating System Fingerprinting Revisited - Network Flows Dataset", about 8 h of university web-server traffic, 111 fields, OS from the User-Agent) is a separate, smaller dataset, moved here from `source_links`. External collections: none found.
- Better data: found as better data for `operating_system_and_browser_identification_in_tls_traffic`.
- Papers and pages: the NOMS 2020 paper (read: Sect. IV dataset, V.C ground truth, VI results).
- Metric: the paper reports "accuracy, precision, recall, and F-score" with micro averaging (Sect. VI.B, Table III), four metrics side by side, so the fallback `log_loss` (MET-5); inputs: the session ID as a group, never a feature.
- Risks for /add-dataset: the HTTP User-Agent OS fields nearly give the label (the paper's User-Agent method: 0.976 accuracy) and go, and the HTTP host and SNI are to judge (LEAK); labels come from DHCP host names, reliable for Apple and Android but editable on Windows and Linux (Sect. V.C; USE-5); the TCP/IP fields alone reach 0.971 accuracy with a decision tree (a TP-4 check); list-valued TLS fields need an encoding; 18.7M rows, so a cut; the anonymised source IP and the session ID are identifiers, not features.
- Priority: gap + (multiclass is thin), use case 0 (asset identification is named, no actor and decision per prediction), source + (a NOMS paper and a documented Zenodo release), shape + (millions of flows, mixed fields, sessions for grouping), risk - (label proxies to drop, host-name labels, near-trivial).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `operating_system_and_browser_identification_in_tls_traffic`.
- as published: flow records of the university's Eduroam wireless devices, 2019-07-12 to 2019-07-16 (5 days); one CSV, 700 MB zipped, row count not on the page; fields: TCP/IP (SYN size, TCP window, TTL), TLS ...; target: operating system of the device (from DHCP logs); access: open.
- Why: Same target (OS) and same feature kind (TLS ClientHello and TCP/IP header fields) as the Zindi record
- Adds: Real traffic of real users' devices instead of scripted browsers in a vendor's lab (the record's Not Representative flag), an open licence instead of a private hackathon, and a session ID that gives the device grouping for an honest split. OS only, no browser label
