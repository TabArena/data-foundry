---
unique_name: intrusion_detection
name: intrusion-detection
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Needs extensive data wrangling
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- No Good Target  / Scientific Discovery
tags:
- Non-IID (Temporal)
- Non-IID (Grouped)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/datasets/bcccdatasets/large-scale-ids-dataset-bccc-cse-cic-ids2018/
- https://www.kaggle.com/datasets/solarmainframe/ids-intrusion-csv
source_row: 636
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-08-12, Lennart): The BCCC re-release re-extracts ~300 features from the original pcaps rather than re-slicing the published CSVs, but its own paper builds a behavioural *profiling* system — "our focus is on developing a profiling system, not a detection system" (Shafi et al., Computers & Security 148:104160, 2025, Sec. 6.1, p. 12) — so no predictive target, split or baseline comes with the data. Its labels are assigned by attacker IP and shipped next to `src_ip`/`dst_ip`/`flow_id`, and the attack classes are minute (infiltration 5 flows, SQL injection 66) against 7-11 GB of benign flows per day.

A data dump from a network profile that requires much preprocessing to make it a dataset. Otherwise, it seems to be a task; need to check the paper

Seems super complicated to parse without a domain expert

## Reference

"Toward Generating a Large Scale Intrusion Detection Dataset and Intruders Behavioral Profiling Using Network and Transportation Layers Traffic Flow Analyzer (NTLFlowLyzer)", MohammadMoein Shafi, Arash Habibi Lashkari & Arousha Haghighian Roudsari, Journal of Network and Systems Management, Vol 33, article 44, 2025
