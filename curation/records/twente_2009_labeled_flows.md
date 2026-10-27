---
unique_name: twente_2009_labeled_flows
name: Twente 2009 Labeled Flow-based IDS Data Set
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Website
year: '2009'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://link.springer.com/chapter/10.1007/978-3-642-04968-2_4
- https://www.simpleweb.org/wiki/index.php/Traces
- https://www.simpleweb.org/wiki/index.php/Labeled_Dataset_for_Intrusion_Detection
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

⚠️ **AI-FILLED — UNVERIFIED**: triaged by an AI (2026-08-12), no human has verified it. Check the verdict and the fields before relying on them.

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: real flow records of one honeypot labelled by its logs, but almost all traffic is suspicious by design, so the IDS task (attack against benign) is not in the data, and the host does not answer.
- Source: Sperotto, Sadre, van Vliet, Pras, "A Labeled Data Set For Flow-based Intrusion Detection", IPOM 2009, LNCS 5843, pp. 39-50 (University of Twente). The data page (simpleweb.org, unreachable from here; read from the Wayback copy of 2022-03-08): "traffic collected at a honeypot hosted in the network of the University of Twente in September 2008", "By design, the honeypot only captured "unexpected" traffic, hence it can be assumed that most of the recorded traffic is at least suspicious"; a gzipped MySQL dump with tables `flows` (anonymized IPs, packets, octets, start and end times, ports, TCP flags, protocol), `alert_type` (service and type, e.g. `icmp_sideeffect`), `alerts` (automated, succeeded, description, timestamp), `flow_alert` and cluster and causality tables. About 14.2M flows, over 98% labelled (from the paper's abstract, via search). IPs are anonymized and do not preserve order.
- Use case: a network operator flags malicious flows; the data holds only traffic that reached a honeypot, so a malicious-against-benign model cannot be trained on it, and an alert-type classifier (ssh, http, ftp, irc, side effect) mirrors the honeypot's log correlation rather than a decision. Fit approximate at best. Regime temporal (one month of flows; scans repeat).
- Siblings and duplicates: `kyoto_2006_plus` (AI, `TBD -> 2nd Tier`, `No Good Target (yet)`, the same honeypot-label concern); no duplicate found. External collections: none found.
- Papers and pages: the IPOM 2009 paper; cited in NIDS dataset surveys as small, one honeypot, little benign traffic (the NTLFlowLyzer survey, Shafi et al. 2025, per the earlier note).
- Metric: none found (the data page, the paper's abstract), so the fallback.
- Risks for /add-dataset: the target is to be built from the alert tables (several tables to join, `Needs extensive data wrangling`); the label is the honeypot's log correlation, so features of the alert side leak it; availability (simpleweb.org down, no mirror checked). The old `problem_type` `Binary Classification` (AI-filled) does not hold for a data set without a benign class; left as set until the labels are read. `original_data_state` changed from `One Table` to `Database (or multiple to-be-joined tables)`: the page lists several tables.
- Priority: gap 0 (technology not thin), use case 0, source + (paper and table guide), shape + (14M flows, temporal), risk - (no benign class, joins, the host down).

Labelled NetFlow data from a honeypot run at the University of Twente (Sperotto et al., IPOM 2009) — real observed traffic, so criterion 4B is fine, but it carries the same honeypot-labelling concern as [[kyoto_2006_plus]]: traffic reaching a honeypot is unsolicited by construction, so check whether the label is anything more than "arrived at the honeypot".

**Source needs recovering first.** simpleweb.org, the distribution point, did not respond at all from here (repeated connection failures, not a 404), so availability must be re-established — try Wayback or the authors — before anyone plans work on it. The paper is paywalled at Springer and was not read; everything above about the labelling is a hypothesis to test, not a finding. Attack variety and volume are also reported as limited by the NTLFlowLyzer survey (Shafi et al., Computers & Security 148:104160, 2025, Sec. 5.1, p. 10).

## Reference

Sperotto, A., Sadre, R., van Vliet, F., Pras, A., "A Labeled Data Set for Flow-Based Intrusion Detection", IP Operations and Management (IPOM), LNCS 5843, pp. 39-50, 2009.
