---
unique_name: unsw_nb15
name: UNSW-NB15
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
original_source: Website
year: '2015'
domain: technology & internet
required_split:
- Custom
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://research.unsw.edu.au/projects/unsw-nb15-dataset
- https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

⚠️ **AI-FILLED — UNVERIFIED**: triaged by an AI (2026-08-12), no human has verified it. Check the verdict and the fields before relying on them.

The most-benchmarked modern tabular IDS dataset and the usual stand-in for KDD'99: 2,540,044 records with 49 features across four CSVs, nine attack categories, plus a prescribed train/test partition (`UNSW_NB15_training-set.csv` / `_testing-set.csv`). Recorded mainly so we have an answer when asked about it.

**Suggested No on criterion 4B**, from the canonical page's own description: the raw packets "was created by the **IXIA PerfectStorm tool** in the Cyber Range Lab of UNSW Canberra for generating a hybrid of real modern normal activities and **synthetic** contemporary attack behaviours". Both sides of the traffic come out of a commercial traffic generator in a lab, so it is the same scripted-testbed situation as [[kddcup99]] and [[intrusion_detection]], only newer. The `attack_cat` column also allows a 9-class framing if the verdict is ever revisited. The paper (Moustafa & Slay, MilCIS 2015) is not read — the quote above is from the project page.

## Reference

Moustafa, N., Slay, J., "UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set)", Military Communications and Information Systems Conference (MilCIS), 2015.
