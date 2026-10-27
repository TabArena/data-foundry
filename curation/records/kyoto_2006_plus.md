---
unique_name: kyoto_2006_plus
name: Kyoto 2006+ (Kyoto University Honeypot Traffic)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Website
year: 2006-2015
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.takakura.com/Kyoto_data/
- https://www.kaggle.com/datasets/harshwardhanbhangale/kyoto-2006
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

⚠️ **AI-FILLED — UNVERIFIED**: triaged by an AI (2026-08-12), no human has verified it. Check the verdict and the fields before relying on them.

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: real honeypot sessions with a labelled attack flag, but the label comes from the deployed detectors and may track the receiving host.
- Source: Song, Takakura, Okabe et al., Kyoto University honeypots, BADGERS 2011; daily session files 2006-11-01 to 2015-12-31 (https://www.takakura.com/Kyoto_data/). As published: one row per session, 24 features (14 KDD-Cup-style connection statistics, 10 extra), `Label` with "'1' means the session was normal, '-1' means known attack was observed in the session, and '-2' means unknown attack was observed" (format document BenchmarkData-Description-New.pdf). Millions of rows per year.
- Use case: a security operator flags a session as an attack as it ends; fit approximate (the source publishes it as NIDS evaluation data, no actor named); regime temporal because the traffic and attacks drift over the years and the files are dated (`Start Time` ships).
- Siblings and duplicates: no duplicate; the network-IDS family: kddcup99 (`No`, Andrej and Lennart: simulated, outdated), nsl_kdd, unsw_nb15, cic_ids2017 (AI `No`, testbed traffic), ctu_13 and twente_2009_labeled_flows (AI `TBD -> 2nd Tier`, observed traffic). External collections: none found.
- Papers and pages: Song et al. 2011 (BADGERS; not read); format document (read); widely used in NIDS papers.
- Metric: none found (project page and format document; the BADGERS paper not read), so the fallback `roc_auc` on attack vs normal (MET-1, MET-8).
- Risks for /add-dataset: `IDS_detection`, `Malware_detection` and `Ashula_detection` are the detectors' outputs ("We used Symantec IDS to extract this feature") and the label is likely derived from them: drop them and check whether the label is reconstructible from them (LEAK, SEL-5); normal traffic comes from separate hosts (mail server, web crawler), so the label may track the destination address or port (a host shortcut, LEAK); IPs are sanitized per month only. The old marker `No Good Target (yet)` replaced by `TBD`: the source defines a target, its validity is the open point.
- Priority: gap - (technology & internet, temporal not thin), use case - (no actor in the source), source + (paper, format document, university page), shape + (large, mixed types, temporal), risk - (detector-derived label, host shortcut).

Session-level records extracted with Bro 2.4 from Kyoto University's honeypots and darknet sensors, as daily files covering 2006-11-01 to 2015-12-31. The traffic is genuinely observed, so criterion 4B is not the problem here — the target is.

**The label is another detector's output.** The canonical page describes the current release as "Bro 2.4 based session extraction. Based on new IDS detection result", i.e. rows are labelled by what the deployed IDS/AV flagged, not by verified ground truth, so a model trained on it distils an IDS rather than learning intrusion. Second concern: the page's "Deployed systems" list separates the honeypots from a mail server and a web crawler, so benign vs attack may track which host received the traffic. Both need checking against the format document linked from the page before this moves either way (Song et al., BADGERS 2011, not read).

## Reference

Song, J., Takakura, H., Okabe, Y., Eto, M., Inoue, D., Nakao, K., "Statistical analysis of honeypot data and building of Kyoto2006+ dataset for NIDS evaluation", Proceedings of the First Workshop on Building Analysis Datasets and Gathering Experience Returns for Security (BADGERS), 2011.
