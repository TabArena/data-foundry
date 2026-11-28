"""Cheap checks that every test fold can be scored and that the target varies.

A score is only defined, and only stable, when each test fold holds the classes in enough rows, or a target that
varies. The class checks of the folds (:func:`fold_class_findings`) run in the bundle checks, for every container;
the rest (:func:`task_findings`) for every v2 task:

* ``splits_test_single_class``: a classification test fold holds a single class. An error under a metric that one class
  leaves undefined (:attr:`~data_foundry.metrics.MetricDef.one_class_undefined`: ROC AUC, average precision, a
  Gini, the early-detection utility), under a metric the registry does not hold (a local one, which cannot say), and
  when the fold's train side lacks that class or the fold no longer holds the task's problem type; a warning under any
  other registered metric, where few or no positives in a window are part of the task (SPLIT-16).
* ``splits_class_missing``: a class is missing from a fold, or too rare for the folds to spread: a multiclass test
  fold lacks a class, a train side lacks a class its test side holds, a fold holds too few classes to keep the task's
  problem type (binary or multiclass), or a class has fewer rows than the folds need. One finding for one cause (a
  rare class leaves a fold without it). An error when a train side lacks a test class, when a fold changes the problem
  type, or when a missing class leaves the metric undefined (a multiclass ROC AUC, and a metric the registry does not
  hold); a warning otherwise.
* ``splits_test_minority_few`` (warning): a binary test fold holds fewer than :data:`MIN_TEST_MINORITY` rows of its
  rarer class, so its ROC AUC rests on a handful of rows.
* ``splits_test_target_constant`` (error): a regression test fold has a constant target, so R^2 is undefined and
  every model scores the same RMSE as the mean of that fold.
* ``task_target_value_dominant`` (warning): one value holds at least :data:`DOMINANT_VALUE_SHARE` of a regression
  target, as with a cap (censored values), a placeholder or a zero-inflated target.

The model-based questions (does any model beat a dummy, is the task solved, do the model families differ) are slow,
so they run on demand: ``data-foundry probe task``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from data_foundry.checks.results import CheckResult
from data_foundry.metrics import METRICS

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer

MIN_TEST_MINORITY = 10
"""A binary test fold with fewer rows of its rarer class gives an unstable ROC AUC."""

DOMINANT_VALUE_SHARE = 0.5
"""A regression target with one value in at least this share of the rows is mostly that value."""


def task_findings(container: CuratedContainer) -> list[CheckResult]:
    """The findings of the module docstring for ``container``, but those of :func:`fold_class_findings`."""
    task = container.task_metadata
    target = container.dataset[task.target_column_name]
    folds = [
        (f"r{repeat}f{fold}", np.asarray(test, dtype=int))
        for repeat, by_fold in container.experiment_metadata.splits.items()
        for fold, (_train, test) in by_fold.items()
    ]
    if task.is_classification:
        return _minority_findings(target, folds) if task.problem_type == "binary_classification" else []
    return _regression_findings(pd.to_numeric(target, errors="coerce"), folds)


def one_class_undefined(metric: str | None) -> bool:
    """Whether a test fold of one class leaves ``metric`` undefined (SPLIT-16): the registry's
    :attr:`~data_foundry.metrics.MetricDef.one_class_undefined`; ROC AUC when no metric is named, and true for a
    metric the registry does not hold, which cannot say.
    """
    spec = METRICS.get(metric or "roc_auc")
    return spec is None or spec.one_class_undefined


def _minority_findings(target: pd.Series, folds: list) -> list[CheckResult]:
    codes, classes = pd.factorize(target, use_na_sentinel=True)
    few = []
    for name, test in folds:
        counts = np.bincount(codes[test][codes[test] >= 0], minlength=len(classes))
        if (counts > 0).sum() > 1 and counts.min() < MIN_TEST_MINORITY:  # a single class is splits_test_single_class
            few.append((name, int(counts.min())))
    if not few:
        return []
    smallest = min(n for _, n in few)
    return [
        CheckResult(
            "splits_test_minority_few",
            "warning",
            f"{len(few)} of {len(folds)} test fold(s) hold fewer than {MIN_TEST_MINORITY} rows of the rarer class "
            f"(smallest: {smallest}): {[name for name, _ in few[:5]]}.",
            hint="The score of such a fold rests on a handful of rows. Widen the test windows, or accept it when "
            "the folds together hold enough positives.",
        ),
    ]


def fold_class_findings(
    target: pd.Series,
    folds: list[tuple[str, np.ndarray, np.ndarray]],
    *,
    binary: bool,
    metric: str | None,
    min_rows: int,
) -> list[CheckResult]:
    """``splits_test_single_class`` and ``splits_class_missing`` (see the module docstring), one finding each.

    Args:
        target: The classification target.
        folds: ``(name, train positions, test positions)`` of every fold.
        binary: Whether the task is binary.
        metric: The metric's name, which decides whether a fold without a class can be scored.
        min_rows: A class with fewer rows is too rare to spread over the folds.
    """
    codes = (
        target.cat.codes.to_numpy()
        if isinstance(target.dtype, pd.CategoricalDtype)
        else pd.factorize(target.astype("string"), use_na_sentinel=True)[0]
    )
    n_classes = len(np.unique(codes[codes >= 0]))
    undefined = one_class_undefined(metric)
    single, missing = [], []  # (name, train lacks a test class, problem type changes[, classes missing from test])
    for name, train, test in folds:
        test_classes = np.unique(codes[test][codes[test] >= 0])
        train_classes = np.unique(codes[train][codes[train] >= 0])
        unseen = bool(np.setdiff1d(test_classes, train_classes).size)
        flips = (max(len(train_classes), len(test_classes)) <= 2) != (n_classes <= 2)
        if len(test_classes) <= 1:
            single.append((name, unseen, flips))
            continue
        absent = 0 if binary else n_classes - len(test_classes)
        if absent or unseen or flips:
            missing.append((name, unseen, flips, absent, len(train_classes), len(test_classes)))
    counts = target.value_counts(dropna=True)
    rare = counts[counts < min_rows]
    findings = []
    if single:
        findings.append(_single_class_finding(single, metric, undefined=undefined))
    if missing or len(rare):
        findings.append(
            _class_missing_finding(missing, rare, min_rows, len(folds), n_classes, metric, undefined=undefined)
        )
    return findings


def _single_class_finding(single: list, metric: str | None, *, undefined: bool) -> CheckResult:
    names = [name for name, *_ in single]
    unseen = [name for name, u, _ in single if u]
    flips = [name for name, _, f in single if f]
    message = (
        f"{len(single)} test fold(s) hold a single class, so "
        + (f"{metric or 'ROC AUC'} is undefined there" if undefined else f"{metric} scores them on one class")
        + f": {names[:5]}"
    )
    if unseen:
        message += f"; the train side of {len(unseen)} of them lacks that class: {unseen[:5]}"
    if flips:
        message += f"; {len(flips)} of them hold too few classes to keep the task's problem type: {flips[:5]}"
    hints = [
        "Widen the window or move its cut until every test fold holds both classes (SPLIT-16)."
        if undefined or unseen or flips
        else "Few or no positives in a window are part of the task (SPLIT-16); accept it with the counts."
    ]
    if flips:
        hints.append("TabArena asserts that every split has the same problem type as the task.")
    return CheckResult(
        "splits_test_single_class",
        "error" if undefined or unseen or flips else "warning",
        message + ".",
        hint=" ".join(hints),
    )


def _class_missing_finding(
    missing: list,
    rare: pd.Series,
    min_rows: int,
    n_folds: int,
    n_classes: int,
    metric: str | None,
    *,
    undefined: bool,
) -> CheckResult:
    absent = [(name, n) for name, _u, _f, n, *_ in missing if n]
    unseen = [name for name, u, *_ in missing if u]
    flips = [f"{name} ({max(n_train, n_test)} of {n_classes})" for name, _u, f, _n, n_train, n_test in missing if f]
    parts, hints = [], []
    if len(rare):
        formatted = ", ".join(f"{k}={int(v)}" for k, v in list(rare.items())[:5])
        parts.append(
            f"{len(rare)} class(es) have fewer than {min_rows} rows, too few to spread over the folds: {formatted}"
        )
        hints.append(
            "Rare classes break stratification and can leave a fold whose test set holds a class the train set never "
            "saw: keep a rare class of the source's labels when its rows carry about their share of the score, "
            "merge only by a convention of the field, else drop it."
        )
    if absent:
        parts.append(
            f"{len(absent)} of {n_folds} multiclass test fold(s) lack at least one class (most: "
            f"{max(n for _, n in absent)} of {n_classes} missing)"
            + (f", so {metric or 'ROC AUC'} is undefined there" if undefined else "")
            + f": {[name for name, _ in absent[:5]]}"
        )
        hints.append(
            "A per-class ROC AUC needs every class in every test fold: widen the windows, merge rare classes, or score "
            "by a metric that one class does not leave undefined."
            if undefined
            else "Macro scores skip or break on the missing classes; merge rare classes or accept it with the class "
            "counts."
        )
    if unseen:
        parts.append(f"{len(unseen)} fold(s) have a test class that never occurs in train: {unseen[:5]}")
        hints.append(
            "A model cannot predict a class it never saw, and probabilistic metrics break on the missing column."
        )
    if flips:
        parts.append(f"{len(flips)} fold(s) flip binary/multiclass relative to the full dataset: {flips[:5]}")
        hints.append("TabArena asserts that every split has the same problem type as the task.")
    error = bool(unseen or flips or (absent and undefined))
    message = "; ".join(parts)
    return CheckResult(
        "splits_class_missing",
        "error" if error else "warning",
        message[:1].upper() + message[1:] + ".",
        hint=" ".join(dict.fromkeys(hints)),
    )


def _regression_findings(target: pd.Series, folds: list) -> list[CheckResult]:
    values = target.to_numpy(dtype=float)
    findings = []
    constant = [name for name, test in folds if np.nanstd(values[test]) == 0]
    if constant:
        findings.append(
            CheckResult(
                "splits_test_target_constant",
                "error",
                f"{len(constant)} test fold(s) have a constant target, so R^2 is undefined there: {constant[:5]}.",
                hint="Check the target and the split: a fold of one repeated value cannot rank models.",
            ),
        )
    counts = target.value_counts(dropna=True, sort=False).sort_values(ascending=False, kind="stable")
    if len(counts) and counts.iloc[0] / counts.sum() >= DOMINANT_VALUE_SHARE:
        findings.append(
            CheckResult(
                "task_target_value_dominant",
                "warning",
                f"The target value {float(counts.index[0]):g} holds {counts.iloc[0] / counts.sum():.0%} of the rows.",
                hint="A cap (a censored value), a placeholder for missing, or a zero-inflated target: say which in "
                "`curation_comments`, drop censored or placeholder rows, or accept it with the reason.",
            ),
        )
    return findings
