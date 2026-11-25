"""F-DATA source exit-state prediction with qualified temporal execution-record splits."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from data_foundry.collections import TABARENA_V0PT2_ROW_BUDGET
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    Source,
    SplitPlan,
    TaskSummary,
    Temporal,
    TemporalSplits,
)
from data_foundry.v2.splits import sample_temporal_splits

# The requests fixed at submission (Fujitsu job manual section 2.5.4: pjalter changes only elapse, rscunit, rscgrp and
# priority), read beside the source's representations.
SOURCE_INPUTS = ("usr", "jnam", "jobenv_req", "nnumr", "cnumr", "freq_req", "mszl")
MSZL_UNLIMITED = 2.0**64
# The collection's budget: this definition builds its own splits, so it caps its test windows itself.
TEST_CAP = TABARENA_V0PT2_ROW_BUDGET.test
# The gap before each window: the lag between building a model and applying it (Andrej, 2026-11-24, review issue 7).
GAP = pd.Timedelta(days=1)

RAW_FILES = {
    "21_03.parquet": (458006207, "012dd8d987585d898e5083416e563988"),
    "21_04.parquet": (150514262, "3178b7481f639511a74b2be85f5079ba"),
    "21_05.parquet": (433282863, "41287430b7e8f7fa6e3e19275b897d1d"),
    "21_06.parquet": (505804135, "d057f2cea79f6442c7a628ffb81bb647"),
    "21_07.parquet": (282781173, "3bebee043638772a88dc915746069d2c"),
    "21_08.parquet": (336376424, "3e1a8b3cf0fdd20bac8cf68a296ccb83"),
    "21_09.parquet": (331322227, "47d05827003c3d25a24353dc1561e90f"),
    "21_10.parquet": (838721618, "4e9d8ae90fe577ab17158419431e6a92"),
    "21_11.parquet": (699421163, "0b89e404f21d719febd23b04c2ad881b"),
    "21_12.parquet": (931034360, "fca13b423e5c38139f92deab4f69c8e7"),
    "22_01.parquet": (1279299122, "dd8de06f73d2c0e3fd8919342b4018ae"),
    "22_02.parquet": (817800643, "0cc8dc1b070ae5decde22eea5a9a7bcd"),
    "22_03.parquet": (746028507, "9b65c2a6f7ebe98498da585d83ce517c"),
    "22_04.parquet": (629137061, "d56caa57f21d4d3b2602bf321f362419"),
    "22_05.parquet": (536735369, "9ca6e67fdee336a856f62e3587736e1a"),
    "22_06.parquet": (586684684, "648f177badf349946e4a173b6ce97c21"),
    "22_07.parquet": (575850359, "7ca28a1e147b375407c4a10ae6bdb38f"),
    "22_08.parquet": (634045511, "6b264abaafd9018553a4db2b808e684f"),
    "22_09.parquet": (841282121, "6098b25b014424314fdd7c67986e3c47"),
    "22_10.parquet": (663519043, "510c146e33c81760b48d39d1e71d02f6"),
    "22_11.parquet": (795290958, "9d5b8c3d8e24d8dc1bb2f20122fdeb68"),
    "22_12.parquet": (855700108, "2f2be33534bdbdca59cbd1cee3094097"),
    "23_01.parquet": (981864234, "681603aba504a37da6c19d0cc173980a"),
    "23_02.parquet": (762060527, "4bd51ee8439d918fc64c5747dc093cdb"),
    "23_03.parquet": (728247174, "17be3481816aa263d7867fa97ffd9828"),
    "23_04.parquet": (575431429, "261dce6e2bdba46820186229d727b600"),
    "23_05.parquet": (635235337, "194e3078ed873869a992c788ad94ce78"),
    "23_06.parquet": (1330520896, "612ce0739c46481fb4d005f533b4e3a5"),
    "23_07.parquet": (968169044, "9cd9e0aa7ebc418e0e5c8c2d977fe969"),
    "23_08.parquet": (1177409305, "974e643024e0811c24354bafee5c988e"),
    "23_09.parquet": (455688150, "edf1560ec5b7cf81dd18662edf89d33e"),
    "23_10.parquet": (885571255, "eb1d96b17237f15f29371ddf40ad9e38"),
    "23_11.parquet": (944751297, "6e4e59472c186a73626d551620c206db"),
    "23_12.parquet": (909941543, "2eb439357d2f23e5dafa9299005470d7"),
    "24_01.parquet": (1050727328, "337879f82a77a75c781a8b19a9bdbeee"),
    "24_02.parquet": (800005340, "ee9fa11d2341a8d92ce9ebdfa2b54220"),
    "24_03.parquet": (529395339, "e722928391ffa01c691b24499d0cb99a"),
    "24_04.parquet": (568138934, "ce7bd7f0d06daf9d7a93844850f4d172"),
}


class FugakuHpcJobFailure1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a submitted Fugaku job terminate with a nonzero exit code?",
        use_case=(
            "For example, a supercomputer operator scores a job when it is submitted, to identify jobs that may need "
            "attention before consuming resources. The source motivates failure-aware workload management."
        ),
        row=(
            "One released job-execution record. The source contains 25,866,900 records from March 2021 to April 2024; this version keeps every training row each window can use and up to 500,000 test rows per window."
        ),
        predicted=(
            "The source's terminal exit state: completed for exit code zero, failed for nonzero. This is not a "
            "hardware-failure diagnosis; an intentional nonzero return may occur without failed computation."
        ),
        known=(
            "The masked submitting user, job name and requested job environment, and the released 384-value "
            "pretrained embedding of those original strings; the requested nodes, cores, CPU frequency and memory "
            "limit; and the submission time. All are known at submission; the user cannot change these requests later."
        ),
        split=(
            "Three successive four-month future windows on the same supercomputer, with earlier completed labels "
            "for training: May–August 2023, September–December 2023, and January–April 2024."
        ),
        changes=(
            "Keep the original labels and representations. Combine categories and embedding, and add the submission "
            "time and the requested nodes, cores, frequency and memory limit; the authors evaluated the "
            "representations separately and without these. Refit for three four-month windows covering May "
            "2023–April 2024 instead of their fixed June 2023–April 2024 holdout. Exclude unavailable training labels; "
            "cap each test window at 500,000 rows, while each training side keeps every earlier labelled row."
        ),
        fit="approximate",
        fit_reason=(
            "The release keeps only jobs with post-run measurements, so coverage of all submissions is unknown, and "
            "each fiscal year is cut at 31 March on end time. Nonzero exit proxies actionable failure, and records do "
            "not map reliably to parent jobs. The operator sees each user's outcomes as jobs finish; that live "
            "history, outside this task, beat models on the identity and time inputs by 0.04-0.12 AUC."
        ),
    )

    unique_name = "fugaku_hpc_job_failure_1m"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.5281/zenodo.11467483",
            license="CC BY 4.0",
            year="2024",
            bibtex=r"""
        @dataset{Antici2024FData,
          author = {Antici, Francesco and Bartolini, Andrea and Domke, Jens and Kiziltan, Zeynep and Yamamoto, Keiji},
          title = {F-DATA: A Fugaku Workload Dataset for Job-centric Predictive Modelling in HPC Systems},
          year = {2024},
          version = {1.0},
          publisher = {Zenodo},
          doi = {10.5281/zenodo.11467483},
          url = {https://doi.org/10.5281/zenodo.11467483}
        }
    """,
        ),
    )
    domain = "technology & internet"
    data_tags = ("Anonymized",)
    download_description = """
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
    """
    curation_comments = (
        """
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
        - Maturity qualification (2026-11-03): the full 25,866,900-row interval audit and all three exact training sides pass recorded completion strictly before refit; 10,387/48,375/28,118 source outcomes are excluded at May/Sep/Jan cutoffs. Completion is a proxy for label arrival, not a verified ingestion timestamp. Near-cutoff class selection is real: before September, late-ending last-day jobs fail at 18.53% versus 0.292% among already completed jobs. A hypothetical 24h reporting delay removes 0.1049–0.1111% of each training side (measured on the 1M training draws of 2026-11-03). Fixed-parameter paired diagnostics change AUC by about -0.010 for that lag and -0.0166/+0.0044/-0.0458 for a seven-day submission embargo, newest first. The one-day gap (Andrej, 2026-11-24) follows the label's delay and was not chosen from these held-out scores; these are bounded single-family checks, not full-budget resampling or full HPO. Keep reporting-latency and maturity sensitivity in the first-tuned-benchmark recheck. Test labels are eventual exit states; completion after a four-month submission window is legitimate, and all recorded source ends precede release publication.
        - Sampling (Andrej, 2026-11-24): the `_1m` version of the row-budget protocol, as the other sets over the budget. After each cutoff's training-label availability filter, every earlier labelled row stays on the training side; each test window keeps at most 500k rows, a class-proportional random draw on the full-source metadata (native sample_temporal_splits, seed 4267), without balancing classes. A benchmark sub-samples each training side to 1M rows, by default at random from the newest year before the window. This replaces the fixed class-proportional 1M training draw from all history approved on 2026-11-03. Metadata source positions map the selected vectors exactly; _make_splits recomputes membership and removes all lineage columns before models.
        - Split walk (the split decision tree, SPLIT-36, from the record's collection type Dated Event Log): [LOG.meets] the model scores jobs submitted after the data, cases after the data → Order and windows step → [ORDER.order] the submission time is recorded: yes → [ORDER.windows] three four-month test windows, the oldest training on 65.3% of the rows: yes → leaf L-ORDER.windows, Temporal · windows on the time key, the split the definition ships (`split_leaf`). The gap follows the gap rules: one day, training only on jobs submitted at least a day before each window and ended before it.
    """
        + "\n"
        + "Each test window keeps up to 500k rows, class-stratified with the default seed 4267; each training side "
        "keeps every earlier labelled row. Only the rows the splits use have their embeddings materialized; "
        "_make_splits redoes the selection on full-source metadata and verifies membership."
    )

    target = "exit state"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The F-DATA paper (https://doi.org/10.1038/s41597-025-05633-1), Technical Validation, reports accuracy for both classification tasks, and the "
            "pinned baseline calls classification_report. No operator threshold, cost or deliberate "
            "decision-specific accuracy choice is specified. Under MET-5/6/8 use binary ROC AUC; the target is unchanged."
        )
    )
    accepted_check_warnings = {
        "time_newest_period_short": "Accepted (Andrej, 2026-11-24, with the _1m version of review issue 5): the "
        "frame keeps every training row but only a 500,000-row sample of each test window, so its newest 30 days hold "
        "3,055 rows a day against a median of 22,831 (13%). In the full source they hold 59% of the median (14,015 "
        "against 23,854 a day), because the April 2024 observations begin on 4 April (the cohort-limit note).",
    }

    # This horizon describes the period between refits, not a deadline for the terminal-exit target.
    split_leaf = "L-ORDER.windows"
    temporal = Temporal(on="adt", horizon=4, horizon_unit="months", gap=1, gap_unit="days")
    shuffle = False  # stable Japanese time, filename/row order for equal times; no feature-content tie hashing
    prepared_raw_files = (
        "prepared_source_representations.parquet",
        "selection.json",
        "source_metadata.parquet",
        "selection_membership.parquet",
    )
    # The _1m version: this definition builds its own splits, so it caps the test windows itself; train sides stay whole.
    splits_comment = """
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
    """

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One-time full-cohort selection before expanding the large source vectors. Selection is repeated below.
        _prepare(raw_dir, RAW_FILES, _window_spec())

    def _load_raw(self, raw_dir: Path) -> dict:
        return {
            # Arrow frees each column once pandas holds it, so the 24M x 394 frame is never in memory twice.
            "data": pq.read_table(raw_dir / "prepared_source_representations.parquet").to_pandas(self_destruct=True),
            "metadata": pd.read_parquet(raw_dir / "source_metadata.parquet"),
            "selection": json.loads((raw_dir / "selection.json").read_text()),
        }

    def _clean(self, raw: dict) -> pd.DataFrame:
        # _prepare reads the source representations, the four requests fixed at submission, the submission time and
        # nonpredictor lineage.
        # It expands source vectors without fitting an encoder, and keeps original completed/failed labels.
        # All post-submission fields stay in source metadata or are never read; source positions are removed in _make_splits.
        return raw["data"]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["usr", "jnam", "jobenv_req", "freq_req"], datetime=["adt"])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # Recompute the native budget on ALL source metadata, never on an already-reduced denominator.
        selected, _, population = _select_temporal(self.raw["metadata"], _window_spec())
        key = pd.MultiIndex.from_arrays([df._source_file.astype("uint8"), df._source_row.astype("uint32")])
        expected = pd.MultiIndex.from_frame(selected[["_source_file", "_source_row"]])
        assert key.is_unique
        assert len(df) == len(selected)
        positions = key.get_indexer(expected)
        assert np.all(positions >= 0), "Prepared source membership drifted from native sampling."
        assert np.array_equal(df[self.target].astype(str).to_numpy()[positions], selected[self.target].astype(str))
        assert np.array_equal(df.adt.to_numpy()[positions], selected.adt.to_numpy())
        roles = selected._split_roles.to_numpy()
        assert np.array_equal(df._split_roles.to_numpy()[positions].astype("uint8"), roles)
        splits = {
            i: {
                0: (
                    positions[(roles & (1 << (2 * i))) != 0].tolist(),
                    positions[(roles & (1 << (2 * i + 1))) != 0].tolist(),
                )
            }
            for i in range(3)
        }
        return SplitPlan(
            splits=splits,
            df=df.drop(columns=["_source_file", "_source_row", "_split_roles"]),
            before_sampling=population,
        )

    def _decisions(self, raw: dict, df: pd.DataFrame) -> list[Decision]:
        return [
            Decision(
                "Full-source terminal-label availability and the test-window cap",
                "Training labels end strictly before each refit. Source positions and availability dates are never model inputs.",
                pd.DataFrame(raw["selection"]["windows"]),
            )
        ]


def _window_spec() -> TemporalSplits:
    return TemporalSplits(window=4, unit="months", n_windows=3, min_train_fraction=0.5)


def _japan_datetime(values: pd.Series) -> pd.Series:
    return pd.to_datetime(values, format="mixed", utc=True).dt.tz_convert("Asia/Tokyo").dt.tz_localize(None)


def _verified_metadata(raw_dir: Path, manifest: dict) -> tuple[pd.DataFrame, list[dict]]:
    parts = []
    audit = []
    for source_file, (name, spec) in enumerate(sorted(manifest.items())):
        path = raw_dir / "raw" / name
        assert path.stat().st_size == spec[0], f"Source byte count: {name}"
        digest = hashlib.md5(usedforsecurity=False)  # publisher's integrity digest, not an authentication primitive
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
                digest.update(chunk)
        assert digest.hexdigest() == spec[1], f"Source MD5: {name}"
        df = pd.read_parquet(path, columns=["adt", "edt", "ec", "exit state"])
        assert set(df["exit state"].unique()) <= {"completed", "failed"}, name
        assert np.array_equal(df["exit state"], np.where(df.ec.eq(0), "completed", "failed")), name
        for col in ["adt", "edt"]:
            df[col] = _japan_datetime(df[col])
            assert df[col].notna().all(), f"Missing {col}: {name}"
        assert df.edt.ge(df.adt).all(), f"End before submission: {name}"
        df["exit state"] = pd.Categorical(df["exit state"], categories=["completed", "failed"])
        df["_source_file"] = np.uint8(source_file)
        assert len(df) < 2**24, "Source row offsets must remain exact through float32 canonicalization."
        df["_source_row"] = np.arange(len(df), dtype=np.uint32)
        audit.append(
            {
                "file": name,
                "rows": len(df),
                "failed": int(df.ec.ne(0).sum()),
                "submission_min": str(df.adt.min()),
                "submission_max": str(df.adt.max()),
                "end_max": str(df.edt.max()),
                "max_label_delay_days": float((df.edt - df.adt).dt.total_seconds().max() / 86400),
            }
        )
        parts.append(df.drop(columns="ec"))
        print(f"Verified source metadata: {name}, {len(df):,} rows", flush=True)
    meta = pd.concat(parts, ignore_index=True)
    del parts
    # Equal-time order is publisher filename order, then row offset; no outcome-derived tie ordering.
    meta = meta.sort_values("adt", kind="stable").reset_index(drop=True)
    return meta, audit


def _select_temporal(meta: pd.DataFrame, windows: TemporalSplits) -> tuple[pd.DataFrame, dict, SplitPlan]:
    assert windows.unit == "months", "This preparation's label cutoff is the start of a calendar month."
    splits = windows.splits(meta, "adt")
    report = []
    for repeat, folds in splits.items():
        train, test = (np.asarray(side) for side in folds[0])
        cutoff = meta.adt.iloc[test].min().normalize().replace(day=1)
        # A job trains when it was submitted at least GAP before the window and its outcome was recorded before it.
        known = (meta.edt.iloc[train].to_numpy() < np.datetime64(cutoff)) & (
            meta.adt.iloc[train].to_numpy() < np.datetime64(cutoff - GAP)
        )
        report.append(
            {
                "repeat": repeat,
                "cutoff": str(cutoff),
                "train_before_maturity": len(train),
                "train_after_maturity": int(known.sum()),
                "excluded_late_labels": int((~known).sum()),
                "test_before_cap": len(test),
                "test_failed_before_cap": int(meta["exit state"].iloc[test].eq("failed").sum()),
            }
        )
        splits[repeat][0] = (train[known], test)
    assert min(w["train_after_maturity"] for w in report) >= len(meta) * 0.5
    population = SplitPlan(df=meta, splits={repeat: dict(folds) for repeat, folds in splits.items()})
    # Cap the test windows only, class-proportional, on the full source denominator; train sides stay whole.
    selected, splits, trimmed = sample_temporal_splits(
        meta, splits, RowBudget(train=TABARENA_V0PT2_ROW_BUDGET.train, test=TEST_CAP), stratify_on="exit state"
    )
    roles = np.zeros(len(selected), dtype=np.uint8)
    for repeat, folds in splits.items():
        train, test = folds[0]
        assert repeat < 4, "The stored uint8 role mask supports up to four windows."
        roles[np.asarray(train)] |= np.uint8(1 << (2 * repeat))
        roles[np.asarray(test)] |= np.uint8(1 << (2 * repeat + 1))
        report[repeat].update(
            {
                "train": len(train),
                "test": len(test),
                "train_failed": int(selected["exit state"].iloc[train].eq("failed").sum()),
                "test_failed": int(selected["exit state"].iloc[test].eq("failed").sum()),
            }
        )
        assert selected.edt.iloc[train].lt(pd.Timestamp(report[repeat]["cutoff"])).all()
        assert selected.adt.iloc[train].max() < selected.adt.iloc[test].min()
    assert np.all(roles != 0)
    selected["_split_roles"] = roles
    return (
        selected,
        {
            "source_rows": len(meta),
            "selected_rows": len(selected),
            "trimmed": trimmed,
            "windows": report,
            "sampling": "native sample_temporal_splits, default seed 4267, class-stratified test windows of at most 500k "
            "rows; every training row kept",
            "equal_time_order": "publisher filename order, then source row offset",
        },
        population,
    )


def _write_selected(raw_dir: Path, manifest: dict, selected: pd.DataFrame) -> None:
    target = raw_dir / "prepared_source_representations.parquet"
    temporary = target.with_suffix(".parquet.part")
    writer = None
    written = 0
    try:
        for source_file, name in enumerate(sorted(manifest)):
            file_rows = selected.loc[selected._source_file.eq(source_file)].sort_values("_source_row", kind="stable")
            if file_rows.empty:
                continue
            positions = file_rows._source_row.to_numpy()
            offset = 0
            parts = []
            pf = pq.ParquetFile(raw_dir / "raw" / name)
            for batch in pf.iter_batches(batch_size=16384, columns=[*SOURCE_INPUTS, "embedding"], use_threads=False):
                stop = offset + len(batch)
                left, right = np.searchsorted(positions, [offset, stop])
                if right > left:
                    local = positions[left:right] - offset
                    take = pa.Table.from_batches([batch]).take(pa.array(local))
                    embedding = take["embedding"].combine_chunks()
                    assert not embedding.null_count
                    assert np.all(embedding.value_lengths().to_numpy() == 384)
                    vector = embedding.flatten().to_numpy().reshape(-1, 384)
                    assert np.isfinite(vector).all(), f"Nonfinite embedding: {name}"
                    metadata = file_rows.iloc[left:right]
                    arrays = [take[c].combine_chunks() for c in ["usr", "jnam", "jobenv_req"]]
                    names = ["usr", "jnam", "jobenv_req"]
                    for c in ["nnumr", "cnumr"]:
                        values = take[c].to_numpy()
                        assert np.all(values >= 1), f"Nonpositive {c}: {name}"
                        arrays.append(pa.array(values, type=pa.int64()))
                        names.append(c)
                    frequency = take["freq_req"].to_numpy()
                    assert set(np.unique(frequency)) <= {1600, 2000, 2200}, f"Unknown freq_req: {name}"
                    arrays.append(pa.array(frequency.astype(str)))
                    names.append("freq_req")
                    # The memory limit's "unlimited" code (2^64) is a sentinel, not a size: missing plus an indicator.
                    memory = take["mszl"].to_numpy(zero_copy_only=False).astype(np.float64)
                    unlimited = memory == MSZL_UNLIMITED
                    assert np.isfinite(memory).all(), f"Nonfinite mszl: {name}"
                    assert np.all(memory[~unlimited] > 0), f"Nonpositive mszl: {name}"
                    arrays += [pa.array(np.where(unlimited, np.nan, memory)), pa.array(unlimited.astype(np.int8))]
                    names += ["mszl", "mszl_unlimited"]
                    arrays += [pa.array(vector[:, j], type=pa.float32()) for j in range(384)]
                    names += [f"embedding_{j:03d}" for j in range(384)]
                    for c in ["adt", "exit state", "_source_file", "_source_row", "_split_roles"]:
                        values = metadata[c].astype(str) if c == "exit state" else metadata[c]
                        arrays.append(pa.array(values))
                        names.append(c)
                    parts.append(pa.Table.from_arrays(arrays, names=names))
                offset = stop
            # One monthly file at a time, in submission-time order (ties: source row): the files hold disjoint months,
            # so the frame arrives sorted by time and the standard steps need not copy it to sort it.
            table = pa.concat_tables(parts)
            del parts
            table = table.take(pa.array(np.argsort(table["adt"].to_numpy(), kind="stable")))
            if writer is None:
                writer = pq.ParquetWriter(temporary, table.schema, compression="zstd")
            writer.write_table(table)
            written += len(table)
            del table
            print(f"Prepared selected source rows: {name}, {len(file_rows):,}", flush=True)
        assert written == len(selected), (written, len(selected))
    finally:
        if writer is not None:
            writer.close()
    temporary.replace(target)


def _prepare(raw_dir: Path, manifest: dict, windows: TemporalSplits) -> None:
    meta, monthly = _verified_metadata(raw_dir, manifest)
    meta.to_parquet(raw_dir / "source_metadata.parquet", index=False)
    selected, report, _ = _select_temporal(meta, windows)
    del meta
    _write_selected(raw_dir, manifest, selected)
    selected.to_parquet(raw_dir / "selection_membership.parquet", index=False)
    report["monthly"] = monthly
    (raw_dir / "selection.json").write_text(json.dumps(report, indent=2) + "\n")
