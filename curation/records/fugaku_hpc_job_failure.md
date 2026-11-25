---
unique_name: fugaku_hpc_job_failure
name: 'F-DATA: A Fugaku Workload Dataset for Job-centric Predictive Modelling in HPC Systems'
checked_by:
- Myunghwan
- Andrej
data_foundry_status:
- WIP (DF)
- 'DF: Yes'
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Entities: Recur'
- Dated Event Log
original_source: Other
year: '2024'
collection_period: Mar 2021 - Apr 2024
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

**Assessment (AI, 2026-11-06):** review panel (focused): retain the accepted task and decisions under the reviewed source; disputed: none; for the curator: no new issues (IDs1–3 remain resolved). Current claim/precedent audits, mediator and cold editor confirm that source9048f36a matches the actual upstream source used in the completed November5 cycle. Full data/category/membership/spec/version identity and all six scorer comparisons pass under the reviewed runtime; checksum remainsb655fe6b…. Prior actual-data/model/column/split audits are explicitly reused, not relabelled as fresh scans. Source-defined class words, predictor scope, formal SPLIT-10 exception, approximate fit/Selection Bias and the required first-tuned-benchmark recheck remain unchanged. Original source-bound human stores are preserved; no new metric/ship mark or source binding is invented. Priority 3 retained: gap0, use case+1, source+1, shape+1, risk−1, with the same measured support and accepted qualifications.

**Compatibility follow-up (AI, 2026-11-16):** The accepted 1M/500k caps remain unchanged. Current main rejects a custom `_make_splits` on a collection-budgeted `_1m` definition, and its temporal sampler now requires a budget and retains full training history. Migration, selected-vector preparation and requalification remain open before a new build. The historical review, inclusion decision and build evidence are preserved; this rebase does not grant a new scientific exception.

**Assessment (AI, 2026-11-16; compatibility repair):** Use the plain definition name `fugaku_hpc_job_failure` for the already approved custom capped temporal protocol. The `_1m` suffix now selects automatic collection sampling, which retains full training history and is incompatible with custom splits. Preserve the accepted capped-training draw explicitly, then use the current test-sampling API. This is a compatibility repair, without changing target, inputs, metric, temporal windows, label-availability filtering or intended row membership. Historical build/source identities remain preserved; fresh build and exact data/split comparisons are recorded separately when complete.

**Assessment (AI, 2026-11-16; verified compatibility build):** Built the canonical `fugaku_hpc_job_failure` definition from clean source `a6a4ac56259a656b235696d1e74d0a8c36f68f68` as format 2 UUID `01a1e3af-55a4-7df0-bd28-5009e8991055`, checksum `v2:4cfcfaad3da1a6271ad90e17ac9589a303bd8573baf5fe23acdd52e508f09f8d`. The 2,500,499 rows, every value/dtype/category and row order, target, features, metric and all ordered train/test arrays exactly match the previously accepted container. Preserve the approved fixed training draw and test caps; use eligible history after label-availability filtering, before sampling, for the temporal training-floor check. Saved reload/checksum verification and a separate check using only traced inputs both pass with zero errors or warnings. Two existing heavy checks remain skipped under the cell budget. The regenerated card records the canonical name and current build. Original build/source commits and resolved scientific decisions remain preserved. No model refit or new scientific exception is inferred; required downstream method checks and previously accepted limitations remain in force.

**Assessment (AI, 2026-11-21):** collection facts set from the split audit: one row per job with its submission time; the exit state exists at job end (median 2.2 hours after submission, 99.9% within 23.6 days, at most 283 days; measured on all 25,866,900 rows 2026-11-21); users and job names recur.

**Assessment (AI, 2026-11-21):** review panel (full re-check): ship after changes; disputed: live outcome history (USE-6 against CLEAN-6, settled by the LEAK-9 protocol cases: a note and the fit reason, not an input), the memory limit in the requested resources (CLEAN-22, CLEAN-10: added to issue 4's option B), the corrected row identity (LEAK-18, LEAK-20, MET-17: a note under resolved issue 1); for the curator: H and issues 4-5 (issue 5, the 1M training cap, decided with duolingo_spaced_repetition_recall's issue 12). The 861,254 timing-identical rows are distinct executions; the fiscal-year cut does not select on the outcome; leak probe 13 is clean, the neighbour step of the leak probe still needs its tool fix and a rerun after the issue 4 rebuild. Priority 3: gap 0 (no thin domain, type or regime), use case + (source-motivated submission-time triage, approximate), source + (fixed Zenodo release and Scientific Data paper), shape + (25.9M jobs, temporal, recurring users), risk - (selected cohort, live history outside the task, open input and cap decisions).

CC (2026-11-23, Andrej): review issue 4, change to B: "Option B: Add the fixed requests." The requested nodes (`nnumr`) and cores (`cnumr`) ship as numbers, the requested CPU frequency (`freq_req`) as a category and the memory limit (`mszl`, bytes) as a number with its "unlimited" code 2^64 set to missing and the indicator `mszl_unlimited`; the elapsed limit and priority stay out, since pjalter can change them after submission (Fujitsu job manual, section 2.5.4).

CC (2026-11-23, Andrej): the declared horizon (four months, no gap beyond the label filter, windows starting 2024-01-01, 2023-09-01 and 2023-05-01) is checked, kept as implemented (A): no source states a refit cadence, four months is the benchmark's judgment, and the three windows cover one year with each season once and the source paper's June 2023 to April 2024 holdout; training uses only jobs that ended before each window, without a fixed embargo, the recorded exception to the gap rule.

**Assessment (AI, 2026-11-23):** `dataset check` passes with 0 errors after the requests were added (2,500,499 rows, 393 features: 388 before plus `nnumr`, `cnumr`, `freq_req`, `mszl`, `mszl_unlimited`; test 500,000 and train 1,000,000 rows in each window, failed 11.4 / 14.9 / 11.9% of test rows, May-Aug 2023 / Sep-Dec 2023 / Jan-Apr 2024). `mszl` holds the "unlimited" code on 88.6% of the 25,866,900 source rows and 86.3% of the shipped rows; the other limits run from 0.63 to 30.6 GB in the source. `freq_req` is 2000 or 2200 MHz in the shipped rows (1600 on 2 source rows). The share of test rows that share all inputs with another row barely moves: 20.0 / 39.2 / 25.3% with the requests against 20.0 / 39.3 / 25.3% without. Task probes (3 windows, untuned): ROC AUC linear 0.796, random forest 0.757, LightGBM 0.792, best single column 0.729, against 0.794 / 0.758 / 0.783 before; flags `no_spread` and `drift_baseline`, as before (the first-tuned-run recheck of issue 3). Leak probes: all features 0.794, depth-2/3 trees 0.608 / 0.616, `usr` alone 0.794, the memory limit's missing indicator alone 0.585 (a request known at submission); 34.9% of test rows have an exact copy of the non-time inputs in training (16.0% with both labels), 0.0% with the submission time; the probe stopped again at its nearest-neighbour step (an infinite value in its matrix), so the later probes have no results.

CC (2026-11-24, Andrej): the definition names its split-tree leaf, `split_leaf = "L-ORDER.windows"` (windows on the time key; cross-dataset decision B: every definition names its leaf with its split decision). The question how the gap rule's list of cases labels this dataset's training without a gap (an exception, or an ordinary use) moved from the cross-dataset items to this record's review as issue 7, since it touches only this dataset.

CC (2026-11-24, Andrej): review issue 6, as implemented (A): the memory limit's "unlimited" code stays missing in `mszl` with the indicator `mszl_unlimited`; the limits that are set stay amounts in bytes.

CC (2026-11-24, Andrej): review issue 5, C ("Option C: _1m with whole training sides."), applied after the memory fixes: the dataset ships as `fugaku_hpc_job_failure_1m`, every training row kept, test windows capped at 500,000 rows. The check's warning that the newest 30 days are thin is accepted with it (13% in the stored frame from the test-window sample, 59% in the full source from the April 2024 start on 4 April).

CC (2026-11-24, Andrej): review issue 7, D: a one-day gap with the label filter ("Option D: Add a 1-day gap"), replacing the exception of 2026-11-03; the gap rule's list records the dataset as an ordinary use.

CC (2026-11-25, Andrej): the declared split (three four-month windows on the submission time, newest first from January 2024, a one-day gap with the label filter, test windows capped at 500,000 rows; leaf L-ORDER.windows) is checked, as implemented.

CC (2026-11-25, Andrej): verdict ship; nothing open in the review. The build is stale until rebuilt (a large-memory node: about 79 GB at peak).

## Review

**Outcome:** added as `fugaku_hpc_job_failure_1m`. Ship after changes: the full re-check of 2026-11-21 keeps the exit-state task, rows, target, three four-month windows and ROC AUC. Validity: every input is known at submission and no training label arrives after its cutoff; the 861,254 rows that share job ID, times and exit code are separate executions (they differ in their counters) and stay as natural repeats; the fiscal-year cut at 31 March does not select on the outcome (failure-rate ratio 1.00 over 34 months); the operator's live outcome history, worth 0.04-0.12 AUC, stays outside the task under the evaluation protocol, and the fit reason names that gap. Value: LightGBM beats the best one-column failure rate on Jan-Apr 2024 (+0.040) and Sep-Dec 2023 (+0.076) and trails it within seed noise on May-Aug 2023 (-0.008), and the recheck at the first tuned run stays. Weighed: a first-publisher release of 25.9M real jobs with real signal, against a cohort selected after the run, a nonzero exit as a proxy for failure and the live history outside the task. Quality: wording fixes that need no decision are applied to the definition. Decided 2026-11-23: the requested nodes, cores, frequency and memory limit are inputs now (issue 4, B) and the four-month windows stay (H, A); the training cap (issue 5) still needs the curator. The build 01a1e3af is stale after these changes.

**Main points:** No open decision. Not a decision: the build is stale after this round's changes.



**Horizon:**

* **Verdict:** keep four-month windows; medium confidence: no source states a refit cadence for Fugaku, and four months is a benchmark judgment.
* **Length:** four months, used as the step between refits: each window's model is fitted at its start and scores every job submitted in the next four months[^x21f1].
* **Gap:** none beyond the label filter: a refit trains only on jobs that ended before the window starts, which drops 10,387 / 48,375 / 28,118 late labels at the May / September / January cutoffs[^x21f2].
* **Time frame:**
  - The windows cover May 2023 to April 2024: the source paper's holdout (June 2023 to April 2024) plus May 2023, one year with each season once[^x21f3].
  - Training is all earlier history with a uniform 1M draw; the source's authors also trained on all earlier months[^x21f5].
  - The F-DATA paper says models are "more accurate when they are updated frequently over time with recent data" but uses one fixed split; the same authors' [online study](https://arxiv.org/abs/2308.15481) (Marconi100, another machine) refits daily on the last 30 days. The four-month cadence is ours.
  - 1-3 April 2024 are missing from the newest window (maintenance), and each fiscal year is cut on end time at 31 March, so the 25-31 March 2024 submissions are the jobs that ended by then; the same cut simulated in the 34 months without one leaves the failure rate unchanged (median ratio 1.00), so the cut does not select on the outcome, and the newest months show no rows missing near the download date. The definition's notes give the numbers; no option here changes the cut.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Four months (implemented) | Jan-Apr 2024, Sep-Dec 2023, May-Aug 2023 | 3: 2,304,010 / 2,737,058 / 3,918,654 rows, 500k each after the cap; train 91.0% / 80.3% / 65.3% before the cap | one full year, each season once; covers the source's holdout; built and verified | the cadence is ours; a model four months old at a window's end may understate a monthly refit |
  | B | One month, spread over the year | Apr 2024, Dec 2023, Aug 2023 | 3: 420,450 / 626,404 / 1,043,535 rows (420,450 / 500k / 500k after the cap); train 98.4% / 88.7% / 76.4% | a monthly refit matches the monthly release and the paper's frequent updating; still three seasons | covers 3 of 12 months; needs a rebuild and a new label-maturity check |
  | C | One day | three days, one per season | 3: about 14-30k rows each (median 21k a day); train about 99% | the authors' online setting (daily refit) | that study was on another machine; one weekday per window |
  | D | Six months | Nov 2023-Apr 2024, May-Oct 2023, Nov 2022-Apr 2023 | 3: 3,660,437 / 5,299,285 / 4,443,099 rows, 500k each after the cap; train 85.9% / 65.3% / 48.1% | two years tested | the oldest window is under half: the curator's exception[^x21f4] |
  | E | Four months, the newest season twice | Jan-Apr 2024, Sep-Dec 2023, Jan-Apr 2023 | 3: 2,304,010 / 2,737,058 / 2,833,835 rows, 500k each after the cap; train 91.0% / 80.3% / 54.3% before the cap | two years tested; the newest season tested twice, in other years as preferred[^x21f3] | leaves out summer (May-Aug 2023) and 3 of the source's 11 holdout months; custom cutoffs; rebuild |

* **Recommendation:** A: it covers the source's own holdout (June 2023 to April 2024), and we weigh following the source's split[^x21f6] above the preference for windows in other years that E serves[^x21f3]; no source gives a cadence that would favour B, which is the choice if refit fidelity weighs more than whole-year coverage. **Decision:** keep four-month windows (A), or change to B, C, D or E?

**Notes for the AI:** On B, set `_window_spec()` to `window=1`; months that are not adjacent need custom cutoffs in `_select_temporal`, since `TemporalSplits(n_windows=3)` walks back contiguously; rerun the label-maturity audit, rebuild on the curator's ask, update `task_summary.split`, `changes` and the splits comment. On E, the same custom cutoffs (test windows Jan-Apr 2024, Sep-Dec 2023, Jan-Apr 2023; the floor assert holds (54.3% after the label filter)), the same audit and text updates. On any option, the splits comment names the length, step, gap and time unit and where each comes from, the leaf (Temporal · arrival date, label-delay gap) and the count 3 against SPLIT-33's 3; keep the "Exception to SPLIT-10" wording: the gap rule asks for a gap where a selection by the outcome is measured, and it is measured here (18.53% against 0.292% failed among late-ending and completed last-day jobs).

[^x21f1]: **SPLIT-12** (Should): the horizon is a human judgment from the source (how far ahead the actor predicts, the refit cadence); the curator signs off the horizon and the test windows of every new temporal dataset.
[^x21f2]: **SPLIT-10** (Should): train only on rows whose outcome is known by the window's start, with a gap of about the label's delay; no gap only where the measurements show neither a shortcut through recent labels nor a selection by the outcome, and a departure otherwise is an exception. **SPLIT-9** (Must): no training label unknown at the prediction point.
[^x21f6]: **SPLIT-19** (Should): when the source defines the split (a paper's official periods), follow it.
[^x21f3]: **SPLIT-15** (Must for the newest window, Should for the others): prefer windows in other years, then seasons; walking back from the newest needs its reason; aim at the window count of **SPLIT-33** (here 3).
[^x21f4]: **SPLIT-14** (Must): every window trains on at least half the rows; under half is the curator's exception, down to 30%.
[^x21f5]: **SPLIT-20** (Should): the training history follows the use case and what the source's authors trained on.

**Andrej (2026-11-23, ok):** As implemented (A).

**Resolved (2026-11-23, Andrej):** keep the four-month windows (A): Jan-Apr 2024, Sep-Dec 2023 and May-Aug 2023, training only on jobs that ended before each window, no fixed embargo as the recorded exception to the gap rule. No change to the split; the splits comment now names the length and step (four months, the benchmark's refit judgment, since the source states no cadence), the gap (none beyond the label filter, from the recorded end times), the time unit (calendar months of the submission time in Japan time, as the source's monthly files), the leaf (Temporal · arrival date, label-delay gap), the count (3 windows against the target of 3) and the training history (all earlier labelled history, as the source's authors trained). `dataset check`: 0 errors, 0 warnings; 500,000 test and 1,000,000 training rows in each window.

**Issues for Myunghwan:**

1. **Accept the released-execution task with approximate operational fit?** The [source paper](https://doi.org/10.1038/s41597-025-05633-1) motivates workload management and defines “completed” as exit code zero, “failed” as nonzero; every released label matches. A nonzero return can be intentional, so it does not identify preventable failure. The [source cleaner](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/generation_scripts/clean_and_anonmyze_data.py) selects records using post-run measurements. Missing submissions cannot be counted, and eligibility is unknowable at submission. In April 2024, 89,593 of 420,450 records (21.31%) share an identifier/submission-time pair with another record; 180 such groups contain both labels. The [job manual](https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf), §1.4, distinguishes parent/subjob identifiers, but the finer mapping is absent here. These limits affect transport to all submissions and the weighting of parent-job interventions (USE-1/5/8, Must).

   **Implemented:** preserve original labels and execution records, approximate fit, record-level `Selection Bias`, an illustrative advisory action and per-record ROC AUC. No parent-level utility or submission census is claimed. **Alternative:** defer inclusion until cohort coverage, intervention identifiers and actionability are documented; deduplicating IDs or changing the failure classes is unsupported. **Decision:** accept the bounded task as recommended, or defer for that evidence. The prior Yes authorized this investigation and remains in force.

   **Myunghwan (2026-11-03, ok):** As far as some measurement reflects the futures, it's OK

   **Resolved (2026-11-03, Myunghwan):** Accepted the original eventual zero/nonzero exit-state task with approximate per-execution fit.

   **Answer (AI, 2026-11-21):** corrected row-identity facts from the full re-check; no new decision, the issue stays resolved.

   - On all 38 files, 861,254 rows in 300,062 groups share job ID, user, job name, environment, submission, start and end times, exit code and duration; none of the groups is a full copy over the 44 nonembedding fields, because every group differs in its performance and power counters. They are separate executions that ran side by side (bulk subjobs), so the notes' earlier "repeated job IDs have distinct submission/end times" was wrong and is corrected.
   - On the shipped test sides, rows that share all inputs with another row:

     | | May-Aug 2023 | Sep-Dec 2023 | Jan-Apr 2024 |
     |---|---|---|---|
     | Share of test rows | 20.2% | 39.4% | 25.4% |
     | Groups holding both labels | 198 | 942 | 499 |
     | Largest group (rows) | 1,756 | 1,884 | 476 |

   - They are kept as natural repeats, and subjobs of one submission with different exit codes are the task's own label ambiguity[^x21r1]; scores stay per row, since the scheduler places each job, and the notes now say a bulk job counts once per subjob[^x21r2].

   [^x21r1]: **LEAK-18** (Should): few features and plausible repeats are natural, keep them and say so. **LEAK-20** (Should): feature vectors that occur with both labels stay when they are genuine label ambiguity the task has.
   [^x21r2]: **MET-17** (Should): the score stays per row when each row is a decision of its own (a job a scheduler places); the notes then say how unequal the units are.

2. **Accept the proposed exception to the additional training gap?** Training excludes every record whose observed completion is at or after refit: 10,387/48,375/28,118 records at the May/September/January cutoffs. This satisfies the measured outcome boundary of SPLIT-9 (Must). SPLIT-10 (Should) also asks for a gap because the newest eligible training rows are fast completers; exact filtering does not remove that selection. Reporting latency after completion is unreleased. A seven-day embargo would discard another 0.615%/0.576%/0.892% of eligible history, newest to oldest, without establishing which operational delay it repairs.

   **Implemented:** no additional embargo; precise completion dates approximate what a live refit knows, serving SPLIT-1 deployment fidelity. This is a **proposed exception**, not an unconditional SPLIT-10 pass. Three four-month windows cover May 2023–April 2024, refitting instead of using the [paper's](https://doi.org/10.1038/s41597-025-05633-1) single fixed June 2023–April 2024 holdout; the oldest eligible history is 65.322% of source rows. Four months is a disclosed benchmark judgment under SPLIT-12/19, not a documented production cadence. **Alternative:** require an evidence-grounded embargo and requalify affected splits; do not choose a duration from favorable test scores. **Decision:** accept the proposed SPLIT-10 exception as recommended, or require an evidence-grounded gap and requalification of the affected splits.

   **Myunghwan (2026-11-03, change):** Training gap is not a big concern. But potential issues with matured labels need to be checked.

   **Resolved (2026-11-03, Myunghwan):** Requested maturity qualification completed before final ship: zero retained late training outcomes. Keep the confirmed SPLIT-10 exception and latency/fast-completer caveats.

3. **Retain provisionally pending the first tuned benchmark run?** Native linear/RF/LightGBM mean ROC AUC is 0.794/0.758/0.783 versus 0.5. Bounded train-only LightGBM tuning yields ROC AUC 0.8655/0.7775/0.7911, newest window first; the user-only model does not match the full model on every fold. This shows signal and does not establish TP-4 triviality. Two questions remain: whether tuned model families differ reliably (`no_spread`) and whether probability predictions improve on simple baselines (`drift_baseline`). Two configurations do not constitute full benchmark hyperparameter tuning. Oldest-window log loss, where lower is better, is 0.5104 versus 0.4330 for the user-only model. That comparison shows worse probability quality, not a diagnosed calibration mechanism (TP-1/3/4; EV-3/7/8).

   **Implemented:** retain ROC AUC and an explicit first-tuned-run check of family separation, foldwise simple baselines and probability quality. **Alternative:** defer value acceptance until that run exists. **Decision:** retain with the follow-up as recommended, or defer. Neither present flag establishes `Trivial` or `Too Small`.

   **Myunghwan (2026-11-03, ok):** Yes with the recheck

   **Resolved (2026-11-03, Myunghwan):** Retain with the required first-tuned-benchmark recheck; this remains a future trigger, not an unfinished add-stage gate.

   **Answer (AI, 2026-11-21):** reference baselines for the recheck, from the full re-check; no new decision, the issue stays resolved.

   - The first tuned benchmark run compares against these, per window (ROC AUC; the two history rows score every test row of the window, the others the shipped 500k test sides):

     | Baseline | May-Aug 2023 | Sep-Dec 2023 | Jan-Apr 2024 |
     |---|---|---|---|
     | Training failure rate per user (one column) | 0.794 | 0.724 | 0.838 |
     | Training failure rate per job name (one column) | 0.805 | 0.753 | 0.673 |
     | LightGBM on the shipped inputs, 3-seed mean | 0.797 | 0.829 | 0.878 |
     | Bounded-tuned LightGBM (above) | 0.791 | 0.778 | 0.866 |
     | User's last 100 finished jobs, shrunk to the static rate (uses test-window labels, outside the task) | 0.915 | 0.902 | 0.921 |
     | LightGBM on the shipped inputs + each user's and user-job name's last training label and training failure rate | 0.819 | 0.733 | 0.862 |

   - LightGBM beats the best one-column rate on 2 of 3 windows (Sep-Dec 2023 +0.076, Jan-Apr 2024 +0.040); on May-Aug 2023 it trails by 0.008, inside that window's seed spread of 0.021[^x21v1].
   - All three untuned models give worse probabilities than predicting the training failure rate for every job, the flag this recheck already carries[^x21v2] (log loss, lower is better, mean over the three windows):

     | Model | Log loss |
     |---|---|
     | Training failure rate for every job | 0.389 |
     | Linear | 0.498 |
     | Random forest | 0.396 |
     | LightGBM | 0.422 |

   - The live history row is a reference, not a model to ship: it reads labels of earlier test rows, which the evaluation protocol rules out, and the fit reason now names that gap. Built from training labels only, history adds nothing: the row above it scores below LightGBM without it.

   [^x21v1]: **TP-4** (Must): `Trivial` needs proof; when the methods beat the best single feature on most splits, their gain is real.
   [^x21v2]: **TP-3** (Must): if tuned methods spread, keep the dataset; the flags `no_spread` and `drift_baseline` are rechecked with tuned results.

4. **Add the requested resources that are fixed at submission (nodes, cores, frequency, memory limit) as inputs?**

   - **Problem:**
     - The operator in the use case sees the requested nodes, cores, frequency and memory limit at submission, and the release has them, but the definition ships none of them.
     - The stated reasons are that the elapsed limit and priority can change after submission, and that these fields lie outside the authors' input set.
     - The [Fujitsu job manual](https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf) (section 2.5.4) lets users change only the elapsed limit, resource unit, resource group and priority, and the definition already adds the submission time, which the authors did not use.
   - **Effect on the task:** without them the task is to predict from the job's identity and time only, narrower than what the stated actor knows; alone they score ROC AUC 0.63-0.68, while the measured gain inside a model is small and changes sign between windows.
   - **Experiments:**
     - One LightGBM configuration (400 trees, no tuning), 1M mature training rows, 300k test rows per window, ROC AUC:

       | Inputs | May-Aug 2023 | Sep-Dec 2023 | Jan-Apr 2024 |
       |---|---|---|---|
       | Base (user, top-5000 job names, environment, time) | 0.804 | 0.779 | 0.882 |
       | + nodes, cores, memory limit, frequency | 0.810 | 0.740 | 0.884 |
       | + those, time limit and priority | 0.799 | 0.803 | 0.867 |
       | + time limit only | 0.824 | 0.791 | 0.853 |

     - A second check, one column at a time on the full April 2024 source month (420k jobs, ROC AUC of each column alone), then LightGBM on the Jan-Apr 2024 window only (one seed, 115k training rows; the seed spread on this window is up to 0.033):

       | Column or model | ROC AUC |
       |---|---|
       | Requested nodes / cores | 0.681 |
       | Memory limit | 0.633 |
       | Time limit (stays out) | 0.566 |
       | Frequency (the lower level fails more; AUC of the reversed score) | 0.567 |
       | LightGBM, shipped inputs | 0.886 |
       | LightGBM, shipped inputs + nodes, cores, memory limit, frequency and time limit | 0.897 |
       | LightGBM, those requests + user + environment only | 0.902 |

     - Requested nodes differ from allocated nodes on 4-35% of rows per month, so the requests are not overwritten by the allocation; priority is 127 on 99.995% of rows.
     - Caveat: the requested memory limit and frequency equal the allocated values on 100% of rows in all 38 files, so their timing rests on the manual alone; whether a resource-group change resets a group default memory limit is untested, and the same holds for frequency.
     - The memory limit holds the "unlimited" sentinel (2^64) on about 89% of rows; a sentinel is an encoding question, not a reason to drop a column[^x21col3].
   - **Consistency:** inputs the actor holds at the prediction point were added elsewhere although the source's own models left them out (brazilian_ecommerce's promised date, medical_facility_operational_data, qsar_bioconcentration); they stayed out only where the actor's tool accepts nothing else (open_soil_spectral_library), which does not hold here: the source paper lists the requests among the information available at submission[^x21col1].
   - **Panel:** the column audit (2026-11-21), on all 38 files of the release (25,866,900 rows); the task gamer measured the single-column scores; the critic asked to add the memory limit and the advocate conceded.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Identity and time only (implemented) | Keep the 388 inputs | matches the authors' representation; built and verified | leaves out inputs the actor has; the stated reason covers only time limit and priority |
     | B | Add the fixed requests | Add requested nodes and cores (numeric), frequency (categorical) and the memory limit (numeric, the "unlimited" sentinel as missing with an indicator, or as its own level); time limit and priority stay out with their reasons | inputs the actor has; the manual does not list them among what can change after submission; the strongest single columns found | rebuild; no measured AUC gain in one untuned configuration; memory limit and frequency timing rests on the manual |
     | C | Keep A, correct the reason | Keep the inputs; the notes say the fixed requests are left out by choice | no rebuild | the task stays narrower than its actor; departs from the added-input cases without a fact that sets it apart |

   - **Recommendation:** B: the manual's list of what a user can change after submission leaves these fields out[^x21col2], and an input the operator holds at submission stays whatever it scores[^x21col1]; the time limit stays out because it can be shortened after submission. **Decision:** keep A, or change to B or C?

   **Notes for the AI:** On B, add `cnumr`, `nnumr`, `freq_req` and `mszl` to the columns `_write_selected` reads (`pf.iter_batches(columns=[...])`) and append them to `arrays`/`names`; `nnumr` and `cnumr` numeric, `freq_req` categorical (three levels: 2000, 2200, and 1600 on 2 rows); `mszl` numeric with the 2^64 sentinel set to missing plus an indicator column `mszl_unlimited` (or `mszl` categorical with the sentinel as its own level; ask if the curator names neither). Rewrite the "Changes from source experiments" and "Exclusions" bullets with the manual citation (section 2.5.4: pjalter changes `elapse`, `rscunit`, `rscgrp`, `priority`) and the caveat that `mszl` and `freq_req` equal their allocated values on every row; update `task_summary.known` and `changes`; rerun `dataset check` and the leak probes (with the fixed neighbour step) after the rebuild; rebuild only on the curator's ask. On C, replace the sentence "outside this source-experiment input set" with the curator's reason.

   [^x21col1]: **USE-6** (Must): anything known at the prediction point is a legitimate input; dropping it changes the task. Case: brazilian_ecommerce.
   [^x21col2]: **USE-3** (Must): name the prediction point and what is known then. Fujitsu Job Operation Software end-user manual, J2UL-2534-01ENZ0, section 2.5.4 "Changing job parameters": https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf
   [^x21col3]: **CLEAN-22** (Must): a column leaves for what it is (a leak, an identifier, a copy, the measurement that defines the label). **CLEAN-10** (Should): convert proxy missing values to missing; keep a code and say why when it means something.

   **Andrej (2026-11-23, change):** Option B: Add the fixed requests.

   **Resolved (2026-11-23, Andrej):** B, applied. `dataset.py` reads `nnumr`, `cnumr`, `freq_req` and `mszl` from the source files beside the representations: nodes and cores as numbers, the frequency as a category (2000 and 2200 MHz in the shipped rows), the memory limit in bytes as a number with the "unlimited" code 2^64 set to missing (88.6% of source rows, 86.3% of shipped rows) and the indicator `mszl_unlimited`; the elapsed limit and priority stay out. `task_summary.known` and `changes`, the inputs, "Changes from source experiments" and "Exclusions" bullets (with the manual's section 2.5.4 and the caveat that the memory limit and frequency equal their allocated values on every row) and the evaluation-unit counts are rewritten; the live-history figures are dated as measured on the identity and time inputs. `dataset check`: 0 errors, 0 warnings, 2,500,499 rows, 393 features (388 before). Task probes: linear 0.796, random forest 0.757, LightGBM 0.792 ROC AUC (0.794 / 0.758 / 0.783 before), the same flags as before; the leak probe ran up to its nearest-neighbour step, which crashed again; up to there no request column stands out (all features 0.794, the memory limit's missing indicator alone 0.585). The container is not rebuilt (the build 01a1e3af is stale).

5. **Keep the fixed 1M training draw from all history, with the embedding size as the written exception?**

   - **Problem:**
     - Since the row-budget decision of 10 November, a set over the budget keeps every training row and ships under a `_1m` name, and the benchmark draws 1M training rows, by default at random from the newest year before the window[^x21c1].
     - This definition draws its own class-proportional 1M training rows at random from all earlier history under its plain name, approved on 2026-11-03 before that decision, so the departure has no dated curator reason yet.
     - Its 384 float32 embedding columns make a whole training side large: the largest holds 23.53M rows, 36.1 GB of embeddings in memory.
   - **Background:** the house decision's study found that a random draw of all history dilutes recent data on long histories and changed the model ranking, while a random draw of the newest year never lost much; here the history before the windows runs 26 to 34 months.
   - **Effect on the task:** none on the test sides; the draw sets which training rows a model sees (a uniform 1M of all history now, recent jobs weighted more under B, every row under C).
   - **Experiments:** arithmetic only, no run:

     | | Value |
     |---|---|
     | Largest training side | 90.98% of 25,866,900 rows = 23.53M |
     | Its embedding in memory (384 float32 a row) | 36.1 GB |
     | A container with whole training sides (about 25.0M rows) | about 38.5 GB of embeddings in memory, about 20 GB on disk |
     | Today's container (2.5M rows) | 2.0 GB on disk |

   - **Unknown:** how the three draws rank models; a run of the same model on each draw would settle it.
   - **Consistency:** 18 `_1m` folders follow the house decision; duolingo_spaced_repetition_recall's issue 12 asks the same question for a set without the size fact and recommends `_1m`; the source's authors trained on all earlier months[^x21c2]; a model's input limit or runtime is never a curation reason, and container size is close to that[^x21c3].
   - **Panel:** the advocate rests on the 36.1 GB, a fact that sets this dataset apart; the critic answers that the protocol exists for size and that a uniform draw over all history dilutes recent jobs.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Fixed uniform 1M of all history (implemented) | `_make_splits` draws 1M class-proportional training rows per window at random from all earlier labelled history; plain name; the embedding size written as the dated exception | no rebuild; the authors trained on all earlier months; the container stays at 2.5M rows | departs from the house protocol; dilutes recent jobs, which the protocol's study found can change rankings; the reason is close to a storage limit |
     | B | Fixed 1M, drawn the protocol's way | Keep the plain name and the cap; draw the 1M at random from the newest year before each window, extended back until it holds 1M | follows the protocol's sampler; the container stays small | rebuild and a new label-maturity audit; still a custom draw outside `_1m`; leaves the authors' all-history training |
     | C | `_1m` with whole training sides | Rename to `fugaku_hpc_job_failure_1m`; drop the custom draw; row budget 1M train / 500k test | one rule with the 18 `_1m` sets (and duolingo); standard split code; a model may use more history | about 20 GB on disk and 36.1 GB of embeddings in memory per training side; rename and rebuild |

   - **Recommendation:** A: the embedding size is a fact the other sets over the budget lack, and drawing from all history follows what the source's authors trained on; B if the protocol's dilution evidence weighs more, C if one rule should cover this dataset and duolingo. **Decision:** keep A with the exception written, or change to B or C (decide with duolingo_spaced_repetition_recall's issue 12)?

   **Notes for the AI:** On A, add to the splits comment and as a curation bullet: "Exception to the row-budget protocol (<date>, <curator>): the definition draws 1M class-proportional training rows per window at random from all earlier labelled history and ships under its plain name, because the 384 float32 embedding coordinates make a whole training side up to 23.53M rows, 36.1 GB in memory; the source's authors also trained on all earlier months.", and a CC line in the record. On B, restrict the training draw in `_select_temporal` to rows submitted in the 12 months before each cutoff, extended back a month at a time until 1M remain; rerun the label-maturity audit; update the sampling bullet, the trailing note and the splits comment; rebuild only on the curator's ask. On C, `unique_name = "fugaku_hpc_job_failure_1m"`, rename the folder and the class, set the record's `v2_path`; `row_budget = RowBudget(train=1_000_000, test=500_000)`; drop the `TRAIN_CAP` draw so each train side keeps every earlier labelled row (the preparation then expands about 25M embeddings, so the build needs a large-memory node); rewrite `task_summary.row` and `changes`, the sampling bullet, the trailing note and the splits comment; the Outcome then opens "added as `fugaku_hpc_job_failure_1m`"; rebuild only on the curator's ask.

   [^x21c1]: Row budget (issue #70, Lennart, 2026-11-10): the test side is capped in the container; the train side keeps every row available to it; the default sampler draws a random N from the newest year before the window, extended back until it holds N.
   [^x21c2]: **SPLIT-20** (Should): decide what the train side holds from the use case; read what the source's authors trained on.
   [^x21c3]: **EV-4** (Must): a model's input limit, feature cap or runtime is never evidence in a curation decision. **CLEAN-22** (Must): columns leave for what they are.

   **Andrej (2026-11-24, change):** Option C: `_1m` with whole training sides.

   **Answer (AI, 2026-11-24):** C was implemented and does not pass `dataset check` on the largest nodes we have, so it is not applied; the definition is back to A as before, and the choice is open again.
   - What was built: `fugaku_hpc_job_failure_1m`, every training row each window can use, each test window capped at 500,000 rows. The preparation selects 24,039,864 of the 25,866,900 source rows and writes them with their embeddings (14.9 GB on disk).
   - Where it stops: the check is killed at 125.5 GB of memory on a 126 GB node, while loading and splitting that frame. The 384 embedding coordinates alone are about 37 GB in memory, and the framework copies the whole frame several times on its way through the check: Arrow to pandas, the lineage check, the dtype casts, the reordering by time.
   - A second obstacle, in the framework: a `_1m` version may not implement `_make_splits` ("`row_budget` is ignored when the class implements `_make_splits`"), and this definition needs its own splits for the label filter (only jobs that ended before the window start train). A one-line relaxation for a budget that comes from the name works, with a test; it would go in its own framework PR.
   - The same size would meet every benchmark user: loading the container takes more than 37 GB of memory.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | C, after framework work | Make the frame's path through check and build memory-lean (no full copies), relax the `_make_splits` guard for a named budget; then ship `_1m` | one rule with the 18 `_1m` sets and duolingo's B; a benchmark draws its own training rows | open-ended framework work with no assurance it fits 126 GB; a container of about 15 GB that needs more than 37 GB of memory to load |
   | b | B: own 1M draw the protocol's way | Plain name; each window's 1M training rows drawn at random from the newest year before it, extended back until it holds 1M (the protocol's default sampler, applied in the definition) | follows the protocol's sampling, which C was chosen for; builds today (2.5M rows, 2 GB) | still a fixed draw in the container; a new label-maturity audit; departs from the authors' all-history training |
   | c | A: own 1M draw from all history (as before) | Plain name, the class-proportional 1M draw from all earlier history, with the measured size as the written exception | no change; the authors trained on all earlier months | a random draw of all history dilutes recent jobs, which the protocol's study found can change rankings |

   **Recommendation:** b: it keeps what C was chosen for, the protocol's newest-year draw, within what our tools can build; the size that blocks C is a measured fact of this dataset. a only if the framework work is wanted anyway. **Decision:** a, b or c?

   Notes for the AI: the C implementation is kept outside the repository with the review's run files (definition and framework patch), ready for a. On b: in `_select_temporal` replace the all-history draw by `sample_train_positions`-style selection (newest year before each cutoff, extended back a month at a time until 1M rows remain, class-proportional), rerun the label-maturity audit and the check (Slurm), and rewrite the sampling bullet, the trailing note and the splits comment. On c: add the dated exception bullet of the Notes above, with the measured 24.0M rows and 125.5 GB.

   **Andrej (2026-11-24, discuss):** Isn't that just an inefficient implementation on our end? Can we fix this?

   **Answer (AI, 2026-11-24, later):** yes; three steps held the whole frame two or three times over, and with them fixed the `_1m` check fits. Measured with a memory trace in Slurm (24,039,864 rows x 394 columns, about 37 GB of embeddings):

     | Step | Peak before | Peak after | Fix |
     |---|---|---|---|
     | Reading the prepared frame (the definition) | 79.6 GB | 51.9 GB | Arrow frees each column once pandas holds it (`self_destruct`) |
     | Sorting by time (framework) | 78.5 GB | 44.1 GB | the preparation writes the rows in time order, and `order_rows` skips the copy when the order does not change |
     | Duplicate rows in the data summary (framework) | 101.5 GB | 51.7 GB | rows compared by a 64-bit hash built one column at a time, not by copying the candidates; the same counts as `DataFrame.duplicated` (tested) |
     | Whole `dataset check`, preparation included | killed at 125.5 GB | 65.8 GB | |

   - A fourth change is a rule of the framework, not memory: a `_1m` version may now build its own splits (this one needs them for its label filter); a budget a definition declares itself is still refused with custom splits. The framework changes go in their own draft PR.
   - Still true after the fixes: a benchmark that loads this container holds about 37 GB of embeddings, and the check needs a node with about 70 GB.

   **Resolved (2026-11-24, Andrej):** C, applied after the memory fixes (the answer above): ships as `fugaku_hpc_job_failure_1m`. `dataset.py` keeps every training row each window can use after the label filter and caps each test window at 500,000 rows, a class-proportional draw (the collection's budget; a benchmark draws its 1M training rows, by default from the newest year before the window); the preparation reads the prepared frame with Arrow's `self_destruct` and writes the rows in submission-time order; `split_leaf` unchanged. The record's `v2_path` points to the `_1m` folder. `dataset check` (Slurm, 24,039,864 rows x 394 columns, peak memory 58.9 GB): 0 errors, 1 warning, accepted with this decision: the newest 30 days hold 13% of the usual rows a day in the stored frame because only the test windows are sampled, 59% in the full source because April 2024 begins on 4 April. Framework changes that came with it (their own draft PR): the frame is not copied when already in time order, duplicate rows in the data summary are counted by row hashes, and a `_1m` version may build its own splits.

6. **Encode the memory limit's "unlimited" value as missing plus a flag, or as its own category?**

   - **Problem:**
     - Issue 4 B added the requested memory limit, whose "unlimited" code (2^64 bytes) sits on 86.3% of the shipped rows; issue 4 offered two encodings and the mark named neither.
     - The definition now writes "unlimited" as missing plus a 0/1 column `mszl_unlimited`, the first encoding the issue listed.
   - **Effect on the task:** a model sees the same information either way; the encoding changes how a method without native missing-value handling reads the column. The check passes with 0 errors and 0 warnings (393 inputs).
   - **Experiments:** the flag alone scores ROC AUC 0.585 as a single feature; untuned LightGBM moves from 0.783 to 0.792 with the four requests added.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Missing plus a flag (implemented) | `mszl` numeric in bytes, missing where unlimited; `mszl_unlimited` 0/1 | keeps the limit numeric for the 13.7% of rows that set one | one more column |
     | B | Its own category | `mszl` categorical, "unlimited" one of its levels | one column, no missing values | the numeric order of the set limits is lost |

   - **Recommendation:** A: the limits that are set are amounts, and the flag keeps the unlimited case explicit. **Decision:** keep A, or change to B?

   **Notes for the AI:** On B, make `mszl` categorical (the byte values as strings plus "unlimited"), drop `mszl_unlimited`, rerun the check in Slurm and the task probes; add a CC line either way.

   **Resolved (2026-11-24, Andrej):** A, as implemented: `mszl` stays a number in bytes, missing where the source writes "unlimited", with the 0/1 column `mszl_unlimited`. No change to the definition.

7. **Keep this dataset's training without a gap listed as an exception to the gap rule?**
   - **Problem:**
     - On fugaku the jobs that end after a refit date fail far more often than the jobs already finished (18.5% against 0.3% among the last day's jobs before the September 2023 cutoff), so training only on finished jobs leans toward the fast, mostly successful ones.
     - The gap rule allows training with no gap only where the data shows no such lean, so fugaku's setup departs from it, and PR #59 adds fugaku to the rule's list of cases as an `exception`.
     - The question is only how that list labels fugaku (an exception, or an ordinary use of the rule); fugaku's split itself was settled by Myunghwan on 2026-11-03 and does not change here.
   - **Background:**
     - What the rule says: when a label arrives some time after its row, a model refit at a window's start knows only the rows whose label has arrived, so train on those, with a gap of about the label's delay; no gap is needed only where the measurements show neither a shortcut through recent labels nor a lean toward one outcome among the newest training rows[^x24f1].
     - What fugaku does: each refit trains on every job that ended before the window starts (10,387 / 48,375 / 28,118 late jobs left out at the May / September / January cutoffs) and sets no further gap. Myunghwan accepted this as an exception once the label-maturity check found no late label left in training (fugaku's issue 2, resolved 2026-11-03).
     - Why it came up: the split tree, the step-by-step guide to choosing a split, says "a gap of about the delay, or training only on cases whose outcome is known", which reads as if the filter alone were enough; the review of 2026-11-21 first proposed to relabel the row on that wording, then withdrew it; the wording itself is the cross-dataset item "Make the split tree's label-delay wording say what the gap rule says?". The latest split rules (PR #110, on main since 2026-11-24) keep both the rule's text and the tree's "or"; the tree's person-allowed "no gap" `[ORDER.exception]` applies only where three windows need it, and this dataset holds three.
     - What other datasets did with no gap or a short one, as the rule's list of cases records them:

       | Dataset | Training side | Lean toward one outcome measured? | Listed as |
       |---|---|---|---|
       | lt_vehicle_loan_default_prediction | no gap | no: one due date per loan, every label final at release | applied |
       | melbourne_housing_market | no gap | no: the newest weeks are as complete as a later read | applied |
       | ames_housing, perth_house_prices | no gap | no: sales dated by month, longer than the delay | applied |
       | alfa_battle_2_0_task_2, lending_club, spanish_homeowners_motor_insurance_2010_2014 | no gap or a short one | the gap the delay needs would leave too little training data | exception |
       | fugaku_hpc_job_failure (PR #59) | finished jobs only, no gap | yes: 18.5% against 0.3% failed | exception |
       | meituan_food_delivery_time (PR #59) | delivered orders only, no gap | yes: the kept orders are about 2 minutes faster, with no effect on the scores | proposed exception (its horizon item) |

   - **Effect:** none on the data or the scores. The label decides whether fugaku counts toward changing the rule: when one reason has produced three exceptions, the next review proposes to amend the rule[^x24f2]; with meituan, fugaku's reason would have two.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep it as an exception (implemented) | The row in the gap rule's list stays of kind `exception`; the splits comment keeps its "Exception to" the gap rule | matches the rule as written and the measured lean; matches Myunghwan's resolution of fugaku's issue 2; counts toward an amendment if a third case follows | the row stays long |
     | B | Relabel it as applied | The row becomes kind `applied`, shortened to the decision and its evidence (no late label among 25,866,900 jobs); the splits comment says "no fixed gap" | shorter; matches the split tree's present wording | contradicts the rule's text while the rule stands; right only if the rule is amended to accept the filter alone (option C of the cross-dataset item on the split tree's label-delay wording) |
     | C | Add a 7-day gap | Each window trains on jobs submitted at least 7 days before its start and ended before it (99% of label delays are under 7 days); fugaku's row in the gap rule's list becomes an ordinary use of the rule | no exception; removes the most skewed recent jobs; costs 0.4-0.6 points of training share | the models see no outcome of the last week, which changed AUC by -0.017 / +0.004 / -0.046 in the 2026-11-03 run; a rebuild of the splits and a new check |
     | D | Add a 1-day gap | Each window trains on jobs submitted at least 1 day before its start and ended before it: the lag between building a model and applying it, which also covers 90% of the label delays | an ordinary use of the gap rule; May and January lose their lean (99% of the last day's jobs complete, the same fail rate kept as overall); costs at most 0.1 point of training share | September keeps a lean at every gap length up to 7 days (long failing jobs of late August 2023), to be documented |

   - **Recommendation:** D: one day is the deployment lag Andrej names and already removes the lean at two of three cutoffs; seven days (C) buys nothing more, since September's lean persists at every length up to 7 days. **Decision:** keep A, or change to B, C or D?

   **Notes for the AI:** On A nothing changes in the rules or the definition. On B (only together with option C of the cross-dataset item on the split tree's label-delay wording): in splits.md's Cases table set the fugaku_hpc_job_failure SPLIT-10 row's kind to `applied` and its text to "no fixed gap after exact recorded-completion filtering; no late outcome retained among 25,866,900 rows (2026-11-03, Myunghwan)"; in fugaku's `splits_comment` and the curation bullet replace "Exception to SPLIT-10 (2026-11-03, Myunghwan): no additional fixed embargo" with "No fixed embargo (SPLIT-10, as amended)"; fugaku's record keeps its Horizon notes in step.

   [^x24f1]: **SPLIT-10** (Should): "train on the rows whose outcome is known by the window's start, with a gap of about the label's delay between train and test ... No gap is needed where the collection covers what the gap guards against and the measurements show neither" a shortcut through recent labels nor a selection by the outcome at the release end; "Where the gap a case needs breaks SPLIT-14's floor, the departure is an exception" (amended 2026-11-04 and 2026-11-05, Lennart, on lt_vehicle_loan_default_prediction).
   [^x24f2]: principles.md, "Exceptions and amendments": "When the same reason has produced three exceptions, the next pass proposes an amendment."

   Moved here from the cross-dataset items (Andrej, 2026-11-24: it touches only this dataset).

   **Andrej (2026-11-24, discuss):** Why is this allowed as an exception? Wouldn't it be easy to add a gap that is reasonable for this use case?

   **Answer (AI, 2026-11-24):** it was allowed because Myunghwan accepted, on 2026-11-03, training on every job that ended before the window with no further gap, once no late label was left in training (issue 2); the lean toward fast jobs was documented, not removed. A reasonable gap is easy, measured on the full source; added as option C:

     | | Value |
     |---|---|
     | Label delay (end minus submission): median / 90% / 95% / 99% | 2.2 h / 33 h / 62 h / 167 h |
     | Training share at the May / Sep / Jan cutoffs: no gap → 7-day gap | 65.3 / 80.3 / 91.0% → 64.7 / 79.9 / 90.4% |
     | Jobs of the last day before the Sep cutoff: fail rate of those kept vs of all | 0.3% vs 9.3% |
     | Jobs of the last 7 days before the Sep cutoff: kept, fail rate kept vs all | 74.5%, 3.5% vs 5.1% |

   - A 7-day gap keeps the rule's default form (a gap of about the label's delay) and leaves each window above the training floor.
   - The score cost was measured on 2026-11-03 at fixed model settings: AUC -0.017 / +0.004 / -0.046 (newest window first) for a seven-day embargo; that is what a model deployed at a refit really lacks.

   **Notes for the AI:** On C, in `_select_temporal` keep training rows with `adt < cutoff - 7 days` and `edt < cutoff`; declare the gap (`Temporal(..., gap=7, gap_unit="days")`); rewrite the splits comment, the split-walk bullet and the exception bullet (removed); in `splits.md` the fugaku row of the gap rule's list becomes `applied`; re-run the check (Slurm, a large-memory node) and report the shares.

   **Andrej (2026-11-24, discuss):** We split on job start time and filter out jobs that don't have a result yet. That means the only gap we need is the one between starting developing the model and applying it. Seven days sounds like a bit too much,?

   **Answer (AI, 2026-11-24, evening):** agreed on the length, with one correction: the windows are cut on the submission time (`adt`), not the start time; jobs whose result is not in by a window's start (`edt`) are filtered out, as you say. Measured on the full source, the lean the filter leaves for each gap (the last day of training jobs before the gap):

     | Gap | Training share May / Sep / Jan | Last day's jobs kept, May / Sep / Jan | Fail rate kept vs all: May | Sep | Jan |
     |---|---|---|---|---|---|
     | none | 65.3 / 80.3 / 91.0% | 66 / 50 / 78% | 13.6 vs 9.0% | 0.3 vs 9.3% | 8.3 vs 8.4% |
     | 1 day | 65.3 / 80.3 / 90.9% | 99 / 48 / 99% | 3.4 vs 3.4% | 2.2 vs 6.6% | 7.6 vs 7.7% |
     | 3 days | 65.1 / 80.2 / 90.8% | 95 / 73 / 98% | 19.0 vs 18.1% | 4.9 vs 6.3% | 4.1 vs 4.1% |
     | 7 days | 64.7 / 79.9 / 90.4% | 100 / 88 / 100% | 6.3 vs 6.3% | 1.7 vs 13.1% | 10.1 vs 10.1% |

   - One day removes the lean at the May and January cutoffs; September leans at every length up to 7 days, from long-running failing jobs submitted in late August 2023, so seven days is not justified by it either.
   - Added as option D (a 1-day gap) and recommended over C.

   **Andrej (2026-11-24, change):** Option D: Add a 1-day gap.

   **Resolved (2026-11-24, Andrej):** D, applied. `_select_temporal` trains on jobs submitted at least one day before each window and ended before it; `Temporal(..., gap=1, gap_unit="days")`; the exception bullet is replaced by a gap bullet with the September limitation, the horizon text and the split walk follow, and the gap rule's list of cases records the dataset as an ordinary use (`applied`). Training shares 65.3% / 80.3% / 90.9% (May / September / January cutoffs; 27,129 / 57,968 / 45,784 jobs left out by the filter and the gap). `dataset check` (Slurm, peak memory 78.6 GB): 0 errors, 0 warnings, the thin newest period accepted as before.

**Review panel:** ship after changes (mediator, 2026-11-21, full re-check). Applied without a decision: the fit reason names the live-history gap and the fiscal-year cut; the evaluation-protocol line in the splits comment; the row-identity and evaluation-unit bullets corrected; the cohort-limit bullet (fiscal-year cut, elapsed-limit kills almost absent); the node-hours cost note; the jobenv_req switch in April 2024 and the first-appearance id numbering; the download recipe path and a typo; the row-identity facts under issue 1 and the recheck baselines under issue 3. Disputed and settled: the live outcome history is a note under the evaluation protocol, not an input (the critic's cleaning-rule reading ranks below the input and history rules; the protocol cases decide); the memory limit joins issue 4 (the advocate conceded); the corrected row identity is a note under resolved issue 1, not a new item; the "Exception to SPLIT-10" wording stays, with option E added to H. Claim audit: the row-identity sentences refuted and corrected; the download path stale. Blind review, without our notes: include with changes; main concern the missing submission-time requests (issue 4). Task gamer: no exploit beat the seed spread; the missing requests help an honest model. For the curator: H and issues 4-5; issues 1-3 stay resolved. Precedent check: consistent except the in-container training cap, which no curator decision after the row-budget rule covers (issue 5), and the missing other-year window (option E in H). Domain practitioner: would use it as advisory triage, with the live-history gap named. Earlier panels (2026-11-03, 2026-11-05/06) are kept below as dated evidence.

<details><summary>Mediator (2026-11-21)</summary>

**Mediator: fugaku_hpc_job_failure (2026-11-21)**

Read: principles.md; claim auditor, domain practitioner, precedent checker, advocate and critic openings and rebuttals;
blind review and task gamer; column audit (the column audit + evidence); the record's `## Review`
(Horizon block, issues 1-4); `dataset.py`; check.log, leak.log, task/, dtype/; the duolingo and meituan mediator
reports; USE-6, CLEAN-6, CLEAN-19, CLEAN-22, LEAK-9 (cases), LEAK-16 to LEAK-20, LEAK-34, TP-10, SPLIT-10, SPLIT-15,
MET-17, EV-4, and the row-budget protocol (`definitions.md`).

Three Slurm jobs, scripts and logs in the run folder:
`dup44.py`, `fycut.py`, and leak probe 13 run alone, `--period-only`.

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-1/5 hold (fit approximate, USE-8, issue 1 Resolved); USE-6 triggered by the fixed resource requests
  (issue 4, fix B + mszl); live outcome history: kept out by the LEAK-9 protocol (Andrej, 2026-11-09/10), the gap
  named in the fit (USE-8); LEAK-10 holds (adt <= qdt on every row; elpl and pri stay out); LEAK-16/18: the
  861,254 timing-identical rows are distinct executions (counters differ in all 300,062 groups), natural repeats,
  kept with a note; SPLIT-9 holds (0 late training labels); SPLIT-10: exception stays (2026-11-03, Myunghwan);
  SPLIT-14 holds (65.3% minimum); SPLIT-15 newest holds, option E to be offered.
Value: TP-4 holds (methods beat the best one-column rate on 2 of 3 windows by 0.04-0.08); TP-3 flags no_spread and
  drift_baseline stay with the issue 3 recheck.
Quality: doc fixes (row identity, fiscal-year cut, recipe path, typo); CLEAN-14 jnam departure kept.
Weighed: source +, size +, real signal +, cohort selected after the run -, live history missing from the task -.
For the curator: issue 4 (add the requests, now with mszl); H (windows; option E added); new item: the 1M training
  cap, decided with duolingo_spaced_repetition_recall.
```

**Decisive experiments**

**1. Are the timing-identical rows copies? (all 38 raw files, all 44 non-embedding fields)**

| Key | Rows in groups | Groups | Groups that are full 44-field copies |
|---|---|---|---|
| jid, usr, jnam, jobenv_req, adt, sdt, edt, ec, duration | 861,254 | 300,062 | **0** |
| all 44 non-embedding fields | **0** | 0 | - |

Every timing-identical group differs in its performance and power counters (`idle_time_ave`, `perf1`, `flops`,
`mbwidth`, `opint` in all 300,062 groups; `econ`, `avgpcon` in nearly all). They are separate executions that ran side
by side (bulk subjobs), not copies of one record. The README's "no exact duplicates over the 44 non-embedding fields"
holds; its "repeated job IDs have distinct submission/end times" and "38 traced pairs differ in execution timing" are
false.

**2. Does the fiscal-year cut select late-March rows on the outcome? (compact table, all rows)**
The cut was simulated in every month that has no cut: last-7-day submissions, all of them against only those that ended
before the month's end.

| | Value |
|---|---|
| Failure rate of the kept rows over all rows, median over the 34 non-March months | 1.00 (IQR 0.94-1.03) |
| Months where the cut would lower it a lot (late-ending jobs fail more) | 2021-11 0.50, 2022-09 0.48, 2023-09 0.44 |
| Months where it raises it more than 10% | 1 (2022-07, 1.21) |
| Share of last-week rows that end before the month's end, median | 93.5% |
| Late March 2024 failure rate (cut applied) | 0.423, against 0.047-0.118 in the neighbouring months |

The cut does not raise the failure rate. Late March 2024's 42% is a real event (5-9 April 2024 also fail at 31-78%,
claim auditor), not something the cut made. So the cut needs a note, not a decision item on dropping days.

**3. Leak probe 13 alone.** No single newest month is outside the band. Pooled, the newest 6 months have
*more* rows a day (z +3.5), not fewer. Failure rate in April 2024: 0.194 (z +2.9). Nothing points to censoring by the
download date. The tail is denser and fails more, which is drift and the late-March event.

**4. Training cap size (arithmetic, no run).** The largest training side holds 90.98% of 25,866,900 rows = 23.53M
rows. At 384 float32 values per row, the embedding alone is **36.1 GB in memory**, so the precedent checker's figure
holds. The container frame (all training rows plus 1.5M test rows, about 25.0M) would hold about 38.5 GB of
embeddings. On disk it would be about 20 GB, going by the prepared 2.5M-row file (2.0 GB, about 800 B a row).

**Disputes settled**

**(1) Live outcome history: USE-6 against CLEAN-6. Settled by LEAK-9 precedent: a note, not a curator item**

- **Facts (agreed):** an untrained rate over the user's last 100 finished jobs scores 0.915 / 0.902 / 0.921 AUC
  (practitioner), against 0.797-0.878 for the honest LightGBM (gamer, 3-seed means). All of the gain comes from labels
  inside the test window: the same history from training labels only adds nothing (gamer: 0.862 / 0.733 / 0.819).
- **Rank:** the critic's rebuttal ("CLEAN-6 wins") has the rank backwards. CLEAN-6 is part 7 (P7) and cannot bar an
  input that USE-6 (part 2) or LEAK-34 (part 3: an entity's history "is legitimate, also when it carries labels
  forward") makes legitimate. The advocate's first reading, that USE-6 "does not reach labels", is weakened by LEAK-34.
  CLEAN-6 therefore decides nothing here.
- **What does decide it:** the LEAK-9 cases set the evaluation protocol for this exact pattern: "each test row is
  predicted from the training rows and its own features only; no feature or model step may use other test rows".
  - spanish_motor_insurance_coverage_level_2022_2024 (Andrej, 2026-11-09) adds "no history feature built across the
    test fold".
  - loan_default_prediction_imperial_college (Andrej, 2026-11-10) applies it under a temporal split.
  - pricing_game_2016_french_fleet (CLEAN-19 exception) and the meituan mediator's protocol line point the same way.
  - The admitted label history, tunisian_fraud_detection_challenge (USE-10/LEAK-34), was built so that "a test row's
    previous label is always a training label".
  - The practitioner's feature puts earlier test labels into later test rows' features. That is what the protocol
    excludes. Neither side cited it.
- **Remedy (ladder):**
  - Keep the data.
  - Name the gap in the fit reason (USE-8, Must): the operator sees outcomes live; a model frozen for four months does
    not; untrained history is worth +0.04 to +0.12 AUC.
  - Add the LEAK-9 protocol line to `splits_comment`.
  - Put the history scores into the issue 3 recheck as a reference baseline.
  - The training-label-only form (LEAK-34) is admissible, but it measured no gain, so there is nothing to ask for.
- **Curator item or note:** a note. Both sides end at the note. Shipping in-window history would change the LEAK-9
  protocol across datasets. That is an amendment for Andrej, not a fugaku item. Flag it only if he wants to reopen the
  protocol.

**(2) `mszl` in issue 4: add it (critic right; the advocate conceded)**

- Issue 4 keeps the memory limit out because it is "the 'unlimited' sentinel on most rows". About 89% of rows hold
  2^64. CLEAN-22 (Must): a column leaves for what it is (a leak, an identifier, a copy, the label's measurement). A
  sentinel is none of these. Its encoding is CLEAN-10's job: keep the sentinel as its own level, or as missing plus
  an indicator.
- Timing: the manual's pjalter list (§2.5.4: elapse, rscunit, rscgrp, priority) does not include memory. The gamer
  measured univariate AUC 0.633 (April 2024), above `freq_req`'s 0.567, which B already adds.
- Caveat for the note: `mszl == msza` and `freq_req == freq_alloc` on 100% of rows in all 38 files (column audit
  audit.json). Their timing rests on the manual, the same as for `freq_req`. Untested: whether a resource-group change
  (`pjalter rscgrp`) resets a group default. Name this in the note. It does not separate `mszl` from `freq_req`.

**(3) Corrected row-identity facts: a note under resolved issue 1, not a new item (advocate right)**

- The critic's reason for an item was that issue 1 was decided on a refuted fact. Issue 1's own text put the
  repeat structure in front of Myunghwan: 21.31% of April 2024 rows share (jid, adt), 180 groups hold both labels, and
  deduplication is listed as unsupported.
- The decisive experiment refutes the stronger worry: no row is a copy over the 44 fields. The 861,254 timing-identical
  rows are distinct executions.
- So the rules settle it, and nothing is left for the curator:
  - LEAK-18: few features and plausible repeats are natural, so keep them and say so.
  - LEAK-20: subjobs of one submission with different exit codes are genuine label ambiguity of the task.
  - MET-17: per-row scoring stays for "a job a scheduler places".
- Remedy: correct the Row identity and Evaluation unit bullets, and add a dated fact note under issue 1:
  - 861,254 timing-identical rows in 300,062 groups, all distinct in counters;
  - 20.2 / 39.4 / 25.4% of test rows (May-Aug / Sep-Dec / Jan-Apr) sit in identical-input groups, with 198 / 942 /
    499 groups holding both labels;
  - largest group 1,756 / 1,884 / 476 rows.
- The notes also say how unequal the units are (MET-17's requirement). Issue 1 stays resolved.

**(4) 1M training cap: a curator item, decided with duolingo; lean keep, with the embedding size written as the reason**

- Consistent with the duolingo mediator: fugaku has a fact duolingo lacks. Its 384 float32 embedding coordinates make
  a whole training side 36.1 GB in memory (checked above).
- The critic is right that the AI cannot write the exception itself. The cap departs from the row-budget protocol
  (issue #70, 2026-11-10), which came after the cited approval (2026-11-03). The departure therefore needs the curator's
  dated decision.
- A factor against: EV-4 and CLEAN-22 rule out a model's input limit or runtime as an argument. Container size is a
  storage fact, close to that. The curator weighs it.
- Options:
  - a: keep the uniform class-proportional 1M of all history in the container, with the exception written.
  - b: keep a 1M cap, drawn the protocol's way (newest year, extended back). This answers #70's ranking evidence and
    needs a rebuild.
  - c: `_1m` with whole training sides (about 20 GB on disk).
- Lean: a. Choose b if Andrej weighs #70's dilution evidence above SPLIT-20's "what the authors trained on". Choose c
  if he wants one rule for both datasets.

**(5) Horizon: option E and the SPLIT-10 wording**

- **Option E (Jan-Apr 2024, Sep-Dec 2023, Jan-Apr 2023)** goes into the table.
  - SPLIT-15 (Should for older windows) prefers other years and asks a reason for walking back. Both sides agree.
  - Pro: it trains on about 54% (above the floor) and tests the newest season twice.
  - Con: it drops summer and 3 of the source's 11 holdout months, and needs custom cutoffs.
  - A stays recommended, on SPLIT-19 (it covers the paper's June 2023-April 2024 holdout). The recommendation must say
    so in words.
- **"Exception to SPLIT-10" stays.** This is settled with meituan's mediator.
  - The amended SPLIT-10 asks for a gap where a selection by the outcome is measured. Here it is measured (18.53% vs
    0.292%), so no gap is an exception, not an application.
  - Drop the Notes-for-the-AI sentence that rewords it as "No fixed embargo".
  - Footnote [^x21f2] paraphrases `split_tree.md` ("accepts that filter in place of a fixed gap"). Replace it with
    meituan's wording: "SPLIT-10: train only on rows whose outcome is known by the window's start, with a gap of about
    the label's delay; no gap only where the measurements show neither a shortcut through recent labels nor a
    selection by the outcome, and a departure otherwise is an exception."

**Leak probe crash and group.log**

- **group.log:** it is absent by design. `prep.sh` runs the group probe only for grouped datasets, and fugaku is
  temporal. Nothing is missing there.
- **What the leak probe completed:** single features, ablations, the number format, and the exact copies (0.0% across
  the split with `adt`; 38.3% without, which are recurring identities).
- **What it did not complete:**
  - The 1-NN and distance-AUC step crashed: `neighbour_space` standardisation produced inf. This is a tool bug; the
    column audit found no infinite values in the data.
  - Probe 13 and the fills step never ran. Probe 13 has now run (experiment 3: clean).
- **Rerun needed before ship?** Not before the curator's decisions. The missing 1-NN step can only add near-copy
  evidence on recurring identities, which the exact-copy step, the gamer and LEAK-34 already cover.
- **Rerun needed before the "verified" label?** Yes. Fix the probe, rerun it after the issue 4 rebuild (new columns),
  and record the result.

**Open issues in the record**

| Issue | Verdict | What, why |
|---|---|---|
| **H** | **revise** | (1) Add option E as above; A stays recommended with its SPLIT-19 reason written against SPLIT-15's other-year preference. (2) Notes for the AI: drop "the 'Exception to SPLIT-10' wording can become 'No fixed embargo'"; keep the exception. (3) Footnote [^x21f2]: meituan wording. (4) Time-frame bullet "1-3 April 2024 are missing": add the fiscal-year cut (every March file ends at 31 March; late March 2024 = 28,113 test rows, 42.2% failed, 20.0% of window 0's positives; measured not to be selected by the cut). The requested raw-metadata measurement is done (probe 13 + experiment 2): drop it from the notes. |
| **4** | **revise** | Option B adds `mszl` (sentinel as its own level or missing + indicator, CLEAN-10); remove "memory limit stays out" from B and from the Problem bullet's reasons. Add to Experiments the gamer's univariate AUCs (nnumr/cnumr 0.681, mszl 0.633, freq_req 0.567) and its one-seed gain (+0.010 / +0.016, below the 0.033 seed spread). Add the 100%-equality caveat. Recommendation stays B. Notes for the AI: add `mszl` to the columns read; rerun check and leak probes after the fix. |
| 1-3 | keep (resolved) | Issue 1: add the dated row-identity fact note (dispute 3). Issue 3: the recheck spec gains reference baselines (below). No reopening. |

Merges: none.

**New issues for the curator (each one decision)**

1. **Training cap: keep the in-container uniform 1M draw with the embedding size as the written exception, draw it the
   protocol's way, or ship `_1m` with whole training sides?** Decide with duolingo_spaced_repetition_recall's new
   issue 3. Rule: row-budget protocol (issue #70), SPLIT-20; EV-4/CLEAN-22 as the counter-factor. Lean a.
   - Advocate's best evidence: 36.1 GB of embeddings in memory for one training side; the cap is distinguishing to
     fugaku.
   - Critic's best evidence: the protocol exists for size, and a uniform draw over all history dilutes recent jobs,
     which #70 found can change rankings.

No other new item. Live history and row identity are notes (disputes 1 and 3). The fiscal-year cut is a note
(measured: no selection).

**Changes to make now (no decision needed)**

| Change | Rule |
|---|---|
| Fit reason + a note: the operator's live outcome history is not available to a model frozen per window; untrained last-100 history 0.915 / 0.902 / 0.921 against 0.797-0.878; training-label-only history adds nothing | USE-8 |
| `splits_comment`: LEAK-9 protocol line (each test row predicted from the training rows and its own features only; no feature or model step may use other test rows) | LEAK-9 (Andrej 2026-11-09/10) |
| Row identity and Evaluation unit bullets corrected (decisive experiment 1 + test-side shares); dated fact note under issue 1 | EV-1, LEAK-16/18, MET-17 |
| Cohort limit bullet and fit reason: fiscal-year cut at every 31 March; late March 2024 holds 20.0% of window 0's positives; the cut measured not to raise the failure rate (median 1.00 over 34 months) | USE-8 |
| Issue 3 recheck spec: add the per-usr / per-jnam training failure rates (0.794-0.838 / 0.673-0.805), the native models' log loss against the dummy (0.498 / 0.396 / 0.422 vs 0.389) and the history scores as reference baselines | TP-3, TP-4 |
| Note: per-row AUC weighs cheap failures like costly ones (failed share 12.6% of rows, 7.0% of node-hours; top 1% of failed jobs hold 83.5% of failed node-hours); no cost from the source, so no weighted metric | MET-7, MET-17 |
| Column-audit doc fixes: jobenv_req flip in April 2024; masked ids numbered by first appearance | EV-2 |
| `download_description`: `fugaku_hpc_job_failure_1m/dataset.py` → `fugaku_hpc_job_failure/dataset.py`; typo "union's384-value"; regenerate the README | PROV-1 |
| Leak probe: fix the inf in `neighbour_space` (tool), rerun after the issue 4 rebuild | verification checklist (P4, copies across the split) |

**Agreed facts**

- Label = nonzero exit code on all 25,866,900 rows; every input is known at submission (`adt <= qdt` on all 38
  files); 0 late training labels; train shares 91.0 / 80.3 / 65.3%; test caps 500k; `dataset check` 0 errors,
  0 warnings.
- No exploit beat the seed spread (gamer). The embedding is a deterministic function of (usr, jnam, jobenv_req).
- Methods beat the best one-column rate on 2 of 3 windows (+0.040, +0.076; -0.008 within the seed spread). TP-4 is
  not met, and the critic conceded.
- Requested nodes, cores, frequency and memory are fixed at submission per the manual. Time limit and priority are not
  (LEAK-10).
- The 861,254 timing-identical rows are distinct executions (decisive experiment 1).
- The fiscal-year cut exists and does not select on the outcome (decisive experiment 2). Probe 13 shows no download
  censoring.

**Consistency with precedent**

- History: follows LEAK-9 (spanish_motor_insurance, loan_default_prediction_imperial_college), pricing_game_2016 and
  tunisian (training labels only). Nothing departs.
- Issue 4 B: brazilian_ecommerce, medical_facility_operational_data, qsar_bioconcentration. open_soil's actor fact
  is absent.
- SPLIT-10 exception: kept as recorded. Meituan is now its second case of the same kind. The amendment count is
  unchanged, because SPLIT-10's other exceptions serve SPLIT-14.
- Duplicates: LEAK-18 natural repeats (sepsis_survival, tanzania_tourism); MET-17 per-row for scheduler jobs.
- Training cap: the same lean as the duolingo mediator (fugaku keeps the cap on the embedding-size fact; duolingo
  follows `_1m`). If Andrej wants one rule for both, fugaku moves to c.

</details>

<details><summary>Advocate (2026-11-21)</summary>

**Advocate opening: fugaku_hpc_job_failure (2026-11-21)**

Position: ship, after the fixes listed below. None of them needs a new scientific exception. One is a definition change (issue 4, B); the rest are documentation.

**1. The task is real and nobody found a leak (P3, P4: USE-1/3 Must, LEAK, SPLIT-9 Must)**

- The source paper defines this target ("completed if the exit code is 0, failed otherwise") and the task (prediction from "the information available at job submission time" on a temporal split). All 25,866,900 labels match the exit-code rule (claim audit, claim 1).
- Every input is known at submission: `adt <= qdt` on all 38 files (claim 2). The column audit agrees, and so does the blind reviewer ("I found no leak").
- The task gamer tried future same-user submissions, row order, `adt` formats, the `jnam` id order and source lookups. Nothing gained more than the seed spread: +0.001 / +0.005 / -0.005 against a spread of up to 0.033. Verdict: "I could not game this task."
- No training row ends at or after its window start (claim 8; gamer "temporal hygiene").
- `dataset check`: 0 errors, 0 warnings. The dtype probe flags 0 of 387 columns.
- Gap I must disclose: the leak probe crashed in its nearest-neighbour step (`ValueError: Input X contains infinity`, leak.log), and there is no group.log. The independent gamer attacks cover the same ground, but the probe should be rerun once the crash is fixed. It is not evidence of a leak.

**2. The value probe and TP-4 step 1 both say keep (P6: TP-4 Must, TP-2)**

- Task probe: linear 0.794, LightGBM 0.783, RF 0.758 against a dummy at 0.5. Every family beats the dummy on 100% of splits, and the probe's best single feature scores 0.729.
- TP-4 step 1 uses the best single feature chosen on each training side. The claim audit's per-category training failure rates (a target encoding, so stronger than a raw feature) are set against the gamer's honest LightGBM (3-seed means) below.

  | Window | best one-column rate | honest LightGBM | gap |
  |---|---|---|---|
  | Jan-Apr 2024 | usr 0.838 | 0.878 | +0.040 |
  | Sep-Dec 2023 | jnam 0.753 | 0.829 | +0.076 |
  | May-Aug 2023 | jnam 0.805 | 0.797 | -0.008 (within the 0.021 seed spread) |

- The methods are ahead on 2 of 3 windows, by 0.04 to 0.08. In TP-4's words, "the methods beat it on most splits: their gain is real". That leads to step 2, and the curator already ruled there: "Yes with the recheck" (issue 3, Resolved 2026-11-03).
- The rule's first step also says the natural core of a task (here "who submits it") is expected to dominate.

**3. The practitioner's outcome history is not an input we may ship. Its remedy is a note (CLEAN-6 Must outranks the USE-6 reading)**

- The practitioner's strongest objection is that the user's last 100 finished jobs score 0.90 to 0.92 and that leaving them out breaks USE-6.
- Those scores are label-based counts: failure rates over earlier rows' exit states. CLEAN-6 (Must): "Never build features from the labels (target or mean encodings, label-based counts)".
- Precedents point the same way:
  - The applied history feature, african_credit_scoring_challenge's `earlier_loans`, is "built without labels".
  - pricing_game_2016_french_fleet left a fleet's earlier record out because it "would put one test period's claims into another's features".
- Inside a four-month test window, the practitioner's feature puts earlier test labels into later test rows' features. That is the same pattern, and it turns the benchmark into online learning, a different design.
- USE-6's cases are columns of the row: a promised date, a forecast, minutes early. None is another row's outcome. The two rules do not conflict here: CLEAN-6 bounds what may be built, and USE-6 does not reach labels.
- Remedy, mildest first:
  - (a) The note the practitioner offers as the alternative: "the operator's live outcome history is excluded", with its worth (0.04 to 0.12 AUC). Add the scores to the issue 3 recheck as a reference baseline.
  - (b) If staleness is the concern, Horizon option B (monthly windows) is the in-rule remedy (SPLIT-12).
- Label-free history (counts and gaps of earlier submissions, the african_credit pattern) is admissible under CLEAN-19. The gamer's past-only order features gave +0.018 / -0.001 / -0.014, which is noise, so I do not ask for them.

**4. Issue 4: take B. It is a definition fix, not a reason to hold (USE-6 Must, remedy ladder)**

- I concede the gap. Requested nodes, cores and frequency are fixed at submission (Fujitsu manual §2.5.4) and the actor sees them. All three non-column-audit agents (blind reviewer, gamer, practitioner) raised it.
- B adds `nnumr`, `cnumr` and `freq_req`. Time limit and priority stay out: pjalter can change them after submission (LEAK-10). The precedent check finds B consistent (brazilian_ecommerce, medical_facility, qsar_bioconcentration), and the open_soil fact behind C is absent here.
- The gain is suggestive, not proven: +0.010 / +0.016 on one window with one seed (gamer), and mixed in the column audit's ablation. USE-6 does not depend on a gain.
- This is the mildest remedy on the ladder (fix the definition). It does not touch target, split or metric.

**5. Cohort selection is a documented approximate fit, and the curator has accepted it (USE-8 Must, issue 1 Resolved)**

- Three agents found the cohort limits again: the post-run cleaner, nonzero exit as a proxy, and execution records rather than parent jobs. USE-8 asks for these to be written down, not for them to be absent. They are written down, the record carries `Selection Bias`, and Myunghwan accepted this fit (issue 1, 2026-11-03).
- New fact, the fiscal-year cut at 31 March (claim audit finding 1). It is real, and the remedy is (a): name it in the Cohort limit bullet. 2024's late-March spike is partly a real event, because 5-9 April 2024 also fail at 31-78%. Rows of a real event are not an artefact to drop.
- The blind reviewer called the row selection "not uniform". That is the documented 1M-train / 500k-test cap, not label selection. The gamer measured the kit's April 2024 failure rate at 0.1939 against 0.1942 in the source.

**6. Bulk subjobs and the embedding: documentation, not data changes (SPLIT-30, MET-17 Should, CLEAN-2 Must)**

- I concede that the Row identity sentence is false: 861,254 rows are identical subjob records (claim audit claim 4). Correct it and give the shares: 20 to 39% of test rows sit in identical-input groups.
- It is not a leak. Copies never cross the split, because `adt` is a feature and train `adt` < test `adt` (gamer: "signal, not leaks"). MET-17 keeps the score per row because the scheduler places each job. Weighting by (jid, adt) belongs to resolved issue 1 and is the curator's call.
- The blind reviewer suggested PCA on the embedding. That is ours to refuse. The embedding is the source's own representation, and CLEAN-2 (Must) leaves dimension reduction to the pipeline. It also carries real signal: the blind reviewer measured AUC 0.60 to 0.78 on unseen (usr, jnam, env) combinations, against 0.5.

**7. Split, exception and cap: keep as decided, and write down the missing reasons (SPLIT-10/12/14/15/20 Should)**

- Horizon A covers the source's own holdout (June 2023 to April 2024) plus May 2023. Each window trains on at least 65.3% of the rows (SPLIT-14). SPLIT-15 accepts this reason for walking back, and the precedent check agrees. Add its option E (Jan-Apr 2023) to the table for completeness.
- SPLIT-10: the no-gap choice is a curator exception with a stated reason (Resolved 2026-11-03). Keep the "Exception to SPLIT-10" wording (precedent check finding 1, option a). The Horizon note should not relabel it.
- Training cap: write the distinguishing fact as an exception in the splits comment (precedent check finding 3, option a). That fact is the 384 float32 embedding columns, about 36 GB for a full training side. Decide duolingo the same way.
- Mechanical: fix the download recipe path to `fugaku_hpc_job_failure/dataset.py` (PROV-1) and the "union's384-value" typo.

**Changes I support**

| Change | Kind | Source |
|---|---|---|
| Issue 4 B: add nnumr, cnumr, freq_req | definition, rebuild | column audit, gamer, blind |
| Fiscal-year cut named in the Cohort limit | doc | claim audit 1, column audit |
| Row identity / Evaluation unit sentences corrected, with shares | doc | claim audit 2 |
| Note: live outcome history excluded (CLEAN-6), its worth; scores added to the issue 3 recheck | doc | practitioner 1 |
| Keep the "Exception to SPLIT-10" wording; record the cap's reason; add option E | doc | precedent 1-3 |
| Download path, typo | doc | claim audit 4, column audit |
| Rerun the leak probe after fixing the infinity crash; run the group probe | check | leak.log |

</details>

<details><summary>Advocate rebuttal (2026-11-21)</summary>

**Advocate rebuttal: fugaku_hpc_job_failure (2026-11-21)**

We agree on the outcome: ship after changes, with no exclusion. We disagree on two things. The first is whether live outcome history should be offered as an input or written down as a note (point 1). The second is whether the bulk-subjob weighting needs a new decision item (point 4).

| # | Critic's point | Answer |
|---|---|---|
| 1 | Live outcome history | Partly conceded: a decision item is fair. I dispute the recommendation |
| 2 | Requested resources, with `mszl` | Conceded, including `mszl` |
| 3 | Fiscal-year cut | Conceded |
| 4 | Row-identity facts | Correction conceded; new decision item disputed |
| 5 | One-column lookups and log loss | Conceded as recheck input; "mostly IDs" disputed |
| 6 | Split items | Agreed (my point 7) |
| 7 | Verification and recipe | Conceded |

**1. Live outcome history: partly conceded**

**I concede the rank argument.** USE-6 is a Must in part 2, so it outranks CLEAN-6, a Must in part 7. If USE-6 really covers other rows' outcomes, CLEAN-6 cannot block it. Whether it covers them is a reading of the rule. That reading is the curator's call, so a decision item is fair.

**I dispute the recommendation. Option (b), the note, should be the recommendation, and (a) the alternative.**

- **USE-6's cases.** Every applied case is a value attached to the row: a promised date, a forecast, minutes early. None of them is another row's label.
- **The label-based history precedents point to (b).**
  - The one applied history feature (african_credit `earlier_loans`) was built "without labels".
  - pricing_game_2016 kept one test period's claims out of another test period's features.
  - The critic concedes that (a) has the same property: test labels feed later test rows' features.
- **CLEAN-19's "other rows" bullet does not cover labels.** Its case, rain_in_australia, uses other stations' readings, which are features. CLEAN-6 still binds anything that is not settled under USE-6.
- **(a) changes the benchmark design.**
  - A frozen four-month model would be scored partly on label lookups computed from the test window. That is online evaluation.
  - It rests on `edt` as the label arrival time. Reporting latency is unreleased, so (a) needs a lag that nobody can measure.
- **The 0.90-0.92 scores show what history is worth. They do not show that the shipped task is wrong.** The gamer's history from the training side only hurt (0.862 / 0.733 / 0.819). So all of the gain comes from outcomes inside the test window. That is exactly the online-learning ingredient a static benchmark leaves out by design.
- **Horizon option B (monthly windows) is the in-rule way to reduce staleness.**

Proposed item: (b) recommended. (a) is the alternative and must name the cost the critic already names. Put the practitioner's scores into the issue 3 recheck either way.

**2. Issue 4, widened with the memory limit: conceded**

- CLEAN-22 (Must): a column leaves for what it is, not for its values. A sentinel value is no reason to drop the column.
- The manual's pjalter list (§2.5.4) does not include memory, so the limit is fixed at submission.
- Univariate AUC is 0.633 (task gamer).
- Add `mszl`, with "unlimited" treated as its own level or as missing under CLEAN-10. Do not ship it as a large number.
- `elpl` and priority stay out (LEAK-10). We agree on that.

**3. Fiscal-year cut: conceded**

- Name it in the Cohort limit bullet and in the fit reason.
- Run the late-March selection measurement before any item on dropping rows. Raise that item only if the measurement shows selection, since part of the spike is real (5-9 April 2024 fail at 31-78%).
- This matches my point 5 and remedy (a) of the claim auditor.

**4. Row-identity facts: correction conceded, new decision item disputed**

- I concede the correction. The README sentences are false and must give the measured shares (EV-1).
- I dispute that issue 1 "rests on" the false sentence. Issue 1's own text put the fact in front of Myunghwan: "In April 2024, 89,593 of 420,450 records (21.31%) share an identifier/submission-time pair with another record; 180 such groups contain both labels". It also listed "deduplicating IDs" among the unsupported alternatives. He accepted per-execution scoring knowing that.
- The new numbers (20-39% of test rows) are larger than the April figure, but the kind of fact is the same.
- MET-17 keeps per-row scoring for a job the scheduler places.
- Remedy: correct the sentences, and add the shares to the issue 1 note. A new item is needed only if the curator asks to reopen.

**5. One-column lookups and log loss: partly conceded**

- **Conceded:**
  - The log-loss numbers belong in the issue 3 recheck. The models score 0.498 / 0.396 / 0.422 against 0.389 for the dummy. This is the known `drift_baseline` flag.
  - Running the recheck after points 1 and 2 are decided is sensible.
- **Disputed: "mostly measures ID handling."** Against the gamer's honest LightGBM, the methods lead the best one-column rate by +0.040 and +0.076 on two windows. They trail by 0.008 on the third, which is inside the 0.021 seed spread. TP-4 step 1 reads that as a real gain.
- The embedding also adds signal where IDs cannot: AUC 0.60-0.78 on unseen (usr, jnam, env) combinations (blind reviewer).

**6. Split items: agreed**

This is the same as my point 7:

- Keep the "Exception to SPLIT-10" wording.
- Add option E to the Horizon table, with A still recommended.
- Open a decision item on the training cap, paired with duolingo. The distinguishing fact is the size of the embedding block (about 36 GB for a full training side).

**7. Verification and recipe: conceded**

- Fix the recipe path and the typo, then regenerate the README.
- Find the infinite value in the leak probe's encoding, then rerun the leak and group probes.
- Until those probes have run, the dataset is not "verified".

</details>

<details><summary>Critic (2026-11-21)</summary>

**Critic opening brief: fugaku_hpc_job_failure (2026-11-21)**

**Position:** ship only after changes. The task is real: the label is verified on all 25,866,900 rows and every
shipped input is known at submission. But the inputs leave out the two things the stated actor (operator or
admission hook) has on screen at submission, and that changes the task. Two documented facts are false, and the
probes are incomplete. Nothing here is a Must that cannot be fixed, so I ask for no exclusion.

Evidence read: the record (`## Review`, issues 1-4, Horizon block), `dataset.py`, the column audit
(the column audit), the claim auditor, domain practitioner, precedent checker, blind reviewer and
task gamer reports, and `check.log`, `leak.log`, `task.log`, `dtype.log`. There is no `group.log`.

**1. The operator's live outcome history is left out, and it beats the shipped inputs in every window (validity; USE-6 Must, CLEAN-19 Should) — NEW**

- **Problem:** at submission the operator knows how this user's and this job name's earlier jobs ended. The definition
  ships the user only as a fixed category. A model frozen at the window start cannot use any outcome from the
  following four months.
- **Evidence** (domain practitioner, all rows, no fitted model; uses only jobs with `edt < adt`):

  | ROC AUC | May-Aug 2023 | Sep-Dec 2023 | Jan-Apr 2024 |
  |---|---|---|---|
  | Tuned LightGBM on shipped inputs (record, issue 3) | 0.791 | 0.778 | 0.866 |
  | User's last 100 finished jobs | 0.901 | 0.880 | 0.891 |
  | User's last 100, shrunk to the static rate | 0.915 | 0.902 | 0.921 |

  99.8-99.9% of test jobs have such history. Log loss improves too (0.226 vs 0.293 on the oldest window).
- **Effect:** the shipped task is "predict job failure without the job history", and an untrained lookup the actor
  holds beats it by 0.04-0.12 AUC. The task gamer's history from the training side only *hurt* (0.862 / 0.733 /
  0.819), so the gain comes from outcomes inside the window, which the actor has and the frozen model lacks.
- **Rules:** USE-6 (Must): dropping an input known at the prediction point changes the task. CLEAN-19 (Should),
  bullets 3 and 4: build the history a data scientist would build, and the inputs the actor reads from other rows of
  the release, "kept only where they are known by then".
- **Remedy (mildest that works):** a new decision item for the curator.
  - (a) Add past-only history features in `_clean`: per user and per job name, the failure rate and count over the
    last N finished jobs, plus the time since the last failure. Count only rows with `edt` strictly before the row's
    `adt` (plus a lag if the curator wants a margin for reporting latency, which is unreleased), and apply the same
    rule in training and test.
  - (b) Keep the inputs, and say in the fit reason and the notes that the live history is left out and what it is
    worth.
  - Name the cost of (a): test labels feed later test rows' features. That is what the actor sees, unlike the
    entity-split case behind LEAK-9's protocol line, but it is a benchmark design choice, so the curator decides it.

**2. Requested nodes, cores, frequency and memory limit are left out (validity; USE-6 Must) — KNOWN (issue 4), with a widening**

- **Evidence:** three agents found this independently.
  - Column audit: the Fujitsu manual (section 2.5.4) lets `pjalter` change only elapse, rscunit, rscgrp and priority,
    so the other requests are fixed at submission.
  - Task gamer: univariate AUC on April 2024 (420k jobs) is 0.681 for `nnumr`/`cnumr`, 0.633 for `mszl` and 0.567
    for `freq_req`. Adding the requests gains +0.010 to +0.016 on r0 (one seed, below the seed spread).
  - Blind reviewer: jobs requesting more than 30 nodes fail at 18.7%, against 6.6% for 3-8 nodes.
- **Support for issue 4 option B, plus one change:** option B leaves out `mszl` (memory limit) because it holds the
  "unlimited" sentinel on most rows. That is not a reason under CLEAN-22 (Must): a column leaves for what it is, never
  for its values. The manual does not list memory among the fields that can change after submission, and the
  memory limit alone scores AUC 0.633. Add it, typed so that the sentinel is a level, not a number.
- Option C has no distinguishing fact: the precedent checker shows open_soil's "choice of actor" fact is absent here.
- The time limit (`elpl`) and priority stay out, because they can change after submission (LEAK-10).

**3. Every fiscal year ends in a cut, and the newest window's last week carries 20% of its positives (validity; USE-8 Must, SPLIT-10 Should) — NEW**

- **Evidence** (claim auditor, finding 1): in every March file, no job ends after March 31. In every other month,
  0.3-9.3% of jobs end after the month's end. The cause is the fiscal-year maintenance, which ran April 1-4 in 2024.
- Jobs submitted on 25-31 March 2024 are 28,113 test rows (5.6% of window 0). They fail at 42.2% and hold **20.0% of
  that window's positives**. Their cohort keeps only jobs that finished before the stop, which are short-limit jobs.
  Part of the spike is real, since 5-9 April 2024 fail at 31-78%.
- **Effect:** the README's Cohort limit bullet names only the cleaner and the start of April 2024. A selection that
  sets a fifth of the newest window's positives is undisclosed.
- **Remedy:**
  - Name the fiscal-year cut in the Cohort limit bullet and in the fit reason.
  - Measure whether late-March rows are selected on the outcome (failure rate by elapsed limit, late March vs the
    same days of the other years).
  - If they are, add a decision item on dropping those days from the test sides, like the short-last-month check
    under SPLIT-10.

**4. Two row-identity facts are false, and the resolved issue 1 rests on one of them (EV-1 Must, USE-8 Must) — NEW at this scale**

- **Evidence:**
  - The README says "Repeated job IDs have distinct submission/end times" and "all 38 traced pairs of exact projected
    duplicates differ in source execution timing". The claim auditor refutes this: 300,062 groups hold 861,254 rows
    with the same jid, every timestamp, exit code and duration (the largest group has 122 rows).
  - On the shipped test sides, 20.2 / 39.4 / 25.4% of rows have identical inputs to another row. The largest groups
    have 1,756-1,884 rows, and 198-942 groups hold both labels.
  - Leak probe: 38.3% of test rows have an exact copy of their numeric features in training, and 17.7% have copies
    with both labels. This is not a leak, because `adt` differs.
- **Effect:** scores weight a bulk job by its number of subjobs. Issue 1 was accepted on 2026-11-03 against the stated
  fact that repeats differ in timing. EV-1 puts facts before rules, so the curator should see the corrected fact.
- **Remedy:**
  - Correct the Row identity and Evaluation unit bullets with the measured shares.
  - Add one decision item: keep per-row scoring as accepted, or weight or collapse the rows that share (jid, adt) and
    the label. No exclusion.

**5. A one-column lookup comes close to or beats the tuned model, and every native model's probabilities are worse than the prior (value; TP-4 Must, TP-1 Must) — NEW numbers, KNOWN flags (issue 3)**

- **Evidence:**

  | Test side | Training failure rate per usr | per jnam | Tuned LightGBM (record) |
  |---|---|---|---|
  | May-Aug 2023 | 0.794 | **0.805** | 0.791 |
  | Sep-Dec 2023 | 0.724 | 0.753 | 0.778 |
  | Jan-Apr 2024 | 0.838 | 0.673 | 0.866 |

  In `task.log`, the dummy's log loss is 0.389, against 0.498 / 0.396 / 0.422 for the native linear, random forest
  and LightGBM. The flags are `no_spread` and `drift_baseline`.
- **Effect:** these are fitted one-column lookups, so they do not prove `Trivial` (TP-4). But the benchmark as built
  mostly measures how a method handles 3 identifiers and 384 dense coordinates of the same identifiers. Points 1 and 2
  would change that.
- **Remedy:** add these baselines and the log losses to the issue 3 recheck. Run the recheck after points 1 and 2 are
  decided, not before. No exclusion.

**6. Three split choices lack a current decision (SPLIT-15 Should, SPLIT-10 Should, row-budget protocol) — NEW (precedent checker)**

- **Training cap:** `TRAIN_CAP = 1_000_000` draws a uniform 1M of *all* history inside the container. The row-budget
  protocol (issue #70, 2026-11-10) says "N is recorded, not applied", and its sampler takes the newest year. The
  approval cited for the cap (2026-11-03) predates the protocol. Remedy: a decision item paired with
  duolingo_spaced_repetition_recall, which follows the same pattern. If the cap stays, give the reason in the splits
  comment.
- **Horizon options:** none of options A-D tests the same season in another year. SPLIT-15 prefers that. Remedy: add
  option E (Jan-Apr 2024, Sep-Dec 2023, Jan-Apr 2023), which trains on about 54% of the rows, above the floor. A can
  stay the recommendation if its reason is given.
- **"Exception to SPLIT-10":** the Horizon notes propose rewording it as "No fixed embargo". The amended SPLIT-10 sets
  a gap where a measurement shows selection by the outcome, and the record measured one: 18.53% vs 0.292%. Remedy:
  keep the exception wording, and drop that sentence from the notes.

**7. The verification is incomplete, and the rebuild recipe is broken (verification checklist; PROV-1 Must) — NEW**

- **Leak probe:** `leak.log` crashes in the nearest-neighbour step with `ValueError: Input X contains infinity`, so
  the copies-across-the-split part of the verification checklist (leak probe 5) did not complete. `group.log` does not
  exist.
- **Recipe:** `download_description` (line 144) parses `datasets/_dev/tabarena-v0pt2/fugaku_hpc_job_failure_1m/dataset.py`,
  which was removed. Run as written, it fails with FileNotFoundError.
- **Typo:** "union's384-value" (line 179).
- **Remedy:**
  - Fix the path and the typo, and regenerate the README.
  - Find the infinite value in the probe's encoding. Check whether it is `adt` or an embedding coordinate (the column
    audit found none in the embeddings). Then rerun the leak and group probes before the dataset is called verified.

**Ask, in order**

1. Decision items on points 1 (history features) and 4 (weighting by (jid, adt)), and the existing issue 4 widened
   with the memory limit.
2. The documentation fixes from points 3, 4 and 7.
3. The split items from point 6.
4. The issue 3 recheck with the baselines from point 5.

</details>

<details><summary>Critic rebuttal (2026-11-21)</summary>

**Critic rebuttal: fugaku_hpc_job_failure (2026-11-21)**

**Net:** I concede the history-features remedy and the value point. Two disputes remain: the memory limit, and who
decides the training cap. One item stays open for the curator: issue 1 was resolved on a fact that is now refuted.

| Advocate point | Response | Why |
|---|---|---|
| 1. Real task, no leak found; probe rerun needed | **Concede** | We agree. The leak probe crashed (infinity) and the group probe is missing, so both must be rerun before the dataset is called verified. |
| 2. Value: methods beat the one-column rates on 2 of 3 windows | **Concede** | The gamer's 3-seed means are the better comparison than the record's tuned run. TP-4 is not met, and issue 3's recheck covers the rest. My point 5 shrinks to adding the per-usr and per-jnam rates and the log losses (all three native models are worse than the dummy, 0.389) to that recheck. |
| 3. Outcome history is barred by CLEAN-6 | **Concede the remedy, keep the gap** | See below. |
| 4. Issue 4 B | **Concede B; dispute leaving out `mszl`** | See below. |
| 5. Cohort documented; fiscal-year cut is doc only; the late-March spike is partly real | **Mostly concede** | A real event is not an artefact. I drop "drop those days" as a remedy unless a measurement shows the cut selects on the outcome. Naming the cut in the Cohort limit bullet and the fit reason is the fix. One addition: the note should say that late-March rows hold 20.0% of window 0's positives, so a reader knows one week drives that window's score. |
| 6. Bulk subjobs: correct the text; weighting is the curator's call | **Concede the no-leak point; one item stays** | See below. |
| 7. Split: keep A, add E, keep the exception wording, record the cap's reason | **Concede A, E and the exception wording; dispute the cap** | See below. |

**Point 3: CLEAN-6 wins over my remedy (a)**

- CLEAN-6 (Must) names "label-based counts". A user's failure rate over earlier jobs is exactly that.
- The pricing_game_2016 precedent (CLEAN-19 exceptions) also refuses to carry one test period's labels into another's
  features. I withdraw remedy (a).
- The only label-lag exception I know is TP-10's last observation (rain_in_australia), and it is narrow. Its analogue
  here, the user's last finished job, scores 0.775 / 0.782 / 0.805 and does not beat the shipped model. So it is not
  worth asking for.
- What I keep is a USE-8 (Must) point, not a feature request. The fit reason must name the gap: the operator has the
  live outcome history, and it is worth 0.04-0.12 AUC over the shipped model. The issue 3 recheck should carry the
  practitioner's history scores as a reference baseline. This is the advocate's remedy (a), so we agree.
- Horizon option B (monthly windows) is a fair in-rule remedy for staleness. It is already in the Horizon table.

**Point 4: add the memory limit**

- The advocate's B adds only `nnumr`, `cnumr` and `freq_req`.
- `mszl` passes the same timing test: the manual (section 2.5.4) lets `pjalter` change only elapse, rscunit, rscgrp
  and priority. Its only stated reason for staying out is that most rows hold the "unlimited" value.
- CLEAN-22 (Must): a column leaves for what it is, not for its values. The gamer measured AUC 0.633 for it alone on
  April 2024, above `freq_req`'s 0.567, which B adds.
- Remedy: add `mszl` to B, with the "unlimited" value as its own level or as missing.

**Point 6: the curator should see the corrected fact**

- Issue 1 was accepted on 2026-11-03 with the statement that repeated records "differ in source execution timing".
  That is refuted: 861,254 rows are identical in jid, every timestamp, exit code and duration.
- EV-1 (Must) puts facts before rules. Correcting the sentence is not enough, because the curator decided on the old
  one.
- Remedy: one short item that gives the corrected shares (20-39% of test rows sit in identical-input groups) and asks
  whether per-row scoring still stands. Recommend keeping it (MET-17). The curator, not the panel, closes it.

**Point 7: the training cap needs a curator decision, not an AI-written exception**

- The 36 GB figure is the precedent checker's estimate. Nobody measured it, so EV-1 applies.
- The row-budget protocol exists to handle size: it keeps the training side whole and records N. A size reason is
  therefore an argument against the protocol itself.
- The cap also changes what the training side holds: a uniform draw over all history rather than the protocol's
  newest year. Issue #70 found that this choice can change rankings.
- Remedy: a decision item, paired with duolingo_spaced_repetition_recall. The options are the precedent checker's
  a / b / c, each with its measured size. If the curator keeps the cap, the exception is written with the curator's
  reason.

**Remaining asks**

1. Issue 4 B plus `mszl`.
2. Text fixes:
   - the fiscal-year cut, with the 20% share;
   - the row-identity sentences;
   - the fit reason naming the live-history gap and its worth;
   - the download path and the typo.
3. Curator items:
   - per-row scoring on the corrected row-identity fact;
   - the training cap, paired with duolingo;
   - option E added to the Horizon table.
4. Rerun the leak and group probes.
5. The issue 3 recheck with the one-column rates, the log losses and the history scores as reference baselines.

No exclusion.

</details>

<details><summary>Claim audit (2026-11-21)</summary>

**Claim audit: fugaku_hpc_job_failure (fugaku), 2026-11-21**

Data: all 25,866,900 rows from the column audit's compact table (the run folder, 27 source columns; no embeddings). I rebuilt the shipped membership by running the definition's own `_select_temporal` on the full metadata, so it was not sampled. It reproduces every count in the record. Scripts and logs: the run folder (audit1.py, audit2.py). Audit1 crashed after its descriptive part; audit2 redid the membership part. No `check.log`, leak, task, dtype or group probe output exists in the run folder, and there is no `findings/fugaku.md` yet. I did not use them.

**Claims table**

| # | Claim (where) | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 1 | 25,866,900 records, 2,558,519 failed (9.891%); every label is ec==0 vs nonzero (curation_comments: Target) | full pass | holds | 2,558,519 failed (0.098911); 0 mismatches with `ec != 0` | MET-3 |
| 2 | Prediction point is submission, before queue insertion (Prediction point) | adt <= qdt on every file | holds | min share over 38 files = 1.0 | USE-3 |
| 3 | Submission months are disjoint across files (Row identity) | adt month = file month | holds | share = 1.0 in all 38 files | - |
| 4 | "Repeated job IDs have distinct submission/end times" (Row identity); "all 38 traced pairs of exact projected duplicates differ in source execution timing" (Evaluation unit) | group rows on (jid, usr, jnam, jobenv_req, adt, sdt, edt, ec, duration) | **refuted** | 300,062 groups hold 861,254 rows with identical jid, all timestamps, exit code and duration (largest group 122). (jid, adt) is shared by 5,970,638 rows (23.1%); 9,661 of those groups mix both labels | USE-8, EV-1 |
| 5 | No exact duplicates over the 44 non-embedding fields within a month (Row identity) | duplicates on the 17 available fields | untested | 552,536 rows duplicate on the 17 fields I have. The other 27 (counters, energy) are not in the compact table, so this cannot refute the claim | - |
| 6 | jid is a nonunique identifier (Exclusions) | count | holds | 18,814,817 distinct jid for 25,866,900 rows | - |
| 7 | The embedding encodes the original usr/jnam/jobenv_req strings, without outcomes (Inputs) | author code `generate_derived_features.py`; per-triple spread | holds | it encodes `usr_or, jnam_or, jobenv_req_or` joined by commas; within-triple spread is about 2e-7 (float noise; column audit's embdiff) | LEAK |
| 8 | Late labels removed at the cutoffs: 10,387 / 48,375 / 28,118 (May / Sep / Jan) (Maturity, splits_comment) | recompute | holds | 10,387 / 48,375 / 28,118 exactly; shipped train edt max is before each cutoff | SPLIT-9 |
| 9 | Late-ending last-day jobs fail at 18.53% vs 0.292% before September (Maturity) | Aug 31, 2023 submissions | holds | 18.53% (n = 9,428) vs 0.292% | SPLIT-10 |
| 10 | Train share before the cap 91.0 / 80.3 / 65.3%; at least 50% before the oldest window (Horizon, splits_comment) | recompute | holds | 90.98 / 80.32 / 65.32% after the maturity filter (91.09 / 80.51 / 65.36% before it) | SPLIT-14 |
| 11 | Test windows of 2,304,010 / 2,737,058 / 3,918,654 rows, 500k each after the cap; 1M train each (Horizon, README) | rebuild membership | holds | exact; 2,500,499 selected rows; test failed 59,253 / 74,610 / 57,135 (11.85 / 14.92 / 11.43%), newest first | SPLIT-33 |
| 12 | Users seen before: 74.1 / 95.1 / 98.0% (record: blind reviewer) | shipped sides | holds | 74.12 / 95.08 / 97.98% (oldest first) | USE-10 |
| 13 | April 2024 starts April 4; ends run through May 14 (Cohort limit, Horizon) | full pass | holds | first adt 2024-04-04 15:06; edt max 2024-05-14 02:38. Fugaku maintenance ran 1 Apr 00:00 to 4 Apr 16:00 JST ([RIKEN system report 2024-04](https://www.r-ccs.riken.jp/fugaku/docs/workshop/2024/systemreport/systemreport_202404.pdf)) | - |
| 14 | Test labels are eventual exit states; the only cohort limits are the cleaner's post-run filter and April 2024 (Cohort limit, Maturity) | share of each month's jobs ending after the month's end | **refuted (incomplete)** | see finding 1: every March file is cut at March 31 | USE-8, SPLIT-10 |
| 15 | Collection facts: delay median 2.2 h, 99.9% within 23.6 days, maximum 283 days (Assessment 2026-11-21) | quantiles | holds | 0.0908 d (2.18 h), 23.56 d, 283.3 d | - |
| 16 | The source cleaner requires post-run measurements; authors evaluate representations separately; their holdout is 23_06 to 24_04 (Changes, Cohort limit, splits_comment) | read the pinned author code and paper | holds | cleaner drops rows missing perf1-6, econ and the like; `features` loop fits each representation alone; `test_yms` = 23_06 to 24_04; the paper says "more accurate when they are updated frequently over time with recent data" | - |
| 17 | Requested elapsed limit and priority can change after submission (Changes) | manual, as quoted by the column audit | holds | pjalter changes elapse, rscunit, rscgrp and priority (§2.5.4). Issue 4 (KNOWN) covers the other requests | USE-6 |
| 18 | The download recipe recreates the raw inputs (download_description, README Rebuild) | read the path | **refuted** | the recipe parses `datasets/_dev/tabarena-v0pt2/fugaku_hpc_job_failure_1m/dataset.py`, which no longer exists after the rename. Run as written, it fails with FileNotFoundError | PROV-1 |
| 19 | Native linear/RF/LightGBM 0.794 / 0.758 / 0.783; tuned 0.8655 / 0.7775 / 0.7911; the user-only model does not match the full model on every fold (issue 3, Value follow-up) | per-category training failure rate (usr, jnam, usr+jnam) scored on the shipped test sides | holds literally; weaker than it reads | see finding 3 | TP-4 |
| 20 | Metric: the paper reports accuracy with no threshold or cost; the pinned baseline calls classification_report; fallback is roc_auc (metric reason) | paper (PMC12311113), baseline_experiments.py | holds | the paper defines accuracy as the share classified correctly and fixes no threshold or cost; the baseline's `metric` is `classification_report` | MET-1, MET-5/6/8 |
| 21 | Metric computable on our folds (MET-2) | count positives per test fold; constant-prediction AUC | holds | 57k-75k positives per test fold; constant prediction gives 0.5 on every fold; no scoring column needed | MET-2 |
| 22 | No row is a copy across the split (implied) | adt is a feature and train adt < test adt | holds by construction | the bundle duplicate check was skipped (`dataset_duplicates_skipped`). Within-side copies are large (finding 2) | SPLIT-30 |
| 23 | accepted_check_warnings = {} | README bundle_checks | holds | 0 errors, 0 warnings, 2 infos (heavy checks skipped) | - |

**Findings, ranked**

**1. NEW: every fiscal year ends in a cut; jobs still running at March 31 are missing (validity, USE-8 / SPLIT-10, Weigh)**

| March file | jobs ending after Mar 31 | last 2 days: share crossing month end | last 3 days: share with time limit past the cut | last 2 days: share failed |
|---|---|---|---|---|
| 2021 | 0 | 0% | 5.1% | 12.3% |
| 2022 | 0 | 0% | 0.0% | 9.3% |
| 2023 | 0 | 0% | 0.0% | 4.8% |
| 2024 | 0 | 0% | 0.6% | **44.7%** |
| other 34 months | 0.3-9.3% of the month | 2.6-64% | Feb 2022 / 2023 / 2024: 11.7 / 1.1 / 11.7% | - |

- Each March file's last end time falls minutes after its last submission. The pattern fits the fiscal-year maintenance: in 2024 it ran from April 1 00:00 to April 4 16:00, and no April file starts on April 1.
- March-submitted jobs that would run past March 31 are absent: deleted at the stop, or held and run in April. The April files hold only April submissions, so held jobs would be missing either way.
- In the newest test window this matters: 28,113 test rows (5.6%) come from 25-31 March 2024. They fail at 42.2% and hold **20.0% of that window's positives**. Their cohort keeps only short-limit jobs.
- The 2024 spike is not explained by the cut alone. Late March 2022 and 2023 do not show it, and 5-9 April 2024 also fail at 31-78%, so part of it is a real event.
- Remedy, mildest first:
  - (a) Name the fiscal-year cut in the Cohort limit bullet and in fit_reason. Note that late-March rows are a short-limit cohort and that their failure rate carries 20% of window 0's positives.
  - (b) For the curator: drop the submissions of the last days before a fiscal-year stop from the test sides, like the ames_housing short-last-month check under SPLIT-10. Measure first whether their class mix is selected.

**2. NEW (scale) / KNOWN (concept, issue 1 resolved): row-identity sentences are false, and identical-input groups dominate the test sides (USE-8, EV-1)**

- The Row identity sentence "Repeated job IDs have distinct submission/end times" is wrong: 861,254 rows share jid, every timestamp, exit code and duration with another row. These are bulk or step subjobs.
- On the shipped test sides, rows whose usr, jnam, jobenv_req and adt are identical to another row (the embedding follows the triple) make up:

  | | Jan-Apr 2024 | Sep-Dec 2023 | May-Aug 2023 |
  |---|---|---|---|
  | Share of test rows | 25.4% | 39.4% | 20.2% |
  | Largest group (rows) | 476 | 1,884 | 1,756 |
  | Groups with both labels | 499 | 942 | 198 |

- Train sides hold about 190-205k such rows.
- Not a leak: the copies never cross the split, because adt is a feature. But scores weight a bulk job by its subjob count.
- Remedy: correct the two sentences (Row identity, Evaluation unit) and give the measured shares. Whether to weight or group by (jid, adt) is a curator question tied to the resolved issue 1, so raise it as a new item only if the curator wants it.

**3. NEW numbers / KNOWN flag (issue 3): one-column history lookups come close to, or beat, the tuned model (value, TP-4 step 1, adjacent)**

| Shipped test side | Training failure rate per usr | per jnam | per usr+jnam | Tuned LightGBM (record) | Native mean, linear / RF / LGBM (record) |
|---|---|---|---|---|---|
| Jan-Apr 2024 | 0.838 | 0.673 | 0.692 | 0.8655 | 0.794 / 0.758 / 0.783 (mean over the three windows) |
| Sep-Dec 2023 | 0.724 | 0.753 | 0.652 | 0.7775 | (same) |
| May-Aug 2023 | 0.794 | **0.805** | 0.800 | 0.7911 | (same) |

- On the oldest window, an untuned per-job-name (or per-user) training failure rate beats the bounded-tuned LightGBM. On the other two it is within 0.03-0.05.
- These are one-feature fits on the training side, not unfitted rules, so they do not prove `Trivial`. They are the foldwise simple baseline the first tuned benchmark must beat.
- Remedy: add these three numbers to the recheck item. No change now.

**4. NEW: the download recipe points to the old `_1m` path (PROV-1, mechanical)**

- `download_description` (and so the README Rebuild block) reads `fugaku_hpc_job_failure_1m/dataset.py`. Change it to `fugaku_hpc_job_failure/dataset.py`. No rebuild is needed beyond regenerating the README.

**Untested**

- The claim of no exact duplicates over the 44 non-embedding fields: the counter columns are not in the compact table. It needs a pass over the raw Parquets.
- "359,636 masked job names in the selected union": not recounted.
- Issue 4's ablation numbers: KNOWN from this round's column audit; not re-run.

Sources: [F-DATA paper (PMC12311113)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12311113/), [RIKEN Fugaku system report 2024-04](https://www.r-ccs.riken.jp/fugaku/docs/workshop/2024/systemreport/systemreport_202404.pdf)

</details>

<details><summary>Domain practitioner (2026-11-21)</summary>

**Domain practitioner: fugaku_hpc_job_failure (2026-11-21)**

**Actor:** a Fugaku operator, or the scheduler's admission hook. It scores each job when the job is submitted and flags the risky ones for a check or a note to the user.

**Fit: approximate.** The fit stays approximate, and the reasons already recorded still hold: the released cohort was selected after the run, a nonzero exit is a proxy for failure, and execution records do not map cleanly to parent jobs. The biggest new gap is in the inputs. At submission I always know how this user's and this job name's earlier jobs ended. The shipped task leaves that out, and that history alone beats the shipped inputs in every window.

**Metric scores my decision: partly.** ROC AUC ranks one decision per job correctly (MET-8; MET-17 keeps the score per row for "a job a scheduler places"). What it ignores is the cost: failures are mostly short, small jobs, while the node-hours I want to save sit in a few large ones.

**What I tested**

I ran one CPU job on the column audit's compact copy of all 38 release files (25,866,900 rows). The test period is the three shipped windows (May 2023 to April 2024, 8,959,722 rows). I fitted no model. Script and output:
the run folder, `practitioner.json` and the job log.

The check, dataset-check and probe logs (check.log, leak/, task/, dtype/, group.log) were not in the run folder when I looked; only `precedent/` existed. There is also no `findings/fugaku.md` in the column-audit folder. I used the record's issue 4 and the column-audit folder's own files instead.

**Findings**

**1. NEW: the operator's strongest input, the recent outcomes of the same user and job name, is left out (USE-6 Must, USE-3 Must)**

When a job arrives, I can see how this user's earlier jobs ended. I only count jobs whose end time is strictly before this job's submission time. The shipped model gets the user only as a fixed category, fitted on labels that were available at the last refit. For the rest of the four-month window it cannot use any newer outcome, even though the operator sees those outcomes live.

Below are untrained scores built only from jobs that ended before each job's submission. "Static" is the user's smoothed failure rate on labels available at refit, which is roughly what a model trained on the shipped user category can learn. "Tuned LightGBM" is the record's bounded train-only tuning on the shipped inputs (issue 3).

| ROC AUC | May-Aug 2023 | Sep-Dec 2023 | Jan-Apr 2024 |
|---|---|---|---|
| Static user rate at refit | 0.792 | 0.731 | 0.859 |
| Tuned LightGBM on shipped inputs (record) | 0.791 | 0.778 | 0.866 |
| User's last finished job | 0.775 | 0.782 | 0.805 |
| User's last 10 finished jobs | 0.855 | 0.857 | 0.862 |
| User's last 100 finished jobs | 0.901 | 0.880 | 0.891 |
| Job name's last 100 finished jobs | 0.912 | 0.882 | 0.916 |
| User's last 100, shrunk to the static rate | **0.915** | **0.902** | **0.921** |
| Log loss: static / shrunk last 100 | 0.293 / 0.226 | 0.418 / 0.296 | 0.237 / 0.201 |

- Nearly every test job has history: 99.8 to 99.9% have a finished earlier job by the same user, and 78 to 85% have one with the same job name.
- These scores need no model and use nothing a live operator lacks. Without fitting anything, history gains 0.04 to 0.12 AUC over the tuned model. The shipped task is therefore "predict without the operator's job history". USE-6 says that dropping an input known at the prediction point changes the task.
- The gap is largest in Sep-Dec 2023, where the static rate scores only 0.731. That is drift within the window, which a model frozen at the refit cannot follow.
- **What an expert would change:** add rolling history features computed in `_clean`, using only rows that ended strictly before each row's submission time (`edt < adt`). For example: the user's failure rate and count over their last N finished jobs, the same for the job name, and the time since the user's last failure. In training rows they must use the same `edt < adt` rule, never the refit cutoff, or train and test features differ.
- **Open points:**
  - End time stands in for when the label arrives. The 24-hour reporting-lag check in the record should be repeated for these features.
  - The masked job name is a global code. Generic names shared across users may blur it, so user plus job name may work better.
  - I have not checked whether a rule such as the minimal-preprocessing guidance limits feature engineering across rows. This is a decision for the curator, not a fix.
- **Alternative:** keep the task as it is, but say in the notes that the operator's live outcome history is excluded and how much it is worth. The fit reason would name that gap.

**2. NEW: "failed" is mostly generic exit code 1 and quick crashes, not timeouts (USE-5, information only)**

| In the failed class, test period | Value |
|---|---|
| Exit code 1 | 89.4% |
| Exit codes 16 / 4 / 127 / 255 / 2 | 2.5% / 2.2% / 1.5% / 1.2% / 0.9% |
| Ran to within 60 s of the elapsed limit (timeout) | 0.13% (completed jobs: 0.27%) |
| Ran under 60 s | 32.9% (completed jobs: 11.4%) |

- Timeouts do not make up the failed class. Most failures are script or application errors, a third of them within the first minute.
- For me as the operator, this supports the target: these are the jobs a pre-submission check (bad path, missing module, wrong input file) catches. It adds weight to the recorded "nonzero exit is a proxy" caveat, but it does not dispute it.
- Exit code 127 means "command not found" and 126 "not executable". At least 1.8% of failures are configuration errors in the strict sense.
- I tested `deldt` and cannot use it: it reads as set on 100% of rows in the compact copy, against 0.07 to 1.1% in the column audit's `audit.json`. My reading of that column is unreliable, and nothing above rests on it.

**3. NEW: per-row AUC weighs cheap failures equally with costly ones (MET-1 Must, MET-7, MET-17; note only)**

| Test period | Value |
|---|---|
| Failed share of rows | 12.6% |
| Failed share of node-hours (allocated nodes × duration) | 7.0% |
| Share of failed node-hours held by the top 1% of failed jobs | 83.5% |
| Rows submitted in bursts of 10 or more per user per minute (failed / all) | 85.9% / 85.5% |

- The node-hours wasted on failures sit in a few large jobs. Per-row AUC is driven by many small, quick, bulk-submitted failures.
- The source fixes no cost and no capacity, so MET-7 gives no basis for a cost-weighted metric. MET-17 keeps the score per row because each job is placed on its own.
- I would keep ROC AUC as the declared metric. The notes should say how unequal the cost per row is (the figures above), and that a node-hours-weighted score would rank models differently. That second part is untested.

**4. KNOWN: requested nodes, cores and frequency are left out (USE-6)**

The column audit's issue 4 already covers this, and I agree with its recommendation B. These values are on the operator's screen at submission and cannot be changed afterwards. Finding 1 is the larger form of the same gap: of everything the operator has at submission, the job history matters more than the resource request.

**5. KNOWN, still valid**

The earlier practitioner's points remain unchanged:
- the post-run cohort selection (USE-8, `Selection Bias`);
- execution records versus parent jobs;
- a nonzero exit as a proxy;
- log loss or Brier for probability quality.

The log-loss comparison in finding 1 repeats that last point: a user-history probability beats the shipped model there too.

**Ranked gaps between the dataset and the real decision**

1. Live outcome history is left out (finding 1). It is worth +0.04 to +0.12 AUC with no model, and it changes what the task is.
2. The release only contains jobs that ran and were measured (KNOWN, USE-8).
3. The requested resources are left out (KNOWN, issue 4).
4. Each row is an execution record rather than a parent job (KNOWN). 85% of rows come in bulk bursts.
5. Per-row scoring does not follow the node-hour cost (finding 3). This needs a note, not a change.

**Would I use it?**

I would use it as advisory triage, but not a model trained only on these inputs and frozen for four months. My first comparison would be the user's recent failure rate, and on these data that untrained rate beats the shipped model in every window.

**Sources**

- The record's `## Review` (issues 1 to 4, Horizon block, the historical practitioner) and `dataset.py`.
- The column-audit folder: `feature_list.csv`, `audit.json`, `compact.parquet`.
- The F-DATA paper (doi 10.1038/s41597-025-05633-1) and the Fujitsu job manual J2UL-2534-01ENZ0, as cited in the record.
- `use_case.md` (USE-3/5/6/8) and `metrics.md` (MET-1/7/8/17).
- Exit codes 126 and 127 follow the POSIX shell convention.

</details>

<details><summary>Precedent check (2026-11-21)</summary>

**Precedent check: fugaku_hpc_job_failure (2026-11-21)**

**What I tested**

- Ran `decision_register.py` (5,933 decisions; JSON at the run folder) and read every flag that names this dataset, SPLIT-10, SPLIT-12/14/15 or USE-6.
- Read the record, `dataset.py`, the SPLIT-9/10/12/14/15/19/20/33 rule texts and Cases rows, USE-6 and its cases, LEAK-38, the split tree's dated-event-log branch, the row-budget protocol (`split_protocol.md`, `definitions.md`), and the closest sibling definitions and records.
- Monthly row counts come from the column audit's `out/audit.json`, covering all 25,866,900 rows. I fitted no models.
- `check.log` was still running when I checked: it had verified the source files up to 23_05. There were no leak, task, dtype or group logs in the panel folder yet.

**Verdict per decision**

| Decision | Closest precedents | Verdict |
|---|---|---|
| Target: zero vs. nonzero exit code; fit approximate; `Selection Bias` (issue 1, Resolved 2026-11-03) | lt_vehicle_loan_default_prediction (Selection Bias plus approximate fit, 2026-10-23, Myunghwan). Memory rule: target treated case by case, as recorded | consistent |
| Inputs: masked ids plus the source embedding; `jnam` kept categorical (CLEAN-14 departure) | high-cardinality ids kept as categories elsewhere (meituan courier and merchant ids) | departs, with a stated reason (opaque masked identities) |
| Submission time `adt` as an input | time-column actor test (the operator holds the submission time) | consistent |
| Metric: `roc_auc` fallback, because the paper's accuracy is a habit (MET-6/8) | the MET-8 fallback pattern | consistent |
| Split leaf: dated event log, forward, case arrives, late labels → **Temporal · arrival date, label-delay gap** | the leaf's examples: lusaka (1-day gap), aeolus_rebuilt_1m (1-day gap), african_credit_scoring_challenge (filter on due date + 30 days), acquire_valued_shoppers (5-day gap) | consistent leaf |
| No gap beyond the completion filter (Exception to SPLIT-10, 2026-11-03, Myunghwan) | see Finding 1 | departs, with a stated reason (P4); the Horizon note's proposed rewording would hide it |
| Horizon: three contiguous four-month windows (Horizon block, open) | SPLIT-12 family case (each source keeps its own cadence, 2026-10-21, Lennart); aeolus (fortnights chosen by season, CC 2026-11-10); medical_facility (follows the source's horizon) | A is consistent with SPLIT-12/19; one option under SPLIT-15 is missing (Finding 2) |
| Window count 3 against SPLIT-33's target of 3; train share 65.3% or more (SPLIT-14) | rule text | consistent |
| Training side: a uniform 1M of all history, capped in the container | issue #70 protocol (Lennart, 2026-11-10); duolingo_spaced_repetition_recall (same PR, same pattern) | departs; no curator decision after the rule (Finding 3) |
| Issue 4: add the requested nodes, cores and frequency (open; recommendation B) | brazilian_ecommerce, medical_facility_operational_data (2026-11-05, Lennart), qsar_bioconcentration (2026-10-26, Lennart); counter-case open_soil_spectral_library (2026-11-05, Lennart) | B is consistent; C needs an actor fact that is absent here (Finding 4) |

Register flags that are not findings:
- `exception_to_must` on SPLIT-1 and SPLIT-9 is a keyword artefact. The exception cites SPLIT-1 and SPLIT-9 as the rules it *serves*: SPLIT-9 is met by the completion filter, and SPLIT-1 is the reason given.
- `amendment_due` on SPLIT-10 (11 datasets): of the SPLIT-10 exceptions in the Cases table, fugaku is the only one that serves P4 deployment fidelity. alfa_battle, lending_club, spanish_homeowners and wisconsin all serve SPLIT-14's floor. So fugaku is not a third case of any kind, and it adds nothing toward an amendment.

**Findings**

**1. Keep the "Exception to SPLIT-10" label; the Horizon note proposes rewording it as "No fixed embargo" (NEW; SPLIT-10, split tree)**

- **Problem:**
  - The Horizon block's notes for the AI say the "Exception to SPLIT-10" wording "can become 'No fixed embargo', since the tree's leaf accepts the completion filter as the gap".
  - SPLIT-10 as amended (2026-11-04/05, Lennart, on lt_vehicle) is more specific than that. "A gap is set where a measurement shows ... a selection by the outcome", and "no gap is needed where ... the measurements show neither."
  - The record's own maturity audit measured exactly that selection: late-ending last-day jobs fail at 18.53% against 0.292% among jobs already complete. The definition also feeds `adt` to the model as a datetime. That is the case SPLIT-10's "Why" names: "the newest training rows are the fast ones, and a model that sees the time as a number is biased."
  - lt_vehicle's no-gap application rests on a fixed outcome horizon, which removes the selection. Fugaku's delay varies (tag `Target: Varying Delay`; median 2.2 h, 99.9% within 23.6 days), so that reason does not carry over.
  - The siblings with exact end times all set a gap where training rows end after the cutoff: nyc_taxi_trip_duration_1m, pkdd_15, cooking_time_1m and maps_router_eta_1m (one-day gap, 2026-10-21, Lennart), plus lusaka and aeolus_rebuilt_1m. A 7-day embargo would cost fugaku only 0.58-0.89% of eligible history, so SPLIT-14 is not at stake. alfa_battle, lending_club and spanish_homeowners could invoke SPLIT-14 for their exceptions; fugaku cannot.
  - The curator settled this as an exception, with a stated P4 reason (Resolved 2026-11-03), and the splits.md Cases table records it as `exception`. Relabelling it as an application would remove the record that this case departs from its siblings.
- **Reflection prompt (draft, issue shape):** Keep the no-gap choice recorded as an exception to SPLIT-10, or relabel it an application of the label-delay leaf?

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep "Exception to SPLIT-10" (no change). Distinguishing fact: exact completion times plus a cutoff at a calendar month, so the filter matches what a live refit knows, and the selection is kept as a disclosed limitation | matches SPLIT-10's text and the Cases row; no rebuild | the nyc/pkdd family with exact end times chose a gap; the pair stays a recorded departure |
  | b | Relabel it an application ("No fixed embargo") | shorter wording | contradicts the amended SPLIT-10 trigger (measured selection) and the Cases row |
  | c | Set a gap of about the delay (for example 7 days, or 24 days for 99.9% of jobs) | follows nyc/pkdd and SPLIT-10's Why | rebuild; reopens a Resolved decision |

  **Recommendation:** a. Drop that sentence from the Horizon notes for the AI. c only if Andrej wants the nyc/pkdd pair decided alike across curators.

  Rules: SPLIT-10 (Should, amended 2026-11-04/05), SPLIT-9, SPLIT-14; principles.md "Exceptions and amendments".

**2. The Horizon options leave out a window in another year (NEW; SPLIT-15, SPLIT-14)**

- **Problem:**
  - SPLIT-15 (amended 2026-11-10, Andrej and Lennart): "Prefer windows in other years, then other seasons ... over the windows just before the newest. Walking back from the newest is one choice among others and needs its reason."
  - Options A to D all walk back contiguously. The only one that reaches another year is D (six months), and its oldest window drops under 50% of the rows for training.
  - On the release's monthly counts, a four-month window Jan-Apr 2023 trains on 54.4% of the rows before the label filter. The filter removes about 0.1-0.2% more, so the window stays above the floor. It is the same season as the newest window (Jan-Apr 2024), one year earlier. Sep-Dec 2022 (43.6%) would be under the floor.
  - A's stated reason (it covers the source's June 2023-April 2024 holdout, SPLIT-19) is a valid reason under SPLIT-15. The table should still offer the other-year alternative.
- **Suggested extra row for the Horizon options table:** E | Jan-Apr 2024, Sep-Dec 2023, Jan-Apr 2023 | train about 91% / 80% / 54% | Pro: two years; the newest season tested twice, as SPLIT-15 prefers | Con: leaves out May-Aug 2023 (summer) and 3 of the source's 11 holdout months; rebuild; custom cutoffs in `_select_temporal`.
- The recommendation can stay A. Its reason should then say why the source holdout outweighs the other-year preference.

**3. The training side is capped in the container, against the row-budget protocol (NEW; SPLIT-20, issue #70)**

- **Problem:**
  - The row-budget protocol (`definitions.md`, "Larger than the row budget", issue #70, Lennart 2026-11-10) says "The train side keeps every row available to it ... N is recorded, not applied." Its default sampler takes the newest year before the window, because "a random N of all history dilutes recent data on long histories".
  - `dataset.py` applies a class-proportional random 1M of **all** history in the container (`TRAIN_CAP`, `_select_temporal`). The record states the intent: "Preserve the approved fixed training draw", in the 2026-11-16 compatibility repair.
  - The approval it cites (2026-11-03, Myunghwan) predates the issue #70 rule. No CC after 2026-11-10 decides the cap. The Horizon block mentions "a uniform 1M draw" but raises no item on it.
  - duolingo_spaced_repetition_recall (same PR) has the same pattern (`TRAIN_CAP` in its definition), so the two are a pair to decide alike.
  - Distinguishing fact (my best guess): the 384 float32 embedding coordinates per row. A whole training side, up to 91% of 25.9M rows, is about 36 GB of embeddings alone. A container of that size would be out of line with the others (aeolus_rebuilt_1m keeps 13.7M rows, but with few columns). Neither the record nor the splits comment says this.
- **Reflection prompt (draft):** Keep the training sides capped at a uniform 1M of all history in the container, or follow the protocol: keep whole training sides and let a benchmark sample the newest year?

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep the cap, and write the fact (embedding size) as an exception in the splits comment | no rebuild; the container stays at a workable size | the uniform draw dilutes recent jobs, which the #70 study found can change rankings |
  | b | Keep the cap but draw it the protocol's way (newest year, extended back to 1M) | follows #70's sampler; small change | rebuild and requalify; departs from the authors' all-history training (SPLIT-20) |
  | c | Whole training sides plus a recorded budget | follows the protocol exactly | very large container; prepare step rewrite |

  **Recommendation:** a, or b if Andrej weighs #70's ranking evidence above SPLIT-20's "what the authors trained on". Decide duolingo the same way.

  Rules: SPLIT-20 (Should), SPLIT-11; `definitions.md` row-budget protocol (2026-11-10, Lennart).

**4. Issue 4, option C would need the open_soil kind of fact, which is absent here (KNOWN issue; precedent added)**

- Recommendation B follows USE-6 (Must) and its cases:
  - brazilian_ecommerce: the promised date kept as an input.
  - medical_facility_operational_data: `minutes_early` added although the source's features left it out (2026-11-05, Lennart).
  - qsar_bioconcentration: logKOW added, because the assessor holds it (2026-10-26, Lennart).
- The counter-case is open_soil_spectral_library (CC 2026-11-05, Lennart). There, inputs that a lab knows were left out as "a choice of actor", because the source's prediction service accepts only the spectra. For fugaku the source paper lists requested resources among "the information available at job submission time", and the stated actor (operator or scheduler) sees them. So the fact that set open_soil apart does not hold here. C ("left out by choice") would depart from USE-6 without a distinguishing fact.
- Keeping the elapsed limit and priority out is consistent. The manual (section 2.5.4) documents that they can change after submission, so their timing is known to be possibly late (LEAK-10). LEAK-38 does not apply: the release is not the data owner's own competition.

**Things checked and found consistent (no finding)**

- Recurring users and job names stay in a temporal split, not a grouped one. The use case does not target unseen users (the first question of the split tree; SPLIT-13).
- Test windows are capped at 500k rows each (protocol).
- The masked-`jnam` CLEAN-14 departure has a written reason. It is the AI's documentation decision, endorsed by the 2026-11-03 mediator; no curator turn contradicts it.

</details>

<details><summary>Blind review (2026-11-21)</summary>

**Blind review: Fugaku job failure (`exit state`)**

**Verdict: include with changes.** The task is real and the split is honest, but the table is mostly three IDs plus a 384-dimension text embedding of those same IDs. It leaves out the submission-time resource requests a real failure predictor would use. The row selection is not uniform across months and not documented.

Task: predict at submission (`adt` = "Arrival datetime (submission time)") whether a Fugaku job will end with exit code != 0. Users or the scheduler could act on that before resources are spent, which is a real use. The source paper (Antici et al., Sci Data 2025, F-DATA) proposes exactly this task with a temporal split. All prepared features are known at submission, so I found no leak.

**Experiments (200k sample, LightGBM on Slurm cpuhigh32)**
My own windows (the real ones are unknown to me); each test window is trained on everything before it.

| test window | n test | fail rate | per-user past fail rate (AUC) | LGBM ids+time | LGBM embedding only | LGBM usr+env+time+embedding | logloss prior / best |
|---|---|---|---|---|---|---|---|
| 2023-07..09 | 28,734 | 8.5% | 0.768 | 0.782 | 0.750 | 0.790 | 0.292 / 0.272 |
| 2023-10..12 | 31,817 | 14.7% | 0.881 | 0.865 | 0.863 | 0.900 | 0.429 / 0.289 |
| 2024-01..04 | 40,008 | 11.9% | 0.872 | 0.834 | 0.784 | 0.857 | 0.366 / 0.234 |

Embedding model, AUC on test rows whose (usr, jnam, jobenv_req) combination was seen in training vs. not seen: 0.90/0.95/0.89 vs 0.60/0.78/0.72. Between 49% and 70% of test rows have an unseen combination.

**Concerns, most serious first**
1. **The signal is mostly "which user", and 384 of the 388 features re-encode the IDs.** A smoothed per-user historical failure rate alone gets within 0.00-0.03 AUC of the best LightGBM, and beats it in window 3. The embedding is almost a function of the (usr, jnam, jobenv_req) combination: 50,922 combinations give 51,923 distinct vectors, at most 2 per combination. The source says it encodes "the de-anonymized user information, job name and job environment" with SBERT all-MiniLM-L6-v2. Its real value is name similarity for unseen job names (AUC 0.60-0.78 on unseen combinations). As prepared, the benchmark mostly scores how a method handles 384 dense correlated columns and high-cardinality IDs. *Change:* add the submission-time numeric fields (item 2). Consider reducing the embedding (for example with PCA to about 16-32 dimensions) so it does not dominate the column count.
2. **Submission-time features were dropped.** The public `feature_list.csv` includes fields known at submission: `nnumr` (nodes requested), `cnumr` (cores requested), `elpl` (time limit), `mszl` (memory limit), `freq_req` (requested frequency) and possibly `pri`. They carry signal. In raw April 2021, jobs with `elpl` <= 1 h fail 19.9% of the time vs 6.8% for 1-2 h, and jobs with more than 30 nodes requested fail 18.7% vs 6.6% for 3-8 nodes. *Change:* add `nnumr`, `cnumr`, `elpl`, `mszl`, `freq_req` (and `pri` if it is set at submission; I did not confirm that). Keep out anything recorded after start (allocations, `qdt`, `sdt`, `edt`, `duration`, performance and power).
3. **The row selection is undocumented and not uniform over time.** The source has about 24M jobs, the prepared full table 2,500,499. Comparing the implied monthly counts (sample count × 2,500,499/200,000) with the raw monthly files (parquet footers on Zenodo):

   | month | raw jobs | implied prepared rows | rate |
   |---|---|---|---|
   | 2021-04 | 116,977 | 6,764 | 5.8% |
   | 2021-07 | 338,251 | 19,216 | 5.7% |
   | 2022-01 | 1,307,407 | 76,165 | 5.8% |
   | 2023-06 | 1,303,631 | 166,546 | 12.8% |
   | 2024-03 | 508,286 | 108,934 | 21.4% |
   | 2024-04 | 420,450 | 92,606 | 22.0% |

   Whatever the filter or cap is, it is not a uniform subsample, and it weights the later (test) period. *Change:* document the selection in the task, or draw a uniform random subsample, or deduplicate as in item 4. (2,500,499 is also close to the paper's "around 2.5 million" failed jobs, but the table holds 11% failures, so it is not the failed jobs only.)
4. **Bulk submissions give exact copies and concentrate the task on a few users.** 16.3% of the 200k sampled rows are exact copies of another sampled row (all 388 columns including `adt`). In the raw April file, 43% of rows share (usr, jnam, adt) with another row, and 116,977 rows carry only 70,375 distinct `jid`. The top 20 users account for 62% of the failures. Copies in the same second share their label most of the time: only 68% of rows sit in an ID combination with a pure label, the rest vary. With a temporal split these copies rarely cross train and test, so this is a weighting problem rather than a leak. *Change:* collapse rows sharing (usr, jnam, jobenv_req, adt, label) into one row, or weight them, so a few heavy users do not decide the score.
5. **The label is noisy by construction.** `exit state` = "failed" if the exit code is not 0, and the paper says "we cannot preclude that a user's application intentionally returns a non-0 exit code". In raw April, 73% of failures end within 60 s (start-up or script errors) and the exit codes are mixed (1, 255, 4, 127, 16, ...). It is still a sensible target, but it should be noted in the task.
6. **Minor points.**
   - `jobenv_req` is almost constant (96% one value) and has no signal on its own (AUC 0.44-0.50).
   - The monthly failure rate drifts from 1.9% (2022-08) to 22% (2021-03), so the scores of the three windows will differ a lot.
   - `adt` is naive local time (JST); the source stores it with "+09". That is fine as long as all rows are the same.
   - There is no weight column, so I had nothing to check there.

**What I could not check**
- The exact rule that produced the 2.5M rows: I only compared 6 monthly row counts, not the full 24M.
- The real test-window boundaries.
- Whether `pri` is set at submission.
- How cancellations and wall-time kills map to exit codes. `deldt` is filled for every job, so it does not identify them.
- The SBERT input strings, which are not public.

I loaded one raw monthly file (21_04) and the footers of five others from the public Zenodo record. I opened no file outside the clean room except the interpreter.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC12311113/ , https://zenodo.org/records/11467483 (feature_list.csv, monthly parquet files).

</details>

<details><summary>Task gamer (2026-11-21)</summary>

**Task gamer report: Fugaku job failure (`exit state`)**

**Verdict:** I could not game this task. None of my attacks beat the honest model by more than the seed-to-seed spread. The weaker spot is the other way round: the kit leaves out the resources a job requests at submission, and those help an honest model.

All fits were LightGBM (300 trees, lr 0.05, 63 leaves, bagging 0.8, colsample 0.5, `n_jobs=2`) on the shipped splits, scored with `score.py`, run as Slurm jobs on cpuhigh32. No rows were subsampled except where noted. Encoding: `usr` and `jobenv_req` as categories, `jnam` as its integer id, `adt` in epoch seconds, plus the 384 embedding columns.

**Honest baseline and noise**

| Model | r0f0 (Jan-Apr 24) | r1f0 (Sep-Dec 23) | r2f0 (May-Aug 23) |
|---|---|---|---|
| base, 3 seeds (default, 1, 2) | 0.898 / 0.871 / 0.865 | 0.825 / 0.824 / 0.838 | 0.787 / 0.796 / 0.808 |
| base, mean of 3 seeds | 0.878 | 0.829 | 0.797 |
| base + random column | 0.868 | 0.829 | 0.802 |
| base + past-only order features, mean of 3 seeds | 0.896 | 0.828 | 0.783 |

The seed spread is large: up to 0.033 AUC on r0 from bagging and column-sampling randomness alone. Every gain below should be read against it.

**Exploits ranked by gain**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Future submissions of the same user and the same (user, job name): gap to the next job, counts in the next 1 h / 1 d, number of later jobs (test-window composition) | `work/build_feats.py`, `work/fit.py base_past_fut` | base+past, 3-seed mean: 0.896 / 0.828 / 0.783 | 0.897 / 0.833 / 0.778 | +0.001 / +0.005 / -0.005 (within noise) | No | None needed |
| 2 | `jnam` anonymisation id used as a number | `work/fit.py base_noemb*`, `work/jnam_ids.py` | id replaced by first appearance in the kit, no embedding: 0.889 / 0.802 / 0.780 | 0.887 / 0.831 / 0.770 | -0.002 / +0.029 / -0.010 | Yes: ids rise with the month a name first appeared (checked month by month), so the id is "when this name was first used", which is known at submission | None needed |

No exploit holds up. The future-submission features alone score 0.563 / 0.576 / 0.425, and the third split falls below 0.5, so they do not even carry a stable direction.

**Flaws that hurt an honest model**

| # | What is wrong | Honest choice | Kit score | Honest-choice score | Gain | Fix |
|---|---|---|---|---|---|---|
| A | The kit leaves out the submission-time request columns (`nnumr`/`cnumr` nodes and cores requested, `elpl` time limit, `mszl` memory limit, `freq_req` frequency). They are in the source and known when the job is submitted. | Join them from Zenodo by (usr, jnam, jobenv_req, adt); 100% of kit rows match | r0 only, trained on the r0 training rows of Sep-Dec 2023 (115k rows): 0.886 | kit + request: 0.897; request columns + usr + jobenv only: 0.902 | +0.010 / +0.016 (one seed, r0 only) | Add the request columns as features |

Univariate AUCs on the full source month April 2024 (420k jobs) are `nnumr`/`cnumr` 0.681, `mszl` 0.633, `elpl` 0.566 and `freq_req` 0.567 (inverted). The model gain is one seed on one split and is below the r0 seed spread, so it is suggestive only. The univariate AUCs are solid. Script: `work/extract_src.py`, `work/subfit.py`; source months 23_09 to 24_04 were downloaded and reduced to these columns in `work/src/`.

**Findings**

1. **Future submissions (#1).** A job that fails is often followed by a resubmission, so the gap to the next same-name job and the count of later jobs could reveal a failure. They do not: the gain over the past-only model is +0.001, +0.005 and -0.005 on the 3-seed means, while the seed spread is 0.01 to 0.03. The kit is not exposed to test-set composition in any way I could measure.
2. **`jnam` id (#2).** The ids were assigned file by file in the release script, and the median id per month of first appearance rises steadily (about 24k in 2021-03, 1.22M in 2023-01). So the id is a first-seen date for the job name, which is honest. Dropping it costs 0.02 to 0.05 AUC without the embedding, and replacing it with first appearance in the kit recovers most of that. That makes it signal, not an exploit.
3. **Missing request columns (A).** The source has the requested resources for every job. They are submission-time inputs and the strongest single predictors I found, but the kit ships only user, job name, job environment, submit time and an embedding. According to the source's generation script, the embedding is Sentence-BERT (all-MiniLM-L6-v2) applied to the raw "usr,jnam,jobenv_req" string, so it duplicates the three id columns. Mildest fix: add `nnumr`, `cnumr`, `elpl`, `mszl` and `freq_req`.

**Attacks that found nothing**

| Attack | Result |
|---|---|
| Formats: share of `adt` at second 0, by class | 0.0180 completed vs 0.0184 failed |
| Formats: last digit of the `adt` second, by class | Flat (0.096 to 0.113 per digit in both classes) |
| Other columns | No numeric columns besides the float32 embedding and `adt` |
| Row order | Rows sorted by `adt`. Row position AUC 0.554 and `usr` id AUC 0.521 reflect the time trend. Next-row label agreement 0.938 comes from bursts of the same job; test labels are unseen, so it cannot be used beyond the first rows after the split date. |
| Temporal hygiene | No training row at or after its test window start, on all 3 splits |
| Copies across the split | 50% of test rows have a job name seen in training, 74 to 98% a known user. The embedding is a deterministic function of (usr, jnam, jobenv_req) (0.06% collisions), so "copies" are recurring jobs: signal, not leaks. |
| Naive label history (last training label and failure rate of the same user and the same (user, name)) | Hurts: 0.862 / 0.733 / 0.819. In training the previous label is seconds old; in test it is up to 4 months stale. Not a task flaw. |
| Train only on recent rows | Last 120 days: 0.890 / 0.764 / 0.792. Last 365 days: 0.860 / 0.773 / 0.790. Not better than the full training set. |
| Dropping `adt` | 0.863 / 0.825 / 0.801, within noise of the baseline |
| Is the kit's sample label-dependent? | April 2024: kit failure rate 0.1939 vs 0.1942 in the source month. The kit holds 21.8% of the source rows, with no sign of label-dependent sampling. |
| Source lookup | Works: every kit row of April 2024 matches the Zenodo file on (usr, jnam, jobenv_req, adt), with `ec` and `exit state` attached. As expected for a public dataset; not ranked. |
| Web | No competition, leak or "magic feature" threads exist for F-DATA. The source repository's own failure baseline is a kNN on the embeddings or the ids. |

**What I could not check**

- The request-column gain on r1 and r2, and with the full training sets. That needs all 38 source months (about 25 GB); I used 8.
- Whether jobs that never started (dropped by the source's cleaning, which requires start and end times and performance counters) would change the label base rate. The kit cannot show it.
- More seeds. The 3-seed means carry roughly ±0.01 to ±0.015 uncertainty.

</details>

<details><summary>Column audit (2026-11-21)</summary>

**fugaku column audit (2026-11-21) — all 38 files (25,866,900 rows); 1 issue (record issue 4: add requested nodes/cores/frequency); facts hold**
- Inputs: usr, jnam, jobenv_req, 384-d MiniLM embedding of the comma-joined original strings (per-row function, no fit), adt. All known at submission.
- Masked ids numbered in first-appearance order over the whole release (Spearman 0.99): inert as categories.
- jobenv_req flips _0 -> _1 in April 2024 (99.94% of April rows); the embedding shifts with it; newest window's last quarter; drift, kept.
- Requested nnumr/cnumr/freq_req fixed at submission (Fujitsu manual 2.5.4: pjalter changes only elapse, rscunit, rscgrp, priority); not shipped -> issue 4.
- Each fiscal year cut on end time at 31 March (March files: latest ends 09:25/23:52/23:55/23:52; other months 2.2-16.5% of last-week submissions end after month end) -> ~0.4% of newest window missing; selection, doc only.
- Elapsed-limit kills ~absent (0.005% of rows); failed = nonzero exit of a job that ran to its end.
- Label delay: median 2.2 h, p99.9 23.6 d, max 283 d (Assessment corrected).
Doc fixes: download recipe path points at removed fugaku_hpc_job_failure_1m folder; typo "union's384-value"; cohort-limit bullet (fiscal-year cut, kills absent); inputs bullet (jobenv flip, first-appearance numbering).
Evidence: the run folder (stats.py, analyse.py, monthend.py, ablation.py, out/compact.parquet).

</details>

<details><summary>Historical panel summary (2026-11-03)</summary>

ship after changes (mediator). The advocate and critic agree on retaining the original exit-state task with approximate operational fit. The three open decisions concern that fit, the proposed SPLIT-10 exception and provisional value acceptance. Full panel tier. The proposed no-extra-gap exception and operational-fit/value weighing remain for Myunghwan; source scope and the categorical-name rationale need no renewed authorization. Blind concerns about lineage, timing and repetition were substantially answered by full-source checks; broader deployment limits remain explicit.

</details>

<details><summary>Historical mediator (2026-11-03)</summary>

**Mediator judgment record**

**Verdict: ship after changes.** Recommend retaining the original zero/nonzero exit-state task, with the documentation changes below and the curator’s weighing of the bounded operational fit and no-gap exception. This is an add-stage recommendation, not inclusion or build authorization.

**Validity:** USE-1/3/5/8 support a plausible submission-time, per-execution risk task with approximate fit. The published label is verified; preventable failure, all-submission coverage and parent-job utility remain unverified. Retained inputs are source-supported at submission. SPLIT-9’s measurable future-label shortcut is removed using recorded completion as the availability proxy. Temporal same-system evaluation follows USE-10 and SPLIT-1/3/4. No irreparable Must violation is established. SPLIT-10 needs an explicit proposed exception.

**Value:** Useful chronological discrimination is established. TP-4 triviality and TP-5/9 smallness are not established. `no_spread` and `drift_baseline` have received bounded follow-up; definitive tuned-family separation and operational probability quality remain unresolved. TP-3’s sufficient keep condition is not claimed.

**Quality:** Retain the source representations and all finite, nonconstant embedding coordinates. Document categorical masked job names as a CLEAN-14 departure. The existing source-representations-first authorization resolves the feature-scope question.

**Weighed:** verified source target, faithful representations, substantial chronological support and useful signal favor retention; outcome-selected coverage, unresolved intervention identity, fast-completer selection, reporting latency and incomplete tuned evaluation qualify that recommendation.

**Changes to make now that need no separate decision**

1. **Add `Selection Bias` to the record’s `decision_markers`.** Keep the dataset’s schema-valid `data_tags`. This follows the dated superconductivity and infrared-thermography decisions and the principles’ consistency requirement; it is not a newly imported pinned Must.

2. **Document why masked `jnam` stays categorical.** State that its 359,636 levels are opaque stable identities, while the private original names are unavailable. Text processing cannot recover those semantics and could attach meaning to arbitrary token suffixes. This is a justified CLEAN-14 **Should** departure serving USE-1/10. Writing the rationale is an agent task; it does not need another scope question.

3. **Write the proposed SPLIT-10 exception explicitly.** Distinguish removal of unavailable labels from the additional-gap default. State the proposed rationale—precise completion filtering represents labels available to a live refit—and retain fast-completer selection and unknown reporting latency. Preparing that proposal needs no decision; accepting the departure belongs to the curator.

4. **Record the first tuned benchmark follow-up.** Preserve both flags and specify a recheck of family separation, foldwise simple baselines and probability quality under TP-1/3/4 and EV-3/7/8. Do not describe bounded tuning as full TabArena HPO.

The regenerated README, corrected twelve-month calendar prose, illustrative action, expanded approximate fit and per-record evaluation wording are already installed. They are not outstanding repairs.

**Issues for the curator, ranked**

**1. P3 validity — accept the bounded task’s operational fit?**

The strongest retention case is concrete: the source publishes exit-state prediction for workload management, every released label matches its documented construction, submission-time inputs are available, and advisory investigation is plausible.

The strongest contrary evidence concerns deployment transport and action resolution. Eligibility depends on post-run completeness. April contains 89,593 rows in repeated identifier/submission-time groups, including 180 groups with conflicting labels. Per-record AUC therefore cannot establish performance per actionable parent submission or across all attempted submissions.

USE-1/5/8 are **Must** requirements. Approximate fit cannot excuse a demonstrated wrong target. Here, however, predicting recorded nonzero exits is faithful; a requirement to predict preventable or parent-job failure has not been established.

**Decision:** accept this approximate per-execution benchmark with its named limitations, or defer because the remaining operational gap is too material. A submission census, finer intervention identifiers and adjudicated actionability evidence would resolve broader utility claims. Renaming release survivors as the operator’s intake would not resolve the gap. Retargeting, aggregation and deduplication are unsupported remedies.

**2. P4 validity — accept the no-extra-gap exception and disclosed refit adaptation?**

SPLIT-9 **Must** is met for recorded completion: no retained training outcome ends after its cutoff. SPLIT-10 **Should** independently addresses the newest training rows being fast completers. Exact filtering does not erase that concern.

For no additional gap, precise completion dates support live-refit fidelity under SPLIT-1. Against it, reporting latency is unavailable, and Fugaku lacks the independent completeness evidence supporting some no-gap precedents. Seven- and thirty-day embargoes remove additional mature observations but do not establish which operational delay they repair.

**Decision:** accept the specific proposed exception with both limitations retained, or require an evidence-grounded embargo. Do not choose a duration from favorable test scores.

The three four-month windows also adapt the source’s fixed eleven-month holdout. They satisfy the three-window requirement, retain a 65.322% oldest eligible history, and cover twelve months. The source supports updating models, but does not establish a production four-month cadence. The four-month windows are the implemented benchmark judgment under SPLIT-12/19; no separate renewed investigation authorization is needed.

**3. P6 value — retain provisionally pending the first tuned benchmark run?**

Native task probes show mean AUC approximately 0.794/0.758/0.783 for linear/RF/LightGBM versus 0.5. On the bounded follow-up protocol, train-only tuning produces 0.8655/0.7775/0.7911; raw-user prediction does not match it on every fold. Triviality is unproved.

Conversely, two configurations do not establish tuned-family separation. Oldest-window full-model log loss is 0.5104 versus 0.4330 for raw-user prediction. This establishes worse probability quality in that comparison, not a diagnosed calibration mechanism by itself.

**Decision:** retain with an explicit first-tuned-run recheck, as recommended, or defer final value acceptance until those results exist. No present evidence supports `Trivial`, `Too Small`, or changing the primary metric.

**Agreed facts and evidence boundary**

- All 25,866,900 released labels agree with zero/nonzero exit code; 2,558,519 are nonzero.
- The final frame has 2,500,499 records and 388 predictors: three nominal fields, 384 published embedding coordinates and submission time.
- Each native window contains 1M training and 500k test records, with 57,135–74,610 failed test records. Independent membership, chronology and completion-cutoff checks pass.
- Zero exact 44-field raw duplicates were found. All 38 traced projected-duplicate pairs differ in execution timing. This supports retention, not universal independence.
- Recurring identities are expected for future same-system prediction. Cold-start grouping and guessed similarity groups would change the task.
- Check 3 completed with zero errors, zero warnings and two disclosed informational skips. `post-prose-check.json` confirms unchanged computational AST and native checksum after prose repairs.
- The leak diagnostic’s float32 normalization failure was transparently repaired for its neighbour tail; it is not a complete clean native CLI pass. The dataset was unchanged.
- No new experiment was necessary for mediation: the disputed measurements already have decisive evidence.
- The supplemental temporal hidden-group probe remains outside this report’s completed evidence. Inspect its actual result before final synthesis. Step 5 mandates that probe for IID tasks, so its unfinished temporal run is not itself a failed gate.

**Consistency with precedent**

Selection marking and approximate fit follow superconductivity; infrared thermography does not justify direct fit without evidence that deployment shares release selection. Retaining distinct executions follows HIVA and repeat-observation precedents; unrecoverable cold-start entities in maternal health and hazelnut are materially different. No-gap acceptance needs its own rationale rather than borrowing Ames/Perth’s coarse-date exceptions. ROC AUC follows the fallback cases; Fugaku has no APS-style fixed cost matrix. A first-tuned-run recheck follows OULAD without treating its decision as proof that Fugaku’s flags are cleared.

The governing rules remain vendor pin `1964e1b`; later curator cases supply precedent facts, not automatically imported amendments.

**Mediator final addendum — completed supplemental temporal recurrence probe**

**Recommendation unchanged: ship after changes and curator weighing.** The completed result supplies recurrence evidence, not a new defect requiring a different target, split, deduplication or feature set. It does not change the three substantive curator issues: approximate per-execution operational fit; the proposed SPLIT-10 no-extra-gap exception; and provisional value acceptance with a first-tuned-run recheck. The disclosed four-month cadence is a documented benchmark adaptation; issue 2's remaining decision is the no-extra-gap exception.

**Evidence inspected.** `fugaku_hpc_job_failure_1m.json`, `hidden-groups.log`, and the pinned native hidden-group implementation. The JSON identifies the temporal regime and 2,500,499 final-frame records. The run completed in approximately 2,550 seconds with exit status zero. This supersedes the original mediator report's pending-result boundary for this probe only.

**What it measured.** Of 386 candidate columns, the reported 20 entity-like candidates are source embedding coordinates. The three candidates with temporal recurrence measurements have mean exact-value recurrence of 38.39–38.49% of test records, ranging from 32.39% to 43.68% across folds. These are coordinate-value matches, not recovered parent-job identities. The 384 coordinates encode only three underlying source metadata fields, so coordinate aliases and stable profiles are unsurprising. This interpretation is supported by the existing source provenance and direct identity-recurrence measurements; the new probe does not independently prove every alias's physical identity.

No composite key was counted among 79 checked one-column-left-out keys from 388 possible keys. That is a bounded search result, not an exhaustive absence-of-groups finding. The near-copy diagnostic used 11 informative tokens, reported 21.37% within-cluster repetition, and found mean train-to-test cluster recurrence of 3.2404% (2.1888–3.9068% across folds). It left 1,695,438 records in large clusters as singletons. Thus the small reported cross-cutoff cluster recurrence is not an upper bound on actual workload recurrence, and the similarity clusters are not valid replacement group identifiers.

**Rule consequence.** The pinned implementation explicitly produces no gap test and no hit for temporal tasks; it reports recurrence instead. `hits: []` therefore means neither absence of entities nor a clean leakage pass. USE-10, LEAK-34 and SPLIT-1/3/4 continue to support future same-system evaluation with recurring workloads. EV-3 and SPLIT-30 prevent recurrence alone from demanding regrouping, while SPLIT-24 prevents promoting similarity clusters into guessed entities. The result adds no demonstrated copied-outcome mechanism, no evidence that deployment requires unseen entities, and no recovery of the unresolved execution-to-intervention mapping. Step 5's mandatory hidden-group gate applies to IID tasks; this temporal run remains supplemental evidence.


**Disposition.** Attach this addendum to the original report, retain the agreed documentation remedies, and present the three numbered curator issues. No new debate round or empirical remedy is warranted by this result.

**Final completion reconciliation (AI, 2026-11-03).** Check 4 completed with zero errors, zero warnings and two disclosed large-cell-count informational skips. The final native checksum is `v2:259a23c34d5183aec23231613772e7c3a4fec65d058cf149e213da22bc46126a`. Historical check-3 checksum statements apply to that earlier documentation version. The framework hashes both curation comments and the split explanation. An independent final native reconstruction exactly matches the audited frame values/order, category metadata, all six train/test membership hashes, scorer and library versions; restoring only the historical curation comments and split explanation exactly reproduces the check-3 checksum. Existing model and diagnostic results therefore apply to the final computational task. Both framework checksum identity and computational identity were checked separately. No container was saved.

**Editorial reconciliation (AI, 2026-11-03).** The cold editor changes were applied: explicit validity/value/quality judgment, one no-gap decision in issue 2, defined value flags and model order, quantified April multiplicity and a substantive panel summary. The four-month windows remain a disclosed implemented adaptation. The three substantive issues remain for Myunghwan; source scope is already authorized.

</details>

<details><summary>Historical claim audit (2026-11-03)</summary>

**Independent claim audit — Fugaku, 2026-11-03**

**Recommendation.** No irreparable validity defect or demonstrated feature leak was established. The current definition has corrected the important broad submission-census and hardware-failure interpretations. Retain those limits prominently. The remaining leading questions concern the operational decision unit and generalization beyond the post-run selected cohort; they are unknowns, not proven failures. Clarify the illustrative operator action and the nonunique ID semantics, correct one verification sentence, and finish the outstanding recurrence/value assessment before a final inclusion recommendation. This report recommends; it does not change a verdict or authorize a build.

**Identity and evidence boundary.** Reviewed the definition and generated README at work base `07274691`, using runtime/rules `1964e1b`, author code `db67a65a4b6e91dcebd26147de191fa0051ad790`. Definition SHA256: `8684b512d50ad5aa39c6afbf012f70b8743eaa651416b7b98b8c4f522f7ec475`, matching `snapshot.json`. Read the canonical record, `claims.md`, `verification.md`, source paper XML/body, source cleaner/derivation/baseline, publisher metadata, and task/leak outputs. Source documents were read from the retained evidence, not newly downloaded. Repository files were read only; this report and scratch are in the panel folder.

**Independent measurements.** `audit_claims.py` and `claim-auditor-checks.json` record a separate streamed check of all 38 raw files' exit codes and labels, a first-1,024-vector sample from each file, all three exported native folds, the native metric scorer, and April row/ID multiplicity. Execution succeeded in 84.56 seconds, peak RSS 1,618,780 KiB. `claim-auditor-source-manifest.json` compares the definition's complete manifest with retained publisher metadata; `claim-auditor-recurrence.json` measures recurrence on the exported native folds. Earlier full-vector, whole-table duplicate and fitted-model checks are explicitly identified below as prior run evidence, not newly rerun here.

**Primary sources.** [F-DATA v1.0 and fixed files](https://doi.org/10.5281/zenodo.11467483); [Scientific Data defining paper](https://doi.org/10.1038/s41597-025-05633-1); [pinned cleaner](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/generation_scripts/clean_and_anonmyze_data.py); [pinned derived features/encoding](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/generation_scripts/generate_derived_features.py); [pinned baseline](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/baseline_experiments.py). Paper references below identify its section; these documents establish meanings and construction, not independently verified deployment effectiveness.

**Claim table.** IDs refer to the supplied `claims.md`; quoted phrases identify the exact load-bearing claims. “Holds” means the stated bounded claim survived the specified check. “Untested” never means pass.

| Claim | Source | Cheapest refuting test actually used | Result | Evidence | Rule |
|---|---|---|---|---|---|
| C1: “Will a submitted Fugaku job terminate with a nonzero exit code?” | `task_summary.question`, README | Compare every released `exit state` with `ec==0`; check whether release is a submission census | **Holds** as exit-state prediction for released execution records; applicability to all submissions **untested** | 25,866,900 rows; 2,558,519 nonzero/failed; zero disagreements. Cleaner excludes rows using post-run measurements. See scope issue 1 | USE-1/5/8; EV-1/7 |
| C2: “A supercomputer operator scores a job when it is submitted, to identify jobs that may need attention before consuming resources.” | `task_summary.use_case` | Read paper's Data Records/application discussion and Technical Validation for actor/action evidence | **Untested** as an actual operational triage policy; plausible illustrative application | Paper explicitly proposes “failure-aware scheduling strategies or checkpoint/restart libraries”; no implemented triage policy, threshold or effect estimate is supplied. Add “For example” | USE-1; EV-2/7 |
| C2: “The source motivates failure-aware workload management.” | same | Look for an explicit source motivation | **Holds** | Paper Data Records connects exit-state prediction to resource-waste reduction. This supports a prediction use case, not proof of realized savings | USE-1; EV-2 |
| C3: “One released job-execution record”; “25,866,900 records from March 2021 to April 2024” | `task_summary.row` | Count raw rows and examine nonunique ID/submission combinations | **Holds** for released records; one-to-one submitted-job identity **untested** | Independent count 25,866,900 across 38 files. April: 420,450 rows, 316,571 `jid`, 334,237 `jid+adt`; 180 `jid+adt` groups have both exit labels. Thus do not replace “record” with “unique submitted job” | USE-5; PROV-1; EV-1 |
| C4: “completed for exit code zero, failed for nonzero”; not hardware diagnosis | `task_summary.predicted` | Exhaustive raw label/code comparison; read source target construction | **Holds** | Zero discrepancies across all raw rows; author derivation uses exactly that rule. Source cautions intentional nonzero returns may not be failed computation | USE-5; LEAK-10; EV-2 |
| C5: three masked fields, released 384-value embedding, and submission time; “All are based on information known at submission.” | `task_summary.known` | Trace encoder inputs and final columns, looking for outcome/post-run inputs | **Holds**, source-supported timing | Encoder consumes only original user, job name and requested environment, with a pretrained encoder and no label fitting. Paper Methods describes the submitted job inputs. Final snapshot has precisely these 3 nominal fields, 384 coordinates and `adt`; no `ec`, `edt`, resources or lineage predictors. Original private text/snapshot immutability cannot be independently reconstructed | USE-3/6; LEAK-10/27; EV-2/7 |
| C6: three successive four-month future windows “with earlier completed labels for training” | `task_summary.split` | Check each native index against submission and completion cutoffs | **Holds** for the recorded end-time proxy | All 3 folds: zero training-submission, training-end or test-window violations; zero within-fold index overlap. Cutoffs Jan 1 2024, Sep 1 2023, May 1 2023. Additional reporting latency after `edt` is unreleased | SPLIT-1/3/9/10; EV-1/7 |
| C7: original labels and representations retained; categories/embedding combined, submission time added; paper used separate representations and a fixed Jun 2023–Apr 2024 holdout | `task_summary.changes` | Compare author baseline, source calendar, definition and reference experiment | **Holds**, with disclosed experimental change | Pinned baseline separately defines integer, anonymous-embedding and sensitive-embedding views. Definition adds time and nominal categories jointly. Source-reference run uses 200k train/200k test with repaired maturity; it is not an author reproduction | PROV-1; USE-8; EV-8 |
| C8/C9: fit “approximate”; selected post-run measurements mean coverage of all attempted submissions cannot be established | `fit`, `fit_reason` | Read cleaner for eligibility, then seek excluded-row denominators in release | **Holds** as a limitation; unrestricted deployment transport **untested** | Cleaner requires valid arrival/start/end and nonmissing counters, energy/power and other values before writing. Public files contain only survivors, so excluded early/nonexecuting/uninstrumented submissions and their labels cannot be counted | USE-1/5/8; EV-7 |
| C10: native class-stratified budget, default seed 4267, full eligible history, 1M train/500k test | `version_comment` | Read native sampler and definition calls; compare membership hashes and full-source counts | **Holds** | All six membership hashes match `snapshot.json`; each fold is 1M/500k. Native sampler takes proportional quotas, not a 50:50 balance. Full histories checked separately from the selected union | SPLIT-14/19; EV-1/8 |
| C11: F-DATA v1.0, Jun 5 2024, fixed DOI; 38 pinned publisher Parquets, CC BY4.0, 27.2GB | `download_description`, README | Compare literal manifest with retained Zenodo/DataCite metadata and actual file sizes | **Holds** | 38/38 entries match publisher size/digest pairs; total 27,231,795,050 bytes; DOI/date/license agree. Prior preparation/source audit records actual MD5 checks. This auditor independently rechecked sizes and manifest, not all digests | PROV-1/10; EV-4/8 |
| C11: standard-library recipe recreates and verifies raw inputs over public HTTPS | same | Inspect fixed URL construction, resume condition, locks, size/digest assertions | **Untested** as a fresh end-to-end download in this audit | Recipe verifies each completed file before promotion; no new 27GB network download was needed. Actual existing raw files and prior source-fetch evidence support the inputs, but do not establish future network availability | PROV-10; EV-7 |
| C11: only selected union vectors materialized; `_make_splits` recomputes selection and removes lineage | definition preparation and `_make_splits` | Trace data flow and compare exported metadata/target ordering and fold hashes | **Holds** | Output contains 2,500,499 union records; independent target/time alignment with `selection_membership.parquet` passes. `_make_splits` checks unique source positions, time/target/roles and drops all 3 lineage columns. Original native snapshot execution supplies the full recomputation evidence | LEAK-27/31; PROV-10; EV-8 |
| C12 prediction point: “before queue insertion, scheduling or execution” and exclusion of all post-run fields | `curation_comments` | Inspect final 389-column schema and paper feature dictionary | **Holds** as intended prediction point | 388 predictors consist only of the named source inputs/time. Source timestamps sometimes have scheduler-order anomalies, but those fields are excluded; their anomalies do not time-travel a retained feature | USE-3; LEAK-10 |
| C12 target counts: “23,308,381 completed and 2,558,519 failed (9.891%)” | same | Independent full raw label/code scan | **Holds** | Counts exactly reproduced; failed share 9.8911%. No alternative failure taxonomy or fixed-duration label introduced | USE-5; PROV-1; EV-1 |
| C12 embedding: pretrained `all-MiniLM-L6-v2`, original versions of the same three strings, no outcomes; “All source vectors are float32, length 384 and finite” | same | Read author generator; inspect Arrow type; independently sample vectors from all files; read prior full audits | **Holds** within available construction evidence | First 1,024 vectors per file: 38,912 vectors, zero wrong lengths/nonfinite values. Arrow source element type is float32. Earlier full-source audits report zero wrong lengths/nonfinite values. No encoder retraining here. Exact encoder-model revision and private source text are not reproducible from public release | LEAK-27; PROV-1/13; EV-2/7/8 |
| C12 changes: requested resources “not silently added”; elapsed limits/priority require timing qualification before extension | same | Inspect actual final feature set and read code path | **Holds** for current exclusion; external manual extension premise not retested | No requested-resource/priority/time-limit columns ship. No present decision depends on settling their editability; do not silently extend the input set | USE-3; CLEAN-1; EV-7 |
| C12 `jid` “is a storage/parent identifier, not a unique released-record key” | same | Test ID uniqueness and joint ID/submission outcomes | Nonunique-key part **holds**; exact “storage/parent” semantics **untested** | April has 103,879 excess rows over unique `jid`; max `jid+adt` multiplicity 2,000, with 180 mixed-label groups. Data establishes nonuniqueness, not the precise bulk/step/retry or ID-reuse mechanism | USE-5; PROV-1; EV-6 |
| C12 row identity: “no exact duplicates over the 44 nonembedding source fields within a month”; months disjoint; repeated IDs have different execution times | same | Inspect full source audit summaries and paired source-vector trace; independent April group test | **Holds** as reported raw audit and sampled trace, not a proof of independent executions | Prior raw audit reports zero full nonembedding duplicates in each file and one submission month per file. All 38 traced projected-duplicate pairs differ in execution timing; independent April test finds 3,373 `jid+adt` groups with different end times | LEAK-16/18/20; EV-6/8 |
| C12 time: parse as instants, convert to Japan time, stable publisher/row ties | same and `_japan_datetime`, `_verified_metadata` | Inspect actual conversion/sort and test native calendar membership | **Holds** | Code performs UTC-aware parse → Asia/Tokyo → timezone removal, then stable sort; all native time-window tests pass. No outcome-valued tie key is used | SPLIT-1; PROV-13; EV-1 |
| C12 cohort: April begins Apr 4; completions through May 14; this does not prove a full submission census | same | Compare original April audit dates and selection procedure | **Holds** | Raw audit min arrival Apr 4 15:06:45; max end May 14 02:38:02, Japan time. Later completions refute a simple end-April-only truncation story, but cannot prove absent submissions did not exist | USE-8; EV-6/7 |
| C12 sampling: full metadata, label availability first, native quotas, exact vector positions | same | Inspect order of operations; independently count histories and mature native indices | **Holds** | Oldest eligible history 16,896,791 / 25,866,900 = 65.3%; unavailable counts 10,387 / 48,375 / 28,118 at May/Sep/Jan cutoffs. No mature-label violation survives sampling | SPLIT-9/10/14/19; EV-1 |
| C13/C14: target `exit state`, `binary_classification` | class fields, README | Count target categories and inspect target feature exclusion | **Holds** | Exactly `completed`/`failed`, untransformed; target absent from predictor list | USE-5; MET-2/3 |
| C15: `Metric.fallback` to binary ROC AUC because source accuracy lacks an operator threshold/cost or decision-specific rationale | metric, README Metric block | Re-read Technical Validation and baseline; run native scorer on every test fold | **Holds** | Paper calls its metrics “simple and widely used metrics”; baseline calls `classification_report`. No unique decision threshold/cost found. Native constant score AUC 0.5, perfect ordering 1.0 on all 3 folds, with no auxiliary inputs | MET-1/2/5/6/8/11/12 |
| C16: `accepted_check_warnings = {}` | definition | Read exact native check-2 output, including infos | **Holds** as a mechanical-check claim | 0 errors, 0 warnings, 2 info across 26 checks. `dataset_duplicates_skipped` and `dataset_pure_feature_value_skipped` are infos; separate snapshot/probe evidence is needed and exists. Clean check is not a semantic pass | EV-3/7 |
| C17: `Temporal(on="adt", horizon=4, horizon_unit="months")` | definition | Inspect label derivation and actual windows | **Holds** as refit/test-window length | Three 4-month windows; eventual terminal exit label is unchanged. Four months is not a failure deadline | USE-5; SPLIT-1; MET-2 |
| C18: earlier mature history, at least 50% full-source floor, recurring source identities, newest-first windows, paper holdout plus May | `splits_comment` | Full-metadata counts, exported membership tests, recurrence computation, calendar arithmetic | **Holds** | Every fold has 1M/500k selected rows; oldest eligible fraction 65.3%. Test users seen in train: 97.9808%, 95.0844%, 74.1210% newest first; job names 49.7718%, 49.8328%, 47.9916%. Temporal same-system evaluation is not an unseen-user claim | USE-10; SPLIT-1/3/14/30; EV-1 |
| Implied: projected copies do not leak future exact records across a fold | definition, snapshot/probes | Compare datetime-inclusive vs datetime-free overlap and source duplicate trace | **Holds** for tested exact-copy mechanism; all possible relational dependence **untested** | Native leak prefix: 25.5% retained-profile overlap excluding date, 0% including date. Snapshot: 556,583 repeated full retained rows, confined to identical times; source trace confirms distinct execution timing in all 38 inspected pairs. Recurring inputs alone do not require a grouped split | LEAK-16–20; SPLIT-30; EV-3/6 |
| Implied: combined categories and embedding are valid model inputs | definition | Trace whether these are duplicate columns or two source representations; compare existing source-calendar ablation | **Holds**; not a claim of 388 independent information sources | Same three underlying fields yield two views. Whole-frame snapshot has zero duplicate columns. Prior 200k/200k source-calendar LightGBM AUC: nominal categories 0.7790, embedding 0.7632, combination 0.7920; integer suffixes 0.6946. Joint representation is disclosed, not source reproduction | SEL-12; CLEAN-7; EV-8 |
| Implied: worth benchmarking and not a proven one-feature task | model summaries | Examine actual per-fold model and raw-user follow-up, not majority accuracy | **Holds** for learnable/nontrivial signal tested; full model-separation qualification **untested** | Native 3-fold mean AUC linear/RF/LGBM 0.7941/0.7576/0.7826 vs dummy 0.5. Train-only bounded LGBM tuning AUC 0.8655/0.7775/0.7911; raw-user model 0.8622/0.7121/0.7740. User does not match full model on every fold; full TabArena HPO absent | TP-1–4; EV-3/5/8 |
| “three refits covering a year plus May2023” | `verification.md`, Procedure Notes/code | Calendar arithmetic against dates in same file | **Refuted** | May 2023 through Apr 2024 is 12 months total: source's 11-month holdout plus May. Definition/README/C18 already say this correctly | PROV-1; EV-1 |
| Historical “26 months”, rough 24M/20GB, “fit direct”, and cancellation/time-limit interpretation | old record comments, explicitly historical | Compare source dates/counts/manifest, cleaner and target rule | 26-month arithmetic **refuted**; broad direct-fit and particular code semantics **untested**, superseded in current definition | Mar 2021–May 2023 inclusive is 27 months; exact source count 25,866,900 and bytes 27.232GB. Only zero/nonzero is verified. Old text must not be silently promoted as current evidence | USE-5/8; PROV-1; EV-2/7/8 |

**Ranked unresolved issues and mild remedies.**

1. **P3 — deployment population/action unit, unresolved rather than proven invalid (USE-1/5/8).** The strongest steelman is the current source-supported task: rank exit-state risk for released execution records on the same machine; the paper directly motivates workload decisions. The contrary evidence is real selection and multiplicity: post-run completeness is an inclusion condition, and April contains 89,593 rows in repeated `jid+adt` groups (21.31% of April), including 180 groups with conflicting labels. The evaluator therefore estimates per-record performance conditional on release inclusion, potentially weighting large execution groups many times. It does not directly estimate one decision per submitted parent job, nor recover missing submissions. Mild remedy: retain the source label and rows; explicitly describe the operator action as an example and say that scores weight released execution records, not uniquely identified parent submissions. Soften `jid` to “nonunique released identifier; precise parent/subjob semantics unresolved.” Broader all-submission or parent-job claims require a source submission census/subjob mapping; no split trick can supply it. These observations alone do not justify exclusion or deduplication.

2. **P4 — completion as label-availability proxy, plus pending recurrence review (SPLIT-9/10/30; EV-7).** Recorded end-time cutoffs pass exhaustively on native selected training rows. No independent publication timestamp is available to prove immediate reporting. Keep the explicit proxy limitation; do not invent a fixed lag without evidence. Independent measured recurrence agrees with the chosen same-system temporal use case. The supplemental temporal hidden-group probe was still outstanding at this review's evidence boundary; this report supplies no claim about its eventual outcome. Inspect its actual result before final synthesis, without treating recurrence/gap alone as leakage or changing to unseen-user evaluation.

3. **P6 — signal established, probability calibration and model separation still limited (TP-1/3; MET-1/8).** The native `drift_baseline` is a log-loss question even though primary AUC beats 0.5. The bounded tuning partly addresses divergence, but newest-to-oldest tuned log losses are 0.2202/0.4018/0.5104; in the oldest window the raw-user model's 0.4330 is better calibrated than the full model despite lower AUC. `no_spread` compares a mean skill gap 0.0729 with paired SE 0.0850 over only three windows. These are reasons to limit claims, not a metric change or automatic retirement. Mild remedy: preserve the ROC AUC fallback and report discrimination separately from calibration; keep full benchmark HPO/model-separation uncertainty explicit. No proven `Trivial`, `Too Small` or no-signal exclusion follows.

4. **P5/documentation — correct the one definite current overstatement (EV-1/7).** Replace “a year plus May2023” in verification prose with “the eleven-month source holdout plus May 2023 (twelve months total).” Preserve old record assessments as dated history while pointing to the measured current add-stage facts; no historical rewrite or verdict edit is recommended.

**Checks deliberately not claimed.** No new full definition load, container build/reload, author-baseline reproduction, full HPO, private-text reconstruction, independently verified privacy guarantee, full submission coverage test, parent/subjob recovery, future public-network availability, or completed supplemental hidden-group result. Original leak CLI failed at float32 standard-deviation underflow; recovered JSON transparently retains the printed rounded prefix and rerun float64 neighbour tail. Its 292 lower individual feature scores are not retained. The tail's agreement 0.8214 versus chance 0.8039, closest tenth 0.9480 and distance AUC 0.5308 are diagnostic evidence; they are not a complete clean native leak-CLI pass. The two tiny nonconstant coordinates are finite source values, and the repair did not change the dataset. No demonstrated source damage, generated target shortcut, or outcome-fitted representation follows from that numeric failure.

</details>

<details><summary>Historical column audit (2026-11-03)</summary>

**Column auditor — independent Phase A report, 2026-11-03**

**Verdict:** No blocking defect demonstrated in the retained 389 columns (388 predictors and the target). Keep the submission-time source representations, with the scope and dtype notes below. This is a column review, not a whole-dataset shipping decision.

**Contract and identities:** Authoritative role and full applicable principles/use_case/leak_checks/cleaning_features rules were read from vendor Data Foundry at `1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b`. Dataset and record are the selected work-checkout versions. Definition SHA256 `8684b512d50ad5aa39c6afbf012f70b8743eaa651416b7b98b8c4f522f7ec475` matches the frozen snapshot. Its recorded frame-value/order SHA256 is `2c64d4129380d494ae03e3f24a3f9ccd593f1811ce077cb6fd20c0ebfce04e5b`; this audit checks exact stored columns/values, not an independent recomputation of that framework frame hash.

**Version reconciliation:** The newer checkout role adds a dtype-probe CLI requirement absent from the pinned role. The pinned vendor has neither `dtype_probes.py` nor its `curation_probes/dtypes.py` implementation. Pinned CLEAN-14 still requires semantic typing but lacks the newer ordinal/default/codebook/probe additions. Newer LEAK-10 adds conditional-window and late-value exceptions, newer LEAK-13/15 expands class-format/batch rules, and newer USE-8 adds explicit selection-fit guidance. None changes this column verdict: no late predictors are retained, no outcome-window statistic is retained, and original latent coordinates remain numeric. CLEAN-22 and USE-6, relevant to the omitted-resource scope question, are unchanged. Principles are byte-identical.

**Execution:** Independently streamed all 2,500,499 saved-frame rows in 306 full-width Arrow batches, checked all 389 dtypes against the snapshot, and invoked the actually pinned native `_check_dataset_frame` and `_check_target` guards on every batch. Result: zero native findings, zero missing cells, zero nonfinite embedding values, no constant numeric columns and no identical numeric-column SHA256 groups; the datetime is monotonically increasing. Native target guards inspect batches; aggregate class/missing counts are independently accumulated over the complete frame. The initial run peaked at **2578 MiB**, exceeding the requested 2 GiB coordination preference; this is disclosed, not claimed compliant. A narrower rerun was interrupted after two projections at the coordinator's direction to prioritize the completed report; it is not additional complete evidence. No definition reload, model fit, upstream mutation or dataset rewrite occurred. `dataset_io.py` was inspected; its full-definition loader was deliberately replaced by the coordinator-authorized exact final-frame snapshot for bounded independent inspection.

**Supplementary dtype probe:** Also executed the newer checkout's `curation_probes.dtypes.column_table` and `flagged` functions, one full-length exact column projection at a time, with the local publisher codebook plus explicit real-valued coordinate entries. Implementation SHA256 `803e454cdb1af8d49c3ac52cf45a1190a79e68d148c2a787cd81e511ba3773f1`; CLI wrapper SHA256 `53aa763d97af2aa51236b155de748413f7a3740fc76c2bcc1592714c179cbc09`. This is supplementary newer tooling, **not a pinned gate or CLI run**. It examined all 388 predictors; by design its output covers 387 categorical/numeric columns, excludes the target and skips the datetime. **Zero flags**. Independent date/target checks above cover those omitted roles. Peak RSS414 MiB.

**Primary evidence:** Publisher feature list and paper Table2 / Methods / Technical Validation, plus author `clean_and_anonmyze_data.py`, `generate_derived_features.py` and `baseline_experiments.py`, pinned author commit `db67a65a4b6e91dcebd26147de191fa0051ad790`. The encoder consumes only original `usr_or`, `jnam_or`, `jobenv_req_or`, uses pretrained all-MiniLM-L6-v2 and does not fit on this release's labels. Expanding its 384 stored coordinates fits no encoder. Individual latent-coordinate meanings are **unknown**; that is stated in every row rather than inventing measurements. Paper/source code support availability of the underlying strings at submission; they do not independently expose the private database's full change log. Public sources: [paper](https://doi.org/10.1038/s41597-025-05633-1), [fixed release](https://doi.org/10.5281/zenodo.11467483), [author code](https://github.com/francescoantici/F-DATA/tree/db67a65a4b6e91dcebd26147de191fa0051ad790).

**Per-column table:** Every physical column is enumerated once in exact snapshot order. “Yes, source-supported” means a fixed input-only representation can be formed at submission, not that this reviewer accessed private source strings. Numeric ranges below are exact scanned float32 extrema; negative and very small coordinates are legitimate latent values. No new scaling/imputation is warranted.

| Column | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `usr` | Stable masked submitting-user identity | Yes, source-supported | category; 2,781 levels, no nulls/literal missing proxies; not an ordered quantity | Fine | USE-10; LEAK-34; CLEAN-4/14 |
| `jnam` | Stable masked job-name identity; original free text unavailable | Yes, source-supported | category; 359,636 levels, no nulls/literal missing proxies; high cardinality note Q3 | Fine with dtype note Q3 | CLEAN-14 (Should); USE-1/10; LEAK-34 |
| `jobenv_req` | Stable masked requested job-environment identity | Yes, source-supported | category; 4 levels, no nulls/literal missing proxies; no ordering | Fine | USE-3; LEAK-10; CLEAN-14 |
| `embedding_000` | Coordinate 0 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.180876, 0.11201] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_001` | Coordinate 1 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1818668, 0.1283703] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_002` | Coordinate 2 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2123353, 0.09931392] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_003` | Coordinate 3 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1924075, 0.1358613] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_004` | Coordinate 4 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1488604, 0.2144028] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_005` | Coordinate 5 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1854399, 0.08473557] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_006` | Coordinate 6 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1621371, 0.1062793] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_007` | Coordinate 7 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09766247, 0.2071697] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_008` | Coordinate 8 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1773856, 0.1035268] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_009` | Coordinate 9 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1883061, 0.113292] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_010` | Coordinate 10 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09334016, 0.2073423] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_011` | Coordinate 11 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1820198, 0.1201165] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_012` | Coordinate 12 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2115648, 0.08934817] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_013` | Coordinate 13 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1536418, 0.1185855] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_014` | Coordinate 14 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1938939, 0.09319228] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_015` | Coordinate 15 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1484645, 0.1765369] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_016` | Coordinate 16 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1865383, 0.1468052] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_017` | Coordinate 17 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.189383, 0.08689253] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_018` | Coordinate 18 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1188146, 0.1978614] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_019` | Coordinate 19 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1588795, 0.1807677] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_020` | Coordinate 20 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1784865, 0.1397425] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_021` | Coordinate 21 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1340855, 0.1575733] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_022` | Coordinate 22 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1348359, 0.1550464] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_023` | Coordinate 23 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1543443, 0.1267538] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_024` | Coordinate 24 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09697916, 0.1558348] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_025` | Coordinate 25 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1861526, 0.1201585] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_026` | Coordinate 26 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1365361, 0.1782831] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_027` | Coordinate 27 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1052755, 0.2005411] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_028` | Coordinate 28 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1733911, 0.1508146] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_029` | Coordinate 29 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2292729, 0.08005076] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_030` | Coordinate 30 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09330726, 0.2171672] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_031` | Coordinate 31 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1201803, 0.1692037] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_032` | Coordinate 32 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1807454, 0.1378355] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_033` | Coordinate 33 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1614813, 0.1260666] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_034` | Coordinate 34 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.08762819, 0.2235059] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_035` | Coordinate 35 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.08754033, 0.2492716] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_036` | Coordinate 36 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1301724, 0.2022719] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_037` | Coordinate 37 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2490153, 0.07919412] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_038` | Coordinate 38 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1973144, 0.1085646] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_039` | Coordinate 39 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.171389, 0.1101384] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_040` | Coordinate 40 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1325882, 0.1894105] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_041` | Coordinate 41 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1343777, 0.1313858] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_042` | Coordinate 42 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1192477, 0.1949777] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_043` | Coordinate 43 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.112927, 0.1989766] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_044` | Coordinate 44 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1322439, 0.1796107] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_045` | Coordinate 45 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09925783, 0.1828905] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_046` | Coordinate 46 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1550591, 0.1462643] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_047` | Coordinate 47 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1154135, 0.1643215] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_048` | Coordinate 48 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1004968, 0.1483973] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_049` | Coordinate 49 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1682315, 0.1477089] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_050` | Coordinate 50 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1645418, 0.1217434] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_051` | Coordinate 51 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09141926, 0.2360994] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_052` | Coordinate 52 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1147394, 0.1562886] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_053` | Coordinate 53 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1835926, 0.1271206] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_054` | Coordinate 54 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1332684, 0.2070955] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_055` | Coordinate 55 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1707885, 0.1066102] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_056` | Coordinate 56 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1956647, 0.1096048] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_057` | Coordinate 57 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1356676, 0.2028199] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_058` | Coordinate 58 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1181904, 0.1793419] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_059` | Coordinate 59 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2008801, 0.1435137] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_060` | Coordinate 60 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1214227, 0.1856545] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_061` | Coordinate 61 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1354486, 0.1716046] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_062` | Coordinate 62 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1496763, 0.1521952] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_063` | Coordinate 63 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1186536, 0.14651] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_064` | Coordinate 64 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1621376, 0.1610097] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_065` | Coordinate 65 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1438249, 0.1274008] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_066` | Coordinate 66 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1306398, 0.1667103] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_067` | Coordinate 67 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2165259, 0.08047042] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_068` | Coordinate 68 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1728076, 0.124895] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_069` | Coordinate 69 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1307275, 0.1780796] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_070` | Coordinate 70 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1935674, 0.1218796] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_071` | Coordinate 71 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.138284, 0.1279528] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_072` | Coordinate 72 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.174449, 0.2420114] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_073` | Coordinate 73 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1550876, 0.1630112] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_074` | Coordinate 74 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1853158, 0.1649615] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_075` | Coordinate 75 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1321233, 0.1753946] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_076` | Coordinate 76 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1503694, 0.1258952] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_077` | Coordinate 77 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1650484, 0.1218388] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_078` | Coordinate 78 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1452632, 0.170269] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_079` | Coordinate 79 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1898782, 0.1093565] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_080` | Coordinate 80 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1640015, 0.1772834] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_081` | Coordinate 81 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1596964, 0.1193841] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_082` | Coordinate 82 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1671985, 0.1329792] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_083` | Coordinate 83 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2056145, 0.1247355] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_084` | Coordinate 84 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1495498, 0.1407974] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_085` | Coordinate 85 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1146404, 0.195379] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_086` | Coordinate 86 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1660776, 0.140979] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_087` | Coordinate 87 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1340266, 0.1359039] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_088` | Coordinate 88 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1618759, 0.1989022] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_089` | Coordinate 89 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1834724, 0.1383988] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_090` | Coordinate 90 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1216864, 0.1920135] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_091` | Coordinate 91 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1524876, 0.1145877] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_092` | Coordinate 92 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1784218, 0.1742453] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_093` | Coordinate 93 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1014267, 0.1528879] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_094` | Coordinate 94 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.179651, 0.1281503] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_095` | Coordinate 95 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.0996425, 0.1604593] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_096` | Coordinate 96 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1093443, 0.2354192] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_097` | Coordinate 97 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.131488, 0.2238267] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_098` | Coordinate 98 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1928235, 0.09445985] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_099` | Coordinate 99 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.03996554, 0.1657972] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_100` | Coordinate 100 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1858407, 0.136697] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_101` | Coordinate 101 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1544627, 0.1461584] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_102` | Coordinate 102 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1797691, 0.1631328] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_103` | Coordinate 103 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.121107, 0.2081194] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_104` | Coordinate 104 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1541709, 0.1731049] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_105` | Coordinate 105 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1182158, 0.1729951] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_106` | Coordinate 106 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1741259, 0.1433744] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_107` | Coordinate 107 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1357988, 0.1773079] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_108` | Coordinate 108 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1569399, 0.1362287] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_109` | Coordinate 109 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2097341, 0.1147822] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_110` | Coordinate 110 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1178387, 0.1959237] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_111` | Coordinate 111 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1576813, 0.1380793] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_112` | Coordinate 112 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1967161, 0.1197041] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_113` | Coordinate 113 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1591324, 0.1279828] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_114` | Coordinate 114 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1055811, 0.2186769] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_115` | Coordinate 115 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1684457, 0.206332] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_116` | Coordinate 116 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1582187, 0.1241078] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_117` | Coordinate 117 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1318282, 0.1806174] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_118` | Coordinate 118 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1473459, 0.1221457] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_119` | Coordinate 119 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1783378, 0.1112046] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_120` | Coordinate 120 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1990665, 0.1150903] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_121` | Coordinate 121 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2060798, 0.1215455] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_122` | Coordinate 122 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2084792, 0.1094834] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_123` | Coordinate 123 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1641217, 0.1585407] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_124` | Coordinate 124 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2141639, 0.1155916] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_125` | Coordinate 125 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.164309, 0.13013] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_126` | Coordinate 126 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1948058, 0.1521154] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_127` | Coordinate 127 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-3.752856e-33, 1.837042e-32] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_128` | Coordinate 128 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09642281, 0.2295485] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_129` | Coordinate 129 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1825074, 0.1376265] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_130` | Coordinate 130 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1670224, 0.1590368] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_131` | Coordinate 131 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1151943, 0.2180749] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_132` | Coordinate 132 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1221047, 0.1860843] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_133` | Coordinate 133 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1708107, 0.1473579] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_134` | Coordinate 134 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1576231, 0.1279534] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_135` | Coordinate 135 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1834176, 0.1069456] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_136` | Coordinate 136 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1988696, 0.09792034] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_137` | Coordinate 137 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1402557, 0.176069] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_138` | Coordinate 138 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1664707, 0.145567] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_139` | Coordinate 139 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1851351, 0.1164755] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_140` | Coordinate 140 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1469056, 0.1323441] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_141` | Coordinate 141 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1265253, 0.2181012] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_142` | Coordinate 142 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1624587, 0.1518676] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_143` | Coordinate 143 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2065625, 0.1472833] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_144` | Coordinate 144 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1261056, 0.2092466] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_145` | Coordinate 145 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1356824, 0.1389093] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_146` | Coordinate 146 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1545937, 0.172452] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_147` | Coordinate 147 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1223108, 0.1695405] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_148` | Coordinate 148 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1017884, 0.2228405] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_149` | Coordinate 149 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1137274, 0.1756745] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_150` | Coordinate 150 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1796338, 0.1037951] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_151` | Coordinate 151 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.166828, 0.1322566] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_152` | Coordinate 152 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1036817, 0.2034131] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_153` | Coordinate 153 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1039352, 0.2183302] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_154` | Coordinate 154 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1410708, 0.1496886] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_155` | Coordinate 155 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1729689, 0.1285957] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_156` | Coordinate 156 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.08304919, 0.231508] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_157` | Coordinate 157 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.07092414, 0.1029183] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_158` | Coordinate 158 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1762595, 0.135415] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_159` | Coordinate 159 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1383528, 0.1381482] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_160` | Coordinate 160 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1739316, 0.1008892] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_161` | Coordinate 161 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1851379, 0.1556847] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_162` | Coordinate 162 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.184524, 0.1350926] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_163` | Coordinate 163 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2191808, 0.09230767] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_164` | Coordinate 164 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1748959, 0.1404926] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_165` | Coordinate 165 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09773599, 0.1511304] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_166` | Coordinate 166 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1652346, 0.1074145] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_167` | Coordinate 167 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1725797, 0.1381065] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_168` | Coordinate 168 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1285463, 0.1656134] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_169` | Coordinate 169 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09191144, 0.1864933] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_170` | Coordinate 170 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1993573, 0.1373753] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_171` | Coordinate 171 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1511139, 0.1333784] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_172` | Coordinate 172 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.07457084, 0.2311944] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_173` | Coordinate 173 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1691898, 0.1107276] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_174` | Coordinate 174 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1427771, 0.1844724] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_175` | Coordinate 175 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.08254025, 0.190071] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_176` | Coordinate 176 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1131703, 0.1862408] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_177` | Coordinate 177 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1334024, 0.1921437] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_178` | Coordinate 178 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1832209, 0.1132902] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_179` | Coordinate 179 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1276354, 0.1358403] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_180` | Coordinate 180 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1923338, 0.1755022] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_181` | Coordinate 181 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1639964, 0.1399004] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_182` | Coordinate 182 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1460042, 0.130822] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_183` | Coordinate 183 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.211693, 0.06442773] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_184` | Coordinate 184 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1599203, 0.1323915] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_185` | Coordinate 185 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1472166, 0.1686409] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_186` | Coordinate 186 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1353318, 0.1200878] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_187` | Coordinate 187 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1155327, 0.219785] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_188` | Coordinate 188 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1073862, 0.2137375] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_189` | Coordinate 189 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09560403, 0.2108531] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_190` | Coordinate 190 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1368023, 0.1297676] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_191` | Coordinate 191 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1601761, 0.1279785] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_192` | Coordinate 192 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1211115, 0.1799483] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_193` | Coordinate 193 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1812976, 0.1391198] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_194` | Coordinate 194 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1922083, 0.141892] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_195` | Coordinate 195 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1636282, 0.1378098] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_196` | Coordinate 196 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1576805, 0.1694368] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_197` | Coordinate 197 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.103178, 0.2154925] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_198` | Coordinate 198 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1672328, 0.09903606] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_199` | Coordinate 199 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1748911, 0.1301325] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_200` | Coordinate 200 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.0898036, 0.2426871] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_201` | Coordinate 201 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.06149862, 0.2464301] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_202` | Coordinate 202 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1262315, 0.1718453] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_203` | Coordinate 203 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1436778, 0.1322029] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_204` | Coordinate 204 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1522373, 0.1976715] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_205` | Coordinate 205 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1549588, 0.1240769] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_206` | Coordinate 206 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1576519, 0.1545169] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_207` | Coordinate 207 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1314413, 0.1411062] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_208` | Coordinate 208 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2175255, 0.1292744] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_209` | Coordinate 209 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1004099, 0.1701238] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_210` | Coordinate 210 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1890125, 0.1048562] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_211` | Coordinate 211 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1967983, 0.1386588] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_212` | Coordinate 212 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1897412, 0.1603728] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_213` | Coordinate 213 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1767296, 0.1483794] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_214` | Coordinate 214 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.183659, 0.1365619] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_215` | Coordinate 215 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1693553, 0.1155005] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_216` | Coordinate 216 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1607149, 0.1322211] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_217` | Coordinate 217 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1240984, 0.1974992] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_218` | Coordinate 218 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1204757, 0.1935809] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_219` | Coordinate 219 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1923176, 0.1666111] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_220` | Coordinate 220 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1366846, 0.2036663] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_221` | Coordinate 221 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1401989, 0.1656417] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_222` | Coordinate 222 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2096822, 0.1098112] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_223` | Coordinate 223 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-1.853761e-32, 1.324199e-33] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_224` | Coordinate 224 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1656704, 0.1203094] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_225` | Coordinate 225 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1106881, 0.1546047] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_226` | Coordinate 226 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1592587, 0.166203] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_227` | Coordinate 227 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2108156, 0.1346492] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_228` | Coordinate 228 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.167545, 0.09993516] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_229` | Coordinate 229 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1008317, 0.1672624] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_230` | Coordinate 230 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1597803, 0.1270813] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_231` | Coordinate 231 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1933029, 0.1797101] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_232` | Coordinate 232 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.16176, 0.166006] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_233` | Coordinate 233 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1556719, 0.1788854] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_234` | Coordinate 234 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1412881, 0.1844932] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_235` | Coordinate 235 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1486839, 0.1531404] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_236` | Coordinate 236 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1237568, 0.1763167] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_237` | Coordinate 237 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.189987, 0.1091046] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_238` | Coordinate 238 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1067963, 0.2167653] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_239` | Coordinate 239 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1507368, 0.1397377] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_240` | Coordinate 240 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1467063, 0.1397441] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_241` | Coordinate 241 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.145417, 0.1677734] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_242` | Coordinate 242 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1447334, 0.2143416] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_243` | Coordinate 243 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1421978, 0.1472435] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_244` | Coordinate 244 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1495853, 0.1601188] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_245` | Coordinate 245 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.05438969, 0.2388762] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_246` | Coordinate 246 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1528016, 0.1563626] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_247` | Coordinate 247 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1527356, 0.1649731] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_248` | Coordinate 248 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1437663, 0.1566999] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_249` | Coordinate 249 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1320913, 0.1770043] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_250` | Coordinate 250 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1219891, 0.180965] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_251` | Coordinate 251 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1251524, 0.2163541] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_252` | Coordinate 252 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1579356, 0.1342332] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_253` | Coordinate 253 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1479, 0.1723566] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_254` | Coordinate 254 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1749962, 0.1819288] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_255` | Coordinate 255 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1401353, 0.1951409] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_256` | Coordinate 256 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1804233, 0.1041513] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_257` | Coordinate 257 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.07602412, 0.1915893] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_258` | Coordinate 258 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1178974, 0.193541] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_259` | Coordinate 259 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1397772, 0.1290715] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_260` | Coordinate 260 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1300187, 0.1810513] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_261` | Coordinate 261 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1554395, 0.1452023] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_262` | Coordinate 262 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1831813, 0.1265285] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_263` | Coordinate 263 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1700141, 0.1110125] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_264` | Coordinate 264 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1238033, 0.1834499] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_265` | Coordinate 265 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1580334, 0.2080899] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_266` | Coordinate 266 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1999435, 0.1135229] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_267` | Coordinate 267 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1145535, 0.1885575] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_268` | Coordinate 268 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1555586, 0.1206457] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_269` | Coordinate 269 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1550953, 0.1640047] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_270` | Coordinate 270 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1466603, 0.1794999] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_271` | Coordinate 271 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1697428, 0.1420045] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_272` | Coordinate 272 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1966897, 0.1124455] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_273` | Coordinate 273 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2366934, 0.1043942] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_274` | Coordinate 274 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1259716, 0.1541787] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_275` | Coordinate 275 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1647228, 0.1311768] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_276` | Coordinate 276 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.142413, 0.1691847] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_277` | Coordinate 277 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1147139, 0.1779653] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_278` | Coordinate 278 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1547692, 0.1291161] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_279` | Coordinate 279 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1642572, 0.1564806] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_280` | Coordinate 280 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1476625, 0.2201847] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_281` | Coordinate 281 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09637076, 0.2163943] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_282` | Coordinate 282 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.176542, 0.175573] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_283` | Coordinate 283 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1414307, 0.1414178] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_284` | Coordinate 284 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1240743, 0.1619385] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_285` | Coordinate 285 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1554775, 0.1592722] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_286` | Coordinate 286 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1528673, 0.1386399] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_287` | Coordinate 287 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1693842, 0.1597283] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_288` | Coordinate 288 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1629632, 0.1465517] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_289` | Coordinate 289 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1895573, 0.09587523] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_290` | Coordinate 290 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2528889, 0.1146087] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_291` | Coordinate 291 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1703176, 0.1902059] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_292` | Coordinate 292 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1353338, 0.1699012] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_293` | Coordinate 293 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1490592, 0.1871816] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_294` | Coordinate 294 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1785016, 0.1128384] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_295` | Coordinate 295 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1532047, 0.1512048] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_296` | Coordinate 296 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1345823, 0.1667265] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_297` | Coordinate 297 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1163471, 0.1744518] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_298` | Coordinate 298 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1445023, 0.15119] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_299` | Coordinate 299 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1466362, 0.1631378] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_300` | Coordinate 300 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2077097, 0.09078656] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_301` | Coordinate 301 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1318607, 0.1469028] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_302` | Coordinate 302 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1560033, 0.111011] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_303` | Coordinate 303 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1509032, 0.1644567] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_304` | Coordinate 304 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1855861, 0.133706] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_305` | Coordinate 305 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1315105, 0.1650462] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_306` | Coordinate 306 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1309474, 0.1544432] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_307` | Coordinate 307 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.0959398, 0.1869495] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_308` | Coordinate 308 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.189775, 0.1555853] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_309` | Coordinate 309 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1599311, 0.12836] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_310` | Coordinate 310 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1045291, 0.1926664] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_311` | Coordinate 311 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.07840351, 0.1992951] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_312` | Coordinate 312 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1037013, 0.1606549] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_313` | Coordinate 313 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1992786, 0.1261218] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_314` | Coordinate 314 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1341985, 0.1408801] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_315` | Coordinate 315 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1446166, 0.1576852] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_316` | Coordinate 316 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1462276, 0.154441] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_317` | Coordinate 317 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.07190011, 0.2155968] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_318` | Coordinate 318 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1740266, 0.1503001] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_319` | Coordinate 319 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-5.677104e-08, -1.516795e-08] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_320` | Coordinate 320 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.09896339, 0.1872556] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_321` | Coordinate 321 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1777936, 0.1308779] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_322` | Coordinate 322 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.165939, 0.1499364] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_323` | Coordinate 323 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1395751, 0.1335203] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_324` | Coordinate 324 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1178394, 0.185907] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_325` | Coordinate 325 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1570929, 0.1480913] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_326` | Coordinate 326 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1664356, 0.1479231] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_327` | Coordinate 327 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1643176, 0.1803961] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_328` | Coordinate 328 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1540664, 0.1256025] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_329` | Coordinate 329 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1501586, 0.1520917] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_330` | Coordinate 330 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1809223, 0.2013978] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_331` | Coordinate 331 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.140799, 0.1695541] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_332` | Coordinate 332 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1580304, 0.1359123] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_333` | Coordinate 333 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1801235, 0.1327326] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_334` | Coordinate 334 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.131127, 0.1664775] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_335` | Coordinate 335 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1426232, 0.1744367] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_336` | Coordinate 336 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.201266, 0.1086553] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_337` | Coordinate 337 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.104099, 0.2048567] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_338` | Coordinate 338 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1150472, 0.0862922] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_339` | Coordinate 339 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1658617, 0.1431501] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_340` | Coordinate 340 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1234203, 0.164238] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_341` | Coordinate 341 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1620792, 0.1418934] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_342` | Coordinate 342 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1461012, 0.1218947] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_343` | Coordinate 343 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2034237, 0.1143459] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_344` | Coordinate 344 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1491968, 0.1365024] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_345` | Coordinate 345 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1449301, 0.1469281] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_346` | Coordinate 346 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.07325447, 0.2051452] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_347` | Coordinate 347 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1430459, 0.1625364] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_348` | Coordinate 348 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1768519, 0.1213164] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_349` | Coordinate 349 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1498732, 0.1054178] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_350` | Coordinate 350 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1819596, 0.1243685] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_351` | Coordinate 351 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1244789, 0.17781] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_352` | Coordinate 352 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2099288, 0.1244816] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_353` | Coordinate 353 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.169161, 0.1087894] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_354` | Coordinate 354 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1393633, 0.1891135] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_355` | Coordinate 355 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1365881, 0.1682709] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_356` | Coordinate 356 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1863479, 0.142506] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_357` | Coordinate 357 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1270757, 0.1998253] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_358` | Coordinate 358 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1745278, 0.2005375] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_359` | Coordinate 359 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2031667, 0.1029897] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_360` | Coordinate 360 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1643906, 0.1239995] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_361` | Coordinate 361 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1108392, 0.1939043] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_362` | Coordinate 362 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1518658, 0.1225585] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_363` | Coordinate 363 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.0949853, 0.1242699] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_364` | Coordinate 364 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.176507, 0.1534484] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_365` | Coordinate 365 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1517145, 0.138235] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_366` | Coordinate 366 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1826994, 0.1142279] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_367` | Coordinate 367 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1639029, 0.1833611] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_368` | Coordinate 368 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1444254, 0.1346938] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_369` | Coordinate 369 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1515412, 0.1778609] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_370` | Coordinate 370 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1630572, 0.1242509] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_371` | Coordinate 371 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1527582, 0.1495636] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_372` | Coordinate 372 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.158905, 0.1262801] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_373` | Coordinate 373 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1954818, 0.1370567] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_374` | Coordinate 374 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1803072, 0.1393378] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_375` | Coordinate 375 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1988736, 0.0849824] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_376` | Coordinate 376 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.2475298, 0.05047776] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_377` | Coordinate 377 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1386388, 0.1813802] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_378` | Coordinate 378 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1749637, 0.1118316] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_379` | Coordinate 379 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1904072, 0.1542658] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_380` | Coordinate 380 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1449499, 0.2125899] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_381` | Coordinate 381 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1422439, 0.1433506] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_382` | Coordinate 382 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1696566, 0.1056501] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `embedding_383` | Coordinate 383 of original user/job-name/requested-environment pretrained embedding; latent meaning unknown | Yes, source-supported | float32; finite, no nulls, nonconstant; [-0.1402641, 0.1232124] | Fine | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `adt` | Actual job submission instant, also temporal split index | Yes, at submission | datetime64[ns]; no missing, ordered; instants converted to Asia/Tokyo before removing timezone | Fine | USE-3; CLEAN-14/23; LEAK-37 |
| `exit state` | Publisher terminal ec==0 completed versus nonzero failed | No; target only, never predictor | category; 2,224,912 completed, 275,587 failed; no missing; no merged/dropped class | Fine as terminal target | USE-5; LEAK-10; CLEAN-15/17 |

**Problems and curator questions in principle order**

1. **Q1 — P3/P4: cohort and operational snapshot limits, already disclosed; no new retained-column leak.** The operator scores at submission before queue insertion/scheduling/execution. Source data cleaning selects rows with recorded post-run measurements. The public cohort cannot quantify excluded early failures or pending submissions. The existing approximate-fit explanation is warranted; this audit cannot certify coverage of all submissions. Values of user/name/requested environment are source-supported submission inputs, and the ordinary alteration list does not include those names, but private snapshot semantics remain unavailable. Mildest remedy: preserve the explicit released-execution cohort and original zero/nonzero target limitations; revisit if authoritative change-history evidence contradicts their initial availability. No speculative relabelling, timing inference or new `Potential leak` designation is justified by absence of private evidence alone. Rules USE-1/3/5/8 and LEAK-10/22–26.

2. **Q2 — P3/P5/P7: decide source-representation scope explicitly, not by pretending all omitted request quantities leak.** The paper names requested cores `cnumr`, nodes `nnumr`, memory `mszl` and frequency `freq_req` as submission inputs. They are absent because the source validation uses name/user/environment representations, and the curator authorized investigating those first. That is a real task-fidelity argument, and there is no evidence that width/runtime motivated these four omissions. Conversely USE-6 and CLEAN-22 protect relevant known inputs; preserving a published baseline is not blanket authority to discard operational inputs from a broader submission-triage task. The current version already combines source representations and adds time, so it is an adaptation rather than an exact reproduction. Mildest remedy: curator affirm this as the named source-representation version and keep that qualification in task changes, or authorize a later explicitly broader version after checking the released resource snapshots and dtypes. Do not silently add them or call them proved leaks. `elpl` and `pri` are a separate uncertainty: the official job manual permits post-submission alterations, so requested does not establish their released initial values; keep them excluded unless initial versions are verified. [Fujitsu job-operation manual](https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf), sections1.7.2/2.5.4. This is a curator scope question, not a demonstrated retained-feature defect or an automatic veto.

3. **Q3 — P7: explain high-cardinality masked `jnam` as an intentional CLEAN-14 departure.** The pinned rule defaults high-cardinality values to string; 359,636 distinct masked names are high cardinality. Here the source deliberately replaces real names with stable opaque tokens, and the published integer representation treats them as nominal identities. Treating those tokens as text cannot recover the private names and may invent semantics from their arbitrary suffixes. Category is therefore defensible for source-task fidelity (USE-1/10, LEAK-34), with an explicit short exception/note. `usr` has2,781 levels and the same nominal meaning; environment has4. Mildest remedy: document the categorical choice rather than numeric ordinal codes or reconstructed text. No mandatory dtype change is demonstrated; zero supplementary numeric/count/code flags does not decide this semantic Should-rule question.

**Exclusion sweep:** All allocated/used cores/nodes/memory/frequency; queue/scheduled/start/end/deletion timestamps; exit code; elapsed duration; idle time; CPU-use counters; perf1–perf6; flops, bandwidth, operational intensity and pclass; power and energy fields are absent from the389 final columns. These are later execution/scheduling/outcome measurements and must not enter the at-submission predictors (LEAK-10 Must). End time/exit code enter only upstream availability/target checks and are absent from this final-frame scan. The storage/parent job ID and `_source_file`, `_source_row`, `_split_roles` are also absent. Stable user/name identities are legitimate recurring-entity inputs under the temporal use case, not group-metadata columns. No target encoding or full-release learned feature transform is introduced. Source learned embeddings are retained published input-only features; CLEAN-6 forbids building such features during curation, not mechanically exposing the source's existing coordinates.

**Tiny coordinates:** `embedding_127` ranges from approximately−3.75e−33 to1.84e−32, `embedding_223` from−1.85e−32 to1.32e−33. Both are finite and nonconstant over the entire exact frame. The probe's float32 variance/normalization underflow is not source corruption and does not authorize dropping dimensions, rounding them to zero, or rescaling the dataset. Preserve all384 coordinates (CLEAN-5/14/22, LEAK-29).

**Evidence boundaries:** This independent review did not reproduce the full raw 38-file digest/row-unit/label audit or model probes. Their reported results remain separate evidence in verification and source-reconciliation artifacts. Existing `column-dtype-audit.py/json` were not treated as independent proof; the all-column scan and supplementary probe above were executed afresh. Source anonymization can mask the private meanings of missing originals, so literal proxy absence is not proof that private originals were all complete. No mapping or raw identifying row is reconstructed.

**Artifacts:** `column-auditor-independent.py`, `column-auditor-independent-wide-attempt.json` (complete exact scan, actual peak disclosed), `column-auditor-independent.json` (same completed result), `column-auditor-projected-attempt.py` (interrupted follow-up, not passed evidence), `column-auditor-dtype-probe.py/json` (complete supplementary newer probe). Repository source remained read-only. This scoped audit contributes evidence for the overall curation decision.

</details>

<details><summary>Historical split audit (2026-11-03)</summary>

**Split verdict: right with notes.** The temporal regime correctly tests future released execution records on Fugaku with recurring users and workloads. No measured split violation requires regrouping, deduplication, an extra embargo, or a changed target. The principal limitation is the source-selected cohort, followed by incomplete parent/subjob identity and the judgment involved in adopting four-month refits. These remain visible qualifications, not established reasons to replace the split.

**Reviewed identity and evidence.** Runtime/instruction pin `1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b`; work checkout head `0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8`; reviewed definition SHA256 `8684b512d50ad5aa39c6afbf012f70b8743eaa651416b7b98b8c4f522f7ec475`. Read `dataset.py`, generated `README.md`, `fugaku_hpc_job_failure.md`, the full split/use-case/evidence/principles references, `verification.md`, `snapshot.json`, native task results, `flag-followup.json`, `leak-probes.log`, recovered leak JSON, source-reference results, source paper body and pinned author scripts. `split-audit-narrow.py` independently verified the saved final row order against source-position membership dates/labels, all six split-index hashes against `snapshot.json`, train/test disjointness, calendar bounds and training completion before cutoff. It streamed only two full-source metadata columns and read selected identity columns; peak RSS was 888,340 KiB. No pipeline reload, dense whole-frame load, build, repository edit or curator decision was made.

**Prediction point and unit.** Submission time `adt` means submission, not scheduling, start or completion. Convert timestamp instants to Japanese calendar time before deriving windows. Inputs are the submission-time user/name/environment representations, their published pretrained embedding, and submission time. End time serves only training-label availability. One prediction is one released execution record's eventual source exit state; four months describes the period between refits, not a deadline after which unfinished jobs are called successful or failed. The original zero/nonzero target is retained.

**Measured calendar and support.** Newest window first; every shipped side has 1,000,000 train and 500,000 test rows.

| Test period | Eligible history after maturity | Share of all 25,866,900 source rows | Excluded unavailable training labels | Failed test rows |
|---|---:|---:|---:|---:|
| January–April 2024 | 23,534,772 | 90.984% | 28,118 | 59,253 |
| September–December 2023 | 20,777,457 | 80.324% | 48,375 | 74,610 |
| May–August 2023 | 16,896,791 | 65.322% | 10,387 | 57,135 |

All three histories start in March 2021, exceed the 50% full-source floor after availability filtering, and include more than two annual cycles before their cutoffs. Each sampled test calendar month has at least 77,945 rows. The three windows collectively span a full year, so most windows are not repeats of one seasonal slice. Strict chronology and no equal-time crossing hold. Earlier test periods can legitimately supply mature labels to later refits; that is an expanding operational evaluation, and the three scores are not independent experiments. The native proportional 1M/500k cap follows full-cohort calendar construction and maturity filtering; a 2,500,499-row retained union is not the denominator for the pre-cap 50% rule. Sampling does not balance classes. Evidence: `selection.json`, `snapshot.json`, `split-audit-narrow.json`; rules SPLIT-2/9/11/14/15/17 and the native `_1m` protocol.

**Ranked finding 1 — P3/P4, cohort qualification; concern, not a demonstrated wrong split.** The author cleaner requires nonempty valid submission/start/end times and many performance, power and resource fields, so the benchmark is conditional on recorded instrumented executions. Zero label/code mismatches across 25,866,900 released rows establishes the released target, not complete coverage of attempted submissions. April 2024 starts on April 4, and recorded completions extend to May 14; the tail diagnostic includes observed delays up to 27.69 days. This refutes a simple claim that April outcomes stop on April 30, but cannot count absent pending or early-failure jobs, establish all-submission completeness, or prove absence of outcome-dependent selection. No second raw extraction is public here. Rules USE-1/5/8, EV-2/7; censoring is a question under the `drift_baseline` reading, not proven merely by a changing class share. **Mildest remedy:** retain approximate fit and the explicit released-cohort restriction already in the definition. No evidence currently selects a defensible earlier truncation month. Broad all-attempted-submission inference remains cannot-verify. Evidence: `clean_and_anonmyze_data.py`, `full-release-summary.json`, `release-tail-april2024.json`, [source release](https://doi.org/10.5281/zenodo.11467483).

**Ranked finding 2 — P3/P4, recurring identities and parent/subjob unit; qualified pass.** The use case predicts later submissions on the same system, not first-ever users or new sites. On the actual capped test sides, identities seen in train are:

| Identity | January–April 2024 | September–December 2023 | May–August 2023 |
|---|---:|---:|---:|
| User | 97.981% | 95.084% | 74.121% |
| Job name | 49.772% | 49.833% | 47.992% |
| Environment | 99.9998% | 100% | 100% |
| Masked job ID, excluded from predictors | 0.0256% | 0.0120% | 0.0050% |

These independently measured recurrences support a mixture of known and new workloads; forcing user/name groups to opposite sides would answer a different cold-start question. The label is per execution, not one immutable label per user or parent ID. The April 2021 source audit found 5,008 repeated IDs, 4,674 with different submission times and 308 with both labels. Full-release exact 44-field duplicates are zero. The projected-duplicate source trace found distinct execution timings in all 38 inspected pairs, although it does not resolve every bulk/step/retry relationship. The [Fujitsu/RIKEN manual](https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf), section 1.4, distinguishes parent job IDs from subjob identifiers; the public release does not retain the latter. Therefore finer identity and the exact relationship of every execution to a parent-level triage action remain unknown. Rules USE-10, SPLIT-1/3/4/13/23/24/26, EV-3. **Mildest remedy:** retain execution rows and temporal evaluation, excluded `jid`, and the explicit identity limit. Do not aggregate conflicting outcomes, deduplicate by parent ID, or invent similarity/hash groups. Evidence: `split-audit-narrow.json`, `first-file-row-unit-audit.json`, `row-unit-source-reconciliation.md`, `projected-duplicate-source-trace.json`.

The leak prefix reports 25.5% exact predictor-profile overlap when date is omitted and 0% when date is included. The repaired float64 diagnostic gives nearest-neighbor agreement 0.8214 against chance 0.8039, closest-tenth agreement 0.9480, and label-free distance AUC 0.5308 versus the prefix full-model AUC about 0.804. These fit recurring workloads; they do not prove independent records, nor establish copied outcomes across time. Same-time projected duplicates remain together across any cutoff. The separate native full hidden-group probe had no completed result available when this report was written; it is not counted as a clean pass. The independent selected-identity recurrence measurements above are completed evidence.

**Ranked finding 3 — P4, label maturity and gap; pass with an availability assumption.** Every retained training end time precedes its refit. The independent maxima are 23:58:59 before January 1, 23:57:10 before September 1, and 23:59:36 before May 1. The removed unmatured fractions are respectively 0.1193%, 0.2323% and 0.0614% of earlier submissions. Thus the hypothesized future-label shortcut is actually filtered, rather than ignored because it is rare. The paper describes outcome characteristics as accessible at completion, supporting `edt` as the released availability proxy. Actual reporting/ingestion timestamps are not released; zero additional reporting latency remains an assumption, not a measured property. Rules SPLIT-9/10, USE-3, EV-7.

**Mildest remedy:** keep the exact availability filter. A fixed gap based on submission age is not needed to remove already-excluded unfinished jobs and is less precise than their observed completion times. A seven-day embargo additionally removes 0.615%/0.576%/0.892% of mature full-history records; 30 days removes 2.446%/4.607%/3.598%, without establishing which missing reporting latency it repairs. The newest retained rows can be fast-completing jobs, as in any live refit; no measured shortcut or required latency interval is established beyond that real eligibility condition. Record the no-extra-gap rationale and unavailable reporting latency rather than invent an interval from test scores. If actual operational delivery latency is later obtained, filter on completion plus that delay and recheck. These counts compare concrete alternatives; no gap-model fit was needed after the exact label-date check resolved the suspected future-label mechanism.

**Ranked finding 4 — P4, source holdout adaptation; right with a judgment note.** The source's fixed calendar trains March 2021–May 2023 and tests June 2023–April 2024, which is 27 training months despite its prose saying 26. The paper's Technical Validation / Model training and testing explicitly notes that models improve with frequent updating: “models are more accurate when they are updated frequently over time with recent data”. The three refits preserve future same-system evaluation while satisfying the benchmark's minimum three windows and covering a year; they add May 2023 to the evaluated period. Four months is a benchmark design choice, not a verified production refit cadence prescribed by the authors. The mature historical floor remains 65.3% in the oldest window. Rules SPLIT-5/11/12/14/19/20/21: the source supports temporal ordering and updating, while the exact cadence is a Should-level judgment. **Mildest remedy:** keep the explicit change note and avoid presenting this as literal author reproduction or deployed cadence. The existing `results.json` provides the source-calendar diagnostic with repaired maturity and 200k/side budgets: categorical-plus-embedding LightGBM AUC 0.792, categories 0.779, embedding 0.763 and integer codes 0.695. It is a measured alternate protocol, not evidence for choosing the four-month windows by a favorable score. [Paper](https://doi.org/10.1038/s41597-025-05633-1); [pinned author baseline](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/baseline_experiments.py).

**P6 consequences, not grounds to change the regime.** Native three-window mean AUC is 0.794 linear, 0.758 random forest and 0.783 LightGBM, versus dummy 0.5; flags are `no_spread` and `drift_baseline`. The latter uses log loss, whose sensitivity to changing prevalence differs from the primary ROC ranking. Train-only bounded categorical tuning yields AUC 0.865/0.777/0.791; its oldest-window log loss remains poor, so calibration/shift concerns remain. Neither these scores nor the newest-to-oldest 11.851%/14.922%/11.427% sampled test failure rates justify changing windows or history after seeing outcomes. Full benchmark HPO and precision of family separation remain outside these diagnostics. Rules SPLIT-4/21, EV-3/5/8; see task JSON and `flag-followup.json`.

**Unresolved weighing calls for the mediator/curator.** Accepting the approximate released-execution cohort for the submission-time operational purpose is the substantive choice; full-population coverage cannot be recovered by a different split. Four-month refits are a disclosed, reasonable benchmark adaptation, with exact production cadence unverified. Parent/subjob resolution and reporting latency remain named evidence limits. There is no demonstrated split defect to cure by a cold-start variant, additional gap, aggregation, target replacement or arbitrary tail removal. Reassess if the running hidden-group probe produces a concrete mechanism inconsistent with future same-system scoring; recurrence percentages alone do not do so.

This independent add-stage audit is dated November 3, 2026. It is not final inclusion, saved-container validation or curator acceptance; the reviewed definition and split hashes bind the measured results.

</details>

<details><summary>Historical domain practitioner (2026-11-03)</summary>

**Fit: approximate.** As a Fugaku operator, I could use a submission-time nonzero-exit risk score to prioritize investigation, but this selected execution cohort does not establish coverage of all submissions, preventable failures, or a one-to-one match between rows and interventions. This is a real predictive task with named limitations, rather than fit none (USE-1, USE-5, USE-8).

**My actor, moment and action.** When a job arrives, I would use its risk estimate to decide whether to inspect its configuration or contact its submitter before execution. That concrete triage action is my interpretation of the paper’s broader workload-management motivation; the source does not demonstrate an operating intervention policy. I would request a probability, accompanied by an explanation, rather than automatically reject a predicted failure. Fugaku’s software provides holding and parameter-change operations, but their existence does not establish that predicted nonzero exits justify using them. [F-DATA paper](https://doi.org/10.1038/s41597-025-05633-1), [Fujitsu guide, §§2.5.3–2.5.4](https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf)

**Inputs and target availability.** I have the submitting user, job name, requested environment and submission timestamp at this moment. Their masked categories and pretrained embedding are plausible released representations of those inputs. The pinned generation code encodes only the original user/name/environment strings; it does not encode outcomes. Combining these representations and adding time are disclosed changes from the source experiments. [Pinned author generation code](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/generation_scripts/generate_derived_features.py)

I do not yet know the exit state or execution measurements. Their exclusion is correct under USE-3. Training labels must also have become available before refitting; the supplied snapshot and definition implement that boundary using end time. Reporting latency beyond end time remains unverified.

For operational assessment I would additionally consult the submission script, requested resources and prior outcomes. Those are information gaps, not grounds to silently extend this source-focused feature set. In particular, the manual permits post-submission changes to elapsed limits and priority; a released request field is not automatically its initial value. [Fujitsu guide, §2.5.4](https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf)

**Gaps, ranked by impact on my decision.**

1. **Actionable failure versus nonzero exit.** The original target is precisely defined and the supplied full-release audit reports zero disagreement with `ec == 0`. However, the paper explicitly allows intentional nonzero returns without failed computation. I therefore treat the target as nonzero-exit risk, not a diagnosis of hardware failure or avoidable wasted computation. A correct prediction can still identify a job needing no intervention. This limits the operational claim under USE-5; it does not justify replacing the approved original target. [F-DATA paper, Derived Features](https://doi.org/10.1038/s41597-025-05633-1)

2. **Post-run cohort selection.** The source cleaner excludes records missing timestamps and several execution measurements. At submission I cannot know whether a job will satisfy that eventual eligibility condition. The release cannot quantify omitted early failures, uninstrumented executions or pending work. This is a substantive deployment-population gap under USE-8. Rephrasing the actor as selecting only eventual eligible executions would excuse an unknowable condition, contrary to the caution accompanying USE-9. [Pinned author cleaner](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/generation_scripts/clean_and_anonmyze_data.py)

3. **Execution row versus intervention unit.** A row can reasonably receive an execution-risk prediction, but it is not established that each row represents an independent submission-level action. The manual distinguishes parent job IDs from bulk/step subjob identifiers. The public release lacks the finer identifier, while supplied audits find repeated IDs with different timings and sometimes labels. I would preserve those executions, not deduplicate by `jid`; I cannot claim parent-job or workflow-level performance from per-row scores (USE-1, USE-5; MET-1–2). [Fujitsu guide, §1.4](https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf)

4. **Operational history and drift.** The three future windows reasonably simulate periodic refitting on the same system, rather than new-site or new-user generalization (USE-10). Supplied recurrence evidence shows previously observed users comprise approximately 74.1%, 95.1% and 98.0% of test rows across the windows. This is useful historical continuity, not itself leakage. I would nevertheless need evidence that predictions remain useful as users and workloads change.

**Metric scores my decision: partly.** I support the declared **ROC AUC fallback** for comparing per-execution nonzero-exit rankings. The paper uses generic accuracy, and neither its evaluation description nor the supplied baseline establishes an operator threshold, review capacity or error-cost matrix. Retaining accuracy would therefore lack decision support (MET-1, MET-5–6, MET-8). Class imbalance alone does not warrant substituting average precision (MET-9). [F-DATA paper, Technical Validation](https://doi.org/10.1038/s41597-025-05633-1)

For probability-driven triage, I would also choose **log loss or Brier score**, evaluated chronologically, because AUC does not assess probability accuracy. The supplied bounded probes make this distinction concrete: in the oldest window the combined model has AUC about 0.791 and log loss 0.510, while the historical user-rate baseline has AUC about 0.795 and log loss 0.431. These results do not establish calibrated operational probabilities.

If my actual service had a documented daily review capacity, I would score precision at that capacity, using the verified intervention unit. If it had documented intervention costs, I would use the corresponding expected cost. Neither quantity should be invented here (MET-2, MET-7). ROC AUC can remain the benchmark fallback while operational utility remains unproven.

**Would I use it?** I would trial it as advisory triage on the same system, retaining the original zero/nonzero target. Before consequential scheduling actions, I would require calibration assessment, a small adjudicated study of whether flagged nonzero exits need attention, cohort coverage evidence and recoverable intervention identifiers. These are practitioner validation needs, not a request to redefine this dataset.

**Recommendation.** Keep **approximate** and preserve the original task for curator review. Expand `fit_reason` beyond coverage to name the actionable-failure proxy and unresolved execution-to-intervention unit. The supplied evidence supports a credible exit-state prediction benchmark; it does not yet establish resource savings or warrant final inclusion.

**Evidence inspected.** `dataset.py`, generated README, canonical record, full use-case and metric rules, publisher paper text, pinned author scripts, row-unit/timing reconciliation, `verification.md`, `snapshot.json`, `entity-recurrence.json`, `flag-followup.json`, and `results.json`. No files were edited.

**Pinned-rules confirmation: conclusions unchanged.** I read the full authoritative `domain-practitioner.md`, `use_case.md`, and `metrics.md` under `.claude` at the supplied pin `1964e1b`. Every rule ID cited in my report remains applicable.

**Clarification for the saved report:** the nonzero-exit label is documented and verified; I am not invoking USE-5’s exception for undocumented labels. The defensible task is advisory triage for **nonzero-exit risk**. Interpreting it as prediction of preventable computational failure would require additional evidence and could fail USE-5. Cohort selection and unresolved execution-to-intervention identity independently support **approximate** fit under USE-8.

**Metric confirmation:** **partly** remains my assessment of operational decision alignment. Retaining `roc_auc` as the benchmark fallback remains supported by MET-5/6/8; probability-quality checks and any future capacity/cost metric remain supplemental practitioner needs under MET-1/2/7/9.

No edits or model runs were performed.

</details>

<details><summary>Historical blind review (2026-11-03)</summary>

**Verdict:** Include with changes, provided the benchmark documents its population and split construction, enforces outcome availability at training cutoffs, and audits repeated records.

**1. Submission chronology alone does not establish an honest evaluation.**
The task specifies temporal splitting on `adt`, but supplies neither window boundaries nor training-label availability rules. The source defines `adt` as submission time; outcomes become available after completion, and some jobs run for days. Thus, a job submitted before a cutoff could have an outcome learned only afterward. This is an unresolved leakage risk, not evidence that leakage occurred. [Source paper](https://www.nature.com/articles/s41597-025-05633-1)

**Change:** Publish the three exact train/validation/test windows. Build training sets using completion and ingestion times strictly before each training cutoff; preserve those timestamps as evaluation metadata rather than predictors. Keep identical submission timestamps together, and document retraining frequency and validation-based tuning.

**2. The benchmark population is insufficiently explained.**
The public release describes roughly 24 million jobs across March 2021–April 2024, whereas `task.md` describes 2,500,499 prepared rows and only explains the subsequent 200,000-row review sample. [Zenodo release](https://zenodo.org/records/11467483) The inspected sample spans the stated period, but that does not establish how the earlier reduction happened or whether it depended on outcomes.

**Change:** Provide a reproducible source-to-benchmark manifest: release/file checksums, selection and exclusion rules, sampling steps, label construction, and counts before and after each operation. Retain source job identifiers in audit metadata. Establish whether the resulting population represents all submissions, executed jobs, or another selected population.

**3. Repetition needs investigation and explicit evaluation treatment.**
In the sample:

- 32,666 rows—16.3%—are exact duplicates beyond their first occurrence; the largest exact group contains 147 rows.
- Only 50,922 distinct `(usr, jnam, jobenv_req)` combinations occur.
- Identical complete predictor vectors, including submission time, have conflicting labels in 352 groups containing 2,801 rows.

These could include genuine separate jobs or job-array members; the supplied fields cannot distinguish those cases from duplicated extraction records. Conflicting labels are therefore not automatically annotation errors.

In my diagnostic temporal windows, approximately 30–37% of test rows reused a categorical feature combination from training. Such recurrence is legitimate for future workload prediction on the same system, but it does not measure generalization to new workloads.

**Change:** Audit duplication using source identifiers before deleting anything. Remove confirmed extraction copies, retain legitimate executions, report performance separately for previously seen and unseen workloads, and assess uncertainty using temporal/workload blocks rather than independent-row assumptions. Do not impose user-disjoint splitting unless that is the intended deployment.

**4. Define the actor and outcome precisely.**
A credible setting is an HPC submission service scoring a newly submitted job and routing high-risk submissions to additional validation or user review. That decision is my proposed interpretation; `task.md` does not name an actor or action.

The source label is `ec == 0` versus nonzero exit code. The authors explicitly acknowledge that applications can intentionally return nonzero codes despite completing. Consequently, this is prediction of a recorded exit-code convention, with imperfect correspondence to operational failure. [Source paper](https://www.nature.com/articles/s41597-025-05633-1)

**Change:** State the submission-time decision and describe the target as nonzero exit-code risk. Avoid interpreting it directly as hardware failure, unsuccessful science, or avoidable resource waste without additional evidence.

**5. There is useful signal, but drift and simple baselines matter.**
The sample contains 21,942 failures, or 10.97%, across 1,700 observed users. Monthly failure prevalence ranges from 1.86% to 25.46%.

I ran small, untuned diagnostics using all earlier submissions for training. These are **my illustrative windows, not the unspecified benchmark splits**, and remain subject to the outcome-availability concern above.

| Test period | Failures | User-history ROC-AUC | LightGBM, all predictors ROC-AUC / AP |
|---|---:|---:|---:|
| Jan–Jun 2023 | 15.21% | 0.851 | 0.856 / 0.568 |
| Jul–Dec 2023 | 11.72% | 0.710 | 0.760 / 0.391 |
| Jan–Apr 2024 | 11.92% | 0.885 | 0.847 / 0.684 |

The user-history baseline used smoothed training-only failure rates. It outperformed the larger model in the final window. The task has substantive signal, but method rankings may depend strongly on workload composition.

**Change:** Require constant-prevalence and user/workload-history baselines. Report each window separately, using ROC-AUC, average precision and probabilistic loss; select any decision threshold using earlier validation data. Accuracy alone would obscure the imbalance.

**6. The types are usable; the representation needs disclosure.**
There are no missing cells or nonfinite embedding values. The table comprises three categorical predictors, a timestamp, and 384 floating-point embedding dimensions. The source describes these embeddings as pretrained Sentence-BERT encodings of submission metadata, which supports prediction-time availability and provides no obvious direct outcome leakage. [Source paper](https://www.nature.com/articles/s41597-025-05633-1)

**Change:** Label this an embedding-augmented tabular task and pin the embedding provenance. Keep anonymized identifiers categorical. Remove unused category metadata during fold preparation and handle unseen categories explicitly. Near-identical embeddings differ by up to roughly 2.2e−7 for some identical categorical combinations, so embedding-byte equality is unsuitable as the sole duplicate audit.

**What I could not check:** The full 2.5-million-row prepared dataset; source-to-prepared row correspondence; the actual three splits; completion/ingestion timing; duplicate job identities; extraction and embedding-generation code; raw exit-code correctness; or whether the proposed operational action improves outcomes. I inspected the supplied sample and task description, public release documentation, accessible source-paper text, and public baseline code. These limitations prevent unconditional inclusion of the preparation as currently documented.

</details>

<details><summary>Historical precedent check (2026-11-03)</summary>

**Independent precedent check — Fugaku add stage, 2026-11-03**

**Overall finding.** The proposed target, conditional cohort, retention of distinct execution records, temporal regime, ROC AUC fallback and cautious response to task-probe flags largely follow precedent. Two changes need attention: retain the `Selection Bias` marker alongside approximate fit, and present no additional temporal gap as a proposed exception to SPLIT-10, rather than an unconditional pass. Neither finding establishes that the dataset must be excluded.

This is an add-stage assessment, not confirmation of inclusion or build authority. Myunghwan’s November 2 screening decision authorized investigation of the original zero/nonzero target; it did not settle these newly measured issues.

**Evidence boundary.** Read the supplied decision register first, then the current definition/README, canonical record, claims, claim/split/blind reviews, verification and bounded task follow-up. Read the governing principles and relevant rules, and inspected the actual precedent records cited below. Reviewed checkout `0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8`; definition SHA256 `8684b512d50ad5aa39c6afbf012f70b8743eaa651416b7b98b8c4f522f7ec475`. Column/domain reports were unavailable at this review boundary. No repository files or reports were edited during the initial inspection, and no new models were fitted. This panel report was subsequently saved at the parent’s explicit request.

**Authoritative-pin confirmation.** Governing role/rules/scripts are the vendor snapshot `1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b`, independently read in full for principles, use case, splits, selection, leak checks, metrics, task probes and cleaning/features. Later dated precedent facts are taken from the inspected work checkout `0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8`; links pin that exact revision. SPLIT-9/10 and the other operative split rules cited below are unchanged across these versions. The pinned selection vocabulary does not yet contain `Selection Bias`, nor does pinned USE-8 contain its later selection-specific amendment: the marker/fit comparison below follows the explicit October 27 curator records, not an automatically adopted newer rule or a pinned Must. Implement the marker in the record’s `decision_markers`, retaining the definition’s explanatory prose; do not add it to dataset `data_tags`, whose native schema does not allow it. Pinned CLEAN-19 already permits a reasonable combination; later additions concerning other stations’ readings are not needed here. Pinned LEAK-18/20 and the recorded source distinctions support retention; the later expanded LEAK-19 wording is corroborating precedent, not an automatically governing amendment.

**1. Conditional released-execution cohort and approximate fit — consistent, subject to preserving the actual gap.**

The nearest decided comparison is [superconductivity](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/superconductivity.md): on **2026-10-27, Lennart** changed its fit from direct to approximate because its released rows contain only superconductors, whereas a screening application meets mostly nonsuperconductors. The dataset stayed; the selection gap and marker stayed.

The counter-case is [infrared thermography](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/infrared_thermography_temperature.md): on **2026-10-27, Lennart** kept direct fit because the university-clinic deployment setting shares the release’s predominantly young population. The `Selection Bias` marker nevertheless remained. These decisions amended USE-8 deliberately; they are not inconsistent outcomes.

Fugaku’s post-run measurement requirements select instrumented recorded executions. An at-submission operator cannot know that a future submission will survive that selection. Approximate fit therefore matches superconductivity more closely than infrared thermography. Describing evaluation as conditional on released records is accurate; it does not establish that the operator’s actual intake shares the selection.

[Heart disease](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/heart_disease.md), **2026-10-27, Lennart**, also supports examining the real setting rather than treating every restriction as a gap: referral for angiography became the setting of the clinical decision, while obsolete/protocol-mandated tests remained the approximate-fit reasons. Fugaku cannot obtain the same direct-fit result merely by renaming its release survivors as the deployment population.

The action should remain an illustrative submission-time triage decision, explicitly introduced as “For example.” The source motivates workload management; an implemented triage policy and realized resource savings are unverified.

**2. Omitting `Selection Bias` while documenting that cohort gap — departs without a stated reason.**

The current definition carries `Anonymized`, while the current record and definition lack `Selection Bias`. Both closest October 27 precedents retain that marker, regardless of direct versus approximate fit. The [later selection guidance](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/.claude/skills/knowledge-curation/references/selection.md) explicitly treats the marker as a concern, usually compatible with `Yes`; this is later guidance, outside the operative vendor vocabulary, supported here by the dated curator decisions themselves.

This is a documentation departure, with a cheap remedy: add the record-level decision marker and retain the present cohort explanation. It does not require changing the target, split or verdict. The definition’s `data_tags` must remain schema-valid.

**Consistency check (AI, 2026-11-03):** shipping Fugaku without `Selection Bias` differs from superconductivity and infrared thermography, both marked on 2026-10-27 despite different fit judgments. What sets Fugaku apart? (a) The intended operational intake demonstrably shares the released cohort’s post-run selection, recorded with supporting evidence; (b) add the marker as in those cases; (c) reopen those cases to match Fugaku; (d) amend the marker policy. At present, the public release does not establish option (a).

**3. Original zero/nonzero exit-state target — consistent; broader failure interpretations would be unsupported.**

The favorable precedent is [diabetes_3](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/diabetes_3.md), **2026-10-21, Lennart**: an incompletely documented published label was retained with approximate fit and an explicit gap, under the amended USE-5.

The important opposing precedent is [corporate credit rating](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/corporate_credit_rating.md), **2026-10-16, Lennart**: retirement followed evidence that labels mixed issuer and instrument ratings, quantities different from the actor’s intended target. Approximate fit could not cure that demonstrated mismatch.

Fugaku’s original label rule is unusually well checked: all released labels match zero/nonzero exit code. Intentional nonzero returns weaken the interpretation as unsuccessful computation; they do not contradict a task explicitly predicting recorded nonzero exits. Retaining that target follows the mild-remedy ladder and the curator’s authorized investigation. Inventing hardware-failure classes or a fixed-hour deadline would depart from the source and require new evidence.

The qualification is substantive: if the eventual action is established to require parent-job failure rather than per-record exit state, approximate fit cannot by itself override USE-5’s requirement to predict at the actor’s resolution.

**4. Retain execution rows despite equal predictors and unresolved parent/subjob linkage — consistent with stated distinctions.**

Three close precedents support keeping distinct source observations:

- [HIVA agnostic](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/hiva_agnostic.md), **2026-10-21, Lennart**: repeated descriptor vectors stayed because the underlying screened compounds had distinct source identities.
- [Superconductivity](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/superconductivity.md), **2026-10-06, Lennart**: repeated compositions and differing temperatures stayed per row, despite unresolved sample/phase/pressure differences. Averaging would create another dataset.
- [California house prices](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/california_house_prices_2020.md), **2026-10-21, Lennart**: retain real repeat sales; remove exact copies of one sale.

Fugaku’s 384 embedding coordinates encode only three underlying metadata fields. Their width does not make every equal projected vector evidence of an extraction copy. Zero exact nonembedding raw duplicates, different execution timings in traced pairs, and equal-time profiles remaining on one temporal side distinguish genuine information projection from confirmed duplicated extraction.

The adverse precedents are [maternal health risk](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/maternal_health_risk.md) and [hazelnut contamination](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/hazelnut_spread_contaminant_detection.md), both **2026-09-30, Lennart**. Those tasks required generalization beyond unrecoverable collection entities or physical setups; guessed grouping could not provide honest evaluation. Fugaku instead tests later records on the same system, where recurring users/workloads are expected. Unknown finer linkage alone does not establish the same failure.

Keep the precise limitation: one score weights one released execution record; it is not demonstrated to represent one independent parent submission. Source audits support retention, not universal independence. Do not deduplicate by nonunique `jid`, average conflicting exits, or fabricate similarity groups.

**5. Training maturity and no additional gap — SPLIT-9 consistent; SPLIT-10 departure has a stated reason but needs explicit treatment.**

Filtering every training row to recorded completion before refit directly meets SPLIT-9’s measurable requirement. This follows the mechanism addressed in [hotel booking demand](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/hotel_booking_demand.md) and avoids the unremoved future-label shortcut that drove the [Alfa Battle](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/alfa_battle_2_0_task_2.md) decision, ratified **2026-10-26, Lennart**.

However, SPLIT-10 expressly asks for a gap about the label delay because the newest eligible training observations can otherwise be the fast-completing ones. An exact maturity filter does not, by itself, erase that Should-level concern.

Actual comparisons matter:

- [NYC taxi](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/nyc_taxi_trip_duration.md), [Porto taxi](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/pkdd_15_taxi_trip_time_prediction_ii.md) and [cooking time](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/cooking_time.md), **2026-10-21**, adopted one-day gaps after identifying unfinished training outcomes.
- [Delivery ETA](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/delivery_eta.md), **2026-10-21**, added no gap because overnight closure already left every earlier order completed. Fugaku instead actively excludes unfinished records.
- [Melbourne housing](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/melbourne_housing_market.md), **2026-10-21/22, Lennart**, retained no gap after comparing earlier sheets with later archives and finding no recording shortfall.
- [Ames](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/ames_housing.md) and [Perth housing](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/perth_house_prices.md), **2026-10-26, Lennart**, have explicit exceptions based jointly on coarse month resolution and no measured outcome selection. Fugaku has precise timestamps and no equivalent independent completeness comparison.

Fugaku supplies a concrete distinguishing rationale: exact outcome timestamps permit training on the labels a live refit could actually have, and arbitrary seven-/thirty-day exclusions have no established reporting-latency interpretation. That can support a proposed exception serving P4’s deployment fidelity. Record it as such and obtain the curator’s call; retain unknown ingestion latency and fast-completer selection explicitly. Do not describe the absence of demonstrated extra latency as proof that SPLIT-10’s default is satisfied.

This would **not** be the third Ames/Perth exception of the same reason. Their coarse-resolution rationale is materially different. The register’s count of exceptions grouped only by rule does not establish amendment due.

**6. Generic accuracy to ROC AUC — consistent.**

[Heart disease](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/heart_disease.md), **2026-10-27, Lennart**, confirms fallback ROC AUC where the paper supplied reliability and accuracy across several thresholds rather than one operational decision. [Ljubljana breast cancer](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/ljubljana_breast_cancer.md), **2026-10-21 AI assessment**, is a closer accuracy-only example, but remains an assessment rather than independent curator authority.

The contrasting failure-domain case is [APS failure](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/aps_failure.md), **2026-10-21, Lennart**: retain its challenge’s explicit 10/500 cost matrix. Fugaku has no equivalent fixed cost or threshold. Thus preserving its classes while declaring fallback ROC AUC follows MET-5/6/8/11. Imbalance alone supplies no reason to switch to average precision.

**7. Categories plus published embedding and submission time; no requested-resource extension — consistent, with a disclosed adaptation.**

[Rosbank](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/rosbank1.md), **2026-10-26, Lennart**, accepted the baseline plus a useful time block after comparing alternatives; it rejected an indiscriminate union. [Alfa Battle](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/alfa_battle_2_0_task_2.md), **2026-10-21**, established the same CLEAN-19 principle.

Fugaku retains two published views of the same submission metadata; it does not fit a new encoder or a label-dependent representation. The source-calendar comparison provides bounded support for their combination. Submission time is known at prediction; ship its datetime and leave encoding to the pipeline, as the **2026-10-21** NYC/Porto decisions require.

This remains a modification of the authors’ separate-view experiments, not literal reproduction. The user’s task-fidelity preference supports retaining the original target and documenting that change. It does not justify silently extending to every requested-resource snapshot before establishing its submission-time immutability.

For scope, [online news popularity](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/onlinenewspopularity.md), **2026-10-26, Lennart**, retained a text-derived task while preserving modality concerns. That supports case-specific SEL-12 assessment, not automatic rejection or automatic clearance of embeddings. Fugaku’s private original text prevents a new raw-language comparison; keep that limit.

**8. Bounded answers to `no_spread`/`drift_baseline`, with HPO and calibration unresolved — consistent as a provisional keep recommendation.**

The strongest procedural precedent is [OULAD](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/open_university_learning_analytics_dataset.md), **2026-10-22, Lennart**, kept despite `no_spread` with an explicit recheck at the first tuned run; shipping was confirmed October 26.

[African credit scoring](https://github.com/TabArena/data-foundry/blob/0727469103cb3f01ad28e6b6ccbfe55e48ecdfd8/curation/records/african_credit_scoring_challenge.md) is the closest mechanism comparison: its October 7 case distinguishes a log-loss drift flag from ROC AUC discrimination; its final **2026-10-26, Lennart** shipping decision followed additional feature/model investigation. It is not authority to dismiss every later drift flag without checking.

Fugaku has completed train-only tuning, date ablations and raw-user comparisons. The raw-user feature does not match the full model on every fold, so TP-4 triviality is unproved. Useful AUC does not establish calibrated operational probabilities, and two configurations are not full benchmark HPO. Preserve both limitations and a first-tuned-benchmark recheck; do not claim TP-3’s definitive “tuned methods spread” condition has been established.

**Register and drift conclusion.** The register’s flags were leads, not findings. Opposite outcomes for triviality, minority support or forecasting concern materially different mechanisms. Historical amendments and cited rule IDs also generate apparent Must-exception flags that do not show a Fugaku Must violation. I found no documented same-curator drift or third same-reason exception requiring an amendment here. The actionable consistency issues are the missing selection marker and the treatment of the no-gap choice.


</details>

<details><summary>Historical advocate (2026-11-03)</summary>

**Opening advocate brief — Fugaku add review**

**Recommendation: retain the current source-representation task, with the small documentation remedies below.** The completed evidence establishes a credible benchmark of future per-execution nonzero-exit risk. It establishes neither deployment benefit nor complete submission coverage. No irreparable Must violation has been demonstrated. This recommendation does not authorize inclusion or build; the pending hidden-group result must enter the final synthesis.

1. **The original target is verified and supports a plausible decision.** The claim auditor independently checked all **25,866,900** source records: zero disagreements between the published labels and `ec == 0` versus nonzero. The source motivates failure-aware workload management; the domain practitioner identifies submission-time investigation as a plausible action. **USE-1/3/5/8 (Must)** require that concrete framing and its limits, rather than proof of a deployed intervention. The current definition now introduces the action with “For example” and names the actionable-failure proxy and unresolved intervention unit in approximate fit. Those are appropriate repairs. Approximate fit cannot rescue a demonstrated wrong target: this case remains defensible because the task explicitly predicts nonzero-exit risk, rather than claiming to identify preventable computational or hardware failures.

2. **The selected cohort is a real limitation with a mild remedy.** The author cleaner selects records using post-run completeness, so this release cannot establish coverage of every attempted submission. I concede that an operator cannot identify release eligibility when scoring a new job. Preserve approximate fit and the conditional population description under **USE-8 (Must)**; do not obtain direct fit by renaming eventual survivors as the operational intake. Add the record-level **`Selection Bias`** marker, following the October 27 superconductivity and infrared-thermography decisions identified by the precedent checker. Those decisions support retaining a useful task while exposing its gap. The marker is a documentation remedy, not a new dataset `data_tag`, a proof of invalidity, or a reason to invent an alternative target.

3. **The actual temporal splits remove the measured future-label shortcut.** Independent verification found zero submission, completion-cutoff, membership or within-fold-overlap violations. Every fold has 1M training and 500k test records; the oldest eligible history contains **65.322%** of the full source, and test windows contain **57,135–74,610** failures. That supports **SPLIT-1/2/3/9/14 (Must)**. I nevertheless concede the precedent checker’s narrower point: **SPLIT-10 (Should)** explicitly addresses fast-completer selection, so exact maturity filtering alone should not be called unconditional satisfaction of its gap default. Recommend a documented no-extra-gap exception: precise completion timestamps reproduce labels available to a live refit, serving P4, while no extra reporting interval is established. Keep completion as an availability proxy and reporting latency unknown. This is a specific judgment for the existing curator review, not a new blanket permission gate. An arbitrary embargo does not acquire validity from its duration or score.

4. **Repeated predictors do not establish duplicated executions or require cold-start evaluation.** The source audit found zero exact copies over the 44 nonembedding fields; all **38** traced projected-duplicate pairs differed in execution timing. The 384 coordinates represent only three underlying metadata fields, so their width exaggerates the apparent degrees of freedom. **LEAK-16 (Must)** requires the explicit duplicate decision; **LEAK-18/20 (Should)** permit plausible repeats and genuine ambiguity. **USE-10, LEAK-34 and SPLIT-3/4 (Must)** support future same-system scoring with recurring identities. User recurrence of approximately **74–98%** is therefore expected signal. Concede unresolved parent/subjob linkage and unequal execution-group weighting. The current definition’s nonunique-ID wording and per-record evaluation statement are the mild repairs; deduplicating by `jid`, aggregating conflicting outcomes or fabricating groups would create unsupported data. The pending hidden-group probe may add evidence; this brief claims no result from it.

5. **The retained representations are source-supported; the two column questions need explicit reasoning.** The independent full-frame scan found zero missing cells, nonfinite coordinates, constant numeric columns or duplicate numeric columns. Author code encodes only original user/name/environment strings with a pretrained model; no outcome-fitted encoder or post-submission measurement enters the predictors. This supports **USE-3, LEAK-10/27 and CLEAN-9 (Must)**. The combined source views are a disclosed adaptation, supported by the source-calendar comparison: AUC **0.792 combined**, versus **0.779 categories** and **0.763 embedding**, consistent with **CLEAN-19 (Should)**. Requested cores/nodes/memory/frequency are legitimate candidate inputs, not established leaks. Their omission follows the explicitly authorized source-representations-first investigation; no width/runtime rationale is shown under **CLEAN-22 (Must)**. Preserve that named scope rather than silently broadening it. For 359,636 masked job names, acknowledge the **CLEAN-14 (Should)** departure: opaque stable identities justify categories because treating arbitrary tokens as text cannot restore their private semantics. Document that choice; neither question currently demonstrates a retained-column defect.

6. **The signal and baselines support keeping the task without claiming definitive model separation.** Native mean AUC is **0.794 linear, 0.758 random forest and 0.783 LightGBM**, against 0.5. Train-only bounded tuning yields **0.8655/0.7775/0.7911**; the raw-user comparator does not match it on every fold. **TP-4 (Must)** therefore does not establish triviality. **TP-1 and EV-3 (Must)** make `no_spread` and `drift_baseline` questions, while **TP-2 (Should)** favors retaining real signal absent a concrete task defect. Concede that bounded tuning is not full benchmark HPO, and **TP-3’s** definitive tuned-spread condition is unproved. Retain the first-tuned-run recheck. Oldest-window calibration remains poor; AUC must not be presented as evidence of calibrated operational probabilities.

7. **The metric and provenance support this exact bounded version.** The independently reconciled manifest matches all **38** publisher files and their recorded sizes/digests; the label, sampling and split checks bind the prepared version. Generic paper accuracy supplies no fixed operator threshold or cost, so ROC AUC follows **MET-5/6/8 (Should)**; inventing a decision threshold would not improve **MET-1/2 (Must)** alignment. The blind reviewer’s requests for lineage, actual windows, maturity enforcement and duplicate investigation are substantially answered by the later full-source evidence, which outranks the limited sample’s uncertainty under **EV-2 (Must)**. Finish README regeneration and the definite calendar-prose correction. `prose-only-fixes.json` confirms unchanged computational AST; the earlier native check’s 0 errors/0 warnings is mechanical evidence, not a semantic verdict or a completed new check.

**Weighed:** verified original target, faithful source representations, substantial chronological support and useful signal favor retention. Selected-population transport, intervention-unit uncertainty, no-gap treatment and limited tuned separation remain explicit qualifications. Preserve the task through the remedy ladder; do not promote screening authorization into shipping authority.

**Advocate rebuttal — substantial agreement with the critic**

1. **Population, target and action unit — concede the limitations and accept the remedy.** All 25,866,900 released labels satisfy the original zero/nonzero rule, while submission coverage and parent-level intervention performance remain unverified. Preserve approximate fit, illustrative triage wording and per-record evaluation under **USE-1/5/8 (Must)**. Add the record-level `Selection Bias` marker consistently with the cited curator precedents. These qualifications support retaining the bounded task; they establish no reason to retarget, aggregate or exclude it.

2. **Maturity and additional gap — concede the Should-level distinction.** The independent checks establish removal of unavailable training labels, satisfying **SPLIT-9 (Must)** using recorded completion as the availability proxy. They do not automatically satisfy **SPLIT-10 (Should)**. Recommend the explicit no-extra-gap exception already described: precise completion filtering serves live-refit fidelity under **SPLIT-1 (Must)**, while fast-completer selection and unknown ingestion latency remain named limitations. The existing curation review can decide that exception; no arbitrary embargo or additional model comparison is warranted by the evidence.

3. **Value and probability quality — concede the remaining uncertainty.** Useful discrimination and the raw-user comparison leave triviality unproved under **TP-4 (Must)**. They do not establish calibrated probabilities or definitive tuned-family separation. Preserve `no_spread`, `drift_baseline`, the oldest-window log-loss limitation and the first tuned benchmark recheck under **TP-1/EV-3 (Must)**. Retain the ROC AUC fallback under **MET-5/6/8 (Should)**. Neither flag supplies a concrete exclusion reason.

4. **Masked-name dtype — concede the documentation remedy.** With 359,636 opaque job-name identities, categorical typing departs from **CLEAN-14’s Should-level high-cardinality default**. Record the short rationale: stable masked identities serve the recurring-workload task, and string processing cannot recover the private names. Preserve the categorical values and all finite, nonconstant embedding coordinates. No dtype change or exclusion follows.

**Completion update.** The critic’s README concern is now resolved. I inspected the regenerated README: it contains the illustrative action, expanded approximate-fit explanation, unresolved identifier semantics, per-record evaluation unit and completion-time proxy limitation. Check 3 completed with **0 errors, 0 warnings and 2 informational skips**. `post-prose-check.json` confirms unchanged computational AST and native checksum before/after the prose repairs. These results support reuse of the computational evidence; they do not constitute semantic acceptance or build authority.

**Remaining boundary.** The hidden-group probe is still running. Its elapsed time establishes neither success nor failure. Inspect its actual result before final synthesis. Subject to that evidence, the critic and advocate agree on retaining this task with the stated qualifications.

</details>

<details><summary>Historical critic (2026-11-03)</summary>

**Critic opening brief — ship only with the remaining qualifications recorded.** I find no established, irreparable Must violation that warrants exclusion. The defensible task is temporal prediction of recorded nonzero exits for released execution records. It does not establish all-submission coverage, preventable failure, parent-job intervention performance or calibrated operational probabilities.

**Evidence boundary.** Read all six Phase A reports, the current definition/README, canonical record, pinned critic role and governing principles. Governing rules are vendor pin `1964e1b`; current definition SHA256 is `10b8ba1f1ad6f323f313651120955efb2e8a03c7d8b780fffced4bcee2d5683f`. `prose-only-fixes.json` establishes unchanged computational AST relative to the audited definition. I made no edits or model runs.

1. **P3 — retain the population, target and action-unit gaps as substantive limits.**
   **Problem/effect:** The operator acts at submission, but release eligibility depends on post-run measurements, nonzero exits can be intentional, and several execution records can correspond to an unresolved submission relationship. Per-record AUC therefore cannot establish performance per actionable parent submission. Approximate fit names these gaps; it does not demonstrate their absence.
   **Evidence:** The cleaner selects records using execution measurements. April contains 89,593 rows in repeated `jid+adt` groups, including 180 groups with both labels. The practitioner identifies the triage policy as illustrative. Conversely, all 25,866,900 released labels match the original zero/nonzero rule, so the exit-state target itself is verified. The latest definition now names all three gaps and makes the action illustrative.
   **Rule/strength:** USE-1, USE-5 and USE-8 **Must**; the bounded source task can satisfy them. A demonstrated wrong action target could not be rescued merely by approximate fit, but that stronger failure is not established here. The October 27 superconductivity and infrared-thermography decisions support retaining a `Selection Bias` marker; that is curator precedent, not a marker requirement newly imported from the later rules.
   **Mildest remedy:** Preserve the repaired wording, original labels and execution rows. Add the record-level `Selection Bias` marker consistently with those precedents, keeping schema-valid dataset tags. Keep parent-level utility and all-submission transport explicitly unverified. No retargeting, aggregation or repeated authorization question is justified.

2. **P4 — exact maturity passes SPLIT-9, but does not automatically satisfy SPLIT-10’s gap default.**
   **Problem/effect:** Training immediately before each cutoff includes only fast-completing recent submissions. That can be faithful to a live refit, yet it is the selection concern SPLIT-10 expressly names. Unknown reporting latency is a separate limitation.
   **Evidence:** Independent native-index checks find zero retained training completion violations; 10,387/48,375/28,118 unavailable labels were removed. Thus the measurable future-label shortcut is fixed. Seven- and thirty-day alternatives remove additional mature observations without establishing an operational latency they repair. The precedent review distinguishes Fugaku from delivery ETA’s naturally closed overnight history and from Ames/Perth’s coarse-month exceptions.
   **Rule/strength:** SPLIT-9 **Must**, met using the recorded completion proxy; SPLIT-10 **Should**, requiring either compliance or an explicit exception. SPLIT-1 **Must** supports deployment fidelity; SPLIT-21 **Must** prevents choosing a gap from favorable test scores.
   **Mildest remedy:** Retain exact maturity filtering and propose a documented SPLIT-10 exception: precise completion timestamps simulate labels available to the live refit, while no additional reporting interval is established. Name fast-completer selection and unreleased ingestion latency. The final curation call must distinguish this exception from an unconditional pass. I request no arbitrary embargo or additional model comparison.

3. **P6 — learnability is supported; model separation and probability quality remain unsettled.**
   **Problem/effect:** Strong AUC does not answer `drift_baseline`, which concerns probabilistic loss, or prove that tuned benchmark families separate. Treating either flag as cleared would overstate benchmarking and operational value.
   **Evidence:** Native mean AUC is approximately 0.794/0.758/0.783 for linear/RF/LightGBM versus 0.5. Bounded train-only tuning produces useful discrimination, and raw-user prediction does not match the full model on every fold. Nevertheless, the oldest tuned full-model log loss remains about 0.510, worse than the raw-user model’s approximately 0.433. `no_spread` rests on only three overlapping historical windows; two configurations are not full benchmark HPO.
   **Rule/strength:** TP-1 and EV-3 **Must** require investigating flags rather than converting them into verdicts; TP-3 **Must** supplies a sufficient keep condition only when tuned methods actually spread. TP-4 **Must** requires foldwise proof of triviality, which is absent. MET-5/6/8 **Should** support the ROC AUC fallback.
   **Mildest remedy:** Keep the task provisionally, preserve both flags and the calibration limit, and record a first tuned benchmark recheck. Retain ROC AUC; do not invent costs, thresholds or review capacity. No new models are needed for this panel, and no `Trivial`, `Too Small` or no-signal exclusion follows.

4. **P7 — document categorical masked job names as a deliberate CLEAN-14 departure.**
   **Problem/effect:** `jnam` has 359,636 levels, while the pinned typing rule defaults high-cardinality values to string. Leaving the rationale implicit makes the chosen representation appear inconsistent.
   **Evidence:** The values are stable opaque source identifiers; their private original text is unavailable. String processing cannot recover that text and can exploit arbitrary token suffixes. The column auditor found no blocking column defect and supports retaining nominal identity.
   **Rule/strength:** CLEAN-14 **Should**; USE-1/10 **Must** support the recurring-identity task. This is a quality documentation issue, not an exclusion ground.
   **Mildest remedy:** Add a short explicit exception/note explaining why masked names remain categorical. Preserve the coordinates, including the two tiny finite nonconstant dimensions; diagnostic float32 underflow is not source damage.

**Objections I do not sustain.** The November 2 curator instruction already authorizes investigating the original target and source representations first. Requested cores/nodes/memory/frequency are not proved leaks, but their omission from this expressly disclosed source-representation version does not establish a width-driven CLEAN-22 violation or require renewed permission. Combining the source views and adding submission time remain disclosed adaptations. Recurring users and projected duplicate profiles do not justify cold-start grouping, guessed groups or deduplication: exact raw nonembedding copies were absent, traced projected pairs differ in execution timing, and equal-time profiles remain on one temporal side.

**Completion limits.** The README I inspected still contained the earlier prose; check 3 had no completed result available. Regenerate and inspect it before representing those repairs as installed documentation. Likewise, the supplemental temporal hidden-group probe remains pending at this boundary. Inspect its actual result before final synthesis; neither claim a pass nor infer failure from its unfinished state. Prior check 2’s zero errors/warnings establishes its mechanical result, not semantic acceptance.


**Critic rebuttal — substantial agreement; retain the remaining documentation remedies.**

1. **Original target and plausible decision — concede.** Zero label disagreements across 25,866,900 records establish recorded zero/nonzero exit-state prediction. The regenerated README now makes triage illustrative and names the actionable-failure and intervention-unit gaps. USE-1/3/5/8 **Must** support this bounded framing. They do not establish preventable-failure or parent-job utility; the advocate appropriately makes neither claim.

2. **Selected cohort — concede the proposed remedy.** Post-run eligibility remains unknowable at submission, so approximate fit and the conditional-population explanation must stay. Add the record-level `Selection Bias` marker following the dated curator precedents. That marker is a consistency remedy, not a newly imported pinned Must or an exclusion argument. This resolves my first point without changing the target or rows.

3. **Maturity and additional gap — concede, provided the exception is recorded explicitly.** The independent cutoff checks support SPLIT-9 **Must**. SPLIT-10 **Should** separately addresses fast-completer selection; exact maturity alone does not erase that concern. The advocate accepts this distinction and proposes the appropriate no-extra-gap exception serving SPLIT-1’s **Must** deployment fidelity. Preserve completion as a proxy and reporting latency as unknown. No arbitrary embargo or new permission gate follows.

4. **Repeated predictors and execution identity — concede.** Zero exact raw nonembedding copies and distinct execution timing in all 38 traced projected pairs support preserving records. USE-10 and SPLIT-3/4 **Must** favor temporal same-system evaluation, while SPLIT-30 **Must** prevents treating recurrence alone as grounds for regrouping. Parent/subjob linkage and unequal execution weighting remain limitations, now stated in the regenerated README. Do not infer independence or fabricate groups.

5. **Representations, omitted resources and categorical names — concede with the agreed note outstanding.** Source code supports input-only pretrained representations, and the combined-view adaptation is disclosed. The existing source-representations-first authorization answers the scope question; no new evidence warrants asking again or alleging a CLEAN-22 **Must** violation. Document the masked-name categorical choice as a CLEAN-14 **Should** exception. Opaque token suffixes do not recover private text semantics.

6. **Learnability, separation and calibration — concede the bounded recommendation.** Useful AUC and the foldwise raw-user comparison defeat an established TP-4 **Must** triviality finding. They do not establish TP-3’s **Must** sufficient tuned-spread condition. The advocate preserves this distinction, the TP-1/EV-3 **Must** flag assessment, the first tuned benchmark recheck and the calibration limitation. I request no additional models for this panel.

7. **Metric, provenance and completed prose verification — concede; withdraw the pending-README objection.** ROC AUC remains supported by MET-5/6/8 **Should** without invented costs or thresholds. New evidence shows check 3 completed with zero errors, zero warnings and two disclosed infos. The regenerated README contains the repaired action, fit, identifier, evaluation-unit and availability wording. `post-prose-check.json` records unchanged native checksum `v2:7d4130ef49f4c8fd85ea7894aa39e2a509d1b0edc048515ec543f162e6d44e3b`; computational AST is unchanged. Reusing the computational evidence is therefore supported. Mechanical success remains distinct from semantic acceptance under EV-7 **Must**.

**Remaining position.** Retain the bounded task recommendation after recording the selection marker, proposed SPLIT-10 exception, categorical-name rationale and tuned-result follow-up. Inspect the still-running hidden-group probe’s actual result before final synthesis; no result is claimed here. No new exclusion case or computational repair has emerged. This rebuttal grants no inclusion or build authority.

</details>

<details><summary>Historical review editor (2026-11-03)</summary>

**Readiness:** Ready for curator review after the edits below and the coordinator’s final evidence update; no new scientific probe is requested.

**Concrete edits, most important first**

1. Replace the Outcome paragraph with an explicit judgment record.

   **Old:** “The panel recommends ship after changes, subject to the three judgments below. The original zero/nonzero exit-state target … final inclusion remains Myunghwan's decision.”

   **New:** “The panel recommends retention for curator review. Validity: the original exit-state target supports an approximate per-execution task under USE-1/5/8; the recorded-completion boundary of SPLIT-9 is met, while the proposed SPLIT-10 exception remains open. Value: useful chronological ranking favors retention under TP-2, with tuned-model separation and probability quality unresolved. Quality: the categorical masked-name choice is documented as a CLEAN-14 Should departure. Verified labels, source-supported inputs and substantial temporal support favor retention; cohort coverage, intervention identity and reporting latency qualify it. Myunghwan decides issues 1–3.”

   Preserve the required opening sentence: “added as `fugaku_hpc_job_failure_1m`.”

2. Give issue 2 one decision.

   **Old title:** “Accept the proposed no-extra-gap exception and refit adaptation?”

   **New title:** “Accept the proposed exception to the additional training gap?”

   **Old decision:** “accept the proposed exception and disclosed windows as recommended, or request that repair.”

   **New decision:** “accept the proposed SPLIT-10 exception as recommended, or require an evidence-grounded gap and requalification of the affected splits.”

   Keep the four-month windows as a disclosed implemented adaptation. In the Mediator section, replace “Accept that disclosed benchmark judgment under SPLIT-12/19” with “The four-month windows are the implemented benchmark judgment under SPLIT-12/19.” Otherwise the issue requests separate decisions about gap and cadence.

3. Explain the value issue without requiring a panel dive.

   **Old:** “Bounded train-only tuning yields 0.8655/0.7775/0.7911 across the three windows, and raw-user prediction does not match the full model on every fold.”

   **New:** “Bounded train-only LightGBM tuning yields ROC AUC 0.8655/0.7775/0.7911, newest window first; the user-only model does not match the full model on every fold.”

   **Old:** “However, `no_spread` and `drift_baseline` remain qualified: two configurations are not full benchmark HPO, and oldest-window log loss is 0.5104 versus 0.4330 for the user-only model.”

   **New:** “Two questions remain: whether tuned model families differ reliably (`no_spread`) and whether probability predictions improve on simple baselines (`drift_baseline`). Two configurations do not constitute full benchmark hyperparameter tuning. Oldest-window log loss, where lower is better, is 0.5104 versus 0.4330 for the user-only model.”

   Preserve the existing sentence limiting this to probability quality rather than a diagnosed calibration mechanism.

4. Make issue 1’s operational effect easier to assess.

   **Old:** “In April, 89,593 rows share an identifier/submission-time pair with another row; 180 such groups contain both labels.”

   **New:** “In April 2024, 89,593 of 420,450 records (21.31%) share an identifier/submission-time pair with another record; 180 such groups contain both labels.”

   **Old:** “These limits affect transport to all submissions and the weighting of parent-job interventions.”

   **New:** “These limits prevent direct generalization to all submissions and can give one parent-job intervention multiple weights in the evaluation.”

5. Lead the panel summary with substance.

   **Old:** “Full panel: six independent evidence reviewers, advocate and critic with one rebuttal each, mediator and a cold editor.”

   **New:** “The advocate and critic agree on retaining the original exit-state task with approximate operational fit. The three open decisions concern that fit, the proposed SPLIT-10 exception and provisional value acceptance.”

   The role sections already show panel composition. Keep the summary’s statement that full-source evidence substantially answered the blind reviewer’s lineage, timing and repetition concerns.

6. Make completion claims specific to the completed version.

   **Old:** “`post-prose-check.json` confirms unchanged computational AST and native checksum after prose repairs.”

   **New:** “`post-prose-check.json` records the check-3 comparison. The latest documentation changes require the final check-4 result; computational equivalence and framework checksum identity are separate claims.”

   The README inspected during this review contains checksum `v2:259a23c34d5183aec23231613772e7c3a4fec65d058cf149e213da22bc46126a`, while the embedded historical critic report names `v2:7d4130…`. Preserve historical reports and report the actual final result in the completion update. Do not claim that the pending supplemental temporal hidden-group probe passed.

**Format assessment:** The three issues are ranked P3, P4, P6, with clear implemented choices, alternatives and decisions. There is one panel block, nine matched role toggles, no nested toggles, no extra headings beyond the record title, and no absolute local paths. No record-field disagreement rows are present. Append this editor report as the tenth role. The full historical reports can remain collapsed; the curator can decide from the revised outcome and three issues.

</details>

<details><summary>Prior focused claim audit (2026-11-05)</summary>

**Independent focused claim audit — Fugaku, 2026-11-05**

**Recommendation:** retain the reviewed definition and past decisions. No new target, predictor, split or metric defect was established by the updated-main recheck. Preserve the approximate selected-execution scope, confirmed SPLIT-10 exception, source/lineage limitations and required first-tuned-benchmark follow-up. This is a focused compatibility/claim audit, not a new curator verdict or a clean full leak-CLI pass.

**Identity and method.** Current main is `9048f36a`; the definition is byte-identical to the accepted November 3 definition (`16f04dad…`). I independently read the current definition, record, native check, relevant current rules and probe changes, fixed primary-source evidence, and the original actual-data results. The current identity proof establishes exact frame values/order, categories, all six membership arrays, metric specification and library versions. The new empty task metadata field `special_features=[]` alone changes the native checksum to `b655fe6b…`; encoding the old metadata exactly recovers `c7436e8d…`. Source evidence was reread from its retained fixed-version files; their SHA-256 identities match the original source manifest. No source document was newly downloaded, and no repository or prior-evidence file was edited by this audit.

**Fresh measurements.** All 38 actual raw files were reread, their current sizes and publisher MD5s verified, and every exit code/label compared: 25,866,900 records, 2,558,519 failed (9.89109%), zero disagreements. The current native scorer returns dummy AUC 0.5 and oracle sanity AUC 1.0 on every exact 500,000-record test fold. New native-function probe 17 uses all 384 float coordinates, three exact shipped folds, the native RNG-0 50,000-per-side caps, 200-tree untuned LightGBM and two threads: format-only AUC 0.500000, top-three format features 0.500000 each, against a fresh same-protocol numeric/categorical baseline of 0.804219. This baseline is not the differently capped three-family task probe and is not HPO.

**Primary sources.** [Fixed F-DATA release](https://doi.org/10.5281/zenodo.11467483); [defining paper](https://doi.org/10.1038/s41597-025-05633-1), Methods and Technical Validation; [pinned encoder/target derivation](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/generation_scripts/generate_derived_features.py); [pinned cleaner](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/generation_scripts/clean_and_anonmyze_data.py); [source baseline](https://github.com/francescoantici/F-DATA/blob/db67a65a4b6e91dcebd26147de191fa0051ad790/baseline_experiments.py). Source code supports the stated construction; inaccessible private original strings and excluded submissions cannot be reconstructed from it.

**Claim-by-claim result.** “Holds” refers to the bounded statement as written, not an unqualified operational extension. The complete literal task-summary, 14 curation bullets, split comment and warning inventory is retained with the audit evidence.

| Claim | Source in the current package | Refuting test used | Result | Evidence | Rule |
|---|---|---|---|---|---|
| Predict eventual nonzero exit of a submitted job | `task_summary.question/predicted`; target bullet | Exhaustive raw code/label comparison; inspect source target construction | Holds for released execution records | All 25,866,900 labels exactly equal zero versus nonzero exit code; no fixed-duration target was introduced | USE-5; LEAK-4; EV-1/2 |
| An operator could score at submission for attention before resource use | `use_case`; prediction-point bullet | Read source motivation and field lifecycle; check whether a deployed policy is asserted | Holds as the explicitly illustrative use; deployed benefit untested | “For example” correctly qualifies the action; source motivates failure-aware workload management but supplies no intervention-effect evaluation | USE-1/3/8; EV-7 |
| One released execution record, not one uniquely identified parent intervention | `row`; row-identity/evaluation-unit bullets | Inspect source fields and preserved raw ID/timing audits | Holds; parent mapping untested | `jid` repeats; prior exhaustive/April audits and 38 traced projected-duplicate pairs have distinct execution timing; no finer subjob identifier is shipped | USE-5/11; PROV-1; EV-7 |
| The source has March 2021–April 2024 data and this version is the capped union | `row`; version comment | Raw file counts/manifest plus current frame/membership identity | Holds | 38 fixed monthly files; 25,866,900 source rows; 2,500,499 retained union rows | PROV-1/10; SPLIT-14; EV-1 |
| Nonzero can be intentional; this is not hardware-failure diagnosis | `predicted`; target bullet | Read paper target discussion and derivation | Holds as a bounded label interpretation | Source warns about false-positive failure semantics; the implementation does not invent a cancellation/timeout taxonomy | USE-5/8; EV-2 |
| Only masked user/job/environment, 384 source coordinates and submission time are inputs | `known`; inputs/exclusion bullets | Compare exact current frame columns against source codebook and encoder inputs | Holds | 388 predictors; no `ec`, `edt`, duration, resource use or source-position fields reach models | USE-3/6; LEAK-1/2/10/27 |
| Released embeddings are pretrained encodings of the three original strings without outcome fitting | Inputs bullet | Re-read pinned encoder code; verify fixed source identity and prior exhaustive vector audit | Holds as the published construction; exact private-text regeneration untested | `JOB_FEATURES` contains only the three original string fields and encoder is `all-MiniLM-L6-v2`; all 38 raw bytes still match the audited publisher files | LEAK-27/29/30/32; PROV-1; EV-7 |
| Every source vector is float32, length 384 and finite | Inputs bullet | Fresh file/schema identity plus preserved complete vector scan | Holds by exact-source evidence reuse | Prior per-month exhaustive audits find length384 for every row and no nonfinite/zero-norm vectors; all current publisher digests match | CLEAN-1; PROV-13; EV-8 |
| High-cardinality masked job names are nominal categories | Typing bullet | Fresh retained-category support/missingness; inspect anonymization maps | Holds with the documented Should rationale | 359,636 job names, 2,781 users, four environments; no missing retained categories; token suffixes are arbitrary map indices, not recoverable natural text | CLEAN-14; USE-1/10 |
| Combined views/time and three refits adapt, rather than reproduce, source experiments | `changes`; source-experiment bullet | Re-read baseline representation choices and calendars | Holds | Authors evaluate the views separately and a fixed June2023–April2024 holdout; this version combines them, adds known submission time and refits for three four-month windows | USE-8; PROV-1; EV-8 |
| Requested-resource extensions are not silently added | Source-experiment/exclusion bullets | Exact column inventory and definition read | Holds | Requested/allocated resource counts, limits, frequency and priority are absent; possible mutability of release snapshots is not used to add unqualified predictors | LEAK-10; USE-6 |
| The excluded fields include direct target/post-execution proxies | Exclusion bullet | Current native-function probe20 on actual source-aligned `ec` and duration | Holds | Excluded `ec` alone AUC1.0000 and duration0.6735; both are absent from predictors. The perfect target proxy is expected and does not make the retained task trivial | LEAK-10; TP-4; EV-1 |
| No full raw nonembedding duplicates were found; do not deduplicate by nonunique `jid` | Row-identity bullet | Preserved exhaustive 44-field audit under fresh raw digests; new bounded native raw-copy checks | Holds for the stated scans | Prior complete per-month audit reports zero exact44-field copies; eight fresh 10k actual-source windows also have zero native raw-copy groups, even after the native helper excludes individually unique fields | LEAK-16/18/19/20; EV-8 |
| Retained repeated vectors can be distinct executions and the score weights records | Evaluation-unit bullet | Preserved 38-pair source trace and current membership identity | Holds; independence/parent utility is not established | All38 traced pairs differ in execution timing. This is evidence about those pairs, not a complete parent-job reconstruction | USE-11; LEAK-16/17; EV-7 |
| Source offsets become Japanese calendar time; equal-time order is publisher file/row order | Time bullet; `shuffle=False`; split comment | Read conversion/stable-sort operations and current exact order/membership comparison | Holds | UTC instants are converted to Asia/Tokyo before removing timezone; stable chronological sorting and verified row-order hashes are unchanged | SPLIT-1/9/12; CLEAN-1 |
| The release is selected using post-run measurements | `fit_reason`; cohort bullet | Re-read missing-value restrictions in the author cleaner | Holds | Arrival/start/end and execution counters/energy/power fields are required by the source cleaner; no excluded-row denominator ships | USE-7/8; LEAK-22/25; EV-2/7 |
| Coverage of all attempted submissions and final-month pending jobs is unknown | `fit_reason`; cohort bullet | Seek that denominator in the release/code; compare end-of-release target profile | Holds as an acknowledged limit; census transport untested | No pending/missing-submission roster exists. Native full-source period13 sees rising April failure rate, not a falling terminal-label signal; this does not prove a complete submission census | USE-8; LEAK-24/25; EV-7 |
| Three successive four-month test windows predict future jobs on the same system | `split`; split comment | Current exact six-array proof and independent fold support counts | Holds | Jan–Apr2024, Sep–Dec2023, May–Aug2023, newest first; each test side500k and train side1M; actual test failures59,253/74,610/57,135 | SPLIT-1/3/13/19; TP-9 |
| Training retains only recorded completion strictly before refit | `split`; maturity bullet; split comment | Current end-time membership proof and prior full-source maturity audit | Holds for `edt` proxy | Zero retained unavailable recorded training outcomes in all three exact memberships; post-completion reporting arrival remains unavailable | SPLIT-9; LEAK-12; EV-7 |
| No additional embargo is a confirmed, qualified SPLIT-10 exception | Split comment; record exception | Check actual stored notes, applied maturity follow-through and current Cases row | Holds as the retained decision, not an ordinary zero-gap pass | Original Nov3 decision and factual follow-through remain; fast-completer selection and reporting latency caveats are not erased by the newer fixed-horizon precedent | SPLIT-10; P4; EV-8 |
| At least half the full source history precedes the oldest test window | Split comment; window specification | Inspect unchanged full-source native selection assertion and current memberships | Holds | The assertion is evaluated on all source metadata before the cap; native split logic and exact memberships match the reviewed version | SPLIT-14; EV-1 |
| Caps are native class-proportional quotas and do not balance the classes | Version/sampling bullets; split comment | Current native array equality, source-position selection and class counts | Holds | Native preparation keeps1M/500k per side after maturity filtering; selected union failed11.02% versus9.891% source, not50/50. Union share need not equal any one window's quota share | SPLIT-14; CLEAN-11; EV-1 |
| Selection is calculated on full-source metadata, then lineage columns leave model data | Sampling bullet; methods | Inspect `_select_temporal`, source-key matches and final389 columns | Holds | Current membership proof is exact; `_source_file`, `_source_row`, `_split_roles` and `edt` are absent from predictors | LEAK-10/29; SPLIT-9/14 |
| Source identities recur by design; this is not an unseen-user task | Split comment | Reuse complete temporal recurrence audit under exact frame/split identity | Holds | Temporal recurrence was explicitly measured and accepted; hidden-group `hits:[]` was never evidence of no recurrence | USE-10; SPLIT-13; EV-8 |
| A four-month horizon describes refits, not a terminal-label deadline | Temporal declaration/comment | Compare target construction with window calculation | Holds | Labels remain eventual zero/nonzero outcomes; test labels can end after their submission window and every recorded source end precedes publication | USE-5; SPLIT-12/19 |
| Fallback ROC AUC reflects an accuracy-only source report without fixed operating cost/threshold | Metric declaration/reason | Reread Technical Validation and baseline; inspect declared spec | Holds | Source reports accuracy/classification report, with no prescribed operator threshold/cost; unchanged fallback probability ranking is source-compatible under the accepted task | MET-1/2/5/6/8/11 |
| The metric computes at the shipped unit on every fold | Metric; metadata | Fresh independent native dummy/oracle scorers and support counts | Holds | Row-unit evaluation, no auxiliary metric inputs; dummy0.5 and oracle sanity1.0 in each exact500k test side with both classes present | MET-2/3/13; TP-5/9 |
| Native task flags received follow-up but do not establish tuned-family separation or calibrated utility | Value bullet; record assessments | Inspect preserved native task results, bounded follow-up and exact reuse conditions | Holds as a qualified conclusion | Prior mean AUC linear/RF/LightGBM0.7941/0.7576/0.7826; `no_spread`/`drift_baseline` remain. The first full tuned-family/probability recheck has not run | TP-1/2/3/4; EV-3/7/8 |
| The maturity sensitivity numbers are bounded diagnostics and did not select a gap | Maturity bullet; record | Read predeclared sensitivity specification, saved exact baseline reproduction and accepted exception | Holds as dated evidence reuse | Hypothetical24h reporting delay and seven-day embargo comparisons retain their original single-family/200k-test scope. They do not establish actual ingestion latency or full-budget HPO | SPLIT-9/10; EV-1/7/8 |
| The curator accepted the task, qualified gap choice and retain-with-recheck, then said “ship this” | Curator bullet; restored record/review history | Read original source-bound decision stores and exact words, not a new inferred mark | Holds | Original issue IDs1–3 and final Nov3 verdict are retained at their original identities; Nov5 request authorizes reuse, not rebinding old marks | EV-2/7; consistent judgment |
| Accepted check warnings are empty and current native bundle check is clean | `accepted_check_warnings`; generated card | Read actual current native check output | Holds | 27 checks: zero errors/warnings, two explicitly budget-skipped informational checks; prior whole-table audits supplement them | EV-7; verification procedure |
| Historical screening “about24M/about20GB/direct fit” is current fact | Older dated record notes | Compare stronger measured source facts and later accepted notes | Refuted as a current interpretation; already superseded | Actual source is25,866,900rows/27.2GB and fit is approximate. Current record explicitly preserves old notes as history; no new correction/decision is needed | EV-2; USE-8 |

**New-probe interpretation.** Native source-order probe10 flags all38 files, but each has11,707–204,890 label transitions: none is literally sorted into two class blocks. The signal is clustering in the published order; the publisher's preprocessing has no label-sort operation. The benchmark reorders by real submission time and tests future windows, so clustering alone is not a demonstrated shortcut. Native full-source period13 uses38 monthly periods, testing the newest seven against the previous31: April rows/day z−1.3 does not show an exceptional count collapse; April failed rate19.42%, z+3.2, rises. The native reading identifies a rise as drift. Missing submissions remain unknown; this is no completeness certification.

Native probe18 was applied to eight separate actual-source head/tail windows (four files,10k records each;30.72M embedding cells), preserving within-window row order. It reports74,418 straight-line-morphology cells,24,194 surviving a much tighter value-relative check. A second, no-fit check of the most-hit April tail window shows19,642 of22,724 native hits (86.44%) in three-row runs with the same masked user/job/environment profile and both adjacent full vectors within1e-6 maximum absolute difference. Small nonzero steps of nearly identical encodings explain that measured subset. The published encoder is a fixed row-local transform of original strings and contains no neighbor interpolation; its cleaner excludes missing measurements rather than interpolating them. Remaining sparse morphology is unclassified, not a proven fill operation or class-dependent recording route. It would be wrong to call this either “no hits” or demonstrated interpolation leakage. Probe17's format-only AUC0.5 supplies a separate negative format-route test; it does not erase the raw morphology observations.

Native probe19 on the source-position preparation selection finds23,366,401 of25,866,900 rows excluded from the retained union, none unlabeled. Removed and kept failed shares are9.77% and11.02%, a1.251-percentage-point gap, below that helper's10-point flag. This is a transparent native temporal-budget/maturity selection, not `_clean` removing an outcome class: `_clean` returns its prepared data unchanged. The small global gap does not negate the already measured near-cutoff fast-completer selection. Probe20 scores only two actual excluded source columns here; ec1.0000 and duration0.6735 support their exclusion. Other dropped columns were not refitted merely to reconfirm known post-execution timing. Probe21 finds zero raw copies in the eight44-nonembedding windows; the exhaustive38-file raw-copy audit remains separately reused, not relabeled as a new full native probe21 run.

**Tooling boundary.** The updated raw CLI returns no raw table because `_load_raw` returns a dict. The tests above call the current native functions on explicitly aligned actual-source records; they are not a successful generic `--raw` CLI run. The current nearest-neighbor normalizer is AST-identical to the old one and still computes float32 standard deviations before promotion. On all2,500,499 retained values of embedding127/223, both stds underflow to0 despite383,135/379,755 distinct values; the native normalized output has5,000,998 nonfinite cells. Float64 stds are approximately1.697e-33/1.252e-33. The old separately labeled float64 tail recovery is still applicable under exact identity, but the full native leak CLI remains unpassed. No new nearest-neighbor fit was run and no lower292 historical feature scores were invented. This is a diagnostic implementation limitation, not nonfinite shipped data or a reason to mutate the source coordinates.

**What remains untested or limited.** Actual post-completion reporting latency; excluded/pending submission denominators; private original string regeneration; reliable parent/subjob intervention mapping; causal/preventable failure utility; complete new raw-interpolation coverage; and the first full tuned-family/probability check remain unknown or limited at the stated scopes. They are already part of the accepted approximate task or future trigger, not new affirmative claims. No current claim established a new Must violation or justified re-asking a settled decision. Full native leak-CLI success must not be claimed.

**Executed audit artifacts.** `claim-inventory.json`, `claim-primary-source-recheck.json`, `claim-metric-checks.json`, `claim-format-probe.json`, `claim-raw-probes.json`, `claim-period-probe.json`, `claim-fill-recheck.json`, `claim-probe-summary.json`, their scripts/logs and the current identity proof retain exact scopes and results. This audit ran no HPO, changed no data, and authored no human marks.

</details>

<details><summary>Prior focused column audit (2026-11-05)</summary>

**Focused column audit — current main, 2026-11-05**

**Verdict:** No new retained-column leak, dtype defect or cleaning decision is demonstrated. All 389 physical columns have a verdict: 388 predictors and the target. Preserve the accepted submission-time source representations and meaningful source class names. No new curator input is needed from this column recheck.

**Current checks and reuse boundary:** The current-runtime identity proof matches the reviewed frame-value/order fingerprint, dtypes, categorical values and order, all six membership arrays, metric spec and numerical-library versions. The full source-label/finite-value/constant-column scan from the prior audit is reused on that verified same frame, rather than represented as a new raw-source scan. The earlier audit's definition hash differs because it preceded final explanatory notes; its frame fingerprint is identical. The current copied definition remains byte-identical to the accepted final definition. The framework checksum changes from c7436e8d... to b655fe6b... solely because task metadata now explicitly serializes an empty `special_features` list; encoding the current metadata with the prior schema exactly restores the old checksum. This is no newly encoded feature.

**Executed now:** The updated native `curation_probes.dtypes.column_table` and `flagged` functions examined every categorical/numeric predictor as an exact, full-length column projection, using the local publisher codebook plus explicitly described latent coordinates. They produce 387 table rows, exclude the target and intentionally skip the datetime: **zero flags**, across all 2,500,499 rows. Peak RSS was 414.6 MiB. This is a direct invocation of the current native functions, not a claim that the CLI rebuilt the frame or fetched a remote codebook. Fresh full-length narrow checks separately verify all three nominal masks, their dtypes/levels/missing-proxy absence, the submission date and the target. No untyped object column occurs in that narrow projection. The machine-readable column table enumerates every physical column exactly once; the grouped table below summarizes it.

| Columns | Meaning and prediction-time status | Dtype/cleaning verdict | Current rule |
|---|---|---|---|
| `usr` | Stable masked submitting-user identity, source-supported at submission; 2,781 levels | Fine: unordered category, no nulls or common literal missing proxies | USE-3/10; LEAK-34; CLEAN-4/12/14 |
| `jnam` | Stable masked job-name identity, source-supported at submission; 359,636 levels; private original text unavailable | Fine with the accepted nominal rationale: opaque masks have no recoverable language semantics or ordered numeric scale | CLEAN-12/14; USE-1/10; LEAK-34 |
| `jobenv_req` | Stable masked requested-environment identity, source-supported at submission; 4 levels | Fine: unordered category, no nulls or common literal missing proxies | USE-3; LEAK-10; CLEAN-12/14 |
| `embedding_000` through `embedding_383` | The 384 publisher pretrained coordinates of original user/name/environment strings; individual latent meanings unknown; fixed input-only representation can be formed at submission | Fine: retain all published float32 coordinates; no new fit, scaling, imputation or label/all-row transform | LEAK-10/27/29; CLEAN-6/9/14/22 |
| `adt` | Submission instant, known at prediction and also temporal split index | Fine: datetime64[ns], monotonic, no nulls, 2021-03-01 through 2024-04-30 23:59:16; source offsets converted to Japanese calendar before timezone removal | USE-3; CLEAN-14/23; LEAK-37 |
| `exit state` | Eventual source label, not available at submission and never a predictor | Fine: unordered source words `completed`/`failed`, counts 2,224,912/275,587; no nulls, merge or dropped class; sorted positive class remains `failed` | USE-5; CLEAN-15/17/25 |

**Source/timing check:** The local publisher feature list names `usr` as submitting username, `jnam` as job name, `jobenv_req` as requested environment, and `adt` as arrival/submission time. The pinned author generation script fixes `JOB_FEATURES = [usr_or, jnam_or, jobenv_req_or]`, instantiates pretrained all-MiniLM-L6-v2, and passes only those original strings to `encoder.encode`. Exit state is computed separately from `ec`. Our definition only expands the published vectors and fits no encoder. This supports input-only availability; it does not expose the private original strings or private source change logs. The existing approximate-fit and post-run cohort-selection limits remain necessary.

**Changed rules do not create a new choice:** CLEAN-12 now expressly keeps undocumented/anonymized codes as categories; no private dictionary exists to decode the masks into human names. The richer ordinal/code-label helpers do not turn these nominal identities into measured quantities. CLEAN-25 expressly keeps a binary target that the source already names in words, so `completed`/`failed` is directly compliant: no No/Yes renaming or ordered target is needed. The updated scorer's sorted-class convention leaves this target's positive class unchanged. CLEAN-24 and CLEAN-26 concern molecule structures and measured spectra; these language-embedding coordinates have no molecular structure or spectral axis, so no spectrum/SMILES declaration or recommended domain encoding is appropriate.

**Runtime implementation check:** Current preprocessing adds `set_missing`, `decode`, ordinal support, and an `order_positions` refactor. The Fugaku definition calls neither new decoder nor ordinal declaration, and its stable chronological ordering and all column values are covered by the identity proof. Empty special-feature metadata alters serialization only. There is no new feature, target class, dtype or cleaning transformation to requalify semantically.

**Known limits retained, no new column issue:** Post-run source selection, nonzero-exit actionability and absent execution-to-parent identifiers qualify operational fit; they were already measured and accepted. Source strings have source-supported availability, while private snapshot completeness remains unavailable. Requested resource quantities outside this named source-representation version are not newly declared leaks, nor silently added. All allocated/used-resource fields, queue/scheduling/start/end/deletion times, exit code, duration, energy/power and performance-derived outcomes remain excluded; end time/exit code are used only upstream for maturity/target checks. Storage/lineage keys do not enter the 389-column frame. Recurring masked identities are legitimate under the accepted temporal known-system task.

**Tiny coordinates:** `embedding_127` and `embedding_223` remain finite and nonconstant, at approximately 1e-32 scale. A float32 normalization underflow in a diagnostic does not justify dropping or rounding them. Current dtype checks find no semantic code/count/ordinal issue; retain the original coordinates.

**Evidence and limits:** Artifacts include `column-verdicts.csv` (389 rows), `column-probe-current.json` (updated native functions, no flags), `column-nominal-target-current.json` (fresh narrow full-length checks), and `column-audit-current.json` (identities and scope). No models were fit and no whole 38-file raw audit was rerun by this column role. The old whole-frame scan is explicitly reused only after current identity verification. The repository, past decision stores and raw data were not modified. Public source basis remains the fixed F-DATA release, defining Scientific Data paper and author code at db67a65a4b6e91dcebd26147de191fa0051ad790.

</details>

<details><summary>Prior focused split audit (2026-11-05)</summary>

**Independent focused split audit — current-main refresh**

**Verdict: right with notes.** Retain the accepted temporal protocol and its formal SPLIT-10 exception. No new split, target, gap or curator input is required by the current-main changes examined. This is a focused recheck, not a new full-panel or model-family qualification.

**Fresh tests.** Independently read the full25,866,900-row narrow source metadata, the2,500,499-row selected membership table and the actual saved train/test arrays. All source submission/end intervals are present and nonnegative; latest recorded end is2024-05-14 02:38:02. The source-position pair is unique in selected metadata. Submission time and target align exactly with the identity-proven curated frame. Every one of the three1,000,000-row train sides and500,000-row test sides is disjoint, lies within its prescribed Japanese calendar side, and has strictly separated submission times. All retained training ends are strictly before the window start: zero late recorded outcomes.

The current definition's native full-source selection was rerun independently on those narrow tables. It exactly reconstructs all selected source positions, dates, target values and role bits, hence all six actual membership arrays. The core native split sampler is byte-identical across1964e1b2→9048f36a, git blob543a7fa66364eb77e785dfc7f3fb1bef0fd8a649. Fresh audit duration29.39seconds; no388-feature reconstruction or model fit was run.

| Test submissions | Eligible full-source train share before cap | Prior submissions excluded for late completion | Retained late train outcomes | Failed train / test | Test rows with training user |
|---|---:|---:|---:|---:|---:|
| Jan–Apr2024 | 90.984% | 28,118 | 0 | 97,086 / 59,253 | 97.981% |
| Sep–Dec2023 | 80.324% | 48,375 | 0 | 89,970 / 74,610 | 95.084% |
| May–Aug2023 | 65.322% | 10,387 | 0 | 84,588 / 57,135 | 74.121% |

**What the numbers establish.** The full-source eligible histories expand from65.322% through80.324% to90.984%, satisfying the50% historical-support floor before the native1M/500k per-side budget (SPLIT-14). The cap is not class balancing: failed counts differ by window and side. Three successive four-month windows are distinct refits with expanding underlying histories, newest first (SPLIT-11/14). The four-month refit cadence and extra May2023 evaluation month remain disclosed benchmark judgments rather than a claimed production cadence or literal reproduction of the paper's single June2023–April2024 holdout (SPLIT-12/19). No window was selected from these fresh checks or outer-model scores (SPLIT-21).

**Accepted exception remains an exception.** Current SPLIT-9 requires removal of outcome shortcuts; the recorded-completion filter still removes every observed late training outcome. Current SPLIT-10 also permits some ordinary no-gap applications when a fixed horizon or collection completeness removes fast-outcome selection. Fugaku does not gain that fact from the amendment: its target is eventual exit state with variable delay, and fast-completer selection is directly measured. Immediately before September,49.566% of last-day source submissions finish after refit; those late jobs fail at18.530%, versus0.292% among already completed jobs. This confirms, rather than eliminates, the known selection concern. Keep the exact completion filter, explicit Myunghwan-approved SPLIT-10 exception and its higher-principle live-refit rationale; do not recast it as an unconditional pass or an ordinary fixed-horizon application.

**Availability limits stay explicit.** Recorded completion is an availability proxy, not a verified ingestion clock. Hypothetical24h post-completion lag excludes1,099/1,049/1,111 records from the shipped newest-to-oldest train sides. No public reporting log or census of missing/pending/uninstrumented submissions is available in these artifacts. The fresh exact membership/scorer identity supports reuse of the existing paired200k-test sensitivity experiments: reviewed AUC0.86548/0.77748/0.79111; hypothetical24h lag0.85588/0.76689/0.78086; seven-day submission embargo0.84888/0.78190/0.74529. These are reused historical single-family diagnostics, not new fits or full HPO, and their score directions are not a reason to select the gap. The first tuned benchmark must still recheck maturity/reporting-latency sensitivity together with family separation, simple/user-history baselines and probability quality.

**Eventual target and recurrence.** In the selected test sides,1,080/5,092/6,253 labels end after their four-month submission windows, newest first. That is valid for the original eventual zero/nonzero target; the window limits submission dates and refit cadence, not a deadline for the outcome. All observed source labels eventually end before release. This does not establish complete submission coverage. User recurrence of97.981%/95.084%/74.121% is expected when predicting future executions on the same system, and is not a reason to fabricate cold-start grouping (USE-10; SPLIT-1/3/13). The unresolved execution-to-parent mapping remains an approximate-fit/weighting limit; no parent-level utility or submission-census claim is established.

**Current-rule disposition.** The amended temporal rules add no contradictory source fact, changed membership or newly demonstrated shortcut. Preserve prior issues1–3 and the final ship decision with their original provenance; no renewed acceptance or amendment is needed in this audit's scope. There is no fresh scientific finding requiring a remedy. The source-cohort, reporting-clock and parent-unit limits remain concerns already accepted with notes, not newly verified absences.

</details>

<details><summary>Prior focused precedent check (2026-11-05)</summary>

**Independent precedent review: updated-main Fugaku recheck**

**Status:** final independent precedent review complete. The current native identity proof and post-migration register support carrying forward the accepted decisions. No new curator input or reflection prompt is required within this rule-and-precedent review. I independently ran the old-runtime ROC-AUC comparison below; raw-data/model qualification is not independently rerun by this role.

**Inputs examined:** current main `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`; current principles, temporal rules, metric rules, CLEAN-14, review application and persistent-review file contract; original item and final ship stores and their application receipts; both decision registers (4,023 decisions/21 candidate flags before migration; 4,079 decisions/25 candidate flags after migration, 176 rule IDs); closest Cases rows and actual CC history. The current native definition is the byte-identical carried-over reviewed Fugaku definition; the main session's exact computational identity proof passed.

| Decision | Result | Closest precedent and current-rule reading |
|---|---|---|
| Preserve eventual zero/nonzero exit-state prediction at submission | consistent; implemented task unchanged | Original item1 and final ship accept a future measurement with approximate execution-record fit; USE-5/8 preserve the real measured target and state its actionability/cohort gap. No updated rule requires a fixed-hour target, parent-level target, or silent new failure taxonomy. |
| Preserve precise recorded-completion filtering and zero additional embargo | departs with an already stated and accepted reason | This remains the original SPLIT-10 Should exception, serving P4/SPLIT-1 live-refit fidelity, with every retained recorded outcome ending before refit. It is not an exception to SPLIT-9 Must. New SPLIT-9 wording still requires removing any demonstrated late-own-entity shortcut. No new such shortcut follows from reading the amendment alone. |
| Keep fast-completer selection and unreleased reporting latency explicit | consistent and necessary | The amended SPLIT-10 makes measured selection and label timing central. Fugaku has an eventual variable-delay outcome and measured recent selection; it is unlike the new lt_vehicle_loan_default_prediction application, which relies on one common due-date horizon and no measured outcome selection. Do not relabel Fugaku's accepted exception as a clean zero-gap application or a fixed-horizon case. Existing factual maturity and latency-sensitivity obligations were completed and remain evidence, not proof of actual ingestion timing. |
| Keep original masked identities nominal, pretrained 384-coordinate representation numeric, and submission datetime | consistent with the documented CLEAN-14 Should departure | Updated CLEAN-14's ordered-scale rules do not turn opaque nominal user/job/environment identities into an ordinal scale. The explicit rationale for high-cardinality job names survives: their arbitrary masked strings do not recover private original text. No new reinterpretation is justified without contradictory source/data evidence. |
| Retain declared fallback ROC AUC | consistent | MET-5/6/8 and MET-11 still allow the binary fallback where the paper reports generic accuracy/classification-report metrics without an operational threshold, cost or uniquely justified selection criterion. The new context origin is available when the task makes a different metric obvious; it does not force a new origin or metric here. The heart_disease fallback case remains analogous; no source-defined cost or threshold is newly established. |
| Retain with the first-tuned-benchmark recheck | consistent | open_university_learning_analytics_dataset TP-3 explicitly retains no_spread pending the first tuned run; it is now an applied case, not an unfulfilled requirement to perform full HPO before this build. Fugaku's original no_spread/drift_baseline decisions preserve family separation, simple/user-history baselines, probability quality and label-maturity/reporting-latency sensitivity as that future trigger. This recheck/build is not itself a tuned benchmark run. |
| Carry forward the actual overall ship decision | consistent; task identity and fixture scorer equivalence passed | Original final ship is an actual Myunghwan decision, not a panel recommendation. The new user request explicitly says to reuse past decisions. A new semantic question is warranted only if the current package or stronger evidence contradicts those decisions. |

**Metric-review UI:** the new separate metric box is a procedural presentation change, not evidence that the accepted metric changed. The original final ship snapshot included the ROC-AUC fallback definition and its stated reason. If the current check proves the same labels, inputs, memberships, objective and scoring behavior, a faithful CC/history line can say the declared metric was accepted within that original ship decision and is carried forward under the November5 reuse instruction. Do not invent a new `metric.ok` human mark, silently assign the old mark a new snapshot identity, or claim the curator separately clicked a metric control that did not exist. If the implementation or score direction changes, requalify it first and return only a resulting semantic choice.

**Review-history migration:** restore archived original issue IDs1–3, retain the exact actual human turns and their dated resolved outcomes, and retain the original full panel as historical evidence. Append the new focused review as current evidence; do not present the old panel as rerun. The next genuinely new issue is4. Current policy retains REVIEW.md after resolution; the old deletion was historical behavior, not a reason to erase or re-ask the decisions. A fresh page may display resolved history and reference the original ship provenance without importing old marks against fresh fingerprints.

**Register candidates checked:** the pre-migration register's broad amendment_due flag counts six SPLIT-10 dataset names, including dated exception history and separate case-table entries. Current rule text already records the November4/5 amendment; stale exception text for lt_vehicle is explicitly superseded by later CC/application. The operative principle asks whether the same reason has produced a third exception, not whether every exception anywhere mentions SPLIT-10. Fugaku's measured-completion/live-refit rationale differs from missing outcome dates plus a training-floor conflict (lending_club/alfa), month-resolution delays (Ames/Perth), and fixed-horizon finalized first-EMI outcomes (lt_vehicle). No new third-same-reason amendment or reflection prompt is established. Likewise, mentioning SPLIT-9 inside the rationale for an exception to SPLIT-10 does not create an exception to SPLIT-9.

**Original decisions preserved:** the original item decisions, their notes and the explicit November 3 ship verdict remain separately attributed. Later checks establish reuse of the reviewed task rather than a new scientific decision.

**For the mediator:** preserve the accepted choices and future recheck. Keep the formal SPLIT-10 exception and qualification caveats. Current identity/scorer verification and the post-migration register reading are complete as below; preserve persistent resolved history. Bring back only a concrete new contradiction or a genuinely changed task choice; no new reflection prompt is required by this independent check.


**Current identity and scorer verification completed:** the current definition SHA remains `16f04dad621437b6b0d7e3a9d59ed77882641954ec379c640573cf9c31cedd98`. Native checking passed27 checks with zero errors/warnings and the same two informational heavy-check skips. The main session's saved proof exactly matches reviewed frame values/order SHA `2c64d4129380d494ae03e3f24a3f9ccd593f1811ce077cb6fd20c0ebfce04e5b`, category metadata, all six membership hashes, metric spec and library versions. All three1M training sides still have zero recorded unavailable labels. The only native serialized-metadata addition is the empty task field `special_features=[]`. Re-encoding the actual old metadata layout on the current container exactly restores the original checksum `v2:c7436e8df22a906088cadbb4d641da32cd709976aeaa43e087ac12ff278475cd` from the new `v2:b655fe6b87263768dd5a2e1232484929a22c3364e7daeeaa6b5cb6a30dc4a06d`; no existing metadata field differs.

I independently ran the pinned old runtime's scoring core on the current scorer's deterministic fixtures for every500k test row of each shipped fold, both one-column probabilities and aligned two-column probabilities. All six old/new scores match exactly (absolute difference0): newest to oldest `0.49743700643841415`, `0.4985142501699026`, `0.498459600516546`. This is a score-equivalence diagnostic on synthetic probabilities over actual test labels, not a new model result. The old no-input, row-unit score core is exactly the part called by that old container scorer; no old container reconstruction or model fit was needed. Evidence: `identity.json`, `scorer-current.json`, and this panel's `scorer-old-runtime.json`; the fixture SHA is `fbca8c30ff0380071bba6063699efbc7b7d01e2385af4c90c1760d5d1ebe1fa8`.

**Post-migration register reading:** five of its25 candidate flags mention Fugaku. Two exception_to_must flags attach SPLIT-1 to the exception paragraph/Case; a third attaches SPLIT-9; the generic SPLIT-9 third-exception flag inherits that misclassification. The exception is explicitly to SPLIT-10 only. SPLIT-1 is the higher rule it serves, and SPLIT-9 is explicitly still satisfied. The final generic SPLIT-10 seven-dataset flag mixes the distinct mechanisms and superseded history described above; it is not the third occurrence of Fugaku's reason. These are candidates rejected by semantic inspection, not new scientific departures to put to the curator.

**Final recommendation for the mediator:** carry forward original issues1–3, their completed maturity follow-through, the original ship verdict and its unchanged metric. Preserve the formal SPLIT-10 exception and selected-cohort/action-unit/reporting-latency limitations. Restore persistent resolved review history under current main's convention, with exact original human provenance and original panel identified as historical; append the new focused panel as current. Do not manufacture fresh source-bound marks or pretend the existing model evidence is a new run. No new curator decision is required by this review. The first tuned-benchmark recheck remains a future obligation; this runtime refresh and build do not discharge it. Any genuinely new factual contradiction from another auditor must still be considered on its own evidence.

</details>

<details><summary>Prior focused mediator (2026-11-05)</summary>

**Focused-panel mediation — Fugaku current-main refresh, 2026-11-05**

**Recommendation: ship the unchanged task, carrying forward the accepted decision.** This is an agent recommendation after the current focused recheck, not a new human mark. The current evidence establishes no new target, retained-feature, split or metric defect that requires reopening Myunghwan's November3 decisions.

**Validity:** The original eventual zero/nonzero exit-state target, submission-time representations and temporal execution-record evaluation remain supported (USE-1/3/5/8; LEAK-1/2/10; SPLIT-1/9). Operational fit remains approximate: the released cohort is selected after execution, nonzero exit is not necessarily actionable failure, and parent/subjob intervention identity is unrecoverable. Keep the explicit SPLIT-10 exception and its fast-completer/reporting-latency qualifications. **Value:** Existing ranking evidence remains applicable, with no_spread/drift_baseline and the agreed first-tuned-benchmark recheck preserved (TP-1/2/3/4). No full HPO or newly established operational probability utility is claimed. **Quality:** The original class words and nominal masks remain appropriate under current CLEAN-12/14/25; the source coordinates are unchanged. **Weighed:** source provenance, substantial temporal support and measured ranking signal favor retention; cohort/action-unit and reporting-clock uncertainty remain the accepted limitations. **For the curator:** zero new decisions from this recheck.

**Changes to make now, requiring no new decision**

1. Retain restored issue IDs1–3 with their exact original human turns and dated resolved outcomes, the original ship provenance and the historical full panel. Append the current focused reports as new evidence. Do not import old marks against a new snapshot, invent a fresh metric click or present old model/panel work as newly rerun (EV-2/7/8; current persistent-review contract).
2. Retain the faithful current CC explanation that the unchanged ROC-AUC metric is checked through the original package acceptance and the explicit November5 reuse request. The separate metric UI is procedural; scorer equivalence supplies the required factual bridge, not a new semantic choice (MET-2/5/6/8/11).
3. Complete the separately authorized build/reload/input-reproduction work using current main. The generated card currently marks the November3 UUID stale because the new schema serializes `special_features=[]`; a new current-runtime container is the appropriate mechanical update. Do not change the target, features, categories, memberships or metric to recover the old framework checksum.
4. Preserve the probe limitations accurately: current native-function supplements ran at their stated scopes; generic raw CLI applicability and full native nearest-neighbor CLI completion are not passing checks. No new native bundle warning needs acceptance, and no source coordinate should be dropped to hide a diagnostic normalization bug (EV-3/7/8; CLEAN-1/22).

**Issues for the curator**

None newly established. Original issues1–3 are settled, and the prior overall ship decision remains applicable. The first tuned benchmark must still examine model-family separation, foldwise simple/user-history baselines, probability quality and maturity/reporting-latency sensitivity. This refresh and its untuned diagnostic fits do not discharge that future obligation.

**Agreed facts and disputed-flag dispositions**

- Exact current frame values/order, category metadata, all six membership arrays, metric specification and library versions match the reviewed package. The only serialized metadata addition is an empty `special_features` field. Encoding the actual old metadata layout on the current container exactly restores `c7436e8d…` from current `b655fe6b…`. All six old/current ROC-AUC comparisons on every500k-row test side match exactly; these are synthetic-probability scorer tests, not new model performance.
- The fresh claim audit verified all38 publisher file sizes/MD5s and every zero/nonzero label:25,866,900 records,2,558,519 failed, zero label-code disagreements. The split auditor independently reconstructed full-source native selection and every actual array: each train/test side is1M/500k, zero retained recorded late outcomes, correct Japanese calendar boundaries and no balancing. Current native checking passes27 checks with zero errors/warnings and two known budget-skip infos, supplemented by the recorded full-data audits.
- Current-rule changes do not convert Fugaku into the fixed-horizon no-gap case. Its eventual variable-delay target and measured recent fast-completer selection persist. The accepted exception serves live-refit fidelity while satisfying the observed completion boundary; ingestion arrival remains unknown. The exact same memberships/scorer support reusing the existing paired latency/embargo diagnostics without selecting a gap from outer scores (SPLIT-9/10; EV-8).
- New format-only probe17 scores0.5 AUC versus0.804219 for its fresh same-protocol numeric/categorical baseline, on the three shipped folds with50k-per-side caps and200-tree untuned LightGBM. It establishes no predictive number-format route. It is not comparable to the differently capped historical three-family means and is not HPO (LEAK-13/15/39; EV-8/9).
- Raw-order flags in all38 files establish clustering, not literal class sorting: every file has many label transitions. Full-source period13 finds a rising April failed rate, not a falling terminal-outcome signal; no exceptional row-count collapse is flagged. Neither result establishes a submission census or rules out missing/pending jobs (LEAK-24/25; EV-3/7).
- Raw18 finds straight-line morphology in eight actual-source10k windows. Native absolute tolerance overflags tiny coordinates; the tighter check still has sparse hits. A second check explains86.44% of the worst-window native hits through recurring three-field profiles and nearly identical neighboring vectors. The inspected pinned encoder is row-local and has no neighbor interpolation; its cleaner excludes missing measurements rather than filling them. The unclassified remainder is not a demonstrated fill operation or class-specific recording route. Report these observations and their scope; neither erase the hits nor label them interpolation leakage (LEAK-13/15/39/40; EV-3/6/7).
- Probe19's kept/removed source-preparation shares differ by1.251percentage points, within declared temporal/maturity/budget selection; `_clean` is identity. This does not erase the already measured near-cutoff selection concern. Probe20's excluded `ec` AUC1.0 is a positive control for a known target-derived field, not evidence that the retained task is trivial; excluded duration is likewise unavailable at submission. Eight fresh raw-copy windows contain zero copies; the full38-file raw-copy scan is explicitly reused under identical publisher bytes, not relabeled as a fresh exhaustive probe21.
- The generic raw CLI returns no table for this dict-based loader. Current nearest-neighbor normalization is unchanged and still underflows float32 standard deviations in two finite, nonconstant source dimensions. The resulting nonfinite normalized cells are a diagnostic implementation failure, not nonfinite shipped values. The old separately labelled float64 recovery remains separate; no new NN fit or clean full native leak-CLI pass is claimed (EV-7/8).

**Consistency and provenance**

The independent precedent review supports carrying the original task, qualified SPLIT-10 exception, ROC-AUC fallback, ship verdict and future recheck forward. Register flags that attach SPLIT-1/SPLIT-9 to the SPLIT-10 exception paragraph are mechanical rule-ID overreach; the generic third-exception count mixes distinct mechanisms and superseded history. They do not establish an unreasoned departure or a new reflection question. Current CLEAN-25 expressly preserves binary class words already named by the source, and CLEAN-12 supports opaque codes as categories. No rule amendment or renewed task/label choice is needed.

The original source-bound decision stores remain unchanged. Persistent resolved review history and the current focused panel are a transparent procedural migration. This recommendation is limited to the completed focused claim, column, split and precedent evidence plus current identity/scorer checks; it is not a new full panel, causal utility validation, ingestion-clock verification, submission-census certification or completed future tuned benchmark.

</details>

<details><summary>Prior focused review editor (2026-11-05)</summary>

**Current focused cold review editor (2026-11-05)**

**Verdict:** Ready to carry forward the accepted scientific decisions after the two presentation corrections below. No new curator choice, model experiment or acceptance mark is needed. The separately authorized current-runtime build still has to complete.

I read the current review-editor brief and full current principles, writing and review-file-format references before the draft. I read the opening outcome/issues cold, the historical panel structure and status statements, and all five current focused reports; I checked claims against the current definition, generated README and curation record. This is an editorial/provenance review, not an independent rerun of the other auditors' experiments or a direct re-audit of the original decision stores.

Concrete corrections, most important first:

1. Scope the record's leading warning to its historical screening text. At `curation/records/fugaku_hpc_job_failure.md:33`, the warning currently applies to every note below it, including the restored human acceptance and measured qualification. The later historical explanation is too far down to repair that first impression.

   Old: “**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**”

   New wrapper: “**Current status (2026-11-05):** Myunghwan accepted the reviewed task on November 3 with the required first-tuned-benchmark recheck; the November 5 refresh carries that decision forward. The earlier screening drafts below retain their original status and wording.” Then “**Historical AI-screening notice (preserved verbatim):**”, followed by the complete original warning as a blockquote.

   The parent has accepted this finding and plans this stronger preservation approach under a fresh ownership guard. This report does not claim it is already installed.

   Preserve the dated screening/scouting entries themselves and all exact human words. This is a clarity repair, not a new verification request or permission to change the record's structured workflow fields.

2. Date each old panel role's wrapper as historical. The top panel paragraph and first historical-summary toggle already explain the boundary correctly, but the next ten toggles have undated names such as “Mediator” and “Claim audit”. A reader opening “Mediator” encounters “ship after changes” and three apparently pending choices. The current file-format documentation also says the mediator section is initially open on the review page. Make the history boundary visible on each old toggle, preserving every original report body.

   Old: `<details><summary>Mediator</summary>`

   New: `<details><summary>Historical mediator (2026-11-03)</summary>`

   Apply the same wrapper-only change to Claim audit, Column audit, Split audit, Domain practitioner, Blind review, Precedent check, Advocate, Critic and Review editor. Leave the dated “Current focused … (2026-11-05)” sections separate. Do not rewrite the old reports' pending-result or earlier-checksum statements as current facts.

3. Optional copy edit: make Main points solely the current decision summary. Its present next-issue-number and decision-store sentences are useful AI migration instructions but distract from the curator's remaining action.

   Old: “**Main points:** Reuse the November 3 ship decision under the explicit November 5 request. Original issues 1–3 remain resolved below; the next new issue would be 4. No issue, field disagreement or metric choice needs renewed input. The original decision stores retain their exact source identities. Reporting latency, cohort/parent-unit limitations and the first-tuned-run follow-up remain explicit.”

   New: “**Main points:** No new decision is required. Carry forward the November 3 ship decision under the November 5 request, preserving approximate execution-record fit, the accepted no-extra-gap exception, reporting-latency limits and the first-tuned-benchmark recheck.”

   Keep the issue-number and source-store instructions in the existing current precedent/mediator reports. The next genuinely new issue remains 4.

4. Optional copy edit: add missing spaces around numbers in current focused reports only. Examples: “all38” → “all 38”; “every500k” → “every 500k”; “issues1–3” → “issues 1–3”; “Hypothetical24h” → “Hypothetical 24h”; “by1.251percentage points” → “by 1.251 percentage points”; “November3” → “November 3”. Keep numbers, hashes, artifact basenames and exact stored human words unchanged. Do not mechanically rewrite preserved historical reports.

**What is already ready**

- The outcome leads with carry-forward shipping, then validity, value and quality, with no new curator decision. Its claims are supported by the current focused reports. Source-selected cohort, intentional nonzero exit, unrecoverable parent/subjob action unit, fast-completer selection and unobserved reporting latency remain explicit. The exception remains to SPLIT-10; the recorded SPLIT-9 boundary still has zero retained late training outcomes.
- Original issue IDs 1–3 each have a dated resolved turn. Their human strings match the restored record: “As far as some measurement reflects the futures, it's OK”; “Training gap is not a big concern. But potential issues with matured labels need to be checked.”; “Yes with the recheck”. The record separately preserves “ship this”. These archived resolved issues should remain history; their older prose format is not a reason to reopen them or create replacement issues. No record-field disagreement row is present.
- There is one panel label, sixteen matched nonnested details sections, one record-title heading and three resolved issue labels before the panel. The old reports and current focused reports are separate. Do not claim the full original panel was rerun.
- The metric-history line expressly carries forward acceptance within the old package verdict and the current reuse request. It claims no separate new metric click. Current precedent evidence explicitly forbids `metric.ok` invention and rebinding old source snapshots. This editor has not modified or independently rehashed those decision stores.
- The generated README reports current checksum `v2:b655fe6b87263768dd5a2e1232484929a22c3364e7daeeaa6b5cb6a30dc4a06d` and the actual November 3 build with `v2:c7436e8df22a906088cadbb4d641da32cd709976aeaa43e087ac12ff278475cd`, marked stale. That is the expected pre-build state. The focused reports explain the new empty `special_features` metadata field. Complete the authorized build and regenerate the card; do not hand-edit the generated stale marker or alter the unchanged task to recover an older checksum. The boilerplate claim that `dataset.py` changed is explained by the current mediation's serialization note; it is not evidence of a new scientific task.
- Current reports preserve the first tuned-benchmark obligation: family separation, foldwise simple/user-history baselines, probability quality and maturity/reporting-latency sensitivity. Current untuned fits and synthetic-probability scorer comparisons do not fulfill that obligation.
- Generic raw CLI applicability remains limited by the dict loader. Native nearest-neighbor normalization still fails on finite nonconstant tiny source coordinates; historical float64 recovery is separately labeled. The text does not promote native-function supplements to a clean complete native leak-CLI pass, claim new NN fitting, or use the diagnostic bug to justify dropping coordinates.

**Reviewed local identities**

- REVIEW.md SHA-256: `13f9db52b5ccb2e0ecb7f6179106ed71af26d6b55a4c8f4f8687c995244041ef`.
- dataset.py SHA-256: `16f04dad621437b6b0d7e3a9d59ed77882641954ec379c640573cf9c31cedd98`.
- README.md SHA-256: `600fc02501c4c175893b158b35715fd2686719537222108204a1b5d0e51db9f4`.
- Record SHA-256: `d730d99bb361d8de7470520543538801600bf1eee617a986baa6b5f28b99c267`.


</details>

<details><summary>Current maintained-runtime claim audit (2026-11-06)</summary>

**Independent focused claim audit — Fugaku, 2026-11-06**

**Recommendation:** retain the accepted definition and decisions. This maintained-environment recheck establishes no new target, feature, split, metric or source-procedure defect. **New curator issues: 0.** The original issues 1–3 remain resolved; the required first tuned-benchmark follow-up remains outstanding. The accepted approximate execution-record task, cohort/parent-unit limitations and explicit SPLIT-10 exception remain part of this conclusion.

The independent reuse check compared qualification code and dependencies with the November 5 version: all 49 files under `src` match, and the only difference among 80 curation-guidance files is the existing Fugaku SPLIT-10 Cases row. The five numerical-library versions match. No new scientific or probe implementation is inferred from a different installation.

I read the current definition, migrated record and README claims, the current claim-auditor contract, principles/evidence/metric rules, the prior literal claim inventory and 32-claim report, and actual metric, format, raw, period, fill, column and split evidence. I reread the cached pinned encoder/cleaner and the load-bearing paper/experiment sections; all five cached primary-source files freshly match SHA-256s in their original source manifest. No source document was downloaded and no raw cohort/model was rerun by this auditor. The script records the exact source and reused evidence identities in `claim-reuse-check.json`.

**Current claims tested adversarially.** “Holds” has the bounded scope stated in the row. Parent-executed data identity is distinguished from this auditor's independent comparisons and scorer checks.

| Claim | Source | Cheapest refuting test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| Current source pin is `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`, the same upstream main used November 5 | Current migration/delta; November 5 manifest | Compare actual source/procedure bytes rather than infer change from the word “upgrade” | Holds | 49 source files identical across all three copies; 80 procedure/agent files identical between work checkouts; only vendor's missing local SPLIT-10 case differs | EV-1/2/8 |
| “past_decisions_reused”; no new scientific marks | Migration; migrated record/REVIEW | Compare inherited definition/record/review to actual completed prior package and read decision attribution | Holds for the inspected migration | Definition, initial migrated record and REVIEW byte-identical; original November 3 ship, gap and retain-with-recheck history and November 5 metric carry-forward remain attributed to their original decisions. This auditor creates no human marks | EV-2/7; consistent judgment |
| The current definition preserves the accepted task | Definition and migration | SHA-256 comparison to November 5 accepted definition | Holds, independently executed | SHA-256 `16f04dad621437b6b0d7e3a9d59ed77882641954ec379c640573cf9c31cedd98` | USE-5/8; EV-1 |
| Historical data probes speak for the current shipped task | Current `identity.json` | Compare frame/order/dtypes/category domains, every membership array, metric spec and libraries; inspect actual proof code | Holds at exact inspected identity | Parent freshly executed native check/frame identity. I independently compared its results to November 5: frame hash `2c64d412…`, all four categorical domains and all six split hashes match; 2,500,499 rows and 388 predictors unchanged | EV-7/8; PROV-1; SPLIT-9/14 |
| Current checksum remains `v2:b655fe6b…`, with earlier `c7436e8d…` explained solely by old metadata encoding | Current identity and November 5 identity | Compare fresh checksum and old-schema counterfactual; inspect metadata differences | Holds | Both exact checksums match November 5. The only difference from the November 3 schema remains empty `special_features=[]`, not a new November 6 data change | EV-1/2/8 |
| All six fresh one-/two-column ROC-AUC fixture scores match the prior runtime | Current `scorer-current.json` | Exact numeric comparison to actual November 5 file | Holds, independently compared | All six equal exactly: per-fold AUC 0.49743700643841415, 0.4985142501699026, 0.498459600516546 in both representations | MET-2/13; EV-1/8 |
| “The metric computes at the shipped unit on every fold” | Definition fallback `roc_auc`; README Metric | Independently score constant and oracle predictions on current identity's actual 500k fold-label fixtures through installed native `scorer` | Holds, newly executed | Dummy 0.5 and oracle 1.0 for all three folds; failed support 59,253 / 74,610 / 57,135; row unit, identity target scale, no auxiliary metric inputs | MET-2/3/13; TP-5/9 |
| Source has no fixed operator cost/threshold or deliberate task-specific accuracy criterion | Definition metric reason | Reread retained Technical Validation and baseline code at pinned source revision | Holds as retained source reading | Paper describes “simple and widely used metrics,” accuracy for classification; baseline calls `classification_report`. No newly discovered competing selection criterion. Source files match their fixed manifest | MET-1/5/6/8/11; EV-2/7 |
| “accepted_check_warnings = {}”; current native check clean | Definition; current identity check bundle | Read actual fresh native check output | Holds | 27 native checks; 0 errors, 0 warnings, 2 explicit budget-skipped infos. Heavy duplicate/pure-value skips are not newly completed whole-table checks | EV-7; verification |
| “The raw data is not one table” for this definition's generic raw CLI | Actual `_load_raw`; `dataset_io._raw_state` | Inspect actual unchanged loader and helper predicate | Holds as a tooling limitation | Definition returns dict; helper returns no raw table unless it is a DataFrame. November 5 native-function raw tests were explicitly aligned actual source, not generic CLI success | EV-7/8 |
| Float32 neighbor normalization and its previous failure are unchanged | Actual `curation_probes/leak.py`; prior normalizer measurements | Byte-compare helper implementation and confirm exact current task identity | Holds by exact-source/data evidence reuse | Helper still computes `num.std()` before float promotion. Prior measured embedding127/223 stds underflow to 0 despite 383,135/379,755 distinct values; 5,000,998 normalized nonfinite cells. No new neighbor fit or full native leak-CLI pass is claimed | EV-3/7/8; CLEAN-22 |

**Exact carry-forward scope.** The full literal inventory is `retained local evidence`; the prior claim-by-claim table is `retained local evidence`. Its 32 bounded claims and their source/test/result/rule entries are incorporated as dated evidence, supported by the newly established identity predicates above. They are not relabeled as newly executed source/model tests. The prior record's already-superseded “about 24M/about 20GB/direct fit” interpretation remains refuted as a current fact; the current accepted record already preserves it as historical, so this supplies no new issue.

The reused actual artifacts, each freshly hashed in `claim-reuse-check.json`, establish the following scopes:

| Evidence reused | What it establishes | Boundary preserved |
|---|---|---|
| November 5 `claim-raw-probes.json` | All 38 raw publisher MD5/byte counts and all 25,866,900 exit-code/label comparisons passed; failed count 2,558,519; zero mismatches. Native source-order checks found 11,707–204,890 label transitions per file, none literally two class blocks | These are November 5 scans. This auditor does not claim another November 6 full raw read; the parent's independent archive verification is separately evidenced. Source clustering alone does not demonstrate a temporal predictor shortcut |
| November 5 `claim-format-probe.json` | All 384 retained float coordinates in three exact folds, native RNG0 50k-per-side caps, 200-tree LightGBM: format-only and top-three format scores 0.5 against numeric/categorical baseline 0.8042185 | This is the same-protocol diagnostic, not the differently capped three-family task probe, not HPO and not a fresh fit today |
| November 5 `claim-period-probe.json` | Full-source 38-month period13; April failure rate 19.42%, z+3.24; rows/day z−1.26. Native reading is rate-rise drift | It does not establish a submission census, complete pending-job coverage or absence of censoring outside the released selected cohort |
| November 5 `claim-raw-probes.json`, `claim-fill-recheck.json`, `claim-probe-summary.json` | Eight separate actual source head/tail windows, 80k rows and 30.72M embedding cells: 74,418 native morphology hits; 24,194 survive tight relative check. Of 22,724 hits in most-hit April tail window, 19,642 (86.44%) have identical masked profiles and adjacent vectors within 1e-6. Zero raw-copy groups in those eight windows | Morphology is not proven interpolation and is not “no hits.” Remaining hits are unclassified; eight windows are not a full-cohort interpolation sweep. The prior exhaustive 38-file nonembedding duplicate audit remains separately dated |
| November 5 column audit and original whole-value/vector checks | 389 total columns/388 predictors; three nominal features and datetime support; zero fresh dtype flags; finite, length384 float32 source vectors under the prior complete scan | Byte-identical source construction/current retained frame supports reuse; private original text and private encoder regeneration remain unavailable |
| November 5 `split-auditor.json` plus current exact membership proof | Full-source rows 25,866,900; minimum eligible history 65.322%; zero missing/negative source intervals; zero unavailable recorded train outcomes. Native caps 1M/500k; late source outcomes excluded 28,118/48,375/10,387 newest-first. Test-user recurrence 97.9808%/95.0844%/74.1210% | Recorded completion is only a label-arrival proxy. Fast-completer selection is real; the September last-day late-versus-completed failed shares are 18.53% vs 0.292%. The SPLIT-10 exception is retained, not converted into an ordinary zero-gap pass |
| Original actual task-probe and train-only follow-up, carried explicitly by the November 5 panel | Mean untuned linear/RF/LightGBM AUC about 0.7941/0.7576/0.7826; ranking signal, bounded date/user-baseline follow-up and paired maturity sensitivity | `no_spread`/`drift_baseline` and required first tuned-family/probability/simple-baseline/maturity check remain. Two configurations are not full HPO, family separation or causal operational utility |

**Untested/limited claims, ranked.** Under P3/P4, complete attempted/pending submission coverage, reliable parent/subjob mapping, actionable/preventable failure utility and actual post-completion reporting latency remain unverified, exactly as accepted approximate-fit qualifications. Under P4/P5, private-string regeneration and complete raw-interpolation coverage remain unavailable/limited; there is no demonstrated new leakage mechanism. Under P6, full tuned-family separation, probability quality and the first tuned-run sensitivity recheck remain pending. Under EV-7, a successful complete generic raw or native float32-neighbor leak CLI is not established. The mildest remedy is to preserve the existing bounds and execute the already-required tuned-run trigger when that stage is authorized; none justifies reopening settled issue IDs or changing the definition today.

This audit writes only its own current run artifacts. It changes no repository source, prior evidence, decision stores, data or human marks; uses no network, GPU or additional qualification; and runs no model fits.

</details>

<details><summary>Current maintained-runtime precedent check (2026-11-06)</summary>

**Independent precedent review — maintained qualification refresh, 2026-11-06**

**Verdict:** carry forward the original accepted Fugaku decisions and ship verdict. **New human inputs: 0. New reflection prompts: 0.** No current rule, case comparison or native identity result examined here supplies a concrete contradiction requiring a new scientific choice. Preserve the formal SPLIT-10 exception, approximate execution-record fit, selected-cohort/action-unit/reporting-latency limitations and first-tuned-benchmark recheck.

This consistency review inspected the original curator decisions, relevant temporal/metric/type/value/use-case rules, prior qualification, the decision register, closest precedents and the new identity checks. It did not rerun raw-data or model qualification.

**Actual upgrade delta.** The reviewed source is `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`, already the actual source reviewed on November 5. My independent comparison of 20 relevant rule/procedure/role/register/metric-library files found every current checkout file byte-identical to November 5. Against the reference source, the sole difference is the restored Fugaku SPLIT-10 Cases row; normative rule text is identical. Exact hashes are in `precedent-rule-identity.json`. This source-identity reconciliation does not create a new metric or ship decision.

| Decision | Result | Closest evidence and rule reading |
|---|---|---|
| Keep original eventual zero/nonzero exit-state task and original class words | consistent | Myunghwan's November 3 item 1 and final ship accept the measured future terminal outcome with approximate per-execution operational fit. USE-1/3/5/8 and CLEAN-25 do not require a new failure taxonomy, fixed-hour target or parent-job aggregation. Preserve all cohort/actionability limits. |
| Keep exact recorded-completion filtering and zero additional fixed embargo | departs with an already stated and accepted reason | November 3 item 2, completed maturity follow-through and explicit SPLIT-10 exception serve SPLIT-1/P4 fidelity to completed outcomes at live refit. This remains a Should departure. It is no exception to SPLIT-9 Must. Current identity reports zero unavailable recorded labels in each shipped training side; unobserved ingestion latency remains a qualification. |
| Preserve masked categorical identities, 384 numeric source embedding coordinates and submission datetime | consistent | Original source-representations-first authorization and unchanged definition remain applicable. CLEAN-14's high-cardinality masked-name departure is documented: opaque token identities cannot recover unavailable original text. Ordered-scale amendments introduce no contradictory fact about these nominal identities. |
| Preserve fallback ROC AUC | consistent | MET-5/6/8/11 still support the fallback when the source reports generic accuracy/classification-report metrics without a unique operational threshold or cost. The applied heart_disease precedent (October 21; checked October 27) remains analogous. No newly established context metric or score-direction change appears. |
| Preserve actual overall ship and metric acceptance provenance | consistent | The actual November 3 final human words are “ship this”; the accepted package includes the unchanged declared metric. The November 5 CC faithfully records that provenance and explicit reuse instruction. Current HUMAN_REVIEW preserves earlier decisions absent contradictory evidence. The newer metric UI does not require inventing a separate historical metric click or a fresh ship mark for an identical task/scorer. |
| Preserve first-tuned-benchmark recheck | consistent | The applied open_university_learning_analytics_dataset TP-3 case (Lennart, October 22; later ship October 26) retains `no_spread` pending the first tuned run. Fugaku's equivalent November 3 choice additionally preserves foldwise simple/user-history baselines, probability quality and maturity/reporting-latency sensitivity. This refresh/build does not discharge that future obligation. |
| Preserve resolved issue IDs 1–3 and dated human turns | consistent | Current review-added skill and file format retain resolved history and the original full panel as historical. Issue 4 is the next genuinely new issue. No old mark should receive a fresh source snapshot, and the historical panel is not a newly rerun panel. |

**Register candidates inspected.** `decision-register-fugaku.json` contains 68 selected decisions out of 4,090, with 176 defined rule IDs and five Fugaku-related candidate flags. These are candidates, not findings:

1. Two `exception_to_must: SPLIT-1` flags index the record exception and its Cases row. Both explicitly depart from SPLIT-10 and cite SPLIT-1 as the higher rule served. They do not announce an exception to SPLIT-1.
2. The `exception_to_must: SPLIT-9` flag indexes the same paragraph's statement that unavailable labels still leave under SPLIT-9. It does not declare a departure from that Must.
3. The `amendment_due: SPLIT-9` count inherits broad rule-ID attribution and includes superseded lt_vehicle history. The actual alfa/Fugaku exception headings name SPLIT-10, while their text says SPLIT-9 must be met. The current lt_vehicle CC of November 5 explicitly supersedes its old exception and treats gap zero as an application.
4. The `amendment_due: SPLIT-10` seven-dataset count mixes distinct reasons: missing outcome dates and the training-floor conflict (alfa/lending_club), month-resolution with no measured outcome selection (Ames/Perth and related historical rows), superseded fixed-horizon lt_vehicle history, and Fugaku's precise-completion/live-refit rationale. Current rule amendments already address the earlier shared reasons. The principles ask whether **the same reason** has produced three exceptions, not whether three names mention one rule. No third instance of Fugaku's reason is established.

The register also classifies numbered text in preserved historical panel reports as `open_issue`. That heuristic count is not evidence that resolved curator issues reopened. Current issues 1–3 have their exact actual human turns and resolved labels.

**Current native identity evidence.** I inspected the main session's new `identity.json`; I did not independently regenerate its frame. Its status is `current_runtime_data_categories_splits_metric_and_versions_match_reviewed_task`. It reports byte-identical definition, frame/order SHA `2c64d4129380d494ae03e3f24a3f9ccd593f1811ce077cb6fd20c0ebfce04e5b`, identical category metadata, all six original membership hashes and unchanged metric specification. Each training side has zero recorded unavailable labels. Native checking reports 27 checks, zero errors, zero warnings and the same two disclosed heavy-check skips. I independently compared the fresh `scorer-current.json` to November 5: all six deterministic fixture scores match exactly for both one- and two-column probabilities on all three folds. The maintained metric-library bytes are also unchanged.

The current checksum remains `v2:b655fe6b87263768dd5a2e1232484929a22c3364e7daeeaa6b5cb6a30dc4a06d`. As on November 5, the historical checksum difference is fully explained by the new empty `special_features=[]` metadata field; encoding the original metadata schema restores `v2:c7436e8df22a906088cadbb4d641da32cd709976aeaa43e087ac12ff278475cd`. This is identity/scorer evidence, not new model performance or a newly established ingestion clock.

**Original decision stores preserved.** Repeated SHA-256 checks during this review exactly match the November 5 report:

| Original store | Snapshot binding retained | File SHA-256 unchanged |
|---|---|---|
| `retained local evidence` | `460955057d7ae98d40dab1ada853ce0be837c92fe306a8d2357635353e0a95e9` | `d288452f085392f408011f07ec120e78fe135f8bae9b3dde61554791605f787d` |
| `retained local evidence` | `86a1370cc633a537278cd750bc214b421d978f6519ac6635d34b7030a1dec54f` | `3e914cf13f78c9540255bd33ec1866ab1c32526bc07cc7974a3fd0156109400d` |

The item store retains Myunghwan's exact words: item 1, “As far as some measurement reflects the futures, it's OK”; item 2, “Training gap is not a big concern. But potential issues with matured labels need to be checked.”; item 3, “Yes with the recheck”. The final store retains the actual overall `ship` mark and “ship this”. Neither store contains a fabricated new metric mark, and neither was rebound to this run's source identity. Full checks and exact input provenance are in `precedent-checker.json`.

**For the mediator.** Proceed using the existing scientific decisions under the explicit repeated-cycle request. Preserve the original stores and resolved history; append only current evidence. No new human question is justified by this precedent review. A genuinely new contradiction from another audit still needs assessment on its own evidence. Actual post-completion reporting latency and the first tuned benchmark's value checks remain unresolved limits, as already accepted.

</details>

<details><summary>Current maintained-runtime mediator (2026-11-06)</summary>

**Focused mediator judgment record (2026-11-06)**

**Verdict: ship with the previously accepted qualifications.** Carry forward Myunghwan's original ship decision under the explicit repeated add/review/build request. The maintained runtime binding now points to the same source actually used on November 5. The completed current claim and precedent reports establish no new contradictory fact requiring a task change or curator choice.

**Validity:** USE-1/3/5/8 remain satisfied at the accepted approximate execution-record fit: eventual zero/nonzero exit state at submission, within the released selected cohort. The recorded-completion boundary meets the measured SPLIT-9 requirement; the accepted SPLIT-10 Should exception remains explicit and serves SPLIT-1 live-refit fidelity. Actual post-completion label arrival, complete attempted/pending submission coverage, preventable-failure utility and parent/subjob decision identity remain unverified. No new Must failure or leakage mechanism is established.

**Value:** Historical ranking signal remains applicable under exact task/scorer identity. MET-2/3/5/6/8/11 support the unchanged ROC-AUC fallback and its computation on every fold. TP-1/3/4 follow-through remains required at the first tuned benchmark run: family separation, foldwise simple/user-history baselines, probability quality and maturity/reporting-latency sensitivity. This maintenance cycle does not fulfill that future obligation.

**Quality:** Retain the accepted nominal masked identities, 384 finite source embedding coordinates, datetime input and original class words. The documented CLEAN-14 departure remains justified by unavailable private text and opaque stable identities. There is no newly supported cleaning remedy.

**Weighed:** source traceability, exact reproducibility, substantial chronological support and useful ranking signal favor retention. Selected-cohort coverage, uncertain intervention unit, fast-completer selection, unknown reporting delay and incomplete tuned evaluation retain their accepted limits.

**Changes to make now that need no decision**

1. Append the November 6 evidence and focused assessment to the current record/review, preserving dated resolved issues 1–3 and all historical report bodies. Distinguish the November 6 claim/precedent/mediator/editor roles from the reused November 5 column, split, dtype, raw, format and model evidence. The next genuinely new issue remains 4. This is evidence and judgment-history maintenance under the principles' process precedence and add-dataset step 8, not a new scientific mark.
2. Describe the change precisely: maintained pin/import binding to `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`, already November 5's actual source. Record the qualification source revision. The earlier November 3-to-5 metadata/checksum change is historical; the current checksum remains `v2:b655fe6b87263768dd5a2e1232484929a22c3364e7daeeaa6b5cb6a30dc4a06d` (EV-7/8).
3. Keep the current archive-verification and subsequent build results as separate evidence with actual completion status. At this mediation read, the parent reports archive verification ongoing; this report neither certifies it nor claims a new build. Preserve the previous built UUID/date until the actual build regenerates documentation. Routine evidence updates need no task/metric amendment (EV-7/8).

**Issues for the curator: 0. Disputed new decisions: none.** Earlier choices are preserved, not reopened. This is an agent recommendation and creates no human ship/metric field. Original review-store snapshot bindings must remain unchanged. The explicit later build stage remains outside this mediator's execution scope.

**Agreed facts and evidence scope**

- `upgrade-delta.json`, `runtime-equivalence.json` and `identity.json` report unchanged actual source, rules, numerical-library versions, definition, frame values/order, category domains, all six train/test memberships and metric specification relative to November 5. The claim auditor independently compared all 49 source files across the two work checkouts and installed vendor; the two work checkouts' 80 procedure/agent files also match. The vendor difference is the restored local Fugaku SPLIT-10 Cases row, with unchanged normative text. The definition SHA-256 is `16f04dad621437b6b0d7e3a9d59ed77882641954ec379c640573cf9c31cedd98`.
- The parent's freshly executed native identity/check proof reports 2,500,499 rows, 388 predictors, three 1M/500k train/test sides and zero recorded unavailable training labels. Frame/order SHA-256 is `2c64d4129380d494ae03e3f24a3f9ccd593f1811ce077cb6fd20c0ebfce04e5b`. Native checking ran 27 checks with zero errors, zero warnings and two known budget-skip infos. Skipped whole-table checks are not newly completed scans.
- All six fresh one-/two-column fixture ROC-AUC scores exactly match November 5. The current claim auditor additionally executed constant/oracle scores of 0.5/1.0 on each actual fold-label fixture. These checks test scorer behavior, not model performance.
- The current claim auditor rechecked cached primary-source identities and source reading, and independently compared reused evidence hashes. The November 5 38-file raw label/MD5 scan, column/split audits, format model fits, period/fill diagnostics and original task/maturity models remain dated reused evidence. This mediator ran no raw scan, model, scorer or data reconstruction.
- Source/timing qualifications, generic raw-CLI inapplicability for the dict loader and the unchanged float32 nearest-neighbor normalization failure remain explicit. The float64 recovery stays separately labeled. No clean full native leak-CLI pass or exhaustive raw-interpolation absence is claimed.

**Consistency with precedent**

The current independent precedent checker supports each carried decision. Fugaku's variable-delay terminal outcome and measured fast-completer selection distinguish it from the fixed-horizon zero-gap application in the amended lt_vehicle case. Preserve the accepted SPLIT-10 exception; no exception to SPLIT-9 or SPLIT-1 is implied. Register candidates naming those Must rules arise from paragraph-level attribution, while the generic third-exception count mixes mechanisms and superseded history; the checker found no third instance of the same Fugaku rationale. The applied accuracy-only-source ROC-AUC precedent and retain-with-first-tuned-recheck precedent remain aligned. No amendment or reflection prompt follows.

**Panel tier and freshness**

Focused recheck: current independent claim auditor and precedent checker, this mediator, and the cold editor still to read the synthesized draft. The definition, target, features and splits are unchanged, so the full blind/gamer/debate panel and new column/split runs are not triggered by this binding repair. The November 3 full panel and November 5 focused reports remain historical.


</details>

<details><summary>Current maintained-runtime cold editor (2026-11-06)</summary>

**Current maintained-runtime cold review editor (2026-11-06)**

**Verdict:** Ready to carry forward the accepted scientific decisions with the planned final composition and authorized build. Zero new curator choices or marks are needed. This report does not certify the subsequent build.

I read the full review-editor contract and its writing, principles and review-file-format references, then read the opening judgment and issues cold. I checked the historical/current panel boundary, current claim/precedent/mediator synthesis, definition, generated README, record and generated page data. The identity, upgrade-delta and runtime-equivalence reports support the scope of the refresh. I inspected reported identity results; I did not recreate their frame, run models or rescan source data.

Concrete editorial points, most important first:

1. Clarify the generated page's historical issue count in its run subtitle. The native collector's header says “Open: 1 record, 3 issues, 0 record fields, 0 cross-dataset items.” Its actual dataset has `openMarks=0`, exactly three items with `resolved=true`, and no field rows. A reader should not mistake the generated total for three renewed choices.

   Old subtitle: “Original decisions are retained under the November6 repeat request; new runtime-binding checks and reused evidence are dated separately.”

   Suggested replacement: “All three displayed issues are historical and resolved; no new curator decision is requested. Original decisions are retained under the November 6 repeat request; current runtime-binding checks and reused evidence are dated separately.”

   The parent reports this clarification applied to its run-local render helper for the final rebuild. I have not inspected that later output. Do not hand-edit the generated report or change the shared generator for this refresh.

2. Finish the already planned dated evidence composition. At this read, the record's leading status and last assessment are dated November 5. The current mediator accurately states that archive verification was ongoing at its read and makes no new-build claim. Preserve those dated statements, append the November 6 assessment and completed artifact facts at final composition, and regenerate the page after the actual build.

   Old leading status: “**Current accepted status (AI, 2026-11-05):** Myunghwan accepted this definition on November 3 and explicitly requested reuse of those decisions for the updated-main cycle on November 5.”

   Suggested current wrapper: “**Current accepted status (AI, 2026-11-06):** Myunghwan accepted this definition on November 3 and requested reuse of those decisions for the November 5 and November 6 refreshes. The maintained-runtime recheck found no new scientific choice; the first-tuned-benchmark recheck remains required.”

   Keep the dated November 5 assessments and exact human words. Record a new UUID/build time only from the completed native build. The parent confirms this final record update and separate dated completion evidence are planned; neither is a renewed scientific decision.

**What passes**

- The outcome leads with the ship recommendation, then validity, value and quality. The current reports support its unchanged task, approximate execution-record fit, measured completed-label boundary, historical ranking signal and preserved future recheck. The higher-ranked operational/timing qualifications remain visible in the current mediator.
- The only numbered issues remain 1–3, in validity-to-value order, each closed with its original dated human turn. The current review procedure preserves resolved history. Their older prose format is therefore no reason to rewrite them into new option tables, reopen them or manufacture issue 4. No field disagreement is buried in the panel.
- Every historical panel wrapper is explicitly dated; November 5 focused and November 6 maintained-runtime reports are separate. The draft page has 20 panel sections before this editor is appended. Old pending-result/checksum statements remain historical. Appending this report completes the named current panel; the full blind/debate panel is not represented as newly rerun.
- Generated page data exactly matches the current definition text. It contains three resolved items, zero open marks and zero field rows. The carried `metricChecked` is dated November 5 and expressly records unchanged-metric acceptance within the November 3 package and reuse request. It claims no separate new metric click. The old ship stores need no rebinding.
- `identity.json`, `upgrade-delta.json` and `runtime-equivalence.json` support the maintained import from vendor pin `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`, already the actual November 5 source. The definition is byte-identical; frame/order, categories, all six membership arrays, metric specification and numerical-library versions match. Six deterministic scorer fixtures match. This supports reuse of dated evidence without implying a new model comparison.
- The record and definition retain the formal SPLIT-10 exception, zero recorded unavailable training labels, fast-completer and unobserved reporting-latency limits, selected-cohort and parent/intervention-unit limits, and the required first tuned-run check of family separation, foldwise simple/user-history baselines, probability quality and maturity/latency sensitivity.
- The current checksum remains `v2:b655fe6b87263768dd5a2e1232484929a22c3364e7daeeaa6b5cb6a30dc4a06d`. The empty `special_features=[]` change explains the historical November 3-to-5 checksum difference. The pre-build README truthfully carries the November 5 UUID/time; it is not evidence of a November 6 build.
- Existing generic raw-CLI applicability and native float32 neighbour-normalization limits remain qualified. The historical float64 recovery is separately labeled. These accepted boundaries establish no new scientific choice and were not reopened by this review.

**Input identities at review**

| Input | SHA-256 |
|---|---|
| REVIEW.md | `ce687447d0c5ccdcc1401b0e1e9c4ab38e2f8ea40333db91f41ab11097ab9903` |
| dataset.py | `16f04dad621437b6b0d7e3a9d59ed77882641954ec379c640573cf9c31cedd98` |
| README.md | `80c15bc9f42ccc5d8bda69b52ae2a21d56cb98c8691dd358f0eb0c2a3042f8a3` |
| Curation record | `b11b1b55ef55eb7eaa8fc360fcc4e96ac983d2d58499f9f3218094c33bbc3fa7` |
| Draft review-page data.json | `a73783aac27cd169e1c7086844257601b7a43bbc3ee8655198e8c51bbada0844` |
| identity.json | `3502f67f12b079e986890e094264735ab146d6a4d4f388ada6225aa5cc057a82` |
| upgrade-delta.json | `c88126fa974ec88cb470b29e643aaea2ada9ec32f08147ab1847392de16343b9` |
| runtime-equivalence.json | `fd14468af3aa463ace37f0249e1a87988c26524a68111c83af64a18f0511cd24` |

These identities bind the reviewed draft rather than a later build. This review performed no new model fitting or raw-data qualification.

</details>
