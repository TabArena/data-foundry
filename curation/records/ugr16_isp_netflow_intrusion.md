---
unique_name: ugr16_isp_netflow_intrusion
name: 'UGR''16: NetFlow traces of a Spanish tier-3 ISP with labelled attacks and anomalies'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2018'
domain: technology & internet
required_split:
- Temporal (NON-IID)
source_links:
- https://doi.org/10.1016/j.cose.2017.11.004
- https://nesg.ugr.es/nesg-ugr16/ (official download; answered 403 to this session)
- https://huggingface.co/datasets/mehedi107/ugr-16 (mirror of the official weekly labelled CSVs)
- https://huggingface.co/datasets/Lystea/UGR16-PARQUET (parquet conversion)
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: NetFlow records of a Spanish tier-3 ISP over five months of 2016, with real customer background traffic, attacks the authors launched inside it and real anomalies labelled afterwards; the real-traffic counterpart of the generated IDS sets, with label and size risks to settle.
- Source: University of Granada, NESG group: Maciá-Fernández, Camacho, Magán-Carrión, García-Teodoro and Therón, "UGR'16: A new dataset for the evaluation of cyclostationarity-based network IDSs", Computers & Security 73:411-424, 2018 (Crossref); site nesg.ugr.es/nesg-ugr16 (answered 403). The abstract (Semantic Scholar, paraphrased): a dataset built from real traffic with up-to-date attacks, for IDSs that model long-term evolution and periodicity (day and night, weekdays and weekends). As published (the Hugging Face mirrors and the run's Assessment): weekly labelled CSVs of unidirectional NetFlow records, 17 calibration weeks (March-June 2016) and 6 test weeks (July-August 2016), about 16.9 billion flows (Lystea's parquet conversion: about 17B rows), 239 GB compressed (mehedi107's mirror); fields times, IPs, ports, protocol, flags, packets, bytes and a label: background, blacklist, dos, scan11, scan44, nerisbotnet, anomaly-spam, anomaly-sshscan, anomaly-udpscan.
- Use case: an ISP's network operator flags malicious flows, or hosts in a time window, from exported NetFlow; the paper evaluates IDSs and names no operator decision; fit approximate: the DoS, scans and botnet were launched by the authors in the test weeks, spam and SSH and UDP scans are real anomalies found by detection, and `background` is unverified rather than benign. Regime temporal: the source's calibration and test weeks.
- Siblings and duplicates: `ctu_13` (`TBD -> Yes`, priority 4: real background traffic, botnets run by the lab; the closest precedent), `kyoto_2006_plus` (`TBD -> 2nd Tier`: labels from deployed detectors, like the anomaly classes here), `cic_ids2017` and `unsw_nb15` (`No`, AHDS: generated benign traffic), `kddcup99` (`No`), `intrusion_detection` (`No`). No duplicate. External collections: none found.
- Better data: found as better data for `cic_ids2017`, `kddcup99`, `unsw_nb15` (the run's Assessment); no further search this round.
- Papers and pages: the paper (not read: ScienceDirect 403, the green copy at digibug.ugr.es behind a bot wall; 215 citations per Semantic Scholar); mirrors huggingface.co/datasets/mehedi107/ugr-16 (the official weekly archives, unmodified, with a SHA-256 manifest) and huggingface.co/datasets/Lystea/UGR16-PARQUET (a 54-column conversion into another schema, licence "source-license-unstated").
- Metric: none found (the paper was not readable here; the mirrors state none), so the fallback: `roc_auc` for an attack flag, `log_loss` for the families (MET-1, MET-8); read the paper's evaluation before adding.
- Risks for /add-dataset: `background` means unlabelled, not benign (drop it or treat it as unknown, as for `ctu_13`); the authors' attacks sit only in the test weeks and come from a few known hosts, so a temporal split meets classes unseen in training, and IP addresses or ports would give them away (LEAK, TP-4); billions of flows need a documented subsample (the 1M cap) that keeps whole windows; the anomaly classes come from the authors' detectors (labels that follow a detector, as for `kyoto_2006_plus`); no licence stated on the mirrors (EV-4: no reason for a verdict); the official download refused this session.
- Not checked: the paper's text (the labelling procedure, the attack schedule, its evaluation); the label counts per week.
- Priority: gap + (multiclass is thin, 24 accepted, if the attack family is the target), use case 0 (no operator decision in the source, fit approximate), source + (a peer-reviewed data paper from the university), shape + (months of dated flows, mixed types), risk - (unverified background, synthetic attacks in the test weeks only, size).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `cic_ids2017`, `kddcup99`, `unsw_nb15`.
- as published: about 16.6 billion unidirectional NetFlow records in 23 weekly files: 17 calibration weeks (March-June 2016) and 6 test weeks (July-August 2016), per the mirrors' cards; NetFlow fields (times, IPs, ...; target: flow label: background, blacklist, or an attack family (dos, scan11, scan44, nerisbotnet, anomaly-spam, anomaly-sshscan, anomaly-udpscan); access: open.
- Why: the same flow-level intrusion detection task with flow features of the same kind, but on real ISP traffic: the background is captured from customers, not generated by a traffic tool (IXIA PerfectStorm for UNSW-NB15, B-Profile agents for CIC-IDS2017, the DARPA'98 simulation for KDD'99)
- Adds: real benign-side traffic, months of dated weeks for a temporal split, far more flows. Caveats: the DoS, scan and botnet attacks in the test weeks were launched by the authors inside the real network (synthetic attacks), while spam, SSH and UDP scans and blacklist hits are real anomalies found afterwards; background ...
