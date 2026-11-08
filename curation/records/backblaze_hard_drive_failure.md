---
unique_name: backblaze_hard_drive_failure
name: 'Backblaze hard drive test data: drive failure from daily SMART statistics'
checked_by:
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: 'Yes'
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the task's table is one row per drive at a cut date with "fails within N days", about 354,000 drives per cut in 2026. A quarter brings about 1,500 failures: 0.42% at a 90-day horizon, about 0.14% at 30 days. There are up to 194 inputs, of which about 36 SMART columns are filled for most drives. The call stands at priority 3. One label risk is new: about half the failures are Backblaze's own proactive replacements.
- As published: daily CSVs with one row per operational drive per day ("The daily snapshot of one drive is one record or row of data"), in yearly zips for 2013-2015 and quarterly zips since 2016 (https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data). The current schema (https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/Drive_Stats_Schema_Current.csv, "Last Updated Q2 2024") has 197 columns: date, serial_number, model, capacity_bytes, failure, datacenter, cluster_id, vault_id, pod_id, pod_slot_num, is_legacy_format and 186 SMART columns (93 attributes, raw and normalized). The header of 2026-06-30.csv matches it. Earlier quarters have fewer columns (Drive_Stats_Schema_2018_Onward.csv): 105 in Q1 2018, 129 from Q4 2018, 131 from Q4 2019, 149 from Q4 2020, 179 from Q4 2021, 193 from Q3 2023. Totals on the page: lifetime 558,148,607 drive-days and 21,609 failed drives; 2025: 115,638,676 drive-days and 4,317 failures; Q2 2026: 31,553,350 drive-days, 1,498 failures, 354,415 drives.
- The task's table: one row per drive at a cut date (our framing, SEL-11), counts computed from the stated totals. For one quarterly cut in 2026: about 354,415 rows, with 1,498 positives in the quarter (0.42% at a 90-day horizon; about 500 a month, 0.14%, at 30 days). For 2025 with monthly cuts at a 30-day horizon: about 3.8 million rows (12 cuts of the 316,818 drives on an average day, 115,638,676 / 365), with 4,317 positives (0.11%). The rows as published, per drive-day, are 31.6 million in Q2 2026 alone, at 4.7 positives per 100,000. Inputs: model, capacity_bytes, datacenter, cluster_id, vault_id, pod_id, pod_slot_num, is_legacy_format and up to 186 SMART columns. In a 4,522-row preview of 2026-06-30, 36 SMART columns were filled in more than half the rows; which attributes a drive reports depends on its maker and model. serial_number is the group and date the cut. Lags or trends of the SMART values would be our features.
- Access: open download, no login. A quarter is a zip of 1.0 to 2.1 GB (Q2 2026: 2,092,757,685 bytes, 91 daily files of about 138 MB each, 11.7 GB unpacked); one year of 2025 is about 4.4 GB zipped and 46 GB unpacked (the page's four quarters). Terms: "Cite Backblaze as the source if you use the data", "You can not sell the data itself to anyone; it is free" (no named licence).
- Changes the call: a label risk the screening did not name. "for our purposes drive failure is either reactive or proactive", and "failed drives fall basically evenly into these two categories". A proactive failure means indicators "signal that the drive is having difficulty and drive failure is highly probable" (https://www.backblaze.com/blog/backblaze-drive-stats-for-q3-2024/). On the SATA pods, the drive sentinel tool cuts access to a drive whose read and write errors pass a threshold (https://www.backblaze.com/blog/backblaze-drive-stats-for-q3-2025/). About half the positives are therefore Backblaze's own replacement decisions, taken on signals that overlap the SMART inputs: a label that partly follows the operator's rule (USE-5). The rule is not published, so SEL-5 does not decide it; a TP-4 check at /add-dataset does (e.g. how far SMART 5, 187, 188, 197 and 198 above zero alone go). The Q3 2025 post also describes "cosmetic" failures: drives of a Toshiba MG08 population pulled for firmware updates and counted as failed. The risk point is already taken, so priority 3 stands. A related source, not better data: the PAKDD 2020 Alibaba AI Ops competition (https://github.com/alibaba-edu/dcbrain, `diskdata/`; Tianchi dataId 70251) has "over 200 thousands hard disk drives" of Alibaba Cloud, 2017-07-31 to 2018-12-31, as daily SMART logs of 514 columns plus a fault-tag table. It is scored by a precision and recall over 30-day windows. It is older and has fewer drives, but it fixes the task, a 30-day horizon per disk, that the Backblaze framing has to define itself; no record exists for it.
- Not checked: positives per horizon counted on the files (computed from the page's totals); whether drives later found healthy are reset to `failure=0` in the published files (the Q3 2024 post says the dataset "is updated accordingly"); SMART fill rates over all models (one preview of one day).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).
