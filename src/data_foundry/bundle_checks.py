"""Post-hoc integrity checks for a curated bundle (a :class:`CuratedContainer`).

Where the other two check layers sit:

* :mod:`data_foundry.schema` — *coherence of one metadata object*, enforced in
  ``__post_init__`` at creation time (e.g. ``group_labels`` requires ``group_on``).
  Cheap, no DataFrame needed, so a broken combination cannot even be constructed.
* :mod:`data_foundry.dataset_checks` — *exploratory* report on the DataFrame
  (``run_all_checks``): statistics a human reads while curating.
* this module — *cross-referential* checks that need the whole bundle at once:
  the DataFrame, the task metadata, the splits, and the dataset metadata together.
  These are the ones that can only run at the end: "does ``time_on`` name a real
  column, is it sorted, do the splits index inside the frame, does every fold's
  train set cover the classes its test set contains, do the ``data_tags`` agree
  with the split regime the task actually declares".

Usage in a curation notebook — build the container, check it, then save::

    report = run_bundle_checks(curated_data)
    report.raise_if_errors()
    save_path = curated_data.save()
    verify_saved_container(save_path, container=curated_data).raise_if_errors()

Every finding carries a stable ``slug``; pass ``ignore=["slug", ...]`` to accept a
finding on purpose (the notebook then documents the accepted deviation).
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import numpy as np
import pandas as pd

from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import as_column_list

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator

    from data_foundry.schema import (
        DatasetMetadata,
        PredictiveMLSplitsMetadata,
        PredictiveMLTaskMetadata,
    )

Severity = Literal["error", "warning", "info"]

SEVERITY_ORDER: dict[Severity, int] = {"error": 0, "warning": 1, "info": 2}

DEFAULT_HEAVY_CELL_BUDGET = 50_000_000
"""Cell budget (``n_rows * n_cols``) above which O(rows x cols) checks are skipped.

Skipped checks are reported as ``info`` findings — never silently dropped.
"""

KNOWN_METRICS: dict[str, set[str]] = {
    "binary_classification": {
        "roc_auc",
        "average_precision",
        "log_loss",
        "accuracy",
        "balanced_accuracy",
        "f1",
        "mcc",
        "precision",
        "recall",
    },
    "multiclass_classification": {
        "log_loss",
        "accuracy",
        "balanced_accuracy",
        "f1_macro",
        "f1_micro",
        "f1_weighted",
        "mcc",
        "roc_auc_ovo_macro",
        "roc_auc_ovr_macro",
    },
    "regression": {
        "rmse",
        "root_mean_squared_error",
        "mae",
        "mean_absolute_error",
        "mse",
        "mean_squared_error",
        "r2",
        "rmsle",
        "root_mean_squared_logarithmic_error",
        "mape",
        "mean_absolute_percentage_error",
        "median_absolute_error",
        "pearsonr",
        "spearmanr",
    },
}
"""Metric names we recognize per problem type (sklearn / AutoGluon spelling).

An unrecognized name is not an error — custom competition metrics (e.g.
``amex_metric``) are intentional — but it must be registered on the consumer side,
so it is surfaced as an ``info``.
"""

TABARENA_DEFAULT_METRICS: dict[str, str] = {
    "binary_classification": "roc_auc",
    "multiclass_classification": "log_loss",
    "regression": "root_mean_squared_error",
}
"""Metric TabArena falls back to when it does not accept ``objective_metric_name``.

Mirrors ``tabarena.benchmark.task.data_foundry.DEFAULT_EVAL_METRICS``; only used to
tell the curator which metric a run would *actually* optimize.
"""

MISSING_VALUE_SENTINELS: tuple[float, ...] = (-1.0, -9.0, -99.0, -999.0, -9999.0, -99999.0, 999.0, 9999.0, 99999.0)
"""Numeric values that are commonly a proxy for "missing" rather than a real value.

The curation guidelines require proxy missing values to be converted to explicit
``NA`` whenever the encoding can be inferred, so a suspicious spike is worth a look.
"""

MISSING_VALUE_STRINGS: frozenset[str] = frozenset({"", " ", "?", "na", "n/a", "nan", "null", "missing"})
"""Category/string labels that almost always encode a missing value rather than a class.

Deliberately excludes ambiguous levels (``"none"``, ``"unknown"``, ``"-"``): those are
real, documented categories in many datasets, so flagging them is noise.
"""

DUPLICATE_ROW_WARN_SHARE = 0.01
"""Share of duplicated rows above which duplicates are a warning rather than an info.

A handful of duplicates is normal in real-world tabular data; a large share means the
split protocol will spread copies of the same row across train and test.
"""

PLACEHOLDER_PATTERNS: tuple[str, ...] = (r"\bTODO\b", r"\bFIXME\b", r"xxx\.csv", r"<unique_name>")
"""Scaffolding markers (regexes) that must not survive into a shipped bundle."""


class BundleCheckError(RuntimeError):
    """Raised by :meth:`BundleCheckReport.raise_if_errors` when a bundle has errors."""


@dataclass(frozen=True)
class CheckResult:
    """One finding of a bundle check.

    Attributes:
        slug: Stable identifier of the check (use it in ``ignore=[...]``).
        severity: ``"error"`` (must fix), ``"warning"`` (look at it), or ``"info"``.
        message: What was found, including the offending values.
        hint: Optional "what to do about it" follow-up.
    """

    slug: str
    severity: Severity
    message: str
    hint: str | None = None

    def __str__(self) -> str:
        text = f"[{self.slug}] {self.message}"
        return f"{text}\n    -> {self.hint}" if self.hint else text


@dataclass
class BundleCheckReport:
    """The findings of :func:`run_bundle_checks` for one bundle.

    Print it (``print(report)`` / just evaluate it in a notebook cell) for the
    human-readable report, use :meth:`raise_if_errors` to fail a notebook run, and
    :meth:`to_dict` to persist a machine-readable record of what was checked.
    """

    unique_name: str
    results: list[CheckResult] = field(default_factory=list)
    ignored: tuple[str, ...] = ()
    n_checks_run: int = 0

    def by_severity(self, severity: Severity) -> list[CheckResult]:
        """Return all findings of one severity, in the order they were produced."""
        return [r for r in self.results if r.severity == severity]

    @property
    def errors(self) -> list[CheckResult]:
        """Findings that must be fixed before the bundle is saved/shipped."""
        return self.by_severity("error")

    @property
    def warnings(self) -> list[CheckResult]:
        """Findings that need a human call (often fine, sometimes a real defect)."""
        return self.by_severity("warning")

    @property
    def infos(self) -> list[CheckResult]:
        """Informational findings, including checks skipped for cost reasons."""
        return self.by_severity("info")

    @property
    def ok(self) -> bool:
        """Whether the bundle produced no errors (warnings are allowed)."""
        return not self.errors

    @property
    def slugs(self) -> list[str]:
        """The slugs of all findings, in report order."""
        return [r.slug for r in self.results]

    def raise_if_errors(self) -> BundleCheckReport:
        """Raise :class:`BundleCheckError` if any finding is an error, else return self."""
        if self.ok:
            return self
        details = "\n".join(f"  - {r}" for r in self.errors)
        raise BundleCheckError(
            f"{len(self.errors)} bundle check error(s) for {self.unique_name!r}:\n{details}\n"
            "Fix the bundle, or pass `ignore=[<slug>, ...]` to accept a finding on purpose.",
        )

    def to_dict(self) -> dict:
        """Return a JSON-serializable record of the report."""
        return {
            "unique_name": self.unique_name,
            "n_checks_run": self.n_checks_run,
            "ignored": list(self.ignored),
            "counts": {
                "error": len(self.errors),
                "warning": len(self.warnings),
                "info": len(self.infos),
            },
            "findings": [
                {"slug": r.slug, "severity": r.severity, "message": r.message, "hint": r.hint} for r in self.results
            ],
        }

    def to_json(self, path: Path | str) -> Path:
        """Write :meth:`to_dict` to ``path`` (as an audit trail next to the bundle)."""
        path = Path(path)
        with path.open("w") as f:
            json.dump(self.to_dict(), f, indent=2)
        return path

    def summary(self) -> str:
        """Return the human-readable report (same text as ``str(report)``)."""
        head = (
            f"Bundle checks — {self.unique_name}: "
            f"{len(self.errors)} error(s), {len(self.warnings)} warning(s), {len(self.infos)} info "
            f"({self.n_checks_run} checks run"
            + (f", {len(self.ignored)} ignored: {', '.join(self.ignored)}" if self.ignored else "")
            + ")"
        )
        if not self.results:
            return f"{head}\nAll checks passed. ✓"

        lines = [head]
        for severity, label in (("error", "ERRORS"), ("warning", "WARNINGS"), ("info", "INFO")):
            found = self.by_severity(severity)  # type: ignore[arg-type]
            if not found:
                continue
            lines.append(f"\n{label}")
            lines.extend(f"  {r}" for r in found)
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.summary()

    def __repr__(self) -> str:
        return self.summary()


# --- Shared, precomputed view of the bundle ------------------------------------------
@dataclass
class _Ctx:
    """Everything the individual checks need, resolved once."""

    container: CuratedContainer
    heavy_cell_budget: int

    @property
    def df(self) -> pd.DataFrame:
        return self.container.dataset

    @property
    def dataset_metadata(self) -> DatasetMetadata:
        return self.container.dataset_metadata

    @property
    def task(self) -> PredictiveMLTaskMetadata:
        return self.container.task_metadata

    @property
    def splits_metadata(self) -> PredictiveMLSplitsMetadata:
        return self.container.experiment_metadata

    @property
    def n_rows(self) -> int:
        return len(self.df)

    @property
    def target(self) -> str:
        return self.task.target_column_name

    @property
    def regime(self) -> str:
        return self.task.split_regime

    @property
    def heavy_allowed(self) -> bool:
        return self.df.size <= self.heavy_cell_budget

    @property
    def flat_splits(self) -> list[tuple[int, int, np.ndarray, np.ndarray]]:
        """``[(repeat, fold, train_idx, test_idx), ...]`` with in-bounds integer arrays.

        Out-of-bounds indices are dropped here (reported by
        :func:`_check_splits_index_bounds`) so downstream checks cannot raise.
        """
        if self._flat is None:

            def in_bounds(indices: list[int]) -> np.ndarray:
                array = np.asarray(indices, dtype=np.int64)
                return array[(array >= 0) & (array < self.n_rows)]

            self._flat = [
                (repeat_i, fold_i, in_bounds(train_idx), in_bounds(test_idx))
                for repeat_i, folds in self.splits_metadata.splits.items()
                for fold_i, (train_idx, test_idx) in folds.items()
            ]
        return self._flat

    _flat: list[tuple[int, int, np.ndarray, np.ndarray]] | None = None

    def columns_of(self, value: str | list[str] | None) -> list[str]:
        """Normalize a metadata field that may be a name, a list of names, or None."""
        return as_column_list(value)

    def has_column(self, name: str) -> bool:
        return name in self.df.columns

    def numeric_time(self, column: str) -> np.ndarray | None:
        """Return ``column`` as a sortable float array, or None if it is not time-like."""
        series = self.df[column]
        if pd.api.types.is_datetime64_any_dtype(series):
            return series.astype("int64").to_numpy(dtype="float64")
        if isinstance(series.dtype, pd.PeriodDtype):
            return series.astype("int64").to_numpy(dtype="float64")
        if pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series):
            return series.to_numpy(dtype="float64", na_value=np.nan)
        return None

    def group_codes(self) -> np.ndarray | None:
        """Return one integer code per row identifying its group, or None if ungrouped."""
        group_columns = self.columns_of(self.task.group_on)
        if not group_columns or any(not self.has_column(c) for c in group_columns):
            return None
        frame = self.df[group_columns].astype("string").fillna("<NA>")
        joined = frame.iloc[:, 0] if len(group_columns) == 1 else frame.agg("\x1f".join, axis=1)
        return pd.factorize(joined, use_na_sentinel=False)[0]


_Check = "Callable[[_Ctx], Iterable[CheckResult]]"
_CHECKS: list[Callable[[_Ctx], Iterable[CheckResult]]] = []


def _check(func: Callable[[_Ctx], Iterable[CheckResult]]) -> Callable[[_Ctx], Iterable[CheckResult]]:
    """Register a check function so :func:`run_bundle_checks` runs it."""
    _CHECKS.append(func)
    return func


# --- 1. The DataFrame itself ---------------------------------------------------------
@_check
def _check_dataset_frame(ctx: _Ctx) -> Iterator[CheckResult]:
    """Frame-level invariants: shape, index, column names, dtypes."""
    df = ctx.df
    if df is None:
        yield CheckResult("dataset_missing", "error", "Container has no `dataset` loaded.")
        return
    if ctx.n_rows == 0 or df.shape[1] == 0:
        yield CheckResult("dataset_empty", "error", f"Dataset is empty (shape={df.shape}).")
        return

    expected_index = pd.RangeIndex(start=0, stop=ctx.n_rows)
    if not df.index.equals(expected_index):
        yield CheckResult(
            "dataset_index_range",
            "error",
            f"Dataset index is not a RangeIndex(0, {ctx.n_rows}) — got {df.index.__class__.__name__} "
            f"[{df.index[0]!r} … {df.index[-1]!r}].",
            hint="Split indices are positional. Call `df = df.reset_index(drop=True)` *before* building the "
            "splits, otherwise label-based indices silently point at the wrong rows after save/load.",
        )

    non_str = [c for c in df.columns if not isinstance(c, str)]
    if non_str:
        yield CheckResult(
            "dataset_column_names",
            "error",
            f"{len(non_str)} column name(s) are not strings: {non_str[:5]}.",
            hint="Parquet requires string column names; cast with `df.columns = df.columns.astype(str)`.",
        )
    duplicated_names = df.columns[df.columns.duplicated()].tolist()
    if duplicated_names:
        yield CheckResult(
            "dataset_duplicate_column_names",
            "error",
            f"Duplicate column names: {duplicated_names[:5]}.",
        )

    object_columns = df.select_dtypes(include=["object"]).columns.tolist()
    if object_columns:
        yield CheckResult(
            "dataset_object_dtype",
            "error",
            f"{len(object_columns)} column(s) have `object` dtype: {object_columns[:5]}.",
            hint="Cast to `category` (fixed, finite value set), `string` (free text), a numeric dtype, or datetime. "
            "TabArena rejects object columns.",
        )


@_check
def _check_dataset_columns_quality(ctx: _Ctx) -> Iterator[CheckResult]:
    """Per-column quality signals: constant, identifier-like, all-missing, unused categories."""
    df = ctx.df
    if df is None or ctx.n_rows == 0:
        return

    constant, all_missing, id_like, unused_categories, sentinel_hits, string_missing = [], [], [], [], [], []
    for column in df.columns:
        series = df[column]
        n_unique = series.nunique(dropna=True)
        if series.isna().all():
            all_missing.append(column)
        elif n_unique <= 1:
            constant.append(column)

        is_labelish = isinstance(series.dtype, pd.CategoricalDtype) or series.dtype == "string"
        if column != ctx.target and is_labelish and n_unique == ctx.n_rows and ctx.n_rows > 1:
            id_like.append(column)

        if isinstance(series.dtype, pd.CategoricalDtype):
            unused = set(series.dtype.categories) - set(series.dropna().unique())
            if unused:
                unused_categories.append((column, len(unused)))
        if is_labelish:
            hits = {str(v) for v in series.dropna().unique()[:1000] if str(v).strip().lower() in MISSING_VALUE_STRINGS}
            if hits:
                string_missing.append((column, sorted(hits)))

        if pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series) and n_unique > 2:
            value_counts = series.value_counts(dropna=True)
            if len(value_counts):
                most_common = float(value_counts.index[0])
                share = value_counts.iloc[0] / ctx.n_rows
                if most_common in MISSING_VALUE_SENTINELS and share >= 0.01:
                    sentinel_hits.append((column, most_common, share))

    if all_missing:
        yield CheckResult(
            "dataset_all_missing_column",
            "warning",
            f"{len(all_missing)} column(s) are entirely missing: {all_missing[:5]}.",
            hint="Drop them — they carry no signal.",
        )
    if constant:
        yield CheckResult(
            "dataset_constant_column",
            "warning",
            f"{len(constant)} constant column(s) (1 distinct non-null value): {constant[:5]}.",
            hint="Drop them unless the constant is meaningful for the task.",
        )
    if id_like:
        yield CheckResult(
            "dataset_identifier_column",
            "warning",
            f"{len(id_like)} column(s) have one distinct value per row: {id_like[:5]}.",
            hint="Uninformative sample identifiers should be dropped (curation guidelines); keep and process only "
            "informative ones (e.g. a time index).",
        )
    if unused_categories:
        formatted = ", ".join(f"{c} (+{n})" for c, n in unused_categories[:5])
        yield CheckResult(
            "dataset_unused_categories",
            "warning",
            f"{len(unused_categories)} category column(s) declare categories that never occur: {formatted}.",
            hint="Call `df[col] = df[col].cat.remove_unused_categories()`; unused levels distort class counts and "
            "one-hot widths downstream.",
        )
    if string_missing:
        formatted = ", ".join(f"{c}={vals}" for c, vals in string_missing[:5])
        yield CheckResult(
            "dataset_missing_value_label",
            "warning",  # narrow token list keeps this high-signal (see MISSING_VALUE_STRINGS)
            f"{len(string_missing)} label column(s) contain missing-value-looking levels: {formatted}.",
            hint="Convert proxy missing values to explicit `pd.NA` (curation guidelines).",
        )
    if sentinel_hits:
        formatted = ", ".join(f"{c}={value:g} ({share:.1%})" for c, value, share in sentinel_hits[:5])
        yield CheckResult(
            "dataset_missing_value_sentinel",
            "warning",
            f"{len(sentinel_hits)} numeric column(s) are dominated by a sentinel-looking value: {formatted}.",
            hint="If it encodes 'missing', replace it with `np.nan` (curation guidelines); if it is a real value, "
            "ignore this finding.",
        )


@_check
def _check_dataset_duplicates(ctx: _Ctx) -> Iterator[CheckResult]:
    """Duplicate columns and contradictory duplicate rows (same features, different target)."""
    df = ctx.df
    if df is None or ctx.n_rows == 0 or not ctx.has_column(ctx.target):
        return
    if not ctx.heavy_allowed:
        yield CheckResult(
            "dataset_duplicates_skipped",
            "info",
            f"Skipped duplicate-column/row checks: {df.size:,} cells exceed the budget of {ctx.heavy_cell_budget:,}.",
            hint="Raise `heavy_cell_budget=` to force them, or rely on `dataset_checks.run_all_checks`.",
        )
        return

    hashes: dict[int, str] = {}
    duplicate_pairs: list[tuple[str, str]] = []
    for column in df.columns:
        digest = int(pd.util.hash_pandas_object(df[column].astype("string"), index=False).sum())
        first = hashes.get(digest)
        if first is not None and df[first].astype("string").equals(df[column].astype("string")):
            duplicate_pairs.append((first, column))
        else:
            hashes.setdefault(digest, column)

    target_duplicates = [(a, b) for a, b in duplicate_pairs if ctx.target in (a, b)]
    other_duplicates = [(a, b) for a, b in duplicate_pairs if ctx.target not in (a, b)]
    if target_duplicates:
        leaking = [b if a == ctx.target else a for a, b in target_duplicates]
        yield CheckResult(
            "dataset_feature_equals_target",
            "error",
            f"Feature column(s) are identical to the target {ctx.target!r}: {leaking}.",
            hint="This is target leakage — drop the column(s).",
        )
    if other_duplicates:
        yield CheckResult(
            "dataset_duplicate_columns",
            "warning",
            f"{len(other_duplicates)} duplicated column pair(s): {other_duplicates[:5]}.",
            hint="Keep one of each pair.",
        )

    feature_columns = [c for c in df.columns if c != ctx.target]
    if feature_columns:
        duplicated_features = df.duplicated(subset=feature_columns, keep=False)
        n_dup_feature_rows = int(duplicated_features.sum())
        if n_dup_feature_rows:
            candidates = df.loc[duplicated_features, [*feature_columns, ctx.target]]
            n_exact = int(candidates.duplicated(keep="first").sum())
            n_feature_only = int(candidates.duplicated(subset=feature_columns, keep="first").sum())
            n_conflicting = n_feature_only - n_exact
            if n_exact:
                share = n_exact / ctx.n_rows
                yield CheckResult(
                    "dataset_duplicate_rows",
                    "warning" if share >= DUPLICATE_ROW_WARN_SHARE else "info",
                    f"{n_exact:,} exact duplicate row(s) ({share:.1%} of the data).",
                    hint="Duplicates spread across train and test inflate scores — deduplicate unless the "
                    "repetition is meaningful.",
                )
            if n_conflicting:
                share = n_conflicting / ctx.n_rows
                yield CheckResult(
                    "dataset_conflicting_duplicate_rows",
                    "warning" if share >= DUPLICATE_ROW_WARN_SHARE else "info",
                    f"{n_conflicting:,} row(s) ({share:.1%}) share all features with another row but carry a "
                    "different target.",
                    hint="Either the rows differ in a dropped column, or the label is noisy — this caps the "
                    "achievable score.",
                )


@_check
def _check_row_order(ctx: _Ctx) -> Iterator[CheckResult]:
    """Row order must not carry signal for IID/grouped data (guidelines: always shuffle)."""
    if ctx.df is None or ctx.n_rows < 50 or not ctx.has_column(ctx.target):
        return
    if ctx.regime == "temporal_non_iid":
        return

    target = ctx.df[ctx.target]
    if isinstance(target.dtype, pd.CategoricalDtype):
        values = target.cat.codes.to_numpy(dtype="float64")
    elif pd.api.types.is_numeric_dtype(target):
        values = target.to_numpy(dtype="float64", na_value=np.nan)
    else:
        values = pd.factorize(target)[0].astype("float64")

    positions = pd.Series(np.arange(ctx.n_rows, dtype="float64"))
    rho = pd.Series(values).corr(positions, method="spearman")
    if rho is not None and not math.isnan(rho) and abs(rho) > 0.15:
        yield CheckResult(
            "dataset_row_order_leaks_target",
            "warning",
            f"Target correlates with row position (Spearman rho={rho:+.2f}); the data looks ordered, not shuffled.",
            hint="Shuffle IID and grouped data before creating splits (curation guidelines) — ordered rows let "
            "models exploit position and make the recommended splits non-representative.",
        )


# --- 2. Task metadata against the DataFrame -----------------------------------------
@_check
def _check_task_columns_exist(ctx: _Ctx) -> Iterator[CheckResult]:
    """Every column the task metadata names must exist in the dataset."""
    if ctx.df is None:
        return
    task = ctx.task
    referenced = {
        "target_column_name": ctx.columns_of(task.target_column_name),
        "stratify_on": ctx.columns_of(task.stratify_on),
        "time_on": ctx.columns_of(task.time_on),
        "group_on": ctx.columns_of(task.group_on),
        "group_time_on": ctx.columns_of(task.group_time_on),
    }
    for field_name, columns in referenced.items():
        missing = [c for c in columns if not ctx.has_column(c)]
        if missing:
            yield CheckResult(
                f"task_{field_name}_missing_column",
                "error",
                f"`{field_name}` references column(s) not in the dataset: {missing}.",
                hint=f"Available columns (first 10): {list(ctx.df.columns[:10])}",
            )


@_check
def _check_target(ctx: _Ctx) -> Iterator[CheckResult]:
    """Target dtype, class count, and missing values must match ``problem_type``."""
    if ctx.df is None or not ctx.has_column(ctx.target):
        return
    task = ctx.task
    target = ctx.df[ctx.target]

    n_missing = int(target.isna().sum())
    if n_missing:
        yield CheckResult(
            "task_target_missing_values",
            "error",
            f"Target {ctx.target!r} has {n_missing:,} missing value(s) ({n_missing / ctx.n_rows:.1%}).",
            hint="Drop those rows — a sample without a label cannot be trained on or scored.",
        )

    n_classes = int(target.nunique(dropna=True))
    if task.is_classification:
        if not isinstance(target.dtype, pd.CategoricalDtype):
            yield CheckResult(
                "task_target_dtype",
                "error",
                f"Classification target {ctx.target!r} has dtype {target.dtype} — expected `category`.",
                hint="`df[target] = df[target].astype('category')`; TabArena rejects non-categorical "
                "classification targets.",
            )
        if task.problem_type == "binary_classification" and n_classes != 2:
            yield CheckResult(
                "task_target_class_count",
                "error",
                f"`problem_type='binary_classification'` but the target has {n_classes} distinct classes.",
            )
        if task.problem_type == "multiclass_classification" and n_classes < 3:
            yield CheckResult(
                "task_target_class_count",
                "error",
                f"`problem_type='multiclass_classification'` but the target has only {n_classes} distinct classes.",
                hint="Use `binary_classification` for a 2-class target.",
            )

        counts = target.value_counts(dropna=True)
        n_splits_max = max((len(folds) for folds in ctx.splits_metadata.splits.values()), default=1)
        rare = counts[counts < max(5, n_splits_max)]
        if len(rare):
            formatted = ", ".join(f"{k}={int(v)}" for k, v in list(rare.items())[:5])
            yield CheckResult(
                "task_target_rare_class",
                "warning",
                f"{len(rare)} class(es) have fewer samples than folds/5: {formatted}.",
                hint="Rare classes break stratification and can leave a fold whose test set holds a class the "
                "train set never saw — merge or drop them.",
            )
    elif not pd.api.types.is_numeric_dtype(target) or pd.api.types.is_bool_dtype(target):
        yield CheckResult(
            "task_target_dtype",
            "error",
            f"Regression target {ctx.target!r} has dtype {target.dtype} — expected a numeric dtype.",
        )
    elif n_classes <= 10:
        yield CheckResult(
            "task_target_low_cardinality",
            "warning",
            f"Regression target {ctx.target!r} has only {n_classes} distinct values.",
            hint="Confirm this is really a regression task and not a (ordinal) classification one.",
        )


@_check
def _check_metric(ctx: _Ctx) -> Iterator[CheckResult]:
    """``objective_metric_name`` must be set and fit the problem type."""
    task = ctx.task
    metric = (task.objective_metric_name or "").strip()
    if not metric:
        yield CheckResult(
            "task_metric_empty",
            "error",
            "`objective_metric_name` is empty.",
            hint="Set the metric of the original task, or the default for the problem type "
            f"({TABARENA_DEFAULT_METRICS[task.problem_type]}).",
        )
        return

    known = KNOWN_METRICS[task.problem_type]
    if metric.lower() in known:
        return
    other_problem_types = [p for p, metrics in KNOWN_METRICS.items() if metric.lower() in metrics]
    if other_problem_types:
        yield CheckResult(
            "task_metric_problem_type_mismatch",
            "error",
            f"Metric {metric!r} belongs to {other_problem_types} but `problem_type` is {task.problem_type!r}.",
        )
        return
    yield CheckResult(
        "task_metric_unknown",
        "info",
        f"Metric {metric!r} is not one of the standard names for {task.problem_type}.",
        hint="Fine for a custom competition metric, but it has to be registered on the consumer side — TabArena "
        f"otherwise silently falls back to {TABARENA_DEFAULT_METRICS[task.problem_type]!r}.",
    )


@_check
def _check_stratify_column(ctx: _Ctx) -> Iterator[CheckResult]:
    """``stratify_on`` must name a discrete, complete column of a classification-style task."""
    task = ctx.task
    columns = ctx.columns_of(task.stratify_on)
    if not columns or ctx.df is None:
        return

    if not task.is_classification:
        yield CheckResult(
            "task_stratify_on_regression",
            "warning",
            f"`stratify_on={task.stratify_on!r}` is set but `problem_type` is {task.problem_type!r}.",
            hint="Stratification needs a discrete column. For regression, either drop `stratify_on` or confirm it "
            "names a discrete feature (not the target) that the splits should be balanced on.",
        )

    for column in columns:
        if not ctx.has_column(column):
            continue
        series = ctx.df[column]
        n_unique = int(series.nunique(dropna=True))
        is_discrete = isinstance(series.dtype, pd.CategoricalDtype) or pd.api.types.is_bool_dtype(series)
        if not is_discrete and (not pd.api.types.is_integer_dtype(series) or n_unique > 50):
            yield CheckResult(
                "task_stratify_dtype",
                "error",
                f"`stratify_on={column!r}` has dtype {series.dtype} with {n_unique} distinct values — "
                "not a discrete column.",
                hint="Stratified splitters need a categorical / low-cardinality integer column.",
            )
            continue
        if int(series.isna().sum()):
            yield CheckResult(
                "task_stratify_missing_values",
                "error",
                f"`stratify_on={column!r}` has {int(series.isna().sum()):,} missing value(s).",
                hint="Stratified splitters cannot handle NaN in the stratification column.",
            )
        if n_unique > 50:
            yield CheckResult(
                "task_stratify_high_cardinality",
                "warning",
                f"`stratify_on={column!r}` has {n_unique} distinct values.",
                hint="High-cardinality stratification produces near-deterministic splits; usually you want the "
                "target column.",
            )


@_check
def _check_time_column(ctx: _Ctx) -> Iterator[CheckResult]:
    """``time_on`` / ``group_time_on`` must be sortable, complete, and (for splits) sorted."""
    task = ctx.task
    for field_name in ("time_on", "group_time_on"):
        column = getattr(task, field_name)
        if column is None or not ctx.has_column(column):
            continue
        series = ctx.df[column]
        values = ctx.numeric_time(column)
        if values is None:
            yield CheckResult(
                f"task_{field_name}_dtype",
                "error",
                f"`{field_name}={column!r}` has dtype {series.dtype} — expected datetime, period, or numeric.",
                hint="Convert dates to datetime (`YYYY-MM-DD`) or reconstruct a numeric time index; consumers "
                "assert this dtype when deriving validation splits.",
            )
            continue
        n_missing = int(np.isnan(values).sum())
        if n_missing:
            yield CheckResult(
                f"task_{field_name}_missing_values",
                "error",
                f"`{field_name}={column!r}` has {n_missing:,} missing value(s).",
                hint="A row without a time stamp cannot be placed in a temporal split; drop or impute it.",
            )
        n_unique = int(series.nunique(dropna=True))
        if n_unique < 2:
            yield CheckResult(
                f"task_{field_name}_constant",
                "error",
                f"`{field_name}={column!r}` has {n_unique} distinct value(s).",
            )
        elif n_unique < 10:
            yield CheckResult(
                f"task_{field_name}_few_unique",
                "warning",
                f"`{field_name}={column!r}` has only {n_unique} distinct time points.",
                hint="Consumers derive inner validation folds by cutting the time axis into intervals; too few "
                "time points makes that degenerate.",
            )

    if task.time_on is not None and ctx.has_column(task.time_on):
        values = ctx.numeric_time(task.time_on)
        if values is not None and not np.all(values[:-1] <= values[1:]):
            yield CheckResult(
                "task_time_on_not_sorted",
                "warning",
                f"Dataset is not sorted ascending by `time_on={task.time_on!r}`.",
                hint="Temporal data should be sorted chronologically (curation guidelines): "
                "`df = df.sort_values(time_on).reset_index(drop=True)` before building the splits. Expected only "
                "when rows were subsampled per split afterwards (`curation_recommendations.subsample_temporal`) — "
                "the per-fold leakage check is what actually guards the protocol.",
            )


@_check
def _check_group_columns(ctx: _Ctx) -> Iterator[CheckResult]:
    """Group structure sanity, including the ``group_labels='per_group'`` contract."""
    task = ctx.task
    group_columns = ctx.columns_of(task.group_on)
    if not group_columns or ctx.df is None:
        return
    if any(not ctx.has_column(c) for c in group_columns):
        return

    codes = ctx.group_codes()
    if codes is None:
        return
    n_groups = int(codes.max()) + 1 if len(codes) else 0
    if n_groups == ctx.n_rows:
        yield CheckResult(
            "task_group_on_unique_per_row",
            "error",
            f"`group_on={task.group_on!r}` has one group per row ({n_groups} groups).",
            hint="A grouped split needs repeated group values; this column is a sample identifier.",
        )
    elif n_groups < 10:
        yield CheckResult(
            "task_group_count_low",
            "warning",
            f"`group_on={task.group_on!r}` yields only {n_groups} groups.",
            hint="Few groups make grouped CV coarse and high-variance.",
        )

    n_missing = int(ctx.df[group_columns].isna().any(axis=1).sum())
    if n_missing:
        yield CheckResult(
            "task_group_on_missing_values",
            "warning",
            f"`group_on={task.group_on!r}` has {n_missing:,} row(s) with a missing group value.",
            hint="Those rows are lumped into one artificial group; check whether they should be dropped.",
        )

    if task.group_labels == "per_group" and ctx.has_column(ctx.target):
        target_codes = pd.factorize(ctx.df[ctx.target].astype("string"), use_na_sentinel=False)[0]
        per_group_unique = pd.Series(target_codes).groupby(codes, observed=True).nunique()
        n_multi = int((per_group_unique > 1).sum())
        if n_multi:
            yield CheckResult(
                "task_group_labels_per_group_violated",
                "error",
                f"`group_labels='per_group'` but {n_multi:,} of {n_groups:,} groups carry more than one target value.",
                hint="Either the task has one label per sample (`group_labels='per_sample'`) or the group column "
                "is wrong.",
            )


# --- 3. Splits against the DataFrame -------------------------------------------------
@_check
def _check_splits_index_bounds(ctx: _Ctx) -> Iterator[CheckResult]:
    """Split indices must be positional indices into the dataset."""
    if ctx.df is None:
        return
    offenders: list[str] = []
    for repeat_i, folds in ctx.splits_metadata.splits.items():
        for fold_i, (train_idx, test_idx) in folds.items():
            for label, indices in (("train", train_idx), ("test", test_idx)):
                array = np.asarray(indices, dtype=np.int64)
                if array.size and (array.min() < 0 or array.max() >= ctx.n_rows):
                    offenders.append(f"r{repeat_i}f{fold_i}/{label} in [{array.min()}, {array.max()}]")
    if offenders:
        yield CheckResult(
            "splits_index_out_of_bounds",
            "error",
            f"{len(offenders)} split(s) index outside [0, {ctx.n_rows - 1}]: {offenders[:5]}.",
            hint="Split indices are positional. Build them from a `reset_index(drop=True)` frame, and never after "
            "filtering rows.",
        )


@_check
def _check_splits_disjointness(ctx: _Ctx) -> Iterator[CheckResult]:
    """Within a fold: train and test disjoint, no repeated indices."""
    overlapping: list[str] = []
    repeated: list[str] = []
    for repeat_i, fold_i, train, test in ctx.flat_splits:
        if np.intersect1d(train, test, assume_unique=False).size:
            overlapping.append(f"r{repeat_i}f{fold_i}")
        for label, array in (("train", train), ("test", test)):
            if np.unique(array).size != array.size:
                repeated.append(f"r{repeat_i}f{fold_i}/{label}")
    if overlapping:
        yield CheckResult(
            "splits_train_test_overlap",
            "error",
            f"{len(overlapping)} fold(s) share rows between train and test: {overlapping[:5]}.",
        )
    if repeated:
        yield CheckResult(
            "splits_duplicate_indices",
            "error",
            f"{len(repeated)} split index list(s) contain repeated indices: {repeated[:5]}.",
        )


@_check
def _check_splits_coverage(ctx: _Ctx) -> Iterator[CheckResult]:
    """Which rows the splits actually use, and how often each row is tested."""
    if ctx.df is None or not ctx.flat_splits:
        return
    used = np.zeros(ctx.n_rows, dtype=bool)
    tested = np.zeros(ctx.n_rows, dtype=bool)
    for _repeat_i, _fold_i, train, test in ctx.flat_splits:
        used[train] = True
        used[test] = True
        tested[test] = True

    n_unused = int((~used).sum())
    if n_unused:
        share = n_unused / ctx.n_rows
        severity: Severity = "warning" if ctx.regime == "temporal_non_iid" else "error"
        yield CheckResult(
            "splits_rows_unused",
            severity,
            f"{n_unused:,} row(s) ({share:.1%}) appear in no train and no test set.",
            hint="Expected for temporal splits (rows inside a planning gap or before the earliest train cut); "
            "for IID/grouped splits it means the splits do not cover the data — consider dropping the unused "
            "rows so the shipped frame matches what is evaluated.",
        )

    # Only k-fold-shaped splits (>1 fold per repeat) promise to test every row; a single
    # train/test split per repeat deliberately leaves most rows in train only.
    n_folds_per_repeat = {len(folds) for folds in ctx.splits_metadata.splits.values()}
    if ctx.regime != "temporal_non_iid" and n_folds_per_repeat != {1}:
        n_never_tested = int((~tested).sum())
        if n_never_tested:
            yield CheckResult(
                "splits_rows_never_tested",
                "warning",
                f"{n_never_tested:,} row(s) ({n_never_tested / ctx.n_rows:.1%}) are never in a test set, although "
                "the splits look like cross-validation.",
                hint="In k-fold CV every row is tested exactly once per repeat; check the split construction.",
            )


@_check
def _check_splits_class_coverage(ctx: _Ctx) -> Iterator[CheckResult]:
    """Every fold's train set must cover the classes of its test set."""
    task = ctx.task
    if not task.is_classification or ctx.df is None or not ctx.has_column(ctx.target):
        return
    target = ctx.df[ctx.target]
    codes = (
        target.cat.codes.to_numpy()
        if isinstance(target.dtype, pd.CategoricalDtype)
        else pd.factorize(target.astype("string"), use_na_sentinel=True)[0]
    )
    n_classes_total = len(np.unique(codes[codes >= 0]))

    unseen: list[str] = []
    changed_problem_type: list[str] = []
    for repeat_i, fold_i, train, test in ctx.flat_splits:
        train_classes = np.unique(codes[train])
        test_classes = np.unique(codes[test])
        train_classes = train_classes[train_classes >= 0]
        test_classes = test_classes[test_classes >= 0]
        if np.setdiff1d(test_classes, train_classes).size:
            unseen.append(f"r{repeat_i}f{fold_i}")
        n_fold_classes = max(len(train_classes), len(test_classes))
        if (n_fold_classes <= 2) != (n_classes_total <= 2):
            changed_problem_type.append(f"r{repeat_i}f{fold_i} ({n_fold_classes} of {n_classes_total})")

    if unseen:
        yield CheckResult(
            "splits_test_class_unseen_in_train",
            "error",
            f"{len(unseen)} fold(s) have a test class that never occurs in train: {unseen[:5]}.",
            hint="Stratify the splits or merge/drop rare classes — a model cannot predict a class it never saw, "
            "and probabilistic metrics break on the missing column.",
        )
    if changed_problem_type:
        yield CheckResult(
            "splits_fold_problem_type_differs",
            "error",
            f"{len(changed_problem_type)} fold(s) flip binary/multiclass relative to the full dataset: "
            f"{changed_problem_type[:5]}.",
            hint="TabArena asserts that every split has the same problem type as the task.",
        )


@_check
def _check_splits_temporal(ctx: _Ctx) -> Iterator[CheckResult]:
    """Temporal splits: no future leakage, and folds ordered newest-first."""
    task = ctx.task
    if task.time_on is None or ctx.df is None or not ctx.has_column(task.time_on):
        return
    values = ctx.numeric_time(task.time_on)
    if values is None:
        return

    leaking: list[str] = []
    test_end: list[tuple[str, float]] = []
    for repeat_i, fold_i, train, test in ctx.flat_splits:
        if not train.size or not test.size:
            continue
        train_max = np.nanmax(values[train])
        test_min = np.nanmin(values[test])
        if not train_max < test_min:
            leaking.append(f"r{repeat_i}f{fold_i}")
        test_end.append((f"r{repeat_i}f{fold_i}", float(np.nanmax(values[test]))))

    if leaking:
        yield CheckResult(
            "splits_temporal_leakage",
            "error",
            f"{len(leaking)} fold(s) train on rows that are not strictly older than their test rows: {leaking[:5]}.",
            hint="A temporal split must satisfy max(train time) < min(test time); otherwise the benchmark "
            "measures temporal leakage instead of generalization.",
        )

    if len(test_end) > 1:
        ends = [value for _label, value in test_end]
        if not all(a >= b for a, b in zip(ends, ends[1:], strict=False)):
            newest = max(test_end, key=lambda item: item[1])[0]
            yield CheckResult(
                "splits_temporal_order",
                "warning",
                f"Temporal folds are not ordered by descending test time — the newest test window is {newest}, "
                f"not the first split ({test_end[0][0]}).",
                hint="Convention: the first split holds the most recent test time point (most training data, "
                "most representative); order the rest by descending test time.",
            )

    n_folds_per_repeat = {len(folds) for folds in ctx.splits_metadata.splits.values()}
    if n_folds_per_repeat and n_folds_per_repeat != {1}:
        yield CheckResult(
            "splits_temporal_layout",
            "info",
            f"Temporal splits use {sorted(n_folds_per_repeat)} fold(s) per repeat.",
            hint="Shipped temporal tasks put each time window in its own repeat with a single fold "
            "(`splits[window] = {0: (train_idx, test_idx)}`).",
        )


@_check
def _check_splits_groups(ctx: _Ctx) -> Iterator[CheckResult]:
    """Grouped splits: no group may appear in both train and test of a fold."""
    if ctx.task.group_on is None:
        return
    codes = ctx.group_codes()
    if codes is None:
        return
    leaking: list[str] = []
    for repeat_i, fold_i, train, test in ctx.flat_splits:
        if np.intersect1d(np.unique(codes[train]), np.unique(codes[test]), assume_unique=True).size:
            leaking.append(f"r{repeat_i}f{fold_i}")
    if leaking:
        yield CheckResult(
            "splits_group_leakage",
            "error",
            f"{len(leaking)} fold(s) share a `group_on` value between train and test: {leaking[:5]}.",
            hint="A grouped split must keep every group entirely in one side of the split.",
        )


@_check
def _check_splits_dimensions(ctx: _Ctx) -> Iterator[CheckResult]:
    """Compare the split dimensions against the recommended protocol."""
    from data_foundry.curation_recommendations import get_recommended_splits_dimensions

    task = ctx.task
    if ctx.df is None or task.time_on is not None or not ctx.flat_splits:
        return
    if isinstance(task.group_on, list):
        # The recommendation helper only understands a single group column.
        return
    n_repeats = len(ctx.splits_metadata.splits)
    folds_per_repeat = {len(folds) for folds in ctx.splits_metadata.splits.values()}
    if len(folds_per_repeat) != 1:
        return
    n_folds = next(iter(folds_per_repeat))

    try:
        recommended = get_recommended_splits_dimensions(
            dataset=ctx.df,
            group_on=task.group_on if isinstance(task.group_on, str) else None,
            time_on=None,
            group_labels=task.group_labels,
        )
    except (ValueError, KeyError):
        return
    rec_repeats, rec_folds, rec_test_size = recommended
    if (n_repeats, n_folds) != (rec_repeats, rec_folds):
        yield CheckResult(
            "splits_dimensions_off_protocol",
            "warning",
            f"Splits are {n_repeats}x{n_folds} but the recommendation for this size is {rec_repeats}x{rec_folds}"
            + (f" (test_size={rec_test_size:,})" if rec_test_size else "")
            + ".",
            hint="Deviating is allowed when the task demands it — record why in `splits_comment`.",
        )


# --- 4. Dataset metadata coherence ---------------------------------------------------
@_check
def _check_temporal_metadata(ctx: _Ctx) -> Iterator[CheckResult]:
    """A temporal task must declare its prediction horizon, and vice versa."""
    task = ctx.task
    splits_metadata = ctx.splits_metadata
    if task.time_on is not None and splits_metadata.time_horizon is None:
        yield CheckResult(
            "meta_time_horizon_missing",
            "error",
            f"`time_on={task.time_on!r}` makes this a temporal task, but `time_horizon` is not set.",
            hint="Record the prediction horizon you chose for the test windows (e.g. `time_horizon=6, "
            "time_horizon_unit='weeks'`) — it is part of the task definition, not an optional note.",
        )
    if task.time_on is None and splits_metadata.time_horizon is not None:
        yield CheckResult(
            "meta_time_horizon_without_time_on",
            "error",
            f"`time_horizon={splits_metadata.time_horizon!r}` is set but the task has no `time_on` column.",
        )


@_check
def _check_time_horizon_plausible(ctx: _Ctx) -> Iterator[CheckResult]:
    """Cross-check the declared horizon against the observed test window."""
    task, splits_metadata = ctx.task, ctx.splits_metadata
    horizon, unit = splits_metadata.time_horizon, splits_metadata.time_horizon_unit
    if horizon is None or unit is None or task.time_on is None or ctx.df is None:
        return
    if not ctx.has_column(task.time_on) or not ctx.flat_splits:
        return
    try:
        horizon_value = float(horizon)
    except (TypeError, ValueError):
        return

    series = ctx.df[task.time_on]
    _repeat_i, _fold_i, _train, test = ctx.flat_splits[0]
    if not test.size:
        return
    test_values = series.iloc[test]

    if unit == "steps":
        observed = float(test_values.nunique())
        observed_label = f"{observed:,.0f} distinct time points"
    elif pd.api.types.is_datetime64_any_dtype(series):
        days_per_unit = {"days": 1.0, "weeks": 7.0, "months": 30.44, "years": 365.25}
        if unit not in days_per_unit:
            return
        observed = (test_values.max() - test_values.min()).total_seconds() / 86400 + 1
        horizon_value *= days_per_unit[unit]
        observed_label = f"{observed:,.0f} days"
        unit = "days"
    else:
        yield CheckResult(
            "meta_time_horizon_unit",
            "info",
            f"`time_horizon_unit={splits_metadata.time_horizon_unit!r}` implies calendar time, but "
            f"`time_on={task.time_on!r}` has dtype {series.dtype}, so the horizon cannot be cross-checked.",
            hint="Fine when the numeric values themselves are calendar units (e.g. a year column); otherwise use "
            "`time_horizon_unit='steps'` for a plain numeric time index.",
        )
        return

    if observed and not 0.5 * horizon_value <= observed <= 2.0 * horizon_value:
        yield CheckResult(
            "meta_time_horizon_mismatch",
            "warning",
            f"Declared horizon is {horizon} {splits_metadata.time_horizon_unit} (~{horizon_value:,.0f} {unit}) but "
            f"the first test window spans {observed_label}.",
            hint="Either the horizon does not describe the test windows, or the windows were built differently "
            "than documented.",
        )


@_check
def _check_data_tags(ctx: _Ctx) -> Iterator[CheckResult]:
    """``data_tags`` must agree with the split regime the task actually declares."""
    tags = set(ctx.dataset_metadata.data_tags)
    regime = ctx.regime
    expected = {
        "iid": "IID",
        "temporal_non_iid": "Temporal",
        "grouped_non_iid": "Grouped",
    }[regime]
    non_iid_tags = {"Temporal", "Grouped", "GroupedTemporal"}

    if regime == "iid":
        if "IID" not in tags and "ForcedIIDFromTemporal" not in tags:
            yield CheckResult(
                "meta_tags_missing_iid",
                "warning",
                f"Task declares no `time_on`/`group_on` (IID split) but `data_tags={sorted(tags)}` has no `IID` tag.",
            )
        wrong = tags & (non_iid_tags | {"Non-IID"})
        if wrong:
            yield CheckResult(
                "meta_tags_contradict_regime",
                "warning",
                f"`data_tags` claim {sorted(wrong)} but the task defines an IID split.",
                hint="Either set `time_on`/`group_on`, or fix the tags (`ForcedIIDFromTemporal` is the tag for "
                "temporal data shipped without a usable time index).",
            )
    else:
        if expected not in tags and "GroupedTemporal" not in tags:
            yield CheckResult(
                "meta_tags_missing_regime",
                "warning",
                f"Task defines a {regime.replace('_non_iid', '')} split but `data_tags={sorted(tags)}` lacks "
                f"`{expected}`.",
            )
        if "Non-IID" not in tags:
            yield CheckResult(
                "meta_tags_missing_non_iid",
                "warning",
                f"Task defines a non-IID split but `data_tags={sorted(tags)}` lacks `Non-IID`.",
            )
        if "IID" in tags:
            yield CheckResult(
                "meta_tags_contradict_regime",
                "warning",
                f"`data_tags` claim `IID` but the task defines a {regime.replace('_non_iid', '')} split.",
            )
        extra = (tags & non_iid_tags) - {expected, "GroupedTemporal"}
        if extra:
            yield CheckResult(
                "meta_tags_multiple_regimes",
                "warning",
                f"`data_tags` carry {sorted(tags & non_iid_tags)} — only one split regime applies (here: {expected}).",
                hint="Tag the regime that the split actually uses; describe the other structure in "
                "`curation_comments`.",
            )


@_check
def _check_bibtex(ctx: _Ctx) -> Iterator[CheckResult]:
    """Lightweight BibTeX validation: it must parse, balance, and define the declared key(s)."""
    metadata = ctx.dataset_metadata
    bibtex = metadata.academic_reference_bibtex or ""
    declared = [k.strip() for k in (metadata.academic_reference_bibtex_key or "").split(",") if k.strip()]

    if not bibtex.strip():
        yield CheckResult("meta_bibtex_empty", "error", "`academic_reference_bibtex` is empty.")
        return

    n_open, n_close = bibtex.count("{"), bibtex.count("}")
    if n_open != n_close:
        yield CheckResult(
            "meta_bibtex_unbalanced_braces",
            "error",
            f"BibTeX has {n_open} '{{' but {n_close} '}}' — it will not compile.",
        )

    entries = re.findall(r"@(\w+)\s*\{\s*([^,\s}]+)\s*,", bibtex)
    if not entries:
        yield CheckResult(
            "meta_bibtex_no_entry",
            "error",
            "`academic_reference_bibtex` contains no `@type{key, ...}` entry.",
            hint="Paste a real BibTeX entry (the template ships `@` as a placeholder).",
        )
        return
    entry_keys = [key for _entry_type, key in entries]

    if not declared:
        yield CheckResult(
            "meta_bibtex_key_empty",
            "error",
            f"`academic_reference_bibtex_key` is empty; the BibTeX defines {entry_keys}.",
            hint="Set it to the citation key(s), comma-separated for multiple entries.",
        )
    else:
        unknown = [key for key in declared if key not in entry_keys]
        if unknown:
            yield CheckResult(
                "meta_bibtex_key_not_defined",
                "error",
                f"`academic_reference_bibtex_key` names {unknown} but the BibTeX defines {entry_keys}.",
            )
        if len(entry_keys) != len(declared):
            yield CheckResult(
                "meta_bibtex_key_count",
                "warning",
                f"BibTeX defines {len(entry_keys)} entry/entries {entry_keys} but "
                f"`academic_reference_bibtex_key` lists {len(declared)}: {declared}.",
                hint="List every key, comma-separated, so citing the dataset pulls in all entries.",
            )

    missing_fields = [
        f"{key}: {', '.join(sorted(missing))}"
        for entry_type, key, missing in _bibtex_missing_fields(bibtex, entries)
        if missing
    ]
    if missing_fields:
        yield CheckResult(
            "meta_bibtex_fields_missing",
            "info",
            f"BibTeX entries miss recommended fields — {'; '.join(missing_fields[:5])}.",
        )

    hazards = _latex_hazards(bibtex)
    if hazards:
        yield CheckResult(
            "meta_bibtex_latex_hazard",
            "warning",
            f"BibTeX contains characters LaTeX treats as markup outside of `\\url{{}}`: {hazards}.",
            hint="Escape them (`\\&`, `\\%`, `\\#`, `\\_`) or wrap the value in `\\url{...}` so the citation compiles.",
        )


def _bibtex_missing_fields(bibtex: str, entries: list[tuple[str, str]]) -> list[tuple[str, str, set[str]]]:
    """Return ``(entry_type, key, missing_recommended_fields)`` per BibTeX entry."""
    recommended = {"title", "year"}
    author_like = {"author", "editor", "howpublished", "organization", "publisher"}
    bodies = re.split(r"@\w+\s*\{", bibtex)[1:]
    out = []
    for (entry_type, key), body in zip(entries, bodies, strict=False):
        present = {m.lower() for m in re.findall(r"(\w+)\s*=", body)}
        missing = recommended - present
        if not (present & author_like):
            missing.add("author")
        out.append((entry_type, key, missing))
    return out


def _latex_hazards(text: str) -> list[str]:
    r"""Return the unescaped LaTeX special characters in the typeset parts of the BibTeX.

    Citation keys and URL-ish values (``\\url{}``, ``\\href{}``, ``doi``, ``url``, ...) are
    never typeset, so special characters there are harmless and are excluded.
    """
    stripped = re.sub(r"@\w+\s*\{[^,]*,", "", text)
    stripped = re.sub(r"\\(?:url|href)\{[^}]*\}", "", stripped)
    stripped = re.sub(r"\b(?:doi|url|eprint|isbn|issn|archiveprefix)\s*=\s*\{[^}]*\}", "", stripped, flags=re.I)
    hazards = []
    for char in ("&", "%", "#"):
        if re.search(rf"(?<!\\){re.escape(char)}", stripped):
            hazards.append(char)
    # `_` is only a hazard in text mode, i.e. outside $...$.
    without_math = re.sub(r"\$[^$]*\$", "", stripped)
    if re.search(r"(?<!\\)_", without_math):
        hazards.append("_")
    return hazards


@_check
def _check_dataset_metadata_completeness(ctx: _Ctx) -> Iterator[CheckResult]:
    """Provenance fields a consumer needs: license, link, year, download recipe, no placeholders."""
    metadata = ctx.dataset_metadata

    if metadata.license is None:
        yield CheckResult(
            "meta_license_unknown",
            "warning",
            "`license` is None (unknown or missing).",
            hint="Record the license if one exists — downstream users need it to redistribute the data.",
        )

    link = (metadata.original_dataset_source_download_link or "").strip()
    if not re.match(r"(https?://|doi:|10\.\d{4})", link):
        yield CheckResult(
            "meta_source_link",
            "warning",
            f"`original_dataset_source_download_link={link!r}` does not look like a URL or DOI.",
        )

    year = str(metadata.dataset_year).strip()
    if not re.fullmatch(r"(19|20)\d{2}", year):
        yield CheckResult(
            "meta_dataset_year",
            "warning",
            f"`dataset_year={metadata.dataset_year!r}` is not a plausible 4-digit year.",
        )

    if not (metadata.download_description or "").strip():
        yield CheckResult(
            "meta_download_description_empty",
            "warning",
            "`download_description` is empty — the raw download is not reproducible.",
        )

    if not (metadata.curation_comments or "").strip():
        yield CheckResult(
            "meta_curation_comments_empty",
            "info",
            "`curation_comments` is empty. Fine for a plain CSV read; otherwise document what you changed.",
        )

    if not (ctx.splits_metadata.splits_comment or "").strip():
        yield CheckResult(
            "meta_splits_comment_empty",
            "warning",
            "`splits_comment` is empty — the split protocol is undocumented.",
        )

    fields_to_scan = {
        "unique_name": metadata.unique_name,
        "download_description": metadata.download_description,
        "academic_reference_bibtex": metadata.academic_reference_bibtex,
        "academic_reference_bibtex_key": metadata.academic_reference_bibtex_key,
        "curation_comments": metadata.curation_comments,
        "version_comment": metadata.version_comment,
        "target_column_name": ctx.task.target_column_name,
        "objective_metric_name": ctx.task.objective_metric_name,
        "splits_comment": ctx.splits_metadata.splits_comment,
    }
    placeholders = {
        name: re.search(pattern, str(value)).group(0)  # type: ignore[union-attr]
        for name, value in fields_to_scan.items()
        if value
        for pattern in PLACEHOLDER_PATTERNS
        if re.search(pattern, str(value))
    }
    if placeholders:
        yield CheckResult(
            "meta_placeholder_left",
            "error",
            f"Scaffolding placeholders left in metadata: {placeholders}.",
            hint="Fill in the template TODOs before exporting.",
        )


# --- 5. Optional test dataset --------------------------------------------------------
@_check
def _check_test_dataset(ctx: _Ctx) -> Iterator[CheckResult]:
    """A shipped ``test_dataset`` must be schema-compatible with the main frame."""
    test_dataset = ctx.container.test_dataset
    if test_dataset is None or ctx.df is None:
        return

    missing = [c for c in ctx.df.columns if c not in test_dataset.columns]
    extra = [c for c in test_dataset.columns if c not in ctx.df.columns]
    if missing and missing != [ctx.target]:
        yield CheckResult(
            "test_dataset_missing_columns",
            "error",
            f"`test_dataset` is missing column(s) present in `dataset`: {missing[:5]}.",
            hint="Only the target column may be absent (unlabeled deployment data).",
        )
    if extra:
        yield CheckResult(
            "test_dataset_extra_columns",
            "error",
            f"`test_dataset` has column(s) absent from `dataset`: {extra[:5]}.",
        )

    mismatched = {
        column: (str(ctx.df[column].dtype), str(test_dataset[column].dtype))
        for column in ctx.df.columns
        if column in test_dataset.columns and str(ctx.df[column].dtype) != str(test_dataset[column].dtype)
    }
    if mismatched:
        yield CheckResult(
            "test_dataset_dtype_mismatch",
            "error",
            f"`test_dataset` dtypes differ from `dataset`: {dict(list(mismatched.items())[:5])}.",
            hint="Cast with `test[col] = test[col].astype(df[col].dtype)` so categories align.",
        )

    if not test_dataset.index.equals(pd.RangeIndex(start=0, stop=len(test_dataset))):
        yield CheckResult(
            "test_dataset_index_range",
            "warning",
            "`test_dataset` index is not a RangeIndex starting at 0.",
            hint="Call `reset_index(drop=True)`; the index is written to the parquet file.",
        )


# --- Runner --------------------------------------------------------------------------
def run_bundle_checks(
    container: CuratedContainer,
    *,
    ignore: Iterable[str] = (),
    heavy_cell_budget: int = DEFAULT_HEAVY_CELL_BUDGET,
    verbose: bool = True,
) -> BundleCheckReport:
    """Run every cross-referential check on a curated bundle.

    Call this after building the :class:`~data_foundry.curation_container.CuratedContainer`
    and before :meth:`~data_foundry.curation_container.CuratedContainer.save`, so a
    broken bundle never reaches the warehouse. See the module docstring for how this
    layer relates to the schema's ``__post_init__`` validation and to
    :func:`data_foundry.dataset_checks.run_all_checks`.

    Args:
        container: The bundle to check. Its ``dataset`` must be loaded.
        ignore: Check slugs to accept on purpose. Ignored findings are dropped from
            the report and listed in :attr:`BundleCheckReport.ignored`.
        heavy_cell_budget: Cell budget (``n_rows * n_cols``) above which O(rows x cols)
            checks (duplicate rows/columns) are skipped with an ``info`` finding.
        verbose: Print the report when done.

    Returns:
        The :class:`BundleCheckReport`. Call ``.raise_if_errors()`` to fail loudly.
    """
    ignored = tuple(dict.fromkeys(ignore))
    ctx = _Ctx(container=container, heavy_cell_budget=heavy_cell_budget)
    results: list[CheckResult] = []

    for check in _CHECKS:
        try:
            results.extend(check(ctx))
        except Exception as error:  # noqa: BLE001 - a broken check must not hide the other findings
            results.append(
                CheckResult(
                    "check_crashed",
                    "error",
                    f"Check `{check.__name__}` raised {type(error).__name__}: {error}",
                    hint="This is a bug in the check or an unexpected bundle shape — report it.",
                ),
            )

    results = [r for r in results if r.slug not in ignored]
    results.sort(key=lambda r: SEVERITY_ORDER[r.severity])
    report = BundleCheckReport(
        unique_name=container.dataset_metadata.unique_name,
        results=results,
        ignored=ignored,
        n_checks_run=len(_CHECKS),
    )
    if verbose:
        print(report.summary())
    return report


def verify_saved_container(
    path: Path | str,
    *,
    container: CuratedContainer | None = None,
    verbose: bool = True,
) -> BundleCheckReport:
    """Reload a saved bundle from disk and verify it round-tripped byte-for-byte.

    This is the one check that can only run *after* export: it re-reads the container
    directory and compares the reloaded artifact against the in-memory one — the file
    inventory, the recomputed checksum, every column dtype, the frame contents, and
    the three metadata objects.

    Args:
        path: The directory returned by :meth:`CuratedContainer.save`.
        container: The in-memory container that was saved. When omitted, only the
            self-consistency checks (files present, checksum recomputable) run.
        verbose: Print the report when done.

    Returns:
        A :class:`BundleCheckReport` with slugs prefixed ``export_``.
    """
    path = Path(path)
    results: list[CheckResult] = []
    unique_name = container.dataset_metadata.unique_name if container is not None else path.parent.name

    expected_files = [
        "dataset.parquet",
        "dtypes.json",
        "container_metadata.json",
        "dataset_metadata.dataset-mold-v1.json",
        "task_metadata.predictive-ml-task-mold-v1.json",
        "experiment_metadata.predictive-ml-splits-mold-v1.json",
    ]
    if container is not None and container.test_dataset is not None:
        expected_files += ["test_dataset.parquet", "test_dtypes.json"]
    missing_files = [name for name in expected_files if not (path / name).is_file()]
    if missing_files:
        results.append(
            CheckResult("export_files_missing", "error", f"Saved container is missing {missing_files}."),
        )
        report = BundleCheckReport(unique_name=unique_name, results=results, n_checks_run=1)
        if verbose:
            print(report.summary())
        return report

    has_test_dataset = container is not None and container.test_dataset is not None
    reloaded = CuratedContainer.load(path, load_dataset=True, load_test_data=has_test_dataset)

    recomputed = reloaded._create_checksum()
    if recomputed != reloaded.checksum:
        results.append(
            CheckResult(
                "export_checksum_mismatch",
                "error",
                f"Checksum recomputed from disk ({recomputed[:16]}…) differs from the stored one "
                f"({(reloaded.checksum or '')[:16]}…).",
                hint="The saved artifact does not match its own metadata — do not ship it. Usually a dtype that "
                "does not survive parquet (see `export_dtype_changed`).",
            ),
        )

    if container is not None:
        if reloaded.uuid != container.uuid:
            results.append(
                CheckResult("export_uuid_mismatch", "error", f"UUID changed: {container.uuid} -> {reloaded.uuid}."),
            )
        if path.name != container.uuid:
            results.append(
                CheckResult(
                    "export_path_layout",
                    "warning",
                    f"Save directory {path.name!r} is not the container UUID {container.uuid!r}.",
                ),
            )
        results.extend(_compare_frames(container.dataset, reloaded.dataset, label="dataset"))
        if container.test_dataset is not None and reloaded.test_dataset is not None:
            results.extend(_compare_frames(container.test_dataset, reloaded.test_dataset, label="test_dataset"))
        for name, before, after in (
            ("dataset_metadata", container.dataset_metadata, reloaded.dataset_metadata),
            ("task_metadata", container.task_metadata, reloaded.task_metadata),
            ("experiment_metadata", container.experiment_metadata, reloaded.experiment_metadata),
        ):
            if before != after:
                results.append(
                    CheckResult(
                        "export_metadata_changed",
                        "error",
                        f"`{name}` differs after the JSON round-trip.",
                        hint="A field type does not survive serialization; check the schema types.",
                    ),
                )

    results.sort(key=lambda r: SEVERITY_ORDER[r.severity])
    report = BundleCheckReport(unique_name=unique_name, results=results, n_checks_run=len(expected_files) + 4)
    if verbose:
        print(report.summary())
    return report


def _compare_frames(before: pd.DataFrame, after: pd.DataFrame, *, label: str) -> list[CheckResult]:
    """Compare an in-memory frame against its reloaded copy (shape, dtypes, values)."""
    results: list[CheckResult] = []
    if before.shape != after.shape:
        results.append(
            CheckResult("export_shape_changed", "error", f"`{label}` shape changed: {before.shape} -> {after.shape}."),
        )
        return results

    changed = {
        column: (str(before[column].dtype), str(after[column].dtype))
        for column in before.columns
        if str(before[column].dtype) != str(after[column].dtype)
    }
    if changed:
        results.append(
            CheckResult(
                "export_dtype_changed",
                "error",
                f"`{label}` dtypes changed on round-trip: {dict(list(changed.items())[:5])}.",
                hint="Parquet plus `dtypes.json` restoration could not reproduce the dtype. Use a dtype that "
                "survives (e.g. `datetime64[ns]` instead of a period, `category` with plain string categories).",
            ),
        )

    if not before.reset_index(drop=True).equals(after.reset_index(drop=True)):
        results.append(
            CheckResult(
                "export_values_changed",
                "error",
                f"`{label}` values differ after the save/load round-trip.",
                hint="Compare with `before.compare(after)` to find the offending column.",
            ),
        )
    return results
