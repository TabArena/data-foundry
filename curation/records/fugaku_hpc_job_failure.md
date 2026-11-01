---
unique_name: fugaku_hpc_job_failure
name: 'F-DATA: A Fugaku Workload Dataset for Job-centric Predictive Modelling in HPC Systems'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2024'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1038/s41597-025-05633-1
- https://doi.org/10.5281/zenodo.11467483
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: about 24 million real jobs of the supercomputer Fugaku (2021-2024) with the features known at submission, published for job-centric prediction, and the authors' own validation predicts the exit state on a temporal split; "failed" is any non-zero exit code, which the paper says may include false positives.
- Source: F-DATA by Antici, Bartolini, Domke, Kiziltan, Yamamoto (University of Bologna and RIKEN R-CCS), Zenodo v1.0 of 2024-06-05 (https://doi.org/10.5281/zenodo.11467483, CC BY 4.0), paper in Scientific Data 12:1321 (2025, https://doi.org/10.1038/s41597-025-05633-1, read on PMC12311113). As published: "around 24 million jobs" from March 2021 to April 2024, 38 monthly parquet files (27.2 GB) and feature_list.csv; per job the submission information (anonymised user, submission time, requested cores, nodes, memory and frequency, job environment), the allocation, start and end times, exit code, duration, power and energy, performance counters (perf1-perf6, flops, memory bandwidth) and the memory- or compute-bound class `pclass`. Target: exit state, "completed if the exit code is 0, and as failed otherwise" (over 21 million completed, "around 2.5 million" failed).
- Use case: the paper lists failure, runtime and power prediction for workload management and scheduling, with "the information available at job submission time" as the first feature category; the scheduler or the centre's operators act at submission (hold, place or power-cap a job); fit direct for the exit state at submission; regime temporal (the paper trains on the first 26 months, 21/03 to 23/05, and tests on 23/06 to 24/04), with users repeating across the cut.
- Siblings and duplicates: `cpu_act` (`TBD -> 2nd Tier`; 1990s sar activity measures, another task in the same domain); no other HPC job record (searched fugaku, F-DATA and both DOIs). External collections: none known (not searched).
- Better data: no new search; found as a related task next to `cpu_act`.
- Papers and pages: Antici et al. 2025 (Technical Validation: XGBoost, random forest and kNN with default settings on exit state, pclass, average power and duration; text encodings compared); Antici, Borghesi, Kiziltan 2024, "Online Job Failure Prediction in an HPC System" (not read).
- Metric: the paper scores "the regression tasks [by] Mean Absolute Error (MAE), and ... the classification tasks [by] accuracy", one rule for all four targets with no threshold or cost fixed: a habit under MET-6, so the fallback `roc_auc` for the exit state (MET-8). Inputs: none (the submission time for the split ships).
- Risks for /add-dataset: the label: a non-zero exit code also covers cancellations and time-limit kills (the paper: the failed count "may include false positives"; check the exit-code values); the post-run columns (start and end times, duration, energy, counters, allocated resources, exit code) must go (LEAK); when `schedsdt` and `qdt` become known is unclear; user, job name, job id and job environment are replaced by indices, and the original user, job name and environment ship only as a 384-dimensional Sentence-BERT embedding (text-derived, SEL-12 to weigh; `Anonymized` to weigh for the job environment); 24 M rows need a subsample by month.
- Priority: gap 0 (technology, binary and temporal are not thin), use case + (the source names the prediction at submission for scheduling), source + (Scientific Data paper, Zenodo, feature list), shape + (millions of jobs, temporal, users), risk - (a noisy failure label, post-run columns to drop).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `cpu_act`.
- as published: about 24 million jobs run on the supercomputer Fugaku, March 2021 to April 2024, 38 monthly parquet files (about 20 GB), 45 columns listed in feature_list.csv; target: per job: exit state (completed or failed); alternatives in the same file are duration, energy or average node power, and the memory- or compute-bound class ...; access: open.
- Why: Same domain as cpu_act (performance modelling of computer systems from activity measures), but a current, decision-linked task. The features known at submission are requested cores and nodes, time limit, memory limit, priority, requested frequency, job environment, the anonymized user and a Sentence-BERT encoding of ...
- Adds: Real jobs from 2021-2024 on current hardware (millions of rows against 8,192 rows of 1990s sar data), with a time stamp for a temporal split and a user column for grouping. A subsample is needed.
