"""The curation checks that need the definition class, and the check run of ``dataset check``.

:func:`run_definition_checks` runs the bundle checks (:mod:`data_foundry.checks.bundle`), the checks of a v2 task
(:mod:`data_foundry.checks.task`, :mod:`data_foundry.checks.groups`) and the checks below, then drops the findings
the definition accepts in ``accepted_check_warnings`` as the registry allows
(:meth:`data_foundry.checks.registry.Check.accepts`):

* the definition file (:func:`definition_findings`, :func:`summary_findings`): scaffold markers (joined with the
  bundle's placeholders in the metadata into one ``meta_placeholder_left``), nondeterministic code, the task summary;
* the raw files (:func:`raw_file_findings`): a pattern that matches nothing, files changed since the README;
* a temporal split (:func:`floor_findings`, :func:`window_size_findings`): SPLIT-14's training floor and least test
  window (SPLIT-15's number of windows is a split-protocol check,
  :func:`data_foundry.checks.protocol.protocol_checks`);
* the newest period of a temporal task (:func:`newest_period_findings`).
"""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from data_foundry.checks import (
    groups as group_checks,
    task as task_checks,
)
from data_foundry.checks.bundle import run_bundle_checks
from data_foundry.checks.protocol import scored_units_of
from data_foundry.checks.registry import CHECKS
from data_foundry.checks.results import SEVERITY_ORDER, BundleCheckReport, CheckResult, merge_same_slug, run_guarded
from data_foundry.definition.dataset import (
    DEFINITION_FILENAME,
    REPORT_FILENAME,
    SUMMARY_MAX_WORDS,
    clean_text,
    definition_file,
    nondeterministic_calls,
)
from data_foundry.definition.report import read_report

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer
    from data_foundry.definition.dataset import AbstractCuratedDataset
    from data_foundry.schema import RawFile

NEWEST_PERIOD_DAYS = 30
"""The span whose rows a day the newest-period check compares with the spans before it."""

NEWEST_PERIOD_RATIO = 0.6
"""Below this share of the earlier spans' median, the newest period is flagged as short."""

FLOOR_CORE = 0.5
"""SPLIT-14's floor: every window trains on this share of the rows or more, unless the curator makes an exception."""

FLOOR_LOWER = 0.3
"""SPLIT-14's lower bound: a curator's exception goes down to this share of the rows, never below."""

MIN_TEST_UNITS = 33
"""SPLIT-14's least test window: 33 scored units, a third of a 100-unit table as one IID test fold holds it."""


def newest_period_rate(times: pd.Series, *, days: int = NEWEST_PERIOD_DAYS) -> tuple[float, float, float] | None:
    """Rows a day in the newest ``days`` days of a date column, the median over up to twelve spans of ``days`` days
    before them, and their ratio; ``None`` for a column that is no date or spans fewer than four such spans.
    """
    if not pd.api.types.is_datetime64_any_dtype(times):
        return None
    days_of = times.dropna().dt.floor("D")
    if days_of.empty:
        return None
    first, last = days_of.min(), days_of.max()
    per_day = days_of.value_counts().reindex(pd.date_range(first, last, freq="D"), fill_value=0).to_numpy()
    if len(per_day) < 4 * days:
        return None
    newest = float(per_day[-days:].mean())
    spans = [per_day[-(k + 1) * days : -k * days].mean() for k in range(1, min(12, len(per_day) // days - 1) + 1)]
    median = float(np.median(spans))
    return (newest, median, newest / median) if median > 0 else None


def run_definition_checks(
    ds: AbstractCuratedDataset,
    container: CuratedContainer,
    *,
    verbose: bool,
    group_stats: group_checks.GroupStats | None = None,
) -> BundleCheckReport:
    """Every check of ``ds``'s container, without the findings its ``accepted_check_warnings`` may silence."""
    accepted = tuple(ds.accepted_check_warnings)
    # a format-2 container: the v2 protocol checks included
    report = run_bundle_checks(container, verbose=False, from_definition=True)
    shared = report.results
    own: list[CheckResult] = []
    for name, run in (
        ("definition", lambda: definition_findings(ds)),
        ("group", lambda: group_checks.group_findings(group_stats)),
        ("task", lambda: task_checks.task_findings(container)),
        ("raw files", lambda: raw_file_findings(ds, container.dataset_metadata.raw_files)),
        ("floor", lambda: floor_findings(ds, container)),
        ("newest period", lambda: newest_period_findings(ds)),
    ):
        own += run_guarded(f"{name} checks", run)
    found = merge_same_slug([*shared, *own], "meta_placeholder_left")
    unused = [slug for slug in accepted if slug not in {r.slug for r in found}]
    if unused:
        found.append(
            CheckResult(
                "accepted_check_warnings_unused",
                "info",
                f"Accepted on purpose but not found: {unused}.",
                hint="Remove the entries that no longer apply, or fix a misspelled slug.",
            ),
        )
    kept = [r for r in found if r.slug not in accepted or not CHECKS[r.slug].accepts(r.severity)]
    report.results = sorted(kept, key=lambda r: SEVERITY_ORDER[r.severity])
    report.ignored = accepted
    if verbose:
        print("\n".join(["Metric:", *container.task_metadata.objective_metric.describe_lines()]))
        print(report.summary())
    return report


def floor_findings(ds: AbstractCuratedDataset, container: CuratedContainer) -> list[CheckResult]:
    """SPLIT-14 on a temporal split: every window trains on at least half the rows; a window under half is a
    curator's exception (a warning accepted once the record carries the curator's CC line), down to 30% and never
    below (an error); every test window holds at least ``MIN_TEST_UNITS`` scored units (an error). SPLIT-15's
    number of windows is ``splits_dimensions_off_protocol``, a split-protocol check.

    The shares count every row of the curated frame: a `_1m` version's container keeps every training row but
    samples its test windows.
    """
    if ds.temporal is None:
        return []
    n_rows = getattr(ds, "_frame_rows", None) or len(container.dataset)
    splits = container.experiment_metadata.splits
    windows = [(repeat, train, test) for repeat, folds in splits.items() for train, test in folds.values()]
    if not windows:
        return []
    shares = {repeat: len(train) / n_rows for repeat, train, _test in windows}
    under = {r: s for r, s in shares.items() if s < FLOOR_CORE}
    low = {r: s for r, s in under.items() if s < FLOOR_LOWER}
    findings = []
    if under:
        listed = ", ".join(f"window {r} on {s:.1%}" for r, s in sorted(under.items()))
        findings.append(
            CheckResult(
                "splits_train_under_half",
                "warning",
                f"{len(under)} window(s) train on less than half the rows: {listed}.",
                hint="SPLIT-14 asks every window to train on at least half the rows; a window under half is the "
                "curator's exception for this dataset: raise it in the record's `## Review`, and once the record "
                "carries the curator's CC line, accept this warning with that date.",
            )
        )
    if low:
        findings.append(
            CheckResult(
                "splits_train_under_floor",
                "error",
                "Window(s) under SPLIT-14's lower bound of 30%: "
                + ", ".join(f"window {r} on {s:.1%}" for r, s in sorted(low.items()))
                + ".",
                hint="No exception goes below 30% of the rows: drop the window or widen the others "
                "(knowledge-curation splits.md, SPLIT-14).",
            )
        )
    findings += window_size_findings(container, windows)
    return findings


def window_size_findings(container: CuratedContainer, windows: list) -> list[CheckResult]:
    """SPLIT-14's least test window, in scored units (SPLIT-33): ``splits_test_too_small``.

    The units are those of :func:`data_foundry.checks.protocol.scored_units_of`: a scored unit no window cuts, else
    the rows.
    """
    units = scored_units_of(container, windows)

    def count(rows) -> int:
        return int(units.iloc[list(rows)].nunique(dropna=False)) if units is not None else len(rows)

    small = sorted((repeat, n) for repeat, _train, test in windows if (n := count(test)) < MIN_TEST_UNITS)
    if not small:
        return []
    return [
        CheckResult(
            "splits_test_too_small",
            "error",
            f"Test window(s) with fewer than {MIN_TEST_UNITS} scored units: "
            + ", ".join(f"window {r} with {n}" for r, n in small)
            + ".",
            hint="SPLIT-14: widen the windows (or fewer of them) until each holds 33 scored units.",
        )
    ]


def newest_period_findings(ds: AbstractCuratedDataset) -> list[CheckResult]:
    """A newest period with far fewer rows a day than the spans before it: often a download or a scrape cut
    before the outcomes were complete (kickstarter, reviews of 2026-11-10 and 11; LEAK-24).
    """
    rate = getattr(ds, "_newest_rate", None)
    if rate is None or rate[2] >= NEWEST_PERIOD_RATIO:
        return []
    last, median, ratio = rate
    return [
        CheckResult(
            "time_newest_period_short",
            "warning",
            f"The newest {NEWEST_PERIOD_DAYS} days hold {last:,.0f} rows a day against a median of {median:,.0f} "
            f"over the {NEWEST_PERIOD_DAYS}-day spans before ({ratio:.0%}).",
            hint="Check whether the release cut the newest period before its outcomes were complete (a scrape "
            "that keeps only ended cases, a download before late reports): compare its target rate with earlier "
            "periods, and cut the data where follow-up is complete; or accept it with the reason (a seasonal "
            "low, a real decline).",
        )
    ]


def summary_findings(ds: AbstractCuratedDataset) -> list[CheckResult]:
    """Findings about :attr:`task_summary`: missing, no use case, or too long to read at a glance."""
    summary = ds.task_summary
    if summary is None:
        return [
            CheckResult(
                "definition_summary_missing",
                "error",
                "`task_summary` is not set: the README has no plain-language summary of the task.",
                hint="Add `task_summary = TaskSummary(...)` at the top of the class (knowledge-data-foundry "
                'definitions.md, "In brief").',
            ),
        ]
    findings = []
    if summary.fit == "none":
        findings.append(
            CheckResult(
                "definition_no_use_case",
                "error",
                f"`TaskSummary(fit='none')`: {clean_text(summary.fit_reason)}",
                hint="A dataset that simulates no decision is retired (`No Good Target / Scientific Discovery`), "
                "not shipped.",
            ),
        )
    long = {name: len(text.split()) for name, text in summary.fields().items() if len(text.split()) > SUMMARY_MAX_WORDS}
    if long:
        findings.append(
            CheckResult(
                "definition_summary_long",
                "warning",
                f"`task_summary` field(s) over {SUMMARY_MAX_WORDS} words: {long}.",
                hint="Keep each field to one or two plain sentences; the evidence belongs in `curation_comments`.",
            ),
        )
    return findings


def definition_findings(ds: AbstractCuratedDataset) -> list[CheckResult]:
    """Findings about the definition file: scaffold markers, nondeterministic code, and the summary. A placeholder
    license is in the container's metadata, which the bundle's ``meta_placeholder_left`` reads.
    """
    findings = []
    file = definition_file(type(ds))
    if file is not None:
        text = file.read_text()
        todo = [i for i, line in enumerate(text.splitlines(), start=1) if "TODO(verify)" in line]
        if todo:
            findings.append(
                CheckResult(
                    "meta_placeholder_left",
                    "error",
                    f"{DEFINITION_FILENAME} still has {len(todo)} `TODO(verify)` marker(s), on line(s) {todo[:20]}.",
                    hint="Resolve each `TODO(verify)` marker (check the data, then write the step or delete the stub).",
                ),
            )
        unstable = nondeterministic_calls(ast.parse(text))
        if unstable:
            listed = "; ".join(f"line {line}: {why}" for line, why in unstable[:10])
            findings.append(
                CheckResult(
                    "definition_nondeterministic",
                    "error",
                    f"{DEFINITION_FILENAME} has {len(unstable)} call(s) whose result can change between runs or "
                    f"machines: {listed}.",
                    hint="Seed every random step (`random_state=`, a seeded `default_rng`, `anonymize_ids` for "
                    'ids), sort with `kind="stable"`, wrap file listings in `sorted(...)`, and use '
                    "`maintain_order=True` in a polars `group_by`.",
                ),
            )
    findings += summary_findings(ds)
    changed = getattr(ds, "_time_changed_in_split", 0)
    if changed:
        time_on = ds.task_metadata.time_on
        findings.append(
            CheckResult(
                "definition_time_changed_in_split",
                "warning",
                f"`_make_splits` changes the time column `{time_on}` on {changed:,} rows. The rows were ordered "
                "by its values before that step, so within a coarsened period they keep the order of the finer "
                "time (the minute of chicago_traffic_crashes, 2026-11-04).",
                hint=f"Coarsen `{time_on}` in `_clean`; within a period the rows then follow the content order.",
            ),
        )
    return findings


def raw_file_findings(ds: AbstractCuratedDataset, manifest: list[RawFile]) -> list[CheckResult]:
    """A source's file pattern that matches nothing, and raw files changed since the README was written."""
    findings = []
    unmatched = getattr(ds, "_unmatched_raw_files", [])
    if unmatched:
        findings.append(
            CheckResult(
                "raw_files_missing",
                "error",
                f"`Source(files=...)` names {unmatched}, which match no file under {ds.raw_dir}.",
                hint="Download the files (`download_description`), or fix the pattern.",
            ),
        )
    before = read_report(ds.report_path).get("raw_files") if ds.report_path is not None else None
    if before:
        now = {f.path: f.sha256 for f in manifest}
        changed = sorted(p for p in now if p in before and before[p] != now[p])
        added, removed = sorted(set(now) - set(before)), sorted(set(before) - set(now))
        if changed or added or removed:
            parts = [
                f"{label}: {paths[:10]}"
                for label, paths in (("changed", changed), ("new", added), ("gone", removed))
                if paths
            ]
            findings.append(
                CheckResult(
                    "raw_files_changed",
                    "warning",
                    f"The raw files differ from those {REPORT_FILENAME} was written from; {'; '.join(parts)}.",
                    hint="A source may have published a new version: check what changed before writing the "
                    "README again.",
                ),
            )
    return findings
