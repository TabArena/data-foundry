"""Tests for the cheap scorability checks of v2 tasks (``data_foundry.v2.task_checks``)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import DatasetMetadata, PredictiveMLSplitsMetadata, PredictiveMLTaskMetadataV2
from data_foundry.v2.task_checks import task_findings


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
            target_column_name="y", problem_type=problem_type, objective_metric_name="m"
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
