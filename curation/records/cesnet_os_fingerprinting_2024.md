---
unique_name: cesnet_os_fingerprinting_2024
name: Transferability of TCP/IP-based OS fingerprinting models (datasets)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2025'
domain: technology & internet
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.5281/zenodo.14703490
- https://dl.ifip.org/db/conf/networking/networking2025/1571127729.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: passive OS identification from TCP/IP flow features on real traffic of about 24,000 devices in four networks of the CESNET3 research network (2024); labels are partly heuristic and no device id ships.
- Source: Hulák, Bartoš, Čejka (CESNET), "Transferability of TCP/IP-based OS fingerprinting models", IFIP Networking 2025; data on Zenodo (doi 10.5281/zenodo.14703490, 2025-01-20, CC BY 4.0, one zip of 281 MB). As published (Zenodo): flows exported by ipfixprobe, "All data were captured same day in September 2024"; subnet1-4 from CESNET3 (2.07M, 5.54M, 4.06M and 14.08M flows from 8,634, 4,667, 5,266 and 5,680 devices; 20 features: ports, SYN size, TCP window, MSS, options, packets, bytes, flags, protocol, TTL "rounded to nearest higher power of two"), plus a local network (16.9M flows, 984 devices, 6 features, labels "from DHCP logs and intern clients database"). Target `OS_LABEL`, 5 classes; the subnets were annotated "using HTTP user-agent, HTTP Host Name, TLS SNI, QUIC SNI, hand annotation, reverse DNS lookup and Shodan".
- Use case: a network operator infers each device's OS from flow records to keep an inventory and spot policy violations; the record's framing, since the Zenodo page names no actor and the paper could not be read. Fit approximate: one row is a flow, while the operator decides per device. Regime grouped: the paper's question is transfer to another network, and one device's flows repeat many times; with no device id, the only group is the network (four subnets share the 20 features).
- Siblings and duplicates: `operating_system_and_browser_identification_in_tls_traffic` (`TBD -> 2nd Tier`, priority 1, TLS sessions of scripted browsers in a vendor's lab) is the record it was found for; `tls_os_fingerprinting_masaryk` (candidate of this run: Masaryk University Eduroam flows of 2019 with DHCP labels and TLS fields) is another source with the same target, its own record (PROV-4), and the curator may want only one of the two. External collections: none known.
- Better data: found as better data for `operating_system_and_browser_identification_in_tls_traffic`; no further search this round.
- Papers and pages: the IFIP Networking 2025 paper (dl.ifip.org/db/conf/networking/networking2025/1571127729.pdf, answered 403, not read); the ipfixprobe field documentation.
- Metric: none found (the Zenodo description; the paper's evaluation section is unread). The fallback `log_loss`; inputs none.
- Risks for /add-dataset: labels from reverse DNS and Shodan are inferences, not ground truth (USE-5; check their share in the paper); classes are very unequal (subnet1: Windows 1,780,003 of 2,072,414 flows, iOS 413), so per-fold class counts matter (TP-5, TP-8); without a device id an IID split puts one device's flows on both sides, and a split by network has four groups (SPLIT rules); TTL nearly separates Windows from the rest (a TP-4 probe); one day of capture; rows in the millions, so a cut.
- Priority: gap + (multiclass is thin), use case 0 (not stated by the source), source +, shape + (millions of flows, 20 features), risk - (heuristic labels, no device grouping).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `operating_system_and_browser_identification_in_tls_traffic`.
- as published: 42,678,919 flows from 25,231 devices, 5 OS classes (Android, iOS, Linux, macOS, Windows); four subnets of the CESNET3 research network (2.1M to 14.1M flows each, 20 TCP/IP features: TTL, TCP window, ...; target: OS_LABEL (annotated from HTTP User-Agent, host name, TLS and QUIC SNI, hand annotation, reverse DNS, Shodan); access: open.
- Why: Same target (OS) with features of the same kind as the Zindi data's TCP/IP fields (ip.ttl, tcp.window_size_value)
- Adds: Newest and largest: real traffic of thousands of devices on four networks, so a split by subnet tests transfer. No TLS fields and the labels are partly heuristic (reverse DNS, Shodan); Windows dominates most subnets

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the task's table is the published flow table itself, 42,678,919 rows. The four CESNET3 subnets have 21 inputs and the dormitory network 6. No device id or time ships, and the inputs collapse onto a few hundred header tuples. `tls_os_fingerprinting_masaryk` is the same task from another group, and it ships what this one lacks. Priority 2 is proposed.
- As published: Zenodo 10.5281/zenodo.14703490 (v1, 2025-01-20, CC BY 4.0), one zip `OS_datasets_0924.zip` of 281,335,021 bytes with five CSVs. Uncompressed sizes from the zip directory: local.csv 555,103,168 bytes, subnet1.csv 166,887,574, subnet2.csv 440,357,891, subnet3.csv 313,452,051, subnet4.csv 1,043,586,455. Rows (Zenodo table): subnet1 2,072,414 (8,634 devices), subnet2 5,543,868 (4,667), subnet3 4,061,360 (5,266), subnet4 14,082,272 (5,680), local 16,919,278 (984); 42,678,919 in all. Columns, read from previews: each subnet CSV has 22 columns, OS_LABEL and 21 fields: DST_PORT, SRC_PORT, TCP_SYN_SIZE, TCP_WIN, TCP_WIN_REV, TCP_MSS, PACKETS, PACKETS_REV, BYTES, BYTES_REV, TCP_OPTIONS, TCP_OPTIONS_REV, DIR_BIT_FIELD (twice, under the same name), FLOW_END_REASON, L3_FLAGS, L3_FLAGS_REV, PROTOCOL, TCP_FLAGS, TTL, TTL_REV. local.csv has 7: SRC_PORT, TCP_SYN_SIZE, TCP_WIN, TCP_MSS, PROTOCOL, TTL, OS_LABEL. No IP address, device id or timestamp ships. The labels are lower-case: android, ios, linux, macos, windows.
- The paper (IFIP Networking 2025, now read at https://networking.ifip.org/2025/images/Net25_papers/1571127729.pdf). Sect. III.B: local was captured in "a local network of a university dormitory" and labelled from registration data. Sect. III.C: a device (an IP address) gets a label only when every annotator that answers agrees: hand, reverse DNS, Shodan, HTTP User-Agent, HTTP Host, TLS SNI, QUIC SNI. Validated on local: "The multi-annotator method successfully labelled 79.3 % of the flows, out of which 98.4 % flows were labelled correctly". Sect. IV.A: flows with TCP_SYN_SIZE or TCP_WIN equal to zero are removed, classes above 40,000 flows are under-sampled, flows per device are capped, iOS is merged into macOS, and "we exclusively used macro-averaged Precision and F1-score". The models use five features (TCP_SYN_SIZE, TCP_WIN, TCP_MSS, TTL, SRC_PORT). Results: macro F1 of 87 to 99% within one network, from a random forest on a random 60:20:20 flow split (Table II); 70 to 98% across networks (Table III).
- The task's table: one row per flow, 42,678,919 rows as published (stated), before the paper's filter on a zero SYN size or window (the count after it is not stated). Inputs: 21 in the subnets, 6 in local. The five header fields carry the OS; the rest describe the connection. The operator decides per device, but no device key ships, so a per-device table cannot be built and an IID split puts each device's flows on both sides (SPLIT rules). The only grouping is the network: 4 subnets with the same 21 fields, plus local with 6. The rows repeat a few stack fingerprints many times. In the previews, the first 134,469 rows of local.csv hold 44 distinct combinations of the inputs other than the source port, and the first 22,666 rows of subnet1.csv hold 199 distinct (TCP_SYN_SIZE, TCP_WIN, TCP_MSS, TTL) tuples.
- Access: open, CC BY 4.0, a 281 MB zip of five CSVs (2.5 GB unpacked), no login.
- Changes the call: (1) `tls_os_fingerprinting_masaryk` is the same task from another publisher (CESNET and CTU Prague here, Masaryk University there), another network (CESNET3 subnets and a dormitory against Masaryk's Eduroam) and another year (September 2024 against July 2019). It is not a version (PROV-6) and not a shared source (PROV-7), so each keeps its own record (PROV-4), and the curator picks. This one is newer and larger (42.7M flows and 25,231 devices, against 18.7M flows and 11,962 MAC addresses) and has five networks for a transfer test. Masaryk's label comes from DHCP host names, a record independent of the traffic, and it ships a session id for a grouping, timestamps for the paper's temporal split, TLS fields and more inputs. (2) The shape point (+) rested on a grouped or temporal structure that this table lacks, and the rows collapse onto few fingerprint tuples, which needs a TP-4 check at /add-dataset (a lookup on TCP_SYN_SIZE, TCP_WIN, TCP_MSS and TTL). Proposed priority 2: gap +, use case 0, source +, shape 0, risk -. (3) Metric: macro precision and macro F1 are reported side by side (Sect. IV.A), both on hard labels, so the fallback `log_loss` stands (MET-5, MET-6).
- Not checked: the row count after the paper's zero-field filter; distinct-tuple counts over the full files (previews only); whether subnets 2-4 include Masaryk University's network (the paper says only "large universities").
