---
unique_name: cesnet_quic22_service_classification
name: 'CESNET-QUIC22: QUIC traffic dataset for service classification'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Many features
- Many class
original_source: Other
year: '2022'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zenodo.org/record/7409923
- https://doi.org/10.1016/j.dib.2023.108888
- '# the evaluation paper (TMA 2023) with the weekly split'
- https://tma.ifip.org/2023/wp-content/uploads/sites/12/2023/06/tma2023-final13.pdf
v2_path: datasets/_dev/tabarena-v0pt2/cesnet_quic22_service_classification_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 4: 153 million QUIC flows of four weeks on a Czech research backbone (CESNET2, November 2022), labelled with 102 web services from the decrypted SNI, with flow statistics, packet histograms and the sizes, directions and times of the first 30 packets; the authors' own study names the operator's decision, splits by week and finds LightGBM on par with a multi-modal CNN, so it is a wide numeric multiclass task outside biology.
- Source: Luxemburk, Hynek, Čejka, Lukačovič, Šiška (CESNET), "CESNET-QUIC22: A large one-month QUIC network traffic dataset from backbone lines", Data in Brief 2023, 108888 (doi 10.1016/j.dib.2023.108888; publisher page 403, not read); Zenodo concept 7409923 (v1 2022-12-07, latest 10728760 of 2024-02-29, CC BY 4.0): one zip of 20.95 GB (89 GB unpacked) and `servicemap.csv` (services, providers and the SNI domains used for labelling). As published (Zenodo): weeks W-2022-44 to W-2022-47 (31.10. to 27.11.2022) with 32.6M, 42.6M, 33.7M and 44.1M flows, 153M in all; 30 fields: ID, SRC_IP, DST_IP, DST_ASN, ports, protocol, QUIC_VERSION, QUIC_SNI, QUIC_USER_AGENT, first and last packet times, duration, bytes and packets each way, PPI (sizes, directions and inter-packet times of the first 30 packets), PPI length, duration and roundtrips, four 8-bin packet histograms, APP (102 services and 3 background classes), CATEGORY and three flow-end reasons. Services were subsampled at collection, the more prevalent ones more, so "the class imbalances in the dataset differ from the true distribution of the original network" (TMA paper, footnote 2); JSON files with the flow counts before sampling ship.
- The task's table: one row per flow, 153M rows (stated) x about 133 numeric inputs (8 flow statistics, 32 histogram bins, 3 end reasons and 90 packet values: the TMA paper's FLOWSTATS and PSTATS), with QUIC version, user agent, destination ASN and ports to weigh; target APP (105 classes). The paper trains on the first week (30M flows) and tests on 20M flows of the next three; a cut is needed (a training week and later test windows, capped). Access: open, CC BY 4.0, one 21 GB zip; the CESNET DataZoo library (github.com/CESNET/cesnet-datazoo) serves sized subsets.
- Use case: an ISP's monitoring system identifies the web service behind an encrypted QUIC flow without decrypting the handshake, for "QoS prioritization, or the enforcement of network-usage policies" and against "SNI faking" and Encrypted Client Hello (Luxemburk, Hynek, Čejka, "Encrypted traffic classification: the QUIC case", TMA 2023, Sec. I, read). Fit direct: the SNI gives the ground truth and is withheld from the inputs, as it would be under Encrypted Client Hello. Regime temporal: train on one week, test on the following weeks (TMA Sec. IV), which measures the drift the paper studies.
- Siblings and duplicates: `cesnet_os_fingerprinting_2024` (CESNET, operating system from TCP/IP flows; kept for later by the curator), `tls_os_fingerprinting_masaryk` and `operating_system_and_browser_identification_in_tls_traffic` predict an operating system, another target (PROV-7). No service-classification record (grep: cesnet, quic, traffic classification). The same group's CESNET-TLS22 and CESNET-TLS-Year22 hold the TLS counterpart (another protocol; no record). External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08). In passing: CESNET-QUICEXT-25 (https://zenodo.org/records/17249078, 2025-10-02, CC BY 4.0, the same group): a year of QUIC flows on CESNET3 (June 2024 to May 2025) sampled uniformly 1:100, so with the network's own service mix, with the same flow, histogram and PPI fields plus extended QUIC and TLS handshake fields and QUIC_SNI, but no service label: one would be built from the SNI with `servicemap.csv`. Newer and longer; whether it holds the same task depends on that labelling, the curator's call.
- Papers and pages: the TMA 2023 paper (read: Table I gives LightGBM 80.87% accuracy, 98.26% provider-level accuracy, 80.65% macro F1 and 78.05% macro recall, against 77.41%, 97.94%, 82.74% and 80.60% for the multi-modal CNN and 68.68% accuracy for a lookup of destination IPs); the Data in Brief article (not read); the DataZoo documentation.
- Metric: the TMA paper reports accuracy, provider-level accuracy, macro F1 and macro recall side by side (Sec. IV, Table I) with no single criterion, so the fallback `log_loss` (MET-5, MET-8); its footnote that recall survives the per-service sampling while accuracy and F1 do not bears on MET-2 (the class mix is not the network's). Inputs: none.
- Risks for /add-dataset: QUIC_SNI is the label's source and goes (LEAK-10), as do ID and SRC_IP; DST_IP and DST_ASN identify many services by lookup (the paper's IP baseline), an input the operator has but that goes stale, so its place is a choice; the user agent may name the app; the per-service sampling makes the class mix artificial (MET-2); the PPI is a packet sequence for which CNNs are the field's other tool, though LightGBM matched one here (SEL-12 holds on the paper's numbers); 153M rows need a cut that keeps every service in each window (TP-8).
- Priority: gap + (multiclass is thin), use case + (the paper names the operator's decisions), source + (data paper, documented Zenodo release, an evaluation paper), shape + (millions of flows, about 133 inputs, weekly windows), risk - (SNI and IP shortcuts, a sampled class mix).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the use case reworded to labelling exported flow records for reporting, accounting and audit, with the first-30-packets score in the notes, log loss 0.260 against 0.220, USE-3, LEAK-1; the closed world named in the fit note, USE-8; the class mix from the source's per-service sampling in the metric reason, MET-5, MET-6; the 1-in-20 sample of a temporal frame recorded as a departure, class shares hold; split notes on the 31 Oct-1 Nov capture break, the 17 Nov holiday and sampling drift, SPLIT-20; negative inter-packet gaps and dst_asn 65535 to missing, CLEAN-11; ppi_dir as a named CLEAN-14 exception; 132 features; quic_version 0xfaceb00x named as Meta's QUIC stacks). Correction to the screening: the task ships 102 classes and draws from the release's 140.47M service flows; 105 classes and 153M flows are the release's totals. Disputed: USE-6/USE-10 (the server address and network as inputs), USE-5/USE-8 (the closed world), MET-5/MET-16 (class-weighted log loss); for the curator: issues 1-3. Priority 4: gap +, use case +, source +, shape +, risk - (gap: multiclass is thin; use case: the evaluation paper names the operator's decision; source: data article, documented Zenodo release and an evaluation paper; shape: 2.5M rows, 132 features, temporal; risk: the server address is much of the score, a sampled class mix, a closed world).
