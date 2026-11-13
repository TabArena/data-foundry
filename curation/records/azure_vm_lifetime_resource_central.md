---
unique_name: azure_vm_lifetime_resource_central
name: 'Azure Public Dataset: VM traces (Resource Central)'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 5
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Company
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/Azure/AzurePublicDataset
- https://github.com/Azure/AzurePublicDataset/blob/master/AzurePublicDatasetV2.md
- https://doi.org/10.1145/3132747.3132772
v2_path: datasets/_dev/tabarena-v0pt2/azure_vm_lifetime_resource_central_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 3: Microsoft's public Azure VM trace (V2, 2019: 2,695,548 VMs over 30 days) from the Resource Central paper, which predicts at deployment each VM's lifetime, utilisation and deployment size in buckets for the VM scheduler; a named decision on a production trace, but the public table has four inputs at creation and the subscription history has to be built.
- Source: Cortez, Bonde, Muzio, Russinovich, Fontoura, Bianchini, "Resource Central: Understanding and Predicting Workloads for Improved Resource Management in Large Cloud Platforms", SOSP 2017 (doi 10.1145/3132747.3132772; read from Microsoft's PDF); traces in github.com/Azure/AzurePublicDataset (CC BY 4.0 for the data): V1 (2017, about 2M VMs) and V2 (2019). V2 (AzurePublicDatasetV2.md): "a representative subset of the first-party Azure VM workload in one geographical region", 30 consecutive days, 2,695,548 VMs, 6,687 subscriptions, 1,942,780,023 five-minute CPU readings, 235 GB in 198 files. Tables (`schema.csv`): `vmtable` (11 columns: vm, subscription and deployment ids, created and deleted timestamps, max, average and p95 CPU, `vm category`, core-count bucket, memory bucket; 438 MB gz), `subscriptions` (first VM time, VM count), `deployment` (size), and the CPU readings in 195 files. Ids are encrypted. In a 2,444-row preview of `vmtable`, the category is Unknown for 90%, Delay-insensitive 6%, Interactive 3%.
- The task's table: one row per VM, 2,695,548 rows (stated) x 4 inputs at creation (creation time, core bucket, memory bucket, deployment id) with the subscription id as a key, plus the subscription's history built from its earlier VMs ("the most important attributes in determining prediction accuracy are the percentage of VMs classified into each bucket to date in the subscription", Sec. 6.1); the target the lifetime (deleted minus created) in the paper's buckets (up to 15 min, 15-60 min, 1-24 h, over 24 h; Table 3), or the average-CPU bucket. Access: open, direct downloads from the repository's release.
- Use case: Azure's VM scheduler asks Resource Central, when a deployment arrives, for each VM's predicted lifetime and utilisation and packs servers with them ("we modify Azure's VM scheduler to leverage predictions in oversubscribing servers", abstract; the case study of Sec. 5). Fit direct for the moment and the decision, with fewer inputs: the public trace lacks the paper's service name, operating system, VM role and exact size. Regime temporal: the paper trains on two months and tests on the third (Sec. 6.1); the public trace has 30 days, so the test windows are short.
- Siblings and duplicates: `alibaba_pai_2020_job_duration` (`TBD -> Yes`, priority 3: a GPU job's duration from submit-time requests, another company and task) and `fugaku_hpc_job_failure` (`TBD -> Yes`, priority 3). V1 and V2 are versions of one source (PROV-6; V2 is larger and newer). The repository's Azure packing trace of 2020 (VM requests with priority and lifetimes) is a sibling, not read. External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the SOSP paper; Microsoft's "Virtual Machine Allocation with Lifetime Predictions" (MLSys 2023, not read) continues the lifetime task.
- Metric: the paper reports per target the accuracy and per-bucket precision and recall, with and without a no-prediction answer below a score of 0.6 (Sec. 6.1, Table 4: accuracy "between 79% (lifetime) and 90% (workload class)"), several side by side and on hard labels, so the fallback `log_loss` (MET-5, MET-6, MET-8). Inputs: none.
- Risks for /add-dataset: `vm category` comes from an FFT of the CPU series over three days (Sec. 3) and the CPU statistics are the utilisation targets, so both leave the inputs of a lifetime task (LEAK-10); deployment size and the subscription's VM count are counted over the whole trace (LEAK-10: count to date instead); VMs created at time 0 existed before the trace and VMs alive at its end are cut at 30 days (LEAK-23, LEAK-24: drop them or keep them only in a bucket they surely reach); subscriptions recur thousands of times, and their history is legitimate (LEAK-34, SPLIT-13); with four native inputs the task rests on history features we build (a TP-4 check on the subscription's bucket shares to date).
- Priority: gap + (multiclass is thin; the paper's targets are buckets), use case + (the paper names the scheduler and its decision), source + (SOSP paper and Microsoft's documented release), shape 0 (2.7M VMs over 30 days, but four native inputs), risk - (leaky category and counts, censored lifetimes, features to build).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: `subscription_vms_in_slot` dropped and the deployment's same-slot count replaced by its count of the previous 5-minute slot, LEAK-10 clause 2, since the next slot's arrivals, the part of the late count that can be measured, lower log loss by 0.013 in 8 of 9 fits while the lag costs nothing measured; a LEAK-9 protocol line and kept-on-purpose note for the chain through the cumulative counts, which lowers log loss by 0.115 to 0.203 per window for a participant who reads later test rows; `subscription_vms_created_24h` missing on day 0 in subscriptions with VMs from before the trace, CLEAN-1 and CLEAN-19; `trace_day_of_week` a number, CLEAN-14; the notes: the scheduler "can ask" (USE-1, fit direct: the paper envisions it, Barbalho et al., MLSys 2023, built it), the trace's deployment is a subscription's VMs of one day, not a request, the MET-17 group sizes and ranking, and the false horizon reason replaced); disputed: LEAK-10 clause 2 (the deployment's same-slot count: lag, drop or keep), SPLIT-12 (3-day windows as an exception, or 4 to 4.5 days); for the curator: issues 1-2. Priority 5: gap +, use case +, source +, shape +, risk 0 (gap: multiclass classification is thin among the 151 accepted definitions; use case: the paper names the scheduler and the co-location decision, fit direct; risk: the look-ahead found is lagged out, the test-row chain is covered by the protocol line, and the open window length changes no row or label).
