---
report_format: data-foundry-report-v2
unique_name: fugaku_hpc_job_failure_1m
container_format: 2
checksum: v2:32c8b66e36ba62d860a64ab054e5ae8a7fdc45d9c7fd3299fbdbdd2fa49ef1e0
build:
  uuid: 01a1e3af-55a4-7df0-bd28-5009e8991055
  checksum: v2:4cfcfaad3da1a6271ad90e17ac9589a303bd8573baf5fe23acdd52e508f09f8d
  built_at: '2026-11-16T09:29:09+00:00'
  path: fugaku_hpc_job_failure/01a1e3af-55a4-7df0-bd28-5009e8991055
  data_foundry_version: 0.0.5
  git_sha: a6a4ac56259a656b235696d1e74d0a8c36f68f68
  libraries:
    python: 3.12.3
    pandas: 3.1.0
    numpy: 2.5.4
    pyarrow: 26.0.0
    scikit-learn: 1.7.2
    polars: 2.0.0
build_stale: true
data:
  n_rows: 24025345
  n_features: 393
  dtypes:
    category: 5
    datetime64[ns]: 1
    float32: 384
    float64: 1
    int64: 2
    int8: 1
  n_test_dataset_rows: null
task:
  target: exit state
  problem_type: binary_classification
  metric: roc_auc
  metric_origin: fallback
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: exit state
  time_on: adt
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 3
  n_folds: 1
  random_state: 4267
  time_horizon: 4
  time_horizon_unit: months
  time_gap: 1
  time_gap_unit: days
  n_train:
    min: 16880049
    max: 23517106
  n_test:
    min: 500000
    max: 500000
  row_budget:
    train: 1000000
    test: 500000
  train_sampling:
    default: newest_year
    unit: rows
    stratify_on: exit state
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicates_skipped
  - dataset_pure_feature_value_skipped
  accepted:
    time_newest_period_short: 'Accepted (Andrej, 2026-11-24, with the _1m version
      of review issue 5): the frame keeps every training row but only a 500,000-row
      sample of each test window, so its newest 30 days hold 3,055 rows a day against
      a median of 22,831 (13%). In the full source they hold 59% of the median (14,015
      against 23,854 a day), because the April 2024 observations begin on 4 April
      (the cohort-limit note).'
decisions:
- Full-source terminal-label availability and the test-window cap
---

# fugaku_hpc_job_failure_1m

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Binary classification of `exit state`, scored with `roc_auc` on temporal splits by `adt`. 24,025,345 rows and 393 features. Source: Other (2024).

Built as `01a1e3af-55a4-7df0-bd28-5009e8991055` on 2026-11-16, but `dataset.py` has changed since: it now gives checksum `v2:32c8b66e36ba62d860a64ab054e5ae8a7fdc45d9c7fd3299fbdbdd2fa49ef1e0`, so the build is stale. See [Build](#build).

## In brief

**Question.** Will a submitted Fugaku job terminate with a nonzero exit code?

**Use case.** For example, a supercomputer operator scores a job when it is submitted, to identify jobs that may need attention before consuming resources. The source motivates failure-aware workload management.

**One row.** One released job-execution record. The source contains 25,866,900 records from March 2021 to April 2024; this version keeps every training row each window can use and up to 500,000 test rows per window.

**Predicted.** The source's terminal exit state: completed for exit code zero, failed for nonzero. This is not a hardware-failure diagnosis; an intentional nonzero return may occur without failed computation.

**Known at prediction time.** The masked submitting user, job name and requested job environment, and the released 384-value pretrained embedding of those original strings; the requested nodes, cores, CPU frequency and memory limit; and the submission time. All are known at submission; the user cannot change these requests later.

**What the test data stands for.** Three successive four-month future windows on the same supercomputer, with earlier completed labels for training: May–August 2023, September–December 2023, and January–April 2024.

**Our changes to the source.** Keep the original labels and representations. Combine categories and embedding, and add the submission time and the requested nodes, cores, frequency and memory limit; the authors evaluated the representations separately and without these. Refit for three four-month windows covering May 2023–April 2024 instead of their fixed June 2023–April 2024 holdout. Exclude unavailable training labels; cap each test window at 500,000 rows, while each training side keeps every earlier labelled row.

> **Use case fit: approximate (a stand-in with a known gap).** The release keeps only jobs with post-run measurements, so coverage of all submissions is unknown, and each fiscal year is cut at 31 March on end time. Nonzero exit proxies actionable failure, and records do not map reliably to parent jobs. The operator sees each user's outcomes as jobs finish; that live history, outside this task, beat models on the identity and time inputs by 0.04-0.12 AUC.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/fugaku_hpc_job_failure.md`](../../../../curation/records/fugaku_hpc_job_failure.md)
- The original source: <https://doi.org/10.5281/zenodo.11467483>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/fugaku_hpc_job_failure/`. To get them:

```text
F-DATA v1.0 (2024-06-05), DOI 10.5281/zenodo.11467483. Download the 38 monthly Parquets from
that fixed Zenodo record, not a moving latest-release link. The publisher's byte counts and MD5s are pinned in
RAW_FILES in this definition. CC BY 4.0 applies to the released dataset; the separately licensed article and
restricted original RIKEN database are different artifacts. Retain attribution to Antici et al. and the DOI.

From the repository root, this standard-library recipe recreates and verifies the raw inputs. It needs public
HTTPS access to Zenodo, no registration or credentials. Every file is checked against the pinned publisher
byte count and digest before it becomes an accepted raw input.

    python3 - <<'PY'
    import ast, concurrent.futures, fcntl, hashlib, shutil, urllib.request
    from pathlib import Path
    definition = Path('datasets/_dev/tabarena-v0pt2/fugaku_hpc_job_failure_1m/dataset.py')
    tree = ast.parse(definition.read_text())
    files = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'RAW_FILES' for t in n.targets))
    raw = Path('local-data-warehouse/fugaku_hpc_job_failure/raw')
    raw.mkdir(parents=True, exist_ok=True)
    def md5(p):
        h = hashlib.md5(usedforsecurity=False)
        with p.open('rb') as f:
            for b in iter(lambda: f.read(8*1024*1024), b''):
                h.update(b)
        return h.hexdigest()
    def fetch(item):
        name, (size, checksum) = item
        target = raw/name
        with (raw/('.'+name+'.download.lock')).open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if not target.exists():
                partial = raw/(name+'.part')
                offset = partial.stat().st_size if partial.exists() else 0
                headers = {'Range': 'bytes='+str(offset)+'-'} if offset else {}
                request = urllib.request.Request('https://zenodo.org/records/11467483/files/'+name+'?download=1', headers=headers)
                with urllib.request.urlopen(request, timeout=90) as response:
                    assert not offset or response.status == 206, 'Resume range was not honored'
                    with partial.open('ab') as stream:
                        shutil.copyfileobj(response, stream, length=1024*1024)
                assert partial.stat().st_size == size and md5(partial) == checksum, name
                partial.replace(target)
            assert target.stat().st_size == size and md5(target) == checksum, name
        print(name, 'verified', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(fetch, sorted(files.items())))
    PY

Preparation reads all source rows' submission/end times and labels, checks the original zero/nonzero mapping,
and caps each test window at the collection's 500,000 test rows; every training row stays. It then expands the
384-value source vectors of the rows the splits use only. source_metadata.parquet and selection_membership.parquet
retain local selection lineage; selection.json records full-source monthly counts, cutoff exclusions and class
support per side. These are reproducible intermediates,
not additional upstream releases and not model inputs. The preparation code and constants participate in the
framework's prepared-input cache hash. _make_splits repeats native selection against full-source metadata and
checks exact source positions before removing lineage columns. No container is built by dataset check.
```

On first use, `_prepare_raw_files` writes `prepared_source_representations.parquet`, `selection.json`, `source_metadata.parquet`, `selection_membership.parquet` into the same folder.

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/fugaku_hpc_job_failure_1m   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/fugaku_hpc_job_failure_1m   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://doi.org/10.5281/zenodo.11467483 |
| year | 2024 |
| domain | technology & internet |
| license | CC BY 4.0 |
| data_tags | Non-IID, Temporal, Anonymized |
| reference | Antici2024FData |
| rows x columns | 24,025,345 x 394 |
| task.target | exit state |
| task.problem_type | binary_classification |
| task.metric | roc_auc |
| task.split_regime | temporal_non_iid |
| task.stratify_on | exit state |
| task.time_on | adt |

**Metric**

| field | value |
|---|---|
| name | `roc_auc` (standard; takes proba; higher is better) |
| origin | fallback: the default for the problem type: the source defines no metric the task would use in practice |
| definition | area under the ROC curve |
| reason | The F-DATA paper (https://doi.org/10.1038/s41597-025-05633-1), Technical Validation, reports accuracy for both classification tasks, and the pinned baseline calls classification_report. No operator threshold, cost or deliberate decision-specific accuracy choice is specified. Under MET-5/6/8 use binary ROC AUC; the target is unchanged. |

<details>
<summary>Feature types: 5 categorical, 0 string, 1 datetime</summary>

- categorical (5): `usr`, `jnam`, `jobenv_req`, `freq_req`, `exit state`
- string (0): none
- datetime (1): `adt`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@dataset{Antici2024FData,
  author = {Antici, Francesco and Bartolini, Andrea and Domke, Jens and Kiziltan, Zeynep and Yamamoto, Keiji},
  title = {F-DATA: A Fugaku Workload Dataset for Job-centric Predictive Modelling in HPC Systems},
  year = {2024},
  version = {1.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.11467483},
  url = {https://doi.org/10.5281/zenodo.11467483}
}
```

</details>

## Sample rows

The first 5 of 24,025,345 rows of the final frame (the oldest rows: the frame is sorted by `adt`); 12 of 394 columns, the target first. Cells are cut at 40 characters.

| exit state | usr | jnam | jobenv_req | nnumr | cnumr | freq_req | mszl | mszl_unlimited | embedding_000 | embedding_001 | embedding_002 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| completed | usr_195 | jnam_36208 | jobenv_req_0 | 1 | 48 | 2000 | nan | 1 | 0.0183393 | -0.0319794 | -0.0887759 |
| completed | usr_195 | jnam_36220 | jobenv_req_0 | 1 | 48 | 2000 | nan | 1 | 0.0343249 | -0.0311781 | -0.0919015 |
| completed | usr_195 | jnam_36360 | jobenv_req_0 | 1 | 48 | 2000 | nan | 1 | 0.0355374 | -0.0345894 | -0.084488 |
| completed | usr_195 | jnam_36473 | jobenv_req_0 | 1 | 48 | 2000 | nan | 1 | 0.0222108 | -0.041198 | -0.091809 |
| completed | usr_195 | jnam_36509 | jobenv_req_0 | 1 | 48 | 2000 | nan | 1 | 0.0318812 | -0.0389236 | -0.0873182 |

## Curation notes

We start with all 38 publisher Parquets from F-DATA v1.0 (Zenodo 11467483), checked against the pinned sizes and MD5s.

        - Prediction point: job submission, before queue insertion, scheduling or execution.
        - Target: retain the source completed/failed strings, exactly ec==0 versus nonzero. All 25,866,900 records agree with that rule: 23,308,381 completed and 2,558,519 failed (9.891%). A nonzero return may be intentional; this is exit-state prediction, not hardware-failure diagnosis or failure within a fixed duration.
        - Inputs: source masked usr, jnam and jobenv_req as nominal categories; the requests fixed at submission: nodes (nnumr) and cores (cnumr) as numbers, CPU frequency in MHz (freq_req: 2000, 2200, and 1600 on 2 source rows) as a category, and the memory limit (mszl, bytes) as a number, its "unlimited" code (2^64, on 88.6% of source rows) set to missing with the indicator mszl_unlimited; and the 384 coordinates of the source embedding. The embedding encodes the original versions of those same strings with pretrained all-MiniLM-L6-v2, without outcomes. All source vectors are float32, length 384 and finite. We fit no new encoder and do not reconstruct the private original strings. Author code: https://github.com/francescoantici/F-DATA/tree/db67a65a4b6e91dcebd26147de191fa0051ad790 . The masked ids are numbered in order of first appearance over the release, so a job name's id tracks when the name was first used, which is known at submission. jobenv_req switches from its _0 to its _1 level in April 2024 (99.94% of April rows) and the embedding shifts with it: drift in the newest window, kept.
        - Typing rationale (CLEAN-14 Should departure, serving USE-1/10): usr, jnam and jobenv_req are stable opaque nominal identities. The selected union has 359,636 masked job names; text processing cannot recover the private originals and could attach meaning to arbitrary token suffixes. Keep those source identities categorical despite the high-cardinality string default.
        - Changes from source experiments: combine their separate category/embedding representations, add the known submission time as a datetime input, and add the requested nodes, cores, frequency and memory limit (Andrej, 2026-11-23), which the source paper lists among the information available at submission. The Fujitsu job manual, section 2.5.4 "Changing job parameters" (https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf), lets pjalter change only the elapsed limit (elapse), resource unit (rscunit), resource group (rscgrp) and priority after submission, so the four added requests are as fixed at submission. Requested nodes differ from allocated nodes on 4-35% of rows per month, so the release does not overwrite them with the allocation. Caveat: the requested memory limit and frequency equal their allocated values on every row of all 38 files, so their timing rests on the manual alone; whether a resource-group change resets a group default memory limit is untested.
        - Exclusions: jid is a nonunique released identifier, not a unique execution-record key; its exact parent/subjob semantics are unresolved. Do not deduplicate by it. Exclude all allocated/used resource fields, queue/scheduling/start/deletion/end timestamps, exit code, duration, power/energy, counters and performance-derived outcomes from predictors. End time and exit code are read only for label availability and target checks. The requested elapsed (time) limit and priority stay out: pjalter can change both after submission (manual section 2.5.4), and the release keeps one snapshot of unknown timing; priority is also 127 on 99.995% of rows.
        - Row identity: no two rows agree on all 44 nonembedding source fields, and submission months are disjoint across files. 861,254 rows in 300,062 groups share job ID, user, job name, environment, submission, start and end times, exit code and duration; every group differs in its performance and power counters, so these are separate executions that ran side by side (bulk subjobs), not copies. The public release lacks explicit subjob identifiers; the finer bulk/step/retry structure cannot be recovered. Preserve the released execution records as natural repeats and evaluate future jobs on the same system with recurring identities.
        - Evaluation unit: scores weight released execution records, not parent submissions, so a bulk job counts once per subjob. On the test sides (May-Aug 2023 / Sep-Dec 2023 / Jan-Apr 2024; measured 2026-11-23 with the requested resources), 20.0 / 39.2 / 25.3% of rows share all inputs with another row; the largest such group holds 1,756 / 1,822 / 448 rows, and 193 / 916 / 699 groups hold both labels. The four requests split almost none of these groups (without them: 20.0 / 39.3 / 25.3%). Per-row AUC also weighs cheap failures like costly ones: failed jobs are 12.6% of test rows but 7.0% of node-hours, and the top 1% of failed jobs hold 83.5% of failed node-hours. The source names no cost, so the metric is not weighted.
        - Time: parse the source offset timestamps as instants, convert to Asia/Tokyo and remove the timezone only then, preserving Japanese calendar boundaries. Equal-time ties keep publisher filename and row order; no outcome-based tie order is introduced.
        - Cohort limit: the source cleaner requires several post-run measurements. Excluded early failures, uninstrumented executions and still-pending submissions cannot be counted from the release. April 2024 observations begin April 4 and have completion times through May 14; this does not prove every long-queued April submission is represented. Each fiscal year is cut on end time at 31 March: every March file ends that day, while in other months 2.2-16.5% of last-week submissions end after the month. Late March 2024 holds 28,113 test rows, 42.2% failed, 20.0% of the newest window's positives. Simulating the cut in the 34 months without one leaves the failure rate unchanged (median ratio 1.00, IQR 0.94-1.03), and 5-9 April 2024 fail at 31-78% too, so the late-March rate is a real event, not made by the cut. Jobs killed at their elapsed limit are almost absent (0.005% of rows): a failure is a nonzero exit of a job that ran to its end. Fit is approximate for all submitted jobs, and the benchmark describes the released recorded-execution cohort without claiming a complete submission census.
        - Value follow-up: native task flags no_spread and drift_baseline received bounded train-only tuning, date ablations and foldwise raw-user comparisons. Ranking signal is present; two configurations do not establish tuned-family separation or operational probability quality. Recheck family separation, foldwise simple baselines and probability quality at the first tuned benchmark run (TP-1/3/4; EV-3/7/8).
        - Live outcome history (measured 2026-11-21, before the requested resources were added): an operator sees each user's outcomes as jobs finish. An untrained failure rate over the user's last 100 finished jobs, shrunk to the static rate, scores ROC AUC 0.915 / 0.902 / 0.921 (May-Aug 2023 / Sep-Dec 2023 / Jan-Apr 2024), against 0.797 / 0.829 / 0.878 for LightGBM on the identity and time inputs (3-seed means). All of that gain comes from labels inside the test window: adding each user's last training label and training failure rate to LightGBM scores 0.819 / 0.733 / 0.862, below the model without them. A test row may not use other test rows' labels (the evaluation protocol below), so this history stays out and the fit reason names the gap.
        - Curator decisions (2026-11-03, Myunghwan): accepts this measured future exit-state task and retains it with the first-tuned-benchmark recheck. The gap choice was accepted subject to completion/maturity checks, which passed the recorded-label boundary on the full source and exact shipped train sides; recent outcome selection and reporting-latency sensitivity remain documented. No target or submission-time input rule is changed.
        - Maturity qualification (2026-11-03): the full 25,866,900-row interval audit and all three exact training sides pass recorded completion strictly before refit; 10,387/48,375/28,118 source outcomes are excluded at May/Sep/Jan cutoffs. Completion is a proxy for label arrival, not a verified ingestion timestamp. Near-cutoff class selection is real: before September, late-ending last-day jobs fail at 18.53% versus 0.292% among already completed jobs. A hypothetical 24h reporting delay removes 0.1049–0.1111% of each training side (measured on the 1M training draws of 2026-11-03). Fixed-parameter paired diagnostics change AUC by about -0.010 for that lag and -0.0166/+0.0044/-0.0458 for a seven-day submission embargo, newest first. No gap was chosen from these held-out scores; these are bounded single-family checks, not full-budget resampling or full HPO. Keep reporting-latency and maturity sensitivity in the first-tuned-benchmark recheck. Test labels are eventual exit states; completion after a four-month submission window is legitimate, and all recorded source ends precede release publication.
        - Sampling (Andrej, 2026-11-24): the `_1m` version of the row-budget protocol, as the other sets over the budget. After each cutoff's training-label availability filter, every earlier labelled row stays on the training side; each test window keeps at most 500k rows, a class-proportional random draw on the full-source metadata (native sample_temporal_splits, seed 4267), without balancing classes. A benchmark sub-samples each training side to 1M rows, by default at random from the newest year before the window. This replaces the fixed class-proportional 1M training draw from all history approved on 2026-11-03. Metadata source positions map the selected vectors exactly; _make_splits recomputes membership and removes all lineage columns before models.
        - Split walk (the split decision tree, SPLIT-36, from the record's collection type Dated Event Log): [LOG.meets] the model scores jobs submitted after the data, cases after the data → Order and windows step → [ORDER.order] the submission time is recorded: yes → [ORDER.windows] three four-month test windows, the oldest training on 65.3% of the rows: yes → leaf L-ORDER.windows, Temporal · windows on the time key, the split the definition ships (`split_leaf`). The gap follows the gap rules: one day, training only on jobs submitted at least a day before each window and ended before it.

Each test window keeps up to 500k rows, class-stratified with the default seed 4267; each training side keeps every earlier labelled row. Only the rows the splits use have their embeddings materialized; _make_splits redoes the selection on full-source metadata and verifies membership.

## Splits

Three four-month test windows walk backward from the latest source month; training is the earlier history,
with at least 50% of full-source rows before the oldest window. End time must precede each window's start
as the observed proxy for label availability; any later reporting delay is unreleased. Each test window keeps at
most 500k rows, a class-proportional random draw (native sample_temporal_splits, default seed 4267) that does
not balance the classes; each train side keeps every earlier labelled row, and a benchmark sub-samples it to 1M
rows.
Each test row is predicted from the training rows and its own features only; no feature or model step may
use other test rows, so no user history is built across the test window (LEAK-9).
Source identities recur: this tests future jobs on the same system, not unseen users. Equal submission
times retain publisher filename and row order. Source positions and label-availability times are lineage
metadata, removed before models. Windows are May–August 2023, September–December 2023 and January–April 2024, newest first. These cover the paper's eleven-month holdout plus May 2023; unlike its fixed training period, each window refits on earlier observed labels. Four months is the disclosed benchmark refit judgment, not a source-established production cadence.
Horizon (checked, Andrej, 2026-11-23): length four months and step four months (the windows adjoin), both the
benchmark's refit judgment, since the source states no refit cadence (its paper tests one fixed holdout and
notes that models updated frequently with recent data are more accurate); gap one day (Andrej, 2026-11-24): a
job trains when it was submitted at least one day before the window and its end was recorded before it; time unit the calendar month of the submission time in
Japan time, the unit of the source's monthly files. Leaf: L-ORDER.windows (Temporal · windows on the time key,
here the submission time; the gap by the gap rules: one day, with the label filter).
Windows: 3, against the target of 3 that SPLIT-15 takes from SPLIT-33. Training history: all earlier labelled
history, as the source's authors also trained on all earlier months.
Gap (SPLIT-10, Andrej, 2026-11-24, replacing the exception of 2026-11-03): one day between the newest training submission and the window, the lag between building a model and applying it; 90% of the label delays (end minus submission) are within 33 hours. At the May and January cutoffs the newest training day then keeps 99% of its jobs at the overall failure rate; at the September cutoff long failing jobs of late August 2023 stay under-represented at every gap up to seven days (kept 2.2% failed against 6.6%), a limitation, not a cut. Unavailable labels still leave under SPLIT-9.

3 repeat(s) x 1 fold(s) with seed 4267; train 16,880,049 to 23,517,106 rows, test 500,000 rows. Prediction horizon: 4 months. Gap between train and test: 1 days. Row budget: at most 500k test rows per split; a benchmark trains on at most 1M. The train sides keep every row available to them; `subsample_train` draws the 1M rows a benchmark fits on from the newest year before each window, extended back in time until it holds that many rows, at random, as rows.

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 23517106 | 500000 | 2021-03-01 00:00:00 | 2023-12-30 23:59:24 | 2024-01-01 00:00:15 | 2024-04-30 23:59:16 |
| 1 | 0 | 20767864 | 500000 | 2021-03-01 00:00:00 | 2023-08-30 23:59:54 | 2023-09-01 00:03:42 | 2023-12-31 23:59:54 |
| 2 | 0 | 16880049 | 500000 | 2021-03-01 00:00:00 | 2023-04-29 23:59:50 | 2023-05-01 00:00:11 | 2023-08-31 23:57:36 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows fugaku_hpc_job_failure_1m`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | Jan 2024 - Apr 2024 | 500000 | 0.979 | failed 11.3% (about 56,325) | failed 9.6% (about 2,252,939) | 2.519 | usr (2.52), jnam (1.47), jobenv_req (1.16) | 0.4793 |
| 1 | Sep 2023 - Dec 2023 | 500000 | 0.864 | failed 14.9% (about 74,625) | failed 9.3% (about 1,941,795) | 2.704 | usr (2.70), jnam (1.57), embedding_085 (0.47) | 0.4783 |
| 2 | May 2023 - Aug 2023 | 500000 | 0.703 | failed 11.5% (about 57,250) | failed 8.7% (about 1,471,940) | 3.076 | usr (3.08), jnam (1.64), embedding_009 (0.70) | 0.4973 |

## Decisions

### 1. Full-source terminal-label availability and the test-window cap

Training labels end strictly before each refit. Source positions and availability dates are never model inputs.

| repeat | cutoff | train_before_maturity | train_after_maturity | excluded_late_labels | test_before_cap | test_failed_before_cap | train | test | train_failed | test_failed |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2024-01-01 00:00:00 | 23562890 | 23517106 | 45784 | 2304010 | 273041 | 23517106 | 500000 | 2283422 | 59253 |
| 1 | 2023-09-01 00:00:00 | 20825832 | 20767864 | 57968 | 2737058 | 408425 | 20767864 | 500000 | 1869321 | 74610 |
| 2 | 2023-05-01 00:00:00 | 16907178 | 16880049 | 27129 | 3918654 | 447783 | 16880049 | 500000 | 1426978 | 57135 |

## Bundle checks

0 error(s), 0 warning(s), 2 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicates_skipped`: Skipped duplicate-column/row checks: 9,465,985,930 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to force them, or rely on `dataset_checks.run_all_checks`.)
- **info** `dataset_pure_feature_value_skipped`: Skipped the pure-feature-value check: 9,465,985,930 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to force it.)

Accepted on purpose:

- `time_newest_period_short`: Accepted (Andrej, 2026-11-24, with the _1m version of review issue 5): the frame keeps every training row but only a 500,000-row sample of each test window, so its newest 30 days hold 3,055 rows a day against a median of 22,831 (13%). In the full source they hold 59% of the median (14,015 against 23,854 a day), because the April 2024 observations begin on 4 April (the cohort-limit note).

## Data checks

### Feature summary

<details>
<summary>Show the table (394 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| usr | category | 0 | 0 | 3417 | usr_1898, usr_1122, usr_1365, usr_1912, usr_2111, usr_1586, usr_1214, usr_341, … |
| jnam | category | 0 | 0 | 2.05944e+06 | jnam_47, jnam_796198, jnam_296120, jnam_108, jnam_985, jnam_1570714, jnam_38245… |
| jobenv_req | category | 0 | 0 | 5 | jobenv_req_0, jobenv_req_1, jobenv_req_8, jobenv_req_2, jobenv_req_6 |
| freq_req | category | 0 | 0 | 3 | 2000, 2200, 1600 |
| exit state | category | 0 | 0 | 2 | completed, failed |
| adt | datetime64\[ns\] | 0 | 0 | 1.08999e+07 | 2021-07-01 11:39:20, 2021-07-01 17:43:40, 2021-11-15 18:51:08, 2021-07-01 16:45… |
| embedding_000 | float32 | 0 | 0 | 2.09283e+06 | 0.0258, -0.0508, 0.0258, 0.0072, 0.0055, -0.041, -0.0224, -0.0735, -0.0391, -0.… |
| embedding_001 | float32 | 0 | 0 | 2.09703e+06 | -0.0542, -0.0843, -0.0933, -0.036, -0.0436, -0.0884, -0.0129, -0.0237, -0.0199,… |
| embedding_002 | float32 | 0 | 0 | 2.04464e+06 | -0.0112, -0.117, -0.0842, -0.1201, -0.1013, -0.1201, -0.0462, -0.023, -0.0286, … |
| embedding_003 | float32 | 0 | 0 | 2.04643e+06 | -0.0914, 0.0193, -0.0557, -0.1302, -0.0284, 0.027, -0.0768, -0.0347, -0.0069, -… |
| embedding_004 | float32 | 0 | 0 | 2.02819e+06 | 0.113, 0.0436, 0.0491, 0.0015, 0.0451, 0.0438, 0.0798, 0.0763, 0.0237, 0.0584 |
| embedding_005 | float32 | 0 | 0 | 2.03711e+06 | -0.0586, -0.0175, -0.0712, -0.0042, -0.116, -0.0161, -0.0709, -0.0402, -0.0624,… |
| embedding_006 | float32 | 0 | 0 | 2.10392e+06 | -0.0532, -0.0343, -0.0095, -0.0784, -0.0266, -0.032, -0.0573, 0.005, -0.0581, -… |
| embedding_007 | float32 | 0 | 0 | 2.07677e+06 | 0.0776, 0.0524, 0.0534, 0.0327, 0.0565, 0.05, 0.0493, 0.088, 0.0643, 0.1477 |
| embedding_008 | float32 | 0 | 0 | 2.07221e+06 | -0.0734, 0.0011, -0.08, -0.0194, -0.0922, -0.0114, -0.0084, 0.0175, 0.0265, -0.… |
| embedding_009 | float32 | 0 | 0 | 2.06677e+06 | -0.0615, 0.0394, -0.0743, -0.0593, -0.08, 0.0445, -0.0174, 0.0446, 0.0078, 0.00… |
| embedding_010 | float32 | 0 | 0 | 2.02326e+06 | 0.0569, 0.0228, 0.0463, -0.0354, 0.0859, 0.0232, 0.0338, 0.0629, 0.0174, 0.0543 |
| embedding_011 | float32 | 0 | 0 | 2.08453e+06 | -0.0709, -0.0147, -0.0235, -0.002, -0.0445, -0.0252, -0.0347, -0.0496, -0.0145,… |
| embedding_012 | float32 | 0 | 0 | 2.0254e+06 | -0.0624, -0.0715, -0.0436, -0.1075, -0.0587, -0.0728, -0.0853, -0.0642, -0.0511… |
| embedding_013 | float32 | 0 | 0 | 2.11336e+06 | 0.0082, -0.0188, -0.0406, -0.0326, -0.0294, -0.0056, -0.0373, -0.0212, -0.0279,… |
| embedding_014 | float32 | 0 | 0 | 2.0652e+06 | -0.0427, -0.0191, 0.0322, -0.0802, -0.0438, -0.0187, -0.0032, -0.0218, -0.0275,… |
| embedding_015 | float32 | 0 | 0 | 2.11857e+06 | 0.0178, 0.0553, -0.0088, -0.0307, -0.0312, 0.0562, -0.0066, 0.0101, 0.0149, -0.… |
| embedding_016 | float32 | 0 | 0 | 2.11146e+06 | 0.0558, -0.0878, 0.0381, 0.0699, 0.0292, -0.0697, 0.0061, -0.0141, -0.0017, -0.… |
| embedding_017 | float32 | 0 | 0 | 2.03584e+06 | -0.0356, -0.0997, -0.0805, -0.0185, -0.0834, -0.102, -0.0501, -0.0625, -0.0595,… |
| embedding_018 | float32 | 0 | 0 | 2.0492e+06 | 0.0274, 0.0787, -0.0154, 0.0194, 0.0501, 0.0905, 0.0668, 0.0862, 0.0886, 0.0054 |
| embedding_019 | float32 | 0 | 0 | 2.11984e+06 | 0.0589, -0.0274, -0.0177, -0.0064, 0.0371, -0.0392, 0.075, -0.009, 0.0178, -0.0… |
| embedding_020 | float32 | 0 | 0 | 2.11918e+06 | -0.0049, -0.0986, -0.0578, -0.0452, 0.034, -0.099, -0.0105, 0.0088, -0.034, -0.… |
| embedding_021 | float32 | 0 | 0 | 2.1102e+06 | 0.021, 0.0249, -0.0265, -0.1125, 0.0045, 0.0107, 0.0427, 0.0588, 0.026, 0.0111 |
| embedding_022 | float32 | 0 | 0 | 2.09475e+06 | 0.0234, 0.0339, -0.0708, 0.0295, -0.0345, 0.044, -0.0203, 0.0051, -0.0054, 0.02… |
| embedding_023 | float32 | 0 | 0 | 2.08354e+06 | 0.023, -0.042, -0.0613, -0.0854, -0.0268, -0.0343, -0.0521, -0.0503, -0.041, -0… |
| embedding_024 | float32 | 0 | 0 | 2.07928e+06 | 0.0141, -0.0289, 0.0079, 0.0121, 0.028, -0.0352, 0.0263, 0.0344, 0.0079, 0.0097 |
| embedding_025 | float32 | 0 | 0 | 2.05298e+06 | -0.0318, -0.0716, -0.0523, -0.0153, -0.0631, -0.0212, -0.0649, -0.0878, -0.055,… |
| embedding_026 | float32 | 0 | 0 | 2.10483e+06 | -0.025, -0.0155, 0.0069, 0.0285, 0.0353, -0.0172, 0.0238, 0.0088, 0.0179, 0.0329 |
| embedding_027 | float32 | 0 | 0 | 2.04682e+06 | 0.0274, 0.0946, 0.0701, 0.0765, 0.0624, 0.1006, -0.0064, 0.0217, 0.0163, 0.0388 |
| embedding_028 | float32 | 0 | 0 | 2.11937e+06 | 0.0351, -0.0318, 0.0266, -0.0144, 0.0337, -0.0374, -0.0553, -0.0698, -0.095, -0… |
| embedding_029 | float32 | 0 | 0 | 2.01324e+06 | -0.0652, -0.0755, -0.0893, -0.1032, -0.0883, -0.0851, -0.0944, -0.1066, -0.0951… |
| embedding_030 | float32 | 0 | 0 | 2.00737e+06 | 0.0967, 0.0884, 0.0407, 0.0618, 0.1152, 0.0663, 0.1044, 0.106, 0.0733, 0.1247 |
| embedding_031 | float32 | 0 | 0 | 2.11405e+06 | 0.041, 0.0229, 0.0023, -0.0308, -0.0101, 0.0104, -0.0281, -0.0143, -0.0132, -0.… |
| embedding_032 | float32 | 0 | 0 | 2.10867e+06 | 0.0466, 0.0145, -0.0134, -0.0212, -0.0194, 0.0181, -0.015, 0.0073, -0.03, 0.0041 |
| embedding_033 | float32 | 0 | 0 | 2.11773e+06 | -0.0082, 0.0067, 0.0011, 0.0026, -0.011, 0.0014, -0.0328, -0.0604, -0.0182, -0.… |
| embedding_034 | float32 | 0 | 0 | 2.04814e+06 | -0.0363, 0.1575, 0.0112, -0.02, 0.0695, 0.1443, 0.0653, 0.0562, 0.0661, 0.1192 |
| embedding_035 | float32 | 0 | 0 | 2.05079e+06 | 0.0772, 0.1025, -0.0021, 0.0499, 0.0617, 0.0935, 0.1315, 0.1486, 0.1233, 0.1646 |
| embedding_036 | float32 | 0 | 0 | 2.08334e+06 | 0.0121, 0.0933, 0.0286, 0.0199, 0.0821, 0.0892, 0.1156, 0.1377, 0.0938, 0.0755 |
| embedding_037 | float32 | 0 | 0 | 2.00613e+06 | -0.1259, -0.0797, -0.1025, -0.1193, -0.1376, -0.0907, -0.1237, -0.081, -0.1032,… |
| embedding_038 | float32 | 0 | 0 | 2.05102e+06 | -0.0703, -0.0858, -0.1151, -0.102, -0.1012, -0.0872, -0.1351, -0.1105, -0.0995,… |
| embedding_039 | float32 | 0 | 0 | 2.06791e+06 | 0.0161, -0.013, -0.0486, -0.0227, -0.0323, -0.0099, 0.0039, 0.0305, 0.0022, -0.… |
| embedding_040 | float32 | 0 | 0 | 2.11086e+06 | -0.0291, 0.0361, -0.0175, -0.0394, -0.0115, 0.0303, 0.032, 0.0374, 0.0492, -0.0… |
| embedding_041 | float32 | 0 | 0 | 2.12294e+06 | -0.0103, 0.0184, -0.0202, 0.008, -0.0568, 0.013, 0.0271, 0.0459, 0.0062, 0.0397 |
| embedding_042 | float32 | 0 | 0 | 2.08594e+06 | -0.0088, -0.0318, 0.0468, -0.0002, 0.0446, -0.0289, 0.0309, 0.0089, 0.0172, -0.… |
| embedding_043 | float32 | 0 | 0 | 2.08709e+06 | 0.0446, 0.0688, 0.0619, 0.1549, 0.0813, 0.0632, -0.001, -0.0304, 0.0077, -0.0244 |
| embedding_044 | float32 | 0 | 0 | 2.11987e+06 | -0.0395, -0.0364, 0.0265, 0.0606, 0.0531, -0.0443, 0.0051, -0.017, -0.0131, -0.… |
| embedding_045 | float32 | 0 | 0 | 2.03369e+06 | 0.0504, 0.0998, 0.0536, 0.0614, 0.0655, 0.0961, 0.0759, 0.0311, 0.0632, 0.0153 |
| embedding_046 | float32 | 0 | 0 | 2.12137e+06 | 0.0435, -0.0518, 0.001, -0.0515, 0.0122, -0.0469, -0.0181, -0.0349, -0.0327, 0.… |
| embedding_047 | float32 | 0 | 0 | 2.07116e+06 | -0.0109, 0.0378, 0.0399, 0.0183, 0.0946, 0.0237, 0.0294, -0.0137, -0.0382, -0.0… |
| embedding_048 | float32 | 0 | 0 | 2.08404e+06 | 0.0241, -0.0244, 0.0346, 0.042, 0.021, -0.0225, 0.051, 0.0297, -0.0001, 0.0387 |
| embedding_049 | float32 | 0 | 0 | 2.10975e+06 | 0.0168, 0.0288, -0.0064, 0.02, 0.0231, 0.0253, 0.0402, 0.0561, 0.0292, -0.0727 |
| embedding_050 | float32 | 0 | 0 | 2.12054e+06 | -0.0267, -0.0159, -0.0408, -0.0584, 0.0075, -0.0238, 0.0253, -0.0084, -0.0075, … |
| embedding_051 | float32 | 0 | 0 | 2.05493e+06 | 0.0957, 0.0652, 0.078, 0.0121, 0.0974, 0.0614, 0.0821, 0.0484, 0.041, 0.0854 |
| embedding_052 | float32 | 0 | 0 | 2.08345e+06 | 0.0553, -0.0215, 0.0339, 0.0594, 0.0567, -0.0224, 0.0727, 0.0676, 0.0483, 0.0153 |
| embedding_053 | float32 | 0 | 0 | 2.12008e+06 | -0.0911, -0.0608, 0.0371, -0.0232, -0.0114, -0.0617, -0.0607, -0.0015, -0.1158,… |

(334 more rows not shown)

</details>

### Target distribution

| exit state | count | pct |
|---|---|---|
| completed | 21682318 | 90.25 |
| failed | 2343027 | 9.75 |

### Numeric features

<details>
<summary>Show the table (388 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| nnumr | 2.40253e+06 | 39.4843 | 708.843 | 1 | 158976 |
| cnumr | 2.40253e+06 | 1895.25 | 34024.4 | 48 | 7.63085e+06 |
| mszl | 249117 | 2.38277e+10 | 1.01898e+10 | 6.29146e+08 | 3.06016e+10 |
| mszl_unlimited | 2.40253e+06 | 0.896311 | 0.304857 | 0 | 1 |
| embedding_000 | 2.40253e+06 | -0.028326 | 0.0376377 | -0.180876 | 0.11201 |
| embedding_001 | 2.40253e+06 | -0.0370075 | 0.0353586 | -0.170656 | 0.113702 |
| embedding_002 | 2.40253e+06 | -0.0688388 | 0.0353262 | -0.208607 | 0.0993139 |
| embedding_003 | 2.40253e+06 | -0.0521164 | 0.0370679 | -0.183782 | 0.103022 |
| embedding_004 | 2.40253e+06 | 0.0631557 | 0.0345966 | -0.14886 | 0.197575 |
| embedding_005 | 2.40253e+06 | -0.0548582 | 0.0322861 | -0.185101 | 0.0847356 |
| embedding_006 | 2.40253e+06 | -0.0315894 | 0.0306023 | -0.153767 | 0.106279 |
| embedding_007 | 2.40253e+06 | 0.047866 | 0.0336079 | -0.102457 | 0.20717 |
| embedding_008 | 2.40253e+06 | -0.0440753 | 0.0369533 | -0.182498 | 0.0998717 |
| embedding_009 | 2.40253e+06 | -0.0409777 | 0.0419344 | -0.191844 | 0.110905 |
| embedding_010 | 2.40253e+06 | 0.0553216 | 0.0344216 | -0.072472 | 0.212721 |
| embedding_011 | 2.40253e+06 | -0.0355667 | 0.0331913 | -0.177128 | 0.118812 |
| embedding_012 | 2.40253e+06 | -0.0686575 | 0.0327 | -0.211565 | 0.0826581 |
| embedding_013 | 2.40253e+06 | -0.0211445 | 0.0265202 | -0.153642 | 0.115138 |
| embedding_014 | 2.40253e+06 | -0.0253758 | 0.031315 | -0.169447 | 0.0952337 |
| embedding_015 | 2.40253e+06 | -0.00226391 | 0.0350129 | -0.160394 | 0.176537 |
| embedding_016 | 2.40253e+06 | -0.00701781 | 0.0421361 | -0.174232 | 0.146805 |
| embedding_017 | 2.40253e+06 | -0.0642499 | 0.0313509 | -0.192067 | 0.0868925 |
| embedding_018 | 2.40253e+06 | 0.05085 | 0.035573 | -0.105959 | 0.20577 |
| embedding_019 | 2.40253e+06 | -0.0096054 | 0.0384222 | -0.157842 | 0.175351 |
| embedding_020 | 2.40253e+06 | -0.00651032 | 0.038441 | -0.178486 | 0.143252 |
| embedding_021 | 2.40253e+06 | 0.0156507 | 0.0387176 | -0.134086 | 0.157573 |
| embedding_022 | 2.40253e+06 | -0.0109034 | 0.0379453 | -0.139315 | 0.155046 |
| embedding_023 | 2.40253e+06 | -0.0347043 | 0.0289907 | -0.158285 | 0.108543 |
| embedding_024 | 2.40253e+06 | 0.0206238 | 0.0281559 | -0.102507 | 0.152581 |
| embedding_025 | 2.40253e+06 | -0.052138 | 0.0313699 | -0.174278 | 0.109607 |
| embedding_026 | 2.40253e+06 | 0.0144594 | 0.038684 | -0.136536 | 0.178871 |
| embedding_027 | 2.40253e+06 | 0.0523365 | 0.0370482 | -0.0888224 | 0.200541 |
| embedding_028 | 2.40253e+06 | -0.00325488 | 0.0421723 | -0.172834 | 0.150074 |
| embedding_029 | 2.40253e+06 | -0.0891397 | 0.0312789 | -0.229273 | 0.0850638 |
| embedding_030 | 2.40253e+06 | 0.0750207 | 0.0313404 | -0.0933073 | 0.217167 |
| embedding_031 | 2.40253e+06 | 0.00870022 | 0.0322949 | -0.127574 | 0.169204 |
| embedding_032 | 2.40253e+06 | -0.0153722 | 0.0346283 | -0.184006 | 0.137836 |
| embedding_033 | 2.40253e+06 | -0.0228588 | 0.0305303 | -0.16352 | 0.126067 |
| embedding_034 | 2.40253e+06 | 0.0535242 | 0.0472684 | -0.0876282 | 0.21492 |
| embedding_035 | 2.40253e+06 | 0.0716599 | 0.0450432 | -0.0892579 | 0.242067 |
| embedding_036 | 2.40253e+06 | 0.0547247 | 0.0404058 | -0.137421 | 0.190332 |
| embedding_037 | 2.40253e+06 | -0.0931106 | 0.0344702 | -0.249015 | 0.0709566 |
| embedding_038 | 2.40253e+06 | -0.0784558 | 0.0337427 | -0.214031 | 0.108565 |
| embedding_039 | 2.40253e+06 | -0.0258916 | 0.0335118 | -0.168124 | 0.110138 |
| embedding_040 | 2.40253e+06 | 0.00669178 | 0.0385002 | -0.132588 | 0.180046 |
| embedding_041 | 2.40253e+06 | -0.00941669 | 0.0295162 | -0.131995 | 0.131386 |
| embedding_042 | 2.40253e+06 | 0.0188006 | 0.0334954 | -0.119248 | 0.200029 |
| embedding_043 | 2.40253e+06 | 0.0438554 | 0.0414213 | -0.12001 | 0.200236 |
| embedding_044 | 2.40253e+06 | 0.0100983 | 0.0351556 | -0.125231 | 0.164251 |
| embedding_045 | 2.40253e+06 | 0.0598562 | 0.0301164 | -0.0992578 | 0.184798 |
| embedding_046 | 2.40253e+06 | -0.00546854 | 0.0362653 | -0.172069 | 0.135079 |
| embedding_047 | 2.40253e+06 | 0.0278367 | 0.0326271 | -0.115413 | 0.160293 |
| embedding_048 | 2.40253e+06 | 0.0243516 | 0.0281095 | -0.101076 | 0.156967 |
| embedding_049 | 2.40253e+06 | 0.0136234 | 0.0313091 | -0.169778 | 0.147709 |
| embedding_050 | 2.40253e+06 | -0.00985604 | 0.0315385 | -0.164542 | 0.121743 |
| embedding_051 | 2.40253e+06 | 0.060642 | 0.0351273 | -0.111925 | 0.236099 |
| embedding_052 | 2.40253e+06 | 0.0417938 | 0.0310897 | -0.114739 | 0.156289 |
| embedding_053 | 2.40253e+06 | -0.0255269 | 0.0403509 | -0.185422 | 0.125154 |
| embedding_054 | 2.40253e+06 | 0.05197 | 0.0351192 | -0.133268 | 0.182516 |
| embedding_055 | 2.40253e+06 | -0.0315341 | 0.0312349 | -0.194375 | 0.101905 |

(328 more rows not shown)

</details>

### Categorical features

<details>
<summary>Show the table (25 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| adt | 1 | 2021-07-01 11:39:20 | 1456 | 0.06 |
| adt | 2 | 2021-07-01 17:43:40 | 1407 | 0.06 |
| adt | 3 | 2021-11-15 18:51:08 | 1399 | 0.06 |
| adt | 4 | 2021-07-01 16:45:30 | 1367 | 0.06 |
| adt | 5 | 2023-08-19 21:29:00 | 1333 | 0.06 |
| exit state | 1 | completed | 2168413 | 90.26 |
| exit state | 2 | failed | 234121 | 9.74 |
| freq_req | 1 | 2000 | 2014786 | 83.86 |
| freq_req | 2 | 2200 | 387747 | 16.14 |
| freq_req | 3 | 1600 | 1 | 0 |
| jnam | 1 | jnam_47 | 125020 | 5.2 |
| jnam | 2 | jnam_796198 | 113257 | 4.71 |
| jnam | 3 | jnam_296120 | 106268 | 4.42 |
| jnam | 4 | jnam_108 | 76298 | 3.18 |
| jnam | 5 | jnam_985 | 45730 | 1.9 |
| jobenv_req | 1 | jobenv_req_0 | 2392892 | 99.6 |
| jobenv_req | 2 | jobenv_req_1 | 9633 | 0.4 |
| jobenv_req | 3 | jobenv_req_8 | 9 | 0 |
| jobenv_req | 4 | jobenv_req_2 | 0 | 0 |
| jobenv_req | 5 | jobenv_req_6 | 0 | 0 |
| usr | 1 | usr_1898 | 124502 | 5.18 |
| usr | 2 | usr_1122 | 79513 | 3.31 |
| usr | 3 | usr_1365 | 77166 | 3.21 |
| usr | 4 | usr_1912 | 75768 | 3.15 |
| usr | 5 | usr_2111 | 67714 | 2.82 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a1e3af-55a4-7df0-bd28-5009e8991055 |
| checksum | v2:4cfcfaad3da1a6271ad90e17ac9589a303bd8573baf5fe23acdd52e508f09f8d |
| built_at | 2026-11-16T09:29:09+00:00 |
| path | fugaku_hpc_job_failure/01a1e3af-55a4-7df0-bd28-5009e8991055 |
| data_foundry_version | 0.0.5 |
| git_sha | a6a4ac56259a656b235696d1e74d0a8c36f68f68 |
| libraries | {'python': '3.12.3', 'pandas': '3.1.0', 'numpy': '2.5.4', 'pyarrow': '26.0.0', 'scikit-learn': '1.7.2', 'polars': '2.0.0'} |
| stale | yes: the definition now gives checksum `v2:32c8b66e36ba62d860a64ab054e5ae8a7fdc45d9c7fd3299fbdbdd2fa49ef1e0` |
