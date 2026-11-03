---
unique_name: luflow_intrusion_detection
name: LUFlow Network Intrusion Detection Data Set
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Kaggle
domain: technology & internet
required_split:
- Temporal (NON-IID)
source_links:
- https://www.kaggle.com/datasets/mryanm/luflow-network-intrusion-detection-data-set
- 'https://arxiv.org/pdf/2502.06688 (2025 NIDS dataset survey: 206.56M bidirectional flows, 16 features)'
- https://arxiv.org/pdf/2502.06688 (2025 NIDS dataset survey, per scout_26)
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: real flows of Lancaster University's address space (2020-2022, about 206M) labelled benign, malicious or outlier, but the malicious label comes from matching third-party threat feeds and the classes come from different hosts (honeypots against production services), the label concern of `kyoto_2006_plus`.
- Source: R. Mills (Lancaster University), "LUFlow Network Intrusion Detection Data Set", Kaggle mryanm/luflow-network-intrusion-detection-data-set (CC BY-SA 4.0; sources "Servers deployed within Lancaster University"; DOI 10.34740/kaggle/dsv/11194052 in the survey's references). Description (Kaggle API): "LUFlow contains telemetry containing emerging attack vectors through the composition of honeypots within Lancaster University's address space. The labelling mechanism is autonomous and is supported by a robust ground truth through correlation with third part Cyber Threat Intelligence (CTI) sources ... Flows which were unable to be determined as malicious, but are not part of the normal telemetry profile are labelled as outliers ... Normal traffic is also captured from production services, e.g. ssh and database traffic." Daily CSVs in year/month folders from 2020-06-19, 60 to 420 MB per day (file list). The NIDS survey of Goldschmidt and Chudá (arXiv 2502.06688, Computers & Security 2025; its table and text read): 2020-22, real traffic, bidirectional flows, 16 features, IPs included, 206.56M flows, labelled "as benign, malicious, or outlier", and "no longer updated".
- Use case: a network operator flags malicious flows; the source names only "detection mechanisms suitable for emerging threats"; fit approximate: the label says a flow's source matched a threat feed, and benign rows come from production servers while malicious ones reach honeypots. Regime temporal (dated daily files; the source's aim is emerging threats).
- Siblings and duplicates: the network-IDS family: `kyoto_2006_plus` and `twente_2009_labeled_flows` (AI `TBD -> 2nd Tier`, priority 2: honeypot traffic with detector or log labels), `ctu_13` (AI `TBD -> Yes`, priority 4) and `ctu_sme_11` (AI `TBD -> Yes`, priority 2: captured traffic with expert labels), `cic_ids2017`, `unsw_nb15`, `kddcup99` (`No`, AHDS: generated traffic). No duplicate (grep luflow, lancaster). External collections: none found.
- Better data: found as better data for `cic_ids2017`, `kddcup99`, `kyoto_2006_plus`, `twente_2009_labeled_flows` and `unsw_nb15`; no further search this round.
- Papers and pages: the Kaggle description; the survey above; a companion paper by Mills et al. on detecting emerging threats was not read. The record's two links to the survey are a related paper, not a download (records.md: related work goes into the comments).
- Metric: none found (the Kaggle page, the survey), so the fallback: `roc_auc` for malicious against benign, `log_loss` if the outlier class is kept (MET-1, MET-8, MET-11); inputs none.
- Risks for /add-dataset: `src_ip`, `dest_ip` and the ports can give the class away (a feed match on the address; classes captured on different hosts): drop the addresses and probe a destination-port shortcut (LEAK; `Class-dependent Recording` to check, LEAK-13); the outlier class has no ground truth (drop it or ship three classes, USE-5); 206M flows need a sample by day; the start and end times serve the split, not the features; the 16 columns were not seen (no file was opened).
- Priority: gap 0 (technology & internet has 4 accepted, not thin), use case 0 (no actor), source + (an identified university source with a DOI, described by a peer-reviewed survey), shape + (hundreds of millions of dated flows), risk - (a feed-match label, class-dependent capture).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `cic_ids2017`, `kddcup99`, `kyoto_2006_plus`, `twente_2009_labeled_flows`, `unsw_nb15`.
- as published: daily CSV files, one row per bidirectional flow, 16 features (bytes and packets in/out, inter-packet time, entropy, ports, protocol, times); a survey counts 206.56M flows; CC BY-SA 4.0; target: label: benign, malicious or outlier; access: open.
- Why: Same task as both records (flow or session-level intrusion detection on real traffic from honeypots in a university address space), labelled by correlation with third-party cyber threat intelligence rather than by the honeypot's own logs or an IDS | same flow-level intrusion detection task on real traffic captured in ...
- Adds: Newer (2020-2022 against 2009 and 2006-2015) and has a benign class captured from production services (ssh, database), which twente_2009 lacks; dated daily files for a temporal split. Same risk as kyoto: benign and malicious come from different hosts, so check for a destination host or port shortcut; the outlier ...
