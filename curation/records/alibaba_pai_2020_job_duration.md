---
unique_name: alibaba_pai_2020_job_duration
name: 'Alibaba PAI GPU cluster trace 2020: job processing time at submission (ATLAS)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Company
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020
- https://www.usenix.org/conference/nsdi22/presentation/weng
- https://openreview.net/pdf/8ca5e492247976318731f968eb3da9085e63d867.pdf
- '# a copy of the ATLAS repository; the paper links github.com/zhiyunjiang0810/non-clairvoyant-with-predictions'
- https://github.com/gsadra/non-clairvoyant-with-predictions
- https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Alibaba's production GPU-cluster trace (July-August 2020) gives each ML job's processing time and its submit-time requests; ATLAS (ICLR 2026) defines the scheduler's prediction task on it with a temporal split, but the task table has to be built from joined tables.
- Source: Alibaba, `cluster-trace-gpu-v2020` in github.com/alibaba/clusterdata (tables as tar.gz on Alibaba OSS with SHA-256 checksums), documented in Weng et al. 2022, "MLaaS in the Wild: Workload Analysis and Scheduling in Large-Scale Heterogeneous GPU Clusters", NSDI '22. As published: "over 6,500 GPUs on about 1,800 machines", July and August 2020, timestamps offset by a constant (time of day and day of week kept); seven tables joined on `job_name`, `inst_id`, `worker_name` and `machine`: `pai_job_table` (job_name, inst_id, user, status, start_time, end_time), `pai_task_table` (task_name, inst_num, status, times, plan_cpu, plan_mem, plan_gpu, gpu_type), `pai_instance_table`, `pai_sensor_table`, `pai_group_tag_table` (user, gpu_type_spec, group, workload), `pai_machine_spec`, `pai_machine_metric`. Row counts from the run's note (job table 1,055,501, task table 1,261,050), not checked; a secondary review of ATLAS reports more than 730,000 jobs (unverified).
- Use case: ATLAS (Jiang, Zhao, Xia and Zomaya, "ATLAS: Alibaba Dataset and Benchmark for Learning-Augmented Scheduling", ICLR 2026) predicts each job's processing time at submission for a scheduler that orders the queue (learning-augmented shortest-job-first against total completion time, max-stretch and makespan). Its README defines the target as the latest task end minus the earliest task start (jobs at or below zero dropped), modelled as log(1 + p), from submit-time features only: "Instance and sensor tables are excluded to focus on non-clairvoyant scheduling", and assigned hardware and post-submission outcomes are excluded. Fit direct. Regime temporal: ATLAS splits by submission time, earliest 70% train, next 15% validation, last 15% test (SPLIT-6, SPLIT-19), with recurring jobs of a user or group inside (SPLIT-13).
- Siblings and duplicates: no record of this trace (`grep` for alibaba, clusterdata, GPU, cluster trace). `ijcai15_repeat_buyers` and `tianchi_o2o_coupon_redemption` are other Alibaba releases with unrelated tasks; `autotuning_benchmark_hub_gpu_kernel_runtime` predicts kernel runtimes, another task (PROV-7). External collections: ATLAS (its repository ships the compressed job, task and group-tag tables and notebooks).
- Better data: from the curator's Zotero collection (item 156); no further search this round.
- Papers and pages: Weng et al., NSDI '22 (the trace); Jiang et al., ICLR 2026 (the task, the feature groups: resource 9, temporal 5, signature statistics 6, causal histories 8, prior 1, categorical 4; the split).
- Metric: the ATLAS README reports RMSLE, coverage at 25% and 50% (Cov@τ) and Spearman's rank correlation side by side; the paper's PDF (OpenReview) was behind a browser check and not read, so whether RMSLE is its one ranked criterion is open. Provisionally the fallback `rmse` (MET-5, MET-8), or `rmsle` on the processing time with a log1p target if the paper ranks by it (MET-3); inputs none.
- Risks for /add-dataset: the task table is built from the job, task and group-tag tables, and ATLAS's "causal histories" and "signature statistics" summarise a user's earlier jobs, which must count only jobs finished before the submission (LEAK, SPLIT-9); failed or killed jobs: decide whether their duration is a processing time (USE-5); timestamps are shifted, so only relative time is real; the repository carries no licence file (no criterion, EV-4).
- Priority: gap 0 (technology & internet, regression and temporal are not thin), use case +, source +, shape + (hundreds of thousands of jobs, numeric requests and high-cardinality categoricals, temporal), risk - (joins and history features to build).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 156: "Scholar Inbox - Free Academic Paper Recommendations".
- as published: ML jobs on a production cluster of about 6,500 GPUs on about 1,800 machines, July-August 2020. Job table 1,055,501 rows, task table 1,261,050 rows, plus a group-tag table. The ATLAS table of ...; target: job processing time (latest task end minus earliest task start, seconds; ATLAS models log1p); access: open.
- Why: A real production trace with a fixed per-job target and submit-time features, temporal by nature (SEL-11). The trace is documented in the NSDI paper and ATLAS publishes leakage-safe feature definitions and a temporal split. Downloads are open from Alibaba OSS; the repo has no licence file.
- Adds: A new domain (cluster job runtime prediction). It is large, with high-cardinality user and group categoricals and recurring jobs, so it suits a temporal or grouped split.
