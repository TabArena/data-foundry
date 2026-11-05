---
unique_name: fugaku_hpc_job_failure
name: 'F-DATA: A Fugaku Workload Dataset for Job-centric Predictive Modelling in HPC Systems'
checked_by:
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
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
v2_path: datasets/_dev/tabarena-v0pt2/fugaku_hpc_job_failure_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**Current accepted status (AI, 2026-11-05):** Myunghwan accepted this definition on November 3 and explicitly requested reuse of those decisions for the updated-main cycle on November 5. The current focused recheck finds no new decision. The dated AI screening notice and early source estimates below are historical; later measured qualification and curator decisions supersede them where stated. The first-tuned-benchmark recheck remains required.

**Historical AI-screening notice (preserved verbatim):**

> **⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**


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

**Restored curation history (AI, 2026-11-05):** the following prior decisions and measured follow-through are restored from the accepted private package. They retain their original dates and attribution; the earlier screening text above remains historical. Myunghwan requested the current-main add/review/build cycle using those past decisions, with a new input only if needed. No new curator marks are invented.

CC (2026-11-02, Myunghwan): proceed to add-dataset on the reviewed original zero/nonzero exit-state target at job submission, investigating source representations first and qualifying temporal evaluation. This accepts screening for investigation, not final inclusion or build. The required precedent check found no conflict.

**Assessment (AI, 2026-11-03):** added as `fugaku_hpc_job_failure_1m` for added-dataset review; full independent/blind panel recommends ship after documentation changes and curator judgment, not final acceptance. All 38 publisher-checksummed files contain 25,866,900 execution records, 2,558,519 failed (9.891%); all labels match the original zero/nonzero exit-code rule. The native temporal-budget union has 2,500,499 rows and 388 predictors. Native check passes with zero errors/warnings; original leak-CLI normalization failure and recovered diagnostic tail are explicitly distinguished. Task-probe mean ROC AUC is 0.794 linear, 0.758 RF and 0.783 LightGBM versus 0.5. Bounded train-only tuning, date ablations and foldwise raw-user comparisons show useful ranking; they do not establish definitive tuned-family separation or calibrated operational utility. Preserve no_spread/drift_baseline follow-up at the first tuned benchmark run. Approximate fit names post-run cohort selection, nonzero-exit actionability and unresolved execution-to-parent decision identity; Selection Bias is an AI concern marker, not a new curator verdict. The no-additional-gap SPLIT-10 departure is proposed for precise live-refit completion filtering, with fast-completer selection/reporting-latency limits, pending curator judgment. Masked names remain categorical with a CLEAN-14 rationale; original labels and source representations are preserved, with combined views/time and three four-month refits disclosed as adaptations. No container build or dataset publication. Priority 3: gap 0 (no thin domain/type/regime among 163 accepted definitions), use case +1 (source-motivated submission-time risk triage, approximate), source +1 (fixed first-publisher release and defining paper), shape +1 (2.5M rows, mixed features and temporal evaluation), risk -1 (conditional cohort/action unit and gap/value judgments remain).

CC (2026-11-03, Myunghwan): added-review item1 accepted: "As far as some measurement reflects the futures, it's OK". Preserve the original future terminal zero/nonzero exit-state task and approximate execution-record fit.

CC (2026-11-03, Myunghwan): added-review item3 accepted: "Yes with the recheck". Retain with a required first-tuned-benchmark recheck of family separation, foldwise simple baselines and probability quality.

**Assessment (AI, 2026-11-03):** actual added-review answers preserved in the source-bound local review store. Independent precedent check finds no unreasoned conflict. Items1/3 applied; item2 requests maturity qualification and remains open. No overall ship field, build, commit, future-predictor permission or general rule amendment was inferred.

CC (2026-11-03, Myunghwan): added-review item2: "Training gap is not a big concern. But potential issues with matured labels need to be checked.". The no-additional-gap choice is accepted subject to factual maturity qualification, preserving the exact completed-label filter.

**Exception to SPLIT-10 (2026-11-03, Myunghwan):** no additional fixed embargo after exact recorded-completion filtering. Precise completion timestamps allow each refit to use the recorded outcomes ending before it; the requested full-source/exact-membership qualification found zero retained training outcomes at/after any cutoff. Fast-completer selection and unreleased post-completion reporting latency remain limitations; unavailable labels still leave under SPLIT-9. Serves P4: SPLIT-1 fidelity to the completed outcomes available at a live refit.

**Assessment (AI, 2026-11-03):** requested maturity qualification completed over25,866,900 source intervals and exact shipped memberships. No missing/negative intervals or unavailable training outcomes remain. Before sampling,10,387/48,375/28,118 late outcomes leave at May/Sep/Jan cutoffs. Local class selection is material (September last-day late jobs18.53% failed versus0.292% already complete); ingestion latency remains unobserved. Fixed historical LightGBM settings exactly reproduce the prior baseline; hypothetical24h reporting lag changes AUC about−0.010/window, while seven-day submission embargo changes it−0.0166/+0.0044/−0.0458 newest first. These paired200k-test diagnostics do not select a benchmark gap or complete full HPO. The scientific reason for the accepted exception remains live-refit fidelity, not favorable held-out scores. Test labels are eventual exits; all recorded source ends precede publisher release. Original target, predictors, native memberships and scorer remain unchanged. First-tuned benchmark recheck remains required, including maturity/latency sensitivity, family separation, foldwise simple baselines and probability quality.

**Review history (AI, 2026-11-03):** actual added-review items1–3 applied; their exact human notes and original source snapshot are retained. Closed issue IDs1/2/3 must not be reused; the next new issue is4. The fulfilled maturity check does not supply an independent overall ship field, build or commit authorization.

CC (2026-11-03, Myunghwan): final added-dataset verdict ship: "ship this". Accept the reviewed Fugaku definition with the previously agreed first-tuned-benchmark recheck; numbered issues1–3 and maturity follow-through are settled.

**Final added-review ship (AI, 2026-11-03):** actual verdict stored against final review snapshot86a1370cc633a537278cd750bc214b421d978f6519ac6635d34b7030a1dec54f and checked independently for consistency. The existing definition already implements all accepted choices, so no data, target, predictor, split, scorer or definition change is required. Native checksumc7436e8d… and prior successful checks remain applicable. The first tuned benchmark run must recheck family separation, foldwise simple/user-history baselines, probability quality, and maturity/reporting-lag sensitivity. Approximate fit, Selection Bias and the qualified SPLIT-10 exception remain documented. Scientific review is complete; claim/WIP remains until repository integration, and DF: Yes is set by the integration PR as required.

CC (2026-11-05, Myunghwan): the declared metric roc_auc is checked as the unchanged metric accepted within the 2026-11-03 "ship this" verdict, carried forward under the explicit request to use our past decision. This records the prior package acceptance and current reuse instruction, not a separate new metric click.

**Assessment (AI, 2026-11-05):** the updated runtime preserves every data value/order, category, target, predictor, membership array and metric specification. All six old/current ROC-AUC scorer comparisons match exactly over the shipped 500k-row test sides. Only the new empty special_features metadata field changes the framework checksum; encoding the old metadata fields on the actual current container exactly restores the accepted checksum. Original source-bound decision stores are retained unchanged; no old mark receives a new snapshot identity.

**Assessment (AI, 2026-11-05):** review panel (focused): ship with the previously accepted qualifications; disputed: none after current-rule/runtime checks; for the curator: no new issues (prior IDs1–3 remain resolved). Claim, column, split and precedent audits, mediator and cold editor completed. Updated native dtype and number-format checks find no new retained-feature defect; all source MD5/labels and exact mature-label memberships pass. Straight-line raw patterns were investigated and are not demonstrated interpolation; the generic raw CLI is inapplicable to this dictionary loader and the known native float32 neighbour diagnostic limitation remains explicit. Prior source-bound ship/metric/gap decisions are reused under the current request; no new human marks or full HPO were invented. Priority 3: gap0 (current accepted set not thin here), use case+1 (source-motivated submission-time triage, approximate), source+1 (first-publisher release/paper), shape+1 (2.5M mixed temporal rows), risk−1 (accepted cohort, reporting clock, parent unit and future value recheck).
