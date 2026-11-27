"""Tests for the cheap scorability checks of the folds and the target (``data_foundry.checks.task``)."""

from __future__ import annotations

import inspect
import warnings

import numpy as np
import pandas as pd

from data_foundry.checks.task import fold_class_findings, one_class_undefined, task_findings
from data_foundry.curation_container import CuratedContainer
from data_foundry.metrics import METRICS
from data_foundry.schema import PredictiveMLSplitsMetadata, PredictiveMLTaskMetadataV2
from tests.helpers import make_spec, toy_dataset_metadata


def _container(y: list, splits: dict, problem_type: str) -> CuratedContainer:
    df = pd.DataFrame({"x": np.arange(len(y), dtype=float), "y": y})
    if problem_type != "regression":
        df["y"] = df["y"].astype("category")
    return CuratedContainer(
        dataset=df,
        dataset_metadata=toy_dataset_metadata(unique_name="toy", dataset_source="Other"),
        task_metadata=PredictiveMLTaskMetadataV2(
            target_column_name="y", problem_type=problem_type, objective_metric=make_spec(problem_type)
        ),
        experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="toy", splits=splits),
        uuid="u",
    )


def _slugs(container: CuratedContainer) -> dict[str, str]:
    """The findings of the task checks and of the fold class checks the bundle runs."""
    task = container.task_metadata
    found = task_findings(container)
    if task.is_classification:
        folds = [
            (f"r{r}f{f}", np.asarray(train), np.asarray(test))
            for r, by_fold in container.experiment_metadata.splits.items()
            for f, (train, test) in by_fold.items()
        ]
        binary = task.problem_type == "binary_classification"
        metric = task.objective_metric.name
        found += fold_class_findings(container.dataset["y"], folds, binary=binary, metric=metric, min_rows=5)
    return {r.slug: r.severity for r in found}


def _class_findings(target: pd.Series, train, test, *, binary: bool, metric: str) -> list[tuple[str, str]]:
    folds = [("r0f0", np.asarray(train), np.asarray(test))]
    return [(r.slug, r.severity) for r in fold_class_findings(target, folds, binary=binary, metric=metric, min_rows=5)]


def test_binary_folds_with_one_class_or_few_positives() -> None:
    y = [0] * 90 + [1] * 10
    one_class = {0: {0: (list(range(50, 100)), list(range(50)))}}
    assert _slugs(_container(y, one_class, "binary_classification")) == {"splits_test_single_class": "error"}
    few = {0: {0: (list(range(0, 100, 2)), list(range(1, 100, 2)))}}
    assert _slugs(_container(y, few, "binary_classification")) == {"splits_test_minority_few": "warning"}


def test_a_single_class_fold_is_an_error_only_under_a_metric_it_leaves_undefined() -> None:
    """SPLIT-16: one class cannot be ranked; other metrics score the fold, a warning."""
    target = pd.Series([0] * 90 + [1] * 10)
    train, test = np.arange(50, 100), np.arange(50)
    assert _class_findings(target, train, test, binary=True, metric="roc_auc") == [
        ("splits_test_single_class", "error")
    ]
    assert _class_findings(target, train, test, binary=True, metric="log_loss") == [
        ("splits_test_single_class", "warning")
    ]
    # a train side without the test fold's class is an error under any metric, in the same one finding
    assert _class_findings(target, np.arange(90, 100), test, binary=True, metric="log_loss") == [
        ("splits_test_single_class", "error")
    ]


def test_every_binary_metric_one_class_leaves_undefined_says_so() -> None:
    """SPLIT-16: a binary metric that scores an all-negative fold as NaN carries `one_class_undefined`, so a new metric
    of that kind cannot fall back to a warning; a metric the registry does not hold counts as undefined.
    """
    flagged = {name for name, spec in METRICS.items() if spec.one_class_undefined}
    rng = np.random.default_rng(0)
    p1 = rng.random(60)
    undefined = set()
    for name, spec in METRICS.items():
        if "binary_classification" not in spec.problem_types:
            continue
        args = inspect.signature(spec.fn).parameters
        pred = np.column_stack([1 - p1, p1]) if spec.prediction == "proba" else (p1 > 0.5).astype(int)
        kw = {"labels": np.array([0, 1])} if "labels" in args else {}
        if "group" in args:
            kw["group"] = np.repeat(np.arange(6), 10)
        if "order" in args:
            kw["order"] = np.tile(np.arange(10), 6)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                if "params" in args:  # the defaults; a metric that needs parameters without one is skipped
                    kw["params"] = (spec.check_params({}) if spec.check_params else None) or {}
                value = spec.fn(np.zeros(60, dtype=int), pred, **kw)
            except (TypeError, KeyError, ValueError):
                continue
        if not np.isfinite(value):
            undefined.add(name)
    assert undefined.issuperset({"roc_auc", "average_precision", "normalized_early_detection_utility"})
    assert undefined.issubset(flagged)
    assert one_class_undefined("a_local_metric")
    assert one_class_undefined(None)
    assert not one_class_undefined("log_loss")


def test_balanced_binary_folds_pass() -> None:
    y = [0, 1] * 50
    splits = {0: {0: (list(range(50)), list(range(50, 100)))}}
    assert _slugs(_container(y, splits, "binary_classification")) == {}


def test_multiclass_fold_missing_a_class() -> None:
    y = [0] * 40 + [1] * 40 + [2] * 20
    test = list(range(10)) + list(range(40, 50))
    missing = {0: {0: ([i for i in range(100) if i not in test], test)}}
    assert _slugs(_container(y, missing, "multiclass_classification")) == {"splits_class_missing": "warning"}


def test_one_cause_of_a_fold_without_classes_is_one_finding() -> None:
    """A test fold of classes 0 and 1 over a train side of 0 and 2: class 2 missing from the test side, class 1 from
    the train side, and two classes on each side, so the fold is binary: one error, which says all three.
    """
    y = [0] * 40 + [1] * 40 + [2] * 20
    splits = {0: {0: (list(range(80, 100)) + list(range(30)), list(range(40, 80)) + list(range(30, 40)))}}
    container = _container(y, splits, "multiclass_classification")
    assert _slugs(container) == {"splits_class_missing": "error"}
    folds = [("r0f0", np.asarray(splits[0][0][0]), np.asarray(splits[0][0][1]))]
    (found,) = fold_class_findings(container.dataset["y"], folds, binary=False, metric="log_loss", min_rows=5)
    assert "lack at least one class" in found.message
    assert "never occurs in train" in found.message
    assert "flip binary/multiclass" in found.message


def test_a_single_class_test_fold_is_one_finding() -> None:
    """A single-class test fold whose class the train side lacks, in a fold that holds two classes of three: one
    `splits_test_single_class` error, not three findings.
    """
    y = pd.Series([0] * 40 + [1] * 40 + [2] * 20)
    assert _class_findings(y, np.arange(40, 80), np.arange(20), binary=False, metric="log_loss") == [
        ("splits_test_single_class", "error")
    ]


def test_a_rare_class_and_the_folds_it_leaves_without_it_are_one_finding() -> None:
    y = pd.Series([0] * 50 + [1] * 47 + [2] * 3)
    train, test = np.arange(100), np.r_[0:25, 50:75]
    found = fold_class_findings(y, [("r0f0", train, test)], binary=False, metric="log_loss", min_rows=5)
    assert [(r.slug, r.severity) for r in found] == [("splits_class_missing", "warning")]
    assert "fewer than 5 rows" in found[0].message
    assert "lack at least one class" in found[0].message


def test_regression_constant_fold_and_dominant_value() -> None:
    y = [0.0] * 60 + list(np.linspace(1, 2, 40))
    splits = {0: {0: (list(range(30, 100)), list(range(30)))}}
    assert _slugs(_container(y, splits, "regression")) == {
        "splits_test_target_constant": "error",
        "task_target_value_dominant": "warning",
    }


def test_a_missing_class_is_an_error_under_a_multiclass_auc() -> None:
    """A multiclass ROC AUC is NaN on a test fold without one of the classes, so the fold cannot be scored; a metric
    that scores it (log loss) keeps the warning.
    """
    target = pd.Series([0] * 40 + [1] * 40 + [2] * 20)
    for metric, severity in [("roc_auc_ovr_macro", "error"), ("roc_auc_ovo_macro", "error"), ("log_loss", "warning")]:
        found = _class_findings(target, np.arange(100), np.arange(80), binary=False, metric=metric)
        assert found == [("splits_class_missing", severity)]
