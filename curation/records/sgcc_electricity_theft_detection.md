---
unique_name: sgcc_electricity_theft_detection
name: SGCC electricity theft detection dataset (State Grid Corporation of China)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Time-series (Classification)
tags:
- AI-Filled (Verify)
original_source: Github
year: '2018'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1109/TII.2017.2785963
- https://github.com/henryRDlab/ElectricityTheftDetection
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the State Grid electricity-theft set, 42,372 customers by 1,035 daily readings with a theft flag per customer, the widely cited real theft data. Its features are one daily series per customer, and the release does not say where the labels come from.
- Source: Zheng, Yang, Niu, Dai, Zhou, "Wide and Deep Convolutional Neural Networks for Electricity-Theft Detection to Secure Smart Grids", IEEE Transactions on Industrial Informatics 14(4):1606-1615 (2018), doi 10.1109/TII.2017.2785963 (closed access, not read). Data on GitHub (henryRDlab/ElectricityTheftDetection, a split zip of `data.zip`, `data.z01`, `data.z02`); README (read 2026-10-31): "a realistic electricity consumption dataset released by State Grid Corporation of China (http://www.sgcc.com.cn/). This dataset contains the electricity consumption data of 42,372 electricity customers within 1,035 days (from Jan. 1, 2014 to Oct. 31, 2016)"; "Please cite our paper when you use this dataset". The README says nothing about the labels; the number of thieves and how they were confirmed were not checked (the archive was not downloaded). No licence.
- Use case: the utility decides which customers to send inspectors to for suspected theft or meter tampering. Fit direct if the flag comes from inspections (not stated in the release). Regime IID by customer (one row each; the window is shared, and when a theft was found is unknown).
- Siblings and duplicates: `smart_meter_electricity_consumption_dataset` (`No`: "looks very fake", no source) is the record this was found next to; no record of the SGCC data. External collections: none known.
- Better data: found as a related task next to `smart_meter_electricity_consumption_dataset` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the TII paper (its abstract is served neither by IEEE Xplore to a fetch nor by Semantic Scholar, which counts 678 citations); the GitHub README.
- Metric: unknown until the paper is read (closed access), so the fallback `roc_auc` for now (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the features are one series of daily consumption per customer, a time-series classification where series models may be the tool (`Time-series (Classification)`; SEL-12: check on the shipped splits whether tabular models are competitive). When the theft happened within the 1,035 days, and whether readings after its detection are in the series (LEAK). Where the labels come from. Many missing days.
- Priority: gap 0, use case 0 (not stated by the release), source + (a journal paper publishes the data and names SGCC), shape 0 (42,372 customers, but one kind of feature), risk - (series modality, undocumented labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `smart_meter_electricity_consumption_dataset`.
- as published: 42,372 customers x 1,035 daily consumption readings (2014-01-01 to 2016-10-31); about 3,600 labelled thieves per the paper (to check); target: Electricity theft (yes/no) per customer; access: open.
- Why: The record's stated use case is fraudulent consumption; this is the widely used real theft dataset, with the customer as unit and a confirmed theft label instead of a per-reading anomaly
- Adds: A real utility source with 42k customers. Concerns: the features are only the daily series (Time-series (Classification) marker likely), many missing days, label provenance thinly documented in the README, no licence (cite the paper)
