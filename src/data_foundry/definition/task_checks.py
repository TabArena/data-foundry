"""Cheap checks that every test fold can be scored and that the target varies, for every v2 task.

They complement the shared bundle checks, which look at the target as a whole (dtype, class count, rare classes):
a score is only defined, and only stable, when each test fold holds both classes in enough rows, or a target that
varies.

* ``splits_test_single_class``: a classification test fold holds a single class. An error under a metric that one class
  leaves undefined (:attr:`~data_foundry.metrics.MetricDef.one_class_undefined`: ROC AUC, average precision, a
  Gini, the early-detection utility) and under a metric the registry does not hold (a local one, which cannot say);
  a warning under any other registered metric, where few or no positives in a window are part of the task (SPLIT-16).
* ``splits_test_minority_few`` (warning): a binary test fold holds fewer than :data:`MIN_TEST_MINORITY` rows of its
  rarer class, so its ROC AUC rests on a handful of rows.
* ``splits_test_class_missing``: a multiclass test fold lacks one or more classes. An error under a metric that one
  class leaves undefined (a multiclass ROC AUC, NaN on such a fold) and under a metric the registry does not hold; a
  warning under any other.
* ``splits_test_target_constant`` (error): a regression test fold has a constant target, so R^2 is undefined and
  every model scores the same RMSE as the mean of that fold.
* ``task_target_value_dominant`` (warning): one value holds at least :data:`DOMINANT_VALUE_SHARE` of a regression
  target, as with a cap (censored values), a placeholder or a zero-inflated target.

The model-based questions (does any model beat a dummy, is the task solved, do the model families differ) are slow,
so they run on demand: ``.claude/skills/knowledge-data-foundry/scripts/task_probes.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from data_foundry.bundle_checks import CheckResult
from data_foundry.metrics import METRICS

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer

MIN_TEST_MINORITY = 10
"""A binary test fold with fewer rows of its rarer class gives an unstable ROC AUC."""

DOMINANT_VALUE_SHARE = 0.5
"""A regression target with one value in at least this share of the rows is mostly that value."""


def task_findings(container: CuratedContainer) -> list[CheckResult]:
    """The findings of the module docstring for ``container``."""
    task = container.task_metadata
    target = container.dataset[task.target_column_name]
    folds = [
        (f"r{repeat}f{fold}", np.asarray(test, dtype=int))
        for repeat, by_fold in container.experiment_metadata.splits.items()
        for fold, (_train, test) in by_fold.items()
    ]
    if task.is_classification:
        metric = getattr(task.objective_metric, "name", None)
        return _classification_findings(
            target, folds, binary=task.problem_type == "binary_classification", metric=metric
        )
    return _regression_findings(pd.to_numeric(target, errors="coerce"), folds)


def one_class_undefined(metric: str | None) -> bool:
    """Whether a test fold of one class leaves ``metric`` undefined (SPLIT-16): the registry's
    :attr:`~data_foundry.metrics.MetricDef.one_class_undefined`; ROC AUC when no metric is named, and true for a
    metric the registry does not hold, which cannot say.
    """
    spec = METRICS.get(metric or "roc_auc")
    return spec is None or spec.one_class_undefined


def _classification_findings(
    target: pd.Series, folds: list, *, binary: bool, metric: str | None = None
) -> list[CheckResult]:
    codes, classes = pd.factorize(target, use_na_sentinel=True)
    n_classes = len(classes)
    single, few, missing = [], [], []
    for name, test in folds:
        counts = np.bincount(codes[test][codes[test] >= 0], minlength=n_classes)
        present = int((counts > 0).sum())
        if present <= 1:
            single.append(name)
        elif binary and counts.min() < MIN_TEST_MINORITY:
            few.append((name, int(counts.min())))
        elif not binary and present < n_classes:
            missing.append((name, n_classes - present))
    findings = []
    if single:
        undefined = one_class_undefined(metric)
        findings.append(
            CheckResult(
                "splits_test_single_class",
                "error" if undefined else "warning",
                f"{len(single)} test fold(s) hold a single class, so "
                + (f"{metric or 'ROC AUC'} is undefined there" if undefined else f"{metric} scores them on one class")
                + f": {single[:5]}.",
                hint=(
                    "Widen the window or move its cut until every test fold holds both classes (SPLIT-16)."
                    if undefined
                    else "Few or no positives in a window are part of the task (SPLIT-16); accept it with the counts."
                ),
            ),
        )
    if few:
        smallest = min(n for _, n in few)
        findings.append(
            CheckResult(
                "splits_test_minority_few",
                "warning",
                f"{len(few)} of {len(folds)} test fold(s) hold fewer than {MIN_TEST_MINORITY} rows of the rarer class "
                f"(smallest: {smallest}): {[name for name, _ in few[:5]]}.",
                hint="The score of such a fold rests on a handful of rows. Widen the test windows, or accept it when "
                "the folds together hold enough positives.",
            ),
        )
    if missing:
        undefined = one_class_undefined(metric)
        findings.append(
            CheckResult(
                "splits_test_class_missing",
                "error" if undefined else "warning",
                f"{len(missing)} of {len(folds)} multiclass test fold(s) lack at least one class (most: "
                f"{max(n for _, n in missing)} of {n_classes} missing)"
                + (f", so {metric or 'ROC AUC'} is undefined there" if undefined else "")
                + f": {[name for name, _ in missing[:5]]}.",
                hint=(
                    "A per-class ROC AUC needs every class in every test fold: widen the windows, merge rare classes, "
                    "or score by a metric that one class does not leave undefined."
                    if undefined
                    else "Macro scores skip or break on the missing classes; merge rare classes or accept it with the "
                    "class counts."
                ),
            ),
        )
    return findings


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
