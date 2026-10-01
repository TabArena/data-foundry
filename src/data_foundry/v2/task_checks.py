"""Cheap checks that every test fold can be scored and that the target varies, for every v2 task.

They complement the shared bundle checks, which look at the target as a whole (dtype, class count, rare classes):
a score is only defined, and only stable, when each test fold holds both classes in enough rows, or a target that
varies.

* ``splits_test_single_class`` (error): a classification test fold holds a single class, so ROC AUC is undefined.
* ``splits_test_minority_few`` (warning): a binary test fold holds fewer than :data:`MIN_TEST_MINORITY` rows of its
  rarer class, so its ROC AUC rests on a handful of rows.
* ``splits_test_class_missing`` (warning): a multiclass test fold lacks one or more classes.
* ``splits_test_target_constant`` (error): a regression test fold has a constant target, so R^2 is undefined and
  every model scores the same RMSE as the mean of that fold.
* ``task_target_value_dominant`` (warning): one value holds at least :data:`DOMINANT_VALUE_SHARE` of a regression
  target, as with a cap (censored values), a placeholder or a zero-inflated target.

The model-based questions (does any model beat a dummy, is the task solved, do the model families differ) are slow,
so they run on demand: ``scripts/v2/task_probes.py``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from data_foundry.bundle_checks import CheckResult

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
        return _classification_findings(target, folds, binary=task.problem_type == "binary_classification")
    return _regression_findings(pd.to_numeric(target, errors="coerce"), folds)


def _classification_findings(target: pd.Series, folds: list, *, binary: bool) -> list[CheckResult]:
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
        findings.append(
            CheckResult(
                "splits_test_single_class",
                "error",
                f"{len(single)} test fold(s) hold a single class, so ROC AUC is undefined there: {single[:5]}.",
                hint="Use fewer, larger test folds or windows, or stratify; a task this unbalanced may be too small.",
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
        findings.append(
            CheckResult(
                "splits_test_class_missing",
                "warning",
                f"{len(missing)} of {len(folds)} multiclass test fold(s) lack at least one class (most: "
                f"{max(n for _, n in missing)} of {n_classes} missing): {[name for name, _ in missing[:5]]}.",
                hint="Macro scores skip or break on the missing classes; merge rare classes or accept it with the "
                "class counts.",
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
