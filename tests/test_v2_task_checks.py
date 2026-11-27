"""Tests for the cheap scorability checks of v2 tasks (``data_foundry.definition.task_checks``)."""

from __future__ import annotations

import inspect
import warnings

import numpy as np
import pandas as pd

from data_foundry.curation_container import CuratedContainer
from data_foundry.definition.task_checks import _classification_findings, one_class_undefined, task_findings
from data_foundry.metrics import METRICS
from data_foundry.schema import PredictiveMLSplitsMetadata, PredictiveMLTaskMetadataV2
from data_foundry.v1 import DatasetMetadata
from tests.test_bundle_checks import make_spec


def _container(y: list, splits: dict, problem_type: str) -> CuratedContainer:
    df = pd.DataFrame({"x": np.arange(len(y), dtype=float), "y": y})
    if problem_type != "regression":
        df["y"] = df["y"].astype("category")
    return CuratedContainer(
        dataset=df,
        dataset_metadata=DatasetMetadata(
            unique_name="toy",
            dataset_year="2025",
            domain_str="finance",
            dataset_source="Other",
            original_dataset_source_download_link="http://example",
            download_description="d",
            academic_reference_bibtex="b",
            academic_reference_bibtex_key="k",
            license=None,
            data_tags=["IID"],
            curation_comments=None,
        ),
        task_metadata=PredictiveMLTaskMetadataV2(
            target_column_name="y", problem_type=problem_type, objective_metric=make_spec(problem_type)
        ),
        experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="toy", splits=splits),
        uuid="u",
    )


def _slugs(container: CuratedContainer) -> dict[str, str]:
    return {r.slug: r.severity for r in task_findings(container)}


def test_binary_folds_with_one_class_or_few_positives() -> None:
    y = [0] * 90 + [1] * 10
    one_class = {0: {0: (list(range(50, 100)), list(range(50)))}}
    assert _slugs(_container(y, one_class, "binary_classification")) == {"splits_test_single_class": "error"}
    few = {0: {0: (list(range(0, 100, 2)), list(range(1, 100, 2)))}}
    assert _slugs(_container(y, few, "binary_classification")) == {"splits_test_minority_few": "warning"}


def test_a_single_class_fold_is_an_error_only_under_a_metric_it_leaves_undefined() -> None:
    """SPLIT-16: one class cannot be ranked; other metrics score the fold, a warning."""
    from data_foundry.definition.task_checks import _classification_findings

    target = pd.Series([0] * 90 + [1] * 10)
    folds = [("r0f0", np.arange(50))]
    assert [(r.slug, r.severity) for r in _classification_findings(target, folds, binary=True, metric="roc_auc")] == [
        ("splits_test_single_class", "error")
    ]
    assert [(r.slug, r.severity) for r in _classification_findings(target, folds, binary=True, metric="log_loss")] == [
        ("splits_test_single_class", "warning")
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
    splits = {0: {0: (list(range(80, 100)) + list(range(40)), list(range(40, 80)) + list(range(30, 40)))}}
    assert _slugs(_container(y, splits, "multiclass_classification")) == {"splits_test_class_missing": "warning"}


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
    folds = [("r0f0", np.arange(80))]
    for metric, severity in [("roc_auc_ovr_macro", "error"), ("roc_auc_ovo_macro", "error"), ("log_loss", "warning")]:
        found = _classification_findings(target, folds, binary=False, metric=metric)
        assert [(r.slug, r.severity) for r in found] == [("splits_test_class_missing", severity)]
