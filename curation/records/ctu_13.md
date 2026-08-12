---
unique_name: ctu_13
name: CTU-13
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

⚠️ **AI-FILLED — UNVERIFIED**: triaged by an AI (2026-08-12), no human has verified it. Check the verdict and the fields before relying on them.

Thirteen botnet captures ('scenarios') taken at CTU University, Czech Republic, in 2011; per the canonical page the goal was "a large capture of **real** botnet traffic mixed with normal traffic and background traffic", with a specific malware sample executed per scenario. That makes it the one candidate in the network-IDS family whose background traffic is genuinely observed rather than profile-generated, so criterion 4B does not auto-fail it the way it does [[intrusion_detection]], [[kddcup99]] and [[unsw_nb15]] — hence 2nd Tier rather than No.

**Must be checked before any work.** (1) The three-way label is Botnet / Normal / **Background**, and `Background` means *ground truth unknown*, not benign — most flows are Background, so the usable labelled subset may be small. (2) How labels were assigned: believed to be from the known infected-host IPs, which would be the same label-by-IP shortcut as the BCCC release — unverified, the source is Garcia et al., "An empirical comparison of botnet detection methods", Computers & Security 45:100-123, 2014, which I have not read. (3) The page states the unidirectional NetFlows "should not be used because they were outperformed by our second analysis" using bidirectional NetFlows — take the bidirectional ones. Generalising to an unseen botnet means a grouped split by scenario; within a scenario the flows are also temporal.

## Reference

Garcia, S., Grill, M., Stiborek, J., Zunino, A., "An empirical comparison of botnet detection methods", Computers & Security 45:100-123, 2014.
