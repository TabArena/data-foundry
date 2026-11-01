---
unique_name: litnet_2020_network_intrusion
name: LITNET-2020 annotated real-world network flow dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
year: '2020'
domain: technology & internet
problem_type: Multiclass Classification
source_links:
- https://github.com/Grigaliunas/electronics9050800
- https://doi.org/10.3390/electronics9050800
- https://www.kaggle.com/datasets/dhoogla/litnet2020
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: NetFlow records of the Lithuanian research and education network (LITNET, March 2019 to January 2020; 45.3 million flows, 5.3 million in 12 attack types) with real background traffic, but the attack labels come from the authors' attack rules over the same flow fields, so the task may be a rule to relearn (SEL-5, TP-4).
- Source: Damasevicius, Venckauskas, Grigaliunas, Toldinas, Morkevicius, Aleliunas and Smuikys, "LITNET-2020: An Annotated Real-World Network Flow Dataset for Network Intrusion Detection", Electronics 9(5):800 (2020, https://doi.org/10.3390/electronics9050800; text read from the KTU repository copy, epubl.ktu.edu, since MDPI answered 403); data first at dataset.litnet.lt, which now redirects to https://github.com/Grigaliunas/electronics9050800 (12 per-attack zips plus ALLinONE.zip, 1.15 GB; "freely available for research purposes", no licence file). As published: "The dataset was created at KTU LITNET network from 06/03/2019 to 31/01/2020"; Table 4: 45,330,333 flows, 5,328,934 attack flows (TCP SYN flood 3,725,838, Code Red worm 1,255,702 down to packet fragmentation 477); 85 features: 49 NetFlow v9 fields, 15 extended fields, 19 attack-recognition attributes (Table 6) and 12 time-slice counts over the previous 10,000 connections (Table 7); labels `attack_t` (type or none) and `attack_a` (0 background, 1 attack); "The IP addresses of network nodes have been anonymized".
- Use case: a network operator flags attack flows from exported NetFlow; the paper evaluates NIDS features and names no operator decision; fit approximate. Regime temporal (ten months of dated flows); the release ships one file per attack type, each with its own background flows (Table 4).
- Siblings and duplicates: `ugr16_isp_netflow_intrusion` (`TBD -> Yes`, priority 3; real ISP background with launched attacks, the closest precedent), `ctu_13` (`TBD -> Yes`, priority 4), `kyoto_2006_plus` and `luflow_intrusion_detection` (`TBD -> 2nd Tier`, priority 2: labels from detectors or threat feeds, the label concern here), `twente_2009_labeled_flows` (`TBD -> 2nd Tier`), `cic_ids2017`, `unsw_nb15`, `kddcup99`, `intrusion_detection` (`No`, generated traffic). No duplicate. External collections: a Kaggle re-upload (https://www.kaggle.com/datasets/dhoogla/litnet2020); listed in the intrusion-dataset survey arXiv 2502.06688.
- Better data: from the curator's Zotero collection (item 85, a review of cyber-risk data availability); no further search this round.
- Papers and pages: the paper (statistics and clustering of the features, no supervised benchmark); the survey arXiv 2502.06688: "The authors emulated 12 types of intrusions, but similar to previous datasets, they provide no information about used tools and their parameters", against the paper's Section 3.5, "contains real network attacks over the country-wide network infrastructure": whether the attacks are real or launched by the authors is open.
- Metric: none found (the paper trains no classifier: feature statistics, t-SNE and density clustering; the GitHub page states none), so the fallback `log_loss` for the attack type, `roc_auc` for the attack flag (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: the labels: Section 3.1, "In this time interval, we counted the number of packets, which satisfied the attack rules to distinguish the type of attack", and Section 3.4, "The generator creates additional 19 attributes for attack type recognition ... The combinations of these and NetFlow attributes are used to detect attacks"; Section 3.2 defines types by ports, flags and protocol ("The attack packets are directed only to 80 port"), so drop the 19 attack-recognition attributes and check whether ports, flags and protocol alone reproduce the label (SEL-5, TP-4); background is unverified traffic, not labelled benign (as for `ctu_13`, `ugr16_isp_netflow_intrusion`); attack windows differ per file, so time and window counts can tell the class (LEAK-13 to LEAK-15, `Class-dependent Recording` to check); 45 million flows need a documented subsample.
- Priority: gap + (multiclass is thin, with the attack type as the target), use case 0 (no operator decision in the source; fit approximate), source + (a peer-reviewed data paper with feature tables), shape + (ten months of dated flows, 85 mixed features), risk - (rule-made labels; real or emulated attacks unsettled).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 85: "Cyber risk and cybersecurity: a systematic review of data availability".
- as published: NetFlow records from the Lithuanian academic network, 85 flow features, 12 attack types, per-attack zips (ALLinONE.zip 1.15 GB); target: attack type (or attack vs normal) per flow; access: open.
- Why: background traffic from a real production network, unlike the testbed sets rejected as AHDS (cic_ids2017, unsw_nb15)
- Adds: a newer real-network IDS source next to ctu_13 and kyoto_2006_plus
