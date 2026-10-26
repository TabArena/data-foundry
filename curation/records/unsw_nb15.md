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

**Screening (AI, 2026-10-22):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16; PROV-3): the traffic was generated in a lab by a commercial traffic generator, with synthetic attacks, like `kddcup99` (Andrej, `No`) and `cic_ids2017`.
- Source: UNSW Canberra Cyber Range Lab, Moustafa & Slay, "UNSW-NB15: a comprehensive data set for network intrusion detection systems", MilCIS 2015 (<https://research.unsw.edu.au/projects/unsw-nb15-dataset>); as published: "The total number of records is two million and 540,044", 49 features "with the class label", nine attack categories, a prescribed training set (175,341 records) and testing set (82,332 records).
- Decisive words (project page): "The raw network packets of the UNSW-NB 15 dataset was created by the IXIA PerfectStorm tool in the Cyber Range Lab of UNSW Canberra for generating a hybrid of real modern normal activities and synthetic contemporary attack behaviours." Both classes come out of the traffic generator: the attacks are synthetic, the "normal activities" are profiles replayed by the tool, not observed users.
- Siblings: `kddcup99` (`No`, Andrej: simulated, outdated), `intrusion_detection` (Lennart, `No`), `cic_ids2017` (AI `No`, testbed traffic); `ctu_13` (AI `TBD -> Yes`) differs by its real background traffic; `kyoto_2006_plus` (real honeypot traffic). External collections: many IDS benchmarks, none of ours.
- Metric: not needed for a reject (the papers report accuracy, detection and false-alarm rates side by side).
- Not checked: the MilCIS 2015 paper's text (not read); the old AI note quoted the same page.
- Reject check (AI, 2026-10-22): stands. SEL-16/PROV-3 (Must) holds on the source's own words, not a reading of them: "The raw network packets of the UNSW-NB 15 dataset was created by the IXIA PerfectStorm tool in the Cyber Range Lab of UNSW Canberra for generating a hybrid of real modern normal activities and synthetic contemporary attack behaviours" (https://research.unsw.edu.au/projects/unsw-nb15-dataset, re-read 2026-10-22). Both classes come out of a commercial traffic generator; the 'real ... normal activities' are profiles the tool emulates, not observed users. The curator-checked siblings take the same call: kddcup99 (Andrej, Lennart: No, AHDS) and intrusion_detection (Lennart: No, AHDS); ctu_13 differs because its background traffic was captured, not generated.

The most-benchmarked modern tabular IDS dataset and the usual stand-in for KDD'99: 2,540,044 records with 49 features across four CSVs, nine attack categories, plus a prescribed train/test partition (`UNSW_NB15_training-set.csv` / `_testing-set.csv`). Recorded mainly so we have an answer when asked about it.

**Suggested No on criterion 4B**, from the canonical page's own description: the raw packets "was created by the **IXIA PerfectStorm tool** in the Cyber Range Lab of UNSW Canberra for generating a hybrid of real modern normal activities and **synthetic** contemporary attack behaviours". Both sides of the traffic come out of a commercial traffic generator in a lab, so it is the same scripted-testbed situation as [[kddcup99]] and [[intrusion_detection]], only newer. The `attack_cat` column also allows a 9-class framing if the verdict is ever revisited. The paper (Moustafa & Slay, MilCIS 2015) is not read — the quote above is from the project page.

## Reference

Moustafa, N., Slay, J., "UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set)", Military Communications and Information Systems Conference (MilCIS), 2015.
