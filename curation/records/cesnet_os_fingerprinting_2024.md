---
unique_name: cesnet_os_fingerprinting_2024
name: Transferability of TCP/IP-based OS fingerprinting models (datasets)
checked_by:
- AI (UNVERIFIED)
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
