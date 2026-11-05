"""F-DATA source exit-state prediction with qualified temporal execution-record splits."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    SplitPlan,
    TaskSummary,
    Temporal,
    TemporalSplits,
)
from data_foundry.v2.splits import sample_temporal_splits

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
            "One released job-execution record. The source contains 25,866,900 records from March 2021 to April 2024; this version retains the union of the capped temporal sides."
        ),
        predicted=(
            "The source's terminal exit state: completed for exit code zero, failed for nonzero. This is not a "
            "hardware-failure diagnosis; an intentional nonzero return may occur without failed computation."
        ),
        known=(
            "The masked submitting user, job name and requested job environment; the released 384-value pretrained "
            "embedding of those original strings; and the submission time. All are based on information known at submission."
        ),
        split=(
            "Three successive four-month future windows on the same supercomputer, with earlier completed labels "
            "for training: May–August 2023, September–December 2023, and January–April 2024."
        ),
        changes=(
            "Keep the original labels and representations. Combine categories and embedding, and add submission time; "
            "the authors evaluated representations separately. Refit for three four-month windows covering May "
            "2023–April 2024 instead of their fixed June 2023–April 2024 holdout. Exclude unavailable training labels "
            "and apply the native row budget."
        ),
        fit="approximate",
        fit_reason=(
            "The release selects jobs with several recorded post-run measurements. Its coverage of all attempted "
            "submissions cannot be established from the public selected cohort alone. Nonzero exit is a proxy for "
            "actionable failure, and released records cannot be mapped reliably to parent-job decisions."
        ),
    )

    unique_name = "fugaku_hpc_job_failure_1m"
    version_of = "fugaku_hpc_job_failure"
    version_comment = (
        "The native class-stratified temporal budget keeps up to 1M training and 500k test rows per window, "
        "using the default seed 4267 over the full eligible history. Only the selected union's embeddings are "
        "materialized to bound memory; _make_splits redoes selection on full-source metadata and verifies membership."
    )
    year = "2024"
    domain = "technology & internet"
    source = "Other"
    source_url = "https://doi.org/10.5281/zenodo.11467483"
    license = "CC BY 4.0"
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
        and applies the native temporal row budget. It then expands only the selected union's384-value source vectors.
        source_metadata.parquet and selection_membership.parquet retain local selection lineage; selection.json records
        full-source monthly counts, cutoff exclusions and capped class support. These are reproducible intermediates,
        not additional upstream releases and not model inputs. The preparation code and constants participate in the
        framework's prepared-input cache hash. _make_splits repeats native selection against full-source metadata and
        checks exact source positions before removing lineage columns. No container is built by dataset check.
    """
    bibtex = r"""
        @dataset{Antici2024FData,
          author = {Antici, Francesco and Bartolini, Andrea and Domke, Jens and Kiziltan, Zeynep and Yamamoto, Keiji},
          title = {F-DATA: A Fugaku Workload Dataset for Job-centric Predictive Modelling in HPC Systems},
          year = {2024},
          version = {1.0},
          publisher = {Zenodo},
          doi = {10.5281/zenodo.11467483},
          url = {https://doi.org/10.5281/zenodo.11467483}
        }
    """
    curation_comments = """
        We start with all 38 publisher Parquets from F-DATA v1.0 (Zenodo 11467483), checked against the pinned sizes and MD5s.

        - Prediction point: job submission, before queue insertion, scheduling or execution.
        - Target: retain the source completed/failed strings, exactly ec==0 versus nonzero. All 25,866,900 records agree with that rule: 23,308,381 completed and 2,558,519 failed (9.891%). A nonzero return may be intentional; this is exit-state prediction, not hardware-failure diagnosis or failure within a fixed duration.
        - Inputs: source masked usr, jnam and jobenv_req as nominal categories, and the 384 coordinates of the source embedding. The latter encodes the original versions of those same strings with pretrained all-MiniLM-L6-v2, without outcomes. All source vectors are float32, length 384 and finite. We fit no new encoder and do not reconstruct the private original strings. Author code: https://github.com/francescoantici/F-DATA/tree/db67a65a4b6e91dcebd26147de191fa0051ad790 .
        - Typing rationale (CLEAN-14 Should departure, serving USE-1/10): usr, jnam and jobenv_req are stable opaque nominal identities. The selected union has 359,636 masked job names; text processing cannot recover the private originals and could attach meaning to arbitrary token suffixes. Keep those source identities categorical despite the high-cardinality string default.
        - Changes from source experiments: combine their separate category/embedding representations and add the known submission time as a datetime input. Requested resources are not silently added. Requested elapsed limits and priority can be altered after submission (Fujitsu job manual section2.5.4, https://www.r-ccs.riken.jp/fugaku/docs/manual/en/jos/j2ul-2534-01enz0.pdf), so their released snapshot timing would also need qualification before any extension.
        - Exclusions: jid is a nonunique released identifier, not a unique execution-record key; its exact parent/subjob semantics are unresolved. Do not deduplicate by it. Exclude all allocated/used resource fields, queue/scheduling/start/deletion/end timestamps, exit code, duration, power/energy, counters and performance-derived outcomes from predictors. End time and exit code are read only for label availability and target checks. Requested cores, nodes, memory, frequency, time limit and priority are outside this source-experiment input set.
        - Row identity: there are no exact duplicates over the 44 nonembedding source fields within a month, and submission months are disjoint across files. Repeated job IDs have distinct submission/end times and sometimes labels. The public release lacks explicit subjob identifiers; the finer bulk/step/retry structure cannot be recovered. Preserve the released execution records and evaluate future jobs on the same system with recurring identities.
        - Evaluation unit: scores weight released execution records, not uniquely identified parent submissions. Repeated retained inputs can describe distinct executions: all 38 traced pairs of exact projected duplicates differ in source execution timing. No full raw nonembedding copies were found; this does not establish independence or recover subjob structure.
        - Time: parse the source offset timestamps as instants, convert to Asia/Tokyo and remove the timezone only then, preserving Japanese calendar boundaries. Equal-time ties keep publisher filename and row order; no outcome-based tie order is introduced.
        - Cohort limit: the source cleaner requires several post-run measurements. Excluded early failures, uninstrumented executions and still-pending submissions cannot be counted from the release. April 2024 observations begin April 4 and have completion times through May 14; this does not prove every long-queued April submission is represented. Fit is approximate for all submitted jobs, and the benchmark describes the released recorded-execution cohort without claiming a complete submission census.
        - Value follow-up: native task flags no_spread and drift_baseline received bounded train-only tuning, date ablations and foldwise raw-user comparisons. Ranking signal is present; two configurations do not establish tuned-family separation or operational probability quality. Recheck family separation, foldwise simple baselines and probability quality at the first tuned benchmark run (TP-1/3/4; EV-3/7/8).
        - Curator decisions (2026-11-03, Myunghwan): accepts this measured future exit-state task and retains it with the first-tuned-benchmark recheck. The gap choice was accepted subject to completion/maturity checks, which passed the recorded-label boundary on the full source and exact shipped train sides; recent outcome selection and reporting-latency sensitivity remain documented. No target or submission-time input rule is changed.
        - Maturity qualification (2026-11-03): the full 25,866,900-row interval audit and all three exact 1M training sides pass recorded completion strictly before refit; 10,387/48,375/28,118 source outcomes are excluded at May/Sep/Jan cutoffs. Completion is a proxy for label arrival, not a verified ingestion timestamp. Near-cutoff class selection is real: before September, late-ending last-day jobs fail at 18.53% versus 0.292% among already completed jobs. A hypothetical 24h reporting delay removes 0.1049–0.1111% of each capped training side. Fixed-parameter paired diagnostics change AUC by about -0.010 for that lag and -0.0166/+0.0044/-0.0458 for a seven-day submission embargo, newest first. No gap was chosen from these held-out scores; these are bounded single-family checks, not full-budget resampling or full HPO. Keep reporting-latency and maturity sensitivity in the first-tuned-benchmark recheck. Test labels are eventual exit states; completion after a four-month submission window is legitimate, and all recorded source ends precede release publication.
        - Sampling: native class-proportional sampling is applied on the full-source metadata after each cutoff's training-label availability filter, never on the reduced union. It keeps at most 1M training and 500k test records per window, without balancing classes. Metadata source positions map the selected vectors exactly; _make_splits recomputes membership and removes all lineage columns before models.
    """

    target = "exit state"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The F-DATA paper (https://doi.org/10.1038/s41597-025-05633-1), Technical Validation, reports accuracy for both classification tasks, and the "
            "pinned baseline calls classification_report. No operator threshold, cost or deliberate "
            "decision-specific accuracy choice is specified. Under MET-5/6/8 use binary ROC AUC; the target is unchanged."
        )
    )
    accepted_check_warnings = {}

    # This horizon describes the period between refits, not a deadline for the terminal-exit target.
    temporal = Temporal(on="adt", horizon=4, horizon_unit="months")
    shuffle = False  # stable Japanese time, filename/row order for equal times; no feature-content tie hashing
    prepared_raw_files = (
        "prepared_source_representations.parquet",
        "selection.json",
        "source_metadata.parquet",
        "selection_membership.parquet",
    )
    splits_comment = """
        Three four-month test windows walk backward from the latest source month; training is the earlier history,
        with at least 50% of full-source rows before the oldest window. End time must precede each window's start
        as the observed proxy for label availability; any later reporting delay is unreleased. Sampling follows native sample_temporal_splits with default seed 4267,
        proportional class quotas, up to 1M training and 500k test rows per window. It does not balance the classes.
        Source identities recur: this tests future jobs on the same system, not unseen users. Equal submission
        times retain publisher filename and row order. Source positions and label-availability times are lineage
        metadata, removed before models. Windows are May–August 2023, September–December 2023 and January–April 2024, newest first. These cover the paper's eleven-month holdout plus May 2023; unlike its fixed training period, each window refits on earlier observed labels. Four months is the disclosed benchmark refit judgment, not a source-established production cadence.
        Exception to SPLIT-10 (2026-11-03, Myunghwan): no additional fixed embargo after exact recorded-completion filtering. Precise completion timestamps let each refit use recorded outcomes ending before it. The full-source and exact-membership audit finds zero retained training outcomes at/after any cutoff; unavailable labels still leave under SPLIT-9. Fast-completer selection and unreleased post-completion reporting latency remain limitations. Serves P4: SPLIT-1 deployment fidelity to the completed outcomes available at a live refit.
    """

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One-time full-cohort selection before expanding the large source vectors. Selection is repeated below.
        _prepare(raw_dir, RAW_FILES, _window_spec())

    def _load_raw(self, raw_dir: Path) -> dict:
        return {
            "data": pd.read_parquet(raw_dir / "prepared_source_representations.parquet"),
            "metadata": pd.read_parquet(raw_dir / "source_metadata.parquet"),
            "selection": json.loads((raw_dir / "selection.json").read_text()),
        }

    def _clean(self, raw: dict) -> pd.DataFrame:
        # _prepare reads only source experiment representations, plus submission time and nonpredictor lineage.
        # It expands source vectors without fitting an encoder, and keeps original completed/failed labels.
        # All post-submission fields stay in source metadata or are never read; source positions are removed in _make_splits.
        return raw["data"]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["usr", "jnam", "jobenv_req"], datetime=["adt"])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # Recompute the native budget on ALL source metadata, never on an already-reduced denominator.
        selected, _ = _select_temporal(self.raw["metadata"], _window_spec())
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
        return SplitPlan(splits=splits, df=df.drop(columns=["_source_file", "_source_row", "_split_roles"]))

    def _decisions(self, raw: dict, df: pd.DataFrame) -> list[Decision]:
        return [
            Decision(
                "Full-source terminal-label availability and native row budgets",
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


def _select_temporal(meta: pd.DataFrame, windows: TemporalSplits) -> tuple[pd.DataFrame, dict]:
    assert windows.unit == "months", "This preparation's label cutoff is the start of a calendar month."
    splits = windows.splits(meta, "adt")
    report = []
    for repeat, folds in splits.items():
        train, test = (np.asarray(side) for side in folds[0])
        cutoff = meta.adt.iloc[test].min().normalize().replace(day=1)
        known = meta.edt.iloc[train].to_numpy() < np.datetime64(cutoff)
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
    selected, splits, trimmed = sample_temporal_splits(meta, splits, stratify_on="exit state")
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
    return selected, {
        "source_rows": len(meta),
        "selected_rows": len(selected),
        "trimmed": trimmed,
        "windows": report,
        "sampling": "native sample_temporal_splits, default seed 4267, class-stratified 1M train / 500k test",
        "equal_time_order": "publisher filename order, then source row offset",
    }


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
            pf = pq.ParquetFile(raw_dir / "raw" / name)
            for batch in pf.iter_batches(
                batch_size=16384, columns=["usr", "jnam", "jobenv_req", "embedding"], use_threads=False
            ):
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
                    arrays += [pa.array(vector[:, j], type=pa.float32()) for j in range(384)]
                    names += [f"embedding_{j:03d}" for j in range(384)]
                    for c in ["adt", "exit state", "_source_file", "_source_row", "_split_roles"]:
                        values = metadata[c].astype(str) if c == "exit state" else metadata[c]
                        arrays.append(pa.array(values))
                        names.append(c)
                    table = pa.Table.from_arrays(arrays, names=names)
                    if writer is None:
                        writer = pq.ParquetWriter(temporary, table.schema, compression="zstd")
                    writer.write_table(table)
                    written += len(table)
                offset = stop
            print(f"Prepared selected source rows: {name}, {len(file_rows):,}", flush=True)
        assert written == len(selected), (written, len(selected))
    finally:
        if writer is not None:
            writer.close()
    temporary.replace(target)


def _prepare(raw_dir: Path, manifest: dict, windows: TemporalSplits) -> None:
    meta, monthly = _verified_metadata(raw_dir, manifest)
    meta.to_parquet(raw_dir / "source_metadata.parquet", index=False)
    selected, report = _select_temporal(meta, windows)
    del meta
    _write_selected(raw_dir, manifest, selected)
    selected.to_parquet(raw_dir / "selection_membership.parquet", index=False)
    report["monthly"] = monthly
    (raw_dir / "selection.json").write_text(json.dumps(report, indent=2) + "\n")
