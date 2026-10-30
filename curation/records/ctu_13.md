---
unique_name: ctu_13
name: CTU-13
checked_by:
- Myunghwan
suggestion: 'No'
tags:
- Non-IID (Temporal)
- Non-IID (Grouped)
original_source: Website
year: '2011'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.stratosphereips.org/datasets-ctu13
- https://www.kaggle.com/datasets/dhoogla/ctu13
- https://doi.org/10.1016/j.cose.2014.05.011
type_adapter_id: curation-record-v1
---

## Comments

⚠️ **AI-FILLED — UNVERIFIED**: triaged by an AI (2026-08-12), no human has verified it. Check the verdict and the fields before relying on them.

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: the one network-traffic candidate with real captured
background traffic and a detection paper, and a natural grouped split by scenario; the labels need checking first.
- Source: Stratosphere Lab, CTU Prague, captured 2011, published with Garcia, Grill, Stiborek & Zunino, "An empirical
  comparison of botnet detection methods", Computers & Security 45:100-123, 2014. Page: "The goal of the dataset was to
  have a large capture of real botnet traffic mixed with normal traffic and background traffic"; 13 scenarios, each
  one malware sample; labels Background, Botnet, C&C Channels, Normal ("we manually analyzed and label each scenario");
  bidirectional Argus NetFlows with labels; full pcaps not released; "These unidirectional NetFlows should not be used".
- Use case: a network operator flags infected hosts from flow records (the paper's detection task); fit direct.
  Regime grouped by scenario (an unseen botnet), temporal within a scenario.
- Siblings and duplicates: `intrusion_detection` (`No`, Lennart: BCCC profiling, labels by attacker IP), `kddcup99`,
  `unsw_nb15`, `cic_ids2017` (`No`, AHDS: generated traffic); CTU-13 differs by its real background traffic. Kaggle
  mirror dhoogla/ctu13 is a re-export, not a separate source.
- Papers and pages: Garcia et al. 2014 (BClus, CAMNEP, BotHunter compared); widely reused in botnet-detection papers.
- Metric: the paper defines its own comparison methodology and "a novel error metric" for botnet detection that scores
  per IP address over time windows (stratosphereips.org publication page; definition not read in full); deliberate
  (MET-5); inputs the source IP and the flow start time, which ship in the NetFlows. To read in the paper before adding.
- Risks for /add-dataset: `Background` means unknown, not benign (drop or treat as unlabelled); labels assigned by
  infected-host IP, and the same infected IPs recur across scenarios, so IP addresses must not be features (LEAK);
  13 scenarios make few groups; very large files.
- Priority: gap + (Grouped thin), use case +, source + (paper, lab page), shape + (millions of flows, mixed types),
  risk - (label-by-IP shortcut, unlabelled background).

Thirteen botnet captures ('scenarios') taken at CTU University, Czech Republic, in 2011; per the canonical page the goal was "a large capture of **real** botnet traffic mixed with normal traffic and background traffic", with a specific malware sample executed per scenario. That makes it the one candidate in the network-IDS family whose background traffic is genuinely observed rather than profile-generated, so criterion 4B does not auto-fail it the way it does [[intrusion_detection]], [[kddcup99]] and [[unsw_nb15]] — hence 2nd Tier rather than No.

**Must be checked before any work.** (1) The three-way label is Botnet / Normal / **Background**, and `Background` means *ground truth unknown*, not benign — most flows are Background, so the usable labelled subset may be small. (2) How labels were assigned: believed to be from the known infected-host IPs, which would be the same label-by-IP shortcut as the BCCC release — unverified, the source is Garcia et al., "An empirical comparison of botnet detection methods", Computers & Security 45:100-123, 2014, which I have not read. (3) The page states the unidirectional NetFlows "should not be used because they were outperformed by our second analysis" using bidirectional NetFlows — take the bidirectional ones. Generalising to an unseen botnet means a grouped split by scenario; within a scenario the flows are also temporal.

CC (2026-10-27, Myunghwan): "so in this case, we decide no for this dataset". Reject CTU-13 after the discussion of shallow two-port rules and insufficient benchmark headroom. This final No supersedes the earlier provisional/add-stage Yes; no further tuned qualification is requested.

**Assessment (AI, 2026-10-29):** Preserve the already applied curator rejection. The actual-data review retained 799,689 labelled records after excluding unknown/background annotations and unsupported infected-source annotations. The shallow two-port rule gave ROC AUC 0.852 in the first fold, close to the separate train-only LightGBM result of 0.858, with the other folds nearly perfect. Representations and training caps differed, so this is a case-specific low-headroom judgment, not a completed matched/tuned TP-4 proof. No Trivial or proven-leak marker is added. The unshipped draft and review were archived, the v2 pointer cleared, and the official claim released. Raw data, probes and the independent panel are preserved locally. Earlier screening text above is historical, not the current verdict.

## Reference

Garcia, S., Grill, M., Stiborek, J., Zunino, A., "An empirical comparison of botnet detection methods", Computers & Security 45:100-123, 2014.
