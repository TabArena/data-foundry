---
unique_name: backblaze_hard_drive_failure
name: 'Backblaze hard drive test data: drive failure from daily SMART statistics'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Company
year: '2013'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data
- https://github.com/awesomedata/apd-core/tree/master/core//TimeSeries/Hard-Drive-Failure-Rates.yml
- https://github.com/ErikinBC/SurvSet
- https://arxiv.org/abs/2203.03094
- https://cran.r-project.org/package=frailtySurv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Backblaze's daily SMART snapshots of every drive in its data centres since 2013 (354,415 drives in Q2 2026), with the day a drive failed; a real fleet-maintenance task once framed as "fails within N days" at a cut date.
- Source: Backblaze, "Hard Drive Data and Stats" (backblaze.com/cloud-storage/resources/hard-drive-test-data): "Each day, Backblaze takes a snapshot of every operational drive"; "The daily snapshot of one drive is one record or row of data", with basic drive information and raw and normalized S.M.A.R.T. attributes; yearly files for 2013-2015, quarterly since 2016, the latest Q2 2026 (354,415 drives, 1,498 failures in the quarter); "schema changes from quarter to quarter do occur". Terms: "Cite Backblaze as the source if you use the data"; "You can not sell the data itself to anyone; it is free" (no criterion, EV-4). Failure: "Drives which have failed are marked as such and their data is no longer logged", and drives removed for other reasons are not failures (Backblaze blog, Andy Klein, 2016-10-06, "What SMART Stats Indicate Hard Drive Failures").
- Use case: the operator decides which drive to investigate, migrate or replace before it fails: "When the RAW value for one of these five attributes is greater than zero, we have a reason to investigate" (the same post); fit direct for a fixed-horizon label at a cut date; regime temporal (train on earlier cut dates, test on later ones), with the drive serial as the group.
- Siblings and duplicates: `ai4i_2020_predictive_maintenance_dataset` (`TBD -> 2nd Tier`, synthetic), `tokyo1` (`TBD -> 2nd Tier`), `scania_component_x` and `antarex_hpc_fault_classification` (unscreened): other sources and tasks, no duplicate. External collections: SurvSet (`hdfail`, a small survival extract, by the scout), awesome-public-datasets.
- Better data: found as better data for `ai4i_2020_predictive_maintenance_dataset`, and as a related task for `tokyo1`; also in the curator's Zotero collection (items 96, 140, 148); no further search this round.
- Papers and pages: the Backblaze data page and its Drive Stats posts; SurvSet (arXiv 2203.03094).
- Metric: none found (Backblaze publishes failure rates, no prediction task), so the fallback `roc_auc` (MET-8; the imbalance alone is no reason for PR AUC, MET-9); inputs none beyond the cut date and serial for the split.
- Risks for /add-dataset: the framing is ours and comes first: one row per drive at a cut date, the SMART values known then (lags if the curator wants them), the label "fails within N days", drives removed without failure treated as censored (SEL-11; no series value is forecast, so not SEL-10); about 1,500 failures among 354,415 drives in a quarter; the schema changes by quarter; 13 years of daily files ask for a sampling plan; SMART attributes differ by maker and model.
- Priority: gap 0 (technology & internet, binary and temporal are not thin), use case + (the operator's own triage rule), source + (the operator publishes and documents it), shape + (hundreds of thousands of drives, temporal and grouped), risk - (the framing and the volume).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ai4i_2020_predictive_maintenance_dataset`; a related task next to `tokyo1`; the curator's Zotero collection, item 140: "SurvSet: An open-source time-to-event dataset repository"; the curator's Zotero collection, item 148: "awesomedata/awesome-public-datasets"; the curator's Zotero collection, item 96: "SurvSet: An open-source time-to-event dataset repository".
- as published: One row per operational drive per day (date, serial, model, capacity, failure flag, raw and normalized SMART attributes); 354,415 drives in Q2 2026; 558,148,607 drive-days and 21,609 failures in total; target: failure (the drive fails that day), turned into 'fails within N days' at a snapshot date; access: open, open (cite Backblaze; the data itself may not be sold).
- Why: Real fleet telemetry from the operator, open, widely used for disk-failure prediction, still updated. | a real predictive-maintenance task (equipment failure from condition-monitoring readings), the task ai4i simulates | tokyo1 classifies a server's state from performance counters, a task no newer labelled public ...
- Adds: Hardware reliability, no record. Caveats: extreme imbalance (about 4 failures per 100,000 drive-days); per-drive series must become fixed-horizon snapshots (SEL-11); very large, so subsample; terms: cite Backblaze, the data itself may not be sold, no named licence. | real failures at very large scale, 13 years of ...
