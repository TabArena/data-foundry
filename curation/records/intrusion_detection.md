---
unique_name: intrusion_detection
name: intrusion-detection
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
- AHDS (Artifical/Handmade/Deterministic/Simulated)
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

# intrusion-detection

## Comments

A data dump from a network profile that requires much preprocessing to make it a dataset. Otherwise, it seems to be a task; need to check the paper

Seems super complicated to parse without a domain expert

## Reference

"Toward Generating a Large Scale Intrusion Detection Dataset and Intruders Behavioral Profiling Using Network and Transportation Layers Traffic Flow Analyzer (NTLFlowLyzer)", MohammadMoein Shafi, Arash Habibi Lashkari & Arousha Haghighian Roudsari, Journal of Network and Systems Management, Vol 33, article 44, 2025
